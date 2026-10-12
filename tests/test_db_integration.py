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
        await c.execute("TRUNCATE users, teams, star_payments, game_stats, auctions, ledger RESTART IDENTITY")
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
    assert u["miner_junior_count"] == 1 and u["miner_premium_count"] == 1
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
