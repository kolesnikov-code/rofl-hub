from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()


# ----------------------------------------------------------------
# 🏪 ГЛАВНАЯ ВИТРИНА МАГАЗИНА
# ----------------------------------------------------------------
@router.message(Command("shop"))
@router.message(Command("buy_miner"))
@router.message(Command("buy_coins"))
async def cmd_shop_catalog(message: types.Message):
    shop_text = (
        "🏪 <b>МАРКЕТПЛЕЙС ИГРОВЫХ ТОВАРОВ ROFL HUB</b>\n"
        "..................................................\n"
        "🤖 <b>Прокачай свой аккаунт и запусти пассивный доход!</b>\n"
        "Покупки совершаются моментально через официальные звёзды Telegram Stars.\n"
        "..................................................\n"
        "👇 <b>ВЫБЕРИ ТОВАР ДЛЯ ПОКУПКИ:</b>"
    )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🤖 Робот «Младший Майнер» | ★ 49 Stars", callback_data="buy_miner_junior")],
        [types.InlineKeyboardButton(text="⚡ Робот «Кибер Бурильщик» | ★ 99 Stars", callback_data="buy_miner_premium")],
        [types.InlineKeyboardButton(text="📦 Холодильник на 2 котлеты | ★ 49 Stars", callback_data="buy_slot_2")],
        [types.InlineKeyboardButton(text="🔒 Холодильник на 3 котлеты | ★ 99 Stars", callback_data="buy_slot_3")],
        [types.InlineKeyboardButton(text="🥩 Пакет «Кибер-котлеты» (3 шт.) | ★ 9 Stars", callback_data="buy_cutlets_pack")],
        [types.InlineKeyboardButton(text="🚀 Буст (+2 монеты за победу) | ★ 79 Stars", callback_data="buy_boost_win")],
        [types.InlineKeyboardButton(text="💸 \"Бизнесмен\": 1 500 монет | ★ 49 Stars", callback_data="buy_coins_1500")],
        [types.InlineKeyboardButton(text="💰 \"Олигарх\": 10 000 монет | ★ 299 Stars", callback_data="buy_coins_10k")],
        [types.InlineKeyboardButton(text="👑 \"Президент\": 50 000 монет | ★ 999 Stars", callback_data="buy_coins_50k")]
    ])
    await message.answer(shop_text, reply_markup=keyboard, parse_mode="HTML")


# ----------------------------------------------------------------
# 💳 ПЕРЕХВАТЧИКИ КЛИКОВ (CALLBACK QUERIES)
# ----------------------------------------------------------------
@router.callback_query(F.data.startswith("buy_"))
async def process_shop_purchase(callback: types.CallbackQuery):
    product_type = callback.data

    # Психологический триггер для Казны Олигарха за ★ 999 Stars!
    if product_type == "buy_coins_50k":
        invoice_text = (
            "💎 <b>ОФОРМЛЕНИЕ ЗАКАЗА: КАЗНА \"ПРЕЗИДЕНТ\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>50 000 рофлов</b>\n"
            "💳 Стоимость: <b>★ 999 Telegram Stars</b>\n"
            "..................................................\n"
            "🔥 <i>Этого количества монет тебе хватит на шикарные донаты в ROFL HUB!</i>\n\n"
            "🔒 Шлюз безопасной покупки активирован. Кнопка оплаты Stars появится ниже..."
        )
    # Психологический триггер для Премиум Бурильщика за ★ 99 Stars!
    elif product_type == "buy_miner_premium":
        invoice_text = (
            "⚡ <b>ОФОРМЛЕНИЕ ЗАКАЗА: \"КИБЕР-БУРИЛЬЩИК\"</b>\n"
            "..................................................\n"
            "🎁 Товар: <b>робот-майнер 5-го поколения (Лицензия на 30 дней)</b>\n"
            "⚡ Скорость добычи - 5 монет в час\n"
            "💳 Стоимость: <b>★ 99 Stars</b>\n"
            "..................................................\n"
            "🤖 <i>Станок начнет круглосуточно качать тебе монеты! Главное — не забывай кормить его кибер-котлетами.</i>"
        )
    else:
        invoice_text = f"⚙️ <b>Модуль оплаты товара [{product_type}] вызван успешно!</b>\nШлюз Telegram Stars (XTR) готовится к приему транзакции."

    await callback.message.edit_text(invoice_text, parse_mode="HTML")
    await callback.answer()
