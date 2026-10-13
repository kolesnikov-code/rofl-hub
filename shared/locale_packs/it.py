"""Итальянская (Italiano) локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> monete
# Младший Майнер -> Robo-Minatore
# Кибер-Бурильщик -> Cyber-Trivella (кратко: Trivella)
# кибер-котлета -> cyber-cotoletta (кратко: cotoletta)
# Холодильник -> Frigo
# склад (инвентарь) -> inventario
# ферма -> fattoria; Кибер-Ферма -> Cyber-Fattoria
# Ядерный Разгон x5 -> Boost Nucleare x5
# Азотное Охлаждение +40% -> Raffreddamento ad Azoto +40%
# Мастер-дрон -> Master Drone
# Кибер-Сейф -> Cyber-Cassaforte (игра «Сейф» -> Cassaforte)
# Мега-Клан -> Mega-Clan
# Безлимит / снятие лимитов -> rimozione dei limiti
# дуэли -> duelli; ставка -> puntata; банк -> piatto; стол -> tavolo; жест -> mossa
# битвы -> battaglie
# квесты -> quest (le quest)
# уровень интеллекта -> livello di intelligenza
# КНБ -> Morra Cinese (Sasso / Forbici / Carta)

BUTTONS = {
    "main_menu": "📱 MENU PRINCIPALE",
    "profile": "👤 IL MIO PROFILO",
    "farm": "🚜 LA MIA FATTORIA",
    "games_zone": "🕹️ ZONA GIOCHI",
    "teams": "🏆 SQUADRE E CLAN",
    "shop": "🏪 NEGOZIO",
    "shop_cat_farm": "🚜 PER LA FATTORIA",
    "shop_cat_games": "🕹️ GAMING",
}

STRINGS = {
    # ---------------- общее ----------------
    "common.no_profile": "⚠️ Profilo non trovato. Premi /start per registrarti.",
    "common.btn_menu": "💿 Menu Principale",
    "common.blocked": "🚫 Il tuo account è stato bloccato dall'amministrazione di ROFL HUB.",
    "common.feature_off": "⚙️ Questa sezione è in manutenzione. Torna un po' più tardi!",
    "common.maintenance": "🛠 ROFL HUB è in rapida manutenzione. Torniamo presto — le tue monete e i tuoi progressi sono al sicuro!",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Che bello rivederti, @{username}!</b>\nI tuoi progressi sono al sicuro. Il pannello di navigazione è in fondo allo schermo.",
    "start.btn_continue": "🛸 CONTINUA",
    "start.btn_cutlet": "Cos'è una cyber-cotoletta?🥩🤔",
    "start.btn_fight": "Dimmi tutto e poi in BATTAGLIA!",
    "start.console": "🚀 <b>Console di comando attivata! Usa i pulsanti in fondo allo schermo.</b>",
    "start.intro1": (
        "👋 <b>Ciao! Sono ROFL HUB BOT, il bot principale dell'ecosistema di gioco ROFL HUB. "
        "Un hub di divertimento e conoscenza di nuova generazione!</b>\n\n"
        "<b>Qui puoi:</b>\n"
        "🎮 Giocare ai giochi chat-bot contro il bot e altri giocatori\n"
        "💸 Ottenere valuta di gioco con le vittorie o avviare una fattoria che la estrae 24 ore su 24\n"
        "🤼 Creare una squadra e volare in cima alla classifica\n"
        "🏆 Trasformare la squadra in un clan e lottare nella classifica internazionale\n"
        "💰 Vincere un jackpot da un milione di monete insieme alla tua banda\n"
        "👑 Comprare una pubblicazione in prima pagina sui social o sul sito per farti conoscere o promuovere il tuo blog\n\n"
        "<b>Questo chat-bot sa:</b>\n"
        "🎮 Mostrare la lista di tutti i giochi, canali e siti di ROFL HUB\n"
        "⚡ Accreditare monete nei giochi, nelle battaglie di squadre e clan, per obiettivi, attività e referral\n"
        "🔄 Trasferire monete di gioco a un altro giocatore di ROFL HUB\n"
        "💎 Vendere pubblicazioni sul sito e posti VIP per personaggi e blogger\n"
        "🚀 Vendere potenziamenti, titoli, status e molto altro...\n\n"
        "<i>Premi “CONTINUA” e ti racconto di più 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>ECCO LE TUE PRIME RICOMPENSE DI REGISTRAZIONE!</b>\n"
        "..................................................\n"
        "💸 Hai ricevuto: <b>{balance} monete</b>\n"
        "🥩 Hai ricevuto: <b>{cutlets} cyber-cotoletta</b>\n"
        "..................................................\n"
        "È il tuo bonus di benvenuto per l'ingresso nel club ROFL HUB.\n\n"
        "🔒 <i>Il bonus viene dato una sola volta, al momento della registrazione.</i>\n\n"
        "Le monete si possono spendere in tanti modi: sono la base dell'economia dell'hub. Custodiscile bene...\n\n"
        "⁉️ <b>Ma di sicuro ti stai chiedendo:</b> cos'è questa cotoletta? A chi devo darla da mangiare?"
    ),
    "start.intro3": (
        "<b>PRIMA DI TUTTO: PERCHÉ LE MONETE DI GIOCO SONO COSÌ IMPORTANTI?</b>\n\n"
        "Le monete sono la base di tutti gli scambi, le gare e gli acquisti in <b>ROFL HUB</b>. "
        "È quasi l'unica valuta di gioco al mondo che puoi estrarre gratis!\n"
        "..................................................\n"
        "<b>Puoi farlo in tanti modi:</b>\n"
        "- Invitare gli amici con il tuo link d'invito\n"
        "- Vincere nei giochi contro il bot\n"
        "- Vincere i duelli contro altri giocatori\n"
        "- Partecipare alle battaglie di squadre e clan\n"
        "- Ritirare il bonus dell'accesso giornaliero e completare le missioni\n"
        "- Prenderti un robot che estrae monete 24 ore su 24 (Robo-Minatore / Cyber-Trivella)\n"
        "..................................................\n"
        "<b>Se hai un robot di secondo livello (la Cyber-Trivella), va nutrito ogni giorno. "
        "Ed è qui che entra in gioco la cyber-cotoletta: il carburante per l'estrazione automatica, "
        "distribuito gratis ogni giorno! Il tuo compito è semplice: passare e dare da mangiare al robot.</b>\n\n"
        "Se non lo nutri in tempo, il robot si scarica e l'estrazione si ferma.\n\n"
        "Il Robo-Minatore (primo livello) non ha bisogno di carburante. "
        "Importante! Ogni robot si compra per 30 giorni: poi va ricomprato, oppure ti serve un Master Drone. "
        "Capirai tutto strada facendo:) Non distraiamoci.\n\n"
        "Voglio raccontarti ancora un po' di <b>ROFL HUB</b>, così capisci come funziona tutto qui.\n\n"
        "🛑 <b>Questo è l'ultimo messaggio di presentazione. Poi si va dritti in battaglia:)</b>"
    ),
    "start.intro4": (
        "<b>IN BREVISSIMO. ROFL HUB È:</b>\n"
        "- Giochi chat-bot per tutti i gusti\n"
        "- La possibilità di creare una squadra (fino a 50 persone)\n"
        "- La possibilità di trasformarla in un clan (fino a 1000 persone)\n"
        "- Battaglie di squadre e clan con premi\n"
        "- Il canale di divertimento e conoscenza ROFL HUB CHANNEL\n"
        "- La pagina Instagram — rofl_hub_global\n"
        "- Il sito rofl-hub.com per chiacchierare e promuoversi senza registrazione\n"
        "- Migliaia di giocatori in tutto il mondo, tra cui i tuoi futuri amici!\n"
        "..................................................\n"
        "<b>Come promesso, questo è il messaggio finale. Ora in battaglia! Comandi utili:</b>\n\n"
        "/menu — controllo rapido delle funzioni\n"
        "/games — lista di tutti i giochi\n"
        "/faq — domande frequenti\n"
        "/rules — accordo utente\n"
    ),

    # ---------------- меню и игровая зона ----------------
    "menu.text": (
        "📱 <b>MENU PRINCIPALE DELL'ECOSISTEMA ROFL HUB</b>\n"
        "..................................................\n\n"
        "👤 <b>PROFILO PERSONALE E PASSAPORTO:</b>\n"
        "• /start — Inizia la presentazione e registra l'account\n"
        "• /profile — Il tuo passaporto, saldo e squadra in tempo reale\n"
        "• /my_stats — Le tue statistiche storiche degli ultimi 30 giorni\n\n"
        "🚜 <b>CYBER-FATTORIA E AUTOMAZIONE:</b>\n"
        "• /farm — Hub del carburante: rifornimento e velocità dei robot\n"
        "• /shop — Marketplace: acquisto di minatori, cotolette e potenziamenti dell'hub\n\n"
        "🕹️ <b>SALA GIOCHI:</b>\n"
        "• /games — Hub inline di tutti i giochi contro il bot\n"
        "• /quiz — Quiz a tempo: 15 secondi per rispondere, livelli e bonus\n"
        "• /duel — DUELLI 1 contro 1 con giocatori veri: tavoli 10/100/1000\n"
        "• /quests — QUEST: gialli, commedie e rompicapi con ricompense\n"
        "• /rps, /high_low, /coin, /dice, /safe — Giochi rapidi a monete\n\n"
        "👥 <b>GESTIONE DELLA BANDA:</b>\n"
        "• /create_team — Registra la tua squadra per 100.000 monete\n"
        "• /my_team — Dashboard della banda e LISTA COMPAGNI con livelli 🧠\n"
        "• /all_teams — Roulette di squadre casuali\n\n"
        "💸 <b>SOLDI E AMICI:</b>\n"
        "• /invite — Il tuo link d'invito: +1000 monete per ogni amico\n"
        "• /transfer — Trasferisci monete a un altro giocatore\n\n"
        "📚 <b>GUIDA E REGOLE:</b>\n"
        "• /faq — La guida completa dell'ecosistema (si apre nella Mini App)\n"
        "• /rules — Accordo utente\n"
        "..................................................\n"
        "<i>⚙️ Usa il pannello di gioco fisso a due colonne in fondo allo schermo per una navigazione istantanea tra le sezioni!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>TI DIAMO IL BENVENUTO NELLA ZONA GIOCHI DI ROFL HUB!</b>\n"
        "..................................................\n\n"
        "Qui puoi sfidare il bot in duelli rapidi o affrontare lo sprint-test "
        "d'intelligenza per fare il colpo grosso... o bruciare il saldo!\n\n"
        "💸 Una vittoria paga: <b>+2 monete</b> (Cyber-Cassaforte: <b>+5</b>)\n"
        "💀 Una sconfitta o un pareggio costa: <b>-1 moneta</b>\n"
        "🧠 Il Quiz ha un timer di 15 secondi e livelli di intelligenza: il 1º livello si chiude con 10 risposte esatte e vale <b>+100 monete</b>, "
        "ogni livello successivo è più lungo di 10 risposte, ma la ricompensa cresce di 100!\n\n"
        "..................................................\n"
        "👇 <b>TOCCA UN PULSANTE QUI SOTTO PER INIZIARE SUBITO UN ROUND:</b>"
    ),
    "menu.btn_quiz": "🧠 Quiz",
    "menu.btn_rps": "🪨 Morra Cinese",
    "menu.btn_hl": "📈 Alto/Basso",
    "menu.btn_coin": "🪙 Testa o Croce",
    "menu.btn_dice": "🎲 Dadi",
    "menu.btn_safe": "🔐 Cyber-Cassaforte",
    "menu.btn_duel": "⚔️ DUELLI 1 contro 1",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Passaporto, fattoria, squadra e la top dei più ricchi — su un unico schermo al neon. "
        "E puoi ritirare la cotoletta giornaliera direttamente da lì!\n\n"
        "👇 Premi il pulsante:"
    ),
    "app.btn": "🎮 APRI LA MINI APP",
    "app.unavailable": "⚙️ La Mini App si sta ancora collegando ai server dell'ecosistema. Riprova tra poco!",
    "faq.teaser": (
        "📚 <b>GUIDA DELL'ECOSISTEMA ROFL HUB</b>\n"
        "..................................................\n\n"
        "L'essenziale in breve:\n"
        "🚜 I robot estraggono monete 24 ore su 24: il Robo-Minatore — 5/h senza carburante, "
        "la Cyber-Trivella — 10/h, e OGNI Trivella mangia la sua cyber-cotoletta al giorno. "
        "Tutti i robot vivono 30 giorni (il Master Drone mette in pausa l'usura).\n"
        "🧠 Quiz: 15 secondi per rispondere, livelli di intelligenza con ricompense crescenti.\n"
        "⚔️ Duelli con giocatori veri ai tavoli da 10/100/1000 monete.\n"
        "🏆 Squadre fino a 50 combattenti (Mega-Clan — fino a 1000) e Battaglie-evento con premi per tutti.\n\n"
        "..................................................\n"
        "👇 <b>La guida completa con tutte le meccaniche — a un tocco da qui:</b>"
    ),
    "faq.btn_open": "📖 APRI LA GUIDA COMPLETA",
    "rules.teaser": (
        "📜 <b>ACCORDO UTENTE DI ROFL HUB</b>\n"
        "..................................................\n\n"
        "L'essenziale in due parole:\n"
        "🪙 Le monete e tutti gli oggetti di gioco sono elementi virtuali di intrattenimento: "
        "non sono denaro e non si scambiano con fondi reali.\n"
        "💫 Gli acquisti passano solo dalle Telegram Stars ufficiali; gli articoli digitali vengono "
        "consegnati all'istante e, se la consegna fallisce, le Stars tornano automaticamente.\n"
        "🛡️ Non raccogliamo numeri di telefono, posizione né dati personali.\n"
        "🤝 Vietati insulti, trucchi per gonfiare i punteggi e i multi-account: chi viola rischia il blocco.\n\n"
        "..................................................\n"
        "👇 <b>Il testo completo dell'accordo e la liberatoria — a un tocco da qui:</b>\n"
        "<i>⚖️ Usando il bot confermi di accettare le condizioni.</i>"
    ),
    "rules.btn_open": "📜 APRI L'ACCORDO COMPLETO",
    "quest.list_header": (
        "🗺️ <b>QUEST DI ROFL HUB</b>\n"
        "..................................................\n\n"
        "Storie interattive con scelte e bivi: gialli, commedie, rompicapi. "
        "La prima vittoria in ogni quest paga monete e puoi rigiocare quante volte vuoi!\n"
        "🌐 <i>Per ora le storie delle quest sono in russo — la versione tradotta è in arrivo.</i>\n\n"
        "👇 <b>Scegli una storia:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} monete per la prima vittoria\n"
        "..................................................\n\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Quest completata, ricompensa ritirata. Rigioca quanto ti pare!</i>",
    "quest.card_progress": "⏯ <i>Hai una partita lasciata a metà.</i>",
    "quest.card_new": "🆕 <i>Non hai ancora iniziato questa storia.</i>",
    "quest.btn_start": "▶️ INIZIA LA QUEST",
    "quest.btn_restart": "🔄 RICOMINCIA",
    "quest.btn_resume": "⏯ CONTINUA",
    "quest.btn_list": "🗺️ Alla lista delle quest",
    "quest.btn_replay": "🔄 Gioca di nuovo",
    "quest.win_first": "\n\n🏆 <b>QUEST COMPLETATA! Ricompensa: +{coins} monete.</b>",
    "quest.win_repeat": "\n\n✅ <b>Completata di nuovo!</b> La ricompensa di questa quest era già stata ritirata.",
    "quest.fail_footer": "\n\n💀 <i>Non proprio il miglior finale... ma puoi sempre rigiocare la storia!</i>",
    "quest.stale": "⏳ Quella scena è già alle spalle — si continua dal punto attuale!",
    "quest.no_coins": "❌ Non hai abbastanza monete per l'indizio ({cost}). Passa dalla fattoria!",
    "quest.not_found": "❌ Quest non trovata.",
    "menu.btn_quests": "🗺️ QUEST",

    # ---------------- ферма ----------------
    "farm.btn_bonus": "🎁 RITIRA IL BONUS (cotoletta ogni 24 h)",
    "farm.btn_load1": "🥩 Carica 1 cotoletta",
    "farm.btn_loadall": "⚡ Carica TUTTE",
    "farm.btn_shop": "🏪 Vai al Negozio",
    "farm.status_all_fueled": "🟢 Tutte le Cyber-Trivelle sono rifornite e stanno estraendo monete!",
    "farm.status_partial": "🟡 Rifornite {fueled} Cyber-Trivelle su {total}. Le altre aspettano le cotolette nel frigo!",
    "farm.status_no_fuel": "🔴 Le Cyber-Trivelle si sono fermate! Non c'è abbastanza carburante nel frigo.",
    "farm.status_no_drills": "💡 Prenditi delle Cyber-Trivelle in /shop per aumentare le entrate.",
    "farm.boost_nuclear": "🔋 Boost Nucleare x5 fino a {until} UTC (consumo cotolette ×3)",
    "farm.boost_nitrogen": "❄️ Raffreddamento ad Azoto +40% fino a {until} UTC",
    "farm.boost_drone": "🛸 Il Master Drone prolunga la vita dei robot fino a {until} UTC",
    "farm.no_boosts": "Nessun boost attivo — dai un'occhiata a /shop.",
    "farm.burnout": "🔥 Prossimo robot a esaurirsi: <b>{until} UTC</b>\n",
    "farm.dashboard": (
        "🚜 <b>HUB CENTRALE DEL CARBURANTE ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Robot attivi in fabbrica: <b>{total}</b>\n"
        "• Robo-Minatori ({junior_rate} monete/h): <code>{junior}</code>\n"
        "• Cyber-Trivelle ({premium_rate} monete/h): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VELOCITÀ ATTUALE DELLA TUA FATTORIA:</b>\n"
        "• Produzione all'ora: <b>+{speed_hour} monete</b>\n"
        "• Produzione al giorno: <b>+{speed_day} monete</b>\n\n"
        "⚡ <b>BOOST:</b>\n{boosts}\n\n"
        "📋 <b>STATO DELLA FABBRICA DI GIOCO:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>STATO DEL FRIGO AUTOMATICO:</b>\n"
        "🥩 Scorta di carburante: <b>{fridge} / {capacity}</b>\n"
        "💼 Cotolette nell'inventario: <code>{inv}</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Importante: i robot vivono 30 giorni (il Master Drone mette in pausa l'usura). "
        "OGNI Cyber-Trivella consuma la SUA cotoletta intera dal frigo ogni "
        "24 ore di lavoro: 3 robot — 3 cotolette al giorno. Tieni d'occhio il rifornimento!</i>"
    ),
    "farm.bonus_ok": "🎁 Cyber-cotoletta aggiunta all'inventario! Torna tra 24 ore.",
    "farm.bonus_wait": "⏳ Bonus già ritirato! Prossima cotoletta tra {hours} h {minutes} min.",
    "farm.no_inv_cutlets": "❌ Non hai cyber-cotolette nell'inventario! Comprale in /shop",
    "farm.fridge_full": "📦 Il tuo Frigo è già pieno zeppo!",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>PROFILO GIOCATORE ROFL HUB</b>\n"
        "..................................................\n\n"
        "🆔 Il tuo ID Passaporto: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Monete attuali: <b>{balance} monete</b>\n"
        "🏆 Il tuo status: <b>{team}</b>\n"
        "🧠 Livello di intelligenza: <b>{level}</b> · al livello {next_level}: "
        "<b>{left}</b> risposte esatte in /quiz (ricompensa: +{reward} monete)\n\n"
        "..................................................\n"
        "<i>Qui vedi ciò che possiedi in questo momento. Usa i pulsanti per volare nelle altre sezioni!</i>"
    ),
    "profile.no_team": "Nessuna squadra",
    "profile.team_label": "Squadra",
    "profile.clan_label": "Clan",
    "profile.btn_farm": "🚜 La mia Cyber-Fattoria",
    "profile.btn_shop": "🏪 Negozio",
    "profile.stats": (
        "📊 <b>STATISTICHE DI GIOCO E TRAGUARDI (30 GIORNI)</b>\n"
        "..................................................\n\n"
        "🧠 Livello di intelligenza di gioco: <b>{level}</b> (risposte esatte totali: {total})\n"
        "🎮 Round di duello giocati: <b>{played}</b>\n"
        "🏆 Vittorie conquistate: <code>{won}</code>\n"
        "👥 Amici attivi invitati: <b>{refs}</b>\n\n"
        "..................................................\n"
        "<i>Le statistiche conservano i tuoi meriti storici anche se le monete vinte sono già state spese al market!</i>"
    ),
    "img.passport": "ID PASSAPORTO: {user_id}",
    "img.owner": "CAPO: @{username}",
    "img.balance": "Saldo: {balance} monete",
    "img.fridge": "Nel frigo: {fridge} / {capacity}",
    "img.inv": "Cotolette nell'inventario: {inv}",
    "img.junior": "Robo-Minatori: {count}",
    "img.premium": "Cyber-Trivelle: {count}",

    # ---------------- игры: общий движок ----------------
    "games.win": "🎉 <b>VITTORIA!</b> 🎉\nMonete accreditate: <b>+{reward}</b>",
    "games.lose": "💀 <b>SCONFITTA!</b>\nMonete scalate: <b>-{penalty}</b>",
    "games.draw": "🤝 <b>PAREGGIO!</b>\nMonete scalate: <b>-{penalty}</b>",
    "games.limit": (
        "🛑 <b>Limite giornaliero raggiunto!</b>\n\n"
        "Nel gioco {game} hai già messo a segno {limit} vittorie per oggi. Il limite si azzera alle 00:00 UTC.\n\n"
        "⚡ Togli il limite per 24 ore — 5 ★, per 30 giorni — 99 ★ (sezione “Gaming” in /shop)."
    ),
    "games.no_coins": "❌ Hai 0 monete — non puoi pagare la quota del round. Riscuoti i guadagni della fattoria in /farm!",
    "games.balance": "💰 Saldo: <b>{balance} monete</b>",
    "games.btn_retry": "🎮 Gioca ancora!",
    "games.btn_hub": "🕹️ Zona giochi",
    "games.level_up": (
        "🏅 <b>LIVELLO DI INTELLIGENZA AUMENTATO: {level}!</b> Ricompensa: <b>+{bonus} monete</b>!\n"
        "Prossimo livello: {next_required} risposte esatte → +{next_reward} monete."
    ),
    "games.name.rps": "Morra Cinese",
    "games.name.hl": "Alto/Basso",
    "games.name.quiz": "Quiz",
    "games.name.coin": "Testa o Croce",
    "games.name.dice": "Dadi",
    "games.name.safe": "Cassaforte",

    # ---------------- КНБ ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>MORRA CINESE: SASSO-FORBICI-CARTA</b>\n\n"
        "Vittoria: <b>+{reward}</b> · Sconfitta/pareggio: <b>-{penalty}</b>\n"
        "Limite di vittorie al giorno: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Sasso",
    "rps.scissors": "✂️ Forbici",
    "rps.paper": "🧻 Carta",
    "rps.draw": "🤝 <b>Pareggio!</b> Entrambi avete scelto {bot}.",
    "rps.win": "🏆 <b>Vittoria!</b> {user} batte {bot}.",
    "rps.lose": "💀 <b>Ha vinto il bot.</b> {bot} batte {user}.",

    # ---------------- Больше/Меньше ----------------
    "hl.intro": (
        "🎲 <b>ALTO O BASSO</b>\n\nIl bot ha fissato il numero: <b>{base}</b>.\n"
        "Il numero nascosto sarà più alto o più basso?\n"
        "Vittoria: <b>+{reward}</b> · Sconfitta: <b>-{penalty}</b> · Limite: <b>{limit}</b> vittorie"
    ),
    "hl.btn_up": "📈 Più alto",
    "hl.btn_down": "📉 Più basso",
    "hl.result": "🎲 <b>RISULTATO DEL ROUND</b>\n\nNumero del bot: <b>{base}</b> · Nascosto: <b>{secret}</b>",

    # ---------------- викторина ----------------
    "quiz.round": (
        "🧠 <b>QUIZ • {category}</b>\n"
        "🤔 DOMANDA: <b>{question}</b>\n\n"
        "<i>🌐 Per ora le domande sono in russo — il pacchetto italiano è in arrivo!</i>"
    ),
    "quiz.btn_new": "🧠 Nuova domanda",
    "quiz.timeout": "⌛ <b>TEMPO SCADUTO!</b> ⌛\nRisposta esatta: <b>{correct}</b>",
    "quiz.stale": "⏳ Questa domanda non è più attiva. Lanciane una nuova!",
    "quiz.stale_alert": "Questa domanda non è più attiva. Lanciane una nuova!",
    "quiz.empty": "⚠️ Il database delle domande è vuoto. Avvisa l'amministratore.",
    "quiz.wrong": "❌ <b>Sbagliato</b> ❌\nRisposta esatta: <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} moneta</b> per la sconfitta!",
    "quiz.level_line": (
        "🧠 Livello di intelligenza: <b>{level}</b>\n"
        "Vittorie mancanti al livello {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} secondi per rispondere!\n"
        "Risposta esatta: +{win} monete sul saldo\n"
        "Errore / tempo scaduto: -{penalty} moneta\n"
        "Limite: {limit} vittorie al giorno</i>"
    ),

    # ---------------- Орёл/Решка ----------------
    "coin.intro": (
        "🪙 <b>TESTA O CROCE</b>\n\n"
        "Il bot lancia una cyber-moneta. Indovina su quale lato cadrà!\n"
        "Vittoria: <b>+{reward}</b> · Sconfitta: <b>-{penalty}</b> · Limite: <b>{limit}</b> vittorie"
    ),
    "coin.heads": "🦅 Testa",
    "coin.tails": "🪙 Croce",
    "coin.result": "🪙 La moneta gira... è uscita <b>{result}</b>! La tua puntata: {choice}.",

    # ---------------- Кубики ----------------
    "dice.intro": (
        "🎲 <b>DADI</b>\n\n"
        "Tu e il bot lanciate un dado a testa. Chi fa più punti si prende il round!\n"
        "Vittoria: <b>+{reward}</b> · Sconfitta/pareggio: <b>-{penalty}</b> · Limite: <b>{limit}</b> vittorie"
    ),
    "dice.btn_roll": "🎲 LANCIA I DADI",
    "dice.toast": "Dadi lanciati!",
    "dice.result": "🎲 Il tuo dado (il primo): <b>{player}</b> · Dado del bot: <b>{bot}</b>",

    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>CYBER-CASSAFORTE</b>\n\n"
        "Dentro c'è un jackpot da <b>{jackpot} monete</b>! Lo sportello è bloccato da un codice da 1 a {codes}. "
        "Hai un solo tentativo.\n"
        "Scassinata: <b>+{jackpot}</b> · Allarme: <b>-{penalty}</b> · Limite: <b>{limit}</b> vittorie"
    ),
    "safe.btn_retry": "🔐 Scassina ancora!",
    "safe.win": "🔓 <b>Cassaforte aperta!</b> Il codice era: <b>{code}</b>.",
    "safe.lose": "🚨 <b>È scattato l'allarme!</b> Hai digitato {guess}, ma il codice era: <b>{code}</b>.",

    # ---------------- дуэли ----------------
    "duel.intro": (
        "⚔️ <b>DUELLI 1 CONTRO 1: MORRA CINESE CON PUNTATA</b>\n"
        "..................................................\n\n"
        "Scegli il tavolo adatto alle tue tasche, come nel poker. La puntata viene prelevata subito "
        "e l'avversario è un giocatore vero di ROFL HUB!\n\n"
        "💰 Il piatto = le due puntate. Il vincitore prende l'<b>{payout_percent}%</b> del piatto, "
        "il <b>{burn_percent}%</b> brucia per sempre (deflazione!).\n"
        "🤝 Pareggio: si rigiocano subito le mosse, il piatto resta sul tavolo.\n"
        "⏱ Per la mossa hai <b>{move_timeout} secondi</b>; chi tace si becca una mossa scelta dal generatore casuale.\n"
        "🏆 Le vittorie nei duelli contano per la tua squadra nelle Battaglie!\n\n"
        "👇 <b>SCEGLI UN TAVOLO:</b>"
    ),
    "duel.btn_table": "⚔️ Tavolo {stake} monete",
    "duel.btn_cancel": "❌ Lascia il tavolo (rimborso)",
    "duel.btn_move_rock": "🪨 Sasso",
    "duel.btn_move_scissors": "✂️ Forbici",
    "duel.btn_move_paper": "🧻 Carta",
    "duel.waiting": (
        "🪑 <b>Sei al tavolo da {stake} monete.</b> La puntata è nel piatto.\n"
        "Aspettiamo il secondo sfidante... Appena si siede, a entrambi comparirà la scelta della mossa!\n"
        "<i>La coda dura {ttl} minuti, poi la puntata torna automaticamente.</i>"
    ),
    "duel.cancelled": "🚪 Hai lasciato il tavolo. La puntata di <b>{stake} monete</b> è tornata sul saldo.",
    "duel.expired": "⌛ Nessun avversario si è presentato al tavolo da {stake}. La puntata di <b>{stake} monete</b> è stata rimborsata.",
    "duel.matched": (
        "⚔️ <b>AVVERSARIO TROVATO! Tavolo da {stake} monete.</b>\n"
        "Piatto: <b>{bank} monete</b> · Al vincitore: <b>{payout}</b>\n\n"
        "⏱ Hai <b>{timeout} secondi</b> per scegliere la mossa!"
    ),
    "duel.move_saved": "✊ Mossa registrata! Aspettiamo la mossa dell'avversario...",
    "duel.draw_replay": (
        "🤝 <b>PAREGGIO! Round {round}.</b> Avete mostrato la stessa mossa.\n"
        "Il piatto resta sul tavolo. ⏱ Di nuovo {timeout} secondi — scegli la mossa:"
    ),
    "duel.win": (
        "🏆 <b>IL DUELLO È TUO!</b>\n\n"
        "La tua mossa {winner_move} batte {loser_move}.\n"
        "💰 Vincita: <b>+{payout} monete</b> · 🔥 Bruciate dal piatto: {burned}\n"
        "💼 Saldo: <b>{balance} monete</b>"
    ),
    "duel.lose": (
        "💀 <b>DUELLO PERSO.</b>\n\n"
        "La mossa {winner_move} dell'avversario batte la tua {loser_move}.\n"
        "📉 La puntata di <b>{stake} monete</b> è finita nel piatto del vincitore.\n"
        "Rivincita?"
    ),
    "duel.reaper_prefix": "⏰ <b>Tempo scaduto per il round!</b> Le mosse mancanti le ha scelte il generatore casuale.\n\n",
    "duel.bad_table": "❌ Questo tavolo non esiste.",
    "duel.already_in": "⚠️ Sei già a un tavolo o nel bel mezzo di un duello! Prima finisci quello in corso.",
    "duel.no_coins": "❌ Per questo tavolo servono {stake} monete sul saldo.",
    "duel.cancel_impossible": "⚠️ Questa coda non si può più annullare (avversario trovato o tavolo chiuso).",
    "duel.not_active": "⌛ Questo duello è già finito.",
    "duel.not_participant": "🔒 Questo non è il tuo duello!",
    "duel.move_already": "✋ Hai già mostrato la mossa in questo round. Aspettiamo l'avversario!",
    "duel.bad_move": "❌ Mossa sconosciuta.",
    "duel.btn_rematch": "⚔️ Rivincita (ai tavoli)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>PROGRAMMA REFERRAL DI ROFL HUB</b>\n"
        "..................................................\n\n"
        "Invita gli amici e ricevi <b>+{bonus} monete</b> per ognuno "
        "che si registra con il tuo link personale!\n\n"
        "🔗 <b>Il tuo link (tocca per copiarlo):</b>\n<code>{link}</code>\n\n"
        "📊 <b>LE TUE STATISTICHE:</b>\n"
        "👥 Amici invitati: <b>{invited}</b>\n"
        "💰 Guadagnato dai referral: <b>{earned} monete</b>\n\n"
        "..................................................\n"
        "<i>Manda il link nelle chat di classe, agli amici e sui social: più grande è la banda, più in fretta cresce il tuo saldo!</i>"
    ),
    "ref.btn_share": "📣 Condividi il link",
    "ref.share_text": "Entra nell'ecosistema di gioco ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Ricompensa doppia:</b> quando un amico invitato gioca {rounds} "
                           "round, ricevi altre <b>+{bonus} monete</b>!"),
    "ref.qualified_notify": ("🤝 <b>Il tuo amico ci ha preso gusto: già {rounds} round!</b>\n"
                             "Hai guadagnato <b>+{bonus} monete</b> per un invitato qualificato. "
                             "Invitane altri!"),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>TRASFERIMENTO DI MONETE A UN ALTRO GIOCATORE</b>\n"
        "..................................................\n\n"
        "Formato del comando:\n"
        "<code>/transfer ID importo</code> — per ID Passaporto (lo vedi in /profile)\n"
        "<code>/transfer @username importo</code> — per username\n"
        "<code>/transfer ROFL-HUB-777 importo</code> — per VIP ID d'asta\n\n"
        "Esempi:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Importo minimo: <b>{min} monete</b>"
    ),
    "tr.not_found": "❌ Destinatario non trovato. Controlla l'ID Passaporto o lo @username — il giocatore deve essere registrato nel bot.",
    "tr.self": "🤨 Non puoi trasferire monete al tuo stesso account — sarebbe il moto perpetuo dell'economia!",
    "tr.blocked": "🚫 Questo giocatore è bloccato — i trasferimenti verso questo account non sono disponibili.",
    "tr.min": "❌ L'importo minimo del trasferimento è di {min} monete.",
    "tr.insufficient": "❌ Monete insufficienti! Il tuo saldo: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Monete insufficienti sul saldo.",
    "tr.confirm": (
        "🔄 <b>CONFERMA IL TRASFERIMENTO:</b>\n\n"
        "👤 Destinatario: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Importo prelevato: <b>{amount} monete</b>{fee_line}\n"
        "💰 Il destinatario riceverà: <b>{received} monete</b>\n\n"
        "<i>I trasferimenti non si possono annullare — controlla bene il destinatario!</i>"
    ),
    "tr.fee_line": "\n🔥 Commissione dell'hub: <b>{fee} monete</b> (bruciate)",
    "tr.btn_confirm": "✅ CONFERMA TRASFERIMENTO",
    "tr.btn_cancel": "❌ Annulla",
    "tr.cancelled_toast": "Trasferimento annullato",
    "tr.cancelled": "❌ <b>Trasferimento annullato.</b> Le monete sono rimaste al loro posto.",
    "tr.not_yours": "🔒 Questo non è il tuo trasferimento!",
    "tr.done_toast": "✅ Trasferimento eseguito!",
    "tr.done": (
        "✅ <b>TRASFERIMENTO ESEGUITO!</b>\n\n"
        "💸 Inviate: <b>{amount} monete</b> al giocatore ID <code>{recipient_id}</code>\n"
        "💰 Il tuo saldo: <b>{balance} monete</b>"
    ),
    "tr.received": (
        "💰 <b>Hai ricevuto {amount} monete!</b>\n"
        "Mittente: ID <code>{sender_id}</code>. Il saldo è già stato aggiornato — controlla /profile!"
    ),

    # ---------------- магазин и платежи ----------------
    "shop.header": "🏪 <b>NEGOZIO ROFL HUB</b>\nGli acquisti passano dalle Telegram Stars ufficiali. Scegli una categoria con i pulsanti in basso.",
    "shop.cat_farm": (
        "🚜 <b>NEGOZIO · PER LA FATTORIA</b>\n"
        "..................................................\n"
        "Robot per 30 giorni, carburante, frigo, boost e il Master Drone.\n"
        "📦 Il tuo frigo attuale: <b>{capacity} cotolette</b>\n"
        "..................................................\n"
        "👇 <b>Scegli un articolo:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>NEGOZIO · GAMING</b>\n"
        "..................................................\n"
        "Rimozione dei limiti di vittorie, pacchetti di monete e la licenza Mega-Clan.\n"
        "..................................................\n"
        "👇 <b>Scegli un articolo:</b>"
    ),
    "pay.invoice_desc": "Consegna istantanea di contenuti di gioco ROFL HUB.",
    "pay.invoice_error": "⚠️ Impossibile creare la fattura Telegram Stars. Riprova più tardi.",
    "pay.success": "🎉 <b>Pagamento confermato!</b>\n🧾 <code>{charge}</code>\n💵 Addebitate: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 Il pagamento è andato a buon fine, ma la consegna è temporaneamente fallita. Ce ne stiamo già occupando.\n"
        "Conserva il numero del pagamento: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Le Stars sono state rimborsate automaticamente sul tuo conto.",
    "pay.keep_charge": "Conserva il numero del pagamento per il rimborso: <code>{charge}</code>",
    "pay.already": "✅ Questo pagamento era già stato elaborato, l'articolo è stato consegnato in precedenza.",
    "pay.support": (
        "🛟 <b>SUPPORTO PAGAMENTI TELEGRAM STARS</b>\n"
        "..................................................\n\n"
        "Tutti gli articoli di ROFL HUB sono digitali e vengono consegnati subito dopo il pagamento.\n\n"
        "⚙️ <b>Se hai pagato ma l'articolo non è arrivato:</b>\n"
        "il bot rimborsa le Stars automaticamente quando la consegna fallisce. Se non è successo, "
        "manda qui il numero del pagamento (è nella ricevuta, formato <code>xxxx...</code>) e descrivi il problema. "
        "L'amministrazione controllerà il pagamento nel database e risolverà la questione entro 24 ore.\n\n"
        "💫 <b>Politica dei rimborsi:</b>\n"
        "il rimborso è possibile se l'articolo non è stato ricevuto o è stato consegnato con un errore. "
        "Gli articoli digitali consegnati correttamente non sono rimborsabili.\n\n"
        "..................................................\n"
        "<i>Questa sezione è il punto ufficiale di supporto agli acquisti secondo le regole di Telegram.</i>"
    ),

    # ---------------- доставка ----------------
    "dlv.cutlets": "🥩 Aggiunte all'inventario: <b>{qty} cotolette</b>.",
    "dlv.miner": "🤖 Il robot <b>“{name}”</b> è stato consegnato alla tua fattoria.\n⏳ In servizio fino a <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robo-Minatore",
    "dlv.miner_premium": "Cyber-Trivella",
    "dlv.fridge": "📦 Frigo ampliato a <b>{capacity} cotolette</b>.",
    "dlv.coins": "💰 Accreditate <b>+{amount} monete</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nucleare x5 attivo fino a <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Raffreddamento ad Azoto +40% attivo fino a <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Il Master Drone sorveglia la fattoria fino a <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limiti di vittorie rimossi fino a <b>{until} UTC</b>.",
    "dlv.clan": "🏆 La squadra ha ottenuto lo status <b>MEGA-CLAN</b>: fino a {max} posti.",
    "dlv.err_fridge": "Hai già un frigo di questa capienza o più grande.",
    "dlv.err_no_team": "Non hai ancora creato una squadra. Prima creala con /create_team.",
    "dlv.err_mega": "La tua squadra ha già lo status di Mega-Clan.",

    # ---------------- команды/кланы (основные поверхности) ----------------
    "clan.no_team": "⚠️ <b>Non hai ancora una squadra!</b>\n\nPuoi registrare la tua banda personale proprio ora, toccando il pulsante qui sotto.",
    "clan.btn_create": "🏆 Crea una Squadra per 100k",
    "clan.btn_members": "👥 LISTA COMPAGNI",
    "clan.btn_leave": "🚪 Lascia la squadra / Molla la banda",
    "clan.btn_dashboard": "🏆 Dashboard della squadra",
    "clan.status_clan": "👑 STATUS: CLAN DELL'IMPERO",
    "clan.status_team": "👥 STATUS: SQUADRA NORMALE",
    "clan.dashboard": (
        "🏆 <b>DASHBOARD INFORMATIVA DELLA TUA SQUADRA</b>\n"
        "..................................................\n\n"
        "📌 Nome: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Capitano della banda: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Motto: <i>“{motto}”</i>\n"
        "🔮 Simbolo dell'emblema: {symbol}\n\n"
        "👥 Membri: <b>{members} / {max_members}</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVIGAZIONE:</b>"
    ),
    "clan.members_only": "🔒 La lista dei compagni è visibile solo ai membri di questa squadra!",
    "clan.members_gone": "❌ La squadra è già stata sciolta.",
    "clan.members_header": (
        "👥 <b>FORMAZIONE DELLA SQUADRA “{name}”</b>\n"
        "🧠 — livello di intelligenza di gioco (si allena solo in /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
        "📄 Pagina <b>{page} / {pages}</b> · Combattenti totali: <b>{members}</b>\n"
        "<i>Tocca lo @username di un compagno per scrivergli, creare la vostra chat "
        "e chiamare a raccolta la banda per le sfide di squadra!</i>"
    ),
    "clan.btn_prev": "⬅️ Indietro",
    "clan.btn_next": "Avanti ➡️",
    "clan.join_ok": (
        "🎉 <b>CONGRATULAZIONI, SEI IN GIOCO!</b>\n\nOra fai parte della squadra <b>{name}</b>!\n"
        "📍 Scrivi /my_team per controllare la formazione!"
    ),
    "clan.leave_ok": "🚪 Hai lasciato la squadra <b>{name}</b>. Ora sei uno spirito libero!",
}

MINIAPP = {
    "subtitle": "il tuo impero di gioco su un unico schermo",
    "passport": "📋 PASSAPORTO GIOCATORE",
    "coins": "monete",
    "brain": "🧠 Livello di intelligenza",
    "toNext": "al livello {n}: {left} risposte esatte nel quiz (+{reward} monete)",
    "farm": "🚜 CYBER-FATTORIA",
    "robots": "Robot (minatori / trivelle)",
    "fueled": "Trivelle rifornite",
    "speed": "Velocità di estrazione",
    "perHour": "{v} monete/ora",
    "fridge": "Frigo",
    "inv": "Cotolette nell'inventario",
    "burnout": "Prossimo esaurimento",
    "boosts": "Boost attivi",
    "none": "nessuno",
    "bonusReady": "🎁 RITIRA LA COTOLETTA GIORNALIERA",
    "bonusWait": "⏳ Bonus tra {h} h {m} min",
    "bonusDone": "🎉 Cotoletta aggiunta!",
    "team": "🏆 LA MIA SQUADRA",
    "clan": "CLAN",
    "teamLabel": "Squadra",
    "captain": "👑 Al comando ci sei tu!",
    "members": "Formazione",
    "noTeam": "Ancora nessuna squadra — raduna la tua banda nella chat del bot!",
    "top": "👑 TOP-100 DEI PIÙ RICCHI DELL'ECOSISTEMA",
    "shop": "🏪 NEGOZIO",
    "shopFarm": "🚜 PER LA FATTORIA",
    "shopGames": "🕹️ GAMING",
    "shopHint": "Paga con le Telegram Stars ufficiali — direttamente qui, in un tocco.",
    "paid": "🎉 Pagato! L'articolo è già sul tuo account.",
    "payFail": "Il pagamento non è andato a buon fine. Riprova.",
    "oldClient": "Aggiorna Telegram per comprare dalla Mini App, oppure apri il negozio nella chat del bot.",
    "ctaNoRobots": "💤 La fattoria è vuota! Prenditi il primo robot — le monete pioveranno 24 ore su 24.",
    "ctaHungry": "🚨 Le Trivelle hanno fame ({n} senza carburante) — l'estrazione è ferma!",
    "ctaLowFuel": "⚠️ Le cotolette non bastano per un giorno di lavoro delle Trivelle.",
    "ctaShopBtn": "🛒 Al negozio",
    "footer": "Controllo completo nella chat del bot: /menu",
    "noProfile": "Profilo non trovato. Apri il bot e premi /start!",
    "blocked": "Account bloccato dall'amministrazione.",
    "error": "Impossibile caricare i dati. Riprova più tardi.",
    "outside": "Apri questa app dal bot Telegram di ROFL HUB.",
}

COMMANDS = {
    "app": "🎮 Apri la Mini App",
    "menu": "📱 Menu principale",
    "profile": "👤 Il mio profilo e passaporto",
    "farm": "🚜 Cyber-Fattoria e rifornimento",
    "shop": "🏪 Negozio (Telegram Stars)",
    "games": "🕹️ Tutti i giochi contro il bot",
    "quiz": "🧠 Quiz: 15 secondi per rispondere",
    "duel": "⚔️ Duello 1 contro 1 con puntata",
    "quests": "🗺️ Quest: storie con scelte",
    "my_team": "🏆 La mia squadra e i compagni",
    "invite": "🤝 Link d'invito: +1000 per ogni amico",
    "transfer": "🔄 Trasferisci monete a un giocatore",
    "my_stats": "📊 Le mie statistiche",
    "faq": "📚 Domande frequenti",
    "rules": "📜 Accordo utente",
    "paysupport": "🛟 Supporto pagamenti",
}
