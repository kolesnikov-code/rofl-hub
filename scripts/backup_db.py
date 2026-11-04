"""
Локальный бэкап базы Cyber Barons в JSON-файл.

Запуск (из корня проекта, DATABASE_URL берётся из .env):
    python -m scripts.backup_db

Файл сохраняется в backups/rofl_hub_backup_<дата_время>.json.
Тот же снимок можно получить командой /backup в админ-боте.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from pathlib import Path

from shared.database import db
from shared.db_admin import backup_to_json_bytes, dump_database

BACKUPS_DIR = Path(__file__).resolve().parents[1] / "backups"


async def main() -> None:
    await db.connect()
    try:
        async with db.pool.acquire() as conn:
            dump = await dump_database(conn)
    finally:
        await db.close()

    BACKUPS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = BACKUPS_DIR / f"rofl_hub_backup_{stamp}.json"
    payload = backup_to_json_bytes(dump)
    path.write_bytes(payload)

    rows_total = sum(len(v) for v in dump["tables"].values())
    print(f"Бэкап сохранён: {path}")
    print(f"Таблиц: {len(dump['tables'])} · строк: {rows_total} · размер: {len(payload) / 1024:.1f} КБ")


if __name__ == "__main__":
    asyncio.run(main())
