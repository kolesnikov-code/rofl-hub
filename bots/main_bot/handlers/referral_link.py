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
from shared.locales import t

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


@router.message(Command("invite"))
@router.message(Command("ref"))
async def cmd_invite(message: types.Message, bot: Bot, user_lang: str = "ru"):
    user_id = message.from_user.id
    stats = await _referral_stats(user_id)
    if stats is None:
        await message.answer(t(user_lang, "common.no_profile"))
        return

    me = await bot.me()
    link = f"https://t.me/{me.username}?start={user_id}"
    invited, earned = stats
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=t(user_lang, "ref.btn_share"),
            url=f"https://t.me/share/url?url={link}&text={t(user_lang, 'ref.share_text')}")],
        [types.InlineKeyboardButton(text=t(user_lang, "common.btn_menu"),
                                    callback_data="refresh_main_menu")],
    ])
    await message.answer(
        t(user_lang, "ref.text", link=link, invited=invited, earned=earned,
          bonus=REFERRAL_SIGNUP_BONUS),
        reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data == "open_referral")
async def open_referral_callback(callback: types.CallbackQuery, bot: Bot, user_lang: str = "ru"):
    await callback.answer()
    stats = await _referral_stats(callback.from_user.id)
    if stats is None:
        await callback.message.answer(t(user_lang, "common.no_profile"))
        return
    me = await bot.me()
    link = f"https://t.me/{me.username}?start={callback.from_user.id}"
    invited, earned = stats
    await callback.message.answer(
        t(user_lang, "ref.text", link=link, invited=invited, earned=earned,
          bonus=REFERRAL_SIGNUP_BONUS),
        parse_mode="HTML")
