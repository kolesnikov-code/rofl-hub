import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage

# Намертво привязываем чтение .env к корню проекта
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Сверяем токен строго по вашей конфигурации из .env
BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("🚨 КРИТИЧЕСКИЙ КРАШ: Переменная MAIN_BOT_TOKEN отсутствует в .env! Запуск заблокирован.")

# Импортируем пул базы данных PostgreSQL на Railway
from shared.database import db
from bots.main_bot.utils.questions_loader import load_questions_from_csv

# ============================================================================
# # 🔗 ИМПОРТ АБСОЛЮТНО ВСЕХ РОУТЕРОВ ЭКОСИСТЕМЫ С ВАШЕГО СКРИНШОТА
# ============================================================================
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.menu import router as menu_router
from bots.main_bot.handlers.profile import router as profile_router
from bots.main_bot.handlers.farm import router as farm_router
from bots.main_bot.handlers.clans import router as clans_router
from bots.main_bot.handlers.shop import router as shop_router
from bots.main_bot.handlers.games import router as games_router
from bots.main_bot.handlers.payments import router as payments_router
from bots.main_bot.handlers.faq import router as faq_router
from bots.main_bot.handlers.rules import router as rules_router

# ============================================================================
# ⚙️ ИМПОРТ ФУНКЦИЙ-ОБРАБОТЧИКОВ ДЛЯ ПРЯМОЙ REPLY-СВЯЗИ
# ============================================================================
from bots.main_bot.handlers.menu import cmd_main_menu, cmd_games_hub
from bots.main_bot.handlers.profile import cmd_profile_stats
from bots.main_bot.handlers.farm import cmd_farm
from bots.main_bot.handlers.clans import cmd_clan_hub
from bots.main_bot.handlers.shop import cmd_premium_shop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())

# Включаем абсолютно все роутеры в диспетчер
dp.include_router(start_router)
dp.include_router(menu_router)
dp.include_router(profile_router)
dp.include_router(farm_router)
dp.include_router(clans_router)
dp.include_router(shop_router)
dp.include_router(games_router)
dp.include_router(payments_router)
dp.include_router(faq_router)
dp.include_router(rules_router)


async def main() -> None:
    """Главная асинхронная точка запуска продакшен-контура"""
    bot = Bot(token=BOT_TOKEN)

    # Подключение к СУБД Railway и инициализация структуры таблиц
    await db.connect()
    await db.create_tables()

    # Загрузка буфера 5000 вопросов викторины из CSV-таблицы
    try:
        load_questions_from_csv()
    except Exception as e:
        logger.error(f"Ошибка загрузки вопросов викторины: {e}")

    # Регистрация обработчиков текстовых Reply-кнопок
    dp.message.register(cmd_profile_stats, F.text == "👤 МОЙ ПРОФИЛЬ")
    dp.message.register(cmd_farm, F.text == "🚜 МОЯ ФЕРМА")
    dp.message.register(cmd_games_hub, F.text == "🕹️ ИГРОВАЯ ЗОНА")
    dp.message.register(cmd_clan_hub, F.text == "🏆 КОМАНДЫ И КЛАНЫ")
    dp.message.register(cmd_premium_shop, F.text == "🏪 МАГАЗИН")
    dp.message.register(cmd_main_menu, F.text == "📱 ГЛАВНОЕ МЕНЮ")

    logger.info("🟢 ГЛАВНЫЙ ЮЗЕР-БОТ УСПЕШНО СИНХРОНИЗИРОВАН И ГОТОВ К РАБОТЕ!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
