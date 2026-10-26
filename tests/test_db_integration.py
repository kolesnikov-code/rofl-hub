"""
Интеграционные тесты на реальной PostgreSQL.

Запуск: задать TEST_DATABASE_URL (ОТДЕЛЬНАЯ пустая база!) и выполнить pytest.
Без переменной тесты пропускаются.
"""
import os
import uuid

import pytest

asyncpg = pytest.importorskip("asyncpg")

from shared.database import Database  # noqa: E402
from shared.delivery import DeliveryError, already_delivered, deliver_order  # noqa: E402
from shared.economy import START_BALANCE  # noqa: E402
from shared.ledger import InsufficientFunds, change_balance  # noqa: E402
from bots.main_bot.catalog import build_order  # noqa: E402

TEST_DSN = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not TEST_DSN, reason="TEST_DATABASE_URL не задан")


@pytest.fixture
async def conn():
    database = Database()
    await database.connect(TEST_DSN)
    await database.create_tables()
    async with database.pool.acquire() as c:
        await c.execute("TRUNCATE users, teams, star_payments, game_stats, auctions, ledger, "
                        "miners, duels, battles, vip_aliases, quest_progress, events, "
                        "daily_activity, promoters, metrics_snapshots, market_orders, "
                        "user_resources, resource_ledger, raids, daily_goal_claims, "
                        "team_stations, team_donations, market_trades, resource_swaps, weekly_crafts, team_help, user_items, team_banners, user_tech, user_badges, "
                        "season_results, battle_entries, battle_entry_log, reward_grants, expedition_targets, expeditions, "
                        "expedition_members, expedition_votes, expedition_log, expedition_peeks RESTART IDENTITY")
        await c.execute("UPDATE mines SET team_id = NULL, battle_id = NULL, captured_at = NULL, "
                        "captured_until = NULL, last_paid_at = NULL")
        await c.execute("DELETE FROM feature_flags WHERE key LIKE 'wsr:%'")
        yield c
    await database.close()


async def _mk_user(conn, user_id: int, balance: int = 0, **cols):
    extra_cols = "".join(f", {k}" for k in cols)
    extra_vals = "".join(f", ${i + 3}" for i in range(len(cols)))
    await conn.execute(
        f"INSERT INTO users (user_id, username, balance{extra_cols}) VALUES ($1, 'u', $2{extra_vals})",
        user_id, balance, *cols.values())


async def _tech(conn, user_id: int, **levels):
    """Уровни Лаборатории тестовому игроку (tools/comm/scout/attack/defense/science)."""
    for tech, level in levels.items():
        await conn.execute(
            "INSERT INTO user_tech (user_id, tech, level, updated_at) VALUES ($1, $2, $3, NOW() - INTERVAL '400 days') "
            "ON CONFLICT (user_id, tech) DO UPDATE SET level = EXCLUDED.level, updated_at = EXCLUDED.updated_at",
            user_id, tech, level)


# ---------------------------------------------------------------- ledger
async def test_change_balance_writes_ledger_and_blocks_negative(conn):
    await _mk_user(conn, 1, 100)
    assert await change_balance(conn, 1, -60, "test") == 40
    with pytest.raises(InsufficientFunds):
        await change_balance(conn, 1, -41, "test")
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1") == 40
    rows = await conn.fetch("SELECT delta, reason FROM ledger WHERE user_id = 1 ORDER BY id")
    assert [(r["delta"], r["reason"]) for r in rows] == [(-60, "test")]


async def test_db_constraint_rejects_negative_balance_even_with_raw_sql(conn):
    await _mk_user(conn, 2, 10)
    with pytest.raises(asyncpg.CheckViolationError):
        await conn.execute("UPDATE users SET balance = balance - 11 WHERE user_id = 2")


# ---------------------------------------------------------------- delivery
async def test_all_19_items_deliver(conn):
    from bots.main_bot.catalog import CATALOG
    from shared.economy import permanent_expiry, utcnow
    await _mk_user(conn, 3, 0)
    await conn.execute("INSERT INTO teams (team_name, captain_id) VALUES ('t', 3)")
    # Условия апгрейда Стажёра: сам Стажёр + 3 квалифицированных друга
    now = utcnow()
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES (3, 'intern', $1, $2)",
        now, permanent_expiry(now))
    for uid in (31, 32, 33):
        await _mk_user(conn, uid, 0, referred_by=3, qualified_at=now)
    capacity = 1
    for sku in CATALOG:
        order = build_order(sku, current_capacity=capacity)
        async with conn.transaction():
            await deliver_order(conn, 3, order, f"charge_{sku}")
        if order["type"] == "fridge_upgrade":
            capacity = order["capacity"]
    u = await conn.fetchrow("SELECT * FROM users WHERE user_id = 3")
    assert u["balance"] == 165_000
    assert u["inv_cutlets"] == 160
    assert u["fridge_capacity"] == 100
    kinds = [r["kind"] for r in await conn.fetch(
        "SELECT kind FROM miners WHERE user_id = 3 ORDER BY kind")]
    assert kinds == ["junior", "junior", "premium"]   # Стажёр стал вечным Майнером
    expiry = await conn.fetchval("SELECT MIN(expires_at - purchased_at) FROM miners WHERE user_id = 3")
    assert expiry.days == 30
    assert u["boost_nuclear_until"] and u["boost_nitrogen_until"] and u["drone_until"] and u["unlimit_until"]
    assert await conn.fetchval("SELECT max_members FROM teams WHERE captain_id = 3") == 1000
    assert await conn.fetchval("SELECT COUNT(*) FROM star_payments WHERE user_id = 3") == 19


async def test_delivery_is_idempotent_per_charge_id(conn):
    await _mk_user(conn, 4, 0)
    order = build_order("coins_5k")
    charge = str(uuid.uuid4())
    async with conn.transaction():
        await deliver_order(conn, 4, order, charge)
    assert await already_delivered(conn, charge)
    with pytest.raises(asyncpg.UniqueViolationError):
        async with conn.transaction():
            await deliver_order(conn, 4, order, charge)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 4") == 5000


async def test_clan_upgrade_without_team_raises_and_rolls_back(conn):
    await _mk_user(conn, 5, 0)
    with pytest.raises(DeliveryError):
        async with conn.transaction():
            await deliver_order(conn, 5, build_order("clan_upgrade"), "c5")
    assert await conn.fetchval("SELECT COUNT(*) FROM star_payments") == 0


async def test_unlimit_stacks(conn):
    await _mk_user(conn, 6, 0)
    async with conn.transaction():
        await deliver_order(conn, 6, build_order("unlimit_24h"), "u1")
    first = await conn.fetchval("SELECT unlimit_until FROM users WHERE user_id = 6")
    async with conn.transaction():
        await deliver_order(conn, 6, build_order("unlimit_30d"), "u2")
    second = await conn.fetchval("SELECT unlimit_until FROM users WHERE user_id = 6")
    assert (second - first).days == 30


# ---------------------------------------------------------------- registration
async def test_register_user_remembers_referrer_but_pays_nothing(conn):
    """С 26.10 за регистрацию друга не платится ничего — бонус только за АКТИВНОГО друга."""
    from bots.main_bot.handlers.start import register_user
    await _mk_user(conn, 10, 0)
    assert await register_user(conn, 11, "new", "en", referrer_id=10) is True
    assert await register_user(conn, 11, "new", "en", referrer_id=10) is False
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 10") == 0
    assert await conn.fetchval("SELECT COUNT(*) FROM ledger WHERE user_id = 10") == 0
    u = await conn.fetchrow("SELECT balance, inv_cutlets, lang, referred_by FROM users WHERE user_id = 11")
    assert (u["balance"], u["inv_cutlets"], u["lang"], u["referred_by"]) == (START_BALANCE, 1, "en", 10)


async def test_register_user_ignores_unknown_referrer(conn):
    from bots.main_bot.handlers.start import register_user
    await register_user(conn, 12, "x", "ru", referrer_id=999_999)
    assert await conn.fetchval("SELECT referred_by FROM users WHERE user_id = 12") is None


# ---------------------------------------------------------------- ферма (Блок 2)
async def test_lazy_farm_credits_mining_via_ledger_and_burns_fuel(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.farm_logic import apply_lazy_farm

    now = utcnow()
    await _mk_user(conn, 20, 0, fridge_cutlets=1)
    await conn.execute("UPDATE users SET last_update_time = $1 WHERE user_id = 20",
                       now - timedelta(hours=48))
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES "
        "(20, 'junior', $1, $2), (20, 'premium', $1, $2)",
        now - timedelta(hours=48), now + timedelta(days=29))

    async with conn.transaction():
        user, miners = await apply_lazy_farm(conn, 20, now)

    # junior: 48ч*5 = 240; premium: 1 котлета = ровно 24ч*10 = 240
    assert user["balance"] == 480
    assert user["fridge_cutlets"] == 0
    assert len(miners) == 2
    row = await conn.fetchrow("SELECT delta, reason FROM ledger WHERE user_id = 20")
    assert (row["delta"], row["reason"]) == (480, "mining")


async def test_lazy_farm_deletes_expired_miners(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.farm_logic import apply_lazy_farm

    now = utcnow()
    await _mk_user(conn, 21, 0)
    await conn.execute("UPDATE users SET last_update_time = $1 WHERE user_id = 21",
                       now - timedelta(hours=10))
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES (21, 'junior', $1, $2)",
        now - timedelta(days=30, hours=10), now - timedelta(hours=5))

    async with conn.transaction():
        user, miners = await apply_lazy_farm(conn, 21, now)

    assert user["balance"] == 25  # доработал 5 часов до сгорания
    assert miners == []
    assert await conn.fetchval("SELECT COUNT(*) FROM miners WHERE user_id = 21") == 0


# ---------------------------------------------------------------- игры (Блок 3)
@pytest.fixture
async def global_db():
    """Подключает глобальный db (его использует execute_solo_game_payout)."""
    from shared.database import db as gdb
    await gdb.connect(TEST_DSN)
    yield gdb
    await gdb.close()


async def test_quiz_level_1_closes_after_10_answers_and_resets_progress(conn, global_db):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.games import execute_solo_game_payout
    await _mk_user(conn, 30, 100)
    await conn.execute(
        "INSERT INTO game_stats (user_id, quiz_correct_total, quiz_level_progress) VALUES (30, 9, 9)")

    ok, text, balance = await execute_solo_game_payout(30, True, "quiz")

    assert ok and balance == 100 + 2 + 100  # победа +2 и награда уровня 1 (+100)
    stats = await conn.fetchrow(
        "SELECT quiz_correct_total, quiz_level, quiz_level_progress FROM game_stats WHERE user_id = 30")
    assert (stats["quiz_correct_total"], stats["quiz_level"], stats["quiz_level_progress"]) == (10, 1, 0)
    reasons = {r["reason"]: r["delta"] for r in await conn.fetch("SELECT reason, delta FROM ledger WHERE user_id = 30")}
    assert reasons == {"game_win:quiz": 2, "quiz_level_up": 100}


async def test_quiz_level_2_requires_20_fresh_answers(conn, global_db):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.games import execute_solo_game_payout
    await _mk_user(conn, 34, 0)
    # Уровень 1 уже закрыт, в текущей итерации 18 из 20 верных
    await conn.execute(
        "INSERT INTO game_stats (user_id, quiz_level, quiz_level_progress) VALUES (34, 1, 18)")

    ok, _, balance = await execute_solo_game_payout(34, True, "quiz")   # 19/20 — уровня нет
    assert ok and balance == 2
    assert await conn.fetchval("SELECT quiz_level FROM game_stats WHERE user_id = 34") == 1

    ok, _, balance = await execute_solo_game_payout(34, True, "quiz")   # 20/20 — уровень 2, +200
    assert ok and balance == 2 + 2 + 200
    stats = await conn.fetchrow("SELECT quiz_level, quiz_level_progress FROM game_stats WHERE user_id = 34")
    assert (stats["quiz_level"], stats["quiz_level_progress"]) == (2, 0)


async def test_safe_win_pays_increased_reward(conn, global_db):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.games import execute_solo_game_payout
    from shared.economy import SAFE_WIN_REWARD
    await _mk_user(conn, 31, 0)

    ok, text, balance = await execute_solo_game_payout(31, True, "safe")

    assert ok and balance == SAFE_WIN_REWARD
    assert await conn.fetchval("SELECT daily_wins_safe FROM game_stats WHERE user_id = 31") == 1


async def test_new_day_resets_all_win_counters(conn, global_db):
    pytest.importorskip("aiogram")
    from datetime import timedelta
    from bots.main_bot.handlers.games import execute_solo_game_payout
    from shared.economy import utcnow
    await _mk_user(conn, 32, 0)
    await conn.execute(
        "INSERT INTO game_stats (user_id, daily_wins_rps, daily_wins_hl, daily_wins_quiz, "
        "daily_wins_safe, last_game_date) "
        "VALUES (32, 15, 15, 30, 15, $1)", utcnow().date() - timedelta(days=1))

    ok, text, balance = await execute_solo_game_payout(32, True, "safe")  # вчерашний лимит не мешает

    assert ok and balance == 5
    stats = await conn.fetchrow("SELECT * FROM game_stats WHERE user_id = 32")
    assert stats["daily_wins_safe"] == 1
    for col in ("daily_wins_rps", "daily_wins_hl", "daily_wins_quiz"):
        assert stats[col] == 0, col


async def test_daily_limit_blocks_win_for_new_games(conn, global_db):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.games import execute_solo_game_payout
    from shared.economy import utcnow
    await _mk_user(conn, 33, 0)
    await conn.execute(
        "INSERT INTO game_stats (user_id, daily_wins_safe, last_game_date) VALUES (33, 15, $1)", utcnow().date())

    ok, text, balance = await execute_solo_game_payout(33, True, "safe")

    assert not ok and "лимит" in text.lower()
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 33") == 0


# ---------------------------------------------------------------- Блок 4: команды, переводы, админ
async def test_team_create_and_join_set_team_joined_at(conn, global_db):
    pytest.importorskip("aiogram")
    from shared.db_clans import create_new_team_in_db
    await _mk_user(conn, 40, 200_000)
    await _mk_user(conn, 41, 0)

    ok, _ = await create_new_team_in_db(40, "Тест-Банда", "девиз", "🔥")
    assert ok
    assert await conn.fetchval("SELECT team_joined_at FROM users WHERE user_id = 40") is not None
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 40") == 100_000


