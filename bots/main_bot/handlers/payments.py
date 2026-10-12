import logging
import random
import os
from aiogram import Router, types, F, Bot
from aiogram.types import LabeledPrice, PreCheckoutQuery
from shared.database import db
from bots.main_bot.catalog import calculate_stars_order

router = Router()
logger = logging.getLogger(__name__)

# 🔥 ТУМБЛЕР БЕЗОПАСНОСТИ АНАТОЛИЯ АЛЕКСЕЕВИЧА
# Впиши сюда свой реальный Telegram ID, чтобы тестировать покупки бесплатно!
ADMIN_TESTER_ID = 227653457  # Подставить актуальный ID при деплое


# ============================================================================
# 🏪 1. ПЕРЕХВАТ НАЖАТИЯ КНОПОК КАТАЛОГА (ГЕНЕРАЦИЯ ИНВОЙСА / ТЕСТ-РЕЖИМ)
# ============================================================================
@router.callback_query(F.data.startswith("buy_"))
async def process_shop_purchase_intent(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    payload = callback.data

    await callback.answer()

    # Извлекаем текущие лимиты игрока из PostgreSQL на Railway
    async with db.pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT fridge_capacity, boost_level FROM users WHERE user_id = $1",
            user_id
        )

    current_capacity = user_data["fridge_capacity"] if user_data else 1
    current_boost = user_data["boost_level"] if user_data else 0

    if payload == "buy_boost_upgrade":
        next_level = current_boost + 1
        if next_level > 3:
            await callback.message.answer("❌ Достигнут максимальный уровень Боевого Буста!")
            return
        payload = f"boost:{next_level}"

    try:
        # Валидируем покупку через единый бэкенд-каталог
        order = calculate_stars_order(payload, current_capacity, current_boost)
    except ValueError as e:
        await callback.message.answer(f"❌ {e}")
        return

    # 🛡️ ПРОВЕРКА ТУМБЛEРА: ЕСЛИ КЛИКАЕТ ТЕСТИРОВЩИК — ВЫДАЕМ МГНОВЕННО И БЕСПЛАТНО
    if user_id == ADMIN_TESTER_ID:
        charge_id = f"LOCAL_TEST_XTR_{random.randint(100000, 999999)}"
        success, result_msg = await award_item_to_user(user_id, order, payload, charge_id)

        if success:
            success_text = (
                f"💎 <b>ТЕСТОВЫЙ РЕЖИМ АКТИВИРОВАН (ID: {user_id})</b>\n"
                f"..................................................\n\n"
                f"🧾 Чек симулятора: <code>{charge_id}</code>\n"
                f"💵 Стоимость: <s>{order['stars']} ★</s> (Списано: 0 ★)\n\n"
                f"..................................................\n\n"
                f"{result_msg}\n\n"
                f"📊 <i>База данных Railway обновлена без реальных затрат Stars. Проверяй!</i>"
            )
            await callback.message.answer(success_text, parse_mode="HTML")
        else:
            await callback.message.answer(f"❌ Ошибка начисления: {result_msg}")
        return

    # 💳 РЕЖИМ РЕАЛЬНОГО КИТа: ВЫКАTЫВАЕМ ОФИЦИАЛЬНЫЙ ПЛАТЕЖНЫЙ ШЛЮЗ TELEGRAM STARS
    prices = [LabeledPrice(label="XTR", amount=order["stars"])]

    try:
        await bot.send_invoice(
            chat_id=user_id,
            title=order["title"],
            description=f"Покупка и мгновенная доставка внутриигрового контента холдинга ROFL HUB CORE.",
            prices=prices,
            provider_token="",  # Строго пустая строка для Telegram Stars (XTR)
            currency="XTR",
            payload=f"{payload}:{order['stars']}",  # Запечатываем параметры в payload чека
            start_parameter="rofl_hub_shop"
        )
    except Exception as e:
        logger.error(f"[STARS_INVOICE_ERROR] Ошибка отправки инвойса: {e}")
        await callback.message.answer("⚠️ Не удалось сформировать чек Telegram Stars. Попробуй позже.")


# ============================================================================
# 🛡️ 2. ВАЛИДАЦИЯ ПЛАТЕЖА ЗА 10 СЕКУНД ДО СПИСАНИЯ (PRE-CHECKOUT)
# ============================================================================
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """
    Официальный шлюз окончательной верификации платежа серверами Telegram.
    Проверяет, не пытается ли читер купить уже заполненный холодильник.
    """
    user_id = pre_checkout_query.from_user.id
    payload = pre_checkout_query.invoice_payload.split(":")[0]

    async with db.pool.acquire() as conn:
        user_data = await conn.fetchrow("SELECT fridge_capacity, boost_level FROM users WHERE user_id = $1", user_id)

    if not user_data:
        await pre_checkout_query.answer(ok=False, error_message="Профиль игрока не найден в PostgreSQL. Нажми /start")
        return

    # Дополнительная защита на этапе Pre-Checkout
    if payload.startswith("buy_fridge_"):
        target_capacity = int(payload.split("_")[-1])
        if target_capacity <= user_data["fridge_capacity"]:
            await pre_checkout_query.answer(ok=False,
                                            error_message="🚨 Читерство! Твой холодильник уже равен или больше этого уровня.")
            return

    # Железно одобряем списание звезд
    await pre_checkout_query.answer(ok=True)


