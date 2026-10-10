import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)


# ============================================================================
# 🏪 1. ГЛАВНАЯ КОМАНДА ВИТРИНЫ: /shop ИЛИ /store
# ============================================================================
@router.message(Command("shop"))
@router.message(Command("store"))
async def cmd_shop(message: types.Message):
    user_id = message.from_user.id

    # Вытягиваем из базы Railway текущий уровень буста и вместимость хаба юзера
    async with db.pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT fridge_capacity, boost_level FROM users WHERE user_id = $1",
            user_id
        )

    # Защитный fallback, если юзер не прожал /start
    fridge_capacity = user_data["fridge_capacity"] if user_data else 1
    boost_level = user_data["boost_level"] if user_data else 0

    # ДИНАМИЧЕСКИЙ РAСЧЁТ КНOПКИ БУСТА
    if boost_level == 0:
        boost_btn_text = "🚀 Купить Боевой Буст I Ур. | ★ 99 Stars"
    elif boost_level == 1:
        boost_btn_text = "🚀🚀 Апгрейд Буста до II Ур. | ★ 199 Stars"
    elif boost_level == 2:
        boost_btn_text = "🚀🚀🚀 Апгрейд Буста до III Ур. | ★ 299 Stars"
    else:
        boost_btn_text = "👑 МАКСИМАЛЬНЫЙ БУСТ АКТИВИРОВАН"

    # Собираем инлайн-клавиатуру магазина по нашему алфавитному и логическому порядку
    buttons = [
        # 🤖 Раздел: Роботы-майнеры
        [types.InlineKeyboardButton(text="🤖 Робот «Младший Майнер» | ★ 49 Stars", callback_data="buy_miner_junior")],
        [types.InlineKeyboardButton(text="⚡ Робот «Кибер Бурильщик» | ★ 99 Stars", callback_data="buy_miner_premium")],

        # 🥩 Раздел: Кибер-котлеты
        [types.InlineKeyboardButton(text="🥩 1 кибер-котлета | ★ 7 Stars", callback_data="buy_cutlet_1")],
        [types.InlineKeyboardButton(text="🥩 5 кибер-котлет | ★ 29 Stars", callback_data="buy_cutlet_5")],
        [types.InlineKeyboardButton(text="🥩 10 кибер-котлет | ★ 49 Stars", callback_data="buy_cutlet_10")],
        [types.InlineKeyboardButton(text="🥩 50 кибер-котлет | ★ 239 Stars", callback_data="buy_cutlet_50")],
        [types.InlineKeyboardButton(text="🥩 100 кибер-котлет | ★ 449 Stars", callback_data="buy_cutlet_100")]
    ]

    # 📦 Раздел: Центральные Холодильники (Показываем только те, что выше текущего объема!)
    if fridge_capacity < 5:
        buttons.append(
            [types.InlineKeyboardButton(text="📦 Холодильник на 5 котлет | ★ 49 Stars", callback_data="buy_fridge_5")])
    if fridge_capacity < 10:
        buttons.append(
            [types.InlineKeyboardButton(text="📦 Холодильник на 10 котлет | ★ 99 Stars", callback_data="buy_fridge_10")])
    if fridge_capacity < 50:
        buttons.append([types.InlineKeyboardButton(text="📦 Холодильник на 50 котлет | ★ 499 Stars",
                                                   callback_data="buy_fridge_50")])
    if fridge_capacity < 100:
        buttons.append([types.InlineKeyboardButton(text="👑 Холодильник на 100 котлет | ★ 999 Stars",
                                                   callback_data="buy_fridge_100")])

    # 💰 Раздел: Розничная монетарная казна (Игровые Рофлы — ДО 100 000 МОНЕТ МАКСИМУМ)
    buttons.extend([
        [types.InlineKeyboardButton(text="💰 «Солдат»: 1 000 монет | ★ 49 Stars", callback_data="buy_coins_1k")],
        [types.InlineKeyboardButton(text="💰 «Капитан»: 3 000 монет | ★ 99 Stars", callback_data="buy_coins_3k")],
        [types.InlineKeyboardButton(text="💰 «Ветеран»: 10 000 монет | ★ 299 Stars", callback_data="buy_coins_10k")],
        [types.InlineKeyboardButton(text="👑 «Легенда»: 50 000 монет | ★ 1299 Stars", callback_data="buy_coins_50k")],
        [types.InlineKeyboardButton(text="👑 «Генерал армии»: 100 000 монет | ★ 2499 Stars",
                                    callback_data="buy_coins_100k")],

        # 🔥🏆 Раздел: Специальные предприимчивые предложения (Кланы и Спецпакеты)
        [types.InlineKeyboardButton(text="🏆 Лицензия Клана (до 1000 чел.) | ★ 2499 Stars",
                                    callback_data="buy_clan_upgrade")],
        [types.InlineKeyboardButton(text="🎁 Элитарный Бандл «VIP-Старт» | ★ 149 Stars",
                                    callback_data="buy_vip_start_bundle")],
        [types.InlineKeyboardButton(text=boost_btn_text,
                                    callback_data=f"buy_boost_upgrade" if boost_level < 3 else "boost_maxed_alert")],
        [types.InlineKeyboardButton(text="⚙️ Зайти в Ремонтную Мастерскую Роботов", callback_data="open_repair_shop")]
    ])

    shop_keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    shop_text = (
        f"🛒 <b>МАРКЕТПЛЭЙС ИГРOВOЙ ЭКOСИСТЕМЫ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"🚀 <b>Прокачай свой аккаунт и запусти пассивный доход!</b>\n"
        f"Покупки совершаются моментально через официальные звёзды Telegram Stars.\n\n"
        f"📌 <i>Твой текущий уровень заправки хаба: <b>CAPACITY {fridge_capacity}</b>\n"
        f"📌 Твой текущий Боевой Буст: <b>+{boost_level} к победе в дуэлях</b></i>\n\n"
        f"..................................................\n"
        f"👇 <b>ВЫБЕРИ ТОВAР ДЛЯ ПОКУПКИ:</b>"
    )
    await message.answer(shop_text, reply_markup=shop_keyboard, parse_mode="HTML")


