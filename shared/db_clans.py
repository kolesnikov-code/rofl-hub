"""Создание команды: одна транзакция, FOR UPDATE, списание через ledger."""
from __future__ import annotations

import logging

from shared.database import db
from shared.economy import TEAM_CREATE_COST
from shared.ledger import InsufficientFunds, change_balance

logger = logging.getLogger(__name__)


async def create_new_team_in_db(captain_id: int, team_name: str, city: str, school: str) -> tuple[bool, str]:
    """Возвращает (успех, статус/ошибка)."""
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow(
                "SELECT balance, team_id FROM users WHERE user_id = $1 FOR UPDATE", captain_id)
            if not user:
                return False, "Профиль не найден. Нажми /start"
            if user["team_id"] is not None:
                return False, "⚠️ Ты уже состоишь в команде или клане!"
            if user["balance"] < TEAM_CREATE_COST:
                return False, (f"❌ Недостаточно рофлов! Твой баланс: {user['balance']:,} из "
                               f"{TEAM_CREATE_COST:,} необходимых.").replace(",", " ")

            if await conn.fetchval("SELECT team_id FROM teams WHERE captain_id = $1", captain_id):
                return False, "⚠️ Ты уже являешься Капитаном другой команды!"
            if await conn.fetchval("SELECT team_id FROM teams WHERE team_name = $1", team_name):
                return False, f"⚠️ Название «{team_name}» уже занято! Придумай уникальное."

            try:
                await change_balance(conn, captain_id, -TEAM_CREATE_COST, "team_create", team_name)
            except InsufficientFunds:
                return False, "❌ Недостаточно рофлов."

            team_id = await conn.fetchval(
                """
                INSERT INTO teams (team_name, captain_id, city, school_num)
                VALUES ($1, $2, $3, $4) RETURNING team_id
                """,
                team_name, captain_id, city, school,
            )
            await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = $2", team_id, captain_id)
            logger.info("[TEAM_CREATED] team=%s captain=%s", team_id, captain_id)
            return True, "OK"
