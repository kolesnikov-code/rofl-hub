"""
Фиче-тумблеры (пульт владельца): дефолты, отказоустойчивость без БД.
Главная гарантия: сбой базы НИКОГДА не выключает работающую игру.
"""
import asyncio

from shared.feature_flags import (
    FLAG_DEFAULTS,
    FLAG_TITLES,
    _default_for,
    get_flag,
    invalidate_cache,
)


def test_defaults_are_safe():
    assert FLAG_DEFAULTS["maintenance"] is False   # техработы по умолчанию ВЫКЛЮЧЕНЫ
    for key in ("games", "duels", "quests", "shop", "transfers", "market"):
        assert FLAG_DEFAULTS[key] is True          # разделы по умолчанию ВКЛЮЧЕНЫ
    assert _default_for("quest:golden_cutlet") is True   # квесты видимы, пока не скрыты
    assert _default_for("unknown_key") is True


def test_every_flag_has_title_for_control_panel():
    assert set(FLAG_TITLES) == set(FLAG_DEFAULTS)


def test_get_flag_without_database_returns_default_and_never_raises():
    invalidate_cache()
    assert asyncio.run(get_flag("games")) is True
    assert asyncio.run(get_flag("maintenance")) is False
    assert asyncio.run(get_flag("quest:locked_safe")) is True
