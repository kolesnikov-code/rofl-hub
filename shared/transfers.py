"""
Перевод монет между игроками. Ядро без Telegram: только asyncpg-соединение.

Гарантии:
- обе строки users блокируются FOR UPDATE в порядке возрастания user_id (анти-дедлок);
- списание и зачисление — через ledger (reasons: transfer_out / transfer_in);
- комиссия TRANSFER_FEE_PERCENT сжигается (списана, но не зачислена).
"""
from __future__ import annotations

import logging

from shared.economy import TRANSFER_MIN_AMOUNT, transfer_fee
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import t

logger = logging.getLogger(__name__)


class TransferError(Exception):
    """Причина отказа в переводе: ключ локали + параметры (локализуется в обработчике)."""

    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(t("ru", key, **kwargs))

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


async def transfer_coins(conn, sender_id: int, recipient_id: int, amount: int) -> tuple[int, int]:
    """
    Выполняет перевод внутри транзакции вызывающего кода.
    Возвращает (получено адресатом, новый баланс отправителя). Бросает TransferError.
    """
    if sender_id == recipient_id:
        raise TransferError("tr.self")
    if amount < TRANSFER_MIN_AMOUNT:
        raise TransferError("tr.min", min=TRANSFER_MIN_AMOUNT)

    rows = await conn.fetch(
        "SELECT user_id, is_blocked FROM users WHERE user_id = ANY($1::bigint[]) "
        "ORDER BY user_id FOR UPDATE",
        [sender_id, recipient_id],
    )
    by_id = {r["user_id"]: r for r in rows}
    if sender_id not in by_id:
        raise TransferError("common.no_profile")
    if recipient_id not in by_id:
        raise TransferError("tr.not_found")
    if by_id[recipient_id]["is_blocked"]:
        raise TransferError("tr.blocked")

    try:
        sender_balance = await change_balance(conn, sender_id, -amount, "transfer_out", str(recipient_id))
    except InsufficientFunds:
        raise TransferError("tr.err_insufficient")

    received = amount - transfer_fee(amount)
    await change_balance(conn, recipient_id, received, "transfer_in", str(sender_id))
    logger.info("[TRANSFER] %s -> %s amount=%s received=%s", sender_id, recipient_id, amount, received)
    return received, sender_balance
