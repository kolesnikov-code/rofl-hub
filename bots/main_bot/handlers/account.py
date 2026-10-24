"""
🗑 Удаление аккаунта по желанию игрока (кнопка в /profile).

Защита от случайного нажатия: экран-предупреждение, кнопки «Оставить» / «Да, удалить»
в случайном порядке, «Да, удалить» срабатывает не раньше ACCOUNT_DELETE_CONFIRM_SECONDS
после показа предупреждения, затем 7 дней заморозки с кнопкой отмены. Механика —
shared/account_deletion.py; жнец account_reaper_loop исполняет созревшие заявки.
"""
from __future__ import annotations

import asyncio
import logging
import random
import time

from aiogram import Bot, F, Router, types

from bots.main_bot.guards import feature_enabled
from shared.account_deletion import cancel_deletion, due_for_purge, purge_account, request_deletion
from shared.database import db
from shared.economy import (ACCOUNT_DELETE_CONFIRM_SECONDS, ACCOUNT_DELETE_GRACE_DAYS,
                            ACCOUNT_REAPER_INTERVAL_SECONDS, utcnow)
from shared.locales import resolve_lang, t

router = Router()
logger = logging.getLogger(__name__)

UNDO_CALLBACK = "acct_undo"


def undo_keyboard(lang: str) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text=t(lang, "acct.btn_undo"), callback_data=UNDO_CALLBACK)]])


def _fmt_date(dt) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")


@router.callback_query(F.data == "acct_del")
async def ask_delete(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "account_delete", user_lang):
        return
    await callback.answer()
    buttons = [
        types.InlineKeyboardButton(text=t(user_lang, "acct.btn_keep"), callback_data="acct_keep"),
        types.InlineKeyboardButton(text=t(user_lang, "acct.btn_confirm"),
                                   callback_data=f"acct_del_go:{int(time.time())}"),
    ]
    random.shuffle(buttons)   # «Да» не всегда на одном месте — палец не нажмёт по привычке
    await callback.message.answer(
        t(user_lang, "acct.warn", days=ACCOUNT_DELETE_GRACE_DAYS, seconds=ACCOUNT_DELETE_CONFIRM_SECONDS),
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons]),
        parse_mode="HTML")


@router.callback_query(F.data == "acct_keep")
async def keep_account(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    try:
        await callback.message.edit_text(t(user_lang, "acct.kept"))
    except Exception:
        await callback.message.answer(t(user_lang, "acct.kept"))


@router.callback_query(F.data.startswith("acct_del_go:"))
async def confirm_delete(callback: types.CallbackQuery, user_lang: str = "ru"):
    raw = callback.data.split(":", 1)[1]
    shown_at = int(raw) if raw.isdigit() else 0
    wait = ACCOUNT_DELETE_CONFIRM_SECONDS - (int(time.time()) - shown_at)
    if wait > 0:
        await callback.answer(t(user_lang, "acct.wait", seconds=wait), show_alert=True)
        return
    if not await feature_enabled(callback, "account_delete", user_lang):
        return
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            due = await request_deletion(conn, callback.from_user.id, utcnow())
    if due is None:
        await callback.answer(t(user_lang, "common.no_profile"), show_alert=True)
        return
    await callback.answer()
    text = t(user_lang, "acct.scheduled", date=_fmt_date(due))
    try:
        await callback.message.edit_text(text, reply_markup=undo_keyboard(user_lang), parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=undo_keyboard(user_lang), parse_mode="HTML")


@router.callback_query(F.data == UNDO_CALLBACK)
async def undo_delete(callback: types.CallbackQuery, user_lang: str = "ru"):
    async with db.pool.acquire() as conn:
        undone = await cancel_deletion(conn, callback.from_user.id)
    await callback.answer()
    await callback.message.answer(t(user_lang, "acct.undone" if undone else "acct.kept"))


async def pending_notice(lang: str, requested_at) -> str:
    from shared.account_deletion import deletion_due_at
    return t(lang, "acct.pending_notice", date=_fmt_date(deletion_due_at(requested_at)))


async def account_reaper_loop(bot: Bot | None = None) -> None:
    """Раз в час исполняет созревшие заявки на удаление. Сбой одной заявки не мешает другим."""
    while True:
        try:
            await asyncio.sleep(ACCOUNT_REAPER_INTERVAL_SECONDS)
            if not db.is_connected:
                continue
            async with db.pool.acquire() as conn:
                ids = await due_for_purge(conn, utcnow())
            for user_id in ids:
                try:
                    async with db.pool.acquire() as conn:
                        lang = resolve_lang(await conn.fetchval("SELECT lang FROM users WHERE user_id = $1", user_id))
                        async with conn.transaction():
                            done = await purge_account(conn, user_id, utcnow())
                    if done and bot is not None:
                        try:
                            await bot.send_message(user_id, t(lang, "acct.purged"))
                        except Exception:
                            pass
                except Exception:
                    logger.exception("[ACCOUNT_REAPER] user=%s не удалён", user_id)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("[ACCOUNT_REAPER] сбой цикла")
