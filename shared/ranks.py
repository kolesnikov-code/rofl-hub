"""
Звания игроков по стажу в экосистеме (решение владельца 22.10.2026, иерархия v2 — 02.11.2026).

Чистая логика порогов — в shared/economy.py (RANKS, rank_key_for), здесь — подпись
на языке игрока: Новичок → Рядовой → Боец → Капитан → Генерал → Легенда → Властелин, все 7 переведены на 14 языков.
"""
from __future__ import annotations

from datetime import datetime

from shared.economy import rank_key_for
from shared.locales import t


def rank_label(lang: str, created_at: datetime | None, now: datetime) -> str:
    """Название звания на языке игрока или пустая строка (дата регистрации неизвестна)."""
    key = rank_key_for(created_at, now)
    return t(lang, f"rank.{key}") if key else ""


def name_with_rank(name_html: str, lang: str, created_at: datetime | None, now: datetime) -> str:
    """«@username · 🎖 Боец» — звание справа от имени, как просил владелец."""
    label = rank_label(lang, created_at, now)
    return f"{name_html} · 🎖 {label}" if label else name_html
