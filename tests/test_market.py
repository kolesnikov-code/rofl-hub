"""
Биржа котлет: чистые проверки (валидация, комиссия) + локали на 14 языках.
Сделки с деньгами и эскроу — в интеграционных тестах (test_db_integration).
"""
import pytest

from shared.economy import (
    MARKET_FEE_PERCENT,
    MARKET_MAX_OPEN_ORDERS,
    MARKET_MAX_PRICE,
    MARKET_MAX_QTY,
    MARKET_MIN_PRICE,
    market_fee,
)
from shared.market import MarketError, validate_order


def test_fee_is_burned_percent():
    assert MARKET_FEE_PERCENT == 10
    assert market_fee(100) == 10
    assert market_fee(9) == 0          # мелкие сделки без комиссии (целочисленно)
    assert market_fee(0) == 0


def test_validate_order_bounds():
    validate_order(1, MARKET_MIN_PRICE)
    validate_order(MARKET_MAX_QTY, MARKET_MAX_PRICE)
    for qty, price in ((0, 10), (MARKET_MAX_QTY + 1, 10), (-5, 10)):
        with pytest.raises(MarketError) as e:
            validate_order(qty, price)
        assert e.value.key == "mk.err_qty"
    for qty, price in ((1, MARKET_MIN_PRICE - 1), (1, MARKET_MAX_PRICE + 1)):
        with pytest.raises(MarketError) as e:
            validate_order(qty, price)
        assert e.value.key == "mk.err_price"


def test_market_error_localizes():
    err = MarketError("mk.err_too_many", max=MARKET_MAX_OPEN_ORDERS)
    assert str(MARKET_MAX_OPEN_ORDERS) in err.localized("ru")
    assert str(MARKET_MAX_OPEN_ORDERS) in err.localized("en")
    assert err.localized("ru") != err.localized("en")


def test_market_keys_exist_in_all_languages():
    from shared.locales import STRINGS
    for lang, strings in STRINGS.items():
        for key in ("mk.header", "mk.buy_done", "mk.sold_notify", "mk.err_own", "farm.btn_market"):
            assert key in strings, (lang, key)
        # header держит все плейсхолдеры витрины
        strings["mk.header"].format(orders=1, cutlets=2, best=3, fee=10, inv=0, body="x")
