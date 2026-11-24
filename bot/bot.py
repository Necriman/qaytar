"""Qaytar — Telegram bot that helps get back 12% income tax (contract, school, mortgage).

Run:  python bot.py
"""
import asyncio
import html
import io
import logging
import re
from datetime import datetime, timedelta, timezone

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    LinkPreviewOptions,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import ai_check
import config
import db
import stickers
from calc import calc_refund, fmt_sum, parse_sum, tax_season
from texts import ARTICLES, T, t

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("qaytar")

router = Router()
TASHKENT = timezone(timedelta(hours=5))
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


# ====================== states ======================
class Check(StatesGroup):
    kind = State()
    who = State()
    age = State()
    employed = State()
    paid = State()
    salary = State()


class Docs(StatesGroup):
    choose = State()
    ai_consent = State()
    upload = State()
    manual = State()


class Booking(StatesGroup):
    consent = State()
    name = State()
    phone = State()
    fmt = State()
    receipt = State()


# ====================== helpers ======================
async def lang_of(user_id: int) -> str:
    return await db.get_lang(user_id) or "uz"


def both(key: str) -> set[str]:
    return {T[key]["uz"], T[key]["ru"]}


def ik(rows: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=txt, callback_data=cb) for txt, cb in row] for row in rows]
    )


def main_menu(lang: str) -> ReplyKeyboardMarkup:
    b = lambda k: KeyboardButton(text=t(k, lang))  # noqa: E731
    return ReplyKeyboardMarkup(
        keyboard=[
            [b("btn_check")],
            [b("btn_docs"), b("btn_guide")],
            [b("btn_book"), b("btn_articles")],
            [b("btn_remind"), b("btn_privacy")],
            [b("btn_lang")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Qaytar 🛡",
    )


def cancel_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t("cancel", lang))]], resize_keyboard=True)


async def say(message: Message, text: str, effect: str | None = None, **kwargs) -> Message:
    """Send HTML text; try a message effect, silently fall back without it."""
    kwargs.setdefault("link_preview_options", NO_PREVIEW)
    if effect and message.chat.type == "private":
        try:
            return await message.answer(text, message_effect_id=effect, **kwargs)
        except TelegramBadRequest:
            pass
    return await message.answer(text, **kwargs)


LANG_KB = ik([[("🇺🇿 O'zbekcha", "lang:uz"), ("🇷🇺 Русский", "lang:ru")]])


async def ask_language(message: Message) -> None:
    await stickers.send(message, "lang")
    await message.answer(t("choose_lang", "uz"), reply_markup=LANG_KB)


def links(lang: str) -> dict:
    return {"privacy": config.PRIVACY_URL, "terms": config.TERMS_URL}


async def notify_admins(bot: Bot, text: str, **kwargs) -> None:
    for admin_id in config.ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text, **kwargs)
        except Exception:
            log.exception("Cannot notify admin %s", admin_id)


# ====================== start / language ======================
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await db.ensure_user(message.from_user.id)
    lang = await db.get_lang(message.from_user.id)
    if not lang or lang not in ("uz", "ru"):
        await ask_language(message)
        return
    await send_welcome(message, lang)


async def send_welcome(message: Message, lang: str):
    await stickers.send(message, "welcome")
    await say(message, t("welcome", lang), effect=config.EFFECT_FIRE, reply_markup=main_menu(lang))


@router.message(Command("lang"))
@router.message(F.text.in_(both("btn_lang")))
async def cmd_lang(message: Message, state: FSMContext):
    await state.clear()
    await ask_language(message)


@router.callback_query(F.data.startswith("lang:"))
async def cb_lang(call: CallbackQuery):
    lang = call.data.split(":")[1]
    await db.set_lang(call.from_user.id, lang)
    await call.answer("🇺🇿 O'zbek tili tanlandi" if lang == "uz" else "🇷🇺 Выбран русский язык")
    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass
    await send_welcome(call.message, lang)


