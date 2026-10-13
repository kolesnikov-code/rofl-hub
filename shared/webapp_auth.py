"""
Проверка подлинности Telegram Mini App initData.

Алгоритм по документации Telegram:
- secret_key = HMAC_SHA256(key="WebAppData", msg=bot_token)
- data_check_string = отсортированные пары "key=value" через \n (без поля hash)
- подпись = HMAC_SHA256(key=secret_key, msg=data_check_string).hexdigest()
Подделать initData без токена бота невозможно.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

DEFAULT_MAX_AGE_SECONDS = 24 * 3600  # initData старше суток не принимаем


def validate_init_data(init_data: str, bot_token: str,
                       max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
                       now: float | None = None) -> dict | None:
    """
    Проверяет подпись initData. Возвращает словарь полей (user уже распарсен)
    или None, если подпись неверна/протухла/данные битые.
    """
    if not init_data or not bot_token:
        return None
    try:
        pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    except ValueError:
        return None

    received_hash = pairs.pop("hash", None)
    if not received_hash:
        return None

    data_check_string = "\n".join(f"{k}={pairs[k]}" for k in sorted(pairs))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    calculated = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated, received_hash):
        return None

    auth_date = pairs.get("auth_date", "")
    if not auth_date.isdigit():
        return None
    now = now if now is not None else time.time()
    if now - int(auth_date) > max_age_seconds:
        return None

    if "user" in pairs:
        try:
            pairs["user"] = json.loads(pairs["user"])
        except (ValueError, TypeError):
            return None
        if not isinstance(pairs["user"], dict) or "id" not in pairs["user"]:
            return None
    return pairs


def sign_init_data(pairs: dict[str, str], bot_token: str) -> str:
    """
    Собирает подписанную строку initData (для тестов: мы — «Telegram»).
    pairs — поля БЕЗ hash; значения-словари сериализуются в JSON.
    """
    from urllib.parse import urlencode
    flat = {k: (json.dumps(v, separators=(",", ":"), ensure_ascii=False)
                if isinstance(v, dict) else str(v))
            for k, v in pairs.items()}
    data_check_string = "\n".join(f"{k}={flat[k]}" for k in sorted(flat))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    signature = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return urlencode({**flat, "hash": signature})
