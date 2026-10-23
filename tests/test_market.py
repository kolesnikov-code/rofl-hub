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
    from shared.economy import MARKET_CUTLET_MIN_PRICE, MARKET_RESOURCE_MAX_QTY
    validate_order(1, MARKET_CUTLET_MIN_PRICE)
    validate_order(MARKET_MAX_QTY, MARKET_MAX_PRICE)
    validate_order(1, MARKET_MIN_PRICE, asset="metal")
    validate_order(MARKET_RESOURCE_MAX_QTY, 5, asset="crystal")
    for qty, price in ((0, 300), (MARKET_MAX_QTY + 1, 300), (-5, 300)):
        with pytest.raises(MarketError) as e:
            validate_order(qty, price)
        assert e.value.key == "mk.err_qty"
    for qty, price in ((1, MARKET_CUTLET_MIN_PRICE - 1), (1, MARKET_MAX_PRICE + 1)):
        with pytest.raises(MarketError) as e:
            validate_order(qty, price)
        assert e.value.key == "mk.err_price"
    with pytest.raises(MarketError) as e:
        validate_order(1, 5, asset="gold")
    assert e.value.key == "mk.err_asset"


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


# ---------------------------------------------------------------- пол цены котлеты (решение владельца 24.10)
def test_cutlet_floor_keeps_the_shop_cheaper_than_the_market():
    """
    Котлета на бирже не может быть дешевле котлеты из магазина в пересчёте на монеты:
    самый выгодный пак котлет (★ за штуку) × самый выгодный курс пака монет (🪙 за ★).
    Тест сверяет константы экономики с реальным каталогом — поменяли цены в магазине,
    тест напомнит пересчитать пол.
    """
    from bots.main_bot.catalog import CATALOG
    from shared import economy
    cutlet_packs = [i for i in CATALOG.values() if i["type"] == "cutlets"]
    coin_packs = [i for i in CATALOG.values() if i["type"] == "coins"]
    best_stars_per_cutlet = min(i["stars"] / i["qty"] for i in cutlet_packs)
    best_coins_per_star = max(i["coins_amount"] / i["stars"] for i in coin_packs)
    assert abs(best_stars_per_cutlet * 100 - economy.SHOP_CUTLET_BEST_STARS_X100) < 1
    assert abs(best_coins_per_star - economy.SHOP_COINS_PER_STAR_BEST) < 1
    shop_cutlet_in_coins = best_stars_per_cutlet * best_coins_per_star
    assert economy.MARKET_CUTLET_MIN_PRICE >= shop_cutlet_in_coins
    assert economy.market_min_price("cutlet") == economy.MARKET_CUTLET_MIN_PRICE
    assert economy.market_min_price("metal") == economy.MARKET_MIN_PRICE


def test_cutlet_on_market_does_not_pay_off_for_a_plain_driller():
    """Без бустов Бурильщик за сутки добывает 240 🪙 на одной котлете: бирже почти нечего предложить."""
    from shared import economy
    daily = economy.miner_hourly_rate("premium") * 24
    assert daily - economy.MARKET_CUTLET_MIN_PRICE <= daily // 5


def test_fee_discount_is_only_for_shuttle_owner():
    from shared.economy import SHUTTLE_MARKET_FEE_PERCENT
    assert market_fee(1000, shuttle=True) == 1000 * SHUTTLE_MARKET_FEE_PERCENT // 100
    assert market_fee(1000, shuttle=False) == 100


def test_index_change_handles_empty_and_trends():
    from shared.market import index_change
    assert index_change([{"day": "d", "avg": None, "volume": 0}])["last"] is None
    hist = [{"day": str(i), "avg": p, "volume": 1} for i, p in enumerate([100, None, 100, 130])]
    idx = index_change(hist)
    assert idx["last"] == 130 and idx["week_avg"] == 110.0 and idx["change_pct"] == 18.2 and idx["volume"] == 4


def test_swap_validation():
    from shared.market import validate_swap
    validate_swap("metal", 10, "hydrogen", 5)
    for args, key in ((("metal", 10, "metal", 5), "sw.err_same"), (("gold", 1, "metal", 1), "mk.err_asset"),
                      (("metal", 0, "parts", 1), "sw.err_qty"), (("metal", 1, "hydrogen", 0), "sw.err_qty")):
        with pytest.raises(MarketError) as e:
            validate_swap(*args)
        assert e.value.key == key


def test_swap_qty_error_is_about_swaps_not_cutlets():
    """Регрессия 25.10: при обмене 1 металла на 0 водорода игрок видел текст про «котлеты в ордере»."""
    from shared.locales import t
    from shared.market import validate_swap
    with pytest.raises(MarketError) as e:
        validate_swap("metal", 1, "hydrogen", 0)
    for lang in ("ru", "en"):
        text = e.value.localized(lang)
        assert "котлет" not in text and "cutlet" not in text
    assert "котлет" not in t("ru", "mk.err_qty", max=1000)
