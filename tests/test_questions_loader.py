import csv
import html
import io
from pathlib import Path

from bots.main_bot.utils import questions_loader as ql

HEADER = "category;question;correct_answer;option_1;option_2;option_3\n"


def _parse(text: str):
    return ql.parse_questions(csv.DictReader(io.StringIO(text), delimiter=";"), source="test")


def test_parses_valid_rows_and_escapes_html():
    qs = _parse(HEADER + "Гео;Столица <Франции>?;Париж;Лондон;Рим;Берлин\n")
    assert len(qs) == 1
    q = qs[0]
    assert q["q"] == "Столица &lt;Франции&gt;?"
    assert q["correct"] == "Париж"
    assert set(q["options"]) == {"Париж", "Лондон", "Рим", "Берлин"}
    assert q["id"] == 1


def test_skips_broken_rows_but_keeps_ids_stable():
    text = HEADER + "A;q1;c;a;b;d\nB;;c;a;b;d\nC;q3;c;a;;d\nD;q4;c;c;b;d\nE;q5;c;a;b;d\n"
    qs = _parse(text)
    assert [q["id"] for q in qs] == [1, 5]  # id = номер строки в файле, а не порядковый


def test_shipped_csv_loads(tmp_path: Path):
    n = ql.load_questions_from_csv(ql.DEFAULT_CSV_PATH)
    assert n >= 1
    q = ql.get_random_question()
    assert q is not None and ql.get_question_by_id(q["id"]) is q


def test_missing_file_falls_back(tmp_path: Path):
    n = ql.load_questions_from_csv(tmp_path / "nope.csv")
    assert n == len(ql.FALLBACK_QUESTIONS)
    ql.load_questions_from_csv()  # вернуть кэш в нормальное состояние


def test_callback_data_for_any_answer_fits_64_bytes():
    ql.load_questions_from_csv()
    for q in ql._questions:
        for i in range(4):
            assert len(f"quiz_check:{q['id']}:{i}".encode()) <= 64


# ---------------------------------------------------------------- Блок 3: боевая база
def test_shipped_csv_has_200_plus_questions():
    n = ql.load_questions_from_csv(ql.DEFAULT_CSV_PATH)
    assert n >= 200, f"В базе {n} вопросов, по ТЗ нужно 200+"


def test_shipped_csv_has_no_duplicate_questions():
    ql.load_questions_from_csv(ql.DEFAULT_CSV_PATH)
    texts = [q["q"] for q in ql._questions]
    dupes = {t for t in texts if texts.count(t) > 1}
    assert not dupes, f"Повторяющиеся вопросы: {dupes}"


def test_shipped_csv_every_question_valid_for_buttons():
    """4 уникальных варианта, правильный среди них, тексты влезают в кнопку."""
    ql.load_questions_from_csv(ql.DEFAULT_CSV_PATH)
    for q in ql._questions:
        assert len(set(q["options"])) == 4, q["q"]
        assert q["correct"] in q["options"], q["q"]
        for opt in q["options"]:
            assert len(opt) <= 40, f"Слишком длинный вариант у «{q['q']}»: {opt}"


def test_shipped_csv_covers_rofl_hub_category():
    ql.load_questions_from_csv(ql.DEFAULT_CSV_PATH)
    categories = {q["category"] for q in ql._questions}
    assert "Bot Barons" in categories
    assert len(categories) >= 10


def test_pick_unseen_gives_every_question_once_per_lap():
    """Викторина без повторов: пока игрок не прошёл всю базу, вопрос не повторяется; потом — новый круг."""
    from bots.main_bot.utils import questions_loader as ql
    total = ql.load_questions_from_csv()
    seen: set[str] = set()
    for _ in range(total):
        q, lap_done = ql.pick_unseen(seen)
        assert not lap_done and q["key"] not in seen
        seen.add(q["key"])
    q, lap_done = ql.pick_unseen(seen)
    assert lap_done and q is not None
    assert len({q["key"] for q in ql._questions}) == total     # ключи уникальны — дублей текста нет


def test_question_key_ignores_case_and_spaces():
    from bots.main_bot.utils.questions_loader import question_key
    assert question_key("  Какой Город? ") == question_key("какой город?") and len(question_key("x")) == 16


# ---------------------------------------------------------------- 30.10: вопросы на языке игрока
def test_language_without_translation_falls_back_to_english_base():
    """Нет своей базы — английская (понятнее не-русскому игроку); русскому — всегда русская."""
    ql.load_questions_from_csv()
    ql._lang_banks.pop("xx", None)
    assert ql.has_lang("ru") and not ql.has_lang("xx")
    q, _ = ql.pick_unseen(set(), "xx")
    assert q is not None and ql.get_question_by_id(q["id"], "xx") is ql.get_question_by_id(q["id"], "en")
    assert q in ql._lang_bank("en")[0]
    assert ql.get_question_by_id(q["id"], "ru") is ql.get_question_by_id(q["id"])


def test_untranslated_languages_say_questions_are_in_english():
    from shared.locales import t
    for lang in ("es", "fr", "de", "it", "pt", "pl", "id", "zh", "hi", "bn", "ar"):
        assert "🌐" in t(lang, "quiz.round", category="X", question="Y"), lang


def test_translated_banks_are_valid_and_match_the_russian_size():
    """Каждый questions_<язык>.csv: формат кнопок, без дублей, не меньше 90% русской базы, без запретного слова."""
    ru = ql.load_questions_from_csv(ql.DEFAULT_CSV_PATH)
    for path in sorted(Path(ql.DEFAULT_CSV_PATH).parent.glob("questions_*.csv")):
        lang = path.stem.split("_", 1)[1]
        ql._lang_banks.pop(lang, None)
        assert ql.has_lang(lang), path
        qs = ql._lang_bank(lang)[0]
        assert len(qs) >= ru * 0.9, (lang, len(qs), ru)
        texts = [q["q"] for q in qs]
        assert len(set(texts)) == len(texts), f"{lang}: повторы"
        for q in qs:
            assert len(set(q["options"])) == 4 and q["correct"] in q["options"], q["q"]
            assert all(len(html.unescape(o)) <= 40 for o in q["options"]), q["q"]
            assert "&#x27;" not in q["q"] + "".join(q["options"]), q["q"]   # апостроф на кнопках — как есть
            assert "рофл" not in q["q"].lower() and "rofl" not in q["q"].lower().replace("rofl hub", ""), q["q"]
        for i in range(4):
            assert all(len(f"quiz_check:{q['id']}:{i}".encode()) <= 64 for q in qs)


def test_quiz_round_drops_the_russian_only_note_when_translated(monkeypatch):
    from bots.main_bot.handlers import games
    q = {"id": 1, "category": "Gео", "q": "Savol?", "correct": "A", "options": ["A", "B", "C", "D"]}
    monkeypatch.setattr(games, "has_lang", lambda lang: True)
    text, _, _ = games._quiz_round(q, "uz")
    assert "🌐" not in text and "Savol?" in text
    monkeypatch.setattr(games, "has_lang", lambda lang: lang == "ru")
    assert "🌐" in games._quiz_round(q, "uz")[0]
