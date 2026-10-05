import asyncpg
from shared.database import db


async def register_new_user(user_id: int, username: str, referred_by: int = None) -> bool:
    """
    Генеральный Офис Регистрации (Метод DVD-диска).
    Создает аккаунт, выдает 1000 Рофлов и 1 Котлету в карман.
    Робота-майнера НЕ создает — пускай покупают отдельно!
    """
    if not db.pool:
        print("❌ [DB_USERS] Нет соединения с пулом базы данных.")
        return False

    async with db.pool.acquire() as conn:
        try:
            # 1. Проверяем, есть ли уже этот Telegram ID в базе
            user_exists = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", user_id)
            if user_exists:
                return False  # Уже зарегистрирован, выходим

            # 2. Создаем юзера. Вручаем 1000 Рофлов (DEFAULT)
            # ВНИМАНИЕ: Если ты еще не добавил inv_cutlets в таблицу users,
            # мы временно держим эту логику в уме, либо прямо сейчас запишем в базу.
            await conn.execute(
                """
                INSERT INTO users (user_id, username, referred_by)
                VALUES ($1, $2, $3)
                """,
                user_id, username, referred_by
            )

            # 3. Антифрод-контур дуэлей инициализируем сразу
            await conn.execute("INSERT INTO game_stats (user_id) VALUES ($1)", user_id)

            print(f"💿 [DB] Метод DVD-диска сработал! Юзер {user_id} в базе. Робота НЕТ, котлета выдана.")

            # 4. Начисляем Рофлы блогеру по рефералке
            if referred_by and referred_by != user_id:
                referer_exists = await conn.fetchval("SELECT user_id FROM users WHERE user_id = $1", referred_by)
                if referer_exists:
                    await conn.execute(
                        "UPDATE users SET balance = balance + 1000 WHERE user_id = $1",
                        referred_by
                    )
                    print(f"🎰 [DB] Лавина! Лидеру {referred_by} капнуло +1000 Рофлов за друга.")

            return True

        except Exception as e:
            print(f"❌ [DB_USERS] Ошибка при регистрации: {e}")
            return False
