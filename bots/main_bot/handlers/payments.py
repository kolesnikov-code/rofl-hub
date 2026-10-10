import logging
import random
from aiogram import Router, types, F
from shared.database import db
from bots.main_bot.catalog import calculate_stars_order

router = Router()
logger = logging.getLogger(__name__)


# Вспомогательный метод сборки клавиатуры, чтобы обновить маркет на лету
def get_updated_shop_keyboard(fridge_capacity: int, boost_level: int) -> types.InlineKeyboardMarkup:
    if boost_level == 0:
        boost_btn_text = "🚀 Купить Боевой Буст I Ур. | ★ 99 Stars"
    elif boost_level == 1:
        boost_btn_text = "🚀🚀 Апгрейд Буста до II Ур. | ★ 199 Stars"
    elif boost_level == 2:
        boost_btn_text = "🚀🚀🚀 Апгрейд Буста до III Ур. | ★ 299 Stars"
    else:
        boost_btn_text = "👑 МАКСИМАЛЬНЫЙ БУСТ АКТИВИРОВАН"

    buttons = [
        [types.InlineKeyboardButton(text="🤖 Робот «Младший Майнер» | ★ 49 Stars", callback_data="buy_miner_junior")],
        [types.InlineKeyboardButton(text="⚡ Робот «Кибер Бурильщик» | ★ 99 Stars", callback_data="buy_miner_premium")],
        [types.InlineKeyboardButton(text="🥩 1 кибер-котлета | ★ 7 Stars", callback_data="buy_cutlet_1")],
        [types.InlineKeyboardButton(text="🥩 5 кибер-котлет | ★ 29 Stars", callback_data="buy_cutlet_5")],
        [types.InlineKeyboardButton(text="🥩 10 кибер-котлет | ★ 49 Stars", callback_data="buy_cutlet_10")],
        [types.InlineKeyboardButton(text="🥩 50 кибер-котлет | ★ 239 Stars", callback_data="buy_cutlet_50")],
        [types.InlineKeyboardButton(text="🥩 100 кибер-котлет | ★ 449 Stars", callback_data="buy_cutlet_100")]
    ]

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

    buttons.extend([
        [types.InlineKeyboardButton(text="💰 «Солдат»: 1 000 монет | ★ 49 Stars", callback_data="buy_coins_1k")],
        [types.InlineKeyboardButton(text="💰 «Капитан»: 3 000 монет | ★ 99 Stars", callback_data="buy_coins_3k")],
        [types.InlineKeyboardButton(text="💰 «Ветеран»: 10 000 монет | ★ 299 Stars", callback_data="buy_coins_10k")],
        [types.InlineKeyboardButton(text="👑 «Легенда»: 50 000 монет | ★ 1299 Stars", callback_data="buy_coins_50k")],
        [types.InlineKeyboardButton(text="👑 «Генерал армии»: 100 000 монет | ★ 2499 Stars",
                                    callback_data="buy_coins_100k")],
        [types.InlineKeyboardButton(text="🏆 Лицензия Клана (до 1000 чел.) | ★ 2499 Stars",
                                    callback_data="buy_clan_upgrade")],
        [types.InlineKeyboardButton(text="🎁 Элитарный Бандл «VIP-Старт» | ★ 149 Stars",
                                    callback_data="buy_vip_start_bundle")],
        [types.InlineKeyboardButton(text=boost_btn_text,
                                    callback_data="buy_boost_upgrade" if boost_level < 3 else "boost_maxed_alert")],
        [types.InlineKeyboardButton(text="⚙️ Зайти в Ремонтную Мастерскую Роботов", callback_data="open_repair_shop")]
    ])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


