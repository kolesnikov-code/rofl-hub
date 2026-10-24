"""
Сбор продуктовой аналитики ROFL HUB.

ЖЕЛЕЗНОЕ ПРАВИЛО: аналитика никогда не ломает игру. track() и mark_daily_activity()
глотают ЛЮБЫЕ исключения (в лог) и вызываются ПОСЛЕ игровых транзакций — сбой записи
события не может откатить начисление монет.

Исключение из правила — qualify_referral_if_due(): это ИГРОВАЯ механика (бонус рефереру
за «активного» друга: 3 уровень интеллекта + 3 ежедневные котлеты), она живёт ВНУТРИ
транзакции повышения уровня / получения котлеты и обязана быть атомарной.
«Ровно один раз» гарантирует UPDATE ... WHERE qualified_at IS NULL RETURNING:
из двух конкурентных транзакций строку получает только одна.
"""
from __future__ import annotations

import json
import logging
import re
from datetime import date, datetime

from shared.database import db
from shared.economy import (
    EVENTS_RETENTION_DAYS,
    PROMOTER_CODE_MAX_LEN,
    REFERRAL_QUALIFIED_BONUS,
    REFERRAL_QUALIFIED_CUTLETS,
    REFERRAL_QUALIFIED_RESOURCES,
    REFERRAL_QUALIFY_BONUS_CLAIMS,
    RESOURCE_KINDS,
    REFERRAL_QUALIFY_QUIZ_LEVEL,
    utcnow,
)
from shared.ledger import change_balance

logger = logging.getLogger(__name__)

# Источники трафика (users.source): считаются ОДИН раз, при регистрации
SOURCE_ORGANIC = "organic"
SOURCE_REFERRAL = "referral"
SOURCE_TG_AFFILIATE = "tg_affiliate"   # официальная партнёрка Telegram (?start=_tgr_...)

_CODE_RE = re.compile(r"^[a-z0-9_-]{1,%d}$" % PROMOTER_CODE_MAX_LEN)


def parse_source(start_arg: str | None, referrer_id: int | None) -> str:
    """
    Источник первого касания из аргумента /start:
    <digits> → referral, p_<code> → p_<code> (промоутер), c_<code> → c_<code> (канал),
    _tgr_* → tg_affiliate, иначе organic. Код валидируется ([a-z0-9_-], до 16 зн.).
    """
    if referrer_id is not None:
        return SOURCE_REFERRAL
    if not start_arg:
        return SOURCE_ORGANIC
    arg = start_arg.strip()
    if arg.startswith("_tgr_"):
        return SOURCE_TG_AFFILIATE
    for prefix in ("p_", "c_"):
        if arg.startswith(prefix) and _CODE_RE.fullmatch(arg[len(prefix):].lower()):
            return prefix + arg[len(prefix):].lower()
    return SOURCE_ORGANIC


async def track(user_id: int, event: str, **props) -> None:
    """Пишет событие поведения. Никогда не бросает исключений."""
    try:
        payload = json.dumps(props, ensure_ascii=False, default=str) if props else "{}"
        await db.pool.execute(
            "INSERT INTO events (user_id, event, props) VALUES ($1, $2, $3::jsonb)",
            user_id, event[:64], payload)
    except Exception:
        logger.warning("[ANALYTICS] событие %s user=%s не записано", event, user_id, exc_info=True)


# Кэш «этот игрок сегодня уже отмечен»: {user_id: date}. После рестарта пуст —
# по одному лишнему INSERT ... ON CONFLICT DO NOTHING на игрока, это дёшево.
_daily_marked: dict[int, date] = {}


async def mark_daily_activity(user_id: int, today: date | None = None) -> None:
    """Отмечает день активности (основа DAU/WAU/MAU/retention). Никогда не бросает."""
    try:
        day = today or utcnow().date()
        if _daily_marked.get(user_id) == day:
            return
        await db.pool.execute(
            "INSERT INTO daily_activity (user_id, day) VALUES ($1, $2) ON CONFLICT DO NOTHING",
            user_id, day)
        _daily_marked[user_id] = day
        if len(_daily_marked) > 50_000:   # предохранитель от бесконечного роста памяти
            _daily_marked.clear()
    except Exception:
        logger.warning("[ANALYTICS] daily_activity user=%s не записана", user_id, exc_info=True)


def referral_reward_text() -> str:
    """«+500 🪙 · 1 🥩 · 10 ⛏ · 10 💧 · 10 💎 · 10 ⚙️» — награда за активного друга."""
    from shared.resources import RESOURCE_ICONS
    parts = [f"+{REFERRAL_QUALIFIED_BONUS} 🪙"]
    if REFERRAL_QUALIFIED_CUTLETS:
        parts.append(f"{REFERRAL_QUALIFIED_CUTLETS} 🥩")
    if REFERRAL_QUALIFIED_RESOURCES:
        parts += [f"{REFERRAL_QUALIFIED_RESOURCES} {RESOURCE_ICONS[k]}" for k in RESOURCE_KINDS]
    return " · ".join(parts)


