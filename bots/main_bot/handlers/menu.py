import logging
from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()
logger = logging.getLogger(__name__)

def get_reply_main_keyboard() -> types.ReplyKeyboardMarkup:
    """
    🎰 ОПТИМИЗИРОВАННАЯ СЕТКА КНОПОК ПОД МОБИЛЬНЫЕ СМАРТФОНЫ (ФOРМАТ 2х3)
    Идеально центрирует текст на любых экранах, исключая эффект 'школы под мостом'.
    """
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="📱 ГЛАВНОЕ МЕНЮ"),
                types.KeyboardButton(text="👤 МОЙ ПРОФИЛЬ")
            ],
            [
                types.KeyboardButton(text="🚜 МОЯ ФЕРМА"),
                types.KeyboardButton(text="🕹️ ИГРОВАЯ ЗОНА")
            ],
            [
                types.KeyboardButton(text="🏆 КОМАНДЫ И КЛАНЫ"),
                types.KeyboardButton(text="🏪 МАГАЗИН")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )

def get_games_inline_keyboard() -> types.InlineKeyboardMarkup:
    """Инлайн-панель моментального запуска дуэлей и игр"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🪨 КНБ дуэль (/rps)", callback_data="game_retry:rps"),
            types.InlineKeyboardButton(text="🎲 Больше/Меньше (/high_low)", callback_data="game_retry:hl")
        ],
        [
            types.InlineKeyboardButton(text="🧠 Пройти Викторину (/quiz)", callback_data="game_retry:quiz")
        ]
    ])

# ============================================================================
# 📱 1. ВЫЗОВ СТРОГОГО ГЛАВНОГО МЕНЮ КОМАНД
# ============================================================================
@router.message(Command("menu"))
@router.message(F.text == "📱 ГЛАВНОЕ МЕНЮ")
@router.message(F.text.lower() == "меню")
async def cmd_main_menu(message: types.Message):
    """Выводит лаконичный, стерильный список всех cmd-команд империи"""
    menu_text = (
        "📱 <b>ГЛАВНОЕ МЕНЮ ЭКОСИСТЕМЫ ROFL HUB</b>\n"
        "..................................................\n\n"
        "👤 <b>ЛИЧНЫЙ ПРОФИЛЬ И ПАСПОРТ:</b>\n"
        "• /start — Начать знакомство и зарегистрировать аккаунт\n"
        "• /profile — Твой паспорт, баланс и команда в реальном времени\n"
        "• /my_stats — Твоя историческая статистика за последние 30 дней\n\n"
        "🚜 <b>КИБЕР-ФЕРМА И АВТОМАТИЗАЦИЯ:</b>\n"
        "• /farm — Топливный хаб: заправка и скорость выработки роботов\n"
        "• /shop — Маркетплейс: закупка майнеров, котлет и улучшений хаба\n\n"
        "🕹️ <b>ИГРОВАЯ КОМНАТА:</b>\n"
        "• /games — Запустить инлайн-хаб дуэлей и спринт-тестов против бота\n\n"
        "👥 <b>УПРАВЛЕНИЕ БАНДАМИ:</b>\n"
        "• /create_team — Зарегистрировать свою команду за 100 000 рофлов\n"
        "• /my_team — Проверить дашборд и девиз своей банды\n"
        "• /all_teams — Игровая рулетка случайных команд СНГ\n\n"
        "📚 <b>ЮРИДИЧЕСКИЙ БЛОК:</b>\n"
        "• /faq — Часто задаваемые вопросы и ответы\n"
        "• /rules — Пользовательское соглашение и юридический бронежилет\n"
        "..................................................\n"
        "<i>⚙️ Используй вечную двухколонную гейм-панель внизу экрана для мгновенной навигации по разделам!</i>"
    )
    await message.answer(menu_text, reply_markup=get_reply_main_keyboard(), parse_mode="HTML")

# ============================================================================
# 🕹️ 2. ВЫЗОВ ИЗОЛИРОВАННОГО ИГРОВОГО ХАБА
# ============================================================================
@router.message(Command("games"))
@router.message(F.text == "🕹️ ИГРОВАЯ ЗОНА")
async def cmd_games_hub(message: types.Message):
    """Выводит красивую инлайн-панель выбора игр без дублирования основного меню"""
    games_text = (
        "🕹️ <b>ДОБРО ПОЖАЛОВАТЬ В ИГРОВУЮ ЗОНУ ROFL HUB!</b>\n"
        "..................................................\n\n"
        "Здесь ты можешь сразиться с ботом в быстрых дуэлях или пройти "
        "интеллектуальный спринт-тест, чтобы сорвать куш или слить баланс!\n\n"
        "💸 Победа приносит: <b>+2 рофла</b>\n"
        "💀 Капкан проигрыша списывает: <b>до -5 рофлов!</b>\n\n"
        "..................................................\n"
        "👇 <b>КЛИКАЙ ПО КНОПКЕ НИЖЕ ДЛЯ НЕМЕДЛЕННОГО СТАРТА РAУНДA:</b>"
    )
    await message.answer(games_text, reply_markup=get_games_inline_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "refresh_main_menu")
async def refresh_main_menu_callback(callback: types.CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await cmd_main_menu(callback.message)
