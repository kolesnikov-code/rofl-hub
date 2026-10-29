"""
Дуэли (КНБ 1-на-1 со ставками): матчмейкинг по столам, эскроу, сжигание 20%.

Правила:
- ставка списывается СРАЗУ при входе за стол (ledger reason='duel_stake');
- отмена ожидания или протухшая очередь — полный возврат (reason='duel_refund');
- победитель получает 80% банка (reason='duel_win'), 20% сгорает (списаны оба,
  начислен один — сжигание происходит само собой, эмиссии нет);
- ничья в раунде — переигровка жестов, банк не трогаем;
- все функции вызываются ВНУТРИ транзакции вызывающего кода.
"""
from __future__ import annotations

import logging
import random
from dataclasses import dataclass

import secrets

from shared.economy import DUEL_INVITE_CODE_LEN, DUEL_INVITE_TTL_HOURS, DUEL_TABLES, DUEL_WAITING_TTL_MINUTES, duel_payout, utcnow
from shared.ledger import InsufficientFunds, change_balance

logger = logging.getLogger(__name__)

RPS_BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
DUEL_MOVES = tuple(RPS_BEATS)


class DuelError(Exception):
    """Причина отказа: ключ локали для показа игроку."""

    def __init__(self, key: str, **kwargs):
        self.key = key
        self.kwargs = kwargs
        super().__init__(key)


@dataclass
class JoinResult:
    duel_id: int
    matched: bool               # True — пара собрана, дуэль началась
    opponent_id: int | None = None  # соперник (player1), если matched


@dataclass
class MoveResult:
    finished: bool              # дуэль завершена
    draw_replay: bool = False   # ничья — нужен новый раунд
    waiting_opponent: bool = False  # ход записан, ждём второго игрока
    winner_id: int | None = None
    loser_id: int | None = None
    winner_move: str | None = None
    loser_move: str | None = None
    payout: int = 0
    burned: int = 0
    rounds: int = 1


async def has_premium(conn, user_id: int) -> bool:
    """⚡ Безлимит активен — комиссия дуэли DUEL_BURN_PERCENT_PREMIUM вместо DUEL_BURN_PERCENT."""
    until = await conn.fetchval("SELECT unlimit_until FROM users WHERE user_id = $1", user_id)
    return until is not None and until > utcnow()


async def active_duel_of(conn, user_id: int):
    """Текущая незавершённая дуэль игрока (waiting или active) или None."""
    return await conn.fetchrow(
        "SELECT * FROM duels WHERE status IN ('waiting', 'active') "
        "AND (player1 = $1 OR player2 = $1) LIMIT 1", user_id)


async def join_or_create_duel(conn, user_id: int, stake: int) -> JoinResult:
    """Сажает игрока за стол: либо матч с ожидающим, либо новая очередь."""
    if stake not in DUEL_TABLES:
        raise DuelError("duel.bad_table")

    if await active_duel_of(conn, user_id) is not None:
        raise DuelError("duel.already_in")

    # Эскроу ставки (атомарно защищает и от нехватки баланса)
    try:
        await change_balance(conn, user_id, -stake, "duel_stake", f"table_{stake}")
    except InsufficientFunds:
        raise DuelError("duel.no_coins", stake=stake)

    waiting = await conn.fetchrow(
        "SELECT * FROM duels WHERE status = 'waiting' AND stake = $1 AND player1 != $2 AND invite_code IS NULL "
        "ORDER BY duel_id LIMIT 1 FOR UPDATE SKIP LOCKED",
        stake, user_id)

    if waiting:
        await conn.execute(
            "UPDATE duels SET player2 = $2, status = 'active', round_started_at = NOW() "
            "WHERE duel_id = $1",
            waiting["duel_id"], user_id)
        return JoinResult(duel_id=waiting["duel_id"], matched=True, opponent_id=waiting["player1"])

    duel_id = await conn.fetchval(
        "INSERT INTO duels (stake, player1) VALUES ($1, $2) RETURNING duel_id", stake, user_id)
    return JoinResult(duel_id=duel_id, matched=False)


# ---------------------------------------------------------------- ⚔️ вызов друга по ссылке (27.10)
_CODE_ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"   # без 0/o/1/l/i — код читается вслух


def new_invite_code() -> str:
    return "".join(secrets.choice(_CODE_ALPHABET) for _ in range(DUEL_INVITE_CODE_LEN))


def valid_invite_code(code: str | None) -> bool:
    return bool(code) and len(code) == DUEL_INVITE_CODE_LEN and all(c in _CODE_ALPHABET for c in code)


