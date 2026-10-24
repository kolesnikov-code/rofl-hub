"""
Команды и кланы — общая механика для чат-бота и игрового приложения (одни и те же правила):
создание (одна транзакция, FOR UPDATE, списание через ledger), вступление, выход с передачей
короны, рулетка свободных команд, поиск по названию, состав команды.
Ошибки — TeamError с ключом локали: чат и приложение показывают их на языке игрока.
"""
from __future__ import annotations

import html
import logging
import re

from shared.database import db
from shared.economy import (TEAM_CREATE_COST, TEAM_MOTTO_MAX_LEN, TEAM_NAME_MAX_LEN, TEAM_ROULETTE_SIZE,
                            TEAM_SEARCH_LIMIT, TEAM_SYMBOL_MAX_LEN)
from shared.ledger import InsufficientFunds, change_balance
from shared.locales import t

logger = logging.getLogger(__name__)

# 🛡️ Фильтры текста команд (анти-спам, анти-фишинг, анти-мат) — для названия, девиза, эмблемы и поиска
URL_REGEX = re.compile(r'(https?://[^\s]+|t\.me/[^\s]+|@[^\s]+)')
PHONE_REGEX = re.compile(r'(\+?\d[\d\-\(\) ]{7,}\d)')   # 9+ цифр подряд (с пробелами/скобками/дефисами)
PROHIBITED_WORDS = ["хуй", "пизда", "ебать", "член", "сука", "бля", "трахать", "мудак"]


class TeamError(Exception):
    def __init__(self, key: str, **kwargs):
        super().__init__(key)
        self.key, self.kwargs = key, kwargs

    def localized(self, lang: str) -> str:
        return t(lang, self.key, **self.kwargs)


def validate_team_text(text: str | None, max_len: int) -> str:
    """Проверяет ввод игрока и возвращает его HTML-экранированным (так он хранится в teams)."""
    cleaned = (text or "").strip()
    if not cleaned or len(cleaned) > max_len:
        raise TeamError("team.err_len", max=max_len)
    if URL_REGEX.search(cleaned) or PHONE_REGEX.search(cleaned):
        raise TeamError("team.err_link")
    if any(word in cleaned.lower() for word in PROHIBITED_WORDS):
        raise TeamError("team.err_badword")
    return html.escape(cleaned)


def public_team(row) -> dict:
    """Карточка команды для списков: только публичное (без капитана и состава)."""
    return {"id": row["team_id"], "name": html.unescape(row["team_name"] or ""),
            "motto": html.unescape(row["city"] or ""), "symbol": html.unescape(row["school_num"] or ""),
            "members": row["members_count"], "max": row["max_members"],
            "is_clan": row["max_members"] >= 1000}


async def random_teams(conn, limit: int = TEAM_ROULETTE_SIZE) -> list[dict]:
    """Рулетка: случайные команды со свободными местами — при каждом запросе новый набор."""
    rows = await conn.fetch(
        "SELECT * FROM teams WHERE members_count < max_members ORDER BY RANDOM() LIMIT $1", limit)
    return [public_team(r) for r in rows]


async def search_teams(conn, query: str, limit: int = TEAM_SEARCH_LIMIT) -> list[dict]:
    """Поиск по фрагменту названия (без учёта регистра); названия хранятся экранированными."""
    needle = validate_team_text(query, TEAM_NAME_MAX_LEN)
    needle = needle.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    rows = await conn.fetch(
        "SELECT * FROM teams WHERE team_name ILIKE $1 ORDER BY members_count DESC, team_id LIMIT $2",
        f"%{needle}%", limit)
    return [public_team(r) for r in rows]


async def join_team(conn, user_id: int, team_id: int) -> dict:
    """Вступление (внутри транзакции вызывающего). Возвращает публичную карточку команды."""
    team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1 FOR UPDATE", team_id)
    user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not team:
        raise TeamError("team.err_gone")
    if not user:
        raise TeamError("common.no_profile")
    if user["team_id"] is not None:
        raise TeamError("team.err_already")
    if team["members_count"] >= team["max_members"]:
        raise TeamError("team.err_full")
    await conn.execute("UPDATE teams SET members_count = members_count + 1 WHERE team_id = $1", team_id)
    await conn.execute("UPDATE users SET team_id = $1, team_joined_at = NOW() WHERE user_id = $2", team_id, user_id)
    return public_team(team)


async def team_members(conn, team_id: int, captain_id: int, limit: int = 1000, offset: int = 0) -> list[dict]:
    """Состав: капитан первым, дальше ветераны по старшинству вступления."""
    rows = await conn.fetch(
        """
        SELECT u.user_id, u.username, u.display_name, u.created_at,
               COALESCE(g.quiz_level, 0) AS quiz_level
        FROM users u
        LEFT JOIN game_stats g ON g.user_id = u.user_id
        WHERE u.team_id = $1
        ORDER BY (u.user_id = $2) DESC, u.team_joined_at ASC NULLS LAST, u.user_id ASC
        LIMIT $3 OFFSET $4
        """,
        team_id, captain_id, limit, offset)
    return [dict(r) for r in rows]


