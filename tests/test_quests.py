"""
Движок квестов: валидация сценариев, фильтрация выборов, графы прохождений.

Главная гарантия: каждый боевой сценарий корректен (все переходы существуют,
победа достижима, callback'и влезают в лимит Telegram) — битый JSON не доедет
до игроков, тест упадёт раньше.
"""
import pytest

from bots.main_bot.utils.quest_loader import (
    QUESTS_DIR,
    all_quests,
    get_quest,
    load_quests,
    validate_quest,
    scene_edges,
    visible_choices,
    win_reachable,
)


@pytest.fixture(autouse=True)
def _load():
    load_quests(QUESTS_DIR)


# ---------------------------------------------------------------- боевые сценарии
def test_all_quests_loaded_in_order():
    """3 флагмана + 7 «в запас» под ротацию (/quests_admin). Порядок — поле order."""
    quests = all_quests()
    ids = [q["id"] for q in quests]
    assert ids[:10] == [
        "golden_cutlet", "miner_career", "locked_safe",
        "night_drone", "cutlet_exchange", "robot_chef",
        "ice_expedition", "space_signal", "blackout", "metro_veteran",
    ]
    assert "forty_candles" in ids   # ⭐ эпик (27.10) — вне ротации, только с Безлимитом
    # банк растёт заходами (docs/quests/QUEUE.md): порядок — по order, без повторов
    orders = [q["order"] for q in quests]
    assert orders == sorted(orders) and len(set(orders)) == len(orders) and len(set(ids)) == len(ids)


def test_every_quest_is_valid():
    for q in all_quests():
        assert validate_quest(q) == [], q["id"]


def test_win_is_reachable_in_every_quest():
    """BFS по (сцена, флаги): из старта обязан существовать путь к победе."""
    for q in all_quests():
        assert win_reachable(q), f"{q['id']}: победа недостижима!"


def test_every_scene_is_reachable_from_start():
    """Мёртвых сцен нет: каждая сцена достижима хоть каким-то путём."""
    for q in all_quests():
        scenes = q["scenes"]
        seen_scenes: set[str] = set()
        seen_states: set[tuple[str, frozenset]] = set()
        stack = [(q["start"], frozenset())]
        while stack:
            key, flags = stack.pop()
            if (key, flags) in seen_states:
                continue
            seen_states.add((key, flags))
            seen_scenes.add(key)
            scene = scenes[key]
            if scene.get("end"):
                continue
            for goto, add in scene_edges(scene, set(flags)):   # выборы + ввод ответа + таймер
                stack.append((goto, flags | add))
        dead = set(scenes) - seen_scenes
        assert not dead, f"{q['id']}: недостижимые сцены {dead}"


def test_no_stuck_states():
    """В любом достижимом состоянии не-концовки есть хотя бы один видимый выбор."""
    for q in all_quests():
        scenes = q["scenes"]
        seen: set[tuple[str, frozenset]] = set()
        stack = [(q["start"], frozenset())]
        while stack:
            key, flags = stack.pop()
            if (key, flags) in seen:
                continue
            seen.add((key, flags))
            scene = scenes[key]
            if scene.get("end"):
                continue
            edges = scene_edges(scene, set(flags))
            assert edges, f"{q['id']}/{key}: тупик при флагах {sorted(flags)}"
            for goto, add in edges:
                stack.append((goto, flags | add))


def test_rewards_and_hints_are_sane():
    for q in all_quests():
        assert 20 <= q["reward_coins"] <= 100, q["id"]  # владелец 27.10: обычные 20–50, эпик 100
        for key, scene in q["scenes"].items():
            for ch in scene.get("choices") or []:
                if ch.get("cost"):
                    assert ch["cost"] <= q["reward_coins"], f"{q['id']}/{key}: подсказка дороже награды"


def test_detective_requires_evidence_for_win():
    """Сюжетная гарантия: в детективе нельзя победить без изобличения В.И.К."""
    q = get_quest("golden_cutlet")
    accuse = q["scenes"]["accuse"]
    win_choices = [ch for ch in accuse["choices"] if ch["goto"] == "end_win"]
    assert win_choices and all("vik_caught" in ch.get("need", []) for ch in win_choices)


