"""
Дуэли 1-на-1 (КНБ на ставку): столы 10/100/1000, сжигание 20% банка.

Вся логика с деньгами — в shared/duels.py (транзакции, эскроу, ledger).
Здесь — Telegram-обвязка: столы, жесты, уведомления обоим игрокам и вотчдоги.
Состояние дуэли живёт в БД, а не в FSM — рестарт бота ничего не теряет,
глобальный жнец (duel_reaper_loop) доигрывает зависшие раунды случайными жестами.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from shared.database import db
from shared.duels import (
    DuelError,
    MoveResult,
    cancel_waiting_duel,
    expire_waiting_duels,
    find_stuck_active_duels,
    join_or_create_duel,
    record_move,
    resolve_stuck_duel,
)
from shared.economy import (
    DUEL_BURN_PERCENT,
    DUEL_MOVE_TIMEOUT_SECONDS,
    DUEL_TABLES,
    DUEL_WAITING_TTL_MINUTES,
    duel_payout,
)
from shared.locales import resolve_lang, t

router = Router()
logger = logging.getLogger(__name__)

REAPER_INTERVAL_SECONDS = 20


async def _lang_of(conn, user_id: int) -> str:
    return resolve_lang(await conn.fetchval("SELECT lang FROM users WHERE user_id = $1", user_id))


def duel_tables_keyboard(lang: str) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(lang, "duel.btn_table", stake=stake),
                                    callback_data=f"duel_join:{stake}")]
        for stake in DUEL_TABLES
    ] + [[types.InlineKeyboardButton(text=t(lang, "games.btn_hub"), callback_data="games_hub")]])


def duel_intro_text(lang: str) -> str:
    return t(lang, "duel.intro",
             payout_percent=100 - DUEL_BURN_PERCENT, burn_percent=DUEL_BURN_PERCENT,
             move_timeout=DUEL_MOVE_TIMEOUT_SECONDS)


def move_keyboard(lang: str, duel_id: int) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text=t(lang, "duel.btn_move_rock"),
                                   callback_data=f"duel_move:{duel_id}:rock"),
        types.InlineKeyboardButton(text=t(lang, "duel.btn_move_scissors"),
                                   callback_data=f"duel_move:{duel_id}:scissors"),
        types.InlineKeyboardButton(text=t(lang, "duel.btn_move_paper"),
                                   callback_data=f"duel_move:{duel_id}:paper"),
    ]])


def _rematch_kb(lang: str) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(lang, "duel.btn_rematch"), callback_data="duel_tables")],
        [types.InlineKeyboardButton(text=t(lang, "games.btn_hub"), callback_data="games_hub")],
    ])


@router.message(Command("duel"))
async def cmd_duel(message: types.Message, user_lang: str = "ru"):
    await message.answer(duel_intro_text(user_lang),
                         reply_markup=duel_tables_keyboard(user_lang), parse_mode="HTML")


@router.callback_query(F.data == "duel_tables")
async def duel_tables_callback(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    try:
        await callback.message.edit_text(duel_intro_text(user_lang),
                                         reply_markup=duel_tables_keyboard(user_lang), parse_mode="HTML")
    except Exception:
        await callback.message.answer(duel_intro_text(user_lang),
                                      reply_markup=duel_tables_keyboard(user_lang), parse_mode="HTML")


# ============================================================================
# Вход за стол: эскроу ставки, матчмейкинг
# ============================================================================
@router.callback_query(F.data.startswith("duel_join:"))
async def duel_join(callback: types.CallbackQuery, bot: Bot, user_lang: str = "ru"):
    parts = callback.data.split(":")
    if len(parts) != 2 or not parts[1].isdigit():
        await callback.answer()
        return
    stake = int(parts[1])
    user_id = callback.from_user.id

    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await join_or_create_duel(conn, user_id, stake)
            opponent_lang = await _lang_of(conn, result.opponent_id) if result.matched else None
    except DuelError as e:
        await callback.answer(t(user_lang, e.key, **e.kwargs), show_alert=True)
        return

    await callback.answer()

    if not result.matched:
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text=t(user_lang, "duel.btn_cancel"),
                                        callback_data=f"duel_cancel:{result.duel_id}")]])
        try:
            await callback.message.edit_text(
                t(user_lang, "duel.waiting", stake=stake, ttl=DUEL_WAITING_TTL_MINUTES),
                reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass
        return

    # Пара собрана: обоим — выбор жеста
    payout, _ = duel_payout(stake)
    matched_kwargs = {"stake": stake, "bank": stake * 2, "payout": payout,
                      "timeout": DUEL_MOVE_TIMEOUT_SECONDS}
    try:
        await callback.message.edit_text(t(user_lang, "duel.matched", **matched_kwargs),
                                         reply_markup=move_keyboard(user_lang, result.duel_id),
                                         parse_mode="HTML")
    except Exception:
        pass
    try:
        await bot.send_message(result.opponent_id,
                               t(opponent_lang, "duel.matched", **matched_kwargs),
                               reply_markup=move_keyboard(opponent_lang, result.duel_id),
                               parse_mode="HTML")
    except Exception:
        logger.info("[DUEL] не доставлено приглашение сопернику %s", result.opponent_id)

    asyncio.create_task(_round_watchdog(bot, result.duel_id))


@router.callback_query(F.data.startswith("duel_cancel:"))
async def duel_cancel(callback: types.CallbackQuery, user_lang: str = "ru"):
    parts = callback.data.split(":")
    if len(parts) != 2 or not parts[1].isdigit():
        await callback.answer()
        return
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                stake = await cancel_waiting_duel(conn, int(parts[1]), callback.from_user.id)
    except DuelError as e:
        await callback.answer(t(user_lang, e.key, **e.kwargs), show_alert=True)
        return
    await callback.answer()
    try:
        await callback.message.edit_text(t(user_lang, "duel.cancelled", stake=stake),
                                         reply_markup=_rematch_kb(user_lang), parse_mode="HTML")
    except Exception:
        pass


# ============================================================================
# Жест игрока и развязка раунда
# ============================================================================
@router.callback_query(F.data.startswith("duel_move:"))
async def duel_move(callback: types.CallbackQuery, bot: Bot, user_lang: str = "ru"):
    parts = callback.data.split(":")
    if len(parts) != 3 or not parts[1].isdigit():
        await callback.answer()
        return
    duel_id, move = int(parts[1]), parts[2]
    user_id = callback.from_user.id

    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await record_move(conn, duel_id, user_id, move)
    except DuelError as e:
        await callback.answer(t(user_lang, e.key, **e.kwargs), show_alert=True)
        return

    await callback.answer()

    if result.waiting_opponent:
        try:
            await callback.message.edit_text(t(user_lang, "duel.move_saved"), parse_mode="HTML")
        except Exception:
            pass
        return

    await _broadcast_round_result(bot, duel_id, result)


async def _broadcast_round_result(bot: Bot, duel_id: int, result: MoveResult,
                                  reaper: bool = False) -> None:
    """Рассылает обоим игрокам итог раунда: переигровку или финал дуэли."""
    async with db.pool.acquire() as conn:
        duel = await conn.fetchrow("SELECT * FROM duels WHERE duel_id = $1", duel_id)
        langs = {p: await _lang_of(conn, p) for p in (duel["player1"], duel["player2"])}
        balances = {}
        if result.finished:
            balances[result.winner_id] = await conn.fetchval(
                "SELECT balance FROM users WHERE user_id = $1", result.winner_id)

    prefix = {p: (t(langs[p], "duel.reaper_prefix") if reaper else "") for p in langs}

    if result.draw_replay:
        for player, lang in langs.items():
            try:
                await bot.send_message(
                    player,
                    prefix[player] + t(lang, "duel.draw_replay",
                                       round=result.rounds, timeout=DUEL_MOVE_TIMEOUT_SECONDS),
                    reply_markup=move_keyboard(lang, duel_id), parse_mode="HTML")
            except Exception:
                pass
        asyncio.create_task(_round_watchdog(bot, duel_id))
        return

    w_lang, l_lang = langs[result.winner_id], langs[result.loser_id]
    win_text = prefix[result.winner_id] + t(
        w_lang, "duel.win",
        winner_move=t(w_lang, f"duel.btn_move_{result.winner_move}"),
        loser_move=t(w_lang, f"duel.btn_move_{result.loser_move}"),
        payout=result.payout, burned=result.burned, balance=balances[result.winner_id])
    lose_text = prefix[result.loser_id] + t(
        l_lang, "duel.lose",
        winner_move=t(l_lang, f"duel.btn_move_{result.winner_move}"),
        loser_move=t(l_lang, f"duel.btn_move_{result.loser_move}"),
        stake=duel["stake"])
    for player, text, lang in ((result.winner_id, win_text, w_lang),
                               (result.loser_id, lose_text, l_lang)):
        try:
            await bot.send_message(player, text, reply_markup=_rematch_kb(lang), parse_mode="HTML")
        except Exception:
            pass


# ============================================================================
# Вотчдоги: таймаут раунда и глобальный жнец (переживает рестарты)
# ============================================================================
async def _round_watchdog(bot: Bot, duel_id: int) -> None:
    """Через таймаут доигрывает раунд случайными жестами за молчунов."""
    await asyncio.sleep(DUEL_MOVE_TIMEOUT_SECONDS + 3)
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                duel = await conn.fetchrow(
                    "SELECT * FROM duels WHERE duel_id = $1 AND status = 'active' "
                    "AND (move1 IS NULL OR move2 IS NULL) FOR UPDATE", duel_id)
                if not duel:
                    return  # раунд уже разрешён игроками
                result = await resolve_stuck_duel(conn, duel)
        await _broadcast_round_result(bot, duel_id, result, reaper=True)
    except Exception:
        logger.exception("[DUEL_WATCHDOG] сбой по дуэли %s", duel_id)


async def duel_reaper_loop(bot: Bot) -> None:
    """
    Глобальный жнец (стартует в main): после рестарта бота in-memory вотчдоги
    мертвы — жнец доигрывает зависшие раунды и возвращает ставки протухших очередей.
    """
    logger.info("[DUEL_REAPER] жнец дуэлей запущен")
    while True:
        try:
            await asyncio.sleep(REAPER_INTERVAL_SECONDS)
            if not db.is_connected:
                continue
            async with db.pool.acquire() as conn:
                async with conn.transaction():
                    stuck = await find_stuck_active_duels(conn, DUEL_MOVE_TIMEOUT_SECONDS + 10)
                    results = [(d["duel_id"], await resolve_stuck_duel(conn, d)) for d in stuck]
                    expired = await expire_waiting_duels(conn, DUEL_WAITING_TTL_MINUTES)
            for duel_id, result in results:
                await _broadcast_round_result(bot, duel_id, result, reaper=True)
            for duel_id, player, stake in expired:
                try:
                    async with db.pool.acquire() as conn:
                        lang = await _lang_of(conn, player)
                    await bot.send_message(player, t(lang, "duel.expired", stake=stake),
                                           reply_markup=_rematch_kb(lang), parse_mode="HTML")
                except Exception:
                    pass
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("[DUEL_REAPER] сбой цикла — продолжаю")
