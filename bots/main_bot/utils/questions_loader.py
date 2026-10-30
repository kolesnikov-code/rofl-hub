"""
База вопросов викторины: CSV (разделитель ;) → кэш в памяти при старте.

Формат строки: category;question;correct_answer;option_1;option_2;option_3
Тексты экранируются для HTML один раз при загрузке.

Языки (30.10): data/questions.csv — русская база, data/questions_<код>.csv — переводы (тот же формат).
Есть файл для языка игрока — вопросы на его языке, нет — русская база (has_lang подскажет, нужна ли приписка).
"""
from __future__ import annotations

import csv
import hashlib
import html
import logging
import random
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "questions.csv"

_questions: list[dict] = []
_by_id: dict[int, dict] = {}
# переводы: код языка → (вопросы, по id); None — файла нет, работаем на русской базе
_lang_banks: dict[str, tuple[list[dict], dict[int, dict]] | None] = {}

FALLBACK_QUESTIONS = [
    {"id": 1, "category": "Экономика ROFL HUB", "q": "Сколько монет в час приносит Кибер-Бурильщик?",
     "correct": "10", "options": ["5", "10", "20", "50"]},
]


def question_key(text: str) -> str:
    """Стабильный ключ вопроса для «уже видел»: не зависит от порядка строк в CSV."""
    return hashlib.sha1(text.strip().lower().encode("utf-8")).hexdigest()[:16]


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
            "key": question_key(q),
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


def lang_csv_path(lang: str) -> Path:
    return PROJECT_ROOT / "data" / f"questions_{lang}.csv"


def _lang_bank(lang: str | None) -> tuple[list[dict], dict[int, dict]] | None:
    """Переведённая база языка (лениво, один раз). Битый/пустой файл — None: игра идёт на русской базе."""
    if not lang or lang == "ru":
        return None
    if lang not in _lang_banks:
        bank = None
        path = lang_csv_path(lang)
        if path.exists():
            try:
                with open(path, encoding="utf-8-sig", newline="") as f:
                    qs = parse_questions(csv.DictReader(f, delimiter=";"), source=str(path))
                if qs:
                    bank = (qs, {q["id"]: q for q in qs})
                    logger.info("[QUIZ_CSV] %s: загружено вопросов: %s", lang, len(qs))
            except Exception:
                logger.exception("[QUIZ_CSV] ошибка чтения %s", path)
        _lang_banks[lang] = bank
    return _lang_banks[lang]


def has_lang(lang: str | None) -> bool:
    """Есть ли вопросы на языке игрока (иначе — русская база и приписка «пока на русском»)."""
    return lang == "ru" or _lang_bank(lang) is not None


def _pool(lang: str | None) -> list[dict]:
    bank = _lang_bank(lang)
    if bank:
        return bank[0]
    if not _questions:
        load_questions_from_csv()
    return _questions


def get_random_question(lang: str | None = "ru") -> dict | None:
    pool = _pool(lang)
    return random.choice(pool) if pool else None


def pick_unseen(seen: set[str], lang: str | None = "ru") -> tuple[dict | None, bool]:
    """Случайный вопрос, которого игрок ещё не видел. (вопрос, база_пройдена): если видел все — круг заново.
    Ключ — по тексту, поэтому у каждого языка свой круг «невиданных»."""
    pool = _pool(lang)
    if not pool:
        return None, False
    fresh = [q for q in pool if q["key"] not in seen]
    if fresh:
        return random.choice(fresh), False
    return random.choice(pool), True


def get_question_by_id(qid: int, lang: str | None = "ru") -> dict | None:
    bank = _lang_bank(lang)
    if bank:
        return bank[1].get(qid)
    if not _by_id:
        load_questions_from_csv()
    return _by_id.get(qid)
