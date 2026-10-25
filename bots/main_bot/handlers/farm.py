import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

from shared.analytics import notify_referrer_qualified, qualify_referral_if_due, track
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
from bots.main_bot.webapp_links import app_button
from shared.economy import ARMOR_BONUS_PER_LEVEL, STATION_BONUS_PER_LEVEL, armor_level_active, farm_bonus_percent

router = Router()
logger = logging.getLogger(__name__)

# Арты роботов владельца (22.10): флагман фермы показывается фото в /farm
ROBOT_ART_DIR = Path(__file__).resolve().parents[3] / "static" / "webapp" / "img" / "robots"
CAPTION_LIMIT = 1024          # лимит подписи к фото в Telegram
_art_file_ids: dict[str, str] = {}   # kind → file_id после первой отправки (не грузить файл каждый раз)


def flagship_kind(counts: dict) -> str | None:
    """Самый крутой робот на ферме: Бурильщик > Майнер > Стажёр."""
    for kind in ("premium", "junior", "intern"):
        if counts.get(kind, 0) > 0:
            return kind
    return None


def _robot_art(kind: str):
    cached = _art_file_ids.get(kind)
    if cached:
        return cached
    path = ROBOT_ART_DIR / f"{kind}.jpg"
    return FSInputFile(path) if path.exists() else None


async def station_level_for(conn, user) -> int:
    """Уровень станции команды игрока (бонус к добыче всем участникам)."""
    if user["team_id"] is None:
        return 0
    return await conn.fetchval("SELECT level FROM team_stations WHERE team_id = $1", user["team_id"]) or 0


async def send_farm(target: types.Message, user, miners: list[MinerState], now: datetime,
                    lang: str, station_level: int = 0) -> None:
    """Дашборд фермы: с фото флагманского робота, если арт есть и подпись влезает."""
    text = render_farm_text(user, miners, now, lang, station_level)
    kb = get_farm_keyboard(lang, user["intern_claimed"], user["interns_pending"])
    kind = flagship_kind(farm_counts(miners, now))
    art = _robot_art(kind) if kind else None
    if art is not None:
        # Telegram считает лимит подписи без HTML-тегов; держим запас
        fits = len(re.sub(r"<[^>]+>", "", text)) <= CAPTION_LIMIT - 24
        name_key = {"junior": "dlv.miner_junior", "premium": "dlv.miner_premium"}.get(kind)
        short = f"🤖 <b>{t(lang, name_key)}</b>" if name_key else None
        try:
            sent = await target.answer_photo(photo=art, caption=text if fits else short,
                                             reply_markup=kb if fits else None, parse_mode="HTML")
            if sent.photo:
                _art_file_ids[kind] = sent.photo[-1].file_id
            if fits:
                return
        except Exception:
            logger.warning("[FARM] фото робота %s не отправилось — шлю текст", kind, exc_info=True)
    await target.answer(text, reply_markup=kb, parse_mode="HTML")


async def edit_farm(message: types.Message, text: str, kb: types.InlineKeyboardMarkup) -> None:
    """Обновляет дашборд: подпись у фото или текст у обычного сообщения."""
    try:
        if message.photo:
            if len(text) <= CAPTION_LIMIT:
                await message.edit_caption(caption=text, reply_markup=kb, parse_mode="HTML")
            else:
                await message.answer(text, reply_markup=kb, parse_mode="HTML")
        else:
            await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass  # текст не изменился — Telegram кидает ошибку, это не сбой


async def activate_intern(conn, user_id: int, now: datetime) -> None:
    """Выдаёт стартового Робота Стажёра (вечный, 1 монета/ч). Вызывать в транзакции с FOR UPDATE."""
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES ($1, 'intern', $2, $3)",
        user_id, now, permanent_expiry(now))
    await conn.execute("UPDATE users SET intern_claimed = TRUE WHERE user_id = $1", user_id)


async def claim_pending_intern(conn, user_id: int, now: datetime) -> bool:
    """Забирает одного Стажёра, заработанного уровнем интеллекта. Вызывать в транзакции."""
    left = await conn.fetchval(
        "UPDATE users SET interns_pending = interns_pending - 1 WHERE user_id = $1 AND interns_pending > 0 "
        "RETURNING interns_pending", user_id)
    if left is None:
        return False
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES ($1, 'intern', $2, $3)",
        user_id, now, permanent_expiry(now))
    return True


def get_farm_keyboard(lang: str = "ru", intern_claimed: bool = True, pending: int = 0) -> types.InlineKeyboardMarkup:
    """Кнопки фермы: Стажёры (стартовый и за уровни), бонус, заправка и ферма с биржей в приложении."""
    rows = []
    if not intern_claimed:
        rows.append([types.InlineKeyboardButton(text=t(lang, "farm.btn_activate_intern"),
                                                callback_data="farm_action:activate_intern")])
    if pending > 0:
        rows.append([types.InlineKeyboardButton(text=t(lang, "farm.btn_claim_intern", n=pending),
                                                callback_data="farm_action:claim_intern")])
    return types.InlineKeyboardMarkup(inline_keyboard=rows + [
        [
            types.InlineKeyboardButton(text=t(lang, "farm.btn_bonus"),
                                       callback_data="farm_action:daily_bonus")
        ],
        [
            types.InlineKeyboardButton(text=t(lang, "farm.btn_load1"), callback_data="farm_action:load_1"),
            types.InlineKeyboardButton(text=t(lang, "farm.btn_loadall"), callback_data="farm_action:load_all")
        ],
    ] + _app_rows(lang))


