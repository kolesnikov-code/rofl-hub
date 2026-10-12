"""
Точка входа главного бота ROFL HUB. Запуск: python -m bots.main_bot.bot
"""
from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent

from bots.main_bot.config import BOT_TOKEN, SHOP_TEST_MODE, SHOP_TEST_USER_IDS
from bots.main_bot.handlers.clans import router as clans_router
from bots.main_bot.handlers.faq import router as faq_router
from bots.main_bot.handlers.farm import router as farm_router
from bots.main_bot.handlers.games import router as games_router
from bots.main_bot.handlers.menu import router as menu_router
from bots.main_bot.handlers.payments import router as payments_router
from bots.main_bot.handlers.profile import router as profile_router
from bots.main_bot.handlers.referral_link import router as referral_router
from bots.main_bot.handlers.rofl_hub_all import router as rofl_hub_all_router
from bots.main_bot.handlers.rules import router as rules_router
from bots.main_bot.handlers.shop import router as shop_router
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.transfer import router as transfer_router
from bots.main_bot.middleware import ActivityMiddleware
from bots.main_bot.utils.questions_loader import load_questions_from_csv
from shared.database import db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())
# Блокировка игроков + учёт активности (DAU) — на каждый апдейт
dp.update.outer_middleware(ActivityMiddleware())
# Порядок важен: start (регистрация) и payments (деньги) — первыми
for r in (start_router, payments_router, shop_router, games_router, farm_router, profile_router,
          clans_router, transfer_router, referral_router, menu_router, faq_router, rules_router,
          rofl_hub_all_router):
    dp.include_router(r)


@dp.error()
async def on_error(event: ErrorEvent) -> None:
    """Любое необработанное исключение — в лог целиком, игроку — короткий ответ, бот живёт дальше."""
    logger.exception("Необработанная ошибка в обработчике: %s", event.exception)
    update = event.update
    try:
        if update.callback_query:
            await update.callback_query.answer("⚠️ Что-то пошло не так. Попробуй ещё раз.", show_alert=True)
        elif update.message:
            await update.message.answer("⚠️ Что-то пошло не так. Попробуй ещё раз через минуту.")
    except Exception:
        pass


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await db.connect()
    await db.create_tables()
    load_questions_from_csv()

    if SHOP_TEST_MODE:
        logger.warning("SHOP_TEST_MODE=1: бесплатные покупки для %s. На проде выключить!", sorted(SHOP_TEST_USER_IDS))

    me = await bot.get_me()
    logger.info("Главный бот @%s запущен.", me.username)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
