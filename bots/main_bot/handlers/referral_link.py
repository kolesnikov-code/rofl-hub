"""
Реферальная программа: персональная ссылка, счётчик друзей, заработок.

Deep-link формата t.me/<bot>?start=<user_id> уже обрабатывается в start.py
(register_user начисляет рефереру REFERRAL_SIGNUP_BONUS через ledger).
"""
from __future__ import annotations

import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from shared.database import db
from shared.economy import REFERRAL_SIGNUP_BONUS

router = Router()
logger = logging.getLogger(__name__)


async def _referral_stats(user_id: int) -> tuple[int, int] | None:
    """(приглашено друзей, заработано рофлов) или None, если профиля нет."""
    async with db.pool.acquire() as conn:
        exists = await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1", user_id)
        if not exists:
            return None
        invited = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1", user_id)
        earned = await conn.fetchval(
            "SELECT COALESCE(SUM(delta), 0) FROM ledger "
            "WHERE user_id = $1 AND reason = 'referral_signup'", user_id)
    return invited, earned


def referral_text(link: str, invited: int, earned: int) -> str:
    return (
        f"🤝 <b>РЕФЕРАЛЬНАЯ ПРОГРАММА ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"Приглашай друзей и получай <b>+{REFERRAL_SIGNUP_BONUS} рофлов</b> за каждого, "
        f"кто зарегистрируется по твоей персональной ссылке!\n\n"
        f"🔗 <b>Твоя ссылка (нажми, чтобы скопировать):</b>\n"
        f"<code>{link}</code>\n\n"
        f"📊 <b>ТВОЯ СТАТИСТИКА:</b>\n"
        f"👥 Приглашено друзей: <b>{invited} чел.</b>\n"
        f"💰 Заработано на рефералах: <b>{earned} рофлов</b>\n\n"
        f"..................................................\n"
        f"<i>Кидай ссылку в чаты класса, друзьям и в соцсети — чем больше банда, "
        f"тем быстрее растёт твой баланс!</i>"
    )


@router.message(Command("invite"))
@router.message(Command("ref"))
async def cmd_invite(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    stats = await _referral_stats(user_id)
    if stats is None:
        await message.answer("⚠️ Профиль не найден. Нажми /start для регистрации.")
        return

    me = await bot.me()
    link = f"https://t.me/{me.username}?start={user_id}"
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="📣 Поделиться ссылкой",
            url=f"https://t.me/share/url?url={link}&text=Залетай в игровую экосистему ROFL HUB!")],
        [types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")],
    ])
    await message.answer(referral_text(link, *stats), reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "open_referral")
async def open_referral_callback(callback: types.CallbackQuery, bot: Bot):
    await callback.answer()
    stats = await _referral_stats(callback.from_user.id)
    if stats is None:
        await callback.message.answer("⚠️ Профиль не найден. Нажми /start для регистрации.")
        return
    me = await bot.me()
    link = f"https://t.me/{me.username}?start={callback.from_user.id}"
    await callback.message.answer(referral_text(link, *stats), parse_mode="HTML")
