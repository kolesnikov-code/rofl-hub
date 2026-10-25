"""
Ресурсы экосистемы (волна 22.10, вечер): ⛏ Металл, 💧 Водород, 💎 Кристаллы, ⚙️ Детали.

Философия: в каждой игре добывается СВОЙ ресурс (КНБ → металл, Больше/Меньше → водород,
Викторина → кристаллы, Сейф → детали; дуэли — металл, квесты — набор). Ресурсы не продаются
и не покупаются за Stars — только добыча и применение: мастерская, налёты, станция команды.

Дисциплина как у монет: любое изменение запаса — ТОЛЬКО через change_resource()
внутри транзакции вызывающего кода; каждая операция — строка в resource_ledger;
запас не уходит в минус (проверка в UPDATE + CHECK в БД).
"""
from __future__ import annotations

import logging

from shared.economy import (ALL_KINDS, GAME_RESOURCE, RES_CAPACITY_BASE, RESOURCE_KINDS, RESOURCE_MAX_STOCK,
                            RESOURCE_PER_WIN)
from shared.locales import t

logger = logging.getLogger(__name__)

RESOURCE_ICONS = {"metal": "⛏", "hydrogen": "💧", "crystal": "💎", "parts": "⚙️",
                  "stone": "🪨", "wood": "🪵", "fire": "🔥", "energy": "⚡", "battery": "🔋", "cow": "🐄", "core": "☢️"}


class InsufficientResources(Exception):
    def __init__(self, kind: str, need: int, have: int):
        self.kind, self.need, self.have = kind, need, have
        super().__init__(f"{kind}: need {need}, have {have}")


def resource_name(lang: str, kind: str) -> str:
    """Локализованное имя ресурса с иконкой."""
    return f"{RESOURCE_ICONS[kind]} {t(lang, f'res.{kind}')}"


def format_bundle(lang: str, bundle: dict[str, int], sep: str = " · ") -> str:
    """«⛏ 20 Металл · 💧 20 Водород» — для цен и добычи."""
    parts = [f"{RESOURCE_ICONS[k]} {bundle[k]} {t(lang, f'res.{k}')}"
             for k in ALL_KINDS if bundle.get(k)]
    return sep.join(parts) if parts else "—"


def game_resource_gain(game_type: str) -> tuple[str, int] | None:
    """Какой ресурс и сколько даёт победа в соло-игре."""
    kind = GAME_RESOURCE.get(game_type)
    if kind is None:
        return None
    return kind, RESOURCE_PER_WIN.get(game_type, 1)


async def get_resources(conn, user_id: int, kinds: tuple = RESOURCE_KINDS) -> dict[str, int]:
    """Запасы видов kinds (по умолчанию 4 базовых; нулевые тоже), без блокировки."""
    rows = await conn.fetch("SELECT kind, qty FROM user_resources WHERE user_id = $1", user_id)
    stock = {k: 0 for k in kinds}
    for r in rows:
        if r["kind"] in stock:
            stock[r["kind"]] = r["qty"]
    return stock


async def lock_resources(conn, user_id: int) -> dict[str, int]:
    """То же, но строки заблокированы FOR UPDATE (внутри транзакции)."""
    rows = await conn.fetch(
        "SELECT kind, qty FROM user_resources WHERE user_id = $1 ORDER BY kind FOR UPDATE", user_id)
    stock = {k: 0 for k in ALL_KINDS}
    for r in rows:
        if r["kind"] in stock:
            stock[r["kind"]] = r["qty"]
    return stock


async def resource_capacity(conn, user_id: int) -> int:
    """Вместимость склада игрока на КАЖДЫЙ ресурс."""
    cap = await conn.fetchval("SELECT res_capacity FROM users WHERE user_id = $1", user_id)
    return int(cap or RES_CAPACITY_BASE)


async def change_resource(conn, user_id: int, kind: str, delta: int, reason: str,
                          ref: str | None = None, cap: int | None = None) -> int:
    """
    Атомарно меняет запас ресурса kind на delta, пишет resource_ledger.
    Возвращает новый запас. Бросает InsufficientResources при уходе в минус.
    cap — вместимость склада для ДОБЫЧИ (игры, сундук, квесты, трофеи): излишек пропадает,
    уже лежащее сверх лимита не отнимается. Переводы между игроками (биржа, обмен, возвраты
    эскроу) вызывают без cap — место проверяется до сделки. Технический потолок —
    RESOURCE_MAX_STOCK.
    """
    if kind not in ALL_KINDS:
        raise ValueError(f"unknown resource {kind}")
    if delta == 0:
        return (await get_resources(conn, user_id, ALL_KINDS))[kind]

    if delta > 0:
        limit = min(cap, RESOURCE_MAX_STOCK) if cap is not None else RESOURCE_MAX_STOCK
        old = await conn.fetchval(
            "SELECT qty FROM user_resources WHERE user_id = $1 AND kind = $2 FOR UPDATE", user_id, kind) or 0
        gained = max(0, min(old + delta, max(limit, old)) - old)
        if gained == 0:
            return old     # склад полон — добыча пропала, в журнал нечего писать
        delta = gained
        new_qty = await conn.fetchval(
            """
            INSERT INTO user_resources (user_id, kind, qty) VALUES ($1, $2, $3::int)
            ON CONFLICT (user_id, kind) DO UPDATE SET qty = user_resources.qty + $3::int
            RETURNING qty
            """, user_id, kind, delta)
    else:
        new_qty = await conn.fetchval(
            """
            UPDATE user_resources SET qty = qty + $3::int
            WHERE user_id = $1 AND kind = $2 AND qty + $3::int >= 0
            RETURNING qty
            """, user_id, kind, delta)
        if new_qty is None:
            have = (await get_resources(conn, user_id, ALL_KINDS))[kind]
            raise InsufficientResources(kind, -delta, have)

    await conn.execute(
        "INSERT INTO resource_ledger (user_id, kind, delta, reason, ref) VALUES ($1, $2, $3, $4, $5)",
        user_id, kind, delta, reason[:64], ref)
    return new_qty


async def spend_bundle(conn, user_id: int, bundle: dict[str, int], reason: str,
                       ref: str | None = None) -> dict[str, int]:
    """
    Списывает набор ресурсов целиком. Сначала проверяет ВСЕ позиции по заблокированным
    строкам, потом списывает — либо всё, либо ничего (внутри транзакции вызывающего).
    Возвращает остатки.
    """
    stock = await lock_resources(conn, user_id)
    for kind, need in bundle.items():
        if need > 0 and stock.get(kind, 0) < need:
            raise InsufficientResources(kind, need, stock.get(kind, 0))
    for kind, need in bundle.items():
        if need > 0:
            stock[kind] = await change_resource(conn, user_id, kind, -need, reason, ref)
    return stock


async def grant_bundle(conn, user_id: int, bundle: dict[str, int], reason: str,
                       ref: str | None = None, cap: int | None = None) -> None:
    for kind, qty in bundle.items():
        if qty > 0:
            await change_resource(conn, user_id, kind, qty, reason, ref, cap=cap)


async def free_space(conn, user_id: int, kind: str) -> int:
    """Сколько ресурса ещё влезет на склад (для проверок перед покупкой/обменом)."""
    cap = await resource_capacity(conn, user_id)
    have = (await get_resources(conn, user_id, ALL_KINDS))[kind]
    return max(0, cap - have)


def total_resources(stock: dict[str, int]) -> int:
    return sum(stock.get(k, 0) for k in RESOURCE_KINDS)
