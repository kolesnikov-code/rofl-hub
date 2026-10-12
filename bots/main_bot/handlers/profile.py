import os
import logging
from datetime import datetime, timezone
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from PIL import Image, ImageDraw, ImageFont
from shared.database import db

router = Router()
logger = logging.getLogger(__name__)

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "static")
FONT_PATH = os.path.join(STATIC_DIR, "Arial.ttf")

JUNIOR_RATE_HOUR = 2
PREMIUM_RATE_HOUR = 5


# ============================================================================
# ⚙️ ТИТАНОВЫЙ ЛЕHИВЫЙ ДВИЖОК НАЧИСЛЕНИЯ (СОХРАНЯЕТ ДРОБНЫЕ СЕКУНДЫ)
# ============================================================================
async def apply_lazy_mining_earnings(user_id: int, conn) -> dict:
    """
    Ленивый часовой расчет пассивного дохода на автопилоте.
    Исключает потерю монет через сохранение остатка секунд.
    """
    user = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1 FOR UPDATE", user_id)
    if not user:
        return None

    current_time = datetime.now(timezone.utc)
    last_update = user["last_update_time"]

    # Считаем чистые секунды, прошедшие с момента последнего захода
    seconds_passed = int((current_time - last_update).total_seconds())
    if seconds_passed <= 0:
        return user

    hours_passed = seconds_passed / 3600.0
    fridge_cutlets = user["fridge_cutlets"]
    miner_junior = user["miner_junior_count"]
    miner_premium = user["miner_premium_count"]
    balance = user["balance"]

    # 1. РАСЧЕТ МЛАДШИХ МАЙНЕРОВ (Не едят, но зависят от точных часов)
    earned_junior = hours_passed * miner_junior * JUNIOR_RATE_HOUR
    total_earned = earned_junior

    # 2. РАСЧЕТ КИБЕР-БУРИЛЬЩИКОВ (1 бурильщик съедает 1 котлету за 86400 секунд)
    if miner_premium > 0 and fridge_cutlets > 0:
        cutlets_needed_per_second = miner_premium / 86400.0
        total_cutlets_needed = seconds_passed * cutlets_needed_per_second

        if fridge_cutlets >= total_cutlets_needed:
            earned_premium = hours_passed * miner_premium * PREMIUM_RATE_HOUR
            fridge_cutlets = max(0, fridge_cutlets - int(total_cutlets_needed))
        else:
            # Еда закончилась раньше, чем пользователь зашел в бота
            seconds_worked = int(fridge_cutlets / cutlets_needed_per_second)
            hours_worked = seconds_worked / 3600.0
            earned_premium = hours_worked * miner_premium * PREMIUM_RATE_HOUR
            fridge_cutlets = 0
        total_earned += earned_premium

    # Накатываем чистый заработок без обрезания копеек времени
    new_balance = balance + int(total_earned)

    await conn.execute(
        """
        UPDATE users
        SET balance          = $1,
            fridge_cutlets   = $2,
            last_update_time = $3
        WHERE user_id = $4
        """,
        new_balance, fridge_cutlets, current_time, user_id
    )
    return await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)


def generate_profile_image(user_id: int, username: str, data: dict) -> str:
    """Рендерит сочный неоновый паспорт инвентаря. Шаблоны больше не удаляются!"""
    capacity = data["fridge_capacity"]
    template_path = os.path.join(STATIC_DIR, f"fridge_{capacity}.jpg")
    if not os.path.exists(template_path):
        template_path = os.path.join(STATIC_DIR, "fridge_1.jpg")

    output_path = os.path.join(STATIC_DIR, f"user_{user_id}_profile.jpg")

    try:
        with Image.open(template_path) as img:
            draw = ImageDraw.Draw(img)
            try:
                font_id = ImageFont.truetype(FONT_PATH, 24)
                font_data = ImageFont.truetype(FONT_PATH, 20)
            except IOError:
                font_id = font_data = ImageFont.load_default()

            draw.text((50, 40), f"ID ПAСПOPТA: {user_id}", fill="#00ffff", font=font_id)
            draw.text((50, 80), f"ВОЖAК: @{username}", fill="#ffffff", font=font_data)
            draw.text((50, 150), f"💰 Бaлaнс: {data['balance']} рофлов", fill="#ffff00", font=font_id)
            draw.text((50, 200), f"🥩 В холодильнике: {data['fridge_cutlets']} / {capacity} шт.", fill="#ff00ff",
                      font=font_data)
            draw.text((50, 240), f"💼 Котлеты в инвентаре: {data['inv_cutlets']} шт.", fill="#ffffff", font=font_data)
            draw.text((50, 310), f"🤖 Млaдшие Мaйнеры: {data['miner_junior_count']} шт.", fill="#00ff00", font=font_data)
            draw.text((50, 350), f"⚡ Кибер Бурильщики: {data['miner_premium_count']} шт.", fill="#ff3300",
                      font=font_data)
            draw.text((50, 390), f"🚀 Боевой Буст: Уровень {data['boost_level']}", fill="#aa00ff", font=font_data)
            img.save(output_path, "JPEG")
            return output_path
    except Exception as e:
        logger.error(f"[PILLOW_RENDER_ERROR] Сбой рендеринга графики: {e}")
        return template_path