def test_safe_door_is_typed_by_hand_under_a_timer():
    """27.10, вечер: код двери игрок НАБИРАЕТ сам (кнопки с готовым кодом нет), одна попытка и 90 секунд."""
    q = get_quest("locked_safe")
    door = q["scenes"]["door"]
    assert door["input"]["answers"] == ["4607"] and door["input"]["ok"] == "end_win" and door["input"]["tries"] == 1
    assert door["timer"]["goto"] == "end_timeout" and q["scenes"]["end_timeout"]["end"] == "fail"
    assert all("4607" not in ch["label"] and "4-6-0-7" not in ch["label"] for ch in door["choices"])
    # каждая из четырёх головоломок открывает свою цифру
    sets = {f for k in ("pa_win", "pb_win", "pc_win", "pd_win") for ch in q["scenes"][k]["choices"] for f in ch.get("set", [])}
    assert {"digit_a", "digit_b", "digit_c", "digit_d"} <= sets


def test_answers_are_normalized_and_validator_checks_input_and_timer():
    from bots.main_bot.utils.quest_loader import normalize_answer
    assert normalize_answer(" Ёлка - 1 ") == normalize_answer("елка1") == "елка1"
    assert normalize_answer("4-6-0-7") == "4607"
    q = _mini_quest()
    q["scenes"]["a"]["input"] = {"answers": ["x"], "ok": "nowhere", "fail": "w"}
    q["scenes"]["a"]["timer"] = {"seconds": 5, "goto": "w"}
    errs = " ".join(validate_quest(q))
    assert "input.ok" in errs and "timer.seconds" in errs


def test_annoyed_line_after_third_visit():
    from bots.main_bot.utils.quest_loader import ANNOY_AFTER_VISITS, annoyed_line
    q = get_quest("forty_candles")
    assert annoyed_line(q, "vera", {"vera": 1}) == ""
    first = annoyed_line(q, "vera", {"vera": ANNOY_AFTER_VISITS})
    assert first and first == q["scenes"]["vera"]["annoyed"][0]
    # сцена-пересказ того же персонажа берёт его реплики
    assert annoyed_line(q, "vera_note", {"vera": 99}) == q["scenes"]["vera"]["annoyed"][-1]
    # галочек «уже выяснено» больше нет — о повторах скажет сам персонаж
    assert not any(ch["label"].endswith("✓") for sc in q["scenes"].values() for ch in sc.get("choices", []))


# ---------------------------------------------------------------- валидатор и фильтр
def _mini_quest(**overrides):
    q = {
        "id": "mini", "order": 1, "title": "t", "genre": "g", "minutes": "5",
        "teaser": "tz", "reward_coins": 30, "start": "a",
        "scenes": {
            "a": {"text": "x", "choices": [{"label": "go", "goto": "w"}]},
            "w": {"text": "win", "end": "win"},
        },
    }
    q.update(overrides)
    return q


def test_validator_catches_broken_goto():
    q = _mini_quest()
    q["scenes"]["a"]["choices"][0]["goto"] = "nowhere"
    assert any("не существует" in e for e in validate_quest(q))


def test_validator_catches_missing_win_and_dead_end():
    q = _mini_quest()
    q["scenes"]["w"] = {"text": "oops"}  # ни end, ни choices
    errors = validate_quest(q)
    assert any("тупик" in e for e in errors)
    assert any("победной концовки" in e for e in errors)


def test_validator_passes_good_quest():
    assert validate_quest(_mini_quest()) == []


def test_visible_choices_need_missing():
    scene = {"choices": [
        {"label": "a", "goto": "x"},
        {"label": "b", "goto": "x", "need": ["key"]},
        {"label": "c", "goto": "x", "missing": ["key"]},
    ]}
    without = [i for i, _ in visible_choices(scene, set())]
    with_key = [i for i, _ in visible_choices(scene, {"key"})]
    assert without == [0, 2]
    assert with_key == [0, 1]


def test_age_16_label_is_the_only_allowed_age():
    """🔞 14.11: "age": 16 — бейдж и предупреждение; другие значения — ошибка (без поля квест 12+)."""
    import copy
    from pathlib import Path
    q = _mini_quest()
    assert validate_quest(dict(copy.deepcopy(q), age=16)) == []
    assert any("age" in e for e in validate_quest(dict(copy.deepcopy(q), age=18)))
    html = (Path(__file__).resolve().parents[1] / "static" / "webapp" / "index.html").read_text(encoding="utf-8")
    assert "qs_ageWarn" in html and 'localStorage.getItem("age16_"' in html
