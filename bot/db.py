"""Minimal SQLite storage. Document images are NEVER stored here."""
import time

import aiosqlite

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    lang TEXT,
    created_at INTEGER,
    privacy_consent_at INTEGER,
    reminders INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    kind TEXT,
    paid INTEGER,
    refund INTEGER,
    created_at INTEGER
);
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    phone TEXT,
    format TEXT,
    status TEXT DEFAULT 'new',
    created_at INTEGER
);
CREATE TABLE IF NOT EXISTS sent_reminders (
    key TEXT PRIMARY KEY
);
"""


async def init() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def ensure_user(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            # lang stays NULL until the user picks a language on the first /start
            "INSERT OR IGNORE INTO users(user_id, lang, created_at) VALUES(?, NULL, ?)", (user_id, int(time.time()))
        )
        await db.commit()


async def get_lang(user_id: int) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT lang FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None


async def set_lang(user_id: int, lang: str) -> None:
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
        await db.commit()


async def set_consent(user_id: int) -> None:
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET privacy_consent_at=? WHERE user_id=?", (int(time.time()), user_id))
        await db.commit()


async def has_consent(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT privacy_consent_at FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return bool(row and row[0])


async def toggle_reminders(user_id: int) -> bool:
    await ensure_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET reminders = 1 - reminders WHERE user_id=?", (user_id,))
        await db.commit()
        cur = await db.execute("SELECT reminders FROM users WHERE user_id=?", (user_id,))
        return bool((await cur.fetchone())[0])


async def reminder_users() -> list[tuple[int, str]]:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT user_id, lang FROM users WHERE reminders=1")
        return list(await cur.fetchall())


async def mark_reminder_sent(key: str) -> bool:
    """Returns True if this reminder key was not sent before."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("INSERT OR IGNORE INTO sent_reminders(key) VALUES(?)", (key,))
        await db.commit()
        return cur.rowcount == 1


async def add_check(user_id: int, kind: str, paid: int, refund: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO checks(user_id, kind, paid, refund, created_at) VALUES(?,?,?,?,?)",
            (user_id, kind, paid, refund, int(time.time())),
        )
        await db.commit()


async def add_booking(user_id: int, name: str, phone: str, fmt: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO bookings(user_id, name, phone, format, created_at) VALUES(?,?,?,?,?)",
            (user_id, name, phone, fmt, int(time.time())),
        )
        await db.commit()
        return cur.lastrowid


async def set_booking_status(booking_id: int, status: str) -> int | None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE bookings SET status=? WHERE id=?", (status, booking_id))
        await db.commit()
        cur = await db.execute("SELECT user_id FROM bookings WHERE id=?", (booking_id,))
        row = await cur.fetchone()
        return row[0] if row else None


async def delete_user_data(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        for table in ("checks", "bookings", "users"):
            await db.execute(f"DELETE FROM {table} WHERE user_id=?", (user_id,))
        await db.commit()


async def all_user_ids() -> list[tuple[int, str]]:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT user_id, lang FROM users")
        return list(await cur.fetchall())


async def stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        async def one(sql: str):
            cur = await db.execute(sql)
            return (await cur.fetchone())[0] or 0

        return {
            "users": await one("SELECT COUNT(*) FROM users"),
            "checks": await one("SELECT COUNT(*) FROM checks"),
            "refund_found": await one("SELECT SUM(refund) FROM checks WHERE refund > 0"),
            "eligible": await one("SELECT COUNT(DISTINCT user_id) FROM checks WHERE refund > 0"),
            "bookings": await one("SELECT COUNT(*) FROM bookings"),
            "paid": await one("SELECT COUNT(*) FROM bookings WHERE status='paid'"),
            "reminders": await one("SELECT COUNT(*) FROM users WHERE reminders=1"),
        }
