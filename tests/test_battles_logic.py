"""
Битвы и акции v2: чистая логика (номинации, зачёт, рудники по местам, призы, посты на 14 языках).
"""
from datetime import datetime, timezone
from pathlib import Path

from shared.battles import (
    BATTLE_NOMINATIONS,
    BATTLE_SCOPES,
    MANUAL_NOMINATIONS,
    battery_fee,
    battle_mines,
    is_manual,
    medals,
    nomination_title,
    prizes_by_place,
)

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------- номинации
def test_nominations_catalog_is_rich_and_well_formed():
    assert len(BATTLE_NOMINATIONS) >= 8  # владелец просил больше номинаций и азарта
    for key, nom in BATTLE_NOMINATIONS.items():
        assert nom["title"] and nom["unit"], key
        assert nom["kind"] in ("ledger_sum", "ledger_count", "ledger_sum_positive",
                               "ledger_count_like", "referrals", "stars"), key
        if nom["kind"] in ("ledger_sum", "ledger_count"):
            assert nom.get("reason"), key
        if nom["kind"] == "ledger_count_like":
            assert nom.get("reason_like"), key


def test_key_owner_nominations_present():
    """Номинации из ТЗ владельца: нафармить, дуэли, КНБ, викторина, рефералы, соцсети."""
    for key in ("farm_mined", "duel_wins", "duels_played", "rps_wins", "quiz_wins", "referrals"):
        assert key in BATTLE_NOMINATIONS, key
    assert set(MANUAL_NOMINATIONS) == {"insta_reels", "youtube_shorts", "tiktok"}
    assert not set(MANUAL_NOMINATIONS) & set(BATTLE_NOMINATIONS)


def test_manual_and_custom_nominations():
    assert is_manual("insta_reels") and is_manual("custom") and not is_manual("farm_mined")
    assert nomination_title("custom", "Самый смешной мем") == "Самый смешной мем"
    assert nomination_title("tiktok").startswith("🎵")
    assert nomination_title("farm_mined") == BATTLE_NOMINATIONS["farm_mined"]["title"]


def test_scopes_and_battery_fees():
    assert BATTLE_SCOPES == ("team", "clan", "teams", "solo")
    assert battery_fee(False) == 5 and battery_fee(True) == 25      # заявка команды / клана


def test_battle_mines_by_place_and_legacy_single_mine():
    class R(dict):
        pass
    assert battle_mines(R(mine_ids=[7, 3, 12], mine_id=None)) == [7, 3, 12]   # порядок = призовые места
    assert battle_mines(R(mine_ids=[], mine_id=4)) == [4]
    assert battle_mines(R(mine_ids=None, mine_id=None)) == []


def test_prizes_by_place_v2_and_legacy():
    v2 = prizes_by_place({"1": [{"kind": "coins", "amount": 500}, {"kind": "resource", "res": "core", "qty": 2}],
                          "2": [{"kind": "bogus"}]})
    assert v2 == {1: [{"kind": "coins", "amount": 500}, {"kind": "resource", "res": "core", "qty": 2}], 2: []}
    legacy = prizes_by_place('{"1": {"mode": "manual", "value": "iPhone"}, "2": {"mode": "sku", "value": "cutlet_10"}}')
    assert legacy == {1: [{"kind": "text", "text": "iPhone"}]}


def test_medals():
    assert [medals(i) for i in (1, 2, 3, 4, 10)] == ["🥇", "🥈", "🥉", "4.", "10."]


