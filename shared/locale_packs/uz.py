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
# биржа котлет -> Kotlet birjasi; ордер -> buyurtma; комиссия -> komissiya
# ресурсы (волна 22.10): Металл -> Metall; Водород -> Vodorod; Кристаллы -> Kristallar;
#   Детали -> Detallar; Мастерская -> Ustaxona; Кибер-броня -> Kiber-zirh; Шаттл -> Shattl;
#   Налёт -> Bosqin; Стойка обороны -> Himoya pozitsiyasi; Разведка -> Razvedka;
#   Реванш -> Revansh; Щит -> Qalqon; Сундук -> Sandiq; Серия -> Seriya;
#   Станция команды -> Jamoa stansiyasi; вылет -> parvoz; трофей/добыча -> o'lja

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
    "common.feature_off": "⚙️ Bu bo'lim vaqtincha texnik xizmatda. Birozdan keyin qaytib ko'r!",
    "common.maintenance": "🛠 ROFL HUB qisqa texnik ishlarda. Tez orada qaytamiz — tangalaring va yutuqlaring xavfsiz!",

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
        "💸 Senga hisoblandi: <b>{balance} 🪙</b>\n"
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
        "• /rps, /high_low, /safe — Tanga uchun tezkor o'yinlar\n\n"
        "👥 <b>JAMOALARNI BOSHQARISH:</b>\n"
        "• /create_team — O'z jamoangni ro'yxatdan o'tkazish: 100 000 🪙\n"
        "• /my_team — Jamoa dashbordi va 🧠 darajali JAMOADOSHLAR RO'YXATI\n"
        "• /all_teams — Tasodifiy jamoalar o'yin ruletkasi\n\n"
        "💸 <b>PUL VA DO'STLAR:</b>\n"
        "• /invite — Referal havolang: har bir do'st uchun +1000 🪙\n"
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
        "💸 G'alaba keltiradi: <b>+2 🪙</b> (Kiber-Seyf: <b>+5</b>)\n"
        "💀 Mag'lubiyat yoki durang olib ketadi: <b>-1 🪙</b>\n"
        "🧠 Viktorinada — 15 soniyalik taymer va intellekt darajalari: 1-daraja — 10 to'g'ri javob va <b>+100 🪙</b>, "
        "keyin har bir daraja 10 javobga uzunroq, lekin mukofot ham 100 ga o'sadi!\n\n"
        "..................................................\n"
        "👇 <b>RAUNDNI HOZIROQ BOSHLASH UCHUN PASTDAGI TUGMANI BOS:</b>"
    ),
    "menu.btn_quiz": "🧠 Viktorina",
    "menu.btn_rps": "🪨 Tosh-Qaychi",
    "menu.btn_hl": "📈 Katta/Kichik",
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
        "⚔️ Jonli o'yinchilar bilan 10/100/1000 🪙 stollarida duellar.\n"
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
        "🎭 {genre} · ⏱ {minutes} daqiqa · 🏆 ilk g'alaba uchun +{reward} 🪙\n"
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
    "quest.win_first": "\n\n🏆 <b>KVEST O'TILDI! Mukofot: +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>Yana o'tildi!</b> Bu kvest uchun mukofot avvalroq olingan.",
    "quest.fail_footer": "\n\n💀 <i>Yakun unchalik zo'r emas... lekin hikoyani har doim qayta o'ynasa bo'ladi!</i>",
    "quest.stale": "⏳ Bu sahna allaqachon ortda qoldi — hozirgi joydan davom etamiz!",
    "quest.no_coins": "❌ Maslahat {cost} 🪙 turadi, balansingda esa kamroq. Fermaga kirib chiq!",
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
    "farm.status_no_drills": "💡 /shop'dan kuchliroq robot ol — ferma ko'proq qazib beradi.",
    "farm.boost_nuclear": "🔋 Yadroviy Tezlatish x5 — {until} UTC gacha (kotlet sarfi ×3)",
    "farm.boost_nitrogen": "❄️ Azotli Sovutish +40% — {until} UTC gacha",
    "farm.boost_drone": "🛸 Master-Dron robotlar umrini {until} UTC gacha uzaytiradi",
    "farm.no_boosts": "Faol kuchaytirgichlar yo'q — /shop'ga kirib chiq.",
    "farm.burnout": "🔥 Keyingi robot kuyishi: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Stajyor Robotni faollashtirish (bepul)",
    "farm.intern_activated": "🤖 Stajyor Robot smenaga chiqdi! Abadiy soatiga +1 🪙 — yoqilg'isiz va muddatsiz.",
    "farm.intern_already": "🤖 Stajyor Roboting allaqachon ishlayapti.",
    "farm.intern_line": "• Stajyor Robotlar ({rate} 🪙/soat, abadiy): <code>{count} dona</code>\n",
    "farm.intern_hint": "🎁 Senda bepul Stajyor Robot bor! Pastdagi tugmani bos — u abadiy soatiga 1 🪙 qazib beradi.",
    "farm.dashboard": (
        "🚜 <b>ROFL HUB MARKAZIY YOQILG'I HUBI</b>\n"
        "..................................................\n\n"
        "🤖 Zavoddagi faol robotlar: <b>{total} dona</b>\n"
        "{intern}"
        "• Kichik Maynerlar ({junior_rate} 🪙/soat): <code>{junior} dona</code>\n"
        "• Kiber-Burg'ulovchilar ({premium_rate} 🪙/soat): <code>{premium} dona</code>\n"
        "{burnout}\n"
        "📊 <b>FERMANGNING HOZIRGI TEZLIGI:</b>\n"
        "• Soatiga ishlab chiqarish: <b>+{speed_hour} 🪙</b>\n"
        "• Kuniga ishlab chiqarish: <b>+{speed_day} 🪙</b>\n\n"
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
        "💰 Hozirgi tangalar: <b>{balance} 🪙</b>\n"
        "🏆 Statusing: <b>{team}</b>\n"
        "🧠 Intellekt darajasi: <b>{level}</b> · {next_level}-darajagacha: "
        "/quiz da <b>{left}</b> to'g'ri javob (mukofot: +{reward} 🪙)\n\n"
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
    "games.win": "🎉 <b>G'ALABA!</b> 🎉\nHisoblandi: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>MAG'LUBIYAT!</b>\nYechildi: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>DURANG!</b>\nYechildi: <b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>Kunlik limitga yetding!</b>\n\n"
        "{game} o'yinida bugun allaqachon {limit} ta g'alaba olding. Limit 00:00 UTC da yangilanadi.\n\n"
        "⚡ Limitni 24 soatga olib tashlash — 5 ★, 30 kunga — 99 ★ (/shop'dagi «O'yinlar» bo'limi)."
    ),
    "games.no_coins": "❌ Senda 0 🪙 — raund yig'imini to'lashga hech narsa yo'q. /farm'dan ferma daromadini yig'ib ol!",
    "games.balance": "💰 Balans: <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 Yana bir bor o'ynash!",
    "games.btn_hub": "🕹️ O'yin zonasi",
    "games.level_up": (
        "🏅 <b>INTELLEKT DARAJASI OSHDI: {level}!</b> Mukofot: <b>+{bonus} 🪙</b>!\n"
        "Keyingi daraja: {next_required} to'g'ri javob → +{next_reward} 🪙."
    ),
    "games.name.rps": "Tosh-Qaychi-Qog'oz",
    "games.intern_bonus": "🤖 {level}-daraja! Fermaga yana bitta Stajyor Robot keldi — endi ular {count} ta.",
    "games.name.hl": "Katta/Kichik",
    "games.name.quiz": "Viktorina",
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
    "quiz.lost_line": "💀 Mag'lubiyat uchun <b>-{penalty} 🪙</b>!",
    "quiz.level_line": (
        "🧠 Intellekt darajasi: <b>{level}</b>\n"
        "{next_level}-darajagacha qolgan g'alabalar: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>Javobga {seconds} soniya!\n"
        "To'g'ri: balansga +{win} 🪙\n"
        "Xato / ulgurmaslik: -{penalty} 🪙 yechiladi\n"
        "Limit: kuniga {limit} g'alaba</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>KIBER-SEYF</b>\n\n"
        "Ichida — <b>{jackpot} 🪙</b> jekpot! Eshik 1–{codes} oralig'idagi kod bilan qulflangan. "
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
    "duel.btn_table": "⚔️ Stol {stake} 🪙",
    "duel.btn_cancel": "❌ Stolni tark etish (garov qaytadi)",
    "duel.btn_move_rock": "🪨 Tosh",
    "duel.btn_move_scissors": "✂️ Qaychi",
    "duel.btn_move_paper": "🧻 Qog'oz",
    "duel.waiting": (
        "🪑 <b>Sen {stake} 🪙 stolidasan.</b> Garov bankda.\n"
        "Ikkinchi jangchini kutyapmiz... U o'tirishi bilan ikkalangizga ham ishora tanlovi keladi!\n"
        "<i>Navbat {ttl} daqiqa yashaydi, keyin garov avtomatik qaytadi.</i>"
    ),
    "duel.cancelled": "🚪 Sen stolni tark etding. Garov (<b>{stake} 🪙</b>) balansga qaytdi.",
    "duel.expired": "⌛ {stake} stolida raqib topilmadi. Garov (<b>{stake} 🪙</b>) qaytarildi.",
    "duel.matched": (
        "⚔️ <b>RAQIB TOPILDI! Stol {stake} 🪙.</b>\n"
        "Bank: <b>{bank} 🪙</b> · G'olibga: <b>{payout}</b>\n\n"
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
        "💰 Yutuq: <b>+{payout} 🪙</b> · 🔥 Bankda kuydi: {burned}\n"
        "💼 Balans: <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>DUEL BOY BERILDI.</b>\n\n"
        "Raqibning {winner_move} ishorasi sening {loser_move} ishorangni yengadi.\n"
        "📉 Garov (<b>{stake} 🪙</b>) g'olib bankiga ketdi.\n"
        "Revansh-chi?"
    ),
    "duel.reaper_prefix": "⏰ <b>Raund vaqti tugadi!</b> Yetishmagan ishoralarni tasodif generatori tanladi.\n\n",
    "duel.bad_table": "❌ Bunaqa stol mavjud emas.",
    "duel.already_in": "⚠️ Sen allaqachon stoldasan yoki jangdasan! Avval hozirgi duelni tugat.",
    "duel.no_coins": "❌ Bu stol uchun balansda {stake} 🪙 kerak.",
    "duel.cancel_impossible": "⚠️ Bu navbatni endi bekor qilib bo'lmaydi (raqib topilgan yoki stol yopilgan).",
    "duel.not_active": "⌛ Bu duel allaqachon yakunlangan.",
    "duel.not_participant": "🔒 Bu sening dueling emas!",
    "duel.move_already": "✋ Bu raundda ishorangni allaqachon ko'rsatding. Raqibni kutyapmiz!",
    "duel.bad_move": "❌ Noma'lum ishora.",
    "duel.btn_rematch": "⚔️ Revansh (stollarga)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 Unvon: <b>{rank}</b>\n",
    "rank.rookie": "Yangi",
    "rank.fighter": "Jangchi",
    "rank.legend": "Afsona",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.dead": "DEAD",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>ROFL HUB REFERAL DASTURI</b>\n"
        "..................................................\n\n"
        "Do'stlaringni taklif qil va shaxsiy havolang orqali ro'yxatdan o'tgan "
        "har bir kishi uchun <b>+{bonus} 🪙</b> ol!\n\n"
        "🔗 <b>Havolang (nusxalash uchun bos):</b>\n<code>{link}</code>\n\n"
        "📊 <b>SENING STATISTIKANG:</b>\n"
        "👥 Taklif qilingan do'stlar: <b>{invited} kishi</b>\n"
        "💰 Referallardan topilgani: <b>{earned} 🪙</b>\n\n"
        "..................................................\n"
        "<i>Havolani sinfdoshlar chatiga, do'stlarga va ijtimoiy tarmoqlarga tashla — davrang qancha katta bo'lsa, balansing shuncha tez o'sadi!</i>"
    ),
    "ref.btn_share": "📣 Havolani ulashish",
    "ref.share_text": "ROFL HUB o'yin ekotizimiga qo'shil!",
    "ref.qualified_line": ("⭐ <b>Ikki karra foyda:</b> taklif qilingan do'sting {rounds} raund "
                           "o'ynasa — senga yana <b>+{bonus} 🪙</b> va <b>{cutlets} 🥩 kiber-kotlet</b> keladi!"),
    "ref.qualified_notify": ("🤝 <b>Do'sting o'yinga berilib ketdi: allaqachon {rounds} raund!</b>\n"
                             "Malakali referal uchun senga <b>+{bonus} 🪙</b> va omborga <b>{cutlets} 🥩 kiber-kotlet</b> yozildi. "
                             "Yana chaqir!"),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>BOSHQA O'YINCHIGA TANGA O'TKAZISH</b>\n"
        "..................................................\n\n"
        "Buyruq formati:\n"
        "<code>/transfer ID summa</code> — Pasport ID bo'yicha (/profile da ko'rinadi)\n"
        "<code>/transfer @username summa</code> — username bo'yicha\n"
        "<code>/transfer ROFL-HUB-777 summa</code> — auksiondan olingan VIP ID bo'yicha\n\n"
        "Misollar:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Eng kam summa: <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ Qabul qiluvchi topilmadi. Pasport ID yoki @username'ni tekshir — o'yinchi botda ro'yxatdan o'tgan bo'lishi kerak.",
    "tr.self": "🤨 O'zingga tanga o'tkazib bo'lmaydi — bu abadiy iqtisodiyot bo'lardi!",
    "tr.blocked": "🚫 Bu o'yinchi bloklangan — unga o'tkazma qilib bo'lmaydi.",
    "tr.min": "❌ Eng kam o'tkazma summasi — {min} 🪙.",
    "tr.insufficient": "❌ Tanga yetarli emas! Balansing: <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ Balansda tanga yetarli emas.",
    "tr.confirm": (
        "🔄 <b>O'TKAZMANI TASDIQLA:</b>\n\n"
        "👤 Qabul qiluvchi: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Yechiladigan summa: <b>{amount} 🪙</b>{fee_line}\n"
        "💰 Qabul qiluvchi oladi: <b>{received} 🪙</b>\n\n"
        "<i>O'tkazmalarni bekor qilib bo'lmaydi — qabul qiluvchini tekshir!</i>"
    ),
    "tr.fee_line": "\n🔥 Hub komissiyasi: <b>{fee} 🪙</b> (kuyadi)",
    "tr.btn_confirm": "✅ O'TKAZMANI TASDIQLASH",
    "tr.btn_cancel": "❌ Bekor qilish",
    "tr.cancelled_toast": "O'tkazma bekor qilindi",
    "tr.cancelled": "❌ <b>O'tkazma bekor qilindi.</b> Tangalar joyida qoldi.",
    "tr.not_yours": "🔒 Bu sening o'tkazmang emas!",
    "tr.done_toast": "✅ O'tkazma bajarildi!",
    "tr.done": (
        "✅ <b>O'TKAZMA BAJARILDI!</b>\n\n"
        "💸 Yuborildi: <b>{amount} 🪙</b> — ID <code>{recipient_id}</code> o'yinchiga\n"
        "💰 Balansing: <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>Senga {amount} 🪙 o'tkazildi!</b>\n"
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
    "dlv.coins": "💰 Hisoblandi: <b>+{amount} 🪙</b>.",
    "dlv.boost_nuclear": "🔋 Yadroviy Tezlatish x5 <b>{until} UTC</b> gacha faol.",
    "dlv.boost_nitrogen": "❄️ Azotli Sovutish +40% <b>{until} UTC</b> gacha faol.",
    "dlv.drone": "🛸 Master-Dron fermani <b>{until} UTC</b> gacha qo'riqlaydi.",
    "dlv.unlimit": "⚡ G'alaba limitlari <b>{until} UTC</b> gacha olib tashlandi.",
    "dlv.clan": "🏆 Jamoang <b>MEGA-KLAN</b> statusini oldi: {max} tagacha joy.",
    "dlv.err_fridge": "Senda allaqachon shu yoki kattaroq hajmdagi muzlatkich bor.",
    "dlv.err_no_team": "Senda tuzilgan jamoa yo'q. Avval /create_team orqali uni tuz.",
    "dlv.err_mega": "Jamoang allaqachon Mega-Klan statusiga ega.",
    "dlv.intern_upgrade": "♾ Stajyor Robot <b>ABADIY Kichik Maynerga</b> ko'tarildi: soatiga 5 🪙, muddatsiz!",
    "dlv.err_no_intern": "Faollashtirilgan Stajyor Robot yo'q — avval uni /farm da faollashtir.",
    "dlv.err_intern_refs": "Yangilash uchun {need} ta malakali do'st kerak (har biri 30 raund); senda {have} ta.",
    "mk.header": "📈 <b>KOTLET BIRJASI</b>\n..................................................\n\nOchiq buyurtmalar: <b>{orders}</b> · sotuvdagi kotletlar: <b>{cutlets}</b> · eng yaxshi narx: <b>{best}</b>\nHab komissiyasi: har sotuvdan <b>{fee}%</b> (yondiriladi — inflyatsiyadan himoya)\n🥩 Ombordagi kotletlaring: <b>{inv}</b>\n\n{body}\n\n<i>Sotib olish — buyurtmani bos. Sotish — /sell buyrug'i.</i>",
    "mk.empty": "Hozircha takliflar yo'q. Birinchi bo'l: /sell soni narxi",
    "mk.order_line": "🥩 #{id} · <b>{qty} dona</b>, donasi <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} dona, donasi {price} 🪙",
    "mk.btn_my": "📋 Mening buyurtmalarim",
    "mk.btn_sell_help": "💰 Kotlet qanday sotiladi",
    "mk.btn_refresh": "🔄 Yangilash",
    "mk.btn_back": "← Birjaga",
    "mk.pick": "🛒 <b>Buyurtma #{id}</b>: {qty} dona mavjud, donasi {price} 🪙.\nNechta olasan?",
    "mk.btn_qty": "{qty} dona — {total} 🪙",
    "mk.btn_qty_all": "Hammasi, {qty} dona — {total} 🪙",
    "mk.buy_toast": "Bitim yopildi!",
    "mk.buy_done": "✅ <b>{qty} kotlet</b> <b>{total} 🪙</b> evaziga sotib olindi. Ular omborda — Burg'ulovchilarni to'ldir!",
    "mk.sold_notify": "💰 <b>Birja: sotildi!</b> Buyurtma #{id}: {qty} dona, donasi {price}. Senga <b>+{got} 🪙</b> tushdi (komissiya {fee} yondirildi).",
    "mk.sell_help": "💰 <b>KOTLET QANDAY SOTILADI</b>\n\nBuyruq: <code>/sell soni narxi</code>\nMisol: <code>/sell 10 250</code> — 10 ta kotlet, donasi 250 🪙.\n\nKotletlar ombordan olinib buyurtmada xaridorni kutadi (istalgan vaqtda olib tashlash mumkin). Bitta buyurtmada {max_qty} tagacha, {max_orders} tagacha ochiq buyurtma. Sotuvda {fee}% komissiya yondiriladi. Kotlet {min} 🪙 dan arzon bo'lmaydi: do'kondan Stars evaziga olingan yoqilg'i har doim birjadan foydaliroq. Resurslar, sotib olish so'rovlari va almashuv — o'yin ilovasida.",
    "mk.sell_confirm": "📝 <b>{qty} kotlet</b>ni donasi <b>{price}</b> 🪙 narxda qo'yamizmi?\nBitim summasi: {total} · komissiya {fee} yonadi · senga <b>{got} 🪙</b> tushadi.",
    "mk.btn_confirm_sell": "✅ BIRJAGA QO'YISH",
    "mk.btn_cancel": "❌ Bekor qilish",
    "mk.sell_toast": "Buyurtma qo'yildi!",
    "mk.sell_done": "✅ Buyurtma <b>#{id}</b> birjada: {qty} dona, donasi {price} 🪙. Sotilgach xabar beraman.",
    "mk.cancelled_toast": "Bekor qilindi",
    "mk.cancel_text": "❌ <b>Bekor qilindi.</b> Kotletlar omborda qoldi.",
    "mk.my_header": "📋 <b>SENING BUYURTMALARING</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} dona, donasi {price} 🪙",
    "mk.my_empty": "📋 Ochiq buyurtmalaring yo'q.",
    "mk.btn_cancel_order": "❌ #{id} buyurtmani olib tashlash",
    "mk.order_cancelled": "↩️ #{id} buyurtma olib tashlandi: <b>{qty} kotlet</b> omborga qaytdi.",
    "mk.err_qty": "❌ Soni: bitta buyurtmada 1 dan {max} donagacha.",
    "mk.err_price": "❌ Narx: donasi uchun {min}–{max} 🪙.",
    "mk.err_no_cutlets": "❌ Omborda faqat {have} ta kotlet bor. Muzlatkichdagi kotletlar birjaga chiqmaydi — /farm ga qara.",
    "mk.err_too_many": "❌ Chegara: {max} tadan ko'p ochiq buyurtma bo'lmaydi. «Mening buyurtmalarim»da birini olib tashla.",
    "mk.err_not_found": "❌ Bu buyurtma allaqachon yopilgan.",
    "mk.err_own": "🤨 O'z buyurtmangni sotib olib bo'lmaydi.",
    "mk.err_insufficient": "❌ Yetmaydi: {total} 🪙 kerak.",
    "farm.btn_market": "📈 Kotlet birjasi",

    # ---------------- ресурсы (волна 22.10, вечер) ----------------
    "res.metal": "Metall",
    "res.hydrogen": "Vodorod",
    "res.crystal": "Kristallar",
    "res.parts": "Detallar",
    "res.none": "hozircha bo'sh",
    "games.resource_gain": "{icon} Qazildi: <b>+{qty} {name}</b> (jami {total}) → /workshop",
    "duel.metal_gain": "⛏ Duel o'ljasi: <b>+{metal} Metall</b> → /workshop",
    "quest.win_resources": "\n📦 Qo'shimcha resurs to'plami: har biridan <b>{qty}</b> tadan → /workshop",
    "profile.resources_line": "🧰 Resurslar: {stock}\n",
    "menu.btn_goals": "🎯 Kundalik maqsadlar",
    "menu.btn_raids": "🏴‍☠️ Bosqinlar",
    "menu.btn_workshop": "🔧 Ustaxona",
    "farm.btn_workshop": "🔧 Ustaxona",
    "farm.btn_app": "🏭 Ilovadagi ferma",
    "menu.btn_app": "🚀 O'yin ilovasi: ferma, ustaxona, bosqinlar",
    "app.btn_section": "🚀 ILOVADA OCHISH",
    "app.goto_workshop": "🔧 <b>Ustaxona</b> o'yin ilovasida: resurslar, retseptlar va bir bosishda yasash.",
    "app.goto_raids": "🏴\u200d☠️ <b>Bosqinlar</b> o'yin ilovasida: razvedka, himoya pozitsiyasi va revansh.",
    "app.goto_station": "🛰 <b>Jamoa stansiyasi</b> o'yin ilovasida: progress, hissalar va butun jamoa uchun bonus.",
    "app.goto_market": "📈 <b>Kotlet birjasi</b> o'yin ilovasida qulayroq: vitrina, sotuv va buyurtmalaring bitta ekranda.",
    "mk.err_asset": "❌ Birjada bunday tovar yo'q.",
    "mk.err_no_resource": "❌ Resurs yetmaydi: omborda faqat {have}.",
    "mk.bid_filled_notify": "🙋 <b>Birja: so'rov bajarildi!</b> So'rov #{id}: donasi {price} 🪙 dan <b>+{qty} {icon}</b> sotib olindi.",
    "sw.err_same": "❌ Resursni xuddi o'zi bilan almashtirib bo'lmaydi.",
    "sw.err_qty": "❌ Almashuvda 1 dan {max} gacha miqdor kiriting — ham beradiganingiz, ham olmoqchi bo'lganingiz uchun.",
    "shop.btn_info": "ℹ️ Har bir mahsulot nima beradi",
    "sw.done_notify": "🔄 <b>#{id} almashuv amalga oshdi!</b> Berildi: {give}, olindi: {want}.",
    "ws.err_coins": "🔒 Tanga yetmaydi: {need} 🪙 kerak, balansda {have} 🪙.",
    "wk.eff_nitrogen": "❄️ Azot +40% {h} soatga",
    "wk.eff_nuclear": "☢️ Yadroviy x5 {h} soatga",
    "wk.eff_drone": "🛸 Master-Dron {h} soatga",
    "wk.eff_shield": "🛡 Qalqon {h} soatga",
    "wk.eff_unlimit": "⚡ Cheksiz o'yinlar {h} soatga",
    "wk.eff_cutlet": "🥩 Kotlet ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ Bu haftalik retsept endi mavjud emas.",
    "wk.err_limit": "🔒 Bu retseptning haftalik limiti tugadi ({limit}). Yangi hafta — dushanba 00:00 UTC dan.",
    "games.resource_full": "📦 {icon} ombori to'la ({cap}) — ortiqchasi yo'qoladi. Sarfla, sot yoki ustaxonada omborni kengaytir.",
    "mk.err_storage_full": "📦 Omborda joy yetmaydi: bo'sh joy {free}. Omborni ustaxonada kengaytir.",
    "mk.err_buyer_full": "📦 Xaridorning ombori to'la — bitimni hozir o'tkazib bo'lmaydi (bo'sh joy {free}).",
    "ws.recipe_storage": "Omborni {cap} gacha kengaytirish",
    "ws.done_storage": "📦 <b>Ombor kengaytirildi:</b> har bir resursdan {cap} tagacha. Bu abadiy.",
    "ws.err_storage_max": "📦 Ombor allaqachon maksimal hajmda.",
    "farm.boost_armor": "🛡 Kiber-zirh {level}-dar.: {until} UTC gacha qazib olishga +{percent}%",
    "farm.boost_station": "🛰 Jamoa stansiyasi {level}-dar.: qazib olishga +{percent}%",
    "clan.btn_station": "🛰 Jamoa stansiyasi",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>USTAXONA</b>\n"
        "..................................................\n\n"
        "🧰 Resurslaring: {stock}\n"
        "⛏ Metall — Tosh-Qaychi va duellar · 💧 Vodorod — Katta/Kichik · "
        "💎 Kristallar — Viktorina · ⚙️ Detallar — Kiber-Seyf. Kvestlar to'plam beradi.\n\n"
        "🛡 Kiber-zirh: daraja <b>{armor}/{armor_max}</b> (har daraja qazib olishga +{armor_pct}%, 30 kunga)\n"
        "🚀 Shattl: <b>{shuttle}</b> — birja komissiyasi {shuttle_fee}%, bitta buyurtmada {shuttle_qty} tagacha kotlet\n\n"
        "<i>✅ — resurs yetarli, 🔒 — hozircha yo'q. Bir bosish — va tayyor.</i>"
    ),
    "ws.shuttle_yes": "yig'ilgan",
    "ws.shuttle_no": "yig'ilmagan",
    "ws.recipe_nitro_6h": "Azotli Sovutish 6 soatga",
    "ws.recipe_nuclear_3h": "Yadroviy Tezlatish 3 soatga",
    "ws.recipe_drone_24h": "Master-Dron bir sutkaga",
    "ws.recipe_shield_24h": "Bosqinlardan qalqon bir sutkaga",
    "ws.recipe_cutlet": "Kiber-kotlet sintezi",
    "ws.recipe_armor": "Kiber-zirh {level}-dar.",
    "ws.recipe_shuttle": "Shattlni yig'ish",
    "ws.btn_shuttle_owned": "🚀 Shattl yig'ilgan",
    "ws.btn_armor_max": "🛡 Kiber-zirh: maksimum",
    "ws.btn_refresh": "🔄 Yangilash",
    "ws.btn_farm": "🚜 Fermaga",
    "ws.noop": "Allaqachon maksimumda",
    "ws.toast": "Tayyor!",
    "ws.done_nitrogen": "❄️ <b>Azotli Sovutish +40%</b> {until} UTC gacha faol.",
    "ws.done_nuclear": "☢️ <b>Yadroviy Tezlatish x5</b> {until} UTC gacha faol. Burg'ulovchilar ×3 kotlet yeydi!",
    "ws.done_drone": "🛸 <b>Master-Dron</b> robotlarni {until} UTC gacha asraydi.",
    "ws.done_shield": "🛡 <b>Bosqinlardan qalqon</b> {until} UTC gacha turadi. Resurslaring himoyada.",
    "ws.done_cutlet": "🥩 Sintez qilindi: omborga <b>+{qty} kiber-kotlet</b>. /farm da yoqilg'i quy!",
    "ws.done_armor": "🛡 <b>Kiber-zirh {level}-daraja!</b> Ferma qazib olishi: 30 kunga <b>+{percent}%</b>.",
    "ws.done_shuttle": "🚀 <b>Shattl yig'ildi!</b> Sening sotuvlaringga komissiya endi {fee}%, bitta buyurtmada {qty} tagacha kotlet. Shattl faqat seniki va abadiy.",
    "ws.err_unknown": "❌ Bunday retsept yo'q.",
    "ws.err_resources": "🔒 Yetmaydi: {kind} {need} ta kerak, senda {have} ta. O'yinlarda qazib ol!",
    "ws.err_shuttle_owned": "🚀 Shattl allaqachon yig'ilgan — har o'yinchiga bittadan.",
    "ws.err_armor_max": "🛡 Zirh allaqachon maksimal darajada ({max}).",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>BOSQINLAR</b>\n"
        "..................................................\n\n"
        "💧 Vodorod: <b>{hydrogen}</b> (bitta parvoz {fuel} turadi)\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ Himoya pozitsiyasi: <b>{stance}</b>\n\n"
        "📊 Bosqinlar: <b>{attacks}</b> (muvaffaqiyatli {attack_wins}) · qaytarilgan: <b>{holds}/{defenses}</b>\n\n"
        "<i>O'lja — faqat resurslar: nishon zaxirasining {percent}%, har resursdan ko'pi bilan {cap} ta. "
        "Tangalar, robotlar va kotletlarga tegilmaydi. Sening ishorang nishonning pozitsiyasiga qarshi — "
        "qarorga qarshi qaror. Har {cooldown} soatda bitta parvoz; revansh — bepul.</i>"
    ),
    "raid.ready_line": "Kema parvozga tayyor",
    "raid.cooldown_line": "Qayta zaryadlash: yana {minutes} daqiqa",
    "raid.shield_on": "Qalqon {until} UTC gacha faol",
    "raid.shield_newbie": "Yangi o'yinchi himoyasi (dastlabki {days} kun)",
    "raid.shield_off": "Qalqon yo'q — /workshop da yig'",
    "raid.stance_random": "tasodifiy (menyudan tanla!)",
    "raid.btn_scout": "🔭 RAZVEDKA: nishon topish",
    "raid.btn_revenge": "⚔️ Revansh: {name}",
    "raid.btn_stance": "✊ Himoya pozitsiyasi",
    "raid.btn_workshop": "🛡 Qalqon yig'ish",
    "raid.btn_refresh": "🔄 Yangilash",
    "raid.btn_back": "← Orqaga",
    "raid.btn_open": "🏴‍☠️ Bosqinlarni ochish",
    "raid.btn_again": "🏴‍☠️ Bosqinlarga",
    "raid.stance_pick": "✊ <b>Himoya pozitsiyasi</b>\nUni faqat birovning bosqini natijasi ko'rsatadi: hujumchi ishorasi sening pozitsiyangga qarshi. Vaqti-vaqti bilan o'zgartirib tur — oldindan bilsa bo'ladiganlarni talashadi.",
    "raid.stance_saved": "Pozitsiya: {stance}",
    "raid.scout": "🔭 <b>Razvedka nishonlarni topdi.</b> Parvoz {fuel} 💧 yechadi. Tanla:",
    "raid.btn_target": "🎯 {name} · resurslar ≈{total}",
    "raid.no_targets": "🔭 Razvedka hech kimni topmadi: hozir mos nishon yo'q (qalqonlar, kuldaunlar, yangilar). Keyinroq kirib ko'r.",
    "raid.pick_move": "✊ <b>Ishorang?</b> U nishonning himoya pozitsiyasiga qarshi o'ynaydi. Parvoz: −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>Revansh! Ishorang?</b> Parvoz bepul va qayta zaryadlashsiz.",
    "raid.result_win": "🏴‍☠️ <b>BOSQIN MUVAFFAQIYATLI!</b>\nNishon {name}: {move} {stance}ga qarshi.\nO'lja: <b>{loot}</b>",
    "raid.result_draw": "😐 <b>Durang.</b> Nishon {name}: {move} {stance}ga qarshi. Kema bo'sh qaytdi, yoqilg'i kuydi.",
    "raid.result_lose": "💥 <b>MUDOFAA CHIDAB BERDI.</b> Nishon {name}: {move} {stance}ga qarshi.\nNishonga tegdi: <b>{loot}</b>",
    "raid.result_footer": "<i>Resurslar — /workshop da. Qalqon javob zarbasidan himoya qiladi.</i>",
    "raid.victim_lost": "🚨 <b>Senga bosqin qilishdi!</b> {name}: {move} sening {stance} pozitsiyangga qarshi.\nYo'qotildi: <b>{loot}</b>\n\n⚔️ {hours} soat ichida revansh bepul. Qalqon — /workshop da.",
    "raid.victim_draw": "🛡 <b>Bosqin durang bilan qaytarildi.</b> {name}: {move} sening {stance} pozitsiyangga qarshi. Hech narsa yo'qotilmadi.",
    "raid.victim_held": "🛡 <b>Mudofaa chidab berdi!</b> {name}: {move} sening {stance} pozitsiyangga qarshi.\nMudofaa o'ljasi: <b>{loot}</b>",
    "raid.err_stance": "❌ Noma'lum ishora.",
    "raid.err_self": "🤨 O'zingga bosqin? Yo'q.",
    "raid.err_gone": "❌ Nishon mavjud emas.",
    "raid.err_teammate": "🤝 O'zimiznikilarni talamaymiz — bu jamoadosh.",
    "raid.err_shielded": "🛡 Nishonda qalqon bor. Boshqasini tanla.",
    "raid.err_revenge_gone": "❌ Revansh oynasi yopildi.",
    "raid.err_cooldown": "⏳ Qayta zaryadlash: yana {minutes} daqiqa.",
    "raid.err_victim_cooldown": "⏳ Bu nishon yaqinda talangan ({hours} soat tanaffus).",
    "raid.err_fuel": "💧 Vodorod yetmaydi: {need} kerak, senda {have}. U Katta/Kichikda qaziladi.",

    # ---------------- ежедневные цели ----------------
    "goal.header": (
        "🎯 <b>BUGUNGI MAQSADLAR</b>\n"
        "..................................................\n\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 Sandiq: <b>+{coins} 🪙</b> va tasodifiy resursdan <b>+{res}</b> ta\n"
        "🔥 Seriya: <b>{streak}</b> kun · ketma-ket har {every}-kun sandiqqa +{bonus} 🪙 qo'shadi\n\n"
        "<i>Maqsadlar 00:00 UTC da yangilanadi.</i>"
    ),
    "goal.status_progress": "⏳ Uchalasini bajar — sandiq seniki.",
    "goal.status_ready": "✅ <b>Barcha maqsadlar bajarildi! Sandiqni ol.</b>",
    "goal.status_claimed": "🎁 Bugungi sandiq allaqachon olingan. Ertaga — yangi maqsadlar!",
    "goal.btn_claim": "🎁 SANDIQNI OLISH",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Yangilash",
    "goal.toast": "Sandiq ochildi!",
    "goal.chest": "🎁 <b>SANDIQ OCHILDI!</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 Seriya: {streak} kun",
    "goal.err_claimed": "🎁 Bugun allaqachon olgansan.",
    "goal.err_not_done": "⏳ Hali hamma maqsad bajarilmagan.",
    "goal.win_quiz": "Viktorinada {n} raund yutish",
    "goal.win_rps": "Tosh-Qaychida {n} raund yutish",
    "goal.win_hl": "Katta/Kichikda {n} raund yutish",
    "goal.win_safe": "Kiber-Seyfni {n} marta ochish",
    "goal.play_rounds": "Istalgan o'yinda {n} raund o'ynash",
    "goal.duel": "Duel o'ynash",
    "goal.bonus": "Fermada kundalik kotletni olish",
    "goal.craft": "Ustaxonada biror narsa yig'ish",
    "goal.raid": "Bosqin qilish",
    "goal.market_deal": "Birjada bitim tuzish",
    "goal.donate": "Jamoa stansiyasiga resurs qo'shish",

    # ---------------- станция команды ----------------
    "st.header": (
        "🛰 <b>«{team}» JAMOA STANSIYASI</b>\n"
        "..................................................\n\n"
        "Daraja: <b>{level}/{max}</b> → har bir jangchiga ferma qazib olishiga <b>+{percent}%</b> "
        "(har daraja +{per_level}%)\n\n"
        "📦 Keyingi darajagacha:\n{progress}\n\n"
        "🧾 So'nggi hissalar:\n{feed}\n\n"
        "🧰 Resurslaring: {stock}\n"
        "<i>Stansiya umumiy: butun jamoa quradi, bonusni har kim oladi. Jamoadan chiqding — bonus yo'qoldi.</i>"
    ),
    "st.max_level": "🏁 Stansiya qurib bitkazildi — maksimal daraja!",
    "st.feed_empty": "hali hech kim hissa qo'shmagan — birinchi bo'l",
    "st.no_team": "🛰 Stansiyani jamoa quradi. Jamoaga qo'shil yoki o'zingnikini tuz — va birga quringlar.",
    "st.btn_find_team": "🏆 Jamoa va klanlar",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ Hammasi: {qty} {icon} {name}",
    "st.btn_refresh": "🔄 Yangilash",
    "st.btn_team": "🏆 Jamoaga",
    "st.toast": "Qo'shildi +{qty} {icon}",
    "st.level_up": "🛰 <b>Jamoa stansiyasi {level}-darajaga o'sdi!</b> Endi barcha jangchilarda ferma qazib olishiga +{percent}%.",
    "st.err_qty": "❌ Noto'g'ri miqdor.",
    "st.err_no_team": "❌ Sen jamoada emassan.",
    "st.err_max": "🏁 Stansiya allaqachon qurib bitkazilgan ({max}-daraja).",
    "st.err_resources": "🔒 Resurs yetmaydi: senda {have} ta.",

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
    "tab_passport": "📋 Pasport", "tab_farm": "🚜 Ferma", "tab_goals": "🎯 Maqsadlar", "tab_workshop": "🔧 Ustaxona",
    "tab_raids": "🏴‍☠️ Bosqinlar", "tab_market": "📈 Birja", "tab_team": "🏆 Jamoa", "tab_shop": "🏪 Do'kon", "tab_top": "👑 TOP",
    "passport": "📋 O'YINCHI PASPORTI", "coins": "🪙",
    "brain": "🧠 Intellekt darajasi", "toNext": "{n}-darajagacha: viktorinada {left} to'g'ri javob (+{reward} 🪙)",
    "farm": "🚜 KIBER-FERMA", "robots": "Robotlar (maynerlar / burg'ulovchilar)",
    "intern": "Stajyor Robotlar (1 🪙/soat, abadiy)", "activateIntern": "🚀 STAJYOR ROBOTNI FAOLLASHTIRISH",
    "internDone": "🤖 Stajyor Robot smenaga chiqdi!", "rank": "🎖 Unvon",
    "openFarm": "🏭 SHAXTANI OCHISH", "farmScene": "🏭 SENING FERMANG", "back": "← Orqaga",
    "minedVisit": "shu tashrifda qazildi", "unit_intern": "Stajyor Robot", "unit_junior": "Kichik Mayner",
    "unit_premium": "Kiber-Burg'ulovchi", "eternal": "abadiy", "fueledAll": "yoqilg'i bor",
    "fueledPart": "{b} tadan {a} tasida yoqilg'i bor", "license": "30 kunlik litsenziya",
    "emptyFarm": "Shaxta bo'sh. Stajyor Robotni faollashtir yoki do'kondan robot ol!",
    "madeBy": "O'z loyihang uchun shunday bot kerakmi? @mister_telebot ga yoz",
    "fueled": "To'ldirilgan burg'ulovchilar", "speed": "Qazib olish tezligi",
    "perHour": "{v} 🪙/soat", "fridge": "Muzlatkich", "inv": "Ombordagi kotletlar",
    "burnout": "Eng yaqin kuyish", "boosts": "Faol kuchaytirgichlar", "none": "yo'q",
    "resources": "🧰 Resurslar", "bonusPct": "Qazib olishga doimiy bonus", "shuttle": "🚀 Shattl yig'ilgan",
    "resHint": "Har bir g'alaba o'sha o'yinning resursini beradi, Cheksiz rejimda — cheklovsiz. Ularni ustaxonada sarfla.",
    "bonusReady": "🎁 KUNDALIK KOTLETNI OLISH",
    "bonusWait": "⏳ Bonus {h} soat {m} daqiqadan keyin", "bonusDone": "🎉 Kotlet omborda!",
    "team": "🏆 MENING JAMOAM", "clan": "KLAN", "teamLabel": "Jamoa", "captain": "👑 Sen sardorsan!",
    "members": "Tarkib", "noTeam": "Hozircha jamoasizsan. Bot chatida o'z jamoangni tuz yoki boshqasiga qo'shil: «🏆 JAMOA VA KLANLAR».",
    "top": "👑 EKOTIZIMNING TOP-100 BOYLARI",
    "shop": "🏪 DO'KON", "shopFarm": "🚜 FERMA UCHUN", "shopGames": "🕹️ O'YINLAR",
    "shopHint": "To'lov rasmiy Telegram Stars bilan — shu yerning o'zida, bir bosishda.",
    "paid": "🎉 To'landi! Tovar allaqachon akkauntingda.",
    "payFail": "To'lov o'tmadi. Yana urinib ko'r.",
    "oldClient": "Ilovadan xarid qilish uchun Telegram'ni yangila yoki do'konni bot chatida och.",
    "ctaNoRobots": "💤 Ferma deyarli bo'sh! Kuchliroq robot ol — 🪙 kecha-yu kunduz oqib keladi.",
    "ctaHungry": "🚨 Burg'ulovchilar och qoldi ({n} tasi yoqilg'isiz) — qazib olish to'xtab turibdi!",
    "ctaLowFuel": "⚠️ Kotletlar Burg'ulovchilarning bir kunlik ishiga ham yetmaydi.",
    "ctaShopBtn": "🛒 Do'konga",
    "footer": "O'yinlar va viktorina — bot chatida",
    "noProfile": "Profil topilmadi. Botni ochib, /start ni bos!",
    "blocked": "Akkaunt ma'muriyat tomonidan bloklangan.",
    "error": "Ma'lumotlarni yuklab bo'lmadi. Keyinroq urinib ko'r.",
    "outside": "Bu ilovani ROFL HUB Telegram-botidan och.",
    "robotsTitle": "🤖 SENING ROBOTLARING", "buyMore": "🛒 Sotib olish", "rateShort": "{v} 🪙/soat",
    "refuelOne": "🥩 1 ta quyish", "refuelAll": "⚡ Hammasini quyish", "refueled": "Quyildi: {n} 🥩",
    "res_metal_src": "Tosh-Qaychi va duellar", "res_hydrogen_src": "Katta/Kichik", "res_crystal_src": "Viktorina",
    "res_parts_src": "Kiber-Seyf", "resWhere": "qayerda qazib olinadi",
    "ws_title": "🔧 USTAXONA", "ws_hint": "O'yinlardagi resurslar kuchaytirgichlarga aylanadi. Resurs yetarli bo'lsa — «Yasash»ni bos.",
    "ws_craft": "Yasash", "ws_owned": "✅ Allaqachon bor", "ws_crafted": "Tayyor! Kuchaytirgich allaqachon ishlayapti.",
    "ws_armor": "🛡 Kiber-zirh", "ws_armorLvl": "daraja {l}/{m} · har darajaga +{p}%, 30 kunga",
    "ws_shuttleOn": "🚀 Shattl yig'ilgan: birja komissiyasi {fee}%", "ws_shuttleOff": "🚀 Shattl yig'ilmagan: birja komissiyasi {fee}%",
    "eff_nitrogen": "barcha robotlar qazib olishiga +40%", "eff_nuclear": "qazib olish ×5, Burg'ulovchilar ×3 kotlet yeydi",
    "eff_drone": "robotlar eskirmaydi", "eff_shield": "senga bosqin qilib bo'lmaydi",
    "eff_cutlet": "omborga 1 kiber-kotlet (qimmat: yoqilg'i do'konda arzonroq)", "eff_armor": "har darajaga qazib olishga +10%, 30 kunga",
    "eff_storage": "resurslar uchun ko'proq joy — abadiy",
    "eff_shuttle": "faqat seniki: sotuvlaringga 5% komissiya va buyurtmalar 500 kotletgacha — abadiy",
    "raid_title": "🏴‍☠️ BOSQINLAR", "raid_how": "📖 Bu qanday ishlaydi",
    "raid_rule1": "Sen ishora tanlaysan, nishonda esa oldindan himoya pozitsiyasi qo'yilgan. Natijani tosh-qaychi-qog'oz hal qiladi: bu lotereya emas, qarorlar dueli.",
    "raid_rule2": "G'alaba: nishonning har bir resursidan {pct}% olasan, har resursdan {cap} tagacha. Muvaffaqiyatsizlik: nishonga o'zingnikidan {fpct}% berasan, {fcap} tagacha. Durang: yoqilg'i kuydi.",
    "raid_rule3": "Faqat resurslar talanadi. Tangalar, robotlar va kotletlar to'liq xavfsiz. Yangi o'yinchilar {days} kun himoyada, jamoadoshlarga tegib bo'lmaydi.",
    "raid_rule4": "Parvoz {fuel} 💧 vodorod turadi, keyingisi — {cd} soatdan keyin. Senga bosqin qilishsa, {rh} soat davomida revansh bepul.",
    "raid_fuel": "💧 Vodorod", "raid_ready": "🚀 Kema parvozga tayyor", "raid_cooldown": "⏳ Qayta zaryad: {m} daqiqa",
    "raid_shieldOn": "🛡 Qalqon {t} gacha", "raid_shieldNewbie": "🛡 Yangi o'yinchi himoyasi", "raid_shieldOff": "🛡 Qalqon yo'q — ustaxonada yasa",
    "raid_stance": "✊ SENING HIMOYA POZITSIYANG", "raid_stanceHint": "U bilan begona bosqinlarni kutib olasan. Vaqti-vaqti bilan almashtir — oldindan bilinadiganlarni ko'proq talashadi.",
    "raid_stanceNone": "Pozitsiya tanlanmagan — tasodifiy bo'ladi", "raid_stanceSaved": "Pozitsiya saqlandi",
    "raid_stats": "Bosqinlar: {a} (muvaffaqiyatli: {w}) · qaytarildi: {d} tadan {h} tasi",
    "raid_scout": "🔭 RAZVEDKA: nishon topish", "raid_targets": "🎯 Nishonni tanla", "raid_res": "resurslar ≈{n}",
    "raid_noTargets": "Hozir mos nishon yo'q: qalqonlar, qayta zaryad, yangi o'yinchilar. Keyinroq kirib ko'r.",
    "raid_pickMove": "✊ {name} pozitsiyasiga qarshi ishorang", "raid_revenge": "⚔️ REVANSH", "raid_revengeBtn": "⚔️ Javob qaytarish: {name}",
    "raid_win": "🏴‍☠️ Bosqin muvaffaqiyatli!", "raid_draw": "😐 Durang — kema bo'sh qaytdi",
    "raid_lose": "💥 Himoya bardosh berdi", "raid_vs": "{m} vs {s}", "raid_loot": "O'lja: {l}", "raid_lost": "Nishonga berildi: {l}",
    "rock": "🪨 Tosh", "scissors": "✂️ Qaychi", "paper": "📄 Qog'oz",
    "mk_title": "📈 BIRJA", "mk_stats": "Buyurtmalar: {o} · kotletlar: {c} · eng yaxshi narx: {b} 🪙",
    "mk_feeLine": "Sotuvdan {f}% komissiya yondiriladi — inflyatsiyadan himoya", "mk_inv": "🥩 Omboringda: {n}",
    "mk_offers": "🛒 TAKLIFLAR", "mk_empty": "Hozircha takliflar yo'q — birinchi bo'lib o'zingnikini qo'y!",
    "mk_offer": "{q} 🥩 × {p} 🪙", "mk_buyHow": "Nechta olasan?", "mk_all": "Hammasi: {q}",
    "mk_sellTitle": "💰 KOTLET SOTISH", "mk_qty": "Nechta kotlet", "mk_price": "Donasining narxi, 🪙",
    "mk_preview": "Bitim {t} 🪙 · olasan {g} 🪙 · yonadi {f} 🪙", "mk_sell": "Birjaga qo'yish",
    "mk_limits": "Buyurtmada {q} tagacha kotlet, {o} tagacha ochiq buyurtma",
    "mk_my": "📋 BUYURTMALARIM", "mk_cancel": "Olib tashlash", "mk_bought": "{q} 🥩 sotib olindi: {t} 🪙",
    "mk_listed": "Buyurtma qo'yildi! Sotib olishganda xabar beraman.", "mk_cancelledMsg": "Buyurtma olib tashlandi, kotletlar omborga qaytdi",
    "as_cutlet": "Kotletlar", "as_metal": "Metall", "as_hydrogen": "Vodorod", "as_crystal": "Kristallar", "as_parts": "Detallar",
    "mk_index": "📈 BIRJA INDEKSI", "mk_chart": "📊 7 KUNLIK NARX", "mk_noTrades": "Hali bitimlar bo'lmagan — birinchi bo'l!",
    "mk_avg": "Haftalik o'rtacha narx: {p} 🪙 · sotildi: {v}", "mk_asks": "🛒 SOTISHADI", "mk_bids": "🙋 SOTIB OLISHADI",
    "mk_noBids": "Hozircha sotib olish so'rovlari yo'q", "mk_sellTo": "Sotish", "mk_sellHow": "Nechta sotasan?",
    "mk_bidTitle": "🙋 SOTIB OLISH SO'ROVI", "mk_bidHint": "Tangalar bitimgacha so'rovda muzlatiladi. So'rovni olib tashlasang — tangalar qaytadi.",
    "mk_bid": "So'rov qo'yish", "mk_bidPreview": "{t} 🪙 muzlatiladi", "mk_have": "Senda: {n}",
    "mk_floor": "Kotlet {p} 🪙 dan arzon bo'lmaydi: do'kondan Stars evaziga yoqilg'i har doim foydaliroq",
    "mk_side_sell": "sotaman", "mk_side_buy": "sotib olaman", "mk_listedBid": "So'rov qo'yildi! Tangalar bitimgacha muzlatildi.",
    "mk_sold": "{q} sotildi, komissiyadan keyin {g} 🪙 olindi", "mk_shuttleNote": "🚀 Shattling: sotuvlaringga {f}% komissiya",
    "sw_title": "🔄 RESURS ALMASHUVI", "sw_hint": "Ortiqchasini ber — keraklisini ol. Tangasiz va komissiyasiz.",
    "sw_give": "Siz berasiz", "sw_want": "Siz olmoqchisiz", "sw_qty": "Nechta", "sw_create": "Almashuv taklif qilish", "sw_take": "Almashish",
    "shop_info": "ℹ️ Har bir mahsulot nima beradi", "sw_youGet": "Sizga beriladi", "sw_youGive": "Evaziga berasiz",
    "sw_takeBtn": "Almashish — {x} berish", "sw_mineLine": "Siz {g} berasiz → {w} olmoqchisiz",
    "sw_qtyErr": "Ikkala maydonda ham noldan katta miqdor kiriting",
    "sw_empty": "Hozircha almashuv takliflari yo'q", "sw_mine": "Mening takliflarim", "sw_done": "Almashuv amalga oshdi!",
    "sw_created": "Taklif qo'yildi, resurslar ajratib qo'yildi", "sw_cancelled": "Taklif olib tashlandi, resurslar qaytdi",
    "ws_armorUntil": "🛡 Zirh {t} gacha amal qiladi",
    "tab_friends": "🤝 Do'stlar", "ref_title": "🤝 DO'STLARNI TAKLIF QIL",
    "ref_rules": "Har bir do'st uchun darhol +{s} 🪙. Do'st {r} raund o'ynasa — yana +{q} 🪙 va {c} 🥩 kiber-kotlet.",
    "ref_copy": "📋 Nusxa olish", "ref_copied": "Havola nusxalandi!", "ref_share": "📤 Ulashish",
    "ref_stats": "📊 SENING BAZANG", "ref_invited": "taklif qilingan", "ref_qualified": "faol", "ref_earned": "ishlab topilgan",
    "ref_cutlets": "🥩 Faol do'stlar uchun olingan kotletlar: {n}", "ref_top": "🏆 KIMNING DO'STLARI KO'P",
    "ref_topHint": "✅ — faol do'stlar (30 raund o'ynagan), 👥 — barcha taklif qilinganlar", "ref_empty": "Reyting hozircha bo'sh — birinchi bo'l!",
    "wk_title": "🔥 HAFTA RETSEPTLARI", "wk_hint": "Vaqtinchalik retseptlar: hab qaroriga ko'ra paydo bo'ladi va yo'qoladi. Yig'ishga ulgur!",
    "wk_left": "bu hafta qolgan yig'ishlar: {m} tadan {n} ta", "st_cap": "📦 Ombor: har bir resursdan {c} tagacha — ortiqcha o'lja yo'qoladi",
    "st_title": "🛰 JAMOA STANSIYASI", "st_level": "Daraja: {l} / {m}", "st_bonus": "har bir jangchiga qazib olishga +{p}%",
    "st_next": "{n}-darajaga har resursdan {c} ta kerak", "st_max": "🏁 Stansiya qurib bitkazildi!",
    "st_feed": "🧾 So'nggi hissalar", "st_feedEmpty": "Hali hech kim hissa qo'shmagan — birinchi bo'l",
    "st_donate": "Hissa qo'shish", "st_all": "Hammasi", "st_done": "Qo'shildi!",
    "st_hint": "Butun jamoa quradi, bonusni har kim oladi. Jamoadan chiqding — bonus yo'qoldi.",
    "st_off": "Stansiya vaqtincha texnik xizmatda",
    "goals_title": "🎯 BUGUNGI MAQSADLAR", "goals_chest": "🎁 Uchchalasi uchun sandiq: +{c} 🪙 va tasodifiy resursdan +{r}",
    "goals_streak": "🔥 Seriya: {s} kun · ketma-ket har {e}-kun +{b} 🪙", "goals_claim": "🎁 SANDIQNI OLISH",
    "goals_claimed": "🎁 Bugungi sandiq olindi. Ertaga — yangi maqsadlar!", "goals_reset": "Maqsadlar 00:00 UTC da yangilanadi",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · seriya {s} kun",
    "featureOff": "⚙️ Bo'lim texnik xizmatda", "done": "Tayyor!", "loading": "⏳ Yuklanmoqda…",
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
    "market": "📈 Kotlet birjasi: sotib olish yoki sotish",
    "sell": "💰 Kotlet sotish: /sell soni narxi",
    "my_stats": "📊 Statistikam",
    "faq": "📚 Ko'p so'raladigan savollar",
    "rules": "📜 Foydalanuvchi shartnomasi",
    "paysupport": "🛟 To'lovlar bo'yicha yordam",
    "workshop": "🔧 Ustaxona: resurslardan kuchaytirgichlar",
    "raid": "🏴‍☠️ Bosqinlar: razvedka va revansh",
    "goals": "🎯 Kundalik maqsadlar va sandiq",
    "station": "🛰 Jamoa stansiyasi: umumiy loyiha",
}