@router.message(Command("cancel"))
@router.message(F.text.in_(both("cancel")))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    ai_check.session_pop(message.from_user.id)
    lang = await lang_of(message.from_user.id)
    await message.answer(t("cancelled", lang), reply_markup=main_menu(lang))


# ====================== eligibility check ======================
@router.message(Command("check"))
@router.message(F.text.in_(both("btn_check")))
async def check_start(message: Message, state: FSMContext, uid: int | None = None):
    await state.clear()
    uid = uid or message.from_user.id
    lang = await lang_of(uid)
    if not await db.has_consent(uid):
        await say(
            message,
            t("consent_basic", lang, **links(lang)),
            reply_markup=ik([[(t("btn_agree", lang), "consent:yes"), (t("btn_disagree", lang), "consent:no")]]),
        )
        return
    await ask_kind(message, state, lang)


@router.callback_query(F.data.startswith("consent:"))
async def cb_consent(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data.endswith("yes"):
        await db.set_consent(call.from_user.id)
        await ask_kind(call.message, state, lang)
    else:
        await call.message.answer(t("consent_declined", lang), reply_markup=main_menu(lang))


async def ask_kind(message: Message, state: FSMContext, lang: str):
    await state.set_state(Check.kind)
    await stickers.send(message, "check")
    await message.answer("👇", reply_markup=cancel_kb(lang))
    await message.answer(
        t("q_kind", lang),
        reply_markup=ik([
            [(t("kind_uni", lang), "kind:uni")],
            [(t("kind_school", lang), "kind:school")],
            [(t("kind_mortgage", lang), "kind:mortgage")],
        ]),
    )


@router.callback_query(Check.kind, F.data.startswith("kind:"))
async def cb_kind(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    kind = call.data.split(":")[1]
    await state.update_data(kind=kind)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    if kind == "uni":
        await state.set_state(Check.who)
        await call.message.answer(
            t("q_who", lang),
            reply_markup=ik([
                [(t("who_self", lang), "who:self")],
                [(t("who_child", lang), "who:child"), (t("who_spouse", lang), "who:spouse")],
            ]),
        )
    else:
        await ask_employed(call.message, state, lang)


@router.callback_query(Check.who, F.data.startswith("who:"))
async def cb_who(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    who = call.data.split(":")[1]
    await state.update_data(who=who)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    if who == "self":
        await ask_employed(call.message, state, lang)
    else:
        await state.set_state(Check.age)
        await call.message.answer(
            t("q_age", lang), reply_markup=ik([[(t("yes", lang), "age:yes"), (t("no", lang), "age:no")]])
        )


@router.callback_query(Check.age, F.data.startswith("age:"))
async def cb_age(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data.endswith("no"):
        await state.clear()
        await stickers.send(call.message, "sad")
        await call.message.answer(t("not_eligible_age", lang), reply_markup=main_menu(lang))
        return
    await ask_employed(call.message, state, lang)


async def ask_employed(message: Message, state: FSMContext, lang: str):
    await state.set_state(Check.employed)
    await message.answer(
        t("q_employed", lang),
        reply_markup=ik([
            [(t("yes", lang), "emp:yes"), (t("no", lang), "emp:no")],
            [(t("dont_know", lang), "emp:unknown")],
        ]),
    )


@router.callback_query(Check.employed, F.data.startswith("emp:"))
async def cb_employed(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    answer = call.data.split(":")[1]
    if answer == "no":
        data = await state.get_data()
        await db.add_check(call.from_user.id, data.get("kind", "?"), 0, 0)
        await state.clear()
        await stickers.send(call.message, "sad")
        await call.message.answer(t("not_eligible_employed", lang), reply_markup=main_menu(lang))
        return
    if answer == "unknown":
        await call.message.answer(t("employed_unknown", lang))
    await state.set_state(Check.paid)
    await call.message.answer(t("q_paid", lang))


@router.message(Check.paid, F.text)
async def msg_paid(message: Message, state: FSMContext):
    lang = await lang_of(message.from_user.id)
    value = parse_sum(message.text)
    if not value or value < 10_000:
        await message.answer(t("bad_number", lang))
        return
    await state.update_data(paid=value)
    await state.set_state(Check.salary)
    await message.answer(t("q_salary", lang))


@router.message(Check.salary, F.text)
async def msg_salary(message: Message, state: FSMContext):
    lang = await lang_of(message.from_user.id)
    salary = parse_sum(message.text)
    if not salary or salary < 10_000:
        await message.answer(t("bad_number", lang))
        return
    data = await state.get_data()
    await state.clear()
    res = calc_refund(data["paid"], salary)
    year, deadline = tax_season()
    await db.add_check(message.from_user.id, data.get("kind", "?"), data["paid"], res.refund)

    text = t(
        "result",
        lang,
        refund=fmt_sum(res.refund),
        paid=fmt_sum(data["paid"]),
        by_expense=fmt_sum(res.by_expense),
        by_tax=fmt_sum(res.by_tax_paid),
        limit_note=t("limit_note", lang) if res.limited_by_salary else "",
        year=year,
        deadline=deadline.strftime("%d.%m.%Y"),
    )
    if data.get("kind") == "mortgage":
        text = text.replace("\n\n<i>⚠️", t("mortgage_note", lang) + "\n<i>⚠️", 1)
    await stickers.send(message, "result")
    await say(message, text, effect=config.EFFECT_PARTY, reply_markup=main_menu(lang))
    await message.answer(
        "👇",
        reply_markup=ik([
            [(t("btn_docs", lang), "go:docs")],
            [(t("btn_guide", lang), "go:guide"), (t("btn_book", lang), "go:book")],
        ]),
    )


@router.callback_query(F.data.startswith("go:"))
async def cb_go(call: CallbackQuery, state: FSMContext):
    await call.answer()
    target = call.data.split(":")[1]
    uid = call.from_user.id
    if target == "docs":
        await docs_start(call.message, state, uid=uid)
    elif target == "guide":
        await guide_start(call.message, state, uid=uid)
    elif target == "book":
        await book_start(call.message, state, uid=uid)


# ====================== documents ======================
@router.message(Command("docs"))
@router.message(F.text.in_(both("btn_docs")))
async def docs_start(message: Message, state: FSMContext, uid: int | None = None):
    await state.clear()
    uid = uid or message.from_user.id
    lang = await lang_of(uid)
    await stickers.send(message, "docs")
    await state.set_state(Docs.choose)
    await message.answer(
        t("docs_intro", lang),
        reply_markup=ik([[(t("btn_docs_ai", lang), "docs:ai")], [(t("btn_docs_manual", lang), "docs:manual")]]),
    )


@router.callback_query(Docs.choose, F.data.startswith("docs:"))
async def cb_docs_choose(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data.endswith("ai"):
        if not ai_check.ai_enabled():
            await call.message.answer(t("ai_disabled", lang))
            await manual_start(call.message, state, lang)
            return
        await state.set_state(Docs.ai_consent)
        await say(
            call.message,
            t("ai_consent", lang, **links(lang)),
            reply_markup=ik([[(t("btn_agree", lang), "aic:yes"), (t("btn_disagree", lang), "aic:no")]]),
        )
    else:
        await manual_start(call.message, state, lang)


@router.callback_query(Docs.ai_consent, F.data.startswith("aic:"))
async def cb_ai_consent(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data.endswith("no"):
        await manual_start(call.message, state, lang)
        return
    ai_check.session_start(call.from_user.id)
    await state.set_state(Docs.upload)
    await call.message.answer(
        t("send_docs", lang),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=t("btn_docs_done", lang))], [KeyboardButton(text=t("cancel", lang))]],
            resize_keyboard=True,
        ),
    )


@router.message(Docs.upload, F.photo | F.document)
async def docs_upload(message: Message, state: FSMContext, bot: Bot):
    lang = await lang_of(message.from_user.id)
    if message.photo:
        file_id, mime = message.photo[-1].file_id, "image/jpeg"
    else:
        doc = message.document
        mime = doc.mime_type or ""
        if not (mime.startswith("image/") or mime == "application/pdf") or (doc.file_size or 0) > 15_000_000:
            await message.answer(t("doc_need_photo", lang))
            return
        file_id = doc.file_id

    status = await message.answer(t("doc_reading", lang))
    buf = io.BytesIO()
    await bot.download(file_id, destination=buf)
    info = await ai_check.read_document(buf.getvalue(), mime)
    buf.close()
    del buf
    # remove the user's photo from the chat right away
    try:
        await message.delete()
    except TelegramBadRequest:
        pass
    try:
        await status.delete()
    except TelegramBadRequest:
        pass

    if info is None or not info.readable:
        await message.answer(t("doc_read_fail", lang))
        return
    if info.doc_type in ("passport_or_id", "bank_card"):
        await message.answer(t("doc_sensitive", lang))
        return
    ai_check.session_add(message.from_user.id, info)
    kind, details = ai_check.describe(info, lang)
    await message.answer(t("doc_read_ok", lang, kind=kind, details=details or "—"))


@router.message(Docs.upload, F.text.in_(both("btn_docs_done")))
async def docs_done(message: Message, state: FSMContext):
    lang = await lang_of(message.from_user.id)
    docs = ai_check.session_pop(message.from_user.id)
    await state.clear()
    if not docs:
        await message.answer(t("docs_none", lang), reply_markup=main_menu(lang))
        return
    year, _ = tax_season()
    issues, total_paid = ai_check.build_report(docs, lang, year)
    text = t("docs_report_title", lang)
    if issues:
        text += "\n" + "\n\n".join(issues)
    else:
        text += t("docs_all_ok", lang)
    if total_paid:
        label = "💵 Сумма платежей" if lang == "ru" else "💵 To'lovlar summasi"
        refund_label = "≈ можно вернуть" if lang == "ru" else "≈ qaytishi mumkin"
        text += f"\n\n{label}: <b>{fmt_sum(total_paid)}</b>\n🎯 {refund_label}: <b>{fmt_sum(total_paid * config.TAX_RATE)}</b>"
    text += t("docs_footer", lang)
    await stickers.send(message, "docs_issues" if issues else "docs_ok")
    await say(message, text, effect=None if issues else config.EFFECT_LIKE, reply_markup=main_menu(lang))


@router.message(Docs.upload)
async def docs_upload_other(message: Message):
    lang = await lang_of(message.from_user.id)
    await message.answer(t("doc_need_photo", lang))


MANUAL_Q = ["mq1", "mq2", "mq3", "mq4", "mq5", "mq6"]


async def manual_start(message: Message, state: FSMContext, lang: str):
    await state.set_state(Docs.manual)
    await state.update_data(mi=0, issues=[])
    await ask_manual(message, 0, lang)


async def ask_manual(message: Message, i: int, lang: str):
    await message.answer(
        t(MANUAL_Q[i], lang), reply_markup=ik([[(t("yes", lang), f"mq:{i}:y"), (t("no", lang), f"mq:{i}:n")]])
    )


@router.callback_query(Docs.manual, F.data.startswith("mq:"))
async def cb_manual(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    _, i, ans = call.data.split(":")
    i = int(i)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    if i != data.get("mi"):
        return
    issues = data.get("issues", [])
    if ans == "n":
        issues.append(f"mfix{i + 1}")
    if i + 1 < len(MANUAL_Q):
        await state.update_data(mi=i + 1, issues=issues)
        await ask_manual(call.message, i + 1, lang)
        return
    await state.clear()
    await stickers.send(call.message, "docs_issues" if issues else "docs_ok")
    if not issues:
        await say(call.message, t("manual_ok", lang), effect=config.EFFECT_LIKE, reply_markup=main_menu(lang))
    else:
        text = t("manual_issues", lang, n=len(issues)) + "\n\n".join(t(k, lang) for k in issues)
        await call.message.answer(text, reply_markup=main_menu(lang))


# ====================== guide ======================
def guide_page(lang: str, i: int) -> tuple[str, InlineKeyboardMarkup]:
    steps = T["guide_steps"][lang]
    text = steps[i] + (T["guide_disclaimer"][lang] if i == len(steps) - 1 else "")
    nav = []
    if i > 0:
        nav.append((t("btn_prev", lang), f"guide:{i - 1}"))
    if i < len(steps) - 1:
        nav.append((t("btn_next", lang), f"guide:{i + 1}"))
    rows = [nav]
    if i == len(steps) - 1:
        rows.append([(t("btn_book", lang), "go:book")])
    return text, ik(rows)


@router.message(Command("guide"))
@router.message(F.text.in_(both("btn_guide")))
async def guide_start(message: Message, state: FSMContext, uid: int | None = None):
    await state.clear()
    uid = uid or message.from_user.id
    lang = await lang_of(uid)
    text, kb = guide_page(lang, 0)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.startswith("guide:"))
async def cb_guide(call: CallbackQuery):
    lang = await lang_of(call.from_user.id)
    i = int(call.data.split(":")[1])
    text, kb = guide_page(lang, i)
    await call.answer()
    try:
        await call.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        pass


# ====================== articles ======================
def articles_kb(lang: str) -> InlineKeyboardMarkup:
    return ik([[(a["title"][lang], f"art:{i}")] for i, a in enumerate(ARTICLES)])


@router.message(Command("articles"))
@router.message(F.text.in_(both("btn_articles")))
async def articles(message: Message, state: FSMContext):
    await state.clear()
    lang = await lang_of(message.from_user.id)
    await message.answer(t("articles_title", lang), reply_markup=articles_kb(lang))


@router.callback_query(F.data.startswith("art:"))
async def cb_article(call: CallbackQuery):
    lang = await lang_of(call.from_user.id)
    key = call.data.split(":")[1]
    await call.answer()
    if key == "list":
        text, kb = t("articles_title", lang), articles_kb(lang)
    else:
        text = ARTICLES[int(key)]["body"][lang]
        kb = ik([[(t("btn_back", lang), "art:list")], [(t("btn_check", lang), "go_check")]])
    try:
        await call.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "go_check")
async def cb_go_check(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await check_start(call.message, state, uid=call.from_user.id)


# ====================== booking ======================
@router.message(Command("book"))
@router.message(F.text.in_(both("btn_book")))
async def book_start(message: Message, state: FSMContext, uid: int | None = None):
    await state.clear()
    uid = uid or message.from_user.id
    lang = await lang_of(uid)
    await stickers.send(message, "book")
    await message.answer(
        t("book_intro", lang, price=fmt_sum(config.BOOKING_PRICE), fee=config.SUCCESS_FEE_PERCENT),
        reply_markup=ik([[(t("btn_book_start", lang), "book:start")]]),
    )


@router.callback_query(F.data == "book:start")
async def cb_book_start(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Booking.consent)
    await say(
        call.message,
        t("book_consent", lang, **links(lang)),
        reply_markup=ik([[(t("btn_agree", lang), "bc:yes"), (t("btn_disagree", lang), "bc:no")]]),
    )


@router.callback_query(Booking.consent, F.data.startswith("bc:"))
async def cb_book_consent(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data.endswith("no"):
        await state.clear()
        await call.message.answer(t("consent_declined", lang), reply_markup=main_menu(lang))
        return
    await db.set_consent(call.from_user.id)
    await state.set_state(Booking.name)
    await call.message.answer(t("q_name", lang), reply_markup=cancel_kb(lang))


@router.message(Booking.name, F.text)
async def book_name(message: Message, state: FSMContext):
    lang = await lang_of(message.from_user.id)
    name = message.text.strip()[:80]
    if name in both("cancel"):
        return await cmd_cancel(message, state)
    await state.update_data(name=name)
    await state.set_state(Booking.phone)
    await message.answer(
        t("q_phone", lang),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=t("btn_share_phone", lang), request_contact=True)],
                [KeyboardButton(text=t("cancel", lang))],
            ],
            resize_keyboard=True,
        ),
    )


