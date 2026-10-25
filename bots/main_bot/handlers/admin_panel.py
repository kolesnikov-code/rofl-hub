"""
🎛 /admin — кнопка пульта владельца (Mini App). Скрытая команда: не в синем меню, отвечает только
ID из ADMIN_ID; остальным молчит. Пульт открывается из главного бота, потому что initData Mini App
подписывается токеном того бота, из которого он открыт, а сервер приложения живёт здесь.
"""
from __future__ import annotations

from aiogram import Router, types
from aiogram.filters import Command

from bots.main_bot.config import WEBAPP_URL
from bots.main_bot.webapp_admin import admin_ids

router = Router()


def admin_panel_url(base: str | None = None) -> str | None:
    base = WEBAPP_URL if base is None else base
    if not base:
        return None
    return base.split("?")[0].rstrip("/") + "/admin"


@router.message(Command("admin"))
async def cmd_admin(message: types.Message) -> None:
    if not message.from_user or message.from_user.id not in admin_ids():
        return
    url = admin_panel_url()
    if url is None:
        await message.answer("Пульт недоступен: не задан WEBAPP_URL.")
        return
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="🎛 Открыть пульт", web_app=types.WebAppInfo(url=url))]])
    await message.answer("🎛 <b>Пульт ROFL HUB</b>: битвы и акции, призы, подарки, VIP-аукционы, тумблеры.",
                         reply_markup=kb, parse_mode="HTML")
