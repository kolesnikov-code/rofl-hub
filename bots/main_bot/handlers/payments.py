"""
Платёжный контур Telegram Stars.

Поток: кнопка buy_<sku> → валидация → инвойс → pre_checkout (повторная валидация)
→ successful_payment → deliver_order в транзакции с FOR UPDATE.

Защита:
- повторная доставка одного charge_id невозможна (проверка + UNIQUE);
- если товар нельзя выдать ПОСЛЕ оплаты (гонка: команда удалена и т.п.) — Stars возвращаются
  автоматически через refund_star_payment, админ получает тревогу.
"""
from __future__ import annotations

import logging
import uuid

from aiogram import Bot, F, Router, types
from aiogram.types import LabeledPrice, PreCheckoutQuery

from bots.main_bot.catalog import CatalogError, build_order, normalize_sku
from bots.main_bot.config import ADMIN_SECRET_CHANNEL_ID, is_shop_tester
from shared.database import db
from shared.delivery import DeliveryError, already_delivered, deliver_order

router = Router()
logger = logging.getLogger(__name__)


async def _load_order_for_user(conn, user_id: int, payload: str) -> dict:
    """Собирает заказ с учётом состояния игрока. Бросает CatalogError."""
    row = await conn.fetchrow("SELECT fridge_capacity FROM users WHERE user_id = $1", user_id)
    if row is None:
        raise CatalogError("Профиль не найден. Нажми /start для регистрации.")
    return build_order(payload, current_capacity=row["fridge_capacity"])


async def _precheck_deliverable(conn, user_id: int, order: dict) -> str | None:
    """Возвращает текст ошибки, если товар сейчас нельзя выдать, иначе None."""
    if order["type"] == "clan_upgrade":
        team = await conn.fetchrow("SELECT max_members FROM teams WHERE captain_id = $1", user_id)
        if not team:
            return "Мега-Клан можно купить только капитану уже созданной команды. Сначала /create_team."
        if team["max_members"] >= order["max_members"]:
            return "Твоя команда уже имеет статус Мега-Клана."
    return None


