"""
Перевод рофлов между игроками. Ядро без Telegram: только asyncpg-соединение.

Гарантии:
- обе строки users блокируются FOR UPDATE в порядке возрастания user_id (анти-дедлок);
- списание и зачисление — через ledger (reasons: transfer_out / transfer_in);
- комиссия TRANSFER_FEE_PERCENT сжигается (списана, но не зачислена).
"""
from __future__ import annotations

import logging

from shared.economy import TRANSFER_MIN_AMOUNT, transfer_fee
from shared.ledger import InsufficientFunds, change_balance

logger = logging.getLogger(__name__)


class TransferError(Exception):
    """Человекочитаемая причина отказа в переводе."""


async def transfer_coins(conn, sender_id: int, recipient_id: int, amount: int) -> tuple[int, int]:
    """
    Выполняет перевод внутри транзакции вызывающего кода.
    Возвращает (получено адресатом, новый баланс отправителя). Бросает TransferError.
    """
    if sender_id == recipient_id:
        raise TransferError("Нельзя перевести монеты самому себе.")
    if amount < TRANSFER_MIN_AMOUNT:
        raise TransferError(f"Минимальная сумма перевода — {TRANSFER_MIN_AMOUNT} рофлов.")

    rows = await conn.fetch(
        "SELECT user_id, is_blocked FROM users WHERE user_id = ANY($1::bigint[]) "
        "ORDER BY user_id FOR UPDATE",
        [sender_id, recipient_id],
    )
    by_id = {r["user_id"]: r for r in rows}
    if sender_id not in by_id:
        raise TransferError("Твой профиль не найден. Нажми /start")
    if recipient_id not in by_id:
        raise TransferError("Получатель не найден. Проверь ID Паспорта — он виден в /profile.")
    if by_id[recipient_id]["is_blocked"]:
        raise TransferError("Этот игрок заблокирован — переводы ему недоступны.")

    try:
        sender_balance = await change_balance(conn, sender_id, -amount, "transfer_out", str(recipient_id))
    except InsufficientFunds:
        raise TransferError("Недостаточно рофлов на балансе.")

    received = amount - transfer_fee(amount)
    await change_balance(conn, recipient_id, received, "transfer_in", str(sender_id))
    logger.info("[TRANSFER] %s -> %s amount=%s received=%s", sender_id, recipient_id, amount, received)
    return received, sender_balance