@router.message(Booking.phone, F.contact | F.text)
async def book_phone(message: Message, state: FSMContext):
    lang = await lang_of(message.from_user.id)
    if message.text and message.text in both("cancel"):
        return await cmd_cancel(message, state)
    if message.contact:
        if message.contact.user_id and message.contact.user_id != message.from_user.id:
            await message.answer(t("bad_phone", lang))
            return
        phone = message.contact.phone_number
    else:
        digits = re.sub(r"\D", "", message.text or "")
        if len(digits) == 9:
            digits = "998" + digits
        if len(digits) != 12 or not digits.startswith("998"):
            await message.answer(t("bad_phone", lang))
            return
        phone = digits
    phone = "+" + phone.lstrip("+")
    await state.update_data(phone=phone)
    await state.set_state(Booking.fmt)
    await message.answer("👌", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        t("q_format", lang), reply_markup=ik([[(t("fmt_offline", lang), "fmt:offline"), (t("fmt_video", lang), "fmt:video")]])
    )


@router.callback_query(Booking.fmt, F.data.startswith("fmt:"))
async def cb_book_fmt(call: CallbackQuery, state: FSMContext, bot: Bot):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    fmt = call.data.split(":")[1]
    booking_id = await db.add_booking(call.from_user.id, data["name"], data["phone"], fmt)
    await state.set_state(Booking.receipt)
    await state.update_data(booking_id=booking_id)
    holder = f"👤 {config.PAYMENT_HOLDER}" if config.PAYMENT_HOLDER else ""
    await stickers.send(call.message, "book_done")
    await say(
        call.message,
        t("book_done", lang, id=booking_id, card=config.PAYMENT_CARD, holder=holder, price=fmt_sum(config.BOOKING_PRICE)),
        effect=config.EFFECT_PARTY,
        reply_markup=main_menu(lang),
    )
    username = f"@{call.from_user.username}" if call.from_user.username else "—"
    await notify_admins(
        bot,
        f"🆕 <b>Bron №{booking_id}</b>\n👤 {html.escape(data['name'])} ({username})\n📱 {data['phone']}\n📍 {fmt}\n🌐 {lang}",
    )


