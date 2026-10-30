"""
🕵️ Проверка на абуз, 🎟 лимит опыта пропуска за игры, 🧥 костюм за 10 активных друзей (решения владельца 30.10).
Чистые правила без БД; интеграционный сценарий фермы твинков — в test_db_integration.py.
"""
import os
import re
from pathlib import Path

os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from shared import abuse  # noqa: E402
from shared import season_pass as sp  # noqa: E402
from shared.economy import (REFERRAL_QUALIFY_BONUS_CLAIMS, REFERRAL_QUALIFY_QUIZ_LEVEL, REFERRAL_SUIT_FRIENDS,  # noqa: E402
                            TEAM_HELP_GIVER_MIN_BONUS_CLAIMS, TEAM_HELP_GIVER_MIN_QUIZ_LEVEL)
from shared.locales import PACK_CODES, t  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ADMIN = (ROOT / "static/webapp/admin.html").read_text(encoding="utf-8")
APP = (ROOT / "static/webapp/index.html").read_text(encoding="utf-8")
name = lambda u: f"#{u}"  # noqa: E731


def total(f) -> int:
    return sum(s["points"] for s in abuse.score_user(f, name))


def test_clean_player_scores_zero_and_is_green():
    assert abuse.score_user({}, name) == []
    assert abuse.level_of(0) == "green" and abuse.level_of(10) == "yellow"
    assert abuse.level_of(30) == "orange" and abuse.level_of(60) == "red"
    # одна случайная сделка, налёт и дуэль — не повод
    assert total({"market_pairs": {2: 1}, "raid_wins_vs": {3: 1}, "duel_pairs": {4: (2, 1)}}) == 0


def test_twink_farm_feeding_one_account_is_the_worst_case():
    """Пятеро «своих» рефералов дарят ресурсы и монеты пригласившему — жёсткий случай, сверху ленты."""
    boss = {"help_in": {i: 150 for i in range(10, 15)}, "tr_in": {i: 900 for i in range(10, 15)},
            "own_ref_feeders": list(range(10, 15))}
    sigs = abuse.score_user(boss, name)
    assert {s["code"] for s in sigs} >= {"funnel", "coin_funnel", "ref_feeders"}
    assert abuse.level_of(total(boss)) == "red"
    assert all(s["text"] for s in sigs) and sigs == sorted(sigs, key=lambda s: -s["points"])
    twink = {"help_out": {1: 150}, "tr_out": {1: 900}, "feeds_referrer": 1, "thin": True}
    assert {s["code"] for s in abuse.score_user(twink, name)} == {"feeder", "feeds_referrer"}
    # честный тиммейт, раздающий понемногу разным, — не «кормушка»
    assert total({"help_out": {1: 40, 2: 40, 3: 40}}) == 0


def test_market_overpay_duel_dump_and_raid_farm_are_caught():
    assert total({"overpay": [{"asset": "metal", "qty": 10, "price": 500, "median": 20, "coins": 5000, "cp": 7,
                               "role": "купил(а)"}]}) >= 25
    assert "duel_dump_win" in {s["code"] for s in abuse.score_user({"duel_pairs": {9: (6, 6)}}, name)}
    assert "duel_dump_lose" in {s["code"] for s in abuse.score_user({"duel_pairs": {9: (6, 0)}}, name)}
    assert total({"duel_pairs": {9: (6, 3)}}) == 0                 # ровная пара — нормальная игра
    assert "raid_farm" in {s["code"] for s in abuse.score_user({"raid_wins_vs": {5: 4}}, name)}
    assert "raid_victim" in {s["code"] for s in abuse.score_user({"raid_losses_to": {5: 4}}, name)}


def test_signal_points_are_capped():
    huge = {"help_in": {i: 10 ** 6 for i in range(100)}}
    assert abuse.score_user(huge, name)[0]["points"] == 50
    assert abuse.score_user({"bot_days": 30}, name)[0]["points"] == 40


def test_referral_farms_and_bots():
    codes = {s["code"] for s in abuse.score_user({"refs_abandoned": 3, "refs_qualified": 4, "refs_day_max": 7,
                                                  "bot_days": 2, "refunds": 1, "banned_links": [8]}, name)}
    assert codes == {"ref_abandoned", "ref_burst", "bot_hours", "refunds", "banned_links"}


def test_admin_panel_has_abuse_feed_and_full_player_card():
    assert 'abuse: ["🕵️ Проверка", viewAbuse]' in ADMIN
    for cat in ("why", "links", "coins", "res", "gifts", "transfers", "market", "raids", "duels", "games", "exp", "pay", "refs", "gear"):
        assert f'["{cat}", ' in ADMIN, cat
    src = (ROOT / "bots/main_bot/webapp_admin.py").read_text(encoding="utf-8")
    for route in ("/api/admin/abuse", "/api/admin/abuse/user", "/api/admin/abuse/review", "/api/admin/abuse/block"):
        assert f'"{route}"' in src


def test_team_help_giver_threshold_is_the_active_account():
    assert (TEAM_HELP_GIVER_MIN_QUIZ_LEVEL, TEAM_HELP_GIVER_MIN_BONUS_CLAIMS) == \
           (REFERRAL_QUALIFY_QUIZ_LEVEL, REFERRAL_QUALIFY_BONUS_CLAIMS) == (3, 3)


def test_pass_game_xp_daily_cap():
    assert sp.PASS_GAME_XP_DAILY == 200 and sp.PASS_DAILY_CAPPED == ("game_win",)
    # 30 уровней × 100 опыта: одними играми — не быстрее 15 дней
    assert sp.PASS_LEVELS * sp.PASS_XP_PER_LEVEL / sp.PASS_GAME_XP_DAILY == 15
    assert "pass_gameCap:" in APP


def test_referral_suit_task_texts_and_wiring():
    assert REFERRAL_SUIT_FRIENDS == 10
    assert "function refSuitCard(d)" in APP and '"/api/gear/ref_suit"' in APP
    for lang in ("ru", "en", *PACK_CODES):
        assert t(lang, "gear.err_ref_taken") != "gear.err_ref_taken"
        assert "10" in t(lang, "gear.err_ref_need", n=10, have=3)
    for key in ("ref_suitTitle", "ref_suitHint", "ref_suitProgress", "ref_suitAsk", "ref_suitDone", "ref_suitTaken", "ref_suitLocked"):
        assert len(re.findall(rf"\b{key}: ", APP)) >= 2, key
