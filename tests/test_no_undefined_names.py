"""
14.11: /api/me упал на неопределённой переменной (`lang` вместо payload["lang"]) — приложение не открывалось 20 минут,
а юнит-тесты этот путь не проходили. Статическая проверка: ни одного «undefined name» во всём коде ботов и shared.
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_no_undefined_names_in_bots_and_shared():
    api = pytest.importorskip("pyflakes.api")
    from pyflakes import messages, reporter as rep

    found = []

    class _Collect(rep.Reporter):
        def __init__(self):
            pass

        def flake(self, msg):
            if isinstance(msg, (messages.UndefinedName, messages.UndefinedLocal)):
                found.append(f"{msg.filename}:{msg.lineno} {msg.message % msg.message_args}")

        def syntaxError(self, *a):
            found.append(f"syntax: {a[0]}")

        def unexpectedError(self, filename, msg):
            found.append(f"{filename}: {msg}")

    for folder in ("bots", "shared"):
        for path in sorted((ROOT / folder).rglob("*.py")):
            api.check(path.read_text(encoding="utf-8"), str(path), _Collect())
    assert not found, found
