"""
Загрузчик и чистая логика квестов. Сценарий — JSON-файл в data/quests/:

{
  "id": "golden_cutlet",            # ascii, попадает в callback_data
  "order": 1,                        # порядок в списке
  "title": "🕵️ Дело о золотой котлете",
  "genre": "Детектив", "minutes": "10–15",
  "teaser": "...",                   # карточка квеста
  "reward_coins": 150,               # награда за ПЕРВУЮ победу (далее — без наград)
  "start": "intro",
  "scenes": {
    "intro": {"text": "...", "choices": [
        {"label": "...", "goto": "scene2"},
        {"label": "...", "goto": "x", "set": ["clue"], "need": ["a"], "missing": ["b"], "cost": 25}
    ]},
    "end_win": {"text": "...", "end": "win"}
  }
}

Правила движка:
- выбор виден, если все need-флаги собраны и ни один missing-флаг не собран;
- "set" добавляет флаги при выборе; "cost" списывает монеты (платная подсказка);
- сцена с "end": "win"/"fail" завершает квест; у неё нет choices;
- "mood" (у квеста — по умолчанию, у сцены — своя) — атмосфера сцены в приложении (static/webapp/fx.js);
- "fx_text" (у сцены) — надпись для эффекта «🪞 запотевшее зеркало» — дословно фраза из сцены, от которой мурашки;
  без надписи палец рисует на стекле "fx_draw": "figure" (высокая фигура, по умолчанию) или "face" (лицо духа/зверя).
  Зеркало ставим только туда, где в тексте есть зеркало/стекло (ванная, шкаф, витрина), и НИКОГДА в комедии (HORROR_MOODS);
- "fx_lock" (у сцены с mood "keypad") — исход набора кода по сюжету: "open" или "error"; без него — только набор, без вердикта;
- "epic": true — эпик (~час игры): вне ротации и суточного лимита, владелец включает отдельно (тумблер epic:<id>).

Новый квест = новый JSON-файл, кода не требуется. Тесты проверяют каждый
сценарий: корректность переходов, достижимость победы, длину callback_data.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
QUESTS_DIR = PROJECT_ROOT / "data" / "quests"

_quests: dict[str, dict] = {}
# 😂 владелец 27.10: «только в комедию случайно не вставь» — жуткие эффекты в комедиях запрещены валидатором
HORROR_MOODS = frozenset({"mirror", "mirrorface", "mirrortext", "handprints", "ghosts", "ghostsE", "skulls", "eyes", "spiders"})
FX_TEXT_MAX = 32   # 🪞 надпись на запотевшем зеркале (mood "mirror"): короткая, чтобы влезла в 2 строки на телефоне


def _mood_ok(mood) -> bool:
    """✨ «mood» сцены/квеста (необязательно): строка-метка или список до двух меток (эффекты — static/webapp/fx.js)."""
    if mood is None:
        return True
    moods = [mood] if isinstance(mood, str) else mood
    return isinstance(moods, list) and 1 <= len(moods) <= 2 and all(isinstance(m, str) and m.isascii() and m for m in moods)


def validate_quest(q: dict) -> list[str]:
    """Список ошибок сценария (пустой — сценарий валиден)."""
    errors: list[str] = []
    qid = q.get("id", "")
    if not qid or not qid.replace("_", "").isascii() or not qid.replace("_", "").isalnum():
        errors.append(f"id должен быть ascii (буквы/цифры/_): {qid!r}")
    for field in ("title", "teaser", "genre", "minutes", "start"):
        if not q.get(field):
            errors.append(f"{qid}: нет поля {field}")
    if not isinstance(q.get("reward_coins"), int) or q["reward_coins"] < 0:
        errors.append(f"{qid}: reward_coins должен быть неотрицательным числом")

    scenes = q.get("scenes") or {}
    if q.get("start") not in scenes:
        errors.append(f"{qid}: стартовая сцена {q.get('start')!r} не найдена")

    if "epic" in q and not isinstance(q["epic"], bool):
        errors.append(f"{qid}: epic — true/false")
    if "notes" in q and not isinstance(q["notes"], bool):
        errors.append(f"{qid}: notes — true/false (совет «записывай детали на бумаге»)")
    if not _mood_ok(q.get("mood")):
        errors.append(f"{qid}: mood — метка атмосферы (static/webapp/fx.js) или список до двух меток")
    is_comedy = "омеди" in str(q.get("genre", "")).lower()
    if is_comedy and any(m in HORROR_MOODS for m in ([q.get("mood")] if isinstance(q.get("mood"), str) else q.get("mood") or [])):
        errors.append(f"{qid}: в комедии без хоррор-эффектов")
    endings = 0
    for key, scene in scenes.items():
        if not key.replace("_", "").isalnum() or not key.isascii():
            errors.append(f"{qid}: имя сцены {key!r} должно быть ascii")
        if not _mood_ok(scene.get("mood")):
            errors.append(f"{qid}/{key}: mood — метка атмосферы или список до двух меток")
        fx_text = scene.get("fx_text")
        if fx_text is not None and (not isinstance(fx_text, str) or not 0 < len(fx_text) <= FX_TEXT_MAX):
            errors.append(f"{qid}/{key}: fx_text — надпись на зеркале, 1–{FX_TEXT_MAX} символов")
        if scene.get("fx_draw") not in (None, "figure", "face"):
            errors.append(f"{qid}/{key}: fx_draw — figure или face")
        if scene.get("fx_lock") not in (None, "open", "error"):
            errors.append(f"{qid}/{key}: fx_lock — open (код подошёл) или error (не подошёл)")
        if is_comedy and any(m in HORROR_MOODS for m in ([scene.get("mood")] if isinstance(scene.get("mood"), str) else scene.get("mood") or [])):
            errors.append(f"{qid}/{key}: в комедии без хоррор-эффектов ({', '.join(sorted(HORROR_MOODS))})")
        if not scene.get("text"):
            errors.append(f"{qid}/{key}: пустой текст")
        if scene.get("end"):
            endings += 1
            if scene["end"] not in ("win", "fail"):
                errors.append(f"{qid}/{key}: end должен быть win|fail")
            if scene.get("choices"):
                errors.append(f"{qid}/{key}: у концовки не должно быть choices")
            continue
        choices = scene.get("choices") or []
        if not choices:
            errors.append(f"{qid}/{key}: сцена без choices и без end — тупик")
        for i, ch in enumerate(choices):
            if not ch.get("label"):
                errors.append(f"{qid}/{key}#{i}: пустой label")
            if ch.get("goto") not in scenes:
                errors.append(f"{qid}/{key}#{i}: goto {ch.get('goto')!r} не существует")
            if ch.get("cost") is not None and (not isinstance(ch["cost"], int) or ch["cost"] <= 0):
                errors.append(f"{qid}/{key}#{i}: cost должен быть положительным числом")
            callback = f"qst:{qid}:{key}:{i}"
            if len(callback.encode()) > 64:
                errors.append(f"{qid}/{key}#{i}: callback длиннее 64 байт: {callback}")
    if not any(s.get("end") == "win" for s in scenes.values()):
        errors.append(f"{qid}: нет ни одной победной концовки")
    return errors


def visible_choices(scene: dict, flags: set[str]) -> list[tuple[int, dict]]:
    """Выборы, доступные при текущих флагах: [(индекс в полном списке, выбор)]."""
    result = []
    for i, ch in enumerate(scene.get("choices") or []):
        if any(f not in flags for f in ch.get("need", [])):
            continue
        if any(f in flags for f in ch.get("missing", [])):
            continue
        result.append((i, ch))
    return result


def win_reachable(q: dict) -> bool:
    """BFS по состояниям (сцена, флаги): достижима ли победа из старта."""
    scenes = q["scenes"]
    seen: set[tuple[str, frozenset]] = set()
    queue: list[tuple[str, frozenset]] = [(q["start"], frozenset())]
    while queue:
        scene_key, flags = queue.pop()
        if (scene_key, flags) in seen:
            continue
        seen.add((scene_key, flags))
        scene = scenes[scene_key]
        if scene.get("end") == "win":
            return True
        if scene.get("end"):
            continue
        for _, ch in visible_choices(scene, set(flags)):
            queue.append((ch["goto"], flags | frozenset(ch.get("set", []))))
    return False


def load_quests(path: Path | str | None = None) -> int:
    """Загружает все сценарии в кэш. Битые файлы пропускаются с логом."""
    global _quests
    quests_dir = Path(path) if path else QUESTS_DIR
    loaded: dict[str, dict] = {}
    if quests_dir.exists():
        for file in sorted(quests_dir.glob("*.json")):
            try:
                quest = json.loads(file.read_text(encoding="utf-8"))
            except Exception:
                logger.exception("[QUESTS] не читается %s", file)
                continue
            errors = validate_quest(quest)
            if errors:
                logger.error("[QUESTS] %s пропущен: %s", file.name, "; ".join(errors[:5]))
                continue
            loaded[quest["id"]] = quest
    _quests = dict(sorted(loaded.items(), key=lambda kv: kv[1].get("order", 999)))
    logger.info("[QUESTS] загружено сценариев: %s", len(_quests))
    return len(_quests)


def all_quests() -> list[dict]:
    if not _quests:
        load_quests()
    return list(_quests.values())


def get_quest(qid: str) -> dict | None:
    if not _quests:
        load_quests()
    return _quests.get(qid)
