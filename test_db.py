import asyncio
import sys
import os
from dotenv import load_dotenv
from shared import database

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

env_path = os.path.join('bots', 'main_bot', '.env')
load_dotenv(dotenv_path=env_path)


async def main():
    await database.init_db(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
    )
    print("✅ БД инициализирована. Таблица users создана.")

    code = database.generate_ref_code()
    print(f"🎲 Пример реферального кода: {code}")

    await database.close_db()
    print("✅ Соединение закрыто.")


if __name__ == '__main__':
    asyncio.run(main())