async def test_captain_succession_goes_to_earliest_joined(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    now = utcnow()
    await conn.execute("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('t', 50, 3)")
    team_id = await conn.fetchval("SELECT team_id FROM teams WHERE captain_id = 50")
    # Капитан 50; ветеран 51 вступил раньше, новичок 52 — позже, но заходил в бота позже всех
    await _mk_user(conn, 50, 0, team_id=team_id)
    await _mk_user(conn, 51, 0, team_id=team_id)
    await _mk_user(conn, 52, 0, team_id=team_id)
    await conn.execute("UPDATE users SET team_joined_at = $1 WHERE user_id = 51", now - timedelta(days=10))
    await conn.execute("UPDATE users SET team_joined_at = $1, last_seen_at = $2 WHERE user_id = 52",
                       now - timedelta(days=1), now)

    # Запрос наследования — тот же, что в обработчике выхода капитана
    next_captain = await conn.fetchval(
        "SELECT user_id FROM users WHERE team_id = $1 AND user_id != $2 "
        "ORDER BY team_joined_at ASC NULLS LAST, user_id ASC LIMIT 1", team_id, 50)
    assert next_captain == 51  # старшинство вступления, а не активность


async def _make_active(conn, user_id: int):
    """Активный аккаунт: 3 уровень интеллекта + 3 ежедневные котлеты (право отправлять монеты)."""
    await conn.execute("UPDATE users SET bonus_claims = 3 WHERE user_id = $1", user_id)
    await conn.execute(
        "INSERT INTO game_stats (user_id, quiz_level) VALUES ($1, 3) "
        "ON CONFLICT (user_id) DO UPDATE SET quiz_level = 3", user_id)


async def test_transfer_moves_coins_and_writes_ledger(conn):
    from shared.transfers import transfer_coins
    await _mk_user(conn, 60, 1000)
    await _make_active(conn, 60)
    await _mk_user(conn, 61, 0)

    async with conn.transaction():
        received, sender_balance = await transfer_coins(conn, 60, 61, 300)

    assert (received, sender_balance) == (300, 700)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 61") == 300
    rows = await conn.fetch("SELECT user_id, delta, reason, ref FROM ledger ORDER BY id")
    assert [(r["user_id"], r["delta"], r["reason"], r["ref"]) for r in rows] == [
        (60, -300, "transfer_out", "61"), (61, 300, "transfer_in", "60")]


async def test_transfer_rejects_bad_cases(conn):
    from shared.transfers import TransferError, transfer_coins
    await _mk_user(conn, 62, 100)
    await _make_active(conn, 62)
    await _mk_user(conn, 63, 0, is_blocked=True)

    for sender, recipient, amount in [(62, 62, 50), (62, 999, 50), (62, 63, 50), (62, 63, 5)]:
        with pytest.raises(TransferError):
            async with conn.transaction():
                await transfer_coins(conn, sender, recipient, amount)
    # Нехватка баланса
    await _mk_user(conn, 64, 0)
    with pytest.raises(TransferError):
        async with conn.transaction():
            await transfer_coins(conn, 62, 64, 500)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 62") == 100


async def test_admin_block_gift_and_report(conn):
    from shared.db_admin import admin_gift_coins, collect_daily_report, set_user_blocked
    await _mk_user(conn, 70, 50)

    assert await set_user_blocked(conn, 70, True) is True
    assert await conn.fetchval("SELECT is_blocked FROM users WHERE user_id = 70") is True
    assert await set_user_blocked(conn, 999_999, True) is False

    async with conn.transaction():
        assert await admin_gift_coins(conn, 70, 1000, admin_id=1) == 1050
    row = await conn.fetchrow("SELECT delta, reason, ref FROM ledger WHERE user_id = 70")
    assert (row["delta"], row["reason"], row["ref"]) == (1000, "admin_gift", "1")

    report = await collect_daily_report(conn)
    assert report["total_users"] == 1
    assert report["blocked_users"] == 1
    assert report["dau"] == 1  # last_seen_at по умолчанию = сейчас
    assert report["cohort_f2p"] == 1
    assert report["coins_mass"] == 1050


# ---------------------------------------------------------------- дуэли
async def test_duel_full_cycle_with_burn(conn):
    from shared.duels import join_or_create_duel, record_move
    await _mk_user(conn, 90, 100)
    await _mk_user(conn, 91, 100)

    async with conn.transaction():
        r1 = await join_or_create_duel(conn, 90, 100)
    assert not r1.matched
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 90") == 0  # эскроу

    async with conn.transaction():
        r2 = await join_or_create_duel(conn, 91, 100)
    assert r2.matched and r2.opponent_id == 90 and r2.duel_id == r1.duel_id

    async with conn.transaction():
        m1 = await record_move(conn, r1.duel_id, 90, "rock")
    assert m1.waiting_opponent
    async with conn.transaction():
        m2 = await record_move(conn, r1.duel_id, 91, "scissors")

    assert m2.finished and m2.winner_id == 90 and m2.loser_id == 91
    assert (m2.payout, m2.burned) == (160, 40)  # сжигание 20% банка
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 90") == 160
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 91") == 0
    reasons = [r["reason"] for r in await conn.fetch("SELECT reason FROM ledger ORDER BY id")]
    assert reasons == ["duel_stake", "duel_stake", "duel_win"]
    # 40 монет исчезли из оборота навсегда
    assert await conn.fetchval("SELECT SUM(delta) FROM ledger") == -40


async def test_duel_draw_replays_and_guards(conn):
    from shared.duels import DuelError, join_or_create_duel, record_move
    await _mk_user(conn, 92, 50)
    await _mk_user(conn, 93, 50)
    async with conn.transaction():
        r1 = await join_or_create_duel(conn, 92, 10)
        r2 = await join_or_create_duel(conn, 93, 10)
    duel_id = r2.duel_id

    # Нельзя сесть за второй стол, пока дуэль активна
    with pytest.raises(DuelError):
        async with conn.transaction():
            await join_or_create_duel(conn, 92, 10)

    async with conn.transaction():
        await record_move(conn, duel_id, 92, "rock")
        result = await record_move(conn, duel_id, 93, "rock")
    assert result.draw_replay and result.rounds == 2  # ничья → переигровка, банк на столе

    duel = await conn.fetchrow("SELECT * FROM duels WHERE duel_id = $1", duel_id)
    assert duel["move1"] is None and duel["move2"] is None and duel["status"] == "active"

    async with conn.transaction():
        await record_move(conn, duel_id, 92, "paper")
        result = await record_move(conn, duel_id, 93, "scissors")
    assert result.finished and result.winner_id == 93


async def test_duel_cancel_and_expire_refund(conn):
    from shared.duels import cancel_waiting_duel, expire_waiting_duels, join_or_create_duel
    await _mk_user(conn, 94, 1000)
    async with conn.transaction():
        r = await join_or_create_duel(conn, 94, 1000)
        assert await cancel_waiting_duel(conn, r.duel_id, 94) == 1000
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 94") == 1000

    # Протухшая очередь возвращается жнецом
    async with conn.transaction():
        r2 = await join_or_create_duel(conn, 94, 10)
    await conn.execute("UPDATE duels SET created_at = NOW() - INTERVAL '2 hours' WHERE duel_id = $1",
                       r2.duel_id)
    async with conn.transaction():
        expired = await expire_waiting_duels(conn, 30)
    assert expired == [(r2.duel_id, 94, 10)]
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 94") == 1000


async def test_duel_stuck_round_resolved_by_reaper(conn):
    from shared.duels import find_stuck_active_duels, join_or_create_duel, record_move, resolve_stuck_duel
    await _mk_user(conn, 95, 20)
    await _mk_user(conn, 96, 20)
    async with conn.transaction():
        await join_or_create_duel(conn, 95, 10)
        r = await join_or_create_duel(conn, 96, 10)
        await record_move(conn, r.duel_id, 95, "rock")  # второй игрок молчит
    await conn.execute("UPDATE duels SET round_started_at = NOW() - INTERVAL '5 minutes' "
                       "WHERE duel_id = $1", r.duel_id)

    async with conn.transaction():
        stuck = await find_stuck_active_duels(conn, 60)
        assert len(stuck) == 1
        result = await resolve_stuck_duel(conn, stuck[0])
    assert result.finished and result.winner_id in (95, 96)
    total = sum(r["delta"] for r in await conn.fetch("SELECT delta FROM ledger"))
    assert total == -4  # сжигание 20% банка (20) при любом исходе


# ---------------------------------------------------------------- битвы команд
async def test_battle_team_scores_counts_only_window_and_teams(conn):
    from datetime import timedelta
    from shared.battles import battle_team_scores
    from shared.economy import utcnow
    now = utcnow()
    await conn.execute("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Alpha', 100, 2)")
    await conn.execute("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Beta', 102, 1)")
    alpha = await conn.fetchval("SELECT team_id FROM teams WHERE team_name = 'Alpha'")
    beta = await conn.fetchval("SELECT team_id FROM teams WHERE team_name = 'Beta'")
    await _mk_user(conn, 100, 0, team_id=alpha)
    await _mk_user(conn, 101, 0, team_id=alpha)
    await _mk_user(conn, 102, 0, team_id=beta)
    await _mk_user(conn, 103, 0)  # без команды — не в зачёте

    async def mined(user_id, delta, when):
        await conn.execute(
            "INSERT INTO ledger (user_id, delta, reason, created_at) VALUES ($1, $2, 'mining', $3)",
            user_id, delta, when)

    starts, ends = now - timedelta(days=7), now
    await mined(100, 300, now - timedelta(days=1))
    await mined(101, 200, now - timedelta(days=2))   # Alpha суммарно 500
    await mined(102, 400, now - timedelta(days=3))   # Beta 400
    await mined(103, 900, now - timedelta(days=1))   # без команды — мимо
    await mined(100, 999, now - timedelta(days=30))  # вне окна — мимо

    scores = await battle_team_scores(conn, "farm_mined", starts, ends)
    assert [(s["team_name"], s["score"]) for s in scores] == [("Alpha", 500), ("Beta", 400)]


async def test_transfer_by_vip_alias(conn):
    from shared.transfers import transfer_coins
    await _mk_user(conn, 120, 500)
    await _make_active(conn, 120)
    await _mk_user(conn, 121, 0)
    await conn.execute("INSERT INTO vip_aliases (alias, user_id) VALUES ('ROFL-HUB-777', 121)")

    # Резолв алиаса — как в обработчике /transfer (регистронезависимый)
    recipient = await conn.fetchrow(
        "SELECT u.user_id FROM vip_aliases v JOIN users u ON u.user_id = v.user_id "
        "WHERE UPPER(v.alias) = UPPER($1)", "rofl-hub-777")
    assert recipient["user_id"] == 121

    async with conn.transaction():
        received, _ = await transfer_coins(conn, 120, recipient["user_id"], 100)
    assert received == 100
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 121") == 100


# ---------------------------------------------------------------- квесты
async def test_quest_reward_only_for_first_win(conn):
    from shared.ledger import change_balance
    await _mk_user(conn, 140, 0)
    # Имитация движка: первая победа — награда + completed_at
    await conn.execute(
        "INSERT INTO quest_progress (user_id, quest_id, scene, flags) "
        "VALUES (140, 'golden_cutlet', 'end_win', '[]'::jsonb)")
    completed = await conn.fetchval(
        "SELECT completed_at FROM quest_progress WHERE user_id = 140 AND quest_id = 'golden_cutlet'")
    assert completed is None
    async with conn.transaction():
        await change_balance(conn, 140, 150, "quest_reward", "golden_cutlet")
        await conn.execute(
            "UPDATE quest_progress SET completed_at = NOW() WHERE user_id = 140 AND quest_id = 'golden_cutlet'")
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 140") == 150
    row = await conn.fetchrow(
        "SELECT reason, ref FROM ledger WHERE user_id = 140 AND reason = 'quest_reward'")
    assert row["ref"] == "golden_cutlet"
    # Повторная победа: completed_at уже стоит — движок награду не выдаёт
    completed = await conn.fetchval(
        "SELECT completed_at FROM quest_progress WHERE user_id = 140 AND quest_id = 'golden_cutlet'")
    assert completed is not None


async def test_quest_progress_upsert_resets_scene_but_keeps_completion(conn):
    await _mk_user(conn, 141, 0)
    await conn.execute(
        "INSERT INTO quest_progress (user_id, quest_id, scene, flags, completed_at) "
        "VALUES (141, 'locked_safe', 'end_win', '[\"digit_a\"]'::jsonb, NOW())")
    # Рестарт квеста (как quest_start): сцена и флаги сбрасываются, completed_at живёт
    await conn.execute(
        """
        INSERT INTO quest_progress (user_id, quest_id, scene, flags, updated_at)
        VALUES (141, 'locked_safe', 'intro', '[]'::jsonb, NOW())
        ON CONFLICT (user_id, quest_id)
        DO UPDATE SET scene = 'intro', flags = '[]'::jsonb, updated_at = NOW()
        """)
    row = await conn.fetchrow(
        "SELECT scene, flags, completed_at FROM quest_progress WHERE user_id = 141")
    assert row["scene"] == "intro"
    assert row["completed_at"] is not None  # отметка первой победы не теряется


# ---------------------------------------------------------------- Блок 5: бэкап и возвраты
async def test_backup_dumps_all_tables_to_valid_json(conn):
    import json
    from shared.db_admin import BACKUP_TABLES, backup_to_json_bytes, dump_database
    await _mk_user(conn, 80, 500)
    await conn.execute(
        "INSERT INTO miners (user_id, kind, expires_at) VALUES (80, 'junior', NOW() + INTERVAL '30 days')")
    await conn.execute(
        "INSERT INTO star_payments (user_id, telegram_charge_id, item_payload, stars_amount) "
        "VALUES (80, 'ch_backup', 'cutlet_10', 49)")

    dump = await dump_database(conn)
    restored = json.loads(backup_to_json_bytes(dump).decode("utf-8"))

    assert set(restored["tables"]) == set(BACKUP_TABLES)
    assert restored["tables"]["users"][0]["user_id"] == 80
    assert restored["tables"]["miners"][0]["kind"] == "junior"
    # даты сериализованы строками ISO, а не упали в json.dumps
    assert "T" in restored["tables"]["users"][0]["created_at"]


async def test_refund_marking_is_single_shot(conn):
    from shared.db_admin import find_payment, mark_refunded
    await _mk_user(conn, 81, 0)
    await conn.execute(
        "INSERT INTO star_payments (user_id, telegram_charge_id, item_payload, stars_amount) "
        "VALUES (81, 'ch_refund', 'unlimit_24h', 5)")

    payment = await find_payment(conn, "ch_refund")
    assert payment["refunded_at"] is None
    assert await mark_refunded(conn, "ch_refund") is True
    assert await mark_refunded(conn, "ch_refund") is False  # повторный возврат невозможен
    assert await mark_refunded(conn, "no_such_charge") is False
    assert (await find_payment(conn, "ch_refund"))["refunded_at"] is not None


async def test_counter_migration_moves_robots_to_miners_table_once(conn):
    database = Database()
    await database.connect(TEST_DSN)
    try:
        await _mk_user(conn, 22, 0, miner_junior_count=2, miner_premium_count=1)
        await database.create_tables()
        await database.create_tables()  # повторный запуск не дублирует роботов
        rows = await conn.fetch("SELECT kind FROM miners WHERE user_id = 22 ORDER BY kind")
        assert [r["kind"] for r in rows] == ["junior", "junior", "premium"]
        u = await conn.fetchrow("SELECT miner_junior_count, miner_premium_count FROM users WHERE user_id = 22")
        assert (u["miner_junior_count"], u["miner_premium_count"]) == (0, 0)
    finally:
        await database.close()


# ============================================================================
# Продуктовая аналитика: квалификация рефералов, события, метрики
# ============================================================================
async def test_referral_qualification_pays_exactly_once_under_race():
    """Две конкурентные транзакции видят выполненное условие активного друга — бонус строго один."""
    import asyncio
    from shared.analytics import qualify_referral_if_due
    from shared.economy import REFERRAL_QUALIFIED_BONUS

    database = Database()
    await database.connect(TEST_DSN)
    await database.create_tables()
    try:
        async with database.pool.acquire() as c:
            await c.execute("TRUNCATE users, ledger, events, daily_activity, game_stats RESTART IDENTITY")
            await _mk_user(c, 100, 0)
            await _mk_user(c, 101, 0, referred_by=100, bonus_claims=3)
            await c.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (101, 3)")

        async def attempt():
            async with database.pool.acquire() as c:
                async with c.transaction():
                    return await qualify_referral_if_due(c, 101)

        results = await asyncio.gather(attempt(), attempt())
        assert sorted(r is not None for r in results) == [False, True]

        async with database.pool.acquire() as c:
            rows = await c.fetch(
                "SELECT delta, reason FROM ledger WHERE user_id = 100 ORDER BY id")
            assert [(r["delta"], r["reason"]) for r in rows] == \
                   [(REFERRAL_QUALIFIED_BONUS, "referral_qualified")]
            assert await c.fetchval("SELECT balance FROM users WHERE user_id = 100") == \
                   REFERRAL_QUALIFIED_BONUS
            assert await c.fetchval("SELECT qualified_at FROM users WHERE user_id = 101") is not None
    finally:
        await database.close()


async def test_referral_qualification_needs_both_conditions_and_live_accounts(conn):
    """Активный друг = 3 уровень интеллекта И 3 ежедневные котлеты; блокировки отсекают фейки."""
    from shared.analytics import qualify_referral_if_due

    await _mk_user(conn, 110, 0)
    await _mk_user(conn, 111, 0, referred_by=110, bonus_claims=2)      # котлет мало
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (111, 3)")
    assert await qualify_referral_if_due(conn, 111) is None
    await _mk_user(conn, 112, 0, referred_by=110, bonus_claims=3)      # интеллекта мало
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (112, 2)")
    assert await qualify_referral_if_due(conn, 112) is None
    await _mk_user(conn, 113, 0, bonus_claims=9)                       # пришёл сам
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (113, 9)")
    assert await qualify_referral_if_due(conn, 113) is None
    await _mk_user(conn, 114, 0, referred_by=110, bonus_claims=3, is_blocked=True)   # забанен
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (114, 3)")
    assert await qualify_referral_if_due(conn, 114) is None
    assert await conn.fetchval(
        "SELECT COUNT(*) FROM ledger WHERE reason = 'referral_qualified'") == 0

    # Заблокированный пригласитель: друг засчитан активным, но бонус не начислен
    await _mk_user(conn, 115, 0, is_blocked=True)
    await _mk_user(conn, 116, 0, referred_by=115, bonus_claims=3)
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (116, 3)")
    assert await qualify_referral_if_due(conn, 116) is None
    assert await conn.fetchval("SELECT qualified_at FROM users WHERE user_id = 116") is not None
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 115") == 0


async def test_track_and_daily_activity_write_rows():
    """track() пишет событие, mark_daily_activity() не плодит дублей за день."""
    from shared import analytics
    from shared.database import db as global_db

    await global_db.connect(TEST_DSN)
    try:
        await global_db.create_tables()
        async with global_db.pool.acquire() as c:
            await c.execute("TRUNCATE users, events, daily_activity RESTART IDENTITY")
            await _mk_user(c, 120, 0)
        analytics._daily_marked.clear()
        await analytics.track(120, "game_round", game="rps", result="win")
        await analytics.mark_daily_activity(120)
        await analytics.mark_daily_activity(120)
        async with global_db.pool.acquire() as c:
            ev = await c.fetchrow("SELECT event, props->>'game' AS game FROM events")
            assert (ev["event"], ev["game"]) == ("game_round", "rps")
            assert await c.fetchval(
                "SELECT COUNT(*) FROM daily_activity WHERE user_id = 120") == 1
    finally:
        await global_db.close()


async def test_metrics_match_hand_computed_values(conn):
    """Фикстурные данные → метрики сверяются с посчитанными вручную числами."""
    from datetime import timedelta
    from shared import metrics
    from shared.economy import utcnow

    now = utcnow()

    def d(days):
        return now - timedelta(days=days)

    # Игроки: A — органика 10 дней назад; B и C — рефералы A (B квалифицирован)
    await _mk_user(conn, 200, 0, created_at=d(10), source="organic")
    await _mk_user(conn, 201, 0, created_at=d(5), source="referral",
                   referred_by=200, qualified_at=d(1))
    await _mk_user(conn, 202, 0, created_at=d(4), source="p_blog", referred_by=200)

    # Активность: A вчера и сегодня, B сегодня
    await conn.execute(
        "INSERT INTO daily_activity (user_id, day) VALUES "
        "(200, $1), (200, $2), (201, $2)", d(1).date(), now.date())

    # Платежи: B купил безлимит сегодня (5 звёзд); A — пак 2 дня назад (149);
    # возврат и TEST-чек в выручку не попадают
    await conn.execute(
        """INSERT INTO star_payments (user_id, telegram_charge_id, item_payload,
                                      stars_amount, created_at, refunded_at) VALUES
           (201, 'ch1', 'unlimit_24h', 5, $1, NULL),
           (200, 'ch2', 'coins_5k', 149, $2, NULL),
           (200, 'ch3', 'coins_100k', 999, $1, $1),
           (201, 'TEST_ch4', 'coins_5k', 777, $1, NULL)""", d(0), d(2))

    # События: B упёрся в лимит (купил безлимит < 24 ч спустя), 3 раунда викторины
    await conn.execute(
        """INSERT INTO events (user_id, event, props, created_at) VALUES
           (201, 'daily_limit_hit', '{"game": "quiz"}', $1),
           (200, 'game_round', '{"game": "quiz", "result": "win"}', $1),
           (201, 'game_round', '{"game": "quiz", "result": "win"}', $1),
           (201, 'game_round', '{"game": "quiz", "result": "lose"}', $2)""",
        now - timedelta(hours=20), now - timedelta(hours=2))

    # Монеты: эмиссия +100 (ферма), сжигание -30 (проигрыши)
    await conn.execute(
        """INSERT INTO ledger (user_id, delta, reason, created_at) VALUES
           (200, 100, 'mining', $1), (201, -30, 'game_loss:quiz', $1)""", d(1))
    await conn.execute("UPDATE users SET balance = 70 WHERE user_id = 200")

    activity = await metrics.fetch_activity(conn, now.date())
    assert (activity["dau"], activity["wau"], activity["mau"]) == (2, 2, 2)
    assert activity["stickiness_pct"] == 100.0

    vir = await metrics.fetch_virality(conn, d(11), now)
    assert vir["cohort_size"] == 3
    assert vir["k_raw"] == round(2 / 3, 3)
    assert vir["k_qualified"] == round(1 / 3, 3)
    assert vir["inviter_share_pct"] == 33.3

    mon = await metrics.fetch_monetization(conn, d(1), now + timedelta(seconds=1))
    assert mon["revenue_stars"] == 5 and mon["payers"] == 1
    assert mon["by_sku"] == [{"sku": "unlimit_24h", "n": 1, "stars": 5}]
    assert mon["cr_base_pct"] == round(100 / 3, 2)
    assert mon["limit_hit_users"] == 1 and mon["limit_to_unlimit_pct"] == 100.0
    assert mon["repeat_buyers_pct"] == 0.0     # у каждого платящего по одной покупке

    eco = await metrics.fetch_coin_economy(conn, d(2), now)
    assert (eco["emission"], eco["burn"], eco["net_inflation"]) == (100, 30, 70)
    assert eco["coin_supply"] == 70

    gf = await metrics.fetch_games_farm(conn, d(1), now)
    assert gf["games"] == [{"game": "quiz", "rounds": 3, "winrate_pct": 66.7}]
    assert gf["limit_hits"] == [{"game": "quiz", "n": 1}]

    funnel = await metrics.fetch_activation_funnel(conn, d(11), now)
    assert funnel["registered"] == 3
    assert funnel["played"] == 0       # первые игры были позже 24 ч от регистрации

    retention = await metrics.fetch_retention_cohorts(conn, last_n=7)
    cohort_b = next(c for c in retention if c["cohort"] == d(5).date().isoformat())
    assert cohort_b["size"] == 1 and cohort_b["d1_pct"] == 0.0


async def test_feature_flags_set_toggle_and_cache():
    """Тумблер переключается, значение переживает сброс кэша (живёт в БД)."""
    from shared import feature_flags as ff
    from shared.database import db as global_db

    await global_db.connect(TEST_DSN)
    try:
        await global_db.create_tables()
        async with global_db.pool.acquire() as c:
            await c.execute("TRUNCATE feature_flags")
        ff.invalidate_cache()

        assert await ff.get_flag("games") is True          # дефолт
        await ff.set_flag("games", False)
        assert await ff.get_flag("games") is False
        ff.invalidate_cache()
        assert await ff.get_flag("games") is False         # прочитано из БД, не из кэша

        assert await ff.toggle_flag("quest:golden_cutlet") is False   # был виден → скрыт
        assert await ff.get_flag("quest:golden_cutlet") is False
        assert await ff.toggle_flag("quest:golden_cutlet") is True

        await ff.set_flag("games", True)                   # вернуть как было
    finally:
        ff.invalidate_cache()
        await global_db.close()


async def test_intern_upgrade_requires_three_qualified_referrals(conn):
    """Апгрейд Стажёра: без 3 квалифицированных друзей — отказ; с ними — вечный Майнер."""
    from datetime import timedelta
    from shared.economy import permanent_expiry, utcnow
    now = utcnow()
    await _mk_user(conn, 300, 0)
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES (300, 'intern', $1, $2)",
        now, permanent_expiry(now))
    order = build_order("intern_upgrade")
    for i in range(2):   # два квалифицированных — мало
        await _mk_user(conn, 301 + i, 0, referred_by=300, qualified_at=now)
    with pytest.raises(DeliveryError):
        async with conn.transaction():
            await deliver_order(conn, 300, order, "charge_up_fail")
    await _mk_user(conn, 303, 0, referred_by=300, qualified_at=now)   # третий — достаточно
    await _mk_user(conn, 304, 0, referred_by=300)                      # незавершённый не считается
    async with conn.transaction():
        text = await deliver_order(conn, 300, order, "charge_up_ok")
    assert "ВЕЧНОГО" in text
    robot = await conn.fetchrow("SELECT kind, expires_at FROM miners WHERE user_id = 300")
    assert robot["kind"] == "junior"
    assert robot["expires_at"] > now + timedelta(days=365 * 50)
    assert await conn.fetchval("SELECT COUNT(*) FROM star_payments WHERE user_id = 300") == 1


async def test_new_intellect_level_gives_a_claimable_intern(conn, global_db):
    """Уровень, кратный 10, = Стажёр ждёт на ферме; на ферму попадает только по кнопке."""
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.farm import claim_pending_intern
    from bots.main_bot.handlers.games import execute_solo_game_payout
    from shared.economy import utcnow
    await _mk_user(conn, 310, 0)
    await conn.execute(
        "INSERT INTO game_stats (user_id, quiz_level, quiz_level_progress) VALUES (310, 1, 19)")
    ok, text, _ = await execute_solo_game_payout(310, True, "quiz")      # закрыт уровень 2
    assert ok and "Стажёр" not in text
    assert await conn.fetchval("SELECT interns_pending FROM users WHERE user_id = 310") == 0
    await conn.execute("UPDATE game_stats SET quiz_level = 9, quiz_level_progress = 99 WHERE user_id = 310")
    ok, text, _ = await execute_solo_game_payout(310, True, "quiz")      # закрыт уровень 10
    assert ok and "Стажёр" in text
    assert await conn.fetchval("SELECT interns_pending FROM users WHERE user_id = 310") == 1
    assert await conn.fetchval("SELECT COUNT(*) FROM miners WHERE user_id = 310") == 0   # сам не падает
    assert await claim_pending_intern(conn, 310, utcnow()) is True
    assert await claim_pending_intern(conn, 310, utcnow()) is False        # второго нет
    kinds = [r["kind"] for r in await conn.fetch("SELECT kind FROM miners WHERE user_id = 310")]
    assert kinds == ["intern"]
    assert await conn.fetchval("SELECT interns_pending FROM users WHERE user_id = 310") == 0


