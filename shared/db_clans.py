import asyncpg
from shared.database import db


async def create_new_team_in_db(captain_id: int, team_name: str, city: str, school: str) -> tuple[bool, str]:
    """
    Единый Генеральный Офис Регистрации Команд.
    Объединяет проверку и списание в одну атомарную транзакцию с блокировкой FOR UPDATE.
    Исключает дюп кланов, Race Condition и уход баланса в минус.
    Возвращает (Успех: bool, Текст_Ошибки/Статус: str).
    """
    if not db.pool:
        return False, "Ошибка пула БД"

    async with db.pool.acquire() as conn:
        # Включаем официальный контекстный менеджер транзакций asyncpg
        async with conn.transaction():
            try:
                # ------------------------------------------------------------
                # ШАГ 1: НАВЕШИВАЕМ ТИТАНОВЫЙ ЗАМОК (FOR UPDATE) НА СТРОКУ ЮЗЕРА
                # ------------------------------------------------------------
                user = await conn.fetchrow(
                    "SELECT balance, team_id FROM users WHERE user_id = $1 FOR UPDATE",
                    captain_id
                )

                if not user:
                    return False, "Юзер не найден в базе данных. Нажми /start"

                if user["team_id"] is not None:
                    return False, "⚠️ Ты уже состоишь в команде или клане!"

                if user["balance"] < 100000:
                    return False, f"❌ Недостаточно рофлов! Твой баланс: {user['balance']} из 100 000 необходимых."

                # ------------------------------------------------------------
                # ШАГ 2: ПРОВЕРКА НА СУЩЕСТВОВАНИЕ КАПИТАНСТВА В ДРУГОЙ ТАБЛИЦЕ
                # ------------------------------------------------------------
                is_captain = await conn.fetchval("SELECT team_id FROM teams WHERE captain_id = $1", captain_id)
                if is_captain:
                    return False, "⚠️ Ты уже являешься Капитаном другой команды!"

                # Проверяем уникальность имени банды, чтобы избежать дублей по UNIQUE ограничению
                name_exists = await conn.fetchval("SELECT team_id FROM teams WHERE team_name = $1", team_name)
                if name_exists:
                    return False, f"⚠️ Название '{team_name}' уже занято другой бандой! Придумай уникальное."

                # ------------------------------------------------------------
                # ШАГ 3: АТОМАРНАЯ СИНХРОНИЗАЦИЯ: СПИСАНИЕ, ЗАПИСЬ И ПРИВЯЗКА
                # ------------------------------------------------------------
                # 1. Списываем 100 000 Рофлов у Капитана
                await conn.execute("UPDATE users SET balance = balance - 100000 WHERE user_id = $1", captain_id)

                # 2. Создаем строку в таблице teams
                team_id = await conn.fetchval(
                    """
                    INSERT INTO teams (team_name, captain_id, city, school_num)
                    VALUES ($1, $2, $3, $4) RETURNING team_id
                    """,
                    team_name, captain_id, city, school
                )

                # 3. Привязываем Капитана к созданной команде в таблице users
                await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = $2", team_id, captain_id)

                print(f"👥 [DB_CLANS] Команда '{team_name}' успешно создана капитаном {captain_id}! 100к списано.")
                return True, "OK"

            except Exception as e:
                # Внутри asyncpg блок conn.transaction() сам сделает ROLLBACK при любой ошибке!
                print(f"❌ [DB_CLANS] Критический краш транзакции создания команды: {e}")
                return False, "Произошла внутренняя ошибка сервера базы данных на Railway."
