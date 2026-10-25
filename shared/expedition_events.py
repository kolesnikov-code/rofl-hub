"""
🗺 Развилки экспедиций: события в пути и варианты решения (решение владельца 28.10 — игра решений,
а не кубик). У варианта честные последствия (числа видит отряд с 🛰 шпионом или 🔭 разведкой 2+):
- cargo — добыча, которую отряд добавляет к грузу (атакующие дроны усиливают её на «силовых» вариантах);
- loss — процент груза, который теряется (защитники отряда снижают потери);
- delay — минуты, на которые путь удлиняется (отрицательные — срезали дорогу и пришли раньше);
- fight — «силовой» вариант (работают ⚔️ атакующие дроны).
Тексты: ru и en; остальные языки добавляются сюда же (при отсутствии — английский).
Новое событие = новая запись в EVENTS, код менять не нужно.
"""
from __future__ import annotations

EVENTS: tuple[dict, ...] = (
    {"id": "storm", "icon": "🌪", "text": {
        "ru": "Песчаная буря закрывает горизонт. Приборы сходят с ума.",
        "en": "A sandstorm swallows the horizon. Instruments go haywire."},
     "options": (
        {"text": {"ru": "Переждать в укрытии", "en": "Wait it out in shelter"}, "cargo": 5, "loss": 0, "delay": 60},
        {"text": {"ru": "Идти напролом", "en": "Push straight through"}, "cargo": 20, "loss": 15, "delay": -20},
        {"text": {"ru": "Обойти по старому руслу", "en": "Detour along the old riverbed"}, "cargo": 10, "loss": 5, "delay": 25},
     )},
    {"id": "depot", "icon": "🏚", "text": {
        "ru": "Заброшенный склад. Двери заварены, внутри что-то гудит.",
        "en": "An abandoned depot. Doors welded shut, something hums inside."},
     "options": (
        {"text": {"ru": "Вскрыть двери", "en": "Cut the doors open"}, "cargo": 35, "loss": 10, "delay": 30, "fight": True},
        {"text": {"ru": "Обыскать периметр", "en": "Search the perimeter"}, "cargo": 12, "loss": 0, "delay": 15},
        {"text": {"ru": "Не тратить время", "en": "Don't waste time"}, "cargo": 0, "loss": 0, "delay": -15},
     )},
    {"id": "rivals", "icon": "🚩", "text": {
        "ru": "На горизонте чужой отряд. Они тоже нас заметили.",
        "en": "Another squad on the horizon. They've spotted us too."},
     "options": (
        {"text": {"ru": "Предложить обмен", "en": "Offer a trade"}, "cargo": 15, "loss": 0, "delay": 20},
        {"text": {"ru": "Устроить засаду", "en": "Set an ambush"}, "cargo": 40, "loss": 20, "delay": 10, "fight": True},
        {"text": {"ru": "Уйти в тень", "en": "Slip into the shadows"}, "cargo": 0, "loss": 0, "delay": 30},
     )},
    {"id": "bridge", "icon": "🌉", "text": {
        "ru": "Подвесной мост над ущельем. Пара тросов уже лопнула.",
        "en": "A rope bridge over a gorge. A couple of cables have already snapped."},
     "options": (
        {"text": {"ru": "Переправляться по одному", "en": "Cross one by one"}, "cargo": 5, "loss": 0, "delay": 45},
        {"text": {"ru": "Рвануть всем отрядом", "en": "Rush across together"}, "cargo": 10, "loss": 18, "delay": -25},
        {"text": {"ru": "Починить мост", "en": "Repair the bridge"}, "cargo": 15, "loss": 0, "delay": 70},
     )},
    {"id": "cave", "icon": "🕳", "text": {
        "ru": "Пещера светится изнутри — похоже на кристаллы.",
        "en": "A cave glowing from within — looks like crystals."},
     "options": (
        {"text": {"ru": "Спуститься глубже", "en": "Go deeper"}, "cargo": 45, "loss": 15, "delay": 50},
        {"text": {"ru": "Собрать у входа", "en": "Gather near the entrance"}, "cargo": 15, "loss": 0, "delay": 15},
        {"text": {"ru": "Отметить на карте и идти", "en": "Mark the map and move on"}, "cargo": 0, "loss": 0, "delay": 0},
     )},
    {"id": "drone_swarm", "icon": "🐝", "text": {
        "ru": "Рой диких дронов кружит над тропой.",
        "en": "A swarm of wild drones circles over the trail."},
     "options": (
        {"text": {"ru": "Сбить рой", "en": "Shoot the swarm down"}, "cargo": 30, "loss": 12, "delay": 15, "fight": True},
        {"text": {"ru": "Заглушить сигналом", "en": "Jam them with a signal"}, "cargo": 10, "loss": 0, "delay": 25},
        {"text": {"ru": "Проползти под ними", "en": "Crawl beneath them"}, "cargo": 0, "loss": 5, "delay": 5},
     )},
    {"id": "oasis", "icon": "🌴", "text": {
        "ru": "Оазис. Вода, тень и чьи-то следы у источника.",
        "en": "An oasis. Water, shade and someone's footprints by the spring."},
     "options": (
        {"text": {"ru": "Отдохнуть и пополнить запасы", "en": "Rest and resupply"}, "cargo": 20, "loss": 0, "delay": 60},
        {"text": {"ru": "Набрать воды и дальше", "en": "Grab water and go"}, "cargo": 8, "loss": 0, "delay": 10},
        {"text": {"ru": "Пойти по следам", "en": "Follow the footprints"}, "cargo": 30, "loss": 10, "delay": 35},
     )},
    {"id": "minefield", "icon": "💥", "text": {
        "ru": "Старое минное поле. Табличка почти стёрлась.",
        "en": "An old minefield. The warning sign is barely legible."},
     "options": (
        {"text": {"ru": "Разминировать проход", "en": "Clear a path"}, "cargo": 15, "loss": 0, "delay": 55},
        {"text": {"ru": "Пройти по своим следам", "en": "Step in each other's footprints"}, "cargo": 5, "loss": 10, "delay": 10},
        {"text": {"ru": "Обойти поле", "en": "Go around the field"}, "cargo": 0, "loss": 0, "delay": 40},
     )},
    {"id": "signal", "icon": "📡", "text": {
        "ru": "Слабый сигнал SOS с радиовышки в стороне от маршрута.",
        "en": "A faint SOS from a radio tower off the route."},
     "options": (
        {"text": {"ru": "Свернуть на помощь", "en": "Turn back to help"}, "cargo": 35, "loss": 0, "delay": 60},
        {"text": {"ru": "Передать координаты и идти", "en": "Relay coordinates and move on"}, "cargo": 8, "loss": 0, "delay": 5},
        {"text": {"ru": "Проверить — вдруг ловушка", "en": "Scout it — could be a trap"}, "cargo": 25, "loss": 8, "delay": 35, "fight": True},
     )},
    {"id": "train", "icon": "🚂", "text": {
        "ru": "По рельсам ползёт автоматический товарняк.",
        "en": "An automated freight train crawls along the rails."},
     "options": (
        {"text": {"ru": "Запрыгнуть на ходу", "en": "Jump aboard on the move"}, "cargo": 10, "loss": 12, "delay": -40},
        {"text": {"ru": "Отцепить вагон", "en": "Uncouple a wagon"}, "cargo": 40, "loss": 15, "delay": 25, "fight": True},
        {"text": {"ru": "Пропустить", "en": "Let it pass"}, "cargo": 0, "loss": 0, "delay": 15},
     )},
    {"id": "ice", "icon": "🧊", "text": {
        "ru": "Озеро покрыто тонким льдом. По льду — прямая дорога.",
        "en": "A lake under thin ice. Across it — a straight path."},
     "options": (
        {"text": {"ru": "По льду", "en": "Over the ice"}, "cargo": 0, "loss": 15, "delay": -35},
        {"text": {"ru": "Вдоль берега", "en": "Along the shore"}, "cargo": 5, "loss": 0, "delay": 30},
        {"text": {"ru": "Порыбачить у полыньи", "en": "Fish by an ice hole"}, "cargo": 20, "loss": 0, "delay": 45},
     )},
    {"id": "trader", "icon": "🧙", "text": {
        "ru": "Странствующий торговец предлагает «очень редкую» карту.",
        "en": "A wandering trader offers a 'very rare' map."},
     "options": (
        {"text": {"ru": "Купить карту", "en": "Buy the map"}, "cargo": -10, "loss": 0, "delay": -45},
        {"text": {"ru": "Поторговаться", "en": "Haggle"}, "cargo": 10, "loss": 0, "delay": 20},
        {"text": {"ru": "Вежливо отказаться", "en": "Politely decline"}, "cargo": 0, "loss": 0, "delay": 0},
     )},
)
EVENTS_BY_ID = {e["id"]: e for e in EVENTS}


def event_text(value: dict, lang: str) -> str:
    return value.get(lang) or value.get("en") or next(iter(value.values()))


def event_for(expedition_id: int, fork_no: int) -> dict:
    """Событие развилки детерминировано: у отряда события не повторяются, у разных отрядов — разные."""
    import zlib
    base = zlib.crc32(f"exp{expedition_id}".encode()) % len(EVENTS)
    step = 5 if len(EVENTS) % 5 else 7   # шаг, взаимно простой с числом событий, — без повторов подряд
    return EVENTS[(base + (fork_no - 1) * step) % len(EVENTS)]
