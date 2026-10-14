import logging
from aiogram import Router, types, F
from aiogram.filters import Command

from bots.main_bot.config import WEBAPP_URL
from bots.main_bot.guards import feature_enabled
from shared.locales import btn, btn_variants, t

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("app"))
async def cmd_open_app(message: types.Message, user_lang: str = "ru"):
    """Кнопка запуска Telegram Mini App (работает только с HTTPS-адресом сервера)."""
    if not WEBAPP_URL:
        await message.answer(t(user_lang, "app.unavailable"))
        return
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(user_lang, "app.btn"),
                                    web_app=types.WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(t(user_lang, "app.open"), reply_markup=kb, parse_mode="HTML")


def get_reply_main_keyboard(lang: str = "ru") -> types.ReplyKeyboardMarkup:
    """
    🎰 ОПТИМИЗИРОВАННАЯ СЕТКА КНОПОК ПОД МОБИЛЬНЫЕ СМАРТФОНЫ (ФOРМАТ 2х3)
    Кнопки строятся на языке игрока; обработчики ловят оба языка через btn_variants().
    """
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text=btn(lang, "main_menu")),
                types.KeyboardButton(text=btn(lang, "profile"))
            ],
            [
                types.KeyboardButton(text=btn(lang, "farm")),
                types.KeyboardButton(text=btn(lang, "games_zone"))
            ],
            [
                types.KeyboardButton(text=btn(lang, "teams")),
                types.KeyboardButton(text=btn(lang, "shop"))
            ]
        ],
        # БЕЗ is_persistent (решение владельца 15.10): игрок сам прячет/открывает панель
        # нативной кнопкой Telegram ⊞ у поля ввода; persistent разворачивал её насильно.
        resize_keyboard=True,
    )


def get_games_inline_keyboard(lang: str = "ru") -> types.InlineKeyboardMarkup:
    """Инлайн-панель моментального запуска дуэлей и игр"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=t(lang, "menu.btn_quiz"), callback_data="game_retry:quiz")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "menu.btn_rps"), callback_data="game_retry:rps"),
            types.InlineKeyboardButton(text=t(lang, "menu.btn_hl"), callback_data="game_retry:hl")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "menu.btn_coin"), callback_data="game_retry:coin"),
            types.InlineKeyboardButton(text=t(lang, "menu.btn_dice"), callback_data="game_retry:dice")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "menu.btn_safe"), callback_data="game_retry:safe")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "menu.btn_duel"), callback_data="duel_tables")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "menu.btn_quests"), callback_data="quest_list")
        ]
    ])


# ============================================================================
# 📱 1. ВЫЗОВ СТРОГОГО ГЛАВНОГО МЕНЮ КОМАНД
# ============================================================================
@router.message(Command("menu"))
@router.message(F.text.in_(btn_variants("main_menu")))
@router.message(F.text.lower().in_({"меню", "menu"}))
async def cmd_main_menu(message: types.Message, user_lang: str = "ru"):
    """Выводит лаконичный, стерильный список всех cmd-команд империи"""
    await message.answer(t(user_lang, "menu.text"),
                         reply_markup=get_reply_main_keyboard(user_lang), parse_mode="HTML")


# ============================================================================
# 🕹️ 2. ВЫЗОВ ИЗОЛИРОВАННОГО ИГРОВОГО ХАБА
# ============================================================================
@router.message(Command("games"))
@router.message(F.text.in_(btn_variants("games_zone")))
async def cmd_games_hub(message: types.Message, user_lang: str = "ru"):
    """Выводит красивую инлайн-панель выбора игр без дублирования основного меню"""
    if not await feature_enabled(message, "games", user_lang):
        return
    await message.answer(t(user_lang, "menu.games_hub"),
                         reply_markup=get_games_inline_keyboard(user_lang), parse_mode="HTML")


@router.callback_query(F.data == "games_hub")
async def games_hub_callback(callback: types.CallbackQuery, user_lang: str = "ru"):
    if not await feature_enabled(callback, "games", user_lang):
        return
    await callback.answer()
    await cmd_games_hub(callback.message, user_lang=user_lang)


@router.callback_query(F.data == "refresh_main_menu")
async def refresh_main_menu_callback(callback: types.CallbackQuery, user_lang: str = "ru"):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await cmd_main_menu(callback.message, user_lang=user_lang)
