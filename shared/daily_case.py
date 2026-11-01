"""
🕵️ ДЕЛО ДНЯ (решение владельца 27.10 по итогам оценки 9 агентов: «топ-идея, реализуй механику»).

Одно короткое дело на всех игроков в сутки UTC — как Wordle, только детектив. Четыре подозреваемых, четыре улики.
Первая улика открыта сразу; каждая следующая — «ход». Обвинение — одно. Раскрыл(а) с меньшим числом улик — больше
награда (economy.DAILY_CASE_REWARD) и красивее строка для «поделиться» (🔍🔍⬛⬛ ✅) — без спойлеров.
Серия раскрытых дней подряд (🔥), каждый DAILY_CASE_STREAK_BONUS_EVERY-й день — бонус.

Содержание — data/daily_cases.json (ru + en; остальные языки видят en). Дело выбирается по номеру дня от
CASE_EPOCH по кругу, поэтому порядок в файле = расписание; новое дело дописывается в конец.
Правило автора: по всем четырём уликам виновный определяется ОДНОЗНАЧНО, а внимательный игрок может вычислить
его раньше (тест test_daily_cases_are_well_formed проверяет форму; логику — вычитка агентами).
Все функции записи вызываются ВНУТРИ транзакции вызывающего.
"""
from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path

from shared.economy import DAILY_CASE_REWARD, DAILY_CASE_STREAK_BONUS, DAILY_CASE_STREAK_BONUS_EVERY, utcnow
from shared.ledger import change_balance

logger = logging.getLogger(__name__)

CASES_PATH = Path(__file__).resolve().parents[1] / "data" / "daily_cases.json"
CASE_EPOCH = date(2026, 10, 28)      # дело №1
CLUES = 4
SUSPECTS = 4
# ru/en — прямо в деле (case["ru"], case["en"]); 12 языков паков — в case["tr"][код] (01.11). Отдельный раздел нужен,
# потому что код индонезийского «id» совпадает с полем дела «id». Нет перевода — английская версия.
BASE_LANGS = ("ru", "en")
CONTENT_LANGS = BASE_LANGS + ("uz", "es", "fr", "pt", "de", "it", "pl", "id", "zh", "hi", "bn", "ar")

_cases: list[dict] | None = None


class CaseError(Exception):
    """code: done | bad"""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def load_cases(path: Path | None = None) -> list[dict]:
    global _cases
    try:
        _cases = json.loads(Path(path or CASES_PATH).read_text(encoding="utf-8"))
    except Exception:
        logger.exception("[CASE] не читается %s", path or CASES_PATH)
        _cases = []
    return _cases


def all_cases() -> list[dict]:
    return _cases if _cases is not None else load_cases()


def case_number(day: date) -> int:
    return (day - CASE_EPOCH).days + 1


def case_for_day(day: date) -> dict | None:
    cases = all_cases()
    if not cases:
        return None
    return cases[(case_number(day) - 1) % len(cases)]


def case_body(case: dict, lang: str) -> dict:
    """Текст дела на языке игрока (нет перевода — английский)."""
    if lang in BASE_LANGS:
        return case[lang]
    return (case.get("tr") or {}).get(lang) or case["en"]


def validate_case(c: dict) -> list[str]:
    """Ошибки формы дела (пусто — дело валидно)."""
    errs = []
    cid = c.get("id", "?")
    if not isinstance(c.get("culprit"), int) or not 0 <= c["culprit"] < SUSPECTS:
        errs.append(f"{cid}: culprit — индекс 0..{SUSPECTS - 1}")
    for lang in CONTENT_LANGS:
        body = (c.get(lang) if lang in BASE_LANGS else (c.get("tr") or {}).get(lang)) or {}
        for field in ("title", "story", "solution"):
            if not isinstance(body.get(field), str) or not body[field].strip():
                errs.append(f"{cid}/{lang}: нет {field}")
        sus = body.get("suspects") or []
        if len(sus) != SUSPECTS or any(not s.get("name") or not s.get("emoji") or not s.get("alibi") for s in sus):
            errs.append(f"{cid}/{lang}: нужно {SUSPECTS} подозреваемых с name/emoji/alibi")
        clues = body.get("clues") or []
        if len(clues) != CLUES or any(not isinstance(x, str) or not x.strip() for x in clues):
            errs.append(f"{cid}/{lang}: нужно {CLUES} улики")
    return errs


async def _run(conn, user_id: int, day: date, lock: bool = False):
    return await conn.fetchrow("SELECT * FROM daily_case_runs WHERE user_id = $1 AND day = $2"
                               + (" FOR UPDATE" if lock else ""), user_id, day)


