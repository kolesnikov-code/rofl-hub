"""
Движок экономики фермы (Блок 2).

Чистая часть (simulate_farm и помощники) не знает про БД и Telegram — на ней
живут юнит-тесты сценариев начисления. apply_lazy_farm() — единственная точка
входа для обработчиков: блокирует строки, прогоняет симуляцию, пишет итог.

Правила:
- каждый робот — строка в таблице miners со своей датой сгорания (30 дней);
- Мастер-дрон «замораживает» жизнь роботов: пока дрон активен, срок сгорания
  не тикает (expires_at сдвигается ровно на защищённое время);
- Кибер-Бурильщик ест топливо ЦЕЛЫМИ котлетами: одна котлета — 24 часа работы.
  Под Ядерным разгоном котлета горит втрое быстрее — 8 часов (решение владельца 26.10: разгон работает
  при любом числе котлет, раньше на новый цикл требовалось сразу 3 и с 1–2 котлетами робот стоял).
  miners.fuel_until хранит «конец топлива без разгона»; реальный конец считает fuel_real_end().
  Никаких дробных списаний «int() в ноль» — вечный бурильщик больше невозможен;
- бусты действуют по времени своего сегмента: Азот +40% к базе, Ядерный ×5,
  эффекты складываются (5→7→35, 10→14→70);
- начисления точные: копим монето-микросекунды (MINING_ACC_PER_ROFL на 1 монета),
  на баланс уходят только целые монеты, остаток хранится в users.mining_acc.
"""
from __future__ import annotations

import heapq
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta

from shared.economy import (
    AWAY_MIN_MINUTES,
    CUTLET_ENERGY_SECONDS,
    MINING_ACC_PER_ROFL,
    NUCLEAR_FUEL_MULTIPLIER,
    cutlets_per_cycle,
    farm_bonus_percent,
    BANNER_BONUS_PERCENT,
    THERMOS_FUEL_CYCLE_SECONDS,
    is_active,
    miner_hourly_rate,
    utcnow,
)
from shared.ledger import change_balance

_MICROSECOND = timedelta(microseconds=1)
FUEL_CYCLE = timedelta(seconds=CUTLET_ENERGY_SECONDS)
THERMOS_CYCLE = timedelta(seconds=THERMOS_FUEL_CYCLE_SECONDS)   # 🧊 Термос: котлеты хватает дольше


def _micros(td: timedelta) -> int:
    """Длительность в целых микросекундах (точная целочисленная математика)."""
    return td // _MICROSECOND


@dataclass
class MinerState:
    """Снимок одной строки таблицы miners."""
    miner_id: int
    kind: str                       # 'intern' | 'junior' | 'premium'
    purchased_at: datetime
    expires_at: datetime
    fuel_until: datetime | None = None


@dataclass
class FarmTick:
    """Результат одного ленивого пересчёта."""
    earned: int                     # целых монет к зачислению
    acc: int                        # новый остаток монето-микросекунд (< MINING_ACC_PER_ROFL)
    fridge_cutlets: int
    cutlets_consumed: int
    miners: list[MinerState]        # обновлённые состояния (включая сгоревших)
    expired_ids: list[int] = field(default_factory=list)


def integrate_rate_micros(start: datetime, end: datetime, kind: str,
                          nuclear_until: datetime | None,
                          nitrogen_until: datetime | None,
                          bonus_percent: int = 0,
                          armor_percent: int = 0,
                          armor_until: datetime | None = None,
                          windows: tuple = ()) -> int:
    """
    Монето-микросекунды, заработанные роботом kind за [start, end),
    с разбиением на сегменты по моментам окончания бустов.
    bonus_percent — постоянный бонус (станция команды); armor_percent действует до
    armor_until (Кибер-броня на 30 дней). Бонусы применяются к микросекундам сегмента. windows — окна временных бонусов
    ((начало, конец, процент), …): Знамя команды; действуют только внутри окна.
    """
    if end <= start:
        return 0
    points = {start, end}
    window_points = [p for w in windows for p in (w[0], w[1])]
    for boundary in (nuclear_until, nitrogen_until, armor_until if armor_percent else None, *window_points):
        if boundary is not None and start < boundary < end:
            points.add(boundary)
    total = 0
    ordered = sorted(points)
    for seg_start, seg_end in zip(ordered, ordered[1:]):
        rate = miner_hourly_rate(
            kind,
            nuclear_active=is_active(nuclear_until, seg_start),
            nitrogen_active=is_active(nitrogen_until, seg_start),
        )
        seg_bonus = bonus_percent + (armor_percent if is_active(armor_until, seg_start) else 0)
        seg_bonus += sum(w[2] for w in windows if w[0] <= seg_start < w[1])
        micros = _micros(seg_end - seg_start) * rate
        total += micros * (100 + seg_bonus) // 100 if seg_bonus else micros
    return total


