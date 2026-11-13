"""
🔐 ПИН пульта владельца (/admin, владелец 14.11 — «это вопрос денег для семьи»): второй ключ к пульту поверх подписи Telegram.

Как в пульте холдинга (репозиторий pult, pult/auth.py): ПИН 4–8 цифр хранится только как PBKDF2-хэш с солью (таблица
admin_pin, одна строка); 5 ошибок подряд — вход закрыт на 15 минут, каждая следующая ошибка удваивает срок (до суток),
владельцу — личное сообщение. После ПИНа — сессия на SESSION_HOURS, подписанная секретом от токена бота и «версией ПИНа»:
смена или сброс ПИНа гасит все старые сессии. Забыл ПИН — переменная ADMIN_RESET_PIN=1 на хостинге и перезапуск.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import time

SESSION_HOURS = 12
PIN_MIN_LEN, PIN_MAX_LEN = 4, 8
PIN_ITERATIONS = 200_000
MAX_PIN_FAILS = 5
LOCK_SECONDS = 15 * 60
SESSION_HEADER = "X-Admin-Session"


def valid_pin(pin) -> bool:
    return isinstance(pin, str) and pin.isdigit() and PIN_MIN_LEN <= len(pin) <= PIN_MAX_LEN


def hash_pin(pin: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), bytes.fromhex(salt), PIN_ITERATIONS).hex()
    return f"{salt}${digest}"


def check_pin(pin: str, stored: str | None) -> bool:
    try:
        salt, _ = (stored or "").split("$", 1)
        return hmac.compare_digest(hash_pin(pin, salt), stored)
    except (ValueError, TypeError):
        return False


def lock_seconds(fails: int) -> int:
    """0 до MAX_PIN_FAILS ошибок; дальше 15 мин, 30, 60… (не больше суток)."""
    if fails < MAX_PIN_FAILS:
        return 0
    return min(LOCK_SECONDS * 2 ** (fails - MAX_PIN_FAILS), 24 * 3600)


def session_secret(bot_token: str) -> str:
    """Секрет сессий — производный от токена бота: отдельной переменной на хостинге не нужно."""
    return hmac.new(bot_token.encode(), b"cb-admin-pin-session", hashlib.sha256).hexdigest()


def _sig(secret: str, uid: int, exp: int, pin_ver: str) -> str:
    return hmac.new(secret.encode(), f"{uid}.{exp}.{pin_ver}".encode(), hashlib.sha256).hexdigest()[:40]


def issue_session(secret: str, uid: int, pin_ver: str, now: float | None = None) -> str:
    exp = int((now if now is not None else time.time()) + SESSION_HOURS * 3600)
    return f"{uid}.{exp}.{_sig(secret, uid, exp, pin_ver)}"


def verify_session(token: str | None, secret: str, uid: int, pin_ver: str | None, now: float | None = None) -> bool:
    if not token or not pin_ver:
        return False
    parts = token.split(".")
    if len(parts) != 3 or not parts[0].isdigit() or not parts[1].isdigit() or int(parts[0]) != uid:
        return False
    if int(parts[1]) < (now if now is not None else time.time()):
        return False
    return hmac.compare_digest(_sig(secret, uid, int(parts[1]), pin_ver), parts[2])
