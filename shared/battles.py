"""
Битвы команд и кланов — событийные состязания, запускаемые владельцем вручную.

Принципы (решения владельца 13.10.2026):
- битвы ПЕРИОДИЧЕСКИЕ, а не ежедневные: событие, как ЧМ по футболу;
- считается ТОЛЬКО общий результат всех игроков команды — мотивация звать актив;
- зачёт по журналу ledger за окно [starts_at, ends_at] — задним числом не накрутишь;
- команда игрока определяется на момент подведения итогов;
- призы: за 1-е и места 2–10, каждый — либо товар из магазина (авто-выдача каждому
  участнику команды), либо ручное описание (владелец вручает сам).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime

from shared.delivery import DeliveryError, deliver_order

logger = logging.getLogger(__name__)

MAX_PRIZE_PLACES = 10

# Номинации: kind определяет формулу подсчёта по ledger/users за окно битвы
BATTLE_NOMINATIONS: dict[str, dict] = {
    "farm_mined": {"title": "⛏️ Больше всех нафармить рофлов фермой",
                   "kind": "ledger_sum", "reason": "mining", "unit": "рофлов"},
    "coins_earned": {"title": "💰 Больше всех заработать рофлов (все источники)",
                     "kind": "ledger_sum_positive", "unit": "рофлов"},
    "duel_wins": {"title": "⚔️ Больше всех побед в дуэлях",
                  "kind": "ledger_count", "reason": "duel_win", "unit": "побед"},
    "duels_played": {"title": "🎲 Больше всех сыгранных дуэлей",
                     "kind": "ledger_count", "reason": "duel_stake", "unit": "дуэлей"},
    "quiz_wins": {"title": "🧠 Больше всех верных ответов в Викторине",
                  "kind": "ledger_count", "reason": "game_win:quiz", "unit": "ответов"},
    "rps_wins": {"title": "🪨 Больше всех побед в КНБ",
                 "kind": "ledger_count", "reason": "game_win:rps", "unit": "побед"},
    "safe_wins": {"title": "🔐 Больше всех вскрытых Кибер-Сейфов",
                  "kind": "ledger_count", "reason": "game_win:safe", "unit": "сейфов"},
    "game_wins_total": {"title": "🏆 Больше всех побед во всех играх против бота",
                        "kind": "ledger_count_like", "reason_like": "game_win:%", "unit": "побед"},
    "referrals": {"title": "🤝 Больше всех привести новичков в экосистему",
                  "kind": "referrals", "unit": "новичков"},
    "stars_spent": {"title": "💵 Больше всех поддержать экосистему (Stars)",
                    "kind": "stars", "unit": "★"},
}


async def battle_team_scores(conn, nomination_key: str, starts_at: datetime,
                             ends_at: datetime, limit: int = MAX_PRIZE_PLACES) -> list[dict]:
    """
    ТОП команд по номинации за окно битвы:
    [{team_id, team_name, is_clan, score}] по убыванию. Нулевые результаты не попадают.
    """
    nom = BATTLE_NOMINATIONS[nomination_key]
    kind = nom["kind"]

    if kind in ("ledger_sum", "ledger_count", "ledger_sum_positive", "ledger_count_like"):
        if kind == "ledger_sum":
            metric, condition = "SUM(l.delta)", "l.reason = $3"
            args = [starts_at, ends_at, nom["reason"]]
        elif kind == "ledger_count":
            metric, condition = "COUNT(*)", "l.reason = $3"
            args = [starts_at, ends_at, nom["reason"]]
        elif kind == "ledger_count_like":
            metric, condition = "COUNT(*)", "l.reason LIKE $3"
            args = [starts_at, ends_at, nom["reason_like"]]
        else:  # ledger_sum_positive
            metric, condition = "SUM(l.delta)", "l.delta > 0"
            args = [starts_at, ends_at]
        query = f"""
            SELECT u.team_id, t.team_name, t.max_members >= 1000 AS is_clan,
                   {metric}::bigint AS score
            FROM ledger l
            JOIN users u ON u.user_id = l.user_id
            JOIN teams t ON t.team_id = u.team_id
            WHERE l.created_at >= $1 AND l.created_at < $2 AND {condition}
            GROUP BY u.team_id, t.team_name, t.max_members
            HAVING {metric} > 0
            ORDER BY {metric} DESC, u.team_id ASC
            LIMIT {int(limit)}
        """
        rows = await conn.fetch(query, *args)
    elif kind == "referrals":
        rows = await conn.fetch(
            """
            SELECT ref.team_id, t.team_name, t.max_members >= 1000 AS is_clan,
                   COUNT(*)::bigint AS score
            FROM users newbie
            JOIN users ref ON ref.user_id = newbie.referred_by
            JOIN teams t ON t.team_id = ref.team_id
            WHERE newbie.created_at >= $1 AND newbie.created_at < $2
            GROUP BY ref.team_id, t.team_name, t.max_members
            ORDER BY COUNT(*) DESC, ref.team_id ASC
            LIMIT {limit}
            """.replace("{limit}", str(int(limit))),
            starts_at, ends_at)
    elif kind == "stars":
        rows = await conn.fetch(
            """
            SELECT u.team_id, t.team_name, t.max_members >= 1000 AS is_clan,
                   SUM(p.stars_amount)::bigint AS score
            FROM star_payments p
            JOIN users u ON u.user_id = p.user_id
            JOIN teams t ON t.team_id = u.team_id
            WHERE p.created_at >= $1 AND p.created_at < $2
            GROUP BY u.team_id, t.team_name, t.max_members
            HAVING SUM(p.stars_amount) > 0
            ORDER BY SUM(p.stars_amount) DESC, u.team_id ASC
            LIMIT {limit}
            """.replace("{limit}", str(int(limit))),
            starts_at, ends_at)
    else:
        raise ValueError(f"Неизвестный вид номинации: {kind}")

    return [dict(r) for r in rows]


async def award_sku_to_team(conn, team_id: int, sku: str, order: dict,
                            battle_id: int, place: int) -> tuple[int, int]:
    """
    Выдаёт товар КАЖДОМУ участнику команды. Возвращает (выдано, пропущено).
    Идемпотентно: charge_id уникален на битву/место/игрока, повтор упрётся в UNIQUE.
    """
    members = await conn.fetch("SELECT user_id FROM users WHERE team_id = $1", team_id)
    delivered = skipped = 0
    for m in members:
        charge_id = f"BATTLE{battle_id}_P{place}_U{m['user_id']}"
        try:
            async with conn.transaction():
                await conn.execute("SELECT 1 FROM users WHERE user_id = $1 FOR UPDATE", m["user_id"])
                await deliver_order(conn, m["user_id"], order, charge_id)
            delivered += 1
        except DeliveryError as e:
            skipped += 1
            logger.info("[BATTLE_PRIZE] пропуск user=%s sku=%s: %s", m["user_id"], sku, e)
        except Exception:
            skipped += 1
            logger.exception("[BATTLE_PRIZE] сбой выдачи user=%s sku=%s", m["user_id"], sku)
    return delivered, skipped


def medals(place: int) -> str:
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(place, f"{place}.")


def build_results_post(battle, scores: list[dict], prize_notes: dict[int, str]) -> str:
    """
    Публикация итогов в канал: тройка лидеров — ярко, места 4–10 — скромнее.
    prize_notes: {place: строка о призе} (авто-выданные или ручные описания).
    """
    lines = [
        f"🏁 <b>БИТВА «{battle['title']}» ЗАВЕРШЕНА!</b>",
        f"🏅 Номинация: <i>{battle['nomination_text']}</i>",
        "..................................................", ""
    ]
    unit = BATTLE_NOMINATIONS.get(battle["nomination_key"], {}).get("unit", "очков")

    if not scores:
        lines.append("😶 Ни одна команда не набрала очков в этой битве. Такое бывает только раз!")
        return "\n".join(lines)

    for i, row in enumerate(scores[:3], start=1):
        crown = "👑 КЛАН" if row["is_clan"] else "🏆 Команда"
        lines.append(f"{medals(i)} <b>{row['team_name']}</b> ({crown}) — <b>{row['score']} {unit}</b>")
        if i in prize_notes:
            lines.append(f"      🎁 {prize_notes[i]}")
        lines.append("")

    rest = scores[3:]
    if rest:
        lines.append("<i>Остальные герои турнирной таблицы:</i>")
        for i, row in enumerate(rest, start=4):
            suffix = f" · 🎁 {prize_notes[i]}" if i in prize_notes else ""
            lines.append(f"{medals(i)} {row['team_name']} — {row['score']} {unit}{suffix}")
        lines.append("")

    lines.append("..................................................")
    lines.append("<i>Собирай свою банду в /my_team — следующая битва не за горами!</i>")
    return "\n".join(lines)


def build_announce_post(battle) -> str:
    """Анонс новой битвы в канал игроков."""
    return (
        f"📣 <b>ОБЪЯВЛЕНА БИТВА КОМАНД И КЛАНОВ: «{battle['title']}»!</b>\n"
        "..................................................\n\n"
        f"🏅 Номинация: <b>{battle['nomination_text']}</b>\n"
        f"🕐 Старт зачёта: <b>{battle['starts_at']:%d.%m.%Y %H:%M} UTC</b>\n"
        f"🏁 Финиш: <b>{battle['ends_at']:%d.%m.%Y %H:%M} UTC</b>\n\n"
        "⚡ Считается ОБЩИЙ результат всех игроков команды — зови актив в банду, "
        "каждый боец приближает победу!\n"
        "🎁 Призы получит КАЖДЫЙ участник команд-призёров. Подробности — после финиша.\n\n"
        "..................................................\n"
        "<i>Вступай в команду через /my_team или /all_teams в боте — и в бой!</i>"
    )


def parse_battle_moment(raw: str, base: datetime | None = None) -> datetime | None:
    """
    Парсер моментов битвы: 'ДД.ММ.ГГГГ ЧЧ:ММ' (UTC) либо число часов от base.
    Возвращает None, если распарсить не удалось.
    """
    raw = raw.strip()
    if raw.isdigit() and base is not None:
        from datetime import timedelta
        return base + timedelta(hours=int(raw))
    try:
        from datetime import timezone
        return datetime.strptime(raw, "%d.%m.%Y %H:%M").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def prizes_to_json(prizes: dict[int, dict]) -> str:
    return json.dumps({str(k): v for k, v in prizes.items()}, ensure_ascii=False)


def prizes_from_row(value) -> dict[int, dict]:
    data = json.loads(value) if isinstance(value, str) else (value or {})
    return {int(k): v for k, v in data.items()}
