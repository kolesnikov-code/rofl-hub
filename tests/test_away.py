"""🌙 «Пока тебя не было» (владелец 13.11): окно с добычей роботов с прошлого открытия приложения."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from shared.economy import AWAY_MIN_MINUTES
from shared.farm_logic import away_summary

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 11, 13, 12, 0, tzinfo=timezone.utc)


def test_away_needs_a_real_break_and_some_mining():
    long_ago = NOW - timedelta(hours=5, minutes=3)
    assert away_summary(long_ago, NOW, 1564) == {"coins": 1564, "seconds": 5 * 3600 + 180}
    assert away_summary(None, NOW, 1564) is None                                     # первое открытие
    assert away_summary(long_ago, NOW, 0) is None                                    # роботов нет — окна нет
    assert away_summary(NOW - timedelta(minutes=AWAY_MIN_MINUTES - 1), NOW, 50) is None   # переключал вкладки
    assert away_summary(NOW - timedelta(minutes=AWAY_MIN_MINUTES), NOW, 50)["coins"] == 50


def test_me_counts_mining_since_previous_open_and_moves_the_mark():
    src = (ROOT / "bots/main_bot/webapp.py").read_text(encoding="utf-8")
    assert "mined_since(conn, user_id, prev_seen)" in src and "SET app_seen_at = $2" in src
    assert 'payload["away"] = away' in src
    schema = (ROOT / "shared/database.py").read_text(encoding="utf-8")
    assert "ADD COLUMN IF NOT EXISTS app_seen_at TIMESTAMPTZ" in schema


def test_app_shows_the_window_once_on_open_in_every_language():
    html = (ROOT / "static/webapp/index.html").read_text(encoding="utf-8")
    assert "showAway(afterAway)" in html and "me.away = null" in html
    for key in ("aw_title", "aw_text", "aw_ok"):
        assert html.count(key + ":") == 2                       # ru и en
        for code in ("ar", "bn", "de", "es", "fr", "hi", "id", "it", "pl", "pt", "uz", "zh"):
            pack = json.loads((ROOT / f"static/webapp/i18n/{code}.json").read_text(encoding="utf-8"))
            assert pack.get(key), (code, key)
            if key == "aw_text":
                assert "{t}" in pack[key]
