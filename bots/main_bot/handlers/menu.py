import logging
from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()
logger = logging.getLogger(__name__)

def get_menu_keyboard() -> types.InlineKeyboardMarkup:
    """Вспомогательная функция сборки быстрой навигации под списком команд"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🏪 Зайти в Магазин /shop", callback_data="open_shop_from_farm"),
            types.InlineKeyboardButton(text="🚜 Моя Ферма /farm", callback_data="open_shop_from_farm")
        ]
    ])

# ============================================================================
# 💿 ЦЕНТРАЛЬНАЯ НАВИГАЦИОННАЯ КОМАНДА: /menu ИЛИ /commands
# ============================================================================
@router.message(Command("menu"))
@router.message(Command("commands"))
@router.message(F.text.lower() == "меню")
async def cmd_main_menu(message: types.Message):
    """
    Выводит сухой, строгий и информативный список всех рабочих команд
    пользовательского интерфейса ROFL HUB.
    """
    menu_text = (
        "💿 <b>СПИСОК ВСЕХ КОМАНД ЧАТ-БОТА ROFL HUB</b>\n"
        "..................................................\n\n"
        "👤 <b>ЛИЧНЫЙ ПРОФИЛЬ И ПАСПОРТ:</b>\n"
        "• /start — Начать диалог заново и пройти знакомство\n"
        "• /profile — Твой неоновый паспорт инвентаря и ресурсов\n"
        "• /my_stats — Альтернативный вызов личного кабинета\n\n"
        "🚜 <b>КИБЕР-ФЕРМА И АВТОМАТИЗАЦИЯ:</b>\n"
        "• /farm — Топливный хаб: заправка роботов и запуск завода\n"
        "• /shop — Маркетплейс: покупка Бурильщиков, котлет, монет и бустов\n\n"
        "🕹️ <b>БЫСТРЫЕ ИГРЫ С БОТОМ:</b>\n"
        "• /rps — Сыграть в Камень-Ножницы-Бумага с ботом (+2 / -3 рофла)\n"
        "• /high_low — Сыграть в Больше или Меньше с ботом (+2 / -3 рофла)\n"
        "• /quiz — Школьный интеллектуальный спринт-тест (+2 / -5 рофлов)\n\n"
        "👥 <b>ШКОЛЬНЫЕ БАНДЫ И КЛАНЫ:</b>\n"
        "• /create_clan — Создать свою команду за 100 000 рофлов\n\n"
        "📚 <b>СПРАВКА И ПОДДЕРЖКА:</b>\n"
        "• /faq — Часто-задаваемые вопросы и ответы\n"
        "• /rules — Правила экосистемы и юридический бронежилет\n"
        "..................................................\n"
        "👇 <b>ИСПОЛЬЗУЙ КНОПКИ ДЛЯ БЫСТРОГО ДОСТУПА К МАРКЕТУ:</b>"
    )
    await message.answer(menu_text, reply_markup=get_menu_keyboard(), parse_mode="HTML")
