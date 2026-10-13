"""
/rules: ключевые пункты в чате + полное Пользовательское соглашение в Mini App.

Полный документ — static/webapp/rules.html (та же схема, что /faq:
простыни юридического текста в чат-боте нечитаемы).
"""
import logging

from aiogram import Router, types, F
from aiogram.filters import Command

from bots.main_bot.config import WEBAPP_URL
from shared.locales import t

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("rules"))
@router.message(F.text == "📜 Пользовательское Соглашение")
async def cmd_rules(message: types.Message, user_lang: str = "ru"):
    """Выжимка соглашения + кнопка полного документа."""
    rows = []
    if WEBAPP_URL:
        rows.append([types.InlineKeyboardButton(
            text=t(user_lang, "rules.btn_open"),
            web_app=types.WebAppInfo(url=f"{WEBAPP_URL}/rules"))])
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "common.btn_menu"),
                                            callback_data="refresh_main_menu")])
    await message.answer(t(user_lang, "rules.teaser"),
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=rows),
                         parse_mode="HTML")
