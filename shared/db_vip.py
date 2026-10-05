import asyncpg
from shared.database import db

async def check_and_buy_vip_id(user_id: int, vip_id: str) -> str:
    """
    Офис Регистрации VIP ID.
    Проверяет баланс (цена: 100 000 Рофлов), уникальность VIP ID,
    списывает монеты и намертво вшивает имя в таблицу users.
    """
    if not db.pool:
        return "Ошибка соединения с базой"

    # Очищаем ввод от лишних пробелов и переводим в верхний регистр
    vip_id = vip_id.strip().upper()

    if len(vip_id) < 3 or len(vip_id) > 15:
        return "⚠️ Длина VIP ID должна быть от 3 до 15 символов!"

    async with db.pool.acquire() as conn:
        # Открываем транзакцию — либо всё запишется, либо всё откатится
        tx = conn.transaction()
        await tx.start()
        try:
            # 1. Проверяем баланс покупателя
            user_balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", user_id)
            if user_balance is None:
                await tx.rollback()
                return "Юзер не найден в базе"
            if user_balance < 100000:
                await tx.rollback()
                return "❌ Недостаточно рофлов! Покупка VIP ID стоит 100 000 монет."

            # 2. Проверяем, не занят ли этот VIP ID кем-то другим
            is_taken = await conn.fetchval("SELECT user_id FROM users WHERE rofl_hub_id = $1", vip_id)
            if is_taken:
                await tx.rollback()
                return f"⚠️ Красивый ID <b>{vip_id}</b> уже выкуплен другим Олигархом!"

            # 3. Списываем 100 000 Рофлов
            await conn.execute("UPDATE users SET balance = balance - 100000 WHERE user_id = $1", user_id)

            # 4. Вбиваем VIP ID в ДНК юзера
            await conn.execute("UPDATE users SET rofl_hub_id = $1 WHERE user_id = $2", vip_id, user_id)

            await tx.commit()
            return "OK"
        except Exception as e:
            await tx.rollback()
            print(f"❌ [DB_VIP] Ошибка покупки VIP ID: {e}")
            return f"Ошибка базы данных: {e}"
