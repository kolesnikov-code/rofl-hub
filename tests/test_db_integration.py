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
from shared.economy import START_BALANCE, REFERRAL_SIGNUP_BONUS  # noqa: E402
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
                        "team_stations, team_donations, market_trades, resource_swaps RESTART IDENTITY")
        yield c
    await database.close()


async def _mk_user(conn, user_id: int, balance: int = 0, **cols):
    extra_cols = "".join(f", {k}" for k in cols)
    extra_vals = "".join(f", ${i + 3}" for i in range(len(cols)))
    await conn.execute(
        f"INSERT INTO users (user_id, username, balance{extra_cols}) VALUES ($1, 'u', $2{extra_vals})",
        user_id, balance, *cols.values())


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
async def test_register_user_gives_bonus_to_referrer_once(conn):
    from bots.main_bot.handlers.start import register_user
    await _mk_user(conn, 10, 0)
    assert await register_user(conn, 11, "new", "en", referrer_id=10) is True
    assert await register_user(conn, 11, "new", "en", referrer_id=10) is False
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 10") == REFERRAL_SIGNUP_BONUS
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
    from datetime import date, timedelta
    from bots.main_bot.handlers.games import execute_solo_game_payout
    await _mk_user(conn, 32, 0)
    await conn.execute(
        "INSERT INTO game_stats (user_id, daily_wins_rps, daily_wins_hl, daily_wins_quiz, "
        "daily_wins_safe, last_game_date) "
        "VALUES (32, 15, 15, 30, 15, $1)", date.today() - timedelta(days=1))

    ok, text, balance = await execute_solo_game_payout(32, True, "safe")  # вчерашний лимит не мешает

    assert ok and balance == 5
    stats = await conn.fetchrow("SELECT * FROM game_stats WHERE user_id = 32")
    assert stats["daily_wins_safe"] == 1
    for col in ("daily_wins_rps", "daily_wins_hl", "daily_wins_quiz"):
        assert stats[col] == 0, col


async def test_daily_limit_blocks_win_for_new_games(conn, global_db):
    pytest.importorskip("aiogram")
    from datetime import date
    from bots.main_bot.handlers.games import execute_solo_game_payout
    await _mk_user(conn, 33, 0)
    await conn.execute(
        "INSERT INTO game_stats (user_id, daily_wins_safe, last_game_date) VALUES (33, 15, $1)", date.today())

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


async def test_transfer_moves_coins_and_writes_ledger(conn):
    from shared.transfers import transfer_coins
    await _mk_user(conn, 60, 1000)
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


async def test_battle_prize_delivery_to_every_member_is_idempotent(conn):
    from shared.battles import award_sku_to_team
    from bots.main_bot.catalog import get_item
    await conn.execute("INSERT INTO teams (team_name, captain_id, members_count) VALUES ('Win', 110, 2)")
    team_id = await conn.fetchval("SELECT team_id FROM teams WHERE team_name = 'Win'")
    await _mk_user(conn, 110, 0, team_id=team_id)
    await _mk_user(conn, 111, 0, team_id=team_id)

    order = {**get_item("cutlet_10"), "stars": 0}  # призы не считаются продажами
    delivered, skipped = await award_sku_to_team(conn, team_id, "cutlet_10", order, battle_id=1, place=1)
    assert (delivered, skipped) == (2, 0)
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 110") == 10

    # Повторная выдача (например, повторный вызов finish) не задвоит призы
    delivered2, skipped2 = await award_sku_to_team(conn, team_id, "cutlet_10", order, battle_id=1, place=1)
    assert delivered2 == 0 and skipped2 == 2
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 110") == 10
    assert await conn.fetchval(
        "SELECT COALESCE(SUM(stars_amount), 0) FROM star_payments") == 0


# ---------------------------------------------------------------- VIP ID
async def test_transfer_by_vip_alias(conn):
    from shared.transfers import transfer_coins
    await _mk_user(conn, 120, 500)
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
    """Две конкурентные транзакции доводят друга до 30 раундов — бонус строго один."""
    import asyncio
    from shared.analytics import qualify_referral_if_due
    from shared.economy import REFERRAL_QUALIFIED_BONUS, REFERRAL_QUALIFY_ROUNDS

    database = Database()
    await database.connect(TEST_DSN)
    await database.create_tables()
    try:
        async with database.pool.acquire() as c:
            await c.execute("TRUNCATE users, ledger, events, daily_activity RESTART IDENTITY")
            await _mk_user(c, 100, 0)
            await _mk_user(c, 101, 0, referred_by=100)

        async def attempt():
            async with database.pool.acquire() as c:
                async with c.transaction():
                    return await qualify_referral_if_due(c, 101, REFERRAL_QUALIFY_ROUNDS)

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


