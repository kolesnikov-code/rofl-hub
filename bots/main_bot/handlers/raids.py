"""
Налёты /raid: текстовое меню действий в духе космо-игр.

Экран: статус (топливо, кулдаун, щит, стойка обороны, счёт), кнопки по одной в ряд:
🔭 разведка (3 случайные цели) → выбор цели → жест КНБ → итог; ⚔️ реванш (если на тебя
налетели); 🛡 стойка обороны (камень/ножницы/бумага — хранится в БД и решает исход
чужих налётов). Цели показываются по имени без username/ID — никакой травли.
Жертве уходит ЛС на её языке с итогом и подсказкой про щит и реванш.
Вся логика и ресурсы — shared/raids.py.
"""
from __future__ import annotations

import html
import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from bots.main_bot.webapp_links import app_button, send_app_link
from shared.analytics import track
from shared.database import db
from shared.economy import (
    RAID_ATTACK_COOLDOWN_HOURS,
    RAID_FUEL_HYDROGEN,
    RAID_LOOT_CAP,
    RAID_LOOT_PERCENT,
    RAID_NEWBIE_SHIELD_DAYS,
    RAID_REVENGE_HOURS,
    utcnow,
)
from shared.locales import resolve_lang, t
from shared.raids import (
    STANCES,
    RaidError,
    attack_cooldown_left,
    display_name_of,
    execute_raid,
    find_targets,
    raid_stats,
    revenge_options,
    set_stance,
    shield_active,
)
from shared.ranks import name_with_rank
from shared.resources import format_bundle, get_resources

router = Router()
logger = logging.getLogger(__name__)


def _move_label(lang: str, move: str) -> str:
    return t(lang, f"duel.btn_move_{move}")


async def _status_view(user_id: int, lang: str) -> tuple[str, types.InlineKeyboardMarkup]:
    now = utcnow()
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
        if not user:
            return t(lang, "common.no_profile"), types.InlineKeyboardMarkup(inline_keyboard=[])
        stock = await get_resources(conn, user_id)
        stats = await raid_stats(conn, user_id)
        revenges = await revenge_options(conn, user_id, now)

    left = attack_cooldown_left(user["last_raid_at"], now)
    if left > 0:
        ready = t(lang, "raid.cooldown_line", minutes=-(-left // 60))
    else:
        ready = t(lang, "raid.ready_line")
    if shield_active(user, now):
        until = user["raid_shield_until"]
        shield = t(lang, "raid.shield_on", until=f"{until:%d.%m %H:%M}") if until and until > now \
            else t(lang, "raid.shield_newbie", days=RAID_NEWBIE_SHIELD_DAYS)
    else:
        shield = t(lang, "raid.shield_off")
    stance = user["raid_stance"]
    stance_text = _move_label(lang, stance) if stance in STANCES else t(lang, "raid.stance_random")

    text = t(lang, "raid.header", hydrogen=stock["hydrogen"], fuel=RAID_FUEL_HYDROGEN,
             ready=ready, shield=shield, stance=stance_text,
             attacks=stats["attacks"], attack_wins=stats["attack_wins"],
             defenses=stats["defenses"], holds=stats["defense_holds"],
             percent=RAID_LOOT_PERCENT, cap=RAID_LOOT_CAP, cooldown=RAID_ATTACK_COOLDOWN_HOURS)
    rows = [[types.InlineKeyboardButton(text=t(lang, "raid.btn_scout"), callback_data="raid_scout")]]
    for r in revenges[:3]:
        rows.append([types.InlineKeyboardButton(
            text=t(lang, "raid.btn_revenge", name=display_name_of(r)[:20]),
            callback_data=f"raid_target:{r['attacker_id']}:{r['raid_id']}")])
    rows.append([types.InlineKeyboardButton(text=t(lang, "raid.btn_stance"), callback_data="raid_stance")])
    rows.append([types.InlineKeyboardButton(text=t(lang, "raid.btn_workshop"), callback_data="open_workshop")])
    rows.append([types.InlineKeyboardButton(text=t(lang, "raid.btn_refresh"), callback_data="raid_refresh")])
    return text, types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _safe_edit(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        try:
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass


@router.message(Command("raid"))
async def cmd_raid(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "raids", user_lang):
        return
    if await send_app_link(message, user_lang, "raids", "app.goto_raids"):
        return
    text, kb = await _status_view(message.from_user.id, user_lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.in_({"raid_refresh", "open_raids"}))
async def raid_refresh(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "raids", user_lang):
        return
    await callback.answer()
    if callback.data == "open_raids" and await send_app_link(callback.message, user_lang, "raids", "app.goto_raids"):
        return
    text, kb = await _status_view(callback.from_user.id, user_lang)
    if callback.data == "open_raids":
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await _safe_edit(callback.message, text, kb)


# ============================================================================
# Стойка обороны
# ============================================================================
@router.callback_query(F.data == "raid_stance")
async def raid_stance_menu(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    rows = [[types.InlineKeyboardButton(text=_move_label(user_lang, m),
                                        callback_data=f"raid_set_stance:{m}")] for m in STANCES]
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "raid.btn_back"), callback_data="raid_refresh")])
    await _safe_edit(callback.message, t(user_lang, "raid.stance_pick"),
                     types.InlineKeyboardMarkup(inline_keyboard=rows))


@router.callback_query(F.data.startswith("raid_set_stance:"))
async def raid_set_stance(callback: types.CallbackQuery, user_lang: str = "ru"):
    stance = callback.data.split(":", 1)[1]
    if stance not in STANCES:
        await callback.answer()
        return
    async with db.pool.acquire() as conn:
        await set_stance(conn, callback.from_user.id, stance)
    await callback.answer(t(user_lang, "raid.stance_saved", stance=_move_label(user_lang, stance)))
    text, kb = await _status_view(callback.from_user.id, user_lang)
    await _safe_edit(callback.message, text, kb)


