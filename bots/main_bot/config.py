import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Переменная MAIN_BOT_TOKEN отсутствует в окружении / .env. Запуск заблокирован.")


def _parse_ids(raw: str) -> frozenset[int]:
    return frozenset(int(x.strip()) for x in raw.split(",") if x.strip().isdigit())


# Тест-режим магазина: товары выдаются без оплаты ТОЛЬКО перечисленным ID и ТОЛЬКО при SHOP_TEST_MODE=1
SHOP_TEST_MODE: bool = os.getenv("SHOP_TEST_MODE", "0").strip() == "1"
SHOP_TEST_USER_IDS: frozenset[int] = _parse_ids(os.getenv("SHOP_TEST_USER_IDS", ""))

# Куда слать тревоги о сбоях доставки (опционально)
_secret = os.getenv("ADMIN_SECRET_CHANNEL_ID", "").strip()
ADMIN_SECRET_CHANNEL_ID: int | None = int(_secret) if _secret.lstrip("-").isdigit() else None

ADMIN_IDS: frozenset[int] = _parse_ids(os.getenv("ADMIN_ID", ""))

# Mini App: публичный HTTPS-адрес (на хостинге), без него кнопки Mini App не показываются
WEBAPP_URL: str | None = os.getenv("WEBAPP_URL", "").strip() or None
# Порт веб-сервера Mini App (хостинг подставляет PORT сам)
_port = os.getenv("PORT", "") or os.getenv("WEBAPP_PORT", "8080")
WEBAPP_PORT: int = int(_port) if _port.isdigit() else 8080


def is_shop_tester(user_id: int) -> bool:
    return SHOP_TEST_MODE and user_id in SHOP_TEST_USER_IDS
