"""
🗺 Движок квестов — общий для чата (/quests) и приложения (вкладка «🕹 Игры» → «🗺 Квесты»), шаг 3 плана 27.10.

Сценарии — JSON в data/quests (загрузчик и валидатор — bots/main_bot/utils/quest_loader.py). Прогресс в quest_progress
(сцена + флаги, переживает рестарты); награда — только за ПЕРВУЮ победу (ledger quest_reward + набор ресурсов),
платные подсказки — ledger quest_hint. choose() вызывается ВНУТРИ транзакции.

Ротация v3 (владелец 30.10): каждый день UTC всем показываются ОДНИ И ТЕ ЖЕ QUEST_ROTATION_SIZE случайных обычных квестов
из всего банка (daily_rotation — перемешивание по дате); тумблер quest:<id> теперь значит «в банке ротации» (по умолчанию
да; выключенный владельцем квест не выпадает). Начатый и недопройденный квест остаётся в списке игрока, пока не пройден.
Ротация v2 (владелец 27.10): эпики (epic:<id>, поле
"epic": true в JSON — событие ≥20 минут, ТОЛЬКО с ⚡ Безлимитом: «эпики должны быть платными»). За сутки UTC
засчитываются QUEST_DAILY_NEW новых прохождений; потом непройденные квесты гаснут до 00:00 (Безлимит снимает),
пройденные переигрываются без ограничений.
"""
from __future__ import annotations

import hashlib
import json

from datetime import timedelta

from bots.main_bot.utils.quest_loader import all_quests, normalize_answer, visible_choices, visit_key
from shared.economy import (QUEST_DAILY_NEW, QUEST_STONE_KIND, quest_stones, QUEST_ROTATION_SIZE,
                            RESOURCE_KINDS, is_active, utcnow)
from shared.feature_flags import get_flag
from shared.ledger import InsufficientFunds, change_balance
from shared.resources import grant_bundle, resource_capacity


class QuestStale(Exception):
    """Выбор в сцене, которая уже позади (старое сообщение / вторая вкладка): current — актуальная сцена."""

    def __init__(self, current: str, flags: set[str]):
        super().__init__(current)
        self.current, self.flags = current, flags


class QuestLocked(Exception):
    """Квест закрыт: reason "day" — новые прохождения на сегодня закончились, "epic" — эпик только с Безлимитом."""

    def __init__(self, reason: str = "day"):
        super().__init__(reason)
        self.reason = reason


class QuestNoCoins(Exception):
    def __init__(self, cost: int):
        super().__init__(cost)
        self.cost = cost


def visits_of(raw) -> dict:
    if raw is None:
        return {}
    return json.loads(raw) if isinstance(raw, str) else dict(raw)


def flags_of(row) -> set[str]:
    raw = row["flags"] if row else "[]"
    return set(json.loads(raw) if isinstance(raw, str) else raw)


def is_finished(quest: dict, scene_key: str) -> bool:
    scene = quest["scenes"].get(scene_key)
    return bool(scene and scene.get("end"))


def is_epic(quest: dict) -> bool:
    return bool(quest.get("epic"))


def flag_key(quest: dict) -> str:
    return f"{'epic' if is_epic(quest) else 'quest'}:{quest['id']}"


def total_count() -> int:
    """Сколько квестов в базе всего (динамический счётчик на плашке: «доступ к большему — с Безлимитом»)."""
    return len(all_quests())


def daily_rotation(pool: list[dict], day) -> list[dict]:
    """Квесты дня: одинаковые для всех — порядок задаёт хэш (дата, id), меняется каждые сутки UTC."""
    def key(q):
        return hashlib.sha256(f"{day.isoformat()}:{q['id']}".encode()).hexdigest()
    return sorted(pool, key=key)[:QUEST_ROTATION_SIZE]


