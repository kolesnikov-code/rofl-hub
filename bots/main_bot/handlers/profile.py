import html
import os
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from PIL import Image, ImageDraw, ImageFont
from shared.database import db
from shared.economy import quiz_answers_required, quiz_level_reward, utcnow
from shared.farm_logic import apply_lazy_farm, farm_counts
from shared.locales import btn_variants, t
from shared.ranks import rank_label
from shared.resources import RESOURCE_ICONS, get_resources

router = Router()
logger = logging.getLogger(__name__)

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "static")
FONT_CANDIDATES = [
    os.path.join(STATIC_DIR, "DejaVuSans.ttf"),
    os.path.join(STATIC_DIR, "Arial.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)

# Ленивый движок начисления переехал в shared/farm_logic.apply_lazy_farm:
# роботы живут в таблице miners, топливо списывается целыми циклами 24ч,
# начисления идут через ledger без потери «копеек времени».


# DejaVu/Arial не содержат глифов CJK, деванагари, бенгальского и не умеют RTL-шейпинг —
# подписи на картинке для этих языков рисуем по-английски (тексты бота остаются на языке игрока)
IMG_FALLBACK_TO_EN_LANGS = {"zh", "hi", "bn", "ar"}


def generate_profile_image(user_id: int, username: str, data: dict, lang: str = "ru") -> str:
    """Рендерит сочный неоновый паспорт инвентаря. Шаблоны больше не удаляются!"""
    if lang in IMG_FALLBACK_TO_EN_LANGS:
        lang = "en"
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
            except (IOError, TypeError):
                font_id = font_data = ImageFont.load_default()

            draw.text((50, 40), t(lang, "img.passport", user_id=user_id), fill="#00ffff", font=font_id)
            draw.text((50, 80), t(lang, "img.owner", username=username), fill="#ffffff", font=font_data)
            draw.text((50, 150), t(lang, "img.balance", balance=data["balance"]), fill="#ffff00", font=font_id)
            draw.text((50, 200), t(lang, "img.fridge", fridge=data["fridge_cutlets"], capacity=capacity),
                      fill="#ff00ff", font=font_data)
            draw.text((50, 240), t(lang, "img.inv", inv=data["inv_cutlets"]), fill="#ffffff", font=font_data)
            draw.text((50, 310), t(lang, "img.junior", count=data["miner_junior_count"]),
                      fill="#00ff00", font=font_data)
            draw.text((50, 350), t(lang, "img.premium", count=data["miner_premium_count"]),
                      fill="#ff3300", font=font_data)
            img.save(output_path, "JPEG")
            return output_path
    except Exception as e:
        logger.error(f"[PILLOW_RENDER_ERROR] Сбой рендеринга графики: {e}")
        return template_path


# ============================================================================
# 👤 ТЕКУЩИЙ ЛИЧНЫЙ КАБИНЕТ: /profile ИЛИ НАЖАТИЕ НИЖНЕЙ КНОПКИ
# ============================================================================
def profile_keyboard_for(lang: str) -> types.InlineKeyboardMarkup:
    """Решение владельца 28.10: под профилем одна кнопка — «Открыть приложение» (удаление аккаунта —
    командой /delete_account в меню). Без приложения — прежние кнопки фермы, магазина и меню."""
    from bots.main_bot.webapp_links import app_button
    button = app_button(t(lang, "profile.btn_app"), "passport")
    if button is not None:
        return types.InlineKeyboardMarkup(inline_keyboard=[[button]])
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(lang, "profile.btn_farm"), callback_data="open_farm_from_profile"),
         types.InlineKeyboardButton(text=t(lang, "profile.btn_shop"), callback_data="open_shop_from_farm")],
        [types.InlineKeyboardButton(text=t(lang, "common.btn_menu"), callback_data="refresh_main_menu")],
    ])


@router.message(Command("profile"))
@router.message(F.text.in_(btn_variants("profile")))
async def cmd_profile_stats(message: types.Message, user_lang: str = "ru"):
    user_id = message.from_user.id
    username = html.escape(message.from_user.username or f"user_{user_id}")

    now = utcnow()
    async with db.pool.acquire() as conn:
        async with conn.transaction():
            user, miners = await apply_lazy_farm(conn, user_id, now)
            if not user:
                await message.answer(t(user_lang, "common.no_profile"))
                return

            team_name = t(user_lang, "profile.no_team")
            if user["team_id"] is not None:
                t_row = await conn.fetchrow("SELECT team_name, max_members FROM teams WHERE team_id = $1",
                                            user["team_id"])
                if t_row:
                    status_team = t(user_lang, "profile.clan_label") if t_row["max_members"] >= 1000 \
                        else t(user_lang, "profile.team_label")
                    team_name = f"{status_team} «{t_row['team_name']}»"

            quiz_row = await conn.fetchrow(
                "SELECT quiz_level, quiz_level_progress FROM game_stats WHERE user_id = $1", user_id)
            vip_rows = await conn.fetch(
                "SELECT alias FROM vip_aliases WHERE user_id = $1 ORDER BY created_at", user_id)

    counts = farm_counts(miners, now)
    user_data_dict = {
        "balance": user["balance"], "fridge_capacity": user["fridge_capacity"],
        "fridge_cutlets": user["fridge_cutlets"], "inv_cutlets": user["inv_cutlets"],
        "miner_junior_count": counts["junior"], "miner_premium_count": counts["premium"],
        "boost_level": user["boost_level"]
    }

    photo_path = generate_profile_image(user_id, username, user_data_dict, user_lang)

    profile_keyboard = profile_keyboard_for(user_lang)

    quiz_level = quiz_row["quiz_level"] if quiz_row else 0
    quiz_progress = quiz_row["quiz_level_progress"] if quiz_row else 0
    next_level = quiz_level + 1
    required = quiz_answers_required(next_level)

    vip_line = ""
    rank = rank_label(user_lang, user["created_at"], now)
    if rank:
        vip_line += t(user_lang, "profile.rank_line", rank=rank)
    if vip_rows:
        aliases = ", ".join(html.escape(r["alias"]) for r in vip_rows)
        vip_line += t(user_lang, "profile.vip_line", aliases=aliases)

    async with db.pool.acquire() as conn:
        stock = await get_resources(conn, user_id)
    vip_line += t(user_lang, "profile.resources_line",
                  stock="  ".join(f"{RESOURCE_ICONS[k]} {stock[k]}" for k in stock))
    caption_text = t(
        user_lang, "profile.caption",
        user_id=user_id, vip=vip_line, balance=user["balance"], team=team_name,
        level=quiz_level, next_level=next_level, left=required - quiz_progress,
        reward=quiz_level_reward(next_level),
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
async def cmd_historical_stats(message: types.Message, user_lang: str = "ru"):
    user_id = message.from_user.id

    async with db.pool.acquire() as conn:
        g_row = await conn.fetchrow(
            "SELECT games_played, games_won, quiz_level, quiz_correct_total "
            "FROM game_stats WHERE user_id = $1", user_id)
        ref_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE referred_by = $1", user_id)

    stats_text = t(
        user_lang, "profile.stats",
        level=g_row["quiz_level"] if g_row else 0,
        total=g_row["quiz_correct_total"] if g_row else 0,
        played=g_row["games_played"] if g_row else 0,
        won=g_row["games_won"] if g_row else 0,
        refs=ref_count,
    )

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=t(user_lang, "common.btn_menu"),
                                    callback_data="refresh_main_menu")]
    ])
    await message.answer(stats_text, reply_markup=kb, parse_mode="HTML")