async def test_market_sell_buy_cancel_with_burned_fee(conn):
    """Эскроу котлет, покупка с комиссией (сгорает), частичная сделка, снятие ордера."""
    from shared.market import MarketError, buy_from_order, cancel_order, list_open_orders, place_sell_order
    await _mk_user(conn, 400, 0, inv_cutlets=20)      # продавец
    await _mk_user(conn, 401, 1500)                   # покупатель
    await conn.execute("TRUNCATE market_orders RESTART IDENTITY")

    order_id = await place_sell_order(conn, 400, 10, 250)  # 10 котлет по 250 (пол — 200)
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 400") == 10  # эскроу
    with pytest.raises(MarketError) as e:
        await place_sell_order(conn, 400, 11, 250)     # на складе осталось 10
    assert e.value.key == "mk.err_no_cutlets"
    with pytest.raises(MarketError) as e:
        await buy_from_order(conn, 400, order_id, 1)   # свой ордер
    assert e.value.key == "mk.err_own"

    deal = await buy_from_order(conn, 401, order_id, 4)    # 4 × 250 = 1000, комиссия 100
    assert {k: deal[k] for k in ("qty", "price", "total", "fee", "seller_id", "seller_got", "shuttle")} ==         {"qty": 4, "price": 250, "total": 1000, "fee": 100, "seller_id": 400, "seller_got": 900, "shuttle": False}
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 401") == 500
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 400") == 900
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 401") == 4
    burned = await conn.fetchval(
        "SELECT -SUM(delta) FROM ledger WHERE reason IN ('market_buy', 'market_sell')")
    assert burned == 100                                    # 1000 списано, 900 зачислено
    assert (await list_open_orders(conn))[0]["qty"] == 6

    # покупатель без монет
    await _mk_user(conn, 402, 10)
    with pytest.raises(MarketError) as e:
        await buy_from_order(conn, 402, order_id, 1)
    assert e.value.key == "mk.err_insufficient"

    qty_back = await cancel_order(conn, 400, order_id)
    assert qty_back == 6
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 400") == 16
    assert await conn.fetchval("SELECT status FROM market_orders WHERE id = $1", order_id) == "cancelled"
    with pytest.raises(MarketError):
        await cancel_order(conn, 400, order_id)             # второй раз — уже снят


async def test_purge_old_events_removes_only_stale_rows():
    from datetime import timedelta

    from shared import analytics
    from shared.database import db as global_db
    from shared.economy import utcnow

    await global_db.connect(TEST_DSN)
    try:
        await global_db.create_tables()
        async with global_db.pool.acquire() as c:
            await c.execute("TRUNCATE events RESTART IDENTITY")
            await c.execute(
                "INSERT INTO events (user_id, event, created_at) VALUES "
                "(1, 'old', $1), (1, 'fresh', $2)",
                utcnow() - timedelta(days=200), utcnow())
        deleted = await analytics.purge_old_events()
        assert deleted == 1
        async with global_db.pool.acquire() as c:
            assert await c.fetchval("SELECT event FROM events") == "fresh"
    finally:
        await global_db.close()


# ---------------------------------------------------------------- волна 22.10 (вечер): ресурсы и механики
async def test_game_win_mines_resource_and_ledger_blocks_negative(conn, global_db, monkeypatch):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers import games
    from bots.main_bot.handlers.games import execute_solo_game_payout
    monkeypatch.setattr(games.random, "randrange", lambda n: n - 1)      # ⚡ не выпало (шанс 25%)
    from shared.resources import InsufficientResources, change_resource, get_resources
    await _mk_user(conn, 500, 100)

    ok, text, _ = await execute_solo_game_payout(500, True, "safe")
    assert ok and "⚙️" in text
    stock = await get_resources(conn, 500)
    assert stock == {"metal": 0, "hydrogen": 0, "crystal": 0, "parts": 3}
    ok, _, _ = await execute_solo_game_payout(500, False, "rps")   # проигрыш — ресурса нет
    assert ok and (await get_resources(conn, 500))["metal"] == 0

    with pytest.raises(InsufficientResources):
        await change_resource(conn, 500, "parts", -4, "test")
    assert (await get_resources(conn, 500))["parts"] == 3
    rows = await conn.fetch("SELECT kind, delta, reason FROM resource_ledger WHERE user_id = 500")
    assert [(r["kind"], r["delta"], r["reason"]) for r in rows] == [("parts", 3, "game_win:safe")]
    monkeypatch.setattr(games.random, "randrange", lambda n: 0)          # ⚡ выпало
    ok, text, _ = await execute_solo_game_payout(500, True, "safe")
    assert ok and "⚡" in text
    assert (await get_resources(conn, 500, ("energy",)))["energy"] == 1


async def test_workshop_crafts_spend_all_or_nothing(conn):
    from datetime import timedelta
    from shared.economy import ARMOR_MAX_LEVEL, utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.workshop import WorkshopError, craft
    now = utcnow()
    await _mk_user(conn, 510, 0, created_at=utcnow() - timedelta(days=60))   # ветеран: все рецепты открыты
    await grant_bundle(conn, 510, {"metal": 20, "hydrogen": 19}, "test")

    with pytest.raises(WorkshopError) as e:
        await craft(conn, 510, "nitro_6h", now)             # водорода 19 из 20
    assert e.value.key == "ws.err_resources"
    assert (await get_resources(conn, 510))["metal"] == 20  # ничего не списано

    await grant_bundle(conn, 510, {"hydrogen": 1}, "test")
    result = await craft(conn, 510, "nitro_6h", now)
    assert result.until == now + timedelta(hours=6)
    assert (await get_resources(conn, 510)) == {"metal": 0, "hydrogen": 0, "crystal": 0, "parts": 0}
    assert await conn.fetchval("SELECT boost_nitrogen_until FROM users WHERE user_id = 510") == result.until

    # Броня (решение 24.10): уровни растут, каждый крафт даёт +30 дней; на максимуме — продление
    await grant_bundle(conn, 510, {k: 5000 for k in ("metal", "hydrogen", "crystal", "parts")}, "test")
    with pytest.raises(WorkshopError) as e:                  # броне нужен набор инструментов
        await craft(conn, 510, "armor", now)
    assert e.value.key == "tech.err_tool"
    await _tech(conn, 510, tools=4)
    for lvl in range(1, ARMOR_MAX_LEVEL + 1):
        assert (await craft(conn, 510, "armor", now)).level == lvl
    renewed = await craft(conn, 510, "armor", now)
    assert renewed.level == ARMOR_MAX_LEVEL
    assert renewed.until == now + timedelta(days=30 * (ARMOR_MAX_LEVEL + 1))
    # Шаттл стоит ещё и 1000 🪙: без монет — отказ без списания ресурсов
    metal_before = (await get_resources(conn, 510))["metal"]
    with pytest.raises(WorkshopError) as e:
        await craft(conn, 510, "shuttle", now)
    assert e.value.key == "ws.err_coins"
    assert (await get_resources(conn, 510))["metal"] == metal_before
    await conn.execute("UPDATE users SET balance = 1500 WHERE user_id = 510")
    await craft(conn, 510, "shuttle", now)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 510") == 500
    with pytest.raises(WorkshopError) as e:
        await craft(conn, 510, "shuttle", now)
    assert e.value.key == "ws.err_shuttle_owned"
    row = await conn.fetchrow("SELECT farm_armor_level, has_shuttle FROM users WHERE user_id = 510")
    assert (row["farm_armor_level"], row["has_shuttle"]) == (ARMOR_MAX_LEVEL, True)
    with pytest.raises(WorkshopError) as e:                  # котлеты — из коровы и огня (26.10: 🐄 + 2 🔥 → 3 🥩)
        await craft(conn, 510, "cutlet", now)
    assert e.value.key == "ws.err_resources"
    await grant_bundle(conn, 510, {"cow": 1, "fire": 2}, "test")
    assert (await craft(conn, 510, "cutlet", now)).qty == 3
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 510") == 3
    assert (await get_resources(conn, 510, ("cow", "fire"))) == {"cow": 0, "fire": 0}
    assert await conn.fetchval("SELECT shuttle_until FROM users WHERE user_id = 510") > now   # заряд 30 дней


