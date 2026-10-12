import csv
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
    assert "ROFL HUB" in categories
    assert len(categories) >= 10
