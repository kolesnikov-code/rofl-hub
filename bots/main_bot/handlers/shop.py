"""
Магазин: reply-панель «МАГАЗИН / ДЛЯ ФЕРМЫ / ИГРОВЫЕ», витрина — инлайн-кнопки из каталога.
Переключение категории удаляет предыдущее сообщение витрины и рисует новое (по ТЗ).
Тексты и кнопки — на языке игрока (shared/locales).
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bots.main_bot.catalog import CATALOG, CATEGORY_FARM, CATEGORY_GAMES, SHOP_LAYOUT, item_button
from bots.main_bot.config import WEBAPP_URL
from shared.analytics import track
from shared.database import db
from shared.locales import btn, btn_variants, t

router = Router()
logger = logging.getLogger(__name__)


def get_shop_reply_keyboard(lang: str = "ru") -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=btn(lang, "shop"))],
            [types.KeyboardButton(text=btn(lang, "shop_cat_farm")),
             types.KeyboardButton(text=btn(lang, "shop_cat_games"))],
            [types.KeyboardButton(text=btn(lang, "main_menu"))],
        ],
        # БЕЗ is_persistent: уважает нативную кнопку Telegram «спрятать клавиатуру»
        resize_keyboard=True,
    )


def get_catalog_keyboard(category: str, lang: str = "ru") -> types.InlineKeyboardMarkup:
    rows = []
    # Первой строкой — «Что даёт каждый товар» (раздел FAQ в приложении), если оно настроено
    if WEBAPP_URL:
        rows.append([types.InlineKeyboardButton(
            text=t(lang, "shop.btn_info"),
            web_app=types.WebAppInfo(url=f"{WEBAPP_URL.rstrip('/')}/faq?s=shop-items"))])
    for row in SHOP_LAYOUT[category]:
        rows.append([
            types.InlineKeyboardButton(text=item_button(CATALOG[sku], lang), callback_data=f"buy_{sku}")
            for sku in row
        ])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def _category_text(category: str, capacity: int, lang: str) -> str:
    if category == CATEGORY_FARM:
        return t(lang, "shop.cat_farm", capacity=capacity)
    return t(lang, "shop.cat_games")


async def _show_category(message: types.Message, state: FSMContext, category: str,
                         user_id: int, lang: str) -> None:
    async with db.pool.acquire() as conn:
        capacity = await conn.fetchval("SELECT fridge_capacity FROM users WHERE user_id = $1", user_id)
    if capacity is None:
        await message.answer(t(lang, "common.no_profile"))
        return

    data = await state.get_data()
    old_id = data.get("shop_message_id")
    if old_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=old_id)
        except Exception:
            pass

    sent = await message.answer(_category_text(category, capacity, lang),
                                reply_markup=get_catalog_keyboard(category, lang), parse_mode="HTML")
    await state.update_data(shop_message_id=sent.message_id)
    await track(user_id, "shop_opened", category=category)


@router.message(Command("shop"))
@router.message(F.text.in_(btn_variants("shop")))
async def cmd_premium_shop(message: types.Message, state: FSMContext, user_lang: str = "ru"):
    """Вход в магазин: меняем нижнюю панель и показываем категорию «Для фермы»."""
    await message.answer(t(user_lang, "shop.header"),
                         reply_markup=get_shop_reply_keyboard(user_lang), parse_mode="HTML")
    await _show_category(message, state, CATEGORY_FARM, message.from_user.id, user_lang)


@router.message(F.text.in_(btn_variants("shop_cat_farm")))
async def cmd_shop_farm(message: types.Message, state: FSMContext, user_lang: str = "ru"):
    await _show_category(message, state, CATEGORY_FARM, message.from_user.id, user_lang)


@router.message(F.text.in_(btn_variants("shop_cat_games")))
async def cmd_shop_games(message: types.Message, state: FSMContext, user_lang: str = "ru"):
    await _show_category(message, state, CATEGORY_GAMES, message.from_user.id, user_lang)


@router.callback_query(F.data == "open_shop_from_farm")
async def open_shop_from_farm(callback: types.CallbackQuery, state: FSMContext, user_lang: str = "ru"):
    await callback.answer()
    await cmd_premium_shop_for_user(callback.message, state, callback.from_user.id, user_lang)


async def cmd_premium_shop_for_user(message: types.Message, state: FSMContext, user_id: int,
                                    lang: str = "ru") -> None:
    """Вариант для вызова из инлайн-кнопок, где message.from_user — это бот."""
    await message.answer(t(lang, "shop.header"),
                         reply_markup=get_shop_reply_keyboard(lang), parse_mode="HTML")
    await _show_category(message, state, CATEGORY_FARM, user_id, lang)
