"""
Блок 4: чистая логика списка тиммейтов (🧠 уровень, кликабельность, пагинация)
и экономика переводов.
"""
import os

import pytest

pytest.importorskip("aiogram")
os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from bots.main_bot.handlers.clans import format_member_line, team_pages_total  # noqa: E402
from shared.economy import (  # noqa: E402
    TEAM_LIST_PAGE_SIZE,
    TRANSFER_FEE_PERCENT,
    TRANSFER_MIN_AMOUNT,
    transfer_fee,
)


# ---------------------------------------------------------------- строка тиммейта
def test_member_with_username_is_clickable_with_brain_level():
    line = format_member_line(
        {"user_id": 5, "username": "pro_gamer", "display_name": "Вася", "quiz_level": 7}, captain_id=1)
    assert line == "🧠7 · @pro_gamer"


def test_member_without_username_shows_name_without_link():
    line = format_member_line(
        {"user_id": 5, "username": None, "display_name": "Вася Кибер", "quiz_level": 2}, captain_id=1)
    assert "@" not in line
    assert line == "🧠2 · <b>Вася Кибер</b>"


def test_member_without_username_and_name_falls_back_to_id():
    line = format_member_line(
        {"user_id": 42, "username": None, "display_name": None, "quiz_level": 0}, captain_id=1)
    assert line == "🧠0 · <b>Игрок 42</b>"


def test_captain_gets_crown():
    line = format_member_line(
        {"user_id": 1, "username": "boss", "display_name": None, "quiz_level": 9}, captain_id=1)
    assert line == "🧠9 · 👑 @boss"


def test_member_name_is_html_escaped():
    line = format_member_line(
        {"user_id": 5, "username": None, "display_name": "<script>alert(1)</script>", "quiz_level": 0},
        captain_id=1)
    assert "<script>" not in line
    assert "&lt;script&gt;" in line


def test_member_username_is_html_escaped():
    line = format_member_line(
        {"user_id": 5, "username": "a<b>c", "display_name": None, "quiz_level": 1}, captain_id=1)
    assert "<b>" not in line


def test_missing_quiz_level_defaults_to_zero():
    line = format_member_line({"user_id": 5, "username": "x", "display_name": None}, captain_id=1)
    assert line.startswith("🧠0 ")


# ---------------------------------------------------------------- пагинация
@pytest.mark.parametrize("members,pages", [
    (0, 1), (1, 1), (25, 1), (26, 2), (50, 2), (51, 3), (1000, 40),
])
def test_team_pages_total(members, pages):
    assert TEAM_LIST_PAGE_SIZE == 25
    assert team_pages_total(members) == pages


def test_mega_clan_fits_in_40_pages():
    assert team_pages_total(1000) * TEAM_LIST_PAGE_SIZE >= 1000


# ---------------------------------------------------------------- переводы
def test_transfer_constants():
    assert TRANSFER_MIN_AMOUNT == 10
    assert TRANSFER_FEE_PERCENT == 0


def test_transfer_fee_is_floor_percent():
    assert transfer_fee(100) == 100 * TRANSFER_FEE_PERCENT // 100
    assert transfer_fee(TRANSFER_MIN_AMOUNT) >= 0