# ============================================================================
# 🏪 ЛОКАЛЬНЫЙ СИМУЛЯТОР СКАЧИВАНИЯ STARS (С ДИНАМИЧЕСКИМ АПДЕЙТОМ КНОПОК)
# ============================================================================
@router.callback_query(F.data.startswith("buy_"))
async def process_shop_purchase_intent(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    payload = callback.data

    await callback.answer()

    async with db.pool.acquire() as conn:
        user_data = await conn.fetchrow("SELECT fridge_capacity, boost_level FROM users WHERE user_id = $1", user_id)

    current_capacity = user_data["fridge_capacity"] if user_data else 1
    current_boost = user_data["boost_level"] if user_data else 0

    if payload == "buy_boost_upgrade":
        next_level = current_boost + 1
        if next_level > 3:
            await callback.message.answer("❌ Достигнут максимальный уровень буста!")
            return
        payload = f"boost:{next_level}"

    try:
        order = calculate_stars_order(payload, current_capacity, current_boost)
    except ValueError as e:
        await callback.message.answer(f"❌ {e}")
        return

    charge_id = f"LOCAL_TEST_XTR_{random.randint(100000, 999999)}"
    result_msg = ""

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                return

            if order["type"] == "cutlets":
                await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $1 WHERE user_id = $2", order["qty"],
                                   user_id)
                result_msg = f"🥩 В твой карман инвентаря успешно добавлено: <b>{order['qty']} шт.</b>"

            elif order["type"] == "miner":
                if order["kind"] == "junior":
                    await conn.execute(
                        "UPDATE users SET miner_junior_count = miner_junior_count + 1 WHERE user_id = $1", user_id)
                    result_msg = "🤖 <b>Робот «Младший Майнер» успешно доставлен на твой завод!</b>"
                else:
                    await conn.execute(
                        "UPDATE users SET miner_premium_count = miner_premium_count + 1 WHERE user_id = $1", user_id)
                    result_msg = "⚡ <b>Титановый «Кибер Бурильщик» на гусеницах готов к работе!</b>"

            elif order["type"] == "fridge_upgrade":
                await conn.execute("UPDATE users SET fridge_capacity = $1 WHERE user_id = $2", order["capacity"],
                                   user_id)
                result_msg = f"📦 Твой Центральный Холодильник расширен до уровня: <b>CAPACITY {order['capacity']}</b>"

            elif order["type"] == "coins":
                await conn.execute("UPDATE users SET balance = balance + $1 WHERE user_id = $2", order["coins_amount"],
                                   user_id)
                result_msg = f"💰 На твой счёт успешно зачислено: <b>+{order['coins_amount']} рофлов</b>."

            elif order["type"] == "boost_upgrade":
                await conn.execute("UPDATE users SET boost_level = $1 WHERE user_id = $2", order["next_level"], user_id)
                result_msg = f"🚀 Уровень твоего Боевого Буста повышен до: <b>{order['next_level']} уровня</b>!"

            elif order["type"] == "vip_bundle":
                await conn.execute(
                    "UPDATE users SET miner_premium_count = miner_premium_count + 1, inv_cutlets = inv_cutlets + 30 WHERE user_id = $1",
                    user_id)
                result_msg = "🎁 <b>ЭЛИТАРНЫЙ БАНДЛ «VIP-СТАРТ» АКТИВИРОВАН!</b>"

            elif order["type"] == "clan_upgrade":
                team = await conn.fetchrow("SELECT team_id, max_members FROM teams WHERE captain_id = $1", user_id)
                if not team:
                    await callback.message.answer(
                        "❌ Чтобы купить Клан, сначала создай базовую Команду за 100 000 монет через /create_clan!")
                    return
                await conn.execute("UPDATE teams SET max_members = 1000 WHERE captain_id = $1", user_id)
                result_msg = "🏆 <b>ТВОЯ БАНДА ОФИЦИАЛЬНО ПОЛУЧИЛА СТАТУС МЕГА-КЛАНА!</b>"

            await conn.execute(
                "INSERT INTO star_payments (user_id, telegram_charge_id, item_payload, stars_amount) VALUES ($1, $2, $3, $4)",
                user_id, charge_id, payload, order["stars"]
            )

            # Вытягиваем свежие лимиты для мгновенного апдейта интерфейса
            updated = await conn.fetchrow("SELECT fridge_capacity, boost_level FROM users WHERE user_id = $1", user_id)

    success_text = (
        f"💎 <b>УСПЕШНАЯ ТРАНЗАКЦИЯ СИМУЛЯТОРА</b>\n"
        f"..................................................\n\n"
        f"🧾 Чек платежа: <code>{charge_id}</code>\n"
        f"💵 Сумма списания: <b>{order['stars']} ★</b>\n\n"
        f"..................................................\n\n"
        f"{result_msg}"
    )
    await callback.message.answer(success_text, parse_mode="HTML")

    # 🔥 ХАК ДИНАМИКИ: Мгновенно перерисовываем старое сообщение магазина, меняя текст кнопки на лету!
    try:
        updated_text = (
            f"🛒 <b>МАРКЕТПЛЭЙС ИГРOВOЙ ЭКOСИСТЕМЫ ROFL HUB</b>\n"
            f"..................................................\n\n"
            f"🚀 <b>Прокачай свой аккаунт и запусти пассивный доход!</b>\n\n"
            f"📌 <i>Твой уровень заправки хаба: <b>CAPACITY {updated['fridge_capacity']}</b>\n"
            f"📌 Твой Боевой Буст: <b>+{updated['boost_level']} к победе в дуэлях</b></i>"
        )
        await callback.message.edit_text(
            text=updated_text,
            reply_markup=get_updated_shop_keyboard(updated["fridge_capacity"], updated["boost_level"]),
            parse_mode="HTML"
        )
    except Exception:
        pass

# ============================================================================
# 🛡️ БОЕВОЙ ШЛЮЗ TELEGRAM STARS (АКТИВИРУЕТСЯ ПРИ ДЕПЛОЕ НА HTTPS СЕРВЕР)
# ============================================================================
# Когда будешь переносить проект на боевой сервер, этот блок заменит симулятор выше.
# @router.pre_checkout_query()
# async def process_pre_checkout_stars(pre_checkout_query: types.PreCheckoutQuery):
#     await pre_checkout_query.answer(ok=True)

# @router.message(F.successful_payment)
# async def process_successful_stars_payment(message: types.Message):
#     # Сюда копируется аналогичная логика начислений из симулятора
#     pass
