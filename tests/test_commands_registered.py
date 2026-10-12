"""
Каждая /команда, которую бот показывает игроку (меню, онбординг, подсказки), должна иметь обработчик.
Этот тест поймал бы баг «/create_team не отвечает».
"""
import os

import pytest

pytest.importorskip("aiogram")
os.environ.setdefault("MAIN_BOT_TOKEN", "123456:TEST")

from aiogram.filters import Command  # noqa: E402

from bots.main_bot.handlers import (  # noqa: E402
    clans, faq, farm, games, menu, payments, profile, referral_link, rofl_hub_all, rules, shop,
    start, transfer,
)

ROUTERS = [start.router, payments.router, shop.router, games.router, farm.router, profile.router,
           clans.router, transfer.router, referral_link.router, menu.router, faq.router,
           rules.router, rofl_hub_all.router]

ADVERTISED_COMMANDS = {
    "start", "menu", "profile", "my_stats", "farm", "shop", "games",
    "create_team", "my_team", "all_teams", "faq", "rules",
    "rps", "high_low", "quiz", "coin", "dice", "safe",
    "invite", "transfer",
}


def _registered_commands() -> set[str]:
    found: set[str] = set()
    for router in ROUTERS:
        for handler in router.message.handlers:
            for flt in handler.filters or []:
                cb = flt.callback
                if isinstance(cb, Command):
                    for c in cb.commands:
                        if isinstance(c, str):
                            found.add(c.lstrip("/"))
    return found


def test_every_advertised_command_has_a_handler():
    missing = ADVERTISED_COMMANDS - _registered_commands()
    assert not missing, f"Команды без обработчика: {sorted(missing)}"
