"""
⚠️ Жалобы на вопросы викторины (решение владельца 27.10: «в приложении сделай возможность пожаловаться на вопрос»).

Игрок жалуется ПОСЛЕ ответа (вопрос и верный ответ берутся из закрытого раунда game_rounds — подделать текст нельзя).
Одна жалоба игрока на вопрос (повторная — меняет причину), не больше QUIZ_REPORT_DAILY_LIMIT в сутки UTC.
Владелец видит в админ-боте /quiz_reports вопросы с открытыми жалобами (больше жалоб — выше) и закрывает их
кнопкой, когда поправил базу (data/questions.csv).
"""
from __future__ import annotations

import json

from shared.economy import QUIZ_REPORT_DAILY_LIMIT

REASONS = ("answer", "question", "dup", "other")   # неверный ответ · ошибка в вопросе · повтор · другое
REASON_RU = {"answer": "неверный ответ", "question": "ошибка в вопросе", "dup": "повтор", "other": "другое"}


class ReportError(Exception):
    """code: bad | stale | limit."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


async def add_report(conn, user_id: int, round_id: int, reason: str) -> None:
    if reason not in REASONS:
        raise ReportError("bad")
    row = await conn.fetchrow("SELECT state FROM game_rounds WHERE id = $1 AND user_id = $2 AND game = 'quiz' AND done",
                              round_id, user_id)
    if row is None:
        raise ReportError("stale")
    state = json.loads(row["state"]) if isinstance(row["state"], str) else row["state"]
    if not state.get("key") or not state.get("q"):
        raise ReportError("stale")
    today = await conn.fetchval("SELECT COUNT(*) FROM quiz_reports WHERE user_id = $1 "
                                "AND created_at >= date_trunc('day', now() AT TIME ZONE 'UTC') AT TIME ZONE 'UTC'", user_id)
    if today >= QUIZ_REPORT_DAILY_LIMIT:
        raise ReportError("limit")
    await conn.execute(
        """INSERT INTO quiz_reports (user_id, qkey, question, answer, reason) VALUES ($1, $2, $3, $4, $5)
           ON CONFLICT (user_id, qkey) DO UPDATE SET reason = EXCLUDED.reason, resolved_at = NULL""",
        user_id, state["key"], state["q"], state["options"][state["correct"]], reason)


async def open_reports(conn, limit: int = 10) -> list[dict]:
    """Вопросы с открытыми жалобами: больше жалоб — выше; причины — счётчиком."""
    rows = await conn.fetch(
        """SELECT qkey, MAX(question) AS question, MAX(answer) AS answer, COUNT(*) AS n,
                  jsonb_object_agg(reason, cnt) AS reasons, MAX(last_at) AS last_at
           FROM (SELECT qkey, question, answer, reason, COUNT(*) OVER (PARTITION BY qkey, reason) AS cnt,
                        created_at AS last_at
                 FROM quiz_reports WHERE resolved_at IS NULL) r
           GROUP BY qkey ORDER BY n DESC, last_at DESC LIMIT $1""", limit)
    out = []
    for r in rows:
        reasons = json.loads(r["reasons"]) if isinstance(r["reasons"], str) else dict(r["reasons"])
        out.append({"qkey": r["qkey"], "question": r["question"], "answer": r["answer"], "n": r["n"],
                    "reasons": reasons})
    return out


async def open_count(conn) -> int:
    return await conn.fetchval("SELECT COUNT(DISTINCT qkey) FROM quiz_reports WHERE resolved_at IS NULL")


async def resolve(conn, qkey: str) -> int:
    """Владелец разобрал вопрос — все его жалобы закрыты. Возвращает число закрытых."""
    result = await conn.execute("UPDATE quiz_reports SET resolved_at = now() WHERE qkey = $1 AND resolved_at IS NULL", qkey)
    return int(result.split()[-1])
