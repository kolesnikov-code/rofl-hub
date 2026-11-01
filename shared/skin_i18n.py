"""
✨ Названия скинов на 12 языках паков (ru/en лежат прямо в shared/skins.SKINS и season_pass.PASS_THEMES).

Название собирается из ПОНЯТИЯ (WORDS) и ШАБЛОНА цели (TPL: рамка / маркер / сумка / костюм / титул), поэтому
новый скин постоянной коллекции = строка в STATIC + понятие в WORDS каждого языка; скины пропуска сезона
собираются из темы месяца (theme1…theme12). Нет перевода — английское имя (бот не падает).
"""
from __future__ import annotations

# скин → (шаблон цели или None — название без приставки, понятие)
STATIC: dict[str, tuple[str | None, str]] = {
    "aur_suit": (None, "aurora_lights"), "aur_frame": ("frame", "aurora_lights"), "aur_title": (None, "northern_light"),
    "aur_marker": ("marker", "aurora"), "aur_bag": ("bag", "aurora_lights"), "aur_keeper": (None, "keeper"),
    "myth_polar": (None, "polar_crown"), "neo_frame": ("frame", "neon"), "carbon_suit": (None, "carbon"),
    "gold_suit": (None, "gold"), "chrome_frame": ("frame", "chrome"), "wander_title": (None, "wanderer"),
    "rocket_marker": ("marker", "rocket"), "carbon_bag": ("bag", "carbon"),
}

_CONCEPTS = ("aurora_lights", "northern_light", "aurora", "keeper", "polar_crown", "neon", "carbon", "gold", "chrome",
             "wanderer", "rocket")


def _w(concepts: tuple, themes: tuple) -> dict[str, str]:
    assert len(concepts) == len(_CONCEPTS) and len(themes) == 12
    return {**dict(zip(_CONCEPTS, concepts)), **{f"theme{i + 1}": t for i, t in enumerate(themes)}}