async def test_armor_and_station_bonus_reach_the_farm_engine(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.farm_logic import apply_lazy_farm
    now = utcnow()
    await conn.execute("INSERT INTO teams (team_id, team_name, captain_id) VALUES (7, 'Bonus', 520)")
    await conn.execute("INSERT INTO team_stations (team_id, level) VALUES (7, 5)")
    await _mk_user(conn, 520, 0, team_id=7, farm_armor_level=3, armor_until=now + timedelta(days=5),
                   last_update_time=now - timedelta(hours=10))
    await conn.execute(
        "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES (520, 'junior', $1, $2)",
        now - timedelta(days=1), now + timedelta(days=29))
    user, _ = await apply_lazy_farm(conn, 520, now)
    assert user["balance"] == 70       # 10 ч × 5 монет × (1 + 30% брони + 10% станции)


async def test_raid_moves_only_resources_and_respects_rules(conn):
    from datetime import timedelta
    from shared.economy import RAID_FUEL_HYDROGEN, utcnow
    from shared.raids import RaidError, execute_raid, find_targets, revenge_options
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    old = now - timedelta(days=10)
    await _mk_user(conn, 600, 500, created_at=old, last_seen_at=now)              # атакующий
    await _mk_user(conn, 601, 500, created_at=old, last_seen_at=now, raid_stance="scissors")  # цель
    await _mk_user(conn, 602, 500, created_at=now)                                 # новичок
    await grant_bundle(conn, 600, {"hydrogen": 10, "metal": 100}, "test")
    await grant_bundle(conn, 601, {"metal": 100, "crystal": 5}, "test")
    await grant_bundle(conn, 602, {"metal": 100}, "test")
    with pytest.raises(RaidError) as e:                        # без ⚔️ нападения налётов нет
        await execute_raid(conn, 600, 601, "rock", now)
    assert e.value.key == "raid.err_need_tech"
    await _tech(conn, 600, comm=1, scout=1, attack=1)
    await conn.execute("UPDATE users SET meds_until = $2 WHERE user_id = $1", 600, now + timedelta(days=1))

    targets = await find_targets(conn, 600, None, now)
    assert [tg["user_id"] for tg in targets] == [601]          # новичок под защитой, сам — нет

    with pytest.raises(RaidError) as e:
        await execute_raid(conn, 600, 602, "rock", now)
    assert e.value.key == "raid.err_shielded"

    result = await execute_raid(conn, 600, 601, "rock", now)   # камень бьёт ножницы
    assert result.result == "win" and result.loot == {"metal": 20, "crystal": 1}
    assert (await get_resources(conn, 600))["hydrogen"] == 10 - RAID_FUEL_HYDROGEN
    assert (await get_resources(conn, 600))["metal"] == 120
    assert (await get_resources(conn, 601))["metal"] == 80
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 601") == 500   # монеты неприкосновенны

    with pytest.raises(RaidError) as e:                        # кулдаун атакующего
        await execute_raid(conn, 600, 601, "rock", now + timedelta(minutes=5))
    assert e.value.key == "raid.err_cooldown"

    # Реванш жертвы: бесплатно, без кулдауна; стойка атакующего не задана → случайная
    options = await revenge_options(conn, 601, now + timedelta(hours=1))
    assert [o["raid_id"] for o in options] == [result.raid_id]
    revenge = await execute_raid(conn, 601, 600, "paper", now + timedelta(hours=1), revenge_of=result.raid_id)
    assert revenge.is_revenge and revenge.result in ("win", "draw", "lose")
    fuel_rows = await conn.fetchval(
        "SELECT COUNT(*) FROM resource_ledger WHERE user_id = 601 AND reason = 'raid_fuel'")
    assert fuel_rows == 0                                                       # топливо не списано
    assert await revenge_options(conn, 601, now + timedelta(hours=2)) == []     # один реванш на налёт
    await conn.execute("UPDATE raids SET result = 'win' WHERE id = $1", revenge.raid_id)
    assert await revenge_options(conn, 600, now + timedelta(hours=2)) == []     # аудит 2.8: реванш на реванш не даётся
    with pytest.raises(RaidError):
        await execute_raid(conn, 601, 600, "paper", now + timedelta(hours=1), revenge_of=result.raid_id)


async def test_daily_goals_chest_once_per_day_with_streak(conn):
    from datetime import timedelta
    from shared.daily_goals import GoalsError, Goal, claim_chest, goal_progress
    from shared.economy import DAILY_CHEST_COINS, DAILY_CHEST_RESOURCE, utcnow
    from shared.ledger import change_balance
    from shared.resources import get_resources
    now = utcnow()
    today = now.date()
    await _mk_user(conn, 700, 100, goal_streak=3, goal_last_claim=today - timedelta(days=1))
    goals = [Goal("win_rps", 2, "games"), Goal("bonus", 1)]

    with pytest.raises(GoalsError) as e:
        await claim_chest(conn, 700, goals, today)
    assert e.value.key == "goal.err_not_done"
    await conn.execute("DELETE FROM daily_goal_claims WHERE user_id = 700")   # в проде откат делает транзакция

    await change_balance(conn, 700, 2, "game_win:rps")
    await change_balance(conn, 700, 2, "game_win:rps")
    await conn.execute("UPDATE users SET last_bonus_claim_at = $1 WHERE user_id = 700", now)
    assert await goal_progress(conn, 700, goals, today) == {"win_rps": 2, "bonus": 1}

    chest = await claim_chest(conn, 700, goals, today)
    assert chest["coins"] == DAILY_CHEST_COINS and chest["streak"] == 4
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 700") == 104 + DAILY_CHEST_COINS
    assert (await get_resources(conn, 700))[chest["kind"]] == DAILY_CHEST_RESOURCE
    with pytest.raises(GoalsError) as e:
        await claim_chest(conn, 700, goals, today)
    assert e.value.key == "goal.err_claimed"


async def test_team_station_donations_level_up_for_everyone(conn):
    from shared.economy import RESOURCE_KINDS, station_level_cost
    from shared.resources import get_resources, grant_bundle
    from shared.team_station import StationError, donate, get_station, station_level
    await conn.execute("INSERT INTO teams (team_id, team_name, captain_id) VALUES (9, 'Orbit', 800)")
    await _mk_user(conn, 800, 0, team_id=9)
    await _mk_user(conn, 801, 0, team_id=9)
    await _mk_user(conn, 802, 0)                                   # без команды
    cost = station_level_cost(1)
    await grant_bundle(conn, 800, {k: cost for k in RESOURCE_KINDS}, "test")
    await grant_bundle(conn, 802, {"metal": 10}, "test")

    with pytest.raises(StationError) as e:
        await donate(conn, 802, "metal", 10)
    assert e.value.key == "st.err_no_team"
    with pytest.raises(StationError) as e:
        await donate(conn, 801, "metal", 1)
    assert e.value.key == "st.err_resources"

    for k in RESOURCE_KINDS[:-1]:
        res = await donate(conn, 800, k, cost)
        assert res.level == 0
    res = await donate(conn, 800, "parts", cost)
    assert res.level == 1 and res.levels_gained == 1
    assert await station_level(conn, 9) == 1 and await station_level(conn, None) == 0
    station = await get_station(conn, 9)
    assert all(station[k] == 0 for k in RESOURCE_KINDS)        # уровень закрыт, остаток 0
    assert all(v == 0 for v in (await get_resources(conn, 800)).values())
    assert await conn.fetchval("SELECT COUNT(*) FROM team_donations WHERE team_id = 9") == 4


# ---------------------------------------------------------------- биржа v2 (24.10): ресурсы, заявки, обмен
async def test_market_v2_buy_orders_resources_floor_and_shuttle(conn):
    from datetime import timedelta
    from shared.economy import MARKET_CUTLET_MIN_PRICE, utcnow
    from shared.market import (MarketError, cancel_order, fill_order, index_change, place_order,
                               price_history)
    from shared.resources import get_resources, grant_bundle
    await _mk_user(conn, 900, 10_000, inv_cutlets=10, has_shuttle=True,   # продавец с заряженным Шаттлом
                   shuttle_until=utcnow() + timedelta(days=5))
    await _mk_user(conn, 901, 10_000)                                     # покупатель без Шаттла
    await grant_bundle(conn, 900, {"metal": 500}, "test")

    # Пол цены котлеты действует для обеих сторон
    for side in ("sell", "buy"):
        with pytest.raises(MarketError) as e:
            await place_order(conn, 900 if side == "sell" else 901, "cutlet", side, 1, MARKET_CUTLET_MIN_PRICE - 1)
        assert e.value.key == "mk.err_price"

    # Заявка на покупку металла: монеты замораживаются сразу
    bid = await place_order(conn, 901, "metal", "buy", 100, 30)          # полы 26.10: металл от 20 🪙
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 901") == 10_000 - 3000
    # Продавец с Шаттлом закрывает заявку: комиссия 5% с ЕГО продажи
    deal = await fill_order(conn, 900, bid, 100)
    assert (deal["side"], deal["fee"], deal["seller_got"]) == ("buy", 150, 2850)
    assert (await get_resources(conn, 901))["metal"] == 100
    assert (await get_resources(conn, 900))["metal"] == 400
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 900") == 10_000 + 2850

    # Продажа котлет игроком без Шаттла покупателю с Шаттлом: комиссия обычная (Шаттл не «одалживается»)
    ask = await place_order(conn, 901, "metal", "sell", 50, 40)
    deal2 = await fill_order(conn, 900, ask, 50)
    assert (deal2["side"], deal2["fee"]) == ("sell", 200)
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 900") == 10

    # Отмена заявки возвращает замороженные монеты; ордер на продажу — товар
    bid2 = await place_order(conn, 901, "cutlet", "buy", 2, MARKET_CUTLET_MIN_PRICE)
    balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = 901")
    await cancel_order(conn, 901, bid2)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 901") == balance + 2 * MARKET_CUTLET_MIN_PRICE
    with pytest.raises(MarketError) as e:
        await place_order(conn, 901, "metal", "sell", 999, 50)   # у 901 осталось 50 металла
    assert e.value.key == "mk.err_no_resource"

    # История сделок и индекс
    hist = await price_history(conn, "metal", utcnow())
    assert len(hist) == 7 and hist[-1]["volume"] == 150
    assert index_change(hist)["last"] == round((100 * 30 + 50 * 40) / 150, 1)
    trades = await conn.fetchval("SELECT COUNT(*) FROM market_trades")
    assert trades == 2


async def test_resource_swaps_escrow_accept_cancel(conn):
    from shared.market import MarketError, accept_swap, cancel_swap, create_swap
    from shared.resources import get_resources, grant_bundle
    await _mk_user(conn, 910, 0)
    await _mk_user(conn, 911, 0)
    await grant_bundle(conn, 910, {"metal": 100}, "test")
    await grant_bundle(conn, 911, {"hydrogen": 30}, "test")

    swap_id = await create_swap(conn, 910, "metal", 60, "hydrogen", 25)
    assert (await get_resources(conn, 910))["metal"] == 40            # отложено в эскроу
    with pytest.raises(MarketError) as e:
        await accept_swap(conn, 910, swap_id)
    assert e.value.key == "mk.err_own"
    await accept_swap(conn, 911, swap_id)
    assert (await get_resources(conn, 910)) == {"metal": 40, "hydrogen": 25, "crystal": 0, "parts": 0}
    assert (await get_resources(conn, 911)) == {"metal": 60, "hydrogen": 5, "crystal": 0, "parts": 0}
    with pytest.raises(MarketError):
        await accept_swap(conn, 911, swap_id)                         # уже закрыт

    with pytest.raises(MarketError) as e:                             # аудит 2.4: неравный обмен (800 против 10)
        await create_swap(conn, 910, "metal", 40, "parts", 1)
    assert e.value.key == "sw.err_ratio"
    swap2 = await create_swap(conn, 910, "metal", 40, "parts", 80)
    await cancel_swap(conn, 910, swap2)
    assert (await get_resources(conn, 910))["metal"] == 40


# ---------------------------------------------------------------- 25.10: склад с лимитом, рецепты недели, рефералка
async def test_storage_cap_clips_mining_but_not_transfers(conn, global_db):
    pytest.importorskip("aiogram")
    from datetime import timedelta
    from bots.main_bot.handlers.games import execute_solo_game_payout
    from shared.economy import utcnow
    from shared.market import MarketError, fill_order, place_order
    from shared.resources import change_resource, get_resources, grant_bundle
    from shared.workshop import craft
    await _mk_user(conn, 920, 100, unlimit_until=utcnow() + timedelta(hours=1), created_at=utcnow() - timedelta(days=60))
    await _mk_user(conn, 921, 10_000)
    await grant_bundle(conn, 920, {"parts": 499}, "test")

    ok, text, _ = await execute_solo_game_payout(920, True, "safe")       # +3 детали, влезает только 1
    assert ok and "📦" in text
    assert (await get_resources(conn, 920))["parts"] == 500
    rows = await conn.fetch("SELECT delta FROM resource_ledger WHERE user_id = 920 AND reason = 'game_win:safe' "
                            "AND kind = 'parts'")   # ⚡ за победу (шанс 25%) пишется с той же причиной
    assert [r["delta"] for r in rows] == [1]                                # в журнал — фактически полученное

    # Безлимит: победы сверх суточного лимита дают ресурс (16 побед в Больше/Меньше при лимите 15)
    for _ in range(16):
        ok, _, _ = await execute_solo_game_payout(920, True, "hl")
        assert ok
    assert (await get_resources(conn, 920))["hydrogen"] == 16

    # Биржа: купить ресурс сверх вместимости нельзя — проверка до списания монет
    await grant_bundle(conn, 921, {"parts": 100}, "test")
    ask = await place_order(conn, 921, "parts", "sell", 10, 10)
    with pytest.raises(MarketError) as e:
        await fill_order(conn, 920, ask, 10)
    assert e.value.key == "mk.err_storage_full"
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 920") >= 100

    # Расширение склада: 500 → 1000, после него добыча снова идёт
    from shared.economy import STORAGE_LEVELS
    cost = STORAGE_LEVELS[0][1]
    await grant_bundle(conn, 920, {k: v for k, v in cost.items() if k != "parts"}, "test")
    res = await craft(conn, 920, "storage", utcnow())
    assert res.level == 1000
    assert await conn.fetchval("SELECT res_capacity FROM users WHERE user_id = 920") == 1000
    assert await change_resource(conn, 920, "parts", 5, "test", cap=1000) == 500 - cost["parts"] + 5


async def test_weekly_recipe_needs_toggle_and_respects_limit(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.weekly_recipes import WEEKLY_RECIPES, WeeklyError, craft_weekly
    now = utcnow()
    await _mk_user(conn, 930, 0)
    await grant_bundle(conn, 930, {"metal": 400}, "test")
    with pytest.raises(WeeklyError) as e:
        await craft_weekly(conn, 930, "w_cutlet_metal", now, enabled=False)
    assert e.value.key == "wk.err_gone"
    res = await craft_weekly(conn, 930, "w_cutlet_metal", now, enabled=True)
    assert res["left"] == 0
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 930") == 1
    with pytest.raises(WeeklyError) as e:
        await craft_weekly(conn, 930, "w_cutlet_metal", now, enabled=True)
    assert e.value.key == "wk.err_limit"
    # Новая неделя — лимит снова доступен
    await craft_weekly(conn, 930, "w_cutlet_metal", now + timedelta(days=7), enabled=True)
    # Комбо с бустом и щитом, переплавка ресурса
    await grant_bundle(conn, 930, {"metal": 40}, "test")
    await craft_weekly(conn, 930, "w_conv_metal_hydro", now, enabled=True)
    assert (await get_resources(conn, 930))["hydrogen"] == WEEKLY_RECIPES["w_conv_metal_hydro"]["effects"][0]["qty"]
    await grant_bundle(conn, 930, {"metal": 15, "crystal": 15}, "test")
    await craft_weekly(conn, 930, "w_shield_48h", now, enabled=True)
    assert await conn.fetchval("SELECT raid_shield_until FROM users WHERE user_id = 930") == now + timedelta(hours=48)


async def test_active_friend_via_quiz_level_up_pays_500_once(conn, global_db):
    """Друг с 3 котлетами закрывает 3 уровень → пригласителю +500, котлета и по 10 ресурсов, один раз."""
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.games import execute_solo_game_payout
    from shared.analytics import qualify_referral_if_due
    from shared.economy import REFERRAL_QUALIFIED_BONUS, REFERRAL_QUALIFIED_CUTLETS, REFERRAL_QUALIFIED_RESOURCES
    from shared.resources import get_resources
    await _mk_user(conn, 940, 0, inv_cutlets=0)
    await _mk_user(conn, 941, 100, referred_by=940, bonus_claims=3)
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level, quiz_level_progress) VALUES (941, 2, 29)")
    ok, _, _ = await execute_solo_game_payout(941, True, "quiz")          # закрыт уровень 3
    assert ok
    row = await conn.fetchrow("SELECT balance, inv_cutlets FROM users WHERE user_id = 940")
    assert (row["balance"], row["inv_cutlets"]) == (REFERRAL_QUALIFIED_BONUS, REFERRAL_QUALIFIED_CUTLETS)
    assert set((await get_resources(conn, 940)).values()) == {REFERRAL_QUALIFIED_RESOURCES}
    assert await qualify_referral_if_due(conn, 941) is None                # ровно один раз


async def test_intern_rebalance_migration_takes_back_extra_interns(conn):
    """Откат «Стажёр за каждый уровень»: остаются стартовый + по одному за 10 уровней."""
    from datetime import timedelta
    from shared.database import SCHEMA_STATEMENTS
    from shared.economy import utcnow
    now = utcnow()
    await _mk_user(conn, 950, 0, intern_claimed=True, interns_pending=1)    # 2 уровень, 3 Стажёра
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (950, 2)")
    await _mk_user(conn, 951, 0, intern_claimed=True, interns_pending=5)    # 12 уровень, 1 Стажёр
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (951, 12)")
    for uid, n in ((950, 3), (951, 1)):
        for i in range(n):
            await conn.execute(
                "INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES ($1, 'intern', $2, $3)",
                uid, now + timedelta(minutes=i), now + timedelta(days=36500))
    await conn.execute("UPDATE users SET interns_rebalanced = FALSE")
    for stmt in SCHEMA_STATEMENTS:
        if "interns_rebalanced" in stmt and ("DELETE" in stmt or "UPDATE" in stmt):
            await conn.execute(stmt)
    count = "SELECT COUNT(*) FROM miners WHERE user_id = $1 AND kind = 'intern'"
    pending = "SELECT interns_pending FROM users WHERE user_id = $1"
    assert (await conn.fetchval(count, 950), await conn.fetchval(pending, 950)) == (1, 0)
    assert (await conn.fetchval(count, 951), await conn.fetchval(pending, 951)) == (1, 1)


# ============================================================================
# Переводы только с активных аккаунтов; удаление аккаунта (26.10)
# ============================================================================
async def test_transfer_needs_an_active_sender_and_a_live_recipient(conn):
    from shared.transfers import TransferError, transfer_coins
    await _mk_user(conn, 960, 5000, bonus_claims=3)           # котлеты есть, интеллекта нет
    await _mk_user(conn, 961, 0)
    with pytest.raises(TransferError) as e:
        async with conn.transaction():
            await transfer_coins(conn, 960, 961, 100)
    assert e.value.key == "tr.err_not_active"
    await _make_active(conn, 960)
    await conn.execute("UPDATE users SET deletion_requested_at = NOW() WHERE user_id = 961")
    with pytest.raises(TransferError) as e:
        async with conn.transaction():
            await transfer_coins(conn, 960, 961, 100)
    assert e.value.key == "tr.not_found"                       # замороженному не перевести
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 960") == 5000


async def test_account_deletion_full_cycle(conn):
    """Заявка → заморозка (ордера сняты) → обезличивание через 7 дней → возврат без бонусов."""
    from datetime import timedelta
    from bots.main_bot.handlers.start import register_user
    from shared.account_deletion import (cancel_deletion, due_for_purge, purge_account,
                                         request_deletion, restore_account)
    from shared.economy import ACCOUNT_DELETE_GRACE_DAYS, utcnow
    from shared.market import place_sell_order
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    await _mk_user(conn, 970, 777, inv_cutlets=5, display_name="Тестовый Игрок", referred_by=None)
    await _mk_user(conn, 971, 0)
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (970, 4)")
    await grant_bundle(conn, 970, {"metal": 30, "crystal": 7, "stone": 4, "battery": 2, "core": 1}, "test")
    await conn.execute("UPDATE users SET horses = 2, carts = 1, drones_attack = 3, shuttle_until = NOW() + INTERVAL "
                       "'5 days' WHERE user_id = 970")
    await _tech(conn, 970, comm=1)
    await conn.execute("INSERT INTO miners (user_id, kind, expires_at) VALUES (970, 'intern', $1)",
                       now + timedelta(days=36500))
    await conn.execute("INSERT INTO vip_aliases (alias, user_id) VALUES ('ROFL-HUB-DEL', 970)")
    team_id = await conn.fetchval(
        "INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Del', 970, 2) RETURNING team_id")
    await conn.execute("UPDATE users SET team_id = $1, team_joined_at = $2 WHERE user_id = 970", team_id, now)
    await conn.execute("UPDATE users SET team_id = $1, team_joined_at = $2 WHERE user_id = 971",
                       team_id, now + timedelta(minutes=1))
    await place_sell_order(conn, 970, 3, 250)
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 970") == 2

    # Передумать можно
    async with conn.transaction():
        await request_deletion(conn, 970, now)
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 970") == 5   # ордер снят
    assert await cancel_deletion(conn, 970) is True
    assert await cancel_deletion(conn, 970) is False

    # Заявка всерьёз: до срока не удаляется, после — обезличивается
    async with conn.transaction():
        due = await request_deletion(conn, 970, now)
    assert due == now + timedelta(days=ACCOUNT_DELETE_GRACE_DAYS)
    assert await purge_account(conn, 970, now + timedelta(days=1)) is False
    later = now + timedelta(days=ACCOUNT_DELETE_GRACE_DAYS, minutes=1)
    assert await due_for_purge(conn, later) == [970]
    async with conn.transaction():
        assert await purge_account(conn, 970, later) is True
    u = await conn.fetchrow("SELECT * FROM users WHERE user_id = 970")
    assert (u["username"], u["display_name"], u["balance"], u["inv_cutlets"], u["team_id"]) == \
        (None, None, 0, 0, None)
    assert u["deleted_at"] == later and u["deletion_requested_at"] is None
    from shared.economy import ALL_KINDS
    assert set((await get_resources(conn, 970, ALL_KINDS)).values()) <= {0}    # аудит 1.9: всё сырьё, не только базовое
    assert (u["horses"], u["carts"], u["drones_attack"], u["shuttle_until"]) == (0, 0, 0, None)
    for table in ("miners", "vip_aliases", "game_stats", "user_tech"):
        assert await conn.fetchval(f"SELECT COUNT(*) FROM {table} WHERE user_id = 970") == 0
    team = await conn.fetchrow("SELECT captain_id, members_count FROM teams WHERE team_id = $1", team_id)
    assert (team["captain_id"], team["members_count"]) == (971, 1)        # корона — ветерану
    assert await conn.fetchval(
        "SELECT SUM(delta) FROM ledger WHERE user_id = 970 AND reason = 'account_deleted'") == -777

    # Возврат: профиль с нуля, без стартового бонуса
    assert await register_user(conn, 970, "back", "ru", referrer_id=None) is False
    async with conn.transaction():
        assert await restore_account(conn, 970, "back", "Снова Я") is True
    u = await conn.fetchrow("SELECT balance, deleted_at, username FROM users WHERE user_id = 970")
    assert (u["balance"], u["deleted_at"], u["username"]) == (0, None, "back")
    assert await conn.fetchval("SELECT COUNT(*) FROM ledger WHERE user_id = 970 AND reason = 'signup_bonus'") == 0


async def test_account_purge_waits_for_an_auction_leader(conn):
    from datetime import timedelta
    from shared.account_deletion import purge_account, request_deletion
    from shared.economy import utcnow
    now = utcnow()
    await _mk_user(conn, 980, 100)
    await conn.execute("INSERT INTO auctions (item_title, highest_bidder_id) VALUES ('VIP', 980)")
    async with conn.transaction():
        await request_deletion(conn, 980, now)
    later = now + timedelta(days=30)
    assert await purge_account(conn, 980, later) is False                 # ставка-эскроу лидера
    await conn.execute("UPDATE auctions SET status = 'closed'")
    assert await purge_account(conn, 980, later) is True


async def test_leave_team_disbands_a_lonely_captain(conn):
    from shared.db_clans import leave_team
    await _mk_user(conn, 990, 0)
    team_id = await conn.fetchval(
        "INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Solo', 990, 1) RETURNING team_id")
    await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = 990", team_id)
    assert await leave_team(conn, 990, team_id + 1) is None               # чужая/устаревшая кнопка
    left = await leave_team(conn, 990, team_id)
    assert left["outcome"] == "disbanded"
    assert await conn.fetchval("SELECT COUNT(*) FROM teams") == 0
    assert await conn.fetchval("SELECT team_id FROM users WHERE user_id = 990") is None



# ============================================================================
# Команды: общая механика чата и приложения (26.10)
# ============================================================================
async def test_team_create_join_search_roulette_and_roster(conn):
    from shared.db_clans import (TeamError, create_team, join_team, random_teams, search_teams,
                                 team_members)
    from shared.economy import TEAM_CREATE_COST
    await _mk_user(conn, 1000, TEAM_CREATE_COST + 5)
    await _mk_user(conn, 1001, 0)
    await _mk_user(conn, 1002, TEAM_CREATE_COST)

    with pytest.raises(TeamError) as e:                       # ссылки в названии запрещены
        async with conn.transaction():
            await create_team(conn, 1000, "t.me/spam", "девиз", "🔥")
    assert e.value.key == "team.err_link"
    with pytest.raises(TeamError) as e:                       # денег нет — монеты не списаны
        async with conn.transaction():
            await create_team(conn, 1001, "Бедные", "девиз", "🔥")
    assert e.value.key == "team.err_money"

    async with conn.transaction():
        team_id = await create_team(conn, 1000, "Котлеты & Ко", "Вперёд", "🥩")
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1000") == 5
    with pytest.raises(TeamError) as e:                       # название уже занято
        async with conn.transaction():
            await create_team(conn, 1002, "Котлеты & Ко", "x", "🔥")
    assert e.value.key == "team.err_taken"

    async with conn.transaction():
        card = await join_team(conn, 1001, team_id)
    assert card["name"] == "Котлеты & Ко" and card["members"] == 1   # имя без HTML-экранирования
    with pytest.raises(TeamError) as e:
        async with conn.transaction():
            await join_team(conn, 1001, team_id)
    assert e.value.key == "team.err_already"
    with pytest.raises(TeamError) as e:
        async with conn.transaction():
            await join_team(conn, 1002, 999_999)
    assert e.value.key == "team.err_gone"

    found = await search_teams(conn, "котлеты &")
    assert [t["id"] for t in found] == [team_id]
    assert await search_teams(conn, "%") == []                # % ищется как символ, а не «всё подряд»
    assert [t["id"] for t in await random_teams(conn)] == [team_id]
    await conn.execute("UPDATE teams SET members_count = max_members WHERE team_id = $1", team_id)
    assert await random_teams(conn) == []                     # в рулетке только команды со свободными местами
    with pytest.raises(TeamError) as e:
        async with conn.transaction():
            await join_team(conn, 1002, team_id)
    assert e.value.key == "team.err_full"

    roster = await team_members(conn, team_id, 1000)
    assert [m["user_id"] for m in roster] == [1000, 1001]     # капитан первым


# ---------------------------------------------------------------- 26.10: биржа команды и взаимопомощь
async def test_team_market_is_private_cheaper_and_closed_on_leave(conn):
    from shared.db_clans import leave_team
    from shared.economy import CLAN_MARKET_FEE_PERCENT, TEAM_MARKET_FEE_PERCENT
    from shared.market import MarketError, fill_order, list_open_orders, place_order
    from shared.resources import get_resources, grant_bundle
    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) "
                              "VALUES ('Alpha', 1300, 2) RETURNING team_id")
    await _mk_user(conn, 1300, 0, team_id=tid)
    await _mk_user(conn, 1301, 10_000, team_id=tid)
    await _mk_user(conn, 1302, 10_000)                     # чужой
    await grant_bundle(conn, 1300, {"metal": 500}, "test")

    with pytest.raises(MarketError) as e:
        await place_order(conn, 1302, "metal", "buy", 1, 20, team_only=True)
    assert e.value.key == "mk.err_no_team"

    ask = await place_order(conn, 1300, "metal", "sell", 100, 20, team_only=True)
    assert ask not in [o["id"] for o in await list_open_orders(conn, 50, asset="metal", side="sell")]
    assert ask in [o["id"] for o in await list_open_orders(conn, 50, asset="metal", side="sell", team_id=tid)]
    with pytest.raises(MarketError) as e:
        await fill_order(conn, 1302, ask, 10)
    assert e.value.key == "mk.err_team_only"

    deal = await fill_order(conn, 1301, ask, 50)            # 1000 🪙, комиссия команды 5%
    assert deal["fee"] == 1000 * TEAM_MARKET_FEE_PERCENT // 100
    await conn.execute("UPDATE teams SET max_members = 1000 WHERE team_id = $1", tid)
    deal2 = await fill_order(conn, 1301, ask, 50)           # Мега-Клан — 2%
    assert deal2["fee"] == 1000 * CLAN_MARKET_FEE_PERCENT // 100

    ask2 = await place_order(conn, 1300, "metal", "sell", 100, 20, team_only=True)
    async with conn.transaction():
        await leave_team(conn, 1300, tid)
    assert await conn.fetchval("SELECT status FROM market_orders WHERE id = $1", ask2) != "open"
    assert (await get_resources(conn, 1300))["metal"] == 400  # эскроу вернулся


async def test_team_help_rules(conn):
    from datetime import timedelta
    from shared.economy import TEAM_HELP_DAILY_GIVE, utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.team_help import HelpError, cancel_help, give_help, given_today, request_help
    now = utcnow()
    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) "
                              "VALUES ('Beta', 1310, 3) RETURNING team_id")
    await _mk_user(conn, 1310, 0, team_id=tid)
    await _mk_user(conn, 1311, 0, team_id=tid)              # ещё не активный
    await _mk_user(conn, 1312, 0, team_id=tid)
    await _mk_user(conn, 1313, 0)                           # чужой
    await _make_active(conn, 1311)                          # активный, но для дарения мало
    for uid in (1312, 1313):                                # прокачанные: 7 уровень + 10 котлет
        await conn.execute("UPDATE users SET bonus_claims = 10 WHERE user_id = $1", uid)
        await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES ($1, 7)", uid)
    for uid in (1311, 1312, 1313):
        await grant_bundle(conn, uid, {"crystal": 300}, "test")

    hid = await request_help(conn, 1310, "crystal", 150)
    with pytest.raises(HelpError) as e:
        await request_help(conn, 1310, "metal", 10)
    assert e.value.key == "help.err_open"
    with pytest.raises(HelpError) as e:
        await request_help(conn, 1313, "metal", 10)
    assert e.value.key == "mk.err_no_team"

    with pytest.raises(HelpError) as e:
        await give_help(conn, 1310, hid, 10, now)
    assert e.value.key == "help.err_self"
    with pytest.raises(HelpError) as e:
        await give_help(conn, 1313, hid, 10, now)
    assert e.value.key == "mk.err_no_team"
    other = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) "
                                "VALUES ('Gamma', 1313, 1) RETURNING team_id")
    await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = 1313", other)
    with pytest.raises(HelpError) as e:
        await give_help(conn, 1313, hid, 10, now)          # игрок чужой команды
    assert e.value.key == "mk.err_team_only"
    with pytest.raises(HelpError) as e:
        await give_help(conn, 1311, hid, 10, now)
    assert e.value.key == "help.err_not_active"

    res = await give_help(conn, 1312, hid, 150, now)        # режется суточным лимитом
    assert res["qty"] == TEAM_HELP_DAILY_GIVE and not res["done"]
    assert await given_today(conn, 1312, now) == TEAM_HELP_DAILY_GIVE
    with pytest.raises(HelpError) as e:
        await give_help(conn, 1312, hid, 10, now)
    assert e.value.key == "help.err_limit"
    res = await give_help(conn, 1312, hid, 999, now + timedelta(days=1))   # новый день, остаток просьбы
    assert res["qty"] == 150 - TEAM_HELP_DAILY_GIVE and res["done"]
    assert (await get_resources(conn, 1310))["crystal"] == 150
    assert (await get_resources(conn, 1312))["crystal"] == 150

    hid2 = await request_help(conn, 1310, "parts", 10)
    await cancel_help(conn, 1310, hid2)
    with pytest.raises(HelpError) as e:
        await give_help(conn, 1312, hid2, 5, now + timedelta(days=1))
    assert e.value.key == "help.err_not_found"


