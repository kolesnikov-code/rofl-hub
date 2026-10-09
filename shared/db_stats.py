import asyncpg
from shared.database import db


async def get_complete_user_data(user_id: int) -> dict:
    """
    Вытаскивает полный срез ДНК профиля игрока из PostgreSQL на Railway.
    Обеспечивает данными ленивый движок начисления и графический конвейер Pillow.
    """
    if not db.pool:
        return None

    async with db.pool.acquire() as conn:
        try:
            # 🎯 Забираем абсолютно все поля из users (включая холодильник, время и роботов)
            row = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
            if not row:
                return None

            # Забираем игровую аналитику дуэлей
            g_row = await conn.fetchrow(
                "SELECT games_played, games_won FROM game_stats WHERE user_id = $1",
                user_id
            )

            # Считаем живую банду рефералов из базы
            ref_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1", user_id)

            # Собираем монолитный словарь данных под новые нужды profile.py и движка
            return {
                "balance": row["balance"],
                "rofl_hub_id": row["rofl_hub_id"],
                "referred_by": row["referred_by"],
                "created_at": row["created_at"],
                "team_id": row["team_id"],

                # 📦 Твой обновленный центральный топливный хаб
                "fridge_capacity": row["fridge_capacity"],
                "fridge_cutlets": row["fridge_cutlets"],
                "inv_cutlets": row["inv_cutlets"],

                # 🤖 Новые счетчики активных роботов-майнеров
                "miner_junior_count": row["miner_junior_count"],
                "miner_premium_count": row["miner_premium_count"],

                # ⏳ Временная метка для ленивых вычислений пассивного дохода
                "last_update_time": row["last_update_time"],

                # Игровые метрики из таблицы game_stats (если строки нет — ставим нули)
                "games_played": g_row["games_played"] if g_row else 0,
                "games_won": g_row["games_won"] if g_row else 0,
                "ref_count": ref_count or 0
            }
        except Exception as e:
            print(f"[DB_STATS] Критическая ошибка сборки данных: {e}")
            return None
