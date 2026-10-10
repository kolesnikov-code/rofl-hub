import os
from pathlib import Path
from dotenv import load_dotenv

# Намертво находим корень нашего проекта ROFL-HUB
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Единый, монолитный источник токена пользователя
BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "🚨 КРИТИЧЕСКИЙ КРАШ: Переменная MAIN_BOT_TOKEN отсутствует в системе или файле .env! Запуск заблокирован."
    )
