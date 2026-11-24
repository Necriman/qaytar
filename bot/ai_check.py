"""Document reading with Google Gemini + comparison logic.

Privacy: image bytes live only in memory for the duration of one request.
Extracted fields are kept in an in-memory session store with a 30-minute TTL.
Nothing here touches the disk or the database.
"""
import html
import json
import logging
import re
import time

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from config import GEMINI_API_KEY, GEMINI_MODEL

log = logging.getLogger(__name__)

SESSION_TTL = 30 * 60
_sessions: dict[int, dict] = {}  # user_id -> {"started": ts, "docs": [DocInfo dicts]}

_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def ai_enabled() -> bool:
    return _client is not None


class DocInfo(BaseModel):
    doc_type: str = Field(
        description="One of: contract, payment_receipt, bank_statement, mortgage_statement, "
        "passport_or_id, bank_card, other"
    )
    readable: bool = Field(description="False if the image is too blurry or is not a document")
    payer_name: str | None = Field(None, description="Full name of the person who pays / customer (buyurtmachi / заказчик / sender of payment)")
    student_name: str | None = Field(None, description="Full name of the student/child/borrower, if present")
    institution: str | None = Field(None, description="University, school, kindergarten or bank name")
    amount: float | None = Field(None, description="Amount in UZS shown on the document (contract total or payment amount)")
    payment_date: str | None = Field(None, description="Date in YYYY-MM-DD if visible")
    year: int | None = Field(None, description="Year of the payment or contract")


PROMPT = (
    "You check documents for an income-tax refund in Uzbekistan (12% refund for university contract, "
    "private kindergarten/school, or mortgage payments). Read the image and fill the fields. "
    "Documents may be in Uzbek (Latin or Cyrillic), Russian or English. "
    "If the image shows a passport, ID card or bank card, set doc_type accordingly and leave all names and numbers empty. "
    "Never output passport numbers, PINFL/JShShIR, or card numbers. Amounts must be plain numbers in UZS."
)


async def read_document(data: bytes, mime_type: str) -> DocInfo | None:
    if not _client:
        return None
    try:
        resp = await _client.aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=[types.Part.from_bytes(data=data, mime_type=mime_type), PROMPT],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DocInfo,
                temperature=0,
            ),
        )
        if getattr(resp, "parsed", None):
            return resp.parsed
        return DocInfo(**json.loads(resp.text))
    except Exception:  # network, quota, safety block, bad JSON
        log.exception("Gemini read failed")
        return None
    finally:
        del data  # drop our reference to the image bytes


# ---------- in-memory session store ----------

def session_start(user_id: int) -> None:
    _sessions[user_id] = {"started": time.time(), "docs": []}


def session_add(user_id: int, doc: DocInfo) -> None:
    s = _sessions.setdefault(user_id, {"started": time.time(), "docs": []})
    s["docs"].append(doc.model_dump())


def session_pop(user_id: int) -> list[dict]:
    s = _sessions.pop(user_id, None)
    return s["docs"] if s else []


def purge_expired() -> int:
    now = time.time()
    expired = [uid for uid, s in _sessions.items() if now - s["started"] > SESSION_TTL]
    for uid in expired:
        _sessions.pop(uid, None)
    return len(expired)


# ---------- comparison ----------

_CYR = dict(zip(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяўқғҳ",
    ["a", "b", "v", "g", "d", "e", "yo", "j", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t",
     "u", "f", "x", "ts", "ch", "sh", "sh", "", "i", "", "e", "yu", "ya", "o", "q", "g", "h"],
))


def _name_tokens(name: str | None) -> set[str]:
    if not name:
        return set()
    s = "".join(_CYR.get(ch, ch) for ch in name.lower())
    s = s.replace("‘", "").replace("’", "").replace("'", "").replace("`", "")
    for a, b in (("kh", "x"), ("iy", "i"), ("yo", "o"), ("ye", "e"), ("ya", "a"), ("yu", "u"), ("q", "k"), ("w", "v")):
        s = s.replace(a, b)
    tokens = re.findall(r"[a-z]{2,}", s)
    stop = {"ogli", "qizi", "ugli", "kizi", "ovich", "evich", "ovna", "evna"}
    return {tok[:5] for tok in tokens if tok not in stop}  # first 5 letters tolerate endings (-ov/-ova)


def names_match(a: str | None, b: str | None) -> bool | None:
    ta, tb = _name_tokens(a), _name_tokens(b)
    if not ta or not tb:
        return None
    need = min(2, len(ta), len(tb))
    return len(ta & tb) >= need