def _nuclear_left(cursor: datetime, nuclear_until: datetime | None) -> timedelta:
    """Сколько ещё длится Ядерный разгон, начиная с cursor (он всегда активен с начала интервала: включение
    разгона сначала закрывает прошлое время фермы)."""
    if nuclear_until is None or nuclear_until <= cursor:
        return timedelta(0)
    return nuclear_until - cursor


def fuel_real_end(cursor: datetime, energy_end: datetime, nuclear_until: datetime | None) -> datetime:
    """
    Когда реально кончится топливо (решение владельца 26.10 — «по котлете на 8 часов»). energy_end — момент, когда
    оно кончилось бы без разгона; под Ядерным разгоном котлета горит в NUCLEAR_FUEL_MULTIPLIER раз быстрее,
    после разгона остаток догорает в обычном темпе — ни минуты не пропадает.
    """
    energy = energy_end - cursor
    if energy <= timedelta(0):
        return cursor
    boosted = min(energy / NUCLEAR_FUEL_MULTIPLIER, _nuclear_left(cursor, nuclear_until))
    return cursor + boosted + (energy - boosted * NUCLEAR_FUEL_MULTIPLIER)


def fuel_energy_end(cursor: datetime, energy_end: datetime, nuclear_until: datetime | None, at: datetime) -> datetime:
    """Остаток топлива в момент at (cursor ≤ at < реального конца) — снова как «конец без разгона»."""
    nuclear = min(_nuclear_left(cursor, nuclear_until), at - cursor)
    used = nuclear * NUCLEAR_FUEL_MULTIPLIER + (at - cursor - nuclear)
    return at + (energy_end - cursor - used)


