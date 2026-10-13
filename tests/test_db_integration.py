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
                        "miners, duels, battles, vip_aliases RESTART IDENTITY")
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
async def test_all_18_items_deliver(conn):
    from bots.main_bot.catalog import CATALOG
    await _mk_user(conn, 3, 0)
    await conn.execute("INSERT INTO teams (team_name, captain_id) VALUES ('t', 3)")
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
    assert kinds == ["junior", "premium"]
    expiry = await conn.fetchval("SELECT MIN(expires_at - purchased_at) FROM miners WHERE user_id = 3")
    assert expiry.days == 30
    assert u["boost_nuclear_until"] and u["boost_nitrogen_until"] and u["drone_until"] and u["unlimit_until"]
    assert await conn.fetchval("SELECT max_members FROM teams WHERE captain_id = 3") == 1000
    assert await conn.fetchval("SELECT COUNT(*) FROM star_payments WHERE user_id = 3") == 18


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


async def test_new_day_resets_all_six_win_counters(conn, global_db):
    pytest.importorskip("aiogram")
    from datetime import date, timedelta
    from bots.main_bot.handlers.games import execute_solo_game_payout
    await _mk_user(conn, 32, 0)
    await conn.execute(
        "INSERT INTO game_stats (user_id, daily_wins_rps, daily_wins_hl, daily_wins_quiz, "
        "daily_wins_coin, daily_wins_dice, daily_wins_safe, last_game_date) "
        "VALUES (32, 15, 15, 30, 15, 15, 15, $1)", date.today() - timedelta(days=1))

    ok, text, balance = await execute_solo_game_payout(32, True, "coin")  # вчерашний лимит не мешает

    assert ok and balance == 2
    stats = await conn.fetchrow("SELECT * FROM game_stats WHERE user_id = 32")
    assert stats["daily_wins_coin"] == 1
    for col in ("daily_wins_rps", "daily_wins_hl", "daily_wins_quiz", "daily_wins_dice", "daily_wins_safe"):
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
