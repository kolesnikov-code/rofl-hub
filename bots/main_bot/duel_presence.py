"""
⚔️ Кто сейчас смотрит дуэль в приложении (27.10). Приложение опрашивает /api/duel раз в ~1,5 с — по этим отметкам
бот решает, писать ли игроку в чат: открыт экран дуэли — ЛС не нужна (всё видно в приложении), закрыт или игрок
вообще из чата — пишем как раньше. Память процесса: веб-сервер приложения живёт в процессе главного бота.
"""
from __future__ import annotations

import time

APP_PRESENCE_SECONDS = 6      # опрос раз в 1,5 с — 6 с без опроса = экран закрыт
_seen: dict[int, float] = {}


def mark_in_app(user_id: int) -> None:
    _seen[user_id] = time.monotonic()
    if len(_seen) > 5000:     # не копим: старые отметки всё равно ничего не значат
        cutoff = time.monotonic() - APP_PRESENCE_SECONDS
        for uid in [u for u, ts in _seen.items() if ts < cutoff]:
            _seen.pop(uid, None)


def in_app(user_id: int) -> bool:
    ts = _seen.get(user_id)
    return ts is not None and time.monotonic() - ts <= APP_PRESENCE_SECONDS
