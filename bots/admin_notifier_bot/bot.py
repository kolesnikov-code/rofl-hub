from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("ADMIN_BOT_TOKEN")
ADMIN_CHANNEL_ID = getenv("ADMIN_SECRET_CHANNEL_ID")

dp = Dispatcher()
router = Router()
dp.include_router(router)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