# 🔥 БЕСШОВНЫЙ ПЕРЕХОД ИЗ МЕНЮ КИБЕР-ФЕРМЫ В МАГАЗИН
@router.callback_query(F.data == "open_shop_from_farm")
async def open_shop_from_farm_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_shop(callback.message)


# ============================================================================
# ⚙️ 2. РAЗДЕЛ: РЕМОНТНАЯ МАСТЕРСКАЯ РОБОТОВ (SaaS Подписка)
# ============================================================================
@router.callback_query(F.data == "open_repair_shop")
async def open_repair_shop_callback(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id

    async with db.pool.acquire() as conn:
        user = await conn.fetchrow("SELECT miner_premium_count FROM users WHERE user_id = $1", user_id)

    miner_count = user["miner_premium_count"] if user else 0

    repair_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🔧 Чинить пачку на 1 мес. | ★ 49", callback_data="repair_action:1"),
            types.InlineKeyboardButton(text="🔧 Чинить пачку на 3 мес. | ★ 129", callback_data="repair_action:3")
        ],
        [
            types.InlineKeyboardButton(text="⬅️ Вернуться в Магазин", callback_data="back_to_shop")
        ]
    ])

    repair_text = (
        f"🔧 <b>РЕМОНТНАЯ ИНЖЕНЕРНАЯ МАСТЕРСКАЯ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"🤖 Активных Кибер-Бурильщиков на балансе: <b>{miner_count} шт.</b>\n\n"
        f"🛠️ Здесь ты можешь продлить лицензию или починить сломанных роботов-майнеров пачками!\n\n"
        f"..................................................\n"
        f"👇 <b>ВЫБЕРИ СPОК ЛИЦЕНЗИИ ДЛЯ ВСЕЙ ПAЧКИ:</b>"
    )
    await callback.message.edit_text(repair_text, reply_markup=repair_keyboard, parse_mode="HTML")


# Возврат из ремонтной мастерской на главную витрину
@router.callback_query(F.data == "back_to_shop")
async def back_to_shop_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_shop(callback.message)


# Алерт для вожаков, вкачавших максимальный буст
@router.callback_query(F.data == "boost_maxed_alert")
async def boost_maxed_callback(callback: types.CallbackQuery):
    await callback.answer("👑 У тебя уже активирован ультимативный Боевой Буст максимального уровня!", show_alert=True)
