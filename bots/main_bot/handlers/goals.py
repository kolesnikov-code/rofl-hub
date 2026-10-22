"""
Ежедневные цели /goals: три цели на день, сундук за все три, серия дней.

Экран: список целей с прогрессом (✅/⬜), кнопка «🎁 ЗАБРАТЬ СУНДУК» появляется,
когда всё закрыто; быстрые кнопки-переходы к нужным разделам по одной в ряд.
Логика и награды — shared/daily_goals.py (ledger 'daily_chest').
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from shared.analytics import track
from shared.daily_goals import (
    GoalsError,
    all_done,
    chest_coins,
    claim_chest,
    claimed_today,
    goal_progress,
    goals_for,
)
from shared.database import db
from shared.economy import DAILY_CHEST_RESOURCE, DAILY_STREAK_BONUS_COINS, DAILY_STREAK_BONUS_EVERY, utcnow
from shared.feature_flags import FLAG_DEFAULTS, get_flag
from shared.locales import t
from shared.resources import RESOURCE_ICONS

router = Router()
logger = logging.getLogger(__name__)

# Куда ведёт цель (callback существующих разделов)
GOAL_LINKS = {
    "win_quiz": "game_retry:quiz", "win_rps": "game_retry:rps", "win_hl": "game_retry:hl",
    "win_safe": "game_retry:safe", "play_rounds": "games_hub", "duel": "duel_tables",
    "bonus": "open_farm", "craft": "open_workshop", "raid": "open_raids",
    "market_deal": "open_market", "donate": "open_station",
}


async def _enabled_features() -> set[str]:
    return {key for key in FLAG_DEFAULTS if key != "maintenance" and await get_flag(key)}


async def _view(user_id: int, lang: str) -> tuple[str, types.InlineKeyboardMarkup]:
    today = utcnow().date()
    goals = goals_for(user_id, today, await _enabled_features())
    async with db.pool.acquire() as conn:
        progress = await goal_progress(conn, user_id, goals, today)
        claimed = await claimed_today(conn, user_id, today)
        user = await conn.fetchrow("SELECT goal_streak, goal_last_claim FROM users WHERE user_id = $1", user_id)
    streak = user["goal_streak"] if user else 0
    done = all_done(goals, progress)

    lines, rows = [], []
    for g in goals:
        p = progress.get(g.key, 0)
        mark = "✅" if p >= g.target else "⬜"
        lines.append(f"{mark} {t(lang, f'goal.{g.key}', n=g.target)} — <b>{p}/{g.target}</b>")
        if p < g.target and not claimed:
            rows.append([types.InlineKeyboardButton(
                text=t(lang, "goal.btn_go", goal=t(lang, f"goal.{g.key}", n=g.target)[:40]),
                callback_data=GOAL_LINKS.get(g.key, "games_hub"))])
    if claimed:
        status = t(lang, "goal.status_claimed")
    elif done:
        status = t(lang, "goal.status_ready")
        rows.insert(0, [types.InlineKeyboardButton(text=t(lang, "goal.btn_claim"), callback_data="goal_claim")])
    else:
        status = t(lang, "goal.status_progress")
    text = t(lang, "goal.header", goals="\n".join(lines) or "—", status=status,
             coins=chest_coins(0), res=DAILY_CHEST_RESOURCE, streak=streak,
             every=DAILY_STREAK_BONUS_EVERY, bonus=DAILY_STREAK_BONUS_COINS)
    rows.append([types.InlineKeyboardButton(text=t(lang, "goal.btn_refresh"), callback_data="goal_refresh")])
    return text, types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _safe_edit(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        try:
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass


@router.message(Command("goals"))
async def cmd_goals(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "goals", user_lang):
        return
    text, kb = await _view(message.from_user.id, user_lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.in_({"goal_refresh", "open_goals"}))
async def goals_refresh(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "goals", user_lang):
        return
    await callback.answer()
    text, kb = await _view(callback.from_user.id, user_lang)
    if callback.data == "open_goals":
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await _safe_edit(callback.message, text, kb)


@router.callback_query(F.data == "goal_claim")
async def goals_claim(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "goals", user_lang):
        return
    user_id = callback.from_user.id
    today = utcnow().date()
    goals = goals_for(user_id, today, await _enabled_features())
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                chest = await claim_chest(conn, user_id, goals, today)
    except GoalsError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        text, kb = await _view(user_id, user_lang)
        await _safe_edit(callback.message, text, kb)
        return
    await track(user_id, "daily_chest", streak=chest["streak"])
    await callback.answer(t(user_lang, "goal.toast"))
    await callback.message.answer(
        t(user_lang, "goal.chest", coins=chest["coins"], icon=RESOURCE_ICONS[chest["kind"]],
          qty=chest["qty"], name=t(user_lang, f"res.{chest['kind']}"), streak=chest["streak"]),
        parse_mode="HTML")
    text, kb = await _view(user_id, user_lang)
    await _safe_edit(callback.message, text, kb)
