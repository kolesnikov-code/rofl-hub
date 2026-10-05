import asyncpg
from shared.database import db

async def check_user_can_create_team(user_id: int) -> str:
    """
    Офис Проверки Прав.
    Проверяет, имеет ли право юзер создать команду за 100 000 Рофлов.
    Возвращает 'OK' или текст ошибки.
    """
    if not db.pool: return "Ошибка пула БД"

    async with db.pool.acquire() as conn:
        # 1. Проверяем баланс и не состоит ли уже в команде
        user = await conn.fetchrow(
            "SELECT balance, team_id FROM users WHERE user_id = $1",
            user_id
        )
        if not user: return "Юзер не найден в базе"
        if user["team_id"] is not None: return "⚠️ Ты уже состоишь в команде или клане!"
        if user["balance"] < 100000: return "❌ Недостаточно рофлов! Создание команды стоит 100 000 монет."

        # 2. Проверяем, не является ли он уже капитаном другой команды
        is_captain = await conn.fetchval("SELECT team_id FROM teams WHERE captain_id = $1", user_id)
        if is_captain: return "⚠️ Ты уже Капитан другой команды!"

        return "OK"

async def create_new_team_in_db(captain_id: int, team_name: str, city: str, school: str) -> bool:
    """
    Генеральный Офис Регистрации Команд.
    Списывает 100 000 Рофлов, создает команду и привязывает Капитана.
    """
    if not db.pool: return False

    async with db.pool.acquire() as conn:
        # Открываем транзакцию (если один запрос упадет, все изменения откатятся назад!)
        tx = conn.transaction()
        await tx.start()
        try:
            # 1. Списываем 100 000 Рофлов у Капитана
            await conn.execute("UPDATE users SET balance = balance - 100000 WHERE user_id = $1", captain_id)

            # 2. Создаем строку в таблице teams
            team_id = await conn.fetchval(
                """
                INSERT INTO teams (team_name, captain_id, city, school_num)
                VALUES ($1, $2, $3, $4)
                RETURNING team_id
                """,
                team_name, captain_id, city, school
            )

            # 3. Привязываем Капитана к созданной команде в таблице users
            await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = $2", team_id, captain_id)

            await tx.commit()
            print(f"👥 [DB_CLANS] Команда '{team_name}' успешно создана капитаном {captain_id}!")
            return True
        except Exception as e:
            await tx.rollback()
            print(f"❌ [DB_CLANS] Ошибка создания команды: {e}")
            return False
