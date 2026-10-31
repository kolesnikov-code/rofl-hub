"""Оплата за Stars после списания денег: авто-возврат при ошибке каталога, повтор апдейта без возврата (аудит 1.6)."""
import os
from types import SimpleNamespace

import pytest

os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
pytest.importorskip("aiogram")

from bots.main_bot.catalog import CatalogError  # noqa: E402
from bots.main_bot.handlers import payments  # noqa: E402


class _Acquire:
    async def __aenter__(self):
        return object()

    async def __aexit__(self, *a):
        return False


class _Msg:
    def __init__(self):
        self.from_user = SimpleNamespace(id=7)
        self.successful_payment = SimpleNamespace(telegram_payment_charge_id="ch1", invoice_payload="fridge_10:99",
                                                  total_amount=99)
        self.sent = []

    async def answer(self, text, **kw):
        self.sent.append(text)


class _Bot:
    def __init__(self):
        self.refunds = []

    async def refund_star_payment(self, user_id, telegram_payment_charge_id):
        self.refunds.append(telegram_payment_charge_id)
        return True

    async def send_message(self, *a, **k):
        return None


def _patch(monkeypatch, delivered: bool):
    monkeypatch.setattr(payments, "db", SimpleNamespace(pool=SimpleNamespace(acquire=lambda: _Acquire())))

    async def already(conn, charge):
        return delivered

    async def load(conn, user_id, payload):
        raise CatalogError("Холодильник уже такого объёма")

    monkeypatch.setattr(payments, "already_delivered", already)
    monkeypatch.setattr(payments, "_load_order_for_user", load)


async def test_catalog_error_after_payment_refunds_stars(monkeypatch):
    _patch(monkeypatch, delivered=False)
    msg, bot = _Msg(), _Bot()
    await payments.process_successful_payment(msg, bot, "ru")
    assert bot.refunds == ["ch1"]                                   # Stars вернулись автоматически
    assert "Холодильник" in msg.sent[-1]


async def test_repeated_update_does_not_refund_delivered_payment(monkeypatch):
    _patch(monkeypatch, delivered=True)
    msg, bot = _Msg(), _Bot()
    await payments.process_successful_payment(msg, bot, "ru")
    assert bot.refunds == [] and msg.sent                           # товар уже выдан — возврата нет


# ---------- 01.11: Мега-Клан — только для команды (отряд сначала расширяется за монеты) ----------
class _TeamConn:
    def __init__(self, max_members):
        self.max_members, self.updated = max_members, False

    async def fetchrow(self, sql, *a):
        return {"team_id": 1, "max_members": self.max_members}

    async def execute(self, sql, *a):
        self.updated = True


def test_mega_clan_needs_a_team_not_a_squad():
    import asyncio
    from shared.delivery import DeliveryError, _deliver_clan_upgrade
    from shared.economy import MEGA_CLAN_MAX_MEMBERS, SQUAD_MAX_MEMBERS, TEAM_MAX_MEMBERS
    order = {"type": "clan_upgrade", "max_members": MEGA_CLAN_MAX_MEMBERS}
    # до оплаты: отряд — отказ на языке игрока, команда — можно
    assert "отряд" in asyncio.run(payments._precheck_deliverable(_TeamConn(SQUAD_MAX_MEMBERS), 7, order, "ru"))
    assert "squad" in asyncio.run(payments._precheck_deliverable(_TeamConn(SQUAD_MAX_MEMBERS), 7, order, "en"))
    assert asyncio.run(payments._precheck_deliverable(_TeamConn(TEAM_MAX_MEMBERS), 7, order, "ru")) is None
    # при выдаче (если оплата прошла в обход) — отказ, команда не расширяется → авто-возврат
    conn = _TeamConn(SQUAD_MAX_MEMBERS)
    with pytest.raises(DeliveryError):
        asyncio.run(_deliver_clan_upgrade(conn, 7, order, None, "ru"))
    assert not conn.updated
    conn = _TeamConn(TEAM_MAX_MEMBERS)
    asyncio.run(_deliver_clan_upgrade(conn, 7, order, None, "ru"))
    assert conn.updated
