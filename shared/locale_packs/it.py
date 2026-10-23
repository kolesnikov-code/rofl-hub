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
# Больше/Меньше -> Alto/Basso
# ресурсы: Металл -> Metallo; Водород -> Idrogeno; Кристаллы -> Cristalli; Детали -> Componenti
# Мастерская -> Officina; Кибер-броня -> Cyber-Armatura; Шаттл -> Shuttle
# Налёт -> Incursione; Стойка обороны -> Posizione di difesa; Разведка -> Ricognizione
# Реванш -> Rivincita; Щит -> Scudo; Сундук -> Forziere; Серия -> Serie
# Станция команды -> Stazione della squadra; боец (член команды) -> combattente

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
        "💸 Hai ricevuto: <b>{balance} 🪙</b>\n"
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
        "• /rps, /high_low, /safe — Giochi rapidi a monete\n\n"
        "👥 <b>GESTIONE DELLA BANDA:</b>\n"
        "• /create_team — Registra la tua squadra per 100.000 🪙\n"
        "• /my_team — Dashboard della banda e LISTA COMPAGNI con livelli 🧠\n"
        "• /all_teams — Roulette di squadre casuali\n\n"
        "💸 <b>SOLDI E AMICI:</b>\n"
        "• /invite — Il tuo link d'invito: +1000 🪙 per ogni amico\n"
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
        "💸 Una vittoria paga: <b>+2 🪙</b> (Cyber-Cassaforte: <b>+5</b>)\n"
        "💀 Una sconfitta o un pareggio costa: <b>-1 🪙</b>\n"
        "🧠 Il Quiz ha un timer di 15 secondi e livelli di intelligenza: il 1º livello si chiude con 10 risposte esatte e vale <b>+100 🪙</b>, "
        "ogni livello successivo è più lungo di 10 risposte, ma la ricompensa cresce di 100!\n\n"
        "..................................................\n"
        "👇 <b>TOCCA UN PULSANTE QUI SOTTO PER INIZIARE SUBITO UN ROUND:</b>"
    ),
    "menu.btn_quiz": "🧠 Quiz",
    "menu.btn_rps": "🪨 Morra Cinese",
    "menu.btn_hl": "📈 Alto/Basso",
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
        "⚔️ Duelli con giocatori veri ai tavoli da 10/100/1000 🪙.\n"
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
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} 🪙 per la prima vittoria\n"
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
    "quest.win_first": "\n\n🏆 <b>QUEST COMPLETATA! Ricompensa: +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>Completata di nuovo!</b> La ricompensa di questa quest era già stata ritirata.",
    "quest.fail_footer": "\n\n💀 <i>Non proprio il miglior finale... ma puoi sempre rigiocare la storia!</i>",
    "quest.stale": "⏳ Quella scena è già alle spalle — si continua dal punto attuale!",
    "quest.no_coins": "❌ L'indizio costa {cost} 🪙 e il tuo saldo è più basso. Passa dalla fattoria!",
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
    "farm.status_no_drills": "💡 Prenditi un robot più potente in /shop: la fattoria estrarrà di più.",
    "farm.boost_nuclear": "🔋 Boost Nucleare x5 fino a {until} UTC (consumo cotolette ×3)",
    "farm.boost_nitrogen": "❄️ Raffreddamento ad Azoto +40% fino a {until} UTC",
    "farm.boost_drone": "🛸 Il Master Drone prolunga la vita dei robot fino a {until} UTC",
    "farm.no_boosts": "Nessun boost attivo — dai un'occhiata a /shop.",
    "farm.burnout": "🔥 Prossimo robot a esaurirsi: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Attiva il tuo Robot Stagista (gratis)",
    "farm.intern_activated": "🤖 Il tuo Robot Stagista è entrato in turno! +1 🪙 all'ora per sempre, senza carburante e senza scadenza.",
    "farm.intern_already": "🤖 Il tuo Robot Stagista sta già lavorando.",
    "farm.intern_line": "• Robot Stagisti ({rate} 🪙/h, eterni): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 Hai un Robot Stagista gratis! Premi il pulsante qui sotto: estrarrà 1 🪙 all'ora per sempre.",
    "farm.dashboard": (
        "🚜 <b>HUB CENTRALE DEL CARBURANTE ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Robot attivi in fabbrica: <b>{total}</b>\n"
        "{intern}• Robo-Minatori ({junior_rate} 🪙/h): <code>{junior}</code>\n"
        "• Cyber-Trivelle ({premium_rate} 🪙/h): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VELOCITÀ ATTUALE DELLA TUA FATTORIA:</b>\n"
        "• Produzione all'ora: <b>+{speed_hour} 🪙</b>\n"
        "• Produzione al giorno: <b>+{speed_day} 🪙</b>\n\n"
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
        "💰 Monete attuali: <b>{balance} 🪙</b>\n"
        "🏆 Il tuo status: <b>{team}</b>\n"
        "🧠 Livello di intelligenza: <b>{level}</b> · al livello {next_level}: "
        "<b>{left}</b> risposte esatte in /quiz (ricompensa: +{reward} 🪙)\n\n"
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
    "games.win": "🎉 <b>VITTORIA!</b> 🎉\nAccredito: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>SCONFITTA!</b>\nAddebito: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>PAREGGIO!</b>\nAddebito: <b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>Limite giornaliero raggiunto!</b>\n\n"
        "Nel gioco {game} hai già messo a segno {limit} vittorie per oggi. Il limite si azzera alle 00:00 UTC.\n\n"
        "⚡ Togli il limite per 24 ore — 5 ★, per 30 giorni — 99 ★ (sezione “Gaming” in /shop)."
    ),
    "games.no_coins": "❌ Hai 0 🪙 — non puoi pagare la quota del round. Riscuoti i guadagni della fattoria in /farm!",
    "games.balance": "💰 Saldo: <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 Gioca ancora!",
    "games.btn_hub": "🕹️ Zona giochi",
    "games.level_up": (
        "🏅 <b>LIVELLO DI INTELLIGENZA AUMENTATO: {level}!</b> Ricompensa: <b>+{bonus} 🪙</b>!\n"
        "Prossimo livello: {next_required} risposte esatte → +{next_reward} 🪙."
    ),
    "games.name.rps": "Morra Cinese",
    "games.intern_bonus": "🤖 Livello {level}! Un altro Robot Stagista è arrivato nella tua fattoria: ora ne hai {count}.",
    "games.name.hl": "Alto/Basso",
    "games.name.quiz": "Quiz",
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
    "quiz.lost_line": "💀 <b>-{penalty} 🪙</b> per la sconfitta!",
    "quiz.level_line": (
        "🧠 Livello di intelligenza: <b>{level}</b>\n"
        "Vittorie mancanti al livello {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} secondi per rispondere!\n"
        "Risposta esatta: +{win} 🪙 sul saldo\n"
        "Errore / tempo scaduto: -{penalty} 🪙\n"
        "Limite: {limit} vittorie al giorno</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>CYBER-CASSAFORTE</b>\n\n"
        "Dentro c'è un jackpot da <b>{jackpot} 🪙</b>! Lo sportello è bloccato da un codice da 1 a {codes}. "
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
    "duel.btn_table": "⚔️ Tavolo {stake} 🪙",
    "duel.btn_cancel": "❌ Lascia il tavolo (rimborso)",
    "duel.btn_move_rock": "🪨 Sasso",
    "duel.btn_move_scissors": "✂️ Forbici",
    "duel.btn_move_paper": "🧻 Carta",
    "duel.waiting": (
        "🪑 <b>Sei al tavolo da {stake} 🪙.</b> La puntata è nel piatto.\n"
        "Aspettiamo il secondo sfidante... Appena si siede, a entrambi comparirà la scelta della mossa!\n"
        "<i>La coda dura {ttl} minuti, poi la puntata torna automaticamente.</i>"
    ),
    "duel.cancelled": "🚪 Hai lasciato il tavolo. La puntata di <b>{stake} 🪙</b> è tornata sul saldo.",
    "duel.expired": "⌛ Nessun avversario si è presentato al tavolo da {stake}. La puntata di <b>{stake} 🪙</b> è stata rimborsata.",
    "duel.matched": (
        "⚔️ <b>AVVERSARIO TROVATO! Tavolo da {stake} 🪙.</b>\n"
        "Piatto: <b>{bank} 🪙</b> · Al vincitore: <b>{payout}</b>\n\n"
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
        "💰 Vincita: <b>+{payout} 🪙</b> · 🔥 Bruciate dal piatto: {burned}\n"
        "💼 Saldo: <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>DUELLO PERSO.</b>\n\n"
        "La mossa {winner_move} dell'avversario batte la tua {loser_move}.\n"
        "📉 La puntata di <b>{stake} 🪙</b> è finita nel piatto del vincitore.\n"
        "Rivincita?"
    ),
    "duel.reaper_prefix": "⏰ <b>Tempo scaduto per il round!</b> Le mosse mancanti le ha scelte il generatore casuale.\n\n",
    "duel.bad_table": "❌ Questo tavolo non esiste.",
    "duel.already_in": "⚠️ Sei già a un tavolo o nel bel mezzo di un duello! Prima finisci quello in corso.",
    "duel.no_coins": "❌ Per questo tavolo servono {stake} 🪙 sul saldo.",
    "duel.cancel_impossible": "⚠️ Questa coda non si può più annullare (avversario trovato o tavolo chiuso).",
    "duel.not_active": "⌛ Questo duello è già finito.",
    "duel.not_participant": "🔒 Questo non è il tuo duello!",
    "duel.move_already": "✋ Hai già mostrato la mossa in questo round. Aspettiamo l'avversario!",
    "duel.bad_move": "❌ Mossa sconosciuta.",
    "duel.btn_rematch": "⚔️ Rivincita (ai tavoli)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 Grado: <b>{rank}</b>\n",
    "rank.rookie": "Novellino",
    "rank.fighter": "Combattente",
    "rank.legend": "Leggenda",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.king": "KING",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>PROGRAMMA REFERRAL DI ROFL HUB</b>\n"
        "..................................................\n\n"
        "Invita gli amici e ricevi <b>+{bonus} 🪙</b> per ognuno "
        "che si registra con il tuo link personale!\n\n"
        "🔗 <b>Il tuo link (tocca per copiarlo):</b>\n<code>{link}</code>\n\n"
        "📊 <b>LE TUE STATISTICHE:</b>\n"
        "👥 Amici invitati: <b>{invited}</b>\n"
        "💰 Guadagnato dai referral: <b>{earned} 🪙</b>\n\n"
        "..................................................\n"
        "<i>Manda il link nelle chat di classe, agli amici e sui social: più grande è la banda, più in fretta cresce il tuo saldo!</i>"
    ),
    "ref.btn_share": "📣 Condividi il link",
    "ref.share_text": "Entra nell'ecosistema di gioco ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Ricompensa doppia:</b> quando un amico invitato gioca {rounds} "
                           "round, ricevi altre <b>+{bonus} 🪙</b> e <b>{cutlets} 🥩 cyber-cotoletta</b>!"),
    "ref.qualified_notify": ("🤝 <b>Il tuo amico ci ha preso gusto: già {rounds} round!</b>\n"
                             "Hai guadagnato <b>+{bonus} 🪙</b> e <b>{cutlets} 🥩 cyber-cotoletta</b> nell'inventario "
                             "per un invitato qualificato. "
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
        "📌 Importo minimo: <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ Destinatario non trovato. Controlla l'ID Passaporto o lo @username — il giocatore deve essere registrato nel bot.",
    "tr.self": "🤨 Non puoi trasferire monete al tuo stesso account — sarebbe il moto perpetuo dell'economia!",
    "tr.blocked": "🚫 Questo giocatore è bloccato — i trasferimenti verso questo account non sono disponibili.",
    "tr.min": "❌ L'importo minimo del trasferimento è di {min} 🪙.",
    "tr.insufficient": "❌ Monete insufficienti! Il tuo saldo: <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ Monete insufficienti sul saldo.",
    "tr.confirm": (
        "🔄 <b>CONFERMA IL TRASFERIMENTO:</b>\n\n"
        "👤 Destinatario: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Importo prelevato: <b>{amount} 🪙</b>{fee_line}\n"
        "💰 Il destinatario riceverà: <b>{received} 🪙</b>\n\n"
        "<i>I trasferimenti non si possono annullare — controlla bene il destinatario!</i>"
    ),
    "tr.fee_line": "\n🔥 Commissione dell'hub: <b>{fee} 🪙</b> (bruciate)",
    "tr.btn_confirm": "✅ CONFERMA TRASFERIMENTO",
    "tr.btn_cancel": "❌ Annulla",
    "tr.cancelled_toast": "Trasferimento annullato",
    "tr.cancelled": "❌ <b>Trasferimento annullato.</b> Le monete sono rimaste al loro posto.",
    "tr.not_yours": "🔒 Questo non è il tuo trasferimento!",
    "tr.done_toast": "✅ Trasferimento eseguito!",
    "tr.done": (
        "✅ <b>TRASFERIMENTO ESEGUITO!</b>\n\n"
        "💸 Inviate: <b>{amount} 🪙</b> al giocatore ID <code>{recipient_id}</code>\n"
        "💰 Il tuo saldo: <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>Hai ricevuto {amount} 🪙!</b>\n"
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
    "dlv.coins": "💰 Accreditate <b>+{amount} 🪙</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nucleare x5 attivo fino a <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Raffreddamento ad Azoto +40% attivo fino a <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Il Master Drone sorveglia la fattoria fino a <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limiti di vittorie rimossi fino a <b>{until} UTC</b>.",
    "dlv.clan": "🏆 La squadra ha ottenuto lo status <b>MEGA-CLAN</b>: fino a {max} posti.",
    "dlv.err_fridge": "Hai già un frigo di questa capienza o più grande.",
    "dlv.err_no_team": "Non hai ancora creato una squadra. Prima creala con /create_team.",
    "dlv.err_mega": "La tua squadra ha già lo status di Mega-Clan.",
    "dlv.intern_upgrade": "♾ Il tuo Robot Stagista è stato promosso a <b>Robot Minatore ETERNO</b>: 5 🪙 all'ora, senza scadenza!",
    "dlv.err_no_intern": "Nessun Robot Stagista attivato: attivalo prima in /farm.",
    "dlv.err_intern_refs": "L'upgrade richiede {need} amici qualificati (30 round ciascuno); tu ne hai {have}.",
    "mk.header": "📈 <b>BORSA DELLE COTOLETTE</b>\n..................................................\n\nOrdini aperti: <b>{orders}</b> · cotolette in vendita: <b>{cutlets}</b> · miglior prezzo: <b>{best}</b>\nCommissione hub: <b>{fee}%</b> a vendita (bruciata — scudo anti-inflazione)\n🥩 Nel tuo inventario: <b>{inv}</b> cotolette\n\n{body}\n\n<i>Tocca un ordine per comprare. Per vendere: /sell.</i>",
    "mk.empty": "Ancora nessuna offerta. Sii il primo: /sell quantità prezzo",
    "mk.order_line": "🥩 #{id} · <b>{qty} pz</b> a <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} pz a {price} 🪙",
    "mk.btn_my": "📋 I miei ordini",
    "mk.btn_sell_help": "💰 Come vendere",
    "mk.btn_refresh": "🔄 Aggiorna",
    "mk.btn_back": "← Alla borsa",
    "mk.pick": "🛒 <b>Ordine #{id}</b>: {qty} pz disponibili a {price} 🪙.\nQuante?",
    "mk.btn_qty": "{qty} pz — {total} 🪙",
    "mk.btn_qty_all": "Tutte, {qty} pz — {total} 🪙",
    "mk.buy_toast": "Affare fatto!",
    "mk.buy_done": "✅ Comprate <b>{qty} cotolette</b> per <b>{total} 🪙</b>. Sono nell'inventario: rifornisci le Trivelle!",
    "mk.sold_notify": "💰 <b>Borsa: venduto!</b> Ordine #{id}: {qty} pz a {price}. Hai ricevuto <b>+{got} 🪙</b> (commissione di {fee} bruciata).",
    "mk.sell_help": "💰 <b>COME VENDERE LE COTOLETTE</b>\n\nComando: <code>/sell quantità prezzo</code>\nEsempio: <code>/sell 10 250</code> — 10 cotolette a 250 🪙.\n\nLe cotolette lasciano l'inventario e aspettano nell'ordine (annullabile in ogni momento). Fino a {max_qty} pz per ordine e {max_orders} ordini aperti. Alla vendita si brucia una commissione del {fee}%. Una cotoletta non costa meno di {min} 🪙: il carburante del negozio in Stars conviene sempre più della borsa. Risorse, ordini di acquisto e scambi sono nell'app di gioco.",
    "mk.sell_confirm": "📝 Mettere in vendita <b>{qty} cotolette</b> a <b>{price}</b> 🪙?\nTotale: {total} · commissione {fee} bruciata · riceverai <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ METTI IN BORSA",
    "mk.btn_cancel": "❌ Annulla",
    "mk.sell_toast": "Ordine pubblicato!",
    "mk.sell_done": "✅ Ordine <b>#{id}</b> in borsa: {qty} pz a {price} 🪙. Ti avviso appena venduto.",
    "mk.cancelled_toast": "Annullato",
    "mk.cancel_text": "❌ <b>Annullato.</b> Le cotolette restano nell'inventario.",
    "mk.my_header": "📋 <b>I TUOI ORDINI</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} pz a {price} 🪙",
    "mk.my_empty": "📋 Non hai ordini aperti.",
    "mk.btn_cancel_order": "❌ Ritira ordine #{id}",
    "mk.order_cancelled": "↩️ Ordine #{id} ritirato: <b>{qty} cotolette</b> tornate nell'inventario.",
    "mk.err_qty": "❌ Quantità: da 1 a {max} pz. per ordine.",
    "mk.err_price": "❌ Prezzo: da {min} a {max} 🪙 cadauno.",
    "mk.err_no_cutlets": "❌ Hai solo {have} cotolette nell'inventario. Quelle nel frigo non si vendono — vedi /farm.",
    "mk.err_too_many": "❌ Limite: massimo {max} ordini aperti. Ritirane uno in «I miei ordini».",
    "mk.err_not_found": "❌ Questo ordine è già chiuso.",
    "mk.err_own": "🤨 Non puoi comprare il tuo stesso ordine.",
    "mk.err_insufficient": "❌ Non basta: servono {total} 🪙.",
    "farm.btn_market": "📈 Borsa delle cotolette",

    # ---------------- ресурсы (волна 22.10, вечер) ----------------
    "res.metal": "Metallo",
    "res.hydrogen": "Idrogeno",
    "res.crystal": "Cristalli",
    "res.parts": "Componenti",
    "res.none": "ancora vuoto",
    "games.resource_gain": "{icon} Estratto: <b>+{qty} {name}</b> (totale {total}) → /workshop",
    "duel.metal_gain": "⛏ Trofeo del duello: <b>+{metal} Metallo</b> → /workshop",
    "quest.win_resources": "\n📦 In più un set di risorse: <b>{qty}</b> di ciascuna → /workshop",
    "profile.resources_line": "🧰 Risorse: {stock}\n",
    "menu.btn_goals": "🎯 Obiettivi del giorno",
    "menu.btn_raids": "🏴‍☠️ Incursioni",
    "menu.btn_workshop": "🔧 Officina",
    "farm.btn_workshop": "🔧 Officina",
    "farm.btn_app": "🏭 Fattoria nell'app",
    "menu.btn_app": "🚀 App di gioco: fattoria, officina, incursioni",
    "app.btn_section": "🚀 APRI NELL'APP",
    "app.goto_workshop": "🔧 L'<b>officina</b> vive nell'app di gioco: risorse, ricette e crafting in un tocco.",
    "app.goto_raids": "🏴‍☠️ Le <b>incursioni</b> vivono nell'app di gioco: ricognizione, posizione di difesa e rivincita.",
    "app.goto_station": "🛰 La <b>stazione della squadra</b> vive nell'app di gioco: progressi, contributi e un bonus per tutta la squadra.",
    "app.goto_market": "📈 La <b>borsa delle cotolette</b> è più comoda nell'app di gioco: offerte, vendita e i tuoi ordini in un'unica schermata.",
    "mk.err_asset": "❌ Questo articolo non è in borsa.",
    "mk.err_no_resource": "❌ Risorsa insufficiente: nell'inventario ne hai solo {have}.",
    "mk.bid_filled_notify": "🙋 <b>Borsa: ordine di acquisto eseguito!</b> Ordine #{id}: comprati <b>+{qty} {icon}</b> a {price} 🪙.",
    "sw.err_same": "❌ Non puoi scambiare una risorsa con la stessa.",
    "sw.err_qty": "❌ Nello scambio indica una quantità da 1 a {max}: sia ciò che dai sia ciò che vuoi ricevere.",
    "shop.btn_info": "ℹ️ Cosa dà ogni articolo",
    "sw.done_notify": "🔄 <b>Scambio #{id} concluso!</b> Dati {give}, ricevuti {want}.",
    "ws.err_coins": "🔒 Monete insufficienti: servono {need} 🪙, ne hai {have} 🪙.",
    "wk.eff_nitrogen": "❄️ Azoto +40% per {h} h",
    "wk.eff_nuclear": "☢️ Nucleare x5 per {h} h",
    "wk.eff_drone": "🛸 Master Drone per {h} h",
    "wk.eff_shield": "🛡 Scudo per {h} h",
    "wk.eff_unlimit": "⚡ Giochi senza limiti per {h} h",
    "wk.eff_cutlet": "🥩 Cotoletta ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ Questa ricetta della settimana non è più disponibile.",
    "wk.err_limit": "🔒 Limite settimanale di questa ricetta esaurito ({limit}). La nuova settimana parte lunedì alle 00:00 UTC.",
    "games.resource_full": "📦 Deposito {icon} pieno ({cap}): il bottino in eccesso va perso. Spendi, vendi o amplia il deposito nell'officina.",
    "mk.err_storage_full": "📦 Spazio insufficiente nel deposito: liberi {free}. Amplia il deposito nell'officina.",
    "mk.err_buyer_full": "📦 Il deposito dell'acquirente è pieno: ora l'affare non si può concludere (liberi {free}).",
    "ws.recipe_storage": "Amplia il deposito a {cap}",
    "ws.done_storage": "📦 <b>Deposito ampliato:</b> fino a {cap} di ogni risorsa. Per sempre.",
    "ws.err_storage_max": "📦 Il deposito è già alla capienza massima.",
    "farm.boost_armor": "🛡 Cyber-Armatura liv. {level}: +{percent}% all'estrazione fino alle {until} UTC",
    "farm.boost_station": "🛰 Stazione della squadra liv. {level}: +{percent}% all'estrazione",
    "clan.btn_station": "🛰 Stazione della squadra",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>OFFICINA</b>\n"
        "..................................................\n\n"
        "🧰 Le tue risorse: {stock}\n"
        "⛏ Metallo — Morra Cinese e duelli · 💧 Idrogeno — Alto/Basso · "
        "💎 Cristalli — Quiz · ⚙️ Componenti — Cyber-Cassaforte. Le quest danno un set completo.\n\n"
        "🛡 Cyber-Armatura: <b>livello {armor}/{armor_max}</b> (+{armor_pct}% all'estrazione per livello, per 30 giorni)\n"
        "🚀 Shuttle: <b>{shuttle}</b> — commissione della borsa {shuttle_fee}%, fino a {shuttle_qty} cotolette per ordine\n\n"
        "<i>✅ — risorse sufficienti, 🔒 — non ancora. Un tocco ed è fatta.</i>"
    ),
    "ws.shuttle_yes": "costruito",
    "ws.shuttle_no": "non costruito",
    "ws.recipe_nitro_6h": "Raffreddamento ad Azoto per 6 h",
    "ws.recipe_nuclear_3h": "Boost Nucleare per 3 h",
    "ws.recipe_drone_24h": "Master Drone per 24 h",
    "ws.recipe_shield_24h": "Scudo anti-incursioni per 24 h",
    "ws.recipe_cutlet": "Sintesi di una cyber-cotoletta",
    "ws.recipe_armor": "Cyber-Armatura liv. {level}",
    "ws.recipe_shuttle": "Costruisci lo Shuttle",
    "ws.btn_shuttle_owned": "🚀 Shuttle costruito",
    "ws.btn_armor_max": "🛡 Cyber-Armatura: al massimo",
    "ws.btn_refresh": "🔄 Aggiorna",
    "ws.btn_farm": "🚜 Alla fattoria",
    "ws.noop": "Già al massimo",
    "ws.toast": "Fatto!",
    "ws.done_nitrogen": "❄️ <b>Raffreddamento ad Azoto +40%</b> attivo fino alle {until} UTC.",
    "ws.done_nuclear": "☢️ <b>Boost Nucleare x5</b> attivo fino alle {until} UTC. Le Trivelle mangiano ×3 cotolette!",
    "ws.done_drone": "🛸 <b>Master Drone</b> protegge i robot fino alle {until} UTC.",
    "ws.done_shield": "🛡 <b>Scudo anti-incursioni</b> attivo fino alle {until} UTC. Le tue risorse sono al sicuro.",
    "ws.done_cutlet": "🥩 Sintetizzata: <b>+{qty} cyber-cotoletta</b> nell'inventario. Rifornisci in /farm!",
    "ws.done_armor": "🛡 <b>Cyber-Armatura livello {level}!</b> Estrazione della fattoria: <b>+{percent}%</b> per 30 giorni.",
    "ws.done_shuttle": "🚀 <b>Shuttle costruito!</b> La commissione sulle tue vendite ora è del {fee}%, fino a {qty} cotolette per ordine. Lo Shuttle è solo tuo, per sempre.",
    "ws.err_unknown": "❌ Questa ricetta non esiste.",
    "ws.err_resources": "🔒 Non basta: {kind} — servono {need}, ne hai {have}. Estraine nei giochi!",
    "ws.err_shuttle_owned": "🚀 Lo Shuttle è già costruito — uno solo per giocatore.",
    "ws.err_armor_max": "🛡 L'armatura è già al livello massimo ({max}).",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>INCURSIONI</b>\n"
        "..................................................\n\n"
        "💧 Idrogeno: <b>{hydrogen}</b> (un decollo costa {fuel})\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ Posizione di difesa: <b>{stance}</b>\n\n"
        "📊 Incursioni: <b>{attacks}</b> (riuscite {attack_wins}) · respinte: <b>{holds}/{defenses}</b>\n\n"
        "<i>Il bottino è solo in risorse: il {percent}% della scorta del bersaglio, massimo {cap} per risorsa. "
        "Monete, robot e cotolette sono intoccabili. La tua mossa contro la posizione del bersaglio: "
        "decisione contro decisione. Un decollo ogni {cooldown} h; la rivincita è gratis.</i>"
    ),
    "raid.ready_line": "Nave pronta al decollo",
    "raid.cooldown_line": "Ricarica: ancora {minutes} min",
    "raid.shield_on": "Scudo attivo fino alle {until} UTC",
    "raid.shield_newbie": "Protezione principiante (primi {days} giorni)",
    "raid.shield_off": "Nessuno scudo — costruiscilo in /workshop",
    "raid.stance_random": "casuale (scegline una nel menu!)",
    "raid.btn_scout": "🔭 RICOGNIZIONE: trova bersagli",
    "raid.btn_revenge": "⚔️ Rivincita: {name}",
    "raid.btn_stance": "✊ Posizione di difesa",
    "raid.btn_workshop": "🛡 Costruisci uno scudo",
    "raid.btn_refresh": "🔄 Aggiorna",
    "raid.btn_back": "← Indietro",
    "raid.btn_open": "🏴‍☠️ Apri le incursioni",
    "raid.btn_again": "🏴‍☠️ Alle incursioni",
    "raid.stance_pick": "✊ <b>Posizione di difesa</b>\nLa rivela solo l'esito di un'incursione altrui: la mossa dell'attaccante contro la tua posizione. Cambiala ogni tanto — chi è prevedibile viene derubato.",
    "raid.stance_saved": "Posizione: {stance}",
    "raid.scout": "🔭 <b>La ricognizione ha trovato dei bersagli.</b> Il decollo costa {fuel} 💧. Scegli:",
    "raid.btn_target": "🎯 {name} · risorse ≈{total}",
    "raid.no_targets": "🔭 La ricognizione non ha trovato nessuno: al momento non ci sono bersagli adatti (scudi, ricariche, principianti). Ripassa più tardi.",
    "raid.pick_move": "✊ <b>La tua mossa?</b> Giocherà contro la posizione di difesa del bersaglio. Decollo: −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>Rivincita! La tua mossa?</b> Il decollo è gratis e senza ricarica.",
    "raid.result_win": "🏴‍☠️ <b>INCURSIONE RIUSCITA!</b>\n{move} contro {stance} di {name}.\nBottino: <b>{loot}</b>",
    "raid.result_draw": "😐 <b>Pareggio.</b> {move} contro {stance} di {name}. La nave è tornata vuota, il carburante è andato.",
    "raid.result_lose": "💥 <b>LA DIFESA HA RETTO.</b> {move} contro {stance} di {name}.\nAl bersaglio è andato: <b>{loot}</b>",
    "raid.result_footer": "<i>Le risorse sono in /workshop. Uno scudo ti protegge dalla ritorsione.</i>",
    "raid.victim_lost": "🚨 <b>Hai subito un'incursione!</b> {name}: {move} contro la tua posizione {stance}.\nPerso: <b>{loot}</b>\n\n⚔️ Rivincita gratis entro {hours} h. Lo scudo è in /workshop.",
    "raid.victim_draw": "🛡 <b>Incursione finita in pareggio.</b> {name}: {move} contro la tua posizione {stance}. Non hai perso nulla.",
    "raid.victim_held": "🛡 <b>La difesa ha retto!</b> {name}: {move} contro la tua posizione {stance}.\nTrofeo della difesa: <b>{loot}</b>",
    "raid.err_stance": "❌ Mossa sconosciuta.",
    "raid.err_self": "🤨 Un'incursione contro di te? No.",
    "raid.err_gone": "❌ Bersaglio non disponibile.",
    "raid.err_teammate": "🤝 Non si deruba la propria gente — è un compagno di squadra.",
    "raid.err_shielded": "🛡 Il bersaglio ha uno scudo. Scegline un altro.",
    "raid.err_revenge_gone": "❌ La finestra per la rivincita è chiusa.",
    "raid.err_cooldown": "⏳ Ricarica: ancora {minutes} min.",
    "raid.err_victim_cooldown": "⏳ Questo bersaglio è stato derubato da poco (pausa di {hours} h).",
    "raid.err_fuel": "💧 Idrogeno insufficiente: ne servono {need}, ne hai {have}. Si estrae in Alto/Basso.",

    # ---------------- ежедневные цели ----------------
    "goal.header": (
        "🎯 <b>OBIETTIVI DI OGGI</b>\n"
        "..................................................\n\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 Forziere: <b>+{coins} 🪙</b> e <b>+{res}</b> di una risorsa a caso\n"
        "🔥 Serie: <b>{streak}</b> gg · ogni {every}° giorno di fila +{bonus} 🪙 nel forziere\n\n"
        "<i>Gli obiettivi si rinnovano alle 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ Completa tutti e tre e il forziere è tuo.",
    "goal.status_ready": "✅ <b>Tutti gli obiettivi completati! Ritira il forziere.</b>",
    "goal.status_claimed": "🎁 Il forziere di oggi è già stato ritirato. Domani nuovi obiettivi!",
    "goal.btn_claim": "🎁 RITIRA IL FORZIERE",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Aggiorna",
    "goal.toast": "Forziere aperto!",
    "goal.chest": "🎁 <b>FORZIERE APERTO!</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 Serie: {streak} gg",
    "goal.err_claimed": "🎁 Già ritirato oggi.",
    "goal.err_not_done": "⏳ Non hai ancora completato tutti gli obiettivi.",
    "goal.win_quiz": "Vinci {n} round di quiz",
    "goal.win_rps": "Vinci {n} round di Morra Cinese",
    "goal.win_hl": "Vinci {n} round di Alto/Basso",
    "goal.win_safe": "Apri la Cyber-Cassaforte {n} volte",
    "goal.play_rounds": "Gioca {n} round in qualsiasi gioco",
    "goal.duel": "Gioca un duello",
    "goal.bonus": "Ritira la cotoletta giornaliera in fattoria",
    "goal.craft": "Costruisci qualcosa in officina",
    "goal.raid": "Compi un'incursione",
    "goal.market_deal": "Concludi un affare in borsa",
    "goal.donate": "Investi risorse nella stazione della squadra",

    # ---------------- станция команды ----------------
    "st.header": (
        "🛰 <b>STAZIONE DELLA SQUADRA “{team}”</b>\n"
        "..................................................\n\n"
        "Livello: <b>{level}/{max}</b> → ogni combattente riceve <b>+{percent}%</b> all'estrazione della fattoria "
        "(+{per_level}% per livello)\n\n"
        "📦 Al prossimo livello:\n{progress}\n\n"
        "🧾 Ultimi contributi:\n{feed}\n\n"
        "🧰 Le tue risorse: {stock}\n"
        "<i>La stazione è di tutti: la costruisce l'intera squadra, il bonus va a ciascuno. Lasci la squadra — perdi il bonus.</i>"
    ),
    "st.max_level": "🏁 Stazione completata — livello massimo!",
    "st.feed_empty": "nessun contributo finora — fai la prima mossa",
    "st.no_team": "🛰 La stazione la costruisce una squadra. Entra in una squadra o crea la tua — e costruite insieme.",
    "st.btn_find_team": "🏆 Squadre e clan",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ Tutto: {qty} {icon} {name}",
    "st.btn_refresh": "🔄 Aggiorna",
    "st.btn_team": "🏆 Alla squadra",
    "st.toast": "Investito +{qty} {icon}",
    "st.level_up": "🛰 <b>La stazione della squadra è salita al livello {level}!</b> Ora ogni combattente ha +{percent}% all'estrazione della fattoria.",
    "st.err_qty": "❌ Quantità non valida.",
    "st.err_no_team": "❌ Non sei in una squadra.",
    "st.err_max": "🏁 La stazione è già completata (livello {max}).",
    "st.err_resources": "🔒 Risorsa insufficiente: ne hai {have}.",

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
    "tab_passport": "📋 Passaporto",
    "tab_farm": "🚜 Fattoria",
    "tab_goals": "🎯 Obiettivi",
    "tab_workshop": "🔧 Officina",
    "tab_raids": "🏴‍☠️ Incursioni",
    "tab_market": "📈 Borsa",
    "tab_team": "🏆 Squadra",
    "tab_shop": "🏪 Negozio",
    "tab_top": "👑 TOP",
    "passport": "📋 PASSAPORTO GIOCATORE",
    "coins": "🪙",
    "brain": "🧠 Livello di intelligenza",
    "toNext": "al livello {n}: {left} risposte esatte nel quiz (+{reward} 🪙)",
    "farm": "🚜 CYBER-FATTORIA",
    "robots": "Robot (minatori / trivelle)",
    "intern": "Robot Stagisti (1 🪙/h, eterni)",
    "activateIntern": "🚀 ATTIVA IL ROBOT STAGISTA",
    "internDone": "🤖 Il tuo Robot Stagista è in turno!",
    "rank": "🎖 Grado",
    "openFarm": "🏭 APRI LA MINIERA",
    "farmScene": "🏭 LA TUA FATTORIA",
    "back": "← Indietro",
    "minedVisit": "estratto in questa visita",
    "unit_intern": "Robot Stagista",
    "unit_junior": "Robo-Minatore",
    "unit_premium": "Cyber-Trivella",
    "eternal": "eterno",
    "fueledAll": "riforniti",
    "fueledPart": "{a} su {b} riforniti",
    "license": "licenza di 30 giorni",
    "emptyFarm": "La miniera è vuota. Attiva il tuo Robot Stagista o compra robot nel negozio!",
    "madeBy": "Vuoi un bot così per il tuo progetto? Scrivi a @mister_telebot",
    "fueled": "Trivelle rifornite",
    "speed": "Velocità di estrazione",
    "perHour": "{v} 🪙/h",
    "fridge": "Frigo",
    "inv": "Cotolette nell'inventario",
    "burnout": "Prossimo esaurimento",
    "boosts": "Boost attivi",
    "none": "nessuno",
    "resources": "🧰 Risorse",
    "bonusPct": "Bonus permanente all'estrazione",
    "shuttle": "🚀 Shuttle costruito",
    "resHint": "Ogni vittoria porta la risorsa del suo gioco, con la rimozione dei limiti senza alcun tetto. Spendile nell'officina.",
    "bonusReady": "🎁 RITIRA LA COTOLETTA GIORNALIERA",
    "bonusWait": "⏳ Bonus tra {h} h {m} min",
    "bonusDone": "🎉 Cotoletta nell'inventario!",
    "team": "🏆 LA MIA SQUADRA",
    "clan": "CLAN",
    "teamLabel": "Squadra",
    "captain": "👑 Al comando ci sei tu!",
    "members": "Formazione",
    "noTeam": "Ancora nessuna squadra. Creane una o unisciti a un'altra nella chat del bot: «🏆 Squadre e clan».",
    "top": "👑 TOP-100 DEI PIÙ RICCHI DELL'ECOSISTEMA",
    "shop": "🏪 NEGOZIO",
    "shopFarm": "🚜 PER LA FATTORIA",
    "shopGames": "🕹️ GAMING",
    "shopHint": "Paga con le Telegram Stars ufficiali — direttamente qui, in un tocco.",
    "paid": "🎉 Pagato! L'articolo è già sul tuo account.",
    "payFail": "Il pagamento non è andato a buon fine. Riprova.",
    "oldClient": "Aggiorna Telegram per comprare dall'app, oppure apri il negozio nella chat del bot.",
    "ctaNoRobots": "💤 La fattoria è quasi vuota! Prenditi un robot più potente — le 🪙 arriveranno 24 ore su 24.",
    "ctaHungry": "🚨 Le Trivelle hanno fame ({n} senza carburante) — l'estrazione è ferma!",
    "ctaLowFuel": "⚠️ Le cotolette non bastano per un giorno di lavoro delle Trivelle.",
    "ctaShopBtn": "🛒 Al negozio",
    "footer": "Giochi e quiz sono nella chat del bot",
    "noProfile": "Profilo non trovato. Apri il bot e premi /start!",
    "blocked": "Account bloccato dall'amministrazione.",
    "error": "Impossibile caricare i dati. Riprova più tardi.",
    "outside": "Apri questa app dal bot Telegram di ROFL HUB.",
    "robotsTitle": "🤖 I TUOI ROBOT",
    "buyMore": "🛒 Compra",
    "rateShort": "{v} 🪙/h",
    "refuelOne": "🥩 Carica 1",
    "refuelAll": "⚡ Carica tutte",
    "refueled": "Caricate: {n} 🥩",
    "res_metal_src": "Morra Cinese e duelli",
    "res_hydrogen_src": "Alto/Basso",
    "res_crystal_src": "Quiz",
    "res_parts_src": "Cyber-Cassaforte",
    "resWhere": "dove ottenerle",
    "ws_title": "🔧 OFFICINA",
    "ws_hint": "Le risorse dei giochi diventano potenziamenti. Se le risorse bastano, premi «Costruisci».",
    "ws_craft": "Costruisci",
    "ws_owned": "✅ Già tuo",
    "ws_crafted": "Fatto! Il potenziamento è già attivo.",
    "ws_armor": "🛡 Cyber-Armatura",
    "ws_armorLvl": "livello {l}/{m} · +{p}% per livello per 30 giorni",
    "ws_shuttleOn": "🚀 Shuttle costruito: commissione della borsa {fee}%",
    "ws_shuttleOff": "🚀 Shuttle non costruito: commissione della borsa {fee}%",
    "eff_nitrogen": "+40% all'estrazione di tutti i robot",
    "eff_nuclear": "×5 all'estrazione, le Trivelle mangiano ×3 cotolette",
    "eff_drone": "i robot non invecchiano",
    "eff_shield": "nessuno può farti incursioni",
    "eff_cutlet": "1 cyber-cotoletta nell'inventario (cara: il carburante conviene in negozio)",
    "eff_armor": "+10% all'estrazione per livello per 30 giorni",
    "eff_storage": "più spazio per le risorse — per sempre",
    "eff_shuttle": "solo tuo: commissione del 5% sulle tue vendite e ordini fino a 500 cotolette — per sempre",
    "raid_title": "🏴‍☠️ INCURSIONI",
    "raid_how": "📖 Come funziona",
    "raid_rule1": "Scegli una mossa; il bersaglio ha una posizione di difesa impostata in anticipo. Decide la Morra Cinese: è un duello di decisioni, non una lotteria.",
    "raid_rule2": "Vittoria: prendi il {pct}% di ogni risorsa del bersaglio, fino a {cap} per risorsa. Fallimento: dai al bersaglio il {fpct}% delle tue, fino a {fcap}. Pareggio: carburante bruciato.",
    "raid_rule3": "Si possono rubare solo le risorse. Monete, robot e cotolette sono al sicuro. I principianti sono protetti per {days} giorni, i compagni di squadra non si toccano.",
    "raid_rule4": "Un decollo costa {fuel} 💧 di idrogeno, il prossimo tra {cd} h. Se qualcuno ti attacca, la rivincita è gratis per {rh} h.",
    "raid_fuel": "💧 Idrogeno",
    "raid_ready": "🚀 Nave pronta al decollo",
    "raid_cooldown": "⏳ Ricarica: {m} min",
    "raid_shieldOn": "🛡 Scudo fino alle {t}",
    "raid_shieldNewbie": "🛡 Protezione principiante",
    "raid_shieldOff": "🛡 Nessuno scudo — costruiscilo nell'officina",
    "raid_stance": "✊ LA TUA POSIZIONE DI DIFESA",
    "raid_stanceHint": "Con questa accogli le incursioni altrui. Cambiala ogni tanto — chi è prevedibile viene derubato più spesso.",
    "raid_stanceNone": "Nessuna posizione scelta — sarà casuale",
    "raid_stanceSaved": "Posizione salvata",
    "raid_stats": "Incursioni: {a} (riuscite {w}) · respinte: {h} su {d}",
    "raid_scout": "🔭 RICOGNIZIONE: trova bersagli",
    "raid_targets": "🎯 Scegli un bersaglio",
    "raid_res": "risorse ≈{n}",
    "raid_noTargets": "Nessun bersaglio adatto al momento: scudi, ricariche, principianti. Riprova più tardi.",
    "raid_pickMove": "✊ La tua mossa contro la posizione di {name}",
    "raid_revenge": "⚔️ RIVINCITA",
    "raid_revengeBtn": "⚔️ Rispondi a: {name}",
    "raid_win": "🏴‍☠️ Incursione riuscita!",
    "raid_draw": "😐 Pareggio — la nave è tornata vuota",
    "raid_lose": "💥 La difesa ha retto",
    "raid_vs": "{m} contro {s}",
    "raid_loot": "Bottino: {l}",
    "raid_lost": "Ceduto al bersaglio: {l}",
    "rock": "🪨 Sasso",
    "scissors": "✂️ Forbici",
    "paper": "📄 Carta",
    "mk_title": "📈 BORSA",
    "mk_stats": "Ordini: {o} · cotolette: {c} · miglior prezzo: {b} 🪙",
    "mk_feeLine": "La commissione del {f}% su ogni vendita viene bruciata — scudo contro l'inflazione",
    "mk_inv": "🥩 Nel tuo inventario: {n}",
    "mk_offers": "🛒 OFFERTE",
    "mk_empty": "Ancora nessuna offerta — metti in vendita per primo/a!",
    "mk_offer": "{q} 🥩 × {p} 🪙",
    "mk_buyHow": "Quante comprarne?",
    "mk_all": "Tutte, {q}",
    "mk_sellTitle": "💰 VENDI COTOLETTE",
    "mk_qty": "Quante cotolette",
    "mk_price": "Prezzo cadauna, 🪙",
    "mk_preview": "Totale {t} 🪙 · ricevi {g} 🪙 · bruciate {f} 🪙",
    "mk_sell": "Metti in borsa",
    "mk_limits": "Fino a {q} cotolette per ordine, fino a {o} ordini aperti",
    "mk_my": "📋 I MIEI ORDINI",
    "mk_cancel": "Ritira",
    "mk_bought": "Comprate {q} 🥩 per {t} 🪙",
    "mk_listed": "Ordine in borsa! Ti scrivo appena qualcuno compra.",
    "mk_cancelledMsg": "Ordine ritirato, le cotolette sono tornate nell'inventario",
    "st_title": "🛰 STAZIONE DELLA SQUADRA",
    "st_level": "Livello {l} su {m}",
    "st_bonus": "+{p}% all'estrazione per ogni combattente",
    "st_next": "Per il livello {n} servono {c} di ogni risorsa",
    "st_max": "🏁 Stazione completata!",
    "st_feed": "🧾 Ultimi contributi",
    "st_feedEmpty": "Ancora nessun contributo — fai il primo passo",
    "st_donate": "Contribuisci",
    "st_all": "Tutto",
    "st_done": "Contributo versato!",
    "st_hint": "La costruisce tutta la squadra, il bonus va a ognuno. Esci dalla squadra e perdi il bonus.",
    "st_off": "La stazione è temporaneamente in manutenzione",
    "goals_title": "🎯 OBIETTIVI DI OGGI",
    "goals_chest": "🎁 Forziere per tutti e tre: +{c} 🪙 e +{r} di una risorsa a caso",
    "goals_streak": "🔥 Serie: {s} gg · ogni {e}° giorno di fila +{b} 🪙",
    "goals_claim": "🎁 RITIRA IL FORZIERE",
    "goals_claimed": "🎁 Il forziere di oggi è stato ritirato. Domani nuovi obiettivi!",
    "goals_reset": "Gli obiettivi si rinnovano alle 00:00 UTC",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · serie {s} gg",
    "as_cutlet": "Cotolette",
    "as_metal": "Metallo",
    "as_hydrogen": "Idrogeno",
    "as_crystal": "Cristalli",
    "as_parts": "Componenti",
    "mk_index": "📈 INDICE DI BORSA",
    "mk_chart": "📊 PREZZO A 7 GIORNI",
    "mk_noTrades": "Ancora nessuno scambio — sii il primo o la prima!",
    "mk_avg": "Prezzo medio della settimana: {p} 🪙 · venduti: {v}",
    "mk_asks": "🛒 IN VENDITA",
    "mk_bids": "🙋 RICHIESTE",
    "mk_noBids": "Ancora nessun ordine di acquisto",
    "mk_sellTo": "Vendi",
    "mk_sellHow": "Quante venderne?",
    "mk_bidTitle": "🙋 ORDINE DI ACQUISTO",
    "mk_bidHint": "Le monete restano congelate nell'ordine fino allo scambio. Ritiri l'ordine e le monete tornano.",
    "mk_bid": "Piazza l'ordine",
    "mk_bidPreview": "Verranno congelate {t} 🪙",
    "mk_have": "Hai: {n}",
    "mk_floor": "Una cotoletta non costa meno di {p} 🪙: il carburante del negozio in Stars conviene sempre",
    "mk_side_sell": "vendo",
    "mk_side_buy": "compro",
    "mk_listedBid": "Ordine di acquisto piazzato! Monete congelate fino allo scambio.",
    "mk_sold": "Vendute {q}, ricevute {g} 🪙 al netto della commissione",
    "mk_shuttleNote": "🚀 Il tuo Shuttle: commissione del {f}% sulle tue vendite",
    "sw_title": "🔄 SCAMBIO DI RISORSE",
    "sw_hint": "Dai ciò che ti avanza, ricevi ciò che ti serve. Senza monete e senza commissioni.",
    "sw_give": "Tu dai",
    "sw_want": "Vuoi ricevere",
    "sw_qty": "Quantità",
    "sw_create": "Proponi uno scambio",
    "sw_take": "Scambia",
    "shop_info": "ℹ️ Cosa dà ogni articolo",
    "sw_youGet": "Ricevi",
    "sw_youGive": "In cambio dai",
    "sw_takeBtn": "Scambia — dai {x}",
    "sw_mineLine": "Dai {g} → vuoi {w}",
    "sw_qtyErr": "Indica una quantità maggiore di zero in entrambi i campi",
    "sw_empty": "Ancora nessuna proposta di scambio",
    "sw_mine": "Le mie proposte",
    "sw_done": "Scambio concluso!",
    "sw_created": "Proposta pubblicata, risorse messe da parte",
    "sw_cancelled": "Proposta ritirata, risorse restituite",
    "ws_armorUntil": "🛡 Armatura attiva fino al {t}",
    "tab_friends": "🤝 Amici",
    "ref_title": "🤝 INVITA GLI AMICI",
    "ref_rules": "+{s} 🪙 subito per ogni amico. Quando un amico gioca {r} round: altre +{q} 🪙 e {c} 🥩 cyber-cotoletta.",
    "ref_copy": "📋 Copia",
    "ref_copied": "Link copiato!",
    "ref_share": "📤 Condividi",
    "ref_stats": "📊 LA TUA RETE",
    "ref_invited": "invitati",
    "ref_qualified": "attivi",
    "ref_earned": "guadagnate",
    "ref_cutlets": "🥩 Cotolette ricevute per gli amici attivi: {n}",
    "ref_top": "🏆 CHI HA PIÙ AMICI",
    "ref_topHint": "✅ — amici attivi (hanno giocato 30 round), 👥 — tutti gli invitati",
    "ref_empty": "La classifica è ancora vuota: conquista il primo posto!",
    "wk_title": "🔥 RICETTE DELLA SETTIMANA",
    "wk_hint": "Ricette a tempo: compaiono quando lo decide l'hub e poi spariscono. Creale finché puoi!",
    "wk_left": "creazioni rimaste questa settimana: {n} su {m}",
    "st_cap": "📦 Deposito: fino a {c} di ogni risorsa — il bottino in eccesso va perso",
    "featureOff": "⚙️ Sezione in manutenzione",
    "done": "Fatto!",
    "loading": "⏳ Caricamento…",
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
    "market": "📈 Borsa delle cotolette: compra o vendi",
    "sell": "💰 Vendi cotolette: /sell quantità prezzo",
    "my_stats": "📊 Le mie statistiche",
    "faq": "📚 Domande frequenti",
    "rules": "📜 Accordo utente",
    "paysupport": "🛟 Supporto pagamenti",
    "workshop": "🔧 Officina: risorse in potenziamenti",
    "raid": "🏴‍☠️ Incursioni: ricognizione e rivincita",
    "goals": "🎯 Obiettivi del giorno e forziere",
    "station": "🛰 Stazione della squadra: progetto comune",
}