def simulate_farm(*, last_update: datetime, now: datetime, fridge_cutlets: int,
                  acc: int, miners: list[MinerState],
                  nuclear_until: datetime | None = None,
                  nitrogen_until: datetime | None = None,
                  drone_until: datetime | None = None,
                  bonus_percent: int = 0,
                  armor_percent: int = 0,
                  armor_until: datetime | None = None,
                  bonus_windows: tuple = (),
                  thermos_from: datetime | None = None,
                  thermos_until: datetime | None = None) -> FarmTick:
    """
    Чистая симуляция фермы за интервал [last_update, now]. Вход не мутирует.

    Бурильщики заправляются в хронологическом порядке (кто раньше остался без
    топлива — тот раньше берёт котлеты из холодильника): честно при дефиците.
    """
    miners = [replace(m) for m in miners]
    consumed = 0

    if now > last_update:
        refuel_queue: list[tuple[datetime, int, MinerState]] = []

        for m in miners:
            start = max(last_update, m.purchased_at)
            if start >= now or m.expires_at <= start:
                continue  # куплен в будущем относительно интервала или уже сгорел

            # Дрон замораживает срок жизни: сдвигаем сгорание на защищённое время
            if drone_until is not None and drone_until > start:
                protected = min(now, drone_until) - start
                m.expires_at += protected

            work_end = min(now, m.expires_at)

            if m.kind in ("junior", "intern"):   # без топлива: Майнер и Стажёр
                acc += integrate_rate_micros(start, work_end, m.kind, nuclear_until, nitrogen_until,
                                             bonus_percent, armor_percent, armor_until, bonus_windows)
                continue

            # premium: сначала дорабатываем уже оплаченное топливо (fuel_until — «конец без разгона»)
            cursor = start
            if m.fuel_until is not None and m.fuel_until > cursor:
                real_end = fuel_real_end(cursor, m.fuel_until, nuclear_until)
                seg_end = min(real_end, work_end)
                acc += integrate_rate_micros(cursor, seg_end, "premium", nuclear_until, nitrogen_until,
                                             bonus_percent, armor_percent, armor_until, bonus_windows)
                m.fuel_until = fuel_energy_end(cursor, m.fuel_until, nuclear_until, work_end) if real_end > work_end else real_end
                cursor = seg_end
            if cursor < work_end:
                heapq.heappush(refuel_queue, (cursor, m.miner_id, m))

        # Заправки всех бурильщиков — строго по времени наступления. Котлета всегда одна (26.10): под Ядерным
        # разгоном она просто горит втрое быстрее (8 ч вместо 24) — разгон работает при любом числе котлет.
        while refuel_queue:
            moment, _, m = heapq.heappop(refuel_queue)
            cost = cutlets_per_cycle(False)
            if fridge_cutlets < cost:
                continue  # котлет нет — робот простаивает до конца интервала
            fridge_cutlets -= cost
            consumed += cost
            thermos = thermos_from is not None and thermos_until is not None and thermos_from <= moment < thermos_until
            energy_end = moment + (THERMOS_CYCLE if thermos else FUEL_CYCLE)
            real_end = fuel_real_end(moment, energy_end, nuclear_until)
            work_end = min(now, m.expires_at)
            seg_end = min(real_end, work_end)
            acc += integrate_rate_micros(moment, seg_end, "premium", nuclear_until, nitrogen_until,
                                         bonus_percent, armor_percent, armor_until, bonus_windows)
            if real_end < work_end:
                m.fuel_until = real_end
                heapq.heappush(refuel_queue, (real_end, m.miner_id, m))
            else:
                m.fuel_until = fuel_energy_end(moment, energy_end, nuclear_until, work_end) if real_end > work_end else real_end

    earned = acc // MINING_ACC_PER_ROFL
    acc -= earned * MINING_ACC_PER_ROFL
    expired_ids = [m.miner_id for m in miners if m.expires_at <= now]
    return FarmTick(earned=earned, acc=acc, fridge_cutlets=fridge_cutlets,
                    cutlets_consumed=consumed, miners=miners, expired_ids=expired_ids)


def farm_counts(miners: list[MinerState], now: datetime) -> dict[str, int]:
    """Счётчики для витрин: живые роботы и сколько бурильщиков заправлено."""
    alive = [m for m in miners if m.expires_at > now]
    premium = [m for m in alive if m.kind == "premium"]
    fueled = [m for m in premium if m.fuel_until is not None and m.fuel_until > now]
    return {
        "intern": sum(1 for m in alive if m.kind == "intern"),
        "junior": sum(1 for m in alive if m.kind == "junior"),
        "premium": len(premium),
        "premium_fueled": len(fueled),
    }


# --------------------------------------------------------------------------
# Слой БД: вызывается ВНУТРИ транзакции обработчика
# --------------------------------------------------------------------------
async def user_bonus_percent(conn, user) -> int:
    """Постоянный бонус к добыче: станция команды + 📚 наука (броня — отдельно, у неё срок)."""
    from shared.economy import SCIENCE_PERCENT_PER_LEVEL
    science = await conn.fetchval(
        "SELECT level FROM user_tech WHERE user_id = $1 AND tech = 'science'", user["user_id"]) or 0
    station_level = 0
    if user["team_id"] is not None:
        station_level = await conn.fetchval(
            "SELECT level FROM team_stations WHERE team_id = $1", user["team_id"]) or 0
    return farm_bonus_percent(0, station_level) + science * SCIENCE_PERCENT_PER_LEVEL


