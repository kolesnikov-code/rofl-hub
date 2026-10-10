import asyncio
import logging
from aiogram import Bot, Dispatcher
from bots.main_bot.config import BOT_TOKEN

# Импортируем строго существующие боевые роутеры нашей империи
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.menu import router as help_router
from bots.main_bot.handlers.faq import router as faq_router
from bots.main_bot.handlers.rofl_hub_all import router as rofl_hub_all_router
from bots.main_bot.handlers.rules import router as rules_router
from bots.main_bot.handlers.profile import router as profile_router
from bots.main_bot.handlers.clans import router as clans_router
from bots.main_bot.handlers.shop import router as shop_router
from bots.main_bot.handlers.payments import router as payments_router
from bots.main_bot.handlers import games, farm

from shared.database import db

# Настройка системного логирования Highload-уровня
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Главная точка входа в асинхронный контур пользовательского бота.
    Отвечает за инициализацию пулов PostgreSQL на Railway и запуск polling-шлюза.
    """
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    try:
        # Инициализируем пул и создаем монолитные таблицы империи в PostgreSQL
        await db.connect()
        await db.create_tables()

        # Подключаем боевые роутеры строго по нашему новому приоритету удержания юзеров
        for router in (
                start_router,
                help_router,
                faq_router,
                rofl_hub_all_router,
                rules_router,
                profile_router,
                clans_router,
                shop_router,
                payments_router,  # Наш транзакционный Stars-шлюз
                games.router,
                farm.router,
        ):
            dp.include_router(router)

        logger.info("🟢 ГЛАВНЫЙ БОТ ЮЗЕРОВ УСПЕШНО ЗАПУЩЕН И ГОТОВ К НАГРУЗКАМ!")

        # Запускаем асинхронный шлюз прослушивания обновлений Telegram
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"🚨 Фатальный краш во время работы основного бота: {e}")

    finally:
        # Титановое закрытие всех шлюзов связи при перезапуске (SaaS Безопасность)
        logger.info("⏳ Запущена процедура безопасного закрытия сессий и пула PostgreSQL...")
        await bot.session.close()
        await db.disconnect()
        logger.info("🔒 Все асинхронные соединения успешно изолированы и закрыты.")


if __name__ == "__main__":
    asyncio.run(main())
