from aiogram.fsm.state import StatesGroup, State

class TeamCreationStates(StatesGroup):
    """Офис удержания шагов создания команды класса"""
    name = State()        # Шаг 1: Ввод имени банды
    city = State()        # Шаг 2: Ввод города
    school = State()      # Шаг 3: Ввод номера школы
