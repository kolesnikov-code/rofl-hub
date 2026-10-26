"""
Блок 2 «Экономика фермы»: 60+ сценариев начисления на чистом симуляторе.

Ключевые регрессии:
- «вечный бурильщик»: раньше int() обрезал дробный расход котлет до нуля —
  теперь топливо списывается ЦЕЛЫМИ циклами 24ч;
- потеря «копеек времени»: остаток хранится в монето-микросекундах, суммарное
  начисление не зависит от того, на сколько заходов разбит интервал.
"""
from datetime import datetime, timedelta, timezone

import pytest

from shared.economy import (
    MINING_ACC_PER_ROFL,
    cutlets_per_cycle,
    daily_bonus_seconds_left,
    miner_hourly_rate,
)
from shared.farm_logic import (
    MinerState,
    farm_counts,
    integrate_rate_micros,
    simulate_farm,
)

T0 = datetime(2026, 10, 16, 0, 0, tzinfo=timezone.utc)
ROFL = MINING_ACC_PER_ROFL
MONTH = timedelta(days=30)


def h(n: float) -> datetime:
    return T0 + timedelta(hours=n)


def junior(miner_id=1, bought=T0, expires=None) -> MinerState:
    return MinerState(miner_id, "junior", bought, expires or bought + MONTH)


def premium(miner_id=1, bought=T0, expires=None, fuel_until=None) -> MinerState:
    return MinerState(miner_id, "premium", bought, expires or bought + MONTH, fuel_until)


def tick(miners, *, start=T0, hours=1.0, fridge=0, acc=0, nuclear=None, nitrogen=None, drone=None):
    return simulate_farm(
        last_update=start, now=start + timedelta(hours=hours),
        fridge_cutlets=fridge, acc=acc, miners=miners,
        nuclear_until=nuclear, nitrogen_until=nitrogen, drone_until=drone,
    )


# ==========================================================================
# Ставки и стоимость цикла (числа владельца: 5→7→35, 10→14→70, котлеты 1/3)
# ==========================================================================
@pytest.mark.parametrize("kind,nuclear,nitrogen,rate", [
    ("junior", False, False, 5),
    ("junior", False, True, 7),
    ("junior", True, False, 25),
    ("junior", True, True, 35),
    ("premium", False, False, 10),
    ("premium", False, True, 14),
    ("premium", True, False, 50),
    ("premium", True, True, 70),
])
def test_hourly_rates(kind, nuclear, nitrogen, rate):
    assert miner_hourly_rate(kind, nuclear_active=nuclear, nitrogen_active=nitrogen) == rate


@pytest.mark.parametrize("nuclear,cost", [(False, 1), (True, 3)])
def test_cutlets_per_cycle(nuclear, cost):
    assert cutlets_per_cycle(nuclear) == cost


# ==========================================================================
# integrate_rate_micros: интеграл ставки с брейкпоинтами бустов
# ==========================================================================
def test_integrate_plain_hour():
    assert integrate_rate_micros(T0, h(1), "junior", None, None) == 5 * ROFL


def test_integrate_empty_and_reversed_interval():
    assert integrate_rate_micros(T0, T0, "junior", None, None) == 0
    assert integrate_rate_micros(h(1), T0, "junior", None, None) == 0


def test_integrate_nuclear_boundary_split():
    # [0,1] под разгоном 25/ч, [1,2] база 5/ч
    assert integrate_rate_micros(T0, h(2), "junior", h(1), None) == 30 * ROFL


def test_integrate_nitrogen_boundary_split_premium():
    assert integrate_rate_micros(T0, h(2), "premium", None, h(1)) == 24 * ROFL


def test_integrate_boost_expiring_exactly_at_start_is_inactive():
    assert integrate_rate_micros(T0, h(1), "junior", T0, None) == 5 * ROFL


def test_integrate_both_boosts_active():
    assert integrate_rate_micros(T0, h(1), "premium", h(5), h(5)) == 70 * ROFL


def test_integrate_half_hour_fraction():
    assert integrate_rate_micros(T0, T0 + timedelta(minutes=30), "junior", None, None) == 5 * ROFL // 2