async def open_case(conn, user_id: int, now: datetime | None = None):
    """Начать (или продолжить) сегодняшнее дело. Возвращает строку прогона."""
    day = (now or utcnow()).date()
    case = case_for_day(day)
    if case is None:
        raise CaseError("bad")
    await conn.execute("INSERT INTO daily_case_runs (user_id, day, case_id) VALUES ($1, $2, $3) "
                       "ON CONFLICT DO NOTHING", user_id, day, case["id"])
    return await _run(conn, user_id, day)


async def reveal_clue(conn, user_id: int, now: datetime | None = None):
    day = (now or utcnow()).date()
    run = await _run(conn, user_id, day, lock=True)
    if run is None:
        run = await open_case(conn, user_id, now)
    if run["finished_at"] is not None:
        raise CaseError("done")
    if run["clues"] < CLUES:
        await conn.execute("UPDATE daily_case_runs SET clues = clues + 1 WHERE user_id = $1 AND day = $2", user_id, day)
    return await _run(conn, user_id, day)


async def streak(conn, user_id: int, today: date) -> int:
    """Раскрытых дел подряд, считая сегодня (если сегодня раскрыто) или вчера."""
    days = {r["day"] for r in await conn.fetch(
        "SELECT day FROM daily_case_runs WHERE user_id = $1 AND solved AND day > $2", user_id, today - timedelta(days=400))}
    cur = today if today in days else today - timedelta(days=1)
    n = 0
    while cur in days:
        n += 1
        cur -= timedelta(days=1)
    return n


async def accuse(conn, user_id: int, suspect: int, now: datetime | None = None) -> dict:
    """Единственное обвинение дня. Награда — только за раскрытие (ledger 'daily_case')."""
    now = now or utcnow()
    day = now.date()
    if not 0 <= suspect < SUSPECTS:
        raise CaseError("bad")
    run = await _run(conn, user_id, day, lock=True)
    if run is None:
        await open_case(conn, user_id, now)
        run = await _run(conn, user_id, day, lock=True)
    if run["finished_at"] is not None:
        raise CaseError("done")
    case = next((c for c in all_cases() if c["id"] == run["case_id"]), None) or case_for_day(day)
    solved = suspect == case["culprit"]
    reward = DAILY_CASE_REWARD.get(run["clues"], 0) if solved else 0
    await conn.execute("UPDATE daily_case_runs SET accused = $3, solved = $4, reward = $5, finished_at = $6 "
                       "WHERE user_id = $1 AND day = $2", user_id, day, suspect, solved, reward, now)
    bonus = 0
    st = await streak(conn, user_id, day)
    if solved and st and st % DAILY_CASE_STREAK_BONUS_EVERY == 0:
        bonus = DAILY_CASE_STREAK_BONUS
    if reward + bonus:
        await change_balance(conn, user_id, reward + bonus, "daily_case", f"{run['case_id']}:{day.isoformat()}")
    return {"solved": solved, "reward": reward, "bonus": bonus, "streak": st}


async def day_stats(conn, day: date) -> dict:
    row = await conn.fetchrow(
        "SELECT COUNT(*) FILTER (WHERE finished_at IS NOT NULL) AS played, COUNT(*) FILTER (WHERE solved) AS solved, "
        "AVG(clues) FILTER (WHERE solved) AS clues FROM daily_case_runs WHERE day = $1", day)
    return {"played": int(row["played"] or 0), "solved": int(row["solved"] or 0),
            "avg_clues": round(float(row["clues"]), 1) if row["clues"] is not None else None}


async def case_payload(conn, user_id: int, lang: str, now: datetime | None = None) -> dict:
    """Всё для экрана: текст дела на языке игрока, открытые улики, итог (виновный и разбор — только после)."""
    now = now or utcnow()
    day = now.date()
    case = case_for_day(day)
    if case is None:
        return {"ok": False}
    body = case_body(case, lang)
    run = await _run(conn, user_id, day)
    opened = run["clues"] if run else 1
    finished = bool(run and run["finished_at"])
    out = {
        "ok": True, "number": case_number(day), "id": case["id"], "mood": case.get("mood") or "noir",
        "title": body["title"], "story": body["story"],
        "suspects": [{"name": s["name"], "emoji": s["emoji"], "alibi": s["alibi"]} for s in body["suspects"]],
        "clues": body["clues"][:opened], "opened": opened, "total": CLUES, "started": bool(run),
        "finished": finished, "rewards": DAILY_CASE_REWARD, "streak": await streak(conn, user_id, day),
        "streak_every": DAILY_CASE_STREAK_BONUS_EVERY, "streak_bonus": DAILY_CASE_STREAK_BONUS,
        "next_at": (datetime.combine(day + timedelta(days=1), datetime.min.time())).isoformat() + "Z",
    }
    if finished:
        out.update(solved=bool(run["solved"]), accused=run["accused"], culprit=case["culprit"],
                   solution=body["solution"], reward=run["reward"], clues=body["clues"],
                   stats=await day_stats(conn, day))
    return out
