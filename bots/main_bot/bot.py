import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from bots.main_bot.handlers.start import router as start_router
from bots.main_bot.handlers.menu import router as help_router
from bots.main_bot.handlers.faq import router as faq_router
from bots.main_bot.handlers.rofl_hub_all import router as rofl_hub_all_router
from bots.main_bot.handlers.rules import router as rules_router
from bots.main_bot.handlers.profile import router as profile_router
from bots.main_bot.handlers.clans import router as clans_router
from bots.main_bot.handlers.shop import router as shop_router
from bots.main_bot.handlers.vip_shop import router as vip_shop_router
from bots.main_bot.handlers import games
from bots.main_bot.handlers import farm

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
    dp.include_router(rofl_hub_all_router)
    dp.include_router(rules_router)
    dp.include_router(profile_router)
    dp.include_router(clans_router)
    dp.include_router(shop_router)
    dp.include_router(vip_shop_router)
    dp.include_router(games.router)
    dp.include_router(farm.router)

    bot = Bot(token=TOKEN)

    print("🚀 ГЛАВНЫЙ БОТ ЮЗЕРОВ УСПЕШНО ЗАПУЩЕН НА ЛОКАЛЬНОМ ХОСТЕ!")

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

