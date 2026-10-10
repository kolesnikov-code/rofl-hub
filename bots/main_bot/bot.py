import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from bots.main_bot.config import BOT_TOKEN

# Импортируем только реально существующие боевые роутеры
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.menu import router as help_router
from bots.main_bot.handlers.faq import router as faq_router
from bots.main_bot.handlers.rofl_hub_all import router as rofl_hub_all_router
from bots.main_bot.handlers.rules import router as rules_router
from bots.main_bot.handlers.profile import router as profile_router
from bots.main_bot.handlers.clans import router as clans_router
from bots.main_bot.handlers.shop import router as shop_router
from bots.main_bot.handlers.payments import router as payments_router  # Наш титановый Stars-шлюз!
from bots.main_bot.handlers import games, farm

from shared.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    try:
        # Инициализируем пул и создаем таблицы империи в PostgreSQL на Railway
        await db.connect()
        await db.create_tables()

        # Подключаем роутеры строго по нашему новому приоритету
        for router in (
                start_router,
                help_router,
                faq_router,
                rofl_hub_all_router,
                rules_router,
                profile_router,
                clans_router,
                shop_router,
                payments_router,  # Включаем приём платежей!
                games.router,
                farm.router,
        ):
            dp.include_router(router)

        logger.info("🟢 ГЛАВНЫЙ БОТ ЮЗЕРОВ УСПЕШНО ЗАПУЩЕН НА ЛОКАЛЬНОМ ХОСТЕ!")
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"🚨 Фатальная ошибка во время работы основного бота: {e}")

    finally:
        logger.info("⏳ Закрываю сессии бота и пул соединений PostgreSQL...")
        await bot.session.close()
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
