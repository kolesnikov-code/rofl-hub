"""
Переводы монет между игроками: /transfer <ID или @username> <сумма>.

Двухшаговый контур: проверка → кнопка подтверждения (привязана к отправителю)
→ транзакция в shared/transfers.transfer_coins (FOR UPDATE, ledger).
"""
from __future__ import annotations

import html
import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from shared.database import db
from shared.economy import TRANSFER_MIN_AMOUNT, transfer_fee
from shared.locales import resolve_lang, t
from shared.transfers import TransferError, ensure_sender_active, transfer_coins

router = Router()
logger = logging.getLogger(__name__)


async def _resolve_recipient(conn, raw: str) -> dict | None:
    """ID, @username или VIP ID с аукциона → строка users (или None)."""
    raw = raw.strip()
    alive = " AND deleted_at IS NULL AND deletion_requested_at IS NULL"   # удалённых не видно
    if raw.startswith("@"):
        return await conn.fetchrow(
            "SELECT user_id, username, display_name, is_blocked FROM users WHERE LOWER(username) = LOWER($1)"
            + alive, raw[1:])
    if raw.isdigit():
        return await conn.fetchrow(
            "SELECT user_id, username, display_name, is_blocked FROM users WHERE user_id = $1" + alive, int(raw))
    # VIP ID (например BARON-777) — равноправный айдишник для переводов
    return await conn.fetchrow(
        "SELECT u.user_id, u.username, u.display_name, u.is_blocked "
        "FROM vip_aliases v JOIN users u ON u.user_id = v.user_id "
        "WHERE UPPER(v.alias) = UPPER($1)", raw)


def _recipient_label(rec: dict) -> str:
    if rec["username"]:
        return f"@{html.escape(rec['username'])}"
    return html.escape(rec["display_name"] or f"ID {rec['user_id']}")


@router.message(Command("transfer"))
@router.message(Command("send"))
async def cmd_transfer(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "transfers", user_lang):
        return
    sender_id = message.from_user.id
    parts = (message.text or "").split()

    if len(parts) != 3 or not parts[2].isdigit():
        await message.answer(t(user_lang, "tr.help", min=TRANSFER_MIN_AMOUNT), parse_mode="HTML")
        return  # формат: /transfer <ID | @username | VIP ID> <сумма>
    amount = int(parts[2])

    async with db.pool.acquire() as conn:
        sender = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1", sender_id)
        if not sender:
            await message.answer(t(user_lang, "common.no_profile"))
            return
        try:
            await ensure_sender_active(conn, sender_id)
        except TransferError as e:
            await message.answer(e.localized(user_lang))
            return
        recipient = await _resolve_recipient(conn, parts[1])

    if recipient is None:
        await message.answer(t(user_lang, "tr.not_found"))
        return
    if recipient["user_id"] == sender_id:
        await message.answer(t(user_lang, "tr.self"))
        return
    if recipient["is_blocked"]:
        await message.answer(t(user_lang, "tr.blocked"))
        return
    if amount < TRANSFER_MIN_AMOUNT:
        await message.answer(t(user_lang, "tr.min", min=TRANSFER_MIN_AMOUNT))
        return
    if sender["balance"] < amount:
        await message.answer(t(user_lang, "tr.insufficient", balance=sender["balance"]), parse_mode="HTML")
        return

    fee = transfer_fee(amount)
    fee_line = t(user_lang, "tr.fee_line", fee=fee) if fee else ""
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=t(user_lang, "tr.btn_confirm"),
            callback_data=f"tr_go:{sender_id}:{recipient['user_id']}:{amount}")],
        [types.InlineKeyboardButton(text=t(user_lang, "tr.btn_cancel"), callback_data="tr_cancel")],
    ])
    await message.answer(
        t(user_lang, "tr.confirm",
          recipient=_recipient_label(recipient), recipient_id=recipient["user_id"],
          amount=amount, fee_line=fee_line, received=amount - fee),
        reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "tr_cancel")
async def transfer_cancel(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer(t(user_lang, "tr.cancelled_toast"))
    try:
        await callback.message.edit_text(t(user_lang, "tr.cancelled"), parse_mode="HTML")
    except Exception:
        pass


@router.callback_query(F.data.startswith("tr_go:"))
async def transfer_confirm(callback: types.CallbackQuery, bot: Bot, user_lang: str = "ru"):
    parts = callback.data.split(":")
    if len(parts) != 4 or not all(p.lstrip("-").isdigit() for p in parts[1:]):
        await callback.answer()
        return
    sender_id, recipient_id, amount = int(parts[1]), int(parts[2]), int(parts[3])

    # Кнопку мог нажать только сам отправитель
    if callback.from_user.id != sender_id:
        await callback.answer(t(user_lang, "tr.not_yours"), show_alert=True)
        return

    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                received, sender_balance = await transfer_coins(conn, sender_id, recipient_id, amount)
            recipient_lang = resolve_lang(
                await conn.fetchval("SELECT lang FROM users WHERE user_id = $1", recipient_id))
    except TransferError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        return

    await callback.answer(t(user_lang, "tr.done_toast"))
    try:
        await callback.message.edit_text(
            t(user_lang, "tr.done", amount=amount, recipient_id=recipient_id, balance=sender_balance),
            parse_mode="HTML")
    except Exception:
        pass

    try:
        await bot.send_message(
            recipient_id,
            t(recipient_lang, "tr.received", amount=received, sender_id=sender_id),
            parse_mode="HTML")
    except Exception:
        logger.info("[TRANSFER] получатель %s недоступен для уведомления", recipient_id)
