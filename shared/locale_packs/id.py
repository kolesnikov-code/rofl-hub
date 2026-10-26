"""Индонезийская локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> koin
# Младший Майнер -> Robot Penambang
# Кибер-Бурильщик -> Pengebor Siber
# кибер-котлета -> kotlet siber (кратко: kotlet)
# Холодильник -> Kulkas
# склад -> gudang
# ферма -> ladang (кибер-ферма -> Ladang Siber)
# Ядерный Разгон x5 -> Boost Nuklir x5
# Азотное Охлаждение +40% -> Pendingin Nitrogen +40%
# Мастер-дрон -> Drone Master
# Кибер-Сейф -> Brankas Siber
# Мега-Клан -> Mega-Klan
# Безлимит / снятие лимита -> Tanpa Batas / hapus batas
# дуэли -> duel
# битвы -> pertempuran (битвы команд -> Pertempuran Tim)
# квесты -> misi
# уровень интеллекта -> Level Kecerdasan
# команда -> tim, клан -> klan, банда -> geng, викторина -> Kuis
# ресурсы -> sumber daya: Металл -> Logam, Водород -> Hidrogen, Кристаллы -> Kristal, Детали -> Komponen
# Мастерская -> Bengkel, Кибер-броня -> Zirah Siber, Шаттл -> Shuttle
# Налёт -> Serbuan, Стойка обороны -> Kuda-kuda pertahanan, Разведка -> Pengintaian,
# Реванш -> Balas dendam, Щит -> Perisai
# Ежедневные цели -> Target harian, Сундук -> Peti, Серия -> Rentetan
# Станция команды -> Stasiun Tim

BUTTONS = {
    "main_menu": "📱 MENU UTAMA",
    "profile": "👤 PROFILKU",
    "farm": "🚜 LADANGKU",
    "games_zone": "🕹️ ZONA GAME",
    "teams": "🏆 TIM & KLAN",
    "shop": "🏪 TOKO",
    "shop_cat_farm": "🚜 UNTUK LADANG",
    "shop_cat_games": "🕹️ GAME",
}

STRINGS = {
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
    # ---------------- umum ----------------
    "common.no_profile": "⚠️ Profil tidak ditemukan. Tekan /start untuk mendaftar.",
    "common.btn_menu": "💿 Menu Utama",
    "common.blocked": "🚫 Akunmu diblokir oleh admin ROFL HUB.",
    "common.feature_off": "⚙️ Bagian ini sedang dalam perawatan. Coba lagi nanti ya!",
    "common.maintenance": "🛠 ROFL HUB sedang perawatan singkat. Segera kembali — koin dan progresmu aman!",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Selamat datang kembali, @{username}!</b>\nProgresmu aman. Panel navigasi ada di bagian bawah layar.",
    "start.btn_continue": "🛸 LANJUT",
    "start.btn_cutlet": "Apa itu kotlet siber?🥩🤔",
    "start.btn_fight": "Cepat ceritakan — lalu BERTARUNG!",
    "start.console": "🚀 <b>Konsol kendali aktif! Gunakan tombol di bagian bawah layar.</b>",
    "start.intro1": (
        "👋 <b>Hai! Aku ROFL HUB BOT — bot utama ekosistem game ROFL HUB. "
        "Hub hiburan dan pengetahuan generasi baru!</b>\n\n"
        "<b>Di sini kamu bisa:</b>\n"
        "🎮 Main game chat-bot melawan bot dan pemain lain\n"
        "💸 Dapatkan mata uang game dari kemenangan, atau bangun ladang yang menambang nonstop\n"
        "🤼 Buat tim dan serbu puncak papan peringkat\n"
        "🏆 Upgrade timmu jadi klan dan bertarung di peringkat internasional\n"
        "💰 Raih jackpot sejuta koin bersama gengmu\n"
        "👑 Beli publikasi di halaman utama media sosial atau situs kami untuk mempromosikan dirimu atau blogmu\n\n"
        "<b>Chat-bot ini bisa:</b>\n"
        "🎮 Menampilkan daftar semua game, kanal, dan situs ROFL HUB\n"
        "⚡ Memberikan koin untuk game, pertempuran tim dan klan, pencapaian, aktivitas, dan referal\n"
        "🔄 Mentransfer koin game ke pemain ROFL HUB lain\n"
        "💎 Menjual publikasi di situs dan slot VIP untuk tokoh dan bloger\n"
        "🚀 Menjual booster, gelar, status, dan banyak lagi...\n\n"
        "<i>Tekan “LANJUT”, dan aku ceritakan lebih banyak 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>INI HADIAH PERTAMAMU UNTUK PENDAFTARAN!</b>\n"
        "..................................................\n"
        "💸 Kamu menerima: <b>{balance} 🪙</b>\n"
        "🥩 Kamu menerima: <b>{cutlets} kotlet siber</b>\n"
        "..................................................\n"
        "Ini bonus awalmu karena bergabung dengan klub ROFL HUB.\n\n"
        "🔒 <i>Bonus hanya diberikan satu kali, saat pendaftaran.</i>\n\n"
        "Koin bisa dipakai dengan banyak cara — koin adalah tulang punggung ekonomi hub. Jaga baik-baik...\n\n"
        "⁉️ <b>Tapi kamu pasti punya pertanyaan:</b> kotlet apa ini? Siapa yang harus diberi makan?"
    ),
    "start.intro3": (
        "<b>PERTAMA, KENAPA KOIN GAME BEGITU PENTING?</b>\n\n"
        "Koin adalah dasar semua perdagangan, kompetisi, dan pembelian di <b>ROFL HUB</b>. "
        "Ini hampir satu-satunya mata uang game di dunia yang bisa ditambang gratis!\n"
        "..................................................\n"
        "<b>Ada banyak cara mendapatkannya:</b>\n"
        "- Undang teman lewat link referalmu\n"
        "- Menangkan game melawan bot\n"
        "- Menangkan duel melawan pemain lain\n"
        "- Ikut pertempuran tim dan klan\n"
        "- Klaim bonus login harian dan misi\n"
        "- Pelihara robot yang menambang koin 24/7 (Robot Penambang / Pengebor Siber)\n"
        "..................................................\n"
        "<b>Kalau kamu punya robot level dua (Pengebor Siber) — ia harus diberi makan setiap hari. "
        "Di sinilah kotlet siber berperan: bahan bakar untuk penambangan otomatis "
        "yang dibagikan gratis setiap hari! Tugasmu simpel — mampir dan beri makan robotmu.</b>\n\n"
        "Kalau lupa memberi makan — robot kehabisan daya dan penambangan berhenti.\n\n"
        "Robot Penambang (level satu) tidak butuh bahan bakar. "
        "Penting! Setiap robot dibeli untuk 30 hari — setelah itu beli lagi atau pelihara Drone Master. "
        "Nanti kamu paham sambil jalan:) Sekarang kita lanjut dulu.\n\n"
        "Sedikit lagi tentang <b>ROFL HUB</b>, biar kamu paham cara semuanya bekerja di sini.\n\n"
        "🛑 <b>Ini pesan terakhir perkenalan kita. Setelah ini — langsung bertarung:)</b>"
    ),
    "start.intro4": (
        "<b>VERSI SINGKATNYA. ROFL HUB ADALAH:</b>\n"
        "- Game chat-bot untuk semua selera\n"
        "- Kesempatan membuat tim sendiri (hingga 50 pemain)\n"
        "- Kesempatan meng-upgrade-nya jadi klan (hingga 1000 pemain)\n"
        "- Pertempuran tim dan klan berhadiah\n"
        "- Halaman Instagram — rofl_hub_global\n"
        "- Situs rofl-hub.com untuk ngobrol dan promosi tanpa registrasi\n"
        "- Ribuan pemain di seluruh dunia — teman barumu mungkin ada di antaranya!\n"
        "..................................................\n"
        "<b>Seperti janjiku, ini pesan penutup. Sekarang — bertarung! Perintah berguna:</b>\n\n"
        "/menu — kendali cepat semua fitur\n"
        "/games — daftar semua game\n"
        "/faq — pertanyaan yang sering diajukan\n"
        "/rules — perjanjian pengguna\n"
    ),

    # ---------------- menu & zona game ----------------
    "menu.text": (
        "📱 <b>MENU UTAMA EKOSISTEM ROFL HUB</b>\n"
        "..................................................\n"
        "👤 <b>PROFIL PRIBADI & PASPOR:</b>\n"
        "• /start — Mulai perkenalan dan daftarkan akun\n"
        "• /profile — Paspormu, saldo, dan tim secara real time\n"
        "• /my_stats — Statistik historismu selama 30 hari terakhir\n\n"
        "🚜 <b>LADANG SIBER & OTOMATISASI:</b>\n"
        "• /farm — Hub bahan bakar: pengisian dan kecepatan produksi robot\n"
        "• /shop — Marketplace: beli penambang, kotlet, dan upgrade hub\n\n"
        "🕹️ <b>RUANG GAME:</b>\n"
        "• /games — Hub inline semua game melawan bot\n"
        "• /quiz — Kuis kecepatan: 30 detik per jawaban, level dan bonus\n"
        "• /duel — DUEL 1-lawan-1 dengan pemain sungguhan: meja 10/100/1000\n"
        "• /quests — MISI: cerita detektif, komedi, dan teka-teki berhadiah\n"
        "• /rps, /high_low, /safe — Game cepat berhadiah koin\n\n"
        "👥 <b>MANAJEMEN GENG:</b>\n"
        "• /create_team — Daftarkan tim sendiri seharga 100.000 🪙\n"
        "• /my_team — Dasbor geng dan DAFTAR REKAN TIM dengan level 🧠\n"
        "• /all_teams — Rulet tim acak\n\n"
        "💸 <b>UANG & TEMAN:</b>\n"
        "• /invite — Link referalmu: +500 🪙 per teman aktif\n"
        "• /transfer — Kirim koin ke pemain lain\n\n"
        "📚 <b>PANDUAN & ATURAN:</b>\n"
        "• /faq — Panduan lengkap ekosistem (dibuka di Mini App)\n"
        "• /rules — Perjanjian pengguna\n"
        "..................................................\n"
        "<i>⚙️ Gunakan panel game dua kolom permanen di bagian bawah layar untuk navigasi instan antarbagian!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>SELAMAT DATANG DI ZONA GAME ROFL HUB!</b>\n"
        "..................................................\n"
        "Lawan bot dalam duel cepat atau ikuti tes sprint intelektual "
        "untuk menang besar — atau kehilangan semuanya!\n\n"
        "💸 Tiap kemenangan: <b>+2 🪙</b> (Brankas Siber: <b>+5</b>)\n"
        "💀 Kalah atau seri: dipotong <b>-1 🪙</b>\n"
        "🧠 Di Kuis ada timer 30 detik dan level kecerdasan: level 1 = 10 jawaban benar dan <b>+100 🪙</b>, "
        "setiap level berikutnya 10 jawaban lebih panjang — tapi hadiahnya naik 100!\n"
        "..................................................\n"
        "👇 <b>KETUK TOMBOL DI BAWAH UNTUK LANGSUNG MULAI RONDE:</b>"
    ),
    "menu.btn_quiz": "🧠 Kuis",
    "menu.btn_rps": "🪨 Suit",
    "menu.btn_hl": "📈 Besar/Kecil",
    "menu.btn_safe": "🔐 Brankas Siber",
    "menu.btn_duel": "⚔️ DUEL 1-lawan-1",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Paspor, ladang, tim, dan daftar pemain terkaya — dalam satu layar neon. "
        "Kotlet harian bisa diklaim langsung dari sana!\n\n"
        "👇 Ketuk tombolnya:"
    ),
    "app.btn": "🎮 BUKA MINI APP",
    "app.unavailable": "⚙️ Mini App masih dihubungkan ke server ekosistem. Cek lagi nanti ya!",
    "faq.teaser": (
        "📚 <b>PANDUAN EKOSISTEM ROFL HUB</b>\n"
        "..................................................\n"
        "Versi singkatnya:\n"
        "🚜 Robot menambang koin nonstop: Robot Penambang — 5/jam tanpa bahan bakar, "
        "Pengebor Siber — 10/jam, dan SETIAP Pengebor memakan 1 kotlet sibernya sendiri per hari. "
        "Semua robot bertahan 30 hari (Drone Master menghentikan sementara keausan).\n"
        "🧠 Kuis: 30 detik per jawaban, level kecerdasan dengan hadiah yang terus naik.\n"
        "⚔️ Duel melawan pemain sungguhan di meja 10/100/1000 🪙.\n"
        "🏆 Tim hingga 50 petarung (Mega-Klan — hingga 1000) dan event Pertempuran berhadiah untuk semua.\n"
        "..................................................\n"
        "👇 <b>Panduan lengkap dengan semua mekanik — satu ketukan saja:</b>"
    ),
    "faq.btn_open": "📖 BUKA PANDUAN LENGKAP",
    "rules.teaser": (
        "📜 <b>PERJANJIAN PENGGUNA ROFL HUB</b>\n"
        "..................................................\n"
        "Intinya:\n"
        "🪙 Koin dan semua item dalam game adalah elemen hiburan virtual: "
        "bukan uang dan tidak bisa ditukar dengan dana nyata.\n"
        "💫 Pembelian hanya lewat Telegram Stars resmi; barang digital dikirim "
        "instan, dan Stars dikembalikan otomatis jika pengiriman gagal.\n"
        "🛡️ Kami tidak mengumpulkan nomor telepon, lokasi, atau data pribadi.\n"
        "🤝 Dilarang menghina, memakai trik curang, dan multi-akun — pelanggaran bisa berujung blokir.\n"
        "..................................................\n"
        "👇 <b>Teks lengkap perjanjian dan disclaimer — satu ketukan saja:</b>\n"
        "<i>⚖️ Dengan menggunakan bot ini kamu menyatakan setuju dengan ketentuannya.</i>"
    ),
    "rules.btn_open": "📜 BUKA PERJANJIAN LENGKAP",
    "quest.list_header": (
        "🗺️ <b>MISI ROFL HUB</b>\n"
        "..................................................\n"
        "Cerita interaktif dengan pilihan dan percabangan: detektif, komedi, teka-teki. "
        "Kemenangan pertama di setiap misi memberi koin, dan kamu bisa mengulanginya sepuasnya!\n"
        "🌐 <i>Cerita misi masih berbahasa Rusia untuk saat ini — paket bahasa baru segera hadir.</i>\n\n"
        "👇 <b>Pilih cerita:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} mnt · 🏆 +{reward} 🪙 untuk kemenangan pertama\n"
        "..................................................\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Misi selesai, hadiah sudah diklaim. Ulangi kapan saja untuk seru-seruan!</i>",
    "quest.card_progress": "⏯ <i>Kamu punya permainan yang belum selesai.</i>",
    "quest.card_new": "🆕 <i>Kamu belum memainkan cerita ini.</i>",
    "quest.btn_start": "▶️ MULAI MISI",
    "quest.btn_restart": "🔄 MULAI DARI AWAL",
    "quest.btn_resume": "⏯ LANJUTKAN",
    "quest.btn_list": "🗺️ Ke daftar misi",
    "quest.btn_replay": "🔄 Main lagi",
    "quest.win_first": "\n\n🏆 <b>MISI SELESAI! Hadiah: +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>Selesai lagi!</b> Hadiah misi ini sudah pernah diklaim sebelumnya.",
    "quest.fail_footer": "\n\n💀 <i>Bukan akhir yang terbaik... tapi ceritanya selalu bisa diulang!</i>",
    "quest.stale": "⏳ Adegan itu sudah lewat — kita lanjut dari posisi sekarang!",
    "quest.no_coins": "❌ Petunjuk ini seharga {cost} 🪙, saldomu kurang. Mampir ke ladangmu!",
    "quest.not_found": "❌ Misi tidak ditemukan.",
    "menu.btn_quests": "🗺️ MISI",

    # ---------------- ladang ----------------
    "farm.btn_bonus": "🎁 KLAIM BONUS (kotlet tiap 24 jam)",
    "farm.btn_load1": "🥩 Isi 1 kotlet",
    "farm.btn_loadall": "⚡ Isi SEMUA",
    "farm.btn_shop": "🏪 Buka Toko",
    "farm.status_all_fueled": "🟢 Semua Pengebor Siber terisi bahan bakar dan sedang menambang koin!",
    "farm.status_partial": "🟡 {fueled} dari {total} Pengebor Siber sudah terisi. Sisanya menunggu kotlet di kulkas!",
    "farm.status_no_fuel": "🔴 Para Pengebor Siber berhenti! Bahan bakar di kulkas tidak cukup.",
    "farm.status_no_drills": "💡 Ambil robot yang lebih kuat di /shop — ladangmu akan menambang lebih banyak.",
    "farm.boost_nuclear": "🔋 Boost Nuklir x5 sampai {until} UTC (konsumsi kotlet ×3)",
    "farm.boost_nitrogen": "❄️ Pendingin Nitrogen +40% sampai {until} UTC",
    "farm.boost_drone": "🛸 Drone Master memperpanjang umur robot sampai {until} UTC",
    "farm.no_boosts": "Tidak ada boost aktif — cek /shop.",
    "farm.burnout": "🔥 Robot berikutnya hangus pada: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Aktifkan Robot Magang-mu (gratis)",
    "farm.intern_activated": "🤖 Robot Magang-mu mulai bekerja! +1 🪙 per jam selamanya — tanpa bahan bakar, tanpa kedaluwarsa.",
    "farm.intern_already": "🤖 Robot Magang-mu sudah bekerja.",
    "farm.btn_claim_intern": "🎁 Ambil Robot Magang ({n})",
    "farm.intern_pending": "🎁 Robot Magang dari level intelektualmu menunggu: <b>{n}</b> — ambil dengan tombol di bawah!",
    "farm.intern_claimed_new": "🤖 Robot Magang baru mulai bekerja! +1 🪙 per jam selamanya.",
    "farm.intern_none": "🤖 Belum ada Robot Magang baru — robot berikutnya menunggumu di level intelektual 10, 20, 30…",
    "games.intern_ready": "🎁 Level baru memberimu <b>Robot Magang</b> — ambil di farm-mu!",
    "farm.intern_line": "• Robot Magang ({rate} 🪙/jam, abadi): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 Kamu punya Robot Magang gratis! Tekan tombol di bawah — dia akan menambang 1 🪙 per jam selamanya.",
    "farm.dashboard": (
        "🚜 <b>HUB BAHAN BAKAR PUSAT ROFL HUB</b>\n"
        "..................................................\n"
        "🤖 Robot aktif di pabrik: <b>{total}</b>\n"
        "{intern}"
        "• Robot Penambang ({junior_rate} 🪙/jam): <code>{junior}</code>\n"
        "• Pengebor Siber ({premium_rate} 🪙/jam): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>KECEPATAN LADANGMU SAAT INI:</b>\n"
        "• Produksi per jam: <b>+{speed_hour} 🪙</b>\n"
        "• Produksi per hari: <b>+{speed_day} 🪙</b>\n\n"
        "⚡ <b>BOOST:</b>\n{boosts}\n\n"
        "📋 <b>STATUS PABRIK GAME:</b>\n"
        "{status}\n"
        "..................................................\n"
        "📦 <b>STATUS KULKAS OTOMATIS:</b>\n"
        "🥩 Stok bahan bakar: <b>{fridge} / {capacity}</b>\n"
        "💼 Kotlet di gudang: <code>{inv}</code>\n"
        "..................................................\n"
        "<i>💿 Penting: robot bertahan 30 hari (Drone Master menghentikan sementara keausan). "
        "SETIAP Pengebor Siber memakan SATU kotlet utuhnya sendiri dari kulkas per "
        "24 jam kerja: 3 robot — 3 kotlet sehari. Awasi bahan bakarnya!</i>"
    ),
    "farm.bonus_ok": "🎁 Kotlet siber masuk ke gudang! Kembali lagi setelah 24 jam.",
    "farm.bonus_wait": "⏳ Bonus sudah diklaim! Kotlet berikutnya dalam {hours} jam {minutes} menit.",
    "farm.no_inv_cutlets": "❌ Tidak ada kotlet siber di gudangmu! Beli di /shop",
    "farm.fridge_full": "📦 Kulkasmu sudah penuh!",

    # ---------------- profil ----------------
    "profile.caption": (
        "📋 <b>DASBOR PEMAIN ROFL HUB</b>\n"
        "..................................................\n"
        "🆔 ID Paspormu: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Koin saat ini: <b>{balance} 🪙</b>\n"
        "🏆 Statusmu: <b>{team}</b>\n"
        "🧠 Level kecerdasan: <b>{level}</b> · menuju level {next_level}: "
        "<b>{left}</b> jawaban benar di /quiz (hadiah: +{reward} 🪙)\n"
        "..................................................\n"
        "<i>Ini yang kamu miliki saat ini. Gunakan tombol untuk melompat ke bagian lain!</i>"
    ),
    "profile.no_team": "Tanpa tim",
    "profile.team_label": "Tim",
    "profile.clan_label": "Klan",
    "profile.btn_farm": "🚜 Ladang Siberku",
    "profile.btn_shop": "🏪 Toko",
    "profile.stats": (
        "📊 <b>STATISTIK PENCAPAIAN GAME (30 HARI)</b>\n"
        "..................................................\n"
        "🧠 Level kecerdasan game: <b>{level}</b> (total jawaban benar: {total})\n"
        "🎮 Ronde duel dimainkan: <b>{played}</b>\n"
        "🏆 Kemenangan diraih: <code>{won}</code>\n"
        "👥 Teman aktif yang diundang: <b>{refs}</b>\n"
        "..................................................\n"
        "<i>Statistik menyimpan rekam jejak dan pencapaian historismu, bahkan jika koin yang kamu menangkan sudah dibelanjakan di market!</i>"
    ),
    "img.passport": "ID PASPOR: {user_id}",
    "img.owner": "PEMIMPIN: @{username}",
    "img.balance": "Saldo: {balance} koin",
    "img.fridge": "Di kulkas: {fridge} / {capacity}",
    "img.inv": "Kotlet di gudang: {inv}",
    "img.junior": "Robot Penambang: {count}",
    "img.premium": "Pengebor Siber: {count}",

    # ---------------- game: mesin umum ----------------
    "games.win": "🎉 <b>MENANG!</b> 🎉\nDidapat: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>KALAH!</b>\nDipotong: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>SERI!</b>\nDipotong: <b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>Batas harian tercapai!</b>\n\n"
        "Kamu sudah meraih {limit} kemenangan di {game} hari ini. Batas di-reset pada 00:00 UTC.\n\n"
        "⚡ Hapus batas selama 24 jam — 15 ★, selama 30 hari — 249 ★ (bagian “Game” di /shop)."
    ),
    "games.no_coins": "❌ Koinmu 0 — tidak ada yang bisa dipakai membayar biaya ronde. Ambil penghasilan ladangmu di /farm!",
    "games.balance": "💰 Saldo: <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 Main lagi!",
    "games.btn_hub": "🕹️ Zona game",
    "games.level_up": (
        "🏅 <b>LEVEL KECERDASAN NAIK: {level}!</b> Hadiah: <b>+{bonus} 🪙</b>!\n"
        "Level berikutnya: {next_required} jawaban benar → +{next_reward} 🪙."
    ),
    "games.name.rps": "Batu-Gunting-Kertas",
    "games.intern_bonus": "🤖 Level {level}! Satu Robot Magang lagi datang ke farm-mu — sekarang ada {count}.",
    "games.name.hl": "Besar/Kecil",
    "games.name.quiz": "Kuis",
    "games.name.safe": "Brankas",
    "games.name.math": "Math",  # TODO(перевод 26.10)
    "games.name.flags": "Flags and capitals",  # TODO(перевод 26.10)
    "games.name.code": "Code breaker",  # TODO(перевод 26.10)
    "games.name.memory": "Memory",  # TODO(перевод 26.10)

    # ---------------- suit (BGK) ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>BATU-GUNTING-KERTAS</b>\n\n"
        "Menang: <b>+{reward}</b> · Kalah/seri: <b>-{penalty}</b>\n"
        "Batas kemenangan harian: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Batu",
    "rps.scissors": "✂️ Gunting",
    "rps.paper": "🧻 Kertas",
    "rps.draw": "🤝 <b>Seri!</b> Kamu dan bot sama-sama memilih {bot}.",
    "rps.win": "🏆 <b>Menang!</b> {user} mengalahkan {bot}.",
    "rps.lose": "💀 <b>Bot menang.</b> {bot} mengalahkan {user}.",

    # ---------------- Besar/Kecil ----------------
    "hl.intro": (
        "🎲 <b>BESAR ATAU KECIL</b>\n\nBot memasang angka: <b>{base}</b>.\n"
        "Apakah angka tersembunyinya lebih besar atau lebih kecil?\n"
        "Menang: <b>+{reward}</b> · Kalah: <b>-{penalty}</b> · Batas: <b>{limit}</b> kemenangan"
    ),
    "hl.btn_up": "📈 Lebih besar",
    "hl.btn_down": "📉 Lebih kecil",
    "hl.result": "🎲 <b>HASIL RONDE</b>\n\nAngka bot: <b>{base}</b> · Tersembunyi: <b>{secret}</b>",

    # ---------------- kuis ----------------
    "quiz.round": (
        "🧠 <b>KUIS • {category}</b>\n"
        "🤔 PERTANYAAN: <b>{question}</b>\n\n"
        "<i>🌐 Pertanyaan masih berbahasa Rusia untuk saat ini — paket bahasa baru segera hadir!</i>"
    ),
    "quiz.btn_new": "🧠 Pertanyaan baru",
    "quiz.timeout": "⌛ <b>WAKTU HABIS!</b> ⌛\nJawaban yang benar: <b>{correct}</b>",
    "quiz.stale": "⏳ Pertanyaan ini sudah tidak aktif. Mulai yang baru!",
    "quiz.stale_alert": "Pertanyaan ini sudah tidak aktif. Mulai yang baru!",
    "quiz.empty": "⚠️ Bank soal kosong. Beri tahu admin.",
    "quiz.wrong": "❌ <b>Salah</b> ❌\nJawaban yang benar: <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} 🪙</b> karena kalah!",
    "quiz.level_line": (
        "🧠 Level kecerdasan: <b>{level}</b>\n"
        "Kemenangan tersisa menuju level {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} detik per jawaban!\n"
        "Benar: +{win} 🪙 ke saldomu\n"
        "Salah / kehabisan waktu: -{penalty} 🪙\n"
        "Batas: {limit} kemenangan per hari</i>"
    ),



    # ---------------- Brankas ----------------
    "safe.intro": (
        "🔐 <b>BRANKAS SIBER</b>\n\n"
        "Di dalamnya — jackpot <b>{jackpot} 🪙</b>! Pintunya terkunci dengan kode dari 1 sampai {codes}. "
        "Kamu punya satu percobaan.\n"
        "Dibobol: <b>+{jackpot}</b> · Alarm: <b>-{penalty}</b> · Batas: <b>{limit}</b> kemenangan"
    ),
    "safe.btn_retry": "🔐 Bobol lagi!",
    "safe.win": "🔓 <b>Brankas terbuka!</b> Kodenya: <b>{code}</b>.",
    "safe.lose": "🚨 <b>Alarm berbunyi!</b> Kamu menebak {guess}, padahal kodenya: <b>{code}</b>.",

    # ---------------- duel ----------------
    "duel.intro": (
        "⚔️ <b>DUEL 1-LAWAN-1: BATU-GUNTING-KERTAS DENGAN TARUHAN</b>\n"
        "..................................................\n"
        "Pilih meja sesuai kantongmu — seperti di poker. Taruhan langsung dipotong, "
        "dan lawanmu adalah pemain ROFL HUB sungguhan!\n\n"
        "💰 Pot = kedua taruhan. Pemenang mengambil <b>{payout_percent}%</b> pot, "
        "<b>{burn_percent}%</b> terbakar selamanya (deflasi!).\n"
        "🤝 Seri berarti gestur langsung diulang — pot tetap di meja.\n"
        "⏱ Waktu per gestur — <b>{move_timeout} detik</b>; kalau diam saja, gesturmu dipilihkan generator acak.\n"
        "🏆 Kemenangan duel dihitung untuk timmu di Pertempuran!\n\n"
        "👇 <b>PILIH MEJA:</b>"
    ),
    "duel.btn_table": "⚔️ Meja {stake} 🪙",
    "duel.btn_cancel": "❌ Tinggalkan meja (taruhan kembali)",
    "duel.btn_move_rock": "🪨 Batu",
    "duel.btn_move_scissors": "✂️ Gunting",
    "duel.btn_move_paper": "🧻 Kertas",
    "duel.waiting": (
        "🪑 <b>Kamu di meja {stake} 🪙.</b> Taruhanmu sudah masuk pot.\n"
        "Menunggu petarung kedua... Begitu dia duduk, kalian berdua akan diminta memilih gestur!\n"
        "<i>Antrean berlaku {ttl} menit, setelah itu taruhanmu otomatis kembali.</i>"
    ),
    "duel.cancelled": "🚪 Kamu meninggalkan meja. Taruhan <b>{stake} 🪙</b> kembali ke saldomu.",
    "duel.expired": "⌛ Tidak ada lawan yang muncul di meja {stake}. Taruhan <b>{stake} 🪙</b> sudah dikembalikan.",
    "duel.matched": (
        "⚔️ <b>LAWAN DITEMUKAN! Meja {stake} 🪙.</b>\n"
        "Pot: <b>{bank} 🪙</b> · Untuk pemenang: <b>{payout}</b>\n\n"
        "⏱ Kamu punya <b>{timeout} detik</b> untuk memilih gestur!"
    ),
    "duel.move_saved": "✊ Gestur terkunci! Menunggu gestur lawan...",
    "duel.draw_replay": (
        "🤝 <b>SERI! Ronde {round}.</b> Kalian menunjukkan gestur yang sama.\n"
        "Pot tetap di meja. ⏱ {timeout} detik lagi — pilih gesturmu:"
    ),
    "duel.win": (
        "🏆 <b>DUEL INI MILIKMU!</b>\n\n"
        "Gesturmu {winner_move} mengalahkan {loser_move}.\n"
        "💰 Kemenangan: <b>+{payout} 🪙</b> · 🔥 Terbakar dari pot: {burned}\n"
        "💼 Saldo: <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>DUEL KALAH.</b>\n\n"
        "{winner_move} lawan mengalahkan {loser_move} milikmu.\n"
        "📉 Taruhan <b>{stake} 🪙</b> masuk ke pot pemenang.\n"
        "Rematch?"
    ),
    "duel.reaper_prefix": "⏰ <b>Ronde kehabisan waktu!</b> Gestur yang belum dipilih ditentukan oleh generator acak.\n\n",
    "duel.bad_table": "❌ Meja seperti itu tidak ada.",
    "duel.already_in": "⚠️ Kamu sudah di meja atau sedang bertarung! Selesaikan dulu duel yang sedang berjalan.",
    "duel.no_coins": "❌ Kamu butuh {stake} 🪙 di saldo untuk meja ini.",
    "duel.cancel_impossible": "⚠️ Antrean ini sudah tidak bisa dibatalkan (lawan sudah ditemukan atau meja ditutup).",
    "duel.not_active": "⌛ Duel ini sudah berakhir.",
    "duel.not_participant": "🔒 Ini bukan duelmu!",
    "duel.move_already": "✋ Kamu sudah menunjukkan gestur di ronde ini. Menunggu lawan!",
    "duel.bad_move": "❌ Gestur tidak dikenal.",
    "duel.btn_rematch": "⚔️ Rematch (ke meja)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 Pangkat: <b>{rank}</b>\n",
    "rank.rookie": "Pemula",
    "rank.fighter": "Petarung",
    "rank.legend": "Legenda",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.king": "KING",

    # ---------------- referal ----------------
    "ref.text": (
        "🤝 <b>PROGRAM REFERAL ROFL HUB</b>\n"
        "..................................................\n"
        "Undang teman lewat link pribadimu dan dapatkan <b>{bonus}</b> "
        "untuk setiap orang yang menjadi pemain aktif!\n\n"
        "🔗 <b>Link-mu (ketuk untuk menyalin):</b>\n<code>{link}</code>\n\n"
        "📊 <b>STATISTIKMU:</b>\n"
        "👥 Teman yang diundang: <b>{invited}</b>\n"
        "💰 Penghasilan dari referal: <b>{earned} 🪙</b>\n"
        "..................................................\n"
        "<i>Sebarkan link ke teman sekelas, sahabat, dan media sosial — makin besar gengmu, makin cepat saldomu tumbuh!</i>"
    ),
    "ref.btn_share": "📣 Bagikan link",
    "ref.share_text": "Gabung ke ekosistem game ROFL HUB!",
    "ref.qualified_line": ("✅ <b>Teman aktif</b> adalah teman yang mencapai <b>level intelektual {level}</b> di kuis "
                           "dan mengambil <b>{claims} kotlet harian</b> di peternakan. Setelah itu kamu dapat <b>{bonus}</b>, "
                           "satu kali untuk setiap teman. Daftar tanpa bermain tidak dapat bonus — lebih adil untuk semua."),
    "ref.qualified_notify": ("🤝 <b>Temanmu menjadi pemain aktif!</b>\n"
                             "Level intelektual {level} dan {claims} kotlet harian — tercapai. Kamu dapat <b>{bonus}</b>. Undang lagi!"),

    # ---------------- kesalahan tim ----------------
    "team.err_len": "❌ Panjang teks harus 1 sampai {max} karakter!",
    "team.err_link": "🚨 Pemeriksaan keamanan! Tautan, username, dan nomor telepon dilarang keras!",
    "team.err_badword": "❌ Terdeteksi kata kasar! Patuhi aturan hub.",
    "team.err_already": "⚠️ Kamu sudah berada di tim atau klan! Keluar dulu.",
    "team.err_money": "❌ Koin tidak cukup! Membuat tim butuh {cost} 🪙, kamu punya {balance} 🪙.",
    "team.err_captain": "⚠️ Kamu sudah menjadi kapten tim lain!",
    "team.err_taken": "⚠️ Nama «{name}» sudah dipakai! Cari nama yang unik.",
    "team.err_gone": "❌ Tim ini sudah tidak ada.",
    "team.err_full": "📦 Tim ini sudah penuh!",
    "team.err_not_member": "❌ Kamu tidak berada di tim.",
    "mk.err_no_team": "🏆 Bursa tim khusus anggota tim. Gabung ke tim atau buat timmu sendiri.",
    "mk.err_team_only": "🔒 Lot ini hanya untuk anggota tim penjual.",
    "help.err_qty": "Kamu bisa meminta 1 sampai {max} unit sumber daya.",
    "help.err_open": "Kamu masih punya permintaan terbuka — tunggu bantuan atau batalkan dulu.",
    "help.err_not_found": "Permintaan ini sudah ditutup.",
    "help.err_self": "Permintaan sendiri tidak bisa dipenuhi dengan hadiah 🙂",
    "help.err_limit": "Hari ini kamu sudah memberi {max} sumber daya — batas direset pukul 00:00 UTC.",
    "help.err_not_active": "🔒 Kamu bisa memberi sumber daya mulai Level Kecerdasan {level} dan setelah mengambil {claims} kotlet harian.",
    "it.err_none": "Barang ini sudah tidak ada di gudang.",
    "it.err_no_cooldown": "🚀 Tidak ada pengisian ulang — kapal sudah siap terbang.",
    "it.err_forsage_daily": "🔥 Afterburner sudah dipakai — berikutnya {hours} jam lagi.",
    "res.stone": "Batu",
    "res.wood": "Kayu",
    "res.fire": "Api",
    "res.energy": "Listrik",
    "res.battery": "Baterai",
    "res.cow": "Sapi",
    "res.core": "Inti",
    "tech.comm": "Komunikasi",
    "tech.scout": "Pengintaian",
    "tech.attack": "Serangan",
    "tech.defense": "Pertahanan",
    "tech.science": "Sains",
    "tech.err_max": "🏆 Ini sudah level maksimum.",
    "tech.err_unknown": "❌ Teknologi itu tidak ada.",
    "tech.err_tool": "🧰 Butuh set perkakas level {tool} — rakit di Laboratorium.",
    "tech.err_cooldown": "⏳ Level berikutnya bisa dipelajari dalam {hours} jam.",
    "tech.err_science": "📚 Sains level {level} terbuka saat semua teknologi lain sudah di level {level}.",
    "ws.err_items_full": "📦 Gudang barang penuh: maksimal {max} barang. Aktifkan salah satu atau perluas gudang.",
    "post.scope_team": "Peringkat tim",
    "post.scope_clan": "Peringkat klan",
    "post.scope_teams": "Tim dan klan",
    "post.scope_solo": "Peringkat pribadi",
    "nom.farm_mined": "menambang koin terbanyak lewat tambang",
    "nom.coins_earned": "mendapat koin terbanyak",
    "nom.duel_wins": "menang duel terbanyak",
    "nom.duels_played": "memainkan duel terbanyak",
    "nom.quiz_wins": "menjawab kuis dengan benar terbanyak",
    "nom.rps_wins": "menang batu-gunting-kertas terbanyak",
    "nom.safe_wins": "membobol Brankas Siber terbanyak",
    "nom.game_wins_total": "menang game melawan bot terbanyak",
    "nom.referrals": "mengajak teman aktif terbanyak",
    "nom.stars_spent": "mendukung ekosistem paling banyak (Stars)",
    "nom.insta_reels": "reels Instagram siapa yang paling meledak",
    "nom.youtube_shorts": "video YouTube Shorts siapa yang paling meledak",
    "nom.tiktok": "video TikTok siapa yang paling meledak",
    "bt.err_closed": "⏳ Pertempuran ini sudah ditutup.",
    "bt.err_no_entry": "Pertempuran ini tidak perlu pendaftaran.",
    "bt.err_no_team": "🏆 Bergabunglah dengan tim dulu.",
    "bt.err_scope": "Pertempuran ini bukan untuk jenis timmu.",
    "bt.err_full": "✅ Pendaftaran timmu sudah penuh.",
    "bt.err_battery": "🔋 Tidak ada baterai — rakit di bengkel.",
    "horse.err_max": "🐎 Kandang sudah berisi {max} kuda — tidak muat lagi.",
    "horse.err_coins": "🪙 Seekor kuda harganya {price} 🪙 — koinmu belum cukup.",
    "shuttle.err_none": "🚀 Rakit Shuttle di bengkel dulu.",
    "cart.err_horse": "🛒 Gerobak butuh kuda: jumlah gerobak tidak boleh melebihi jumlah kuda (dan maksimal {max}).",
    "raid.err_need_tech": "🔬 Serbuan butuh teknologi «{tech}» level 1 — pelajari di Laboratorium.",
    "raid.err_battery": "🔋 Pengintaian butuh baterai — rakit di bengkel.",
    "games.energy_gain": "⚡ Beruntung: +1 Listrik!",
    "ws.recipe_bonfire": "Api unggun: api dari kayu dan batu",
    "ws.recipe_battery": "Baterai (×2)",
    "ws.recipe_cart": "Gerobak",
    "ws.recipe_meds_72h": "Kotak P3K selama 72 jam",

    # ---------------- penghapusan akun ----------------
    "profile.btn_delete": "🗑 Hapus akun",
    "acct.warn": (
        "⚠️ <b>PENGHAPUSAN AKUN</b>\n"
        "..................................................\n"
        "Bersama akun ini, hal berikut akan <b>hilang permanen</b>:\n"
        "• koin, kotlet siber, sumber daya, dan semua robot ladang;\n"
        "• boost, Tanpa Batas, dan semua yang dibeli dengan Stars — <b>Stars tidak dikembalikan</b>;\n"
        "• VIP ID, progres kuis dan quest;\n"
        "• tempatmu di tim (kapten diteruskan ke veteran tim).\n"
        "Order terbuka di bursa langsung dibatalkan, barangnya kembali ke gudang.\n\n"
        "⏳ Awalnya akun dibekukan selama <b>{days} hari</b> — dalam masa itu kamu bisa berubah pikiran dengan satu ketukan. "
        "Setelah itu penghapusan tidak bisa dibatalkan. Kalau kembali nanti, kamu mulai dari nol: bonus awal tidak diberikan dua kali.\n\n"
        "<i>Tombol hapus aktif dalam {seconds} detik — baca baik-baik.</i>"
    ),
    "acct.btn_keep": "✅ Tidak, pertahankan akunku",
    "acct.btn_confirm": "🗑 Ya, hapus akunku",
    "acct.wait": "⏳ Tunggu {seconds} dtk lagi — baca apa saja yang akan dihapus.",
    "acct.kept": "👍 Bagus, akunmu tetap bersamamu!",
    "acct.scheduled": (
        "🗑 Akunmu dibekukan dan akan dihapus pada <b>{date}</b> (UTC).\n"
        "Order di bursa dibatalkan, barangnya sudah kembali ke gudang.\n\n"
        "Berubah pikiran? Ketuk tombol di bawah, semuanya kembali seperti semula."
    ),
    "acct.pending_notice": (
        "⏳ Akunmu dibekukan dan akan dihapus pada <b>{date}</b> (UTC).\n"
        "Ingin tetap bermain? Ketuk tombol di bawah."
    ),
    "acct.btn_undo": "↩️ Batalkan penghapusan",
    "acct.undone": "🎉 Penghapusan dibatalkan — akunmu kembali milikmu!",
    "acct.purged": "🗑 Akun ROFL HUB-mu telah dihapus. Terima kasih sudah bermain! Ingin kembali? Ketuk /start.",
    "acct.deleted_notice": "Akun sudah dihapus. Ketuk /start untuk memulai dari awal.",
    "acct.welcome_back": (
        "👋 <b>Selamat datang kembali!</b>\n"
        "Profilmu dibuat ulang dari nol. Bonus awal hanya diberikan sekali, jadi saldomu 0 🪙. "
        "Ladang, game, dan kuis menunggumu!"
    ),
    "tr.err_not_active": (
        "🔒 Kamu bisa mengirim koin setelah mencapai level intelektual {level} dan mengambil {claims} kotlet harian — "
        "ini melindungi ekosistem dari akun palsu."
    ),

    # ---------------- transfer ----------------
    "tr.help": (
        "🔄 <b>KIRIM KOIN KE PEMAIN LAIN</b>\n"
        "..................................................\n"
        "Format perintah:\n"
        "<code>/transfer ID jumlah</code> — lewat ID Paspor (lihat /profile)\n"
        "<code>/transfer @username jumlah</code> — lewat username\n"
        "<code>/transfer ROFL-HUB-777 jumlah</code> — lewat VIP ID dari lelang\n\n"
        "Contoh:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Jumlah minimum: <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ Penerima tidak ditemukan. Periksa ID Paspor atau @username — pemainnya harus sudah terdaftar di bot.",
    "tr.self": "🤨 Mengirim koin ke diri sendiri tidak bisa — itu sih mesin ekonomi abadi namanya!",
    "tr.blocked": "🚫 Pemain ini diblokir — transfer ke dia tidak tersedia.",
    "tr.min": "❌ Jumlah transfer minimum adalah {min} 🪙.",
    "tr.insufficient": "❌ Koin tidak cukup! Saldomu: <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ Koin di saldomu tidak cukup.",
    "tr.confirm": (
        "🔄 <b>KONFIRMASI TRANSFER:</b>\n\n"
        "👤 Penerima: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Jumlah yang dipotong: <b>{amount} 🪙</b>{fee_line}\n"
        "💰 Penerima mendapat: <b>{received} 🪙</b>\n\n"
        "<i>Transfer tidak bisa dibatalkan — periksa lagi penerimanya!</i>"
    ),
    "tr.fee_line": "\n🔥 Biaya hub: <b>{fee} 🪙</b> (terbakar)",
    "tr.btn_confirm": "✅ KONFIRMASI TRANSFER",
    "tr.btn_cancel": "❌ Batal",
    "tr.cancelled_toast": "Transfer dibatalkan",
    "tr.cancelled": "❌ <b>Transfer dibatalkan.</b> Koinmu tetap aman.",
    "tr.not_yours": "🔒 Ini bukan transfermu!",
    "tr.done_toast": "✅ Transfer berhasil!",
    "tr.done": (
        "✅ <b>TRANSFER BERHASIL!</b>\n\n"
        "💸 Terkirim: <b>{amount} 🪙</b> ke pemain ID <code>{recipient_id}</code>\n"
        "💰 Saldomu: <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>Kamu menerima {amount} 🪙!</b>\n"
        "Pengirim: ID <code>{sender_id}</code>. Saldomu sudah bertambah — cek /profile!"
    ),

    # ---------------- toko & pembayaran ----------------
    "shop.header": "🏪 <b>TOKO ROFL HUB</b>\nPembelian lewat Telegram Stars resmi. Pilih kategori dengan tombol di bawah.",
    "shop.cat_farm": (
        "🚜 <b>TOKO · UNTUK LADANG</b>\n"
        "..................................................\n"
        "Robot untuk 30 hari, bahan bakar, kulkas, boost, dan Drone Master.\n"
        "📦 Kulkasmu saat ini: <b>{capacity} kotlet</b>\n"
        "..................................................\n"
        "👇 <b>Pilih barang:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>TOKO · GAME</b>\n"
        "..................................................\n"
        "Penghapusan batas kemenangan, paket koin, dan lisensi Mega-Klan.\n"
        "..................................................\n"
        "👇 <b>Pilih barang:</b>"
    ),
    "pay.invoice_desc": "Pengiriman instan konten dalam game ROFL HUB.",
    "pay.invoice_error": "⚠️ Gagal membuat invoice Telegram Stars. Coba lagi nanti.",
    "pay.success": "🎉 <b>Pembayaran dikonfirmasi!</b>\n🧾 <code>{charge}</code>\n💵 Terpotong: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 Pembayaran berhasil, tapi pengirimannya sedang terkendala. Kami sudah tahu masalahnya.\n"
        "Simpan nomor pembayaranmu: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Stars-mu dikembalikan secara otomatis.",
    "pay.keep_charge": "Simpan nomor pembayaran untuk refund: <code>{charge}</code>",
    "pay.already": "✅ Pembayaran ini sudah diproses, barangnya sudah dikirim sebelumnya.",
    "pay.support": (
        "🛟 <b>DUKUNGAN PEMBAYARAN TELEGRAM STARS</b>\n"
        "..................................................\n"
        "Semua barang ROFL HUB bersifat digital dan dikirim instan setelah pembayaran.\n\n"
        "⚙️ <b>Jika sudah bayar tapi barang tidak sampai:</b>\n"
        "bot otomatis mengembalikan Stars saat pengiriman gagal. Kalau itu tidak terjadi — "
        "kirim nomor pembayaranmu ke sini (ada di struk, format <code>xxxx...</code>) dan jelaskan masalahnya. "
        "Admin akan memeriksa pembayaranmu di database dan menyelesaikannya dalam 24 jam.\n\n"
        "💫 <b>Kebijakan refund:</b>\n"
        "refund dimungkinkan jika barang tidak diterima atau dikirim dengan kesalahan. "
        "Barang digital yang terkirim dengan benar tidak bisa di-refund.\n"
        "..................................................\n"
        "<i>Bagian ini adalah titik dukungan pembelian resmi sesuai aturan Telegram.</i>"
    ),

    # ---------------- pengiriman ----------------
    "dlv.cutlets": "🥩 Ditambahkan ke gudangmu: <b>{qty} kotlet</b>.",
    "dlv.miner": "🤖 Robot <b>“{name}”</b> telah tiba di ladangmu.\n⏳ Masa pakai: sampai <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robot Penambang",
    "dlv.miner_premium": "Pengebor Siber",
    "dlv.fridge": "📦 Kulkas diperluas menjadi <b>{capacity} kotlet</b>.",
    "dlv.coins": "💰 Masuk <b>+{amount} 🪙</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nuklir x5 aktif sampai <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Pendingin Nitrogen +40% aktif sampai <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Drone Master menjaga ladangmu sampai <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Batas kemenangan dihapus sampai <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Timmu mendapat status <b>MEGA-KLAN</b>: hingga {max} slot.",
    "dlv.err_fridge": "Kamu sudah punya kulkas sebesar ini atau lebih besar.",
    "dlv.err_no_team": "Kamu belum punya tim. Buat dulu lewat /create_team.",
    "dlv.err_mega": "Timmu sudah berstatus Mega-Klan.",
    "dlv.intern_upgrade": "♾ Robot Magang-mu naik jadi <b>Robot Penambang ABADI</b>: 5 🪙 per jam, tanpa kedaluwarsa!",
    "dlv.err_no_intern": "Belum ada Robot Magang aktif — aktifkan dulu di /farm.",
    "dlv.err_intern_refs": "Upgrade butuh {need} teman aktif (syaratnya ada di /invite); kamu punya {have}.",
    "mk.header": "📈 <b>BURSA KOTLET</b>\n..................................................\nOrder terbuka: <b>{orders}</b> · kotlet dijual: <b>{cutlets}</b> · harga terbaik: <b>{best}</b>\nBiaya hub: <b>{fee}%</b> per penjualan (dibakar — pelindung inflasi)\n🥩 Di gudangmu: <b>{inv}</b> kotlet\n\n{body}\n\n<i>Ketuk order untuk membeli. Untuk menjual: /sell.</i>",
    "mk.empty": "Belum ada penawaran. Jadilah yang pertama: /sell jumlah harga",
    "mk.order_line": "🥩 #{id} · <b>{qty} pcs</b> seharga <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} pcs seharga {price} 🪙",
    "mk.btn_my": "📋 Order saya",
    "mk.btn_sell_help": "💰 Cara menjual kotlet",
    "mk.btn_refresh": "🔄 Muat ulang",
    "mk.btn_back": "← Ke bursa",
    "mk.pick": "🛒 <b>Order #{id}</b>: tersedia {qty} pcs seharga {price} 🪙.\nBeli berapa?",
    "mk.btn_qty": "{qty} pcs — {total} 🪙",
    "mk.btn_qty_all": "Semua {qty} pcs — {total} 🪙",
    "mk.buy_toast": "Transaksi selesai!",
    "mk.buy_done": "✅ Terbeli <b>{qty} kotlet</b> seharga <b>{total} 🪙</b>. Sudah di gudang — isi bahan bakar Pengebor-mu!",
    "mk.sold_notify": "💰 <b>Bursa: terjual!</b> Order #{id}: {qty} pcs seharga {price}. Kamu dapat <b>+{got} 🪙</b> (biaya {fee} dibakar).",
    "mk.sell_help": "💰 <b>CARA MENJUAL KOTLET</b>\n\nPerintah: <code>/sell jumlah harga</code>\nContoh: <code>/sell 10 250</code> — 10 kotlet seharga 250 🪙.\n\nKotlet keluar dari gudang dan menunggu di order (bisa dibatalkan kapan saja). Maks {max_qty} pcs per order dan {max_orders} order terbuka. Biaya {fee}% dibakar saat terjual. Harga kotlet minimal {min} 🪙: bahan bakar dari toko seharga Bintang selalu lebih untung daripada bursa. Sumber daya, order beli, dan tukar ada di aplikasi game.",
    "mk.sell_confirm": "📝 Jual <b>{qty} kotlet</b> seharga <b>{price}</b> 🪙?\nTotal: {total} · biaya {fee} dibakar · kamu dapat <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ PASANG DI BURSA",
    "mk.btn_cancel": "❌ Batal",
    "mk.sell_toast": "Order terpasang!",
    "mk.sell_done": "✅ Order <b>#{id}</b> aktif: {qty} pcs seharga {price} 🪙. Kuberi tahu saat terjual.",
    "mk.cancelled_toast": "Dibatalkan",
    "mk.cancel_text": "❌ <b>Dibatalkan.</b> Kotlet tetap di gudang.",
    "mk.my_header": "📋 <b>ORDER-MU</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} pcs seharga {price} 🪙",
    "mk.my_empty": "📋 Kamu tidak punya order terbuka.",
    "mk.btn_cancel_order": "❌ Batalkan order #{id}",
    "mk.err_newbie_price": "🔒 While your account is new, you can buy at no more than {max} 🪙 apiece. The limit lifts at intelligence level {level} and after {claims} daily cutlets.",
    "mk.err_cancel_room": "📦 Not enough storage room: {free} free. Make room first, then withdraw the lot.",
    "sw.err_ratio": "⚖️ This swap is too uneven: the two sides (valued at the market's minimum prices) may differ by at most {x}×.",
    "mk.order_cancelled": "↩️ Order #{id} dibatalkan: <b>{qty} kotlet</b> kembali ke gudang.",
    "mk.err_qty": "❌ Jumlah: 1 sampai {max} buah per order.",
    "mk.err_price": "❌ Harga: {min} sampai {max} 🪙 per buah.",
    "mk.err_no_cutlets": "❌ Hanya ada {have} kotlet di gudang. Kotlet di kulkas tidak bisa dijual — lihat /farm.",
    "mk.err_too_many": "❌ Batas: maksimal {max} order terbuka. Batalkan satu di «Order saya».",
    "mk.err_not_found": "❌ Order ini sudah ditutup.",
    "mk.err_own": "🤨 Tidak bisa membeli order sendiri.",
    "mk.err_insufficient": "❌ Tidak cukup: butuh {total} 🪙.",
    "farm.btn_market": "📈 Bursa kotlet",

    # ---------------- sumber daya (gelombang 22.10, malam) ----------------
    "res.metal": "Logam",
    "res.hydrogen": "Hidrogen",
    "res.crystal": "Kristal",
    "res.parts": "Komponen",
    "res.none": "masih kosong",
    "games.resource_gain": "{icon} Didapat: <b>+{qty} {name}</b> (total {total}) → /workshop",
    "duel.metal_gain": "🪨 Trofi duel: <b>+{metal} Batu</b> → /workshop",
    "quest.win_resources": "\n📦 Plus paket: <b>{qty}</b> dari tiap sumber daya, 🪵 kayu, dan 🐄 sapi → /workshop",
    "profile.resources_line": "🧰 Sumber daya: {stock}\n",
    "menu.btn_goals": "🎯 Target harian",
    "menu.btn_raids": "🏴‍☠️ Serbuan",
    "menu.btn_workshop": "🔧 Bengkel",
    "farm.btn_workshop": "🔧 Bengkel",
    "farm.btn_app": "🏭 Ladang di aplikasi",
    "menu.btn_app": "🚀 Aplikasi game: ladang, bengkel, serbuan",
    "app.btn_section": "🚀 BUKA DI APLIKASI",
    "app.goto_workshop": "🔧 <b>Bengkel</b> ada di aplikasi game: sumber daya, resep, dan crafting sekali ketuk.",
    "app.goto_raids": "🏴\u200d☠️ <b>Serbuan</b> ada di aplikasi game: pengintaian, kuda-kuda pertahanan, dan balas dendam.",
    "app.goto_station": "🛰 <b>Stasiun Tim</b> ada di aplikasi game: progres, sumbangan, dan bonus untuk seluruh tim.",
    "app.goto_market": "📈 <b>Bursa kotlet</b> lebih nyaman di aplikasi game: penawaran, penjualan, dan order-mu dalam satu layar.",
    "mk.err_asset": "❌ Barang seperti itu tidak ada di bursa.",
    "mk.err_no_resource": "❌ Sumber daya tidak cukup: di gudang hanya ada {have}.",
    "mk.bid_filled_notify": "🙋 <b>Bursa: order beli terpenuhi!</b> Order #{id}: kamu membeli <b>+{qty} {icon}</b> seharga {price} 🪙.",
    "sw.err_same": "❌ Sumber daya tidak bisa ditukar dengan jenis yang sama.",
    "sw.err_qty": "❌ Isi jumlah 1 sampai {max} — baik yang kamu berikan maupun yang kamu inginkan.",
    "shop.btn_info": "ℹ️ Apa isi tiap barang",
    "sw.done_notify": "🔄 <b>Tukar #{id} berhasil!</b> Diberikan {give}, diterima {want}.",
    "ws.err_coins": "🔒 Koin tidak cukup: butuh {need} 🪙, saldomu {have} 🪙.",
    "wk.eff_nitrogen": "❄️ Nitrogen +40% selama {h} jam",
    "wk.eff_nuclear": "☢️ Nuklir x5 selama {h} jam",
    "wk.eff_drone": "🛸 Drone Master selama {h} jam",
    "wk.eff_shield": "🛡 Perisai selama {h} jam",
    "wk.eff_unlimit": "⚡ Game Tanpa Batas selama {h} jam",
    "wk.eff_cutlet": "🥩 Kotlet ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ Resep minggu ini sudah tidak tersedia.",
    "wk.err_limit": "🔒 Batas mingguan resep ini sudah habis ({limit}). Minggu baru mulai Senin 00:00 UTC.",
    "games.resource_full": "📦 Gudang {icon} penuh ({cap}) — kelebihannya hilang. Gunakan, jual, atau perluas gudang di bengkel.",
    "mk.err_storage_full": "📦 Tempat di gudang tidak cukup: sisa {free}. Perluas gudang di bengkel.",
    "mk.err_buyer_full": "📦 Gudang pembeli penuh — transaksi belum bisa dilakukan (sisa {free}).",
    "ws.recipe_storage": "Perluas gudang hingga {cap}",
    "ws.done_storage": "📦 <b>Gudang diperluas:</b> hingga {cap} tiap sumber daya. Selamanya.",
    "ws.err_storage_max": "📦 Gudang sudah berukuran maksimal.",
    "farm.boost_armor": "🛡 Zirah Siber level {level}: +{percent}% penambangan hingga {until} UTC",
    "farm.boost_station": "🛰 Stasiun Tim level {level}: +{percent}% penambangan",
    "clan.btn_station": "🛰 Stasiun Tim",

    # ---------------- bengkel ----------------
    "ws.header": (
        "🔧 <b>BENGKEL</b>\n"
        "..................................................\n"
        "🧰 Sumber dayamu: {stock}\n"
        "⛏ Logam — Suit & duel · 💧 Hidrogen — Besar/Kecil · "
        "💎 Kristal — Kuis · ⚙️ Komponen — Brankas Siber. Misi memberi paket lengkap.\n\n"
        "🛡 Zirah Siber: <b>level {armor}/{armor_max}</b> (+{armor_pct}% penambangan per level, selama 30 hari)\n"
        "🚀 Shuttle: <b>{shuttle}</b> — biaya bursa {shuttle_fee}%, maks {shuttle_qty} kotlet per order\n\n"
        "<i>✅ — sumber daya cukup, 🔒 — belum cukup. Sekali ketuk, langsung jadi.</i>"
    ),
    "ws.shuttle_yes": "sudah dibangun",
    "ws.shuttle_no": "belum dibangun",
    "ws.recipe_nitro_6h": "Pendingin Nitrogen selama 6 jam",
    "ws.recipe_nuclear_3h": "Boost Nuklir selama 3 jam",
    "ws.recipe_drone_24h": "Drone Master selama 24 jam",
    "ws.recipe_shield_24h": "Perisai anti-serbuan 24 jam",
    "ws.recipe_cutlet": "Sintesis kotlet siber",
    "ws.recipe_armor": "Zirah Siber level {level}",
    "ws.recipe_shuttle": "Bangun Shuttle",
    "ws.btn_shuttle_owned": "🚀 Shuttle sudah dibangun",
    "ws.btn_armor_max": "🛡 Zirah Siber: maksimal",
    "ws.btn_refresh": "🔄 Perbarui",
    "ws.btn_farm": "🚜 Ke ladang",
    "ws.noop": "Sudah maksimal",
    "ws.toast": "Selesai!",
    "ws.done_nitrogen": "❄️ <b>Pendingin Nitrogen +40%</b> aktif sampai {until} UTC.",
    "ws.done_nuclear": "☢️ <b>Boost Nuklir x5</b> aktif sampai {until} UTC. Para Pengebor makan kotlet ×3!",
    "ws.done_drone": "🛸 <b>Drone Master</b> menjaga robotmu sampai {until} UTC.",
    "ws.done_shield": "🛡 <b>Perisai anti-serbuan</b> bertahan sampai {until} UTC. Sumber dayamu aman.",
    "ws.done_cutlet": "🥩 Hasil sintesis: <b>+{qty} kotlet siber</b> masuk gudang. Isi bahan bakar di /farm!",
    "ws.done_armor": "🛡 <b>Zirah Siber level {level}!</b> Penambangan ladang: <b>+{percent}%</b> selama 30 hari.",
    "ws.done_shuttle": "🚀 <b>Shuttle selesai dibangun!</b> Biaya untuk penjualanmu kini {fee}%, maks {qty} kotlet per order. Shuttle ini hanya milikmu, selamanya.",
    "ws.err_unknown": "❌ Resep itu tidak ada.",
    "ws.err_off": "🔧 Resep ini sedang tidak tersedia.",
    "ws.err_locked": "🔒 Resep terbuka dalam {hours} jam — resep baru terbuka satu per hari.",
    "ws.recipe_camo_12h": "Kamuflase 12 jam",
    "ws.recipe_trap_24h": "Umpan selama 24 jam",
    "ws.recipe_drill_24h": "Pelatih kuda-kuda 24 jam",
    "ws.recipe_forsage": "Afterburner kapal",
    "ws.recipe_economizer": "Penghemat bahan bakar",
    "ws.recipe_cargo": "Kargo diperluas",
    "ws.recipe_thermos_24h": "Termos kotlet 24 jam",
    "ws.recipe_stamp": "Stempel bursa",
    "ws.recipe_banner_24h": "Panji tim 24 jam",
    "ws.recipe_dome_12h": "Kubah tim 12 jam",
    "ws.err_resources": "🔒 Tidak cukup: {kind} butuh {need}, punya {have}. Kumpulkan di game!",
    "ws.err_shuttle_owned": "🚀 Shuttle sudah dibangun — satu per pemain.",
    "ws.err_armor_max": "🛡 Zirah sudah di level maksimal ({max}).",

    # ---------------- serbuan ----------------
    "raid.header": (
        "🏴‍☠️ <b>SERBUAN</b>\n"
        "..................................................\n"
        "💧 Hidrogen: <b>{hydrogen}</b> (sekali terbang butuh {fuel})\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ Kuda-kuda pertahanan: <b>{stance}</b>\n\n"
        "📊 Serbuan: <b>{attacks}</b> (berhasil {attack_wins}) · ditahan: <b>{holds}/{defenses}</b>\n\n"
        "<i>Jarahan hanya sumber daya: {percent}% dari stok target, maks {cap} per jenis. "
        "Koin, robot, dan kotlet tidak bisa disentuh. Gesturmu melawan kuda-kuda target — "
        "keputusan lawan keputusan. Satu penerbangan tiap {cooldown} jam; balas dendam gratis.</i>"
    ),
    "raid.ready_line": "Kapal siap terbang",
    "raid.cooldown_line": "Pengisian ulang: {minutes} mnt lagi",
    "raid.shield_on": "Perisai aktif sampai {until} UTC",
    "raid.shield_newbie": "Perlindungan pemula ({days} hari pertama)",
    "raid.shield_off": "Tanpa perisai — bangun di /workshop",
    "raid.stance_random": "acak (pilih di menu!)",
    "raid.btn_scout": "🔭 INTAI: cari target",
    "raid.btn_revenge": "⚔️ Balas dendam: {name}",
    "raid.btn_stance": "✊ Kuda-kuda pertahanan",
    "raid.btn_workshop": "🛡 Bangun perisai",
    "raid.btn_refresh": "🔄 Perbarui",
    "raid.btn_back": "← Kembali",
    "raid.btn_open": "🏴‍☠️ Buka serbuan",
    "raid.btn_again": "🏴‍☠️ Ke serbuan",
    "raid.stance_pick": "✊ <b>Kuda-kuda pertahanan</b>\nHanya terlihat dari hasil serbuan orang lain: gestur penyerang melawan kuda-kudamu. Sesekali ganti — yang mudah ditebak bakal dijarah.",
    "raid.stance_saved": "Kuda-kuda: {stance}",
    "raid.scout": "🔭 <b>Pengintaian menemukan target.</b> Penerbangan memakan {fuel} 💧. Pilih:",
    "raid.btn_target": "🎯 {name} · sumber daya ≈{total}",
    "raid.no_targets": "🔭 Pengintaian tidak menemukan siapa pun: belum ada target yang cocok (perisai, pengisian ulang, pemula). Coba lagi nanti.",
    "raid.pick_move": "✊ <b>Gesturmu?</b> Akan diadu dengan kuda-kuda pertahanan target. Penerbangan: −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>Balas dendam! Gesturmu?</b> Penerbangan gratis dan tanpa pengisian ulang.",
    "raid.result_win": "🏴‍☠️ <b>SERBUAN BERHASIL!</b>\n{move} lawan {stance} milik {name}.\nJarahan: <b>{loot}</b>",
    "raid.result_draw": "😐 <b>Seri.</b> {move} lawan {stance} milik {name}. Kapal pulang kosong, bahan bakar terbakar.",
    "raid.result_lose": "💥 <b>PERTAHANAN KOKOH.</b> {move} lawan {stance} milik {name}.\nTarget mendapat: <b>{loot}</b>",
    "raid.result_footer": "<i>Sumber daya ada di /workshop. Perisai melindungimu dari serangan balasan.</i>",
    "raid.victim_lost": "🚨 <b>Kamu diserbu!</b> {name}: {move} lawan kuda-kudamu {stance}.\nHilang: <b>{loot}</b>\n\n⚔️ Balas dendam gratis dalam {hours} jam. Perisai — di /workshop.",
    "raid.victim_draw": "🛡 <b>Serbuan berakhir seri.</b> {name}: {move} lawan kuda-kudamu {stance}. Tidak ada yang hilang.",
    "raid.victim_held": "🛡 <b>Pertahananmu kokoh!</b> {name}: {move} lawan kuda-kudamu {stance}.\nTrofi pertahanan: <b>{loot}</b>",
    "raid.err_stance": "❌ Gestur tidak dikenal.",
    "raid.err_self": "🤨 Menyerbu diri sendiri? Tidak.",
    "raid.err_gone": "❌ Target tidak tersedia.",
    "raid.err_teammate": "🤝 Kita tidak menjarah kawan sendiri — itu rekan tim.",
    "raid.err_shielded": "🛡 Target punya perisai. Pilih yang lain.",
    "raid.err_revenge_gone": "❌ Waktu balas dendam sudah habis.",
    "raid.err_cooldown": "⏳ Pengisian ulang: {minutes} mnt lagi.",
    "raid.err_victim_cooldown": "⏳ Target ini baru saja dijarah (jeda {hours} jam).",
    "raid.err_fuel": "💧 Hidrogen kurang: butuh {need}, punya {have}. Dapatkan di Besar/Kecil.",

    # ---------------- target harian ----------------
    "goal.header": (
        "🎯 <b>TARGET HARI INI</b>\n"
        "..................................................\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 Peti: <b>+{coins} 🪙</b> dan <b>+{res}</b> sumber daya acak\n"
        "🔥 Rentetan: <b>{streak}</b> hari · tiap hari ke-{every} berturut-turut +{bonus} 🪙 ke peti\n\n"
        "<i>Target diperbarui pukul 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ Selesaikan ketiganya — petinya jadi milikmu.",
    "goal.status_ready": "✅ <b>Semua target selesai! Ambil petimu.</b>",
    "goal.status_claimed": "🎁 Peti hari ini sudah diambil. Besok ada target baru!",
    "goal.btn_claim": "🎁 AMBIL PETI",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Perbarui",
    "goal.toast": "Peti terbuka!",
    "goal.chest": "🎁 <b>PETI TERBUKA!</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 Rentetan: {streak} hari",
    "goal.err_claimed": "🎁 Hari ini sudah diambil.",
    "goal.err_not_done": "⏳ Belum semua target selesai.",
    "goal.win_quiz": "Menangkan {n} ronde kuis",
    "goal.win_rps": "Menangkan {n} ronde Suit",
    "goal.win_hl": "Menangkan {n} ronde Besar/Kecil",
    "goal.win_safe": "Bobol Brankas Siber {n} kali",
    "goal.play_rounds": "Mainkan {n} ronde game apa saja",
    "goal.duel": "Mainkan satu duel",
    "goal.bonus": "Ambil kotlet harian di ladang",
    "goal.craft": "Buat sesuatu di bengkel",
    "goal.raid": "Lakukan satu serbuan",
    "goal.market_deal": "Tutup satu transaksi di bursa",
    "goal.donate": "Sumbangkan sumber daya ke stasiun tim",

    # ---------------- stasiun tim ----------------
    "st.header": (
        "🛰 <b>STASIUN TIM “{team}”</b>\n"
        "..................................................\n"
        "Level: <b>{level}/{max}</b> → tiap petarung dapat <b>+{percent}%</b> penambangan ladang "
        "(+{per_level}% per level)\n\n"
        "📦 Menuju level berikutnya:\n{progress}\n\n"
        "🧾 Sumbangan terakhir:\n{feed}\n\n"
        "🧰 Sumber dayamu: {stock}\n"
        "<i>Stasiun milik bersama: dibangun seluruh tim, bonusnya untuk semua. Keluar dari tim — bonus hilang.</i>"
    ),
    "st.max_level": "🏁 Stasiun rampung — level maksimal!",
    "st.feed_empty": "belum ada yang menyumbang — jadilah yang pertama",
    "st.no_team": "🛰 Stasiun dibangun oleh tim. Gabung tim atau buat sendiri — lalu bangun bersama.",
    "st.btn_find_team": "🏆 Tim & klan",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ Semua: {qty} {icon} {name}",
    "st.btn_refresh": "🔄 Perbarui",
    "st.btn_team": "🏆 Ke tim",
    "st.toast": "Disumbangkan +{qty} {icon}",
    "st.level_up": "🛰 <b>Stasiun tim naik ke level {level}!</b> Semua petarung kini dapat +{percent}% penambangan ladang.",
    "st.err_qty": "❌ Jumlah tidak valid.",
    "st.err_no_team": "❌ Kamu belum punya tim.",
    "st.err_max": "🏁 Stasiun sudah rampung (level {max}).",
    "st.err_resources": "🔒 Sumber daya kurang: punya {have}.",

    # ---------------- tim/klan (permukaan utama) ----------------
    "clan.no_team": "⚠️ <b>Kamu belum punya tim!</b>\n\nKamu bisa mendaftarkan geng pribadimu sekarang juga dengan menekan tombol di bawah.",
    "clan.btn_create": "🏆 Buat Tim seharga 100k",
    "clan.btn_members": "👥 DAFTAR REKAN TIM",
    "clan.btn_leave": "🚪 Keluar dari tim / Tinggalkan geng",
    "clan.btn_dashboard": "🏆 Dasbor tim",
    "clan.status_clan": "👑 STATUS: KLAN IMPERIUM",
    "clan.status_team": "👥 STATUS: TIM BIASA",
    "clan.dashboard": (
        "🏆 <b>DASBOR INFORMASI TIMMU</b>\n"
        "..................................................\n"
        "📌 Nama: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Kapten geng: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Moto: <i>“{motto}”</i>\n"
        "🔮 Simbol lambang: {symbol}\n\n"
        "👥 Anggota: <b>{members} / {max_members}</b>\n"
        "..................................................\n"
        "👇 <b>NAVIGASI:</b>"
    ),
    "clan.members_only": "🔒 Daftar anggota hanya bisa dilihat oleh anggota tim ini!",
    "clan.members_gone": "❌ Tim ini sudah dibubarkan.",
    "clan.members_header": (
        "👥 <b>SUSUNAN TIM “{name}”</b>\n"
        "🧠 — level kecerdasan game (hanya bisa dilatih di /quiz)\n"
        "..................................................\n"
    ),
    "clan.members_footer": (
        "\n..................................................\n"
        "📄 Halaman <b>{page} / {pages}</b> · Total petarung: <b>{members}</b>\n"
        "<i>Ketuk @username rekan timmu untuk mengiriminya pesan, bangun chat kalian sendiri, "
        "dan ajak geng ke kompetisi tim!</i>"
    ),
    "clan.btn_prev": "⬅️ Kembali",
    "clan.btn_next": "Lanjut ➡️",
    "clan.join_ok": (
        "🎉 <b>SELAMAT, KAMU SUDAH MASUK!</b>\n\nKamu berhasil bergabung dengan tim <b>{name}</b>!\n"
        "📍 Ketik /my_team untuk mengecek susunan tim!"
    ),
    "clan.leave_ok": "🚪 Kamu keluar dari tim <b>{name}</b>. Sekarang kamu bebas lepas!",
}

MINIAPP = {
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
    "subtitle": "kerajaan game-mu dalam satu layar",
    "tab_passport": "📋 Paspor", "tab_farm": "🚜 Ladang", "tab_goals": "🎯 Target", "tab_workshop": "🔧 Bengkel",
    "tab_raids": "🏴‍☠️ Serbuan", "tab_market": "📈 Bursa", "tab_team": "🏆 Tim", "tab_shop": "🏪 Toko", "tab_top": "👑 TOP",
    "passport": "📋 PASPOR PEMAIN", "coins": "🪙",
    "brain": "🧠 Level kecerdasan", "toNext": "menuju level {n}: {left} jawaban benar di kuis (+{reward} 🪙)",
    "farm": "🚜 LADANG SIBER", "robots": "Robot (penambang / pengebor)",
    "intern": "Robot Magang (1 🪙/jam, abadi)", "activateIntern": "🚀 AKTIFKAN ROBOT MAGANG", "claimIntern": "🎁 AMBIL ROBOT MAGANG ({n})",
    "internDone": "🤖 Robot Magang-mu mulai bekerja!", "rank": "🎖 Pangkat",
    "openFarm": "🏭 BUKA TAMBANG", "farmScene": "🏭 LADANGMU", "back": "← Kembali",
    "minedVisit": "ditambang selama kunjungan ini", "unit_intern": "Robot Magang", "unit_junior": "Robot Penambang",
    "unit_premium": "Pengebor Siber", "eternal": "abadi", "fueledAll": "terisi bahan bakar",
    "fueledPart": "{a} dari {b} terisi", "license": "lisensi 30 hari",
    "emptyFarm": "Tambang kosong. Aktifkan Robot Magang-mu atau beli robot di toko!",
    "madeBy": "Mau bot seperti ini untuk proyekmu? Hubungi @mister_telebot",
    "fueled": "Pengebor terisi", "speed": "Kecepatan menambang",
    "perHour": "{v} 🪙/jam", "fridge": "Kulkas", "inv": "Kotlet di gudang",
    "burnout": "Hangus berikutnya", "boosts": "Boost aktif", "none": "tidak ada",
    "resources": "🧰 Sumber daya", "bonusPct": "Bonus penambangan permanen", "shuttle": "🚀 Shuttle sudah dibangun",
    "resHint": "Setiap kemenangan memberi sumber daya dari game-nya, dan dengan Tanpa Batas jumlahnya tak terbatas. Gunakan di bengkel.",
    "bonusReady": "🎁 KLAIM KOTLET HARIAN",
    "bonusWait": "⏳ Bonus dalam {h} jam {m} mnt", "bonusDone": "🎉 Kotlet masuk gudang!",
    "team": "🏆 TIMKU", "clan": "KLAN", "teamLabel": "Tim", "captain": "👑 Kamu kaptennya!",
    "members": "Anggota", "noTeam": "Kamu belum punya tim: gabung lewat rolet atau pencarian — atau buat sendiri.",
    "tab_faq": "📚 FAQ", "tab_rules": "📜 Perjanjian",
    "tm_roulette": "🎲 ROLET TIM", "tm_rotate": "🔄 Tampilkan tim lain", "tm_noFree": "Belum ada tim kosong — buat sendiri!",
    "tm_search": "🔍 CARI TIM", "tm_searchPh": "Nama atau sebagiannya", "tm_searchBtn": "Cari",
    "tm_notFound": "Tidak ada tim dengan nama itu", "tm_join": "💥 Gabung", "tm_joined": "Kamu masuk tim «{n}»!",
    "tm_create": "🏆 BUAT TIM", "tm_hubHint": "Tim hingga 50 petarung berharga {cost} 🪙. Di toko bisa ditingkatkan jadi Mega-Klan dengan 1000 tempat.",
    "tm_name": "Nama (maks. {n} karakter)", "tm_motto": "Motto (maks. {n} karakter)", "tm_symbol": "Lambang — emoji (maks. {n} karakter)",
    "tm_createBtn": "Buat seharga {cost} 🪙", "tm_created": "Tim «{n}» dibuat — kamu kaptennya!", "tm_noMoney": "Butuh {cost} 🪙, kamu punya {b} 🪙",
    "tm_roster": "👥 ANGGOTA TIM", "tm_mottoL": "💬 Motto", "tm_leave": "🚪 Keluar dari tim",
    "tm_leaveAsk": "Yakin keluar dari tim «{n}»?", "tm_leaveAskCaptain": "Kamu kapten: mahkota berpindah ke veteran tim. Yakin keluar dari «{n}»?",
    "tm_left": "Kamu tidak lagi berada di tim",
    "mk_scopePublic": "🌐 Bursa umum", "mk_scopeTeam": "🏆 Bursa tim",
    "mk_teamHint": "Bursa tim «{t}»: lot hanya terlihat dan bisa dibeli rekan tim, biaya cuma {f}%.",
    "mk_yourStock": "📦 Kamu punya", "mk_yourCoins": "💰 Koinmu",
    "tm_market": "🏪 BURSA TIM", "tm_marketBtn": "Buka bursa tim",
    "tm_marketHint": "Berdagang dengan rekan tim: biaya {f}% dibanding {p}% di bursa umum. Di Mega-Klan — cuma {c}%.",
    "hp_title": "🤝 GOTONG ROYONG", "hp_hint": "Kurang sumber daya? Minta ke timmu. Setiap orang bisa memberi hingga {d} sumber daya per hari.",
    "hp_today": "Kamu sudah memberi hari ini: {g} / {d}", "hp_empty": "Belum ada yang meminta bantuan",
    "hp_give": "🎁 +{n}", "hp_kind": "Yang dibutuhkan", "hp_qty": "Berapa banyak (hingga {n})", "hp_ask": "🙏 Minta bantuan",
    "hp_given": "Diberikan: {q} {k} — terima kasih sudah bermain sebagai tim!", "hp_asked": "Permintaanmu sudah dikirim ke tim!",
    "tab_storage": "📦 Gudang",
    "tab_mines": "⛏ Tambang", "tab_info": "📚 Info",
    "tab_lab": "🔬 Lab",
    "as_stone": "Batu",
    "as_wood": "Kayu",
    "as_fire": "Api",
    "as_energy": "Listrik",
    "as_battery": "Baterai",
    "as_cow": "Sapi",
    "as_core": "Inti",
    "tool_1": "Perkakas kasar",
    "tool_2": "Perkakas penyetelan halus",
    "tool_3": "Kalibrasi",
    "tool_4": "Nanoteknologi",
    "tech_comm": "KOMUNIKASI",
    "tech_scout": "PENGINTAIAN",
    "tech_attack": "SERANGAN",
    "tech_defense": "PERTAHANAN",
    "tech_science": "SAINS",
    "ws_needTool": "Butuh: {t}",
    "ws_teamItem": "🏆 Barang tim — melindungi seluruh tim (untuk Mega-Klan harga ×{x})",
    "eff_make": "bahan mentah diubah jadi material di gudang",
    "eff_cart": "gerobak untuk kuda: +1 lot di bursa",
    "eff_meds": "tanpa sakit saat serbuan dan di tambang",
    "it_meds": "KOTAK P3K",
    "mk_lots": "Lot terbuka: {o} dari {m} (🐎 {h} · 🛒 {c})",
    "badges": "🏅 Penghargaan musim",
    "sk_stable": "🐎 KANDANG",
    "sk_lots": "Lot di bursa: {n}",
    "sk_buyHorse": "🐎 Beli kuda seharga {p} 🪙",
    "sk_stableHint": "Tiap kuda memberi +1 lot di bursa, tiap gerobak tambah +1 (gerobak tidak boleh lebih banyak dari kuda). Koin untuk kuda hangus.",
    "sk_horseBought": "🐎 Kuda masuk kandang! Lot di bursa jadi lebih banyak.",
    "sk_shuttleCharge": "🚀 DAYA SHUTTLE",
    "sk_shuttleUntil": "🔋 Shuttle terisi sampai {t}",
    "sk_shuttleEmpty": "🪫 Daya Shuttle habis — keuntungan bursa tidak berlaku.",
    "sk_chargeBtn": "🔋 Isi: 1 baterai = {d} hari",
    "raid_needTech": "Serbuan butuh 📡 komunikasi, 🔭 pengintaian, dan ⚔️ serangan level 1.",
    "raid_toLab": "🔬 Ke Laboratorium",
    "raid_scoutInfo": "Pengintaian menampilkan target: {n}. Bahan bakar serbuan adalah hidrogen 💧",
    "raid_medsOn": "💊 Kotak P3K sampai {t}: bebas sakit",
    "raid_medsOff": "💊 Tanpa Kotak P3K, 15% jarahan hilang di rumah sakit",
    "raid_note_sick": "🤒 Tanpa Kotak P3K, sebagian jarahan hilang di rumah sakit",
    "mn_mined": "tertambang {n} {i}",
    "mn_left": "penambangan berakhir dalam: {t}",
    "mn_commNote": "Pendapatan masuk ke anggota dengan 📡 komunikasi 1+; tanpa 💊 Kotak P3K, setiap jam ke-7 hilang.",
    "top_season": "🏆 Musim",
    "top_rich": "💰 Terkaya",
    "top_seasonTitle": "🏆 MUSIM {s}",
    "top_left": "Musim berakhir dalam: {t}",
    "top_myPlace": "Peringkatmu: {p} dari {n} · didapat {e} 🪙",
    "top_noPlace": "Kamu belum masuk tabel — mainlah, peringkatmu akan muncul.",
    "top_prizes": "Hadiah musim diumumkan oleh penyelenggara. TOP-10 mendapat lencana musim di paspor.",
    "top_rules": "Dihitung koin yang didapat di game bulan ini: ladang, kemenangan, duel, kuis petualangan, peti, penjualan. Saldo tidak direset.",
    "top_players": "👤 PEMAIN MUSIM INI",
    "top_teams": "🏆 TIM MUSIM INI",
    "top_empty": "Musim baru dimulai — jadilah yang pertama!",
    "top_noTeams": "Belum ada battle di musim ini.",
    "top_teamRules": "Poin untuk peringkat di battle musim ini: 10 · 7 · 5 · 4 · 3 · 2 · 1.",
    "lab_tools": "🧰 PERKAKAS",
    "lab_toolsHint": "Set perkakas tidak habis dipakai — ia membuka resep rumit dan level teknologi.",
    "lab_nextTool": "Set berikutnya: {t}",
    "lab_craftTool": "Rakit set",
    "lab_toolsMax": "🧬 Semua set sudah dirakit!",
    "lab_level": "Level {l} dari {m}",
    "lab_max": "🏆 Level maksimum",
    "lab_wait": "⏳ Level berikutnya dalam {t}",
    "lab_up": "Pelajari level {l}",
    "res_stone_src": "duel, tambang, peti",
    "res_wood_src": "misi, tambang, peti",
    "res_fire_src": "Api unggun di bengkel",
    "res_energy_src": "peluang tiap menang, tambang, peti",
    "res_battery_src": "bengkel",
    "res_cow_src": "misi, peti hari ke-7, bursa",
    "res_core_src": "tambang dan hadiah penyelenggara",
    "sk_items": "🧪 Barang di gudang: {n} / {m} (10% kapasitas)",
    "sk_cutletsName": "Siber-kotlet",
    "it_total": "Di gudang: {n} buah",
    "bt_entry": "🔋 Pendaftaran tim: {n} / {m}",
    "bt_entered": "✅ Timmu ikut pertempuran tambang",
    "bt_give": "Setor 🔋 (kamu punya {n})",
    "bt_info": "Hanya tim yang terdaftar yang bertarung memperebutkan tambang: {f} 🔋, klan — {fc} 🔋. Patungan sama-sama satu tim!",
    "bt_notAllowed": "Pertempuran ini bukan untuk jenis timmu",
    "mn_place": "🏆 hadiah untuk peringkat {p}",
    "mn_soonShort": "Mulai: {d}",
    "top_events": "🎯 Event",
    "ev_empty": "Belum ada event sekarang — cek lagi nanti!",
    "ev_my": "Peringkatmu: {p}",
    "ev_noPlace": "Kamu belum masuk tabel — ayo!",
    "ev_manual": "Pemenang ditentukan oleh penyelenggara",
    "ev_places": "Peringkat berhadiah: {n}",
    "ev_prizes": "🎁 Hadiah",
    "ev_leaders": "Pemimpin",
    "lab_sciGate": "📚 Level {l} terbuka saat semua teknologi sudah di level {l}",
    "lab_cooldown": "Setelah dipelajari, level berikutnya terbuka dalam {d} hr.",
    "lab_done": "🔬 Selesai! Level {l}",
    "lab_eff_comm": "Level 1 — serbuan dan pendapatan tambang; tiap level berikutnya −{c} mnt pengisian ulang serbuan",
    "lab_eff_scout": "Tanpanya tak ada serbuan; target saat pengintaian: 2 + level",
    "lab_eff_attack": "Tanpanya tak ada serbuan; tiap level setelah yang pertama +{a}% jarahan",
    "lab_eff_defense": "Tiap level −{d}% dari yang bisa dibawa penyerbu darimu",
    "lab_eff_science": "+{s}% hasil ladang dan jarahan per level. Lama dipelajari dan butuh ☢️ Inti",
    "lab_how": "📖 Cara kerjanya",
    "lab_rule1": "Perkakas dirakit sekali saja: ⚒️ → 🛠 → 🔬 → 🧬. Tanpa set yang tepat, resep rumit atau level tidak bisa diambil.",
    "lab_rule2": "Setelah satu level dipelajari, level berikutnya dari teknologi yang sama terbuka tepat 30 hari kemudian — tiap peningkatan berharga. Sains tumbuh mengikuti teknologi lain.",
    "lab_rule3": "☢️ Inti hanya didapat lewat kerja tim: peringkat hadiah di battle dan sehari penuh menguasai tambang.",
    "durDH": "{d} h {h} j", "durHM": "{h} j {m} mnt", "durM": "{m} mnt",
    "ws_locked": "🔒 Terbuka dalam {t}", "ws_toStorage": "📦 Barang jadi masuk ke gudang",
    "eff_camo": "kamu tak terlihat di pengintaian serbuan, tapi tetap bisa menyerang", "eff_trap": "penyerbu yang gagal memberimu dua kali lipat",
    "eff_drill": "seri saat bertahan dihitung sebagai kegagalan penyerbu", "eff_thermos": "Pengebor makan kotlet 25% lebih lambat",
    "eff_banner": "+5% penambangan untuk seluruh timmu", "eff_dome": "perisai anti-serbuan untuk seluruh tim",
    "eff_forsage": "menghapus pengisian ulang serbuan (sekali sehari)", "eff_economizer": "penerbangan berikutnya tanpa hidrogen",
    "eff_cargo": "jarahan serbuan berikutnya ×1,5", "eff_stamp": "penjualan berikutnya di bursa tanpa biaya",
    "it_camo": "KAMUFLASE", "it_trap": "UMPAN", "it_drill": "PELATIH KUDA-KUDA", "it_thermos": "TERMOS KOTLET",
    "it_banner": "PANJI TIM", "it_dome": "KUBAH TIM", "it_forsage": "AFTERBURNER KAPAL", "it_economizer": "PENGHEMAT BAHAN BAKAR",
    "it_cargo": "KARGO DIPERLUAS", "it_stamp": "STEMPEL BURSA",
    "it_oneShot": "sekali pakai", "it_charges": "⚡ Terisi: {n}", "it_needTeam": "Barang tim — kamu harus berada di sebuah tim.",
    "it_charged": "⚡ Terisi! Aktif pada aksi berikutnya.", "it_forsaged": "🔥 Pengisian ulang dihapus — siap terbang!",
    "raid_armed": "⚡ Siap: {l}", "raid_guardUntil": "{n} sampai {t}", "raid_domeOn": "🛡 Kubah tim sampai {t}",
    "raid_forsageBtn": "🔥 Afterburner: hapus pengisian ulang ({n})",
    "raid_note_economizer": "⛽ Penghemat: terbang tanpa hidrogen", "raid_note_cargo": "📦 Kargo: jarahan ×1,5",
    "raid_note_trap": "🪤 Umpan target: kamu memberi dua kali lipat", "raid_note_drill": "🎯 Pelatih kuda-kuda target: seri dihitung kegagalanmu",
    "mn_title": "⛏ PETA TAMBANG", "mn_closed": "🔒 Ekspedisi ke tambang tidak mungkin sebelum battle tim atau klan dimulai.",
    "mn_pick": "Ketuk tambang untuk melihat detailnya.", "mn_info": "⛏ TAMBANG",
    "mn_battle": "⚔️ BATTLE «{t}» UNTUK TAMBANG №{n}", "mn_soon": "⏳ BATTLE «{t}» UNTUK TAMBANG №{n} — MULAI {d}",
    "mn_nom": "Kategori: {n}", "mn_ends": "Selesai: {d}", "mn_leaders": "Pemimpin saat ini", "mn_noLeaders": "Belum ada yang mencetak poin — timmu bisa jadi yang pertama!",
    "mn_myTeam": "🏆 TIMMU DI TAMBANG", "mn_income": "Hasil: {n} sumber daya per jam untuk seluruh tim",
    "mn_noIncome": "Belum ada tambang — menangkan battle tim, dan tambang jadi milikmu selama 72 jam.",
    "mn_noTeam": "Tambang hanya direbut oleh tim — gabung ke tim atau buat sendiri.", "mn_teamBtn": "🏆 Ke tim",
    "mn_how": "📖 Cara kerjanya", "mn_rule1": "Setiap battle tim dan klan memperebutkan tepat satu tambang. Menang tim dengan hasil gabungan terbaik dari semua anggotanya di kategori battle.",
    "mn_rule2": "Pemenang menguasai tambang {h} jam: tiap anggota tim mendapat {y} sumber daya tambang per jam. Makin banyak anggota — makin besar hasilnya.",
    "mn_rule3": "Setelah itu tambang bebas lagi, tetapi hanya bisa direbut di battle baru.",
    "mn_name": "⛏ TAMBANG №{n}", "mn_res": "Sumber daya", "mn_holder": "Pemilik", "mn_free": "bebas", "mn_untilL": "Dikuasai sampai",
    "mn_pumping": "Menghasilkan: {n} {i} per jam", "mn_targetOf": "⚔️ Battle «{t}» sedang memperebutkan tambang ini",
    "mn_closedOne": "🔒 Hanya bisa direbut di battle tim — pantau pengumuman.",    "raid_noFuel": "⛽ Kapal belum siap berangkat — butuh bahan bakar",
    "raid_shieldTitle": "🛡 PERISAI SERBUAN", "raid_shieldActive": "AKTIF", "raid_shieldInactive": "TIDAK AKTIF",
    "raid_shieldHint": "Selama perisai aktif, tidak ada yang bisa menyerbu kamu. Perisai dibuat di bengkel dan masuk ke gudang — aktifkan saat diperlukan.",
    "raid_toStorage": "📦 Buka gudang",
    "sk_res": "📦 SUMBER DAYA DI GUDANG", "sk_expand": "🔧 Perluas gudang",
    "sk_cutlets": "🥩 KOTLET SIBER", "sk_cutletsHint": "Bahan bakar Pengebor Siber: 1 kotlet = sehari bekerja.",
    "sk_refuel": "🚜 Isi bahan bakar di ladang",
    "it_nitrogen": "PENDINGIN NITROGEN +40%", "it_nuclear": "BOOST NUKLIR X5", "it_drone": "DRONE MASTER",
    "it_shield": "PERISAI SERBUAN", "it_unlimit": "GAME TANPA BATAS", "it_unlimitDesc": "kemenangan game tanpa batas harian",
    "it_hours": "{h} jam", "it_use": "Aktifkan", "it_empty": "Kosong. Buat di bengkel — barangnya akan masuk ke sini.",
    "it_toWorkshop": "🔧 Ke bengkel", "it_active": "✅ Aktif sampai {t}", "it_used": "✅ Diaktifkan! Aktif sampai {t}",
    "it_stored": "📦 Selesai! Barangnya ada di gudang — aktifkan di tab «Gudang» kapan pun diperlukan.",
    "sk_shuttle": "🚀 SHUTTLE", "sk_shuttleOn": "Dimiliki: biaya bursa {f}%, batas order lebih besar.", "sk_shuttleOff": "Belum punya. Dibuat di bengkel.",
    "sk_armor": "🦾 ZIRAH SIBER", "sk_armorOn": "Level {l} dari {m}: +{p}% penambangan sampai {t}.",
    "sk_armorOff": "Belum dipakai. Tiap level memberi +{p}% penambangan selama 30 hari.",
    "sk_store": "🏗 PERLUASAN GUDANG", "sk_storeLvl": "Kapasitas: {c} untuk tiap sumber daya.", "sk_storeMax": "🏆 Gudang sudah maksimal!",
    "hp_who": "Pemain dari Level Kecerdasan {l} dengan {c} kotlet harian yang sudah diambil bisa memberi.",
    "top": "👑 TOP-100 PEMAIN TERKAYA EKOSISTEM",
    "shop": "🏪 TOKO", "shopFarm": "🚜 UNTUK LADANG", "shopGames": "🕹️ GAME",
    "shopHint": "Bayar dengan Telegram Stars resmi — langsung di sini, sekali ketuk.",
    "paid": "🎉 Pembayaran berhasil! Barangnya sudah ada di akunmu.",
    "payFail": "Pembayaran tidak berhasil. Coba lagi.",
    "oldClient": "Perbarui Telegram untuk belanja dari aplikasi, atau buka toko di chat bot.",
    "ctaNoRobots": "💤 Ladangmu hampir kosong! Ambil robot yang lebih kuat — 🪙 akan mengalir nonstop.",
    "ctaHungry": "🚨 Para Pengebor kelaparan ({n} tanpa bahan bakar) — penambangan berhenti!",
    "ctaLowFuel": "⚠️ Kotlet tidak cukup untuk sehari kerja para Pengebor.",
    "ctaShopBtn": "🛒 Ke toko",
    "footer": "Duels and quests are in the bot chat for now",
    "noProfile": "Profil tidak ditemukan. Buka bot dan tekan /start!",
    "blocked": "Akun diblokir oleh admin.",
    "deleting": "Akunmu dijadwalkan untuk dihapus. Berubah pikiran? Batalkan di chat bot.",
    "error": "Gagal memuat data. Coba lagi nanti.",
    "outside": "Buka aplikasi ini dari bot Telegram ROFL HUB.",
    "robotsTitle": "🤖 ROBOT-ROBOTMU", "buyMore": "🛒 Beli", "rateShort": "{v} 🪙/jam",
    "refuelOne": "🥩 Isi 1", "refuelAll": "⚡ Isi semua", "refueled": "Terisi: {n} 🥩",
    "res_metal_src": "BGK", "res_hydrogen_src": "Besar/Kecil", "res_crystal_src": "Kuis",
    "res_parts_src": "Brankas Siber", "resWhere": "cara mendapatkan",
    "ws_title": "🔧 BENGKEL", "ws_hint": "Sumber daya dari game diubah jadi upgrade. Kalau sumber dayanya cukup — tekan «Rakit».",
    "ws_craft": "Rakit", "ws_owned": "✅ Sudah punya", "ws_crafted": "Selesai! Upgrade-nya sudah aktif.",
    "ws_armor": "🛡 Zirah Siber", "ws_armorLvl": "level {l}/{m} · +{p}% per level selama 30 hari",
    "ws_shuttleOn": "🚀 Shuttle sudah dibangun: biaya bursa {fee}%", "ws_shuttleOff": "🚀 Belum ada Shuttle: biaya bursa {fee}%",
    "eff_nitrogen": "+40% penambangan semua robot", "eff_nuclear": "×5 penambangan, Pengebor makan kotlet ×3",
    "eff_drone": "robot tidak menua", "eff_shield": "tidak ada yang bisa menyerbumu",
    "eff_cutlet": "1 kotlet siber ke gudang (mahal: bahan bakar lebih murah di toko)", "eff_armor": "+10% penambangan per level selama 30 hari",
    "eff_shuttle": "hanya milikmu: biaya 5% untuk penjualanmu dan order hingga 500 kotlet — selamanya",
    "eff_storage": "lebih banyak tempat untuk sumber daya — selamanya",
    "tab_friends": "🤝 Teman", "ref_title": "🤝 UNDANG TEMAN",
    "ref_rules": "{q} untuk setiap teman aktif — satu kali. Teman aktif sudah mencapai level intelektual {l} dan mengambil {c} kotlet harian.",
    "ref_copy": "📋 Salin", "ref_copied": "Link disalin!", "ref_share": "📤 Bagikan",
    "ref_stats": "📊 JARINGANMU", "ref_invited": "diundang", "ref_qualified": "aktif", "ref_earned": "didapat",
    "ref_top": "🏆 SIAPA PUNYA TEMAN TERBANYAK",
    "ref_topHint": "✅ — teman aktif, 👥 — semua yang diundang", "ref_empty": "Peringkat masih kosong — jadilah yang pertama!",
    "wk_title": "🔥 RESEP MINGGU INI", "wk_hint": "Resep terbatas: muncul atas keputusan hub lalu menghilang. Rakit sebelum terlambat!",
    "wk_left": "sisa rakitan minggu ini: {n} dari {m}", "st_cap": "📦 Gudang: hingga {c} tiap sumber daya — kelebihan hasil tambang hilang",
    "raid_title": "🏴‍☠️ SERBUAN", "raid_how": "📖 Cara kerjanya",
    "raid_rule1": "Kamu memilih gestur, target sudah memasang kuda-kuda pertahanan sebelumnya. Hasilnya ditentukan suit batu-gunting-kertas: ini duel keputusan, bukan lotre.",
    "raid_rule2": "Menang: ambil {pct}% tiap sumber daya target, maksimal {cap} per sumber daya. Gagal: berikan {fpct}% milikmu ke target, maksimal {fcap}. Seri: bahan bakar hangus.",
    "raid_rule3": "Hanya sumber daya yang bisa dirampas. Koin, robot, dan kotlet sepenuhnya aman. Pemain baru terlindungi {days} hari, rekan tim tidak boleh diserbu.",
    "raid_rule4": "Sekali terbang butuh {fuel} 💧 hidrogen, berikutnya setelah {cd} jam. Kalau kamu diserbu, balas dendam gratis selama {rh} jam.",
    "raid_fuel": "💧 Hidrogen", "raid_ready": "🚀 Kapal siap terbang", "raid_cooldown": "⏳ Isi ulang: {m} mnt",
    "raid_shieldOn": "🛡 Perisai sampai {t}", "raid_shieldNewbie": "🛡 Perlindungan pemain baru", "raid_shieldOff": "🛡 Tanpa perisai — rakit di bengkel",
    "raid_stance": "✊ KUDA-KUDA PERTAHANANMU", "raid_stanceHint": "Dengan ini kamu menghadapi serbuan pemain lain. Ganti sesekali — yang mudah ditebak lebih sering dirampok.",
    "raid_stanceNone": "Kuda-kuda belum dipilih — akan acak", "raid_stanceSaved": "Kuda-kuda disimpan",
    "raid_stats": "Serbuan: {a} ({w} berhasil) · ditahan: {h} dari {d}",
    "raid_scout": "🔭 PENGINTAIAN: cari target", "raid_targets": "🎯 Pilih target", "raid_res": "sumber daya ≈{n}",
    "raid_noTargets": "Belum ada target yang cocok: perisai, isi ulang, pemain baru. Coba lagi nanti.",
    "raid_pickMove": "✊ Gesturmu melawan kuda-kuda {name}", "raid_revenge": "⚔️ BALAS DENDAM", "raid_revengeBtn": "⚔️ Balas: {name}",
    "raid_win": "🏴‍☠️ Serbuan berhasil!", "raid_draw": "😐 Seri — kapal pulang dengan tangan kosong",
    "raid_lose": "💥 Pertahanan bertahan", "raid_vs": "{m} vs {s}", "raid_loot": "Rampasan: {l}", "raid_lost": "Diberikan ke target: {l}",
    "rock": "🪨 Batu", "scissors": "✂️ Gunting", "paper": "📄 Kertas",
    "mk_title": "📈 BURSA", "mk_stats": "Order: {o} · kotlet: {c} · harga terbaik: {b} 🪙",
    "mk_feeLine": "Biaya {f}% per penjualan dibakar — perisai anti-inflasi", "mk_inv": "🥩 Di gudangmu: {n}",
    "mk_offers": "🛒 PENAWARAN", "mk_empty": "Belum ada penawaran — jadilah yang pertama!",
    "mk_offer": "{q} 🥩 × {p} 🪙", "mk_buyHow": "Beli berapa?", "mk_all": "Semua {q}",
    "mk_sellTitle": "💰 JUAL KOTLET", "mk_qty": "Jumlah kotlet", "mk_price": "Harga per buah, 🪙",
    "mk_preview": "Transaksi {t} 🪙 · kamu dapat {g} 🪙 · dibakar {f} 🪙", "mk_sell": "Pasang di bursa",
    "mk_limits": "Maks {q} kotlet per order, maks {o} order terbuka",
    "mk_my": "📋 ORDER-KU", "mk_cancel": "Batalkan", "mk_bought": "Terbeli {q} 🥩 seharga {t} 🪙",
    "mk_listed": "Order terpasang! Kukabari saat terjual.", "mk_cancelledMsg": "Order dibatalkan, kotlet kembali ke gudang",
    "as_cutlet": "Kotlet", "as_metal": "Logam", "as_hydrogen": "Hidrogen", "as_crystal": "Kristal", "as_parts": "Komponen",
    "mk_index": "📈 INDEKS BURSA", "mk_chart": "📊 HARGA 7 HARI", "mk_noTrades": "Belum ada transaksi — jadilah yang pertama!",
    "mk_avg": "Harga rata-rata seminggu: {p} 🪙 · terjual: {v}", "mk_asks": "🛒 DIJUAL", "mk_bids": "🙋 DICARI",
    "mk_noBids": "Belum ada order beli", "mk_sellTo": "Jual", "mk_sellHow": "Jual berapa?",
    "mk_bidTitle": "🙋 ORDER BELI", "mk_bidHint": "Koin dibekukan di order sampai terjadi transaksi. Batalkan order — koin kembali.",
    "mk_bid": "Pasang order beli", "mk_bidPreview": "{t} 🪙 akan dibekukan", "mk_have": "Punyamu: {n}",
    "mk_floor": "Harga kotlet minimal {p} 🪙: bahan bakar dari toko seharga Bintang selalu lebih untung",
    "mk_side_sell": "jual", "mk_side_buy": "beli", "mk_listedBid": "Order beli terpasang! Koin dibekukan sampai transaksi.",
    "mk_sold": "Terjual {q}, diterima {g} 🪙 setelah biaya", "mk_shuttleNote": "🚀 Shuttle-mu: biaya {f}% untuk penjualanmu",
    "sw_title": "🔄 TUKAR SUMBER DAYA", "sw_hint": "Berikan yang berlebih — dapatkan yang dibutuhkan. Tanpa koin, tanpa biaya.",
    "sw_give": "Kamu berikan", "sw_want": "Ingin kamu dapat", "sw_qty": "Berapa", "sw_create": "Tawarkan tukar", "sw_take": "Tukar",
    "shop_info": "ℹ️ Apa isi tiap barang", "sw_youGet": "Kamu dapat", "sw_youGive": "Sebagai gantinya kamu berikan",
    "sw_takeBtn": "Tukar — berikan {x}", "sw_mineLine": "Kamu berikan {g} → ingin {w}",
    "sw_qtyErr": "Isi jumlah di atas nol di kedua kolom",
    "sw_empty": "Belum ada tawaran tukar", "sw_mine": "Tawaranku", "sw_done": "Tukar berhasil!",
    "sw_created": "Tawaran dipasang, sumber daya disisihkan", "sw_cancelled": "Tawaran dibatalkan, sumber daya kembali",
    "ws_armorUntil": "🛡 Zirah aktif hingga {t}",
    "st_title": "🛰 STASIUN TIM", "st_level": "Level {l} dari {m}", "st_bonus": "+{p}% penambangan untuk setiap petarung",
    "st_next": "Level {n} butuh {c} dari setiap sumber daya", "st_max": "🏁 Stasiun selesai dibangun!",
    "st_feed": "🧾 Sumbangan terbaru", "st_feedEmpty": "Belum ada sumbangan — jadilah yang pertama",
    "st_donate": "Sumbang", "st_all": "Semua", "st_done": "Tersumbang!",
    "st_hint": "Seluruh tim membangunnya, semua dapat bonus. Keluar dari tim — bonus hilang.",
    "st_off": "Stasiun sedang dalam perawatan sementara",
    "goals_title": "🎯 TARGET HARI INI", "goals_chest": "🎁 Peti untuk ketiganya: +{c} 🪙 dan +{r} sumber daya acak",
    "goals_streak": "🔥 Rentetan: {s} hari · tiap hari ke-{e} berturut-turut +{b} 🪙", "goals_claim": "🎁 KLAIM PETI",
    "goals_claimed": "🎁 Peti hari ini sudah diklaim. Target baru besok!", "goals_reset": "Target diperbarui pukul 00:00 UTC",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · rentetan {s} hari",
    "featureOff": "⚙️ Bagian ini sedang dalam perawatan", "done": "Selesai!", "loading": "⏳ Memuat…",
}

COMMANDS = {
    "app": "🎮 Buka Mini App",
    "menu": "📱 Menu utama",
    "profile": "👤 Profil & pasporku",
    "farm": "🚜 Ladang siber & pengisian bahan bakar",
    "shop": "🏪 Toko (Telegram Stars)",
    "games": "🕹️ Semua game melawan bot",
    "quiz": "🧠 Kuis: 15 detik per jawaban",
    "duel": "⚔️ Duel 1-lawan-1 dengan taruhan",
    "quests": "🗺️ Misi: cerita dengan pilihan",
    "my_team": "🏆 Timku & rekan tim",
    "invite": "🤝 Link referal: +500 per teman aktif",
    "transfer": "🔄 Kirim koin ke pemain",
    "market": "📈 Bursa kotlet: beli atau jual",
    "sell": "💰 Jual kotlet: /sell jumlah harga",
    "my_stats": "📊 Statistikku",
    "faq": "📚 Pertanyaan umum",
    "rules": "📜 Perjanjian pengguna",
    "paysupport": "🛟 Dukungan pembayaran",
    "workshop": "🔧 Bengkel: sumber daya jadi peningkatan",
    "raid": "🏴‍☠️ Serbuan: pengintaian & balas dendam",
    "goals": "🎯 Target harian & peti",
    "station": "🛰 Stasiun tim: proyek bersama",
}
