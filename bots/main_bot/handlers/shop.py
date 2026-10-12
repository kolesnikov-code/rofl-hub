import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)


def get_premium_shop_keyboard(current_capacity: int) -> types.InlineKeyboardMarkup:
    """
    Генерирует строго очищенную от розничного мусора витрину магазина.
    Все паки крупные, понятные и вызывают мгновенное желание купить.
    """
    keyboard_buttons = [
        # 1. ЛИНИЙКА РОБОТОВ-МАЙНЕРОВ
        [
            types.InlineKeyboardButton(text="🤖 Младший Майнер | 49 Stars", callback_data="buy_miner_junior"),
            types.InlineKeyboardButton(text="⚡ Кибер Бурильщик | 99 Stars", callback_data="buy_miner_premium")
        ],
        # 2. КРУПНЫЕ ОПТОВЫЕ ПАКИ КОТЛЕТ
        [
            types.InlineKeyboardButton(text="🥩 Пак котлет (10 шт.) | 49 Stars", callback_data="buy_cutlet_10")
        ],
        [
            types.InlineKeyboardButton(text="🥩 Запас котлет (50 шт.) | 239 Stars", callback_data="buy_cutlet_50"),
            types.InlineKeyboardButton(text="🥩 Пром. пак (100 шт.) | 449 Stars", callback_data="buy_cutlet_100")
        ],
        # 3. УЛУЧШЕНИЯ ХОЛОДИЛЬНИКА (СИНХРОНИЗИРОВАНО С ПАКАМИ КОТЛЕТ)
        [
            types.InlineKeyboardButton(text="📦 Холодильник на 10 шт. | 99 Stars", callback_data="buy_fridge_10")
        ],
        [
            types.InlineKeyboardButton(text="📦 Холодильник на 50 шт. | 499 Stars", callback_data="buy_fridge_50"),
            types.InlineKeyboardButton(text="📦 Холодильник на 100 шт. | 999 Stars", callback_data="buy_fridge_100")
        ],
        # 4. ВЫСОКОДОХОДНЫЕ СГОРАЕМЫЕ БУСТЫ ФЕРМЫ (НА 30 ДНЕЙ)
        [
            types.InlineKeyboardButton(text="🔋 Ядерный Разгон x5 | 199 Stars", callback_data="buy_boost_nuclear_30"),
            types.InlineKeyboardButton(text="❄️ Азотное Охлаждение +40% | 299 Stars",
                                       callback_data="buy_boost_nitrogen_30")
        ],
        # 5. СНЯТИЕ СУТОЧНЫХ ЛИМИТОВ НА ГЕЙМИНГ
        [
            types.InlineKeyboardButton(text="⚡ Игровой Безлимит (24ч) | 5 Stars", callback_data="buy_unlimit_24h"),
            types.InlineKeyboardButton(text="🚀 Игровой Безлимит (30д) | 99 Stars", callback_data="buy_unlimit_30d")
        ],
        # 6. VIP-АВТОМАТИЗАЦИЯ (ДРОН НА 1 ГОД)
        [
            types.InlineKeyboardButton(text="🤖 VIP Дрон-Ремонтник (1 год) | 999 Stars",
                                       callback_data="buy_repair_drone_365")
        ],
        # 7. ОПТОВАЯ КАЗНА МОНЕТ (БЕЗ МЕЛКОГО МУСОРА)
        [
            types.InlineKeyboardButton(text="💰 Пак 5 000 рофлов | 149 Stars", callback_data="buy_coins_5k"),
            types.InlineKeyboardButton(text="💰 Пак 10 000 рофлов | 299 Stars", callback_data="buy_coins_10k")
        ],
        [
            types.InlineKeyboardButton(text="👑 Пак 50 000 рофлов | 1299 Stars", callback_data="buy_coins_50k"),
            types.InlineKeyboardButton(text="👑 Пак 100 000 рофлов | 2499 Stars", callback_data="buy_coins_100k")
        ],
        # 8. МЕГА-КЛАНЫ
        [
            types.InlineKeyboardButton(text="🏆 Лицензия Мега-Клана | 2499 Stars", callback_data="buy_clan_upgrade")
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


# ============================================================================
# 🏪 ВЫЗОВ ОБНОВЛЕННОГО МАРКЕТПЛЕЙСА: /shop ИЛИ КНОПКА МЕНЮ
# ============================================================================
@router.message(Command("shop"))
@router.message(F.text == "🏪 МАГАЗИН")
async def cmd_premium_shop(message: types.Message):
    user_id = message.from_user.id

    # Считываем текущую вместимость игрока, чтобы бот знал, выдавать ли ошибку при покупке меньшего объема
    async with db.pool.acquire() as conn:
        user_data = await conn.fetchrow("SELECT fridge_capacity FROM users WHERE user_id = $1", user_id)

    current_capacity = user_data["fridge_capacity"] if user_data else 1

    shop_text = (
        "🏪 <b>МАРКЕТПЛЕЙС И ИНЖЕНЕРНАЯ МАСТЕРСКАЯ ROFL HUB</b>\n"
        "..................................................\n\n"
        "Прокачай аккаунт холдинга и увеличивай пассивную скорость добычи монеток! "
        "Покупки совершаются моментально через официальные звёзды Telegram Stars.\n\n"
        f"📦 <b>Текущая вместимость твоего холодильника:</b> CAPACITY {current_capacity}\n\n"
        "..................................................\n"
        "👇 <b>ВЫБЕРИ ТОВАР ДЛЯ ПОКУПКИ:</b>"
    )

    await message.answer(shop_text, reply_markup=get_premium_shop_keyboard(current_capacity), parse_mode="HTML")
