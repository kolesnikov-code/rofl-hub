"""
Гварды разделов: вход в выключенный владельцем раздел вежливо отклоняется.
Тумблеры живут в shared/feature_flags (пульт — в админ-боте, /features).
"""
from __future__ import annotations

from aiogram import types

from shared.feature_flags import get_flag
from shared.locales import t


async def feature_enabled(event: types.Message | types.CallbackQuery, flag: str,
                          lang: str = "ru") -> bool:
    """True — раздел включён. False — игроку уже отправлена заглушка техобслуживания."""
    if await get_flag(flag):
        return True
    text = t(lang, "common.feature_off")
    try:
        if isinstance(event, types.CallbackQuery):
            await event.answer(text, show_alert=True)
        else:
            await event.answer(text)
    except Exception:
        pass
    return False
