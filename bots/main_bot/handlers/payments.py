import logging
import random
from aiogram import Router, types, F
from aiogram.filters import Command
from shared.database import db
from bots.main_bot.catalog import calculate_stars_order

router = Router()
logger = logging.getLogger(__name__)


# ============================================================================
# 🎰 СИМУЛЯТОР УСПЕШНОЙ ОПЛАТЫ STARS (БЕЗ УЧАСТИЯ BOTFATHER)
# ============================================================================
@router.callback_query(F.data.startswith("buy_"))
async def process_shop_purchase_intent(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    payload = callback.data  # Имя кнопки (напр. 'buy_miner_premium')

    # Мгновенно гасим часики анимации Telegram на кнопке, чтобы они не висели!
    await callback.answer()

    # Вытягиваем текущие лимиты юзера из базы Railway
    async with db.pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT fridge_capacity, boost_level FROM users WHERE user_id = $1",
            user_id
        )

    current_capacity = user_data["fridge_capacity"] if user_data else 1
    current_boost = user_data["boost_level"] if user_data else 0

    try:
        # Проверяем товар через каталог
        order = calculate_stars_order(payload, current_capacity, current_boost)
    except ValueError as e:
        await callback.message.answer(f"❌ {e}")
        return

    # Генерируем случайный уникальный ID чека, как это делает Дуров
    charge_id = f"LOCAL_TEST_XTR_{random.randint(100000, 999999)}"

    # 🛡️ АТОМАРНАЯ ЗАПИСЬ В БАЗУ ДАННЫХ RAILWAY
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Навешиваем титановый замок FOR UPDATE
            user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                await callback.message.answer("⚠️ Профиль не найден. Нажми /start")
                return

            # Начисления по типам
            if order["type"] == "cutlets":
                await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $1 WHERE user_id = $2", order["qty"],
                                   user_id)
                result_msg = f"🥩 В твой карман инвентаря добавлено <b>{order['qty']} кибер-котлет</b>!"

            elif order["type"] == "miner":
                if order["kind"] == "junior":
                    await conn.execute(
                        "UPDATE users SET miner_junior_count = miner_junior_count + 1 WHERE user_id = $1", user_id)
                    result_msg = "🤖 <b>Робот «Младший Майнер» доставлен на твой завод!</b>"
                else:
                    await conn.execute(
                        "UPDATE users SET miner_premium_count = miner_premium_count + 1 WHERE user_id = $1", user_id)
                    result_msg = "⚡ <b>Титановый «Кибер Бурильщик» на гусеницах готов!</b>"

            elif order["type"] == "fridge_upgrade":
                await conn.execute("UPDATE users SET fridge_capacity = $1 WHERE user_id = $2", order["capacity"],
                                   user_id)
                result_msg = f"📦 Твой Холодильник расширен до уровня <b>CAPACITY {order['capacity']}</b>!"

            elif order["type"] == "coins":
                await conn.execute("UPDATE users SET balance = balance + $1 WHERE user_id = $2", order["coins_amount"],
                                   user_id)
                result_msg = f"💰 На твой счёт зачислено: <b>+{order['coins_amount']} рофлов</b>."

            elif order["type"] == "boost_upgrade":
                await conn.execute("UPDATE users SET boost_level = $1 WHERE user_id = $2", order["next_level"], user_id)
                result_msg = f"🚀 Уровень Боевого Буста повышен до <b>{order['next_level']} уровня</b>!"

            elif order["type"] == "vip_bundle":
                await conn.execute(
                    "UPDATE users SET miner_premium_count = miner_premium_count + 1, inv_cutlets = inv_cutlets + 30 WHERE user_id = $1",
                    user_id)
                result_msg = "🎁 <b>БАНДЛ «VIP-СТАРТ» АКТИВИРОВАН!</b>"

            # Записываем чек в базу для фин. отчётов
            await conn.execute(
                "INSERT INTO star_payments (user_id, telegram_charge_id, item_payload, stars_amount) VALUES ($1, $2, $3, $4)",
                user_id, charge_id, payload, order["stars"]
            )

    # Выводим сочный чек покупки на экран
    success_text = (
        f"💎 <b>[СИМУЛЯТOР] УСПЕШНАЯ ПОКУПКА!</b>\n"
        f"..................................................\n\n"
        f"🧾 Тестовый чек: <code>{charge_id}</code>\n"
        f"💵 Списано виртуально: <b>{order['stars']} ★</b>\n\n"
        f"..................................................\n\n"
        f"{result_msg}\n\n"
        f"📊 <i>Данные улетели в PostgreSQL на Railway! Проверь /farm или /my_stats!</i>"
    )
    await callback.message.answer(success_text, parse_mode="HTML")