async def create_invite_duel(conn, user_id: int, stake: int) -> tuple[int, str]:
    """Приватная дуэль: ставка в эскроу, стол ждёт друга по ссылке (в общую очередь не попадает)."""
    if stake not in DUEL_TABLES:
        raise DuelError("duel.bad_table")
    if await active_duel_of(conn, user_id) is not None:
        raise DuelError("duel.already_in")
    try:
        await change_balance(conn, user_id, -stake, "duel_stake", f"invite_{stake}")
    except InsufficientFunds:
        raise DuelError("duel.no_coins", stake=stake)
    for _ in range(5):   # коллизия кода почти невозможна, но уникальный индекс всё равно страхует
        code = new_invite_code()
        if not await conn.fetchval("SELECT 1 FROM duels WHERE invite_code = $1", code):
            break
    duel_id = await conn.fetchval(
        "INSERT INTO duels (stake, player1, invite_code) VALUES ($1, $2, $3) RETURNING duel_id", stake, user_id, code)
    return duel_id, code


async def invite_info(conn, code: str):
    """Открытый вызов по коду (ждёт соперника и не протух) или None."""
    if not valid_invite_code(code):
        return None
    return await conn.fetchrow(
        "SELECT d.duel_id, d.stake, d.player1, d.created_at, u.username, u.display_name FROM duels d "
        "JOIN users u ON u.user_id = d.player1 WHERE d.invite_code = $1 AND d.status = 'waiting' "
        "AND d.created_at > NOW() - make_interval(hours => $2)", code, DUEL_INVITE_TTL_HOURS)


async def accept_invite_duel(conn, user_id: int, code: str) -> JoinResult:
    """Друг принимает вызов: его ставка в эскроу, дуэль начинается. Внутри транзакции."""
    if not valid_invite_code(code):
        raise DuelError("duel.invite_gone")
    duel = await conn.fetchrow(
        "SELECT * FROM duels WHERE invite_code = $1 AND status = 'waiting' "
        "AND created_at > NOW() - make_interval(hours => $2) FOR UPDATE", code, DUEL_INVITE_TTL_HOURS)
    if duel is None:
        raise DuelError("duel.invite_gone")
    if duel["player1"] == user_id:
        raise DuelError("duel.invite_self")
    if await active_duel_of(conn, user_id) is not None:
        raise DuelError("duel.already_in")
    try:
        await change_balance(conn, user_id, -duel["stake"], "duel_stake", f"invite_{duel['duel_id']}")
    except InsufficientFunds:
        raise DuelError("duel.no_coins", stake=duel["stake"])
    await conn.execute("UPDATE duels SET player2 = $2, status = 'active', round_started_at = NOW() WHERE duel_id = $1",
                       duel["duel_id"], user_id)
    await conn.execute("UPDATE users SET pending_duel = NULL WHERE user_id = $1", user_id)
    return JoinResult(duel_id=duel["duel_id"], matched=True, opponent_id=duel["player1"])


async def cancel_waiting_duel(conn, duel_id: int, user_id: int) -> int:
    """Отмена своей очереди с возвратом ставки. Возвращает сумму возврата."""
    duel = await conn.fetchrow(
        "SELECT * FROM duels WHERE duel_id = $1 FOR UPDATE", duel_id)
    if not duel or duel["status"] != "waiting" or duel["player1"] != user_id:
        raise DuelError("duel.cancel_impossible")
    await conn.execute("UPDATE duels SET status = 'cancelled', finished_at = NOW() "
                       "WHERE duel_id = $1", duel_id)
    await change_balance(conn, user_id, duel["stake"], "duel_refund", str(duel_id))
    return duel["stake"]


async def record_move(conn, duel_id: int, user_id: int, move: str) -> MoveResult:
    """Записывает жест игрока; когда оба жеста на столе — разрешает раунд."""
    if move not in DUEL_MOVES:
        raise DuelError("duel.bad_move")
    duel = await conn.fetchrow("SELECT * FROM duels WHERE duel_id = $1 FOR UPDATE", duel_id)
    if not duel or duel["status"] != "active":
        raise DuelError("duel.not_active")
    if user_id == duel["player1"]:
        column, already = "move1", duel["move1"]
    elif user_id == duel["player2"]:
        column, already = "move2", duel["move2"]
    else:
        raise DuelError("duel.not_participant")
    if already is not None:
        raise DuelError("duel.move_already")

    await conn.execute(f"UPDATE duels SET {column} = $2 WHERE duel_id = $1", duel_id, move)
    duel = await conn.fetchrow("SELECT * FROM duels WHERE duel_id = $1", duel_id)
    if duel["move1"] is None or duel["move2"] is None:
        return MoveResult(finished=False, waiting_opponent=True, rounds=duel["rounds"])
    return await _resolve_round(conn, duel)


