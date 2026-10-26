"""
🏷 Названия-заготовки для битв, акций и экспедиций (решение владельца 26.10): «прилагательное + существительное +
число» — например «Легендарная равнина 7». Владелец выбирает слова в пульте, игрок видит название на своём языке.

На всех 14 языках учтены род и порядок слов: прилагательное согласуется с родом существительного (ru, pl, de, es,
fr, it, pt, ar), стоит после существительного там, где так принято (es, fr, it, pt, id, ar), или перед ним
(«Gran», «Grande», «Grand» — pre). Где согласование неудобно, выбрана неизменяемая форма («de glace», «हिम»).
Шаблон хранится в title_tpl ({"a": прилагательное, "n": существительное, "num": число}); в title — русская
версия (для пульта и как запасной вариант). 10 прилагательных × 12 существительных = 120 названий × любое число.
"""
from __future__ import annotations

LANGS = ("ru", "en", "uz", "es", "fr", "pt", "de", "it", "pl", "id", "zh", "hi", "ar", "bn")
# Порядок слов: прилагательное после существительного
NOUN_FIRST = {"es", "fr", "pt", "it", "id", "ar"}
TITLE_NUM_MAX = 9999

# Существительное: на каждом языке (слово, род). Род: m / f / n (там, где он есть), иначе "".
NOUNS: dict[str, dict[str, tuple[str, str]]] = {
    "plain": {"ru": ("равнина", "f"), "en": ("Plain", ""), "uz": ("tekislik", ""), "es": ("llanura", "f"),
              "fr": ("plaine", "f"), "pt": ("planície", "f"), "de": ("Ebene", "f"), "it": ("pianura", "f"),
              "pl": ("równina", "f"), "id": ("Dataran", ""), "zh": ("平原", ""), "hi": ("मैदान", ""),
              "ar": ("سهل", "m"), "bn": ("প্রান্তর", "")},
    "volcano": {"ru": ("вулкан", "m"), "en": ("Volcano", ""), "uz": ("vulqon", ""), "es": ("volcán", "m"),
                "fr": ("volcan", "m"), "pt": ("vulcão", "m"), "de": ("Vulkan", "m"), "it": ("vulcano", "m"),
                "pl": ("wulkan", "m"), "id": ("Gunung Api", ""), "zh": ("火山", ""), "hi": ("ज्वालामुखी", ""),
                "ar": ("بركان", "m"), "bn": ("আগ্নেয়গিরি", "")},
    "citadel": {"ru": ("цитадель", "f"), "en": ("Citadel", ""), "uz": ("qal'a", ""), "es": ("ciudadela", "f"),
                "fr": ("citadelle", "f"), "pt": ("cidadela", "f"), "de": ("Zitadelle", "f"), "it": ("cittadella", "f"),
                "pl": ("cytadela", "f"), "id": ("Kastil", ""), "zh": ("城堡", ""), "hi": ("गढ़", ""),
                "ar": ("قلعة", "f"), "bn": ("দুর্গ", "")},
    "island": {"ru": ("остров", "m"), "en": ("Island", ""), "uz": ("orol", ""), "es": ("isla", "f"),
               "fr": ("île", "f"), "pt": ("ilha", "f"), "de": ("Insel", "f"), "it": ("isola", "f"),
               "pl": ("wyspa", "f"), "id": ("Pulau", ""), "zh": ("岛", ""), "hi": ("द्वीप", ""),
               "ar": ("جزيرة", "f"), "bn": ("দ্বীপ", "")},
    "canyon": {"ru": ("каньон", "m"), "en": ("Canyon", ""), "uz": ("kanyon", ""), "es": ("cañón", "m"),
               "fr": ("canyon", "m"), "pt": ("cânion", "m"), "de": ("Canyon", "m"), "it": ("canyon", "m"),
               "pl": ("kanion", "m"), "id": ("Ngarai", ""), "zh": ("峡谷", ""), "hi": ("कैन्यन", ""),
               "ar": ("أخدود", "m"), "bn": ("গিরিখাত", "")},
    "desert": {"ru": ("пустыня", "f"), "en": ("Desert", ""), "uz": ("cho'l", ""), "es": ("desierto", "m"),
               "fr": ("désert", "m"), "pt": ("deserto", "m"), "de": ("Wüste", "f"), "it": ("deserto", "m"),
               "pl": ("pustynia", "f"), "id": ("Gurun", ""), "zh": ("沙漠", ""), "hi": ("रेगिस्तान", ""),
               "ar": ("صحراء", "f"), "bn": ("মরুভূমি", "")},
    "valley": {"ru": ("долина", "f"), "en": ("Valley", ""), "uz": ("vodiy", ""), "es": ("valle", "m"),
               "fr": ("vallée", "f"), "pt": ("vale", "m"), "de": ("Tal", "n"), "it": ("valle", "f"),
               "pl": ("dolina", "f"), "id": ("Lembah", ""), "zh": ("山谷", ""), "hi": ("घाटी", ""),
               "ar": ("وادي", "m"), "bn": ("উপত্যকা", "")},
    "fortress": {"ru": ("крепость", "f"), "en": ("Fortress", ""), "uz": ("qo'rg'on", ""), "es": ("fortaleza", "f"),
                 "fr": ("forteresse", "f"), "pt": ("fortaleza", "f"), "de": ("Festung", "f"), "it": ("fortezza", "f"),
                 "pl": ("twierdza", "f"), "id": ("Benteng", ""), "zh": ("要塞", ""), "hi": ("क़िला", ""),
                 "ar": ("حصن", "m"), "bn": ("কেল্লা", "")},
    "sea": {"ru": ("море", "n"), "en": ("Sea", ""), "uz": ("dengiz", ""), "es": ("mar", "m"),
            "fr": ("mer", "f"), "pt": ("mar", "m"), "de": ("Meer", "n"), "it": ("mare", "m"),
            "pl": ("morze", "n"), "id": ("Laut", ""), "zh": ("海", ""), "hi": ("सागर", ""),
            "ar": ("بحر", "m"), "bn": ("সমুদ্র", "")},
    "cup": {"ru": ("кубок", "m"), "en": ("Cup", ""), "uz": ("kubok", ""), "es": ("copa", "f"),
            "fr": ("coupe", "f"), "pt": ("taça", "f"), "de": ("Pokal", "m"), "it": ("coppa", "f"),
            "pl": ("puchar", "m"), "id": ("Piala", ""), "zh": ("杯", ""), "hi": ("कप", ""),
            "ar": ("كأس", "f"), "bn": ("কাপ", "")},
    "tournament": {"ru": ("турнир", "m"), "en": ("Tournament", ""), "uz": ("turnir", ""), "es": ("torneo", "m"),
                   "fr": ("tournoi", "m"), "pt": ("torneio", "m"), "de": ("Turnier", "n"), "it": ("torneo", "m"),
                   "pl": ("turniej", "m"), "id": ("Turnamen", ""), "zh": ("锦标赛", ""), "hi": ("टूर्नामेंट", ""),
                   "ar": ("بطولة", "f"), "bn": ("টুর্নামেন্ট", "")},
    "race": {"ru": ("забег", "m"), "en": ("Race", ""), "uz": ("poyga", ""), "es": ("carrera", "f"),
             "fr": ("course", "f"), "pt": ("corrida", "f"), "de": ("Rennen", "n"), "it": ("corsa", "f"),
             "pl": ("wyścig", "m"), "id": ("Balapan", ""), "zh": ("竞速赛", ""), "hi": ("दौड़", ""),
             "ar": ("سباق", "m"), "bn": ("দৌড়", "")},
}

