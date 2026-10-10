import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from bots.admin_notifier_bot.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    try:
        logger.info("🟢 АДМИНИСТРАТИВНЫЙ БОТ УСПЕШНО ЗАПУЩЕН НА RAILWAY!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"🚨 Фатальная ошибка во время работы админ-бота: {e}")
    finally:
        logger.info("⏳ Закрываю сессии административного бота...")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
