"""
Доставка купленных товаров в базу. Без Telegram: только asyncpg-соединение.

Контракт:
- deliver_order() вызывается внутри транзакции, строка users уже заблокирована FOR UPDATE;
- у КАЖДОГО типа товара из каталога есть обработчик в DELIVERY_HANDLERS (проверяется тестом);
- повторная доставка по тому же charge_id невозможна: сначала проверяем star_payments.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Awaitable, Callable

from shared.economy import extend_expiry, extend_expiry_hours, utcnow
from shared.ledger import change_balance

logger = logging.getLogger(__name__)


class DeliveryError(Exception):
    """Товар нельзя выдать (например, Мега-клан без команды)."""


Handler = Callable[[object, int, dict, datetime], Awaitable[str]]


async def _deliver_cutlets(conn, user_id: int, order: dict, now: datetime) -> str:
    await conn.execute("UPDATE users SET inv_cutlets = inv_cutlets + $1 WHERE user_id = $2",
                       order["qty"], user_id)
    return f"🥩 На склад добавлено: <b>{order['qty']} котлет</b>."


async def _deliver_miner(conn, user_id: int, order: dict, now: datetime) -> str:
    column = "miner_junior_count" if order["kind"] == "junior" else "miner_premium_count"
    await conn.execute(f"UPDATE users SET {column} = {column} + 1 WHERE user_id = $1", user_id)
    name = "Младший Майнер" if order["kind"] == "junior" else "Кибер-Бурильщик"
    return f"🤖 Робот <b>«{name}»</b> доставлен на твою ферму."


async def _deliver_fridge(conn, user_id: int, order: dict, now: datetime) -> str:
    current = await conn.fetchval("SELECT fridge_capacity FROM users WHERE user_id = $1", user_id)
    if current is not None and order["capacity"] <= current:
        raise DeliveryError("У тебя уже холодильник такого или большего объёма.")
    await conn.execute("UPDATE users SET fridge_capacity = $1 WHERE user_id = $2",
                       order["capacity"], user_id)
    return f"📦 Холодильник расширен до <b>{order['capacity']} котлет</b>."


async def _deliver_coins(conn, user_id: int, order: dict, now: datetime) -> str:
    await change_balance(conn, user_id, order["coins_amount"], "shop_coins", order["sku"])
    return f"💰 Зачислено <b>+{order['coins_amount']:,} рофлов</b>.".replace(",", " ")


async def _extend_column(conn, user_id: int, column: str, *, days: int | None = None,
                         hours: int | None = None, now: datetime) -> datetime:
    current = await conn.fetchval(f"SELECT {column} FROM users WHERE user_id = $1", user_id)
    if days is not None:
        new_until = extend_expiry(current, now, days)
    else:
        new_until = extend_expiry_hours(current, now, hours)
    await conn.execute(f"UPDATE users SET {column} = $1 WHERE user_id = $2", new_until, user_id)
    return new_until


async def _deliver_farm_boost(conn, user_id: int, order: dict, now: datetime) -> str:
    column = {"nuclear": "boost_nuclear_until", "nitrogen": "boost_nitrogen_until"}[order["kind"]]
    until = await _extend_column(conn, user_id, column, days=order["days"], now=now)
    label = "🔋 Ядерный Разгон x5" if order["kind"] == "nuclear" else "❄️ Азотное Охлаждение +40%"
    return f"{label} активен до <b>{until:%d.%m.%Y %H:%M} UTC</b>."


async def _deliver_vip_character(conn, user_id: int, order: dict, now: datetime) -> str:
    until = await _extend_column(conn, user_id, "drone_until", days=order["days"], now=now)
    return f"🛸 Мастер-дрон охраняет ферму до <b>{until:%d.%m.%Y} UTC</b>."


async def _deliver_game_unlimit(conn, user_id: int, order: dict, now: datetime) -> str:
    until = await _extend_column(conn, user_id, "unlimit_until", hours=order["hours"], now=now)
    return f"⚡ Лимиты побед сняты до <b>{until:%d.%m.%Y %H:%M} UTC</b>."


async def _deliver_clan_upgrade(conn, user_id: int, order: dict, now: datetime) -> str:
    team = await conn.fetchrow("SELECT team_id, max_members FROM teams WHERE captain_id = $1 FOR UPDATE", user_id)
    if not team:
        raise DeliveryError("У тебя нет созданной команды. Сначала создай её через /create_team.")
    if team["max_members"] >= order["max_members"]:
        raise DeliveryError("Твоя команда уже имеет статус Мега-Клана.")
    await conn.execute("UPDATE teams SET max_members = $1 WHERE team_id = $2",
                       order["max_members"], team["team_id"])
    return f"🏆 Команда получила статус <b>МЕГА-КЛАН</b>: до {order['max_members']} мест."


DELIVERY_HANDLERS: dict[str, Handler] = {
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


async def deliver_order(conn, user_id: int, order: dict, charge_id: str, now: datetime | None = None) -> str:
    """
    Выдаёт товар и фиксирует платёж. Вызывать внутри транзакции с заблокированной строкой users.
    Возвращает текст для игрока. Бросает DeliveryError / KeyError(неизвестный тип).
    """
    now = now or utcnow()
    handler = DELIVERY_HANDLERS.get(order["type"])
    if handler is None:
        raise DeliveryError(f"Нет обработчика доставки для типа {order['type']}")

    message = await handler(conn, user_id, order, now)

    await conn.execute(
        """
        INSERT INTO star_payments (user_id, telegram_charge_id, item_payload, stars_amount)
        VALUES ($1, $2, $3, $4)
        """,
        user_id, charge_id, order["sku"], order["stars"],
    )
    logger.info("[DELIVERY] user=%s sku=%s stars=%s charge=%s", user_id, order["sku"], order["stars"], charge_id)
    return message
