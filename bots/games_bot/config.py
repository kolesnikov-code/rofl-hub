import os
from pathlib import Path
from dotenv import load_dotenv

# Путь к .env в корне проекта
# __file__ = .../ROFL-HUB/bots/main_bot/config.py
# .parent = .../ROFL-HUB/bots/main_bot/
# .parent.parent = .../ROFL-HUB/bots/
# .parent.parent.parent = .../ROFL-HUB/

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Читаем токен ИМЕННО этого бота
BOT_TOKEN = os.getenv("GAMES_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("GAMES_BOT_TOKEN не найден в .env")