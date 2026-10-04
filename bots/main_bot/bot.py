import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.help import router as help_router
from bots.main_bot.handlers.faq import router as faq_router

#from bots.main_bot.handlers.balance import router as balance_router
#from bots.main_bot.handlers.buy_coins import router as buy_coins_router
#from bots.main_bot.handlers.buy_post import router as buy_post_router
#from bots.main_bot.handlers.buy_vip import router as buy_vip_router
#from bots.main_bot.handlers.catalog import router as catalog_router
#from bots.main_bot.handlers.my_id import router as my_id_router
#from bots.main_bot.handlers.my_stats import router as my_stats_router
#from bots.main_bot.handlers.referral import router as referral_router
#from bots.main_bot.handlers.send_coin import router as send_coin_router
#from bots.main_bot.handlers.support import router as support_router

load_dotenv()

TOKEN = getenv("USER_BOT_TOKEN")
ADMIN_CHANNEL_ID = getenv("ADMIN_SECRET_CHANNEL_ID")

async def main():
    dp = Dispatcher()

    from shared.database import db
    await db.connect()
    await db.create_tables()

    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(faq_router)

    bot = Bot(token=TOKEN)

    print("🚀 ГЛАВНЫЙ БОТ ЮЗЕРОВ УСПЕШНО ЗАПУЩЕН НА ЛОКАЛЬНОМ ХОСТЕ!")

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

