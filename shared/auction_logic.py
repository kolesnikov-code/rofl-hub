"""
Чистая математика возвратного аукциона.

Инвариант: current_price == сумма, которую реально внёс текущий лидер.
При перебитии предыдущему лидеру возвращается ровно его взнос (current_price),
а новый лидер вносит ПОЛНУЮ новую цену. Сумма «балансы игроков + депозит лота»
никогда не меняется — монеты не печатаются и не исчезают.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BidResult:
    ok: bool
    reason: str
    new_price: int = 0
    bidder_charge: int = 0        # сколько списать с нового лидера
    refund_to_previous: int = 0   # сколько вернуть предыдущему лидеру
    previous_bidder_id: int | None = None


def compute_bid(
    *,
    current_price: int,
    min_step: int,
    bid_step: int,
    bidder_id: int,
    bidder_balance: int,
    highest_bidder_id: int | None,
    status: str,
) -> BidResult:
    if status != "open":
        return BidResult(False, "closed")
    if min_step <= 0:
        return BidResult(False, "bad_min_step")
    if bid_step < min_step:
        return BidResult(False, "step_too_small")
    if bid_step % min_step != 0:
        return BidResult(False, "step_not_multiple")

    new_price = current_price + bid_step

    if highest_bidder_id == bidder_id:
        # Лидер поднимает собственную ставку: доплачивает только разницу
        charge = bid_step
        refund = 0
        prev = None
    else:
        charge = new_price
        refund = current_price if highest_bidder_id is not None else 0
        prev = highest_bidder_id

    if bidder_balance < charge:
        return BidResult(False, "insufficient_funds", new_price=new_price, bidder_charge=charge)

    return BidResult(
        True, "ok",
        new_price=new_price,
        bidder_charge=charge,
        refund_to_previous=refund,
        previous_bidder_id=prev,
    )