DOC_LABELS = {
    "contract": {"uz": "Shartnoma", "ru": "Договор"},
    "payment_receipt": {"uz": "To'lov cheki", "ru": "Чек об оплате"},
    "bank_statement": {"uz": "Bank ko'chirmasi", "ru": "Банковская выписка"},
    "mortgage_statement": {"uz": "Ipoteka ma'lumotnomasi", "ru": "Справка по ипотеке"},
    "other": {"uz": "Boshqa hujjat", "ru": "Другой документ"},
}

PAYMENT_TYPES = {"payment_receipt", "bank_statement", "mortgage_statement"}


def describe(doc: DocInfo, lang: str) -> tuple[str, str]:
    from calc import fmt_sum

    label = DOC_LABELS.get(doc.doc_type, DOC_LABELS["other"])[lang]
    lines = []
    L = {
        "uz": ("To'lovchi", "O'quvchi/qarz oluvchi", "Tashkilot", "Summa", "Sana"),
        "ru": ("Плательщик", "Учащийся/заёмщик", "Организация", "Сумма", "Дата"),
    }[lang]
    if doc.payer_name:
        lines.append(f"👤 {L[0]}: {html.escape(doc.payer_name)}")
    if doc.student_name:
        lines.append(f"🎓 {L[1]}: {html.escape(doc.student_name)}")
    if doc.institution:
        lines.append(f"🏛 {L[2]}: {html.escape(doc.institution)}")
    if doc.amount:
        lines.append(f"💵 {L[3]}: {fmt_sum(doc.amount)}")
    if doc.payment_date or doc.year:
        lines.append(f"📅 {L[4]}: {html.escape(str(doc.payment_date or doc.year))}")
    return label, "\n".join(lines)


def build_report(docs: list[dict], lang: str, tax_year: int) -> tuple[list[str], int]:
    """Return (issues, total_paid)."""
    from calc import fmt_sum

    ru = lang == "ru"
    issues: list[str] = []
    contracts = [d for d in docs if d["doc_type"] == "contract"]
    payments = [d for d in docs if d["doc_type"] in PAYMENT_TYPES]

    if not contracts:
        issues.append("❗ Договор не найден. Пришлите первую страницу договора." if ru
                      else "❗ Shartnoma topilmadi. Shartnomaning birinchi sahifasini yuboring.")
    if not payments:
        issues.append("❗ Нет платёжных документов (чеков или выписки)." if ru
                      else "❗ To'lov hujjatlari (chek yoki ko'chirma) yo'q.")

    main_payer = next((c["payer_name"] for c in contracts if c.get("payer_name")), None)
    if main_payer:
        for p in payments:
            if names_match(main_payer, p.get("payer_name")) is False:
                pn, mp = html.escape(p["payer_name"]), html.escape(main_payer)
                issues.append(
                    (f"❗ Плательщик в чеке (<b>{pn}</b>) не совпадает с плательщиком по договору "
                     f"(<b>{mp}</b>). Обычно вернуть налог может только тот, кто реально платил.")
                    if ru else
                    (f"❗ Chekdagi to'lovchi (<b>{pn}</b>) shartnomadagi to'lovchiga (<b>{mp}</b>) "
                     f"mos emas. Odatda soliqni faqat haqiqatda to'lagan odam qaytaradi.")
                )

    years = {p.get("year") or (int(p["payment_date"][:4]) if p.get("payment_date") and p["payment_date"][:4].isdigit() else None)
             for p in payments}
    years.discard(None)
    if len(years) > 1:
        ys = ", ".join(str(y) for y in sorted(years))
        issues.append(f"❗ Платежи за разные годы ({ys}). На каждый год — отдельная декларация." if ru
                      else f"❗ To'lovlar turli yillarda ({ys}). Har bir yil uchun alohida deklaratsiya topshiriladi.")
    elif years and tax_year not in years:
        y = next(iter(years))
        issues.append(f"ℹ️ Платежи за {y} год. Проверьте, что подаёте декларацию именно за {y} год." if ru
                      else f"ℹ️ To'lovlar {y}-yilga tegishli. Deklaratsiyani aynan {y}-yil uchun topshiring.")

    total_paid = int(sum(p.get("amount") or 0 for p in payments))
    contract_sum = next((c["amount"] for c in contracts if c.get("amount")), None)
    if contract_sum and total_paid and total_paid > contract_sum * 1.05:
        issues.append(
            f"ℹ️ Сумма чеков ({fmt_sum(total_paid)}) больше суммы договора ({fmt_sum(contract_sum)}). Проверьте, нет ли лишних чеков." if ru
            else f"ℹ️ Cheklar summasi ({fmt_sum(total_paid)}) shartnoma summasidan ({fmt_sum(contract_sum)}) katta. Ortiqcha chek yo'qligini tekshiring."
        )
    return issues, total_paid