WORDS: dict[str, dict[str, str]] = {
    "uz": _w(("Qutb shafag'i", "Shimoliy nur", "Shafaq", "Shafaq posboni", "Qutb toji", "Neon", "Karbon", "Oltin standart",
              "Xrom", "Neon sayyoh", "Raketa"),
             ("Muz patruli", "Qirmizi bo'ron", "Ilk iliqlik", "Yulduzli parvoz", "May momaqaldirog'i", "Sahro shamoli",
              "Chuqurlik", "Neon tun", "Kiber-hosil", "Qovoq nosozligi", "Qutb navbatchiligi", "Gulchambar")),
    "es": _w(("Aurora boreal", "Luz del norte", "Aurora", "Guardián de la aurora", "Corona polar", "Neón", "Carbono",
              "Patrón oro", "Cromo", "Errante de neón", "Cohete"),
             ("Patrulla de hielo", "Ventisca carmesí", "Primer deshielo", "Ruta estelar", "Trueno de mayo",
              "Viento del desierto", "Las profundidades", "Noche de neón", "Cosecha cibernética", "Fallo de calabaza",
              "Guardia polar", "Guirnalda")),
    "fr": _w(("Aurore boréale", "Lumière du Nord", "Aurore", "Gardien des aurores", "Couronne polaire", "Néon", "Carbone",
              "Étalon-or", "Chrome", "Vagabond néon", "Fusée"),
             ("Patrouille de glace", "Blizzard écarlate", "Premier dégel", "Course stellaire", "Tonnerre de mai",
              "Vent du désert", "Les abysses", "Nuit néon", "Moisson cyber", "Bug citrouille", "Veille polaire", "Guirlande")),
    "pt": _w(("Aurora boreal", "Luz do Norte", "Aurora", "Guardião da aurora", "Coroa polar", "Neon", "Carbono",
              "Padrão ouro", "Cromo", "Andarilho neon", "Foguete"),
             ("Patrulha de gelo", "Nevasca carmesim", "Primeiro degelo", "Rota estelar", "Trovão de maio",
              "Vento do deserto", "As profundezas", "Noite neon", "Colheita cibernética", "Falha de abóbora",
              "Vigília polar", "Guirlanda")),
    "de": _w(("Nordlicht", "Licht des Nordens", "Polarlicht", "Hüter des Nordlichts", "Polarkrone", "Neon", "Carbon",
              "Goldstandard", "Chrom", "Neon-Wanderer", "Rakete"),
             ("Eispatrouille", "Purpurner Schneesturm", "Erstes Tauwetter", "Sternenflug", "Maigewitter", "Wüstenwind",
              "Die Tiefe", "Neonnacht", "Cyber-Ernte", "Kürbis-Glitch", "Polarwache", "Girlande")),
    "it": _w(("Aurora boreale", "Luce del Nord", "Aurora", "Custode dell'aurora", "Corona polare", "Neon", "Carbonio",
              "Standard aureo", "Cromo", "Viandante al neon", "Razzo"),
             ("Pattuglia di ghiaccio", "Bufera cremisi", "Primo disgelo", "Rotta stellare", "Tuono di maggio",
              "Vento del deserto", "Gli abissi", "Notte al neon", "Raccolto cyber", "Glitch di zucca", "Vedetta polare",
              "Ghirlanda")),
    "pl": _w(("Zorza polarna", "Światło Północy", "Zorza", "Strażnik zorzy", "Korona polarna", "Neon", "Karbon",
              "Złoty standard", "Chrom", "Neonowy wędrowiec", "Rakieta"),
             ("Lodowy patrol", "Szkarłatna zamieć", "Pierwsza odwilż", "Gwiezdny rejs", "Majowa burza", "Wiatr pustyni",
              "Głębia", "Neonowa noc", "Cyberżniwa", "Dyniowy glitch", "Polarna warta", "Girlanda")),
    "id": _w(("Aurora Utara", "Cahaya Utara", "Aurora", "Penjaga Aurora", "Mahkota Kutub", "Neon", "Karbon", "Standar Emas",
              "Krom", "Pengembara Neon", "Roket"),
             ("Patroli Es", "Badai Salju Merah", "Pencairan Pertama", "Perjalanan Bintang", "Guntur Mei", "Angin Gurun",
              "Kedalaman", "Malam Neon", "Panen Siber", "Glitch Labu", "Jaga Kutub", "Untaian Hiasan")),
    "zh": _w(("北极光", "北方之光", "极光", "极光守护者", "极地王冠", "霓虹", "碳纤维", "黄金标准", "铬", "霓虹旅人", "火箭"),
             ("冰霜巡逻", "绯红暴雪", "初融", "星际航程", "五月惊雷", "沙漠之风", "深渊", "霓虹之夜", "赛博丰收", "南瓜故障",
              "极地守望", "彩灯花环")),
    "hi": _w(("उत्तरी ध्रुवीय ज्योति", "उत्तर का प्रकाश", "ध्रुवीय ज्योति", "ज्योति का रक्षक", "ध्रुवीय मुकुट", "नियॉन", "कार्बन",
              "स्वर्ण मानक", "क्रोम", "नियॉन यात्री", "रॉकेट"),
             ("बर्फ़ीली गश्त", "लाल बर्फ़ीला तूफ़ान", "पहली पिघलन", "तारों की उड़ान", "मई की गरज", "रेगिस्तानी हवा", "गहराई",
              "नियॉन रात", "साइबर फ़सल", "कद्दू गड़बड़ी", "ध्रुवीय पहरा", "माला")),
    "bn": _w(("উত্তরের মেরুজ্যোতি", "উত্তরের আলো", "মেরুপ্রভা", "মেরুজ্যোতির রক্ষক", "মেরু মুকুট", "নিয়ন", "কার্বন", "স্বর্ণমান",
              "ক্রোম", "নিয়ন পথিক", "রকেট"),
             ("বরফ টহল", "লাল তুষারঝড়", "প্রথম বরফগলা", "তারার যাত্রা", "মে মাসের বজ্র", "মরুভূমির হাওয়া", "গভীরতা",
              "নিয়ন রাত", "সাইবার ফসল", "কুমড়ো গোলযোগ", "মেরু পাহারা", "মালা")),
    "ar": _w(("الشفق القطبي", "نور الشمال", "الشفق", "حارس الشفق", "التاج القطبي", "نيون", "كربون", "المعيار الذهبي",
              "كروم", "جوّال النيون", "صاروخ"),
             ("دورية الجليد", "العاصفة القرمزية", "أول ذوبان", "رحلة النجوم", "رعد مايو", "رياح الصحراء", "الأعماق",
              "ليلة النيون", "الحصاد السيبراني", "خلل اليقطين", "الحراسة القطبية", "إكليل")),
}

