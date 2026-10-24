"""
Mini App: проверка подписи initData (криптография Telegram) и сборка /api/me.
"""
import time
from datetime import datetime, timedelta, timezone

import pytest

from shared.webapp_auth import sign_init_data, validate_init_data

TOKEN = "123456:TEST-TOKEN-FOR-WEBAPP"
NOW = time.time()


def _valid_init_data(**overrides):
    pairs = {
        "auth_date": str(int(NOW)),
        "query_id": "AAE1",
        "user": {"id": 777, "first_name": "Толя", "language_code": "ru"},
    }
    pairs.update(overrides)
    return sign_init_data(pairs, TOKEN)


# ---------------------------------------------------------------- подпись
def test_valid_init_data_passes_and_user_is_parsed():
    parsed = validate_init_data(_valid_init_data(), TOKEN, now=NOW)
    assert parsed is not None
    assert parsed["user"]["id"] == 777
    assert parsed["user"]["first_name"] == "Толя"


def test_wrong_bot_token_rejected():
    assert validate_init_data(_valid_init_data(), "999:OTHER", now=NOW) is None


def test_tampered_payload_rejected():
    data = _valid_init_data()
    tampered = data.replace("777", "666")
    assert validate_init_data(tampered, TOKEN, now=NOW) is None


def test_missing_hash_rejected():
    assert validate_init_data("auth_date=123&user=%7B%7D", TOKEN, now=NOW) is None


def test_expired_init_data_rejected():
    old = _valid_init_data(auth_date=str(int(NOW) - 100_000))
    assert validate_init_data(old, TOKEN, now=NOW) is None
    # но в пределах суток — валидно
    fresh = _valid_init_data(auth_date=str(int(NOW) - 3600))
    assert validate_init_data(fresh, TOKEN, now=NOW) is not None


@pytest.mark.parametrize("garbage", ["", "hash=deadbeef", "обычный текст", None])
def test_garbage_rejected(garbage):
    assert validate_init_data(garbage or "", TOKEN, now=NOW) is None


def test_user_without_id_rejected():
    data = sign_init_data({"auth_date": str(int(NOW)), "user": {"name": "x"}}, TOKEN)
    assert validate_init_data(data, TOKEN, now=NOW) is None


# ---------------------------------------------------------------- /api/me payload
def test_build_me_payload_shape():
    pytest.importorskip("aiohttp")
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    from bots.main_bot.webapp import build_me_payload
    from shared.farm_logic import MinerState

    now = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)
    user = {
        "user_id": 777, "lang": "en", "display_name": "Толя", "username": "tolya",
        "balance": 5000, "fridge_cutlets": 3, "fridge_capacity": 10, "inv_cutlets": 7,
        "boost_nuclear_until": now + timedelta(days=1), "boost_nitrogen_until": None,
        "drone_until": None, "last_bonus_claim_at": now - timedelta(hours=25),
        "created_at": now - timedelta(days=10), "intern_claimed": False, "interns_pending": 0,
        "farm_armor_level": 0, "armor_until": None, "has_shuttle": False, "res_capacity": 500,
    }
    miners = [
        MinerState(1, "junior", now - timedelta(days=1), now + timedelta(days=29)),
        MinerState(2, "premium", now - timedelta(days=1), now + timedelta(days=10),
                   fuel_until=now + timedelta(hours=5)),
    ]
    quiz = {"quiz_level": 2, "quiz_level_progress": 7}
    payload = build_me_payload(user, miners, quiz, None, ["ROFL-HUB-777"], now)

    assert payload["lang"] == "en" and payload["balance"] == 5000
    assert payload["vip_aliases"] == ["ROFL-HUB-777"]
    assert payload["quiz"] == {"level": 2, "progress": 7, "required": 30,
                               "next_level": 3, "next_reward": 300}
    farm = payload["farm"]
    assert (farm["junior"], farm["premium"], farm["premium_fueled"]) == (1, 1, 1)
    # ядерный буст активен: 25 (junior) + 50 (premium) монет/час
    assert farm["speed_hour"] == 25 + 50
    assert farm["bonus_seconds_left"] == 0
    assert farm["boosts"]["nuclear_until"] and farm["boosts"]["drone_until"] is None
    assert farm["nearest_burnout"].startswith("2026-11-11")
    assert farm["units"] == [{"kind": "junior", "fueled": True, "eternal": False},
                             {"kind": "premium", "fueled": True, "eternal": False}]
    assert payload["rank"] == "Fighter"          # 10 дней в экосистеме, язык en
    assert payload["team"] is None


# ---------------------------------------------------------------- /api/shop payload
def test_build_shop_payload_mirrors_catalog():
    pytest.importorskip("aiohttp")
    import os
    os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")
    from bots.main_bot.catalog import CATALOG
    from bots.main_bot.webapp import build_shop_payload

    ru = build_shop_payload("ru")
    en = build_shop_payload("en")

    # Все 19 товаров на витрине, ни один не потерян
    assert len(ru["farm"]) + len(ru["games"]) == len(CATALOG) == 19
    skus = {i["sku"] for i in ru["farm"] + ru["games"]}
    assert skus == set(CATALOG)

    # Подписи локализованы и содержат цену в звёздах
    first_ru, first_en = ru["farm"][0], en["farm"][0]
    assert first_ru["sku"] == first_en["sku"]
    assert first_ru["label"] != first_en["label"]
    for item in ru["farm"] + ru["games"] + en["farm"] + en["games"]:
        assert str(item["stars"]) in item["label"]
        assert "★" in item["label"]
