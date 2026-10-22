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
        "💸 Kamu menerima: <b>{balance} koin</b>\n"
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
        "- Kanal ROFL HUB CHANNEL yang seru dan penuh pengetahuan\n"
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
        "..................................................\n\n"
        "👤 <b>PROFIL PRIBADI & PASPOR:</b>\n"
        "• /start — Mulai perkenalan dan daftarkan akun\n"
        "• /profile — Paspormu, saldo, dan tim secara real time\n"
        "• /my_stats — Statistik historismu selama 30 hari terakhir\n\n"
        "🚜 <b>LADANG SIBER & OTOMATISASI:</b>\n"
        "• /farm — Hub bahan bakar: pengisian dan kecepatan produksi robot\n"
        "• /shop — Marketplace: beli penambang, kotlet, dan upgrade hub\n\n"
        "🕹️ <b>RUANG GAME:</b>\n"
        "• /games — Hub inline semua game melawan bot\n"
        "• /quiz — Kuis kecepatan: 15 detik per jawaban, level dan bonus\n"
        "• /duel — DUEL 1-lawan-1 dengan pemain sungguhan: meja 10/100/1000\n"
        "• /quests — MISI: cerita detektif, komedi, dan teka-teki berhadiah\n"
        "• /rps, /high_low, /safe — Game cepat berhadiah koin\n\n"
        "👥 <b>MANAJEMEN GENG:</b>\n"
        "• /create_team — Daftarkan tim sendiri seharga 100.000 koin\n"
        "• /my_team — Dasbor geng dan DAFTAR REKAN TIM dengan level 🧠\n"
        "• /all_teams — Rulet tim acak\n\n"
        "💸 <b>UANG & TEMAN:</b>\n"
        "• /invite — Link referalmu: +1000 koin per teman\n"
        "• /transfer — Kirim koin ke pemain lain\n\n"
        "📚 <b>PANDUAN & ATURAN:</b>\n"
        "• /faq — Panduan lengkap ekosistem (dibuka di Mini App)\n"
        "• /rules — Perjanjian pengguna\n"
        "..................................................\n"
        "<i>⚙️ Gunakan panel game dua kolom permanen di bagian bawah layar untuk navigasi instan antarbagian!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>SELAMAT DATANG DI ZONA GAME ROFL HUB!</b>\n"
        "..................................................\n\n"
        "Lawan bot dalam duel cepat atau ikuti tes sprint intelektual "
        "untuk menang besar — atau kehilangan semuanya!\n\n"
        "💸 Tiap kemenangan: <b>+2 koin</b> (Brankas Siber: <b>+5</b>)\n"
        "💀 Kalah atau seri: dipotong <b>-1 koin</b>\n"
        "🧠 Di Kuis ada timer 15 detik dan level kecerdasan: level 1 = 10 jawaban benar dan <b>+100 koin</b>, "
        "setiap level berikutnya 10 jawaban lebih panjang — tapi hadiahnya naik 100!\n\n"
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
        "..................................................\n\n"
        "Versi singkatnya:\n"
        "🚜 Robot menambang koin nonstop: Robot Penambang — 5/jam tanpa bahan bakar, "
        "Pengebor Siber — 10/jam, dan SETIAP Pengebor memakan 1 kotlet sibernya sendiri per hari. "
        "Semua robot bertahan 30 hari (Drone Master menghentikan sementara keausan).\n"
        "🧠 Kuis: 15 detik per jawaban, level kecerdasan dengan hadiah yang terus naik.\n"
        "⚔️ Duel melawan pemain sungguhan di meja 10/100/1000 koin.\n"
        "🏆 Tim hingga 50 petarung (Mega-Klan — hingga 1000) dan event Pertempuran berhadiah untuk semua.\n\n"
        "..................................................\n"
        "👇 <b>Panduan lengkap dengan semua mekanik — satu ketukan saja:</b>"
    ),
    "faq.btn_open": "📖 BUKA PANDUAN LENGKAP",
    "rules.teaser": (
        "📜 <b>PERJANJIAN PENGGUNA ROFL HUB</b>\n"
        "..................................................\n\n"
        "Intinya:\n"
        "🪙 Koin dan semua item dalam game adalah elemen hiburan virtual: "
        "bukan uang dan tidak bisa ditukar dengan dana nyata.\n"
        "💫 Pembelian hanya lewat Telegram Stars resmi; barang digital dikirim "
        "instan, dan Stars dikembalikan otomatis jika pengiriman gagal.\n"
        "🛡️ Kami tidak mengumpulkan nomor telepon, lokasi, atau data pribadi.\n"
        "🤝 Dilarang menghina, memakai trik curang, dan multi-akun — pelanggaran bisa berujung blokir.\n\n"
        "..................................................\n"
        "👇 <b>Teks lengkap perjanjian dan disclaimer — satu ketukan saja:</b>\n"
        "<i>⚖️ Dengan menggunakan bot ini kamu menyatakan setuju dengan ketentuannya.</i>"
    ),
    "rules.btn_open": "📜 BUKA PERJANJIAN LENGKAP",
    "quest.list_header": (
        "🗺️ <b>MISI ROFL HUB</b>\n"
        "..................................................\n\n"
        "Cerita interaktif dengan pilihan dan percabangan: detektif, komedi, teka-teki. "
        "Kemenangan pertama di setiap misi memberi koin, dan kamu bisa mengulanginya sepuasnya!\n"
        "🌐 <i>Cerita misi masih berbahasa Rusia untuk saat ini — paket bahasa baru segera hadir.</i>\n\n"
        "👇 <b>Pilih cerita:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} mnt · 🏆 +{reward} koin untuk kemenangan pertama\n"
        "..................................................\n\n"
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
    "quest.win_first": "\n\n🏆 <b>MISI SELESAI! Hadiah: +{coins} koin.</b>",
    "quest.win_repeat": "\n\n✅ <b>Selesai lagi!</b> Hadiah misi ini sudah pernah diklaim sebelumnya.",
    "quest.fail_footer": "\n\n💀 <i>Bukan akhir yang terbaik... tapi ceritanya selalu bisa diulang!</i>",
    "quest.stale": "⏳ Adegan itu sudah lewat — kita lanjut dari posisi sekarang!",
    "quest.no_coins": "❌ Koin tidak cukup untuk petunjuk ({cost}). Mampir ke ladangmu!",
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
    "farm.status_no_drills": "💡 Pelihara Pengebor Siber di /shop untuk menambah penghasilan.",
    "farm.boost_nuclear": "🔋 Boost Nuklir x5 sampai {until} UTC (konsumsi kotlet ×3)",
    "farm.boost_nitrogen": "❄️ Pendingin Nitrogen +40% sampai {until} UTC",
    "farm.boost_drone": "🛸 Drone Master memperpanjang umur robot sampai {until} UTC",
    "farm.no_boosts": "Tidak ada boost aktif — cek /shop.",
    "farm.burnout": "🔥 Robot berikutnya hangus pada: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Aktifkan Robot Magang-mu (gratis)",
    "farm.intern_activated": "🤖 Robot Magang-mu mulai bekerja! +1 koin per jam selamanya — tanpa bahan bakar, tanpa kedaluwarsa.",
    "farm.intern_already": "🤖 Robot Magang-mu sudah bekerja.",
    "farm.intern_line": "🤖 Robot Magang ({rate} koin/jam, abadi): <code>{count}</code>",
    "farm.intern_hint": "🎁 Kamu punya Robot Magang gratis! Tekan tombol di bawah — dia akan menambang 1 koin per jam selamanya.",
    "farm.dashboard": (
        "🚜 <b>HUB BAHAN BAKAR PUSAT ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Robot aktif di pabrik: <b>{total}</b>\n"
        "• Robot Penambang ({junior_rate} koin/jam): <code>{junior}</code>\n"
        "• Pengebor Siber ({premium_rate} koin/jam): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>KECEPATAN LADANGMU SAAT INI:</b>\n"
        "• Produksi per jam: <b>+{speed_hour} koin</b>\n"
        "• Produksi per hari: <b>+{speed_day} koin</b>\n\n"
        "⚡ <b>BOOST:</b>\n{boosts}\n\n"
        "📋 <b>STATUS PABRIK GAME:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>STATUS KULKAS OTOMATIS:</b>\n"
        "🥩 Stok bahan bakar: <b>{fridge} / {capacity}</b>\n"
        "💼 Kotlet di gudang: <code>{inv}</code>\n\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
        "🆔 ID Paspormu: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Koin saat ini: <b>{balance} koin</b>\n"
        "🏆 Statusmu: <b>{team}</b>\n"
        "🧠 Level kecerdasan: <b>{level}</b> · menuju level {next_level}: "
        "<b>{left}</b> jawaban benar di /quiz (hadiah: +{reward} koin)\n\n"
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
        "..................................................\n\n"
        "🧠 Level kecerdasan game: <b>{level}</b> (total jawaban benar: {total})\n"
        "🎮 Ronde duel dimainkan: <b>{played}</b>\n"
        "🏆 Kemenangan diraih: <code>{won}</code>\n"
        "👥 Teman aktif yang diundang: <b>{refs}</b>\n\n"
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
    "games.win": "🎉 <b>MENANG!</b> 🎉\nKoin didapat: <b>+{reward}</b>",
    "games.lose": "💀 <b>KALAH!</b>\nKoin dipotong: <b>-{penalty}</b>",
    "games.draw": "🤝 <b>SERI!</b>\nKoin dipotong: <b>-{penalty}</b>",
    "games.limit": (
        "🛑 <b>Batas harian tercapai!</b>\n\n"
        "Kamu sudah meraih {limit} kemenangan di {game} hari ini. Batas di-reset pada 00:00 UTC.\n\n"
        "⚡ Hapus batas selama 24 jam — 5 ★, selama 30 hari — 99 ★ (bagian “Game” di /shop)."
    ),
    "games.no_coins": "❌ Koinmu 0 — tidak ada yang bisa dipakai membayar biaya ronde. Ambil penghasilan ladangmu di /farm!",
    "games.balance": "💰 Saldo: <b>{balance} koin</b>",
    "games.btn_retry": "🎮 Main lagi!",
    "games.btn_hub": "🕹️ Zona game",
    "games.level_up": (
        "🏅 <b>LEVEL KECERDASAN NAIK: {level}!</b> Hadiah: <b>+{bonus} koin</b>!\n"
        "Level berikutnya: {next_required} jawaban benar → +{next_reward} koin."
    ),
    "games.name.rps": "Batu-Gunting-Kertas",
    "games.intern_bonus": "🤖 Level {level}! Satu Robot Magang lagi datang ke farm-mu — sekarang ada {count}.",
    "games.name.hl": "Besar/Kecil",
    "games.name.quiz": "Kuis",
    "games.name.safe": "Brankas",

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
    "quiz.lost_line": "💀 <b>-{penalty} koin</b> karena kalah!",
    "quiz.level_line": (
        "🧠 Level kecerdasan: <b>{level}</b>\n"
        "Kemenangan tersisa menuju level {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} detik per jawaban!\n"
        "Benar: +{win} koin ke saldomu\n"
        "Salah / kehabisan waktu: -{penalty} koin\n"
        "Batas: {limit} kemenangan per hari</i>"
    ),



    # ---------------- Brankas ----------------
    "safe.intro": (
        "🔐 <b>BRANKAS SIBER</b>\n\n"
        "Di dalamnya — jackpot <b>{jackpot} koin</b>! Pintunya terkunci dengan kode dari 1 sampai {codes}. "
        "Kamu punya satu percobaan.\n"
        "Dibobol: <b>+{jackpot}</b> · Alarm: <b>-{penalty}</b> · Batas: <b>{limit}</b> kemenangan"
    ),
    "safe.btn_retry": "🔐 Bobol lagi!",
    "safe.win": "🔓 <b>Brankas terbuka!</b> Kodenya: <b>{code}</b>.",
    "safe.lose": "🚨 <b>Alarm berbunyi!</b> Kamu menebak {guess}, padahal kodenya: <b>{code}</b>.",

    # ---------------- duel ----------------
    "duel.intro": (
        "⚔️ <b>DUEL 1-LAWAN-1: BATU-GUNTING-KERTAS DENGAN TARUHAN</b>\n"
        "..................................................\n\n"
        "Pilih meja sesuai kantongmu — seperti di poker. Taruhan langsung dipotong, "
        "dan lawanmu adalah pemain ROFL HUB sungguhan!\n\n"
        "💰 Pot = kedua taruhan. Pemenang mengambil <b>{payout_percent}%</b> pot, "
        "<b>{burn_percent}%</b> terbakar selamanya (deflasi!).\n"
        "🤝 Seri berarti gestur langsung diulang — pot tetap di meja.\n"
        "⏱ Waktu per gestur — <b>{move_timeout} detik</b>; kalau diam saja, gesturmu dipilihkan generator acak.\n"
        "🏆 Kemenangan duel dihitung untuk timmu di Pertempuran!\n\n"
        "👇 <b>PILIH MEJA:</b>"
    ),
    "duel.btn_table": "⚔️ Meja {stake} koin",
    "duel.btn_cancel": "❌ Tinggalkan meja (taruhan kembali)",
    "duel.btn_move_rock": "🪨 Batu",
    "duel.btn_move_scissors": "✂️ Gunting",
    "duel.btn_move_paper": "🧻 Kertas",
    "duel.waiting": (
        "🪑 <b>Kamu di meja {stake} koin.</b> Taruhanmu sudah masuk pot.\n"
        "Menunggu petarung kedua... Begitu dia duduk, kalian berdua akan diminta memilih gestur!\n"
        "<i>Antrean berlaku {ttl} menit, setelah itu taruhanmu otomatis kembali.</i>"
    ),
    "duel.cancelled": "🚪 Kamu meninggalkan meja. Taruhan <b>{stake} koin</b> kembali ke saldomu.",
    "duel.expired": "⌛ Tidak ada lawan yang muncul di meja {stake}. Taruhan <b>{stake} koin</b> sudah dikembalikan.",
    "duel.matched": (
        "⚔️ <b>LAWAN DITEMUKAN! Meja {stake} koin.</b>\n"
        "Pot: <b>{bank} koin</b> · Untuk pemenang: <b>{payout}</b>\n\n"
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
        "💰 Kemenangan: <b>+{payout} koin</b> · 🔥 Terbakar dari pot: {burned}\n"
        "💼 Saldo: <b>{balance} koin</b>"
    ),
    "duel.lose": (
        "💀 <b>DUEL KALAH.</b>\n\n"
        "{winner_move} lawan mengalahkan {loser_move} milikmu.\n"
        "📉 Taruhan <b>{stake} koin</b> masuk ke pot pemenang.\n"
        "Rematch?"
    ),
    "duel.reaper_prefix": "⏰ <b>Ronde kehabisan waktu!</b> Gestur yang belum dipilih ditentukan oleh generator acak.\n\n",
    "duel.bad_table": "❌ Meja seperti itu tidak ada.",
    "duel.already_in": "⚠️ Kamu sudah di meja atau sedang bertarung! Selesaikan dulu duel yang sedang berjalan.",
    "duel.no_coins": "❌ Kamu butuh {stake} koin di saldo untuk meja ini.",
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
    "rank.dead": "DEAD",

    # ---------------- referal ----------------
    "ref.text": (
        "🤝 <b>PROGRAM REFERAL ROFL HUB</b>\n"
        "..................................................\n\n"
        "Undang teman dan dapatkan <b>+{bonus} koin</b> untuk setiap orang "
        "yang mendaftar lewat link pribadimu!\n\n"
        "🔗 <b>Link-mu (ketuk untuk menyalin):</b>\n<code>{link}</code>\n\n"
        "📊 <b>STATISTIKMU:</b>\n"
        "👥 Teman yang diundang: <b>{invited}</b>\n"
        "💰 Penghasilan dari referal: <b>{earned} koin</b>\n\n"
        "..................................................\n"
        "<i>Sebarkan link ke teman sekelas, sahabat, dan media sosial — makin besar gengmu, makin cepat saldomu tumbuh!</i>"
    ),
    "ref.btn_share": "📣 Bagikan link",
    "ref.share_text": "Gabung ke ekosistem game ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Hadiah ganda:</b> saat teman yang kamu undang main {rounds} "
                           "ronde, kamu dapat <b>+{bonus} koin</b> lagi!"),
    "ref.qualified_notify": ("🤝 <b>Temanmu ketagihan: sudah {rounds} ronde!</b>\n"
                             "Kamu dapat <b>+{bonus} koin</b> untuk referral berkualitas. "
                             "Undang lagi!"),

    # ---------------- transfer ----------------
    "tr.help": (
        "🔄 <b>KIRIM KOIN KE PEMAIN LAIN</b>\n"
        "..................................................\n\n"
        "Format perintah:\n"
        "<code>/transfer ID jumlah</code> — lewat ID Paspor (lihat /profile)\n"
        "<code>/transfer @username jumlah</code> — lewat username\n"
        "<code>/transfer ROFL-HUB-777 jumlah</code> — lewat VIP ID dari lelang\n\n"
        "Contoh:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Jumlah minimum: <b>{min} koin</b>"
    ),
    "tr.not_found": "❌ Penerima tidak ditemukan. Periksa ID Paspor atau @username — pemainnya harus sudah terdaftar di bot.",
    "tr.self": "🤨 Mengirim koin ke diri sendiri tidak bisa — itu sih mesin ekonomi abadi namanya!",
    "tr.blocked": "🚫 Pemain ini diblokir — transfer ke dia tidak tersedia.",
    "tr.min": "❌ Jumlah transfer minimum adalah {min} koin.",
    "tr.insufficient": "❌ Koin tidak cukup! Saldomu: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Koin di saldomu tidak cukup.",
    "tr.confirm": (
        "🔄 <b>KONFIRMASI TRANSFER:</b>\n\n"
        "👤 Penerima: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Jumlah yang dipotong: <b>{amount} koin</b>{fee_line}\n"
        "💰 Penerima mendapat: <b>{received} koin</b>\n\n"
        "<i>Transfer tidak bisa dibatalkan — periksa lagi penerimanya!</i>"
    ),
    "tr.fee_line": "\n🔥 Biaya hub: <b>{fee} koin</b> (terbakar)",
    "tr.btn_confirm": "✅ KONFIRMASI TRANSFER",
    "tr.btn_cancel": "❌ Batal",
    "tr.cancelled_toast": "Transfer dibatalkan",
    "tr.cancelled": "❌ <b>Transfer dibatalkan.</b> Koinmu tetap aman.",
    "tr.not_yours": "🔒 Ini bukan transfermu!",
    "tr.done_toast": "✅ Transfer berhasil!",
    "tr.done": (
        "✅ <b>TRANSFER BERHASIL!</b>\n\n"
        "💸 Terkirim: <b>{amount} koin</b> ke pemain ID <code>{recipient_id}</code>\n"
        "💰 Saldomu: <b>{balance} koin</b>"
    ),
    "tr.received": (
        "💰 <b>Kamu menerima {amount} koin!</b>\n"
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
        "..................................................\n\n"
        "Semua barang ROFL HUB bersifat digital dan dikirim instan setelah pembayaran.\n\n"
        "⚙️ <b>Jika sudah bayar tapi barang tidak sampai:</b>\n"
        "bot otomatis mengembalikan Stars saat pengiriman gagal. Kalau itu tidak terjadi — "
        "kirim nomor pembayaranmu ke sini (ada di struk, format <code>xxxx...</code>) dan jelaskan masalahnya. "
        "Admin akan memeriksa pembayaranmu di database dan menyelesaikannya dalam 24 jam.\n\n"
        "💫 <b>Kebijakan refund:</b>\n"
        "refund dimungkinkan jika barang tidak diterima atau dikirim dengan kesalahan. "
        "Barang digital yang terkirim dengan benar tidak bisa di-refund.\n\n"
        "..................................................\n"
        "<i>Bagian ini adalah titik dukungan pembelian resmi sesuai aturan Telegram.</i>"
    ),

    # ---------------- pengiriman ----------------
    "dlv.cutlets": "🥩 Ditambahkan ke gudangmu: <b>{qty} kotlet</b>.",
    "dlv.miner": "🤖 Robot <b>“{name}”</b> telah tiba di ladangmu.\n⏳ Masa pakai: sampai <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robot Penambang",
    "dlv.miner_premium": "Pengebor Siber",
    "dlv.fridge": "📦 Kulkas diperluas menjadi <b>{capacity} kotlet</b>.",
    "dlv.coins": "💰 Masuk <b>+{amount} koin</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nuklir x5 aktif sampai <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Pendingin Nitrogen +40% aktif sampai <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Drone Master menjaga ladangmu sampai <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Batas kemenangan dihapus sampai <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Timmu mendapat status <b>MEGA-KLAN</b>: hingga {max} slot.",
    "dlv.err_fridge": "Kamu sudah punya kulkas sebesar ini atau lebih besar.",
    "dlv.err_no_team": "Kamu belum punya tim. Buat dulu lewat /create_team.",
    "dlv.err_mega": "Timmu sudah berstatus Mega-Klan.",
    "dlv.intern_upgrade": "♾ Robot Magang-mu naik jadi <b>Robot Penambang ABADI</b>: 5 koin per jam, tanpa kedaluwarsa!",
    "dlv.err_no_intern": "Belum ada Robot Magang aktif — aktifkan dulu di /farm.",
    "dlv.err_intern_refs": "Upgrade butuh {need} teman berkualitas (30 ronde masing-masing); kamu punya {have}.",

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
        "..................................................\n\n"
        "📌 Nama: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Kapten geng: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Moto: <i>“{motto}”</i>\n"
        "🔮 Simbol lambang: {symbol}\n\n"
        "👥 Anggota: <b>{members} / {max_members}</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVIGASI:</b>"
    ),
    "clan.members_only": "🔒 Daftar anggota hanya bisa dilihat oleh anggota tim ini!",
    "clan.members_gone": "❌ Tim ini sudah dibubarkan.",
    "clan.members_header": (
        "👥 <b>SUSUNAN TIM “{name}”</b>\n"
        "🧠 — level kecerdasan game (hanya bisa dilatih di /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
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
    "subtitle": "kerajaan game-mu dalam satu layar",
    "passport": "📋 PASPOR PEMAIN", "coins": "koin",
    "brain": "🧠 Level kecerdasan", "toNext": "menuju level {n}: {left} jawaban benar di kuis (+{reward} koin)",
    "farm": "🚜 LADANG SIBER", "robots": "Robot (penambang / pengebor)",
    "fueled": "Pengebor terisi", "speed": "Kecepatan menambang",
    "perHour": "{v} koin/jam", "fridge": "Kulkas", "inv": "Kotlet di gudang",
    "burnout": "Hangus berikutnya", "boosts": "Boost aktif", "none": "tidak ada",
    "intern": "Robot Magang (1 koin/jam, abadi)",
    "activateIntern": "🚀 AKTIFKAN ROBOT MAGANG",
    "internDone": "🤖 Robot Magang-mu mulai bekerja!",
    "rank": "🎖 Pangkat",
    "openFarm": "🏭 BUKA FARM",
    "farmScene": "🏭 FARM-MU",
    "back": "← Kembali",
    "minedVisit": "ditambang selama kunjungan ini",
    "unit_intern": "Robot Magang",
    "unit_junior": "Robot Penambang",
    "unit_premium": "Cyber-Bor",
    "eternal": "abadi",
    "fueledAll": "terisi bahan bakar",
    "fueledPart": "{a} dari {b} terisi",
    "license": "lisensi 30 hari",
    "emptyFarm": "Tambang kosong. Aktifkan Robot Magang-mu atau beli robot di toko!",
    "madeBy": "Mau bot seperti ini untuk proyekmu? Hubungi @mister_telebot",
    "bonusReady": "🎁 KLAIM KOTLET HARIAN",
    "bonusWait": "⏳ Bonus dalam {h} jam {m} mnt", "bonusDone": "🎉 Kotlet masuk gudang!",
    "team": "🏆 TIMKU", "clan": "KLAN", "teamLabel": "Tim", "captain": "👑 Kamu kaptennya!",
    "members": "Anggota", "noTeam": "Belum punya tim — bangun gengmu di chat bot!",
    "top": "👑 TOP-100 PEMAIN TERKAYA EKOSISTEM",
    "shop": "🏪 TOKO", "shopFarm": "🚜 UNTUK LADANG", "shopGames": "🕹️ GAME",
    "shopHint": "Bayar dengan Telegram Stars resmi — langsung di sini, sekali ketuk.",
    "paid": "🎉 Pembayaran berhasil! Barangnya sudah ada di akunmu.",
    "payFail": "Pembayaran tidak berhasil. Coba lagi.",
    "oldClient": "Perbarui Telegram untuk belanja dari Mini App, atau buka toko di chat bot.",
    "ctaNoRobots": "💤 Ladangmu kosong! Pelihara robot pertamamu — koin akan mengalir nonstop.",
    "ctaHungry": "🚨 Para Pengebor kelaparan ({n} tanpa bahan bakar) — penambangan berhenti!",
    "ctaLowFuel": "⚠️ Kotlet tidak cukup untuk sehari kerja para Pengebor.",
    "ctaShopBtn": "🛒 Ke toko",
    "footer": "Kendali penuh — di chat bot: /menu",
    "noProfile": "Profil tidak ditemukan. Buka bot dan tekan /start!",
    "blocked": "Akun diblokir oleh admin.",
    "error": "Gagal memuat data. Coba lagi nanti.",
    "outside": "Buka aplikasi ini dari bot Telegram ROFL HUB.",
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
    "invite": "🤝 Link referal: +1000 per teman",
    "transfer": "🔄 Kirim koin ke pemain",
    "my_stats": "📊 Statistikku",
    "faq": "📚 Pertanyaan umum",
    "rules": "📜 Perjanjian pengguna",
    "paysupport": "🛟 Dukungan pembayaran",
}