# ==========================================================================
# Младшие Майнеры: базовые начисления и точность
# ==========================================================================
def test_junior_one_hour():
    r = tick([junior()], hours=1)
    assert (r.earned, r.acc, r.cutlets_consumed) == (5, 0, 0)


def test_junior_half_hour_keeps_remainder():
    r = tick([junior()], hours=0.5)
    assert r.earned == 2
    assert r.acc == 5 * ROFL // 2 - 2 * ROFL


def test_junior_two_passes_equal_one():
    r1 = tick([junior()], hours=0.5)
    r2 = simulate_farm(last_update=h(0.5), now=h(1), fridge_cutlets=0,
                       acc=r1.acc, miners=r1.miners)
    assert r1.earned + r2.earned == 5
    assert r2.acc == 0


def test_three_juniors_two_hours():
    r = tick([junior(1), junior(2), junior(3)], hours=2)
    assert r.earned == 30


def test_junior_bought_mid_interval_clamped():
    r = tick([junior(bought=h(1))], hours=3)
    assert r.earned == 10


def test_junior_bought_in_future_earns_nothing():
    r = tick([junior(bought=h(5))], hours=3)
    assert r.earned == 0
    assert r.expired_ids == []


def test_junior_expires_mid_interval():
    r = tick([junior(expires=h(1))], hours=3)
    assert r.earned == 5
    assert r.expired_ids == [1]


def test_junior_already_expired_before_interval():
    r = tick([junior(expires=T0 - timedelta(hours=1))], hours=3)
    assert r.earned == 0
    assert r.expired_ids == [1]


def test_zero_length_interval_is_noop():
    r = tick([junior()], hours=0, fridge=4)
    assert (r.earned, r.fridge_cutlets, r.cutlets_consumed) == (0, 4, 0)


def test_clock_going_backwards_is_noop():
    r = simulate_farm(last_update=h(1), now=T0, fridge_cutlets=2, acc=0, miners=[junior()])
    assert (r.earned, r.cutlets_consumed) == (0, 0)


def test_no_miners_nothing_earned():
    r = tick([], hours=10, fridge=3)
    assert (r.earned, r.fridge_cutlets) == (0, 3)


def test_sixty_one_minute_passes_lose_nothing():
    """Регрессия: раньше int() на каждом заходе съедал дробные начисления."""
    acc, earned, cursor = 0, 0, T0
    miners = [junior()]
    for _ in range(60):
        r = simulate_farm(last_update=cursor, now=cursor + timedelta(minutes=1),
                          fridge_cutlets=0, acc=acc, miners=miners)
        acc, miners, cursor = r.acc, r.miners, cursor + timedelta(minutes=1)
        earned += r.earned
    assert earned == 5
    assert acc == 0


def test_input_miners_not_mutated():
    m = junior(expires=h(1))
    tick([m], hours=3, drone=h(2))
    assert m.expires_at == h(1)


# ==========================================================================
# Кибер-Бурильщики: топливо целыми циклами 24ч
# ==========================================================================
def test_premium_without_fuel_idles():
    r = tick([premium()], hours=10)
    assert (r.earned, r.cutlets_consumed) == (0, 0)
    assert r.miners[0].fuel_until is None


def test_premium_one_cutlet_runs_exactly_24h_of_48():
    """Регрессия «вечный бурильщик»: 1 котлета = ровно 24 часа, не больше."""
    r = tick([premium()], hours=48, fridge=1)
    assert r.earned == 240
    assert r.cutlets_consumed == 1
    assert r.fridge_cutlets == 0
    assert r.miners[0].fuel_until == h(24)


def test_premium_chains_two_cycles():
    r = tick([premium()], hours=48, fridge=5)
    assert r.earned == 480
    assert r.cutlets_consumed == 2
    assert r.fridge_cutlets == 3
    assert r.miners[0].fuel_until == h(48)


def test_premium_partial_cycle_keeps_fuel_for_later():
    r = tick([premium()], hours=12, fridge=1)
    assert r.earned == 120
    assert r.cutlets_consumed == 1
    assert r.miners[0].fuel_until == h(24)


def test_premium_second_pass_uses_remaining_fuel_without_new_cutlet():
    r1 = tick([premium()], hours=12, fridge=1)
    r2 = simulate_farm(last_update=h(12), now=h(24), fridge_cutlets=0,
                       acc=r1.acc, miners=r1.miners)
    assert r2.earned == 120
    assert r2.cutlets_consumed == 0


