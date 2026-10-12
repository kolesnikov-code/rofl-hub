"""Инвариант аукциона: монеты не печатаются и не исчезают."""
import random

import pytest

from shared.auction_logic import compute_bid


def test_first_bid_charges_full_price():
    r = compute_bid(current_price=1000, min_step=100, bid_step=100, bidder_id=1, bidder_balance=5000,
                    highest_bidder_id=None, status="open")
    assert r.ok
    assert r.new_price == 1100
    assert r.bidder_charge == 1100
    assert r.refund_to_previous == 0
    assert r.previous_bidder_id is None


def test_outbid_refunds_previous_leader_exactly_his_deposit():
    r = compute_bid(current_price=1100, min_step=100, bid_step=100, bidder_id=2, bidder_balance=5000,
                    highest_bidder_id=1, status="open")
    assert r.ok
    assert r.new_price == 1200
    assert r.bidder_charge == 1200
    assert r.refund_to_previous == 1100
    assert r.previous_bidder_id == 1


def test_leader_raising_own_bid_pays_only_the_step():
    r = compute_bid(current_price=1200, min_step=100, bid_step=500, bidder_id=2, bidder_balance=5000,
                    highest_bidder_id=2, status="open")
    assert r.ok
    assert r.bidder_charge == 500
    assert r.refund_to_previous == 0
    assert r.new_price == 1700


def test_insufficient_funds():
    r = compute_bid(current_price=1000, min_step=100, bid_step=100, bidder_id=3, bidder_balance=1099,
                    highest_bidder_id=1, status="open")
    assert not r.ok and r.reason == "insufficient_funds"


def test_closed_auction_rejects():
    r = compute_bid(current_price=0, min_step=100, bid_step=100, bidder_id=1, bidder_balance=999,
                    highest_bidder_id=None, status="closed")
    assert not r.ok and r.reason == "closed"


@pytest.mark.parametrize("step,reason", [(50, "step_too_small"), (150, "step_not_multiple"), (0, "step_too_small")])
def test_bad_steps(step, reason):
    r = compute_bid(current_price=0, min_step=100, bid_step=step, bidder_id=1, bidder_balance=999,
                    highest_bidder_id=None, status="open")
    assert not r.ok and r.reason == reason


def test_money_conservation_random_simulation():
    """Старый код печатал монеты на 3-й ставке. Прогоняем 2000 случайных ставок и считаем сумму."""
    rng = random.Random(42)
    balances = {uid: 100_000 for uid in range(1, 6)}
    total_before = sum(balances.values())
    price, leader = 500, None
    accepted = 0
    for _ in range(2000):
        uid = rng.randint(1, 5)
        step = 100 * rng.randint(1, 5)
        r = compute_bid(current_price=price, min_step=100, bid_step=step, bidder_id=uid,
                        bidder_balance=balances[uid], highest_bidder_id=leader, status="open")
        if not r.ok:
            continue
        accepted += 1
        balances[uid] -= r.bidder_charge
        if r.previous_bidder_id is not None:
            balances[r.previous_bidder_id] += r.refund_to_previous
        price, leader = r.new_price, uid
        assert all(b >= 0 for b in balances.values())
        # депозит лота == цена, и ровно он «вынут» из системы
        assert sum(balances.values()) + price == total_before
    assert accepted > 100