async def _deliver_in_transaction(user_id: int, order: dict, charge_id: str) -> tuple[bool, str]:
    """(True, текст) при успехе; (False, причина) если доставить нельзя. Исключения БД — наружу."""
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            if await already_delivered(conn, charge_id):
                return True, "✅ Этот платёж уже был обработан, товар выдан ранее."
            user = await conn.fetchrow("SELECT user_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            if not user:
                return False, "Профиль не найден."
            try:
                text = await deliver_order(conn, user_id, order, charge_id)
            except DeliveryError as e:
                return False, str(e)
            return True, text


# ============================================================================
# 1. Нажатие кнопки товара: валидация и инвойс (или тест-выдача)
# ============================================================================
@router.callback_query(F.data.startswith("buy_"))
async def process_shop_purchase_intent(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    payload = normalize_sku(callback.data)

    async with db.pool.acquire() as conn:
        try:
            order = await _load_order_for_user(conn, user_id, payload)
        except CatalogError as e:
            await callback.answer(str(e), show_alert=True)
            return
        problem = await _precheck_deliverable(conn, user_id, order)

    if problem:
        await callback.answer(problem, show_alert=True)
        return

    await callback.answer()

    if is_shop_tester(user_id):
        charge_id = f"TEST_{uuid.uuid4().hex[:16]}"
        ok, text = await _deliver_in_transaction(user_id, order, charge_id)
        prefix = "🧪 <b>ТЕСТ-РЕЖИМ: товар выдан без оплаты</b>\n" if ok else "❌ <b>ТЕСТ-РЕЖИМ: доставка не удалась</b>\n"
        await callback.message.answer(f"{prefix}{text}\n<code>{charge_id}</code>", parse_mode="HTML")
        return

    try:
        await bot.send_invoice(
            chat_id=user_id,
            title=order["title"],
            description="Мгновенная доставка внутриигрового контента ROFL HUB.",
            prices=[LabeledPrice(label=order["title"], amount=order["stars"])],
            provider_token="",
            currency="XTR",
            payload=f"{order['sku']}:{order['stars']}",
        )
    except Exception:
        logger.exception("[STARS_INVOICE_ERROR] user=%s sku=%s", user_id, order["sku"])
        await callback.message.answer("⚠️ Не удалось сформировать счёт Telegram Stars. Попробуй позже.")


# ============================================================================
# 2. Pre-checkout: последняя проверка перед списанием Stars
# ============================================================================
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    user_id = pre_checkout_query.from_user.id
    payload = pre_checkout_query.invoice_payload

    try:
        async with db.pool.acquire() as conn:
            order = await _load_order_for_user(conn, user_id, payload)
            problem = await _precheck_deliverable(conn, user_id, order)
    except CatalogError as e:
        await pre_checkout_query.answer(ok=False, error_message=str(e))
        return
    except Exception:
        logger.exception("[PRE_CHECKOUT_DB_ERROR] user=%s payload=%s", user_id, payload)
        await pre_checkout_query.answer(ok=False, error_message="Сервис временно недоступен. Попробуй через минуту.")
        return

    if problem:
        await pre_checkout_query.answer(ok=False, error_message=problem)
        return
    if pre_checkout_query.total_amount != order["stars"] or pre_checkout_query.currency != "XTR":
        logger.warning("[PRE_CHECKOUT_MISMATCH] user=%s payload=%s amount=%s", user_id, payload,
                       pre_checkout_query.total_amount)
        await pre_checkout_query.answer(ok=False, error_message="Сумма счёта не совпадает с ценой товара.")
        return

    await pre_checkout_query.answer(ok=True)


# ============================================================================
# 3. Успешная оплата: доставка, идемпотентность, авто-возврат при сбое
# ============================================================================
@router.message(F.successful_payment)
async def process_successful_payment(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    payment = message.successful_payment
    charge_id = payment.telegram_payment_charge_id
    payload = payment.invoice_payload

    try:
        async with db.pool.acquire() as conn:
            order = await _load_order_for_user(conn, user_id, payload)
        ok, text = await _deliver_in_transaction(user_id, order, charge_id)
    except Exception:
        logger.exception("[PAYMENT_DELIVERY_CRASH] user=%s charge=%s payload=%s", user_id, charge_id, payload)
        await _alert_admin(bot, f"🚨 Сбой доставки после оплаты!\nuser={user_id}\ncharge={charge_id}\npayload={payload}")
        await message.answer(
            "🚨 Оплата прошла, но доставка временно не удалась. Мы уже в курсе.\n"
            f"Сохрани номер платежа: <code>{charge_id}</code>", parse_mode="HTML")
        return

    if ok:
        await message.answer(
            "🎉 <b>Платёж подтверждён!</b>\n"
            f"🧾 <code>{charge_id}</code>\n💵 Списано: <b>{payment.total_amount} ★</b>\n\n{text}",
            parse_mode="HTML")
        return

    # Товар нельзя выдать — возвращаем Stars
    refunded = False
    try:
        refunded = await bot.refund_star_payment(user_id=user_id, telegram_payment_charge_id=charge_id)
    except Exception:
        logger.exception("[REFUND_FAILED] user=%s charge=%s", user_id, charge_id)
    await _alert_admin(bot, f"⚠️ Доставка отклонена: {text}\nuser={user_id}\ncharge={charge_id}\nrefund={refunded}")
    await message.answer(
        f"⚠️ {text}\n\n" + ("💫 Stars возвращены на твой счёт автоматически." if refunded
                           else f"Сохрани номер платежа для возврата: <code>{charge_id}</code>"),
        parse_mode="HTML")


async def _alert_admin(bot: Bot, text: str) -> None:
    if ADMIN_SECRET_CHANNEL_ID is None:
        return
    try:
        await bot.send_message(ADMIN_SECRET_CHANNEL_ID, text)
    except Exception:
        logger.exception("[ADMIN_ALERT_FAILED]")