def _app_rows(lang: str) -> list[list[types.InlineKeyboardButton]]:
    """Решение владельца 28.10: в чате — одна кнопка «Ферма и биржа в приложении»; без приложения — чатовая биржа."""
    farm_btn = app_button(t(lang, "farm.btn_app"), "farm")
    if farm_btn is None:
        return [[types.InlineKeyboardButton(text=t(lang, "farm.btn_market"), callback_data="open_market")]]
    return [[farm_btn]]


def render_farm_text(user, miners: list[MinerState], now: datetime, lang: str = "ru",
                     station_level: int = 0) -> str:
    """Единый текст дашборда фермы: роботы из таблицы miners, ставки с бустами."""
    counts = farm_counts(miners, now)
    junior_count = counts["junior"]
    premium_count = counts["premium"]
    fueled_count = counts["premium_fueled"]

    nuclear = is_active(user["boost_nuclear_until"], now)
    nitrogen = is_active(user["boost_nitrogen_until"], now)
    armor = armor_level_active(user["farm_armor_level"], user["armor_until"], now)
    bonus = farm_bonus_percent(armor, station_level)
    junior_rate = miner_hourly_rate("junior", nuclear_active=nuclear, nitrogen_active=nitrogen,
                                    bonus_percent=bonus)
    premium_rate = miner_hourly_rate("premium", nuclear_active=nuclear, nitrogen_active=nitrogen,
                                     bonus_percent=bonus)

    # В «актуальной скорости» бурильщики считаются только заправленные
    speed_per_hour = junior_count * junior_rate + fueled_count * premium_rate

    boosts = []
    if nuclear:
        boosts.append(t(lang, "farm.boost_nuclear", until=f"{user['boost_nuclear_until']:%d.%m %H:%M}"))
    if nitrogen:
        boosts.append(t(lang, "farm.boost_nitrogen", until=f"{user['boost_nitrogen_until']:%d.%m %H:%M}"))
    if is_active(user["drone_until"], now):
        boosts.append(t(lang, "farm.boost_drone", until=f"{user['drone_until']:%d.%m.%Y}"))
    if armor:
        boosts.append(t(lang, "farm.boost_armor", level=armor, percent=armor * ARMOR_BONUS_PER_LEVEL,
                        until=f"{user['armor_until']:%d.%m %H:%M}"))
    if station_level:
        boosts.append(t(lang, "farm.boost_station", level=station_level,
                        percent=station_level * STATION_BONUS_PER_LEVEL))
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
    intern_rate = miner_hourly_rate("intern", nuclear_active=nuclear, nitrogen_active=nitrogen,
                                    bonus_percent=bonus)
    # Стажёр — первым в списке (от слабого к мощному), даже если пока ноль
    intern_line = t(lang, "farm.intern_line", count=counts["intern"], rate=intern_rate)
    if counts["intern"] == 0 and not user["intern_claimed"]:
        burnout_line = t(lang, "farm.intern_hint") + "\n" + burnout_line
    if user["interns_pending"]:
        burnout_line = t(lang, "farm.intern_pending", n=user["interns_pending"]) + "\n" + burnout_line
    speed_per_hour += counts["intern"] * intern_rate

    return t(
        lang, "farm.dashboard",
        total=junior_count + premium_count + counts["intern"],
        junior=junior_count, premium=premium_count,
        junior_rate=junior_rate, premium_rate=premium_rate,
        intern=intern_line, burnout=burnout_line,
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
            station_level = await station_level_for(conn, user) if user else 0

    if not user:
        await message.answer(t(user_lang, "common.no_profile"))
        return

    await send_farm(message, user, miners, now, user_lang, station_level)


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
    qualified_referrer = None

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

            elif action == "claim_intern":
                if await claim_pending_intern(conn, user_id, now):
                    toast = t(user_lang, "farm.intern_claimed_new")
                    intern_activated = True
                else:
                    toast = t(user_lang, "farm.intern_none")

            elif action == "daily_bonus":
                seconds_left = daily_bonus_seconds_left(user["last_bonus_claim_at"], now)
                if seconds_left > 0:
                    hours, rem = divmod(seconds_left, 3600)
                    toast = t(user_lang, "farm.bonus_wait", hours=hours, minutes=rem // 60)
                else:
                    await conn.execute(
                        "UPDATE users SET inv_cutlets = inv_cutlets + 1, last_bonus_claim_at = $2, "
                        "bonus_claims = bonus_claims + 1 WHERE user_id = $1",
                        user_id, now)
                    toast = t(user_lang, "farm.bonus_ok")
                    bonus_given = True
                    # 3-я ежедневная котлета могла сделать игрока «активным другом»
                    qualified_referrer = await qualify_referral_if_due(conn, user_id)

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
            station_level = await station_level_for(conn, user)

    if intern_activated:
        await track(user_id, "intern_activated")
    if bonus_given:
        await track(user_id, "bonus_claimed", source="bot")
        await notify_referrer_qualified(callback.bot, qualified_referrer)
    elif action in ("load_1", "load_all") and not extra_message:
        await track(user_id, "farm_refuel", mode=action)

    await callback.answer(toast, show_alert=bool(toast and ("⏳" in toast or intern_activated)))
    if extra_message:
        await callback.message.answer(extra_message)

    await edit_farm(callback.message, render_farm_text(user, miners, now, user_lang, station_level),
                    get_farm_keyboard(user_lang, user["intern_claimed"], user["interns_pending"]))


# ============================================================================
# 🎯 3. БЕСШОВНОЕ ОТКРЫТИЕ ДАШБОРДА ФЕРМЫ ИЗ ПРОФИЛЯ
# ============================================================================
@router.callback_query(F.data == "open_farm")
async def open_farm_callback(callback: types.CallbackQuery, user_lang: str = "ru"):
    """Переход на ферму из мастерской/целей: исходный экран не удаляем."""
    await callback.answer()
    await cmd_farm(callback.message, override_user_id=callback.from_user.id, user_lang=user_lang)


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