@router.message(Booking.receipt, F.photo | F.document)
async def book_receipt(message: Message, state: FSMContext, bot: Bot):
    lang = await lang_of(message.from_user.id)
    data = await state.get_data()
    booking_id = data.get("booking_id")
    await state.clear()
    for admin_id in config.ADMIN_IDS:
        try:
            await message.copy_to(
                admin_id,
                caption=f"🧾 Chek — bron №{booking_id}",
                reply_markup=ik([[("✅ To'lov tasdiqlandi", f"paid:{booking_id}")]]),
            )
        except Exception:
            log.exception("Cannot forward receipt")
    await message.answer(t("receipt_received", lang), reply_markup=main_menu(lang))


@router.callback_query(F.data.startswith("paid:"))
async def cb_paid(call: CallbackQuery, bot: Bot):
    if call.from_user.id not in config.ADMIN_IDS:
        await call.answer("⛔️")
        return
    booking_id = int(call.data.split(":")[1])
    user_id = await db.set_booking_status(booking_id, "paid")
    await call.answer("🇺🇿 O'zbek tili tanlandi" if lang == "uz" else "🇷🇺 Выбран русский язык")
    await call.message.edit_reply_markup(reply_markup=None)
    if user_id:
        lang = await lang_of(user_id)
        await stickers.send_to(bot, user_id, "paid")
        try:
            await bot.send_message(user_id, t("booking_paid", lang, id=booking_id), message_effect_id=config.EFFECT_PARTY)
        except TelegramBadRequest:
            await bot.send_message(user_id, t("booking_paid", lang, id=booking_id))


