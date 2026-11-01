"""
🕹 Чистые правила новых игр приложения (27.10, шаг 2 плана владельца) — без БД и сети, покрыты юнит-тестами.

➗ Математика — пример и 4 варианта ответа; 🏳️ Флаги и столицы — data/flags.json (только бесспорные столицы,
у спорных cap_* = null); 💻 Взлом кода — «быки и коровы» на 4 разных цифрах; 🃏 Мемори — 6 пар карточек-ресурсов.
"""
from __future__ import annotations

import json
import random
from functools import lru_cache
from pathlib import Path

from shared.economy import CODE_DIGITS, MEMORY_PAIRS

FLAGS_PATH = Path(__file__).resolve().parents[1] / "data" / "flags.json"
# 01.11: страны и столицы в data/flags.json на всех 14 языках (name — <код>, столица — cap_<код>)
CAPITAL_LANGS = ("ru", "en", "uz", "es", "fr", "pt", "de", "it", "pl", "id", "zh", "hi", "bn", "ar")
MEMORY_ICONS = ("⛏", "💧", "💎", "⚙️", "🪨", "🪵", "🔥", "⚡", "🔋", "🐄")


# ============================================================================ ➗ Математика
def math_problem(rng: random.Random | None = None) -> tuple[str, int]:
    """Пример (текст) и ответ: сложение/вычитание до 100, таблица умножения (иногда двузначное), деление нацело."""
    rng = rng or random
    op = rng.choice("+-×÷")
    if op == "+":
        a, b = rng.randint(11, 89), rng.randint(11, 89)
        return f"{a} + {b}", a + b
    if op == "-":
        a = rng.randint(30, 99)
        b = rng.randint(7, a - 1)
        return f"{a} − {b}", a - b
    if op == "×":
        a, b = (rng.randint(2, 12), rng.randint(2, 12)) if rng.random() < .7 else (rng.randint(11, 19), rng.randint(2, 9))
        return f"{a} × {b}", a * b
    b, q = rng.randint(2, 12), rng.randint(2, 12)
    return f"{b * q} ÷ {b}", q


def number_options(answer: int, rng: random.Random | None = None, n: int = 4) -> list[int]:
    """Правдоподобные неверные варианты рядом с ответом (±1…10, ±10), все разные и положительные."""
    rng = rng or random
    opts = {answer}
    deltas = [d for d in range(-10, 11) if d] + [-20, 20]
    while len(opts) < n:
        cand = answer + rng.choice(deltas)
        if cand > 0:
            opts.add(cand)
    out = list(opts)
    rng.shuffle(out)
    return out


def math_round_state(rng: random.Random | None = None) -> dict:
    rng = rng or random
    text, answer = math_problem(rng)
    options = number_options(answer, rng)
    return {"q": text, "options": [str(o) for o in options], "correct": options.index(answer)}


# ============================================================================ 🏳️ Флаги и столицы
@lru_cache(maxsize=1)
def flags_data() -> tuple[dict, ...]:
    return tuple(json.loads(FLAGS_PATH.read_text(encoding="utf-8")))


def flag_emoji(iso: str) -> str:
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in iso.upper())


def capital_ok(row: dict, lang: str) -> bool:
    """Вопрос о столице имеет смысл: столица бесспорна и не совпадает с названием страны («Тунис — Тунис»)."""
    cap = row.get(f"cap_{lang}")
    return bool(cap) and cap != row.get(lang)


def flags_round_state(lang: str, rng: random.Random | None = None) -> dict:
    """
    «Чей это флаг?» (варианты — ISO-коды, названия на языке игрока рисует приложение) или, для ru/en,
    «Столица какой страны…?» наоборот: страна → 4 столицы. Верный — индекс в options.
    """
    rng = rng or random
    data = flags_data()
    if lang in CAPITAL_LANGS and rng.random() < .5:
        pool = [r for r in data if capital_ok(r, lang)]
        right = rng.choice(pool)
        others = rng.sample([r for r in pool if r["iso"] != right["iso"]], 3)
        rows = [right] + others
        rng.shuffle(rows)
        return {"mode": "capital", "iso": right["iso"], "country": right[lang], "flag": flag_emoji(right["iso"]),
                "options": [r[f"cap_{lang}"] for r in rows], "correct": rows.index(right)}
    right = rng.choice(data)
    others = rng.sample([r for r in data if r["iso"] != right["iso"]], 3)
    rows = [right] + others
    rng.shuffle(rows)
    return {"mode": "flag", "iso": right["iso"], "flag": flag_emoji(right["iso"]),
            "options": [r["iso"] for r in rows], "names": [r.get(lang) or r["en"] for r in rows], "correct": rows.index(right)}


# ============================================================================ 💻 Взлом кода
def code_secret(rng: random.Random | None = None) -> str:
    rng = rng or random
    return "".join(rng.sample("0123456789", CODE_DIGITS))


def valid_code_guess(guess: str) -> bool:
    return len(guess) == CODE_DIGITS and set(guess) <= set("0123456789") and len(set(guess)) == CODE_DIGITS   # isdigit() пропускает «١٢٣٤»


def bulls_cows(secret: str, guess: str) -> tuple[int, int]:
    """🐂 быки — цифра на своём месте, 🐄 коровы — цифра есть, но в другом месте."""
    bulls = sum(1 for s, g in zip(secret, guess) if s == g)
    cows = len(set(secret) & set(guess)) - bulls
    return bulls, cows


# ============================================================================ 🃏 Мемори
def memory_deck(rng: random.Random | None = None) -> list[str]:
    rng = rng or random
    icons = rng.sample(MEMORY_ICONS, MEMORY_PAIRS)
    deck = icons * 2
    rng.shuffle(deck)
    return deck


def memory_flip(state: dict, idx: int) -> dict:
    """
    Открывает карточку idx (state меняется на месте). Возвращает {icon, pair: idx второй карточки хода | None,
    match: bool | None, done: bool}. Ход = две открытые карточки; совпали — остаются открытыми навсегда.
    Ошибки: ValueError (карточка вне колоды, уже найдена или уже открыта в этом ходе).
    """
    deck, matched, pending = state["deck"], state["matched"], state.get("pending")
    if not 0 <= idx < len(deck) or idx in matched or idx == pending:
        raise ValueError("bad card")
    if pending is None:
        state["pending"] = idx
        return {"icon": deck[idx], "pair": None, "match": None, "done": False}
    state["pending"] = None
    state["moves"] += 1
    match = deck[idx] == deck[pending]
    if match:
        matched.extend([pending, idx])
    return {"icon": deck[idx], "pair": pending, "match": match, "done": len(matched) == len(deck)}
