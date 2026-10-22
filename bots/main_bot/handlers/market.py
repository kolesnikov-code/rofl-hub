"""
Биржа котлет (решение владельца 22.10): /market — витрина, /sell — выставить котлеты.

UX: витрина показывает лучшие предложения (по одной кнопке в ряд — правило владельца);
клик по ордеру → выбор количества с суммой прямо в кнопке → покупка. Продавцу
прилетает ЛС на его языке. Ядро и все деньги — shared/market.py (ledger).
"""
from __future__ import annotations

import logging

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from bots.main_bot.guards import feature_enabled
from shared.analytics import track
from shared.database import db
from shared.economy import (
    MARKET_FEE_PERCENT,
    MARKET_MAX_OPEN_ORDERS,
    MARKET_MAX_QTY,
    MARKET_SHOWCASE_LIMIT,
    market_fee,
)
from shared.locales import resolve_lang, t
from shared.market import (
    MarketError,
    buy_from_order,
    cancel_order,
    list_open_orders,
    market_stats,
    my_open_orders,
    place_sell_order,
    validate_order,
)

router = Router()
logger = logging.getLogger(__name__)

QTY_OPTIONS = (1, 5, 10)


def _menu_rows(lang: str) -> list[list[types.InlineKeyboardButton]]:
    return [
        [types.InlineKeyboardButton(text=t(lang, "mk.btn_my"), callback_data="mk_my")],
        [types.InlineKeyboardButton(text=t(lang, "mk.btn_sell_help"), callback_data="mk_sell_help")],
        [types.InlineKeyboardButton(text=t(lang, "mk.btn_refresh"), callback_data="mk_refresh")],
    ]


async def _showcase(user_id: int, lang: str) -> tuple[str, types.InlineKeyboardMarkup]:
    async with db.pool.acquire() as conn:
        stats = await market_stats(conn)
        orders = await list_open_orders(conn, MARKET_SHOWCASE_LIMIT, exclude_user=user_id)
        inv = await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = $1", user_id) or 0
    lines = [t(lang, "mk.order_line", id=o["id"], qty=o["qty"], price=o["price"]) for o in orders]
    body = "\n".join(lines) if lines else t(lang, "mk.empty")
    text = t(lang, "mk.header", orders=stats["orders"], cutlets=stats["cutlets"],
             best=stats["best_price"] if stats["best_price"] is not None else "—",
             fee=MARKET_FEE_PERCENT, inv=inv, body=body)
    rows = [[types.InlineKeyboardButton(
        text=t(lang, "mk.btn_order", id=o["id"], qty=o["qty"], price=o["price"]),
        callback_data=f"mk_pick:{o['id']}")] for o in orders]
    return text, types.InlineKeyboardMarkup(inline_keyboard=rows + _menu_rows(lang))


async def _safe_edit(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        await message.answer(text, reply_markup=kb, parse_mode="HTML")


# ============================================================================
# Витрина
# ============================================================================
@router.message(Command("market"))
async def cmd_market(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "market", user_lang):
        return
    text, kb = await _showcase(message.from_user.id, user_lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.in_({"mk_refresh", "open_market"}))
async def market_refresh(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "market", user_lang):
        return
    await callback.answer()
    text, kb = await _showcase(callback.from_user.id, user_lang)
    if callback.data == "open_market":
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await _safe_edit(callback.message, text, kb)


@router.callback_query(F.data == "mk_sell_help")
async def market_sell_help(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    await callback.message.answer(
        t(user_lang, "mk.sell_help", max_qty=MARKET_MAX_QTY, fee=MARKET_FEE_PERCENT,
          max_orders=MARKET_MAX_OPEN_ORDERS), parse_mode="HTML")


# ============================================================================
# Покупка: выбор количества → сделка
# ============================================================================
@router.callback_query(F.data.startswith("mk_pick:"))
async def market_pick(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "market", user_lang):
        return
    order_id = callback.data.split(":", 1)[1]
    if not order_id.isdigit():
        await callback.answer()
        return
    async with db.pool.acquire() as conn:
        order = await conn.fetchrow(
            "SELECT id, seller_id, qty, price FROM market_orders WHERE id = $1 AND status = 'open'",
            int(order_id))
    if not order or order["qty"] <= 0:
        await callback.answer(t(user_lang, "mk.err_not_found"), show_alert=True)
        return
    if order["seller_id"] == callback.from_user.id:
        await callback.answer(t(user_lang, "mk.err_own"), show_alert=True)
        return
    await callback.answer()
    rows = []
    for q in QTY_OPTIONS:
        if q < order["qty"]:
            rows.append([types.InlineKeyboardButton(
                text=t(user_lang, "mk.btn_qty", qty=q, total=q * order["price"]),
                callback_data=f"mk_buy:{order['id']}:{q}")])
    rows.append([types.InlineKeyboardButton(
        text=t(user_lang, "mk.btn_qty_all", qty=order["qty"], total=order["qty"] * order["price"]),
        callback_data=f"mk_buy:{order['id']}:{order['qty']}")])
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "mk.btn_back"), callback_data="mk_refresh")])
    await _safe_edit(callback.message,
                     t(user_lang, "mk.pick", id=order["id"], qty=order["qty"], price=order["price"]),
                     types.InlineKeyboardMarkup(inline_keyboard=rows))