def away_summary(prev_seen: datetime | None, now: datetime, mined: int) -> dict | None:
    """«Пока тебя не было»: сколько роботы добыли с прошлого открытия приложения (владелец 13.11).
    Окно — только после перерыва не меньше AWAY_MIN_MINUTES и если добыто хоть что-то."""
    if prev_seen is None or mined <= 0 or now - prev_seen < timedelta(minutes=AWAY_MIN_MINUTES):
        return None
    return {"coins": int(mined), "seconds": int((now - prev_seen).total_seconds())}


async def mined_since(conn, user_id: int, since: datetime) -> int:
    """Монеты фермы (ledger 'mining') после момента since — сколько бы раз ферму ни пересчитывали между делом."""
    return int(await conn.fetchval(
        "SELECT COALESCE(SUM(delta), 0) FROM ledger WHERE user_id = $1 AND reason = 'mining' AND created_at > $2",
        user_id, since) or 0)


async def apply_lazy_farm(conn, user_id: int, now: datetime | None = None):
    """
    Ленивый пересчёт фермы. Блокирует users и miners, начисляет добычу через
    ledger, удаляет сгоревших роботов. Возвращает (user_row, живые MinerState)
    или (None, []) если профиля нет.
    """
    user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user:
        return None, []

    now = now or utcnow()
    # Момент мог быть взят ДО блокировки (параллельный запрос или массовая выдача призов успела пересчитать
    # ферму позже) — время фермы никогда не идёт назад, иначе отрезок начислится второй раз
    if user["last_update_time"] is not None and now < user["last_update_time"]:
        now = user["last_update_time"]
    rows = await conn.fetch(
        "SELECT miner_id, kind, purchased_at, expires_at, fuel_until "
        "FROM miners WHERE user_id = $1 ORDER BY miner_id FOR UPDATE",
        user_id,
    )
    before = [MinerState(r["miner_id"], r["kind"], r["purchased_at"],
                         r["expires_at"], r["fuel_until"]) for r in rows]

    bonus = await user_bonus_percent(conn, user)
    windows: tuple = ()
    if user["team_id"] is not None:   # 🏳️ Знамя команды: окна бонуса, пересекающие интервал
        rows_b = await conn.fetch(
            "SELECT starts_at, ends_at FROM team_banners WHERE team_id = $1 AND ends_at > $2 AND starts_at < $3",
            user["team_id"], user["last_update_time"], now)
        windows = tuple((r["starts_at"], r["ends_at"], BANNER_BONUS_PERCENT) for r in rows_b)
    tick = simulate_farm(
        last_update=user["last_update_time"], now=now,
        fridge_cutlets=user["fridge_cutlets"], acc=user["mining_acc"],
        miners=before,
        nuclear_until=user["boost_nuclear_until"],
        nitrogen_until=user["boost_nitrogen_until"],
        drone_until=user["drone_until"],
        bonus_percent=bonus,
        armor_percent=farm_bonus_percent(user["farm_armor_level"], 0),
        armor_until=user["armor_until"],
        bonus_windows=windows,
        thermos_from=user["thermos_from"],
        thermos_until=user["thermos_until"],
    )

    expired = set(tick.expired_ids)
    for old, new in zip(before, tick.miners):
        if new.miner_id in expired:
            continue
        if new.expires_at != old.expires_at or new.fuel_until != old.fuel_until:
            await conn.execute(
                "UPDATE miners SET expires_at = $2, fuel_until = $3 WHERE miner_id = $1",
                new.miner_id, new.expires_at, new.fuel_until,
            )
    if expired:
        await conn.execute("DELETE FROM miners WHERE miner_id = ANY($1::bigint[])", list(expired))

    if tick.earned > 0:
        await change_balance(conn, user_id, tick.earned, "mining")

    await conn.execute(
        """
        UPDATE users
        SET fridge_cutlets = $2, mining_acc = $3, last_update_time = $4
        WHERE user_id = $1
        """,
        user_id, tick.fridge_cutlets, tick.acc, now,
    )

    fresh = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
    alive = [m for m in tick.miners if m.miner_id not in expired]
    return fresh, alive
