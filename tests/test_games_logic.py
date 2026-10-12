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
    QUIZ_LEVEL_REWARD_PER_LEVEL,
    QUIZ_LEVEL_STEP_ANSWERS,
    SAFE_CODES_COUNT,
    SAFE_WIN_REWARD,
    WIN_REWARD,
    quiz_answers_required,
    quiz_level_reward,
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
# Прогрессия владельца: уровень N требует N*10 верных ответов (итерация с нуля),
# награда за уровень N — N*100 рофлов.
@pytest.mark.parametrize("level,required", [
    (1, 10), (2, 20), (3, 30), (4, 40), (10, 100), (100, 1000),
])
def test_quiz_answers_required(level, required):
    assert quiz_answers_required(level) == required


@pytest.mark.parametrize("level,reward", [
    (1, 100), (2, 200), (3, 300), (4, 400), (10, 1000), (100, 10_000),
])
def test_quiz_level_reward(level, reward):
    assert quiz_level_reward(level) == reward


def test_quiz_level_helpers_reject_nonpositive():
    with pytest.raises(ValueError):
        quiz_answers_required(0)
    with pytest.raises(ValueError):
        quiz_level_reward(-1)


def test_quiz_level_constants():
    assert QUIZ_LEVEL_STEP_ANSWERS == 10
    assert QUIZ_LEVEL_REWARD_PER_LEVEL == 100


def test_first_two_levels_fit_exactly_into_daily_limit():
    """Маркетинговая механика: уровни 1+2 = ровно дневной лимит викторины (30 побед),
    уровень 4 (40 ответов) за день без безлимита уже не закрыть."""
    assert quiz_answers_required(1) + quiz_answers_required(2) == limit_for("quiz")
    assert quiz_answers_required(4) > limit_for("quiz")


def test_quiz_inflation_is_bounded():
    """Награда за уровень = 10 рофлов за каждый верный ответ итерации — на любом уровне."""
    for level in (1, 2, 5, 10, 50, 100):
        assert quiz_level_reward(level) / quiz_answers_required(level) == 10
