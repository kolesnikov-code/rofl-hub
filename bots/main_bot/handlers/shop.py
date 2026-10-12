"""
Магазин: reply-панель «МАГАЗИН / ДЛЯ ФЕРМЫ / ИГРОВЫЕ», витрина — инлайн-кнопки из каталога.
Переключение категории удаляет предыдущее сообщение витрины и рисует новое (по ТЗ).
"""
from __future__ import annotations

import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bots.main_bot.catalog import CATALOG, CATEGORY_FARM, CATEGORY_GAMES, SHOP_LAYOUT
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)

BTN_SHOP = "🏪 МАГАЗИН"
BTN_FARM_CAT = "🚜 ДЛЯ ФЕРМЫ"
BTN_GAMES_CAT = "🕹️ ИГРОВЫЕ"
BTN_MAIN_MENU = "📱 ГЛАВНОЕ МЕНЮ"


def get_shop_reply_keyboard() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=BTN_SHOP)],
            [types.KeyboardButton(text=BTN_FARM_CAT), types.KeyboardButton(text=BTN_GAMES_CAT)],
            [types.KeyboardButton(text=BTN_MAIN_MENU)],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def get_catalog_keyboard(category: str) -> types.InlineKeyboardMarkup:
    rows = []
    for row in SHOP_LAYOUT[category]:
        rows.append([
            types.InlineKeyboardButton(text=CATALOG[sku]["button"], callback_data=f"buy_{sku}")
            for sku in row
        ])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


def _category_text(category: str, capacity: int) -> str:
    if category == CATEGORY_FARM:
        return (
            "🚜 <b>МАГАЗИН · ДЛЯ ФЕРМЫ</b>\n"
            "..................................................\n"
            "Роботы на 30 дней, топливо, холодильники, бусты и Мастер-дрон.\n"
            f"📦 Твой холодильник сейчас: <b>{capacity} котлет</b>\n"
            "..................................................\n"
            "👇 <b>Выбери товар:</b>"
        )
    return (
        "🕹️ <b>МАГАЗИН · ИГРОВЫЕ</b>\n"
        "..................................................\n"
        "Снятие лимитов побед, паки рофлов и лицензия Мега-Клана.\n"
        "..................................................\n"
        "👇 <b>Выбери товар:</b>"
    )


async def _show_category(message: types.Message, state: FSMContext, category: str, user_id: int) -> None:
    async with db.pool.acquire() as conn:
        capacity = await conn.fetchval("SELECT fridge_capacity FROM users WHERE user_id = $1", user_id)
    if capacity is None:
        await message.answer("⚠️ Профиль не найден. Нажми /start для регистрации.")
        return

    data = await state.get_data()
    old_id = data.get("shop_message_id")
    if old_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=old_id)
        except Exception:
            pass

    sent = await message.answer(_category_text(category, capacity),
                                reply_markup=get_catalog_keyboard(category), parse_mode="HTML")
    await state.update_data(shop_message_id=sent.message_id)


@router.message(Command("shop"))
@router.message(F.text == BTN_SHOP)
async def cmd_premium_shop(message: types.Message, state: FSMContext):
    """Вход в магазин: меняем нижнюю панель и показываем категорию «Для фермы»."""
    await message.answer(
        "🏪 <b>МАГАЗИН ROFL HUB</b>\nПокупки — через официальные Telegram Stars. Выбери категорию кнопками внизу.",
        reply_markup=get_shop_reply_keyboard(), parse_mode="HTML")
    await _show_category(message, state, CATEGORY_FARM, message.from_user.id)


@router.message(F.text == BTN_FARM_CAT)
async def cmd_shop_farm(message: types.Message, state: FSMContext):
    await _show_category(message, state, CATEGORY_FARM, message.from_user.id)


@router.message(F.text == BTN_GAMES_CAT)
async def cmd_shop_games(message: types.Message, state: FSMContext):
    await _show_category(message, state, CATEGORY_GAMES, message.from_user.id)


@router.callback_query(F.data == "open_shop_from_farm")
async def open_shop_from_farm(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_premium_shop_for_user(callback.message, state, callback.from_user.id)


async def cmd_premium_shop_for_user(message: types.Message, state: FSMContext, user_id: int) -> None:
    """Вариант для вызова из инлайн-кнопок, где message.from_user — это бот."""
    await message.answer(
        "🏪 <b>МАГАЗИН ROFL HUB</b>\nПокупки — через официальные Telegram Stars. Выбери категорию кнопками внизу.",
        reply_markup=get_shop_reply_keyboard(), parse_mode="HTML")
    await _show_category(message, state, CATEGORY_FARM, user_id)