# ============================================================================
# Разведка → цель → жест → налёт
# ============================================================================
@router.callback_query(F.data == "raid_scout")
async def raid_scout(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "raids", user_lang):
        return
    user_id = callback.from_user.id
    now = utcnow()
    async with db.pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT team_id, last_raid_at FROM users WHERE user_id = $1", user_id)
        if not user:
            await callback.answer(t(user_lang, "common.no_profile"), show_alert=True)
            return
        left = attack_cooldown_left(user["last_raid_at"], now)
        if left > 0:
            await callback.answer(t(user_lang, "raid.err_cooldown", minutes=-(-left // 60)), show_alert=True)
            return
        stock = await get_resources(conn, user_id)
        if stock["hydrogen"] < RAID_FUEL_HYDROGEN:
            await callback.answer(t(user_lang, "raid.err_fuel", need=RAID_FUEL_HYDROGEN,
                                    have=stock["hydrogen"]), show_alert=True)
            return
        targets = await find_targets(conn, user_id, user["team_id"], now)
    await callback.answer()
    if not targets:
        await _safe_edit(callback.message, t(user_lang, "raid.no_targets"),
                         types.InlineKeyboardMarkup(inline_keyboard=[[
                             types.InlineKeyboardButton(text=t(user_lang, "raid.btn_back"),
                                                        callback_data="raid_refresh")]]))
        return
    rows = []
    for tg in targets:
        rows.append([types.InlineKeyboardButton(
            text=t(user_lang, "raid.btn_target", name=display_name_of(tg)[:18], total=int(tg["total"])),
            callback_data=f"raid_target:{tg['user_id']}:0")])
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "raid.btn_back"), callback_data="raid_refresh")])
    await _safe_edit(callback.message, t(user_lang, "raid.scout", fuel=RAID_FUEL_HYDROGEN),
                     types.InlineKeyboardMarkup(inline_keyboard=rows))


@router.callback_query(F.data.startswith("raid_target:"))
async def raid_pick_target(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "raids", user_lang):
        return
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await callback.answer()
        return
    target_id, revenge_id = int(parts[1]), int(parts[2])
    await callback.answer()
    rows = [[types.InlineKeyboardButton(text=_move_label(user_lang, m),
                                        callback_data=f"raid_go:{target_id}:{revenge_id}:{m}")]
            for m in STANCES]
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "raid.btn_back"), callback_data="raid_refresh")])
    key = "raid.pick_move_revenge" if revenge_id else "raid.pick_move"
    await _safe_edit(callback.message, t(user_lang, key, fuel=RAID_FUEL_HYDROGEN),
                     types.InlineKeyboardMarkup(inline_keyboard=rows))


@router.callback_query(F.data.startswith("raid_go:"))
async def raid_go(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "raids", user_lang):
        return
    parts = callback.data.split(":")
    if len(parts) != 4 or not (parts[1].isdigit() and parts[2].isdigit()) or parts[3] not in STANCES:
        await callback.answer()
        return
    target_id, revenge_id, move = int(parts[1]), int(parts[2]), parts[3]
    user_id = callback.from_user.id
    now = utcnow()
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await execute_raid(conn, user_id, target_id, move, now,
                                            revenge_of=revenge_id or None)
                defender = await conn.fetchrow(
                    "SELECT user_id, display_name, lang, created_at FROM users WHERE user_id = $1", target_id)
                attacker = await conn.fetchrow(
                    "SELECT user_id, display_name, created_at FROM users WHERE user_id = $1", user_id)
    except RaidError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        text, kb = await _status_view(user_id, user_lang)
        await _safe_edit(callback.message, text, kb)
        return

    await track(user_id, "raid", result=result.result, revenge=result.is_revenge)
    await callback.answer()

    d_name = html.escape(display_name_of(defender))
    loot = format_bundle(user_lang, result.loot)
    key = {"win": "raid.result_win", "draw": "raid.result_draw", "lose": "raid.result_lose"}[result.result]
    text = t(user_lang, key, name=d_name, move=_move_label(user_lang, move),
             stance=_move_label(user_lang, result.stance), loot=loot)
    text += "\n\n" + t(user_lang, "raid.result_footer")
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(user_lang, "raid.btn_again"), callback_data="raid_refresh")]])
    await _safe_edit(callback.message, text, kb)

    # ЛС жертве на её языке — с подсказкой про щит и реванш
    await _notify_defender(callback.bot, defender, attacker, result, now)


async def _notify_defender(bot: Bot, defender, attacker, result, now) -> None:
    try:
        lang = resolve_lang(defender["lang"])
        a_name = name_with_rank(html.escape(display_name_of(attacker)), lang, attacker["created_at"], now)
        loot = format_bundle(lang, result.loot)
        key = {"win": "raid.victim_lost", "draw": "raid.victim_draw", "lose": "raid.victim_held"}[result.result]
        text = t(lang, key, name=a_name, stance=_move_label(lang, result.stance),
                 move=_move_label(lang, result.move), loot=loot, hours=RAID_REVENGE_HOURS)
        button = app_button(t(lang, "raid.btn_open"), "raids") or types.InlineKeyboardButton(
            text=t(lang, "raid.btn_open"), callback_data="open_raids")
        kb = types.InlineKeyboardMarkup(inline_keyboard=[[button]])
        await bot.send_message(defender["user_id"], text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        logger.info("[RAID] не удалось уведомить жертву %s", defender["user_id"] if defender else None)