async def test_referral_qualification_needs_threshold_and_referrer(conn):
    from shared.analytics import qualify_referral_if_due
    from shared.economy import REFERRAL_QUALIFY_ROUNDS

    await _mk_user(conn, 110, 0)
    await _mk_user(conn, 111, 0, referred_by=110)
    assert await qualify_referral_if_due(conn, 111, REFERRAL_QUALIFY_ROUNDS - 1) is None
    await _mk_user(conn, 112, 0)   # игрок без реферера
    assert await qualify_referral_if_due(conn, 112, 999) is None
    assert await conn.fetchval(
        "SELECT COUNT(*) FROM ledger WHERE reason = 'referral_qualified'") == 0


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


async def test_tenth_intellect_level_grants_extra_intern(conn, global_db):
    """Закрытие 10-го уровня викторины выдаёт ещё одного Робота Стажёра."""
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.games import execute_solo_game_payout
    await _mk_user(conn, 310, 0)
    await conn.execute(
        "INSERT INTO game_stats (user_id, quiz_level, quiz_level_progress) VALUES (310, 9, 99)")
    ok, text, _ = await execute_solo_game_payout(310, True, "quiz")
    assert ok and "Стажёр" in text
    interns = await conn.fetch("SELECT kind FROM miners WHERE user_id = 310")
    assert [r["kind"] for r in interns] == ["intern"]
    assert await conn.fetchval("SELECT quiz_level FROM game_stats WHERE user_id = 310") == 10


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
async def test_game_win_mines_resource_and_ledger_blocks_negative(conn, global_db):
    pytest.importorskip("aiogram")
    from bots.main_bot.handlers.games import execute_solo_game_payout
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


async def test_workshop_crafts_spend_all_or_nothing(conn):
    from datetime import timedelta
    from shared.economy import ARMOR_MAX_LEVEL, utcnow
    from shared.resources import get_resources, grant_bundle
    from shared.workshop import WorkshopError, craft
    now = utcnow()
    await _mk_user(conn, 510, 0)
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
    assert (await craft(conn, 510, "cutlet", now)).qty == 1
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 510") == 1


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
    from shared.economy import MARKET_CUTLET_MIN_PRICE, utcnow
    from shared.market import (MarketError, cancel_order, fill_order, index_change, place_order,
                               price_history)
    from shared.resources import get_resources, grant_bundle
    await _mk_user(conn, 900, 10_000, inv_cutlets=10, has_shuttle=True)   # продавец с Шаттлом
    await _mk_user(conn, 901, 10_000)                                     # покупатель без Шаттла
    await grant_bundle(conn, 900, {"metal": 500}, "test")

    # Пол цены котлеты действует для обеих сторон
    for side in ("sell", "buy"):
        with pytest.raises(MarketError) as e:
            await place_order(conn, 900 if side == "sell" else 901, "cutlet", side, 1, MARKET_CUTLET_MIN_PRICE - 1)
        assert e.value.key == "mk.err_price"

    # Заявка на покупку металла: монеты замораживаются сразу
    bid = await place_order(conn, 901, "metal", "buy", 100, 3)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 901") == 10_000 - 300
    # Продавец с Шаттлом закрывает заявку: комиссия 5% с ЕГО продажи
    deal = await fill_order(conn, 900, bid, 100)
    assert (deal["side"], deal["fee"], deal["seller_got"]) == ("buy", 15, 285)
    assert (await get_resources(conn, 901))["metal"] == 100
    assert (await get_resources(conn, 900))["metal"] == 400
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 900") == 10_000 + 285

    # Продажа котлет игроком без Шаттла покупателю с Шаттлом: комиссия обычная (Шаттл не «одалживается»)
    ask = await place_order(conn, 901, "metal", "sell", 50, 4)
    deal2 = await fill_order(conn, 900, ask, 50)
    assert (deal2["side"], deal2["fee"]) == ("sell", 20)
    assert await conn.fetchval("SELECT inv_cutlets FROM users WHERE user_id = 900") == 10

    # Отмена заявки возвращает замороженные монеты; ордер на продажу — товар
    bid2 = await place_order(conn, 901, "cutlet", "buy", 2, MARKET_CUTLET_MIN_PRICE)
    balance = await conn.fetchval("SELECT balance FROM users WHERE user_id = 901")
    await cancel_order(conn, 901, bid2)
    assert await conn.fetchval("SELECT balance FROM users WHERE user_id = 901") == balance + 2 * MARKET_CUTLET_MIN_PRICE
    with pytest.raises(MarketError) as e:
        await place_order(conn, 901, "metal", "sell", 999, 5)    # у 901 осталось 50 металла
    assert e.value.key == "mk.err_no_resource"

    # История сделок и индекс
    hist = await price_history(conn, "metal", utcnow())
    assert len(hist) == 7 and hist[-1]["volume"] == 150
    assert index_change(hist)["last"] == round((100 * 3 + 50 * 4) / 150, 1)
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

    swap2 = await create_swap(conn, 910, "metal", 40, "parts", 1)
    await cancel_swap(conn, 910, swap2)
    assert (await get_resources(conn, 910))["metal"] == 40