# ---------------------------------------------------------------- призы
def test_normalize_rewards_accepts_every_kind_and_rejects_garbage():
    from shared.prizes import REWARD_KINDS, normalize_reward, normalize_rewards
    good = [
        {"kind": "coins", "amount": "1000"},
        {"kind": "resource", "res": "battery", "qty": 5},
        {"kind": "cutlets", "qty": 10},
        {"kind": "item", "effect": "shield", "hours": 48},
        {"kind": "item", "effect": "economizer", "hours": 99, "qty": 3},     # разовое — часы обнуляются
        {"kind": "robot", "robot": "premium", "hours": 8760},
        {"kind": "boost", "boost": "unlimit", "hours": 24},
        {"kind": "bdrone", "drone": "spy", "qty": 2},                         # 28.10: боевой дрон
        {"kind": "text", "text": "Telegram Premium на 3 месяца"},
    ]
    out = normalize_rewards(good)
    assert [r["kind"] for r in out] == ["coins", "resource", "cutlets", "item", "item", "robot", "boost", "bdrone", "text"]
    assert out[0]["amount"] == 1000 and out[4] == {"kind": "item", "effect": "economizer", "hours": 0, "qty": 3}
    assert {r["kind"] for r in out} == set(REWARD_KINDS)
    for bad in ({"kind": "coins", "amount": 0}, {"kind": "coins", "amount": -5}, {"kind": "resource", "res": "gold", "qty": 1},
                {"kind": "item", "effect": "shield", "hours": 0}, {"kind": "robot", "robot": "intern", "hours": 5},
                {"kind": "boost", "boost": "nitrogen", "hours": 999999}, {"kind": "text", "text": "  "}, "x", None,
                {"kind": "station_drone"}, {"kind": "bdrone", "drone": "laser"}):
        assert normalize_reward(bad) is None, bad


def test_reward_labels_are_language_neutral():
    from shared.prizes import rewards_label
    label = rewards_label([{"kind": "coins", "amount": 5000}, {"kind": "resource", "res": "core", "qty": 2},
                           {"kind": "robot", "robot": "premium", "hours": 720, "qty": 1},
                           {"kind": "boost", "boost": "unlimit", "hours": 24}])
    assert label == "5 000 🪙 + 2 ☢️ + ⚡🤖 30d + ♾ 1d"
    assert rewards_label([]) == "—"
    assert rewards_label([{"kind": "robot", "robot": "junior", "hours": 8760 * 2, "qty": 3}]) == "🤖 2y ×3"


def test_needs_farm_close_only_for_farm_rewards():
    from shared.prizes import needs_farm_close
    assert needs_farm_close([{"kind": "robot", "robot": "junior", "hours": 5}])
    assert needs_farm_close([{"kind": "boost", "boost": "nitrogen", "hours": 5}])
    assert not needs_farm_close([{"kind": "boost", "boost": "shield", "hours": 5}, {"kind": "coins", "amount": 1}])


# ---------------------------------------------------------------- посты на всех языках
class _B(dict):
    pass


def _battle(**kw):
    base = dict(battle_id=7, title="Осенний кубок <b>", nomination_key="farm_mined", nomination_text="x",
                scope="teams", places=3, mine_ids=[4, 9], mine_id=None,
                starts_at=NOW, ends_at=datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc))
    base.update(kw)
    return _B(base)


ROOT = Path(__file__).resolve().parent.parent


def test_no_channel_posts_anywhere():
    """26.10: канала нет — ни модуля постов, ни отправки в USERS_CHANNEL_ID."""
    assert not (ROOT / "shared" / "battle_posts.py").exists()
    admin_bot = (ROOT / "bots" / "admin_notifier_bot" / "bot.py").read_text(encoding="utf-8")
    assert "USERS_CHANNEL_ID" not in admin_bot and "battle_posts" not in admin_bot
    assert "send_reward_notices" in admin_bot


def test_reward_notice_text_place_all_manual_and_mine():
    from shared.reward_notify import notice_text
    place = notice_text("ru", {"title": "Кубок <b>", "place": 1, "all": False, "mine_id": 7,
                               "rewards": [{"kind": "resource", "res": "battery", "qty": 10},
                                           {"kind": "text", "text": "Telegram Premium"}]})
    assert "Кубок &lt;b&gt;" in place and "1 месте" in place and "10 🔋" in place
    assert "Telegram Premium" in place and "Рудник №7" in place
    part = notice_text("en", {"title": "Run", "place": 5, "all": True, "rewards": [{"kind": "coins", "amount": 50}]})
    assert "thanks for taking part" in part and "50 🪙" in part
    from shared.locales import PACK_CODES, t
    for lang in ("ru", "en") + tuple(PACK_CODES):
        for key in ("rn.place", "rn.all", "rn.got", "rn.manual", "rn.mine", "rn.where", "auc.outbid", "auc.bid_ok"):
            assert t(lang, key, title="T", place=1, r="x", mine=1, hours=24, refund=1, price=2) != key, (lang, key)
