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
    assert [q["id"] for q in quests] == [
        "golden_cutlet", "miner_career", "locked_safe",
        "night_drone", "cutlet_exchange", "robot_chef",
        "ice_expedition", "space_signal", "blackout", "metro_veteran",
        "forty_candles",   # ⭐ эпик (27.10) — вне ротации, только с Безлимитом
    ]


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
            for _, ch in visible_choices(scene, set(flags)):
                stack.append((ch["goto"], flags | frozenset(ch.get("set", []))))
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
            visible = visible_choices(scene, set(flags))
            assert visible, f"{q['id']}/{key}: тупик при флагах {sorted(flags)}"
            for _, ch in visible:
                stack.append((ch["goto"], flags | frozenset(ch.get("set", []))))


def test_rewards_and_hints_are_sane():
    for q in all_quests():
        assert 50 <= q["reward_coins"] <= 500, q["id"]
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


def test_safe_door_requires_all_four_digits():
    q = get_quest("locked_safe")
    door = q["scenes"]["door"]
    win = [ch for ch in door["choices"] if ch["goto"] == "end_win"]
    assert win and set(win[0]["need"]) == {"digit_a", "digit_b", "digit_c", "digit_d"}


# ---------------------------------------------------------------- валидатор и фильтр
def _mini_quest(**overrides):
    q = {
        "id": "mini", "order": 1, "title": "t", "genre": "g", "minutes": "5",
        "teaser": "tz", "reward_coins": 100, "start": "a",
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
