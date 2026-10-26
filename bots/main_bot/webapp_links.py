"""
Ссылки из чата в игровое приложение (Mini App) на нужную вкладку.

Решение владельца 23.10: тяжёлые механики (мастерская, налёты, станция, биржа, ферма с артами)
живут в приложении, чат остаётся коротким. Вкладка передаётся query-параметром ?tab=…
(хэш URL Telegram занимает своими данными initData). Без WEBAPP_URL кнопки не показываются,
и обработчики откатываются к чатовой версии раздела.
"""
from __future__ import annotations

from aiogram import types

from bots.main_bot.config import WEBAPP_URL
from shared.locales import t

APP_TABS = ("passport", "games", "farm", "storage", "workshop", "raids", "market", "team", "mines", "goals", "shop", "top",
            "info")   # goals → паспорт (старые ссылки), info — FAQ и соглашение


def app_url(tab: str | None = None, base: str | None = None) -> str | None:
    """Адрес приложения с нужной вкладкой или None, если приложение не настроено."""
    base = WEBAPP_URL if base is None else base
    if not base:
        return None
    if not tab:
        return base
    if tab not in APP_TABS:
        raise ValueError(f"unknown tab {tab}")
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}tab={tab}"


def app_button(text: str, tab: str | None = None) -> types.InlineKeyboardButton | None:
    url = app_url(tab)
    if url is None:
        return None
    return types.InlineKeyboardButton(text=text, web_app=types.WebAppInfo(url=url))


async def send_app_link(target: types.Message, lang: str, tab: str, text_key: str) -> bool:
    """Короткое сообщение с кнопкой в нужную вкладку. False — приложение не настроено."""
    button = app_button(t(lang, "app.btn_section"), tab)
    if button is None:
        return False
    await target.answer(t(lang, text_key), parse_mode="HTML",
                        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[button]]))
    return True