async def visible_quests(day=None) -> list[dict]:
    """Список дня: включённые эпики (события) первыми, затем QUEST_ROTATION_SIZE случайных квестов дня из банка."""
    epics, pool = [], []
    for q in all_quests():
        if await get_flag(flag_key(q)):
            (epics if is_epic(q) else pool).append(q)
    return epics + daily_rotation(pool, day or utcnow().date())


async def visible_for(conn, user_id: int, day=None) -> list[dict]:
    """Список игрока: квесты дня + его начатые и не пройденные (чтобы смена дня не обрывала прохождение)."""
    quests = await visible_quests(day)
    shown = {q["id"] for q in quests}
    rows = await conn.fetch("SELECT quest_id, scene FROM quest_progress WHERE user_id = $1 AND completed_at IS NULL",
                            user_id)
    by_id = {q["id"]: q for q in all_quests()}
    for r in rows:
        q = by_id.get(r["quest_id"])
        if q and q["id"] not in shown and not is_finished(q, r["scene"]) and (not is_epic(q) or await get_flag(flag_key(q))):
            quests.append(q)
            shown.add(q["id"])
    return quests


async def daily_state(conn, user_id: int) -> dict:
    """{done: новых прохождений сегодня (без эпиков), max, unlimited, locked: исчерпан ли лимит}."""
    now = utcnow()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    epic_ids = [q["id"] for q in all_quests() if is_epic(q)]
    done = await conn.fetchval("SELECT COUNT(*) FROM quest_progress WHERE user_id = $1 AND completed_at >= $2 "
                               "AND NOT (quest_id = ANY($3::text[]))", user_id, day_start, epic_ids)
    unlimited = is_active(await conn.fetchval("SELECT unlimit_until FROM users WHERE user_id = $1", user_id), now)
    return {"done": done, "max": QUEST_DAILY_NEW, "unlimited": unlimited,
            "locked": not unlimited and done >= QUEST_DAILY_NEW}


def lock_reason(quest: dict, prog, daily: dict) -> str | None:
    """None — играть можно; "epic" — эпик без Безлимита; "day" — лимит новых исчерпан, а квест ещё не пройден."""
    if is_epic(quest):
        return None if daily["unlimited"] else "epic"
    if daily["locked"] and not (prog and prog["completed_at"]):
        return "day"
    return None


def locked_for(quest: dict, prog, daily: dict) -> bool:
    return lock_reason(quest, prog, daily) is not None


async def quest_accessible(conn, quest_id: str, user_id: int) -> bool:
    """Квест сегодня в списке игрока — или он его уже начинал (доигрывание / переигровка пройденного)."""
    quest = next((q for q in all_quests() if q["id"] == quest_id), None)
    if quest is None:
        return False
    if any(q["id"] == quest_id for q in await visible_quests()):
        return True
    return bool(await conn.fetchval("SELECT 1 FROM quest_progress WHERE user_id = $1 AND quest_id = $2",
                                    user_id, quest_id))


async def completed_ids(conn, user_id: int) -> set[str]:
    rows = await conn.fetch("SELECT quest_id FROM quest_progress WHERE user_id = $1 AND completed_at IS NOT NULL",
                            user_id)
    return {r["quest_id"] for r in rows}


async def progress(conn, user_id: int, quest_id: str):
    return await conn.fetchrow("SELECT scene, flags, completed_at, scene_at, tries, visits FROM quest_progress "
                               "WHERE user_id = $1 AND quest_id = $2", user_id, quest_id)


TIMER_GRACE_SECONDS = 2      # сеть и анимация: не отнимаем у игрока последние секунды


def timer_left(scene: dict, prog, now=None) -> int | None:
    """⏱ Сколько секунд осталось на сцене с таймером (None — таймера нет)."""
    timer = scene.get("timer")
    if not timer or not prog or prog.get("scene_at") is None:
        return None
    passed = ((now or utcnow()) - prog["scene_at"]).total_seconds()
    return max(0, int(timer["seconds"] - passed))


