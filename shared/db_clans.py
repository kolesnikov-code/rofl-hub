"""Создание команды: одна транзакция, FOR UPDATE, списание через ledger."""
from __future__ import annotations

import logging

from shared.database import db
from shared.economy import TEAM_CREATE_COST
from shared.ledger import InsufficientFunds, change_balance

logger = logging.getLogger(__name__)


async def leave_team(conn, user_id: int, team_id: int | None = None) -> dict | None:
    """
    Выход игрока из команды (внутри транзакции вызывающего). Капитан передаёт корону тому,
    кто вступил раньше всех (кроме заблокированных и уходящих из экосистемы); один в команде —
    команда расформировывается. team_id — ожидаемая команда (защита от устаревшей кнопки).
    Возвращает {"team_id", "team_name", "outcome": "left"|"passed"|"disbanded", "new_captain"}
    или None, если игрок не в этой команде.
    """
    current = await conn.fetchval("SELECT team_id FROM users WHERE user_id = $1", user_id)
    if current is None or (team_id is not None and current != team_id):
        return None
    # Порядок блокировок как во всём коде: сначала команда, потом игрок
    team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1 FOR UPDATE", current)
    user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user or user["team_id"] != current:
        return None
    clear_user = "UPDATE users SET team_id = NULL, team_joined_at = NULL WHERE user_id = $1"
    if not team:
        await conn.execute(clear_user, user_id)
        return None
    result = {"team_id": current, "team_name": team["team_name"], "outcome": "left", "new_captain": None}
    if team["captain_id"] == user_id:
        next_captain = await conn.fetchrow(
            "SELECT user_id, username FROM users WHERE team_id = $1 AND user_id != $2 "
            "AND NOT is_blocked AND deletion_requested_at IS NULL "
            "ORDER BY team_joined_at ASC NULLS LAST, user_id ASC LIMIT 1",
            current, user_id)
        if next_captain:
            await conn.execute(
                "UPDATE teams SET captain_id = $1, members_count = members_count - 1 WHERE team_id = $2",
                next_captain["user_id"], current)
            result.update(outcome="passed", new_captain=dict(next_captain))
        else:
            # Остались только заблокированные/уходящие — их тоже отвязываем, команды больше нет
            await conn.execute(
                "UPDATE users SET team_id = NULL, team_joined_at = NULL WHERE team_id = $1", current)
            await conn.execute("DELETE FROM teams WHERE team_id = $1", current)
            result["outcome"] = "disbanded"
    else:
        await conn.execute("UPDATE teams SET members_count = members_count - 1 WHERE team_id = $1", current)
    await conn.execute(clear_user, user_id)
    return result


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
                return False, (f"❌ Недостаточно монет! Твой баланс: {user['balance']:,} из "
                               f"{TEAM_CREATE_COST:,} необходимых.").replace(",", " ")

            if await conn.fetchval("SELECT team_id FROM teams WHERE captain_id = $1", captain_id):
                return False, "⚠️ Ты уже являешься Капитаном другой команды!"
            if await conn.fetchval("SELECT team_id FROM teams WHERE team_name = $1", team_name):
                return False, f"⚠️ Название «{team_name}» уже занято! Придумай уникальное."

            try:
                await change_balance(conn, captain_id, -TEAM_CREATE_COST, "team_create", team_name)
            except InsufficientFunds:
                return False, "❌ Недостаточно монет."

            team_id = await conn.fetchval(
                """
                INSERT INTO teams (team_name, captain_id, city, school_num)
                VALUES ($1, $2, $3, $4) RETURNING team_id
                """,
                team_name, captain_id, city, school,
            )
            await conn.execute(
                "UPDATE users SET team_id = $1, team_joined_at = NOW() WHERE user_id = $2",
                team_id, captain_id)
            logger.info("[TEAM_CREATED] team=%s captain=%s", team_id, captain_id)
            return True, "OK"