def test_premium_stops_when_fridge_empty_after_fuel_ends():
    r1 = tick([premium()], hours=24, fridge=1)
    r2 = simulate_farm(last_update=h(24), now=h(30), fridge_cutlets=0,
                       acc=r1.acc, miners=r1.miners)
    assert r2.earned == 0


def test_premium_prefueled_ignores_empty_fridge():
    r = tick([premium(fuel_until=h(24))], hours=48)
    assert r.earned == 240
    assert r.cutlets_consumed == 0


def test_premium_expiry_cuts_earnings_even_with_fuel():
    r = tick([premium(expires=h(10))], hours=24, fridge=5)
    assert r.earned == 100
    assert r.cutlets_consumed == 1  # цикл списан целиком при старте
    assert r.expired_ids == [1]


def test_two_drills_one_cutlet_lower_id_wins():
    r = tick([premium(1), premium(2)], hours=24, fridge=1)
    assert r.earned == 240
    assert r.miners[0].fuel_until == h(24)
    assert r.miners[1].fuel_until is None


def test_refuel_order_is_chronological_not_by_id():
    """Кто раньше остался без топлива — тот раньше берёт котлету."""
    a = premium(1, fuel_until=h(10))
    b = premium(2)
    r = tick([a, b], hours=30, fridge=1)
    # b заправился в t0 и отработал 24ч; a доработал своё топливо и встал в h10
    assert r.earned == 100 + 240
    assert r.cutlets_consumed == 1
    assert r.miners[0].fuel_until == h(10)
    assert r.miners[1].fuel_until == h(24)


def test_mixed_farm_totals():
    r = tick([junior(1), junior(2), premium(3)], hours=24, fridge=1)
    assert r.earned == 5 * 24 * 2 + 240
    assert r.cutlets_consumed == 1


def test_premium_bought_mid_interval_starts_cycle_at_purchase():
    r = tick([premium(bought=h(10))], hours=24, fridge=1)
    assert r.earned == 140  # работал [10, 24]
    assert r.miners[0].fuel_until == h(34)


@pytest.mark.parametrize("fridge,hours,earned,consumed", [
    (0, 24, 0, 0),
    (1, 24, 240, 1),
    (2, 24, 240, 1),
    (2, 48, 480, 2),
    (3, 72, 720, 3),
    (1, 72, 240, 1),
    (10, 24, 240, 1),
])
def test_premium_fuel_table(fridge, hours, earned, consumed):
    r = tick([premium()], hours=hours, fridge=fridge)
    assert (r.earned, r.cutlets_consumed) == (earned, consumed)


# ==========================================================================
# Ядерный Разгон: скорость ×5, расход ×3
# ==========================================================================
def test_nuclear_junior_speed_x5():
    r = tick([junior()], hours=1, nuclear=h(24))
    assert r.earned == 25


def test_nuclear_expires_mid_interval_junior():
    r = tick([junior()], hours=2, nuclear=h(1))
    assert r.earned == 30


def test_nuclear_cycle_costs_three_cutlets():
    r = tick([premium()], hours=24, fridge=3, nuclear=h(24))
    assert r.earned == 24 * 50
    assert r.cutlets_consumed == 3
    assert r.fridge_cutlets == 0


def test_nuclear_works_with_fewer_than_three_cutlets():
    # 26.10: под разгоном котлета горит за 8 ч — 2 котлеты = 16 ч работы ×5, потом простой без топлива
    r = tick([premium()], hours=24, fridge=2, nuclear=h(30))
    assert (r.earned, r.cutlets_consumed, r.fridge_cutlets) == (16 * 50, 2, 0)


def test_nuclear_one_cutlet_lasts_eight_hours():
    r = tick([premium()], hours=10, fridge=1, nuclear=h(30))
    assert (r.earned, r.cutlets_consumed) == (8 * 50, 1)
    assert r.miners[0].fuel_until == h(8)


