"""
Доставка купленных товаров в базу. Без Telegram: только asyncpg-соединение.

Контракт:
- deliver_order() вызывается внутри транзакции, строка users уже заблокирована FOR UPDATE;
- у КАЖДОГО типа товара из каталога есть обработчик в DELIVERY_HANDLERS (проверяется тестом);
- повторная доставка по тому же charge_id невозможна: сначала проверяем star_payments;
- тексты для игрока — на его языке (lang передаёт платёжный контур).
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Awaitable, Callable

from shared.economy import (
    INTERN_UPGRADE_REFERRALS,
    MINER_LICENSE_DAYS,
    extend_expiry,
    extend_expiry_hours,
    permanent_expiry,
    utcnow,
)
from shared.ledger import change_balance
from shared.locales import t

logger = logging.getLogger(__name__)


class DeliveryError(Exception):
    """Товар нельзя выдать (например, Мега-клан без команды)."""


Handler = Callable[[object, int, dict, datetime, str], Awaitable[str]]


async def _deliver_cutlets(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $1 WHERE user_id = $2",
                       order["qty"], user_id)
    return t(lang, "dlv.cutlets", qty=order["qty"])


async def _deliver_miner(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    expires_at = now + timedelta(days=MINER_LICENSE_DAYS)
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES ($1, $2, $3, $4)",
        user_id, order["kind"], now, expires_at,
    )
    name = t(lang, "dlv.miner_junior" if order["kind"] == "junior" else "dlv.miner_premium")
    return t(lang, "dlv.miner", name=name, until=f"{expires_at:%d.%m.%Y %H:%M}")


async def _deliver_fridge(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    current = await conn.fetchval("SELECT fridge_capacity FROM users WHERE user_id = $1", user_id)
    if current is not None and order["capacity"] <= current:
        raise DeliveryError(t(lang, "dlv.err_fridge"))
    await conn.execute("UPDATE users SET fridge_capacity = $1 WHERE user_id = $2",
                       order["capacity"], user_id)
    return t(lang, "dlv.fridge", capacity=order["capacity"])


async def _deliver_coins(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    await change_balance(conn, user_id, order["coins_amount"], "shop_coins", order["sku"])
    return t(lang, "dlv.coins", amount=f"{order['coins_amount']:,}".replace(",", " "))


async def _extend_column(conn, user_id: int, column: str, *, days: int | None = None,
                         hours: int | None = None, now: datetime) -> datetime:
    current = await conn.fetchval(f"SELECT {column} FROM users WHERE user_id = $1", user_id)
    if days is not None:
        new_until = extend_expiry(current, now, days)
    else:
        new_until = extend_expiry_hours(current, now, hours)
    await conn.execute(f"UPDATE users SET {column} = $1 WHERE user_id = $2", new_until, user_id)
    return new_until


async def _deliver_farm_boost(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    column = {"nuclear": "boost_nuclear_until", "nitrogen": "boost_nitrogen_until"}[order["kind"]]
    until = await _extend_column(conn, user_id, column, days=order["days"], now=now)
    key = "dlv.boost_nuclear" if order["kind"] == "nuclear" else "dlv.boost_nitrogen"
    return t(lang, key, until=f"{until:%d.%m.%Y %H:%M}")


async def _deliver_vip_character(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    until = await _extend_column(conn, user_id, "drone_until", days=order["days"], now=now)
    return t(lang, "dlv.drone", until=f"{until:%d.%m.%Y}")


async def _deliver_game_unlimit(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    until = await _extend_column(conn, user_id, "unlimit_until", hours=order["hours"], now=now)
    return t(lang, "dlv.unlimit", until=f"{until:%d.%m.%Y %H:%M}")


async def _deliver_clan_upgrade(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    team = await conn.fetchrow("SELECT team_id, max_members FROM teams WHERE captain_id = $1 FOR UPDATE", user_id)
    if not team:
        raise DeliveryError(t(lang, "dlv.err_no_team"))
    if team["max_members"] >= order["max_members"]:
        raise DeliveryError(t(lang, "dlv.err_mega"))
    await conn.execute("UPDATE teams SET max_members = $1 WHERE team_id = $2",
                       order["max_members"], team["team_id"])
    return t(lang, "dlv.clan", max=order["max_members"])


async def qualified_referrals_count(conn, user_id: int) -> int:
    """Активные друзья игрока (3 уровень интеллекта + 3 ежедневные котлеты) — условие апгрейда Стажёра."""
    return int(await conn.fetchval(
        "SELECT COUNT(*) FROM users WHERE referred_by = $1 AND qualified_at IS NOT NULL", user_id) or 0)


async def _deliver_intern_upgrade(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    """Робот-Стажёр → ВЕЧНЫЙ Младший Майнер (5 монет/ч, без срока). Условие: 3 квалифицированных друга."""
    have = await qualified_referrals_count(conn, user_id)
    if have < INTERN_UPGRADE_REFERRALS:
        raise DeliveryError(t(lang, "dlv.err_intern_refs", need=INTERN_UPGRADE_REFERRALS, have=have))
    intern_id = await conn.fetchval(
        "SELECT miner_id FROM miners WHERE user_id = $1 AND kind = 'intern' "
        "ORDER BY miner_id LIMIT 1 FOR UPDATE", user_id)
    if intern_id is None:
        raise DeliveryError(t(lang, "dlv.err_no_intern"))
    await conn.execute(
        "UPDATE miners SET kind = 'junior', expires_at = $2, purchased_at = $3 WHERE miner_id = $1",
        intern_id, permanent_expiry(now), now)
    return t(lang, "dlv.intern_upgrade")


async def _deliver_skin(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    """✨ Скин за ★: экземпляр с номером тиража. Тираж кончился после оплаты — DeliveryError → авто-возврат Stars."""
    from shared.skins import SKINS, SkinError, grant
    try:
        got = await grant(conn, user_id, order["skin"], "stars", now)
    except SkinError as e:
        raise DeliveryError(t(lang, e.key)) from e
    edition = SKINS[order["skin"]].get("edition")
    title = order["title"] if lang == "ru" else order.get("title_en", order["title"])
    return t(lang, "skin.delivered", name=title, serial=got["serial"], edition=edition or "∞")


async def _deliver_season_pass(conn, user_id: int, order: dict, now: datetime, lang: str) -> str:
    """🎟 Платная дорожка пропуска сезона: сразу открываются все уже пройденные уровни."""
    from shared.season_pass import PassError, activate_premium
    try:
        await activate_premium(conn, user_id, order["season"])
    except PassError as e:
        raise DeliveryError(t(lang, e.key)) from e
    return t(lang, "pass.delivered", season=f"{order['season'][5:7]}.{order['season'][:4]}")


DELIVERY_HANDLERS: dict[str, Handler] = {
    "skin": _deliver_skin,
    "season_pass": _deliver_season_pass,
    "intern_upgrade": _deliver_intern_upgrade,
    "cutlets": _deliver_cutlets,
    "miner": _deliver_miner,
    "fridge_upgrade": _deliver_fridge,
    "coins": _deliver_coins,
    "farm_boost": _deliver_farm_boost,
    "vip_character": _deliver_vip_character,
    "game_unlimit": _deliver_game_unlimit,
    "clan_upgrade": _deliver_clan_upgrade,
}


async def already_delivered(conn, charge_id: str) -> bool:
    return bool(await conn.fetchval("SELECT 1 FROM star_payments WHERE telegram_charge_id = $1", charge_id))


async def deliver_order(conn, user_id: int, order: dict, charge_id: str,
                        now: datetime | None = None, lang: str = "ru") -> str:
    """
    Выдаёт товар и фиксирует платёж. Вызывать внутри транзакции с заблокированной строкой users.
    Возвращает текст для игрока (на его языке). Бросает DeliveryError / KeyError(неизвестный тип).
    """
    now = now or utcnow()
    handler = DELIVERY_HANDLERS.get(order["type"])
    if handler is None:
        raise DeliveryError(f"Нет обработчика доставки для типа {order['type']}")

    message = await handler(conn, user_id, order, now, lang)

    await conn.execute(
        """
        INSERT INTO star_payments (user_id, telegram_charge_id, item_payload, stars_amount)
        VALUES ($1, $2, $3, $4)
        """,
        user_id, charge_id, order["sku"], order["stars"],
    )
    logger.info("[DELIVERY] user=%s sku=%s stars=%s charge=%s", user_id, order["sku"], order["stars"], charge_id)
    return message
