"""Refund math and number parsing. Pure functions, easy to test."""
import re
from dataclasses import dataclass
from datetime import date

from config import TAX_RATE


def parse_sum(text: str) -> int | None:
    """Parse user input like '20 000 000', '20mln', '20 млн', '2,5 mln', '18m', '500 ming'."""
    if not text:
        return None
    t = text.lower().strip().replace("so'm", "").replace("сум", "").replace("som", "")
    t = t.replace(" ", " ")
    m = re.match(r"^\s*([\d\s.,]+)\s*([a-zа-яё'’]*)\s*$", t)
    if not m:
        return None
    num, unit = m.group(1).replace(" ", ""), m.group(2)
    multiplier = 1
    if unit in ("mln", "млн", "m", "million", "миллион", "миллиона", "миллионов", "million"):
        multiplier = 1_000_000
    elif unit in ("ming", "тыс", "k", "минг", "тысяч", "тысячи"):
        multiplier = 1_000
    elif unit in ("mlrd", "млрд"):
        multiplier = 1_000_000_000
    elif unit:
        return None
    if multiplier > 1:
        num = num.replace(",", ".")
        if num.count(".") > 1:
            return None
    else:
        num = num.replace(",", "").replace(".", "")
    try:
        value = float(num) * multiplier
    except ValueError:
        return None
    value = int(round(value))
    return value if value > 0 else None


def fmt_sum(value: int | float) -> str:
    return f"{int(round(value)):,}".replace(",", " ")


@dataclass
class RefundResult:
    by_expense: int      # 12% of what was paid
    by_tax_paid: int     # max tax actually withheld in the year
    refund: int          # what can realistically come back
    limited_by_salary: bool


def calc_refund(paid: int, monthly_salary: int, months: int = 12) -> RefundResult:
    by_expense = int(paid * TAX_RATE)
    by_tax = int(monthly_salary * months * TAX_RATE)
    refund = min(by_expense, by_tax)
    return RefundResult(by_expense, by_tax, refund, by_tax < by_expense)


def tax_season(today: date | None = None) -> tuple[int, date]:
    """Which tax year is being prepared now and its declaration deadline (1 April next year)."""
    today = today or date.today()
    tax_year = today.year - 1 if today.month <= 3 else today.year
    return tax_year, date(tax_year + 1, 4, 1)