async def test_workshop_items_go_to_storage_and_activate_later(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.items import ItemError, activate_item, list_items
    from shared.resources import grant_bundle
    from shared.weekly_recipes import craft_weekly
    from shared.workshop import craft
    now = utcnow()
    await _mk_user(conn, 1320, 0, created_at=now - timedelta(days=60))
    await grant_bundle(conn, 1320, {"metal": 300, "hydrogen": 300, "crystal": 300, "parts": 300}, "test")

    res = await craft(conn, 1320, "shield_24h", now, to_storage=True)        # приложение: на склад
    assert res.stored and res.until is None
    assert await conn.fetchval("SELECT raid_shield_until FROM users WHERE user_id = 1320") is None
    await craft(conn, 1320, "shield_24h", now, to_storage=True)
    await craft_weekly(conn, 1320, "w_combo_guard", now, enabled=True, to_storage=True)   # азот 12 ч + щит 12 ч
    items = {(i["effect"], i["hours"]): i["qty"] for i in await list_items(conn, 1320)}
    assert items == {("shield", 24): 2, ("nitrogen", 12): 1, ("shield", 12): 1}

    until = (await activate_item(conn, 1320, "shield", 24, now))["until"]
    assert until == now + timedelta(hours=24)
    until2 = (await activate_item(conn, 1320, "shield", 24, now))["until"]               # второй продлевает
    assert until2 == now + timedelta(hours=48)
    with pytest.raises(ItemError) as e:
        await activate_item(conn, 1320, "shield", 24, now)
    assert e.value.key == "it.err_none"
    await activate_item(conn, 1320, "nitrogen", 12, now)
    assert await conn.fetchval("SELECT boost_nitrogen_until FROM users WHERE user_id = 1320") == now + timedelta(hours=12)

    res = await craft(conn, 1320, "nitro_6h", now)                            # чат: как раньше, сразу
    assert not res.stored and res.until is not None
    assert {(i["effect"], i["hours"]) for i in await list_items(conn, 1320)} == {("shield", 12)}


async def test_new_items_unlock_limits_and_effects_in_raids_market_station(conn, global_db):
    from datetime import timedelta
    from shared.economy import raid_fail_loss, utcnow
    from shared.items import ItemError, activate_item
    from shared.market import fill_order, place_order
    from shared.raids import RaidError, execute_raid, find_targets
    from shared.resources import get_resources, grant_bundle
    from shared.team_station import donate
    from shared.workshop import WorkshopError, craft
    now = utcnow()
    old = now - timedelta(days=60)
    await _mk_user(conn, 1330, 0, created_at=now - timedelta(hours=2))      # новичок: открыт только Азот
    with pytest.raises(WorkshopError) as e:
        await craft(conn, 1330, "economizer", now, to_storage=True)
    assert e.value.key == "ws.err_locked"

    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Z', 1331, 1) RETURNING team_id")
    await _mk_user(conn, 1331, 10_000, created_at=old, team_id=tid, last_seen_at=now)
    await _mk_user(conn, 1332, 10_000, created_at=old, last_seen_at=now, raid_stance="rock")
    for uid in (1331, 1332):
        await grant_bundle(conn, uid, {k: 900 for k in ("metal", "hydrogen", "crystal", "parts")}, "test")
        await _tech(conn, uid, tools=3, comm=1, scout=1, attack=1)

    # Штамп — раз в неделю; выключенный владельцем рецепт не собирается
    await craft(conn, 1331, "stamp", now, to_storage=True)
    with pytest.raises(WorkshopError) as e:
        await craft(conn, 1331, "stamp", now, to_storage=True)
    assert e.value.key == "wk.err_limit"
    await conn.execute("INSERT INTO feature_flags (key, enabled) VALUES ('wsr:cargo', FALSE) "
                       "ON CONFLICT (key) DO UPDATE SET enabled = FALSE")
    from shared import feature_flags
    feature_flags._cache.clear()
    with pytest.raises(WorkshopError) as e:
        await craft(conn, 1331, "cargo", now, to_storage=True)
    assert e.value.key == "ws.err_off"

    # Маскировка прячет из разведки (до налёта: потом цель скрыта перезарядкой жертвы)
    assert 1332 in [x["user_id"] for x in await find_targets(conn, 1331, tid, now, limit=50)]
    await craft(conn, 1332, "camo_12h", now, to_storage=True)
    await activate_item(conn, 1332, "camo", 12, now)
    assert 1332 not in [x["user_id"] for x in await find_targets(conn, 1331, tid, now, limit=50)]

    # Экономайзер: вылет без водорода; Тренажёр стойки цели: ничья → провал налётчика
    await craft(conn, 1331, "economizer", now, to_storage=True)
    assert (await activate_item(conn, 1331, "economizer", 0, now))["charges"] == 1
    await craft(conn, 1332, "drill_24h", now, to_storage=True)
    await activate_item(conn, 1332, "drill", 24, now)
    hydro = (await get_resources(conn, 1331))["hydrogen"]
    with pytest.raises(RaidError) as e:                                    # аудит 2.9: под Маскировкой не бьют и напрямую
        await execute_raid(conn, 1331, 1332, "rock", now)
    assert e.value.key == "raid.err_gone"
    await conn.execute("UPDATE users SET raid_camo_until = NULL WHERE user_id = 1332")   # Маскировка кончилась
    res = await execute_raid(conn, 1331, 1332, "rock", now)                # rock vs rock = ничья
    assert res.result == "lose" and "drill" in res.notes and "economizer" in res.notes
    # водород ушёл только штрафом за провал (15), а не на вылет (ещё 5)
    assert hydro - (await get_resources(conn, 1331))["hydrogen"] == raid_fail_loss(hydro)

    # Форсаж сбрасывает перезарядку, второй раз за сутки — нельзя
    await craft(conn, 1331, "forsage", now, to_storage=True)
    await craft(conn, 1331, "forsage", now, to_storage=True)
    await activate_item(conn, 1331, "forsage", 0, now)
    assert await conn.fetchval("SELECT last_raid_at FROM users WHERE user_id = 1331") is None
    await conn.execute("UPDATE users SET last_raid_at = $2 WHERE user_id = $1", 1331, now)
    with pytest.raises(ItemError) as e:
        await activate_item(conn, 1331, "forsage", 0, now + timedelta(minutes=5))
    assert e.value.key == "it.err_forsage_daily"

    # Купол команды собирает только игрок в команде; Ремдрона больше нет — вклад засчитывается как есть
    with pytest.raises(WorkshopError) as e:
        await craft(conn, 1332, "dome_12h", now, to_storage=True)
    assert e.value.key == "mk.err_no_team"
    with pytest.raises(WorkshopError):
        await craft(conn, 1331, "station_drone", now, to_storage=True)
    assert (await donate(conn, 1331, "metal", 100)).credited == 100

    # Штамп: продажа без комиссии
    await activate_item(conn, 1331, "stamp", 0, now)
    await conn.execute("UPDATE users SET res_capacity = 5000 WHERE user_id = 1332")   # место под покупку
    ask = await place_order(conn, 1331, "metal", "sell", 10, 20)
    assert (await fill_order(conn, 1332, ask, 10))["fee"] == 0


async def test_mines_capture_and_hourly_payout_to_every_member(conn):
    from datetime import timedelta
    from shared.economy import ALL_KINDS, MINE_CORE_EVERY_HOURS, MINE_CORE_MAX, MINE_HOLD_HOURS, mine_kind, utcnow
    from shared.mines import capture_mine, free_mine_ids, pay_mine, sick_hours
    from shared.resources import get_resources
    now = utcnow()
    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('M', 1340, 3) RETURNING team_id")
    for uid in (1340, 1341, 1342, 1343):
        await _mk_user(conn, uid, 0, team_id=tid)
    for uid in (1340, 1341, 1342):
        await _tech(conn, uid, comm=1)                                              # 1343 — без связи
    await conn.execute("UPDATE users SET meds_until = $2 WHERE user_id = $1", 1340, now + timedelta(days=9))
    await conn.execute("UPDATE users SET is_blocked = TRUE WHERE user_id = 1342")   # заблокированному — ничего
    assert 3 in await free_mine_ids(conn, now)
    until = await capture_mine(conn, 3, tid, None, now)
    assert until == now + timedelta(hours=MINE_HOLD_HOURS)
    assert 3 not in await free_mine_ids(conn, now)
    assert await pay_mine(conn, 3, now + timedelta(minutes=59)) == 0
    assert await pay_mine(conn, 3, now + timedelta(hours=5, minutes=30)) == 5
    kind = mine_kind(3)
    assert (await get_resources(conn, 1340))[kind] == 5 and (await get_resources(conn, 1341))[kind] == 5
    assert (await get_resources(conn, 1342))[kind] == 0
    assert await pay_mine(conn, 3, now + timedelta(hours=5, minutes=50)) == 0       # тот же час не платится дважды
    assert await pay_mine(conn, 3, now + timedelta(hours=MINE_HOLD_HOURS + 3)) == MINE_HOLD_HOURS - 5
    assert (await get_resources(conn, 1340))[kind] == MINE_HOLD_HOURS                # с Аптечкой — без потерь
    assert (await get_resources(conn, 1341))[kind] == MINE_HOLD_HOURS - sick_hours(0, MINE_HOLD_HOURS)
    assert (await get_resources(conn, 1343, ALL_KINDS))[kind] == 0                    # без 📡 связи — ничего
    cores = min(MINE_HOLD_HOURS // MINE_CORE_EVERY_HOURS, MINE_CORE_MAX)
    assert (await get_resources(conn, 1340, ("core",)))["core"] == cores
    assert (await get_resources(conn, 1341, ("core",)))["core"] == cores
    assert await conn.fetchval("SELECT team_id FROM mines WHERE id = 3") is None    # рудник освободился


# ---------------------------------------------------------------- 27.10: ресурсы v3, Лаборатория, сезоны
async def test_lab_tools_tech_tool_gate_and_cooldown(conn):
    from datetime import timedelta
    from shared.economy import TOOL_COSTS, tech_cooldown_days, tech_cost, utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.tech import TechError, get_tech, upgrade_tech, upgrade_tools
    now = utcnow()
    await _mk_user(conn, 1400, 0)
    with pytest.raises(TechError) as e:                      # инструменты стоят ресурсов
        await upgrade_tools(conn, 1400, now)
    assert e.value.key == "ws.err_resources"
    await grant_bundle(conn, 1400, {"metal": 400, "wood": 40, "fire": 5, "crystal": 400, "parts": 400,
                                    "energy": 400, "hydrogen": 400}, "test")
    assert await upgrade_tools(conn, 1400, now) == 1
    assert (await get_resources(conn, 1400, ("wood", "fire"))) == {"wood": 0, "fire": 0}
    assert (await get_resources(conn, 1400))["metal"] == 400 - TOOL_COSTS[1]["metal"]

    assert await upgrade_tech(conn, 1400, "attack", now) == 1
    with pytest.raises(TechError) as e:                      # 2-й уровень — после перезарядки
        await upgrade_tech(conn, 1400, "attack", now + timedelta(days=1))
    assert e.value.key == "tech.err_cooldown"
    later = now + timedelta(days=tech_cooldown_days("attack", 1), minutes=1)
    metal = (await get_resources(conn, 1400))["metal"]
    assert await upgrade_tech(conn, 1400, "attack", later) == 2
    assert (await get_resources(conn, 1400))["metal"] == metal - tech_cost("attack", 2)["metal"]

    with pytest.raises(TechError) as e:                      # ⚔️ 3 требует набор 🛠
        await upgrade_tech(conn, 1400, "attack", later + timedelta(days=31))
    assert (e.value.key, e.value.kwargs) == ("tech.err_tool", {"tool": 2})
    with pytest.raises(TechError) as e:                      # 📚 — только когда все технологии на 1 уровне
        await upgrade_tech(conn, 1400, "science", now)
    assert (e.value.key, e.value.kwargs) == ("tech.err_science", {"level": 1})
    for tech in ("comm", "scout", "defense"):                # 1 уровень — с первого дня
        assert await upgrade_tech(conn, 1400, tech, now) == 1
    with pytest.raises(TechError) as e:                      # ворота открыты, но нужен набор 🛠
        await upgrade_tech(conn, 1400, "science", now)
    assert e.value.key == "tech.err_tool"
    with pytest.raises(TechError) as e:
        await upgrade_tech(conn, 1400, "magic", now)
    assert e.value.key == "tech.err_unknown"
    state = await get_tech(conn, 1400)
    assert state["attack"]["level"] == 2 and state["tools"]["level"] == 1 and state["science"]["level"] == 0


async def test_horses_carts_and_market_lots(conn):
    from shared.economy import HORSE_PRICES, MARKET_BASE_LOTS, MAX_HORSES, utcnow
    from shared.market import MarketError, place_order
    from shared.resources import grant_bundle
    from shared.tech import TechError, buy_horse
    from shared.workshop import WorkshopError, craft
    from datetime import timedelta
    now = utcnow()
    await _mk_user(conn, 1410, sum(HORSE_PRICES) + 100, created_at=now - timedelta(days=60))
    await grant_bundle(conn, 1410, {"metal": 400, "wood": 200, "fire": 20}, "test")
    for _ in range(MARKET_BASE_LOTS):                         # без лошадей — 2 лота
        await place_order(conn, 1410, "metal", "sell", 10, 20)
    with pytest.raises(MarketError) as e:
        await place_order(conn, 1410, "metal", "sell", 10, 20)
    assert e.value.key == "mk.err_too_many"

    await _tech(conn, 1410, tools=1)
    with pytest.raises(WorkshopError) as e:                   # телеге нужна лошадь
        await craft(conn, 1410, "cart", now)
    assert e.value.key == "cart.err_horse"
    assert await buy_horse(conn, 1410) == 1
    ledger = await conn.fetchval("SELECT delta FROM ledger WHERE user_id = 1410 AND reason = 'horse_buy'")
    assert ledger == -HORSE_PRICES[0]                          # монеты сгорели
    await craft(conn, 1410, "cart", now)
    assert await conn.fetchval("SELECT carts FROM users WHERE user_id = 1410") == 1
    for _ in range(2):                                         # +1 лошадь +1 телега
        await place_order(conn, 1410, "metal", "sell", 10, 20)
    with pytest.raises(MarketError):
        await place_order(conn, 1410, "metal", "sell", 10, 20)
    for _ in range(MAX_HORSES - 1):
        await buy_horse(conn, 1410)
    with pytest.raises(TechError) as e:
        await buy_horse(conn, 1410)
    assert e.value.key == "horse.err_max" and MAX_HORSES == 5
    await _mk_user(conn, 1411, 10)
    with pytest.raises(TechError) as e:
        await buy_horse(conn, 1411)
    assert e.value.key == "horse.err_coins"
    assert await conn.fetchval("SELECT horses FROM users WHERE user_id = 1411") == 0


async def test_shuttle_charge_spends_a_battery(conn):
    from datetime import timedelta
    from shared.economy import SHUTTLE_CHARGE_DAYS, utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.tech import TechError, charge_shuttle
    now = utcnow()
    await _mk_user(conn, 1420, 0)
    with pytest.raises(TechError) as e:
        await charge_shuttle(conn, 1420, now)
    assert e.value.key == "shuttle.err_none"
    await conn.execute("UPDATE users SET has_shuttle = TRUE WHERE user_id = 1420")
    with pytest.raises(TechError) as e:
        await charge_shuttle(conn, 1420, now)
    assert e.value.key == "ws.err_resources"
    await grant_bundle(conn, 1420, {"battery": 2}, "test")
    until = await charge_shuttle(conn, 1420, now)
    assert until == now + timedelta(days=SHUTTLE_CHARGE_DAYS)
    until2 = await charge_shuttle(conn, 1420, now + timedelta(days=1))   # заряд копится
    assert until2 == until + timedelta(days=SHUTTLE_CHARGE_DAYS)
    assert (await get_resources(conn, 1420, ("battery",)))["battery"] == 0


async def test_scout_needs_tech_and_fuel_but_no_battery(conn):
    from datetime import timedelta
    from shared.economy import raid_candidates, utcnow
    from shared.raids import RaidError, scout
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    old = now - timedelta(days=10)
    await _mk_user(conn, 1430, 0, created_at=old, last_seen_at=now)
    for uid in range(1431, 1438):
        await _mk_user(conn, uid, 0, created_at=old, last_seen_at=now)
        await grant_bundle(conn, uid, {"metal": 100}, "test")
    with pytest.raises(RaidError) as e:
        await scout(conn, 1430, now)
    assert (e.value.key, e.value.kwargs) == ("raid.err_need_tech", {"tech": "comm"})
    await _tech(conn, 1430, comm=1, scout=1, attack=1)
    with pytest.raises(RaidError) as e:
        await scout(conn, 1430, now)
    assert e.value.key == "raid.err_fuel"                          # топливо налёта — водород
    await grant_bundle(conn, 1430, {"hydrogen": 10}, "test")
    assert len(await scout(conn, 1430, now)) == raid_candidates(1)  # батарейки не нужны
    await _tech(conn, 1430, scout=4)
    assert len(await scout(conn, 1430, now)) == raid_candidates(4)
    assert (await get_resources(conn, 1430))["hydrogen"] == 10      # топливо тратит вылет, не разведка
    assert await conn.fetchval("SELECT COUNT(*) FROM resource_ledger WHERE user_id = 1430 AND kind = 'battery'") == 0


async def test_item_storage_holds_ten_percent_of_capacity(conn):
    from datetime import timedelta
    from shared.economy import items_capacity, utcnow
    from shared.items import items_count
    from shared.resources import grant_bundle
    from shared.workshop import WorkshopError, craft
    now = utcnow()
    await _mk_user(conn, 1560, 0, created_at=now - timedelta(days=60), res_capacity=500)
    assert items_capacity(500) == 50
    await conn.execute("INSERT INTO user_items (user_id, effect, hours, qty) VALUES (1560, 'shield', 24, 30), "
                       "(1560, 'economizer', 0, 19)")
    await grant_bundle(conn, 1560, {"metal": 100, "hydrogen": 100, "parts": 100}, "test")
    await craft(conn, 1560, "nitro_6h", now, to_storage=True)          # 50-е изделие — помещается
    assert await items_count(conn, 1560) == 50
    metal = await conn.fetchval("SELECT qty FROM user_resources WHERE user_id = 1560 AND kind = 'metal'")
    with pytest.raises(WorkshopError) as e:                            # 51-е — нет, ресурсы не списаны
        await craft(conn, 1560, "economizer", now, to_storage=True)
    assert (e.value.key, e.value.kwargs) == ("ws.err_items_full", {"max": 50})
    assert await conn.fetchval("SELECT qty FROM user_resources WHERE user_id = 1560 AND kind = 'metal'") == metal
    await conn.execute("UPDATE users SET res_capacity = 1000 WHERE user_id = 1560")
    await craft(conn, 1560, "economizer", now, to_storage=True)        # расширил склад — место есть
    assert await items_count(conn, 1560) == 51


async def test_raid_without_meds_loses_part_of_loot_and_tech_shifts_it(conn):
    from datetime import timedelta
    from shared.economy import RAID_SICK_LOSS_PERCENT, raid_loot, raid_loot_percent, utcnow
    from shared.raids import execute_raid
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    old = now - timedelta(days=10)
    await _mk_user(conn, 1440, 0, created_at=old, last_seen_at=now)
    await _mk_user(conn, 1441, 0, created_at=old, last_seen_at=now, raid_stance="scissors")
    await _tech(conn, 1440, comm=1, scout=1, attack=3)
    await _tech(conn, 1441, defense=1)
    await grant_bundle(conn, 1440, {"hydrogen": 10}, "test")
    await grant_bundle(conn, 1441, {"metal": 100}, "test")
    res = await execute_raid(conn, 1440, 1441, "rock", now)
    assert res.result == "win" and "sick" in res.notes
    pct = raid_loot_percent(3, 1, 0)
    taken = raid_loot(100, pct)
    got = taken - taken * RAID_SICK_LOSS_PERCENT // 100
    assert (await get_resources(conn, 1441))["metal"] == 100 - taken     # цель теряет полностью
    assert (await get_resources(conn, 1440))["metal"] == got             # налётчик довёз меньше
    assert res.loot["metal"] == got


async def test_bonfire_and_battery_make_resources_with_tools(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.workshop import WorkshopError, craft
    now = utcnow()
    await _mk_user(conn, 1450, 0, created_at=now - timedelta(days=60))
    await grant_bundle(conn, 1450, {"wood": 20, "stone": 10, "energy": 5, "metal": 5}, "test")
    await craft(conn, 1450, "bonfire", now)
    assert (await get_resources(conn, 1450, ("wood", "stone", "fire"))) == {"wood": 10, "stone": 5, "fire": 5}
    with pytest.raises(WorkshopError) as e:                  # батарейкам нужен набор ⚒️
        await craft(conn, 1450, "battery", now)
    assert e.value.key == "tech.err_tool"
    await _tech(conn, 1450, tools=1)
    await craft(conn, 1450, "battery", now)
    assert (await get_resources(conn, 1450, ("battery", "fire", "energy"))) == {"battery": 2, "fire": 4, "energy": 0}


async def test_dome_costs_five_times_more_for_a_mega_clan(conn):
    from datetime import timedelta
    from shared.economy import TEAM_ITEM_CLAN_MULTIPLIER, WORKSHOP_RECIPES, utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.workshop import WorkshopError, craft
    now = utcnow()
    cost = WORKSHOP_RECIPES["dome_12h"]["cost"]
    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('D', 1460, 1) "
                              "RETURNING team_id")
    await _mk_user(conn, 1460, 0, team_id=tid, created_at=now - timedelta(days=60), res_capacity=10_000)
    await _tech(conn, 1460, tools=3)
    await grant_bundle(conn, 1460, {k: v * TEAM_ITEM_CLAN_MULTIPLIER for k, v in cost.items()}, "test")
    await craft(conn, 1460, "dome_12h", now, to_storage=True)                  # команда: ×1
    left = await get_resources(conn, 1460, tuple(cost))
    assert left == {k: v * (TEAM_ITEM_CLAN_MULTIPLIER - 1) for k, v in cost.items()}
    await conn.execute("UPDATE teams SET max_members = 1000 WHERE team_id = $1", tid)
    with pytest.raises(WorkshopError) as e:                                   # Мега-Клан: ×5 — не хватает
        await craft(conn, 1460, "dome_12h", now, to_storage=True)
    assert e.value.key == "ws.err_resources"
    assert await get_resources(conn, 1460, tuple(cost)) == left               # ничего не списано


async def test_duel_win_gives_stone(conn):
    from shared.duels import join_or_create_duel, record_move
    from shared.economy import DUEL_RESOURCE_REWARD
    from shared.resources import get_resources
    await _mk_user(conn, 1470, 100)
    await _mk_user(conn, 1471, 100)
    async with conn.transaction():
        r1 = await join_or_create_duel(conn, 1470, 100)
    async with conn.transaction():
        await join_or_create_duel(conn, 1471, 100)
    async with conn.transaction():
        await record_move(conn, r1.duel_id, 1470, "rock")
    async with conn.transaction():
        await record_move(conn, r1.duel_id, 1471, "scissors")
    assert (await get_resources(conn, 1470, ("stone", "metal"))) == {"stone": DUEL_RESOURCE_REWARD[100], "metal": 0}


async def test_finalize_season_is_idempotent_and_gives_only_badges(conn):
    from datetime import datetime, timezone
    from shared.ledger import change_balance
    from shared.seasons import finalize_season, season_place, season_top, user_badges
    moment = datetime(2026, 10, 15, tzinfo=timezone.utc)
    for i in range(12):
        await _mk_user(conn, 1500 + i, 0)
        await change_balance(conn, 1500 + i, 1000 - i * 10, "mining", "test")
        await conn.execute("UPDATE ledger SET created_at = $2 WHERE user_id = $1", 1500 + i, moment)
    await change_balance(conn, 1500, 5000, "admin_gift", "x")                  # подарок — не заработок
    await conn.execute("UPDATE ledger SET created_at = $1 WHERE reason = 'admin_gift'", moment)
    top = await season_top(conn, moment)
    assert [r["user_id"] for r in top[:3]] == [1500, 1501, 1502] and int(top[0]["earned"]) == 1000
    assert (await season_place(conn, 1503, moment))["place"] == 4

    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('S', 1520, 1) "
                              "RETURNING team_id")
    await _mk_user(conn, 1520, 0, team_id=tid)
    await conn.execute(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, status, results) "
        "VALUES ('B', 'farm', 'farm', $1, $1, 'finished', $2::jsonb)",
        moment, '{"scope": "teams", "places": [{"place": 1, "id": %d, "name": "S", "score": 5}]}' % tid)   # формат v2
    ledger_before = await conn.fetchval("SELECT COUNT(*) FROM ledger")

    res = await finalize_season(conn, moment)
    assert res is not None and len(res["players"]) == 10 and res["teams"][0]["team_id"] == tid
    assert [b["place"] for b in await user_badges(conn, 1500)] == [1]
    assert await user_badges(conn, 1511) == []                                 # 12-й — без значка
    assert await conn.fetchval("SELECT COUNT(*) FROM ledger") == ledger_before  # никаких автопризов
    assert await conn.fetchval("SELECT COUNT(*) FROM resource_ledger") == 0
    assert await finalize_season(conn, moment) is None                         # второй раз — ничего
    assert await finalize_season(conn, datetime(2026, 9, 15, tzinfo=timezone.utc)) is None   # до сезонов


