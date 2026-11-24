"""Settings loaded from .env (never hard-code secrets)."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _int_list(value: str) -> set[int]:
    return {int(x) for x in value.replace(" ", "").split(",") if x.strip().lstrip("-").isdigit()}


BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
ADMIN_IDS = _int_list(os.environ.get("ADMIN_IDS", ""))

PAYMENT_CARD = os.environ.get("PAYMENT_CARD", "")
PAYMENT_HOLDER = os.environ.get("PAYMENT_HOLDER", "")
BOOKING_PRICE = int(os.environ.get("BOOKING_PRICE", "29000"))
SUCCESS_FEE_PERCENT = int(os.environ.get("SUCCESS_FEE_PERCENT", "10"))

SITE_URL = os.environ.get("SITE_URL", "https://qaytar.uz").rstrip("/")
PRIVACY_URL = f"{SITE_URL}/privacy.html"
TERMS_URL = f"{SITE_URL}/terms.html"

STICKER_WELCOME = os.environ.get("STICKER_WELCOME", "")
STICKER_SUCCESS = os.environ.get("STICKER_SUCCESS", "")
STICKER_DOCS = os.environ.get("STICKER_DOCS", "")

DB_PATH = BASE_DIR / "qaytar.db"

TAX_RATE = 0.12

# Telegram message effects (private chats only). If Telegram rejects one,
# the bot silently sends the message without it.
EFFECT_PARTY = "5046509860389126442"   # 🎉
EFFECT_LIKE = "5107584321108051014"    # 👍
EFFECT_FIRE = "5104841245755180586"    # 🔥
