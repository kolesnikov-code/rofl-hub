import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

# Жестко привязываем чтение .env к корню проекта для безопасности токенов холдинга
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Считываем токен главного игрового бота
BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "🚨 КРИТИЧЕСКИЙ КРАШ СИСТЕМЫ: Переменная MAIN_BOT_TOKEN отсутствует в .env! Запуск заблокирован."
    )

# Импортируем пул базы данных PostgreSQL на Railway
from shared.database import db

# Импортируем все наши обновленные роутеры
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.menu import router as menu_router
from bots.main_bot.handlers.profile import router as profile_router
from bots.main_bot.handlers.farm import router as farm_router
from bots.main_bot.handlers.clans import router as clans_router
from bots.main_bot.handlers.shop import router as shop_router
from bots.main_bot.handlers.games import router as games_router
from bots.main_bot.handlers.payments import router as payments_router

# Импортируем сами функции-обработчики для прямой Reply-связи
from bots.main_bot.handlers.menu import cmd_main_menu, cmd_games_hub
from bots.main_bot.handlers.profile import cmd_profile_stats
from bots.main_bot.handlers.farm import cmd_farm
from bots.main_bot.handlers.clans import cmd_clan_hub
from bots.main_bot.handlers.shop import cmd_shop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Главная асинхронная точка входа в контур игрового бота ROFL HUB CORE.
    """
    # Инициализируем бота и диспетчер со встроенным хранилищем состояний FSM
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    try:
        # Подключаемся к асинхронному пулу PostgreSQL на Railway
        await db.connect()
        await db.create_tables()

        # ============================================================================
        # 🎰 ЖЕСТКАЯ ПРИВЯЗКА ТЕКСТОВЫХ REPLY-КНОПОК К НАШИМ ОБРАБОТЧИКАМ
        # ============================================================================
        # Перехватываем нажатия постоянных нижних кнопок до регистрации роутеров
        dp.message.register(cmd_main_menu, F.text == "📱 ГЛАВНОЕ МЕНЮ")
        dp.message.register(cmd_profile_stats, F.text == "👤 МОЙ ПРОФИЛЬ")
        dp.message.register(cmd_farm, F.text == "🚜 МОЯ ФЕРМА")
        dp.message.register(cmd_games_hub, F.text == "🕹️ ИГРОВАЯ ЗОНА")
        dp.message.register(cmd_clan_hub, F.text == "🏆 КОМАНДЫ И КЛАНЫ")
        dp.message.register(cmd_shop, F.text == "🏪 МАГАЗИН")

        # Включаем все наши монолитные изолированные роутеры
        dp.include_router(start_router)
        dp.include_router(menu_router)
        dp.include_router(profile_router)
        dp.include_router(farm_router)
        dp.include_router(clans_router)
        dp.include_router(shop_router)
        dp.include_router(games_router)
        dp.include_router(payments_router)

        logger.info("🟢 ГЛАВНЫЙ БОТ ЮЗЕРОВ УСПЕШНО ЗАПУЩЕН И ГОТОВ К НАГРУЗКАМ!")

        # Запускаем шлюз бесконечного прослушивания апдейтов
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"🚨 Фатальная ошибка во время инициализации bot.py: {e}")

    finally:
        logger.info("⏳ Безопасное закрытие сессий и пула базы данных...")
        await bot.session.close()
        if db.pool:
            await db.pool.close()
        logger.info("🔒 Контур бота полностью изолирован и закрыт.")


if __name__ == "__main__":
    asyncio.run(main())