async def test_full_reset_wipes_game_keeps_payments_and_backs_up(conn):
    from shared.database import RESET_ALL_STATEMENT
    await _mk_user(conn, 1550, 777)
    await conn.execute("INSERT INTO ledger (user_id, delta, reason) VALUES (1550, 777, 'test')")
    await conn.execute("INSERT INTO user_tech (user_id, tech, level) VALUES (1550, 'attack', 3)")
    await conn.execute("UPDATE mines SET team_id = 1, captured_at = NOW(), captured_until = NOW(), "
                       "last_paid_at = NOW() WHERE id = 1")
    await conn.execute("INSERT INTO star_payments (telegram_charge_id, user_id, item_payload, stars_amount) "
                       "VALUES ('KEEP_ME', 1550, 'x', 5) ON CONFLICT DO NOTHING")
    await conn.execute("DELETE FROM feature_flags WHERE key = 'migr:full_reset_20261027'")
    await conn.execute("DROP SCHEMA IF EXISTS reset_backup_20261027 CASCADE")
    await conn.execute(RESET_ALL_STATEMENT)
    for t in ("users", "ledger", "user_tech"):
        assert await conn.fetchval(f"SELECT COUNT(*) FROM {t}") == 0, t
    assert await conn.fetchval("SELECT balance FROM reset_backup_20261027.users WHERE user_id = 1550") == 777
    assert await conn.fetchval("SELECT COUNT(*) FROM star_payments WHERE telegram_charge_id = 'KEEP_ME'") == 1
    assert await conn.fetchval("SELECT team_id FROM mines WHERE id = 1") is None
    assert await conn.fetchval("SELECT enabled FROM feature_flags WHERE key = 'migr:full_reset_20261027'")
    await _mk_user(conn, 1551, 5)                                              # разовый: повтор не трогает
    await conn.execute(RESET_ALL_STATEMENT)
    assert await conn.fetchval("SELECT COUNT(*) FROM users") == 1
    await conn.execute("DELETE FROM star_payments WHERE telegram_charge_id = 'KEEP_ME'")


async def test_admin_rewards_resolve_and_give_all(conn):
    from shared.resources import get_resources
    from shared.rewards import give_all, parse_gift, resolve_recipients
    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Gift', 1530, 3) "
                              "RETURNING team_id")
    for uid in (1530, 1531, 1532):
        await _mk_user(conn, uid, 0, team_id=tid)
    await conn.execute("UPDATE users SET username = 'giftee' WHERE user_id = 1531")
    await conn.execute("UPDATE users SET is_blocked = TRUE WHERE user_id = 1532")
    ids, _ = await resolve_recipients(conn, "player", "@giftee")
    assert ids == [1531]
    ids, _ = await resolve_recipients(conn, "player", "1530")
    assert ids == [1530]
    team_ids, _ = await resolve_recipients(conn, "team", "Gift")
    assert sorted(team_ids) == [1530, 1531]                                   # заблокированному — нет
    assert (await resolve_recipients(conn, "player", "@nobody"))[0] == []
    ok, bad = await give_all(conn, team_ids, parse_gift("coins", "250"))
    assert (ok, bad) == (2, 0)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1531") == 250
    assert await conn.fetchval("SELECT COUNT(*) FROM ledger WHERE reason = 'admin_gift'") == 2
    ok, _ = await give_all(conn, [1530], parse_gift("resource", "core 2"))
    assert ok == 1 and (await get_resources(conn, 1530, ("core",)))["core"] == 2
    ok, bad = await give_all(conn, [999_999], parse_gift("coins", "5"))     # нет игрока — сбой, не падение
    assert (ok, bad) == (0, 1)


async def test_resources_v3_migration_grants_veterans_basic_tech(conn):
    from shared.database import SCHEMA_STATEMENTS
    from shared.tech import tech_levels
    await _mk_user(conn, 1540, 0)
    await conn.execute("UPDATE users SET has_shuttle = TRUE WHERE user_id = 1540")
    await conn.execute("DELETE FROM feature_flags WHERE key = 'migr:resources_v3'")
    migr = [s for s in SCHEMA_STATEMENTS if "migr:resources_v3" in s]
    assert len(migr) == 1
    await conn.execute(migr[0])
    lv = await tech_levels(conn, 1540)
    assert (lv["comm"], lv["scout"], lv["attack"]) == (1, 1, 1)
    assert await conn.fetchval("SELECT shuttle_until > NOW() FROM users WHERE user_id = 1540")
    await _mk_user(conn, 1541, 0)
    await conn.execute(migr[0])                                                # разовая: повтор не трогает новых
    assert (await tech_levels(conn, 1541))["attack"] == 0


# ---------------------------------------------------------------- 27.10: битвы v2, призы, пульт
async def _team(conn, tid_name: str, captain: int, members: list[int], clan: bool = False) -> int:
    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count, max_members) VALUES ($1, $2, $3, $4) "
                              "RETURNING team_id", tid_name, captain, len(members), 1000 if clan else 50)
    for uid in members:
        await _mk_user(conn, uid, 0, team_id=tid)
    return tid


async def test_prize_engine_grants_every_kind_once(conn):
    from shared.economy import utcnow
    from shared.prizes import grant, normalize_rewards
    from shared.resources import get_resources
    now = utcnow()
    await _mk_user(conn, 1600, 0, created_at=now)
    rewards = normalize_rewards([
        {"kind": "coins", "amount": 700}, {"kind": "resource", "res": "core", "qty": 3},
        {"kind": "cutlets", "qty": 4}, {"kind": "item", "effect": "shield", "hours": 48, "qty": 2},
        {"kind": "robot", "robot": "premium", "hours": 24 * 365}, {"kind": "boost", "boost": "unlimit", "hours": 24},
        {"kind": "text", "text": "Telegram Premium"}])
    async with conn.transaction():
        assert await grant(conn, 1600, rewards, "TEST_P1_U1600", now)
    async with conn.transaction():
        assert not await grant(conn, 1600, rewards, "TEST_P1_U1600", now)       # повтор по тому же ref — нет
    user = await conn.fetchrow("SELECT balance, inv_cutlets, unlimit_until FROM users WHERE user_id = 1600")
    assert user["balance"] == 700 and user["inv_cutlets"] == 4 and user["unlimit_until"] > now
    assert (await get_resources(conn, 1600, ("core",)))["core"] == 3
    assert await conn.fetchval("SELECT qty FROM user_items WHERE user_id = 1600 AND effect = 'shield' AND hours = 48") == 2
    robot = await conn.fetchrow("SELECT kind, expires_at FROM miners WHERE user_id = 1600")
    assert robot["kind"] == "premium" and robot["expires_at"] > now + __import__("datetime").timedelta(days=364)
    assert await conn.fetchval("SELECT reason FROM ledger WHERE user_id = 1600") == "prize"
    async with conn.transaction():
        assert not await grant(conn, 999_001, rewards, "TEST_NOBODY", now)       # нет игрока — ничего


async def test_battery_entry_rules(conn):
    from datetime import timedelta
    from shared.battles import BattleError, contribute_battery
    from shared.economy import utcnow
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    team = await _team(conn, "Alpha", 1610, [1610, 1611])
    clan = await _team(conn, "Mega", 1612, [1612], clan=True)
    await _mk_user(conn, 1613, 0)                                                  # без команды
    for uid in (1610, 1611, 1612, 1613):
        await grant_bundle(conn, uid, {"battery": 10}, "test")
    bid = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope, places, mine_ids) "
        "VALUES ('B', 'farm_mined', 'x', $1, $2, 'team', 2, ARRAY[1, 2]) RETURNING battle_id", now, now + timedelta(hours=5))
    for uid, key in ((1613, "bt.err_no_team"), (1612, "bt.err_scope")):
        with pytest.raises(BattleError) as e:
            await contribute_battery(conn, bid, uid, now)
        assert e.value.key == key
    for i in range(5):
        res = await contribute_battery(conn, bid, 1610 if i % 2 else 1611, now)
    assert res == {"batteries": 5, "fee": 5, "registered": True}
    with pytest.raises(BattleError) as e:
        await contribute_battery(conn, bid, 1610, now)
    assert e.value.key == "bt.err_full"
    assert (await get_resources(conn, 1610, ("battery",)))["battery"] + (await get_resources(conn, 1611, ("battery",)))["battery"] == 15
    assert await conn.fetchval("SELECT COUNT(*) FROM battle_entry_log WHERE battle_id = $1", bid) == 5
    with pytest.raises(BattleError) as e:                                          # после финиша — закрыто
        await contribute_battery(conn, bid, 1610, now + timedelta(hours=6))
    assert e.value.key == "bt.err_closed"
    solo = await conn.fetchval("INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope) "
                               "VALUES ('S', 'farm_mined', 'x', $1, $2, 'solo') RETURNING battle_id", now, now + timedelta(hours=5))
    with pytest.raises(BattleError) as e:
        await contribute_battery(conn, solo, 1610, now)
    assert e.value.key == "bt.err_no_entry"
    await conn.execute("UPDATE user_resources SET qty = 0 WHERE user_id = 1612 AND kind = 'battery'")
    cbid = await conn.fetchval("INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope, mine_ids) "
                               "VALUES ('C', 'farm_mined', 'x', $1, $2, 'clan', ARRAY[3]) RETURNING battle_id", now, now + timedelta(hours=5))
    with pytest.raises(BattleError) as e:
        await contribute_battery(conn, cbid, 1612, now)
    assert e.value.key == "bt.err_battery"
    assert clan and team


async def test_mine_battle_only_registered_teams_win_mines_and_prizes(conn):
    from datetime import timedelta
    from shared.battles import contribute_battery, finish_battle
    from shared.economy import utcnow
    from shared.ledger import change_balance
    from shared.resources import grant_bundle
    now = utcnow()
    start = now - timedelta(hours=2)
    a = await _team(conn, "Alpha", 1620, [1620, 1621])
    b = await _team(conn, "Bravo", 1622, [1622])
    c = await _team(conn, "Charlie", 1623, [1623])
    bid = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope, places, mine_ids, prizes) "
        "VALUES ('Mines', 'farm_mined', 'x', $1, $2, 'teams', 2, ARRAY[5, 6], $3::jsonb) RETURNING battle_id",
        start, now + timedelta(minutes=30),
        '{"1": [{"kind": "coins", "amount": 300}], "2": [{"kind": "resource", "res": "core", "qty": 1}]}')
    for uid, amount in ((1620, 50), (1621, 50), (1622, 500), (1623, 20)):            # Bravo впереди, но без заявки
        async with conn.transaction():
            await change_balance(conn, uid, amount, "mining", "t")
    for uid in (1620, 1623):
        await grant_bundle(conn, uid, {"battery": 5}, "test")
    for _ in range(5):
        async with conn.transaction():
            await contribute_battery(conn, bid, 1620, now)
            await contribute_battery(conn, bid, 1623, now)
    await conn.execute("UPDATE battles SET ends_at = NOW() + INTERVAL '1 second' WHERE battle_id = $1", bid)
    battle = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", bid)
    res = await finish_battle(conn, battle, now)
    names = [(p["place"], p["name"], p["mine_id"]) for p in res["places"]]
    assert names == [(1, "Alpha", 5), (2, "Charlie", 6)]                              # Bravo без 🔋-заявки не в зачёте
    assert await conn.fetchval("SELECT team_id FROM mines WHERE id = 5") == a
    assert await conn.fetchval("SELECT team_id FROM mines WHERE id = 6") == c
    assert await conn.fetchval("SELECT COUNT(*) FROM ledger WHERE reason = 'prize'") == 2   # обоим бойцам Alpha
    assert await conn.fetchval("SELECT qty FROM user_resources WHERE user_id = 1623 AND kind = 'core'") == 1
    assert (await finish_battle(conn, battle, now)).get("skipped")                    # второй раз — ничего
    assert await conn.fetchval("SELECT COUNT(*) FROM ledger WHERE reason = 'prize'") == 2
    assert b


async def test_solo_and_manual_battles(conn):
    from datetime import timedelta
    from shared.battles import finish_battle
    from shared.economy import utcnow
    from shared.ledger import change_balance
    now = utcnow()
    for uid, amount in ((1630, 30), (1631, 90), (1632, 60)):
        await _mk_user(conn, uid, 0)
        async with conn.transaction():
            await change_balance(conn, uid, amount, "mining", "t")
    await conn.execute("UPDATE users SET username = 'reelstar' WHERE user_id = 1630")
    solo = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope, places, prizes) "
        "VALUES ('Solo', 'farm_mined', 'x', $1, $1, 'solo', 2, $2::jsonb) RETURNING battle_id",
        now - timedelta(hours=1), '{"1": [{"kind": "cutlets", "qty": 7}], "2": [{"kind": "coins", "amount": 1}]}')
    await conn.execute("UPDATE battles SET ends_at = NOW() + INTERVAL '1 second' WHERE battle_id = $1", solo)
    res = await finish_battle(conn, await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", solo), now)
    assert [p["id"] for p in res["places"]] == [1631, 1632]
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 1631") == 7
    manual = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope, places, prizes, manual_results) "
        "VALUES ('Reels', 'insta_reels', 'x', $1, $1, 'solo', 1, $2::jsonb, $3::jsonb) RETURNING battle_id",
        now, '{"1": [{"kind": "resource", "res": "battery", "qty": 2}, {"kind": "text", "text": "iPhone"}]}',
        '{"1": "@ReelStar"}')
    res = await finish_battle(conn, await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", manual), now)
    assert res["places"][0]["name"] == "@reelstar" and res["places"][0]["given"] == 1
    assert await conn.fetchval("SELECT qty FROM user_resources WHERE user_id = 1630 AND kind = 'battery'") == 2


async def test_admin_panel_api_creates_battle_and_gives_rewards(conn, global_db, monkeypatch):
    import json as _j
    import time as _t
    from aiohttp.test_utils import TestClient, TestServer
    from bots.main_bot.webapp import create_webapp
    from shared.webapp_auth import sign_init_data
    token = "123456:TEST"
    monkeypatch.setenv("ADMIN_ID", "1640")
    await _mk_user(conn, 1640, 0)
    await _mk_user(conn, 1641, 0)
    await conn.execute("UPDATE users SET username = 'lucky' WHERE user_id = 1641")
    head = {"X-Telegram-Init-Data": sign_init_data({"auth_date": str(int(_t.time())), "user": {"id": 1640}}, token)}
    client = TestClient(TestServer(create_webapp(token)))
    await client.start_server()
    try:
        meta = await (await client.get("/api/admin/meta", headers=head)).json()
        assert len(meta["mines"]) == 30 and meta["fee"] == {"team": 5, "clan": 25}
        r = await client.post("/api/admin/battle", headers=head, json={
            "title": "Пульт", "title_tpl": {"a": "golden", "n": "cup", "num": 3}, "scope": "teams",
            "nomination": "farm_mined", "starts_at": "now", "hours": 24,
            "places": 2, "mine_ids": [7, 8], "prizes": {"1": [{"kind": "coins", "amount": 100}]}})
        body = await r.json()
        assert r.status == 200 and body["ok"]
        row = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", body["id"])
        assert list(row["mine_ids"]) == [7, 8] and row["announced"] and row["scope"] == "teams"   # анонс — сразу в приложении
        assert _j.loads(row["prizes"])["1"][0]["amount"] == 100
        assert row["title"] == "Золотой кубок 3" and _j.loads(row["title_tpl"])["n"] == "cup"   # 🏷 заготовка
        bad = await client.post("/api/admin/battle", headers=head, json={"title": "x", "scope": "teams",
                                "nomination": "farm_mined", "hours": 5, "places": 1, "mine_ids": [7]})
        assert bad.status == 400                                                   # рудник №7 уже в битве
        r = await client.post("/api/admin/reward", headers=head, json={"target": "player", "value": "@lucky",
                              "rewards": [{"kind": "resource", "res": "core", "qty": 2}]})
        assert (await r.json())["given"] == 1
        assert await conn.fetchval("SELECT qty FROM user_resources WHERE user_id = 1641 AND kind = 'core'") == 2
        r = await client.post("/api/admin/battle/close", headers=head, json={"id": body["id"], "mode": "cancel"})
        assert (await r.json())["ok"]
        assert await conn.fetchval("SELECT status FROM battles WHERE battle_id = $1", body["id"]) == "cancelled"
        vip = await (await client.get("/api/admin/vip", headers=head)).json()
        alias = vip["free"][0]
        r = await client.post("/api/admin/vip/auction", headers=head, json={"alias": alias, "price": 5000, "step": 500, "hours": 24})
        assert (await r.json())["ok"]
        r = await client.post("/api/admin/vip/auction", headers=head, json={"alias": alias, "price": 5000, "step": 500, "hours": 24})
        assert r.status == 400                                                     # уже на аукционе
        auc = await conn.fetchrow("SELECT * FROM auctions WHERE vip_alias = $1", alias)
        assert auc["status"] == "open" and auc["ends_at"] is not None
        r = await client.post("/api/admin/vip/auction", headers=head, json={"kind": "lot", "title": "VIP-пост",
                              "descr": "Пост в Instagram", "price": 1000, "step": 100, "hours": 12})
        lot = await conn.fetchrow("SELECT * FROM auctions WHERE auction_id = $1", (await r.json())["id"])
        assert lot["item_title"] == "VIP-пост" and lot["vip_alias"] is None and lot["min_step"] == 100
    finally:
        await client.close()


async def test_events_api_for_players(conn, global_db):
    import time as _t
    from datetime import timedelta
    from aiohttp.test_utils import TestClient, TestServer
    from bots.main_bot.webapp import create_webapp
    from shared.economy import utcnow
    from shared.resources import grant_bundle
    from shared.webapp_auth import sign_init_data
    token = "123456:TEST"
    now = utcnow()
    tid = await _team(conn, "Echo", 1650, [1650])
    await grant_bundle(conn, 1650, {"battery": 3}, "test")
    bid = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope, places, mine_ids, prizes) "
        "VALUES ('Live', 'farm_mined', 'x', $1, $2, 'teams', 3, ARRAY[11], $3::jsonb) RETURNING battle_id",
        now - timedelta(hours=1), now + timedelta(hours=5), '{"1": [{"kind": "coins", "amount": 50}]}')
    head = {"X-Telegram-Init-Data": sign_init_data({"auth_date": str(int(_t.time())), "user": {"id": 1650}}, token)}
    client = TestClient(TestServer(create_webapp(token)))
    await client.start_server()
    try:
        ev = (await (await client.get("/api/events", headers=head)).json())["events"]
        assert ev[0]["id"] == bid and ev[0]["mines"] == [11] and ev[0]["prizes"][0]["label"] == "50 🪙"
        assert ev[0]["entry"] == {"allowed": True, "batteries": 0, "fee": 5, "registered": False}
        r = await client.post("/api/battle/battery", headers=head, json={"battle_id": bid})
        assert (await r.json())["batteries"] == 1
        mines = await (await client.get("/api/mines", headers=head)).json()
        assert mines["battles"][0]["mine_ids"] == [11] and mines["batteries"] == 2
        assert next(m for m in mines["mines"] if m["id"] == 11)["place"] == 1
    finally:
        await client.close()
    assert tid


