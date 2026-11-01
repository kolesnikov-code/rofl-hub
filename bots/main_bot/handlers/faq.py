"""
/faq: короткая выжимка в чате + кнопка полного справочника в Mini App.

Полный FAQ — static/webapp/faq.html (решение владельца 13.10: простыни текста
в чат-боте нечитаемы, объёмные документы живут в Mini App).
"""
import logging

from aiogram import Router, types, F
from aiogram.filters import Command

from bots.main_bot.config import WEBAPP_URL
from shared.locales import t

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("faq"))
@router.message(F.text == "📚 Справка и FAQ")
async def cmd_faq(message: types.Message, user_lang: str = "ru"):
    """Короткая выжимка + полный справочник кнопкой."""
    rows = []
    if WEBAPP_URL:
        rows.append([types.InlineKeyboardButton(
            text=t(user_lang, "faq.btn_open"),
            web_app=types.WebAppInfo(url=f"{WEBAPP_URL}/faq?lang={user_lang}"))])
    rows.append([types.InlineKeyboardButton(text=t(user_lang, "common.btn_menu"),
                                            callback_data="refresh_main_menu")])
    await message.answer(t(user_lang, "faq.teaser"),
                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=rows),
                         parse_mode="HTML")