def _expired(scene: dict, prog, now=None) -> bool:
    timer = scene.get("timer")
    if not timer or prog["scene_at"] is None:
        return False
    return (now or utcnow()) > prog["scene_at"] + timedelta(seconds=timer["seconds"] + TIMER_GRACE_SECONDS)


def tries_left(scene: dict, prog) -> int | None:
    inp = scene.get("input")
    if not inp:
        return None
    return max(0, inp.get("tries", 3) - (prog["tries"] if prog else 0))


def status_of(quest: dict, prog) -> str:
    """new | progress | done — для карточки квеста."""
    if prog and prog["completed_at"]:
        return "done"
    if prog and not is_finished(quest, prog["scene"]):
        return "progress"
    return "new"


async def start(conn, user_id: int, quest: dict) -> None:
    """Начать (или начать заново) — со стартовой сцены, флаги сброшены; отметка первой победы сохраняется."""
    await conn.execute(
        """
        INSERT INTO quest_progress (user_id, quest_id, scene, flags, updated_at, scene_at, tries)
        VALUES ($1, $2, $3, '[]'::jsonb, NOW(), NOW(), 0)
        ON CONFLICT (user_id, quest_id) DO UPDATE SET scene = $3, flags = '[]'::jsonb, updated_at = NOW(),
            scene_at = NOW(), tries = 0, visits = '{}'::jsonb
        """, user_id, quest["id"], quest["start"])


def resume_point(quest: dict, prog) -> tuple[str, set[str]]:
    scene_key = prog["scene"] if prog and prog["scene"] in quest["scenes"] else quest["start"]
    return scene_key, flags_of(prog)


async def choose(conn, user_id: int, quest: dict, scene_key: str, idx: int) -> dict | None:
    """
    Выбор idx в сцене scene_key (внутри транзакции). None — квест не начат или выбора нет.
    Ошибки: QuestStale (сцена уже позади / выбор недоступен), QuestNoCoins (платная подсказка).
    Итог: {"scene": ключ новой сцены, "flags": set, "outcome": None | "win_first" | "win_repeat" | "fail"}.
    """
    qid = quest["id"]
    prog = await conn.fetchrow("SELECT * FROM quest_progress WHERE user_id = $1 AND quest_id = $2 FOR UPDATE",
                               user_id, qid)
    if not prog:
        return None
    flags = flags_of(prog)
    if (reason := lock_reason(quest, prog, await daily_state(conn, user_id))) is not None:
        raise QuestLocked(reason)
    if prog["scene"] != scene_key:
        current = prog["scene"] if prog["scene"] in quest["scenes"] else quest["start"]
        raise QuestStale(current, flags)
    scene = quest["scenes"][scene_key]
    choices = scene.get("choices") or []
    if not 0 <= idx < len(choices):
        return None
    choice = choices[idx]
    if (idx, choice) not in visible_choices(scene, flags):   # перепроверка по текущим флагам
        raise QuestStale(scene_key, flags)
    if _expired(scene, prog):                                 # ⏱ не успел(а) — выбор не засчитывается
        return {**await _move(conn, user_id, quest, prog, scene["timer"]["goto"], flags), "timeout": True}

    cost = choice.get("cost") or 0
    if cost:
        try:
            await change_balance(conn, user_id, -cost, "quest_hint", f"{qid}:{scene_key}")
        except InsufficientFunds:
            raise QuestNoCoins(cost) from None

    return await _move(conn, user_id, quest, prog, choice["goto"], flags | set(choice.get("set", [])))