# ====================== reminders ======================
@router.message(Command("remind"))
@router.message(F.text.in_(both("btn_remind")))
async def remind_toggle(message: Message, state: FSMContext):
    await state.clear()
    lang = await lang_of(message.from_user.id)
    on = await db.toggle_reminders(message.from_user.id)
    if on:
        await stickers.send(message, "remind")
    await say(message, t("remind_on" if on else "remind_off", lang), effect=config.EFFECT_LIKE if on else None)


REMINDERS = [((1, 5), "rem_jan"), ((3, 1), "rem_month"), ((3, 25), "rem_week")]


async def reminder_loop(bot: Bot):
    while True:
        try:
            ai_check.purge_expired()
            now = datetime.now(TASHKENT)
            if now.hour >= 10:
                for (month, day), key in REMINDERS:
                    if (now.month, now.day) == (month, day) and await db.mark_reminder_sent(f"{now.year}-{key}"):
                        for user_id, lang in await db.reminder_users():
                            try:
                                await bot.send_message(user_id, t(key, lang or "uz"))
                            except (TelegramForbiddenError, TelegramBadRequest):
                                pass
                            await asyncio.sleep(0.05)
        except Exception:
            log.exception("reminder loop")
        await asyncio.sleep(300)


# ====================== privacy ======================
@router.message(Command("privacy"))
@router.message(F.text.in_(both("btn_privacy")))
async def privacy(message: Message, state: FSMContext):
    await state.clear()
    lang = await lang_of(message.from_user.id)
    await say(
        message, t("privacy_menu", lang, **links(lang)), reply_markup=ik([[(t("btn_delete_me", lang), "del:ask")]])
    )


