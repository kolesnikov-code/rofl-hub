import logging
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from shared.database import db  # Твой официальный экземпляр класса БД
from shared.strings import get_plural_cutlets

router = Router()
logger = logging.getLogger(__name__)


# ================================================================
# ⚙️ ТИТАНОВЫЙ МЕХАНИЗМ ЗАПРАВКИ И РАСЧЁТА ФЕРМЫ
# ================================================================

@router.message(Command("load_fridge"))
async def cmd_load_fridge(message: types.Message):
    """
    КOМАНДA: /load_fridge [количество]
    Перекладывает котлеты из кармана инвентаря в Центральный Топливный Хаб.
    """
    user_id = message.from_user.id
    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        await message.answer("⚠️ Укажи количество котлет! Пример: <code>/load_fridge 5</code>", parse_mode="HTML")
        return

    want_to_load = int(args[1])
    if want_to_load <= 0:
        await message.answer("⚠️ Количество котлет должно быть больше нуля!")
        return

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            # Блокируем строку юзера (защита от дюпа и параллельных кликов)
            user = await conn.fetchrow(
                "SELECT inv_cutlets, fridge_cutlets, fridge_capacity FROM users WHERE user_id = $1 FOR UPDATE",
                user_id
            )
            if not user:
                await message.answer("⚠️ Профиль не найден. Нажми /start")
                return

            inv_cutlets = user["inv_cutlets"]  # Котлеты в кармане (незаправленные)
            fridge_cutlets = user["fridge_cutlets"]  # Котлеты внутри хаба
            fridge_capacity = user["fridge_capacity"]  # Общий объём хаба (5, 10, 50, 100)

            if inv_cutlets == 0:
                await message.answer("❌ У тебя в кармане нет кибер-котлет! Купи их в магазине /shop")
                return

            # Вычисляем, сколько реально можно закинуть с учётом лимитов склада
            available_space = fridge_capacity - fridge_cutlets
            if available_space <= 0:
                await message.answer("📦 Твой Центральный Холодильник забит до отказа! Расширь его в /shop")
                return

            actual_load = min(want_to_load, inv_cutlets, available_space)

            # Перезаписываем данные в PostgreSQL на Railway
            new_inv = inv_cutlets - actual_load
            new_fridge = fridge_cutlets + actual_load

            await conn.execute(
                """
                UPDATE users
                SET inv_cutlets    = $1,
                    fridge_cutlets = $2
                WHERE user_id = $3
                """,
                new_inv, new_fridge, user_id
            )

            logger.info(f"🥩 ХАБ ЗАПРАВЛЕН: Юзер {user_id} переложил {actual_load} котлет в холодильник.")

            await message.answer(
                f"📦 <b>ЦЕНТРАЛЬНЫЙ ТОПЛИВНЫЙ ХАБ ОБНОВЛЕН</b>\n"
                f"..................................................\n\n"
                f"✅ Успешно заправлено: <b>{actual_load} шт.</b>\n"
                f"🥩 В кармане осталось: <code>{new_inv} шт.</code>\n"
                f"🔋 Запас в холодильнике: <b>{new_fridge} / {fridge_capacity} котлет</b>\n\n"
                f"..................................................\n"
                f"🤖 <i>Теперь твои Кибер-Бурильщики сыты и готовы качать кэш на автопилоте!</i>",
                parse_mode="HTML"
            )


@router.message(Command("run_farm"))
async def cmd_run_farm(message: types.Message):
    """
    КОМАНДА: /run_farm
    Запускает суточный цикл кормления роботов. Списывает целые котлеты из хаба
    и продлевает работу Бурильщиков ровно на 24 часа.
    """
    user_id = message.from_user.id
    current_time = datetime.now()

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await conn.fetchrow(
                """
                SELECT fridge_cutlets, miner_premium_count, last_update_time
                FROM users
                WHERE user_id = $1 FOR UPDATE
                """,
                user_id
            )
            if not user:
                return

            fridge_cutlets = user["fridge_cutlets"]
            miner_premium_count = user["miner_premium_count"]

            if miner_premium_count == 0:
                await message.answer("⚠️ У тебя нет активных Кибер-Бурильщиков! Кормить некого. Купи их в /shop")
                return

            # Твоё жёсткое правило: 1 робот = 1 целая котлета в сутки!
            need_cutlets = miner_premium_count

            if fridge_cutlets < need_cutlets:
                await message.answer(
                    f"❌ <b>ОСТАНОВКА ИТ-ЗАВОДА!</b>\n\n"
                    f"У тебя {miner_premium_count} Кибер-Бурильщиков, им нужно ровно {need_cutlets} котлет на сутки! "
                    f"А в твоем хабе лежит всего <b>{fridge_cutlets} шт.</b>\n\n"
                    f"🪓 Часть роботов проголодалась и отключилась! "
                    f"Срочно заправь холодильник командой <code>/load_fridge</code> или докупи еды в /shop!",
                    parse_mode="HTML"
                )
                return

            # Списываем строго ЦЕЛЫЕ котлеты по числу роботов
            new_fridge = fridge_cutlets - need_cutlets

            # Обновляем таймштамп старта работы на текущую секунду
            await conn.execute(
                """
                UPDATE users
                SET fridge_cutlets   = $1,
                    last_update_time = $2
                WHERE user_id = $3
                """,
                new_fridge, current_time, user_id
            )

            await message.answer(
                f"⚡ <b>ИТ-ЗАВОД ROFL HUB НАБИРАЕТ ОБОРОТЫ!</b>\n"
                f"..................................................\n\n"
                f"🥩 Списано из хаба: <b>{need_cutlets} целых котлет</b>.\n"
                f"🤖 Твоя батарея из <b>{miner_premium_count} Бурильщиков</b> сыта и заправлена на 24 часа вперёд!\n"
                f"📦 Остаток в холодильнике: <code>{new_fridge} шт.</code>\n\n"
                f"..................................................\n"
                f"📈 <i>Станок круглосуточно выкачивает монеты из рудников. Счётчик баланса запущен!</i>",
                parse_mode="HTML"
            )
