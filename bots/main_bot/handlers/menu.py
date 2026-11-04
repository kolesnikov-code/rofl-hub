import logging
from aiogram import Router, types, F
from aiogram.filters import Command

from bots.main_bot import config
from bots.main_bot.config import WEBAPP_URL
from bots.main_bot.guards import feature_enabled
from bots.main_bot.webapp_links import app_button
from shared.locales import btn, btn_variants, t

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("app"))
@router.message(F.text.in_(btn_variants("open_app")))
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
            ],
            [types.KeyboardButton(text=btn(lang, "language"))],
        ],
        # БЕЗ is_persistent (решение владельца 15.10): игрок сам прячет/открывает панель
        # нативной кнопкой Telegram ⊞ у поля ввода; persistent разворачивал её насильно.
        resize_keyboard=True,
    )


def get_reply_lang_keyboard(lang: str = "ru") -> types.ReplyKeyboardMarkup:
    """Нижняя панель при подключённом приложении: вся игра в приложении — внизу «Открыть приложение» (04.11),
    под ней смена языка (02.11: случайно выбрали не тот или дети пошутили — игрок не теряется).
    Кнопка приложения — текстовая: web_app в reply-кнопке открывает приложение без initData (игрок не опознаётся),
    поэтому по нажатию бот присылает инлайн-кнопку запуска (cmd_open_app)."""
    return types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=btn(lang, "open_app"))],
                                               [types.KeyboardButton(text=btn(lang, "language"))]],
                                     resize_keyboard=True)


def get_reply_keyboard(lang: str = "ru") -> types.ReplyKeyboardMarkup:
    """Нижняя панель игрока: с приложением — только язык, без него — прежняя сетка разделов (+ язык)."""
    return get_reply_lang_keyboard(lang) if config.WEBAPP_URL else get_reply_main_keyboard(lang)


GAMES_HUB_BUTTONS = (
    ("menu.btn_quiz", "game_retry:quiz"),
    ("menu.btn_rps", "game_retry:rps"),
    ("menu.btn_hl", "game_retry:hl"),
    ("menu.btn_safe", "game_retry:safe"),
    ("menu.btn_duel", "duel_tables"),
    ("menu.btn_quests", "quest_list"),
    ("menu.btn_goals", "open_goals"),
)


def get_games_inline_keyboard(lang: str = "ru") -> types.InlineKeyboardMarkup:
    """
    Хаб игр — СТРОГО по одной кнопке в ряд (решение владельца 23.10: на 14 языках
    две кнопки в ряд обрезаются). Мастерская и налёты живут в приложении.
    """
    rows = [[types.InlineKeyboardButton(text=t(lang, key), callback_data=data)]
            for key, data in GAMES_HUB_BUTTONS]
    app = app_button(t(lang, "menu.btn_app"))
    if app is not None:
        rows.append([app])
    return types.InlineKeyboardMarkup(inline_keyboard=rows)


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
