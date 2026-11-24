"""Animated (incl. Premium) stickers from public Telegram packs.

file_ids are looked up once at startup by pack name + emoji, so this works for any bot token.
Override any moment from .env (STICKER_WELCOME / STICKER_SUCCESS / STICKER_DOCS) with your own file_id.
"""
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

import config

log = logging.getLogger(__name__)

# key -> (pack name, emoji, prefer premium version)
PLAN: dict[str, tuple[str, str, bool]] = {
    "lang": ("UtyaDuck", "🤗", False),
    "welcome": ("UtyaDuck", "👋", False),
    "check": ("UtyaDuck", "🧮", False),
    "result": ("UtyaDuck", "🥳", True),        # premium
    "sad": ("UtyaDuck", "😢", True),           # premium
    "docs": ("UtyaDuck", "🛡", False),
    "thinking": ("UtyaDuck", "🤔", False),
    "docs_ok": ("MrCat", "👍", True),          # premium
    "docs_issues": ("MrCat", "📊", True),      # premium
    "book": ("UtyaDuck", "🤑", False),
    "book_done": ("HotCherry", "💃", True),    # premium
    "paid": ("UtyaDuck", "💪", False),
    "remind": ("UtyaDuck", "📨", False),
    "deleted": ("HotCherry", "👍", True),      # premium
}

OVERRIDES = {
    "welcome": config.STICKER_WELCOME,
    "result": config.STICKER_SUCCESS,
    "docs": config.STICKER_DOCS,
}

_ids: dict[str, str] = {}


async def load(bot: Bot) -> None:
    packs: dict[str, list] = {}
    for key, (pack, emoji, premium) in PLAN.items():
        if OVERRIDES.get(key):
            _ids[key] = OVERRIDES[key]
            continue
        try:
            if pack not in packs:
                packs[pack] = (await bot.get_sticker_set(pack)).stickers
            matches = [s for s in packs[pack] if s.emoji == emoji]
            if premium:
                matches.sort(key=lambda s: not s.premium_animation)  # premium first
            if matches:
                _ids[key] = matches[0].file_id
        except Exception:
            log.warning("Sticker pack %s unavailable", pack)
    log.info("Stickers loaded: %d/%d", len(_ids), len(PLAN))


async def send(message: Message, key: str) -> None:
    file_id = _ids.get(key)
    if not file_id:
        return
    try:
        await message.answer_sticker(file_id)
    except TelegramBadRequest:
        log.warning("Cannot send sticker %s", key)


async def send_to(bot: Bot, chat_id: int, key: str) -> None:
    file_id = _ids.get(key)
    if file_id:
        try:
            await bot.send_sticker(chat_id, file_id)
        except TelegramBadRequest:
            pass
