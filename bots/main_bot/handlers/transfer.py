"""
Переводы рофлов между игроками: /transfer <ID или @username> <сумма>.

Двухшаговый контур: проверка → кнопка подтверждения (привязана к отправителю)
→ транзакция в shared/transfers.transfer_coins (FOR UPDATE, ledger).
"""
from __future__ import annotations

import html
import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from shared.database import db
from shared.economy import TRANSFER_FEE_PERCENT, TRANSFER_MIN_AMOUNT, transfer_fee
from shared.transfers import TransferError, transfer_coins

router = Router()
logger = logging.getLogger(__name__)

HELP_TEXT = (
    f"🔄 <b>ПЕРЕВОД РОФЛОВ ДРУГОМУ ИГРОКУ</b>\n"
    f"..................................................\n\n"
    f"Формат команды:\n"
    f"<code>/transfer ID сумма</code> — по ID Паспорта (виден в /profile)\n"
    f"<code>/transfer @username сумма</code> — по юзернейму\n\n"
    f"Примеры:\n"
    f"<code>/transfer 123456789 500</code>\n"
    f"<code>/transfer @friend 100</code>\n\n"
    f"📌 Минимальная сумма: <b>{TRANSFER_MIN_AMOUNT} рофлов</b>"
    + (f"\n🔥 Комиссия хаба: <b>{TRANSFER_FEE_PERCENT}%</b> (сжигается)" if TRANSFER_FEE_PERCENT else "")
)


async def _resolve_recipient(conn, raw: str) -> dict | None:
    """ID или @username → строка users (или None)."""
    raw = raw.strip()
    if raw.startswith("@"):
        return await conn.fetchrow(
            "SELECT user_id, username, display_name, is_blocked FROM users WHERE LOWER(username) = LOWER($1)",
            raw[1:])
    if raw.isdigit():
        return await conn.fetchrow(
            "SELECT user_id, username, display_name, is_blocked FROM users WHERE user_id = $1", int(raw))
    return None


def _recipient_label(rec: dict) -> str:
    if rec["username"]:
        return f"@{html.escape(rec['username'])}"
    return html.escape(rec["display_name"] or f"Игрок {rec['user_id']}")


@router.message(Command("transfer"))
@router.message(Command("send"))
async def cmd_transfer(message: types.Message):
    sender_id = message.from_user.id
    parts = (message.text or "").split()

    if len(parts) != 3 or not parts[2].isdigit():
        await message.answer(HELP_TEXT, parse_mode="HTML")
        return
    amount = int(parts[2])

    async with db.pool.acquire() as conn:
        sender = await conn.fetchrow("SELECT balance FROM users WHERE user_id = $1", sender_id)
        if not sender:
            await message.answer("⚠️ Профиль не найден. Нажми /start")
            return
        recipient = await _resolve_recipient(conn, parts[1])

    if recipient is None:
        await message.answer("❌ Получатель не найден. Проверь ID Паспорта или @username — "
                             "игрок должен быть зарегистрирован в боте.")
        return
    if recipient["user_id"] == sender_id:
        await message.answer("🤨 Перевести монеты самому себе нельзя — это была бы вечная экономика!")
        return
    if recipient["is_blocked"]:
        await message.answer("🚫 Этот игрок заблокирован — переводы ему недоступны.")
        return
    if amount < TRANSFER_MIN_AMOUNT:
        await message.answer(f"❌ Минимальная сумма перевода — {TRANSFER_MIN_AMOUNT} рофлов.")
        return
    if sender["balance"] < amount:
        await message.answer(f"❌ Недостаточно рофлов! Твой баланс: <b>{sender['balance']}</b>.",
                             parse_mode="HTML")
        return

    fee = transfer_fee(amount)
    received = amount - fee
    fee_line = f"\n🔥 Комиссия хаба: <b>{fee} рофлов</b> (сгорит)" if fee else ""
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="✅ ПОДТВЕРДИТЬ ПЕРЕВОД",
            callback_data=f"tr_go:{sender_id}:{recipient['user_id']}:{amount}")],
        [types.InlineKeyboardButton(text="❌ Отмена", callback_data="tr_cancel")],
    ])
    await message.answer(
        f"🔄 <b>ПОДТВЕРДИ ПЕРЕВОД:</b>\n\n"
        f"👤 Получатель: <b>{_recipient_label(recipient)}</b> (ID <code>{recipient['user_id']}</code>)\n"
        f"💸 Сумма списания: <b>{amount} рофлов</b>{fee_line}\n"
        f"💰 Адресат получит: <b>{received} рофлов</b>\n\n"
        f"<i>Переводы отменить нельзя — проверь получателя!</i>",
        reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "tr_cancel")
async def transfer_cancel(callback: types.CallbackQuery):
    await callback.answer("Перевод отменён")
    try:
        await callback.message.edit_text("❌ <b>Перевод отменён.</b> Монеты остались на месте.", parse_mode="HTML")
    except Exception:
        pass


@router.callback_query(F.data.startswith("tr_go:"))
async def transfer_confirm(callback: types.CallbackQuery, bot: Bot):
    parts = callback.data.split(":")
    if len(parts) != 4 or not all(p.lstrip("-").isdigit() for p in parts[1:]):
        await callback.answer()
        return
    sender_id, recipient_id, amount = int(parts[1]), int(parts[2]), int(parts[3])

    # Кнопку мог нажать только сам отправитель
    if callback.from_user.id != sender_id:
        await callback.answer("🔒 Это не твой перевод!", show_alert=True)
        return

    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                received, sender_balance = await transfer_coins(conn, sender_id, recipient_id, amount)
    except TransferError as e:
        await callback.answer(str(e), show_alert=True)
        return

    await callback.answer("✅ Перевод выполнен!")
    try:
        await callback.message.edit_text(
            f"✅ <b>ПЕРЕВОД ВЫПОЛНЕН!</b>\n\n"
            f"💸 Отправлено: <b>{amount} рофлов</b> игроку ID <code>{recipient_id}</code>\n"
            f"💰 Твой баланс: <b>{sender_balance} рофлов</b>",
            parse_mode="HTML")
    except Exception:
        pass

    try:
        await bot.send_message(
            recipient_id,
            f"💰 <b>Тебе перевели {received} рофлов!</b>\n"
            f"Отправитель: ID <code>{sender_id}</code>. Баланс уже пополнен — проверь /profile!",
            parse_mode="HTML")
    except Exception:
        logger.info("[TRANSFER] получатель %s недоступен для уведомления", recipient_id)
