"""Французская локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> pièces
# Младший Майнер -> Robot Mineur
# Кибер-Бурильщик -> Cyber-Foreur
# кибер-котлета -> cyber-côtelette (кратко: côtelette)
# Холодильник -> Frigo
# склад (инвентарь) -> inventaire / stock
# ферма -> ferme (Cyber-Ferme)
# Ядерный Разгон x5 -> Boost Nucléaire x5
# Азотное Охлаждение +40% -> Refroidissement à l'Azote +40%
# Мастер-дрон -> Maître-Drone
# Кибер-Сейф -> Cyber-Coffre
# Мега-Клан -> Méga-Clan
# Безлимит -> Illimité (снятие лимитов -> lever les limites)
# дуэли -> duels (ставка -> mise, банк -> cagnotte, стол -> table, жест -> geste)
# битвы -> Batailles
# квесты -> quêtes
# уровень интеллекта -> niveau d'intelligence
# викторина -> Quiz; КНБ -> Chifoumi (Pierre-Feuille-Ciseaux)
# команда -> équipe; клан -> clan; банда -> bande

BUTTONS = {
    "main_menu": "📱 MENU PRINCIPAL",
    "profile": "👤 MON PROFIL",
    "farm": "🚜 MA FERME",
    "games_zone": "🕹️ ZONE DE JEU",
    "teams": "🏆 ÉQUIPES & CLANS",
    "shop": "🏪 BOUTIQUE",
    "shop_cat_farm": "🚜 POUR LA FERME",
    "shop_cat_games": "🕹️ JEUX",
}

STRINGS = {
    # ---------------- commun ----------------
    "common.no_profile": "⚠️ Profil introuvable. Appuie sur /start pour t'inscrire.",
    "common.btn_menu": "💿 Menu Principal",
    "common.blocked": "🚫 Ton compte a été bloqué par l'administration de ROFL HUB.",
    "common.feature_off": "⚙️ Cette section est en maintenance. Reviens un peu plus tard !",
    "common.maintenance": "🛠 ROFL HUB est en maintenance rapide. De retour bientôt — tes pièces et ta progression sont en sécurité !",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Content de te revoir, @{username} !</b>\nTa progression est intacte. Le panneau de navigation est en bas de l'écran.",
    "start.btn_continue": "🛸 CONTINUER",
    "start.btn_cutlet": "C'est quoi, une cyber-côtelette ?🥩🤔",
    "start.btn_fight": "Raconte vite, et AU COMBAT !",
    "start.console": "🚀 <b>Console de commande activée ! Utilise les boutons en bas de l'écran.</b>",
    "start.intro1": (
        "👋 <b>Salut ! Je suis ROFL HUB BOT, le bot principal de l'écosystème de jeu ROFL HUB. "
        "Un hub de jeux et de savoir nouvelle génération !</b>\n\n"
        "<b>Ici tu peux :</b>\n"
        "🎮 Jouer à des jeux de chat-bot contre le bot et d'autres joueurs\n"
        "💸 Gagner la monnaie du jeu avec tes victoires, ou lancer une ferme qui la mine 24h/24\n"
        "🤼 Créer une équipe et foncer vers le TOP du classement\n"
        "🏆 Faire évoluer ton équipe en clan et te battre dans le classement international\n"
        "💰 Décrocher le jackpot d'un million de pièces avec ta bande\n"
        "👑 Acheter une publication sur nos pages sociales ou notre site pour faire ta promo ou celle de ton blog\n\n"
        "<b>Ce chat-bot sait :</b>\n"
        "🎮 Afficher la liste de tous les jeux, chaînes et sites ROFL HUB\n"
        "⚡ Créditer des pièces pour les jeux, les batailles d'équipes et de clans, les succès, l'activité et les filleuls\n"
        "🔄 Transférer des pièces de jeu à un autre joueur ROFL HUB\n"
        "💎 Vendre des publications sur le site et des places VIP pour les personnalités et les blogueurs\n"
        "🚀 Vendre des boosters, des titres, des statuts et bien plus...\n\n"
        "<i>Appuie sur « CONTINUER » et je t'en dis plus 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>VOICI TES PREMIÈRES RÉCOMPENSES D'INSCRIPTION !</b>\n"
        "..................................................\n"
        "💸 Tu as reçu <b>{balance} pièces</b>\n"
        "🥩 Tu as reçu <b>{cutlets} cyber-côtelette</b>\n"
        "..................................................\n"
        "C'est ton bonus de bienvenue pour avoir rejoint le club ROFL HUB.\n\n"
        "🔒 <i>Le bonus n'est accordé qu'une seule fois, à l'inscription.</i>\n\n"
        "Les pièces se dépensent de mille façons — elles sont la base de l'économie du hub. Prends-en soin...\n\n"
        "⁉️ <b>Mais tu te poses sûrement une question :</b> c'est quoi, cette côtelette ? Qui dois-je nourrir avec ça ?"
    ),
    "start.intro3": (
        "<b>D'ABORD, POURQUOI LES PIÈCES DE JEU SONT-ELLES SI IMPORTANTES ?</b>\n\n"
        "Les pièces sont le moteur de tous les échanges, compétitions et achats dans <b>ROFL HUB</b>. "
        "C'est presque la seule monnaie de jeu au monde que tu peux miner gratuitement !\n"
        "..................................................\n"
        "<b>Il y a plein de façons d'en gagner :</b>\n"
        "- Inviter des amis avec ton lien de parrainage\n"
        "- Gagner des parties contre le bot\n"
        "- Gagner des duels contre d'autres joueurs\n"
        "- Participer aux batailles d'équipes et de clans\n"
        "- Récupérer le bonus quotidien et accomplir des missions\n"
        "- Adopter un robot qui mine des pièces 24h/24 (Robot Mineur / Cyber-Foreur)\n"
        "..................................................\n"
        "<b>Si tu as un robot de niveau deux (le Cyber-Foreur), il faut le nourrir chaque jour. "
        "C'est là qu'intervient la cyber-côtelette : le carburant du minage automatique, "
        "distribué gratuitement chaque jour ! Ta mission est simple — passer et nourrir ton robot.</b>\n\n"
        "Si tu oublies de le nourrir, le robot se décharge et le minage s'arrête.\n\n"
        "Le Robot Mineur (niveau un) n'a pas besoin de carburant. "
        "Important ! Chaque robot s'achète pour 30 jours — ensuite il faut le racheter ou prendre un Maître-Drone. "
        "Tu pigeras en cours de route :) Ne nous dispersons pas.\n\n"
        "Encore un mot sur <b>ROFL HUB</b>, pour que tu comprennes comment tout fonctionne ici.\n\n"
        "🛑 <b>C'est le dernier message de notre rencontre. Ensuite, direction le combat :)</b>"
    ),
    "start.intro4": (
        "<b>LA VERSION COURTE. ROFL HUB, C'EST :</b>\n"
        "- Des jeux de chat-bot pour tous les goûts\n"
        "- La possibilité de créer une équipe (jusqu'à 50 joueurs)\n"
        "- La possibilité de la faire évoluer en clan (jusqu'à 1000 joueurs)\n"
        "- Des batailles d'équipes et de clans avec des prix\n"
        "- La chaîne ROFL HUB CHANNEL, fun et savoir\n"
        "- Une page Instagram — rofl_hub_global\n"
        "- Le site rofl-hub.com pour discuter et se promouvoir sans inscription\n"
        "- Des milliers de joueurs dans le monde entier — tes futurs amis en font peut-être partie !\n"
        "..................................................\n"
        "<b>Comme promis, c'est le message final. Maintenant, au combat ! Commandes utiles :</b>\n\n"
        "/menu — contrôle rapide des fonctions\n"
        "/games — liste de tous les jeux\n"
        "/faq — questions fréquentes\n"
        "/rules — conditions d'utilisation\n"
    ),

    # ---------------- menu & zone de jeu ----------------
    "menu.text": (
        "📱 <b>MENU PRINCIPAL DE L'ÉCOSYSTÈME ROFL HUB</b>\n"
        "..................................................\n\n"
        "👤 <b>PROFIL PERSONNEL ET PASSEPORT :</b>\n"
        "• /start — Commencer l'intro et créer un compte\n"
        "• /profile — Ton passeport, ton solde et ton équipe en temps réel\n"
        "• /my_stats — Tes statistiques des 30 derniers jours\n\n"
        "🚜 <b>CYBER-FERME ET AUTOMATISATION :</b>\n"
        "• /farm — Hub carburant : ravitaillement et vitesse de production des robots\n"
        "• /shop — Marché : achat de mineurs, de côtelettes et d'améliorations du hub\n\n"
        "🕹️ <b>SALLE DE JEU :</b>\n"
        "• /games — Hub inline de tous les jeux contre le bot\n"
        "• /quiz — Quiz de vitesse : 15 secondes par réponse, niveaux et bonus\n"
        "• /duel — DUELS 1 contre 1 avec de vrais joueurs : tables 10/100/1000\n"
        "• /quests — QUÊTES : polars, comédies et énigmes avec récompenses\n"
        "• /rps, /high_low, /safe — Jeux rapides pour des pièces\n\n"
        "👥 <b>GESTION DE TA BANDE :</b>\n"
        "• /create_team — Enregistrer ta propre équipe pour 100 000 pièces\n"
        "• /my_team — Tableau de bord de la bande et LISTE DES COÉQUIPIERS avec niveaux 🧠\n"
        "• /all_teams — Roulette d'équipes aléatoires\n\n"
        "💸 <b>ARGENT ET AMIS :</b>\n"
        "• /invite — Ton lien de parrainage : +1000 pièces par ami\n"
        "• /transfer — Envoyer des pièces à un autre joueur\n\n"
        "📚 <b>AIDE ET RÈGLES :</b>\n"
        "• /faq — Le guide complet de l'écosystème (s'ouvre dans la Mini App)\n"
        "• /rules — Conditions d'utilisation\n"
        "..................................................\n"
        "<i>⚙️ Utilise le panneau de jeu permanent à deux colonnes en bas de l'écran pour naviguer instantanément !</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>BIENVENUE DANS LA ZONE DE JEU ROFL HUB !</b>\n"
        "..................................................\n\n"
        "Ici tu peux affronter le bot en duels rapides ou passer le sprint-test "
        "intellectuel pour décrocher le jackpot — ou tout perdre !\n\n"
        "💸 Une victoire rapporte : <b>+2 pièces</b> (Cyber-Coffre : <b>+5</b>)\n"
        "💀 Une défaite ou une égalité coûte : <b>-1 pièce</b>\n"
        "🧠 Au Quiz, chrono de 15 secondes et niveaux d'intelligence : le niveau 1, c'est 10 bonnes réponses et <b>+100 pièces</b>, "
        "chaque niveau suivant est plus long de 10 réponses, mais la récompense grimpe de 100 !\n\n"
        "..................................................\n"
        "👇 <b>TAPE SUR UN BOUTON CI-DESSOUS POUR LANCER UNE MANCHE TOUT DE SUITE :</b>"
    ),
    "menu.btn_quiz": "🧠 Quiz",
    "menu.btn_rps": "🪨 Chifoumi",
    "menu.btn_hl": "📈 Plus/Moins",
    "menu.btn_safe": "🔐 Cyber-Coffre",
    "menu.btn_duel": "⚔️ DUELS 1v1",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Passeport, ferme, équipe et top des plus riches — sur un seul écran néon. "
        "Tu peux y récupérer ta côtelette quotidienne directement !\n\n"
        "👇 Tape sur le bouton :"
    ),
    "app.btn": "🎮 OUVRIR LA MINI APP",
    "app.unavailable": "⚙️ La Mini App se connecte encore aux serveurs de l'écosystème. Repasse un peu plus tard !",
    "faq.teaser": (
        "📚 <b>GUIDE DE L'ÉCOSYSTÈME ROFL HUB</b>\n"
        "..................................................\n\n"
        "L'essentiel en bref :\n"
        "🚜 Les robots minent des pièces 24h/24 : Robot Mineur — 5/h sans carburant, "
        "Cyber-Foreur — 10/h, et CHAQUE Foreur mange sa propre cyber-côtelette par jour. "
        "Tous les robots vivent 30 jours (le Maître-Drone met l'usure en pause).\n"
        "🧠 Quiz : 15 secondes par réponse, niveaux d'intelligence aux récompenses croissantes.\n"
        "⚔️ Duels contre de vrais joueurs aux tables de 10/100/1000 pièces.\n"
        "🏆 Équipes jusqu'à 50 combattants (Méga-Clan — jusqu'à 1000) et Batailles événementielles avec des prix pour tous.\n\n"
        "..................................................\n"
        "👇 <b>Le guide complet avec toutes les mécaniques — en un tap :</b>"
    ),
    "faq.btn_open": "📖 OUVRIR LE GUIDE COMPLET",
    "rules.teaser": (
        "📜 <b>CONDITIONS D'UTILISATION DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "L'essentiel en deux mots :\n"
        "🪙 Les pièces et tous les objets du jeu sont des éléments virtuels de divertissement : "
        "ce n'est pas de l'argent et ils ne s'échangent pas contre des fonds réels.\n"
        "💫 Les achats passent uniquement par les Telegram Stars officiels ; les articles numériques "
        "sont livrés instantanément, et les Stars sont remboursées automatiquement si la livraison échoue.\n"
        "🛡️ Nous ne collectons ni numéros de téléphone, ni géolocalisation, ni données personnelles.\n"
        "🤝 Insultes, triche et multi-comptes sont interdits — toute violation peut mener à un blocage.\n\n"
        "..................................................\n"
        "👇 <b>Le texte complet des conditions et la clause de non-responsabilité — en un tap :</b>\n"
        "<i>⚖️ En utilisant le bot, tu acceptes les conditions.</i>"
    ),
    "rules.btn_open": "📜 OUVRIR LES CONDITIONS COMPLÈTES",
    "quest.list_header": (
        "🗺️ <b>QUÊTES ROFL HUB</b>\n"
        "..................................................\n\n"
        "Des histoires interactives avec des choix et des embranchements : polars, comédies, énigmes. "
        "La première victoire dans chaque quête rapporte des pièces, et tu peux rejouer autant que tu veux !\n"
        "🌐 <i>Les histoires des quêtes sont en russe pour l'instant — le pack en français arrive.</i>\n\n"
        "👇 <b>Choisis une histoire :</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} pièces pour la première victoire\n"
        "..................................................\n\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Quête terminée, récompense récupérée. Rejoue autant que tu veux !</i>",
    "quest.card_progress": "⏯ <i>Tu as une partie en cours.</i>",
    "quest.card_new": "🆕 <i>Tu n'as pas encore joué cette histoire.</i>",
    "quest.btn_start": "▶️ LANCER LA QUÊTE",
    "quest.btn_restart": "🔄 RECOMMENCER",
    "quest.btn_resume": "⏯ CONTINUER",
    "quest.btn_list": "🗺️ Liste des quêtes",
    "quest.btn_replay": "🔄 Rejouer",
    "quest.win_first": "\n\n🏆 <b>QUÊTE TERMINÉE ! Récompense : +{coins} pièces.</b>",
    "quest.win_repeat": "\n\n✅ <b>Terminée à nouveau !</b> La récompense de cette quête a déjà été récupérée.",
    "quest.fail_footer": "\n\n💀 <i>Pas la meilleure des fins... mais tu peux toujours rejouer l'histoire !</i>",
    "quest.stale": "⏳ Cette scène est déjà derrière toi — on reprend là où tu en es !",
    "quest.no_coins": "❌ Pas assez de pièces pour l'indice ({cost}). Fais un tour à la ferme !",
    "quest.not_found": "❌ Quête introuvable.",
    "menu.btn_quests": "🗺️ QUÊTES",

    # ---------------- ferme ----------------
    "farm.btn_bonus": "🎁 RÉCUPÉRER LE BONUS (1 côtelette / 24 h)",
    "farm.btn_load1": "🥩 Ravitailler 1",
    "farm.btn_loadall": "⚡ TOUT ravitailler",
    "farm.btn_shop": "🏪 Aller à la Boutique",
    "farm.status_all_fueled": "🟢 Tous les Cyber-Foreurs sont ravitaillés et minent des pièces !",
    "farm.status_partial": "🟡 {fueled} Cyber-Foreurs sur {total} sont ravitaillés. Les autres attendent des côtelettes dans le frigo !",
    "farm.status_no_fuel": "🔴 Les Cyber-Foreurs sont à l'arrêt ! Pas assez de carburant dans le frigo.",
    "farm.status_no_drills": "💡 Prends des Cyber-Foreurs dans /shop pour augmenter tes revenus.",
    "farm.boost_nuclear": "🔋 Boost Nucléaire x5 jusqu'à {until} UTC (consommation de côtelettes ×3)",
    "farm.boost_nitrogen": "❄️ Refroidissement à l'Azote +40% jusqu'à {until} UTC",
    "farm.boost_drone": "🛸 Le Maître-Drone prolonge la vie des robots jusqu'à {until} UTC",
    "farm.no_boosts": "Aucun boost actif — fais un tour dans /shop.",
    "farm.burnout": "🔥 Prochaine expiration de robot : <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Activer ton Robot Stagiaire (gratuit)",
    "farm.intern_activated": "🤖 Ton Robot Stagiaire prend son poste ! +1 pièce par heure pour toujours, sans carburant ni expiration.",
    "farm.intern_already": "🤖 Ton Robot Stagiaire travaille déjà.",
    "farm.intern_line": "🤖 Robots Stagiaires ({rate} pièce/h, éternels) : <code>{count}</code>",
    "farm.intern_hint": "🎁 Tu as un Robot Stagiaire gratuit ! Appuie sur le bouton ci-dessous : il minera 1 pièce par heure pour toujours.",
    "farm.dashboard": (
        "🚜 <b>HUB CARBURANT CENTRAL ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Robots actifs à l'usine : <b>{total}</b>\n"
        "• Robots Mineurs ({junior_rate} pièces/h) : <code>{junior}</code>\n"
        "• Cyber-Foreurs ({premium_rate} pièces/h) : <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VITESSE ACTUELLE DE TA FERME :</b>\n"
        "• Production par heure : <b>+{speed_hour} pièces</b>\n"
        "• Production par jour : <b>+{speed_day} pièces</b>\n\n"
        "⚡ <b>BOOSTS :</b>\n{boosts}\n\n"
        "📋 <b>ÉTAT DE L'USINE DE JEU :</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>ÉTAT DU FRIGO AUTOMATIQUE :</b>\n"
        "🥩 Réserve de carburant : <b>{fridge} / {capacity}</b>\n"
        "💼 Côtelettes dans l'inventaire : <code>{inv}</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Important : les robots vivent 30 jours (le Maître-Drone met l'usure en pause). "
        "CHAQUE Cyber-Foreur consomme SA propre côtelette entière du frigo toutes les "
        "24 heures de travail : 3 robots — 3 côtelettes par jour. Surveille le ravitaillement !</i>"
    ),
    "farm.bonus_ok": "🎁 Cyber-côtelette ajoutée à l'inventaire ! Reviens dans 24 heures.",
    "farm.bonus_wait": "⏳ Bonus déjà récupéré ! Prochaine côtelette dans {hours} h {minutes} min.",
    "farm.no_inv_cutlets": "❌ Tu n'as pas de cyber-côtelettes dans ton inventaire ! Achètes-en dans /shop",
    "farm.fridge_full": "📦 Ton Frigo est déjà plein à craquer !",

    # ---------------- profil ----------------
    "profile.caption": (
        "📋 <b>ESPACE PERSONNEL DU JOUEUR ROFL HUB</b>\n"
        "..................................................\n\n"
        "🆔 Ton ID de Passeport : <code>{user_id}</code>\n"
        "{vip}"
        "💰 Pièces actuellement : <b>{balance} pièces</b>\n"
        "🏆 Ton statut : <b>{team}</b>\n"
        "🧠 Niveau d'intelligence : <b>{level}</b> · jusqu'au niveau {next_level} : "
        "<b>{left}</b> bonnes réponses dans /quiz (récompense : +{reward} pièces)\n\n"
        "..................................................\n"
        "<i>Voici ce que tu possèdes en ce moment. Utilise les boutons pour voler vers d'autres sections !</i>"
    ),
    "profile.no_team": "Pas d'équipe",
    "profile.team_label": "Équipe",
    "profile.clan_label": "Clan",
    "profile.btn_farm": "🚜 Ma Cyber-Ferme",
    "profile.btn_shop": "🏪 Boutique",
    "profile.stats": (
        "📊 <b>STATISTIQUES DE JEU ET SUCCÈS (30 JOURS)</b>\n"
        "..................................................\n\n"
        "🧠 Niveau d'intelligence de jeu : <b>{level}</b> (total de bonnes réponses : {total})\n"
        "🎮 Manches de duel jouées : <b>{played}</b>\n"
        "🏆 Victoires remportées : <code>{won}</code>\n"
        "👥 Amis actifs invités : <b>{refs}</b>\n\n"
        "..................................................\n"
        "<i>Les statistiques gardent tes exploits historiques et tes succès passés, même si les pièces gagnées ont déjà été dépensées au marché !</i>"
    ),
    "img.passport": "ID PASSEPORT : {user_id}",
    "img.owner": "CHEF : @{username}",
    "img.balance": "Solde : {balance} pièces",
    "img.fridge": "Frigo : {fridge} / {capacity}",
    "img.inv": "Côtelettes en stock : {inv}",
    "img.junior": "Robots Mineurs : {count}",
    "img.premium": "Cyber-Foreurs : {count}",

    # ---------------- jeux : moteur commun ----------------
    "games.win": "🎉 <b>VICTOIRE !</b> 🎉\nPièces créditées : <b>+{reward}</b>",
    "games.lose": "💀 <b>DÉFAITE !</b>\nPièces débitées : <b>-{penalty}</b>",
    "games.draw": "🤝 <b>ÉGALITÉ !</b>\nPièces débitées : <b>-{penalty}</b>",
    "games.limit": (
        "🛑 <b>Limite quotidienne atteinte !</b>\n\n"
        "Tu as déjà remporté {limit} victoires au jeu « {game} » aujourd'hui. La limite se réinitialise à 00:00 UTC.\n\n"
        "⚡ Lever la limite pour 24 heures — 5 ★, pour 30 jours — 99 ★ (section « Jeux » dans /shop)."
    ),
    "games.no_coins": "❌ Tu as 0 pièce — impossible de payer les frais de la manche. Récupère les revenus de ta ferme dans /farm !",
    "games.balance": "💰 Solde : <b>{balance} pièces</b>",
    "games.btn_retry": "🎮 Rejouer !",
    "games.btn_hub": "🕹️ Zone de jeu",
    "games.level_up": (
        "🏅 <b>NIVEAU D'INTELLIGENCE AUGMENTÉ : {level} !</b> Récompense : <b>+{bonus} pièces</b> !\n"
        "Niveau suivant : {next_required} bonnes réponses → +{next_reward} pièces."
    ),
    "games.name.rps": "Pierre-Feuille-Ciseaux",
    "games.intern_bonus": "🤖 Niveau {level} ! Un nouveau Robot Stagiaire rejoint ta ferme : tu en as maintenant {count}.",
    "games.name.hl": "Plus/Moins",
    "games.name.quiz": "Quiz",
    "games.name.safe": "Coffre",

    # ---------------- Chifoumi ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>PIERRE-FEUILLE-CISEAUX</b>\n\n"
        "Victoire : <b>+{reward}</b> · Défaite/égalité : <b>-{penalty}</b>\n"
        "Limite de victoires par jour : <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Pierre",
    "rps.scissors": "✂️ Ciseaux",
    "rps.paper": "🧻 Feuille",
    "rps.draw": "🤝 <b>Égalité !</b> Vous avez tous les deux choisi {bot}.",
    "rps.win": "🏆 <b>Victoire !</b> {user} bat {bot}.",
    "rps.lose": "💀 <b>Le bot a gagné.</b> {bot} bat {user}.",

    # ---------------- Plus/Moins ----------------
    "hl.intro": (
        "🎲 <b>PLUS OU MOINS</b>\n\nLe bot a choisi le nombre : <b>{base}</b>.\n"
        "Le nombre caché sera-t-il plus grand ou plus petit ?\n"
        "Victoire : <b>+{reward}</b> · Défaite : <b>-{penalty}</b> · Limite : <b>{limit}</b> victoires"
    ),
    "hl.btn_up": "📈 Plus",
    "hl.btn_down": "📉 Moins",
    "hl.result": "🎲 <b>RÉSULTAT DE LA MANCHE</b>\n\nNombre du bot : <b>{base}</b> · Caché : <b>{secret}</b>",

    # ---------------- quiz ----------------
    "quiz.round": (
        "🧠 <b>QUIZ • {category}</b>\n"
        "🤔 QUESTION : <b>{question}</b>\n\n"
        "<i>🌐 Les questions sont en russe pour l'instant — le pack en français arrive bientôt !</i>"
    ),
    "quiz.btn_new": "🧠 Nouvelle question",
    "quiz.timeout": "⌛ <b>TEMPS ÉCOULÉ !</b> ⌛\nBonne réponse : <b>{correct}</b>",
    "quiz.stale": "⏳ Cette question n'est plus active. Lances-en une nouvelle !",
    "quiz.stale_alert": "Cette question n'est plus active. Lances-en une nouvelle !",
    "quiz.empty": "⚠️ La base de questions est vide. Préviens l'administrateur.",
    "quiz.wrong": "❌ <b>Erreur</b> ❌\nBonne réponse : <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} pièce</b> pour la défaite !",
    "quiz.level_line": (
        "🧠 Niveau d'intelligence : <b>{level}</b>\n"
        "Victoires restantes jusqu'au niveau {next_level} : <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} secondes pour répondre !\n"
        "Correct : +{win} pièces sur ton solde\n"
        "Erreur / temps écoulé : -{penalty} pièce\n"
        "Limite : {limit} victoires par jour</i>"
    ),



    # ---------------- Coffre ----------------
    "safe.intro": (
        "🔐 <b>CYBER-COFFRE</b>\n\n"
        "À l'intérieur : un jackpot de <b>{jackpot} pièces</b> ! La porte est verrouillée par un code de 1 à {codes}. "
        "Tu as une seule tentative.\n"
        "Ouvert : <b>+{jackpot}</b> · Alarme : <b>-{penalty}</b> · Limite : <b>{limit}</b> victoires"
    ),
    "safe.btn_retry": "🔐 Craquer encore une fois !",
    "safe.win": "🔓 <b>Coffre ouvert !</b> Le code était : <b>{code}</b>.",
    "safe.lose": "🚨 <b>L'alarme s'est déclenchée !</b> Tu as tapé {guess}, et le code était : <b>{code}</b>.",

    # ---------------- duels ----------------
    "duel.intro": (
        "⚔️ <b>DUELS 1 CONTRE 1 : PIERRE-FEUILLE-CISEAUX AVEC MISE</b>\n"
        "..................................................\n\n"
        "Choisis une table selon ton budget — comme au poker. La mise est prélevée tout de suite, "
        "et ton adversaire est un vrai joueur ROFL HUB !\n\n"
        "💰 La cagnotte = les deux mises. Le gagnant prend <b>{payout_percent}%</b> de la cagnotte, "
        "<b>{burn_percent}%</b> part en fumée pour de bon (déflation !).\n"
        "🤝 Égalité ? Rejouez aussitôt vos gestes, la cagnotte reste sur la table.\n"
        "⏱ Chaque geste : <b>{move_timeout} secondes</b> ; si tu ne joues pas, le générateur aléatoire choisira pour toi.\n"
        "🏆 Les victoires en duel comptent pour ton équipe dans les Batailles !\n\n"
        "👇 <b>CHOISIS UNE TABLE :</b>"
    ),
    "duel.btn_table": "⚔️ Table {stake} pièces",
    "duel.btn_cancel": "❌ Quitter la table (récupérer la mise)",
    "duel.btn_move_rock": "🪨 Pierre",
    "duel.btn_move_scissors": "✂️ Ciseaux",
    "duel.btn_move_paper": "🧻 Feuille",
    "duel.waiting": (
        "🪑 <b>Tu es à la table de {stake} pièces.</b> Ta mise est dans la cagnotte.\n"
        "On attend un deuxième combattant... Dès qu'il s'assoit, vous choisirez tous les deux votre geste !\n"
        "<i>La file d'attente dure {ttl} minutes, ensuite ta mise revient automatiquement.</i>"
    ),
    "duel.cancelled": "🚪 Tu as quitté la table. La mise de <b>{stake} pièces</b> est revenue sur ton solde.",
    "duel.expired": "⌛ Aucun adversaire ne s'est présenté à la table de {stake}. Ta mise de <b>{stake} pièces</b> a été remboursée.",
    "duel.matched": (
        "⚔️ <b>ADVERSAIRE TROUVÉ ! Table de {stake} pièces.</b>\n"
        "Cagnotte : <b>{bank} pièces</b> · Pour le gagnant : <b>{payout}</b>\n\n"
        "⏱ Tu as <b>{timeout} secondes</b> pour choisir ton geste !"
    ),
    "duel.move_saved": "✊ Geste enregistré ! On attend le geste de l'adversaire...",
    "duel.draw_replay": (
        "🤝 <b>ÉGALITÉ ! Manche {round}.</b> Vous avez montré le même geste.\n"
        "La cagnotte reste sur la table. ⏱ Encore {timeout} secondes — choisis ton geste :"
    ),
    "duel.win": (
        "🏆 <b>LE DUEL EST À TOI !</b>\n\n"
        "Ton geste {winner_move} bat {loser_move}.\n"
        "💰 Gains : <b>+{payout} pièces</b> · 🔥 Parti en fumée : {burned}\n"
        "💼 Solde : <b>{balance} pièces</b>"
    ),
    "duel.lose": (
        "💀 <b>DUEL PERDU.</b>\n\n"
        "Le geste {winner_move} de l'adversaire bat ton geste {loser_move}.\n"
        "📉 Ta mise de <b>{stake} pièces</b> est partie dans la cagnotte du gagnant.\n"
        "Une revanche ?"
    ),
    "duel.reaper_prefix": "⏰ <b>Temps de la manche écoulé !</b> Les gestes manquants ont été choisis par le générateur aléatoire.\n\n",
    "duel.bad_table": "❌ Cette table n'existe pas.",
    "duel.already_in": "⚠️ Tu es déjà à une table ou en plein combat ! Termine d'abord ton duel en cours.",
    "duel.no_coins": "❌ Il te faut {stake} pièces sur ton solde pour cette table.",
    "duel.cancel_impossible": "⚠️ Cette file ne peut plus être annulée (un adversaire a été trouvé ou la table est fermée).",
    "duel.not_active": "⌛ Ce duel est déjà terminé.",
    "duel.not_participant": "🔒 Ce n'est pas ton duel !",
    "duel.move_already": "✋ Tu as déjà montré ton geste dans cette manche. On attend l'adversaire !",
    "duel.bad_move": "❌ Geste inconnu.",
    "duel.btn_rematch": "⚔️ Revanche (vers les tables)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID : <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 Grade : <b>{rank}</b>\n",
    "rank.rookie": "Débutant",
    "rank.fighter": "Combattant",
    "rank.legend": "Légende",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.dead": "DEAD",

    # ---------------- parrainage ----------------
    "ref.text": (
        "🤝 <b>PROGRAMME DE PARRAINAGE ROFL HUB</b>\n"
        "..................................................\n\n"
        "Invite des amis et reçois <b>+{bonus} pièces</b> pour chaque ami "
        "qui s'inscrit via ton lien personnel !\n\n"
        "🔗 <b>Ton lien (tape pour copier) :</b>\n<code>{link}</code>\n\n"
        "📊 <b>TES STATISTIQUES :</b>\n"
        "👥 Amis invités : <b>{invited}</b>\n"
        "💰 Gagné grâce aux filleuls : <b>{earned} pièces</b>\n\n"
        "..................................................\n"
        "<i>Balance le lien dans les chats de classe, à tes amis et sur les réseaux — plus la bande est grande, plus ton solde grimpe vite !</i>"
    ),
    "ref.btn_share": "📣 Partager le lien",
    "ref.share_text": "Rejoins l'écosystème de jeu ROFL HUB !",
    "ref.qualified_line": ("⭐ <b>Double récompense :</b> quand un ami invité joue {rounds} "
                           "manches, tu reçois encore <b>+{bonus} pièces</b> !"),
    "ref.qualified_notify": ("🤝 <b>Ton ami est accro : déjà {rounds} manches !</b>\n"
                             "Tu gagnes <b>+{bonus} pièces</b> pour un filleul qualifié. "
                             "Invites-en d'autres !"),

    # ---------------- transferts ----------------
    "tr.help": (
        "🔄 <b>ENVOI DE PIÈCES À UN AUTRE JOUEUR</b>\n"
        "..................................................\n\n"
        "Format de la commande :\n"
        "<code>/transfer ID montant</code> — par ID de Passeport (visible dans /profile)\n"
        "<code>/transfer @username montant</code> — par nom d'utilisateur\n"
        "<code>/transfer ROFL-HUB-777 montant</code> — par un VIP ID d'enchères\n\n"
        "Exemples :\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Montant minimum : <b>{min} pièces</b>"
    ),
    "tr.not_found": "❌ Destinataire introuvable. Vérifie l'ID de Passeport ou le @username — le joueur doit être inscrit dans le bot.",
    "tr.self": "🤨 Impossible de t'envoyer des pièces à toi-même — ce serait une économie perpétuelle !",
    "tr.blocked": "🚫 Ce joueur est bloqué — les transferts vers lui sont indisponibles.",
    "tr.min": "❌ Le montant minimum du transfert est de {min} pièces.",
    "tr.insufficient": "❌ Pas assez de pièces ! Ton solde : <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Pas assez de pièces sur ton solde.",
    "tr.confirm": (
        "🔄 <b>CONFIRME LE TRANSFERT :</b>\n\n"
        "👤 Destinataire : <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Montant débité : <b>{amount} pièces</b>{fee_line}\n"
        "💰 Le destinataire recevra : <b>{received} pièces</b>\n\n"
        "<i>Les transferts sont irréversibles — vérifie bien le destinataire !</i>"
    ),
    "tr.fee_line": "\n🔥 Commission du hub : <b>{fee} pièces</b> (brûlée)",
    "tr.btn_confirm": "✅ CONFIRMER LE TRANSFERT",
    "tr.btn_cancel": "❌ Annuler",
    "tr.cancelled_toast": "Transfert annulé",
    "tr.cancelled": "❌ <b>Transfert annulé.</b> Tes pièces n'ont pas bougé.",
    "tr.not_yours": "🔒 Ce n'est pas ton transfert !",
    "tr.done_toast": "✅ Transfert effectué !",
    "tr.done": (
        "✅ <b>TRANSFERT EFFECTUÉ !</b>\n\n"
        "💸 Envoyé : <b>{amount} pièces</b> au joueur ID <code>{recipient_id}</code>\n"
        "💰 Ton solde : <b>{balance} pièces</b>"
    ),
    "tr.received": (
        "💰 <b>Tu as reçu {amount} pièces !</b>\n"
        "Expéditeur : ID <code>{sender_id}</code>. Ton solde est déjà crédité — vérifie /profile !"
    ),

    # ---------------- boutique & paiements ----------------
    "shop.header": "🏪 <b>BOUTIQUE ROFL HUB</b>\nLes achats passent par les Telegram Stars officiels. Choisis une catégorie avec les boutons en bas.",
    "shop.cat_farm": (
        "🚜 <b>BOUTIQUE · POUR LA FERME</b>\n"
        "..................................................\n"
        "Robots pour 30 jours, carburant, frigos, boosts et le Maître-Drone.\n"
        "📦 Ton frigo actuellement : <b>{capacity} côtelettes</b>\n"
        "..................................................\n"
        "👇 <b>Choisis un article :</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>BOUTIQUE · JEUX</b>\n"
        "..................................................\n"
        "Levée des limites de victoires, packs de pièces et licence Méga-Clan.\n"
        "..................................................\n"
        "👇 <b>Choisis un article :</b>"
    ),
    "pay.invoice_desc": "Livraison instantanée du contenu en jeu de ROFL HUB.",
    "pay.invoice_error": "⚠️ Impossible de créer la facture Telegram Stars. Réessaie plus tard.",
    "pay.success": "🎉 <b>Paiement confirmé !</b>\n🧾 <code>{charge}</code>\n💵 Débité : <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 Le paiement est passé, mais la livraison a temporairement échoué. On est déjà dessus.\n"
        "Garde le numéro de paiement : <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Tes Stars ont été remboursées automatiquement.",
    "pay.keep_charge": "Garde le numéro de paiement pour un remboursement : <code>{charge}</code>",
    "pay.already": "✅ Ce paiement a déjà été traité, l'article a été livré plus tôt.",
    "pay.support": (
        "🛟 <b>ASSISTANCE PAIEMENTS TELEGRAM STARS</b>\n"
        "..................................................\n\n"
        "Tous les articles ROFL HUB sont numériques et livrés instantanément après paiement.\n\n"
        "⚙️ <b>Si le paiement est passé mais l'article n'est pas arrivé :</b>\n"
        "le bot rembourse automatiquement les Stars en cas d'échec de livraison. Si ce n'est pas le cas, "
        "envoie ici le numéro de paiement (il figure sur le reçu, format <code>xxxx...</code>) et décris le problème. "
        "L'administration vérifiera le paiement dans la base et réglera la question sous 24 heures.\n\n"
        "💫 <b>Politique de remboursement :</b>\n"
        "un remboursement est possible si l'article n'a pas été reçu ou a été livré avec une erreur. "
        "Les articles numériques correctement livrés ne sont pas remboursables.\n\n"
        "..................................................\n"
        "<i>Cette section est le point d'assistance officiel pour les achats, conformément aux règles de Telegram.</i>"
    ),

    # ---------------- livraison ----------------
    "dlv.cutlets": "🥩 Ajouté à l'inventaire : <b>{qty} côtelettes</b>.",
    "dlv.miner": "🤖 Le robot <b>« {name} »</b> a été livré à ta ferme.\n⏳ Durée de service : jusqu'au <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robot Mineur",
    "dlv.miner_premium": "Cyber-Foreur",
    "dlv.fridge": "📦 Frigo agrandi à <b>{capacity} côtelettes</b>.",
    "dlv.coins": "💰 Crédité <b>+{amount} pièces</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nucléaire x5 actif jusqu'au <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Refroidissement à l'Azote +40% actif jusqu'au <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Le Maître-Drone protège ta ferme jusqu'au <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limites de victoires levées jusqu'au <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Ton équipe a reçu le statut <b>MÉGA-CLAN</b> : jusqu'à {max} places.",
    "dlv.err_fridge": "Tu as déjà un frigo de cette taille ou plus grand.",
    "dlv.err_no_team": "Tu n'as pas encore créé d'équipe. Crée-la d'abord via /create_team.",
    "dlv.err_mega": "Ton équipe a déjà le statut Méga-Clan.",
    "dlv.intern_upgrade": "♾ Ton Robot Stagiaire est promu <b>Robot Mineur ÉTERNEL</b> : 5 pièces par heure, sans expiration !",
    "dlv.err_no_intern": "Aucun Robot Stagiaire activé : active-le d'abord dans /farm.",
    "dlv.err_intern_refs": "L'amélioration exige {need} amis qualifiés (30 manches chacun) ; tu en as {have}.",
    "mk.header": "📈 <b>BOURSE DES CÔTELETTES</b>\n..................................................\n\nOrdres ouverts : <b>{orders}</b> · côtelettes en vente : <b>{cutlets}</b> · meilleur prix : <b>{best}</b>\nCommission du hub : <b>{fee}%</b> par vente (brûlée — bouclier anti-inflation)\n🥩 Dans ton entrepôt : <b>{inv}</b> côtelettes\n\n{body}\n\n<i>Touche un ordre pour acheter. Pour vendre : /sell.</i>",
    "mk.empty": "Aucune offre pour l'instant. Sois le premier : /sell quantité prix",
    "mk.order_line": "🥩 #{id} · <b>{qty} pcs</b> à <b>{price}</b> pièces",
    "mk.btn_order": "🛒 #{id} : {qty} pcs à {price} pièces",
    "mk.btn_my": "📋 Mes ordres",
    "mk.btn_sell_help": "💰 Comment vendre",
    "mk.btn_refresh": "🔄 Actualiser",
    "mk.btn_back": "← Retour à la bourse",
    "mk.pick": "🛒 <b>Ordre #{id}</b> : {qty} pcs disponibles à {price} pièces.\nCombien ?",
    "mk.btn_qty": "{qty} pcs — {total} pièces",
    "mk.btn_qty_all": "Tout, {qty} pcs — {total} pièces",
    "mk.buy_toast": "Affaire conclue !",
    "mk.buy_done": "✅ Acheté <b>{qty} côtelettes</b> pour <b>{total} pièces</b>. Elles sont dans ton entrepôt : ravitaille tes Foreuses !",
    "mk.sold_notify": "💰 <b>Bourse : vendu !</b> Ordre #{id} : {qty} pcs à {price}. Tu reçois <b>+{got} pièces</b> (commission de {fee} brûlée).",
    "mk.sell_help": "💰 <b>COMMENT VENDRE DES CÔTELETTES</b>\n\nCommande : <code>/sell quantité prix</code>\nExemple : <code>/sell 10 50</code> — 10 côtelettes à 50 pièces.\n\nLes côtelettes quittent l'entrepôt et attendent dans l'ordre (annulable à tout moment). Jusqu'à {max_qty} pcs par ordre et {max_orders} ordres ouverts. Une commission de {fee}% est brûlée à la vente.",
    "mk.sell_confirm": "📝 Mettre en vente <b>{qty} côtelettes</b> à <b>{price}</b> pièces ?\nTotal : {total} · commission {fee} brûlée · tu recevras <b>{got} pièces</b>.",
    "mk.btn_confirm_sell": "✅ METTRE EN VENTE",
    "mk.btn_cancel": "❌ Annuler",
    "mk.sell_toast": "Ordre publié !",
    "mk.sell_done": "✅ Ordre <b>#{id}</b> en ligne : {qty} pcs à {price} pièces. Je te préviens dès la vente.",
    "mk.cancelled_toast": "Annulé",
    "mk.cancel_text": "❌ <b>Annulé.</b> Les côtelettes restent dans ton entrepôt.",
    "mk.my_header": "📋 <b>TES ORDRES</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} pcs à {price} pièces",
    "mk.my_empty": "📋 Tu n'as aucun ordre ouvert.",
    "mk.btn_cancel_order": "❌ Retirer l'ordre #{id}",
    "mk.order_cancelled": "↩️ Ordre #{id} retiré : <b>{qty} côtelettes</b> de retour dans l'entrepôt.",
    "mk.err_qty": "❌ Quantité : de 1 à {max} côtelettes par ordre.",
    "mk.err_price": "❌ Prix : de {min} à {max} pièces la côtelette.",
    "mk.err_no_cutlets": "❌ Seulement {have} côtelettes dans l'entrepôt. Celles du frigo ne se vendent pas — voir /farm.",
    "mk.err_too_many": "❌ Limite : {max} ordres ouverts maximum. Retire-en un dans « Mes ordres ».",
    "mk.err_not_found": "❌ Cet ordre est déjà clos.",
    "mk.err_own": "🤨 Tu ne peux pas acheter ton propre ordre.",
    "mk.err_insufficient": "❌ Pas assez de pièces : il en faut {total}.",
    "farm.btn_market": "📈 Bourse des côtelettes",

    # ---------------- équipes/clans (surfaces principales) ----------------
    "clan.no_team": "⚠️ <b>Tu n'as pas encore d'équipe !</b>\n\nTu peux enregistrer ta propre bande dès maintenant en tapant sur le bouton ci-dessous.",
    "clan.btn_create": "🏆 Créer une Équipe pour 100k",
    "clan.btn_members": "👥 LISTE DES COÉQUIPIERS",
    "clan.btn_leave": "🚪 Quitter l'équipe / Lâcher la bande",
    "clan.btn_dashboard": "🏆 Tableau de bord",
    "clan.status_clan": "👑 STATUT : CLAN IMPÉRIAL",
    "clan.status_team": "👥 STATUT : ÉQUIPE STANDARD",
    "clan.dashboard": (
        "🏆 <b>TABLEAU DE BORD DE TON ÉQUIPE</b>\n"
        "..................................................\n\n"
        "📌 Nom : <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Capitaine de la bande : 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Devise : <i>« {motto} »</i>\n"
        "🔮 Symbole de l'emblème : {symbol}\n\n"
        "👥 Effectif : <b>{members} / {max_members}</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVIGATION :</b>"
    ),
    "clan.members_only": "🔒 La liste des membres n'est visible que par les membres de cette équipe !",
    "clan.members_gone": "❌ Cette équipe a déjà été dissoute.",
    "clan.members_header": (
        "👥 <b>EFFECTIF DE L'ÉQUIPE « {name} »</b>\n"
        "🧠 — niveau d'intelligence de jeu (progresse uniquement dans /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
        "📄 Page <b>{page} / {pages}</b> · Total de combattants : <b>{members}</b>\n"
        "<i>Tape sur le @username d'un coéquipier pour lui écrire, monter ton propre chat "
        "et appeler la bande aux compétitions d'équipe !</i>"
    ),
    "clan.btn_prev": "⬅️ Retour",
    "clan.btn_next": "Suivant ➡️",
    "clan.join_ok": (
        "🎉 <b>FÉLICITATIONS, TU ES DANS LA PARTIE !</b>\n\nTu as rejoint l'équipe <b>{name}</b> !\n"
        "📍 Tape /my_team pour vérifier l'effectif !"
    ),
    "clan.leave_ok": "🚪 Tu as quitté l'équipe <b>{name}</b>. Te voilà libre comme l'air !",
}

MINIAPP = {
    "subtitle": "ton empire de jeu sur un seul écran",
    "passport": "📋 PASSEPORT DU JOUEUR",
    "coins": "pièces",
    "brain": "🧠 Niveau d'intelligence",
    "toNext": "jusqu'au niveau {n} : {left} bonnes réponses au quiz (+{reward} pièces)",
    "farm": "🚜 CYBER-FERME",
    "robots": "Robots (mineurs / foreurs)",
    "fueled": "Foreurs ravitaillés",
    "speed": "Vitesse de minage",
    "perHour": "{v} pièces/heure",
    "fridge": "Frigo",
    "inv": "Côtelettes en stock",
    "burnout": "Prochaine expiration",
    "intern": "Robots Stagiaires (1 pièce/h, éternels)",
    "activateIntern": "🚀 ACTIVER LE ROBOT STAGIAIRE",
    "internDone": "🤖 Ton Robot Stagiaire prend son poste !",
    "rank": "🎖 Grade",
    "openFarm": "🏭 OUVRIR LA FERME",
    "farmScene": "🏭 TA FERME",
    "back": "← Retour",
    "minedVisit": "miné pendant cette visite",
    "unit_intern": "Robot Stagiaire",
    "unit_junior": "Robot Mineur",
    "unit_premium": "Cyber-Foreuse",
    "eternal": "éternel",
    "fueledAll": "ravitaillés",
    "fueledPart": "{a} sur {b} ravitaillés",
    "license": "licence 30 jours",
    "emptyFarm": "La mine est vide. Active ton Robot Stagiaire ou achète des robots dans la boutique !",
    "madeBy": "Tu veux un bot comme celui-ci pour ton projet ? Écris à @mister_telebot",
    "boosts": "Boosts actifs",
    "none": "aucun",
    "bonusReady": "🎁 RÉCUPÉRER LA CÔTELETTE DU JOUR",
    "bonusWait": "⏳ Bonus dans {h} h {m} min",
    "bonusDone": "🎉 Côtelette ajoutée !",
    "team": "🏆 MON ÉQUIPE",
    "clan": "CLAN",
    "teamLabel": "Équipe",
    "captain": "👑 Tu es capitaine !",
    "members": "Effectif",
    "noTeam": "Pas encore d'équipe — monte ta bande dans le chat du bot !",
    "top": "👑 TOP-100 DES PLUS RICHES DE L'ÉCOSYSTÈME",
    "shop": "🏪 BOUTIQUE",
    "shopFarm": "🚜 POUR LA FERME",
    "shopGames": "🕹️ JEUX",
    "shopHint": "Paiement via les Telegram Stars officiels — ici même, en un tap.",
    "paid": "🎉 Payé ! L'article est déjà sur ton compte.",
    "payFail": "Le paiement n'est pas passé. Réessaie.",
    "oldClient": "Mets à jour Telegram pour acheter depuis la Mini App, ou ouvre la boutique dans le chat du bot.",
    "ctaNoRobots": "💤 Ta ferme est vide ! Adopte ton premier robot — les pièces tomberont 24h/24.",
    "ctaHungry": "🚨 Les Foreurs ont faim ({n} sans carburant) — le minage est à l'arrêt !",
    "ctaLowFuel": "⚠️ Moins de côtelettes qu'il n'en faut pour une journée de travail des Foreurs.",
    "ctaShopBtn": "🛒 Vers la boutique",
    "footer": "Contrôle complet — dans le chat du bot : /menu",
    "noProfile": "Profil introuvable. Ouvre le bot et appuie sur /start !",
    "blocked": "Compte bloqué par l'administration.",
    "error": "Impossible de charger les données. Réessaie plus tard.",
    "outside": "Ouvre cette application depuis le bot Telegram ROFL HUB.",
}

COMMANDS = {
    "app": "🎮 Ouvrir la Mini App",
    "menu": "📱 Menu principal",
    "profile": "👤 Mon profil et passeport",
    "farm": "🚜 Cyber-ferme et ravitaillement",
    "shop": "🏪 Boutique (Telegram Stars)",
    "games": "🕹️ Tous les jeux contre le bot",
    "quiz": "🧠 Quiz : 15 secondes par réponse",
    "duel": "⚔️ Duel 1 contre 1 avec mise",
    "quests": "🗺️ Quêtes : histoires à choix",
    "my_team": "🏆 Mon équipe et mes coéquipiers",
    "invite": "🤝 Lien de parrainage : +1000 par ami",
    "transfer": "🔄 Envoyer des pièces à un joueur",
    "market": "📈 Bourse des côtelettes : acheter ou vendre",
    "sell": "💰 Vendre des côtelettes : /sell quantité prix",
    "my_stats": "📊 Mes statistiques",
    "faq": "📚 Questions fréquentes",
    "rules": "📜 Conditions d'utilisation",
    "paysupport": "🛟 Assistance paiements",
}