async def resolve_stuck_duel(conn, duel) -> MoveResult:
    """
    Жнец для зависших дуэлей: недостающие жесты выбираются случайно,
    ничьи переигрываются случайно же до результата — дуэль всегда закрывается.
    """
    move1 = duel["move1"] or random.choice(DUEL_MOVES)
    move2 = duel["move2"] or random.choice(DUEL_MOVES)
    rounds = duel["rounds"]
    while move1 == move2:
        move1, move2 = random.choice(DUEL_MOVES), random.choice(DUEL_MOVES)
        rounds += 1
    await conn.execute("UPDATE duels SET move1 = $2, move2 = $3, rounds = $4 WHERE duel_id = $1",
                       duel["duel_id"], move1, move2, rounds)
    fresh = await conn.fetchrow("SELECT * FROM duels WHERE duel_id = $1", duel["duel_id"])
    return await _resolve_round(conn, fresh)


async def _resolve_round(conn, duel) -> MoveResult:
    move1, move2 = duel["move1"], duel["move2"]
    if move1 == move2:
        # Ничья: банк не трогаем, жесты очищаем, раунд следующий
        await conn.execute(
            "UPDATE duels SET move1 = NULL, move2 = NULL, rounds = rounds + 1, "
            "round_started_at = NOW() WHERE duel_id = $1",
            duel["duel_id"])
        return MoveResult(finished=False, draw_replay=True, rounds=duel["rounds"] + 1)

    if RPS_BEATS[move1] == move2:
        winner_id, loser_id = duel["player1"], duel["player2"]
        winner_move, loser_move = move1, move2
    else:
        winner_id, loser_id = duel["player2"], duel["player1"]
        winner_move, loser_move = move2, move1

    premium = await has_premium(conn, winner_id)
    payout, burned = duel_payout(duel["stake"], premium)
    await change_balance(conn, winner_id, payout, "duel_win", str(duel["duel_id"]))
    from shared.trophies import record   # 🏆 «пережил дуэль» — оба, победа — победителю
    await record(conn, winner_id, "duel")
    await record(conn, winner_id, "duel_win")
    await record(conn, loser_id, "duel")
    await conn.execute(
        "UPDATE duels SET status = 'finished', winner_id = $2, finished_at = NOW() WHERE duel_id = $1",
        duel["duel_id"], winner_id)
    await conn.execute(
        """
        INSERT INTO game_stats (user_id, games_played, games_won) VALUES ($1, 1, 1)
        ON CONFLICT (user_id) DO UPDATE SET
            games_played = game_stats.games_played + 1, games_won = game_stats.games_won + 1
        """, winner_id)
    await conn.execute(
        """
        INSERT INTO game_stats (user_id, games_played) VALUES ($1, 1)
        ON CONFLICT (user_id) DO UPDATE SET games_played = game_stats.games_played + 1
        """, loser_id)
    logger.info("[DUEL] finished duel=%s stake=%s winner=%s payout=%s burned=%s",
                duel["duel_id"], duel["stake"], winner_id, payout, burned)
    return MoveResult(finished=True, winner_id=winner_id, loser_id=loser_id,
                      winner_move=winner_move, loser_move=loser_move,
                      payout=payout, burned=burned, rounds=duel["rounds"])


async def find_stuck_active_duels(conn, older_than_seconds: int):
    """Активные дуэли, где раунд завис дольше таймаута (для жнеца)."""
    return await conn.fetch(
        "SELECT * FROM duels WHERE status = 'active' "
        "AND round_started_at < NOW() - make_interval(secs => $1) "
        "AND (move1 IS NULL OR move2 IS NULL) FOR UPDATE SKIP LOCKED",
        older_than_seconds)


async def expire_waiting_duels(conn, older_than_minutes: int) -> list[tuple[int, int, int]]:
    """Отменяет протухшие очереди. Возвращает [(duel_id, player1, stake)] для уведомлений."""
    rows = await conn.fetch(   # вызов друга живёт дольше общей очереди (DUEL_INVITE_TTL_HOURS)
        "SELECT * FROM duels WHERE status = 'waiting' AND ("
        "(invite_code IS NULL AND created_at < NOW() - make_interval(mins => $1)) OR "
        "(invite_code IS NOT NULL AND created_at < NOW() - make_interval(hours => $2))) FOR UPDATE SKIP LOCKED",
        older_than_minutes, DUEL_INVITE_TTL_HOURS)
    expired = []
    for duel in rows:
        await conn.execute(
            "UPDATE duels SET status = 'cancelled', finished_at = NOW() WHERE duel_id = $1",
            duel["duel_id"])
        await change_balance(conn, duel["player1"], duel["stake"], "duel_refund", str(duel["duel_id"]))
        expired.append((duel["duel_id"], duel["player1"], duel["stake"]))
    return expired
