"""
📬 Личные сообщения о наградах (решение владельца 26.10: каналов нет — каждому получившему пишет бот).

finish_battle и finalize_target возвращают notices — по записи на игрока, которому что-то выдано:
{user_id, title, place, rewards, all, mine_id?}. Здесь — текст на языке игрока и отправка от имени
ГЛАВНОГО бота (админ-бот первым писать не может). Сбой отправки никогда не ломает итоги.
"""
from __future__ import annotations

import asyncio
import html
import logging

from shared.economy import MINE_HOLD_HOURS
from shared.locales import t

logger = logging.getLogger(__name__)
SEND_PAUSE_SEC = 0.05          # ~20 сообщений в секунду — в лимитах Telegram


def notice_text(lang: str, notice: dict) -> str:
    """Текст личного сообщения: место/участие, что начислено, рудник, ручной приз."""
    from shared.prizes import rewards_label
    from shared.titles import localized_title
    title = html.escape(localized_title(str(notice.get("title") or ""), notice.get("tpl"), lang))
    rewards = notice.get("rewards") or []
    lines = [t(lang, "rn.all" if notice.get("all") else "rn.place", title=title, place=notice.get("place", 0))]
    real = [r for r in rewards if r.get("kind") != "text"]
    if real:
        lines.append(t(lang, "rn.got", r=html.escape(rewards_label(real))))
    for r in rewards:
        if r.get("kind") == "text":
            lines.append(t(lang, "rn.manual", r=html.escape(r.get("text", ""))))
    if notice.get("mine_id"):
        lines.append(t(lang, "rn.mine", mine=notice["mine_id"], hours=MINE_HOLD_HOURS))
    if real:
        lines.append(t(lang, "rn.where"))
    return "\n".join(lines)


async def send_notices(bot, pool, notices: list[dict]) -> int:
    """
    Рассылает уведомления (bot — экземпляр ГЛАВНОГО бота, pool — пул БД: соединение берётся только на
    чтение языков и не держится во время рассылки). Возвращает число доставленных.
    """
    if not notices or bot is None:
        return 0
    ids = sorted({n["user_id"] for n in notices})
    async with pool.acquire() as conn:
        langs = {r["user_id"]: r["lang"] for r in await conn.fetch(
            "SELECT user_id, lang FROM users WHERE user_id = ANY($1::bigint[])", ids)}
    sent = 0
    for n in notices:
        try:
            await bot.send_message(n["user_id"], notice_text(langs.get(n["user_id"]) or "en", n), parse_mode="HTML")
            sent += 1
        except Exception as e:
            logger.warning("[NOTIFY] награда игроку %s не доставлена: %s", n["user_id"], e)
        await asyncio.sleep(SEND_PAUSE_SEC)
    return sent