def test_nuclear_ends_mid_cutlet_rest_burns_at_normal_rate():
    # Разгон 1 ч съел 3 ч «энергии» котлеты, остальные 21 ч она горит как обычно → конец в h22
    r = tick([premium()], hours=24, fridge=2, nuclear=h(1))
    assert r.earned == 50 + 21 * 10 + 2 * 10     # 1 ч ×5, 21 ч обычно, вторая котлета с h22
    assert r.cutlets_consumed == 2 and r.fridge_cutlets == 0
    assert r.miners[0].fuel_until == h(46)        # вторая котлета: энергия до h46 без разгона


def test_two_days_after_short_nuclear():
    r = tick([premium()], hours=48, fridge=4, nuclear=h(1))
    assert r.cutlets_consumed == 3                  # h0→h22, h22→h46, h46→…
    assert r.earned == 50 + 210 + 240 + 20
    assert r.fridge_cutlets == 1


def test_nuclear_burns_prefueled_cutlet_three_times_faster():
    # Заправлен на сутки, разгон на сутки: оставшиеся 24 ч «энергии» сгорают за 8 ч на ×5
    r = tick([premium(fuel_until=h(24))], hours=24, nuclear=h(24))
    assert (r.earned, r.cutlets_consumed) == (8 * 50, 0)


def test_nuclear_split_ticks_equal_one_tick():
    """Ленивый пересчёт кусками даёт то же, что одним интервалом (fuel_until — «энергия без разгона»)."""
    whole = tick([premium()], hours=30, fridge=3, nuclear=h(5))
    acc, fridge, miners, earned = 0, 3, [premium()], 0
    for i in range(30):
        r = simulate_farm(last_update=h(i), now=h(i + 1), fridge_cutlets=fridge, acc=acc, miners=miners,
                          nuclear_until=h(5))
        acc, fridge, miners, earned = r.acc, r.fridge_cutlets, r.miners, earned + r.earned
    assert (earned, fridge) == (whole.earned, whole.fridge_cutlets)


# ==========================================================================
# Азотное Охлаждение: +40% (5→7, 10→14), складывается с разгоном
# ==========================================================================
def test_nitrogen_junior():
    r = tick([junior()], hours=1, nitrogen=h(24))
    assert r.earned == 7


def test_nitrogen_premium_full_day():
    r = tick([premium()], hours=24, fridge=1, nitrogen=h(24))
    assert r.earned == 336
    assert r.cutlets_consumed == 1  # азот НЕ увеличивает расход


def test_nitrogen_expires_mid_interval():
    r = tick([junior()], hours=2, nitrogen=h(1))
    assert r.earned == 12


def test_both_boosts_stack_junior():
    r = tick([junior()], hours=1, nuclear=h(24), nitrogen=h(24))
    assert r.earned == 35


def test_both_boosts_stack_premium():
    r = tick([premium()], hours=24, fridge=3, nuclear=h(24), nitrogen=h(24))
    assert r.earned == 24 * 70
    assert r.cutlets_consumed == 3


def test_boosts_expire_at_different_times():
    # [0,1] оба (35), [1,2] только азот (7), [2,3] база (5)
    r = tick([junior()], hours=3, nuclear=h(1), nitrogen=h(2))
    assert r.earned == 47


# ==========================================================================
# Мастер-дрон: замораживает срок жизни роботов
# ==========================================================================
def test_drone_extends_life_by_protected_time():
    r = tick([junior(expires=h(5))], hours=20, drone=h(10))
    assert r.earned == 75  # жизнь заморожена на 10ч: работал 15ч
    assert r.expired_ids == [1]  # h15 уже позади при now=h20


def test_drone_covering_whole_interval_keeps_robot_alive():
    r = tick([junior(expires=h(5))], hours=20, drone=h(30))
    assert r.earned == 100  # весь интервал жив
    assert r.miners[0].expires_at == h(25)
    assert r.expired_ids == []


def test_drone_does_not_resurrect_dead_robot():
    r = tick([junior(expires=T0 - timedelta(hours=1))], hours=10, drone=h(30))
    assert r.earned == 0
    assert r.miners[0].expires_at == T0 - timedelta(hours=1)


def test_expired_drone_gives_no_protection():
    r = tick([junior(expires=h(5))], hours=20, drone=T0 - timedelta(hours=1))
    assert r.earned == 25
    assert r.miners[0].expires_at == h(5)