async def _move(conn, user_id: int, quest: dict, prog, target_key: str, new_flags: set[str]) -> dict:
    """Переход в сцену: награда за первую победу, отметка концовки, сброс таймера и попыток."""
    qid = quest["id"]
    target = quest["scenes"][target_key]
    outcome = None
    if target.get("end") == "win":
        if prog["completed_at"] is None:
            await conn.execute("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            await change_balance(conn, user_id, quest["reward_coins"], "quest_reward", qid)
            await grant_bundle(conn, user_id, {QUEST_STONE_KIND: quest_stones(quest["reward_coins"], is_epic(quest))},
                               "quest_reward", qid, cap=await resource_capacity(conn, user_id))
            await conn.execute("UPDATE quest_progress SET completed_at = NOW() WHERE user_id = $1 AND quest_id = $2",
                               user_id, qid)
            outcome = "win_first"
        else:
            outcome = "win_repeat"
    elif target.get("end") == "fail":
        outcome = "fail"
    who = visit_key(target_key, target)
    visits = await conn.fetchval(
        "UPDATE quest_progress SET scene = $3, flags = $4::jsonb, updated_at = NOW(), scene_at = NOW(), tries = 0, "
        "visits = visits || jsonb_build_object($5::text, COALESCE((visits->>$5::text)::int, 0) + 1) "
        "WHERE user_id = $1 AND quest_id = $2 RETURNING visits", user_id, qid, target_key, json.dumps(sorted(new_flags)), who)
    return {"scene": target_key, "flags": new_flags, "outcome": outcome, "scene_at": utcnow(), "tries": 0,
            "visits": visits_of(visits)}


async def _locked_scene(conn, user_id: int, quest: dict, scene_key: str):
    """Строка прогресса под блокировкой и проверки «квест открыт» и «это текущая сцена»."""
    prog = await conn.fetchrow("SELECT * FROM quest_progress WHERE user_id = $1 AND quest_id = $2 FOR UPDATE",
                               user_id, quest["id"])
    if not prog:
        return None
    if (reason := lock_reason(quest, prog, await daily_state(conn, user_id))) is not None:
        raise QuestLocked(reason)
    if prog["scene"] != scene_key:
        current = prog["scene"] if prog["scene"] in quest["scenes"] else quest["start"]
        raise QuestStale(current, flags_of(prog))
    return prog


async def answer(conn, user_id: int, quest: dict, scene_key: str, text: str) -> dict | None:
    """
    🔐 Ввод ответа (ребус, шифр, код) в сцене с "input" — внутри транзакции. Верно → input.ok (+ input.set);
    неверно → попытка сгорает, кончились → input.fail. Таймер истёк → timer.goto, ответ не засчитывается.
    Итог как у choose + "wrong": True и "tries_left", если ответ неверный, но попытки остались.
    """
    prog = await _locked_scene(conn, user_id, quest, scene_key)
    if prog is None:
        return None
    scene = quest["scenes"][scene_key]
    inp = scene.get("input")
    if not inp:
        return None
    flags = flags_of(prog)
    if _expired(scene, prog):
        return {**await _move(conn, user_id, quest, prog, scene["timer"]["goto"], flags), "timeout": True}
    given = normalize_answer(text)
    if given and any(given == normalize_answer(a) for a in inp["answers"]):
        return await _move(conn, user_id, quest, prog, inp["ok"], flags | set(inp.get("set", [])))
    tries = prog["tries"] + 1
    if tries >= inp.get("tries", 3):
        return {**await _move(conn, user_id, quest, prog, inp["fail"], flags), "wrong": True}
    await conn.execute("UPDATE quest_progress SET tries = $3 WHERE user_id = $1 AND quest_id = $2", user_id, quest["id"], tries)
    return {"scene": scene_key, "flags": flags, "outcome": None, "wrong": True,
            "scene_at": prog["scene_at"], "tries": tries, "visits": visits_of(prog["visits"])}


async def timeout(conn, user_id: int, quest: dict, scene_key: str) -> dict | None:
    """⏱ Время сцены вышло — переход в timer.goto. Время считает сервер: рано — None (приложение ждёт дальше)."""
    prog = await _locked_scene(conn, user_id, quest, scene_key)
    if prog is None:
        return None
    scene = quest["scenes"][scene_key]
    if not _expired(scene, prog):
        return None
    return {**await _move(conn, user_id, quest, prog, scene["timer"]["goto"], flags_of(prog)), "timeout": True}
