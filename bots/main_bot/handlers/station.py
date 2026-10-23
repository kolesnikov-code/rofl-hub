"""
Станция команды /station: общий проект на ресурсах всей команды.

Экран: уровень, бонус к добыче для всех, прогресс до следующего уровня по каждому
ресурсу, лента последних вкладов (имена — только соклановцам, это их экран).
Кнопки вклада по одной в ряд: «+10 ⛏», «+50 ⛏», «всё ⛏» для каждого ресурса, которого
у игрока хватает. При закрытии уровня — ЛС всем участникам команды (фоновая задача).
Логика — shared/team_station.py.
"""
from __future__ import annotations

import asyncio
import html
import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from bots.main_bot.webapp_links import send_app_link
from shared.analytics import track
from shared.database import db
from shared.economy import (
    RESOURCE_KINDS,
    STATION_BONUS_PER_LEVEL,
    STATION_DONATE_OPTIONS,
    STATION_MAX_LEVEL,
    station_level_cost,
)
from shared.locales import resolve_lang, t
from shared.resources import RESOURCE_ICONS, get_resources
from shared.team_station import (
    StationError,
    donate,
    get_station,
    progress_to_next,
    recent_donations,
    team_member_ids,
)

router = Router()
logger = logging.getLogger(__name__)


def _donor_name(row: dict) -> str:
    name = (row.get("display_name") or "").strip()
    if row.get("username"):
        return "@" + html.escape(row["username"])
    return html.escape(name) if name else f"#{str(row['user_id'])[-4:]}"


async def _view(user_id: int, lang: str) -> tuple[str, types.InlineKeyboardMarkup]:
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1", user_id)
        if not user or user["team_id"] is None:
            kb = types.InlineKeyboardMarkup(inline_keyboard=[[
                types.InlineKeyboardButton(text=t(lang, "st.btn_find_team"), callback_data="clan_main_menu")]])
            return t(lang, "st.no_team"), kb
        team = await conn.fetchrow("SELECT team_name FROM teams WHERE team_id = $1", user["team_id"])
        station = await get_station(conn, user["team_id"])
        feed = await recent_donations(conn, user["team_id"])
        stock = await get_resources(conn, user_id)

    level = station["level"]
    stored = {k: station[k] for k in RESOURCE_KINDS}
    need = progress_to_next(level, stored)
    if level >= STATION_MAX_LEVEL:
        progress_block = t(lang, "st.max_level")
    else:
        cost = station_level_cost(level + 1)
        progress_block = "\n".join(
            f"{RESOURCE_ICONS[k]} {t(lang, f'res.{k}')}: <b>{stored[k]}/{cost}</b>"
            + ("" if need[k] == 0 else f" (−{need[k]})") for k in RESOURCE_KINDS)
    feed_block = "\n".join(
        f"• {_donor_name(d)} +{d['qty']} {RESOURCE_ICONS[d['kind']]}" for d in feed) or t(lang, "st.feed_empty")

    text = t(lang, "st.header", team=html.escape(team["team_name"]), level=level, max=STATION_MAX_LEVEL,
             percent=level * STATION_BONUS_PER_LEVEL, per_level=STATION_BONUS_PER_LEVEL,
             progress=progress_block, feed=feed_block,
             stock="  ".join(f"{RESOURCE_ICONS[k]} {stock[k]}" for k in RESOURCE_KINDS))
    rows = []
    if level < STATION_MAX_LEVEL:
        for k in RESOURCE_KINDS:
            if need.get(k, 0) == 0 or stock[k] <= 0:
                continue
            for opt in STATION_DONATE_OPTIONS:
                if stock[k] >= opt:
                    rows.append([types.InlineKeyboardButton(
                        text=t(lang, "st.btn_donate", qty=opt, icon=RESOURCE_ICONS[k], name=t(lang, f"res.{k}")),
                        callback_data=f"st_donate:{k}:{opt}")])
            give_all = min(stock[k], need[k])
            if give_all not in STATION_DONATE_OPTIONS or give_all > max(STATION_DONATE_OPTIONS):
                rows.append([types.InlineKeyboardButton(
                    text=t(lang, "st.btn_donate_all", qty=give_all, icon=RESOURCE_ICONS[k], name=t(lang, f"res.{k}")),
                    callback_data=f"st_donate:{k}:{give_all}")])
    rows.append([types.InlineKeyboardButton(text=t(lang, "st.btn_refresh"), callback_data="st_refresh")])
    rows.append([types.InlineKeyboardButton(text=t(lang, "st.btn_team"), callback_data="clan_main_menu")])
    return text, types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _safe_edit(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        try:
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass


@router.message(Command("station"))
async def cmd_station(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "station", user_lang):
        return
    if await send_app_link(message, user_lang, "team", "app.goto_station"):
        return
    text, kb = await _view(message.from_user.id, user_lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.in_({"st_refresh", "open_station"}))
async def station_refresh(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "station", user_lang):
        return
    await callback.answer()
    if callback.data == "open_station" and await send_app_link(callback.message, user_lang, "team", "app.goto_station"):
        return
    text, kb = await _view(callback.from_user.id, user_lang)
    if callback.data == "open_station":
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await _safe_edit(callback.message, text, kb)


@router.callback_query(F.data.startswith("st_donate:"))
async def station_donate(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "station", user_lang):
        return
    parts = callback.data.split(":")
    if len(parts) != 3 or parts[1] not in RESOURCE_KINDS or not parts[2].isdigit():
        await callback.answer()
        return
    kind, qty = parts[1], int(parts[2])
    user_id = callback.from_user.id
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await donate(conn, user_id, kind, qty)
                team_id = await conn.fetchval("SELECT team_id FROM users WHERE user_id = $1", user_id)
                members = await team_member_ids(conn, team_id) if result.levels_gained else []
    except StationError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        text, kb = await _view(user_id, user_lang)
        await _safe_edit(callback.message, text, kb)
        return

    await track(user_id, "station_donate", kind=kind, qty=qty, level=result.level)
    await callback.answer(t(user_lang, "st.toast", qty=qty, icon=RESOURCE_ICONS[kind]))
    text, kb = await _view(user_id, user_lang)
    await _safe_edit(callback.message, text, kb)
    if result.levels_gained:
        asyncio.create_task(_announce_level(callback.bot, members, result.level))


async def _announce_level(bot: Bot, members: list[int], level: int) -> None:
    """ЛС всем участникам: станция выросла — у всех +N% к добыче."""
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT user_id, lang FROM users WHERE user_id = ANY($1::bigint[])", members)
    for r in rows:
        try:
            lang = resolve_lang(r["lang"])
            await bot.send_message(r["user_id"], t(lang, "st.level_up", level=level,
                                                   percent=level * STATION_BONUS_PER_LEVEL),
                                   parse_mode="HTML")
            await asyncio.sleep(0.05)
        except Exception:
            pass