# ============================================================================
# 👤 ТЕКУЩИЙ ЛИЧНЫЙ КАБИНЕТ: /profile ИЛИ НАЖАТИЕ НИЖНЕЙ КНОПКИ
# ============================================================================
@router.message(Command("profile"))
@router.message(F.text == "👤 МОЙ ПРОФИЛЬ")
async def cmd_profile_stats(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user = await apply_lazy_mining_earnings(user_id, conn)
            if not user:
                await message.answer("⚠️ Профиль не найден. Прожми /start")
                return

            team_name = "Нет команды"
            if user["team_id"] is not None:
                t_row = await conn.fetchrow("SELECT team_name, max_members FROM teams WHERE team_id = $1",
                                            user["team_id"])
                if t_row:
                    status_team = "Клан" if t_row["max_members"] >= 1000 else "Команда"
                    team_name = f"{status_team} «{t_row['team_name']}»"

    user_data_dict = {
        "balance": user["balance"], "fridge_capacity": user["fridge_capacity"],
        "fridge_cutlets": user["fridge_cutlets"], "inv_cutlets": user["inv_cutlets"],
        "miner_junior_count": user["miner_junior_count"], "miner_premium_count": user["miner_premium_count"],
        "boost_level": user["boost_level"]
    }

    photo_path = generate_profile_image(user_id, username, user_data_dict)

    profile_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🚜 Моя Кибер-Ферма", callback_data="open_farm_from_profile"),
            types.InlineKeyboardButton(text="🏪 Магазин /shop", callback_data="open_shop_from_farm")
        ],
        [
            types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")
        ]
    ])

    caption_text = (
        f"📋 <b>ЛИЧНЫЙ КАБИНЕТ ИГРОКА ROFL HUB</b>\n"
        f"..................................................\n\n"
        f"🆔 Твой ID Паспорта: <code>{user_id}</code>\n"
        f"💰 Монеты сейчас: <b>{user['balance']} рофлов</b>\n"
        f"🏆 Твой статус: <b>{team_name}</b>\n\n"
        f"..................................................\n"
        f"<i>Здесь показано то, что есть у тебя прямо сейчас. Используй кнопки для перелёта в другие разделы!</i>"
    )

    photo_file = FSInputFile(photo_path)
    await message.answer_photo(photo=photo_file, caption=caption_text, reply_markup=profile_keyboard, parse_mode="HTML")

    # 🔥 Фикс: Удаляем только ПЕРСОНАЛЬНЫЙ сгенерированный jpeg, исходные fridge_N.jpg не трогаем!
    try:
        if os.path.exists(photo_path) and f"user_{user_id}" in photo_path:
            os.remove(photo_path)
    except Exception:
        pass


# ============================================================================
# 📊 ЧИСТАЯ СТАТИСТИКА ДОСТИЖЕНИЙ ЗА 30 ДНЕЙ: /my_stats
# ============================================================================
@router.message(Command("my_stats"))
async def cmd_historical_stats(message: types.Message):
    user_id = message.from_user.id

    async with db.pool.acquire() as conn:
        g_row = await conn.fetchrow("SELECT games_played, games_won FROM game_stats WHERE user_id = $1", user_id)
        ref_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1", user_id)

    played = g_row["games_played"] if g_row else 0
    won = g_row["games_won"] if g_row else 0

    stats_text = (
        f"📊 <b>ИГРОВАЯ СТАТИСТИКА ДОСТИЖЕНИЙ (30 ДНЕЙ)</b>\n"
        f"..................................................\n\n"
        f"🎮 Проведено раундов в дуэлях: <b>{played} игр</b>\n"
        f"🏆 Одержано побед над соперниками: <code>{won} раз</code>\n"
        f"👥 Приглашено активных друзей: <b>{ref_count} чел.</b>\n\n"
        f"..................................................\n"
        f"<i>Статистика хранит твои исторические заслуги и прошлые достижения, даже если выигранные монеты уже были потрачены в маркете!</i>"
    )

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💿 Главное Меню /menu", callback_data="refresh_main_menu")]
    ])
    await message.answer(stats_text, reply_markup=kb, parse_mode="HTML")
