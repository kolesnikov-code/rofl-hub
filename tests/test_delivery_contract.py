"""Контракт: у каждого типа товара из каталога есть обработчик доставки (раньше 5 из 18 товаров терялись)."""
from bots.main_bot.catalog import CATALOG
from shared.delivery import DELIVERY_HANDLERS


def test_every_catalog_type_has_delivery_handler():
    types_in_catalog = {item["type"] for item in CATALOG.values()}
    missing = types_in_catalog - set(DELIVERY_HANDLERS)
    assert not missing, f"Нет обработчиков доставки для типов: {missing}"


def test_no_orphan_handlers():
    types_in_catalog = {item["type"] for item in CATALOG.values()}
    assert set(DELIVERY_HANDLERS) == types_in_catalog


def test_expiring_items_declare_duration():
    for sku, item in CATALOG.items():
        if item["type"] in ("farm_boost", "vip_character"):
            assert item.get("days", 0) > 0, sku
        if item["type"] == "game_unlimit":
            assert item.get("hours", 0) > 0, sku
