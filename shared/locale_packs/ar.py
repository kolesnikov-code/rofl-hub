"""Арабская (современный стандартный) локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> عملات (при числе — значок 🪙 после числа: 100 🪙)
# Младший Майнер -> روبوت التعدين
# Кибер-Бурильщик -> الحفّار السيبراني (мн.: الحفّارات السيبرانية)
# кибер-котлета -> كفتة سيبرانية (кратко: كفتة)
# Холодильник -> الثلاجة
# склад (инвентарь) -> المخزون
# ферма -> المزرعة (Кибер-ферма -> المزرعة السيبرانية)
# Ядерный Разгон x5 -> التسريع النووي x5
# Азотное Охлаждение +40% -> التبريد النيتروجيني +40%
# Мастер-дрон -> الدرون المايسترو
# Кибер-Сейф -> الخزنة السيبرانية
# Мега-Клан -> ميغا-كلان
# Безлимит -> إزالة حدود الفوز
# дуэли -> مبارزات (ставка -> رهان, банк -> صندوق الرهان, стол -> طاولة, жест -> حركة)
# битвы -> المعارك
# квесты -> المهام (мهمة)
# уровень интеллекта -> مستوى الذكاء
# викторина -> الكويز; КНБ -> حجر-ورقة-مقص
# команда -> فريق; клан -> كلان; банда -> الشلة
# ресурсы (волна 22.10): Металл -> المعدن; Водород -> الهيدروجين; Кристаллы -> البلّورات; Детали -> القطع
# Мастерская -> الورشة; Кибер-броня -> الدرع السيبراني; Шаттл -> المكوك
# Налёт -> الغارة (мн. الغارات); вылет -> طلعة; Стойка обороны -> وضعية الدفاع
# Разведка -> الاستطلاع; Реванш -> الثأر; Щит (от налётов) -> ترس الحماية (кратко: الترس)
# Сундук -> الصندوق; Серия -> السلسلة; Станция команды -> محطة الفريق; трофей/добыча налёта -> الغنيمة

BUTTONS = {
    "main_menu": "📱 القائمة الرئيسية",
    "profile": "👤 ملفي الشخصي",
    "farm": "🚜 مزرعتي",
    "games_zone": "🕹️ منطقة الألعاب",
    "teams": "🏆 الفرق والكلانات",
    "shop": "🏪 المتجر",
    "shop_cat_farm": "🚜 للمزرعة",
    "shop_cat_games": "🕹️ الألعاب",
}

STRINGS = {
    "quest.btn_answer_app": "🔐 أدخل الإجابة في التطبيق",
    'duel.invite_msg': '⚔️ <b>{name}</b> يتحداك في مبارزة!\nالرهان {stake} 🪙، والفائز يحصل على {payout} 🪙. التحدي صالح لمدة {hours} ساعة.',
    'duel.invite_btn': '⚔️ قبول التحدي',
    'duel.invite_gone': '⌛ هذا التحدي لم يعد صالحًا — تم قبوله أو إلغاؤه أو انتهت مدته.',
    'duel.invite_self': '😅 هذا تحديك أنت — أرسل الرابط إلى صديق.',
    'team.err_not_squad': '⚠️ يمكن توسيع الفرقة فقط.',
    'team.err_not_captain': '⚠️ القائد وحده يمكنه ذلك.',
    "quest.epic_locked": "⭐ الملاحم قصص كبيرة تزيد على 20 دقيقة، وتُفتح مع ⚡ «بلا حدود».",
    "quest.locked": "🔒 أنهيت مهامك الجديدة الـ {n} لهذا اليوم. تُفتح البقية عند 00:00 UTC، أو فعّل ⚡ «بلا حدود». يمكن إعادة المهام المكتملة.",
    # 27.10: «чат — дверь и почтальон», вся игра в приложении
    "app.moved": "🎮 هذا القسم أصبح الآن في تطبيق اللعبة — هناك أسهل وأجمل. اضغط الزر 👇",
    "app.keyboard_gone": "🧹 أزلنا الأزرار القديمة في الأسفل: اللعبة كلها الآن في التطبيق. يمكنك أيضًا فتحه بزر «🎮 ROFL HUB» بجانب حقل الكتابة.",
    "start.console_app": "🚀 <b>جاهز!</b> اللعبة كلها في التطبيق: اضغط الزر في الأسفل. ولاحقًا يمكنك فتحه دائمًا بزر «🎮 ROFL HUB» بجانب حقل الكتابة.",
    "start.welcome_back_app": "👋 <b>أهلًا بعودتك، @{username}!</b> تقدّمك محفوظ — افتح اللعبة 👇",
    "menu.app": "📱 <b>ROFL HUB</b>\nاللعبة كلها في التطبيق 👇\n\n<b>في الدردشة:</b>\n• /invite — ادعُ صديقًا\n• /transfer — أرسل عملات\n• /faq — الأسئلة الشائعة\n• /rules — اتفاقية المستخدم\n• /paysupport — مساعدة في المدفوعات\n• /delete_account — حذف الحساب",
    # TODO(перевод 26.10): история — пока по-английски
    "hist.mining": "⛏ Farm mining",
    "hist.game_win": "🎮 Game win",
    "hist.game_loss": "🎮 Game loss",
    "hist.quiz_level_up": "🧠 New brain level",
    "hist.duel_stake": "⚔️ Duel stake",
    "hist.duel_win": "⚔️ Duel win",
    "hist.duel_refund": "⚔️ Duel stake refund",
    "hist.market_buy": "📈 Market purchase",
    "hist.market_sell": "📈 Market sale",
    "hist.market_bid": "📈 Buy order (frozen)",
    "hist.market_bid_refund": "📈 Buy order refund",
    "hist.market_escrow": "📈 Listed on the market",
    "hist.market_refund": "📈 Taken off the market",
    "hist.swap_escrow": "🔁 Swap: listed",
    "hist.swap_give": "🔁 Swap: given",
    "hist.swap_get": "🔁 Swap: received",
    "hist.swap_refund": "🔁 Swap: refund",
    "hist.transfer_in": "🔄 Transfer from a player",
    "hist.transfer_out": "🔄 Transfer to a player",
    "hist.admin_gift": "🎁 Gift from the team",
    "hist.prize": "🏆 Prize",
    "hist.daily_chest": "🎁 Daily goals chest",
    "hist.daily_case": "🕵️ Case of the day",
    "hist.squad_create": "🛡 Squad created",
    "hist.squad_upgrade": "🛡 Squad expanded into a team",
    "hist.quest_reward": "🗺 Quest reward",
    "hist.quest_hint": "🗺 Quest hint",
    "hist.quiz_hint": "🧠 Quiz hint",
    "hist.shop_coins": "🏪 Coin pack for ★",
    "hist.auction_bid": "🔨 Auction bid",
    "hist.auction_refund": "🔨 Auction bid refund",
    "hist.craft": "🔧 Workshop",
    "hist.weekly": "🔥 Recipe of the week",
    "hist.horse_buy": "🐎 Horse purchase",
    "hist.drone_buy": "🤖 Combat drone purchase",
    "hist.team_create": "🏆 Team creation",
    "hist.referral_qualified": "🤝 Active friend reward",
    "hist.signup_bonus": "👋 Welcome bonus",
    "hist.account_deleted": "🗑 Account deletion",
    "hist.raid_loot": "🏴‍☠️ Raid loot",
    "hist.raid_loss": "🏴‍☠️ You were raided",
    "hist.raid_fail": "🏴‍☠️ Failed raid",
    "hist.raid_defense": "🛡 Defense trophy",
    "hist.raid_fuel": "🏴‍☠️ Raid fuel",
    "hist.exp_fuel": "🗺 Run supplies",
    "hist.exp_gear": "🗺 Squad contribution",
    "hist.exp_refund": "🗺 Supplies refund",
    "hist.station_donate": "🛰 Station contribution",
    "hist.battle_entry": "⛏ Mine battle entry",
    "hist.mine": "⛏ Mine yield",
    "hist.tools": "🔬 Tool kit",
    "hist.tech": "🔬 Technology",
    "hist.shuttle_charge": "🚀 Shuttle charge",
    "hist.team_help_give": "🤝 Help for a teammate",
    "hist.team_help_get": "🤝 Help from a teammate",
    "gear.err_ref_taken": "The friends suit has already been claimed — one per account.",
    "gear.err_ref_need": "🔒 You need {n} active friends, you have {have}.",
    "pass.delivered": "🎟 Premium pass for season {season} is active! Rewards are in the app: «Character» → «Pass».",
    "pass.err_owned": "You already have this season's pass.",
    "pass.err_nothing": "Nothing to claim yet — earn some pass XP.",
    "skin.delivered": "✨ The “{name}” skin is yours: copy #{serial} of {edition}. Wear it in Character → Garage.",
    "skin.err_max": "✨ This skin is already fully tempered.",
    "skin.err_equipped": "✨ Take off the skin you want to feed into tempering first.",
    "skin.err_self": "✨ A skin can't absorb itself.",
    "skin.err_not_yours": "✨ This skin isn't yours.",
    "skin.err_sold_out": "✨ This skin's edition is sold out.",
    "skin.err_unknown": "✨ There is no such skin.",
    "gift.err_taken": "🎁 You've already claimed this gift.",
    "gift.err_limit": "🎁 You've already reached this season's limit for such gifts.",
    "gift.err_gone": "🎁 This gift is no longer available.",
    "gear.err_unknown": "🧥 There is no such part.",
    "gear.err_none": "🧥 You don't have this part.",
    "gear.err_max": "🧥 This part is already at the top level.",
    "gear.err_coins": "🪙 Not enough coins: you need {need}.",
    "gear.err_xp": "🧥 This part hasn't seen enough yet: XP {have} of {need}. Wear it — wins, duels, raids and expeditions count.",
    "gear.err_tech": "🔬 This level needs the {icon} technology at level {n} in the Lab.",
    "gear.err_exo_missing": "💠 Fusion needs all 30 Improved parts: you have {have} of {need}.",
    "hist.gear_upgrade": "⬆️ Suit part upgrade",
    "hist.gear_exo": "💠 Nano exo-armour fusion",
    "hist.suit_miner": "⛏ Miner suit bonus",
    "hist.other": "• Other",
    "hist.src_gift": "🎁 Gift from the team",
    "hist.src_battle": "🏟 Battle or event",
    "hist.src_exp": "🗺 World map run",
    # TODO(перевод 26.10): награды в личку и аукционы — пока по-английски
    "rn.place": "🏁 <b>Results of “{title}”</b>: you took place {place}!",
    "rn.all": "🏁 <b>Results of “{title}”</b>: thanks for taking part!",
    "rn.got": "🎁 Credited: <b>{r}</b>",
    "rn.manual": "🎁 Prize: <b>{r}</b> — the team will contact you to hand it over.",
    "rn.mine": "⛏ Mine #{mine} belongs to your team for {hours} h — every member gets its resource each hour.",
    "rn.where": "Everything is already in your storage and balance — check the game app.",
    "auc.err_none": "🚨 Lot not found.",
    "auc.err_closed": "🚨 This lot is already closed.",
    "auc.err_funds": "❌ You need {need} 🪙, you have {have} 🪙.",
    "auc.err_step": "❌ The bid must be a multiple of the {step} 🪙 step.",
    "auc.outbid": "⚠️ You were outbid on “{title}” (price is now {price} 🪙). {refund} 🪙 are back on your balance.",
    "auc.bid_ok": "💥 Bid accepted! Lot price: {price} 🪙.",
    "profile.btn_app": "📱 OPEN THE APP",
    "exp.err_no_peeks": "No fork scouting left: a squad gets as many as its leader has 🛰 spies and 🔭 Scouting levels.",
    "exp.err_peeked": "This fork is already scouted.",
    # TODO(перевод 28.10): экспедиции и дроны — пока английский
    "exp.err_closed": "This target is already closed.",
    "exp.err_scope": "This target isn't for this kind of squad — check the ranking.",
    "exp.err_already": "You're already heading to this target.",
    "exp.err_busy": "You already have an active solo run — wait for its results.",
    "exp.err_team_busy": "Your team is already gathering or marching to another target.",
    "exp.err_late": "Too late: the trip is longer than the time left.",
    "exp.err_hydrogen": "You need 💧 {need}, you have {have}.",
    "exp.err_no_team": "A team expedition — join a team first.",
    "exp.err_no_cutlets_needed": "Only a Mega-Clan takes cutlets as provisions.",
    "exp.err_retry": "A teammate is opening the gathering — tap again.",
    "exp.err_departed": "The squad has already set out.",
    "exp.err_full": "There's enough of this gear already.",
    "exp.err_battery": "No 🔋 batteries — craft them in the workshop.",
    "exp.err_cutlet": "No 🥩 cutlets in storage.",
    "exp.err_not_member": "This isn't your squad.",
    "exp.err_no_fork": "There's no fork to vote on right now.",
    "ws.recipe_drone_guard": "Build a Guard drone",
    "ws.recipe_drone_attack": "Build an Attack drone",
    "ws.recipe_drone_spy": "Build a Spy drone",
    # ---------------- общее ----------------
    "common.no_profile": "⚠️ لم يتم العثور على ملفك. اضغط /start للتسجيل.",
    "common.btn_menu": "💿 القائمة الرئيسية",
    "common.blocked": "🚫 تم حظر حسابك من قِبل إدارة ROFL HUB.",
    "common.feature_off": "⚙️ هذا القسم تحت الصيانة مؤقتًا. عُد بعد قليل!",
    "common.maintenance": "🛠 ROFL HUB في صيانة سريعة. سنعود قريبًا — عملاتك وتقدمك في أمان!",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>أهلًا بعودتك يا @{username}!</b>\nتقدّمك محفوظ في مكانه. لوحة التنقل في أسفل الشاشة.",
    "start.btn_continue": "🛸 متابعة",
    "start.btn_cutlet": "ما هي الكفتة السيبرانية؟🥩🤔",
    "start.btn_fight": "احكِ بسرعة ثم إلى المعركة!",
    "start.console": "🚀 <b>تم تفعيل لوحة التحكم! استخدم الأزرار في أسفل الشاشة.</b>",
    "start.intro1": (
        "👋 <b>أهلًا! أنا ROFL HUB BOT، البوت الرئيسي لمنظومة ألعاب ROFL HUB. "
        "مركز الترفيه والمعرفة من الجيل الجديد!</b>\n\n"
        "<b>هنا يمكنك:</b>\n"
        "🎮 لعب ألعاب الدردشة ضد البوت وضد لاعبين آخرين\n"
        "💸 كسب عملة اللعبة بالانتصارات، أو إطلاق مزرعة تعدّنها على مدار الساعة\n"
        "🤼 إنشاء فريق واقتحام قمة التصنيف\n"
        "🏆 ترقية فريقك إلى كلان والمنافسة في التصنيف الدولي\n"
        "💰 الفوز بجائزة المليون عملة مع شلتك\n\n"
        "<b>هذا البوت يستطيع:</b>\n"
        "🎮 عرض قائمة بكل ألعاب وقنوات ومواقع ROFL HUB\n"
        "⚡ منح العملات في الألعاب ومعارك الفرق والكلانات وعلى الإنجازات والنشاط والدعوات\n"
        "🔄 تحويل عملات اللعبة إلى لاعب آخر في ROFL HUB\n"
        "🚀 بيع المعزّزات والألقاب والرتب والمزيد...\n\n"
        "<i>اضغط «متابعة» وسأحكي لك المزيد 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>استلم مكافآتك الأولى على التسجيل!</b>\n"
        "..................................................\n"
        "💸 حصلت على: <b>{balance} 🪙</b>\n"
        "🥩 حصلت على: <b>{cutlets} كفتة سيبرانية</b>\n"
        "..................................................\n"
        "هذه مكافأتك الترحيبية على انضمامك إلى نادي ROFL HUB.\n\n"
        "🔒 <i>تُمنح المكافأة مرة واحدة فقط عند التسجيل.</i>\n\n"
        "يمكن إنفاق العملات بطرق كثيرة — فهي أساس اقتصاد المركز. حافظ عليها...\n\n"
        "⁉️ <b>لكن لا بد أن سؤالًا خطر ببالك:</b> ما هذه الكفتة؟ ومَن سأُطعم بها؟"
    ),
    "start.intro3": (
        "<b>أولًا، لماذا عملات اللعبة بهذه الأهمية؟</b>\n\n"
        "العملات هي أساس كل التجارة والمنافسات والمشتريات في <b>ROFL HUB</b>. "
        "إنها تقريبًا عملة اللعب الوحيدة في العالم التي يمكنك تعدينها مجانًا!\n"
        "..................................................\n"
        "<b>هناك طرق كثيرة لكسبها:</b>\n"
        "- دعوة الأصدقاء عبر رابط الدعوة الخاص بك\n"
        "- الفوز في الألعاب ضد البوت\n"
        "- الفوز في المبارزات ضد لاعبين آخرين\n"
        "- المشاركة في معارك الفرق والكلانات\n"
        "- استلام مكافآت الدخول اليومي والمهام\n"
        "- امتلاك روبوت يعدّن العملات على مدار الساعة (روبوت التعدين / الحفّار السيبراني)\n"
        "..................................................\n"
        "<b>إذا امتلكت روبوتًا من المستوى الثاني (الحفّار السيبراني) — فيجب إطعامه كل يوم. "
        "وهنا يأتي دور الكفتة السيبرانية: وقود التعدين الآلي، "
        "ويُمنح مجانًا كل يوم! مهمتك بسيطة — ادخل وأطعم روبوتك.</b>\n\n"
        "إن لم تُطعمه في الوقت المناسب — تنفد طاقة الروبوت ويتوقف التعدين.\n\n"
        "روبوت التعدين (المستوى الأول) لا يحتاج إلى وقود. "
        "مهم! أي روبوت يُشترى لمدة 30 يومًا — بعدها اشترِه من جديد أو احصل على الدرون المايسترو. "
        "ستفهم كل شيء مع الوقت:) لا داعي للتشتت الآن.\n\n"
        "أريد أن أحكي لك المزيد عن <b>ROFL HUB</b> لتفهم كيف تسير الأمور هنا.\n\n"
        "🛑 <b>هذه آخر رسالة في تعارفنا. بعدها إلى المعركة مباشرة:)</b>"
    ),
    "start.intro4": (
        "<b>باختصار شديد. ROFL HUB هو:</b>\n"
        "- ألعاب دردشة لكل الأذواق\n"
        "- إمكانية إنشاء فريق (حتى 50 لاعبًا)\n"
        "- إمكانية ترقيته إلى كلان (حتى 1000 لاعب)\n"
        "- معارك فرق وكلانات على جوائز\n"
        "- آلاف اللاعبين حول العالم، وقد يكون أصدقاؤك الجدد بينهم!\n"
        "..................................................\n"
        "<b>كما وعدتك، هذه هي الرسالة الختامية. والآن إلى المعركة! أوامر مفيدة:</b>\n\n"
        "/menu — تحكم سريع في كل الميزات\n"
        "/games — قائمة بكل الألعاب\n"
        "/faq — الأسئلة الشائعة\n"
        "/rules — اتفاقية الاستخدام\n"
    ),

    # ---------------- меню и игровая зона ----------------
    "menu.text": (
        "📱 <b>القائمة الرئيسية لمنظومة ROFL HUB</b>\n"
        "..................................................\n"
        "👤 <b>الملف الشخصي والجواز:</b>\n"
        "• /start — بدء التعارف وتسجيل حساب\n"
        "• /profile — جوازك ورصيدك وفريقك في الوقت الفعلي\n"
        "• /my_stats — إحصاءاتك التاريخية لآخر 30 يومًا\n\n"
        "🚜 <b>المزرعة السيبرانية والأتمتة:</b>\n"
        "• /farm — مركز الوقود: التزويد وسرعة إنتاج الروبوتات\n"
        "• /shop — المتجر: شراء الروبوتات والكفتات وترقيات المركز\n\n"
        "🕹️ <b>غرفة الألعاب:</b>\n"
        "• /games — مركز كل الألعاب ضد البوت\n"
        "• /quiz — كويز السرعة: 30 ثانية للإجابة، مستويات ومكافآت\n"
        "• /duel — مبارزات 1 ضد 1 مع لاعبين حقيقيين: طاولات 10/100/1000\n"
        "• /quests — المهام: قصص بوليسية وكوميدية وألغاز مع جوائز\n"
        "• /rps, /high_low, /safe — ألعاب سريعة على العملات\n\n"
        "👥 <b>إدارة الفرق:</b>\n"
        "• /create_team — سجّل فريقك الخاص مقابل 100,000 🪙\n"
        "• /my_team — لوحة الشلة وقائمة الزملاء مع مستويات 🧠\n"
        "• /all_teams — روليت فرق عشوائية\n\n"
        "💸 <b>المال والأصدقاء:</b>\n"
        "• /invite — رابط الدعوة الخاص بك: +500 🪙 عن كل صديق نشط\n"
        "• /transfer — تحويل عملات إلى لاعب آخر\n\n"
        "📚 <b>الدليل والقواعد:</b>\n"
        "• /faq — الدليل الكامل للمنظومة (يُفتح في Mini App)\n"
        "• /rules — اتفاقية الاستخدام\n"
        "..................................................\n"
        "<i>⚙️ استخدم لوحة الألعاب الثابتة ذات العمودين في أسفل الشاشة للتنقل الفوري بين الأقسام!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>أهلًا بك في منطقة ألعاب ROFL HUB!</b>\n"
        "..................................................\n"
        "هنا يمكنك تحدي البوت في مبارزات سريعة أو خوض اختبار الذكاء السريع "
        "لتربح الجائزة الكبرى — أو تخسر رصيدك!\n\n"
        "💸 الفوز يمنحك: <b>+2 🪙</b> (الخزنة السيبرانية: <b>+5</b>)\n"
        "💀 الخسارة تخصم: <b>-1 🪙</b>، والتعادل لا يخصم شيئًا\n"
        "🧠 في الكويز مؤقّت 30 ثانية ومستويات ذكاء: المستوى الأول — 10 إجابات صحيحة و<b>+100 🪙</b>، "
        "وكل مستوى تالٍ أطول بعشر إجابات، لكن المكافأة تزيد بمقدار 100 أيضًا!\n"
        "..................................................\n"
        "👇 <b>اضغط على زر بالأسفل لبدء جولة فورًا:</b>"
    ),
    "menu.btn_quiz": "🧠 الكويز",
    "menu.btn_rps": "🪨 حجر-ورقة-مقص",
    "menu.btn_hl": "📈 أعلى/أقل",
    "menu.btn_safe": "🔐 الخزنة السيبرانية",
    "menu.btn_duel": "⚔️ مبارزات 1 ضد 1",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "جوازك ومزرعتك وفريقك وقائمة الأثرياء — على شاشة نيون واحدة. "
        "ويمكنك استلام كفتة اليوم من هناك مباشرة!\n\n"
        "👇 اضغط الزر:"
    ),
    "app.btn": "🎮 افتح Mini App",
    "app.unavailable": "⚙️ لا يزال Mini App يتصل بخوادم المنظومة. عُد بعد قليل!",
    "faq.teaser": (
        "📚 <b>دليل منظومة ROFL HUB</b>\n"
        "..................................................\n"
        "الخلاصة بسرعة:\n"
        "🚜 الروبوتات تعدّن العملات على مدار الساعة: روبوت التعدين — 5/ساعة بلا وقود، "
        "الحفّار السيبراني — 10/ساعة، وكل حفّار يأكل كفتته السيبرانية الواحدة الخاصة به كل يوم. "
        "كل الروبوتات تعيش 30 يومًا (الدرون المايسترو يجمّد الاستهلاك).\n"
        "🧠 الكويز: 30 ثانية للإجابة، ومستويات ذكاء بمكافآت متزايدة.\n"
        "⚔️ مبارزات مع لاعبين حقيقيين على طاولات 10/100/1000 🪙.\n"
        "🏆 فرق حتى 50 مقاتلًا (ميغا-كلان — حتى 1000) ومعارك موسمية بجوائز للجميع.\n"
        "..................................................\n"
        "👇 <b>الدليل الكامل بكل التفاصيل — بضغطة زر:</b>"
    ),
    "faq.btn_open": "📖 افتح الدليل الكامل",
    "rules.teaser": (
        "📜 <b>اتفاقية استخدام ROFL HUB</b>\n"
        "..................................................\n"
        "الأهم باختصار:\n"
        "🪙 العملات وكل عناصر اللعبة أدوات ترفيهية افتراضية: "
        "ليست نقودًا ولا تُستبدل بأموال حقيقية.\n"
        "💫 المشتريات — فقط عبر Telegram Stars الرسمية؛ السلع الرقمية تصل "
        "فورًا، وعند فشل التسليم تُعاد Stars تلقائيًا.\n"
        "🛡️ لا نجمع أرقام الهواتف ولا الموقع الجغرافي ولا البيانات الشخصية.\n"
        "🤝 يُمنع السبّ والتلاعب والحسابات المتعددة — وقد تؤدي المخالفة إلى الحظر.\n"
        "..................................................\n"
        "👇 <b>النص الكامل للاتفاقية وإخلاء المسؤولية — بضغطة زر:</b>\n"
        "<i>⚖️ باستخدامك البوت فإنك تؤكد موافقتك على الشروط.</i>"
    ),
    "rules.btn_open": "📜 افتح الاتفاقية الكاملة",
    "quest.list_header": (
        "🗺️ <b>مهام ROFL HUB</b>\n"
        "..................................................\n"
        "قصص تفاعلية بخيارات وتفرّعات: بوليسية وكوميدية وألغاز. "
        "أول فوز في كل مهمة يمنحك عملات، ويمكنك إعادة اللعب كما تشاء!\n"
        "🌐 <i>قصص المهام باللغة الروسية حاليًا — حزم لغات أخرى قادمة قريبًا.</i>\n\n"
        "👇 <b>اختر قصة:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} دقيقة · 🏆 +{reward} 🪙 عن أول فوز\n"
        "..................................................\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>أنجزت المهمة واستلمت المكافأة. أعد اللعب متى شئت!</i>",
    "quest.card_progress": "⏯ <i>لديك محاولة غير مكتملة.</i>",
    "quest.card_new": "🆕 <i>لم تلعب هذه القصة بعد.</i>",
    "quest.btn_start": "▶️ ابدأ المهمة",
    "quest.btn_restart": "🔄 ابدأ من جديد",
    "quest.btn_resume": "⏯ متابعة",
    "quest.btn_list": "🗺️ إلى قائمة المهام",
    "quest.btn_replay": "🔄 العب مرة أخرى",
    "quest.win_first": "\n\n🏆 <b>أنجزت المهمة! المكافأة: +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>أنجزتها مجددًا!</b> مكافأة هذه المهمة استُلمت من قبل.",
    "quest.fail_footer": "\n\n💀 <i>ليست أفضل نهاية... لكن يمكنك دائمًا إعادة القصة!</i>",
    "quest.stale": "⏳ هذا المشهد صار خلفك — نتابع من الموضع الحالي!",
    "quest.no_coins": "❌ التلميح يكلّف {cost} 🪙، ورصيدك أقل من ذلك. مرّ على مزرعتك!",
    "quest.not_found": "❌ لم يتم العثور على المهمة.",
    "menu.btn_quests": "🗺️ المهام",

    # ---------------- ферма ----------------
    "farm.btn_bonus": "🎁 استلم المكافأة (كفتة كل 24 س)",
    "farm.btn_load1": "🥩 زوّد 1",
    "farm.btn_loadall": "⚡ زوّد الكل",
    "farm.btn_shop": "🏪 ادخل المتجر",
    "farm.status_all_fueled": "🟢 كل الحفّارات السيبرانية مزوّدة بالوقود وتعدّن العملات!",
    "farm.status_partial": "🟡 تم تزويد {fueled} من أصل {total} من الحفّارات السيبرانية بالوقود. والبقية تنتظر الكفتات في الثلاجة!",
    "farm.status_no_fuel": "🔴 توقفت الحفّارات السيبرانية! لا يوجد وقود كافٍ في الثلاجة.",
    "farm.status_no_drills": "💡 احصل على روبوت أقوى من /shop — وستعدّن مزرعتك أكثر.",
    "farm.boost_nuclear": "🔋 التسريع النووي x5 حتى {until} UTC (استهلاك الكفتات ×3)",
    "farm.boost_nitrogen": "❄️ التبريد النيتروجيني +40% حتى {until} UTC",
    "farm.boost_drone": "🛸 الدرون المايسترو يطيل عمر الروبوتات حتى {until} UTC",
    "farm.no_boosts": "لا معزّزات نشطة — ألقِ نظرة على /shop.",
    "farm.burnout": "🔥 أقرب موعد لاحتراق روبوت: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 فعّل روبوت المتدرّب (مجانًا)",
    "farm.intern_activated": "🤖 روبوت المتدرّب بدأ نوبته! +1 🪙 في الساعة إلى الأبد — بلا وقود وبلا انتهاء.",
    "farm.intern_already": "🤖 روبوت المتدرّب يعمل بالفعل.",
    "farm.btn_claim_intern": "🎁 استلم روبوت المتدرّب ({n})",
    "farm.intern_pending": "🎁 روبوتات المتدرّبين التي كسبتها بمستويات الذكاء: <b>{n}</b> — استلمها بالزر أدناه!",
    "farm.intern_claimed_new": "🤖 روبوت متدرّب جديد بدأ نوبته! +1 🪙 في الساعة إلى الأبد.",
    "farm.intern_none": "🤖 لا يوجد متدرّبون جدد بعد — التالي بانتظارك عند مستوى الذكاء 10 و20 و30…",
    "games.intern_ready": "🎁 مستواك الجديد منحك <b>روبوت متدرّب</b> — استلمه في مزرعتك!",
    "farm.intern_line": "• روبوتات المتدرّبين ({rate} 🪙/ساعة، دائمة): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 لديك روبوت متدرّب مجاني! اضغط الزر أدناه — سيستخرج 1 🪙 كل ساعة إلى الأبد.",
    "farm.dashboard": (
        "🚜 <b>مركز الوقود المركزي في ROFL HUB</b>\n"
        "..................................................\n"
        "🤖 الروبوتات النشطة في المصنع: <b>{total}</b>\n"
        "{intern}• روبوتات التعدين ({junior_rate} 🪙/ساعة): <code>{junior}</code>\n"
        "• الحفّارات السيبرانية ({premium_rate} 🪙/ساعة): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>السرعة الحالية لمزرعتك:</b>\n"
        "• الإنتاج في الساعة: <b>+{speed_hour} 🪙</b>\n"
        "• الإنتاج في اليوم: <b>+{speed_day} 🪙</b>\n\n"
        "⚡ <b>المعزّزات:</b>\n{boosts}\n\n"
        "📋 <b>حالة مصنع اللعب:</b>\n"
        "{status}\n"
        "..................................................\n"
        "📦 <b>حالة الثلاجة الآلية:</b>\n"
        "🥩 مخزون الوقود: <b>{fridge} / {capacity}</b>\n"
        "💼 الكفتات في المخزون: <code>{inv}</code>\n"
        "..................................................\n"
        "<i>💿 مهم: الروبوتات تعيش 30 يومًا (الدرون المايسترو يوقف الاستهلاك مؤقتًا). "
        "كل حفّار سيبراني يستهلك كفتته الكاملة الخاصة من الثلاجة كل "
        "24 ساعة عمل: 3 روبوتات — 3 كفتات في اليوم. راقب التزويد!</i>"
    ),
    "farm.bonus_ok": "🎁 أُضيفت كفتة سيبرانية إلى مخزونك! عُد بعد 24 ساعة.",
    "farm.bonus_wait": "⏳ استلمت المكافأة بالفعل! الكفتة التالية بعد {hours} س {minutes} د.",
    "farm.no_inv_cutlets": "❌ لا توجد كفتات سيبرانية في مخزونك! اشترِها من /shop",
    "farm.fridge_full": "📦 ثلاجتك ممتلئة تمامًا!",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>لوحة لاعب ROFL HUB الشخصية</b>\n"
        "..................................................\n"
        "🆔 رقم جوازك: <code>{user_id}</code>\n"
        "{vip}"
        "💰 عملاتك الآن: <b>{balance} 🪙</b>\n"
        "🏆 حالتك: <b>{team}</b>\n"
        "🧠 مستوى الذكاء: <b>{level}</b> · حتى المستوى {next_level}: "
        "<b>{left}</b> إجابة صحيحة في /quiz (المكافأة: +{reward} 🪙)\n"
        "..................................................\n"
        "<i>هنا ما تملكه الآن تحديدًا. استخدم الأزرار للانتقال إلى الأقسام الأخرى!</i>"
    ),
    "profile.no_team": "بلا فريق",
    "profile.team_label": "فريق",
    "profile.clan_label": "كلان",
    "profile.btn_farm": "🚜 مزرعتي السيبرانية",
    "profile.btn_shop": "🏪 المتجر",
    "profile.stats": (
        "📊 <b>إحصاءات الإنجازات في اللعب (30 يومًا)</b>\n"
        "..................................................\n"
        "🧠 مستوى ذكاء اللعب: <b>{level}</b> (مجموع الإجابات الصحيحة: {total})\n"
        "🎮 جولات المبارزات التي خضتها: <b>{played}</b>\n"
        "🏆 الانتصارات المحققة على الخصوم: <code>{won}</code>\n"
        "👥 الأصدقاء النشطون المدعوون: <b>{refs}</b>\n"
        "..................................................\n"
        "<i>تحفظ الإحصاءات إنجازاتك التاريخية حتى لو كانت العملات التي ربحتها قد أُنفقت في المتجر!</i>"
    ),
    "img.passport": "رقم الجواز: {user_id}",
    "img.owner": "القائد: @{username}",
    "img.balance": "الرصيد: {balance} عملة",
    "img.fridge": "في الثلاجة: {fridge} / {capacity}",
    "img.inv": "كفتات في المخزون: {inv}",
    "img.junior": "روبوتات التعدين: {count}",
    "img.premium": "الحفّارات السيبرانية: {count}",

    # ---------------- игры: общий движок ----------------
    "games.win": "🎉 <b>فوز!</b> 🎉\nأُضيف: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>خسارة!</b>\nخُصم: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>تعادل!</b>\nلم تُخصم أي عملات.",
    "games.limit": (
        "🛑 <b>وصلت إلى الحد اليومي!</b>\n\n"
        "حققت اليوم بالفعل {limit} فوزًا في لعبة {game}. يتجدد الحد في 00:00 UTC.\n\n"
        "⚡ إزالة الحد لمدة 24 ساعة — 15 ★، ولمدة 30 يومًا — 249 ★ (قسم «الألعاب» في /shop)."
    ),
    "games.no_coins": "❌ لديك 0 🪙 — لا تملك ما تدفع به رسم الجولة. اجمع دخل مزرعتك من /farm!",
    "games.balance": "💰 الرصيد: <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 العب مرة أخرى!",
    "games.btn_hub": "🕹️ منطقة الألعاب",
    "games.level_up": (
        "🏅 <b>ارتفع مستوى الذكاء: {level}!</b> المكافأة: <b>+{bonus} 🪙</b>!\n"
        "المستوى التالي: {next_required} إجابة صحيحة → +{next_reward} 🪙."
    ),
    "games.name.rps": "حجر-ورقة-مقص",
    "games.intern_bonus": "🤖 المستوى {level}! وصل روبوت متدرّب جديد إلى مزرعتك — أصبح لديك {count}.",
    "games.name.hl": "أعلى/أقل",
    "games.name.quiz": "الكويز",
    "games.name.safe": "الخزنة",
    "games.name.math": "Math",  # TODO(перевод 26.10)
    "games.name.flags": "Flags and capitals",  # TODO(перевод 26.10)
    "games.name.code": "Code breaker",  # TODO(перевод 26.10)
    "games.name.memory": "Memory",  # TODO(перевод 26.10)

    # ---------------- КНБ ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>حجر-ورقة-مقص</b>\n\n"
        "الفوز: <b>+{reward}</b> · الخسارة: <b>-{penalty}</b> · التعادل: <b>0</b>\n"
        "حد الانتصارات اليومي: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 حجر",
    "rps.scissors": "✂️ مقص",
    "rps.paper": "🧻 ورقة",
    "rps.draw": "🤝 <b>تعادل!</b> كلاكما اختار {bot}.",
    "rps.win": "🏆 <b>فوز!</b> {user} يهزم {bot}.",
    "rps.lose": "💀 <b>فاز البوت.</b> {bot} يهزم {user}.",

    # ---------------- Больше/Меньше ----------------
    "hl.intro": (
        "🎲 <b>أعلى أم أقل</b>\n\nوضع البوت الرقم: <b>{base}</b>.\n"
        "هل سيكون الرقم المخفي أعلى أم أقل؟\n"
        "الفوز: <b>+{reward}</b> · الخسارة: <b>-{penalty}</b> · الحد: <b>{limit}</b> فوزًا"
    ),
    "hl.btn_up": "📈 أعلى",
    "hl.btn_down": "📉 أقل",
    "hl.result": "🎲 <b>نتيجة الجولة</b>\n\nرقم البوت: <b>{base}</b> · المخفي: <b>{secret}</b>",

    # ---------------- викторина ----------------
    "quiz.round": (
        "🧠 <b>الكويز • {category}</b>\n"
        "🤔 السؤال: <b>{question}</b>\n\n"
        "<i>🌐 الأسئلة باللغة الإنجليزية حاليًا — الترجمة إلى العربية قادمة قريبًا!</i>"
    ),
    "quiz.btn_new": "🧠 سؤال جديد",
    "quiz.timeout": "⌛ <b>انتهى الوقت!</b> ⌛\nالإجابة الصحيحة: <b>{correct}</b>",
    "quiz.stale": "⏳ هذا السؤال لم يعد نشطًا. ابدأ سؤالًا جديدًا!",
    "quiz.stale_alert": "هذا السؤال لم يعد نشطًا. ابدأ سؤالًا جديدًا!",
    "quiz.empty": "⚠️ قاعدة الأسئلة فارغة. أبلغ المسؤول.",
    "quiz.wrong": "❌ <b>خطأ</b> ❌\nالإجابة الصحيحة: <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} 🪙</b> عن الخسارة!",
    "quiz.level_line": (
        "🧠 مستوى الذكاء: <b>{level}</b>\n"
        "الانتصارات المتبقية حتى المستوى {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>أمامك {seconds} ثانية للإجابة!\n"
        "صحيح: +{win} 🪙 إلى رصيدك\n"
        "خطأ / انتهى الوقت: خصم -{penalty} 🪙\n"
        "الحد: {limit} فوزًا في اليوم</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>الخزنة السيبرانية</b>\n\n"
        "بداخلها جائزة كبرى: <b>{jackpot} 🪙</b>! الباب مقفل برمز من 1 إلى {codes}. "
        "أمامك محاولة واحدة.\n"
        "فتحتها: <b>+{jackpot}</b> · الإنذار: <b>-{penalty}</b> · الحد: <b>{limit}</b> فوزًا"
    ),
    "safe.btn_retry": "🔐 جرّب الاختراق مجددًا!",
    "safe.win": "🔓 <b>فُتحت الخزنة!</b> كان الرمز: <b>{code}</b>.",
    "safe.lose": "🚨 <b>انطلق الإنذار!</b> اخترت {guess}، وكان الرمز: <b>{code}</b>.",

    # ---------------- дуэли ----------------
    "duel.intro": (
        "⚔️ <b>مبارزات 1 ضد 1: حجر-ورقة-مقص على رهان</b>\n"
        "..................................................\n"
        "اختر طاولة على قدر جيبك — كما في البوكر. يُخصم الرهان فورًا، "
        "وخصمك لاعب حقيقي من ROFL HUB!\n\n"
        "💰 صندوق الرهان = الرهانان معًا. يأخذ الفائز <b>{payout_percent}%</b> من الصندوق، "
        "و<b>{burn_percent}%</b> يُحرق للأبد (انكماش اقتصادي!).\n"
        "🤝 التعادل — إعادة فورية للحركات والصندوق يبقى على الطاولة.\n"
        "⏱ للحركة الواحدة — <b>{move_timeout} ثانية</b>، ومن يصمت يختار له مولّد العشوائية.\n"
        "🏆 انتصارات المبارزات تُحسب لفريقك في المعارك!\n\n"
        "👇 <b>اختر طاولة:</b>"
    ),
    "duel.btn_table": "⚔️ طاولة {stake} 🪙",
    "duel.btn_cancel": "❌ غادر الطاولة (استرجاع الرهان)",
    "duel.btn_move_rock": "🪨 حجر",
    "duel.btn_move_scissors": "✂️ مقص",
    "duel.btn_move_paper": "🧻 ورقة",
    "duel.waiting": (
        "🪑 <b>أنت على طاولة {stake} 🪙.</b> رهانك في الصندوق.\n"
        "ننتظر المقاتل الثاني... فور جلوسه ستصلكما دعوة اختيار الحركة!\n"
        "<i>يبقى الطابور {ttl} دقيقة، ثم يعود رهانك تلقائيًا.</i>"
    ),
    "duel.cancelled": "🚪 غادرت الطاولة. عاد رهان <b>{stake} 🪙</b> إلى رصيدك.",
    "duel.expired": "⌛ لم يظهر أي خصم على طاولة {stake}. أُعيد رهان <b>{stake} 🪙</b>.",
    "duel.matched": (
        "⚔️ <b>تم العثور على خصم! طاولة {stake} 🪙.</b>\n"
        "الصندوق: <b>{bank} 🪙</b> · للفائز: <b>{payout}</b>\n\n"
        "⏱ أمامك <b>{timeout} ثانية</b> لاختيار حركتك!"
    ),
    "duel.move_saved": "✊ سُجّلت حركتك! ننتظر حركة الخصم...",
    "duel.draw_replay": (
        "🤝 <b>تعادل! الجولة {round}.</b> أظهر كلاكما الحركة نفسها.\n"
        "الصندوق على الطاولة. ⏱ {timeout} ثانية من جديد — اختر حركتك:"
    ),
    "duel.win": (
        "🏆 <b>المبارزة لك!</b>\n\n"
        "حركتك {winner_move} تهزم {loser_move}.\n"
        "💰 الربح: <b>+{payout} 🪙</b> · 🔥 احترق من الصندوق: {burned}\n"
        "💼 الرصيد: <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>خسرت المبارزة.</b>\n\n"
        "حركة الخصم {winner_move} تهزم حركتك {loser_move}.\n"
        "📉 ذهب رهانك <b>{stake} 🪙</b> إلى صندوق الفائز.\n"
        "ثأر؟"
    ),
    "duel.reaper_prefix": "⏰ <b>انتهى وقت الجولة!</b> الحركات الناقصة اختارها مولّد العشوائية.\n\n",
    "duel.bad_table": "❌ لا توجد طاولة كهذه.",
    "duel.already_in": "⚠️ أنت بالفعل على طاولة أو في قتال! أنهِ مبارزتك الحالية أولًا.",
    "duel.no_coins": "❌ تحتاج إلى {stake} 🪙 في رصيدك لهذه الطاولة.",
    "duel.cancel_impossible": "⚠️ لم يعد بالإمكان إلغاء هذا الطابور (وُجد خصم أو أُغلقت الطاولة).",
    "duel.not_active": "⌛ هذه المبارزة انتهت بالفعل.",
    "duel.not_participant": "🔒 هذه ليست مبارزتك!",
    "duel.move_already": "✋ أظهرت حركتك في هذه الجولة بالفعل. ننتظر الخصم!",
    "duel.bad_move": "❌ حركة غير معروفة.",
    "duel.btn_rematch": "⚔️ الثأر (إلى الطاولات)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 الرتبة: <b>{rank}</b>\n",
    "rank.rookie": "مبتدئ",
    "rank.fighter": "مقاتل",
    "rank.legend": "أسطورة",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.king": "KING",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>برنامج دعوة الأصدقاء في ROFL HUB</b>\n"
        "..................................................\n"
        "ادعُ أصدقاءك عبر رابطك الشخصي واحصل على <b>{bonus}</b> "
        "عن كل من يصبح لاعبًا نشطًا!\n\n"
        "🔗 <b>رابطك (اضغط للنسخ):</b>\n<code>{link}</code>\n\n"
        "📊 <b>إحصاءاتك:</b>\n"
        "👥 الأصدقاء المدعوون: <b>{invited}</b>\n"
        "💰 أرباحك من الدعوات: <b>{earned} 🪙</b>\n"
        "..................................................\n"
        "<i>شارك الرابط مع زملاء الصف والأصدقاء وعلى الشبكات الاجتماعية — كلما كبرت الشلة نما رصيدك أسرع!</i>"
    ),
    "ref.btn_share": "📣 شارك الرابط",
    "ref.share_text": "انضم إلى منظومة ألعاب ROFL HUB!",
    "ref.qualified_line": ("✅ <b>الصديق النشط</b> هو من بلغ <b>مستوى الذكاء {level}</b> في المسابقة "
                           "وجمع <b>{claims} كفتات يومية</b> في المزرعة. عندها تحصل على <b>{bonus}</b>، "
                           "مرة واحدة عن كل صديق. لا مكافأة على التسجيل دون لعب — هذا أعدل للجميع."),
    "ref.qualified_notify": ("🤝 <b>صديقك أصبح لاعبًا نشطًا!</b>\n"
                             "مستوى الذكاء {level} و{claims} كفتات يومية — تحقّق الشرطان. حصلت على <b>{bonus}</b>. ادعُ المزيد!"),

    "team.err_len": "❌ يجب أن يتراوح طول النص بين 1 و{max} حرفًا!",
    "team.err_link": "🚨 خطأ أمني! الروابط وأسماء المستخدمين وأرقام الهواتف ممنوعة منعًا باتًا!",
    "team.err_badword": "❌ تم رصد ألفاظ نابية! التزم بقواعد المنصّة.",
    "team.err_already": "⚠️ أنت عضو في فريق أو كلان بالفعل! اخرج منه أولًا.",
    "team.err_money": "❌ لا يكفي رصيدك من العملات! إنشاء فريق يكلّف {cost} 🪙 ورصيدك {balance} 🪙.",
    "team.err_captain": "⚠️ أنت كابتن فريق آخر بالفعل!",
    "team.err_taken": "⚠️ الاسم «{name}» مستخدم بالفعل! اختر اسمًا فريدًا.",
    "team.err_gone": "❌ هذا الفريق لم يعد موجودًا.",
    "team.err_full": "📦 لا توجد مقاعد شاغرة في هذا الفريق!",
    "team.err_not_member": "❌ لست عضوًا في أي فريق.",
    "mk.err_no_team": "🏆 بورصة الفريق لأعضاء الفرق. انضم إلى فريق أو أنشئ فريقك.",
    "mk.err_team_only": "🔒 هذا العرض لأعضاء فريق البائع فقط.",
    "help.err_qty": "يمكنك طلب من 1 إلى {max} وحدة من المورد.",
    "help.err_open": "لديك طلب مفتوح بالفعل — انتظر المساعدة أو ألغِه.",
    "help.err_not_found": "هذا الطلب مغلق بالفعل.",
    "help.err_self": "لا يمكن تلبية طلبك بهدية منك 🙂",
    "help.err_limit": "أهديت اليوم {max} من الموارد بالفعل — يتجدد الحد عند 00:00 بتوقيت UTC.",
    "help.err_not_active": "🔒 يمكن إهداء الموارد من مستوى الذكاء {level} وبعد استلام {claims} من الكفتات اليومية.",
    "it.err_none": "هذه القطعة لم تعد في المخزون.",

    # ---------------- удаление аккаунта ----------------
    "profile.btn_delete": "🗑 حذف الحساب",
    "acct.warn": (
        "⚠️ <b>حذف الحساب</b>\n"
        "..................................................\n"
        "مع الحساب ستختفي <b>نهائيًا ولا رجعة فيها</b> هذه الأشياء:\n"
        "• العملات والكفتات السيبرانية والموارد وكل روبوتات المزرعة؛\n"
        "• التعزيزات وإزالة حدود الفوز وكل ما اشتريته بـStars — <b>لا تُسترد Stars</b>؛\n"
        "• معرّف VIP وتقدّم الكويز والمهام؛\n"
        "• مكانك في الفريق (تنتقل القيادة إلى أقدم عضو في الفريق).\n"
        "تُلغى أوامر البورصة المفتوحة فورًا، وتعود البضاعة إلى المخزون.\n\n"
        "⏳ يُجمَّد الحساب أولًا لمدة <b>{days} أيام</b> — يمكنك خلالها أن تغيّر رأيك بضغطة زر واحدة. "
        "بعد ذلك يصبح الحذف نهائيًا. وإن عدت لاحقًا فستبدأ من الصفر، ولا تُمنح مكافأة البداية مرتين.\n\n"
        "<i>سيعمل زر الحذف بعد {seconds} ثانية — اقرأ بتمعّن.</i>"
    ),
    "acct.btn_keep": "✅ لا، أبقِ حسابي",
    "acct.btn_confirm": "🗑 نعم، احذف حسابي",
    "acct.wait": "⏳ انتظر {seconds} ثانية أخرى — واقرأ ما الذي سيُحذف بالضبط.",
    "acct.kept": "👍 رائع، حسابك باقٍ معك!",
    "acct.scheduled": (
        "🗑 تم تجميد الحساب وسيُحذف في <b>{date}</b> (UTC).\n"
        "أُلغيت أوامر البورصة وعادت البضاعة إلى المخزون.\n\n"
        "إن غيّرت رأيك فاضغط الزر أدناه، وسيعود كل شيء كما كان."
    ),
    "acct.pending_notice": (
        "⏳ الحساب مجمَّد وسيُحذف في <b>{date}</b> (UTC).\n"
        "هل تريد البقاء في اللعبة؟ اضغط الزر أدناه."
    ),
    "acct.btn_undo": "↩️ إلغاء الحذف",
    "acct.undone": "🎉 أُلغي الحذف — الحساب عاد إليك!",
    "acct.purged": "🗑 تم حذف حسابك في ROFL HUB. شكرًا للعب! إن أردت العودة فاضغط /start.",
    "acct.deleted_notice": "تم حذف الحساب. اضغط /start للبدء من جديد.",
    "acct.welcome_back": (
        "👋 <b>أهلًا بعودتك!</b>\n"
        "أُنشئ ملفك من جديد من الصفر. تُمنح مكافأة البداية مرة واحدة فقط، لذا رصيدك 0 🪙. "
        "المزرعة والألعاب والكويز بانتظارك!"
    ),
    "tr.err_not_active": (
        "🔒 يمكن إرسال العملات بعد بلوغ مستوى الذكاء {level} واستلام {claims} من الكفتات اليومية — "
        "بهذا يُحمى النظام من الحسابات المزيفة."
    ),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>تحويل العملات إلى لاعب آخر</b>\n"
        "..................................................\n"
        "صيغة الأمر:\n"
        "<code>/transfer ID المبلغ</code> — برقم الجواز (تجده في /profile)\n"
        "<code>/transfer @username المبلغ</code> — باسم المستخدم\n"
        "<code>/transfer ROFL-HUB-777 المبلغ</code> — بمعرّف VIP من المزاد\n\n"
        "أمثلة:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 الحد الأدنى للمبلغ: <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ لم يتم العثور على المستلم. تحقق من رقم الجواز أو @username — يجب أن يكون اللاعب مسجلًا في البوت.",
    "tr.self": "🤨 لا يمكنك تحويل العملات إلى نفسك — لكان ذلك اقتصادًا أبديًا!",
    "tr.blocked": "🚫 هذا اللاعب محظور — التحويلات إليه غير متاحة.",
    "tr.min": "❌ الحد الأدنى للتحويل هو {min} 🪙.",
    "tr.insufficient": "❌ لا تكفي العملات! رصيدك: <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ لا توجد عملات كافية في رصيدك.",
    "tr.confirm": (
        "🔄 <b>أكّد التحويل:</b>\n\n"
        "👤 المستلم: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 المبلغ المخصوم: <b>{amount} 🪙</b>{fee_line}\n"
        "💰 سيستلم المستلم: <b>{received} 🪙</b>\n\n"
        "<i>لا يمكن التراجع عن التحويلات — تحقق من المستلم جيدًا!</i>"
    ),
    "tr.fee_line": "\n🔥 عمولة المركز: <b>{fee} 🪙</b> (ستُحرق)",
    "tr.btn_confirm": "✅ تأكيد التحويل",
    "tr.btn_cancel": "❌ إلغاء",
    "tr.cancelled_toast": "أُلغي التحويل",
    "tr.cancelled": "❌ <b>أُلغي التحويل.</b> بقيت عملاتك في مكانها.",
    "tr.not_yours": "🔒 هذا ليس تحويلك!",
    "tr.done_toast": "✅ تم التحويل!",
    "tr.done": (
        "✅ <b>تم تنفيذ التحويل!</b>\n\n"
        "💸 أُرسل: <b>{amount} 🪙</b> إلى اللاعب ID <code>{recipient_id}</code>\n"
        "💰 رصيدك: <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>وصلك تحويل بقيمة {amount} 🪙!</b>\n"
        "المرسل: ID <code>{sender_id}</code>. رصيدك مشحون بالفعل — تفقّد /profile!"
    ),

    # ---------------- магазин и платежи ----------------
    "shop.header": "🏪 <b>متجر ROFL HUB</b>\nالمشتريات عبر Telegram Stars الرسمية. اختر فئة من الأزرار بالأسفل.",
    "shop.cat_farm": (
        "🚜 <b>المتجر · للمزرعة</b>\n"
        "..................................................\n"
        "روبوتات لمدة 30 يومًا، وقود، ثلاجات، معزّزات والدرون المايسترو.\n"
        "📦 سعة ثلاجتك الآن: <b>{capacity} كفتة</b>\n"
        "..................................................\n"
        "👇 <b>اختر سلعة:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>المتجر · الألعاب</b>\n"
        "..................................................\n"
        "إزالة حدود الفوز، باقات العملات ورخصة ميغا-كلان.\n"
        "..................................................\n"
        "👇 <b>اختر سلعة:</b>"
    ),
    "pay.invoice_desc": "تسليم فوري لمحتوى ROFL HUB داخل اللعبة.",
    "pay.invoice_error": "⚠️ تعذّر إنشاء فاتورة Telegram Stars. حاول لاحقًا.",
    "pay.success": "🎉 <b>تم تأكيد الدفع!</b>\n🧾 <code>{charge}</code>\n💵 خُصم: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 نجح الدفع لكن التسليم فشل مؤقتًا. نحن على علم بالمشكلة.\n"
        "احتفظ برقم الدفعة: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 أُعيدت Stars إلى حسابك تلقائيًا.",
    "pay.keep_charge": "احتفظ برقم الدفعة لطلب الاسترجاع: <code>{charge}</code>",
    "pay.already": "✅ هذه الدفعة عولجت من قبل، والسلعة سُلّمت سابقًا.",
    "pay.support": (
        "🛟 <b>دعم مدفوعات Telegram Stars</b>\n"
        "..................................................\n"
        "كل سلع ROFL HUB رقمية وتُسلَّم فورًا بعد الدفع.\n\n"
        "⚙️ <b>إذا دفعت ولم تصلك السلعة:</b>\n"
        "يعيد البوت Stars تلقائيًا عند فشل التسليم. إن لم يحدث ذلك — "
        "أرسل هنا رقم الدفعة (موجود في الإيصال، بصيغة <code>xxxx...</code>) واشرح المشكلة. "
        "ستتحقق الإدارة من الدفعة في قاعدة البيانات وتحل المسألة خلال 24 ساعة.\n\n"
        "💫 <b>سياسة الاسترجاع:</b>\n"
        "الاسترجاع ممكن إذا لم تُستلم السلعة أو سُلّمت بخطأ. "
        "السلع الرقمية المسلَّمة بشكل صحيح غير قابلة للاسترجاع.\n"
        "..................................................\n"
        "<i>هذا القسم هو نقطة الدعم الرسمية للمشتريات وفق قواعد Telegram.</i>"
    ),

    # ---------------- доставка ----------------
    "dlv.cutlets": "🥩 أُضيفت <b>{qty} كفتة</b> إلى مخزونك.",
    "dlv.miner": "🤖 وصل الروبوت <b>«{name}»</b> إلى مزرعتك.\n⏳ مدة الخدمة: حتى <b>{until} UTC</b>.",
    "dlv.miner_junior": "روبوت التعدين",
    "dlv.miner_premium": "الحفّار السيبراني",
    "dlv.fridge": "📦 وُسّعت الثلاجة لتتسع لـ<b>{capacity} كفتة</b>.",
    "dlv.coins": "💰 أُضيفت <b>+{amount} 🪙</b> إلى رصيدك.",
    "dlv.boost_nuclear": "🔋 التسريع النووي x5 نشط حتى <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ التبريد النيتروجيني +40% نشط حتى <b>{until} UTC</b>.",
    "dlv.drone": "🛸 الدرون المايسترو يحرس مزرعتك حتى <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ أُزيلت حدود الفوز حتى <b>{until} UTC</b>.",
    "dlv.clan": "🏆 حصل فريقك على حالة <b>ميغا-كلان</b>: حتى {max} مقعد.",
    "dlv.err_fridge": "لديك بالفعل ثلاجة بهذه السعة أو أكبر.",
    "dlv.err_no_team": "ليس لديك فريق بعد. أنشئ فريقك أولًا عبر /create_team.",
    "dlv.err_mega": "فريقك يحمل حالة ميغا-كلان بالفعل.",
    "dlv.err_need_team": "The Mega-Clan is for teams. First expand your squad into a team in the «Team» tab — for coins.",
    "dlv.err_pass_owned": "You already have this season's pass.",
    "dlv.err_skin_sold": "This skin's edition is sold out.",
    "dlv.intern_upgrade": "♾ تمت ترقية روبوت المتدرّب إلى <b>روبوت تعدين دائم</b>: 5 🪙 في الساعة بلا انتهاء!",
    "dlv.err_no_intern": "لا يوجد روبوت متدرّب مفعّل — فعّله أولًا في /farm.",
    "dlv.err_intern_refs": "تتطلب الترقية {need} أصدقاء نشطين (الشروط في /invite)؛ لديك {have}.",
    "mk.header": "📈 <b>بورصة الكفتة</b>\n..................................................\nالأوامر المفتوحة: <b>{orders}</b> · الكفتة المعروضة: <b>{cutlets}</b> · أفضل سعر: <b>{best}</b>\nعمولة المركز: <b>{fee}%</b> من كل بيع (تُحرق — درع ضد التضخم)\n🥩 في مخزونك: <b>{inv}</b> كفتة\n\n{body}\n\n<i>اضغط على أمر للشراء. للبيع: /sell.</i>",
    "mk.empty": "لا عروض بعد. كن الأول: /sell الكمية السعر",
    "mk.order_line": "🥩 #{id} · <b>{qty} قطعة</b> بسعر <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} قطعة بسعر {price} 🪙",
    "mk.btn_my": "📋 أوامري",
    "mk.btn_sell_help": "💰 كيف أبيع الكفتة",
    "mk.btn_refresh": "🔄 تحديث",
    "mk.btn_back": "← إلى البورصة",
    "mk.pick": "🛒 <b>الأمر #{id}</b>: متاح {qty} قطعة بسعر {price} 🪙.\nكم تشتري؟",
    "mk.btn_qty": "{qty} قطعة — {total} 🪙",
    "mk.btn_qty_all": "الكل {qty} قطعة — {total} 🪙",
    "mk.buy_toast": "تمت الصفقة!",
    "mk.buy_done": "✅ اشتريت <b>{qty} كفتة</b> مقابل <b>{total} 🪙</b>. إنها في مخزونك — زوّد حفّاراتك بالوقود!",
    "mk.sold_notify": "💰 <b>البورصة: تم البيع!</b> الأمر #{id}: بيع {qty} قطعة بسعر {price}. حصلت على <b>+{got} 🪙</b> (أُحرقت عمولة {fee}).",
    "mk.sell_help": "💰 <b>كيف تبيع الكفتة</b>\n\nالأمر: <code>/sell الكمية السعر</code>\nمثال: <code>/sell 10 250</code> — 10 كفتات بسعر 250 🪙 للقطعة.\n\nتخرج الكفتة من المخزون وتنتظر المشتري في الأمر (يمكن إلغاؤه في أي وقت). حتى {max_qty} قطعة في الأمر وحتى {max_orders} أوامر مفتوحة. تُحرق عمولة {fee}% عند البيع. لا يقل سعر الكفتة عن {min} 🪙: الوقود من المتجر مقابل النجوم أوفر دائمًا من البورصة. الموارد وطلبات الشراء والمقايضة — في تطبيق اللعبة.",
    "mk.sell_confirm": "📝 عرض <b>{qty} كفتة</b> بسعر <b>{price}</b> 🪙؟\nالإجمالي: {total} · تُحرق عمولة {fee} · ستحصل على <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ اعرض في البورصة",
    "mk.btn_cancel": "❌ إلغاء",
    "mk.sell_toast": "تم عرض الأمر!",
    "mk.sell_done": "✅ الأمر <b>#{id}</b> في البورصة: {qty} قطعة بسعر {price} 🪙. سأخبرك عند البيع.",
    "mk.cancelled_toast": "أُلغي",
    "mk.cancel_text": "❌ <b>أُلغي.</b> بقيت الكفتة في مخزونك.",
    "mk.my_header": "📋 <b>أوامرك</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} قطعة بسعر {price} 🪙",
    "mk.my_empty": "📋 ليس لديك أوامر مفتوحة.",
    "mk.btn_cancel_order": "❌ سحب الأمر #{id}",
    "mk.err_newbie_price": "🔒 While your account is new, you can buy at no more than {max} 🪙 apiece. The limit lifts at intelligence level {level} and after {claims} daily cutlets.",
    "mk.err_cancel_room": "📦 Not enough storage room: {free} free. Make room first, then withdraw the lot.",
    "sw.err_ratio": "⚖️ This swap is too uneven: the two sides (valued at the market's minimum prices) may differ by at most {x}×.",
    "mk.order_cancelled": "↩️ سُحب الأمر #{id}: عادت <b>{qty} كفتة</b> إلى مخزونك.",
    "mk.err_qty": "❌ الكمية: من 1 إلى {max} قطعة في الأمر.",
    "mk.err_price": "❌ السعر: من {min} إلى {max} 🪙 للقطعة.",
    "mk.err_no_cutlets": "❌ لديك {have} كفتة فقط في المخزون. كفتة الثلاجة لا تُعرض — انظر /farm.",
    "mk.err_too_many": "❌ الحد: لا أكثر من {max} أوامر مفتوحة. اسحب واحدًا من «أوامري».",
    "mk.err_not_found": "❌ هذا الأمر مغلق بالفعل.",
    "mk.err_own": "🤨 لا يمكنك شراء أمرك الخاص.",
    "mk.err_insufficient": "❌ لا يكفي رصيدك: تحتاج {total} 🪙.",
    "farm.btn_market": "📈 بورصة الكفتة",

    # ---------------- ресурсы (волна 22.10, вечер) ----------------
    "res.metal": "المعدن",
    "res.hydrogen": "الهيدروجين",
    "res.crystal": "البلّورات",
    "res.parts": "القطع",
    "res.none": "لا شيء بعد",
    "games.resource_gain": "{icon} تم الاستخراج: <b>+{qty} {name}</b> (المجموع {total}) → /workshop",
    "quest.win_resources": "\n📦 وأيضًا 🪨 حجر: <b>{qty}</b> → /workshop",
    "profile.resources_line": "🧰 الموارد: {stock}\n",
    "menu.btn_goals": "🎯 الأهداف اليومية",
    "menu.btn_raids": "🏴‍☠️ الغارات",
    "menu.btn_workshop": "🔧 الورشة",
    "farm.btn_workshop": "🔧 الورشة",
    "farm.btn_app": "🏭 المزرعة في التطبيق",
    "menu.btn_app": "🚀 تطبيق اللعبة: المزرعة، الورشة، الغارات",
    "app.btn_section": "🚀 افتح في التطبيق",
    "app.goto_workshop": "🔧 <b>الورشة</b> موجودة في تطبيق اللعبة: الموارد والوصفات والصناعة بلمسة واحدة.",
    "app.goto_raids": "🏴\u200d☠️ <b>الغارات</b> موجودة في تطبيق اللعبة: الاستطلاع ووضعية الدفاع والثأر.",
    "app.goto_station": "🛰 <b>محطة الفريق</b> موجودة في تطبيق اللعبة: التقدّم والمساهمات ومكافأة للفريق كله.",
    "app.goto_market": "📈 <b>بورصة الكفتة</b> أسهل في تطبيق اللعبة: العروض والبيع وأوامرك في شاشة واحدة.",
    "mk.err_asset": "❌ لا يوجد صنف كهذا في البورصة.",
    "mk.err_no_resource": "❌ المورد لا يكفي: لديك {have} فقط في المخزون.",
    "mk.bid_filled_notify": "🙋 <b>البورصة: نُفّذ طلب الشراء!</b> الطلب #{id}: اشتريت <b>+{qty} {icon}</b> بسعر {price} 🪙.",
    "sw.err_same": "❌ لا يمكن مقايضة مورد بالمورد نفسه.",
    "sw.err_qty": "❌ في المقايضة حدّد كمية من 1 إلى {max}، لما تعطيه ولما تريد الحصول عليه.",
    "shop.btn_info": "ℹ️ ماذا يمنح كل منتج",
    "sw.done_notify": "🔄 <b>تمت المقايضة #{id}!</b> أعطيت {give}، وحصلت على {want}.",
    "ws.err_coins": "🔒 العملات لا تكفي: تحتاج {need} 🪙، ورصيدك {have} 🪙.",
    "wk.eff_nitrogen": "❄️ النيتروجين +40% لمدة {h} س",
    "wk.eff_nuclear": "☢️ النووي x5 لمدة {h} س",
    "wk.eff_drone": "🛸 الدرون المايسترو لمدة {h} س",
    "wk.eff_shield": "🛡 الترس لمدة {h} س",
    "wk.eff_unlimit": "⚡ إزالة حدود الفوز لمدة {h} س",
    "wk.eff_cutlet": "🥩 كفتة ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ وصفة الأسبوع هذه لم تعد متاحة.",
    "wk.err_limit": "🔒 استُنفد حد هذه الوصفة لهذا الأسبوع ({limit}). يبدأ الأسبوع الجديد يوم الاثنين 00:00 UTC.",
    "games.resource_full": "📦 مخزون {icon} ممتلئ ({cap}) — الفائض يضيع. أنفقه أو بِعه أو وسّع المخزون في الورشة.",
    "mk.err_storage_full": "📦 لا توجد مساحة كافية في المخزون: المتاح {free}. وسّع المخزون في الورشة.",
    "mk.err_buyer_full": "📦 مخزون المشتري ممتلئ — لا يمكن إتمام الصفقة الآن (المتاح {free}).",
    "ws.recipe_storage": "توسيع المخزون إلى {cap}",
    "ws.done_storage": "📦 <b>تم توسيع المخزون:</b> حتى {cap} من كل مورد. إلى الأبد.",
    "ws.err_storage_max": "📦 المخزون بأقصى حجم بالفعل.",
    "farm.boost_armor": "🛡 الدرع السيبراني مستوى {level}: +{percent}% للتعدين حتى {until} UTC",
    "farm.boost_station": "🛰 محطة الفريق مستوى {level}: +{percent}% للتعدين",
    "clan.btn_station": "🛰 محطة الفريق",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>الورشة</b>\n"
        "..................................................\n"
        "🧰 مواردك: {stock}\n"
        "⛏ المعدن — حجر-ورقة-مقص والمبارزات · 💧 الهيدروجين — أعلى/أقل · "
        "💎 البلّورات — الكويز · ⚙️ القطع — الخزنة السيبرانية. المهام تمنح حزمة كاملة.\n\n"
        "🛡 الدرع السيبراني: <b>المستوى {armor}/{armor_max}</b> (+{armor_pct}% للتعدين عن كل مستوى، لمدة 30 يومًا)\n"
        "🚀 المكوك: <b>{shuttle}</b> — عمولة البورصة {shuttle_fee}%، حتى {shuttle_qty} كفتة في الأمر\n\n"
        "<i>✅ — الموارد كافية، 🔒 — ليس بعد. ضغطة واحدة ويتم الأمر.</i>"
    ),
    "ws.shuttle_yes": "مُجمَّع",
    "ws.shuttle_no": "غير مُجمَّع",
    "ws.recipe_nitro_6h": "التبريد النيتروجيني لمدة 6 ساعات",
    "ws.recipe_nuclear_3h": "التسريع النووي لمدة 3 ساعات",
    "ws.recipe_drone_24h": "الدرون المايسترو ليوم كامل",
    "ws.recipe_shield_24h": "ترس الحماية من الغارات ليوم كامل",
    "ws.recipe_cutlet": "تخليق كفتة سيبرانية",
    "ws.recipe_armor": "الدرع السيبراني مستوى {level}",
    "ws.recipe_shuttle": "تجميع المكوك",
    "ws.btn_shuttle_owned": "🚀 المكوك مُجمَّع",
    "ws.btn_armor_max": "🛡 الدرع السيبراني: الحد الأقصى",
    "ws.btn_refresh": "🔄 تحديث",
    "ws.btn_farm": "🚜 إلى المزرعة",
    "ws.noop": "في الحد الأقصى بالفعل",
    "ws.toast": "تم!",
    "ws.done_nitrogen": "❄️ <b>التبريد النيتروجيني +40%</b> نشط حتى {until} UTC.",
    "ws.done_nuclear": "☢️ <b>التسريع النووي x5</b> نشط حتى {until} UTC. الحفّارات تأكل ×3 كفتة!",
    "ws.done_drone": "🛸 <b>الدرون المايسترو</b> يحرس روبوتاتك حتى {until} UTC.",
    "ws.done_shield": "🛡 <b>ترس الحماية من الغارات</b> صامد حتى {until} UTC. مواردك في أمان.",
    "ws.done_cutlet": "🥩 تم التخليق: <b>+{qty} كفتة سيبرانية</b> في المخزون. زوّد الحفّارات في /farm!",
    "ws.done_armor": "🛡 <b>الدرع السيبراني مستوى {level}!</b> تعدين المزرعة: <b>+{percent}%</b> لمدة 30 يومًا.",
    "ws.done_shuttle": "🚀 <b>تم تجميع المكوك!</b> العمولة على مبيعاتك الآن {fee}%، وحتى {qty} كفتة في الأمر. المكوك لك وحدك وإلى الأبد.",
    "ws.err_unknown": "❌ لا توجد وصفة كهذه.",
    "ws.err_off": "🔧 هذه الوصفة غير متاحة حاليًا.",
    "ws.err_locked": "🔒 ستُفتح الوصفة بعد {hours} س — تُفتح وصفة جديدة كل يوم.",
    "ws.recipe_camo_12h": "التمويه لمدة 12 ساعة",
    "ws.recipe_trap_24h": "الطُّعم ليوم كامل",
    "ws.recipe_drill_24h": "مدرّب وضعية الدفاع ليوم كامل",
    "ws.recipe_forsage": "الدفع الإضافي للسفينة",
    "ws.recipe_economizer": "موفّر الوقود",
    "ws.recipe_cargo": "عنبر الشحن الموسّع",
    "ws.recipe_thermos_24h": "ثرموس الكفتة ليوم كامل",
    "ws.recipe_stamp": "ختم البورصة",
    "ws.recipe_banner_24h": "راية الفريق ليوم كامل",
    "ws.recipe_dome_12h": "قبة الفريق لمدة 12 ساعة",
    "it.err_no_cooldown": "🚀 لا توجد إعادة شحن لتجاوزها — السفينة جاهزة للإقلاع أصلًا.",
    "it.err_forsage_daily": "🔥 استُخدم الدفع الإضافي بالفعل — التالي بعد {hours} س.",
    "res.stone": "الحجر",
    "res.wood": "الخشب",
    "res.fire": "النار",
    "res.energy": "الكهرباء",
    "res.battery": "البطاريات",
    "res.cow": "الأبقار",
    "res.core": "النواة",
    "tech.comm": "الاتصالات",
    "tech.scout": "الاستطلاع",
    "tech.attack": "الهجوم",
    "tech.defense": "الدفاع",
    "tech.science": "العلوم",
    "tech.err_max": "🏆 هذا هو المستوى الأقصى بالفعل.",
    "tech.err_unknown": "❌ لا توجد تقنية بهذا الاسم.",
    "tech.err_tool": "🧰 تحتاج إلى طقم أدوات من المستوى {tool} — اصنعه في المختبر.",
    "tech.err_cooldown": "⏳ يمكنك دراسة المستوى التالي بعد {hours} س.",
    "tech.err_science": "📚 يمكن دراسة العلم من المستوى {level} عندما تصل كل التقنيات الأخرى إلى المستوى {level}.",
    "ws.err_items_full": "📦 مخزن العناصر ممتلئ: {max} عنصرًا كحد أقصى. فعّل شيئًا أو وسّع المخزن.",
    "post.scope_team": "ترتيب الفرق",
    "post.scope_clan": "ترتيب العشائر",
    "post.scope_teams": "الفرق والعشائر",
    "post.scope_solo": "الترتيب الفردي",
    "nom.farm_mined": "استخراج أكبر عدد من العملات بالمزرعة",
    "nom.coins_earned": "كسب أكبر عدد من العملات",
    "nom.duel_wins": "أكثر انتصارات في المبارزات",
    "nom.duels_played": "أكثر مبارزات ملعوبة",
    "nom.quiz_wins": "أكثر إجابات صحيحة في المسابقة",
    "nom.rps_wins": "أكثر انتصارات في حجر-ورقة-مقص",
    "nom.safe_wins": "فتح أكبر عدد من الخزائن السيبرانية",
    "nom.game_wins_total": "أكثر انتصارات في الألعاب ضد البوت",
    "nom.referrals": "دعوة أكبر عدد من الأصدقاء النشطين",
    "nom.stars_spent": "أكثر دعم للمنظومة (Stars)",
    "nom.insta_reels": "من ينتشر ريلزه على Instagram أكثر",
    "nom.youtube_shorts": "من ينتشر فيديوه على YouTube Shorts أكثر",
    "nom.tiktok": "من ينتشر فيديوه على TikTok أكثر",
    "bt.err_closed": "⏳ هذه المعركة مغلقة بالفعل.",
    "bt.err_no_entry": "هذه المعركة لا تحتاج إلى طلب مشاركة.",
    "bt.err_no_team": "🏆 انضم إلى فريق أولًا.",
    "bt.err_scope": "هذه المعركة ليست لنوع فريقك.",
    "bt.err_full": "✅ طلب فريقك مكتمل بالفعل.",
    "bt.err_battery": "🔋 لا توجد بطارية — اصنعها في الورشة.",
    "horse.err_max": "🐎 في الإسطبل {max} من الخيول بالفعل — لا مكان لمزيد.",
    "horse.err_coins": "🪙 ثمن الحصان {price} 🪙 — الرصيد لا يكفي بعد.",
    "shuttle.err_none": "🚀 اصنع المكوك في الورشة أولًا.",
    "cart.err_horse": "🛒 العربة تحتاج إلى حصان: عدد العربات لا يزيد على عدد الخيول (ولا على {max}).",
    "raid.err_need_tech": "🔬 الغارة تحتاج إلى تقنية «{tech}» من المستوى 1 — ادرسها في المختبر.",
    "raid.err_battery": "🔋 الاستطلاع يحتاج إلى بطارية — اصنعها في الورشة.",
    "games.energy_gain": "⚡ حظ سعيد: +1 كهرباء!",
    "ws.recipe_bonfire": "موقد: نار من الخشب والحجر",
    "ws.recipe_battery": "بطاريات (×2)",
    "ws.recipe_cart": "عربة",
    "ws.recipe_meds_72h": "حقيبة إسعاف لمدة 72 ساعة",
    "ws.err_resources": "🔒 الموارد لا تكفي: {kind} — تحتاج {need}، لديك {have}. استخرجها في الألعاب!",
    "ws.err_shuttle_owned": "🚀 المكوك مُجمَّع بالفعل — واحد لكل لاعب.",
    "ws.err_armor_max": "🛡 الدرع في مستواه الأقصى بالفعل ({max}).",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>الغارات</b>\n"
        "..................................................\n"
        "💧 الهيدروجين: <b>{hydrogen}</b> (الطلعة تكلّف {fuel})\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ وضعية الدفاع: <b>{stance}</b>\n\n"
        "📊 الغارات: <b>{attacks}</b> (الناجحة {attack_wins}) · صُدّت: <b>{holds}/{defenses}</b>\n\n"
        "<i>الغنيمة موارد فقط: {percent}% من مخزون الهدف، وبحد أقصى {cap} لكل مورد. "
        "العملات والروبوتات والكفتة لا تُمَسّ. حركتك ضد وضعية الهدف — "
        "قرار ضد قرار. طلعة واحدة كل {cooldown} ساعة؛ الثأر مجاني.</i>"
    ),
    "raid.ready_line": "السفينة جاهزة للإقلاع",
    "raid.cooldown_line": "إعادة الشحن: بقيت {minutes} دقيقة",
    "raid.shield_on": "الترس نشط حتى {until} UTC",
    "raid.shield_newbie": "حماية المبتدئين (أول {days} أيام)",
    "raid.shield_off": "لا ترس — جمّعه في /workshop",
    "raid.stance_random": "عشوائية (اخترها من القائمة!)",
    "raid.btn_scout": "🔭 الاستطلاع: البحث عن أهداف",
    "raid.btn_revenge": "⚔️ الثأر: {name}",
    "raid.btn_stance": "✊ وضعية الدفاع",
    "raid.btn_workshop": "🛡 تجميع ترس",
    "raid.btn_refresh": "🔄 تحديث",
    "raid.btn_back": "← رجوع",
    "raid.btn_open": "🏴‍☠️ فتح الغارات",
    "raid.btn_again": "🏴‍☠️ إلى الغارات",
    "raid.stance_pick": "✊ <b>وضعية الدفاع</b>\nلا تظهر إلا في نتيجة غارة الآخرين: حركة المهاجم ضد وضعيتك. غيّرها بين حين وآخر — من يسهل التنبؤ به يُنهَب.",
    "raid.stance_saved": "الوضعية: {stance}",
    "raid.scout": "🔭 <b>الاستطلاع وجد أهدافًا.</b> الطلعة تخصم {fuel} 💧. اختر:",
    "raid.btn_target": "🎯 {name} · الموارد ≈{total}",
    "raid.no_targets": "🔭 الاستطلاع لم يجد أحدًا: لا أهداف مناسبة الآن (أتراس، فترات انتظار، مبتدئون). عُد لاحقًا.",
    "raid.pick_move": "✊ <b>ما حركتك؟</b> ستُلعب ضد وضعية دفاع الهدف. الطلعة: −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>الثأر! ما حركتك؟</b> الطلعة مجانية وبلا إعادة شحن.",
    "raid.result_win": "🏴‍☠️ <b>نجحت الغارة!</b>\n{move} ضد {stance} لدى {name}.\nالغنائم: <b>{loot}</b>",
    "raid.result_draw": "😐 <b>تعادل.</b> {move} ضد {stance} لدى {name}. عادت السفينة فارغة واحترق الوقود.",
    "raid.result_lose": "💥 <b>صمد الدفاع.</b> {move} ضد {stance} لدى {name}.\nحصل الهدف على: <b>{loot}</b>",
    "raid.result_footer": "<i>الموارد في /workshop. الترس يحميك من الرد.</i>",
    "raid.victim_lost": "🚨 <b>تعرّضت لغارة!</b> {name}: {move} ضد وضعيتك {stance}.\nخسرت: <b>{loot}</b>\n\n⚔️ الثأر مجاني خلال {hours} ساعة. الترس — في /workshop.",
    "raid.victim_draw": "🛡 <b>صُدّت الغارة بالتعادل.</b> {name}: {move} ضد وضعيتك {stance}. لم تخسر شيئًا.",
    "raid.victim_held": "🛡 <b>صمد دفاعك!</b> {name}: {move} ضد وضعيتك {stance}.\nغنيمة الدفاع: <b>{loot}</b>",
    "raid.err_stance": "❌ حركة غير معروفة.",
    "raid.err_self": "🤨 غارة على نفسك؟ لا.",
    "raid.err_gone": "❌ الهدف غير متاح.",
    "raid.err_teammate": "🤝 لا نغير على أهلنا — هذا زميلك في الفريق.",
    "raid.err_shielded": "🛡 الهدف محميّ بترس. اختر هدفًا آخر.",
    "raid.err_revenge_gone": "❌ أُغلقت نافذة الثأر.",
    "raid.err_cooldown": "⏳ إعادة الشحن: بقيت {minutes} دقيقة.",
    "raid.err_victim_cooldown": "⏳ هذا الهدف تعرّض لغارة مؤخرًا (استراحة {hours} ساعة).",
    "raid.err_fuel": "💧 الهيدروجين لا يكفي: تحتاج {need}، لديك {have}. يُستخرج في أعلى/أقل.",

    # ---------------- ежедневные цели ----------------
    "goal.header": (
        "🎯 <b>أهداف اليوم</b>\n"
        "..................................................\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 الصندوق: <b>+{coins} 🪙</b> و<b>+{res}</b> من مورد عشوائي\n"
        "🔥 السلسلة: <b>{streak}</b> يوم · كل {every} أيام متتالية تضيف +{bonus} 🪙 إلى الصندوق\n\n"
        "<i>تتجدد الأهداف عند 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ أكمل الأهداف الثلاثة — والصندوق لك.",
    "goal.status_ready": "✅ <b>اكتملت كل الأهداف! استلم الصندوق.</b>",
    "goal.status_claimed": "🎁 صندوق اليوم مُستلَم بالفعل. غدًا أهداف جديدة!",
    "goal.btn_claim": "🎁 استلام الصندوق",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 تحديث",
    "goal.toast": "فُتح الصندوق!",
    "goal.chest": "🎁 <b>فُتح الصندوق!</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 السلسلة: {streak} يوم",
    "goal.err_claimed": "🎁 استلمته اليوم بالفعل.",
    "goal.err_not_done": "⏳ لم تكتمل كل الأهداف بعد.",
    "goal.win_quiz": "الفوز بـ{n} جولات في الكويز",
    "goal.win_rps": "الفوز بـ{n} جولات في حجر-ورقة-مقص",
    "goal.win_hl": "الفوز بـ{n} جولات في أعلى/أقل",
    "goal.win_safe": "فتح الخزنة السيبرانية {n} مرات",
    "goal.play_rounds": "لعب {n} جولات في أي ألعاب",
    "goal.duel": "خوض مبارزة",
    "goal.bonus": "استلام كفتة اليوم في المزرعة",
    "goal.craft": "تجميع أي شيء في الورشة",
    "goal.raid": "تنفيذ غارة",
    "goal.market_deal": "إتمام صفقة في البورصة",
    "goal.donate": "المساهمة بموارد في محطة الفريق",

    # ---------------- станция команды ----------------
    "st.header": (
        "🛰 <b>محطة فريق «{team}»</b>\n"
        "..................................................\n"
        "المستوى: <b>{level}/{max}</b> → كل مقاتل يحصل على <b>+{percent}%</b> لتعدين المزرعة "
        "(+{per_level}% عن كل مستوى)\n\n"
        "📦 حتى المستوى التالي:\n{progress}\n\n"
        "🧾 آخر المساهمات:\n{feed}\n\n"
        "🧰 مواردك: {stock}\n"
        "<i>المحطة مشتركة: يبنيها الفريق كله، والمكافأة للجميع. من يغادر الفريق يفقد المكافأة.</i>"
    ),
    "st.max_level": "🏁 اكتمل بناء المحطة — المستوى الأقصى!",
    "st.feed_empty": "لم يساهم أحد بعد — كن أول المساهمين",
    "st.no_team": "🛰 المحطة يبنيها الفريق. انضم إلى فريق أو أنشئ فريقك — وابنوا معًا.",
    "st.btn_find_team": "🏆 الفرق والكلانات",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ الكل: {qty} {icon} {name}",
    "st.btn_refresh": "🔄 تحديث",
    "st.btn_team": "🏆 إلى الفريق",
    "st.toast": "تمت المساهمة +{qty} {icon}",
    "st.level_up": "🛰 <b>ارتقت محطة الفريق إلى المستوى {level}!</b> كل المقاتلين يحصلون الآن على +{percent}% لتعدين المزرعة.",
    "st.err_qty": "❌ كمية غير صحيحة.",
    "st.err_no_team": "❌ أنت لست في فريق.",
    "st.err_max": "🏁 اكتمل بناء المحطة بالفعل (المستوى {max}).",
    "st.err_resources": "🔒 المورد لا يكفي: لديك {have}.",

    # ---------------- команды/кланы (основные поверхности) ----------------
    "clan.no_team": "⚠️ <b>ليس لديك فريق بعد!</b>\n\nيمكنك تسجيل شلتك الخاصة الآن بالضغط على الزر بالأسفل.",
    "clan.btn_create": "🏆 أنشئ فريقًا مقابل 100 ألف",
    "clan.btn_members": "👥 قائمة الزملاء",
    "clan.btn_leave": "🚪 مغادرة الفريق / ترك الشلة",
    "clan.btn_dashboard": "🏆 لوحة الفريق",
    "clan.status_clan": "👑 الحالة: كلان الإمبراطورية",
    "clan.status_team": "👥 الحالة: فريق عادي",
    "clan.dashboard": (
        "🏆 <b>لوحة معلومات فريقك</b>\n"
        "..................................................\n"
        "📌 الاسم: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 كابتن الشلة: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 الشعار: <i>«{motto}»</i>\n"
        "🔮 رمز الشارة: {symbol}\n\n"
        "👥 عدد الأعضاء: <b>{members} / {max_members}</b>\n"
        "..................................................\n"
        "👇 <b>التنقل:</b>"
    ),
    "clan.members_only": "🔒 قائمة الأعضاء مرئية لأعضاء هذا الفريق فقط!",
    "clan.members_gone": "❌ هذا الفريق حُلّ بالفعل.",
    "clan.members_header": (
        "👥 <b>تشكيلة فريق «{name}»</b>\n"
        "🧠 — مستوى ذكاء اللعب (يرتفع فقط في /quiz)\n"
        "..................................................\n"
    ),
    "clan.members_footer": (
        "\n..................................................\n"
        "📄 الصفحة <b>{page} / {pages}</b> · مجموع المقاتلين: <b>{members}</b>\n"
        "<i>اضغط على @username أي زميل لمراسلته وبناء دردشتكم الخاصة "
        "ودعوة الشلة إلى المنافسات الجماعية!</i>"
    ),
    "clan.btn_prev": "⬅️ السابق",
    "clan.btn_next": "التالي ➡️",
    "clan.join_ok": (
        "🎉 <b>مبروك، أنت في اللعبة!</b>\n\nانضممت بنجاح إلى فريق <b>{name}</b>!\n"
        "📍 اكتب الأمر /my_team للاطلاع على التشكيلة!"
    ),
    "clan.leave_ok": "🚪 غادرت فريق <b>{name}</b> بنجاح. أنت الآن طائر حر!",
}

MINIAPP = {
    # TODO(перевод 30.10): персонаж и костюмы — пока по-английски
    "pass_gameCapUp": "With the 30-day unlimited pass — up to {cap} a day.",
    "ref_suitLocked": "🔒 Unlocks at {n} active friends",
    "ref_suitTaken": "✅ Reward claimed: {s}",
    "ref_suitDone": "🧥 The suit is in your bag! Put it on in the Character tab.",
    "ref_suitAsk": "Claim the full “{s}” suit? You can choose only once.",
    "ref_suitPick": "Pick a suit — it goes straight into your bag.",
    "ref_suitProgress": "Active friends: {have} of {n}",
    "ref_suitHint": "Invite {n} friends who become active (intellect level {l} and {c} daily cutlets) — and claim a full suit of your choice: all 5 parts at once. One reward per account.",
    "ref_suitTitle": "🧥 TASK: {n} ACTIVE FRIENDS",
    "pass_gameCap": "Pass XP from game wins today: {x} / {cap}. Expeditions, raids, duels, quests and the chest have no limit.",
    "pass_shopHint": "more coins, cutlets and 4 exclusive season skins",
    "pass_paid": "Premium",
    "pass_free": "Free",
    "pass_tracks": "🛤 REWARDS BY LEVEL",
    "pass_atLvl": "at level {n}",
    "pass_skinsHint": "These skins exist only in the premium pass: once the month ends, they're gone for good.",
    "pass_skins": "✨ SEASON EXCLUSIVES",
    "pass_owned": "✅ Premium pass active",
    "pass_buyHint": "Unlocks the right track, including levels you've already passed. The season's exclusive skins are sold nowhere else — only here and only this month.",
    "pass_buyNext": "🎟 Next season's pass — {p} ★",
    "pass_buy": "🎟 Premium pass — {p} ★",
    "pass_got": "Received: {r}",
    "pass_claim": "🎁 Claim rewards",
    "pass_how": "Pass XP comes from everything: wins, duels, raids, expeditions, crafts, discoveries, quests and the chest.",
    "pass_maxed": "All levels done 🏁",
    "pass_xp": "Level XP: {x} / {need}",
    "pass_level": "Level {n} of {max}",
    "pass_ends": "Season ends in {n} d",
    "pass_title": "🎟 SEASON PASS",
    "shopSkins": "✨ SKINS",
    "ps_noHist": "This part hasn't lived through anything yet — wear it and it will remember every win.",
    "tr_chest": "Chests",
    "tr_quest": "Quests",
    "tr_tech": "Discoveries",
    "tr_craft": "Items crafted",
    "tr_expedition": "Expeditions",
    "tr_raid_def": "Raids endured",
    "tr_raid_win": "Successful raids",
    "tr_raid": "Raids",
    "tr_duel_win": "Duel wins",
    "tr_duel": "Duels",
    "tr_game_win": "Game wins",
    "gr_toGarage": "🏎 My garage",
    "gr_toShop": "🛍 To the skin shop",
    "gr_stUp": "New stage! The skin is now level {n}",
    "gr_feedSame": "same level, XP adds up",
    "gr_feedTo": "→ Lv. {n} · {s}",
    "gr_xpHint": "Battle XP flows while the skin is worn: game win +1, raid +2…3, duel win +3, expedition +5, quest +5, lab discovery +10. Higher stages also need merges.",
    "gr_max": "♾️ Top stage — only glory beyond",
    "gr_nM": "merges: {m}",
    "gr_nXp": "{xp} more XP",
    "gr_next": "To Lv. {n}: {w}",
    "gr_from": "from Lv. {n}",
    "gr_lvl": "Lv. {n} · {s}",
    "gr_st_immortal": "Immortal",
    "gr_st_legend": "Famed",
    "gr_st_veteran": "Veteran",
    "gr_st_combat": "Battle-worn",
    "gr_st_tempered": "Tempered",
    "gr_st_factory": "Factory",
    "gr_stages": "🪜 UPGRADE STAGES",
    "gr_tabPass": "🎟 Pass",
    "gr_fed": "🔥 Tempered! Skin level: {n}",
    "gr_feedAsk": "This skin will vanish for good and become tempering XP. Continue?",
    "gr_noFood": "You need another skin of yours (not worn).",
    "gr_feed": "Absorb",
    "gr_temperHint": "A skin absorbs another skin of yours — that one is gone for good, and part of its XP and merges carries over. Higher stages need both battle XP and merges: one game or one merge won't get you there.",
    "gr_temperTitle": "Tempering",
    "gr_gExo": "💠 Nano exo-armour assembled",
    "gr_gDays": "days in the game",
    "gr_gCargo": "best expedition cargo",
    "gr_gDuels": "duel wins",
    "gr_gQuiz": "intellect level",
    "gr_gWins": "game wins",
    "gr_glory": "🏛 HALL OF FAME",
    "gr_bought": "✨ The skin is yours — see My skins.",
    "gr_marketEmpty": "Nobody is selling skins right now.",
    "gr_marketHint": "Numbered copies with history. Higher tempering and lower numbers cost more. The fee is burned.",
    "gr_market": "🏷 SKIN MARKET",
    "gr_setReward": "Full set reward: {r} (can't be bought)",
    "gr_set_aurora": "🌌 Northern Lights",
    "gr_sets": "🧩 COLLECTIONS",
    "gr_paid": "✨ Paid! The skin will appear in the Garage in a couple of seconds.",
    "gr_buy": "Buy · {p} ★",
    "gr_until": "On sale until {d}",
    "gr_noLimit": "No edition limit",
    "gr_left": "{n} of {of} left",
    "gr_shopHint": "A skin gives no power — only looks and status. Seasonal skins are numbered editions sold only until the season ends: after that, never again.",
    "gr_shop": "🛍 SKINS FOR ★",
    "gr_r_mythic": "Mythic",
    "gr_r_legendary": "Legendary",
    "gr_r_epic": "Epic",
    "gr_r_rare": "Rare",
    "gr_r_common": "Common",
    "gr_t_bag": "bag",
    "gr_t_marker": "map marker",
    "gr_t_title": "title",
    "gr_t_frame": "frame",
    "gr_t_suit": "suit",
    "gr_temper": "Temper",
    "gr_hist": "History: {h}",
    "gr_serialInf": "#{n}",
    "gr_serial": "#{n} of {of}",
    "gr_mineEmpty": "No skins yet. They're sold below, drop in events and change hands on the market.",
    "gr_mine": "✨ MY SKINS",
    "gr_bragText": "Check out my look in ROFL HUB — can you top it?",
    "gr_brag": "📸 Show off",
    "gr_showHint": "This is how others see you: frame and title in the TOP and your team, suit on the avatar, marker on the expedition map.",
    "gr_title": "🏆 GARAGE",
    "gr_tabGarage": "🏆 Garage",
    "gr_tabChar": "🧍 Character",
    "map_art": "💠 every player who arrives gets an artifact",
    "map_gear": "🧥 Every player who arrives gets a suit part",
    "map_finishN": "⏱ Results come early once {n} players reach the target — speed decides",
    "gf_art": "💠 artifact ×{n}",
    "gf_gear": "🧥 suit part ×{n}",
    "gf_done": "🎁 Gift received!",
    "gf_claim": "Claim gift",
    "gf_default": "Gift",
    "gf_hint": "Gifts wait here until they expire — check in often.",
    "gf_title": "🎁 GIFTS FROM THE DEVELOPER",
    "ps_art_en": "Mechanical warrior",
    "ps_art_sc": "Insight orb",
    "ps_art_st": "Phantom shade",
    "ps_art_ml": "Crimson sunset",
    "ps_art_mn": "Stone of plenty",
    "ps_art_el": "Storm heart",
    "ps_artsText": "Stones for the three belt windows. Each boosts its own line and works together with your suit. One free per season (gifts and expeditions), the rest on the market.",
    "ps_arts": "💠 ARTIFACTS",
    "ps_seasonArt": "artifacts: {got} of {cap}",
    "ps_upgrade": "Upgrade",
    "ps_partOf": "Full suit: {e}.",
    "ps_artsActive": "💠 القطع الأثرية على الحزام:",
    "ps_sellHow": "لبيع قطعة أو قطعة أثرية، اضغط عليها في الحقيبة أعلاه ← «بيع». يمكن عرض قطع المستوى الأساسي فقط.",
    "ps_artGives": "On the belt: {e}. Stacks with your suit.",
    "ps_pickHint": "Tap a bag cell to see what it is and what you can do with it.",
    "ps_belt": "BELT",
    "tab_persona": "🧍 Character",
    "ps_title": "🧍 CHARACTER",
    "ps_hint": "Wear a full suit — 5 parts of the same suit: the bonus works while you wear it.",
    "ps_m": "M",
    "ps_f": "F",
    "ps_slot_head": "Helmet",
    "ps_slot_body": "Jacket",
    "ps_slot_hands": "Gloves",
    "ps_slot_legs": "Trousers",
    "ps_slot_feet": "Boots",
    "ps_suit_el": "⚡ Electrician",
    "ps_suit_mn": "⛏ Miner",
    "ps_suit_ml": "🪖 Soldier",
    "ps_suit_st": "🥷 Stealth",
    "ps_suit_sc": "🔬 Scientist",
    "ps_suit_en": "🔧 Engineer",
    "ps_suit_exo": "💠 Nano exo-armour",
    "ps_eff_el": "electricity drops in {p}% of game wins",
    "ps_eff_mn": "once a day +{p}% of the coins your farm mined",
    "ps_eff_ml": "+{p}% raid loot and expedition haul, trips {p}% faster",
    "ps_eff_st": "{p}% chance to stay off raiders' scouting lists",
    "ps_eff_sc": "{p}% shorter wait between technology levels",
    "ps_eff_en": "workshop recipes need {p}% fewer resources",
    "ps_active": "Suit on: {s} · {n}",
    "ps_none": "No full suit on — no bonuses yet.",
    "ps_level": "lvl {n}",
    "ps_empty": "empty",
    "ps_off": "Take off",
    "ps_wear": "Wear",
    "ps_sell": "Sell",
    "ps_bag": "🎒 BAG",
    "ps_bagEmpty": "Your bag is empty. Suit parts drop in events: expeditions, mine battles and seasonal giveaways.",
    "ps_season": "Parts this season: {got} of {cap}",
    "ps_suits": "📖 SUITS AND BONUSES",
    "ps_upg_el": "Rewind the wiring with copper, sew in grounding and fit a fresh battery — the suit starts catching sparks.",
    "ps_upg_mn": "Stitch the seams with steel thread and pad the elbows with stone — the suit takes a rockfall.",
    "ps_upg_ml": "Weld on plates, fire and temper them — this armour shrugs off an ambush.",
    "ps_upg_st": "Soak the fabric in hydrogen gel and sew on chameleon bark — the suit melts into the background.",
    "ps_upg_sc": "Weave in crystal sensors and run a current — the suit whispers formulas.",
    "ps_upg_en": "Swap the fasteners for precision parts and build in a battery — the suit saves every bolt.",
    "ps_upgAsk": "Upgrade “{part}” to {lv}? Costs: {cost} and {c} 🪙.",
    "ps_lvlName_1": "Basic",
    "ps_lvlName_2": "Improved",
    "ps_lvlName_3": "Legendary",
    "ps_xp": "Part XP: {x} / {need}",
    "ps_xpHint": "XP is what the part lived through while worn: game wins, duels, raids, expeditions, crafts, discoveries, quests.",
    "ps_needTech": "{t} tech level {n} in the Lab",
    "ps_xpNeed": "XP {n}",
    "ps_needTitle": "To {lv}:",
    "ps_maxLvl": "🏆 Legendary — as high as it gets",
    "ps_upgDone": "⬆️ Part upgraded: {lv}!",
    "ps_exoTitle": "💠 NANO EXO-ARMOUR",
    "ps_exoText": "A fusion of all six Improved suits (30 parts): every bonus at once. Fused parts are gone for good.",
    "ps_exoHave": "Improved parts",
    "ps_exoGo": "💠 Fuse the armour",
    "ps_exoAsk": "Fuse 30 parts into nano exo-armour? This is permanent.",
    "ps_exoDone": "💠 Nano exo-armour is ready and on!",
    "ps_market": "🏷 PARTS & ARTIFACTS MARKET",
    "ps_marketHint": "Level-1 parts from {min} 🪙, artifacts from {amin} 🪙. The {fee}% fee is burned.",
    "ps_marketEmpty": "Nobody is selling parts right now.",
    "ps_buy": "Buy for {p} 🪙",
    "ps_bought": "🧥 The part is in your bag!",
    "ps_myLots": "My lots",
    "ps_cancel": "Withdraw",
    "ps_sellTitle": "Sell",
    "ps_price": "Price per item, 🪙 (from {min})",
    "ps_qty": "How many",
    "ps_sellGo": "List it",
    "ps_listed": "🏷 Listed on the parts market",
    "raid_note_suit": "🪖 Soldier suit: bigger loot",
    "qs_fiction": "جميع الشخصيات والأسماء والأحداث في هذه القصص من نسج الخيال. وأي تشابه مع أشخاص حقيقيين، أحياء أو أموات، أو مع أحداث حقيقية هو محض مصادفة.",
    "qs_check": "تحقّق",
    "qs_tries": "المحاولات: {n}",
    "qs_wrong": "❌ خطأ. المحاولات المتبقية: {n}",
    "qs_timeUp": "⏱ انتهى الوقت!",
    "qs_timer": "⏱ وقت القرار",
    "qs_answerPh": "إجابتك",
    "news_season": "🏁 المنتهية منذ اليوم الأول من الشهر: كل شهر موسم جديد وتعود فرص الجميع متساوية.",
    "qs_fxOff": "إيقاف المؤثرات:",
    "qs_fxOn": "تشغيل المؤثرات:",
    "tab_guide": "🧭 طريقة اللعب",
    "dl_premOn": "⚡ You have Unlimited — the winnings fee is {b}% instead of {a}%.",
    "dl_premOff": "⚡ With Unlimited the winnings fee is {b}% instead of {a}%.",
    "md_title": "🧭 كيف تريد أن تلعب؟",
    "md_hint": "ROFL HUB عالم كبير. اختر من أين تبدأ — يمكن تغيير الوضع في أي وقت من الجواز.",
    "md_full": "🌐 المنظومة كاملة",
    "md_fullText": "مزرعة الروبوتات، المخزون، الورشة، البورصة، الفرق، الغارات، المناجم وخريطة العالم — إضافة إلى كل الألعاب والقصص. كل الأقسام مفتوحة من البداية.",
    "md_puzzle": "🧩 ألعاب وقصص",
    "md_puzzleText": "الكويز والألعاب المصغّرة والمهام وقضية اليوم والمبارزات مع الأصدقاء فقط. بلا اقتصاد ولا تبويبات زائدة.",
    "md_later": "المزرعة تعمل في أي وضع — العملات تتراكم حتى لو لم تزرها.",
    "md_toFull": "تفعيل المنظومة كاملة؟ ستظهر المزرعة والمخزون والبورصة والفرق وبقية الأقسام.",
    "md_toPuzzle": "الإبقاء على الألعاب والقصص فقط؟ ستواصل المزرعة العمل، وتختفي بقية التبويبات — ويمكن إعادتها من هنا.",
    "md_now": "🧭 الوضع: {m} · تغيير",
    "lk_new": "🎉 فُتحت أقسام جديدة: <b>{t}</b>. اضغط لإلقاء نظرة!",
    "di_title": "⚔️ لديك تحدٍّ لمبارزة!",
    "di_text": "<b>{n}</b> يتحداك في مبارزة حجر-ورقة-مقص.<br>الرهان {s} 🪙 · للفائز {p} 🪙.",
    "di_accept": "⚔️ قبول التحدي",
    "di_decline": "ليس الآن",
    "di_waiting": "بانتظار صديقك على طاولة {s} 🪙…",
    "di_left": "يبقى التحدي صالحًا {h} ساعة أخرى — ثم يعود رهانك",
    "di_share": "📤 أرسل التحدي إلى صديق",
    "di_waitHint": "أرسل الرابط إلى صديق. عند قبول التحدي سيراسلك البوت في الدردشة. رهانك على الطاولة؛ إن غيّرت رأيك فغادر الطاولة ويعود إليك.",
    "di_head": "🤝 تحدَّ صديقًا",
    "di_hint": "طاولة خاصة عبر رابط: لا تدخل الطابور، وتنتظر صديقك فقط. اللاعب الجديد الذي ينضم عبر الرابط يصبح صديقك.",
    "di_table": "🤝 تحدَّ صديقًا · طاولة {s} 🪙",
    "di_shareText": "أتحداك في مبارزة على ROFL HUB! الرهان {s} 🪙 — لنرَ من يفوز 😎",
    "ac_title": "🏅 إنجازاتي",
    "ac_streak": "🔥 سلسلة قضايا اليوم: {n}",
    "ac_hint": "كل إنجازاتك في بطاقة واحدة — انشرها في قصتك أو أرسلها إلى صديق.",
    "ac_make": "📸 إنشاء البطاقة",
    "ac_cardSub": "إنجازاتي",
    "ac_cardCall": "هل تستطيع التفوّق؟",
    "ac_shareText": "نتيجتي في ROFL HUB: 🧠 المستوى {l}، 🗺 {q} مهمة، 🕵️ {d} قضية، ⚔️ {w} فوز في المبارزات. هل تستطيع التفوّق؟",
    "ac_story": "📲 انشر في قصتي",
    "ac_send": "✈️ أرسل إلى صديق",
    "ac_save": "💾 حفظ الصورة",
    "ac_quests": "مهام مكتملة",
    "ac_epics": "ملاحم",
    "ac_cases": "قضايا محلولة",
    "ac_duels": "فوز في المبارزات",
    "ac_wins": "فوز في الألعاب",
    "ac_friends": "أصدقاء نشطون",
    "ac_robots": "روبوتات",
    "ac_days": "أيام في اللعبة",
    "tf_title": "💸 تحويل العملات",
    "tf_hint": "إلى صديق — عبر @username أو ID أو VIP ID. الحد الأدنى {m} 🪙، العمولة {f}%.",
    "tf_locked": "🔒 إرسال العملات متاح من 🧠 المستوى {l} وبعد استلام {c} كفتات يومية — حتى لا تستنزف الحسابات الوهمية عملات البداية. الاستلام متاح فورًا.",
    "tf_to": "إلى",
    "tf_amount": "كم 🪙",
    "tf_btn": "💸 تحويل",
    "tf_ask": "تحويل {a} 🪙 إلى {to}؟ العمولة {f} 🪙، وسيصل للمستلم {r} 🪙.",
    "tf_done": "تم! وصل إلى {to} {r} 🪙",
    "sq_choose": "اختر ما تريد إنشاءه:",
    "sq_squad": "🛡 فرقة",
    "sq_squadText": "حتى {n} مقاتلين · {c} 🪙. لك ولعدد من الأصدقاء؛ لاحقًا يستطيع القائد توسيعها إلى فريق.",
    "sq_team": "🏆 فريق",
    "sq_teamText": "حتى {n} مقاتل · {c} 🪙. فريق كبير للمعارك والمناجم.",
    "sq_createBtn": "إنشاء فرقة مقابل {cost} 🪙",
    "sq_created": "تم إنشاء الفرقة «{n}» — أنت القائد!",
    "sq_label": "فرقة",
    "sq_upHint": "ضاقت الفرقة؟ وسّعها إلى فريق — حتى {n} مقاتل.",
    "sq_upBtn": "⬆️ التوسيع إلى فريق · {c} 🪙",
    "sq_upAsk": "توسيع الفرقة إلى فريق مقابل {c} 🪙؟ سيصبح عدد الأماكن {n}.",
    "sq_upDone": "أصبحت فرقتك فريقًا!",
    "cs_title": "🕵️ قضية اليوم",
    "cs_tile": "قضية واحدة للجميع · 4 مشتبه بهم · اتهام واحد",
    "cs_none": "لا قضايا اليوم — عد غدًا.",
    "cs_culprit": "الجاني",
    "cs_accuse": "👉 اتهام",
    "cs_clueLocked": "الدليل {n} — ما زال مخفيًا",
    "cs_more": "🔍 اكشف دليلًا آخر (تصبح المكافأة {r} 🪙)",
    "cs_rules": "يمكن اتهام شخص واحد فقط ومرة واحدة فقط. كلما قلّت الأدلة التي احتجتها زادت المكافأة:",
    "cs_solved": "🎉 حُلّت القضية! +{r} 🪙",
    "cs_failed": "خطأ! الجاني هو {n}.",
    "cs_bonus": "🔥 مكافأة السلسلة: +{b} 🪙",
    "cs_solution": "الحل:",
    "cs_stats": "حُلّت اليوم: {s} من {p} · متوسط الأدلة: {a}",
    "cs_share": "📤 تباهَ بها",
    "cs_next": "قضية جديدة بعد {t}",
    "cs_head": "🕵️ القضية رقم {n}",
    "cs_suspects": "👥 المشتبه بهم",
    "cs_clues": "🔍 الأدلة",
    "cs_streak": "🔥 سلسلة القضايا المحلولة: {n} · كل يوم رقم {e} على التوالي +{b} 🪙",
    "cs_accuseAsk": "اتهام {n}؟ الاتهام مرة واحدة — لا تراجع عنه.",
    "cs_shareText": "🕵️ قضية اليوم رقم {n}\n{s}\n🔥 السلسلة: {k}\nهل تستطيع حلّها أسرع؟",
    "qs_epicPaid": "⚡ مع «بلا حدود»",
    "qs_paper": "📝 نصيحة: دوّن التفاصيل على ورقة — الحلّ أسهل على المنتبهين.",
    "qs_total": "📚 المهام في المكتبة: {n}",
    "qs_daily": "الجديدة اليوم: {a}/{b}",
    "qs_dailyUnl": "⚡ بلا حدود — المهام دون قيود",
    "qs_locked": "🔒 حتى 00:00 UTC",
    "qs_lockedNote": "أكملت اليوم {b} مهام جديدة. تُفتح البقية عند 00:00 UTC، ويمكنك إعادة المهام المكتملة كما تشاء. ⚡ وضع «بلا حدود» يرفع القيد.",
    "qs_epic": "⭐ ملحمة ·",
    "qr_btn": "⚠️ الإبلاغ عن السؤال",
    "qr_title": "ما المشكلة في السؤال؟",
    "qr_answer": "❌ الإجابة الصحيحة خاطئة",
    "qr_question": "✏️ خطأ أو خطأ إملائي في السؤال",
    "qr_dup": "🔁 السؤال يتكرر",
    "qr_other": "🤔 شيء آخر (غير واضح، مثير للجدل)",
    "qr_thanks": "شكرًا! سنراجع السؤال ونصححه.",
    "qr_limit": "يكفي هذا العدد من البلاغات اليوم — شكرًا على مساعدتك!",
    # TODO(перевод 26.10): атмосферы квестов (27.10)
    "qs_fxGallery": "🎨 Atmosphere gallery",
    "qs_fxChoice": "🚪 Step inside",
    "qs_fxSample": "Night. You stand at the entrance and listen to the world around you. Something changes — and the scene answers with light, shadow and motion. Pick an atmosphere below to see how it looks under quest text.",
    # TODO(перевод 26.10): дуэли в приложении (27.10)
    "dl_title": "⚔️ Duels",
    "dl_tile": "A live opponent · tables 10 / 100 / 1000 🪙",
    "dl_intro": "Rock-paper-scissors against a live player. The stake is taken right away; the winner gets {p}% of the bank, {b}% burns. {t} s per gesture, a draw is replayed.",
    "dl_table": "⚔️ Table {s} 🪙 · win +{p} 🪙",
    "dl_short": "You need {s} 🪙 on your balance for this table",
    "dl_waiting": "Looking for an opponent at the {s} 🪙 table…",
    "dl_waitLeft": "The queue cancels in {m} min — your stake comes back",
    "dl_waitHint": "You can close the app: once an opponent is found, the bot will message you in the chat.",
    "dl_cancel": "❌ Leave the table (refund stake)",
    "dl_matched": "Opponent found! Bank {b} 🪙 · winner gets {p} 🪙",
    "dl_round": "🤝 Draw — replay! Round {n}",
    "dl_pick": "Pick a gesture",
    "dl_wait": "Gesture locked in — waiting for your opponent…",
    "dl_oppMoved": "⚡ Your opponent has already moved!",
    "dl_timeoutNote": "Run out of time and chance picks your gesture.",
    "dl_win": "🎉 Duel won! +{p} 🪙",
    "dl_lose": "Defeat. Your {s} 🪙 stake went to your opponent's bank.",
    "dl_vs": "You: {a} · Opponent: {b}",
    "dl_cancelled": "You left the table — your {s} 🪙 stake is back on your balance.",
    "dl_again": "⚔️ Another duel",
    # TODO(перевод 26.10): квесты в приложении (27.10)
    "g_name_quests": "🗺 Quests",
    "qs_tile": "Stories with choices · reward for the first win",
    "qs_ruOnly": "Quests are in Russian for now — a translation is on the way.",
    "qs_done": "✅ completed",
    "qs_progress": "⏯ in progress",
    "qs_new": "🆕 new",
    "qs_info": "{g} · {m} min · +{r} 🪙 for the first win",
    "qs_start": "▶️ Start",
    "qs_resume": "⏯ Continue",
    "qs_restart": "🔄 Start over",
    "qs_list": "‹ All quests",
    "qs_again": "🔄 Play again",
    "qs_winFirst": "🏆 Quest completed! +{c} 🪙 and 🪨 {q}",
    "qs_winRepeat": "✅ Completed again! The reward for this quest was already claimed.",
    "qs_fail": "💀 Not the best ending… You can always replay the story!",
    "qs_stale": "That scene is behind you — continuing from where you are",
    "qs_empty": "No quests yet — check back later.",
    # TODO(перевод 26.10): игры и аукцион (27.10)
    "g_sometimes": "Sometimes: +1 ⚡",
    "auc_short": "You need {n} more 🪙 for this bid",
    "auc_confirm": "Bid on “{t}”? {c} 🪙 will be held (returned if you are outbid).",
    # TODO(перевод 26.10): новые игры приложения (27.10)
    "g_streak": "Streak: {i} {a}/{b}",
    "g_every": "{i} for every {n} wins",
    "g_win_coins": "Win: +{r} 🪙",
    "flags_q_flag": "Whose flag is this?",
    "flags_q_cap": "What is the capital of {c}?",
    "code_rules": "Crack a code of {d} different digits in {m} tries. 🐂 — right digit in the right place, 🐄 — right digit in the wrong place.",
    "code_left": "Tries left: {n}",
    "code_try": "Check",
    "mem_rules": "Find all {p} pairs in {m} moves. A move is turning over two cards.",
    "mem_moves": "Moves: {a}/{b}",
    # TODO(перевод 26.10): игры в приложении
    "tab_games": "🕹 Games",
    "g_limit_btn": "⚡ Lift the limit",
    "g_limit_text": "You've used up today's wins in this game. New ones come after 00:00 UTC. Or turn on ⚡ Unlimited and play without limits.",
    "g_limit_title": "⏳ LIMIT FOR TODAY",
    "g_credited": "Credited: {x}",
    "g_charged": "Charged: {x}",
    "g_title": "🕹 GAMES",
    "g_hint": "Win to earn coins and resources. Each game has its own daily win limit (resets at 00:00 UTC).",
    "g_unlimited": "⚡ Unlimited is on — win as much as you like",
    "g_limit": "limit reached · 🔓 can be lifted",
    "g_soon": "soon",
    "g_back": "‹ All games",
    "g_again": "Again",
    "g_balance": "Balance: {b} 🪙",
    "g_name_rps": "✊ Rock-paper-scissors",
    "g_name_hl": "🔼 Higher-Lower",
    "g_name_safe": "🔐 Cyber Safe",
    "g_name_quiz": "🧠 Quiz",
    "g_name_words": "🔤 Words from a word",
    "g_name_math": "➗ Math",
    "g_name_flags": "🏳️ Flags and capitals",
    "g_name_code": "💻 Code breaker",
    "g_name_memory": "🃏 Memory",
    "g_prize": "Win: +{r} 🪙 and {i}",
    "g_win": "🎉 Victory!",
    "g_lose": "Defeat!",
    "g_draw": "🤝 Draw!",
    "g_timeout": "⏱ Time's up!",
    "g_level": "🎉 New intelligence level: {l}! +{b} 🪙",
    "g_intern": "🤖 A new Robot Intern is waiting on the farm",
    "g_full": "storage full",
    "rps_pick": "Pick a gesture — the bot picks at the same time.",
    "rps_rock": "✊ Rock",
    "rps_scissors": "✌️ Scissors",
    "rps_paper": "✋ Paper",
    "rps_vs": "You: {a} · Bot: {b}",
    "hl_q": "Will the next number from 1 to 100 be higher or lower?",
    "hl_up": "▲ Higher",
    "hl_down": "▼ Lower",
    "hl_was": "It was: {n}",
    "hl_next": "Next number",
    "safe_q": "Guess the safe code: one of {n}.",
    "safe_code": "The code was: {n}",
    "quiz_of": "Question {a}/{b}",
    "quiz_hint": "💡 50/50 · {c} 🪙",
    "quiz_next": "Next ›",
    "quiz_correct": "Correct answer: {a}",
    "quiz_sum_title": "🏁 ROUND OVER",
    "quiz_sum": "Correct answers",
    "quiz_coins": "Coins this round",
    "quiz_again": "Another round",
    "quiz_level": "🧠 Level {l} · {a}/{b} correct to the next",
    # TODO(перевод 26.10): история — пока по-английски
    "tab_history": "📜 History",
    "hist_title": "📜 HISTORY FOR {d} DAYS",
    "hist_coins": "🪙 Coins",
    "hist_res": "📦 Resources",
    "hist_market": "📈 Market",
    "hist_gifts": "🎁 Rewards",
    "hist_in": "In",
    "hist_out": "Out",
    "hist_topIn": "Where they came from",
    "hist_topOut": "Where they went",
    "hist_empty": "Nothing here for this period.",
    "hist_bought": "Bought",
    "hist_sold": "Sold",
    "hist_hint": "Kept for 30 days: coins, resources, market deals, rewards and gifts.",
    "mk_floorAny": "At least {p} 🪙 per 1 {x} — for sales and buy orders",
    "mk_sellTitleAny": "💰 SELL: {x}",
    "mk_bidTitleAny": "🙋 BUY: {x}",
    "mk_qtyAny": "Amount, {x}",
    "mk_limitsAny": "Up to {q} {x} per order, up to {o} open orders",
    "mk_boughtAny": "Bought {q} {x} for {t} 🪙",
    "mk_cancelledAny": "Order cancelled — your goods or frozen coins are back",
    # TODO(перевод 26.10): события, аукционы, развилки — пока по-английски
    "map_cargoHint": "📦 Cargo is your run score: you start with 100, forks add or take away. Places are ranked by cargo.",
    "map_forkAhead": "Fork in {t} — choose ahead",
    "map_forkNow": "The squad is at the fork! {t} left to decide — otherwise the squad walks past (no loot, no losses, no delay).",
    "map_voteTeam": "Votes: {a} of {b}. If everyone votes, it applies right at the fork; otherwise the majority decides.",
    "map_myChoice": "your choice",
    "news_title": "📣 EVENTS",
    "news_hint": "All announcements live here: battles, world map runs and auctions. Tap to open.",
    "news_empty": "All quiet for now. As soon as a battle, a run or an auction starts, it shows up here.",
    "news_left": "⏳ {t}",
    "news_won": "🏁 {w}",
    "news_done": "🏁 results are in",
    "tab_auctions": "🔨 Auctions",
    "auc_title": "🔨 AUCTIONS",
    "auc_empty": "No lots yet. VIP IDs and other prizes go up from time to time — check back later.",
    "auc_price": "Current price",
    "auc_leader": "Leader",
    "auc_noBids": "no bids yet",
    "auc_you": "👑 you lead",
    "auc_ends": "Ends in",
    "auc_noEnd": "until the team closes it",
    "auc_bid": "💥 +{s} · costs {c} 🪙",
    "auc_balance": "You have: {b} 🪙",
    "auc_rules": "Bids are refundable: if you are outbid, your coins come back at once. Only the winner pays — those coins burn. A VIP ID moves to the winner automatically; other prizes are handed over by the team.",
    "auc_sold": "🏁 Sold for {p} 🪙",
    "auc_unsold": "🏁 Closed with no bids",
    "auc_closed": "Finished lots",
    "auc_done": "💥 Bid accepted! Lot price: {p} 🪙",
    "map_peek": "🔎 Scout this fork · {n} left",
    "map_peeked": "🔎 Fork scouted — outcomes visible to the whole squad",
    "map_peekBlind": "🙈 The first expedition of the season is blind.",
    # TODO(перевод 28.10): карта мира и дроны — пока английский
    "tab_map": "🗺 Map",
    "map_title": "🗺 WORLD MAP",
    "map_empty": "No targets yet. They appear on the map from time to time — check back later.",
    "map_hint": "The map has solo runs and team squad runs (each target sets its format). Arrive before the results — latecomers are out.",
    "map_resolve": "Results in {t}",
    "map_squads": "Squads: {n}",
    "map_forks": "Forks on the way: {n}",
    "map_path": "Travel",
    "map_mode_solo": "👤 solo",
    "map_mode_team": "🏆 team",
    "map_mode_clan": "👑 clan",
    "map_ok": "in time",
    "map_no": "too late",
    "map_prizes": "Prizes by place",
    "map_rewardAll": "🎒 For taking part: {r}",
    "map_goSolo": "👤 Go solo · 💧 {n}",
    "map_gearBattery": "🔋 Add a battery · {a}/{b}",
    "map_gearCutlet": "🥩 Add a cutlet · {a}/{b}",
    "map_gearHint": "Squad members add gear one piece at a time. Full kit — the squad sets out on its own. Not gathered in time — everything is returned.",
    "map_needTeam": "Team ranking — join a team to march as a squad.",
    "map_notYours": "This target isn't for your squad.",
    "map_my": "🚩 MY SQUAD",
    "map_gathering": "Gathering gear",
    "map_marching": "On the way · arriving in {t}",
    "map_arrived": "Arrived — waiting for the results",
    "map_late": "Running late — take shortcuts at the forks!",
    "map_cargo": "📦 Cargo",
    "map_fork": "Fork {k} of {n}",
    "map_vote": "Voting for {t} more. The team majority decides.",
    "map_voteSolo": "Your choice applies as soon as you reach the fork. You can change it until then.",
    "map_votes": "votes: {n}",
    "map_myVote": "your vote",
    "map_noHint": "A squad can scout as many forks as its leader has 🛰 Spy drones and 🔭 Scouting levels — whichever is lower. The rest are blind.",
    "map_waitFork": "The next fork is further down the road.",
    "map_log": "Travel log",
    "map_effects": "Squad drones: ⚔️ +{a}% loot · 🛡 −{g}% losses · 🛰 −{s}% travel",
    "map_you": "You",
    "map_done": "✅ The squad has set out!",
    "map_added": "✅ Added",
    "map_voted": "🗳 Choice saved",
    "map_fight": "force",
    "map_pick": "Tap a target on the map — or pick one in the list below.",
    "dr_title": "🤖 COMBAT DRONES",
    "dr_guard": "🛡 Guard drone",
    "dr_attack": "⚔️ Attack drone",
    "dr_spy": "🛰 Spy drone",
    "dr_hint": "Personal companions in raids and expeditions. Effects stack; drones are never used up and take no storage.",
    "dr_eff_guard": "Raid on you: −{rg}% to the raider's loot · expeditions: −{eg}% cargo losses. Per drone.",
    "dr_eff_attack": "Your raid: +{ra}% loot · expeditions: +{ec}% to force loot. Per drone.",
    "dr_eff_spy": "Raid scouting: +{st} target · expeditions: {es}% shorter trip, and with the leader's 🔭 Scouting — fork scouting. Per drone.",
    "dr_buy": "Buy for {c} 🪙",
    "dr_bought": "🤖 Drone deployed!",
    "dr_have": "You have: {n}",
    "eff_bdrone": "combat drone — a personal companion in raids and expeditions",
    "raid_note_drones": "🤖 Combat drones kicked in",
    # TODO(перевод): холодильник на ферме — пока английский, переводится следующим заходом
    "fr_title": "🧊 FRIDGE", "fr_cap": "holds {n} 🥩",
    "fr_hint": "Drillers take cutlets from the fridge on their own — the bigger it is, the longer the farm runs without you.",
    "fr_up": "Bigger:", "fr_max": "You have the biggest fridge.",
    "subtitle": "إمبراطوريتك في اللعب على شاشة واحدة",
    "tab_passport": "📋 الجواز",
    "tab_farm": "🚜 المزرعة",
    "tab_goals": "🎯 الأهداف",
    "tab_workshop": "🔧 الورشة",
    "tab_raids": "🏴‍☠️ الغارات",
    "tab_market": "📈 البورصة",
    "tab_team": "🏆 الفريق",
    "tab_shop": "🏪 المتجر",
    "tab_top": "👑 الأفضل",
    "passport": "📋 جواز اللاعب",
    "coins": "🪙",
    "brain": "🧠 مستوى الذكاء",
    "toNext": "حتى المستوى {n}: {left} إجابة صحيحة في الكويز (+{reward} 🪙)",
    "farm": "🚜 المزرعة السيبرانية",
    "robots": "الروبوتات (معدِّنات / حفّارات)",
    "intern": "روبوتات المتدرّبين (1 🪙/ساعة، دائمة)",
    "activateIntern": "🚀 تفعيل روبوت المتدرّب",
    "claimIntern": "🎁 استلم المتدرّب ({n})",
    "internDone": "🤖 روبوت المتدرّب بدأ نوبته!",
    "rank": "🎖 الرتبة",
    "openFarm": "🏭 افتح المنجم",
    "farmScene": "🏭 مزرعتك",
    "back": "← رجوع",
    "minedVisit": "تم استخراجه خلال هذه الزيارة",
    "unit_intern": "روبوت المتدرّب",
    "unit_junior": "روبوت التعدين",
    "unit_premium": "الحفّار السيبراني",
    "eternal": "دائم",
    "fueledAll": "مزوّدة بالوقود",
    "fueledPart": "{a} من {b} مزوّدة بالوقود",
    "license": "رخصة 30 يومًا",
    "emptyFarm": "المنجم فارغ. فعّل روبوت المتدرّب أو احصل على روبوتات من المتجر!",
    "madeBy": "تريد روبوتًا كهذا لمشروعك؟ راسل @mister_telebot",
    "fueled": "الحفّارات المزوّدة بالوقود",
    "speed": "سرعة التعدين",
    "perHour": "{v} 🪙/ساعة",
    "fridge": "الثلاجة",
    "inv": "كفتات في المخزون",
    "burnout": "أقرب احتراق",
    "boosts": "المعزّزات النشطة",
    "none": "لا شيء",
    "resources": "🧰 الموارد",
    "bonusPct": "مكافأة دائمة للتعدين",
    "shuttle": "🚀 المكوك مُجمَّع",
    "resHint": "كل فوز يمنحك مورد لعبته، ومع إزالة حدود الفوز — بلا قيود. أنفق الموارد في الورشة.",
    "bonusReady": "🎁 استلم كفتة اليوم",
    "bonusWait": "⏳ المكافأة بعد {h} س {m} د",
    "bonusDone": "🎉 الكفتة في المخزون!",
    "team": "🏆 فريقي",
    "clan": "كلان",
    "teamLabel": "فريق",
    "captain": "👑 أنت الكابتن!",
    "members": "التشكيلة",
    "noTeam": "لا فريق لديك بعد: انضم إلى فريق من الروليت أو البحث — أو أنشئ فريقك.",
    "tab_faq": "📚 FAQ",
    "tab_rules": "📜 الاتفاقية",
    "tm_roulette": "🎲 روليت الفرق",
    "tm_rotate": "🔄 عرض فرق أخرى",
    "tm_noFree": "لا توجد فرق شاغرة بعد — أنشئ فريقك!",
    "tm_search": "🔍 البحث عن فريق",
    "tm_searchPh": "الاسم أو جزء منه",
    "tm_searchBtn": "بحث",
    "tm_notFound": "لا توجد فرق بهذا الاسم",
    "tm_join": "💥 انضمام",
    "tm_joined": "أنت الآن في فريق «{n}»!",
    "tm_create": "🏆 إنشاء فريق",
    "tm_hubHint": "فريق يضم حتى 50 مقاتلًا يكلّف {cost} 🪙. ويمكن ترقيته في المتجر إلى ميغا-كلان بـ 1000 مقعد.",
    "tm_name": "الاسم (حتى {n} حرفًا)",
    "tm_motto": "الشعار (حتى {n} حرفًا)",
    "tm_symbol": "الرمز — إيموجي (حتى {n} حرفًا)",
    "tm_createBtn": "إنشاء مقابل {cost} 🪙",
    "tm_created": "أُنشئ فريق «{n}» — أنت الكابتن!",
    "tm_noMoney": "تحتاج {cost} 🪙 ولديك {b} 🪙",
    "tm_roster": "👥 تشكيلة الفريق",
    "tm_mottoL": "💬 الشعار",
    "tm_leave": "🚪 مغادرة الفريق",
    "tm_leaveAsk": "هل تريد مغادرة فريق «{n}»؟",
    "tm_leaveAskCaptain": "أنت الكابتن: ستنتقل القيادة إلى قدامى الفريق. هل تريد مغادرة «{n}»؟",
    "tm_left": "لم تعد في أي فريق",
    "mk_scopePublic": "🌐 البورصة العامة",
    "mk_scopeTeam": "🏆 بورصة الفريق",
    "mk_teamHint": "بورصة فريق «{t}»: العروض يراها ويشتريها زملاء الفريق فقط، والعمولة {f}% فقط.",
    "mk_yourStock": "📦 لديك",
    "mk_yourCoins": "💰 رصيدك من العملات",
    "tm_market": "🏪 بورصة الفريق",
    "tm_marketBtn": "افتح بورصة الفريق",
    "tm_marketHint": "تاجر مع زملاء الفريق: عمولة {f}% بدل {p}% في البورصة العامة. وفي الميغا-كلان — {c}% فقط.",
    "hp_title": "🤝 المساعدة المتبادلة",
    "hp_hint": "ينقصك مورد؟ اطلبه من فريقك. يمكن لكل لاعب إهداء حتى {d} من الموارد يوميًا.",
    "hp_today": "ما أهديته اليوم: {g} / {d}",
    "hp_empty": "لا أحد يطلب المساعدة حتى الآن",
    "hp_give": "🎁 +{n}",
    "hp_kind": "ما الذي تحتاجه",
    "hp_qty": "الكمية (حتى {n})",
    "hp_ask": "🙏 اطلب المساعدة",
    "hp_given": "تم الإهداء: {q} {k} — شكرًا على اللعب بروح الفريق!",
    "hp_asked": "أُرسل طلبك إلى الفريق!",
    "tab_storage": "📦 المخزون",
    "tab_mines": "⛏ المناجم",
    "tab_info": "📚 معلومات",
    "tab_lab": "🔬 المختبر",
    "as_stone": "الحجر",
    "as_wood": "الخشب",
    "as_fire": "النار",
    "as_energy": "الكهرباء",
    "as_battery": "البطاريات",
    "as_cow": "الأبقار",
    "as_core": "النواة",
    "tool_1": "أدوات خشنة",
    "tool_2": "أدوات الضبط الدقيق",
    "tool_3": "المعايرة",
    "tool_4": "التقنيات النانوية",
    "tech_comm": "الاتصالات",
    "tech_scout": "الاستطلاع",
    "tech_attack": "الهجوم",
    "tech_defense": "الدفاع",
    "tech_science": "العلوم",
    "ws_needTool": "المطلوب: {t}",
    "ws_teamItem": "🏆 عنصر جماعي — يحمي الفريق كله (للعشيرة الكبرى السعر ×{x})",
    "eff_make": "تتحول المواد الخام إلى مادة في المخزون",
    "eff_cart": "عربة لكل حصان: +1 عرض في البورصة",
    "eff_meds": "لا أمراض في الغارات والمناجم",
    "it_meds": "حقيبة الإسعاف",
    "mk_lots": "العروض المفتوحة: {o} من {m} (🐎 {h} · 🛒 {c})",
    "badges": "🏅 أوسمة المواسم",
    "sk_stable": "🐎 الإسطبل",
    "sk_lots": "العروض في البورصة: {n}",
    "sk_buyHorse": "🐎 اشترِ حصانًا بـ {p} 🪙",
    "sk_stableHint": "كل حصان يمنحك +1 عرض في البورصة، وكل عربة +1 أخرى (لا يزيد عدد العربات على الخيول). العملات المدفوعة ثمنًا للحصان تُحرق.",
    "sk_horseBought": "🐎 صار الحصان في الإسطبل! زاد عدد عروضك في البورصة.",
    "sk_shuttleCharge": "🚀 شحن المكوك",
    "sk_shuttleUntil": "🔋 المكوك مشحون حتى {t}",
    "sk_shuttleEmpty": "🪫 المكوك فارغ الشحن — مزايا البورصة معطّلة.",
    "sk_chargeBtn": "🔋 اشحن: بطارية واحدة = {d} أيام",
    "raid_needTech": "الغارات تحتاج إلى 📡 الاتصالات و🔭 الاستطلاع و⚔️ الهجوم من المستوى 1.",
    "raid_toLab": "🔬 إلى المختبر",
    "raid_scoutInfo": "الاستطلاع يعرض الأهداف: {n}. وقود الغارة هو الهيدروجين 💧",
    "raid_medsOn": "💊 حقيبة الإسعاف حتى {t}: لا خوف من الأمراض",
    "raid_medsOff": "💊 بلا حقيبة إسعاف يضيع 15% من الغنيمة في المستوصف",
    "raid_note_sick": "🤒 بلا حقيبة إسعاف ضاع جزء من الغنيمة في المستوصف",
    "mn_mined": "استُخرج {n} {i}",
    "mn_left": "حتى نهاية الاستخراج: {t}",
    "mn_commNote": "يذهب الدخل إلى المقاتلين الذين لديهم 📡 اتصالات 1+؛ وبلا 💊 حقيبة إسعاف تضيع كل ساعة سابعة.",
    "top_season": "🏆 الموسم",
    "top_rich": "💰 الأثرياء",
    "top_seasonTitle": "🏆 الموسم {s}",
    "top_left": "حتى نهاية الموسم: {t}",
    "top_myPlace": "مركزك: {p} من {n} · ربحت {e} 🪙",
    "top_noPlace": "لست في الجدول بعد — العب وسيظهر مركزك.",
    "top_prizes": "يعلن المنظّم جوائز الموسم. يحصل أفضل 10 على شارة الموسم في الجواز.",
    "top_rules": "تُحسب العملات التي ربحتها في اللعبة خلال الشهر: المزرعة والانتصارات والمبارزات والمهمات والصندوق والمبيعات. الرصيد لا يُصفَّر.",
    "top_players": "👤 لاعبو الموسم",
    "top_teams": "🏆 فرق الموسم",
    "top_empty": "الموسم بدأ للتو — كن الأول!",
    "top_noTeams": "لم تُقم معارك في هذا الموسم بعد.",
    "top_teamRules": "نقاط المراكز في معارك الموسم: 10 · 7 · 5 · 4 · 3 · 2 · 1.",
    "lab_tools": "🧰 الأدوات",
    "lab_toolsHint": "الأطقم لا تُستهلك — فهي تفتح التجميعات المعقدة ومستويات التقنيات.",
    "lab_nextTool": "الطقم التالي: {t}",
    "lab_craftTool": "اصنع الطقم",
    "lab_toolsMax": "🧬 كل الأطقم جاهزة!",
    "lab_level": "المستوى {l} من {m}",
    "lab_max": "🏆 المستوى الأقصى",
    "lab_wait": "⏳ المستوى التالي بعد {t}",
    "lab_up": "ادرس المستوى {l}",
    "res_stone_src": "المهمات، المناجم، الصندوق",
    "res_wood_src": "المناجم، الصندوق",
    "res_fire_src": "نار المخيم في الورشة",
    "res_energy_src": "فرصة مع كل فوز، المناجم، الصندوق",
    "res_battery_src": "الورشة",
    "res_cow_src": "صندوق اليوم السابع، البورصة",
    "res_core_src": "المناجم وجوائز المنظّم",
    "sk_items": "🧪 العناصر في المخزن: {n} / {m} (10% من السعة)",
    "sk_cutletsName": "شرائح سايبر",
    "it_total": "في المخزن: {n} قطعة",
    "bt_entry": "🔋 طلب الفريق: {n} / {m}",
    "bt_entered": "✅ الفريق في معركة المناجم",
    "bt_give": "أضف 🔋 (لديك {n})",
    "bt_info": "يقاتل على المناجم فقط الفرق المقدِّمة للطلب: {f} 🔋، والعشيرة — {fc} 🔋. ساهموا معًا كفريق!",
    "bt_notAllowed": "هذه المعركة ليست لنوع فريقك",
    "mn_place": "🏆 جائزة المركز {p}",
    "mn_soonShort": "البداية: {d}",
    "top_events": "🎯 العروض",
    "ev_empty": "لا توجد عروض الآن — عد لاحقًا!",
    "ev_my": "مركزك: {p}",
    "ev_noPlace": "لست في الجدول بعد — هيا!",
    "ev_manual": "سيحدّد المنظّم الفائزين",
    "ev_places": "عدد المراكز الفائزة: {n}",
    "ev_prizes": "🎁 الجوائز",
    "ev_leaders": "المتصدّرون",
    "lab_sciGate": "📚 يُفتح المستوى {l} عندما تصل كل التقنيات إلى المستوى {l}",
    "lab_cooldown": "بعد الدراسة يأتي المستوى التالي بعد {d} يومًا.",
    "lab_done": "🔬 تم! المستوى {l}",
    "lab_eff_comm": "المستوى 1 — الغارات ودخل المناجم؛ وكل مستوى تالٍ يخفض إعادة شحن الغارة {c} دقيقة",
    "lab_eff_scout": "بدونه لا غارات؛ عدد الأهداف في الاستطلاع: 2 + المستوى",
    "lab_eff_attack": "بدونه لا غارات؛ كل مستوى بعد الأول يزيد الغنائم {a}%",
    "lab_eff_defense": "كل مستوى يقلل بنسبة {d}% ما يستطيع المغير أخذه منك",
    "lab_eff_science": "+{s}% لإنتاج المزرعة والغنائم عن كل مستوى. تُدرس طويلًا وتتطلب ☢️ نواة",
    "lab_how": "📖 كيف تعمل",
    "lab_rule1": "تُصنع الأطقم مرة واحدة: ⚒️ ← 🛠 ← 🔬 ← 🧬. بدون الطقم المناسب لا تُنفَّذ الوصفة المعقدة ولا يُدرس المستوى.",
    "lab_rule2": "بعد دراسة مستوى، يُفتح المستوى التالي من التقنية نفسها بعد 30 يومًا بالضبط — كل تحسين ثمين. العلم ينمو بعد بقية التقنيات.",
    "lab_rule3": "☢️ النواة تُستخرج بالفريق فقط: المراكز الأولى في المعارك وتحمّل المنجم يومًا كاملًا.",
    "durDH": "{d} ي {h} س",
    "durHM": "{h} س {m} د",
    "durM": "{m} د",
    "ws_locked": "🔒 ستُفتح بعد {t}",
    "ws_toStorage": "📦 القطعة الجاهزة تذهب إلى المخزون",
    "eff_camo": "لا تظهر في استطلاع الغارات، وبإمكانك الإغارة",
    "eff_trap": "المغير الفاشل يعطيك ضعف ما يُفترض",
    "eff_drill": "التعادل في الدفاع يُحتسب فشلًا للمغير",
    "eff_thermos": "الحفّارات تأكل الكفتة أبطأ بنسبة 25%",
    "eff_banner": "+5% تعدين لفريقك كله",
    "eff_dome": "ترس حماية من الغارات للفريق كله",
    "eff_forsage": "يلغي إعادة شحن الغارة (مرة في اليوم)",
    "eff_economizer": "الإقلاع التالي بلا هيدروجين",
    "eff_cargo": "غنائم الغارة التالية ×1.5",
    "eff_stamp": "البيع التالي في البورصة بلا عمولة",
    "it_camo": "التمويه",
    "it_trap": "الطُّعم",
    "it_drill": "مدرّب الدفاع",
    "it_thermos": "ثرموس الكفتة",
    "it_banner": "راية الفريق",
    "it_dome": "قبة الفريق",
    "it_forsage": "الدفع الإضافي",
    "it_economizer": "موفّر الوقود",
    "it_cargo": "عنبر الشحن الموسّع",
    "it_stamp": "ختم البورصة",
    "it_oneShot": "لمرة واحدة",
    "it_charges": "⚡ مشحون: {n}",
    "it_needTeam": "قطعة للفريق — يجب أن تكون في فريق.",
    "it_charged": "⚡ تم الشحن! ستعمل عند إجرائك التالي.",
    "it_forsaged": "🔥 أُلغيت إعادة الشحن — انطلق!",
    "raid_armed": "⚡ جاهز: {l}",
    "raid_guardUntil": "{n} حتى {t}",
    "raid_domeOn": "🛡 قبة الفريق حتى {t}",
    "raid_forsageBtn": "🔥 الدفع الإضافي: إلغاء إعادة الشحن ({n})",
    "raid_note_economizer": "⛽ موفّر الوقود: إقلاع بلا هيدروجين",
    "raid_note_cargo": "📦 العنبر: الغنائم ×1.5",
    "raid_note_trap": "🪤 طُعم الهدف: تعطيه ضعف ما يُفترض",
    "raid_note_drill": "🎯 مدرّب دفاع الهدف: التعادل يُحتسب فشلًا لك",
    "mn_title": "⛏ خريطة المناجم",
    "mn_closed": "🔒 لا غارات على المناجم قبل بدء معركة فرق أو عشائر.",
    "mn_pick": "اضغط على منجم لمعرفة التفاصيل.",
    "mn_info": "⛏ المنجم",
    "mn_battle": "⚔️ معركة «{t}» على المنجم رقم {n}",
    "mn_soon": "⏳ معركة «{t}» على المنجم رقم {n} — تبدأ {d}",
    "mn_nom": "الفئة: {n}",
    "mn_ends": "النهاية: {d}",
    "mn_leaders": "المتصدرون الآن",
    "mn_noLeaders": "لم يسجّل أحد نقاطًا بعد — فريقك قد يكون الأول!",
    "mn_myTeam": "🏆 فريقك في المناجم",
    "mn_income": "الإنتاج: {n} من الموارد في الساعة للفريق كله",
    "mn_noIncome": "لا مناجم بعد — فُز في معركة فرق ويصبح المنجم لك 72 ساعة.",
    "mn_noTeam": "المناجم تُؤخذ بالفرق فقط — انضم إلى فريق أو أنشئ فريقك.",
    "mn_teamBtn": "🏆 إلى الفريق",
    "mn_how": "📖 كيف تعمل",
    "mn_rule1": "كل معركة فرق وعشائر تدور على منجم واحد بالضبط. يفوز الفريق صاحب أفضل نتيجة إجمالية لكل مقاتليه في فئة المعركة.",
    "mn_rule2": "يحتفظ الفائز بالمنجم {h} ساعة: يحصل كل عضو في الفريق على {y} من مورد المنجم في الساعة. كلما زاد المقاتلون زاد الإنتاج.",
    "mn_rule3": "بعدها يتحرر المنجم، ولا يمكن الاستيلاء عليه إلا في معركة جديدة.",
    "mn_name": "⛏ المنجم رقم {n}",
    "mn_res": "المورد",
    "mn_holder": "المالك",
    "mn_free": "حر",
    "mn_untilL": "يملكه حتى",
    "mn_pumping": "الإنتاج: {n} {i} في الساعة",
    "mn_targetOf": "⚔️ تدور معركة «{t}» على هذا المنجم",
    "mn_closedOne": "🔒 لا يُؤخذ إلا في معركة فرق — تابع الإعلانات.",
    "raid_noFuel": "⛽ السفينة غير جاهزة للإقلاع — تحتاج إلى وقود",
    "raid_shieldTitle": "🛡 ترس الحماية من الغارات",
    "raid_shieldActive": "مفعّل",
    "raid_shieldInactive": "غير مفعّل",
    "raid_shieldHint": "ما دام الترس مفعّلًا لا أحد يغير عليك. يُجمَّع الترس في الورشة ويُحفظ في المخزون — فعّله عند الحاجة.",
    "raid_toStorage": "📦 افتح المخزون",
    "sk_res": "📦 الموارد في المخزون",
    "sk_expand": "🔧 وسّع المخزون",
    "sk_cutlets": "🥩 الكفتات السيبرانية",
    "sk_cutletsHint": "وقود الحفّارات السيبرانية: كفتة واحدة = يوم عمل.",
    "sk_refuel": "🚜 تزويد في المزرعة",
    "it_nitrogen": "التبريد النيتروجيني +40%",
    "it_nuclear": "التسريع النووي x5",
    "it_drone": "الدرون المايسترو",
    "it_shield": "ترس الحماية من الغارات",
    "it_unlimit": "إزالة حدود الفوز",
    "it_unlimitDesc": "انتصارات في الألعاب بلا حد يومي",
    "it_hours": "{h} س",
    "it_use": "فعّل",
    "it_empty": "فارغ. جمّع قطعة في الورشة — وستظهر هنا.",
    "it_toWorkshop": "🔧 إلى الورشة",
    "it_active": "✅ ساري حتى {t}",
    "it_used": "✅ تم التفعيل! ساري حتى {t}",
    "it_stored": "📦 جاهز! القطعة في المخزون — فعّلها من تبويب «المخزون» عند الحاجة.",
    "sk_shuttle": "🚀 المكوك",
    "sk_shuttleOn": "متوفر: عمولة البورصة {f}% وحدود الأوامر أوسع.",
    "sk_shuttleOff": "غير متوفر بعد. يُجمَّع في الورشة.",
    "sk_armor": "🦾 الدرع السيبراني",
    "sk_armorOn": "المستوى {l} من {m}: +{p}% للتعدين حتى {t}.",
    "sk_armorOff": "غير مرتدى. كل مستوى يمنح +{p}% للتعدين لمدة 30 يومًا.",
    "sk_store": "🏗 توسيع المخزون",
    "sk_storeLvl": "السعة: {c} من كل مورد.",
    "sk_storeMax": "🏆 أقصى مخزون!",
    "hp_who": "يمكن للّاعبين من مستوى الذكاء {l} ومع {c} من الكفتات اليومية الإهداء.",
    "top": "👑 أغنى 100 لاعب في المنظومة",
    "shop": "🏪 المتجر",
    "shopFarm": "🚜 للمزرعة",
    "shopGames": "🕹️ الألعاب",
    "shopHint": "الدفع عبر Telegram Stars الرسمية — هنا مباشرة وبلمسة واحدة.",
    "paid": "🎉 تم الدفع! السلعة على حسابك بالفعل.",
    "payFail": "لم تنجح عملية الدفع. حاول مجددًا.",
    "oldClient": "حدّث Telegram للشراء من التطبيق، أو افتح المتجر في دردشة البوت.",
    "ctaNoRobots": "💤 مزرعتك شبه فارغة! احصل على روبوت أقوى — وستتدفق 🪙 على مدار الساعة.",
    "ctaHungry": "🚨 الحفّارات جائعة ({n} بلا وقود) — التعدين متوقف!",
    "ctaLowFuel": "⚠️ الكفتات أقل مما يكفي ليوم واحد من عمل الحفّارات.",
    "ctaShopBtn": "🛒 إلى المتجر",
    "footer": "The whole game in one app",
    "noProfile": "لم يتم العثور على الملف. افتح البوت واضغط /start!",
    "blocked": "الحساب محظور من قِبل الإدارة.",
    "deleting": "حسابك في قائمة الحذف. غيّرت رأيك؟ ألغِ الحذف في دردشة البوت.",
    "error": "تعذّر تحميل البيانات. حاول لاحقًا.",
    "outside": "افتح هذا التطبيق من بوت Telegram الخاص بـROFL HUB.",
    "robotsTitle": "🤖 روبوتاتك",
    "buyMore": "🛒 شراء",
    "rateShort": "{v} 🪙/ساعة",
    "refuelOne": "🥩 زوّد 1",
    "refuelAll": "⚡ زوّد الكل",
    "refueled": "تم التزويد: {n} 🥩",
    "res_metal_src": "حجر-ورقة-مقص",
    "res_hydrogen_src": "أعلى/أقل",
    "res_crystal_src": "الكويز",
    "res_parts_src": "الخزنة السيبرانية",
    "resWhere": "أين تستخرجها",
    "ws_title": "🔧 الورشة",
    "ws_hint": "موارد الألعاب تتحول إلى تعزيزات. إن كفت الموارد — اضغط «اصنع».",
    "ws_craft": "اصنع",
    "ws_owned": "✅ لديك بالفعل",
    "ws_crafted": "تم! التعزيز يعمل الآن.",
    "ws_armor": "🛡 الدرع السيبراني",
    "ws_armorLvl": "المستوى {l}/{m} · +{p}% لكل مستوى لمدة 30 يومًا",
    "ws_shuttleOn": "🚀 المكوك مُجمَّع: عمولة البورصة {fee}%",
    "ws_shuttleOff": "🚀 المكوك غير مُجمَّع: عمولة البورصة {fee}%",
    "eff_nitrogen": "+40% لتعدين كل الروبوتات",
    "eff_nuclear": "×5 للتعدين، والحفّارات تأكل ×3 كفتة",
    "eff_drone": "الروبوتات لا تشيخ",
    "eff_shield": "لا يمكن لأحد الإغارة عليك",
    "eff_cutlet": "كفتة سيبرانية واحدة إلى المخزون (مكلفة: الوقود أوفر في المتجر)",
    "eff_armor": "+10% للتعدين لكل مستوى لمدة 30 يومًا",
    "eff_storage": "مساحة أكبر للموارد — إلى الأبد",
    "eff_shuttle": "لك وحدك: عمولة 5% على مبيعاتك وأوامر حتى 500 كفتة — إلى الأبد",
    "raid_title": "🏴‍☠️ الغارات",
    "raid_how": "📖 كيف تعمل",
    "raid_rule1": "تختار حركتك، وللهدف وضعية دفاع محددة مسبقًا. يحسم الأمرَ حجر-ورقة-مقص: إنها مبارزة قرارات لا يانصيب.",
    "raid_rule2": "الفوز: تأخذ {pct}% من كل مورد لدى الهدف، حتى {cap} لكل مورد. الفشل: تعطي الهدف {fpct}% من مواردك، حتى {fcap}. التعادل: احترق الوقود.",
    "raid_rule3": "لا يُنهب إلا الموارد. العملات والروبوتات والكفتة في أمان تام. المبتدئون محميون {days} أيام، ولا يمكن الإغارة على الزملاء.",
    "raid_rule4": "الطلعة تكلّف {fuel} 💧 هيدروجين، والتالية بعد {cd} ساعة. إن أغار عليك أحد، فالثأر مجاني خلال {rh} ساعة.",
    "raid_fuel": "💧 الهيدروجين",
    "raid_ready": "🚀 السفينة جاهزة للانطلاق",
    "raid_cooldown": "⏳ إعادة الشحن: {m} دقيقة",
    "raid_shieldOn": "🛡 الترس حتى {t}",
    "raid_shieldNewbie": "🛡 حماية المبتدئ",
    "raid_shieldOff": "🛡 لا ترس — اصنعه في الورشة",
    "raid_stance": "✊ وضعية دفاعك",
    "raid_stanceHint": "بها تواجه غارات الآخرين. غيّرها بين حين وآخر — من يسهل التنبؤ به يُنهَب أكثر.",
    "raid_stanceNone": "لم تُختر وضعية — ستكون عشوائية",
    "raid_stanceSaved": "تم حفظ الوضعية",
    "raid_stats": "الغارات: {a} (الناجحة {w}) · صُدّت: {h} من {d}",
    "raid_scout": "🔭 الاستطلاع: البحث عن أهداف",
    "raid_targets": "🎯 اختر هدفًا",
    "raid_res": "الموارد ≈{n}",
    "raid_noTargets": "لا أهداف مناسبة الآن: أتراس، فترات انتظار، مبتدئون. عُد لاحقًا.",
    "raid_pickMove": "✊ حركتك ضد وضعية {name}",
    "raid_revenge": "⚔️ الثأر",
    "raid_revengeBtn": "⚔️ رُدّ على: {name}",
    "raid_win": "🏴‍☠️ نجحت الغارة!",
    "raid_draw": "😐 تعادل — عادت السفينة فارغة",
    "raid_lose": "💥 صمد الدفاع",
    "raid_vs": "{m} ضد {s}",
    "raid_loot": "الغنائم: {l}",
    "raid_lost": "أُعطي للهدف: {l}",
    "rock": "🪨 حجر",
    "scissors": "✂️ مقص",
    "paper": "📄 ورقة",
    "mk_title": "📈 البورصة",
    "mk_stats": "الأوامر: {o} · الكفتة: {c} · أفضل سعر: {b} 🪙",
    "mk_feeLine": "تُحرق عمولة {f}% من كل بيع — درع ضد التضخم",
    "mk_inv": "🥩 في مخزونك: {n}",
    "mk_offers": "🛒 العروض",
    "mk_empty": "لا عروض بعد — كن أول من يعرض!",
    "mk_offer": "{q} 🥩 × {p} 🪙",
    "mk_buyHow": "كم تشتري؟",
    "mk_all": "الكل {q}",
    "mk_sellTitle": "💰 بيع الكفتة",
    "mk_qty": "كم كفتة",
    "mk_price": "سعر القطعة، 🪙",
    "mk_preview": "الصفقة {t} 🪙 · ستحصل على {g} 🪙 · يُحرق {f} 🪙",
    "mk_sell": "اعرض في البورصة",
    "mk_limits": "حتى {q} كفتة في الأمر، وحتى {o} أوامر مفتوحة",
    "mk_my": "📋 أوامري",
    "mk_cancel": "إلغاء",
    "mk_bought": "اشتريت {q} 🥩 مقابل {t} 🪙",
    "mk_listed": "تم عرض الأمر! سأراسلك عند البيع.",
    "mk_cancelledMsg": "أُلغي الأمر، وعادت الكفتة إلى المخزون",
    "as_cutlet": "الكفتة",
    "as_metal": "المعدن",
    "as_hydrogen": "الهيدروجين",
    "as_crystal": "البلّورات",
    "as_parts": "القطع",
    "mk_index": "📈 مؤشر البورصة",
    "mk_chart": "📊 السعر خلال 7 أيام",
    "mk_noTrades": "لا صفقات بعد — كن أول من يبدأ!",
    "mk_avg": "متوسط سعر الأسبوع: {p} 🪙 · المُباع: {v}",
    "mk_asks": "🛒 يبيعون",
    "mk_bids": "🙋 يشترون",
    "mk_noBids": "لا طلبات شراء بعد",
    "mk_sellTo": "بِع",
    "mk_sellHow": "كم تبيع؟",
    "mk_bidTitle": "🙋 طلب شراء",
    "mk_bidHint": "تُجمَّد العملات في الطلب حتى الصفقة. إذا ألغيت الطلب تعود العملات.",
    "mk_bid": "ضع طلب شراء",
    "mk_bidPreview": "سيُجمَّد {t} 🪙",
    "mk_have": "لديك: {n}",
    "mk_floor": "لا يقل سعر الكفتة عن {p} 🪙: الوقود من المتجر مقابل النجوم أوفر دائمًا",
    "mk_side_sell": "أبيع",
    "mk_side_buy": "أشتري",
    "mk_listedBid": "تم وضع طلب الشراء! العملات مجمّدة حتى الصفقة.",
    "mk_sold": "بيع {q}، وحصلت على {g} 🪙 بعد العمولة",
    "mk_shuttleNote": "🚀 مكوكك: عمولة {f}% على مبيعاتك",
    "sw_title": "🔄 مقايضة الموارد",
    "sw_hint": "أعطِ ما يزيد عن حاجتك — واحصل على ما تحتاجه. بلا عملات وبلا عمولة.",
    "sw_give": "أنت تعطي",
    "sw_want": "تريد الحصول على",
    "sw_qty": "الكمية",
    "sw_create": "اقترح مقايضة",
    "sw_take": "قايِض",
    "shop_info": "ℹ️ ماذا يمنح كل منتج",
    "sw_youGet": "تحصل على",
    "sw_youGive": "في المقابل تعطي",
    "sw_takeBtn": "قايِض — أعطِ {x}",
    "sw_mineLine": "أنت تعطي {g} ← تريد {w}",
    "sw_qtyErr": "أدخل كمية أكبر من صفر في الحقلين",
    "sw_empty": "لا عروض مقايضة بعد",
    "sw_mine": "عروضي",
    "sw_done": "تمت المقايضة!",
    "sw_created": "تم نشر العرض، والموارد محجوزة",
    "sw_cancelled": "سُحب العرض، وعادت الموارد",
    "ws_armorUntil": "🛡 الدرع فعّال حتى {t}",
    "st_title": "🛰 محطة الفريق",
    "st_level": "المستوى {l} من {m}",
    "st_bonus": "+{p}% للتعدين لكل مقاتل",
    "st_next": "المستوى {n} يحتاج {c} من كل مورد",
    "st_max": "🏁 اكتمل بناء المحطة!",
    "st_feed": "🧾 آخر المساهمات",
    "st_feedEmpty": "لم يساهم أحد بعد — كن أول المساهمين",
    "st_donate": "ساهم",
    "st_all": "الكل",
    "st_done": "تمت المساهمة!",
    "st_hint": "يبنيها الفريق كله، ويحصل كل واحد على المكافأة. من يغادر الفريق يفقد المكافأة.",
    "st_off": "المحطة تحت الصيانة مؤقتًا",
    "goals_title": "🎯 أهداف اليوم",
    "goals_chest": "🎁 صندوق الأهداف الثلاثة: +{c} 🪙 و+{r} من مورد عشوائي",
    "goals_streak": "🔥 السلسلة: {s} يوم · كل {e} أيام متتالية +{b} 🪙",
    "goals_claim": "🎁 استلم الصندوق",
    "goals_claimed": "🎁 استلمت صندوق اليوم. أهداف جديدة غدًا!",
    "goals_reset": "تتجدد الأهداف عند 00:00 UTC",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · السلسلة {s} يوم",
    "tab_friends": "🤝 الأصدقاء",
    "ref_title": "🤝 ادعُ أصدقاءك",
    "ref_rules": "{q} عن كل صديق نشط — مرة واحدة. الصديق النشط بلغ مستوى الذكاء {l} وجمع {c} كفتات يومية.",
    "ref_copy": "📋 نسخ",
    "ref_copied": "تم نسخ الرابط!",
    "ref_share": "📤 مشاركة",
    "ref_stats": "📊 شبكتك",
    "ref_invited": "مدعوّون",
    "ref_qualified": "نشطون",
    "ref_earned": "مكتسب",
    "ref_top": "🏆 من لديه أكثر الأصدقاء",
    "ref_topHint": "✅ — الأصدقاء النشطون، 👥 — كل المدعوّين",
    "ref_empty": "التصنيف فارغ حتى الآن — كن أول من يتصدّره!",
    "wk_title": "🔥 وصفات الأسبوع",
    "wk_hint": "وصفات مؤقتة: تظهر بقرار من المركز ثم تختفي. لا تفوّت فرصة تجميعها!",
    "wk_left": "التجميعات المتبقية هذا الأسبوع: {n} من {m}",
    "st_cap": "📦 المخزون: حتى {c} من كل مورد — فائض الغنيمة يضيع",
    "featureOff": "⚙️ هذا القسم تحت الصيانة",
    "done": "تم!",
    "loading": "⏳ جارٍ التحميل…",
}

COMMANDS = {
    "app": "🎮 فتح Mini App",
    "menu": "📱 القائمة الرئيسية",
    "profile": "👤 ملفي الشخصي وجوازي",
    "farm": "🚜 المزرعة السيبرانية والتزويد",
    "shop": "🏪 المتجر (Telegram Stars)",
    "games": "🕹️ كل الألعاب ضد البوت",
    "quiz": "🧠 الكويز: 15 ثانية للإجابة",
    "duel": "⚔️ مبارزة 1 ضد 1 على رهان",
    "quests": "🗺️ المهام: قصص بخيارات",
    "my_team": "🏆 فريقي وزملائي",
    "invite": "🤝 رابط الدعوة: +500 عن كل صديق نشط",
    "transfer": "🔄 تحويل عملات إلى لاعب",
    "market": "📈 بورصة الكفتة: شراء أو بيع",
    "sell": "💰 بيع الكفتة: /sell الكمية السعر",
    "my_stats": "📊 إحصاءاتي",
    "faq": "📚 الأسئلة الشائعة",
    "rules": "📜 اتفاقية الاستخدام",
    "paysupport": "🛟 دعم المدفوعات",
    "workshop": "🔧 الورشة: حوّل الموارد إلى تعزيزات",
    "raid": "🏴‍☠️ الغارات: استطلاع وثأر",
    "goals": "🎯 الأهداف اليومية والصندوق",
    "station": "🛰 محطة الفريق: مشروع مشترك",
}
