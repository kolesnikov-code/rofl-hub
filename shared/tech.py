"""
🔬 Лаборатория (решение владельца 27.10): инструменты, технологии, лошади, заряд Шаттла.

- ИНСТРУМЕНТЫ — уровни 1..4 (⚒️ грубые → 🛠 тонкой настройки → 🔬 калибровка → 🧬 нанотехнологии),
  как в S.T.A.L.K.E.R.: набор не тратится, а открывает сложные сборки. Хранится в user_tech('tools').
- ТЕХНОЛОГИИ — 📡 связь, 🔭 разведка, ⚔️ нападение, 🛡 оборона, 📚 наука (shared/economy.TECHS).
  Уровень покупается за ресурсы при нужном наборе инструментов; следующий — не раньше, чем через
  TECH_COOLDOWN_DAYS (30 дней) — каждое улучшение желанное; наука N — когда все остальные на уровне N.
- 🐎 ЛОШАДИ продаёт игра за монеты (монеты сгорают: ledger 'horse_buy') — лоты на бирже.
- 🔋 ШАТТЛ летает на батарейке: заряд продлевает льготы на SHUTTLE_CHARGE_DAYS.
Всё — внутри транзакции вызывающего кода.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from shared.economy import tech_cooldown_cut, user_bonus
from shared.economy import (HORSE_PRICES, MAX_HORSES, SHUTTLE_CHARGE_DAYS, TECH_ORDER, TECHS, TOOL_COSTS,
                            extend_expiry, science_gate_ok, tech_cooldown_days, tech_cost, tech_tool_required)
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import t
from shared.resources import RESOURCE_ICONS, InsufficientResources, spend_bundle


class TechError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


async def get_tech(conn, user_id: int) -> dict[str, dict]:
    """{tech: {"level", "updated_at", "cut"}} для всех технологий и инструментов (нули тоже).
    cut — скидка перерыва 🔬, закреплённая в момент изучения уровня (костюм потом можно снять)."""
    rows = await conn.fetch("SELECT tech, level, updated_at, cd_cut FROM user_tech WHERE user_id = $1", user_id)
    out = {k: {"level": 0, "updated_at": None, "cut": 0} for k in (*TECH_ORDER, "tools")}
    for r in rows:
        out[r["tech"]] = {"level": r["level"], "updated_at": r["updated_at"], "cut": r["cd_cut"] or 0}
    return out


async def tech_levels(conn, user_id: int) -> dict[str, int]:
    return {k: v["level"] for k, v in (await get_tech(conn, user_id)).items()}


def next_tech_at(tech: str, level: int, updated_at: datetime | None, cut_pct: int = 0) -> datetime | None:
    """Когда можно взять следующий уровень (None — уже можно). cut_pct — 🔬 костюм учёного (30.10)."""
    if level <= 0 or updated_at is None:
        return None
    return updated_at + timedelta(days=tech_cooldown_cut(tech_cooldown_days(tech, level), cut_pct))


async def _spend(conn, user_id: int, cost: dict, reason: str) -> None:
    try:
        await spend_bundle(conn, user_id, cost, reason)
    except InsufficientResources as e:
        raise TechError("ws.err_resources", need=e.need, have=e.have, kind=RESOURCE_ICONS[e.kind]) from e


async def _set_level(conn, user_id: int, tech: str, level: int, now: datetime, cut: int = 0) -> None:
    await conn.execute(
        """INSERT INTO user_tech (user_id, tech, level, updated_at, cd_cut) VALUES ($1, $2, $3, $4, $5)
           ON CONFLICT (user_id, tech) DO UPDATE SET level = EXCLUDED.level, updated_at = EXCLUDED.updated_at,
                                                     cd_cut = EXCLUDED.cd_cut""",
        user_id, tech, level, now, cut)


async def upgrade_tools(conn, user_id: int, now: datetime) -> int:
    """Следующий набор инструментов. Возвращает новый уровень."""
    await conn.fetchval("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    level = (await get_tech(conn, user_id))["tools"]["level"]
    if level >= len(TOOL_COSTS):
        raise TechError("tech.err_max")
    await _spend(conn, user_id, TOOL_COSTS[level + 1], f"tools:{level + 1}")
    await _set_level(conn, user_id, "tools", level + 1, now)
    from shared.trophies import record
    await record(conn, user_id, "tech")
    return level + 1


async def upgrade_tech(conn, user_id: int, tech: str, now: datetime) -> int:
    """Следующий уровень технологии. Возвращает новый уровень."""
    if tech not in TECHS:
        raise TechError("tech.err_unknown")
    user = await conn.fetchrow("SELECT suit, suit_level, art_bonus FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    state = await get_tech(conn, user_id)
    level = state[tech]["level"]
    if level >= TECHS[tech]["max"]:
        raise TechError("tech.err_max")
    if tech == "science" and not science_gate_ok({k: v["level"] for k, v in state.items()}, level + 1):
        raise TechError("tech.err_science", level=level + 1)
    need_tool = tech_tool_required(tech, level + 1)
    if state["tools"]["level"] < need_tool:
        raise TechError("tech.err_tool", tool=need_tool)
    cut = user_bonus(user, "sc")
    # перерыв — по лучшей скидке: закреплённой при прошлом изучении или костюму, надетому сейчас
    ready = next_tech_at(tech, level, state[tech]["updated_at"], max(cut, state[tech]["cut"]))
    if ready is not None and ready > now:
        raise TechError("tech.err_cooldown", hours=max(1, -(-int((ready - now).total_seconds()) // 3600)))
    await _spend(conn, user_id, tech_cost(tech, level + 1), f"tech:{tech}:{level + 1}")
    await _set_level(conn, user_id, tech, level + 1, now, cut)
    from shared.trophies import record
    await record(conn, user_id, "tech")   # 🏆 открытие в Лаборатории
    return level + 1


async def buy_horse(conn, user_id: int) -> int:
    """Покупка лошади у игры за монеты (сгорают). Возвращает число лошадей."""
    horses = await conn.fetchval("SELECT horses FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if horses is None:
        raise TechError("common.no_profile")
    if horses >= MAX_HORSES:
        raise TechError("horse.err_max", max=MAX_HORSES)
    price = HORSE_PRICES[horses]
    try:
        await change_balance(conn, user_id, -price, "horse_buy", str(horses + 1))
    except InsufficientFunds as e:
        raise TechError("horse.err_coins", price=price) from e
    await conn.execute("UPDATE users SET horses = horses + 1 WHERE user_id = $1", user_id)
    return horses + 1


async def charge_shuttle(conn, user_id: int, now: datetime) -> datetime:
    """Заряд Шаттла одной батарейкой: льготы биржи ещё на SHUTTLE_CHARGE_DAYS."""
    user = await conn.fetchrow("SELECT has_shuttle, shuttle_until FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user or not user["has_shuttle"]:
        raise TechError("shuttle.err_none")
    await _spend(conn, user_id, {"battery": 1}, "shuttle_charge")
    until = extend_expiry(user["shuttle_until"], now, SHUTTLE_CHARGE_DAYS)
    await conn.execute("UPDATE users SET shuttle_until = $2 WHERE user_id = $1", user_id, until)
    return until


def shuttle_active(user, now: datetime) -> bool:
    """Льготы Шаттла действуют, пока он заряжен."""
    return bool(user["has_shuttle"]) and user["shuttle_until"] is not None and user["shuttle_until"] > now
