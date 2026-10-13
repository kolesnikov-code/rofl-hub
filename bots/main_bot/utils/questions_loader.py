"""
База вопросов викторины: CSV (разделитель ;) → кэш в памяти при старте.

Формат строки: category;question;correct_answer;option_1;option_2;option_3
Тексты экранируются для HTML один раз при загрузке.
"""
from __future__ import annotations

import csv
import html
import logging
import random
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "questions.csv"

_questions: list[dict] = []
_by_id: dict[int, dict] = {}

FALLBACK_QUESTIONS = [
    {"id": 1, "category": "Экономика ROFL HUB", "q": "Сколько монет в час приносит Кибер-Бурильщик?",
     "correct": "10", "options": ["5", "10", "20", "50"]},
]


def parse_questions(rows, *, source: str = "csv") -> list[dict]:
    """Чистый парсер: список словарей из DictReader → список вопросов. Битые строки пропускаются."""
    result: list[dict] = []
    for idx, row in enumerate(rows, start=1):
        q = (row.get("question") or "").strip()
        correct = (row.get("correct_answer") or "").strip()
        wrong = [(row.get(f"option_{i}") or "").strip() for i in (1, 2, 3)]
        if not q or not correct or any(not w for w in wrong):
            logger.warning("[QUIZ_CSV] строка %s пропущена: пустое поле (%s)", idx, source)
            continue
        options = [html.escape(correct)] + [html.escape(w) for w in wrong]
        if len(set(options)) != 4:
            logger.warning("[QUIZ_CSV] строка %s пропущена: повторяющиеся варианты", idx)
            continue
        result.append({
            "id": idx,
            "category": html.escape((row.get("category") or "Общая").strip()),
            "q": html.escape(q),
            "correct": options[0],
            "options": options,
        })
    return result


def load_questions_from_csv(path: Path | str | None = None) -> int:
    """Загружает вопросы в кэш. Возвращает количество. При ошибке — аварийный пак."""
    global _questions, _by_id
    csv_path = Path(path) if path else DEFAULT_CSV_PATH
    loaded: list[dict] = []
    if csv_path.exists():
        try:
            with open(csv_path, encoding="utf-8-sig", newline="") as f:
                loaded = parse_questions(csv.DictReader(f, delimiter=";"), source=str(csv_path))
        except Exception:
            logger.exception("[QUIZ_CSV] ошибка чтения %s", csv_path)
    else:
        logger.warning("[QUIZ_CSV] файл %s не найден", csv_path)

    if not loaded:
        logger.warning("[QUIZ_CSV] викторина работает на аварийном паке из %s вопросов", len(FALLBACK_QUESTIONS))
        loaded = [dict(q) for q in FALLBACK_QUESTIONS]

    _questions = loaded
    _by_id = {q["id"]: q for q in loaded}
    logger.info("[QUIZ_CSV] загружено вопросов: %s", len(loaded))
    return len(loaded)


def get_random_question() -> dict | None:
    if not _questions:
        load_questions_from_csv()
    return random.choice(_questions) if _questions else None


def get_question_by_id(qid: int) -> dict | None:
    if not _by_id:
        load_questions_from_csv()
    return _by_id.get(qid)
