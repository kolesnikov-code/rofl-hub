"""
Фиче-тумблеры ROFL HUB: пульт владельца в админ-боте.

Хранятся в таблице feature_flags, включаются/выключаются без деплоя.
Кэш в памяти (TTL 20 с), чтобы не дёргать БД на каждый апдейт.
ОТКАЗОУСТОЙЧИВОСТЬ: сбой БД никогда не выключает игру — возвращается дефолт.

Ключи:
- maintenance — режим техработ (True = главный бот отвечает заглушкой всем);
- games / duels / quests / shop / transfers — разделы экосистемы;
- quest:<id> — видимость конкретного квеста в списке /quests.
Начатые игроками раунды/квесты всегда доигрываются — тумблер закрывает только вход.
"""
from __future__ import annotations

import logging
import time

from shared.database import db

logger = logging.getLogger(__name__)

# Дефолты: всё включено, техработы выключены. Квесты (quest:*) по умолчанию видимы.
FLAG_DEFAULTS: dict[str, bool] = {
    "maintenance": False,
    "games": True,
    "duels": True,
    "quests": True,
    "shop": True,
    "transfers": True,
}
# Человеческие подписи для пульта в админ-боте
FLAG_TITLES: dict[str, str] = {
    "maintenance": "🛠 Режим техработ (весь бот)",
    "games": "🕹 Игровая зона (все соло-игры)",
    "duels": "⚔️ Дуэли",
    "quests": "🗺 Квесты (раздел целиком)",
    "shop": "🏪 Магазин и покупки Stars",
    "transfers": "🔄 Переводы монет",
}

_CACHE_TTL = 20.0
_cache: dict[str, tuple[bool, float]] = {}


def _default_for(key: str) -> bool:
    if key.startswith("quest:"):
        return True
    return FLAG_DEFAULTS.get(key, True)


async def get_flag(key: str) -> bool:
    """Текущее значение тумблера. При любом сбое — безопасный дефолт."""
    now = time.monotonic()
    hit = _cache.get(key)
    if hit and now - hit[1] < _CACHE_TTL:
        return hit[0]
    try:
        row = await db.pool.fetchrow("SELECT enabled FROM feature_flags WHERE key = $1", key)
        value = row["enabled"] if row else _default_for(key)
    except Exception:
        logger.warning("[FLAGS] не удалось прочитать %s — использую дефолт", key)
        return _default_for(key)
    _cache[key] = (value, now)
    return value


async def set_flag(key: str, enabled: bool) -> None:
    await db.pool.execute(
        """INSERT INTO feature_flags (key, enabled, updated_at) VALUES ($1, $2, NOW())
           ON CONFLICT (key) DO UPDATE SET enabled = $2, updated_at = NOW()""",
        key[:64], enabled)
    _cache[key] = (enabled, time.monotonic())


async def toggle_flag(key: str) -> bool:
    """Переключает тумблер, возвращает НОВОЕ значение."""
    new_value = not await get_flag(key)
    await set_flag(key, new_value)
    return new_value


async def all_feature_flags() -> dict[str, bool]:
    """Все основные тумблеры (без quest:*) для пульта."""
    return {key: await get_flag(key) for key in FLAG_DEFAULTS}


def invalidate_cache() -> None:
    _cache.clear()