# ============================================================================
# 🎰 3. РЕАЛЬНОЕ НАЧИСЛЕНИЕ КОНТЕНТА ПОСЛЕ УСПЕШНОЙ ОПЛАТЫ (SUCCESSFUL PAYMENT)
# ============================================================================
@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message):
    """
    Срабатывает ТОЛЬКО тогда, когда Telegram Stars официально списаны со счета.
    Выдача товара на 100% запечатана. Избавлено от фейковых начислений.
    """
    user_id = message.from_user.id
    payment_info = message.successful_payment
    charge_id = payment_info.telegram_payment_charge_id  # Официальный ID транзакции Telegram

    payload = payment_info.invoice_payload.split(":")[0]

    async with db.pool.acquire() as conn:
        user_data = await conn.fetchrow("SELECT fridge_capacity, boost_level FROM users WHERE user_id = $1", user_id)

    current_capacity = user_data["fridge_capacity"] if user_data else 1
    current_boost = user_data["boost_level"] if user_data else 0

    order = calculate_stars_order(payload, current_capacity, current_boost)

    success, result_msg = await award_item_to_user(user_id, order, payload, charge_id)

    if success:
        success_text = (
            f"🎉 <b>ПЛАТЕЖ УСПЕШНО ПОДТВЕРЖДЕН!</b>\n"
            f"..................................................\n\n"
            f"🧾 ID Транзакции: <code>{charge_id}</code>\n"
            f"💵 Зачислено Stars: <b>{order['stars']} ★</b>\n\n"
            f"..................................................\n\n"
            f"{result_msg}\n\n"
            f"📊 <i>Продукт доставлен на твой аккаунт на Railway. Баланс обновлен в /profile! Спасибо за поддержку хаба!</i>"
        )
        await message.answer(success_text, parse_mode="HTML")
    else:
        await message.answer(f"🚨 КРИТИЧЕСКАЯ ОШИБКА ДОСТАВКИ: {result_msg}\nСрочно отправь этот чек администрации!")


# ============================================================================
# ⚙️ 4. АТОМАРНЫЙ БЭКЕНД-ОБРАБОТЧИК НАЧИСЛЕНИЙ РЕСУРСОВ В БАЗУ
# ============================================================================
async def award_item_to_user(user_id: int, order: dict, payload: str, charge_id: str) -> tuple[bool, str]:
    """Транзакционный контур начисления купленных товаров с защитой FOR UPDATE"""
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
                if not user:
                    return False, "Профиль не найден"

                if order["type"] == "cutlets":
                    # 🔥 ФИКС: Переносим котлеты НА СКЛАД инвентаря, как решено по архитектуре!
                    await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $1 WHERE user_id = $2", order["qty"], user_id)
                    result_msg = f"🥩 В твой карман инвентаря (на склад) добавлено: <b>{order['qty']} шт.</b>"

                elif order["type"] == "miner":
                    if order["kind"] == "junior":
                        await conn.execute("UPDATE users SET miner_junior_count = miner_junior_count + 1 WHERE user_id = $1", user_id)
                        result_msg = "🤖 <b>Робот «Младший Майнер» доставлен на твой ИТ-завод!</b>"
                    else:
                        await conn.execute("UPDATE users SET miner_premium_count = miner_premium_count + 1 WHERE user_id = $1", user_id)
                        result_msg = "⚡ <b>Титановый «Кибер Бурильщик» на гусеницах готов к работе!</b>"

                elif order["type"] == "fridge_upgrade":
                    await conn.execute("UPDATE users SET fridge_capacity = $1 WHERE user_id = $2", order["capacity"], user_id)
                    result_msg = f"📦 Твой Автоматический Холодильник расширен до уровня: <b>CAPACITY {order['capacity']}</b>"

                elif order["type"] == "coins":
                    await conn.execute("UPDATE users SET balance = balance + $1 WHERE user_id = $2", order["coins_amount"], user_id)
                    result_msg = f"💰 На твой счёт зачислено розничной казны: <b>+{order['coins_amount']} рофлов</b>."

                elif order["type"] == "boost_upgrade":
                    await conn.execute("UPDATE users SET boost_level = $1 WHERE user_id = $2", order["next_level"], user_id)
                    result_msg = f"🚀 Уровень Боевого Буста повышен навсегда до: <b>{order['next_level']} уровня</b>!"

                elif order["type"] == "vip_bundle":
                    await conn.execute(
                        "UPDATE users SET miner_premium_count = miner_premium_count + 1, inv_cutlets = inv_cutlets + 30 WHERE user_id = $1",
                        user_id
                    )
                    result_msg = "🎁 <b>ЭЛИТАРНЫЙ БАНДЛ «VIP-СТАРТ» АКТИВИРОВАН!</b>\n⚡ Получен 1 Кибер-Бурильщик.\n🥩 На склад закинуто 30 котлет!"

                elif order["type"] == "clan_upgrade":
                    team = await conn.fetchrow("SELECT team_id FROM teams WHERE captain_id = $1 FOR UPDATE", user_id)
                    if not team:
                        return False, "У тебя нет созданной команды! Сначала вбей /create_team."
                    await conn.execute("UPDATE teams SET max_members = 1000 WHERE captain_id = $1", user_id)
                    result_msg = "🏆 <b>ТВОЯ КОМАНДА ОФИЦИАЛЬНО ПОЛУЧИЛА ВЫСШИЙ СТАТУС КЛАНА СНГ!</b>\nЛимит расширен до 1000 мест."

                # Фиксируем финансовую операцию в журнал для строгого аудита
                await conn.execute(
                    """
                    INSERT INTO star_payments (user_id, telegram_charge_id, item_payload, stars_amount) 
                    VALUES ($1, $2, $3, $4)
                    """,
                    user_id, charge_id, payload, order["stars"]
                )

                return True, result_msg
    except Exception as e:
        logger.error(f"[DATABASE_AWARD_ERROR] Ошибка записи транзакции: {e}")
        return False, str(e)
