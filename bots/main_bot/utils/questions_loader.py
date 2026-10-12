import csv
import os
import logging
import html
import random

logger = logging.getLogger(__name__)

# Хранилище вопросов в оперативной памяти сервера
_cached_questions = []


def load_questions_from_csv():
    """
    Считывает вопросы из CSV-таблицы в буфер памяти при старте бота.
    Жестко привязан к абсолютному корню проекта ROFL-HUB.
    """
    global _cached_questions
    _cached_questions = []

    # 🔥 ЖЕСТКИЙ ПУТЬ: Находим корень проекта по расположению этого файла
    # bots/main_bot/utils/questions_loader.py -> parents[3] уводит в ROFL-HUB/
    from pathlib import Path
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[3]
    csv_path = os.path.join(project_root, "data", "questions.csv")

    if not os.path.exists(csv_path):
        logger.warning(f"⚠️ Файл базы вопросов {csv_path} не найден! Викторина запущена на аварийном паке.")
        _cached_questions = [
            {
                "id": 1, "category": "Экономика", "q": "Какая скорость добычи дает Кибер-Бурильщик в магазине?",
                "correct": "5 рофлов в час",
                "options": ["2 рофла в час", "5 рофлов в час", "10 рофлов в час", "100 рофлов в час"]
            }
        ]
        return

    try:
        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for idx, row in enumerate(reader, start=1):
                if not row.get("question") or not row.get("correct_answer"):
                    continue

                q_text = html.escape(row["question"].strip())
                ans_correct = html.escape(row["correct_answer"].strip())

                # Собираем все 4 варианта (правильный всегда первый в файле, перемешаем при выдаче)
                options = [
                    ans_correct,
                    html.escape(row["option_1"].strip()),
                    html.escape(row["option_2"].strip()),
                    html.escape(row["option_3"].strip())
                ]

                _cached_questions.append({
                    "id": idx,
                    "category": row.get("category", "Общая").strip(),
                    "q": q_text,
                    "correct": ans_correct,
                    "options": options
                })
        logger.info(f"📊 УСПЕШНО КЭШИРОВАНО ИЗ CSV: {len(_cached_questions)} ВОПРОСОВ ДЛЯ ТУРНИРОВ!")
    except Exception as e:
        logger.error(f"🚨 Ошибка парсинга CSV-файла викторины: {e}")


def get_random_question() -> dict:
    """Выдергивает случайный вопрос из кэша памяти"""
    global _cached_questions
    if not _cached_questions:
        load_questions_from_csv()
    return random.choice(_cached_questions) if _cached_questions else None
