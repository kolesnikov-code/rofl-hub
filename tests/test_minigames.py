"""Новые игры приложения (27.10): математика, флаги и столицы, взлом кода, мемори — чистые правила."""
import random
import re
from pathlib import Path

import pytest

from shared import economy
from shared.minigames import (CAPITAL_LANGS, MEMORY_ICONS, bulls_cows, capital_ok, code_secret, flag_emoji,
                              flags_data, flags_round_state, math_problem, math_round_state, memory_deck,
                              memory_flip, valid_code_guess)

ROOT = Path(__file__).resolve().parents[1]


def _eval(text: str) -> int:
    a, op, b = text.split(" ")
    a, b = int(a), int(b)
    return {"+": a + b, "−": a - b, "×": a * b, "÷": a // b}[op]


def test_math_problems_are_correct_and_integer():
    rng = random.Random(1)
    for _ in range(2000):
        text, answer = math_problem(rng)
        assert _eval(text) == answer and answer > 0
        if "÷" in text:
            a, _, b = text.split(" ")
            assert int(a) % int(b) == 0          # деление всегда нацело


def test_math_options_unique_positive_and_contain_answer():
    rng = random.Random(2)
    for _ in range(500):
        st = math_round_state(rng)
        opts = [int(o) for o in st["options"]]
        assert len(opts) == len(set(opts)) == 4 and min(opts) > 0
        assert opts[st["correct"]] == _eval(st["q"])


def test_flags_data_is_clean():
    data = flags_data()
    assert len(data) >= 100
    isos = [r["iso"] for r in data]
    assert len(isos) == len(set(isos)) and all(re.fullmatch(r"[A-Z]{2}", i) for i in isos)
    for lang in ("ru", "en"):
        names = [r[lang] for r in data]
        assert len(names) == len(set(names)) and all(names)
        caps = [r[f"cap_{lang}"] for r in data if capital_ok(r, lang)]
        assert len(caps) == len(set(caps)) and len(caps) >= 50   # столицы без дублей — варианты не совпадают
    assert flag_emoji("FR") == "🇫🇷"


def test_flags_rounds_have_one_right_answer_for_every_language():
    rng = random.Random(3)
    data = {r["iso"]: r for r in flags_data()}
    for lang in ("ru", "en", "de", "zh", "ar"):
        for _ in range(300):
            st = flags_round_state(lang, rng)
            assert len(st["options"]) == len(set(st["options"])) == 4
            if st["mode"] == "flag":
                assert st["options"][st["correct"]] == st["iso"] and st["flag"] == flag_emoji(st["iso"])
                assert len(st["names"]) == 4
            else:
                assert lang in CAPITAL_LANGS
                assert st["options"][st["correct"]] == data[st["iso"]][f"cap_{lang}"]
                assert st["country"] == data[st["iso"]][lang]


def test_bulls_and_cows():
    assert bulls_cows("1234", "1234") == (4, 0)
    assert bulls_cows("1234", "4321") == (0, 4)
    assert bulls_cows("1234", "1243") == (2, 2)
    assert bulls_cows("1234", "5678") == (0, 0)
    assert bulls_cows("0123", "0456") == (1, 0)
    for _ in range(200):
        sec = code_secret()
        assert valid_code_guess(sec) and len(sec) == economy.CODE_DIGITS
    for bad in ("123", "12345", "1123", "12a4", "", "١٢٣٤"):
        assert not valid_code_guess(bad)


def test_memory_deck_and_flips():
    deck = memory_deck(random.Random(4))
    assert len(deck) == economy.MEMORY_PAIRS * 2 and all(deck.count(i) == 2 for i in deck)
    assert set(deck) <= set(MEMORY_ICONS)
    state = {"deck": deck, "matched": [], "pending": None, "moves": 0}
    first = memory_flip(state, 0)
    assert first["pair"] is None and state["pending"] == 0
    with pytest.raises(ValueError):
        memory_flip(state, 0)                       # та же карточка второй раз за ход
    with pytest.raises(ValueError):
        memory_flip(state, len(deck))               # вне колоды
    twin = next(i for i in range(1, len(deck)) if deck[i] == deck[0])
    r = memory_flip(state, twin)
    assert r["match"] and state["moves"] == 1 and set(state["matched"]) == {0, twin}
    with pytest.raises(ValueError):
        memory_flip(state, twin)                    # найденную не открыть
    # идеальная партия: все пары за MEMORY_PAIRS ходов
    by_icon = {}
    for i, ic in enumerate(deck):
        if i not in state["matched"]:
            by_icon.setdefault(ic, []).append(i)
    last = None
    for a, b in by_icon.values():
        memory_flip(state, a)
        last = memory_flip(state, b)
    assert last["done"] and state["moves"] == economy.MEMORY_PAIRS <= economy.MEMORY_MAX_MOVES


def test_new_games_economy():
    for g in ("math", "flags", "code", "memory"):
        assert economy.DAILY_WIN_LIMITS[g] > 0
    assert economy.GAME_MILESTONES == {"quiz": ("stone", 10), "math": ("energy", 10)}
    assert economy.win_reward_for("code") == 5 and economy.win_reward_for("math") == economy.WIN_REWARD
    # удача (КНБ, Больше-Меньше, Сейф) — только простые ресурсы
    for g in ("rps", "hl", "safe"):
        assert economy.GAME_RESOURCE[g] in economy.RESOURCE_KINDS and g not in economy.GAME_MILESTONES


def test_new_games_in_app_and_api():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for fn in ("function gameTimed", "function gameCode", "function gameMemory", 'GAMES_SOON = ["words"]'):
        assert fn in html, fn
    src = (ROOT / "bots" / "main_bot" / "webapp_games.py").read_text(encoding="utf-8")
    for route in ("/api/math/next", "/api/math/answer", "/api/flags/next", "/api/flags/answer",
                  "/api/code/new", "/api/code/guess", "/api/memory/new", "/api/memory/flip"):
        assert f'"{route}"' in src, route
    # верный ответ флагов и колода мемори не уходят в приложение до конца раунда
    assert '("correct", "iso")' in src and 'deck=state["deck"]' in src


def test_app_script_has_no_duplicate_top_level_names():
    """Повторный const/function на верхнем уровне скрипта — SyntaxError, и приложение не открывается целиком
    (27.10: resLine склада и игр). Ловим грубым разбором: объявления с отступом в 2 пробела."""
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    names = re.findall(r"^  (?:async function|function|const|let) ([A-Za-z_$][\w$]*)", html, re.M)
    dups = sorted({n for n in names if names.count(n) > 1})
    assert not dups, dups


def test_timer_starts_on_display_but_prefetch_gives_at_most_the_slack():
    """Предзагрузка вопроса: таймер — с показа, но не позже created_at + PREFETCH_SLACK_SECONDS."""
    from datetime import datetime, timedelta, timezone
    from bots.main_bot.webapp_games import answered_in_time
    t0 = datetime(2026, 10, 27, tzinfo=timezone.utc)
    full = economy.QUIZ_ANSWER_SECONDS + economy.GAME_ANSWER_GRACE_SECONDS
    slack = economy.PREFETCH_SLACK_SECONDS
    sec = lambda n: timedelta(seconds=n)
    # показан через 3 с после выдачи — у игрока все 30 с от показа
    assert answered_in_time(t0, t0 + sec(3 + full), economy.QUIZ_ANSWER_SECONDS, t0 + sec(3))
    assert not answered_in_time(t0, t0 + sec(3 + full + 1), economy.QUIZ_ANSWER_SECONDS, t0 + sec(3))
    # «показан» через минуту (вопрос читали заранее) — форы не больше slack
    assert not answered_in_time(t0, t0 + sec(slack + full + 1), economy.QUIZ_ANSWER_SECONDS, t0 + sec(60))
    # без показа — от выдачи, как раньше
    assert not answered_in_time(t0, t0 + sec(full + 1), economy.QUIZ_ANSWER_SECONDS)


def _win_path(quest):
    """Кратчайший путь к победе: [(сцена, индекс выбора)] — BFS по (сцена, флаги)."""
    from collections import deque
    from bots.main_bot.utils.quest_loader import visible_choices
    start = (quest["start"], frozenset())
    prev, todo = {start: None}, deque([start])
    while todo:
        node = todo.popleft()
        scene = quest["scenes"][node[0]]
        if scene.get("end") == "win":
            path = []
            while prev[node]:
                node, step = prev[node]
                path.append(step)
            return path[::-1]
        for i, ch in visible_choices(scene, set(node[1])):
            nxt = (ch["goto"], node[1] | frozenset(ch.get("set", [])))
            if nxt not in prev:
                prev[nxt] = (node, (node[0], i))
                todo.append(nxt)
    return None


def test_quest_scene_payload_shows_only_visible_choices_with_original_indexes():
    from bots.main_bot.utils.quest_loader import all_quests
    from bots.main_bot.webapp_quests import scene_payload
    for q in all_quests():
        assert _win_path(q), q["id"]
        p = scene_payload(q, q["start"], set())
        assert p["choices"] and all(q["scenes"][q["start"]]["choices"][c["i"]]["label"] == c["label"] for c in p["choices"])
        win_key = next(k for k, sc in q["scenes"].items() if sc.get("end") == "win")
        assert scene_payload(q, win_key, set())["choices"] == []


def test_quests_live_in_the_app():
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "function viewQuests" in html and "function questScene" in html and '"/api/quest/choose"' in html
    assert "Дуэли и квесты" not in html and "Duels and quests" not in html
