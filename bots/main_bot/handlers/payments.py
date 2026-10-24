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
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

from bots.main_bot.catalog import CatalogError, build_order, item_title, normalize_sku
from bots.main_bot.config import ADMIN_SECRET_CHANNEL_ID, is_shop_tester
from bots.main_bot.guards import feature_enabled
from shared.analytics import track
from shared.database import db
from shared.feature_flags import get_flag
from shared.delivery import DeliveryError, already_delivered, deliver_order, qualified_referrals_count
from shared.economy import INTERN_UPGRADE_REFERRALS
from shared.farm_logic import apply_lazy_farm
from shared.locales import t

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
    if order["type"] == "intern_upgrade":
        has_intern = await conn.fetchval(
            "SELECT 1 FROM miners WHERE user_id = $1 AND kind = 'intern' LIMIT 1", user_id)
        if not has_intern:
            return "Сначала активируй Робота Стажёра в /farm — апгрейдить пока некого."
        have = await qualified_referrals_count(conn, user_id)
        if have < INTERN_UPGRADE_REFERRALS:
            return (f"Для вечного Майнера нужно {INTERN_UPGRADE_REFERRALS} активных друга "
                    f"(у тебя {have}). Условия и ссылка — в /invite.")
    return None


async def _deliver_in_transaction(user_id: int, order: dict, charge_id: str,
                                  lang: str = "ru") -> tuple[bool, str]:
    """(True, текст) при успехе; (False, причина) если доставить нельзя. Исключения БД — наружу."""
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            if await already_delivered(conn, charge_id):
                return True, t(lang, "pay.already")
            # Сначала закрываем прошлое время по старым ставкам: купленный буст,
            # дрон или робот действует строго вперёд, а не задним числом.
            user, _ = await apply_lazy_farm(conn, user_id)
            if not user:
                return False, t(lang, "common.no_profile")
            try:
                text = await deliver_order(conn, user_id, order, charge_id, lang=lang)
            except DeliveryError as e:
                return False, str(e)
            return True, text


# ============================================================================
# 1. Нажатие кнопки товара: валидация и инвойс (или тест-выдача)
# ============================================================================
@router.callback_query(F.data.startswith("buy_"))
async def process_shop_purchase_intent(callback: types.CallbackQuery, bot: Bot, user_lang: str = "ru"):
    if not await feature_enabled(callback, "shop", user_lang):
        return
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
        ok, text = await _deliver_in_transaction(user_id, order, charge_id, user_lang)
        prefix = "🧪 <b>ТЕСТ-РЕЖИМ: товар выдан без оплаты</b>\n" if ok else "❌ <b>ТЕСТ-РЕЖИМ: доставка не удалась</b>\n"
        await callback.message.answer(f"{prefix}{text}\n<code>{charge_id}</code>", parse_mode="HTML")
        return

    title = item_title(order, user_lang)
    try:
        await bot.send_invoice(
            chat_id=user_id,
            title=title,
            description=t(user_lang, "pay.invoice_desc"),
            prices=[LabeledPrice(label=title, amount=order["stars"])],
            provider_token="",
            currency="XTR",
            payload=f"{order['sku']}:{order['stars']}",
        )
    except Exception:
        logger.exception("[STARS_INVOICE_ERROR] user=%s sku=%s", user_id, order["sku"])
        await callback.message.answer(t(user_lang, "pay.invoice_error"))


# ============================================================================
# 1.5 Поддержка платежей: /paysupport обязателен для ботов с цифровыми товарами
# ============================================================================
@router.message(Command("paysupport"))
async def cmd_paysupport(message: types.Message, user_lang: str = "ru"):
    await message.answer(t(user_lang, "pay.support"), parse_mode="HTML")


# ============================================================================
# 2. Pre-checkout: последняя проверка перед списанием Stars
# ============================================================================
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    user_id = pre_checkout_query.from_user.id
    payload = pre_checkout_query.invoice_payload

    if not await get_flag("shop"):   # магазин выключен с пульта — не берём деньги
        await pre_checkout_query.answer(ok=False, error_message=t("ru", "common.feature_off"))
        return

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
async def process_successful_payment(message: types.Message, bot: Bot, user_lang: str = "ru"):
    user_id = message.from_user.id
    payment = message.successful_payment
    charge_id = payment.telegram_payment_charge_id
    payload = payment.invoice_payload

    try:
        async with db.pool.acquire() as conn:
            order = await _load_order_for_user(conn, user_id, payload)
        ok, text = await _deliver_in_transaction(user_id, order, charge_id, user_lang)
    except Exception:
        logger.exception("[PAYMENT_DELIVERY_CRASH] user=%s charge=%s payload=%s", user_id, charge_id, payload)
        await _alert_admin(bot, f"🚨 Сбой доставки после оплаты!\nuser={user_id}\ncharge={charge_id}\npayload={payload}")
        await message.answer(t(user_lang, "pay.crash", charge=charge_id), parse_mode="HTML")
        return

    if ok:
        await track(user_id, "purchase", sku=order["sku"], stars=payment.total_amount)
        await message.answer(
            t(user_lang, "pay.success", charge=charge_id, stars=payment.total_amount, text=text),
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
        f"⚠️ {text}\n\n" + (t(user_lang, "pay.refunded") if refunded
                           else t(user_lang, "pay.keep_charge", charge=charge_id)),
        parse_mode="HTML")


async def _alert_admin(bot: Bot, text: str) -> None:
    if ADMIN_SECRET_CHANNEL_ID is None:
        return
    try:
        await bot.send_message(ADMIN_SECRET_CHANNEL_ID, text)
    except Exception:
        logger.exception("[ADMIN_ALERT_FAILED]")
