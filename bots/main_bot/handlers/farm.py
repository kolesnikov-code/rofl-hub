import logging
from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command

from shared.database import db
from shared.economy import (
    daily_bonus_seconds_left,
    is_active,
    miner_hourly_rate,
    utcnow,
)
from shared.farm_logic import MinerState, apply_lazy_farm, farm_counts

router = Router()
logger = logging.getLogger(__name__)


def get_farm_keyboard() -> types.InlineKeyboardMarkup:
    """Кнопки фермы: ежедневный бонус, заправка и переход в магазин."""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🎁 ЗАБРАТЬ БОНУС (котлета раз в 24 ч)",
                                       callback_data="farm_action:daily_bonus")
        ],
        [
            types.InlineKeyboardButton(text="🥩 Заправить 1 шт.", callback_data="farm_action:load_1"),
            types.InlineKeyboardButton(text="⚡ Заправить ВСЕ", callback_data="farm_action:load_all")
        ],
        [
            types.InlineKeyboardButton(text="🏪 Зайти в Магазин /shop", callback_data="open_shop_from_farm")
        ]
    ])


def render_farm_text(user, miners: list[MinerState], now: datetime) -> str:
    """Единый текст дашборда фермы: роботы из таблицы miners, ставки с бустами."""
    counts = farm_counts(miners, now)
    junior_count = counts["junior"]
    premium_count = counts["premium"]
    fueled_count = counts["premium_fueled"]
    total_miners = junior_count + premium_count

    nuclear = is_active(user["boost_nuclear_until"], now)
    nitrogen = is_active(user["boost_nitrogen_until"], now)
    junior_rate = miner_hourly_rate("junior", nuclear_active=nuclear, nitrogen_active=nitrogen)
    premium_rate = miner_hourly_rate("premium", nuclear_active=nuclear, nitrogen_active=nitrogen)

    # В «актуальной скорости» бурильщики считаются только заправленные
    speed_per_hour = junior_count * junior_rate + fueled_count * premium_rate
    speed_per_day = speed_per_hour * 24

    boosts = []
    if nuclear:
        boosts.append(f"🔋 Ядерный Разгон x5 до {user['boost_nuclear_until']:%d.%m %H:%M} UTC (расход котлет ×3)")
    if nitrogen:
        boosts.append(f"❄️ Азотное Охлаждение +40% до {user['boost_nitrogen_until']:%d.%m %H:%M} UTC")
    if is_active(user["drone_until"], now):
        boosts.append(f"🛸 Мастер-дрон продлевает жизнь роботов до {user['drone_until']:%d.%m.%Y} UTC")
    boosts_block = "\n".join(boosts) if boosts else "Нет активных усилений — загляни в /shop."

    if premium_count > 0:
        if fueled_count == premium_count:
            status_work = "🟢 Все Кибер-Бурильщики заправлены и добывают монеты!"
        elif fueled_count > 0:
            status_work = (f"🟡 Заправлено {fueled_count} из {premium_count} Кибер-Бурильщиков. "
                           f"Остальные ждут котлет в холодильнике!")
        else:
            status_work = "🔴 Кибер-Бурильщики остановились! В холодильнике не хватает топлива."
    else:
        status_work = "💡 Заведи Кибер-Бурильщиков в /shop для увеличения дохода."

    alive = [m for m in miners if m.expires_at > now]
    burnout_line = ""
    if alive:
        nearest = min(m.expires_at for m in alive)
        burnout_line = f"🔥 Ближайшее сгорание робота: <b>{nearest:%d.%m.%Y %H:%M} UTC</b>\n"

    return (
        f"🚜 <b>ЦЕНТРАЛЬНЫЙ ТОПЛИВНЫЙ ХАБ ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"🤖 Активных роботов на заводе: <b>{total_miners} шт.</b>\n"
        f"• Младшие Майнеры ({junior_rate} рофлов/ч): <code>{junior_count} шт.</code>\n"
        f"• Кибер-Бурильщики ({premium_rate} рофлов/ч): <code>{premium_count} шт.</code>\n"
        f"{burnout_line}\n"
        f"📊 <b>АКТУАЛЬНАЯ СКОРОСТЬ ТВОЕЙ ФЕРМЫ:</b>\n"
        f"• Выработка в час: <b>+{speed_per_hour} рофлов</b>\n"
        f"• Выработка в сутки: <b>+{speed_per_day} рофлов</b>\n\n"
        f"⚡ <b>УСИЛЕНИЯ:</b>\n{boosts_block}\n\n"
        f"📋 <b>СТАТУС ИГРОВОГО ЗАВОДА:</b>\n"
        f"{status_work}\n\n"
        f"..................................................\n\n"
        f"📦 <b>СОСТОЯНИЕ АВТОМАТИЧЕСКОГО ХОЛОДИЛЬНИКА:</b>\n"
        f"🥩 Запас топлива: <b>{user['fridge_cutlets']} / {user['fridge_capacity']} шт.</b>\n"
        f"💼 Котлеты на складе инвентаря: <code>{user['inv_cutlets']} шт.</code>\n\n"
        f"..................................................\n\n"
        f"<i>💿 Важно: роботы живут 30 дней (Мастер-дрон приостанавливает износ). "
        f"Кибер-Бурильщик списывает целую котлету из холодильника на каждые 24 часа работы. "
        f"Следи за заправкой!</i>"
    )


