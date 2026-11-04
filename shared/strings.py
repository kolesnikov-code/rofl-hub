import logging

logger = logging.getLogger(__name__)


def get_plural_form(number: int, form_1: str, form_2: str, form_5: str) -> str:
    """
    Универсальный геймдев-валидатор русской лингвистики холдинга CYBER BARONS CORE.
    Ювелирно рассчитывает окончания слов в зависимости от числительного.
    """
    abs_num = abs(number) % 100
    num_last = abs_num % 10

    if abs_num > 10 and abs_num < 20:
        return form_5
    if num_last > 1 and num_last < 5:
        return form_2
    if num_last == 1:
        return form_1

    return form_5


# ============================================================================
# 🥩 ЛИНГВИСТИЧЕСКИЕ ШЛЮЗЫ ИГРОВОГО ИНВЕНТАРЯ (СНАЙПЕРСКИЙ ФИКС ОПЕЧАТОК)
# ============================================================================
def format_cutlets(count: int) -> str:
    """Склоняет кибер-котлеты строго по правилам русского языка (без 'котлен')"""
    return f"{count} " + get_plural_form(count, "кибер-котлета", "кибер-котлеты", "кибер-котлет")


def format_coins(count: int) -> str:
    """Склоняет розничную игровую валюту (монеты)"""
    return f"{count} " + get_plural_form(count, "монета", "монеты", "монет")


def format_miners(count: int) -> str:
    """Склоняет Младших Майнеров на заводе (нейминг строго как в каталоге магазина)"""
    return f"{count} " + get_plural_form(count, "Младший Майнер", "Младших Майнера", "Младших Майнеров")


def format_members(count: int) -> str:
    """Склоняет живых участников внутри школьной банды"""
    return f"{count} " + get_plural_form(count, "участник", "участника", "участников")
