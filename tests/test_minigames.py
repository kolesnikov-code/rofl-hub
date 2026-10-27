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
    names = re.findall(r"^  (?:async function|function) ([A-Za-z_$][\w$]*)", html, re.M)
    # const/let — со всеми именами через запятую («const A = 1, MOVES = […]» — 27.10 так пропустили MOVES)
    for m in re.finditer(r"^  (?:const|let) ", html, re.M):
        names += _declared_names(html, m.end())
    dups = sorted({n for n in names if names.count(n) > 1})
    assert not dups, dups


def _declared_names(src: str, i: int) -> list[str]:
    """Имена из объявления const/let, начиная с позиции i: делим по запятым верхнего уровня до конца оператора."""
    parts, depth, quote, start = [], 0, None, i
    while i < len(src):
        ch = src[i]
        if quote:
            if ch == "\\":
                i += 1
            elif ch == quote:
                quote = None
        elif ch in "\"'`":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif depth == 0 and ch == ",":
            parts.append(src[start:i])
            start = i + 1
        elif depth == 0 and (ch == ";" or (ch == "\n" and not src[start:i].rstrip().endswith((",", "=", "+", "(", "?", ":")))):
            break
        i += 1
    parts.append(src[start:i])
    return [m.group(1) for p in parts if (m := re.match(r"\s*([A-Za-z_$][\w$]*)\s*=", p))]


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
        steps = [((node[0], i), ch["goto"], frozenset(ch.get("set", []))) for i, ch in visible_choices(scene, set(node[1]))]
        if (inp := scene.get("input")):          # 🔐 верный ответ — тоже шаг
            steps.append(((node[0], "answer"), inp["ok"], frozenset(inp.get("set", []))))
        for step, goto, add in steps:
            nxt = (goto, node[1] | add)
            if nxt not in prev:
                prev[nxt] = (node, step)
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


def test_quest_moods_exist_in_the_fx_engine_and_every_scene_has_atmosphere():
    """✨ Каждая метка mood в сценариях — реальный эффект static/webapp/fx.js; у каждой сцены есть атмосфера."""
    from bots.main_bot.utils.quest_loader import all_quests
    from bots.main_bot.webapp_quests import scene_mood
    fx = (ROOT / "static" / "webapp" / "fx.js").read_text(encoding="utf-8")
    effects = set(re.findall(r"^    (\w+):\s+\{ g: \"", fx, re.M))
    assert len(effects) >= 60
    for q in all_quests():
        for key in q["scenes"]:
            moods = scene_mood(q, key)
            assert moods, (q["id"], key)
            assert set(moods) <= effects, (q["id"], key, moods)


def test_fx_engine_is_safe_and_served():
    fx = (ROOT / "static" / "webapp" / "fx.js").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in fx and "fx_off" in fx            # можно выключить, «меньше движения» уважается
    assert "rnd(6000, 14000)" in fx                                      # молния — редко, без стробоскопа
    assert "Math.min(window.devicePixelRatio || 1, 1.5)" in fx           # холст не жрёт батарею на 3x-экранах
    src = (ROOT / "bots" / "main_bot" / "webapp.py").read_text(encoding="utf-8")
    assert '"/fx.js"' in src
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "QuestFX.stop()" in html and 'sc.src = "fx.js"' in html


def test_quiz_report_button_reasons_route_and_owner_command():
    """⚠️ 27.10: жалоба на вопрос — кнопка после ответа, причины = REASONS сервера, маршрут и /quiz_reports владельца."""
    from shared.quiz_reports import REASON_RU, REASONS
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    js = re.search(r'const QR_REASONS = \[([^\]]*)\]', html).group(1)
    assert tuple(re.findall(r'"(\w+)"', js)) == REASONS and set(REASON_RU) == set(REASONS)
    assert '"/api/quiz/report"' in html and 'quizReport(box.querySelector("#qRep"), q.round_id)' in html
    for k in ("qr_btn", "qr_title", "qr_thanks", "qr_limit", *("qr_" + r for r in REASONS)):
        assert html.count(k + ":") == 2, k                          # ru и en в самом приложении
    web = (ROOT / "bots" / "main_bot" / "webapp_games.py").read_text(encoding="utf-8")
    assert '"/api/quiz/report", handle_quiz_report' in web
    admin = (ROOT / "bots" / "admin_notifier_bot" / "bot.py").read_text(encoding="utf-8")
    assert 'Command("quiz_reports")' in admin and "/quiz_reports" in admin and 'startswith("qrep_done:")' in admin
    assert economy.QUIZ_REPORT_DAILY_LIMIT > 0


