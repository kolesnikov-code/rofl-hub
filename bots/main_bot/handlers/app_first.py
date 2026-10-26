"""
📱 «Чат — дверь и почтальон» (шаг 3 плана владельца, 27.10). Вся игра — в приложении; в чате остаются вход (/start),
/app, /menu, /invite, /transfer, /faq, /rules, /paysupport, /delete_account и личные сообщения (награды, налёты,
дуэли, покупки).

Этот роутер стоит ПЕРЕД игровыми и перехватывает команды разделов и кнопки старой нижней клавиатуры: короткий
ответ с кнопкой в нужную вкладку приложения. Работает только при заданном WEBAPP_URL (фильтр app_ready) — без него
сообщения проходят дальше к прежним чатовым обработчикам (отказоустойчивость). Сами старые обработчики и их
callback-кнопки не удалены: ими доигрываются старые сообщения и ЛС (жесты дуэли, квесты).
"""
from __future__ import annotations

from aiogram import F, Router, types
from aiogram.filters import Command

from bots.main_bot import config
from bots.main_bot.webapp_links import app_button
from shared.locales import btn_variants, t

router = Router()

# команда → вкладка приложения
SECTION_TABS = {
    "profile": "passport", "my_stats": "passport", "goals": "passport",
    "farm": "farm", "my_farm": "farm",
    "shop": "shop",
    "games": "games", "quiz": "games", "rps": "games", "high_low": "games", "safe": "games",
    "duel": "games", "quests": "games",
    "market": "market", "sell": "market",
    "clan": "team", "clans": "team", "my_team": "team", "all_teams": "team", "create_team": "team",
}
# кнопки старой нижней клавиатуры → вкладка
REPLY_TABS = {"main_menu": None, "profile": "passport", "farm": "farm", "games_zone": "games", "teams": "team",
              "shop": "shop", "shop_cat_farm": "shop", "shop_cat_games": "shop"}
OLD_REPLY_TEXTS = {text: tab for key, tab in REPLY_TABS.items() for text in btn_variants(key)}


def app_ready(_: object = None) -> bool:
    return bool(config.WEBAPP_URL)


def app_markup(lang: str, tab: str | None = None) -> types.InlineKeyboardMarkup | None:
    """Одна кнопка «открыть игру» (во вкладку tab). None — приложение не настроено."""
    button = app_button(t(lang, "app.btn_section" if tab else "app.btn"), tab)
    return types.InlineKeyboardMarkup(inline_keyboard=[[button]]) if button else None


@router.message(Command(*SECTION_TABS), app_ready)
async def section_moved(message: types.Message, user_lang: str = "ru"):
    cmd = (message.text or "").split()[0].lstrip("/").split("@")[0].lower()
    await message.answer(t(user_lang, "app.moved"), parse_mode="HTML",
                         reply_markup=app_markup(user_lang, SECTION_TABS.get(cmd)))


@router.message(F.text.in_(set(OLD_REPLY_TEXTS)), app_ready)
async def old_keyboard_pressed(message: types.Message, user_lang: str = "ru"):
    """Кнопка старой нижней клавиатуры: убираем клавиатуру и даём кнопку в нужную вкладку."""
    await message.answer(t(user_lang, "app.keyboard_gone"), parse_mode="HTML",
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer(t(user_lang, "app.moved"), parse_mode="HTML",
                         reply_markup=app_markup(user_lang, OLD_REPLY_TEXTS[message.text]))


@router.message(Command("menu"), app_ready)
@router.message(F.text.lower().in_({"меню", "menu"}), app_ready)
async def app_menu(message: types.Message, user_lang: str = "ru"):
    await message.answer(t(user_lang, "menu.app"), parse_mode="HTML", reply_markup=app_markup(user_lang))