def test_drone_partial_window():
    r = tick([junior(expires=h(30))], hours=20, drone=h(8))
    assert r.miners[0].expires_at == h(38)
    assert r.earned == 100


def test_drone_protects_from_purchase_moment_only():
    r = tick([junior(bought=h(2), expires=h(2) + MONTH)], hours=20, drone=h(10))
    assert r.miners[0].expires_at == h(2) + MONTH + timedelta(hours=8)


def test_drone_does_not_feed_drills():
    r = tick([premium(expires=h(12))], hours=30, fridge=2, drone=h(12))
    # жизнь продлена до h24, цикл списан целиком, работал [0,24]
    assert r.earned == 240
    assert r.cutlets_consumed == 1
    assert r.expired_ids == [1]


def test_drone_extension_accumulates_across_passes():
    r1 = tick([junior(expires=h(40))], hours=5, drone=h(30))
    assert r1.miners[0].expires_at == h(45)
    r2 = simulate_farm(last_update=h(5), now=h(10), fridge_cutlets=0,
                       acc=r1.acc, miners=r1.miners, drone_until=h(30))
    assert r2.miners[0].expires_at == h(50)


# ==========================================================================
# Эквивалентность разбиения: итог не зависит от числа заходов в бота
# ==========================================================================
def _run_split(miners, fridge, boundaries, end_h, **boosts):
    acc, earned, consumed, cursor = 0, 0, 0, T0
    for b in [*boundaries, end_h]:
        r = simulate_farm(last_update=cursor, now=h(b), fridge_cutlets=fridge,
                          acc=acc, miners=miners, **boosts)
        acc, miners, fridge, cursor = r.acc, r.miners, r.fridge_cutlets, h(b)
        earned += r.earned
        consumed += r.cutlets_consumed
    return earned, consumed, fridge, acc, miners


@pytest.mark.parametrize("boundaries", [[12], [1, 7, 30], [23.5], [5, 10, 15, 20, 40]])
def test_split_equivalence_premium_fuel(boundaries):
    single = tick([premium()], hours=48, fridge=3)
    split = _run_split([premium()], 3, boundaries, 48)
    assert split[:4] == (single.earned, single.cutlets_consumed, single.fridge_cutlets, single.acc)


@pytest.mark.parametrize("boundaries", [[4], [1, 9], [0.5, 19.5]])
def test_split_equivalence_with_drone_and_boosts(boundaries):
    kwargs = {"nuclear_until": h(6), "nitrogen_until": h(15), "drone_until": h(8)}
    single = simulate_farm(last_update=T0, now=h(20), fridge_cutlets=5, acc=0,
                           miners=[junior(1, expires=h(12)), premium(2)], **kwargs)
    split = _run_split([junior(1, expires=h(12)), premium(2)], 5, boundaries, 20, **kwargs)
    assert split[:4] == (single.earned, single.cutlets_consumed, single.fridge_cutlets, single.acc)
    assert [m.expires_at for m in split[4]] == [m.expires_at for m in single.miners]


# ==========================================================================
# Счётчики витрин и ежедневный бонус
# ==========================================================================
def test_farm_counts():
    miners = [
        junior(1), junior(2, expires=T0 - timedelta(hours=1)),
        premium(3, fuel_until=h(5)), premium(4), premium(5, fuel_until=T0 - timedelta(hours=1)),
    ]
    assert farm_counts(miners, T0) == {"intern": 0, "junior": 1, "premium": 3, "premium_fueled": 1}


def test_farm_counts_empty():
    assert farm_counts([], T0) == {"intern": 0, "junior": 0, "premium": 0, "premium_fueled": 0}


@pytest.mark.parametrize("last_claim,expected", [
    (None, 0),
    (T0, 24 * 3600),
    (T0 - timedelta(hours=12), 12 * 3600),
    (T0 - timedelta(hours=24), 0),
    (T0 - timedelta(hours=25), 0),
    (T0 - timedelta(hours=23, minutes=59), 60),
])
def test_daily_bonus_seconds_left(last_claim, expected):
    assert daily_bonus_seconds_left(last_claim, T0) == expected


def test_daily_bonus_rounds_partial_seconds_up():
    last = T0 - timedelta(hours=23, minutes=59, seconds=59, milliseconds=500)
    assert daily_bonus_seconds_left(last, T0) == 1
