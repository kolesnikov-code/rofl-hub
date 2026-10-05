import asyncio
from datetime import datetime
from shared.database import db

async def register_new_user(user_id: int, username: str, referred_by: int = None) -> bool:
    if not db.pool:
        print("[DB_USERS] нет соединения с пулом базы данных.")
        return False

    async with db.pool.acquire() as conn:
        try:
            user_exists = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", user_id)
            if user_exists:
                return False

            await conn.execute(
                """
                INSERT INTO miners (user_id, miner_type, cutlets_inside, miner_charge)
                    VALUES ($1, 'none', 1, 100)
                """,
                user_id
            )

            await conn.execute(INSERT INTO game_stats (user_id) VALUES ($1)", user_id)
            print(f"[DB] Империя выросла! Юзер {user_id} (@{username}) инициализирован.")

            if referred_by and referred_by != user_id:
                referer_exists = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", referred_by)
                if referer_exists:
                    await conn.execute(
                        "UPDATE users SET balance = balance + 1000 WHERE user_id = $1", referred_by)
                    print(f"[DB] Лавина пошла!")
            return True

        except Exception as e:
            print(f"[DB_USERS] критическая ошибка при регистрации: {e}")
            return False
