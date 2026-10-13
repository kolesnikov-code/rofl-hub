"""Узбекская (латиница, o'zbekcha) локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> tanga / tangalar
# Младший Майнер -> Kichik Mayner
# Кибер-Бурильщик -> Kiber-Burg'ulovchi
# кибер-котлета -> kiber-kotlet (кратко: kotlet)
# Холодильник -> Muzlatkich
# склад -> ombor
# ферма -> ferma
# Ядерный Разгон x5 -> Yadroviy Tezlatish x5
# Азотное Охлаждение +40% -> Azotli Sovutish +40%
# Мастер-дрон -> Master-Dron
# Кибер-Сейф -> Kiber-Seyf
# Мега-Клан -> Mega-Klan
# Безлимит -> Cheksiz rejim (limitlarni olib tashlash)
# дуэли -> duellar (1-на-1 -> yakkama-yakka)
# битвы -> Janglar
# квесты -> kvestlar
# уровень интеллекта -> intellekt darajasi
# ставка -> garov; банк -> bank; жест -> ishora; ничья -> durang; награда -> mukofot

BUTTONS: dict[str, str] = {
    "main_menu": "📱 BOSH MENYU",
    "profile": "👤 PROFILIM",
    "farm": "🚜 FERMAM",
    "games_zone": "🕹️ O'YIN ZONASI",
    "teams": "🏆 JAMOA VA KLANLAR",
    "shop": "🏪 DO'KON",
    "shop_cat_farm": "🚜 FERMA UCHUN",
    "shop_cat_games": "🕹️ O'YINLAR",
}

STRINGS: dict[str, str] = {
    # ---------------- общее ----------------
    "common.no_profile": "⚠️ Profil topilmadi. Ro'yxatdan o'tish uchun /start ni bos.",
    "common.btn_menu": "💿 Bosh Menyu",
    "common.blocked": "🚫 Akkauntingni ROFL HUB ma'muriyati bloklagan.",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Yana xush kelibsan, @{username}!</b>\nProgressing joyida. Navigatsiya paneli — ekranning pastida.",
    "start.btn_continue": "🛸 DAVOM ETISH",
    "start.btn_cutlet": "Kiber-kotlet nima o'zi?🥩🤔",
    "start.btn_fight": "Tezroq aytib ber — JANGGA!",
    "start.console": "🚀 <b>Boshqaruv paneli yoqildi! Ekran pastidagi tugmalardan foydalan.</b>",
    "start.intro1": (
        "👋 <b>Salom! Men — ROFL HUB BOT, ROFL HUB o'yin ekotizimining bosh boti. "
        "Bu — yangi avlod bilim-ko'ngilochar hubi!</b>\n\n"
        "<b>Bu yerda sen:</b>\n"
        "🎮 Botga va boshqa o'yinchilarga qarshi chat-bot o'yinlarini o'ynaysan\n"
        "💸 G'alabalar uchun o'yin valyutasini olasan yoki ferma ochib, uni kecha-yu kunduz qazib olasan\n"
        "🤼 Jamoa tuzib, reyting TOPiga ko'tarilasan\n"
        "🏆 Jamoani klangacha o'stirib, xalqaro reytingda kurashasan\n"
        "💰 O'z jamoang bilan birga million tangalik jekpotni qo'lga kiritasan\n"
        "👑 O'zingni yoki blogingni ilgari surish uchun ijtimoiy tarmoqlar yoki sayt bosh sahifasida e'lon sotib olasan\n\n"
        "<b>Bu chat-bot quyidagilarni biladi:</b>\n"
        "🎮 ROFL HUB'ning barcha o'yinlari, kanallari va saytlari ro'yxatini ko'rsatish\n"
        "⚡ O'yinlar, jamoa va klan janglari, yutuqlar, faollik va referallar uchun tanga hisoblash\n"
        "🔄 O'yin tangalarini boshqa ROFL HUB o'yinchisiga o'tkazish\n"
        "💎 Saytdagi e'lonlar hamda shaxslar va blogerlar uchun VIP joylarni sotish\n"
        "🚀 Tezlatgichlar, unvonlar, statuslar va yana ko'p narsalarni sotish...\n\n"
        "<i>«DAVOM ETISH» tugmasini bos, batafsil aytib beraman 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>RO'YXATDAN O'TGANING UCHUN ILK MUKOFOTLARINGNI OL!</b>\n"
        "..................................................\n"
        "💸 Senga hisoblandi: <b>{balance} tanga</b>\n"
        "🥩 Senga hisoblandi: <b>{cutlets} kiber-kotlet</b>\n"
        "..................................................\n"
        "Bu — ROFL HUB klubiga qo'shilganing uchun boshlang'ich bonusing.\n\n"
        "🔒 <i>Bonus faqat bir marta, ro'yxatdan o'tish paytida beriladi.</i>\n\n"
        "Tangalarni turli yo'llar bilan sarflash mumkin — ular hub iqtisodiyotining asosi. Ularni asrab-avayla...\n\n"
        "⁉️ <b>Lekin senda savol tug'ilgan bo'lsa kerak:</b> bu qanaqa kotlet? Uni kimga yedirish kerak?"
    ),
    "start.intro3": (
        "<b>AVVAL O'YIN TANGALARI NEGA BUNCHALIK MUHIMLIGINI TUSHUNIB OLAYLIK.</b>\n\n"
        "Tangalar — <b>ROFL HUB</b>'dagi barcha savdo, musobaqa va xaridlarning asosi. "
        "Bu — dunyoda bepul qazib olish mumkin bo'lgan deyarli yagona o'yin valyutasi!\n"
        "..................................................\n"
        "<b>Buni turli yo'llar bilan qilsa bo'ladi:</b>\n"
        "- Referal havolang orqali do'stlarni taklif qilish\n"
        "- Botga qarshi o'yinlarda g'alaba qozonish\n"
        "- Boshqa o'yinchilar bilan duellarda yutish\n"
        "- Jamoa va klan janglarida qatnashish\n"
        "- Kundalik kirish bonusi va topshiriqlarni olish\n"
        "- Tangalarni kecha-yu kunduz qazadigan robot olish (Kichik Mayner / Kiber-Burg'ulovchi)\n"
        "..................................................\n"
        "<b>Agar ikkinchi bosqich robotini (Kiber-Burg'ulovchi) olgan bo'lsang — uni har kuni boqish kerak. "
        "Mana shu yerda kiber-kotlet asqatadi: bu avtomatik qazib olish uchun yoqilg'i, "
        "u har kuni bepul beriladi! Vazifang oddiy — kirib, robotni boqish.</b>\n\n"
        "Vaqtida boqmasang — robot o'chadi va qazib olish to'xtaydi.\n\n"
        "Kichik Mayner (birinchi bosqich) yoqilg'i talab qilmaydi. "
        "Muhim! Har qanday robot 30 kunga sotib olinadi — keyin uni qaytadan olish yoki Master-Dron yollash kerak. "
        "Yo'l-yo'lakay o'rganib ketasan:) Chalg'imaylik.\n\n"
        "Hammasi qanday ishlashini tushunishing uchun <b>ROFL HUB</b> haqida yana ozgina gapirib beraman.\n\n"
        "🛑 <b>Bu tanishuvimizning oxirgi xabari. Keyin faqat jangga:)</b>"
    ),
    "start.intro4": (
        "<b>JUDA QISQA QILIB AYTAMAN. ROFL HUB — bu:</b>\n"
        "- Har qanday didga mos chat-bot o'yinlari\n"
        "- Jamoa tuzish imkoniyati (50 kishigacha)\n"
        "- Uni klangacha o'stirish imkoniyati (1000 kishigacha)\n"
        "- Sovrinlar uchun jamoa va klan janglari\n"
        "- Bilim-ko'ngilochar ROFL HUB CHANNEL kanali\n"
        "- Instagram sahifasi — rofl_hub_global\n"
        "- Ro'yxatdan o'tmasdan muloqot qilish va o'zingni ilgari surish uchun rofl-hub.com sayti\n"
        "- Butun dunyo bo'ylab minglab o'yinchilar — yangi do'stlaring ular orasida bo'lishi mumkin!\n"
        "..................................................\n"
        "<b>Va'da qilganimdek, bu yakuniy xabar. Endi faqat jangga! Foydali buyruqlar:</b>\n\n"
        "/menu — funksiyalarni tez boshqarish\n"
        "/games — barcha o'yinlar ro'yxati\n"
        "/faq — ko'p so'raladigan savollar\n"
        "/rules — foydalanuvchi shartnomasi\n"
    ),

    # ---------------- меню и игровая зона ----------------
    "menu.text": (
        "📱 <b>ROFL HUB EKOTIZIMINING BOSH MENYUSI</b>\n"
        "..................................................\n\n"
        "👤 <b>SHAXSIY PROFIL VA PASPORT:</b>\n"
        "• /start — Tanishuvni boshlash va akkaunt ochish\n"
        "• /profile — Pasporting, balansing va jamoang real vaqtda\n"
        "• /my_stats — Oxirgi 30 kunlik tarixiy statistikang\n\n"
        "🚜 <b>KIBER-FERMA VA AVTOMATLASHTIRISH:</b>\n"
        "• /farm — Yoqilg'i hubi: robotlarga yoqilg'i quyish va ishlab chiqarish tezligi\n"
        "• /shop — Marketpleys: maynerlar, kotletlar va hub yaxshilanishlarini xarid qilish\n\n"
        "🕹️ <b>O'YIN XONASI:</b>\n"
        "• /games — Botga qarshi barcha o'yinlarning inlayn-hubi\n"
        "• /quiz — Tezkor viktorina: javobga 15 soniya, darajalar va bonuslar\n"
        "• /duel — Jonli o'yinchilar bilan YAKKAMA-YAKKA DUELLAR: 10/100/1000 stollari\n"
        "• /quests — KVESTLAR: mukofotli detektivlar, komediyalar va boshqotirmalar\n"
        "• /rps, /high_low, /coin, /dice, /safe — Tanga uchun tezkor o'yinlar\n\n"
        "👥 <b>JAMOALARNI BOSHQARISH:</b>\n"
        "• /create_team — 100 000 tangaga o'z jamoangni ro'yxatdan o'tkazish\n"
        "• /my_team — Jamoa dashbordi va 🧠 darajali JAMOADOSHLAR RO'YXATI\n"
        "• /all_teams — Tasodifiy jamoalar o'yin ruletkasi\n\n"
        "💸 <b>PUL VA DO'STLAR:</b>\n"
        "• /invite — Referal havolang: har bir do'st uchun +1000 tanga\n"
        "• /transfer — Boshqa o'yinchiga tanga o'tkazish\n\n"
        "📚 <b>MA'LUMOT VA QOIDALAR:</b>\n"
        "• /faq — Ekotizimning to'liq qo'llanmasi (Mini App'da ochiladi)\n"
        "• /rules — Foydalanuvchi shartnomasi\n"
        "..................................................\n"
        "<i>⚙️ Bo'limlar bo'ylab bir zumda yurish uchun ekran pastidagi doimiy ikki ustunli o'yin panelidan foydalan!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>ROFL HUB O'YIN ZONASIGA XUSH KELIBSAN!</b>\n"
        "..................................................\n\n"
        "Bu yerda botga qarshi tezkor bellashuvlarga kirishing yoki intellektual sprint-testdan "
        "o'tishing mumkin — jekpotni urasan yoki balansni yutqazib qo'yasan!\n\n"
        "💸 G'alaba keltiradi: <b>+2 tanga</b> (Kiber-Seyf: <b>+5</b>)\n"
        "💀 Mag'lubiyat yoki durang olib ketadi: <b>-1 tanga</b>\n"
        "🧠 Viktorinada — 15 soniyalik taymer va intellekt darajalari: 1-daraja — 10 to'g'ri javob va <b>+100 tanga</b>, "
        "keyin har bir daraja 10 javobga uzunroq, lekin mukofot ham 100 tangaga o'sadi!\n\n"
        "..................................................\n"
        "👇 <b>RAUNDNI HOZIROQ BOSHLASH UCHUN PASTDAGI TUGMANI BOS:</b>"
    ),
    "menu.btn_quiz": "🧠 Viktorina",
    "menu.btn_rps": "🪨 Tosh-Qaychi",
    "menu.btn_hl": "📈 Katta/Kichik",
    "menu.btn_coin": "🪙 Gerb/Raqam",
    "menu.btn_dice": "🎲 Zarlar",
    "menu.btn_safe": "🔐 Kiber-Seyf",
    "menu.btn_duel": "⚔️ Yakkama-yakka DUELLAR",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Pasport, ferma, jamoa va eng boy o'yinchilar — bitta neon ekranda. "
        "Kundalik kotletni to'g'ridan-to'g'ri o'sha yerdan olsa bo'ladi!\n\n"
        "👇 Tugmani bos:"
    ),
    "app.btn": "🎮 MINI APP'NI OCHISH",
    "app.unavailable": "⚙️ Mini App hali ekotizim serverlariga ulanmoqda. Birozdan keyin kirib ko'r!",
    "faq.teaser": (
        "📚 <b>ROFL HUB EKOTIZIMI QO'LLANMASI</b>\n"
        "..................................................\n\n"
        "Eng muhimi qisqacha:\n"
        "🚜 Robotlar tangani kecha-yu kunduz qazib beradi: Kichik Mayner — yoqilg'isiz 5/soat, "
        "Kiber-Burg'ulovchi — 10/soat, va HAR BIR Burg'ulovchi kuniga o'zining 1 kiber-kotletini yeydi. "
        "Barcha robotlar 30 kun yashaydi (Master-Dron eskirishni to'xtatib turadi).\n"
        "🧠 Viktorina: javobga 15 soniya, o'sib boruvchi mukofotli intellekt darajalari.\n"
        "⚔️ 10/100/1000 tangalik stollarda jonli o'yinchilar bilan duellar.\n"
        "🏆 50 jangchigacha jamoalar (Mega-Klan — 1000 tagacha) va har kimga sovrinli Jang tadbirlari.\n\n"
        "..................................................\n"
        "👇 <b>Barcha mexanikalar yoritilgan to'liq qo'llanma — tugmada:</b>"
    ),
    "faq.btn_open": "📖 TO'LIQ QO'LLANMANI OCHISH",
    "rules.teaser": (
        "📜 <b>ROFL HUB FOYDALANUVCHI SHARTNOMASI</b>\n"
        "..................................................\n\n"
        "Ikki og'iz so'z bilan eng muhimi:\n"
        "🪙 Tangalar va barcha o'yin buyumlari — virtual ko'ngilochar elementlar: "
        "ular pul emas va real mablag'ga almashtirilmaydi.\n"
        "💫 Xaridlar — faqat rasmiy Telegram Stars orqali; raqamli tovarlar bir zumda "
        "yetkaziladi, yetkazishda nosozlik bo'lsa, Stars avtomatik qaytariladi.\n"
        "🛡️ Biz telefon raqamlari, geolokatsiya va shaxsiy ma'lumotlarni yig'maymiz.\n"
        "🤝 Haqorat, sun'iy ko'tarish va multiakkauntlar taqiqlangan — buzganlar bloklanishi mumkin.\n\n"
        "..................................................\n"
        "👇 <b>Shartnomaning to'liq matni va mas'uliyatdan voz kechish — tugmada:</b>\n"
        "<i>⚖️ Botdan foydalanar ekansan, shartlarga roziligingni tasdiqlaysan.</i>"
    ),
    "rules.btn_open": "📜 TO'LIQ SHARTNOMANI OCHISH",
    "quest.list_header": (
        "🗺️ <b>ROFL HUB KVESTLARI</b>\n"
        "..................................................\n\n"
        "Tanlovlar va burilishlarga boy interaktiv hikoyalar: detektivlar, komediyalar, boshqotirmalar. "
        "Har bir kvestdagi ilk g'alaba tanga keltiradi, qayta o'ynash esa cheksiz!\n"
        "🌐 <i>Kvest hikoyalari hozircha rus tilida — o'zbekcha to'plam yo'lda.</i>\n\n"
        "👇 <b>Hikoyani tanla:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} daqiqa · 🏆 ilk g'alaba uchun +{reward} tanga\n"
        "..................................................\n\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Kvest o'tilgan, mukofot olingan. Xohlaganingcha qayta o'yna!</i>",
    "quest.card_progress": "⏯ <i>Senda tugallanmagan o'tish bor.</i>",
    "quest.card_new": "🆕 <i>Bu hikoyani hali o'ynamagansan.</i>",
    "quest.btn_start": "▶️ KVESTNI BOSHLASH",
    "quest.btn_restart": "🔄 QAYTADAN BOSHLASH",
    "quest.btn_resume": "⏯ DAVOM ETISH",
    "quest.btn_list": "🗺️ Kvestlar ro'yxatiga",
    "quest.btn_replay": "🔄 Yana bir bor o'tish",
    "quest.win_first": "\n\n🏆 <b>KVEST O'TILDI! Mukofot: +{coins} tanga.</b>",
    "quest.win_repeat": "\n\n✅ <b>Yana o'tildi!</b> Bu kvest uchun mukofot avvalroq olingan.",
    "quest.fail_footer": "\n\n💀 <i>Yakun unchalik zo'r emas... lekin hikoyani har doim qayta o'ynasa bo'ladi!</i>",
    "quest.stale": "⏳ Bu sahna allaqachon ortda qoldi — hozirgi joydan davom etamiz!",
    "quest.no_coins": "❌ Maslahat uchun tanga yetmaydi ({cost}). Fermaga kirib chiq!",
    "quest.not_found": "❌ Kvest topilmadi.",
    "menu.btn_quests": "🗺️ KVESTLAR",

    # ---------------- ферма ----------------
    "farm.btn_bonus": "🎁 BONUSNI OLISH (har 24 soatda kotlet)",
    "farm.btn_load1": "🥩 1 ta to'ldirish",
    "farm.btn_loadall": "⚡ HAMMASINI to'ldirish",
    "farm.btn_shop": "🏪 Do'konga kirish",
    "farm.status_all_fueled": "🟢 Barcha Kiber-Burg'ulovchilar to'ldirilgan va tanga qazmoqda!",
    "farm.status_partial": "🟡 {total} tadan {fueled} ta Kiber-Burg'ulovchi to'ldirilgan. Qolganlari muzlatkichdan kotlet kutyapti!",
    "farm.status_no_fuel": "🔴 Kiber-Burg'ulovchilar to'xtab qoldi! Muzlatkichda yoqilg'i yetarli emas.",
    "farm.status_no_drills": "💡 Daromadni oshirish uchun /shop'dan Kiber-Burg'ulovchilarni ol.",
    "farm.boost_nuclear": "🔋 Yadroviy Tezlatish x5 — {until} UTC gacha (kotlet sarfi ×3)",
    "farm.boost_nitrogen": "❄️ Azotli Sovutish +40% — {until} UTC gacha",
    "farm.boost_drone": "🛸 Master-Dron robotlar umrini {until} UTC gacha uzaytiradi",
    "farm.no_boosts": "Faol kuchaytirgichlar yo'q — /shop'ga kirib chiq.",
    "farm.burnout": "🔥 Keyingi robot kuyishi: <b>{until} UTC</b>\n",
    "farm.dashboard": (
        "🚜 <b>ROFL HUB MARKAZIY YOQILG'I HUBI</b>\n"
        "..................................................\n\n"
        "🤖 Zavoddagi faol robotlar: <b>{total} dona</b>\n"
        "• Kichik Maynerlar ({junior_rate} tanga/soat): <code>{junior} dona</code>\n"
        "• Kiber-Burg'ulovchilar ({premium_rate} tanga/soat): <code>{premium} dona</code>\n"
        "{burnout}\n"
        "📊 <b>FERMANGNING HOZIRGI TEZLIGI:</b>\n"
        "• Soatiga ishlab chiqarish: <b>+{speed_hour} tanga</b>\n"
        "• Kuniga ishlab chiqarish: <b>+{speed_day} tanga</b>\n\n"
        "⚡ <b>KUCHAYTIRGICHLAR:</b>\n{boosts}\n\n"
        "📋 <b>O'YIN ZAVODI HOLATI:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>AVTOMATIK MUZLATKICH HOLATI:</b>\n"
        "🥩 Yoqilg'i zaxirasi: <b>{fridge} / {capacity} dona</b>\n"
        "💼 Ombordagi kotletlar: <code>{inv} dona</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Muhim: robotlar 30 kun yashaydi (Master-Dron eskirishni to'xtatib turadi). "
        "HAR BIR Kiber-Burg'ulovchi har 24 soat ish uchun muzlatkichdan O'ZINING butun kotletini "
        "yeydi: 3 robot — kuniga 3 kotlet. To'ldirishni kuzatib bor!</i>"
    ),
    "farm.bonus_ok": "🎁 Kiber-kotlet omborga qo'shildi! 24 soatdan keyin qaytib kel.",
    "farm.bonus_wait": "⏳ Bonus allaqachon olingan! Keyingi kotlet {hours} soat {minutes} daqiqadan keyin.",
    "farm.no_inv_cutlets": "❌ Omboringda kiber-kotlet yo'q! Ularni /shop'dan sotib ol",
    "farm.fridge_full": "📦 Muzlatkiching allaqachon liq to'la!",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>ROFL HUB O'YINCHISINING SHAXSIY KABINETI</b>\n"
        "..................................................\n\n"
        "🆔 Pasport ID'ing: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Hozirgi tangalar: <b>{balance} tanga</b>\n"
        "🏆 Statusing: <b>{team}</b>\n"
        "🧠 Intellekt darajasi: <b>{level}</b> · {next_level}-darajagacha: "
        "/quiz da <b>{left}</b> to'g'ri javob (mukofot: +{reward} tanga)\n\n"
        "..................................................\n"
        "<i>Bu yerda hozir senda bor narsalar ko'rsatilgan. Boshqa bo'limlarga uchish uchun tugmalardan foydalan!</i>"
    ),
    "profile.no_team": "Jamoa yo'q",
    "profile.team_label": "Jamoa",
    "profile.clan_label": "Klan",
    "profile.btn_farm": "🚜 Mening Kiber-Fermam",
    "profile.btn_shop": "🏪 Do'kon",
    "profile.stats": (
        "📊 <b>O'YIN YUTUQLARI STATISTIKASI (30 KUN)</b>\n"
        "..................................................\n\n"
        "🧠 O'yin intellekti darajasi: <b>{level}</b> (jami to'g'ri javoblar: {total})\n"
        "🎮 Duellarda o'ynalgan raundlar: <b>{played} ta</b>\n"
        "🏆 Raqiblar ustidan g'alabalar: <code>{won} marta</code>\n"
        "👥 Taklif qilingan faol do'stlar: <b>{refs} kishi</b>\n\n"
        "..................................................\n"
        "<i>Statistika tarixiy xizmatlaring va o'tgan yutuqlaringni saqlaydi — yutilgan tangalar allaqachon marketda sarflangan bo'lsa ham!</i>"
    ),
    "img.passport": "PASPORT ID: {user_id}",
    "img.owner": "YETAKCHI: @{username}",
    "img.balance": "Balans: {balance} tanga",
    "img.fridge": "Muzlatkichda: {fridge} / {capacity} dona",
    "img.inv": "Ombordagi kotletlar: {inv} dona",
    "img.junior": "Kichik Maynerlar: {count} dona",
    "img.premium": "Kiber-Burg'ulovchilar: {count} dona",

    # ---------------- игры: общий движок ----------------
    "games.win": "🎉 <b>G'ALABA!</b> 🎉\nHisoblandi: <b>+{reward}</b> tanga",
    "games.lose": "💀 <b>MAG'LUBIYAT!</b>\nYechildi: <b>-{penalty}</b> tanga",
    "games.draw": "🤝 <b>DURANG!</b>\nYechildi: <b>-{penalty}</b> tanga",
    "games.limit": (
        "🛑 <b>Kunlik limitga yetding!</b>\n\n"
        "{game} o'yinida bugun allaqachon {limit} ta g'alaba olding. Limit 00:00 UTC da yangilanadi.\n\n"
        "⚡ Limitni 24 soatga olib tashlash — 5 ★, 30 kunga — 99 ★ (/shop'dagi «O'yinlar» bo'limi)."
    ),
    "games.no_coins": "❌ Senda 0 tanga — raund yig'imini to'lashga hech narsa yo'q. /farm'dan ferma daromadini yig'ib ol!",
    "games.balance": "💰 Balans: <b>{balance} tanga</b>",
    "games.btn_retry": "🎮 Yana bir bor o'ynash!",
    "games.btn_hub": "🕹️ O'yin zonasi",
    "games.level_up": (
        "🏅 <b>INTELLEKT DARAJASI OSHDI: {level}!</b> Mukofot: <b>+{bonus} tanga</b>!\n"
        "Keyingi daraja: {next_required} to'g'ri javob → +{next_reward} tanga."
    ),
    "games.name.rps": "Tosh-Qaychi-Qog'oz",
    "games.name.hl": "Katta/Kichik",
    "games.name.quiz": "Viktorina",
    "games.name.coin": "Gerb/Raqam",
    "games.name.dice": "Zarlar",
    "games.name.safe": "Seyf",

    # ---------------- КНБ ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>TOSH-QAYCHI-QOG'OZ</b>\n\n"
        "G'alaba: <b>+{reward}</b> · Mag'lubiyat/durang: <b>-{penalty}</b>\n"
        "Kunlik g'alaba limiti: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Tosh",
    "rps.scissors": "✂️ Qaychi",
    "rps.paper": "🧻 Qog'oz",
    "rps.draw": "🤝 <b>Durang!</b> Ikkala tomon ham {bot}ni tanladi.",
    "rps.win": "🏆 <b>G'alaba!</b> {user} {bot}ni yengadi.",
    "rps.lose": "💀 <b>Bot yutdi.</b> {bot} {user}ni yengadi.",

    # ---------------- Больше/Меньше ----------------
    "hl.intro": (
        "🎲 <b>KATTA YOKI KICHIK</b>\n\nBot raqam qo'ydi: <b>{base}</b>.\n"
        "Yashirin raqam kattaroq bo'ladimi yoki kichikroqmi?\n"
        "G'alaba: <b>+{reward}</b> · Mag'lubiyat: <b>-{penalty}</b> · Limit: <b>{limit}</b> g'alaba"
    ),
    "hl.btn_up": "📈 Katta",
    "hl.btn_down": "📉 Kichik",
    "hl.result": "🎲 <b>RAUND YAKUNI</b>\n\nBot raqami: <b>{base}</b> · Yashirin: <b>{secret}</b>",

    # ---------------- викторина ----------------
    "quiz.round": (
        "🧠 <b>VIKTORINA • {category}</b>\n"
        "🤔 SAVOL: <b>{question}</b>\n\n"
        "<i>🌐 Savollar hozircha rus tilida — o'zbekcha to'plam tez orada!</i>"
    ),
    "quiz.btn_new": "🧠 Yangi savol",
    "quiz.timeout": "⌛ <b>VAQT TUGADI!</b> ⌛\nTo'g'ri javob: <b>{correct}</b>",
    "quiz.stale": "⏳ Bu savol endi faol emas. Yangisini boshla!",
    "quiz.stale_alert": "Bu savol endi faol emas. Yangisini boshla!",
    "quiz.empty": "⚠️ Savollar bazasi bo'sh. Administratorga xabar ber.",
    "quiz.wrong": "❌ <b>Xato</b> ❌\nTo'g'ri javob: <b>{correct}</b>",
    "quiz.lost_line": "💀 Mag'lubiyat uchun <b>-{penalty} tanga</b>!",
    "quiz.level_line": (
        "🧠 Intellekt darajasi: <b>{level}</b>\n"
        "{next_level}-darajagacha qolgan g'alabalar: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>Javobga {seconds} soniya!\n"
        "To'g'ri: balansga +{win} tanga\n"
        "Xato / ulgurmaslik: -{penalty} tanga yechiladi\n"
        "Limit: kuniga {limit} g'alaba</i>"
    ),

    # ---------------- Орёл/Решка ----------------
    "coin.intro": (
        "🪙 <b>GERB YOKI RAQAM</b>\n\n"
        "Bot kiber-tangani otadi. Qaysi tomoni bilan tushishini top!\n"
        "G'alaba: <b>+{reward}</b> · Mag'lubiyat: <b>-{penalty}</b> · Limit: <b>{limit}</b> g'alaba"
    ),
    "coin.heads": "🦅 Gerb",
    "coin.tails": "🪙 Raqam",
    "coin.result": "🪙 Tanga aylanyapti... <b>{result}</b> tushdi! Sening tanloving: {choice}.",

    # ---------------- Кубики ----------------
    "dice.intro": (
        "🎲 <b>ZARLAR</b>\n\n"
        "Sen va bot bittadan zar tashlaysizlar. Kimning ochkosi ko'p — raund o'shaniki!\n"
        "G'alaba: <b>+{reward}</b> · Mag'lubiyat/durang: <b>-{penalty}</b> · Limit: <b>{limit}</b> g'alaba"
    ),
    "dice.btn_roll": "🎲 ZARLARNI TASHLASH",
    "dice.toast": "Zarlar tashlandi!",
    "dice.result": "🎲 Sening zaring (birinchisi): <b>{player}</b> · Bot zari: <b>{bot}</b>",

    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>KIBER-SEYF</b>\n\n"
        "Ichida — <b>{jackpot} tangalik</b> jekpot! Eshik 1–{codes} oralig'idagi kod bilan qulflangan. "
        "Senda bitta urinish bor.\n"
        "Ochding: <b>+{jackpot}</b> · Signalizatsiya: <b>-{penalty}</b> · Limit: <b>{limit}</b> g'alaba"
    ),
    "safe.btn_retry": "🔐 Yana bir bor buzish!",
    "safe.win": "🔓 <b>Seyf ochildi!</b> Kod shu edi: <b>{code}</b>.",
    "safe.lose": "🚨 <b>Signalizatsiya ishladi!</b> Sen {guess} terding, kod esa: <b>{code}</b>.",

    # ---------------- дуэли ----------------
    "duel.intro": (
        "⚔️ <b>YAKKAMA-YAKKA DUELLAR: GAROVGA TOSH-QAYCHI-QOG'OZ</b>\n"
        "..................................................\n\n"
        "Cho'ntagingga mos stolni tanla — xuddi pokerdagidek. Garov darhol yechib olinadi, "
        "raqibing — jonli ROFL HUB o'yinchisi!\n\n"
        "💰 Bank = ikkala garov. G'olib bankning <b>{payout_percent}%</b>ini oladi, "
        "<b>{burn_percent}%</b> esa abadiy kuyadi (deflyatsiya!).\n"
        "🤝 Durang — ishoralar zudlik bilan qayta o'ynaladi, bank stolda qoladi.\n"
        "⏱ Ishoraga — <b>{move_timeout} soniya</b>, jim turganga ishorani tasodif generatori tanlaydi.\n"
        "🏆 Duellardagi g'alabalar Janglarda jamoang hisobiga yoziladi!\n\n"
        "👇 <b>STOLNI TANLA:</b>"
    ),
    "duel.btn_table": "⚔️ {stake} tangalik stol",
    "duel.btn_cancel": "❌ Stolni tark etish (garov qaytadi)",
    "duel.btn_move_rock": "🪨 Tosh",
    "duel.btn_move_scissors": "✂️ Qaychi",
    "duel.btn_move_paper": "🧻 Qog'oz",
    "duel.waiting": (
        "🪑 <b>Sen {stake} tangalik stoldasan.</b> Garov bankda.\n"
        "Ikkinchi jangchini kutyapmiz... U o'tirishi bilan ikkalangizga ham ishora tanlovi keladi!\n"
        "<i>Navbat {ttl} daqiqa yashaydi, keyin garov avtomatik qaytadi.</i>"
    ),
    "duel.cancelled": "🚪 Sen stolni tark etding. <b>{stake} tangalik</b> garov balansga qaytdi.",
    "duel.expired": "⌛ {stake} tangalik stolda raqib topilmadi. <b>{stake} tangalik</b> garov qaytarildi.",
    "duel.matched": (
        "⚔️ <b>RAQIB TOPILDI! Stol: {stake} tanga.</b>\n"
        "Bank: <b>{bank} tanga</b> · G'olibga: <b>{payout}</b>\n\n"
        "⏱ Ishorani tanlashga <b>{timeout} soniya</b> bor!"
    ),
    "duel.move_saved": "✊ Ishora qabul qilindi! Raqib ishorasini kutyapmiz...",
    "duel.draw_replay": (
        "🤝 <b>DURANG! {round}-raund.</b> Ikkalangiz bir xil ishora ko'rsatdingiz.\n"
        "Bank stolda. ⏱ Yana {timeout} soniya — ishorani tanla:"
    ),
    "duel.win": (
        "🏆 <b>DUEL SENIKI!</b>\n\n"
        "Sening {winner_move} ishorang {loser_move}ni yengadi.\n"
        "💰 Yutuq: <b>+{payout} tanga</b> · 🔥 Bankda kuydi: {burned}\n"
        "💼 Balans: <b>{balance} tanga</b>"
    ),
    "duel.lose": (
        "💀 <b>DUEL BOY BERILDI.</b>\n\n"
        "Raqibning {winner_move} ishorasi sening {loser_move} ishorangni yengadi.\n"
        "📉 <b>{stake} tangalik</b> garov g'olib bankiga ketdi.\n"
        "Revansh-chi?"
    ),
    "duel.reaper_prefix": "⏰ <b>Raund vaqti tugadi!</b> Yetishmagan ishoralarni tasodif generatori tanladi.\n\n",
    "duel.bad_table": "❌ Bunaqa stol mavjud emas.",
    "duel.already_in": "⚠️ Sen allaqachon stoldasan yoki jangdasan! Avval hozirgi duelni tugat.",
    "duel.no_coins": "❌ Bu stol uchun balansda {stake} tanga kerak.",
    "duel.cancel_impossible": "⚠️ Bu navbatni endi bekor qilib bo'lmaydi (raqib topilgan yoki stol yopilgan).",
    "duel.not_active": "⌛ Bu duel allaqachon yakunlangan.",
    "duel.not_participant": "🔒 Bu sening dueling emas!",
    "duel.move_already": "✋ Bu raundda ishorangni allaqachon ko'rsatding. Raqibni kutyapmiz!",
    "duel.bad_move": "❌ Noma'lum ishora.",
    "duel.btn_rematch": "⚔️ Revansh (stollarga)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>ROFL HUB REFERAL DASTURI</b>\n"
        "..................................................\n\n"
        "Do'stlaringni taklif qil va shaxsiy havolang orqali ro'yxatdan o'tgan "
        "har bir kishi uchun <b>+{bonus} tanga</b> ol!\n\n"
        "🔗 <b>Havolang (nusxalash uchun bos):</b>\n<code>{link}</code>\n\n"
        "📊 <b>SENING STATISTIKANG:</b>\n"
        "👥 Taklif qilingan do'stlar: <b>{invited} kishi</b>\n"
        "💰 Referallardan topilgani: <b>{earned} tanga</b>\n\n"
        "..................................................\n"
        "<i>Havolani sinfdoshlar chatiga, do'stlarga va ijtimoiy tarmoqlarga tashla — davrang qancha katta bo'lsa, balansing shuncha tez o'sadi!</i>"
    ),
    "ref.btn_share": "📣 Havolani ulashish",
    "ref.share_text": "ROFL HUB o'yin ekotizimiga qo'shil!",

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>BOSHQA O'YINCHIGA TANGA O'TKAZISH</b>\n"
        "..................................................\n\n"
        "Buyruq formati:\n"
        "<code>/transfer ID summa</code> — Pasport ID bo'yicha (/profile da ko'rinadi)\n"
        "<code>/transfer @username summa</code> — username bo'yicha\n"
        "<code>/transfer ROFL-HUB-777 summa</code> — auksiondan olingan VIP ID bo'yicha\n\n"
        "Misollar:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Eng kam summa: <b>{min} tanga</b>"
    ),
    "tr.not_found": "❌ Qabul qiluvchi topilmadi. Pasport ID yoki @username'ni tekshir — o'yinchi botda ro'yxatdan o'tgan bo'lishi kerak.",
    "tr.self": "🤨 O'zingga tanga o'tkazib bo'lmaydi — bu abadiy iqtisodiyot bo'lardi!",
    "tr.blocked": "🚫 Bu o'yinchi bloklangan — unga o'tkazma qilib bo'lmaydi.",
    "tr.min": "❌ Eng kam o'tkazma summasi — {min} tanga.",
    "tr.insufficient": "❌ Tanga yetarli emas! Balansing: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Balansda tanga yetarli emas.",
    "tr.confirm": (
        "🔄 <b>O'TKAZMANI TASDIQLA:</b>\n\n"
        "👤 Qabul qiluvchi: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Yechiladigan summa: <b>{amount} tanga</b>{fee_line}\n"
        "💰 Qabul qiluvchi oladi: <b>{received} tanga</b>\n\n"
        "<i>O'tkazmalarni bekor qilib bo'lmaydi — qabul qiluvchini tekshir!</i>"
    ),
    "tr.fee_line": "\n🔥 Hub komissiyasi: <b>{fee} tanga</b> (kuyadi)",
    "tr.btn_confirm": "✅ O'TKAZMANI TASDIQLASH",
    "tr.btn_cancel": "❌ Bekor qilish",
    "tr.cancelled_toast": "O'tkazma bekor qilindi",
    "tr.cancelled": "❌ <b>O'tkazma bekor qilindi.</b> Tangalar joyida qoldi.",
    "tr.not_yours": "🔒 Bu sening o'tkazmang emas!",
    "tr.done_toast": "✅ O'tkazma bajarildi!",
    "tr.done": (
        "✅ <b>O'TKAZMA BAJARILDI!</b>\n\n"
        "💸 Yuborildi: <b>{amount} tanga</b> — ID <code>{recipient_id}</code> o'yinchiga\n"
        "💰 Balansing: <b>{balance} tanga</b>"
    ),
    "tr.received": (
        "💰 <b>Senga {amount} tanga o'tkazildi!</b>\n"
        "Yuboruvchi: ID <code>{sender_id}</code>. Balans allaqachon to'ldirildi — /profile ni tekshir!"
    ),

    # ---------------- магазин и платежи ----------------
    "shop.header": "🏪 <b>ROFL HUB DO'KONI</b>\nXaridlar — rasmiy Telegram Stars orqali. Pastdagi tugmalar bilan kategoriyani tanla.",
    "shop.cat_farm": (
        "🚜 <b>DO'KON · FERMA UCHUN</b>\n"
        "..................................................\n"
        "30 kunlik robotlar, yoqilg'i, muzlatkichlar, kuchaytirgichlar va Master-Dron.\n"
        "📦 Hozirgi muzlatkiching: <b>{capacity} kotlet</b>\n"
        "..................................................\n"
        "👇 <b>Tovarni tanla:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>DO'KON · O'YINLAR</b>\n"
        "..................................................\n"
        "G'alaba limitlarini olib tashlash, tanga paketlari va Mega-Klan litsenziyasi.\n"
        "..................................................\n"
        "👇 <b>Tovarni tanla:</b>"
    ),
    "pay.invoice_desc": "ROFL HUB o'yin ichidagi kontentni bir zumda yetkazish.",
    "pay.invoice_error": "⚠️ Telegram Stars to'lov hisobini yaratib bo'lmadi. Keyinroq urinib ko'r.",
    "pay.success": "🎉 <b>To'lov tasdiqlandi!</b>\n🧾 <code>{charge}</code>\n💵 Yechildi: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 To'lov o'tdi, lekin yetkazish vaqtincha muvaffaqiyatsiz bo'ldi. Biz allaqachon xabardormiz.\n"
        "To'lov raqamini saqlab qo'y: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Stars hisobingga avtomatik qaytarildi.",
    "pay.keep_charge": "Qaytarish uchun to'lov raqamini saqlab qo'y: <code>{charge}</code>",
    "pay.already": "✅ Bu to'lov allaqachon qayta ishlangan, tovar avvalroq berilgan.",
    "pay.support": (
        "🛟 <b>TELEGRAM STARS TO'LOVLARI BO'YICHA YORDAM</b>\n"
        "..................................................\n\n"
        "Barcha ROFL HUB tovarlari — raqamli va to'lovdan keyin bir zumda yetkaziladi.\n\n"
        "⚙️ <b>Agar to'lov o'tgan-u, tovar kelmagan bo'lsa:</b>\n"
        "yetkazishda nosozlik bo'lsa, bot Stars'ni avtomatik qaytaradi. Agar bu sodir bo'lmasa — "
        "shu yerga to'lov raqamini yubor (u chekda bor, formati <code>xxxx...</code>) va muammoni tasvirlab ber. "
        "Ma'muriyat to'lovni baza bo'yicha tekshiradi va masalani 24 soat ichida hal qiladi.\n\n"
        "💫 <b>Qaytarish siyosati:</b>\n"
        "tovar olinmagan yoki xato berilgan bo'lsa, qaytarish mumkin. "
        "To'g'ri yetkazilgan raqamli tovarlar qaytarilmaydi.\n\n"
        "..................................................\n"
        "<i>Bu bo'lim — Telegram qoidalariga ko'ra xaridlar bo'yicha rasmiy yordam nuqtasi.</i>"
    ),

    # ---------------- доставка ----------------
    "dlv.cutlets": "🥩 Omborga qo'shildi: <b>{qty} kotlet</b>.",
    "dlv.miner": "🤖 <b>«{name}»</b> roboti fermangga yetkazildi.\n⏳ Xizmat muddati: <b>{until} UTC</b> gacha.",
    "dlv.miner_junior": "Kichik Mayner",
    "dlv.miner_premium": "Kiber-Burg'ulovchi",
    "dlv.fridge": "📦 Muzlatkich <b>{capacity} kotlet</b>gacha kengaytirildi.",
    "dlv.coins": "💰 Hisoblandi: <b>+{amount} tanga</b>.",
    "dlv.boost_nuclear": "🔋 Yadroviy Tezlatish x5 <b>{until} UTC</b> gacha faol.",
    "dlv.boost_nitrogen": "❄️ Azotli Sovutish +40% <b>{until} UTC</b> gacha faol.",
    "dlv.drone": "🛸 Master-Dron fermani <b>{until} UTC</b> gacha qo'riqlaydi.",
    "dlv.unlimit": "⚡ G'alaba limitlari <b>{until} UTC</b> gacha olib tashlandi.",
    "dlv.clan": "🏆 Jamoang <b>MEGA-KLAN</b> statusini oldi: {max} tagacha joy.",
    "dlv.err_fridge": "Senda allaqachon shu yoki kattaroq hajmdagi muzlatkich bor.",
    "dlv.err_no_team": "Senda tuzilgan jamoa yo'q. Avval /create_team orqali uni tuz.",
    "dlv.err_mega": "Jamoang allaqachon Mega-Klan statusiga ega.",

    # ---------------- команды/кланы (основные поверхности) ----------------
    "clan.no_team": "⚠️ <b>Senda hali tuzilgan jamoa yo'q!</b>\n\nPastdagi tugmani bosib, hoziroq o'z jamoangni ro'yxatdan o'tkazishing mumkin.",
    "clan.btn_create": "🏆 100k ga Jamoa tuzish",
    "clan.btn_members": "👥 JAMOADOSHLAR RO'YXATI",
    "clan.btn_leave": "🚪 Jamoani tark etish",
    "clan.btn_dashboard": "🏆 Jamoa dashbordi",
    "clan.status_clan": "👑 STATUS: IMPERIYA KLANI",
    "clan.status_team": "👥 STATUS: ODDIY JAMOA",
    "clan.dashboard": (
        "🏆 <b>JAMOANGNING AXBOROT DASHBORDI</b>\n"
        "..................................................\n\n"
        "📌 Nomi: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Jamoa sardori: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Shior: <i>«{motto}»</i>\n"
        "🔮 Emblema belgisi: {symbol}\n\n"
        "👥 A'zolar tarkibi: <b>{members} / {max_members} kishi</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVIGATSIYA:</b>"
    ),
    "clan.members_only": "🔒 A'zolar ro'yxati faqat shu jamoa a'zolariga ko'rinadi!",
    "clan.members_gone": "❌ Jamoa allaqachon tarqatib yuborilgan.",
    "clan.members_header": (
        "👥 <b>«{name}» JAMOASI TARKIBI</b>\n"
        "🧠 — o'yin intellekti darajasi (faqat /quiz da oshiriladi)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
        "📄 Sahifa: <b>{page} / {pages}</b> · Jami jangchilar: <b>{members}</b>\n"
        "<i>Jamoadoshingga yozish, o'z chatingni yig'ish va jamoani jamoaviy bellashuvlarga "
        "chaqirish uchun uning @username'iga bos!</i>"
    ),
    "clan.btn_prev": "⬅️ Orqaga",
    "clan.btn_next": "Oldinga ➡️",
    "clan.join_ok": (
        "🎉 <b>TABRIKLAYMIZ, SEN O'YINDASAN!</b>\n\nSen <b>{name}</b> jamoasiga muvaffaqiyatli qo'shilding!\n"
        "📍 Tarkibni tekshirish uchun /my_team buyrug'ini yoz!"
    ),
    "clan.leave_ok": "🚪 Sen <b>{name}</b> jamoasini tark etding. Endi erkin qushsan!",
}

MINIAPP: dict[str, str] = {
    "subtitle": "bitta ekrandagi o'yin imperiyang",
    "passport": "📋 O'YINCHI PASPORTI", "coins": "tanga",
    "brain": "🧠 Intellekt darajasi", "toNext": "{n}-darajagacha: viktorinada {left} to'g'ri javob (+{reward} tanga)",
    "farm": "🚜 KIBER-FERMA", "robots": "Robotlar (maynerlar / burg'ulovchilar)",
    "fueled": "To'ldirilgan burg'ulovchilar", "speed": "Qazib olish tezligi",
    "perHour": "{v} tanga/soat", "fridge": "Muzlatkich", "inv": "Ombordagi kotletlar",
    "burnout": "Eng yaqin kuyish", "boosts": "Faol kuchaytirgichlar", "none": "yo'q",
    "bonusReady": "🎁 KUNDALIK KOTLETNI OLISH",
    "bonusWait": "⏳ Bonus {h} soat {m} daqiqadan keyin", "bonusDone": "🎉 Kotlet omborda!",
    "team": "🏆 MENING JAMOAM", "clan": "KLAN", "teamLabel": "Jamoa", "captain": "👑 Sen sardorsan!",
    "members": "Tarkib", "noTeam": "Hozircha jamoasizsan — bot chatida o'z jamoangni yig'!",
    "top": "👑 EKOTIZIMNING TOP-100 BOYLARI",
    "shop": "🏪 DO'KON", "shopFarm": "🚜 FERMA UCHUN", "shopGames": "🕹️ O'YINLAR",
    "shopHint": "To'lov rasmiy Telegram Stars bilan — shu yerning o'zida, bir bosishda.",
    "paid": "🎉 To'landi! Tovar allaqachon akkauntingda.",
    "payFail": "To'lov o'tmadi. Yana urinib ko'r.",
    "oldClient": "Mini App'dan xarid qilish uchun Telegram'ni yangila yoki do'konni bot chatida och.",
    "ctaNoRobots": "💤 Ferma bo'sh! Birinchi robotni ol — tangalar kecha-yu kunduz oqib keladi.",
    "ctaHungry": "🚨 Burg'ulovchilar och qoldi ({n} tasi yoqilg'isiz) — qazib olish to'xtab turibdi!",
    "ctaLowFuel": "⚠️ Kotletlar Burg'ulovchilarning bir kunlik ishiga ham yetmaydi.",
    "ctaShopBtn": "🛒 Do'konga",
    "footer": "To'liq boshqaruv — bot chatida: /menu",
    "noProfile": "Profil topilmadi. Botni ochib, /start ni bos!",
    "blocked": "Akkaunt ma'muriyat tomonidan bloklangan.",
    "error": "Ma'lumotlarni yuklab bo'lmadi. Keyinroq urinib ko'r.",
    "outside": "Bu ilovani ROFL HUB Telegram-botidan och.",
}

COMMANDS: dict[str, str] = {
    "app": "🎮 Mini App'ni ochish",
    "menu": "📱 Bosh menyu",
    "profile": "👤 Profilim va pasportim",
    "farm": "🚜 Kiber-ferma va yoqilg'i quyish",
    "shop": "🏪 Telegram Stars do'koni",
    "games": "🕹️ Botga qarshi barcha o'yinlar",
    "quiz": "🧠 Viktorina: javobga 15 soniya",
    "duel": "⚔️ Garovga yakkama-yakka duel",
    "quests": "🗺️ Kvestlar: tanlovli hikoyalar",
    "my_team": "🏆 Jamoam va jamoadoshlarim",
    "invite": "🤝 Referal havola: do'st uchun +1000",
    "transfer": "🔄 O'yinchiga tanga o'tkazish",
    "my_stats": "📊 Statistikam",
    "faq": "📚 Ko'p so'raladigan savollar",
    "rules": "📜 Foydalanuvchi shartnomasi",
    "paysupport": "🛟 To'lovlar bo'yicha yordam",
}
