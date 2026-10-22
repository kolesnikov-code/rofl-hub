"""
Мастерская /workshop: ресурсы из игр → усиления фермы, щит от налётов, котлеты, броня, Шаттл.

Витрина — рецепты по одной кнопке в ряд (правило владельца), в кнопке — цена и
доступность (✅/🔒). Крафт одним нажатием: ресурсы не деньги, подтверждение лишнее;
при нехватке — алерт без списаний. Деньги/ресурсы — только shared/workshop + resources.
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from shared.analytics import track
from shared.database import db
from shared.economy import (
    ARMOR_BONUS_PER_LEVEL,
    ARMOR_MAX_LEVEL,
    SHUTTLE_MARKET_FEE_PERCENT,
    SHUTTLE_MARKET_MAX_QTY,
    WORKSHOP_RECIPES,
    utcnow,
)
from shared.locales import t
from shared.resources import RESOURCE_ICONS, format_bundle, get_resources
from shared.workshop import WorkshopError, can_afford, craft, recipe_cost

router = Router()
logger = logging.getLogger(__name__)

RECIPE_ORDER = ("nitro_6h", "nuclear_3h", "drone_24h", "shield_24h", "cutlet", "armor", "shuttle")


def stock_block(lang: str, stock: dict[str, int]) -> str:
    """Запасы всех четырёх ресурсов (и нули тоже — чтобы игрок знал, что добывать)."""
    return "  ".join(f"{RESOURCE_ICONS[k]} {v}" for k, v in stock.items())


async def _view(user_id: int, lang: str) -> tuple[str, types.InlineKeyboardMarkup]:
    async with db.pool.acquire() as conn:
        stock = await get_resources(conn, user_id)
        user = await conn.fetchrow(
            "SELECT farm_armor_level, has_shuttle FROM users WHERE user_id = $1", user_id)
    armor_level = user["farm_armor_level"] if user else 0
    has_shuttle = bool(user and user["has_shuttle"])

    rows = []
    for rid in RECIPE_ORDER:
        recipe = WORKSHOP_RECIPES[rid]
        effect = recipe["effect"]
        if effect == "shuttle" and has_shuttle:
            rows.append([types.InlineKeyboardButton(text=t(lang, "ws.btn_shuttle_owned"),
                                                    callback_data="ws_noop")])
            continue
        if effect == "armor" and armor_level >= ARMOR_MAX_LEVEL:
            rows.append([types.InlineKeyboardButton(text=t(lang, "ws.btn_armor_max"),
                                                    callback_data="ws_noop")])
            continue
        cost = recipe_cost(rid, armor_level)
        mark = "✅" if can_afford(stock, cost) else "🔒"
        label = t(lang, f"ws.recipe_{rid}", level=armor_level + 1)
        rows.append([types.InlineKeyboardButton(
            text=f"{mark} {label} — {format_bundle(lang, cost, sep=' + ')}",
            callback_data=f"ws_craft:{rid}")])
    rows.append([types.InlineKeyboardButton(text=t(lang, "ws.btn_refresh"), callback_data="ws_refresh")])
    rows.append([types.InlineKeyboardButton(text=t(lang, "ws.btn_farm"), callback_data="open_farm")])

    text = t(lang, "ws.header", stock=stock_block(lang, stock),
             armor=armor_level, armor_max=ARMOR_MAX_LEVEL, armor_pct=ARMOR_BONUS_PER_LEVEL,
             shuttle=t(lang, "ws.shuttle_yes") if has_shuttle else t(lang, "ws.shuttle_no"),
             shuttle_fee=SHUTTLE_MARKET_FEE_PERCENT, shuttle_qty=SHUTTLE_MARKET_MAX_QTY)
    return text, types.InlineKeyboardMarkup(inline_keyboard=rows)


async def _safe_edit(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        try:
            await message.answer(text, reply_markup=kb, parse_mode="HTML")
        except Exception:
            pass


@router.message(Command("workshop"))
async def cmd_workshop(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "workshop", user_lang):
        return
    text, kb = await _view(message.from_user.id, user_lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.in_({"ws_refresh", "open_workshop"}))
async def workshop_refresh(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "workshop", user_lang):
        return
    await callback.answer()
    text, kb = await _view(callback.from_user.id, user_lang)
    if callback.data == "open_workshop":
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await _safe_edit(callback.message, text, kb)


@router.callback_query(F.data == "ws_noop")
async def workshop_noop(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer(t(user_lang, "ws.noop"))


@router.callback_query(F.data.startswith("ws_craft:"))
async def workshop_craft(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "workshop", user_lang):
        return
    rid = callback.data.split(":", 1)[1]
    if rid not in WORKSHOP_RECIPES:
        await callback.answer()
        return
    user_id = callback.from_user.id
    now = utcnow()
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                result = await craft(conn, user_id, rid, now)
    except WorkshopError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        return

    await track(user_id, "craft", recipe=rid)
    effect = result.effect
    if effect in ("nitrogen", "nuclear", "drone", "shield"):
        done = t(user_lang, f"ws.done_{effect}", until=f"{result.until:%d.%m %H:%M}")
    elif effect == "cutlet":
        done = t(user_lang, "ws.done_cutlet", qty=result.qty)
    elif effect == "armor":
        done = t(user_lang, "ws.done_armor", level=result.level,
                 percent=result.level * ARMOR_BONUS_PER_LEVEL)
    else:
        done = t(user_lang, "ws.done_shuttle", fee=SHUTTLE_MARKET_FEE_PERCENT, qty=SHUTTLE_MARKET_MAX_QTY)
    await callback.answer(t(user_lang, "ws.toast"))
    await callback.message.answer(done, parse_mode="HTML")
    text, kb = await _view(user_id, user_lang)
    await _safe_edit(callback.message, text, kb)