# Прилагательное: на каждом языке формы по родам {"m","f","n"} или одна неизменяемая "*";
# "pre" — стоит ПЕРЕД существительным даже в языках с обратным порядком («Gran», «Grande»).
ADJS: dict[str, dict[str, dict[str, str]]] = {
    "legendary": {"ru": {"m": "Легендарный", "f": "Легендарная", "n": "Легендарное"}, "en": {"*": "Legendary"},
                  "uz": {"*": "Afsonaviy"}, "es": {"m": "legendario", "f": "legendaria"},
                  "fr": {"*": "légendaire"}, "pt": {"m": "lendário", "f": "lendária"},
                  "de": {"m": "Legendärer", "f": "Legendäre", "n": "Legendäres"},
                  "it": {"m": "leggendario", "f": "leggendaria"},
                  "pl": {"m": "Legendarny", "f": "Legendarna", "n": "Legendarne"}, "id": {"*": "Legendaris"},
                  "zh": {"*": "传奇"}, "hi": {"*": "पौराणिक"}, "ar": {"m": "أسطوري", "f": "أسطورية"},
                  "bn": {"*": "কিংবদন্তি"}},
    "golden": {"ru": {"m": "Золотой", "f": "Золотая", "n": "Золотое"}, "en": {"*": "Golden"}, "uz": {"*": "Oltin"},
               "es": {"m": "dorado", "f": "dorada"}, "fr": {"m": "doré", "f": "dorée"},
               "pt": {"m": "dourado", "f": "dourada"}, "de": {"m": "Goldener", "f": "Goldene", "n": "Goldenes"},
               "it": {"m": "dorato", "f": "dorata"}, "pl": {"m": "Złoty", "f": "Złota", "n": "Złote"},
               "id": {"*": "Emas"}, "zh": {"*": "黄金"}, "hi": {"*": "स्वर्ण"},
               "ar": {"m": "ذهبي", "f": "ذهبية"}, "bn": {"*": "সোনালি"}},
    "ice": {"ru": {"m": "Ледяной", "f": "Ледяная", "n": "Ледяное"}, "en": {"*": "Ice"}, "uz": {"*": "Muzli"},
            "es": {"m": "helado", "f": "helada"}, "fr": {"*": "de glace"}, "pt": {"*": "de gelo"},
            "de": {"m": "Eisiger", "f": "Eisige", "n": "Eisiges"}, "it": {"*": "di ghiaccio"},
            "pl": {"m": "Lodowy", "f": "Lodowa", "n": "Lodowe"}, "id": {"*": "Es"}, "zh": {"*": "冰封"},
            "hi": {"*": "हिम"}, "ar": {"m": "جليدي", "f": "جليدية"}, "bn": {"*": "বরফের"}},
    "fiery": {"ru": {"m": "Огненный", "f": "Огненная", "n": "Огненное"}, "en": {"*": "Fiery"}, "uz": {"*": "Olovli"},
              "es": {"*": "de fuego"}, "fr": {"*": "de feu"}, "pt": {"*": "de fogo"},
              "de": {"m": "Feuriger", "f": "Feurige", "n": "Feuriges"}, "it": {"*": "di fuoco"},
              "pl": {"m": "Ognisty", "f": "Ognista", "n": "Ogniste"}, "id": {"*": "Membara"}, "zh": {"*": "烈焰"},
              "hi": {"*": "अग्नि"}, "ar": {"m": "ناري", "f": "نارية"}, "bn": {"*": "অগ্নি"}},
    "lost": {"ru": {"m": "Затерянный", "f": "Затерянная", "n": "Затерянное"}, "en": {"*": "Lost"},
             "uz": {"*": "Yo'qolgan"}, "es": {"m": "perdido", "f": "perdida"}, "fr": {"m": "perdu", "f": "perdue"},
             "pt": {"m": "perdido", "f": "perdida"}, "de": {"m": "Verlorener", "f": "Verlorene", "n": "Verlorenes"},
             "it": {"m": "perduto", "f": "perduta"}, "pl": {"m": "Zaginiony", "f": "Zaginiona", "n": "Zaginione"},
             "id": {"*": "Hilang"}, "zh": {"*": "失落"}, "hi": {"*": "लुप्त"}, "ar": {"m": "مفقود", "f": "مفقودة"},
             "bn": {"*": "হারানো"}},
    "great": {"ru": {"m": "Великий", "f": "Великая", "n": "Великое"}, "en": {"*": "Great"}, "uz": {"*": "Buyuk"},
              "es": {"*": "Gran", "pre": "1"}, "fr": {"m": "Grand", "f": "Grande", "pre": "1"},
              "pt": {"*": "Grande", "pre": "1"}, "de": {"m": "Großer", "f": "Große", "n": "Großes"},
              "it": {"*": "Grande", "pre": "1"}, "pl": {"m": "Wielki", "f": "Wielka", "n": "Wielkie"},
              "id": {"*": "Agung"}, "zh": {"*": "大"}, "hi": {"*": "महान"}, "ar": {"m": "عظيم", "f": "عظيمة"},
              "bn": {"*": "মহান"}},
    "secret": {"ru": {"m": "Тайный", "f": "Тайная", "n": "Тайное"}, "en": {"*": "Secret"}, "uz": {"*": "Sirli"},
               "es": {"m": "secreto", "f": "secreta"}, "fr": {"m": "secret", "f": "secrète"},
               "pt": {"m": "secreto", "f": "secreta"}, "de": {"m": "Geheimer", "f": "Geheime", "n": "Geheimes"},
               "it": {"m": "segreto", "f": "segreta"},
               "pl": {"m": "Tajemniczy", "f": "Tajemnicza", "n": "Tajemnicze"}, "id": {"*": "Rahasia"},
               "zh": {"*": "神秘"}, "hi": {"*": "रहस्यमय"}, "ar": {"m": "سري", "f": "سرية"}, "bn": {"*": "রহস্যময়"}},
    "wild": {"ru": {"m": "Дикий", "f": "Дикая", "n": "Дикое"}, "en": {"*": "Wild"}, "uz": {"*": "Yovvoyi"},
             "es": {"*": "salvaje"}, "fr": {"*": "sauvage"}, "pt": {"*": "selvagem"},
             "de": {"m": "Wilder", "f": "Wilde", "n": "Wildes"}, "it": {"m": "selvaggio", "f": "selvaggia"},
             "pl": {"m": "Dziki", "f": "Dzika", "n": "Dzikie"}, "id": {"*": "Liar"}, "zh": {"*": "狂野"},
             "hi": {"*": "जंगली"}, "ar": {"m": "بري", "f": "برية"}, "bn": {"*": "বুনো"}},
    "stellar": {"ru": {"m": "Звёздный", "f": "Звёздная", "n": "Звёздное"}, "en": {"*": "Stellar"},
                "uz": {"*": "Yulduzli"}, "es": {"*": "estelar"}, "fr": {"*": "stellaire"}, "pt": {"*": "estelar"},
                "de": {"m": "Himmlischer", "f": "Himmlische", "n": "Himmlisches"}, "it": {"*": "stellare"},
                "pl": {"m": "Gwiezdny", "f": "Gwiezdna", "n": "Gwiezdne"}, "id": {"*": "Bintang"},
                "zh": {"*": "星辰"}, "hi": {"*": "तारकीय"}, "ar": {"m": "نجمي", "f": "نجمية"}, "bn": {"*": "নক্ষত্র"}},
    "steel": {"ru": {"m": "Стальной", "f": "Стальная", "n": "Стальное"}, "en": {"*": "Steel"}, "uz": {"*": "Po'lat"},
              "es": {"*": "de acero"}, "fr": {"*": "d'acier"}, "pt": {"*": "de aço"},
              "de": {"m": "Stählerner", "f": "Stählerne", "n": "Stählernes"}, "it": {"*": "d'acciaio"},
              "pl": {"m": "Stalowy", "f": "Stalowa", "n": "Stalowe"}, "id": {"*": "Baja"}, "zh": {"*": "钢铁"},
              "hi": {"*": "फ़ौलादी"}, "ar": {"m": "فولاذي", "f": "فولاذية"}, "bn": {"*": "ইস্পাতের"}},
}


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def build_title(lang: str, adj: str, noun: str, num: int | None = None) -> str:
    """Название на языке lang (неизвестный язык — английский). KeyError — нет такого слова."""
    lang = lang if lang in LANGS else "en"
    word, gender = NOUNS[noun][lang]
    forms = ADJS[adj][lang]
    a = forms.get("*") or forms.get(gender) or forms.get("m")
    if lang == "zh":
        text = a + word
    elif lang in NOUN_FIRST and not forms.get("pre"):
        text = _cap(word) + " " + a
    else:
        text = a + " " + word
    if lang == "id":
        text = " ".join(_cap(w) for w in text.split(" "))
    text = _cap(text)
    return f"{text} {num}" if num else text