async def qualify_referral_if_due(conn, user_id: int) -> int | None:
    """
    Вызывается ВНУТРИ транзакции, после которой у приглашённого могло выполниться условие
    «активного друга»: повышение уровня интеллекта и получение ежедневной котлеты.

    Анти-фейк (решение владельца 26.10): за регистрацию друга не платится ничего; рефереру —
    ровно один раз награда (монеты + котлета + по 10 каждого ресурса, referral_reward_text()),
    когда друг дошёл до REFERRAL_QUALIFY_QUIZ_LEVEL
    уровня интеллекта (60 верных ответов) И забрал REFERRAL_QUALIFY_BONUS_CLAIMS ежедневных
    котлет (кулдаун 24 ч → минимум двое суток живой игры). Заблокированный друг не
    квалифицируется; заблокированному рефереру бонус не начисляется (квалификация фиксируется).
    Атомарный UPDATE ... WHERE qualified_at IS NULL — из двух конкурентных транзакций
    бонус получает только одна. Возвращает referrer_id, если бонус начислен прямо сейчас.
    """
    row = await conn.fetchrow(
        """
        UPDATE users u SET qualified_at = NOW()
        FROM game_stats g
        WHERE u.user_id = $1 AND g.user_id = u.user_id
          AND u.referred_by IS NOT NULL AND u.referred_by <> u.user_id
          AND u.qualified_at IS NULL AND NOT u.is_blocked
          AND u.bonus_claims >= $2 AND g.quiz_level >= $3
        RETURNING u.referred_by
        """,
        user_id, REFERRAL_QUALIFY_BONUS_CLAIMS, REFERRAL_QUALIFY_QUIZ_LEVEL)
    if row is None:
        return None
    referrer_id = row["referred_by"]
    try:
        blocked = await conn.fetchval("SELECT is_blocked FROM users WHERE user_id = $1", referrer_id)
        if blocked is None or blocked:
            logger.info("[REFERRAL_QUALIFIED] реферер %s недоступен — бонус не начислен", referrer_id)
            return None
        await change_balance(conn, referrer_id, REFERRAL_QUALIFIED_BONUS,
                             "referral_qualified", str(user_id))
        if REFERRAL_QUALIFIED_CUTLETS:
            await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $2 WHERE user_id = $1",
                               referrer_id, REFERRAL_QUALIFIED_CUTLETS)
        if REFERRAL_QUALIFIED_RESOURCES:
            from shared.resources import grant_bundle, resource_capacity
            await grant_bundle(conn, referrer_id, {k: REFERRAL_QUALIFIED_RESOURCES for k in RESOURCE_KINDS},
                               "referral_qualified", str(user_id),
                               cap=await resource_capacity(conn, referrer_id))
    except Exception:
        # Реферер удалён/сломан — квалификацию фиксируем, бонус сгорает осознанно
        logger.exception("[REFERRAL_QUALIFIED] бонус рефереру %s не начислен", referrer_id)
        return None
    return referrer_id


async def notify_referrer_qualified(bot, referrer_id: int | None) -> None:
    """ЛС рефереру о бонусе за активного друга на его языке. Любой сбой — только в лог."""
    if referrer_id is None or bot is None:
        return
    from shared.locales import resolve_lang, t
    try:
        lang = resolve_lang(await db.pool.fetchval("SELECT lang FROM users WHERE user_id = $1", referrer_id))
        await bot.send_message(
            referrer_id, t(lang, "ref.qualified_notify", bonus=referral_reward_text(),
                           level=REFERRAL_QUALIFY_QUIZ_LEVEL, claims=REFERRAL_QUALIFY_BONUS_CLAIMS),
            parse_mode="HTML")
    except Exception:
        logger.info("[REFERRAL_QUALIFIED] реферер %s недоступен для ЛС", referrer_id)


async def purge_old_events(retention_days: int = EVENTS_RETENTION_DAYS,
                           batch: int = 50_000) -> int:
    """Чистит события старше retention_days батчами. Возвращает число удалённых строк."""
    total = 0
    try:
        while True:
            status = await db.pool.execute(
                """
                DELETE FROM events WHERE id IN (
                    SELECT id FROM events
                    WHERE created_at < NOW() - make_interval(days => $1)
                    LIMIT $2
                )
                """,
                retention_days, batch)
            deleted = int(status.split()[-1])   # asyncpg возвращает строку вида 'DELETE 123'
            total += deleted
            if deleted < batch:
                break
    except Exception:
        logger.exception("[ANALYTICS] очистка старых событий прервана (удалено %s)", total)
    return total