# ======================================================================== 🗺 экспедиции и 🤖 дроны (28.10)
async def _exp_target(conn, scope: str, now, hours: float = 48, forks: int = 2, x: float = 80, y: float = 50,
                      prizes: str = '{}', reward_all: str = '[]', places: int = 3) -> int:
    from datetime import timedelta
    return await conn.fetchval(
        "INSERT INTO expedition_targets (title, x, y, scope, forks, resolve_at, places, prizes, reward_all) "
        "VALUES ('Цель', $1, $2, $3, $4, $5, $8, $6::jsonb, $7::jsonb) RETURNING id",
        x, y, scope, forks, now + timedelta(hours=hours), prizes, reward_all, places)


async def test_expedition_solo_forks_and_results(conn):
    from datetime import timedelta
    from shared.economy import EXP_SOLO_HYDROGEN, utcnow
    from shared.expeditions import ExpError, finalize_target, fork_schedule, resolve_due_forks, start_solo, vote
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    tid = await _exp_target(conn, "solo", now, prizes='{"1": [{"kind": "coins", "amount": 500}]}',
                            reward_all='[{"kind": "resource", "res": "stone", "qty": 3}]', places=1)
    for uid in (1700, 1701):
        await _mk_user(conn, uid, 0)
        await grant_bundle(conn, uid, {"hydrogen": 20}, "test")
    await _mk_user(conn, 1702, 0)
    async with conn.transaction():
        res = await start_solo(conn, 1700, tid, now)
    assert res["departed"] and (await get_resources(conn, 1700))["hydrogen"] == 20 - EXP_SOLO_HYDROGEN
    with pytest.raises(ExpError) as e:
        await start_solo(conn, 1700, tid, now)
    assert e.value.key == "exp.err_already"
    with pytest.raises(ExpError) as e:                                # без водорода не выйти
        await start_solo(conn, 1702, tid, now)
    assert e.value.key == "exp.err_hydrogen"
    async with conn.transaction():
        await start_solo(conn, 1701, tid, now)
    e1 = await conn.fetchrow("SELECT * FROM expeditions WHERE user_id = 1700")
    sched = fork_schedule(e1["departed_at"], e1["planned_minutes"], 2)
    async with conn.transaction():                                    # 26.10: выбор заранее, ещё в пути к развилке
        v = await vote(conn, 1700, e1["id"], 1, now + timedelta(seconds=5))
    assert v["fork"] == 1 and not v["resolved"]
    async with conn.transaction():                                    # дошли до развилки — выбор сработал сам
        fresh = await resolve_due_forks(conn, e1["id"], sched[0][0] + timedelta(minutes=1))
    assert fresh["forks_done"] == 1
    log = await conn.fetchrow("SELECT * FROM expedition_log WHERE expedition_id = $1 AND fork_no = 1", e1["id"])
    assert log["option"] == 1 and log["votes"] == 1 and log["created_at"] == sched[0][0]
    with pytest.raises(ExpError) as e:                                # чужой отряд
        await vote(conn, 1701, e1["id"], 0, sched[1][0] + timedelta(minutes=1))
    assert e.value.key == "exp.err_not_member"
    # Отряд 1701 молчит — после закрытия голосования проходит мимо (аудит 1.2: без добычи, потерь и задержки)
    e2 = await conn.fetchrow("SELECT * FROM expeditions WHERE user_id = 1701")
    s2 = fork_schedule(e2["departed_at"], e2["planned_minutes"], 2)
    async with conn.transaction():
        await resolve_due_forks(conn, e2["id"], s2[1][1] + timedelta(minutes=1))
    assert [r["option"] for r in await conn.fetch(
        "SELECT option FROM expedition_log WHERE expedition_id = $1 ORDER BY fork_no", e2["id"])] == [-1, -1]
    target = await conn.fetchrow("SELECT * FROM expedition_targets WHERE id = $1", tid)
    results = await finalize_target(conn, target, target["resolve_at"] + timedelta(minutes=1))
    assert results["arrived"] == 2 and results["late"] == 0
    winner = await conn.fetchval("SELECT user_id FROM expeditions WHERE target_id = $1 "
                                 "ORDER BY cargo DESC, arrive_at, id LIMIT 1", tid)
    assert results["places"][0]["cargo"] == await conn.fetchval("SELECT cargo FROM expeditions WHERE user_id = $1", winner)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", winner) == 500
    loser = 1701 if winner == 1700 else 1700                           # «за участие» — без призового места
    assert (await get_resources(conn, loser, ("stone",)))["stone"] == 3
    assert (await get_resources(conn, winner, ("stone",)))["stone"] == 0
    notes = {n["user_id"]: n for n in results["notices"]}                # 📬 каждому получившему — личное сообщение
    assert notes[winner]["place"] == 1 and not notes[winner]["all"] and notes[winner]["rewards"][0]["amount"] == 500
    assert notes[loser]["all"] and notes[loser]["rewards"][0]["res"] == "stone"
    sent = []

    class _Bot:
        async def send_message(self, uid, text, parse_mode=None):
            sent.append((uid, text))

    class _Pool:
        def acquire(self):
            class _A:
                async def __aenter__(self_inner):
                    return conn

                async def __aexit__(self_inner, *a):
                    return False
            return _A()

    from shared.reward_notify import send_notices
    assert await send_notices(_Bot(), _Pool(), results["notices"]) == 2
    assert any(uid == winner and "500 🪙" in text for uid, text in sent)
    assert (await finalize_target(conn, target, target["resolve_at"]))["skipped"]   # итоги — один раз
    assert set(r["status"] for r in await conn.fetch("SELECT status FROM expeditions WHERE target_id = $1", tid)) == {"done"}


async def test_expedition_too_far_for_the_deadline(conn):
    from shared.economy import utcnow
    from shared.expeditions import ExpError, start_solo
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    tid = await _exp_target(conn, "solo", now, hours=0.3)
    await _mk_user(conn, 1705, 0)
    await grant_bundle(conn, 1705, {"hydrogen": 20}, "test")
    with pytest.raises(ExpError) as e:
        await start_solo(conn, 1705, tid, now)
    assert e.value.key == "exp.err_late"
    assert (await get_resources(conn, 1705))["hydrogen"] == 20         # водород не списан


async def test_expedition_team_gathers_and_votes_by_majority(conn):
    from datetime import timedelta
    from shared.economy import EXP_BATTERIES, utcnow
    from shared.expeditions import ExpError, contribute, finalize_target, fork_schedule, vote
    from shared.resources import grant_bundle
    now = utcnow()
    tid = await _exp_target(conn, "teams", now, hours=72, forks=3, prizes='{"1": [{"kind": "coins", "amount": 300}]}')
    await _team(conn, "Gamma", 1710, [1710, 1711, 1712])
    await _mk_user(conn, 1799, 0)
    await grant_bundle(conn, 1710, {"battery": 10}, "test")
    await grant_bundle(conn, 1711, {"battery": 2}, "test")
    with pytest.raises(ExpError) as e:                                 # котлеты берёт только клан
        await contribute(conn, 1710, tid, "cutlet", now)
    assert e.value.key == "exp.err_no_cutlets_needed"
    with pytest.raises(ExpError) as e:
        await contribute(conn, 1799, tid, "battery", now)
    assert e.value.key == "exp.err_no_team"
    for _ in range(EXP_BATTERIES["team"] - 1):
        async with conn.transaction():
            r = await contribute(conn, 1710, tid, "battery", now)
    assert not r["departed"] and r["batteries"] == EXP_BATTERIES["team"] - 1
    async with conn.transaction():
        r = await contribute(conn, 1711, tid, "battery", now)
    assert r["departed"]                                               # полный комплект — отряд вышел сам
    with pytest.raises(ExpError) as e:
        await contribute(conn, 1711, tid, "battery", now)
    assert e.value.key == "exp.err_departed"
    exp = await conn.fetchrow("SELECT * FROM expeditions WHERE team_id IS NOT NULL")
    t1 = fork_schedule(exp["departed_at"], exp["planned_minutes"], 3)[0][0] + timedelta(minutes=1)
    async with conn.transaction():
        assert not (await vote(conn, 1710, exp["id"], 1, t1))["resolved"]
    async with conn.transaction():
        assert not (await vote(conn, 1711, exp["id"], 1, t1))["resolved"]
    with pytest.raises(ExpError) as e:
        await vote(conn, 1799, exp["id"], 0, t1)
    assert e.value.key == "exp.err_not_member"
    async with conn.transaction():
        assert (await vote(conn, 1712, exp["id"], 2, t1))["resolved"]   # проголосовали все — решение сразу
    log = await conn.fetchrow("SELECT * FROM expedition_log WHERE expedition_id = $1 AND fork_no = 1", exp["id"])
    assert (log["option"], log["votes"]) == (1, 2)                      # решает большинство
    target = await conn.fetchrow("SELECT * FROM expedition_targets WHERE id = $1", tid)
    results = await finalize_target(conn, target, target["resolve_at"])
    assert results["places"][0]["name"] == "Gamma" and results["places"][0]["members"] == 3
    for uid in (1710, 1711, 1712):                                      # вносившие и голосовавшие
        assert await conn.fetchval("SELECT balance FROM users WHERE user_id = $1", uid) == 300


async def test_expedition_clan_needs_cutlets_and_unfinished_gear_returns(conn):
    from shared.economy import EXP_BATTERIES, EXP_CLAN_CUTLETS, utcnow
    from shared.expeditions import cancel_target, contribute, finalize_target, start_solo
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    tid = await _exp_target(conn, "teams", now, hours=72)
    await _team(conn, "Mega", 1720, [1720], clan=True)
    await conn.execute("UPDATE users SET inv_cutlets = 20 WHERE user_id = 1720")
    await grant_bundle(conn, 1720, {"battery": 40}, "test")
    for _ in range(EXP_BATTERIES["clan"]):
        async with conn.transaction():
            r = await contribute(conn, 1720, tid, "battery", now)
    assert not r["departed"]                                            # клану нужен ещё провиант
    for _ in range(EXP_CLAN_CUTLETS):
        async with conn.transaction():
            r = await contribute(conn, 1720, tid, "cutlet", now)
    assert r["departed"] and await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 1720") == 20 - EXP_CLAN_CUTLETS
    # Команда собрала не всё — к итогам батарейки возвращаются
    tid2 = await _exp_target(conn, "team", now, hours=72)
    await _team(conn, "Half", 1730, [1730])
    await grant_bundle(conn, 1730, {"battery": 5}, "test")
    for _ in range(2):
        async with conn.transaction():
            await contribute(conn, 1730, tid2, "battery", now)
    assert (await get_resources(conn, 1730, ("battery",)))["battery"] == 3
    target2 = await conn.fetchrow("SELECT * FROM expedition_targets WHERE id = $1", tid2)
    res = await finalize_target(conn, target2, target2["resolve_at"])
    assert res["arrived"] == 0 and (await get_resources(conn, 1730, ("battery",)))["battery"] == 5
    assert await conn.fetchval("SELECT status FROM expeditions WHERE target_id = $1", tid2) == "refunded"
    # Отмена цели владельцем: водород соло возвращается
    tid3 = await _exp_target(conn, "solo", now, hours=72)
    await _mk_user(conn, 1740, 0)
    await grant_bundle(conn, 1740, {"hydrogen": 10}, "test")
    async with conn.transaction():
        await start_solo(conn, 1740, tid3, now)
    assert await cancel_target(conn, tid3) and not await cancel_target(conn, tid3)
    assert (await get_resources(conn, 1740))["hydrogen"] == 10


async def test_drones_buy_craft_scout_and_raid(conn):
    from datetime import timedelta
    from shared.economy import DRONE_COIN_PRICE, WORKSHOP_RECIPES, raid_candidates, raid_loot, raid_loot_percent, utcnow
    from shared.raids import execute_raid, scout
    from shared.resources import get_resources, grant_bundle
    from shared.workshop import WorkshopError, buy_drone, craft
    now = utcnow()
    old = now - timedelta(days=90)
    await _mk_user(conn, 1750, DRONE_COIN_PRICE + 500, created_at=old, last_seen_at=now, res_capacity=5000)
    async with conn.transaction():
        assert await buy_drone(conn, 1750, "attack") == 1
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1750") == 500
    assert await conn.fetchval("SELECT reason FROM ledger WHERE user_id = 1750 AND delta < 0") == "drone_buy:attack"
    with pytest.raises(WorkshopError) as e:
        await buy_drone(conn, 1750, "attack")
    assert e.value.key == "ws.err_coins"
    # Сборка — как Шаттл: набор 🔬, ресурсы и монеты
    recipe = WORKSHOP_RECIPES["drone_spy"]
    await grant_bundle(conn, 1750, recipe["cost"], "test", cap=5000)
    await conn.execute("UPDATE users SET balance = balance + $1 WHERE user_id = 1750", recipe["coins"])
    with pytest.raises(WorkshopError) as e:
        await craft(conn, 1750, "drone_spy", now)
    assert e.value.key == "tech.err_tool"
    await _tech(conn, 1750, tools=3, comm=1, scout=1, attack=1)
    async with conn.transaction():
        await craft(conn, 1750, "drone_spy", now)
    assert await conn.fetchval("SELECT drones_spy FROM users WHERE user_id = 1750") == 1
    # 🛰 шпион: +1 цель в разведке
    for uid in range(1760, 1768):
        await _mk_user(conn, uid, 0, created_at=old, last_seen_at=now)
        await grant_bundle(conn, uid, {"metal": 100}, "test")
    await grant_bundle(conn, 1750, {"hydrogen": 10}, "test", cap=5000)
    assert len(await scout(conn, 1750, now)) == raid_candidates(1) + 1
    # ⚔️ атакующий дрон налётчика: трофей больше на 5%
    await conn.execute("UPDATE users SET raid_stance = 'scissors' WHERE user_id = 1760")
    res = await execute_raid(conn, 1750, 1760, "rock", now)
    assert res.result == "win" and "drones" in res.notes
    taken = raid_loot(100, raid_loot_percent(1, 0, 0) + 5)
    assert 100 - (await get_resources(conn, 1760))["metal"] == taken


async def test_map_api_shows_targets_and_squads(conn, global_db):
    import time as _t
    from aiohttp.test_utils import TestClient, TestServer
    from bots.main_bot.webapp import create_webapp
    from shared.economy import utcnow
    from shared.resources import grant_bundle
    from shared.webapp_auth import sign_init_data
    token = "123456:TEST"
    now = utcnow()
    tid = await _exp_target(conn, "teams", now, hours=72, prizes='{"1": [{"kind": "bdrone", "drone": "guard", "qty": 1}]}')
    await _team(conn, "Map", 1780, [1780])
    await grant_bundle(conn, 1780, {"battery": 2, "hydrogen": 30}, "test")
    head = {"X-Telegram-Init-Data": sign_init_data({"auth_date": str(int(_t.time())), "user": {"id": 1780}}, token)}
    client = TestClient(TestServer(create_webapp(token)))
    await client.start_server()
    try:
        d = await (await client.get("/api/map", headers=head)).json()
        t = d["targets"][0]
        assert t["id"] == tid and t["prizes"][0]["label"] == "🛡🤖" and [o["mode"] for o in t["options"]] == ["team"]
        assert t["options"][0]["ok"] and d["me"]["in_team"] and d["me"]["batteries"] == 2
        r = await (await client.post("/api/exp/solo", headers=head, json={"target_id": tid})).json()
        assert r["ok"] is False and r["message"]                                   # цель только для команд
        r = await (await client.post("/api/exp/gear", headers=head, json={"target_id": tid, "what": "battery"})).json()
        assert r["ok"] and r["batteries"] == 1
        d = await (await client.get("/api/map", headers=head)).json()
        assert d["my"][0]["status"] == "gathering" and d["squads"][0]["mine"] and d["squads"][0]["name"] == "Map"
    finally:
        await client.close()


async def test_expedition_peek_first_blind_then_min_of_spies_and_scout(conn):
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.expeditions import ExpError, finalize_target, fork_schedule, peek, start_solo
    from shared.resources import grant_bundle
    now = utcnow()
    await _mk_user(conn, 1790, 0, drones_spy=1)
    await _tech(conn, 1790, scout=2)
    await grant_bundle(conn, 1790, {"hydrogen": 30}, "test")
    t1 = await _exp_target(conn, "solo", now, hours=48, forks=3)
    async with conn.transaction():
        await start_solo(conn, 1790, t1, now)
    e1 = await conn.fetchrow("SELECT * FROM expeditions WHERE target_id = $1", t1)
    at = fork_schedule(e1["departed_at"], e1["planned_minutes"], 3)[0][0] + timedelta(minutes=1)
    with pytest.raises(ExpError) as e:                                 # первая экспедиция сезона — вслепую
        await peek(conn, 1790, e1["id"], at)
    assert e.value.key == "exp.err_no_peeks"
    target = await conn.fetchrow("SELECT * FROM expedition_targets WHERE id = $1", t1)
    await finalize_target(conn, target, target["resolve_at"])
    t2 = await _exp_target(conn, "solo", now, hours=48, forks=3, x=200, y=120)
    async with conn.transaction():
        await start_solo(conn, 1790, t2, now + timedelta(minutes=1))
    e2 = await conn.fetchrow("SELECT * FROM expeditions WHERE target_id = $1", t2)
    sched = fork_schedule(e2["departed_at"], e2["planned_minutes"], 3)
    async with conn.transaction():
        assert (await peek(conn, 1790, e2["id"], sched[0][0] + timedelta(minutes=1)))["left"] == 0   # min(1 шпион, разведка 2) = 1
    with pytest.raises(ExpError) as e:
        await peek(conn, 1790, e2["id"], sched[0][0] + timedelta(minutes=2))
    assert e.value.key == "exp.err_peeked"
    async with conn.transaction():
        from shared.expeditions import vote
        await vote(conn, 1790, e2["id"], 0, sched[0][0] + timedelta(minutes=3))
    with pytest.raises(ExpError) as e:                                 # вторая развилка — разведки кончились
        await peek(conn, 1790, e2["id"], sched[1][0] + timedelta(minutes=1))
    assert e.value.key == "exp.err_no_peeks"
    assert await conn.fetchval("SELECT COUNT(*) FROM mines") == 30