# ============================================================================
# 🚜 1. ЦЕНТРАЛЬНЫЙ УНИВЕРСАЛЬНЫЙ ВЫЗОВ ПАНЕЛИ ФЕРМЫ
# ============================================================================
@router.message(Command("farm"))
@router.message(Command("my_farm"))
@router.message(F.text == "🚜 МОЯ ФЕРМА")
async def cmd_farm(message: types.Message, override_user_id: int = None):
    """
    Выводит дашборд топливного хаба фермы.
    Параметр override_user_id намертво страхует от падения при инлайн-переходах.
    """
    user_id = override_user_id if override_user_id else message.from_user.id
    now = utcnow()

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user, miners = await apply_lazy_farm(conn, user_id, now)

    if not user:
        await message.answer("⚠️ Профиль не найден. Прожми /start для регистрации Паспорта.")
        return

    await message.answer(render_farm_text(user, miners, now),
                         reply_markup=get_farm_keyboard(), parse_mode="HTML")


# ============================================================================
# 🎰 2. ИНЛАЙН-ДЕЙСТВИЯ: БОНУС, ЗАПРАВКА, ОБНОВЛЕНИЕ ЭКРАНА
# ============================================================================
@router.callback_query(F.data.startswith("farm_action:"))
async def process_farm_inline_actions(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    if len(parts) < 2:
        await callback.answer()
        return
    action = parts[1]
    now = utcnow()
    toast: str | None = None
    extra_message: str | None = None

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Сначала ленивый пересчёт (он же блокирует строку users FOR UPDATE)
            user, miners = await apply_lazy_farm(conn, user_id, now)
            if not user:
                await callback.answer("⚠️ Профиль не найден. Прожми /start", show_alert=True)
                return

            if action == "daily_bonus":
                seconds_left = daily_bonus_seconds_left(user["last_bonus_claim_at"], now)
                if seconds_left > 0:
                    hours, rem = divmod(seconds_left, 3600)
                    toast = f"⏳ Бонус уже забран! Следующая котлета через {hours} ч {rem // 60} мин."
                else:
                    await conn.execute(
                        "UPDATE users SET inv_cutlets = inv_cutlets + 1, last_bonus_claim_at = $2 "
                        "WHERE user_id = $1",
                        user_id, now)
                    toast = "🎁 Кибер-котлета зачислена на склад! Возвращайся через 24 часа."

            elif action == "load_1":
                if user["inv_cutlets"] <= 0:
                    extra_message = "❌ У тебя в инвентаре нет кибер-котлет! Купи их в /shop"
                elif user["fridge_cutlets"] >= user["fridge_capacity"]:
                    extra_message = "📦 Твой Холодильник уже полностью забит!"
                else:
                    await conn.execute(
                        "UPDATE users SET inv_cutlets = inv_cutlets - 1, fridge_cutlets = fridge_cutlets + 1 "
                        "WHERE user_id = $1",
                        user_id)

            elif action == "load_all":
                available_space = user["fridge_capacity"] - user["fridge_cutlets"]
                if user["inv_cutlets"] <= 0:
                    extra_message = "❌ У тебя в инвентаре нет кибер-котлет!"
                elif available_space <= 0:
                    extra_message = "📦 Твой Холодильник забит до отказа!"
                else:
                    actual_load = min(user["inv_cutlets"], available_space)
                    await conn.execute(
                        "UPDATE users SET inv_cutlets = inv_cutlets - $1, fridge_cutlets = fridge_cutlets + $1 "
                        "WHERE user_id = $2",
                        actual_load, user_id)

            # Повторный пересчёт со свежим «сейчас»: загруженные котлеты тут же
            # уходят в баки бурильщиков, экран показывает честный статус.
            now = utcnow()
            user, miners = await apply_lazy_farm(conn, user_id, now)

    await callback.answer(toast, show_alert=bool(toast and "⏳" in toast))
    if extra_message:
        await callback.message.answer(extra_message)

    try:
        await callback.message.edit_text(render_farm_text(user, miners, now),
                                         reply_markup=get_farm_keyboard(), parse_mode="HTML")
    except Exception:
        pass  # текст не изменился — Telegram кидает ошибку, это не сбой


# ============================================================================
# 🎯 3. БЕСШОВНОЕ ОТКРЫТИЕ ДАШБОРДА ФЕРМЫ ИЗ ПРОФИЛЯ
# ============================================================================
@router.callback_query(F.data == "open_farm_from_profile")
async def open_farm_from_profile_callback(callback: types.CallbackQuery):
    """Перехватывает клик по кнопке фермы под паспортом, вычищая контекст бота"""
    await callback.answer()

    real_user_id = callback.from_user.id

    try:
        await callback.message.delete()
    except Exception:
        pass

    await cmd_farm(callback.message, override_user_id=real_user_id)
