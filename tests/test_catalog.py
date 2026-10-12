import pytest

from bots.main_bot.catalog import (
    CATALOG,
    CATEGORY_FARM,
    CATEGORY_GAMES,
    SHOP_LAYOUT,
    CatalogError,
    build_order,
    calculate_stars_order,
    normalize_sku,
)

EXPECTED_PRICES = {
    "miner_junior": 49, "miner_premium": 99,
    "cutlet_10": 49, "cutlet_50": 239, "cutlet_100": 449,
    "fridge_10": 99, "fridge_50": 499, "fridge_100": 999,
    "boost_nuclear_30": 199, "boost_nitrogen_30": 299,
    "unlimit_24h": 5, "unlimit_30d": 99,
    "repair_drone_365": 999,
    "coins_5k": 149, "coins_10k": 299, "coins_50k": 1299, "coins_100k": 2499,
    "clan_upgrade": 2499,
}


def test_catalog_has_exactly_18_items_with_tz_prices():
    assert len(CATALOG) == 18
    assert {sku: item["stars"] for sku, item in CATALOG.items()} == EXPECTED_PRICES


def test_every_item_has_required_fields():
    for sku, item in CATALOG.items():
        for field in ("type", "stars", "title", "button", "category"):
            assert field in item, f"{sku} missing {field}"
        assert item["stars"] > 0
        assert item["category"] in (CATEGORY_FARM, CATEGORY_GAMES)


def test_layout_covers_every_sku_exactly_once():
    seen = [sku for cat in SHOP_LAYOUT.values() for row in cat for sku in row]
    assert sorted(seen) == sorted(CATALOG)
    for cat, rows in SHOP_LAYOUT.items():
        for row in rows:
            assert 1 <= len(row) <= 2
            for sku in row:
                assert CATALOG[sku]["category"] == cat


def test_button_callback_data_fits_telegram_limit():
    for sku in CATALOG:
        assert len(f"buy_{sku}".encode()) <= 64


def test_normalize_sku():
    assert normalize_sku("buy_cutlet_10") == "cutlet_10"
    assert normalize_sku("cutlet_10:49") == "cutlet_10"
    assert normalize_sku("buy_coins_5k:149") == "coins_5k"


def test_build_order_returns_sku_and_data():
    order = build_order("buy_coins_5k")
    assert order["sku"] == "coins_5k"
    assert order["coins_amount"] == 5000
    assert order["stars"] == 149


def test_unknown_sku_raises():
    with pytest.raises(CatalogError):
        build_order("buy_unicorn")


@pytest.mark.parametrize("capacity,sku,ok", [
    (1, "fridge_10", True), (10, "fridge_10", False), (50, "fridge_10", False),
    (10, "fridge_50", True), (100, "fridge_100", False),
])
def test_fridge_upgrade_only_upwards(capacity, sku, ok):
    if ok:
        assert build_order(sku, current_capacity=capacity)["capacity"] == int(sku.split("_")[1])
    else:
        with pytest.raises(CatalogError):
            build_order(sku, current_capacity=capacity)


def test_legacy_name_still_works():
    assert calculate_stars_order("buy_miner_junior", 1, 0)["type"] == "miner"
