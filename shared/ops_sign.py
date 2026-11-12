"""
Подпись запросов пульта к проектам (контракт /ops/summary, версия 1).

Пульт ходит к каждому проекту по адресу <url>/ops/summary с заголовками:
  X-Ops-Ts  — время запроса, unix-секунды;
  X-Ops-Sig — hex HMAC-SHA256(секрет проекта, "<ts>\\n<METHOD>\\n<path>").
Проект принимает запрос, только если подпись сходится и время отличается не больше чем на MAX_SKEW секунд.
Этот файл КОПИРУЕТСЯ в каждый проект (ops_endpoint) — проекты живут независимо, общей библиотеки нет.
"""
from __future__ import annotations

import hashlib
import hmac
import time

HEADER_TS = "X-Ops-Ts"
HEADER_SIG = "X-Ops-Sig"
MAX_SKEW = 300          # 5 минут — часы серверов Railway не расходятся сильнее
MIN_SECRET_LEN = 32


def signature(secret: str, ts: int, method: str, path: str) -> str:
    msg = f"{int(ts)}\n{method.upper()}\n{path}".encode()
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()


def sign_headers(secret: str, method: str, path: str, now: float | None = None) -> dict[str, str]:
    ts = int(now if now is not None else time.time())
    return {HEADER_TS: str(ts), HEADER_SIG: signature(secret, ts, method, path)}


def verify(secret: str, method: str, path: str, ts_header: str | None, sig_header: str | None,
           now: float | None = None) -> bool:
    if not secret or len(secret) < MIN_SECRET_LEN or not ts_header or not sig_header:
        return False
    try:
        ts = int(ts_header)
    except ValueError:
        return False
    now = now if now is not None else time.time()
    if abs(now - ts) > MAX_SKEW:
        return False
    return hmac.compare_digest(signature(secret, ts, method, path), sig_header)