def test_quest_rotation_v2_rules_and_app_ui():
    """🗺 27.10 ротация v2: 3 новых прохождения в сутки, потом непройденные гаснут; эпики вне лимита; новые — скрыты."""
    from shared import quest_engine as qe
    from shared.feature_flags import _default_for
    assert economy.QUEST_ROTATION_SIZE == 10 and economy.QUEST_DAILY_NEW == 3
    assert _default_for("quest:new_one") is False and _default_for("epic:big") is False
    locked = {"done": 3, "max": 3, "unlimited": False, "locked": True}
    free = {"done": 1, "max": 3, "unlimited": False, "locked": False}
    q, epic = {"id": "a"}, {"id": "e", "epic": True}
    assert qe.locked_for(q, None, locked) and not qe.locked_for(q, None, free)
    assert not qe.locked_for(q, {"completed_at": "x"}, locked)            # пройденный — переигрывается
    unl = {"done": 9, "max": 3, "unlimited": True, "locked": False}
    assert qe.lock_reason(epic, None, free) == "epic"                     # эпик платный: только с Безлимитом
    assert qe.lock_reason(epic, None, unl) is None and qe.lock_reason(q, None, locked) == "day"
    assert qe.flag_key(epic) == "epic:e" and qe.flag_key(q) == "quest:a"
    html = (ROOT / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    for k in ("qs_total", "qs_daily", "qs_dailyUnl", "qs_locked", "qs_lockedNote", "qs_epic"):
        assert html.count(k + ":") == 2, k
    assert "q.locked === \"day\" ? ' dim'" in html and 'id="qsUnlim"' in html and "data-unlim" in html
    assert html.count("qs_epicPaid:") == 2 and html.count("qs_paper:") == 2
    admin = (ROOT / "bots" / "admin_notifier_bot" / "bot.py").read_text(encoding="utf-8")
    assert 'F.data == "epic_pick"' in admin and "Внести эпик в список" in admin and 'Command("unlimit")' in admin
    db_src = (ROOT / "shared" / "database.py").read_text(encoding="utf-8")
    assert "('quest:golden_cutlet', TRUE)" in db_src                     # первые три остаются видны после смены дефолта


def test_owner_pult_has_quests_tab_and_unlimit_and_mirror_has_no_stock_phrase():
    """27.10: эпики/ротация и Безлимит по @username — и в пульте-приложении; зеркало без дежурной надписи."""
    pult = (ROOT / "static" / "webapp" / "admin.html").read_text(encoding="utf-8")
    api = (ROOT / "bots" / "main_bot" / "webapp_admin.py").read_text(encoding="utf-8")
    assert 'quests: ["🗺 Квесты", viewQuests]' in pult and '"/api/admin/unlimit"' in pult
    for route in ('"/api/admin/quests"', '"/api/admin/quest"', '"/api/admin/unlimit"'):
        assert route in api
    fx = (ROOT / "static" / "webapp" / "fx.js").read_text(encoding="utf-8")
    assert "Я РЯДОМ" not in fx and 'special: "keypad"' in fx and 'special: "candles"' in fx


def test_no_horror_in_comedies_and_lock_words_in_every_language():
    """27.10: «только в комедию случайно не вставь» — валидатор режет хоррор-эффекты в комедиях;
    кодовый замок показывает исход сюжета (fx_lock) словами на языке игрока — все 14 языков."""
    from bots.main_bot.utils.quest_loader import HORROR_MOODS, validate_quest
    from shared.locales import SUPPORTED_LANGS
    base = {"id": "fun", "title": "t", "teaser": "t", "genre": "Комедия", "minutes": "5", "reward_coins": 50, "start": "a",
            "scenes": {"a": {"text": "x", "mood": "mirror", "choices": [{"label": "b", "goto": "w"}]},
                       "w": {"text": "y", "end": "win"}}}
    assert any("комедии" in e for e in validate_quest(base))
    base["genre"] = "Мистика"
    assert validate_quest(base) == []
    base["scenes"]["a"]["fx_lock"] = "maybe"
    assert any("fx_lock" in e for e in validate_quest(base))
    assert {"mirror", "handprints", "skulls"} <= HORROR_MOODS
    fx = (ROOT / "static" / "webapp" / "fx.js").read_text(encoding="utf-8")
    words = fx[fx.index("const FX_WORDS"):fx.index("const RUNES")]
    for lang in SUPPORTED_LANGS:
        assert re.search(r"\b" + lang + r": \{ open: \"[^\"]+\", error: \"[^\"]+\" \}", words), lang
    assert "Math.random() < .4" not in fx                                 # «открыто» — только если открылось по сюжету
