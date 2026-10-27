"""
🗺 Движок квестов — общий для чата (/quests) и приложения (вкладка «🕹 Игры» → «🗺 Квесты»), шаг 3 плана 27.10.

Сценарии — JSON в data/quests (загрузчик и валидатор — bots/main_bot/utils/quest_loader.py). Прогресс в quest_progress
(сцена + флаги, переживает рестарты); награда — только за ПЕРВУЮ победу (ledger quest_reward + набор ресурсов),
платные подсказки — ledger quest_hint. choose() вызывается ВНУТРИ транзакции.

Ротация v2 (владелец 27.10): в списке до QUEST_ROTATION_SIZE квестов (тумблеры quest:<id>) + эпики (epic:<id>, поле
"epic": true в JSON — событие, вне лимитов). За сутки UTC засчитываются QUEST_DAILY_NEW новых прохождений; потом
непройденные квесты гаснут до 00:00 (Безлимит снимает), пройденные переигрываются без ограничений.
"""
from __future__ import annotations

import json

from bots.main_bot.utils.quest_loader import all_quests, visible_choices
from shared.economy import (QUEST_DAILY_NEW, QUEST_EXTRA_BUNDLE, QUEST_RESOURCE_BUNDLE, QUEST_ROTATION_SIZE,
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
    """Новые прохождения на сегодня закончились (QUEST_DAILY_NEW) — квест погас до 00:00 UTC."""


class QuestNoCoins(Exception):
    def __init__(self, cost: int):
        super().__init__(cost)
        self.cost = cost


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


async def visible_quests() -> list[dict]:
    """Включённые владельцем: эпики (события) первыми, затем ротация — не больше QUEST_ROTATION_SIZE."""
    epics, rotation = [], []
    for q in all_quests():
        if await get_flag(flag_key(q)):
            (epics if is_epic(q) else rotation).append(q)
    return epics + rotation[:QUEST_ROTATION_SIZE]


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


def locked_for(quest: dict, prog, daily: dict) -> bool:
    """Погас ли квест сегодня: лимит исчерпан, квест не эпик и ещё ни разу не пройден."""
    return daily["locked"] and not is_epic(quest) and not (prog and prog["completed_at"])


async def quest_accessible(conn, quest_id: str, user_id: int) -> bool:
    """Скрытый квест доступен лишь тем, кто его уже начал (доигрывание в ротации)."""
    quest = next((q for q in all_quests() if q["id"] == quest_id), None)
    if quest and await get_flag(flag_key(quest)):
        return True
    return bool(await conn.fetchval("SELECT 1 FROM quest_progress WHERE user_id = $1 AND quest_id = $2",
                                    user_id, quest_id))


async def completed_ids(conn, user_id: int) -> set[str]:
    rows = await conn.fetch("SELECT quest_id FROM quest_progress WHERE user_id = $1 AND completed_at IS NOT NULL",
                            user_id)
    return {r["quest_id"] for r in rows}


async def progress(conn, user_id: int, quest_id: str):
    return await conn.fetchrow("SELECT scene, flags, completed_at FROM quest_progress WHERE user_id = $1 AND quest_id = $2",
                               user_id, quest_id)


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
        INSERT INTO quest_progress (user_id, quest_id, scene, flags, updated_at)
        VALUES ($1, $2, $3, '[]'::jsonb, NOW())
        ON CONFLICT (user_id, quest_id) DO UPDATE SET scene = $3, flags = '[]'::jsonb, updated_at = NOW()
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
    if locked_for(quest, prog, await daily_state(conn, user_id)):
        raise QuestLocked()
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

    cost = choice.get("cost") or 0
    if cost:
        try:
            await change_balance(conn, user_id, -cost, "quest_hint", f"{qid}:{scene_key}")
        except InsufficientFunds:
            raise QuestNoCoins(cost) from None

    new_flags = flags | set(choice.get("set", []))
    target_key = choice["goto"]
    target = quest["scenes"][target_key]
    outcome = None
    if target.get("end") == "win":
        if prog["completed_at"] is None:
            await conn.execute("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", user_id)
            await change_balance(conn, user_id, quest["reward_coins"], "quest_reward", qid)
            await grant_bundle(conn, user_id, {**{k: QUEST_RESOURCE_BUNDLE for k in RESOURCE_KINDS}, **QUEST_EXTRA_BUNDLE},
                               "quest_reward", qid, cap=await resource_capacity(conn, user_id))
            await conn.execute("UPDATE quest_progress SET completed_at = NOW() WHERE user_id = $1 AND quest_id = $2",
                               user_id, qid)
            outcome = "win_first"
        else:
            outcome = "win_repeat"
    elif target.get("end") == "fail":
        outcome = "fail"
    await conn.execute("UPDATE quest_progress SET scene = $3, flags = $4::jsonb, updated_at = NOW() "
                       "WHERE user_id = $1 AND quest_id = $2", user_id, qid, target_key, json.dumps(sorted(new_flags)))
    return {"scene": target_key, "flags": new_flags, "outcome": outcome}
