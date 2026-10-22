import logging
from datetime import datetime, timedelta

from aiogram import Router, types, F
from aiogram.filters import Command

from shared.analytics import track
from shared.database import db
from shared.economy import (
    daily_bonus_seconds_left,
    is_active,
    miner_hourly_rate,
    permanent_expiry,
    utcnow,
)
from shared.farm_logic import MinerState, apply_lazy_farm, farm_counts
from shared.locales import btn_variants, t

router = Router()
logger = logging.getLogger(__name__)


async def activate_intern(conn, user_id: int, now: datetime) -> None:
    """Выдаёт стартового Робота Стажёра (вечный, 1 монета/ч). Вызывать в транзакции с FOR UPDATE."""
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES ($1, 'intern', $2, $3)",
        user_id, now, permanent_expiry(now))
    await conn.execute("UPDATE users SET intern_claimed = TRUE WHERE user_id = $1", user_id)


def get_farm_keyboard(lang: str = "ru", intern_claimed: bool = True) -> types.InlineKeyboardMarkup:
    """Кнопки фермы: активация Стажёра (пока не забран), бонус, заправка, магазин."""
    rows = []
    if not intern_claimed:
        rows.append([types.InlineKeyboardButton(text=t(lang, "farm.btn_activate_intern"),
                                                callback_data="farm_action:activate_intern")])
    return types.InlineKeyboardMarkup(inline_keyboard=rows + [
        [
            types.InlineKeyboardButton(text=t(lang, "farm.btn_bonus"),
                                       callback_data="farm_action:daily_bonus")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "farm.btn_load1"), callback_data="farm_action:load_1"),
            types.InlineKeyboardButton(text=t(lang, "farm.btn_loadall"), callback_data="farm_action:load_all")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "farm.btn_market"), callback_data="open_market")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "farm.btn_shop"), callback_data="open_shop_from_farm")
        ]
    ])


def render_farm_text(user, miners: list[MinerState], now: datetime, lang: str = "ru") -> str:
    """Единый текст дашборда фермы: роботы из таблицы miners, ставки с бустами."""
    counts = farm_counts(miners, now)
    junior_count = counts["junior"]
    premium_count = counts["premium"]
    fueled_count = counts["premium_fueled"]

    nuclear = is_active(user["boost_nuclear_until"], now)
    nitrogen = is_active(user["boost_nitrogen_until"], now)
    junior_rate = miner_hourly_rate("junior", nuclear_active=nuclear, nitrogen_active=nitrogen)
    premium_rate = miner_hourly_rate("premium", nuclear_active=nuclear, nitrogen_active=nitrogen)

    # В «актуальной скорости» бурильщики считаются только заправленные
    speed_per_hour = junior_count * junior_rate + fueled_count * premium_rate

    boosts = []
    if nuclear:
        boosts.append(t(lang, "farm.boost_nuclear", until=f"{user['boost_nuclear_until']:%d.%m %H:%M}"))
    if nitrogen:
        boosts.append(t(lang, "farm.boost_nitrogen", until=f"{user['boost_nitrogen_until']:%d.%m %H:%M}"))
    if is_active(user["drone_until"], now):
        boosts.append(t(lang, "farm.boost_drone", until=f"{user['drone_until']:%d.%m.%Y}"))
    boosts_block = "\n".join(boosts) if boosts else t(lang, "farm.no_boosts")

    if premium_count > 0:
        if fueled_count == premium_count:
            status_work = t(lang, "farm.status_all_fueled")
        elif fueled_count > 0:
            status_work = t(lang, "farm.status_partial", fueled=fueled_count, total=premium_count)
        else:
            status_work = t(lang, "farm.status_no_fuel")
    else:
        status_work = t(lang, "farm.status_no_drills")

    # Сгорание считаем только по срочным роботам: Стажёры и вечные Майнеры не горят
    mortal = [m for m in miners if m.expires_at > now and m.expires_at < now + timedelta(days=3650)]
    burnout_line = ""
    if mortal:
        nearest = min(m.expires_at for m in mortal)
        burnout_line = t(lang, "farm.burnout", until=f"{nearest:%d.%m.%Y %H:%M}")
    intern_rate = miner_hourly_rate("intern", nuclear_active=nuclear, nitrogen_active=nitrogen)
    if counts["intern"] > 0:
        burnout_line = t(lang, "farm.intern_line", count=counts["intern"], rate=intern_rate) + "\n" + burnout_line
    elif not user["intern_claimed"]:
        burnout_line = t(lang, "farm.intern_hint") + "\n" + burnout_line
    speed_per_hour += counts["intern"] * intern_rate

    return t(
        lang, "farm.dashboard",
        total=junior_count + premium_count + counts["intern"],
        junior=junior_count, premium=premium_count,
        junior_rate=junior_rate, premium_rate=premium_rate,
        burnout=burnout_line,
        speed_hour=speed_per_hour, speed_day=speed_per_hour * 24,
        boosts=boosts_block, status=status_work,
        fridge=user["fridge_cutlets"], capacity=user["fridge_capacity"], inv=user["inv_cutlets"],
    )


