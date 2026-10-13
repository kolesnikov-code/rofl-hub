"""Deutsche (du) Lokalisierung ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> Münzen
# Младший Майнер -> Miner-Bot
# Кибер-Бурильщик -> Cyber-Bohrer
# кибер-котлета -> Cyber-Frikadelle (кратко: Frikadelle)
# Холодильник -> Kühlschrank
# склад -> Lager
# ферма -> Farm (Cyber-Farm)
# Ядерный Разгон x5 -> Nuklear-Boost x5
# Азотное Охлаждение +40% -> Stickstoff-Kühlung +40%
# Мастер-дрон -> Master-Drohne
# Кибер-Сейф -> Cyber-Tresor
# Мега-Клан -> Mega-Clan
# Безлимит -> Limit-Aufhebung (Sieglimits aufgehoben)
# дуэли -> Duelle
# битвы -> Schlachten
# квесты -> Quests
# уровень интеллекта -> Intelligenz-Level
# банда -> Crew; банк (дуэли) -> Pot; жест -> Zeichen; ставка -> Einsatz

BUTTONS = {
    "main_menu": "📱 HAUPTMENÜ",
    "profile": "👤 MEIN PROFIL",
    "farm": "🚜 MEINE FARM",
    "games_zone": "🕹️ SPIELZONE",
    "teams": "🏆 TEAMS & CLANS",
    "shop": "🏪 SHOP",
    "shop_cat_farm": "🚜 FÜR DIE FARM",
    "shop_cat_games": "🕹️ GAMING",
}

STRINGS = {
    # ---------------- allgemein ----------------
    "common.no_profile": "⚠️ Profil nicht gefunden. Tippe auf /start, um dich zu registrieren.",
    "common.btn_menu": "💿 Hauptmenü",
    "common.blocked": "🚫 Dein Account wurde von der ROFL-HUB-Administration gesperrt.",
    "common.feature_off": "⚙️ Dieser Bereich wird gerade gewartet. Schau etwas später wieder vorbei!",
    "common.maintenance": "🛠 ROFL HUB ist kurz in Wartung. Gleich zurück — deine Münzen und dein Fortschritt sind sicher!",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Willkommen zurück, @{username}!</b>\nDein Fortschritt ist sicher. Die Navigationsleiste ist unten auf dem Bildschirm.",
    "start.btn_continue": "🛸 WEITER",
    "start.btn_cutlet": "Was ist eine Cyber-Frikadelle?🥩🤔",
    "start.btn_fight": "Erzähl schnell — und ab in den KAMPF!",
    "start.console": "🚀 <b>Steuerkonsole aktiviert! Nutze die Buttons unten auf dem Bildschirm.</b>",
    "start.intro1": (
        "👋 <b>Hi! Ich bin der ROFL HUB BOT — der Haupt-Bot des Spiele-Ökosystems ROFL HUB. "
        "Ein Hub der neuen Generation für Games und Wissen!</b>\n\n"
        "<b>Hier kannst du:</b>\n"
        "🎮 Chat-Bot-Spiele gegen den Bot und andere Spieler zocken\n"
        "💸 Spielwährung für Siege verdienen oder eine Farm starten, die rund um die Uhr schürft\n"
        "🤼 Ein Team gründen und die Rangliste stürmen\n"
        "🏆 Dein Team zum Clan ausbauen und im internationalen Ranking kämpfen\n"
        "💰 Zusammen mit deiner Crew den Millionen-Münzen-Jackpot knacken\n"
        "👑 Eine Veröffentlichung auf unseren Social-Media-Seiten oder der Website kaufen, um dich oder deinen Blog zu promoten\n\n"
        "<b>Dieser Chat-Bot kann:</b>\n"
        "🎮 Die Liste aller Spiele, Kanäle und Websites von ROFL HUB zeigen\n"
        "⚡ Münzen für Spiele, Team- und Clan-Schlachten, Erfolge, Aktivität und Einladungen gutschreiben\n"
        "🔄 Spielmünzen an andere ROFL-HUB-Spieler überweisen\n"
        "💎 Website-Veröffentlichungen und VIP-Plätze für Persönlichkeiten und Blogger verkaufen\n"
        "🚀 Booster, Titel, Status und vieles mehr verkaufen...\n\n"
        "<i>Tippe auf „WEITER“ und ich erzähle dir mehr 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>HIER SIND DEINE ERSTEN BELOHNUNGEN FÜR DIE REGISTRIERUNG!</b>\n"
        "..................................................\n"
        "💸 Gutgeschrieben: <b>{balance} Münzen</b>\n"
        "🥩 Gutgeschrieben: <b>{cutlets} Cyber-Frikadelle</b>\n"
        "..................................................\n"
        "Das ist dein Startbonus für den Beitritt zum ROFL-HUB-Club.\n\n"
        "🔒 <i>Den Bonus gibt es nur einmal — im Moment der Registrierung.</i>\n\n"
        "Münzen kannst du auf viele Arten ausgeben — sie sind das Fundament der Hub-Wirtschaft. Pass gut auf sie auf...\n\n"
        "⁉️ <b>Aber du fragst dich sicher:</b> Was soll diese Frikadelle? Wen soll ich damit füttern?"
    ),
    "start.intro3": (
        "<b>ZUERST: WARUM SIND SPIELMÜNZEN SO WICHTIG?</b>\n\n"
        "Münzen sind die Grundlage für Handel, Wettkämpfe und Käufe in <b>ROFL HUB</b>. "
        "Sie sind fast die einzige Spielwährung der Welt, die man kostenlos schürfen kann!\n"
        "..................................................\n"
        "<b>Es gibt viele Wege, sie zu verdienen:</b>\n"
        "- Freunde über deinen Einladungslink einladen\n"
        "- Spiele gegen den Bot gewinnen\n"
        "- Duelle gegen andere Spieler gewinnen\n"
        "- An Team- und Clan-Schlachten teilnehmen\n"
        "- Täglichen Login-Bonus und Aufgaben abholen\n"
        "- Einen Roboter holen, der rund um die Uhr Münzen schürft (Miner-Bot / Cyber-Bohrer)\n"
        "..................................................\n"
        "<b>Wenn du einen Roboter der zweiten Stufe hast (den Cyber-Bohrer), musst du ihn jeden Tag füttern. "
        "Genau hier kommt die Cyber-Frikadelle ins Spiel: Treibstoff für das automatische Schürfen, "
        "den es jeden Tag gratis gibt! Deine Aufgabe ist simpel — vorbeischauen und den Roboter füttern.</b>\n\n"
        "Verpasst du die Fütterung, schaltet der Roboter ab und das Schürfen stoppt.\n\n"
        "Der Miner-Bot (erste Stufe) braucht keinen Treibstoff. "
        "Wichtig! Jeder Roboter wird für 30 Tage gekauft — danach kaufst du ihn neu oder holst dir eine Master-Drohne. "
        "Du kommst schnell rein:) Nicht ablenken lassen.\n\n"
        "Noch ein bisschen mehr über <b>ROFL HUB</b>, damit du verstehst, wie hier alles läuft.\n\n"
        "🛑 <b>Das ist die letzte Nachricht unseres Kennenlernens. Danach geht's direkt in den Kampf:)</b>"
    ),
    "start.intro4": (
        "<b>DIE KURZFASSUNG. ROFL HUB IST:</b>\n"
        "- Chat-Bot-Spiele für jeden Geschmack\n"
        "- Die Möglichkeit, ein eigenes Team zu gründen (bis zu 50 Leute)\n"
        "- Die Möglichkeit, es zum Clan auszubauen (bis zu 1000 Leute)\n"
        "- Team- und Clan-Schlachten um Preise\n"
        "- Der ROFL HUB CHANNEL mit Fun und Wissen\n"
        "- Instagram-Seite — rofl_hub_global\n"
        "- Website rofl-hub.com zum Chatten und Promoten ohne Registrierung\n"
        "- Tausende Spieler weltweit — vielleicht sind deine neuen Freunde schon dabei!\n"
        "..................................................\n"
        "<b>Wie versprochen: Das ist die letzte Nachricht. Jetzt geht's in den Kampf! Nützliche Befehle:</b>\n\n"
        "/menu — schnelle Steuerung aller Funktionen\n"
        "/games — Liste aller Spiele\n"
        "/faq — häufig gestellte Fragen\n"
        "/rules — Nutzungsvereinbarung\n"
    ),

    # ---------------- Menü & Spielzone ----------------
    "menu.text": (
        "📱 <b>ROFL HUB ÖKOSYSTEM — HAUPTMENÜ</b>\n"
        "..................................................\n\n"
        "👤 <b>PROFIL & PASS:</b>\n"
        "• /start — Intro starten und Account registrieren\n"
        "• /profile — Dein Pass, Kontostand und Team in Echtzeit\n"
        "• /my_stats — Deine Statistik der letzten 30 Tage\n\n"
        "🚜 <b>CYBER-FARM & AUTOMATISIERUNG:</b>\n"
        "• /farm — Treibstoff-Hub: Auftanken und Schürf-Tempo der Roboter\n"
        "• /shop — Marktplatz: Miner, Frikadellen und Hub-Upgrades\n\n"
        "🕹️ <b>SPIELZONE:</b>\n"
        "• /games — Inline-Hub aller Spiele gegen den Bot\n"
        "• /quiz — Speed-Quiz: 15 Sekunden pro Antwort, Level und Boni\n"
        "• /duel — 1-gegen-1-DUELLE mit echten Spielern: Tische 10/100/1000\n"
        "• /quests — QUESTS: Krimis, Komödien und Rätsel mit Belohnungen\n"
        "• /rps, /high_low, /coin, /dice, /safe — Schnelle Spiele um Münzen\n\n"
        "👥 <b>CREW-VERWALTUNG:</b>\n"
        "• /create_team — Eigenes Team für 100.000 Münzen registrieren\n"
        "• /my_team — Crew-Dashboard und TEAMMATE-LISTE mit 🧠-Leveln\n"
        "• /all_teams — Roulette zufälliger Teams\n\n"
        "💸 <b>GELD & FREUNDE:</b>\n"
        "• /invite — Dein Einladungslink: +1000 Münzen pro Freund\n"
        "• /transfer — Münzen an andere Spieler senden\n\n"
        "📚 <b>GUIDE & REGELN:</b>\n"
        "• /faq — Der komplette Ökosystem-Guide (öffnet sich in der Mini App)\n"
        "• /rules — Nutzungsvereinbarung\n"
        "..................................................\n"
        "<i>⚙️ Nutze die permanente zweispaltige Game-Leiste unten auf dem Bildschirm für blitzschnelle Navigation!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>WILLKOMMEN IN DER ROFL HUB SPIELZONE!</b>\n"
        "..................................................\n\n"
        "Fordere den Bot in schnellen Duellen heraus oder starte den Intelligenz-Sprint — "
        "hol dir den Jackpot oder verzocke alles!\n\n"
        "💸 Ein Sieg bringt: <b>+2 Münzen</b> (Cyber-Tresor: <b>+5</b>)\n"
        "💀 Niederlage oder Unentschieden kostet: <b>-1 Münze</b>\n"
        "🧠 Im Quiz: 15-Sekunden-Timer und Intelligenz-Level. Level 1 = 10 richtige Antworten und <b>+100 Münzen</b>, "
        "jedes weitere Level ist 10 Antworten länger — aber die Belohnung wächst um 100!\n\n"
        "..................................................\n"
        "👇 <b>TIPP AUF EINEN BUTTON UND STARTE SOFORT EINE RUNDE:</b>"
    ),
    "menu.btn_quiz": "🧠 Quiz",
    "menu.btn_rps": "🪨 SSP",
    "menu.btn_hl": "📈 Höher/Tiefer",
    "menu.btn_coin": "🪙 Kopf/Zahl",
    "menu.btn_dice": "🎲 Würfel",
    "menu.btn_safe": "🔐 Cyber-Tresor",
    "menu.btn_duel": "⚔️ 1-gegen-1-DUELLE",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Pass, Farm, Team und die reichsten Spieler — auf einem Neon-Screen. "
        "Die tägliche Frikadelle kannst du direkt dort abholen!\n\n"
        "👇 Tipp auf den Button:"
    ),
    "app.btn": "🎮 MINI APP ÖFFNEN",
    "app.unavailable": "⚙️ Die Mini App verbindet sich noch mit den Servern des Ökosystems. Schau gleich wieder vorbei!",
    "faq.teaser": (
        "📚 <b>ROFL HUB ÖKOSYSTEM-GUIDE</b>\n"
        "..................................................\n\n"
        "Das Wichtigste in Kürze:\n"
        "🚜 Roboter schürfen rund um die Uhr Münzen: Miner-Bot — 5/Std. ohne Treibstoff, "
        "Cyber-Bohrer — 10/Std., und JEDER Bohrer frisst täglich seine eigene Cyber-Frikadelle. "
        "Alle Roboter leben 30 Tage (die Master-Drohne pausiert den Verschleiß).\n"
        "🧠 Quiz: 15 Sekunden pro Antwort, Intelligenz-Level mit wachsenden Belohnungen.\n"
        "⚔️ Duelle gegen echte Spieler an Tischen mit 10/100/1000 Münzen.\n"
        "🏆 Teams bis 50 Kämpfer (Mega-Clan — bis 1000) und Event-Schlachten mit Preisen für alle.\n\n"
        "..................................................\n"
        "👇 <b>Der komplette Guide mit allen Mechaniken — nur einen Tap entfernt:</b>"
    ),
    "faq.btn_open": "📖 KOMPLETTEN GUIDE ÖFFNEN",
    "rules.teaser": (
        "📜 <b>ROFL HUB NUTZUNGSVEREINBARUNG</b>\n"
        "..................................................\n\n"
        "Kurz und knapp:\n"
        "🪙 Münzen und alle Spielgegenstände sind virtuelle Unterhaltungselemente: "
        "Sie sind kein Geld und können nicht in echtes Geld umgetauscht werden.\n"
        "💫 Käufe laufen nur über offizielle Telegram Stars; digitale Artikel werden "
        "sofort geliefert, bei Lieferfehlern werden Stars automatisch erstattet.\n"
        "🛡️ Wir sammeln keine Telefonnummern, Standorte oder persönlichen Daten.\n"
        "🤝 Beleidigungen, Manipulationen und Multi-Accounts sind verboten — Verstöße können zur Sperre führen.\n\n"
        "..................................................\n"
        "👇 <b>Der komplette Text der Vereinbarung samt Haftungsausschluss — per Button:</b>\n"
        "<i>⚖️ Mit der Nutzung des Bots bestätigst du dein Einverständnis mit den Bedingungen.</i>"
    ),
    "rules.btn_open": "📜 KOMPLETTE VEREINBARUNG ÖFFNEN",
    "quest.list_header": (
        "🗺️ <b>ROFL HUB QUESTS</b>\n"
        "..................................................\n\n"
        "Interaktive Storys mit Entscheidungen und Verzweigungen: Krimis, Komödien, Rätsel. "
        "Der erste Sieg in jeder Quest bringt Münzen, und jede Story kannst du beliebig oft wiederholen!\n"
        "🌐 <i>Die Quest-Storys sind vorerst auf Russisch — weitere Sprachpakete folgen.</i>\n\n"
        "👇 <b>Wähl eine Story:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} Min. · 🏆 +{reward} Münzen für den ersten Sieg\n"
        "..................................................\n\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Quest abgeschlossen, Belohnung abgeholt. Wiederhole sie, so oft du willst!</i>",
    "quest.card_progress": "⏯ <i>Du hast einen unvollendeten Durchlauf.</i>",
    "quest.card_new": "🆕 <i>Diese Story hast du noch nicht gespielt.</i>",
    "quest.btn_start": "▶️ QUEST STARTEN",
    "quest.btn_restart": "🔄 NEU STARTEN",
    "quest.btn_resume": "⏯ FORTSETZEN",
    "quest.btn_list": "🗺️ Zur Quest-Liste",
    "quest.btn_replay": "🔄 Noch mal spielen",
    "quest.win_first": "\n\n🏆 <b>QUEST ABGESCHLOSSEN! Belohnung: +{coins} Münzen.</b>",
    "quest.win_repeat": "\n\n✅ <b>Erneut geschafft!</b> Die Belohnung für diese Quest wurde schon früher abgeholt.",
    "quest.fail_footer": "\n\n💀 <i>Nicht das beste Ende... aber du kannst die Story jederzeit neu spielen!</i>",
    "quest.stale": "⏳ Diese Szene liegt schon hinter dir — weiter geht's an der aktuellen Stelle!",
    "quest.no_coins": "❌ Nicht genug Münzen für den Hinweis ({cost}). Schau auf deiner Farm vorbei!",
    "quest.not_found": "❌ Quest nicht gefunden.",
    "menu.btn_quests": "🗺️ QUESTS",

    # ---------------- Farm ----------------
    "farm.btn_bonus": "🎁 BONUS ABHOLEN (Frikadelle/24 Std.)",
    "farm.btn_load1": "🥩 1 Frikadelle tanken",
    "farm.btn_loadall": "⚡ ALLE Frikadellen tanken",
    "farm.btn_shop": "🏪 Zum Shop",
    "farm.status_all_fueled": "🟢 Alle Cyber-Bohrer sind aufgetankt und schürfen Münzen!",
    "farm.status_partial": "🟡 {fueled} von {total} Cyber-Bohrern aufgetankt. Der Rest wartet auf Frikadellen im Kühlschrank!",
    "farm.status_no_fuel": "🔴 Die Cyber-Bohrer stehen still! Zu wenig Treibstoff im Kühlschrank.",
    "farm.status_no_drills": "💡 Hol dir Cyber-Bohrer im /shop und steigere dein Einkommen.",
    "farm.boost_nuclear": "🔋 Nuklear-Boost x5 bis {until} UTC (Frikadellen-Verbrauch ×3)",
    "farm.boost_nitrogen": "❄️ Stickstoff-Kühlung +40% bis {until} UTC",
    "farm.boost_drone": "🛸 Master-Drohne verlängert das Roboterleben bis {until} UTC",
    "farm.no_boosts": "Keine aktiven Boosts — schau im /shop vorbei.",
    "farm.burnout": "🔥 Nächster Roboter-Ablauf: <b>{until} UTC</b>\n",
    "farm.dashboard": (
        "🚜 <b>ROFL HUB ZENTRALER TREIBSTOFF-HUB</b>\n"
        "..................................................\n\n"
        "🤖 Aktive Roboter in der Fabrik: <b>{total}</b>\n"
        "• Miner-Bots ({junior_rate} Münzen/Std.): <code>{junior}</code>\n"
        "• Cyber-Bohrer ({premium_rate} Münzen/Std.): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>AKTUELLES TEMPO DEINER FARM:</b>\n"
        "• Ertrag pro Stunde: <b>+{speed_hour} Münzen</b>\n"
        "• Ertrag pro Tag: <b>+{speed_day} Münzen</b>\n\n"
        "⚡ <b>BOOSTS:</b>\n{boosts}\n\n"
        "📋 <b>STATUS DER SPIELFABRIK:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>STATUS DES AUTOMATISCHEN KÜHLSCHRANKS:</b>\n"
        "🥩 Treibstoffvorrat: <b>{fridge} / {capacity}</b>\n"
        "💼 Frikadellen im Lager: <code>{inv}</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Wichtig: Roboter leben 30 Tage (die Master-Drohne pausiert den Verschleiß). "
        "JEDER Cyber-Bohrer verbraucht pro 24 Stunden Arbeit SEINE eigene ganze Frikadelle aus dem "
        "Kühlschrank: 3 Roboter — 3 Frikadellen pro Tag. Behalte den Tank im Blick!</i>"
    ),
    "farm.bonus_ok": "🎁 Cyber-Frikadelle wurde ins Lager gelegt! Komm in 24 Stunden wieder.",
    "farm.bonus_wait": "⏳ Bonus schon abgeholt! Nächste Frikadelle in {hours} Std. {minutes} Min.",
    "farm.no_inv_cutlets": "❌ Keine Cyber-Frikadellen im Lager! Kauf welche im /shop",
    "farm.fridge_full": "📦 Dein Kühlschrank ist schon komplett voll!",

    # ---------------- Profil ----------------
    "profile.caption": (
        "📋 <b>ROFL HUB SPIELER-DASHBOARD</b>\n"
        "..................................................\n\n"
        "🆔 Deine Pass-ID: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Münzen aktuell: <b>{balance} Münzen</b>\n"
        "🏆 Dein Status: <b>{team}</b>\n"
        "🧠 Intelligenz-Level: <b>{level}</b> · bis Level {next_level}: "
        "<b>{left}</b> richtige Antworten im /quiz (Belohnung: +{reward} Münzen)\n\n"
        "..................................................\n"
        "<i>Hier siehst du, was du gerade besitzt. Nutze die Buttons, um in andere Bereiche zu springen!</i>"
    ),
    "profile.no_team": "Kein Team",
    "profile.team_label": "Team",
    "profile.clan_label": "Clan",
    "profile.btn_farm": "🚜 Meine Cyber-Farm",
    "profile.btn_shop": "🏪 Shop",
    "profile.stats": (
        "📊 <b>SPIEL-STATISTIK DEINER ERFOLGE (30 TAGE)</b>\n"
        "..................................................\n\n"
        "🧠 Spiel-Intelligenz-Level: <b>{level}</b> (richtige Antworten gesamt: {total})\n"
        "🎮 Gespielte Duell-Runden: <b>{played}</b>\n"
        "🏆 Errungene Siege: <code>{won}</code>\n"
        "👥 Eingeladene aktive Freunde: <b>{refs}</b>\n\n"
        "..................................................\n"
        "<i>Die Statistik bewahrt deine historischen Erfolge — auch wenn die gewonnenen Münzen schon im Shop ausgegeben wurden!</i>"
    ),
    "img.passport": "PASS-ID: {user_id}",
    "img.owner": "ANFÜHRER: @{username}",
    "img.balance": "Kontostand: {balance} Münzen",
    "img.fridge": "Im Kühlschrank: {fridge} / {capacity}",
    "img.inv": "Frikadellen im Lager: {inv}",
    "img.junior": "Miner-Bots: {count}",
    "img.premium": "Cyber-Bohrer: {count}",

    # ---------------- Spiele: Engine ----------------
    "games.win": "🎉 <b>SIEG!</b> 🎉\nMünzen gutgeschrieben: <b>+{reward}</b>",
    "games.lose": "💀 <b>NIEDERLAGE!</b>\nMünzen abgebucht: <b>-{penalty}</b>",
    "games.draw": "🤝 <b>UNENTSCHIEDEN!</b>\nMünzen abgebucht: <b>-{penalty}</b>",
    "games.limit": (
        "🛑 <b>Tageslimit erreicht!</b>\n\n"
        "Im Spiel {game} hast du heute schon {limit} Siege geholt. Das Limit wird um 00:00 UTC zurückgesetzt.\n\n"
        "⚡ Limit aufheben: 24 Stunden — 5 ★, 30 Tage — 99 ★ (Bereich „Gaming“ im /shop)."
    ),
    "games.no_coins": "❌ Du hast 0 Münzen — damit kannst du die Rundengebühr nicht zahlen. Hol dir dein Farm-Einkommen in /farm!",
    "games.balance": "💰 Kontostand: <b>{balance} Münzen</b>",
    "games.btn_retry": "🎮 Noch mal spielen!",
    "games.btn_hub": "🕹️ Spielzone",
    "games.level_up": (
        "🏅 <b>INTELLIGENZ-LEVEL GESTIEGEN: {level}!</b> Belohnung: <b>+{bonus} Münzen</b>!\n"
        "Nächstes Level: {next_required} richtige Antworten → +{next_reward} Münzen."
    ),
    "games.name.rps": "Schere-Stein-Papier",
    "games.name.hl": "Höher/Tiefer",
    "games.name.quiz": "Quiz",
    "games.name.coin": "Kopf/Zahl",
    "games.name.dice": "Würfel",
    "games.name.safe": "Tresor",

    # ---------------- SSP ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>SCHERE-STEIN-PAPIER</b>\n\n"
        "Sieg: <b>+{reward}</b> · Niederlage/Unentschieden: <b>-{penalty}</b>\n"
        "Tageslimit an Siegen: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Stein",
    "rps.scissors": "✂️ Schere",
    "rps.paper": "🧻 Papier",
    "rps.draw": "🤝 <b>Unentschieden!</b> Beide haben {bot} gewählt.",
    "rps.win": "🏆 <b>Sieg!</b> {user} schlägt {bot}.",
    "rps.lose": "💀 <b>Der Bot hat gewonnen.</b> {bot} schlägt {user}.",

    # ---------------- Höher/Tiefer ----------------
    "hl.intro": (
        "🎲 <b>HÖHER ODER TIEFER</b>\n\nDer Bot hat eine Zahl vorgelegt: <b>{base}</b>.\n"
        "Ist die versteckte Zahl höher oder tiefer?\n"
        "Sieg: <b>+{reward}</b> · Niederlage: <b>-{penalty}</b> · Limit: <b>{limit}</b> Siege"
    ),
    "hl.btn_up": "📈 Höher",
    "hl.btn_down": "📉 Tiefer",
    "hl.result": "🎲 <b>RUNDENERGEBNIS</b>\n\nZahl des Bots: <b>{base}</b> · Versteckt: <b>{secret}</b>",

    # ---------------- Quiz ----------------
    "quiz.round": (
        "🧠 <b>QUIZ • {category}</b>\n"
        "🤔 FRAGE: <b>{question}</b>\n\n"
        "<i>🌐 Die Fragen sind vorerst auf Russisch — weitere Sprachpakete folgen bald!</i>"
    ),
    "quiz.btn_new": "🧠 Neue Frage",
    "quiz.timeout": "⌛ <b>ZEIT ABGELAUFEN!</b> ⌛\nRichtige Antwort: <b>{correct}</b>",
    "quiz.stale": "⏳ Diese Frage ist nicht mehr aktiv. Starte eine neue!",
    "quiz.stale_alert": "Diese Frage ist nicht mehr aktiv. Starte eine neue!",
    "quiz.empty": "⚠️ Die Fragen-Datenbank ist leer. Sag dem Administrator Bescheid.",
    "quiz.wrong": "❌ <b>Falsch</b> ❌\nRichtige Antwort: <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} Münze</b> für die Niederlage!",
    "quiz.level_line": (
        "🧠 Intelligenz-Level: <b>{level}</b>\n"
        "Bis Level {next_level} fehlen noch <b>{left}</b> Siege"
    ),
    "quiz.rules": (
        "<i>{seconds} Sekunden pro Antwort!\n"
        "Richtig: +{win} Münzen aufs Konto\n"
        "Falsch / zu langsam: -{penalty} Münze\n"
        "Limit: {limit} Siege pro Tag</i>"
    ),

    # ---------------- Kopf/Zahl ----------------
    "coin.intro": (
        "🪙 <b>KOPF ODER ZAHL</b>\n\n"
        "Der Bot wirft eine Cyber-Münze. Rate, auf welcher Seite sie landet!\n"
        "Sieg: <b>+{reward}</b> · Niederlage: <b>-{penalty}</b> · Limit: <b>{limit}</b> Siege"
    ),
    "coin.heads": "🦅 Kopf",
    "coin.tails": "🪙 Zahl",
    "coin.result": "🪙 Die Münze dreht sich... es ist <b>{result}</b>! Dein Tipp: {choice}.",

    # ---------------- Würfel ----------------
    "dice.intro": (
        "🎲 <b>WÜRFEL</b>\n\n"
        "Du und der Bot werft je einen Würfel. Wer mehr Punkte hat, holt die Runde!\n"
        "Sieg: <b>+{reward}</b> · Niederlage/Unentschieden: <b>-{penalty}</b> · Limit: <b>{limit}</b> Siege"
    ),
    "dice.btn_roll": "🎲 WÜRFEL WERFEN",
    "dice.toast": "Würfel geworfen!",
    "dice.result": "🎲 Dein Würfel (der erste): <b>{player}</b> · Würfel des Bots: <b>{bot}</b>",

    # ---------------- Tresor ----------------
    "safe.intro": (
        "🔐 <b>CYBER-TRESOR</b>\n\n"
        "Drinnen wartet ein Jackpot von <b>{jackpot} Münzen</b>! Die Tür ist mit einem Code von 1 bis {codes} gesichert. "
        "Du hast einen Versuch.\n"
        "Geknackt: <b>+{jackpot}</b> · Alarm: <b>-{penalty}</b> · Limit: <b>{limit}</b> Siege"
    ),
    "safe.btn_retry": "🔐 Noch mal knacken!",
    "safe.win": "🔓 <b>Tresor geknackt!</b> Der Code war: <b>{code}</b>.",
    "safe.lose": "🚨 <b>Alarm ausgelöst!</b> Du hast {guess} getippt, der Code war: <b>{code}</b>.",

    # ---------------- Duelle ----------------
    "duel.intro": (
        "⚔️ <b>1-GEGEN-1-DUELLE: SCHERE-STEIN-PAPIER UM DEN EINSATZ</b>\n"
        "..................................................\n\n"
        "Wähl einen Tisch, der zu deinem Budget passt — wie beim Poker. Der Einsatz wird sofort abgebucht, "
        "dein Gegner ist ein echter ROFL-HUB-Spieler!\n\n"
        "💰 Der Pot = beide Einsätze. Der Sieger bekommt <b>{payout_percent}%</b> des Pots, "
        "<b>{burn_percent}%</b> verbrennen für immer (Deflation!).\n"
        "🤝 Unentschieden — sofortige Wiederholung der Zeichen, der Pot bleibt auf dem Tisch.\n"
        "⏱ Pro Zeichen hast du <b>{move_timeout} Sekunden</b>; wer schweigt, für den wählt der Zufallsgenerator.\n"
        "🏆 Duellsiege zählen für dein Team in den Schlachten!\n\n"
        "👇 <b>WÄHL EINEN TISCH:</b>"
    ),
    "duel.btn_table": "⚔️ Tisch {stake} Münzen",
    "duel.btn_cancel": "❌ Tisch verlassen (Einsatz zurück)",
    "duel.btn_move_rock": "🪨 Stein",
    "duel.btn_move_scissors": "✂️ Schere",
    "duel.btn_move_paper": "🧻 Papier",
    "duel.waiting": (
        "🪑 <b>Du sitzt am {stake}-Münzen-Tisch.</b> Dein Einsatz ist im Pot.\n"
        "Wir warten auf den zweiten Kämpfer... Sobald er Platz nimmt, bekommt ihr beide die Zeichenwahl!\n"
        "<i>Die Warteschlange bleibt {ttl} Minuten offen, danach kommt dein Einsatz automatisch zurück.</i>"
    ),
    "duel.cancelled": "🚪 Du hast den Tisch verlassen. Der Einsatz von <b>{stake} Münzen</b> ist zurück auf deinem Konto.",
    "duel.expired": "⌛ Am Tisch {stake} hat sich kein Gegner gefunden. Dein Einsatz von <b>{stake} Münzen</b> wurde erstattet.",
    "duel.matched": (
        "⚔️ <b>GEGNER GEFUNDEN! Tisch {stake} Münzen.</b>\n"
        "Pot: <b>{bank} Münzen</b> · Für den Sieger: <b>{payout}</b>\n\n"
        "⏱ Du hast <b>{timeout} Sekunden</b> für dein Zeichen!"
    ),
    "duel.move_saved": "✊ Zeichen gespeichert! Wir warten auf das Zeichen des Gegners...",
    "duel.draw_replay": (
        "🤝 <b>UNENTSCHIEDEN! Runde {round}.</b> Beide haben dasselbe Zeichen gezeigt.\n"
        "Der Pot bleibt auf dem Tisch. ⏱ Wieder {timeout} Sekunden — wähl dein Zeichen:"
    ),
    "duel.win": (
        "🏆 <b>DAS DUELL GEHÖRT DIR!</b>\n\n"
        "Dein Zeichen {winner_move} schlägt {loser_move}.\n"
        "💰 Gewinn: <b>+{payout} Münzen</b> · 🔥 Im Pot verbrannt: {burned}\n"
        "💼 Kontostand: <b>{balance} Münzen</b>"
    ),
    "duel.lose": (
        "💀 <b>DUELL VERLOREN.</b>\n\n"
        "{winner_move} des Gegners schlägt dein Zeichen {loser_move}.\n"
        "📉 Dein Einsatz von <b>{stake} Münzen</b> ging in den Pot des Siegers.\n"
        "Revanche?"
    ),
    "duel.reaper_prefix": "⏰ <b>Runden-Timeout!</b> Die fehlenden Zeichen hat der Zufallsgenerator gewählt.\n\n",
    "duel.bad_table": "❌ Diesen Tisch gibt es nicht.",
    "duel.already_in": "⚠️ Du sitzt schon an einem Tisch oder steckst im Kampf! Beende erst dein aktuelles Duell.",
    "duel.no_coins": "❌ Für diesen Tisch brauchst du {stake} Münzen auf dem Konto.",
    "duel.cancel_impossible": "⚠️ Diese Warteschlange lässt sich nicht mehr abbrechen (Gegner gefunden oder Tisch geschlossen).",
    "duel.not_active": "⌛ Dieses Duell ist schon vorbei.",
    "duel.not_participant": "🔒 Das ist nicht dein Duell!",
    "duel.move_already": "✋ Du hast dein Zeichen in dieser Runde schon gezeigt. Wir warten auf den Gegner!",
    "duel.bad_move": "❌ Unbekanntes Zeichen.",
    "duel.btn_rematch": "⚔️ Revanche (zu den Tischen)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",

    # ---------------- Einladungsprogramm ----------------
    "ref.text": (
        "🤝 <b>ROFL HUB EINLADUNGSPROGRAMM</b>\n"
        "..................................................\n\n"
        "Lade Freunde ein und erhalte <b>+{bonus} Münzen</b> für jeden, "
        "der sich über deinen persönlichen Link registriert!\n\n"
        "🔗 <b>Dein Link (zum Kopieren antippen):</b>\n<code>{link}</code>\n\n"
        "📊 <b>DEINE STATISTIK:</b>\n"
        "👥 Eingeladene Freunde: <b>{invited}</b>\n"
        "💰 Mit Einladungen verdient: <b>{earned} Münzen</b>\n\n"
        "..................................................\n"
        "<i>Teile den Link im Klassenchat, mit Freunden und auf Social Media — je größer die Crew, desto schneller wächst dein Kontostand!</i>"
    ),
    "ref.btn_share": "📣 Link teilen",
    "ref.share_text": "Komm ins Spiele-Ökosystem von ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Doppelte Belohnung:</b> Wenn ein eingeladener Freund {rounds} "
                           "Runden spielt, bekommst du weitere <b>+{bonus} Münzen</b>!"),
    "ref.qualified_notify": ("🤝 <b>Dein Freund ist am Ball: schon {rounds} Runden!</b>\n"
                             "Du hast <b>+{bonus} Münzen</b> für einen qualifizierten Freund "
                             "erhalten. Lade noch mehr ein!"),

    # ---------------- Überweisungen ----------------
    "tr.help": (
        "🔄 <b>MÜNZEN AN ANDERE SPIELER SENDEN</b>\n"
        "..................................................\n\n"
        "Befehlsformat:\n"
        "<code>/transfer ID Betrag</code> — per Pass-ID (siehe /profile)\n"
        "<code>/transfer @username Betrag</code> — per Username\n"
        "<code>/transfer ROFL-HUB-777 Betrag</code> — per Auktions-VIP-ID\n\n"
        "Beispiele:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Mindestbetrag: <b>{min} Münzen</b>"
    ),
    "tr.not_found": "❌ Empfänger nicht gefunden. Prüfe die Pass-ID oder den @username — der Spieler muss im Bot registriert sein.",
    "tr.self": "🤨 Münzen an dich selbst senden geht nicht — das wäre ein Perpetuum mobile der Wirtschaft!",
    "tr.blocked": "🚫 Dieser Spieler ist gesperrt — Überweisungen an ihn sind nicht möglich.",
    "tr.min": "❌ Der Mindestbetrag für eine Überweisung ist {min} Münzen.",
    "tr.insufficient": "❌ Nicht genug Münzen! Dein Kontostand: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Nicht genug Münzen auf dem Konto.",
    "tr.confirm": (
        "🔄 <b>BESTÄTIGE DIE ÜBERWEISUNG:</b>\n\n"
        "👤 Empfänger: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Abzubuchender Betrag: <b>{amount} Münzen</b>{fee_line}\n"
        "💰 Der Empfänger erhält: <b>{received} Münzen</b>\n\n"
        "<i>Überweisungen lassen sich nicht rückgängig machen — prüfe den Empfänger!</i>"
    ),
    "tr.fee_line": "\n🔥 Hub-Gebühr: <b>{fee} Münzen</b> (verbrennt)",
    "tr.btn_confirm": "✅ ÜBERWEISUNG BESTÄTIGEN",
    "tr.btn_cancel": "❌ Abbrechen",
    "tr.cancelled_toast": "Überweisung abgebrochen",
    "tr.cancelled": "❌ <b>Überweisung abgebrochen.</b> Deine Münzen sind noch da.",
    "tr.not_yours": "🔒 Das ist nicht deine Überweisung!",
    "tr.done_toast": "✅ Überweisung ausgeführt!",
    "tr.done": (
        "✅ <b>ÜBERWEISUNG AUSGEFÜHRT!</b>\n\n"
        "💸 Gesendet: <b>{amount} Münzen</b> an Spieler-ID <code>{recipient_id}</code>\n"
        "💰 Dein Kontostand: <b>{balance} Münzen</b>"
    ),
    "tr.received": (
        "💰 <b>Du hast {amount} Münzen erhalten!</b>\n"
        "Absender: ID <code>{sender_id}</code>. Dein Konto ist schon aufgefüllt — check /profile!"
    ),

    # ---------------- Shop & Zahlungen ----------------
    "shop.header": "🏪 <b>ROFL HUB SHOP</b>\nKäufe laufen über offizielle Telegram Stars. Wähl unten eine Kategorie.",
    "shop.cat_farm": (
        "🚜 <b>SHOP · FÜR DIE FARM</b>\n"
        "..................................................\n"
        "Roboter für 30 Tage, Treibstoff, Kühlschränke, Boosts und die Master-Drohne.\n"
        "📦 Dein Kühlschrank fasst aktuell: <b>{capacity} Frikadellen</b>\n"
        "..................................................\n"
        "👇 <b>Wähl einen Artikel:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>SHOP · GAMING</b>\n"
        "..................................................\n"
        "Sieglimit-Aufhebung, Münzpakete und die Mega-Clan-Lizenz.\n"
        "..................................................\n"
        "👇 <b>Wähl einen Artikel:</b>"
    ),
    "pay.invoice_desc": "Sofortige Lieferung von ROFL-HUB-Ingame-Inhalten.",
    "pay.invoice_error": "⚠️ Die Telegram-Stars-Rechnung konnte nicht erstellt werden. Versuch es später noch mal.",
    "pay.success": "🎉 <b>Zahlung bestätigt!</b>\n🧾 <code>{charge}</code>\n💵 Abgebucht: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 Die Zahlung war erfolgreich, aber die Lieferung hat vorerst nicht geklappt. Wir kümmern uns schon darum.\n"
        "Bewahre die Zahlungsnummer auf: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Deine Stars wurden automatisch erstattet.",
    "pay.keep_charge": "Bewahre die Zahlungsnummer für die Erstattung auf: <code>{charge}</code>",
    "pay.already": "✅ Diese Zahlung wurde schon verarbeitet, der Artikel wurde bereits geliefert.",
    "pay.support": (
        "🛟 <b>SUPPORT FÜR TELEGRAM-STARS-ZAHLUNGEN</b>\n"
        "..................................................\n\n"
        "Alle ROFL-HUB-Artikel sind digital und werden sofort nach der Zahlung geliefert.\n\n"
        "⚙️ <b>Wenn du bezahlt hast, aber der Artikel nicht angekommen ist:</b>\n"
        "Der Bot erstattet Stars automatisch, wenn die Lieferung fehlschlägt. Falls das nicht passiert ist, "
        "schick hier deine Zahlungsnummer (steht auf dem Beleg, Format <code>xxxx...</code>) und beschreibe das Problem. "
        "Die Administration prüft die Zahlung in der Datenbank und klärt den Fall innerhalb von 24 Stunden.\n\n"
        "💫 <b>Erstattungsrichtlinie:</b>\n"
        "Eine Erstattung ist möglich, wenn der Artikel nicht angekommen ist oder fehlerhaft geliefert wurde. "
        "Korrekt gelieferte digitale Artikel sind von der Erstattung ausgeschlossen.\n\n"
        "..................................................\n"
        "<i>Dieser Bereich ist die offizielle Support-Stelle für Käufe nach den Telegram-Regeln.</i>"
    ),

    # ---------------- Lieferung ----------------
    "dlv.cutlets": "🥩 Zum Lager hinzugefügt: <b>{qty} Frikadellen</b>.",
    "dlv.miner": "🤖 Roboter <b>„{name}“</b> wurde auf deine Farm geliefert.\n⏳ Laufzeit: bis <b>{until} UTC</b>.",
    "dlv.miner_junior": "Miner-Bot",
    "dlv.miner_premium": "Cyber-Bohrer",
    "dlv.fridge": "📦 Kühlschrank auf <b>{capacity} Frikadellen</b> erweitert.",
    "dlv.coins": "💰 Gutgeschrieben: <b>+{amount} Münzen</b>.",
    "dlv.boost_nuclear": "🔋 Nuklear-Boost x5 aktiv bis <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Stickstoff-Kühlung +40% aktiv bis <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Die Master-Drohne bewacht deine Farm bis <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Sieglimits aufgehoben bis <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Dein Team hat den Status <b>MEGA-CLAN</b> erhalten: bis zu {max} Plätze.",
    "dlv.err_fridge": "Du hast schon einen Kühlschrank dieser Größe oder größer.",
    "dlv.err_no_team": "Du hast noch kein Team. Erstelle zuerst eins mit /create_team.",
    "dlv.err_mega": "Dein Team hat den Mega-Clan-Status bereits.",

    # ---------------- Teams/Clans (Hauptoberflächen) ----------------
    "clan.no_team": "⚠️ <b>Du hast noch kein eigenes Team!</b>\n\nDu kannst deine eigene Crew sofort registrieren — tippe auf den Button unten.",
    "clan.btn_create": "🏆 Team für 100k erstellen",
    "clan.btn_members": "👥 TEAMMATE-LISTE",
    "clan.btn_leave": "🚪 Team verlassen / Crew aufgeben",
    "clan.btn_dashboard": "🏆 Team-Dashboard",
    "clan.status_clan": "👑 STATUS: IMPERIUMS-CLAN",
    "clan.status_team": "👥 STATUS: NORMALES TEAM",
    "clan.dashboard": (
        "🏆 <b>INFO-DASHBOARD DEINES TEAMS</b>\n"
        "..................................................\n\n"
        "📌 Name: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Crew-Captain: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Motto: <i>„{motto}“</i>\n"
        "🔮 Emblem-Symbol: {symbol}\n\n"
        "👥 Mitglieder: <b>{members} / {max_members}</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVIGATION:</b>"
    ),
    "clan.members_only": "🔒 Die Mitgliederliste sehen nur Mitglieder dieses Teams!",
    "clan.members_gone": "❌ Dieses Team wurde schon aufgelöst.",
    "clan.members_header": (
        "👥 <b>KADER DES TEAMS „{name}“</b>\n"
        "🧠 — Spiel-Intelligenz-Level (nur im /quiz trainierbar)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
        "📄 Seite <b>{page} / {pages}</b> · Kämpfer gesamt: <b>{members}</b>\n"
        "<i>Tippe auf den @username eines Teammates, um ihm zu schreiben, euren eigenen Chat aufzubauen "
        "und die Crew zu Team-Wettkämpfen zu rufen!</i>"
    ),
    "clan.btn_prev": "⬅️ Zurück",
    "clan.btn_next": "Weiter ➡️",
    "clan.join_ok": (
        "🎉 <b>GLÜCKWUNSCH, DU BIST DABEI!</b>\n\nDu bist dem Team <b>{name}</b> beigetreten!\n"
        "📍 Tippe /my_team, um den Kader zu checken!"
    ),
    "clan.leave_ok": "🚪 Du hast das Team <b>{name}</b> verlassen. Jetzt bist du frei wie ein Vogel!",
}

MINIAPP = {
    "subtitle": "dein Spiele-Imperium auf einem Screen",
    "passport": "📋 SPIELER-PASS", "coins": "Münzen",
    "brain": "🧠 Intelligenz-Level", "toNext": "bis Level {n}: {left} richtige Quiz-Antworten (+{reward} Münzen)",
    "farm": "🚜 CYBER-FARM", "robots": "Roboter (Miner / Bohrer)",
    "fueled": "Bohrer aufgetankt", "speed": "Schürf-Tempo",
    "perHour": "{v} Münzen/Std.", "fridge": "Kühlschrank", "inv": "Frikadellen im Lager",
    "burnout": "Nächster Ablauf", "boosts": "Aktive Boosts", "none": "keine",
    "bonusReady": "🎁 TÄGLICHE FRIKADELLE ABHOLEN",
    "bonusWait": "⏳ Bonus in {h} Std. {m} Min.", "bonusDone": "🎉 Frikadelle im Lager!",
    "team": "🏆 MEIN TEAM", "clan": "CLAN", "teamLabel": "Team", "captain": "👑 Du hast das Kommando!",
    "members": "Kader", "noTeam": "Noch kein Team — stell deine Crew im Bot-Chat zusammen!",
    "top": "👑 TOP-100 DER REICHSTEN SPIELER",
    "shop": "🏪 SHOP", "shopFarm": "🚜 FÜR DIE FARM", "shopGames": "🕹️ GAMING",
    "shopHint": "Bezahlung mit offiziellen Telegram Stars — direkt hier, mit einem Tap.",
    "paid": "🎉 Bezahlt! Der Artikel ist schon auf deinem Account.",
    "payFail": "Die Zahlung hat nicht geklappt. Versuch es noch mal.",
    "oldClient": "Aktualisiere Telegram, um in der Mini App zu kaufen, oder öffne den Shop im Bot-Chat.",
    "ctaNoRobots": "💤 Deine Farm ist leer! Hol dir deinen ersten Roboter — Münzen fließen rund um die Uhr.",
    "ctaHungry": "🚨 Die Bohrer hungern ({n} ohne Treibstoff) — das Schürfen steht still!",
    "ctaLowFuel": "⚠️ Weniger Frikadellen als für einen Tag Bohrer-Arbeit.",
    "ctaShopBtn": "🛒 Zum Shop",
    "footer": "Volle Kontrolle — im Bot-Chat: /menu",
    "noProfile": "Profil nicht gefunden. Öffne den Bot und tippe /start!",
    "blocked": "Account von der Administration gesperrt.",
    "error": "Daten konnten nicht geladen werden. Versuch es später noch mal.",
    "outside": "Öffne diese App über den Telegram-Bot von ROFL HUB.",
}

COMMANDS = {
    "app": "🎮 Mini App öffnen",
    "menu": "📱 Hauptmenü",
    "profile": "👤 Mein Profil & Pass",
    "farm": "🚜 Cyber-Farm & Auftanken",
    "shop": "🏪 Shop (Telegram Stars)",
    "games": "🕹️ Alle Spiele gegen den Bot",
    "quiz": "🧠 Quiz: 15 Sekunden pro Antwort",
    "duel": "⚔️ 1-gegen-1-Duell um den Einsatz",
    "quests": "🗺️ Quests: Storys mit Entscheidungen",
    "my_team": "🏆 Mein Team & Teammates",
    "invite": "🤝 Einladungslink: +1000 pro Freund",
    "transfer": "🔄 Münzen an Spieler senden",
    "my_stats": "📊 Meine Statistik",
    "faq": "📚 Häufige Fragen",
    "rules": "📜 Nutzungsvereinbarung",
    "paysupport": "🛟 Zahlungs-Support",
}
