import asyncio
import sys
import os
from dotenv import load_dotenv
from shared import database

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

env_path = os.path.join('bots', 'main-bot', '.env')
load_dotenv(dotenv_path=env_path)

async def main():
    await database.init_db(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
    )
    print("✅ БД инициализирована")

    # Создаём юзера
    user1 = await database.add_user(
        platform="telegram",
        telegram_id=111111111,
        username="tester_one",
        first_name="Тестер Один",
        gender="m",
    )
    print(f"👤 Юзер 1: {user1['eco_id']}, баланс={user1['balance']}, ref_code={user1['ref_code']}")

    # Второй юзер
    user2 = await database.add_user(
        platform="telegram",
        telegram_id=222222222,
        username="tester_two",
        first_name="Тестер Два",
    )
    print(f"👤 Юзер 2: {user2['eco_id']}, баланс={user2['balance']}")

    # Ежедневка
    daily = await database.claim_daily(111111111)
    print(f"📅 Ежедневка: {daily['message']}")

    # Повтор
    daily_again = await database.claim_daily(111111111)
    print(f"📅 Повтор: {daily_again['message']}")

    # Перевод
    transfer = await database.transfer_coins(111111111, user2['eco_id'], 200)
    print(f"💸 Перевод: {transfer['message']}")

    # Реферал
    await database.register_referral(222222222, 111111111)
    print("🤝 Реферал зарегистрирован")

    # Балансы
    u1 = await database.get_user_by_telegram_id(111111111)
    u2 = await database.get_user_by_telegram_id(222222222)
    print(f"💰 Баланс юзера 1: {u1['balance']}")
    print(f"💰 Баланс юзера 2: {u2['balance']}")

    await database.close_db()
    print("\n🎉 Всё работает.")

if __name__ == '__main__':
    asyncio.run(main())