# ============================================================================
# 🚜 1. ЦЕНТРАЛЬНЫЙ УНИВЕРСАЛЬНЫЙ ВЫЗОВ ПАНЕЛИ ФЕРМЫ
# ============================================================================
@router.message(Command("farm"))
@router.message(Command("my_farm"))
@router.message(F.text.in_(btn_variants("farm")))
async def cmd_farm(message: types.Message, override_user_id: int = None, user_lang: str = "ru"):
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
        await message.answer(t(user_lang, "common.no_profile"))
        return

    await message.answer(render_farm_text(user, miners, now, user_lang),
                         reply_markup=get_farm_keyboard(user_lang, user["intern_claimed"]),
                         parse_mode="HTML")


# ============================================================================
# 🎰 2. ИНЛАЙН-ДЕЙСТВИЯ: БОНУС, ЗАПРАВКА, ОБНОВЛЕНИЕ ЭКРАНА
# ============================================================================
@router.callback_query(F.data.startswith("farm_action:"))
async def process_farm_inline_actions(callback: types.CallbackQuery, user_lang: str = "ru"):
    user_id = callback.from_user.id
    parts = callback.data.split(":")
    if len(parts) < 2:
        await callback.answer()
        return
    action = parts[1]
    now = utcnow()
    toast: str | None = None
    extra_message: str | None = None
    bonus_given = False
    intern_activated = False

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Сначала ленивый пересчёт (он же блокирует строку users FOR UPDATE)
            user, miners = await apply_lazy_farm(conn, user_id, now)
            if not user:
                await callback.answer(t(user_lang, "common.no_profile"), show_alert=True)
                return

            if action == "activate_intern":
                if user["intern_claimed"]:
                    toast = t(user_lang, "farm.intern_already")
                else:
                    await activate_intern(conn, user_id, now)
                    toast = t(user_lang, "farm.intern_activated")
                    intern_activated = True

            elif action == "daily_bonus":
                seconds_left = daily_bonus_seconds_left(user["last_bonus_claim_at"], now)
                if seconds_left > 0:
                    hours, rem = divmod(seconds_left, 3600)
                    toast = t(user_lang, "farm.bonus_wait", hours=hours, minutes=rem // 60)
                else:
                    await conn.execute(
                        "UPDATE users SET inv_cutlets = inv_cutlets + 1, last_bonus_claim_at = $2 "
                        "WHERE user_id = $1",
                        user_id, now)
                    toast = t(user_lang, "farm.bonus_ok")
                    bonus_given = True

            elif action == "load_1":
                if user["inv_cutlets"] <= 0:
                    extra_message = t(user_lang, "farm.no_inv_cutlets")
                elif user["fridge_cutlets"] >= user["fridge_capacity"]:
                    extra_message = t(user_lang, "farm.fridge_full")
                else:
                    await conn.execute(
                        "UPDATE users SET inv_cutlets = inv_cutlets - 1, fridge_cutlets = fridge_cutlets + 1 "
                        "WHERE user_id = $1",
                        user_id)

            elif action == "load_all":
                available_space = user["fridge_capacity"] - user["fridge_cutlets"]
                if user["inv_cutlets"] <= 0:
                    extra_message = t(user_lang, "farm.no_inv_cutlets")
                elif available_space <= 0:
                    extra_message = t(user_lang, "farm.fridge_full")
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

    if intern_activated:
        await track(user_id, "intern_activated")
    if bonus_given:
        await track(user_id, "bonus_claimed", source="bot")
    elif action in ("load_1", "load_all") and not extra_message:
        await track(user_id, "farm_refuel", mode=action)

    await callback.answer(toast, show_alert=bool(toast and ("⏳" in toast or intern_activated)))
    if extra_message:
        await callback.message.answer(extra_message)

    try:
        await callback.message.edit_text(render_farm_text(user, miners, now, user_lang),
                                         reply_markup=get_farm_keyboard(user_lang, user["intern_claimed"]),
                                         parse_mode="HTML")
    except Exception:
        pass  # текст не изменился — Telegram кидает ошибку, это не сбой


# ============================================================================
# 🎯 3. БЕСШОВНОЕ ОТКРЫТИЕ ДАШБОРДА ФЕРМЫ ИЗ ПРОФИЛЯ
# ============================================================================
@router.callback_query(F.data == "open_farm_from_profile")
async def open_farm_from_profile_callback(callback: types.CallbackQuery, user_lang: str = "ru"):
    """Перехватывает клик по кнопке фермы под паспортом, вычищая контекст бота"""
    await callback.answer()

    real_user_id = callback.from_user.id

    try:
        await callback.message.delete()
    except Exception:
        pass

    await cmd_farm(callback.message, override_user_id=real_user_id, user_lang=user_lang)
