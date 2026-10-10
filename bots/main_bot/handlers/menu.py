import logging
from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()
logger = logging.getLogger(__name__)

def get_menu_keyboard() -> types.InlineKeyboardMarkup:
    """Генеральная инлайн-панель навигации, доступная из любого узла игры"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🚜 Моя Ферма /farm", callback_data="open_farm_from_profile"),
            types.InlineKeyboardButton(text="🏪 Магазин /shop", callback_data="open_shop_from_farm")
        ],
        [
            types.InlineKeyboardButton(text="🏆 Команды и Кланы", callback_data="clan_main_menu"),
            types.InlineKeyboardButton(text="💿 Повторить Меню", callback_data="refresh_main_menu")
        ]
    ])

# ============================================================================
# 💿 ЦЕНТРАЛЬНАЯ НАВИГАЦИОННАЯ КОМАНДА: /menu
# ============================================================================
@router.message(Command("menu"))
@router.message(F.text.lower() == "меню")
async def cmd_main_menu(message: types.Message):
    """Выводит строгое, лаконичное и информативное меню всех команд системы"""
    menu_text = (
        "💿 <b>СПИСОК ВСЕХ КОМАНД ЭКОСИСТЕМЫ ROFL HUB</b>\n"
        "..................................................\n\n"
        "👤 <b>ЛИЧНЫЙ ПРОФИЛЬ И ПАСПОРТ:</b>\n"
        "• /start — Начать диалог заново и пройти знакомство\n"
        "• /profile — Актуальный личный кабинет, команда и баланс сейчас\n"
        "• /my_stats — Твоя игровая статистика за последние 30 дней\n\n"
        "🚜 <b>КИБЕР-ФЕРМА И АВТОМАТИЗАЦИЯ:</b>\n"
        "• /farm — Топливный хаб: заправка и скорость выработки роботов\n"
        "• /shop — Маркетплейс: покупка Бурильщиков, котлет, монет и бустов\n\n"
        "🕹️ <b>БЫСТРЫЕ ИГРЫ С БОТОМ:</b>\n"
        "• /rps — Сыграть в Камень-Ножницы-Бумага с ботом (+2 / -3 рофла)\n"
        "• /high_low — Сыграть в Больше или Меньше с ботом (+2 / -3 рофла)\n"
        "• /quiz — Игровой интеллектуальный спринт-тест (+2 / -5 рофлов)\n\n"
        "👥 <b>КОМАНДЫ И КЛАНЫ:</b>\n"
        "• /create_team — Создать свою команду за 100 000 рофлов\n"
        "• /my_team — Посмотреть дашборд и состав своей команды\n"
        "• /all_teams — Глобальный поиск команд и списки СНГ\n\n"
        "📚 <b>СПРАВКА И ПОДДЕРЖКА:</b>\n"
        "• /faq — Часто-задаваемые вопросы и ответы\n"
        "• /rules — Правила экосистемы и юридический бронежилет\n"
        "..................................................\n"
        "👇 <b>ИСПОЛЬЗУЙ КНОПКИ ДЛЯ МГНОВЕННОГО ПЕРЕХОДА ИЗ МЕНЮ:</b>"
    )
    await message.answer(menu_text, reply_markup=get_menu_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "refresh_main_menu")
async def refresh_main_menu_callback(callback: types.CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await cmd_main_menu(callback.message)