@router.message(Command("delete_me"))
async def cmd_delete(message: Message):
    lang = await lang_of(message.from_user.id)
    await message.answer(
        t("confirm_delete", lang), reply_markup=ik([[(t("yes", lang), "del:yes"), (t("no", lang), "del:no")]])
    )


@router.callback_query(F.data.startswith("del:"))
async def cb_delete(call: CallbackQuery, state: FSMContext):
    lang = await lang_of(call.from_user.id)
    await call.answer()
    action = call.data.split(":")[1]
    if action == "ask":
        await call.message.answer(
            t("confirm_delete", lang), reply_markup=ik([[(t("yes", lang), "del:yes"), (t("no", lang), "del:no")]])
        )
        return
    await call.message.edit_reply_markup(reply_markup=None)
    if action == "yes":
        await state.clear()
        ai_check.session_pop(call.from_user.id)
        await db.delete_user_data(call.from_user.id)
        await stickers.send(call.message, "deleted")
        await call.message.answer(t("deleted", lang), reply_markup=ReplyKeyboardRemove())


# ====================== admin ======================
def is_admin(message: Message) -> bool:
    return message.from_user.id in config.ADMIN_IDS


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message):
        return
    s = await db.stats()
    await message.answer(
        "<b>📊 Qaytar statistikasi</b>\n\n"
        f"👥 Foydalanuvchilar: <b>{s['users']}</b>\n"
        f"🧮 Tekshiruvlar: <b>{s['checks']}</b>\n"
        f"✅ Huquqi bor: <b>{s['eligible']}</b>\n"
        f"💰 Topilgan pul (jami): <b>{fmt_sum(s['refund_found'])} so'm</b>\n"
        f"📝 Bronlar: <b>{s['bookings']}</b> (to'langan: <b>{s['paid']}</b>)\n"
        f"⏰ Eslatmaga obuna: <b>{s['reminders']}</b>"
    )


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, bot: Bot):
    if not is_admin(message):
        return
    text = message.html_text.partition(" ")[2].strip()
    if not text:
        await message.answer("Foydalanish: <code>/broadcast matn</code>")
        return
    sent = 0
    for user_id, _ in await db.all_user_ids():
        try:
            await bot.send_message(user_id, text)
            sent += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            pass
        await asyncio.sleep(0.05)
    await message.answer(f"✅ Yuborildi: {sent}")


