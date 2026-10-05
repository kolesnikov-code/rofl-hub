import asyncpg
from shared.database import db

async def get_complete_user_data(user_id: int) -> dict:
    if not db.pool:
        return None
    async with db.pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                """
                SELECT u.balance, u.rofl_hub_id, u.inv_cutlets, g.games_played, g.games_won
                FROM users u
                JOIN game_stats g ON u.user_id = g.user_id
                WHERE u.user_id = $1
                """,
                user_id
            )
            if not row:
                return None

            ref_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1", user_id)

            return {
                "balance": row["balance"],
                "rofl_hub_id": row["rofl_hub_id"],
                "inv_cutlets": row["inv_cutlets"],
                "games_played": row["games_played"],
                "games_won": row["games_won"],
                "ref_count": ref_count or 0
            }
        except Exception as e:
            print(f"[DB_STATS] Ошибка сборки данных: {e}")
            return None