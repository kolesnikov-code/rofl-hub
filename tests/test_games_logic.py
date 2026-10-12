"""
Блок 3: чистые правила соло-игр и уровни викторины (без БД и Telegram).
"""
import os

import pytest

pytest.importorskip("aiogram")
os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from bots.main_bot.handlers.games import (  # noqa: E402
    GAME_TITLES,
    WIN_COLUMNS,
    coin_outcome,
    dice_outcome,
    hl_outcome,
    limit_for,
    rps_outcome,
    safe_outcome,
)
from shared.economy import (  # noqa: E402
    QUIZ_ANSWERS_PER_LEVEL,
    QUIZ_LEVEL_UP_BONUS,
    SAFE_CODES_COUNT,
    SAFE_WIN_REWARD,
    WIN_REWARD,
    quiz_answers_to_next_level,
    quiz_level_for,
    win_reward_for,
)


# ---------------------------------------------------------------- каталог игр
def test_every_game_has_title_column_and_limit():
    assert set(GAME_TITLES) == set(WIN_COLUMNS) == {"rps", "hl", "quiz", "coin", "dice", "safe"}
    assert limit_for("quiz") == 30
    for game in ("rps", "hl", "coin", "dice", "safe"):
        assert limit_for(game) == 15


def test_win_rewards():
    assert win_reward_for("safe") == SAFE_WIN_REWARD == 5
    for game in ("rps", "hl", "quiz", "coin", "dice"):
        assert win_reward_for(game) == WIN_REWARD == 2


# ---------------------------------------------------------------- КНБ
@pytest.mark.parametrize("user,bot,win,draw", [
    ("rock", "scissors", True, False),
    ("rock", "paper", False, False),
    ("rock", "rock", False, True),
    ("scissors", "paper", True, False),
    ("scissors", "rock", False, False),
    ("scissors", "scissors", False, True),
    ("paper", "rock", True, False),
    ("paper", "scissors", False, False),
    ("paper", "paper", False, True),
])
def test_rps_outcome(user, bot, win, draw):
    assert rps_outcome(user, bot) == (win, draw)


# ---------------------------------------------------------------- Больше/Меньше
@pytest.mark.parametrize("direction,base,secret,win", [
    ("up", 50, 51, True),
    ("up", 50, 49, False),
    ("down", 50, 49, True),
    ("down", 50, 51, False),
    ("up", 50, 50, False),
    ("down", 50, 50, False),
])
def test_hl_outcome(direction, base, secret, win):
    assert hl_outcome(direction, base, secret) == win


# ---------------------------------------------------------------- Орёл/Решка
@pytest.mark.parametrize("choice,result,win", [
    ("heads", "heads", True),
    ("heads", "tails", False),
    ("tails", "tails", True),
    ("tails", "heads", False),
])
def test_coin_outcome(choice, result, win):
    assert coin_outcome(choice, result) == win


# ---------------------------------------------------------------- Кубики
@pytest.mark.parametrize("player,bot,win,draw", [
    (6, 1, True, False),
    (1, 6, False, False),
    (3, 3, False, True),
    (4, 3, True, False),
    (1, 1, False, True),
])
def test_dice_outcome(player, bot, win, draw):
    assert dice_outcome(player, bot) == (win, draw)


# ---------------------------------------------------------------- Сейф
def test_safe_outcome():
    assert safe_outcome(3, 3) is True
    assert safe_outcome(1, 3) is False
    assert SAFE_CODES_COUNT == 4


def test_safe_expected_value_matches_coin():
    """Баланс экономики: EV сейфа (шанс 1/4, куш 5) равен EV орла/решки (1/2, 2)."""
    ev_safe = SAFE_WIN_REWARD / SAFE_CODES_COUNT - 1 * (SAFE_CODES_COUNT - 1) / SAFE_CODES_COUNT
    ev_coin = WIN_REWARD / 2 - 1 / 2
    assert ev_safe == ev_coin == 0.5


# ---------------------------------------------------------------- Уровни викторины
@pytest.mark.parametrize("total,level", [
    (0, 0), (1, 0), (29, 0), (30, 1), (31, 1), (59, 1), (60, 2), (90, 3), (300, 10),
])
def test_quiz_level_for(total, level):
    assert quiz_level_for(total) == level


@pytest.mark.parametrize("total,to_next", [
    (0, 30), (1, 29), (29, 1), (30, 30), (59, 1), (60, 30),
])
def test_quiz_answers_to_next_level(total, to_next):
    assert quiz_answers_to_next_level(total) == to_next


def test_quiz_level_rejects_negative():
    with pytest.raises(ValueError):
        quiz_level_for(-1)


def test_quiz_level_constants():
    assert QUIZ_ANSWERS_PER_LEVEL == 30
    assert QUIZ_LEVEL_UP_BONUS == 500


def test_level_up_triggers_exactly_on_multiples_of_30():
    triggers = [n for n in range(1, 121) if n % QUIZ_ANSWERS_PER_LEVEL == 0]
    assert triggers == [30, 60, 90, 120]