@router.message(F.sticker)
async def admin_sticker_id(message: Message):
    if is_admin(message):
        await message.answer(f"Sticker file_id:\n<code>{message.sticker.file_id}</code>")


@router.message(StateFilter(None), F.text)
async def fallback(message: Message):
    if is_admin(message) and message.entities:
        ids = [e.custom_emoji_id for e in message.entities if e.type == "custom_emoji"]
        if ids:
            await message.answer("Custom emoji id:\n" + "\n".join(f"<code>{i}</code>" for i in ids))
            return
    lang = await lang_of(message.from_user.id)
    await message.answer(t("unknown", lang), reply_markup=main_menu(lang))


# ====================== setup ======================
async def setup_bot_profile(bot: Bot):
    cmds = {
        "uz": [("start", "Boshlash"), ("check", "Huquqni tekshirish"), ("docs", "Hujjatlarni tekshirish"),
               ("guide", "Yo'riqnoma"), ("book", "Birga topshiramiz"), ("articles", "Maqolalar"),
               ("privacy", "Maxfiylik"), ("lang", "Til")],
        "ru": [("start", "Начать"), ("check", "Проверить право"), ("docs", "Проверить документы"),
               ("guide", "Инструкция"), ("book", "Подать вместе"), ("articles", "Статьи"),
               ("privacy", "Конфиденциальность"), ("lang", "Язык")],
    }
    desc = {
        "uz": ("Kontrakt, xususiy bog'cha/maktab va ipoteka uchun to'langan pulning 12% ini davlatdan qaytarib olishga "
               "yordam beramiz. 1 daqiqada bepul tekshiring! Parol va kodlarni hech qachon so'ramaymiz."),
        "ru": ("Помогаем вернуть от государства 12% денег за контракт в вузе, частный сад/школу и ипотеку. "
               "Бесплатная проверка за 1 минуту! Мы никогда не просим пароли и коды."),
    }
    short = {
        "uz": "Kontrakt va ipoteka uchun 12% ni qaytaring 💸",
        "ru": "Верните 12% за контракт и ипотеку 💸",
    }
    try:
        await bot.set_my_commands([BotCommand(command=c, description=d) for c, d in cmds["uz"]])
        await bot.set_my_commands([BotCommand(command=c, description=d) for c, d in cmds["ru"]], language_code="ru")
        await bot.set_my_description(desc["uz"])
        await bot.set_my_description(desc["ru"], language_code="ru")
        await bot.set_my_short_description(short["uz"])
        await bot.set_my_short_description(short["ru"], language_code="ru")
        await bot.set_my_name("Qaytar — 12% qaytarish")
    except Exception:
        log.exception("Profile setup failed (not critical)")


async def main():
    if not config.BOT_TOKEN:
        raise SystemExit("BOT_TOKEN is empty — fill in .env")
    await db.init()
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await setup_bot_profile(bot)
    await stickers.load(bot)
    asyncio.create_task(reminder_loop(bot))
    me = await bot.get_me()
    log.info("Started @%s | AI: %s | admins: %s", me.username, ai_check.ai_enabled(), config.ADMIN_IDS or "none")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