def normalize_tpl(raw) -> dict | None:
    """Шаблон из пульта: {"a", "n", "num"} — или None, если слова не из списка."""
    if not isinstance(raw, dict) or raw.get("a") not in ADJS or raw.get("n") not in NOUNS:
        return None
    try:
        num = int(raw.get("num") or 0)
    except (TypeError, ValueError):
        num = 0
    return {"a": raw["a"], "n": raw["n"], "num": num if 0 < num <= TITLE_NUM_MAX else 0}


def localized_title(title: str, tpl, lang: str) -> str:
    """Название для игрока: по шаблону на его языке, иначе — как написал владелец."""
    import json
    if isinstance(tpl, str):
        try:
            tpl = json.loads(tpl)
        except ValueError:
            tpl = None
    clean = normalize_tpl(tpl)
    return build_title(lang, clean["a"], clean["n"], clean["num"]) if clean else title


def admin_options() -> dict:
    """Для пульта: прилагательные (русские формы по родам) и существительные (русское слово и род)."""
    return {"adjs": [{"key": k, "forms": {g: v["ru"][g] for g in ("m", "f", "n")}} for k, v in ADJS.items()],
            "nouns": [{"key": k, "word": v["ru"][0], "g": v["ru"][1]} for k, v in NOUNS.items()],
            "num_max": TITLE_NUM_MAX}
