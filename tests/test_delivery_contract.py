"""Контракт: у каждого типа товара из каталога есть обработчик доставки (раньше 5 из 18 товаров терялись)."""
from bots.main_bot.catalog import CATALOG
from shared.delivery import DELIVERY_HANDLERS


def test_every_catalog_type_has_delivery_handler():
    types_in_catalog = {item["type"] for item in CATALOG.values()}
    missing = types_in_catalog - set(DELIVERY_HANDLERS)
    assert not missing, f"Нет обработчиков доставки для типов: {missing}"


def test_no_orphan_handlers():
    types_in_catalog = {item["type"] for item in CATALOG.values()}
    # ✨ скины продаются вне витрины CATALOG — из Гаража (catalog.skin_item), обработчик «skin» свой
    assert set(DELIVERY_HANDLERS) == types_in_catalog | {"skin", "season_pass"}   # 🎟 пропуск — тоже из Магазина «Скины»


def test_every_skin_for_sale_builds_an_order():
    from bots.main_bot.catalog import CatalogError, build_order
    from shared.economy import utcnow
    from shared.skins import SKINS, for_sale, skin_sku
    for sid, s in SKINS.items():
        if for_sale(sid, utcnow()):
            order = build_order(skin_sku(sid))
            assert order["type"] == "skin" and order["stars"] == s["stars"] and order["skin"] == sid
        else:
            try:
                build_order(skin_sku(sid))
                raise AssertionError(sid)
            except CatalogError:
                pass


def test_expiring_items_declare_duration():
    for sku, item in CATALOG.items():
        if item["type"] in ("farm_boost", "vip_character"):
            assert item.get("days", 0) > 0, sku
        if item["type"] == "game_unlimit":
            assert item.get("hours", 0) > 0, sku