@router.callback_query(F.data.startswith("mk_buy:"))
async def market_buy(callback: types.CallbackQuery, bot: Bot, user_lang: str = "ru"):
    if not await feature_enabled(callback, "market", user_lang):
        return
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await callback.answer()
        return
    order_id, qty = int(parts[1]), int(parts[2])
    buyer_id = callback.from_user.id
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                deal = await buy_from_order(conn, buyer_id, order_id, qty)
            seller_lang = resolve_lang(await conn.fetchval(
                "SELECT lang FROM users WHERE user_id = $1", deal["seller_id"]))
    except MarketError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        return

    await track(buyer_id, "market_buy", order_id=order_id, qty=deal["qty"], total=deal["total"])
    await callback.answer(t(user_lang, "mk.buy_toast"))
    await callback.message.answer(
        t(user_lang, "mk.buy_done", qty=deal["qty"], total=deal["total"]), parse_mode="HTML")
    try:
        await bot.send_message(
            deal["seller_id"],
            t(seller_lang, "mk.sold_notify", id=order_id, qty=deal["qty"], price=deal["price"],
              got=deal["seller_got"], fee=deal["fee"]),
            parse_mode="HTML")
    except Exception:
        pass
    text, kb = await _showcase(buyer_id, user_lang)
    await _safe_edit(callback.message, text, kb)


# ============================================================================
# Продажа: /sell <кол-во> <цена> → подтверждение → ордер
# ============================================================================
@router.message(Command("sell"))
async def cmd_sell(message: types.Message, user_lang: str = "ru"):
    if not await feature_enabled(message, "market", user_lang):
        return
    parts = (message.text or "").split()
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await message.answer(
            t(user_lang, "mk.sell_help", max_qty=MARKET_MAX_QTY, fee=MARKET_FEE_PERCENT,
              max_orders=MARKET_MAX_OPEN_ORDERS), parse_mode="HTML")
        return
    qty, price = int(parts[1]), int(parts[2])
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT inv_cutlets, has_shuttle FROM users WHERE user_id = $1",
                                  message.from_user.id)
    if row is None:
        await message.answer(t(user_lang, "common.no_profile"))
        return
    inv = row["inv_cutlets"]
    try:
        validate_order(qty, price, shuttle=bool(row["has_shuttle"]))
    except MarketError as e:
        await message.answer(e.localized(user_lang))
        return
    if inv < qty:
        await message.answer(t(user_lang, "mk.err_no_cutlets", have=inv))
        return
    total = qty * price
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(user_lang, "mk.btn_confirm_sell"),
                                    callback_data=f"mk_sell_go:{qty}:{price}")],
        [types.InlineKeyboardButton(text=t(user_lang, "mk.btn_cancel"), callback_data="mk_cancel")],
    ])
    await message.answer(
        t(user_lang, "mk.sell_confirm", qty=qty, price=price, total=total,
          fee=market_fee(total), got=total - market_fee(total)),
        reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("mk_sell_go:"))
async def market_sell_go(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "market", user_lang):
        return
    parts = callback.data.split(":")
    if len(parts) != 3 or not (parts[1].isdigit() and parts[2].isdigit()):
        await callback.answer()
        return
    qty, price = int(parts[1]), int(parts[2])
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                order_id = await place_sell_order(conn, callback.from_user.id, qty, price)
    except MarketError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        return
    await track(callback.from_user.id, "market_sell_order", order_id=order_id, qty=qty, price=price)
    await callback.answer(t(user_lang, "mk.sell_toast"))
    await _safe_edit(callback.message,
                     t(user_lang, "mk.sell_done", id=order_id, qty=qty, price=price),
                     types.InlineKeyboardMarkup(inline_keyboard=_menu_rows(user_lang)))


@router.callback_query(F.data == "mk_cancel")
async def market_cancel(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer(t(user_lang, "mk.cancelled_toast"))
    try:
        await callback.message.edit_text(t(user_lang, "mk.cancel_text"), parse_mode="HTML")
    except Exception:
        pass


# ============================================================================
# Мои ордера и снятие
# ============================================================================
@router.callback_query(F.data == "mk_my")
async def market_my(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    async with db.pool.acquire() as conn:
        orders = await my_open_orders(conn, callback.from_user.id)
    if not orders:
        text = t(user_lang, "mk.my_empty")
        rows = []
    else:
        text = t(user_lang, "mk.my_header") + "\n".join(
            t(user_lang, "mk.my_line", id=o["id"], qty=o["qty"], price=o["price"]) for o in orders)
        rows = [[types.InlineKeyboardButton(text=t(user_lang, "mk.btn_cancel_order", id=o["id"]),
                                            callback_data=f"mk_cancel_order:{o['id']}")] for o in orders]
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "mk.btn_back"), callback_data="mk_refresh")])
    await _safe_edit(callback.message, text, types.InlineKeyboardMarkup(inline_keyboard=rows))


@router.callback_query(F.data.startswith("mk_cancel_order:"))
async def market_cancel_order(callback: types.CallbackQuery, user_lang: str = "ru"):
    order_id = callback.data.split(":", 1)[1]
    if not order_id.isdigit():
        await callback.answer()
        return
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                qty = await cancel_order(conn, callback.from_user.id, int(order_id))
    except MarketError as e:
        await callback.answer(e.localized(user_lang), show_alert=True)
        return
    await callback.answer(t(user_lang, "mk.cancelled_toast"))
    await callback.message.answer(t(user_lang, "mk.order_cancelled", id=int(order_id), qty=qty),
                                  parse_mode="HTML")
    text, kb = await _showcase(callback.from_user.id, user_lang)
    await _safe_edit(callback.message, text, kb)