async def leave_team(conn, user_id: int, team_id: int | None = None) -> dict | None:
    """
    Выход игрока из команды (внутри транзакции вызывающего). Капитан передаёт корону тому,
    кто вступил раньше всех (кроме заблокированных и уходящих из экосистемы); один в команде —
    команда расформировывается. team_id — ожидаемая команда (защита от устаревшей кнопки).
    Возвращает {"team_id", "team_name", "outcome": "left"|"passed"|"disbanded", "new_captain"}
    или None, если игрок не в этой команде.
    """
    current = await conn.fetchval("SELECT team_id FROM users WHERE user_id = $1", user_id)
    if current is None or (team_id is not None and current != team_id):
        return None
    # Порядок блокировок как во всём коде: сначала команда, потом игрок
    team = await conn.fetchrow("SELECT * FROM teams WHERE team_id = $1 FOR UPDATE", current)
    user = await conn.fetchrow("SELECT team_id FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user or user["team_id"] != current:
        return None
    clear_user = "UPDATE users SET team_id = NULL, team_joined_at = NULL WHERE user_id = $1"
    if not team:
        await conn.execute(clear_user, user_id)
        return None
    result = {"team_id": current, "team_name": team["team_name"], "outcome": "left", "new_captain": None}
    if team["captain_id"] == user_id:
        next_captain = await conn.fetchrow(
            "SELECT user_id, username FROM users WHERE team_id = $1 AND user_id != $2 "
            "AND NOT is_blocked AND deletion_requested_at IS NULL "
            "ORDER BY team_joined_at ASC NULLS LAST, user_id ASC LIMIT 1",
            current, user_id)
        if next_captain:
            await conn.execute(
                "UPDATE teams SET captain_id = $1, members_count = members_count - 1 WHERE team_id = $2",
                next_captain["user_id"], current)
            result.update(outcome="passed", new_captain=dict(next_captain))
        else:
            # Остались только заблокированные/уходящие — их тоже отвязываем, команды больше нет
            await conn.execute(
                "UPDATE users SET team_id = NULL, team_joined_at = NULL WHERE team_id = $1", current)
            await conn.execute("DELETE FROM teams WHERE team_id = $1", current)
            result["outcome"] = "disbanded"
    else:
        await conn.execute("UPDATE teams SET members_count = members_count - 1 WHERE team_id = $1", current)
    await conn.execute(clear_user, user_id)
    return result


async def create_team(conn, captain_id: int, name: str, motto: str, symbol: str) -> int:
    """Создаёт команду (внутри транзакции вызывающего): тексты проверяются, цена — через ledger."""
    name = validate_team_text(name, TEAM_NAME_MAX_LEN)
    motto = validate_team_text(motto, TEAM_MOTTO_MAX_LEN)
    symbol = validate_team_text(symbol, TEAM_SYMBOL_MAX_LEN)
    user = await conn.fetchrow("SELECT balance, team_id FROM users WHERE user_id = $1 FOR UPDATE", captain_id)
    if not user:
        raise TeamError("common.no_profile")
    if user["team_id"] is not None:
        raise TeamError("team.err_already")
    if user["balance"] < TEAM_CREATE_COST:
        raise TeamError("team.err_money", cost=TEAM_CREATE_COST, balance=user["balance"])
    if await conn.fetchval("SELECT team_id FROM teams WHERE captain_id = $1", captain_id):
        raise TeamError("team.err_captain")
    if await conn.fetchval("SELECT team_id FROM teams WHERE team_name = $1", name):
        raise TeamError("team.err_taken", name=name)
    try:
        await change_balance(conn, captain_id, -TEAM_CREATE_COST, "team_create", name)
    except InsufficientFunds:
        raise TeamError("team.err_money", cost=TEAM_CREATE_COST, balance=user["balance"])
    team_id = await conn.fetchval(
        "INSERT INTO teams (team_name, captain_id, city, school_num) VALUES ($1, $2, $3, $4) RETURNING team_id",
        name, captain_id, motto, symbol)
    await conn.execute("UPDATE users SET team_id = $1, team_joined_at = NOW() WHERE user_id = $2", team_id, captain_id)
    logger.info("[TEAM_CREATED] team=%s captain=%s", team_id, captain_id)
    return team_id


async def create_new_team_in_db(captain_id: int, team_name: str, city: str, school: str) -> tuple[bool, str]:
    """
    Вход чат-бота (FSM уже проверил тексты и экранировал их). Возвращает (успех, статус/ошибка).
    Тексты из чата приходят экранированными — разэкранируем, чтобы create_team не экранировал дважды.
    """
    async with db.pool.acquire() as conn:
        try:
            async with conn.transaction():
                await create_team(conn, captain_id, html.unescape(team_name), html.unescape(city),
                                  html.unescape(school))
        except TeamError as e:
            return False, e.localized("ru")
    return True, "OK"