async def test_battle_reward_for_taking_part_goes_to_everyone_without_a_prize_place(conn):
    """28.10 ночью: места 1…N — призы владельца, остальным в зачёте — награда «за участие» (командам — каждому бойцу)."""
    from datetime import timedelta
    from shared.battles import finish_battle
    from shared.economy import utcnow
    from shared.ledger import change_balance
    now = utcnow()
    await _team(conn, "Gold", 1810, [1810])
    await _team(conn, "Silver", 1811, [1811, 1812])
    await _team(conn, "Bronze", 1813, [1813])
    bid = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, scope, places, prizes, reward_all) "
        "VALUES ('Cup', 'farm_mined', 'x', $1, $2, 'teams', 1, $3::jsonb, $4::jsonb) RETURNING battle_id",
        now - timedelta(hours=2), now + timedelta(minutes=5),
        '{"1": [{"kind": "coins", "amount": 1000}]}', '[{"kind": "resource", "res": "stone", "qty": 7}]')
    for uid, amount in ((1810, 90), (1811, 40), (1812, 10), (1813, 5)):
        async with conn.transaction():
            await change_balance(conn, uid, amount, "mining", "t")
    battle = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", bid)
    res = await finish_battle(conn, battle, now + timedelta(minutes=6))
    assert [p["name"] for p in res["places"]] == ["Gold"] and res["participants_rewarded"] == 3
    stone = {r["user_id"]: r["qty"] for r in await conn.fetch("SELECT user_id, qty FROM user_resources WHERE kind = 'stone'")}
    assert stone == {1811: 7, 1812: 7, 1813: 7}                           # призёр получил приз, а не «за участие»
    assert sorted((n["user_id"], n["all"]) for n in res["notices"]) == [(1810, False), (1811, True), (1812, True), (1813, True)]
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1810") == 90 + 1000


async def test_auction_bids_refund_outbid_and_list(conn):
    """🔨 26.10: ставки из приложения и чата — одна функция; перебитому взнос возвращается целиком."""
    from shared.auctions import AuctionError, list_auctions, place_bid
    await _mk_user(conn, 1900, 10_000)
    await _mk_user(conn, 1901, 10_000)
    aid = await conn.fetchval("INSERT INTO auctions (item_title, item_desc, current_price, min_step, status, ends_at) "
                              "VALUES ('Лот', 'x', 1000, 100, 'open', NOW() + INTERVAL '1 day') RETURNING auction_id")
    async with conn.transaction():
        r1 = await place_bid(conn, 1900, aid, 100)
    assert r1["price"] == 1100 and r1["charge"] == 1100 and r1["previous_bidder_id"] is None
    async with conn.transaction():
        r2 = await place_bid(conn, 1901, aid, 500)
    assert r2["price"] == 1600 and r2["previous_bidder_id"] == 1900 and r2["refund"] == 1100
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1900") == 10_000   # взнос вернулся
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1901") == 10_000 - 1600
    async with conn.transaction():
        r3 = await place_bid(conn, 1901, aid, 100)                        # лидер доплачивает только шаг
    assert r3["charge"] == 100 and await conn.fetchval("SELECT balance FROM users WHERE user_id = 1901") == 10_000 - 1700
    for step, key in ((150, "auc.err_step"), (100_000, "auc.err_funds")):
        with pytest.raises(AuctionError) as e:
            await place_bid(conn, 1900, aid, step)
        assert e.value.key == key
    lots = await list_auctions(conn, 1901)
    assert lots[0]["id"] == aid and lots[0]["mine"] and lots[0]["price"] == 1700 and lots[0]["bids"] == [100, 500]
    await conn.execute("UPDATE auctions SET ends_at = NOW() - INTERVAL '1 second' WHERE auction_id = $1", aid)
    with pytest.raises(AuctionError) as e:                                 # время вышло, демон ещё не закрыл
        await place_bid(conn, 1900, aid, 100)
    assert e.value.key == "auc.err_closed"
    await conn.execute("UPDATE auctions SET status = 'closed' WHERE auction_id = $1", aid)
    with pytest.raises(AuctionError) as e:
        await place_bid(conn, 1900, aid, 100)
    assert e.value.key == "auc.err_closed"


async def test_history_api_shows_coins_resources_market_and_gifts(conn, global_db):
    """📜 26.10: история за 30 дней — монеты со сводкой, ресурсы, сделки биржи, награды; чужое не видно."""
    import time as _t
    from datetime import timedelta
    from aiohttp.test_utils import TestClient, TestServer
    from bots.main_bot.webapp import create_webapp
    from shared.economy import utcnow
    from shared.ledger import change_balance
    from shared.prizes import grant
    from shared.resources import change_resource
    from shared.webapp_auth import sign_init_data
    token = "123456:TEST"
    await _mk_user(conn, 1950, 0)
    await _mk_user(conn, 1951, 0)
    async with conn.transaction():
        await change_balance(conn, 1950, 300, "mining")
        await change_balance(conn, 1950, 2, "game_win:quiz")
        await change_balance(conn, 1950, -100, "horse_buy", "1")
        await change_balance(conn, 1951, 999, "mining")                              # чужое
        await change_resource(conn, 1950, "metal", 5, "raid_loot", "1")
        await conn.execute("INSERT INTO market_trades (asset, qty, price, buyer_id, seller_id) VALUES ('metal', 3, 20, 1951, 1950)")
        await grant(conn, 1950, [{"kind": "resource", "res": "battery", "qty": 10}], "E7_P1_U1950", utcnow())
        await conn.execute("INSERT INTO ledger (user_id, delta, reason, created_at) VALUES (1950, 50, 'mining', $1)",
                           utcnow() - timedelta(days=40))                             # старше 30 дней — не видно
    head = {"X-Telegram-Init-Data": sign_init_data({"auth_date": str(int(_t.time())), "user": {"id": 1950}}, token)}
    client = TestClient(TestServer(create_webapp(token)))
    await client.start_server()
    try:
        coins = await (await client.get("/api/history?tab=coins", headers=head)).json()
        assert sorted(x["delta"] for x in coins["items"]) == [-100, 2, 300]
        assert coins["summary"]["income"] == 302 and coins["summary"]["spent"] == 100
        assert coins["summary"]["top_in"][0]["sum"] == 300
        res = await (await client.get("/api/history?tab=res", headers=head)).json()
        assert {(x["kind"], x["delta"]) for x in res["items"]} >= {("metal", 5), ("battery", 10)}
        market = await (await client.get("/api/history?tab=market", headers=head)).json()
        assert market["items"][0]["side"] == "sell" and market["items"][0]["total"] == 60
        gifts = await (await client.get("/api/history?tab=gifts", headers=head)).json()
        assert gifts["items"][0]["what"] == "10 🔋"
    finally:
        await client.close()


async def test_quiz_next_question_skips_seen_and_starts_new_lap(conn, global_db, monkeypatch):
    """Викторина без повторов: просмотренные вопросы пишутся в quiz_seen, пройденная база — новый круг."""
    from bots.main_bot.handlers import games
    from bots.main_bot.utils import questions_loader as ql
    await _mk_user(conn, 1995, 0)
    await conn.execute("DELETE FROM quiz_seen WHERE user_id = 1995")
    pack = [{"id": i, "key": f"k{i}", "category": "x", "q": f"q{i}", "correct": "a", "options": ["a", "b", "c", "d"]}
            for i in (1, 2, 3)]
    monkeypatch.setattr(ql, "_questions", pack)
    got = [(await games._next_question(1995))["key"] for _ in range(3)]
    assert sorted(got) == ["k1", "k2", "k3"]                     # три вопроса — три разных
    assert await conn.fetchval("SELECT COUNT(*) FROM quiz_seen WHERE user_id = 1995") == 3
    await games._next_question(1995)                              # база пройдена — круг заново
    assert await conn.fetchval("SELECT COUNT(*) FROM quiz_seen WHERE user_id = 1995") == 1


async def test_lazy_farm_never_moves_time_backwards(conn):
    """Аудит 1.4: «сейчас», взятое до блокировки, раньше откатывало время фермы — отрезок начислялся дважды."""
    from datetime import timedelta
    from shared.economy import utcnow
    from shared.farm_logic import apply_lazy_farm
    now = utcnow()
    await _mk_user(conn, 21, 0)
    await conn.execute("UPDATE users SET last_update_time = $1 WHERE user_id = 21", now - timedelta(hours=10))
    await conn.execute("INSERT INTO miners (user_id, kind, purchased_at, expires_at) VALUES (21, 'junior', $1, $2)",
                       now - timedelta(hours=10), now + timedelta(days=29))
    async with conn.transaction():
        await apply_lazy_farm(conn, 21, now)                           # 10 ч × 5 = 50
    async with conn.transaction():
        user, _ = await apply_lazy_farm(conn, 21, now - timedelta(hours=2))   # «старое сейчас» — ничего не меняет
    assert user["last_update_time"] == now
    async with conn.transaction():
        user, _ = await apply_lazy_farm(conn, 21, now + timedelta(hours=1))
    assert user["balance"] == 55                                       # +1 ч, без повтора двух часов



async def test_expedition_finish_now_keeps_marching_squads_and_survives_restart(conn):
    """Аудит 1.1/1.3: «Итоги сейчас» не делает опоздавшими тех, кто успевал к плановому часу; зависшие итоги доделываются."""
    from datetime import timedelta
    from shared.economy import FINISH_RETRY_MINUTES, utcnow
    from shared.expeditions import finalize_target, start_solo
    from shared.resources import grant_bundle
    now = utcnow()
    tid = await _exp_target(conn, "solo", now, prizes='{"1": [{"kind": "coins", "amount": 300}]}', places=1)
    await _mk_user(conn, 1710, 0)
    await grant_bundle(conn, 1710, {"hydrogen": 20}, "test")
    async with conn.transaction():
        await start_solo(conn, 1710, tid, now)
    # Владелец жмёт «Итоги сейчас», отряд ещё в пути (как делает пульт)
    await conn.execute("UPDATE expedition_targets SET planned_resolve_at = COALESCE(planned_resolve_at, resolve_at), "
                       "resolve_at = LEAST(resolve_at, $2) WHERE id = $1", tid, now + timedelta(minutes=1))
    # Сбой посреди итогов: статус «подводятся», наград ещё нет
    await conn.execute("UPDATE expedition_targets SET status = 'finishing', finishing_at = $2 WHERE id = $1",
                       tid, now)
    target = await conn.fetchrow("SELECT * FROM expedition_targets WHERE id = $1", tid)
    assert (await finalize_target(conn, target, now + timedelta(minutes=2)))["skipped"]   # свежий захват — не трогаем
    later = now + timedelta(minutes=FINISH_RETRY_MINUTES + 1)
    results = await finalize_target(conn, target, later)                                     # повтор после рестарта
    assert results["arrived"] == 1 and results["late"] == 0
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1710") == 300
    assert await conn.fetchval("SELECT status FROM expedition_targets WHERE id = $1", tid) == "finished"
    assert (await finalize_target(conn, target, later + timedelta(hours=1)))["skipped"]      # дважды не выдаётся


async def test_battle_entries_refund_on_cancel_and_incomplete(conn):
    """Аудит 1.7: батарейки заявки возвращаются при отмене битвы и командам с неполной заявкой."""
    from datetime import timedelta
    from shared.battles import contribute_battery, finish_battle, refund_entries
    from shared.economy import utcnow
    from shared.resources import get_resources, grant_bundle
    now = utcnow()
    for uid in (1720, 1721):
        await _mk_user(conn, uid, 0)
        await grant_bundle(conn, uid, {"battery": 5}, "test")
    t1 = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('R1', 1720, 1) "
                             "RETURNING team_id")
    t2 = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('R2', 1721, 1) "
                             "RETURNING team_id")
    await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = 1720", t1)
    await conn.execute("UPDATE users SET team_id = $1 WHERE user_id = 1721", t2)
    bid = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, status, scope, places, mine_ids) "
        "VALUES ('Руда', 'farm_mined', 'x', $1, $2, 'active', 'teams', 1, ARRAY[3]) RETURNING battle_id",
        now - timedelta(hours=1), now + timedelta(hours=1))
    for _ in range(5):
        async with conn.transaction():
            await contribute_battery(conn, bid, 1720, now)                # полная заявка
    for _ in range(2):
        async with conn.transaction():
            await contribute_battery(conn, bid, 1721, now)                # неполная
    battle = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", bid)
    await finish_battle(conn, battle, now + timedelta(hours=2))
    assert (await get_resources(conn, 1721, ("battery",)))["battery"] == 5    # неполная — вернулась
    assert (await get_resources(conn, 1720, ("battery",)))["battery"] == 0    # полная — сгорела как взнос
    assert await refund_entries(conn, bid, only_incomplete=True) == 0         # повтор — ничего
    assert await conn.fetchval("SELECT status FROM battles WHERE battle_id = $1", bid) == "finished"



async def test_market_newbie_price_cap_and_cancel_needs_room(conn):
    """Аудит 2.3/2.5: новый аккаунт не переплачивает основному; эскроу — не бесплатный склад."""
    from shared.economy import MARKET_NEWBIE_PRICE_MULT, market_min_price
    from shared.market import MarketError, cancel_order, fill_order, place_order
    from shared.resources import grant_bundle
    await _mk_user(conn, 1800, 0)                       # «основной» аккаунт
    await _mk_user(conn, 1801, 100_000)                 # фейк: новый, с монетами
    await grant_bundle(conn, 1800, {"parts": 10}, "test")
    cap = market_min_price("parts") * MARKET_NEWBIE_PRICE_MULT
    pricey = await place_order(conn, 1800, "parts", "sell", 1, 500)
    with pytest.raises(MarketError) as e:
        await fill_order(conn, 1801, pricey, 1)
    assert e.value.key == "mk.err_newbie_price"
    with pytest.raises(MarketError) as e:               # и заявка на покупку тоже
        await place_order(conn, 1801, "parts", "buy", 1, 500)
    assert e.value.key == "mk.err_newbie_price"
    fair = await place_order(conn, 1800, "parts", "sell", 1, cap)
    assert (await fill_order(conn, 1801, fair, 1))["total"] == cap       # по честной цене — можно
    await conn.execute("INSERT INTO game_stats (user_id, quiz_level) VALUES (1801, 3)")
    await conn.execute("UPDATE users SET bonus_claims = 3 WHERE user_id = 1801")
    assert (await fill_order(conn, 1801, pricey, 1))["total"] == 500     # активный — по любой цене
    # Снять ордер можно, только если товар влезет на склад
    await grant_bundle(conn, 1800, {"metal": 400}, "test")
    order = await place_order(conn, 1800, "metal", "sell", 400, 100)
    await grant_bundle(conn, 1800, {"metal": 400}, "test")
    with pytest.raises(MarketError) as e:
        await cancel_order(conn, 1800, order)
    assert e.value.key == "mk.err_cancel_room"
    assert await cancel_order(conn, 1800, order, system=True) == 400     # выход из команды / удаление — без лимита


async def test_team_newcomer_gets_no_battle_prize_for_24h(conn):
    """Аудит 2.7: перешёл в команду перед итогами — ни очков команде, ни приза."""
    from datetime import timedelta
    from shared.battles import finish_battle
    from shared.economy import utcnow
    from shared.ledger import change_balance
    now = utcnow()
    tid = await conn.fetchval("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Vet', 1810, 2) "
                              "RETURNING team_id")
    await _mk_user(conn, 1810, 0, team_id=tid, team_joined_at=now - timedelta(days=3))     # старожил
    await _mk_user(conn, 1811, 0, team_id=tid, team_joined_at=now - timedelta(hours=1))    # перебежчик
    bid = await conn.fetchval(
        "INSERT INTO battles (title, nomination_key, nomination_text, starts_at, ends_at, status, scope, places, prizes) "
        "VALUES ('Заработок', 'coins_earned', 'x', $1, $2, 'active', 'teams', 1, $3::jsonb) RETURNING battle_id",
        now - timedelta(hours=2), now + timedelta(minutes=5), '{"1": [{"kind": "coins", "amount": 100}]}')
    await change_balance(conn, 1810, 10, "game_win:rps")
    await change_balance(conn, 1811, 5000, "game_win:rps")          # очки перебежчика команде не идут
    battle = await conn.fetchrow("SELECT * FROM battles WHERE battle_id = $1", bid)
    res = await finish_battle(conn, battle, now + timedelta(minutes=6))
    assert res["places"][0]["score"] == 10
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1810") == 110
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 1811") == 5000


async def test_app_games_api_rounds_limits_hint_and_timer(conn, global_db):
    """🕹 26.10: игры в приложении — те же движки и лимиты; секреты на сервере; раунд закрывается один раз."""
    import time as _t
    from datetime import timedelta
    from aiohttp.test_utils import TestClient, TestServer
    from bots.main_bot.webapp import create_webapp
    from shared.economy import QUIZ_ANSWER_SECONDS, QUIZ_HINT_COST
    from shared.webapp_auth import sign_init_data
    token = "123456:TEST"
    await _mk_user(conn, 1830, 1000)
    head = {"X-Telegram-Init-Data": sign_init_data({"auth_date": str(int(_t.time())), "user": {"id": 1830}}, token)}
    client = TestClient(TestServer(create_webapp(token)))
    await client.start_server()
    try:
        hub = await (await client.get("/api/games", headers=head)).json()
        assert {g["id"] for g in hub["games"]} == {"rps", "hl", "quiz", "safe"} and hub["quiz"]["seconds"] == 30
        r = await (await client.post("/api/games/rps", headers=head, json={"move": "rock"})).json()
        assert r["ok"] and r["bot"] in ("rock", "paper", "scissors") and r["result"] in ("win", "lose", "draw")
        s = await (await client.post("/api/games/safe", headers=head, json={"guess": 2})).json()
        assert s["ok"] and 1 <= s["code"] <= 4 and (s["result"] == "win") == (s["code"] == 2)
        h = await (await client.post("/api/games/hl/new", headers=head, json={})).json()
        assert "secret" not in h                                            # загаданное не уходит в браузер
        p = await (await client.post("/api/games/hl/play", headers=head, json={"round_id": h["round_id"], "dir": "up"})).json()
        assert p["base"] == h["base"] and (p["result"] == "win") == (p["secret"] > h["base"])
        again = await (await client.post("/api/games/hl/play", headers=head, json={"round_id": h["round_id"], "dir": "up"})).json()
        assert again["ok"] is False                                         # раунд закрывается один раз
        q = await (await client.post("/api/quiz/next", headers=head, json={})).json()
        assert q["ok"] and len(q["options"]) == 4 and "correct" not in q
        bal = await conn.fetchval("SELECT balance FROM users WHERE user_id = 1830")
        hint = await (await client.post("/api/quiz/hint", headers=head, json={"round_id": q["round_id"]})).json()
        assert len(hint["removed"]) == 2 and hint["balance"] == bal - QUIZ_HINT_COST
        state = await conn.fetchval("SELECT state FROM game_rounds WHERE id = $1", q["round_id"])
        import json as _j
        correct = (_j.loads(state) if isinstance(state, str) else state)["correct"]
        assert correct not in hint["removed"]
        a = await (await client.post("/api/quiz/answer", headers=head, json={"round_id": q["round_id"], "option": correct})).json()
        assert a["result"] == "win" and a["info"]["reward"] == 2 and a["info"]["res"]["kind"] == "crystal"
        # Опоздал — ответ не засчитан, даже верный
        q2 = await (await client.post("/api/quiz/next", headers=head, json={})).json()
        await conn.execute("UPDATE game_rounds SET created_at = created_at - $2::interval WHERE id = $1",
                           q2["round_id"], timedelta(seconds=QUIZ_ANSWER_SECONDS + 10))
        st2 = await conn.fetchval("SELECT state FROM game_rounds WHERE id = $1", q2["round_id"])
        right2 = (_j.loads(st2) if isinstance(st2, str) else st2)["correct"]
        late = await (await client.post("/api/quiz/answer", headers=head, json={"round_id": q2["round_id"], "option": right2})).json()
        assert late["result"] == "timeout"
        # Лимит побед: игра не начинается
        from shared.economy import utcnow
        await conn.execute("UPDATE game_stats SET daily_wins_safe = 15, last_game_date = $1 WHERE user_id = 1830",
                           utcnow().date())
        lim = await (await client.post("/api/games/safe", headers=head, json={"guess": 1})).json()
        assert lim["ok"] is False and lim["limit"]
        # Тумблер «игры» выключен в пульте — API приложения закрыто (раньше проверка не срабатывала:
        # пустой aiohttp-ответ «ложный» в if, и тумблеры в приложении не действовали)
        from shared.feature_flags import invalidate_cache, set_flag
        await set_flag("games", False)
        try:
            off = await client.get("/api/games", headers=head)
            assert off.status == 503
        finally:
            await set_flag("games", True)
            invalidate_cache()
    finally:
        await client.close()
