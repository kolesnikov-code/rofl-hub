"""
Журнал движения рофлов. Любое изменение баланса — только через change_balance().

Гарантии:
- баланс не уходит в минус (проверка в самом UPDATE, атомарно);
- каждая операция записана в ledger (кто, сколько, за что, ссылка на объект);
- вызывается ВНУТРИ транзакции вызывающего кода (conn уже в conn.transaction()).
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class InsufficientFunds(Exception):
    pass


class UserNotFound(Exception):
    pass


async def change_balance(conn, user_id: int, delta: int, reason: str, ref: str | None = None) -> int:
    """
    Атомарно меняет баланс на delta и пишет строку в ledger.
    Возвращает новый баланс. Бросает InsufficientFunds / UserNotFound.
    """
    if delta == 0:
        row = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1", user_id)
        if row is None:
            raise UserNotFound(user_id)
        return row["balance"]

    new_balance = await conn.fetchval(
        """
        UPDATE users
        SET balance = balance + $2
        WHERE user_id = $1 AND balance + $2 >= 0
        RETURNING balance
        """,
        user_id, delta,
    )
    if new_balance is None:
        exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1", user_id)
        if not exists:
            raise UserNotFound(user_id)
        raise InsufficientFunds(user_id)

    await conn.execute(
        "INSERT INTO ledger (user_id, delta, reason, ref) VALUES ($1, $2, $3, $4)",
        user_id, delta, reason, ref,
    )
    return new_balance