TPL: dict[str, dict[str, str]] = {
    "uz": {"frame": "«{t}» ramkasi", "marker": "«{t}» markeri", "bag": "«{t}» sumkasi", "suit": "«{t}» kostyumi",
           "title": "«{t}» unvoni"},
    "es": {"frame": "Marco «{t}»", "marker": "Marcador «{t}»", "bag": "Bolsa «{t}»", "suit": "Traje «{t}»",
           "title": "Título «{t}»"},
    "fr": {"frame": "Cadre « {t} »", "marker": "Marqueur « {t} »", "bag": "Sac « {t} »", "suit": "Tenue « {t} »",
           "title": "Titre « {t} »"},
    "pt": {"frame": "Moldura «{t}»", "marker": "Marcador «{t}»", "bag": "Bolsa «{t}»", "suit": "Traje «{t}»",
           "title": "Título «{t}»"},
    "de": {"frame": "Rahmen „{t}“", "marker": "Marker „{t}“", "bag": "Tasche „{t}“", "suit": "Anzug „{t}“",
           "title": "Titel „{t}“"},
    "it": {"frame": "Cornice «{t}»", "marker": "Segnaposto «{t}»", "bag": "Borsa «{t}»", "suit": "Tuta «{t}»",
           "title": "Titolo «{t}»"},
    "pl": {"frame": "Ramka „{t}”", "marker": "Znacznik „{t}”", "bag": "Torba „{t}”", "suit": "Strój „{t}”",
           "title": "Tytuł „{t}”"},
    "id": {"frame": "Bingkai “{t}”", "marker": "Penanda “{t}”", "bag": "Tas “{t}”", "suit": "Kostum “{t}”",
           "title": "Gelar “{t}”"},
    "zh": {"frame": "“{t}”边框", "marker": "“{t}”标记", "bag": "“{t}”背包", "suit": "“{t}”套装", "title": "“{t}”称号"},
    "hi": {"frame": "“{t}” फ़्रेम", "marker": "“{t}” मार्कर", "bag": "“{t}” बैग", "suit": "“{t}” सूट", "title": "“{t}” उपाधि"},
    "bn": {"frame": "“{t}” ফ্রেম", "marker": "“{t}” মার্কার", "bag": "“{t}” ব্যাগ", "suit": "“{t}” পোশাক", "title": "“{t}” উপাধি"},
    "ar": {"frame": "إطار «{t}»", "marker": "علامة «{t}»", "bag": "حقيبة «{t}»", "suit": "بدلة «{t}»", "title": "لقب «{t}»"},
}


def theme_name(month: int, lang: str) -> str | None:
    """Тема пропуска месяца на языке пака (None — языка нет в паках: ru/en берутся из PASS_THEMES)."""
    return WORDS.get(lang, {}).get(f"theme{month}")


def pack_name(skin_id: str, skin: dict, lang: str) -> str | None:
    """Название скина на языке пака; None — перевода нет (вызывающий берёт английское)."""
    words, tpl = WORDS.get(lang), TPL.get(lang)
    if not words or not tpl:
        return None
    if skin_id in STATIC:
        target, concept = STATIC[skin_id]
        word = words[concept]
        return tpl[target].format(t=word) if target else word
    season = skin.get("pass")
    if season:
        theme = words[f"theme{int(season[5:7])}"]
        return tpl[skin["target"]].format(t=theme) + f" · {season[5:7]}.{season[:4]}"
    return None


def pack_text(skin_id: str, skin: dict, lang: str) -> str | None:
    """Надпись титула (то, что видно рядом с именем) на языке пака."""
    words = WORDS.get(lang)
    if not words or skin.get("target") != "title":
        return None
    if skin_id in STATIC:
        return words[STATIC[skin_id][1]]
    if skin.get("pass"):
        return words[f"theme{int(skin['pass'][5:7])}"]
    return None
