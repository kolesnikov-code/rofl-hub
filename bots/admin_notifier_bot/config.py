import os
from pathlib import Path
from dotenv import load_dotenv

# Намертво находим корень нашего проекта ROFL-HUB
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Единый, монолитный источник токена админа
BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "Переменная ADMIN_BOT_TOKEN отсутствует в окружении / .env. Запуск заблокирован."
    )
