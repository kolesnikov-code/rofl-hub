"""Французская локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> pièces
# Младший Майнер -> Robot Mineur
# Кибер-Бурильщик -> Cyber-Foreur
# кибер-котлета -> cyber-côtelette (кратко: côtelette)
# Холодильник -> Frigo
# склад (инвентарь) -> stock (единый термин; не «entrepôt»/«inventaire»)
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
# ресурсы: Металл -> Métal; Водород -> Hydrogène; Кристаллы -> Cristaux; Детали -> Composants
#   (не «pièces» — это монеты)
# Мастерская -> Atelier; Кибер-броня -> Cyber-Armure; Шаттл -> Navette (ж.р.: assemblée)
# Налёт -> Raid; вылет -> vol; Стойка обороны -> Posture de défense; Разведка -> Reconnaissance (кнопка: RECO)
# Реванш -> Revanche; Щит -> Bouclier (anti-raids); Сундук -> Coffret (не Coffre — это Кибер-Сейф)
# Серия -> Série; Станция команды -> Station d'équipe; биржа котлет -> Bourse des côtelettes

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
    'duel.invite_msg': '⚔️ <b>{name}</b> te défie en duel !\nMise {stake} 🪙, le gagnant remporte {payout} 🪙. Le défi est valable {hours} h.',
    'duel.invite_btn': '⚔️ Relever le défi',
    'duel.invite_gone': '⌛ Ce défi n’est plus valable : il a été accepté, annulé ou a expiré.',
    'duel.invite_self': '😅 C’est ton propre défi — envoie le lien à un ami.',
    'team.err_not_squad': '⚠️ Seule une escouade peut être agrandie.',
    'team.err_not_captain': '⚠️ Seul le capitaine peut le faire.',
    "quest.epic_locked": "⭐ Les épopées sont de grandes histoires de 20+ minutes — elles s’ouvrent avec ⚡ Illimité.",
    "quest.locked": "🔒 Tu as fait tes {n} nouvelles quêtes du jour. Les autres s’ouvrent à 00:00 UTC — ou active ⚡ Illimité. Les quêtes terminées se rejouent.",
    # 27.10: «чат — дверь и почтальон», вся игра в приложении
    "app.moved": "🎮 Cette section est désormais dans l'appli du jeu — plus pratique et plus belle. Appuie sur le bouton 👇",
    "app.keyboard_gone": "🧹 Les anciens boutons du bas ont disparu : tout le jeu est désormais dans l'appli. Tu peux aussi l'ouvrir avec le bouton «🎮 ROFL HUB» à côté du champ de saisie.",
    "start.console_app": "🚀 <b>C'est prêt !</b> Tout le jeu est dans l'appli : appuie sur le bouton ci-dessous. Ensuite, tu pourras toujours l'ouvrir avec le bouton «🎮 ROFL HUB» à côté du champ de saisie.",
    "start.welcome_back_app": "👋 <b>Re-bonjour, @{username} !</b> Ta progression est intacte — ouvre le jeu 👇",
    "menu.app": "📱 <b>ROFL HUB</b>\nTout le jeu est dans l'appli 👇\n\n<b>Dans le chat:</b>\n• /invite — inviter un ami\n• /transfer — envoyer des pièces\n• /faq — questions fréquentes\n• /rules — conditions d'utilisation\n• /paysupport — aide aux paiements\n• /delete_account — supprimer le compte",
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
        "💸 Tu as reçu <b>{balance} 🪙</b>\n"
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
        "..................................................\n"
        "👤 <b>PROFIL PERSONNEL ET PASSEPORT :</b>\n"
        "• /start — Commencer l'intro et créer un compte\n"
        "• /profile — Ton passeport, ton solde et ton équipe en temps réel\n"
        "• /my_stats — Tes statistiques des 30 derniers jours\n\n"
        "🚜 <b>CYBER-FERME ET AUTOMATISATION :</b>\n"
        "• /farm — Hub carburant : ravitaillement et vitesse de production des robots\n"
        "• /shop — Boutique : achat de mineurs, de côtelettes et d'améliorations du hub\n\n"
        "🕹️ <b>SALLE DE JEU :</b>\n"
        "• /games — Hub inline de tous les jeux contre le bot\n"
        "• /quiz — Quiz de vitesse : 30 secondes par réponse, niveaux et bonus\n"
        "• /duel — DUELS 1 contre 1 avec de vrais joueurs : tables 10/100/1000\n"
        "• /quests — QUÊTES : polars, comédies et énigmes avec récompenses\n"
        "• /rps, /high_low, /safe — Jeux rapides pour des pièces\n\n"
        "👥 <b>GESTION DE TA BANDE :</b>\n"
        "• /create_team — Enregistrer ta propre équipe pour 100 000 🪙\n"
        "• /my_team — Tableau de bord de la bande et LISTE DES COÉQUIPIERS avec niveaux 🧠\n"
        "• /all_teams — Roulette d'équipes aléatoires\n\n"
        "💸 <b>ARGENT ET AMIS :</b>\n"
        "• /invite — Ton lien de parrainage : +500 🪙 par ami actif\n"
        "• /transfer — Envoyer des pièces à un autre joueur\n\n"
        "📚 <b>AIDE ET RÈGLES :</b>\n"
        "• /faq — Le guide complet de l'écosystème (s'ouvre dans la Mini App)\n"
        "• /rules — Conditions d'utilisation\n"
        "..................................................\n"
        "<i>⚙️ Utilise le panneau de jeu permanent à deux colonnes en bas de l'écran pour naviguer instantanément !</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>BIENVENUE DANS LA ZONE DE JEU ROFL HUB !</b>\n"
        "..................................................\n"
        "Ici tu peux affronter le bot en duels rapides ou passer le sprint-test "
        "intellectuel pour décrocher le jackpot — ou tout perdre !\n\n"
        "💸 Une victoire rapporte : <b>+2 🪙</b> (Cyber-Coffre : <b>+5</b>)\n"
        "💀 Une défaite ou une égalité coûte : <b>-1 🪙</b>\n"
        "🧠 Au Quiz, chrono de 30 secondes et niveaux d'intelligence : le niveau 1, c'est 10 bonnes réponses et <b>+100 🪙</b>, "
        "chaque niveau suivant est plus long de 10 réponses, mais la récompense grimpe de 100 !\n"
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
        "..................................................\n"
        "L'essentiel en bref :\n"
        "🚜 Les robots minent des pièces 24h/24 : Robot Mineur — 5/h sans carburant, "
        "Cyber-Foreur — 10/h, et CHAQUE Foreur mange sa propre cyber-côtelette par jour. "
        "Tous les robots vivent 30 jours (le Maître-Drone met l'usure en pause).\n"
        "🧠 Quiz : 30 secondes par réponse, niveaux d'intelligence aux récompenses croissantes.\n"
        "⚔️ Duels contre de vrais joueurs aux tables de 10/100/1000 🪙.\n"
        "🏆 Équipes jusqu'à 50 combattants (Méga-Clan — jusqu'à 1000) et Batailles événementielles avec des prix pour tous.\n"
        "..................................................\n"
        "👇 <b>Le guide complet avec toutes les mécaniques — en un tap :</b>"
    ),
    "faq.btn_open": "📖 OUVRIR LE GUIDE COMPLET",
    "rules.teaser": (
        "📜 <b>CONDITIONS D'UTILISATION DE ROFL HUB</b>\n"
        "..................................................\n"
        "L'essentiel en deux mots :\n"
        "🪙 Les pièces et tous les objets du jeu sont des éléments virtuels de divertissement : "
        "ce n'est pas de l'argent et ils ne s'échangent pas contre des fonds réels.\n"
        "💫 Les achats passent uniquement par les Telegram Stars officiels ; les articles numériques "
        "sont livrés instantanément, et les Stars sont remboursées automatiquement si la livraison échoue.\n"
        "🛡️ Nous ne collectons ni numéros de téléphone, ni géolocalisation, ni données personnelles.\n"
        "🤝 Insultes, triche et multi-comptes sont interdits — toute violation peut mener à un blocage.\n"
        "..................................................\n"
        "👇 <b>Le texte complet des conditions et la clause de non-responsabilité — en un tap :</b>\n"
        "<i>⚖️ En utilisant le bot, tu acceptes les conditions.</i>"
    ),
    "rules.btn_open": "📜 OUVRIR LES CONDITIONS COMPLÈTES",
    "quest.list_header": (
        "🗺️ <b>QUÊTES ROFL HUB</b>\n"
        "..................................................\n"
        "Des histoires interactives avec des choix et des embranchements : polars, comédies, énigmes. "
        "La première victoire dans chaque quête rapporte des pièces, et tu peux rejouer autant que tu veux !\n"
        "🌐 <i>Les histoires des quêtes sont en russe pour l'instant — le pack en français arrive.</i>\n\n"
        "👇 <b>Choisis une histoire :</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} 🪙 pour la première victoire\n"
        "..................................................\n"
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
    "quest.win_first": "\n\n🏆 <b>QUÊTE TERMINÉE ! Récompense : +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>Terminée à nouveau !</b> La récompense de cette quête a déjà été récupérée.",
    "quest.fail_footer": "\n\n💀 <i>Pas la meilleure des fins... mais tu peux toujours rejouer l'histoire !</i>",
    "quest.stale": "⏳ Cette scène est déjà derrière toi — on reprend là où tu en es !",
    "quest.no_coins": "❌ L'indice coûte {cost} 🪙 et ton solde est plus bas. Fais un tour à la ferme !",
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
    "farm.status_no_drills": "💡 Prends un robot plus puissant dans /shop : ta ferme minera davantage.",
    "farm.boost_nuclear": "🔋 Boost Nucléaire x5 jusqu'à {until} UTC (consommation de côtelettes ×3)",
    "farm.boost_nitrogen": "❄️ Refroidissement à l'Azote +40% jusqu'à {until} UTC",
    "farm.boost_drone": "🛸 Le Maître-Drone prolonge la vie des robots jusqu'à {until} UTC",
    "farm.no_boosts": "Aucun boost actif — fais un tour dans /shop.",
    "farm.burnout": "🔥 Prochaine expiration de robot : <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Activer ton Robot Stagiaire (gratuit)",
    "farm.intern_activated": "🤖 Ton Robot Stagiaire prend son poste ! +1 🪙 par heure pour toujours, sans carburant ni expiration.",
    "farm.intern_already": "🤖 Ton Robot Stagiaire travaille déjà.",
    "farm.btn_claim_intern": "🎁 Récupérer le Robot Stagiaire ({n})",
    "farm.intern_pending": "🎁 Tes niveaux d'intelligence te valent des Robots Stagiaires : <b>{n}</b> — récupère-les avec le bouton ci-dessous !",
    "farm.intern_claimed_new": "🤖 Un nouveau Robot Stagiaire prend son poste ! +1 🪙 par heure pour toujours.",
    "farm.intern_none": "🤖 Pas de nouveau Stagiaire pour l'instant : le prochain t'attend au niveau d'intelligence 10, 20, 30…",
    "games.intern_ready": "🎁 Ton nouveau niveau te vaut un <b>Robot Stagiaire</b> : récupère-le dans ta ferme !",
    "farm.intern_line": "• Robots Stagiaires ({rate} 🪙/h, éternels) : <code>{count}</code>\n",
    "farm.intern_hint": "🎁 Tu as un Robot Stagiaire gratuit ! Appuie sur le bouton ci-dessous : il minera 1 🪙 par heure pour toujours.",
    "farm.dashboard": (
        "🚜 <b>HUB CARBURANT CENTRAL ROFL HUB</b>\n"
        "..................................................\n"
        "🤖 Robots actifs à l'usine : <b>{total}</b>\n"
        "{intern}• Robots Mineurs ({junior_rate} 🪙/h) : <code>{junior}</code>\n"
        "• Cyber-Foreurs ({premium_rate} 🪙/h) : <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VITESSE ACTUELLE DE TA FERME :</b>\n"
        "• Production par heure : <b>+{speed_hour} 🪙</b>\n"
        "• Production par jour : <b>+{speed_day} 🪙</b>\n\n"
        "⚡ <b>BOOSTS :</b>\n{boosts}\n\n"
        "📋 <b>ÉTAT DE L'USINE DE JEU :</b>\n"
        "{status}\n"
        "..................................................\n"
        "📦 <b>ÉTAT DU FRIGO AUTOMATIQUE :</b>\n"
        "🥩 Réserve de carburant : <b>{fridge} / {capacity}</b>\n"
        "💼 Côtelettes en stock : <code>{inv}</code>\n"
        "..................................................\n"
        "<i>💿 Important : les robots vivent 30 jours (le Maître-Drone met l'usure en pause). "
        "CHAQUE Cyber-Foreur consomme SA propre côtelette entière du frigo toutes les "
        "24 heures de travail : 3 robots — 3 côtelettes par jour. Surveille le ravitaillement !</i>"
    ),
    "farm.bonus_ok": "🎁 Cyber-côtelette ajoutée au stock ! Reviens dans 24 heures.",
    "farm.bonus_wait": "⏳ Bonus déjà récupéré ! Prochaine côtelette dans {hours} h {minutes} min.",
    "farm.no_inv_cutlets": "❌ Tu n'as pas de cyber-côtelettes dans ton stock ! Achètes-en dans /shop",
    "farm.fridge_full": "📦 Ton Frigo est déjà plein à craquer !",

    # ---------------- profil ----------------
    "profile.caption": (
        "📋 <b>ESPACE PERSONNEL DU JOUEUR ROFL HUB</b>\n"
        "..................................................\n"
        "🆔 Ton ID de Passeport : <code>{user_id}</code>\n"
        "{vip}"
        "💰 Pièces actuellement : <b>{balance} 🪙</b>\n"
        "🏆 Ton statut : <b>{team}</b>\n"
        "🧠 Niveau d'intelligence : <b>{level}</b> · jusqu'au niveau {next_level} : "
        "<b>{left}</b> bonnes réponses dans /quiz (récompense : +{reward} 🪙)\n"
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
        "..................................................\n"
        "🧠 Niveau d'intelligence de jeu : <b>{level}</b> (total de bonnes réponses : {total})\n"
        "🎮 Manches de duel jouées : <b>{played}</b>\n"
        "🏆 Victoires remportées : <code>{won}</code>\n"
        "👥 Amis actifs invités : <b>{refs}</b>\n"
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
    "games.win": "🎉 <b>VICTOIRE !</b> 🎉\nCrédité : <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>DÉFAITE !</b>\nDébité : <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>ÉGALITÉ !</b>\nDébité : <b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>Limite quotidienne atteinte !</b>\n\n"
        "Tu as déjà remporté {limit} victoires au jeu « {game} » aujourd'hui. La limite se réinitialise à 00:00 UTC.\n\n"
        "⚡ Lever la limite pour 24 heures — 15 ★, pour 30 jours — 249 ★ (section « Jeux » dans /shop)."
    ),
    "games.no_coins": "❌ Tu as 0 🪙 — impossible de payer les frais de la manche. Récupère les revenus de ta ferme dans /farm !",
    "games.balance": "💰 Solde : <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 Rejouer !",
    "games.btn_hub": "🕹️ Zone de jeu",
    "games.level_up": (
        "🏅 <b>NIVEAU D'INTELLIGENCE AUGMENTÉ : {level} !</b> Récompense : <b>+{bonus} 🪙</b> !\n"
        "Niveau suivant : {next_required} bonnes réponses → +{next_reward} 🪙."
    ),
    "games.name.rps": "Pierre-Feuille-Ciseaux",
    "games.intern_bonus": "🤖 Niveau {level} ! Un nouveau Robot Stagiaire rejoint ta ferme : tu en as maintenant {count}.",
    "games.name.hl": "Plus/Moins",
    "games.name.quiz": "Quiz",
    "games.name.safe": "Coffre",
    "games.name.math": "Math",  # TODO(перевод 26.10)
    "games.name.flags": "Flags and capitals",  # TODO(перевод 26.10)
    "games.name.code": "Code breaker",  # TODO(перевод 26.10)
    "games.name.memory": "Memory",  # TODO(перевод 26.10)

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
    "quiz.lost_line": "💀 <b>-{penalty} 🪙</b> pour la défaite !",
    "quiz.level_line": (
        "🧠 Niveau d'intelligence : <b>{level}</b>\n"
        "Victoires restantes jusqu'au niveau {next_level} : <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} secondes pour répondre !\n"
        "Correct : +{win} 🪙 sur ton solde\n"
        "Erreur / temps écoulé : -{penalty} 🪙\n"
        "Limite : {limit} victoires par jour</i>"
    ),



    # ---------------- Coffre ----------------
    "safe.intro": (
        "🔐 <b>CYBER-COFFRE</b>\n\n"
        "À l'intérieur : un jackpot de <b>{jackpot} 🪙</b> ! La porte est verrouillée par un code de 1 à {codes}. "
        "Tu as une seule tentative.\n"
        "Ouvert : <b>+{jackpot}</b> · Alarme : <b>-{penalty}</b> · Limite : <b>{limit}</b> victoires"
    ),
    "safe.btn_retry": "🔐 Craquer encore une fois !",
    "safe.win": "🔓 <b>Coffre ouvert !</b> Le code était : <b>{code}</b>.",
    "safe.lose": "🚨 <b>L'alarme s'est déclenchée !</b> Tu as tapé {guess}, et le code était : <b>{code}</b>.",

    # ---------------- duels ----------------
    "duel.intro": (
        "⚔️ <b>DUELS 1 CONTRE 1 : PIERRE-FEUILLE-CISEAUX AVEC MISE</b>\n"
        "..................................................\n"
        "Choisis une table selon ton budget — comme au poker. La mise est prélevée tout de suite, "
        "et ton adversaire est un vrai joueur ROFL HUB !\n\n"
        "💰 La cagnotte = les deux mises. Le gagnant prend <b>{payout_percent}%</b> de la cagnotte, "
        "<b>{burn_percent}%</b> part en fumée pour de bon (déflation !).\n"
        "🤝 Égalité ? Rejouez aussitôt vos gestes, la cagnotte reste sur la table.\n"
        "⏱ Chaque geste : <b>{move_timeout} secondes</b> ; si tu ne joues pas, le générateur aléatoire choisira pour toi.\n"
        "🏆 Les victoires en duel comptent pour ton équipe dans les Batailles !\n\n"
        "👇 <b>CHOISIS UNE TABLE :</b>"
    ),
    "duel.btn_table": "⚔️ Table {stake} 🪙",
    "duel.btn_cancel": "❌ Quitter la table (récupérer la mise)",
    "duel.btn_move_rock": "🪨 Pierre",
    "duel.btn_move_scissors": "✂️ Ciseaux",
    "duel.btn_move_paper": "🧻 Feuille",
    "duel.waiting": (
        "🪑 <b>Tu es à la table de {stake} 🪙.</b> Ta mise est dans la cagnotte.\n"
        "On attend un deuxième combattant... Dès qu'il s'assoit, vous choisirez tous les deux votre geste !\n"
        "<i>La file d'attente dure {ttl} minutes, ensuite ta mise revient automatiquement.</i>"
    ),
    "duel.cancelled": "🚪 Tu as quitté la table. La mise de <b>{stake} 🪙</b> est revenue sur ton solde.",
    "duel.expired": "⌛ Aucun adversaire ne s'est présenté à la table de {stake}. Ta mise de <b>{stake} 🪙</b> a été remboursée.",
    "duel.matched": (
        "⚔️ <b>ADVERSAIRE TROUVÉ ! Table de {stake} 🪙.</b>\n"
        "Cagnotte : <b>{bank} 🪙</b> · Pour le gagnant : <b>{payout}</b>\n\n"
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
        "💰 Gains : <b>+{payout} 🪙</b> · 🔥 Parti en fumée : {burned}\n"
        "💼 Solde : <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>DUEL PERDU.</b>\n\n"
        "Le geste {winner_move} de l'adversaire bat ton geste {loser_move}.\n"
        "📉 Ta mise de <b>{stake} 🪙</b> est partie dans la cagnotte du gagnant.\n"
        "Une revanche ?"
    ),
    "duel.reaper_prefix": "⏰ <b>Temps de la manche écoulé !</b> Les gestes manquants ont été choisis par le générateur aléatoire.\n\n",
    "duel.bad_table": "❌ Cette table n'existe pas.",
    "duel.already_in": "⚠️ Tu es déjà à une table ou en plein combat ! Termine d'abord ton duel en cours.",
    "duel.no_coins": "❌ Il te faut {stake} 🪙 sur ton solde pour cette table.",
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
    "rank.king": "KING",

    # ---------------- parrainage ----------------
    "ref.text": (
        "🤝 <b>PROGRAMME DE PARRAINAGE ROFL HUB</b>\n"
        "..................................................\n"
        "Invite des amis via ton lien personnel et reçois <b>{bonus}</b> "
        "pour chaque ami qui devient joueur actif !\n\n"
        "🔗 <b>Ton lien (tape pour copier) :</b>\n<code>{link}</code>\n\n"
        "📊 <b>TES STATISTIQUES :</b>\n"
        "👥 Amis invités : <b>{invited}</b>\n"
        "💰 Gagné grâce aux filleuls : <b>{earned} 🪙</b>\n"
        "..................................................\n"
        "<i>Balance le lien dans les chats de classe, à tes amis et sur les réseaux — plus la bande est grande, plus ton solde grimpe vite !</i>"
    ),
    "ref.btn_share": "📣 Partager le lien",
    "ref.share_text": "Rejoins l'écosystème de jeu ROFL HUB !",
    "ref.qualified_line": ("✅ <b>Un ami actif</b> est quelqu'un qui a atteint le <b>niveau d'intelligence {level}</b> "
                           "au quiz et récupéré <b>{claims} côtelettes quotidiennes</b> à la ferme. Alors tu gagnes <b>{bonus}</b>, "
                           "une seule fois par ami. Pas de bonus pour une simple inscription sans jeu : c'est plus juste pour tous."),
    "ref.qualified_notify": ("🤝 <b>Ton ami est devenu un joueur actif !</b>\n"
                             "Niveau d'intelligence {level} et {claims} côtelettes quotidiennes : c'est fait. Tu gagnes <b>{bonus}</b>. "
                             "Invites-en d'autres !"),

    "team.err_len": "❌ Le texte doit faire entre 1 et {max} caractères !",
    "team.err_link": "🚨 Alerte sécurité ! Les liens, pseudos et numéros de téléphone sont strictement interdits !",
    "team.err_badword": "❌ Propos grossiers détectés ! Respecte les règles du hub.",
    "team.err_already": "⚠️ Tu fais déjà partie d'une équipe ou d'un clan ! Quitte-le d'abord.",
    "team.err_money": "❌ Pas assez de pièces ! Créer une équipe coûte {cost} 🪙, tu as {balance} 🪙.",
    "team.err_captain": "⚠️ Tu es déjà capitaine d'une autre équipe !",
    "team.err_taken": "⚠️ Le nom « {name} » est déjà pris ! Trouve-en un unique.",
    "team.err_gone": "❌ Cette équipe n'existe plus.",
    "team.err_full": "📦 Cette équipe n'a plus de places libres !",
    "team.err_not_member": "❌ Tu ne fais partie d'aucune équipe.",
    "mk.err_no_team": "🏆 La bourse d'équipe est réservée aux membres d'une équipe. Rejoins une équipe ou crée la tienne.",
    "mk.err_team_only": "🔒 Cette offre est réservée aux membres de l'équipe du vendeur.",
    "help.err_qty": "Tu peux demander de 1 à {max} unités de ressource.",
    "help.err_open": "Tu as déjà une demande ouverte — attends de l'aide ou retire-la.",
    "help.err_not_found": "Cette demande est déjà clôturée.",
    "help.err_self": "Impossible de répondre à ta propre demande par un cadeau 🙂",
    "help.err_limit": "Aujourd'hui, tu as déjà offert {max} ressources — la limite se réinitialise à 00:00 UTC.",
    "help.err_not_active": "🔒 Tu peux offrir des ressources à partir du niveau d'intellect {level} et après {claims} côtelettes quotidiennes récupérées.",
    "it.err_none": "Cet objet n'est plus dans ton stock.",
    # ---------------- suppression du compte ----------------
    "profile.btn_delete": "🗑 Supprimer le compte",
    "acct.warn": (
        "⚠️ <b>SUPPRESSION DU COMPTE</b>\n"
        "..................................................\n"
        "Avec le compte, ces éléments disparaîtront <b>définitivement</b> :\n"
        "• pièces, côtelettes, ressources et tous les robots de la ferme ;\n"
        "• boosts, Illimité et tout ce qui a été acheté avec des Stars — <b>les Stars ne sont pas remboursées</b> ;\n"
        "• VIP ID, progression du quiz et des quêtes ;\n"
        "• ta place dans l'équipe (la capitainerie passe au vétéran de l'équipe).\n"
        "Les ordres ouverts sur la bourse sont retirés immédiatement, les biens retournent dans ton stock.\n\n"
        "⏳ Le compte sera d'abord gelé pendant <b>{days} jours</b> : tu peux changer d'avis d'un seul bouton. "
        "Ensuite, la suppression est irréversible. Si tu reviens plus tard, tu repars de zéro, et le bonus de départ n'est pas accordé une seconde fois.\n\n"
        "<i>Le bouton de suppression sera actif dans {seconds} secondes : lis bien.</i>"
    ),
    "acct.btn_keep": "✅ Non, garder mon compte",
    "acct.btn_confirm": "🗑 Oui, supprimer mon compte",
    "acct.wait": "⏳ Patiente encore {seconds} s : lis ce qui sera supprimé exactement.",
    "acct.kept": "👍 Parfait, ton compte reste avec toi !",
    "acct.scheduled": (
        "🗑 Le compte est gelé et sera supprimé le <b>{date}</b> (UTC).\n"
        "Les ordres de la bourse sont retirés, les biens sont revenus dans ton stock.\n\n"
        "Si tu changes d'avis, appuie sur le bouton ci-dessous : tout redeviendra comme avant."
    ),
    "acct.pending_notice": (
        "⏳ Le compte est gelé et sera supprimé le <b>{date}</b> (UTC).\n"
        "Tu veux rester dans le jeu ? Appuie sur le bouton ci-dessous."
    ),
    "acct.btn_undo": "↩️ Annuler la suppression",
    "acct.undone": "🎉 Suppression annulée : le compte est de nouveau à toi !",
    "acct.purged": "🗑 Ton compte ROFL HUB a été supprimé. Merci d'avoir joué ! Si tu veux revenir, appuie sur /start.",
    "acct.deleted_notice": "Le compte a été supprimé. Appuie sur /start pour recommencer.",
    "acct.welcome_back": (
        "👋 <b>Content de te revoir !</b>\n"
        "Le profil a été recréé de zéro. Le bonus de départ n'est accordé qu'une fois, donc ton solde est de 0 🪙. "
        "La ferme, les jeux et le quiz t'attendent !"
    ),
    "tr.err_not_active": (
        "🔒 Tu peux envoyer des pièces à partir du niveau d'intelligence {level} et après {claims} côtelettes quotidiennes récupérées : "
        "cela protège l'écosystème des faux comptes."
    ),

    # ---------------- transferts ----------------
    "tr.help": (
        "🔄 <b>ENVOI DE PIÈCES À UN AUTRE JOUEUR</b>\n"
        "..................................................\n"
        "Format de la commande :\n"
        "<code>/transfer ID montant</code> — par ID de Passeport (visible dans /profile)\n"
        "<code>/transfer @username montant</code> — par nom d'utilisateur\n"
        "<code>/transfer ROFL-HUB-777 montant</code> — par un VIP ID d'enchères\n\n"
        "Exemples :\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Montant minimum : <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ Destinataire introuvable. Vérifie l'ID de Passeport ou le @username — le joueur doit être inscrit dans le bot.",
    "tr.self": "🤨 Impossible de t'envoyer des pièces à toi-même — ce serait une économie perpétuelle !",
    "tr.blocked": "🚫 Ce joueur est bloqué — les transferts vers lui sont indisponibles.",
    "tr.min": "❌ Le montant minimum du transfert est de {min} 🪙.",
    "tr.insufficient": "❌ Pas assez de pièces ! Ton solde : <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ Pas assez de pièces sur ton solde.",
    "tr.confirm": (
        "🔄 <b>CONFIRME LE TRANSFERT :</b>\n\n"
        "👤 Destinataire : <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Montant débité : <b>{amount} 🪙</b>{fee_line}\n"
        "💰 Le destinataire recevra : <b>{received} 🪙</b>\n\n"
        "<i>Les transferts sont irréversibles — vérifie bien le destinataire !</i>"
    ),
    "tr.fee_line": "\n🔥 Commission du hub : <b>{fee} 🪙</b> (brûlée)",
    "tr.btn_confirm": "✅ CONFIRMER LE TRANSFERT",
    "tr.btn_cancel": "❌ Annuler",
    "tr.cancelled_toast": "Transfert annulé",
    "tr.cancelled": "❌ <b>Transfert annulé.</b> Tes pièces n'ont pas bougé.",
    "tr.not_yours": "🔒 Ce n'est pas ton transfert !",
    "tr.done_toast": "✅ Transfert effectué !",
    "tr.done": (
        "✅ <b>TRANSFERT EFFECTUÉ !</b>\n\n"
        "💸 Envoyé : <b>{amount} 🪙</b> au joueur ID <code>{recipient_id}</code>\n"
        "💰 Ton solde : <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>Tu as reçu {amount} 🪙 !</b>\n"
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
        "..................................................\n"
        "Tous les articles ROFL HUB sont numériques et livrés instantanément après paiement.\n\n"
        "⚙️ <b>Si le paiement est passé mais l'article n'est pas arrivé :</b>\n"
        "le bot rembourse automatiquement les Stars en cas d'échec de livraison. Si ce n'est pas le cas, "
        "envoie ici le numéro de paiement (il figure sur le reçu, format <code>xxxx...</code>) et décris le problème. "
        "L'administration vérifiera le paiement dans la base et réglera la question sous 24 heures.\n\n"
        "💫 <b>Politique de remboursement :</b>\n"
        "un remboursement est possible si l'article n'a pas été reçu ou a été livré avec une erreur. "
        "Les articles numériques correctement livrés ne sont pas remboursables.\n"
        "..................................................\n"
        "<i>Cette section est le point d'assistance officiel pour les achats, conformément aux règles de Telegram.</i>"
    ),

    # ---------------- livraison ----------------
    "dlv.cutlets": "🥩 Ajouté au stock : <b>{qty} côtelettes</b>.",
    "dlv.miner": "🤖 Le robot <b>« {name} »</b> a été livré à ta ferme.\n⏳ Durée de service : jusqu'au <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robot Mineur",
    "dlv.miner_premium": "Cyber-Foreur",
    "dlv.fridge": "📦 Frigo agrandi à <b>{capacity} côtelettes</b>.",
    "dlv.coins": "💰 Crédité <b>+{amount} 🪙</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nucléaire x5 actif jusqu'au <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Refroidissement à l'Azote +40% actif jusqu'au <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Le Maître-Drone protège ta ferme jusqu'au <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limites de victoires levées jusqu'au <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Ton équipe a reçu le statut <b>MÉGA-CLAN</b> : jusqu'à {max} places.",
    "dlv.err_fridge": "Tu as déjà un frigo de cette taille ou plus grand.",
    "dlv.err_no_team": "Tu n'as pas encore créé d'équipe. Crée-la d'abord via /create_team.",
    "dlv.err_mega": "Ton équipe a déjà le statut Méga-Clan.",
    "dlv.intern_upgrade": "♾ Ton Robot Stagiaire est promu <b>Robot Mineur ÉTERNEL</b> : 5 🪙 par heure, sans expiration !",
    "dlv.err_no_intern": "Aucun Robot Stagiaire activé : active-le d'abord dans /farm.",
    "dlv.err_intern_refs": "L'amélioration exige {need} amis actifs (conditions dans /invite) ; tu en as {have}.",
    "mk.header": "📈 <b>BOURSE DES CÔTELETTES</b>\n..................................................\nOrdres ouverts : <b>{orders}</b> · côtelettes en vente : <b>{cutlets}</b> · meilleur prix : <b>{best}</b>\nCommission du hub : <b>{fee}%</b> par vente (brûlée — bouclier anti-inflation)\n🥩 Dans ton stock : <b>{inv}</b> côtelettes\n\n{body}\n\n<i>Touche un ordre pour acheter. Pour vendre : /sell.</i>",
    "mk.empty": "Aucune offre pour l'instant. Sois le premier : /sell quantité prix",
    "mk.order_line": "🥩 #{id} · <b>{qty} pcs</b> à <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id} : {qty} pcs à {price} 🪙",
    "mk.btn_my": "📋 Mes ordres",
    "mk.btn_sell_help": "💰 Comment vendre",
    "mk.btn_refresh": "🔄 Actualiser",
    "mk.btn_back": "← Retour à la bourse",
    "mk.pick": "🛒 <b>Ordre #{id}</b> : {qty} pcs disponibles à {price} 🪙.\nCombien ?",
    "mk.btn_qty": "{qty} pcs — {total} 🪙",
    "mk.btn_qty_all": "Tout, {qty} pcs — {total} 🪙",
    "mk.buy_toast": "Affaire conclue !",
    "mk.buy_done": "✅ Acheté <b>{qty} côtelettes</b> pour <b>{total} 🪙</b>. Elles sont dans ton stock : ravitaille tes Foreurs !",
    "mk.sold_notify": "💰 <b>Bourse : vendu !</b> Ordre #{id} : {qty} pcs à {price}. Tu reçois <b>+{got} 🪙</b> (commission de {fee} brûlée).",
    "mk.sell_help": "💰 <b>COMMENT VENDRE DES CÔTELETTES</b>\n\nCommande : <code>/sell quantité prix</code>\nExemple : <code>/sell 10 250</code> — 10 côtelettes à 250 🪙.\n\nLes côtelettes quittent ton stock et attendent dans l'ordre (annulable à tout moment). Jusqu'à {max_qty} pcs par ordre et {max_orders} ordres ouverts. Une commission de {fee}% est brûlée à la vente. Une côtelette ne se vend pas moins de {min} 🪙 : le carburant de la boutique en Étoiles est toujours plus avantageux que la bourse. Ressources, ordres d'achat et échanges : dans l'appli de jeu.",
    "mk.sell_confirm": "📝 Mettre en vente <b>{qty} côtelettes</b> à <b>{price}</b> 🪙 ?\nTotal : {total} · commission {fee} brûlée · tu recevras <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ METTRE EN VENTE",
    "mk.btn_cancel": "❌ Annuler",
    "mk.sell_toast": "Ordre publié !",
    "mk.sell_done": "✅ Ordre <b>#{id}</b> en ligne : {qty} pcs à {price} 🪙. Je te préviens dès la vente.",
    "mk.cancelled_toast": "Annulé",
    "mk.cancel_text": "❌ <b>Annulé.</b> Les côtelettes restent dans ton stock.",
    "mk.my_header": "📋 <b>TES ORDRES</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} pcs à {price} 🪙",
    "mk.my_empty": "📋 Tu n'as aucun ordre ouvert.",
    "mk.btn_cancel_order": "❌ Retirer l'ordre #{id}",
    "mk.err_newbie_price": "🔒 While your account is new, you can buy at no more than {max} 🪙 apiece. The limit lifts at intelligence level {level} and after {claims} daily cutlets.",
    "mk.err_cancel_room": "📦 Not enough storage room: {free} free. Make room first, then withdraw the lot.",
    "sw.err_ratio": "⚖️ This swap is too uneven: the two sides (valued at the market's minimum prices) may differ by at most {x}×.",
    "mk.order_cancelled": "↩️ Ordre #{id} retiré : <b>{qty} côtelettes</b> de retour dans le stock.",
    "mk.err_qty": "❌ Quantité : de 1 à {max} pièces par ordre.",
    "mk.err_price": "❌ Prix : de {min} à {max} 🪙 l'unité.",
    "mk.err_no_cutlets": "❌ Seulement {have} côtelettes en stock. Celles du frigo ne se vendent pas — voir /farm.",
    "mk.err_too_many": "❌ Limite : {max} ordres ouverts maximum. Retire-en un dans « Mes ordres ».",
    "mk.err_not_found": "❌ Cet ordre est déjà clos.",
    "mk.err_own": "🤨 Tu ne peux pas acheter ton propre ordre.",
    "mk.err_insufficient": "❌ Pas assez : il faut {total} 🪙.",
    "farm.btn_market": "📈 Bourse des côtelettes",

    # ---------------- ressources (vague 22.10, soir) ----------------
    "res.metal": "Métal",
    "res.hydrogen": "Hydrogène",
    "res.crystal": "Cristaux",
    "res.parts": "Composants",
    "res.none": "rien pour l'instant",
    "games.resource_gain": "{icon} Récolté : <b>+{qty} {name}</b> (total {total}) → /workshop",
    "duel.metal_gain": "🪨 Trophée de duel : <b>+{metal} Pierre</b> → /workshop",
    "quest.win_resources": "\n📦 En plus, un lot : <b>{qty}</b> de chaque ressource, 🪵 du bois et une 🐄 vache → /workshop",
    "profile.resources_line": "🧰 Ressources : {stock}\n",
    "menu.btn_goals": "🎯 Objectifs du jour",
    "menu.btn_raids": "🏴‍☠️ Raids",
    "menu.btn_workshop": "🔧 Atelier",
    "farm.btn_workshop": "🔧 Atelier",
    "farm.btn_app": "🏭 La ferme dans l'appli",
    "menu.btn_app": "🚀 Appli de jeu : ferme, atelier, raids",
    "app.btn_section": "🚀 OUVRIR DANS L'APPLI",
    "app.goto_workshop": "🔧 L'<b>Atelier</b> vit dans l'appli de jeu : ressources, recettes et fabrication en un tap.",
    "app.goto_raids": "🏴‍☠️ Les <b>Raids</b> vivent dans l'appli de jeu : reconnaissance, posture de défense et revanche.",
    "app.goto_station": "🛰 La <b>Station d'équipe</b> vit dans l'appli de jeu : progression, dons et bonus pour toute l'équipe.",
    "app.goto_market": "📈 La <b>Bourse des côtelettes</b> est plus pratique dans l'appli de jeu : offres, vente et tes ordres sur un seul écran.",
    "mk.err_asset": "❌ Cet article n'existe pas à la bourse.",
    "mk.err_no_resource": "❌ Pas assez de cette ressource : tu n'en as que {have} en stock.",
    "mk.bid_filled_notify": "🙋 <b>Bourse : ordre d'achat exécuté !</b> Ordre #{id} : tu as acheté <b>+{qty} {icon}</b> à {price} 🪙.",
    "sw.err_same": "❌ Impossible d'échanger une ressource contre la même.",
    "sw.err_qty": "❌ Dans un échange, indique une quantité de 1 à {max} — pour ce que tu donnes comme pour ce que tu veux recevoir.",
    "shop.btn_info": "ℹ️ Ce que donne chaque article",
    "sw.done_notify": "🔄 <b>Échange #{id} conclu !</b> Donné : {give}, reçu : {want}.",
    "ws.err_coins": "🔒 Pas assez de pièces : il faut {need} 🪙, tu as {have} 🪙.",
    "wk.eff_nitrogen": "❄️ Azote +40% pour {h} h",
    "wk.eff_nuclear": "☢️ Nucléaire x5 pour {h} h",
    "wk.eff_drone": "🛸 Maître-Drone pour {h} h",
    "wk.eff_shield": "🛡 Bouclier pour {h} h",
    "wk.eff_unlimit": "⚡ Jeux illimités pour {h} h",
    "wk.eff_cutlet": "🥩 Côtelette ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ Cette recette de la semaine n'est plus disponible.",
    "wk.err_limit": "🔒 La limite hebdomadaire de cette recette est atteinte ({limit}). Nouvelle semaine dès lundi 00:00 UTC.",
    "games.resource_full": "📦 Stock de {icon} plein ({cap}) — le surplus est perdu. Dépense, vends ou agrandis ton stock à l'atelier.",
    "mk.err_storage_full": "📦 Pas assez de place dans ton stock : {free} de libre. Agrandis ton stock à l'atelier.",
    "mk.err_buyer_full": "📦 Le stock de l'acheteur est plein — la transaction est impossible pour l'instant ({free} de libre).",
    "ws.recipe_storage": "Agrandir le stock à {cap}",
    "ws.done_storage": "📦 <b>Stock agrandi :</b> jusqu'à {cap} de chaque ressource. C'est pour toujours.",
    "ws.err_storage_max": "📦 Le stock est déjà à sa taille maximale.",
    "farm.boost_armor": "🛡 Cyber-Armure niv. {level} : +{percent}% de minage jusqu'au {until} UTC",
    "farm.boost_station": "🛰 Station d'équipe niv. {level} : +{percent}% de minage",
    "clan.btn_station": "🛰 Station d'équipe",

    # ---------------- atelier ----------------
    "ws.header": (
        "🔧 <b>ATELIER</b>\n"
        "..................................................\n"
        "🧰 Tes ressources : {stock}\n"
        "⛏ Métal — Chifoumi et duels · 💧 Hydrogène — Plus/Moins · "
        "💎 Cristaux — Quiz · ⚙️ Composants — Cyber-Coffre. Les quêtes donnent un lot complet.\n\n"
        "🛡 Cyber-Armure : <b>niveau {armor}/{armor_max}</b> (+{armor_pct}% de minage par niveau, pour 30 jours)\n"
        "🚀 Navette : <b>{shuttle}</b> — commission de la bourse {shuttle_fee}%, jusqu'à {shuttle_qty} côtelettes par ordre\n\n"
        "<i>✅ — assez de ressources, 🔒 — pas encore. Une pression et c'est fait.</i>"
    ),
    "ws.shuttle_yes": "assemblée",
    "ws.shuttle_no": "pas encore assemblée",
    "ws.recipe_nitro_6h": "Refroidissement à l'Azote pour 6 h",
    "ws.recipe_nuclear_3h": "Boost Nucléaire pour 3 h",
    "ws.recipe_drone_24h": "Maître-Drone pour 24 h",
    "ws.recipe_shield_24h": "Bouclier anti-raids pour 24 h",
    "ws.recipe_cutlet": "Synthèse d'une cyber-côtelette",
    "ws.recipe_armor": "Cyber-Armure niv. {level}",
    "ws.recipe_shuttle": "Assembler la Navette",
    "ws.btn_shuttle_owned": "🚀 Navette assemblée",
    "ws.btn_armor_max": "🛡 Cyber-Armure : au max",
    "ws.btn_refresh": "🔄 Actualiser",
    "ws.btn_farm": "🚜 Vers la ferme",
    "ws.noop": "Déjà au maximum",
    "ws.toast": "C'est fait !",
    "ws.done_nitrogen": "❄️ <b>Refroidissement à l'Azote +40%</b> actif jusqu'à {until} UTC.",
    "ws.done_nuclear": "☢️ <b>Boost Nucléaire x5</b> actif jusqu'à {until} UTC. Les Foreurs mangent ×3 côtelettes !",
    "ws.done_drone": "🛸 Le <b>Maître-Drone</b> protège tes robots jusqu'à {until} UTC.",
    "ws.done_shield": "🛡 Le <b>Bouclier anti-raids</b> tient jusqu'à {until} UTC. Tes ressources sont à l'abri.",
    "ws.done_cutlet": "🥩 Synthétisé : <b>+{qty} cyber-côtelette</b> dans ton stock. Ravitaille dans /farm !",
    "ws.done_armor": "🛡 <b>Cyber-Armure niveau {level} !</b> Minage de la ferme : <b>+{percent}%</b> pour 30 jours.",
    "ws.done_shuttle": "🚀 <b>Navette assemblée !</b> La commission sur tes ventes passe à {fee}%, jusqu'à {qty} côtelettes par ordre. La Navette n'appartient qu'à toi, pour toujours.",
    "ws.err_unknown": "❌ Cette recette n'existe pas.",
    "ws.err_off": "🔧 Cette recette n'est pas disponible pour le moment.",
    "ws.err_locked": "🔒 Cette recette s'ouvre dans {hours} h — les nouvelles recettes s'ouvrent une par jour.",
    "ws.recipe_camo_12h": "Camouflage pour 12 h",
    "ws.recipe_trap_24h": "Leurre pour 24 h",
    "ws.recipe_drill_24h": "Entraîneur de posture pour 24 h",
    "ws.recipe_forsage": "Postcombustion du vaisseau",
    "ws.recipe_economizer": "Économiseur",
    "ws.recipe_cargo": "Soute agrandie",
    "ws.recipe_thermos_24h": "Thermos à côtelettes pour 24 h",
    "ws.recipe_stamp": "Tampon de la bourse",
    "ws.recipe_banner_24h": "Bannière d'équipe pour 24 h",
    "ws.recipe_dome_12h": "Dôme d'équipe pour 12 h",
    "it.err_no_cooldown": "🚀 Pas de recharge à annuler — ton vaisseau est déjà prêt.",
    "it.err_forsage_daily": "🔥 Postcombustion déjà utilisée — la prochaine dans {hours} h.",
    "res.stone": "Pierre",
    "res.wood": "Bois",
    "res.fire": "Feu",
    "res.energy": "Électricité",
    "res.battery": "Piles",
    "res.cow": "Vaches",
    "res.core": "Noyau",
    "tech.comm": "Communications",
    "tech.scout": "Reconnaissance",
    "tech.attack": "Attaque",
    "tech.defense": "Défense",
    "tech.science": "Science",
    "tech.err_max": "🏆 C'est déjà le niveau maximal.",
    "tech.err_unknown": "❌ Cette technologie n'existe pas.",
    "tech.err_tool": "🧰 Il faut un kit d'outils de niveau {tool} — fabrique-le au Labo.",
    "tech.err_cooldown": "⏳ Le niveau suivant sera étudiable dans {hours} h.",
    "tech.err_science": "📚 La science de niveau {level} s'ouvre quand toutes les autres technologies sont au niveau {level}.",
    "ws.err_items_full": "📦 La réserve d'objets est pleine : {max} objets maximum. Active-en un ou agrandis la réserve.",
    "post.scope_team": "Classement par équipe",
    "post.scope_clan": "Classement des clans",
    "post.scope_teams": "Équipes et clans",
    "post.scope_solo": "Classement individuel",
    "nom.farm_mined": "miner le plus de pièces avec la ferme",
    "nom.coins_earned": "gagner le plus de pièces",
    "nom.duel_wins": "remporter le plus de duels",
    "nom.duels_played": "jouer le plus de duels",
    "nom.quiz_wins": "donner le plus de bonnes réponses au Quiz",
    "nom.rps_wins": "gagner le plus de parties de Chifoumi",
    "nom.safe_wins": "ouvrir le plus de Cyber-Coffres",
    "nom.game_wins_total": "gagner le plus de parties contre le bot",
    "nom.referrals": "amener le plus d'amis actifs",
    "nom.stars_spent": "soutenir le plus l'écosystème (Stars)",
    "nom.insta_reels": "dont le reel Instagram cartonnera le plus",
    "nom.youtube_shorts": "dont la vidéo YouTube Shorts cartonnera le plus",
    "nom.tiktok": "dont la vidéo TikTok cartonnera le plus",
    "bt.err_closed": "⏳ Cette bataille est déjà terminée.",
    "bt.err_no_entry": "Cette bataille ne demande pas d'inscription.",
    "bt.err_no_team": "🏆 Rejoins d'abord une équipe.",
    "bt.err_scope": "Cette bataille n'est pas ouverte à ton type d'équipe.",
    "bt.err_full": "✅ L'inscription de l'équipe est déjà complète.",
    "bt.err_battery": "🔋 Pas de batterie : fabrique-en une à l'atelier.",
    "horse.err_max": "🐎 L'écurie contient déjà {max} chevaux — plus de place.",
    "horse.err_coins": "🪙 Un cheval coûte {price} 🪙 — il t'en manque encore.",
    "shuttle.err_none": "🚀 Assemble d'abord la Navette à l'atelier.",
    "cart.err_horse": "🛒 Une charrette a besoin d'un cheval : pas plus de charrettes que de chevaux (et pas plus de {max}).",
    "raid.err_need_tech": "🔬 Un raid exige la technologie « {tech} » niveau 1 — étudie-la au Labo.",
    "raid.err_battery": "🔋 La reconnaissance exige une pile — fabrique-en une à l'atelier.",
    "games.energy_gain": "⚡ Coup de chance : +1 Électricité !",
    "ws.recipe_bonfire": "Feu de camp : du feu avec du bois et de la pierre",
    "ws.recipe_battery": "Piles (×2)",
    "ws.recipe_cart": "Charrette",
    "ws.recipe_meds_72h": "Trousse de secours pour 72 h",
    "ws.err_resources": "🔒 Pas assez : {kind} — il en faut {need}, tu en as {have}. Récolte-en dans les jeux !",
    "ws.err_shuttle_owned": "🚀 La Navette est déjà assemblée — une seule par joueur.",
    "ws.err_armor_max": "🛡 L'armure est déjà au niveau maximum ({max}).",

    # ---------------- raids ----------------
    "raid.header": (
        "🏴‍☠️ <b>RAIDS</b>\n"
        "..................................................\n"
        "💧 Hydrogène : <b>{hydrogen}</b> (un vol coûte {fuel})\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ Posture de défense : <b>{stance}</b>\n\n"
        "📊 Raids : <b>{attacks}</b> ({attack_wins} réussis) · repoussés : <b>{holds}/{defenses}</b>\n\n"
        "<i>Le butin, c'est uniquement des ressources : {percent}% du stock de la cible, {cap} max par ressource. "
        "Pièces, robots et côtelettes sont intouchables. Ton geste contre la posture de la cible — "
        "décision contre décision. Un vol toutes les {cooldown} h ; la revanche est gratuite.</i>"
    ),
    "raid.ready_line": "Vaisseau prêt au décollage",
    "raid.cooldown_line": "Recharge : encore {minutes} min",
    "raid.shield_on": "Bouclier actif jusqu'à {until} UTC",
    "raid.shield_newbie": "Protection des débutants ({days} premiers jours)",
    "raid.shield_off": "Pas de bouclier — assemble-en un dans /workshop",
    "raid.stance_random": "aléatoire (choisis-la dans le menu !)",
    "raid.btn_scout": "🔭 RECO : trouver des cibles",
    "raid.btn_revenge": "⚔️ Revanche : {name}",
    "raid.btn_stance": "✊ Posture de défense",
    "raid.btn_workshop": "🛡 Assembler un bouclier",
    "raid.btn_refresh": "🔄 Actualiser",
    "raid.btn_back": "← Retour",
    "raid.btn_open": "🏴‍☠️ Ouvrir les raids",
    "raid.btn_again": "🏴‍☠️ Retour aux raids",
    "raid.stance_pick": "✊ <b>Posture de défense</b>\nSeul le résultat d'un raid adverse la révèle : le geste de l'attaquant contre ta posture. Change-la de temps en temps — les prévisibles se font piller.",
    "raid.stance_saved": "Posture : {stance}",
    "raid.scout": "🔭 <b>La reco a trouvé des cibles.</b> Le vol coûtera {fuel} 💧. À toi de choisir :",
    "raid.btn_target": "🎯 {name} · ressources ≈{total}",
    "raid.no_targets": "🔭 La reco n'a trouvé personne : aucune cible valable pour l'instant (boucliers, recharges, débutants). Repasse plus tard.",
    "raid.pick_move": "✊ <b>Ton geste ?</b> Il jouera contre la posture de défense de la cible. Vol : −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>Revanche ! Ton geste ?</b> Le vol est gratuit et sans recharge.",
    "raid.result_win": "🏴‍☠️ <b>RAID RÉUSSI !</b>\n{move} contre {stance} chez {name}.\nButin : <b>{loot}</b>",
    "raid.result_draw": "😐 <b>Égalité.</b> {move} contre {stance} chez {name}. Le vaisseau est rentré à vide, le carburant est parti en fumée.",
    "raid.result_lose": "💥 <b>LA DÉFENSE A TENU.</b> {move} contre {stance} chez {name}.\nLa cible a récupéré : <b>{loot}</b>",
    "raid.result_footer": "<i>Les ressources sont dans /workshop. Un bouclier te protège des représailles.</i>",
    "raid.victim_lost": "🚨 <b>Ta base a été attaquée !</b> {name} : {move} contre ta posture {stance}.\nPerdu : <b>{loot}</b>\n\n⚔️ Revanche gratuite pendant {hours} h. Le bouclier, c'est dans /workshop.",
    "raid.victim_draw": "🛡 <b>Raid repoussé sur égalité.</b> {name} : {move} contre ta posture {stance}. Rien de perdu.",
    "raid.victim_held": "🛡 <b>Ta défense a tenu !</b> {name} : {move} contre ta posture {stance}.\nTrophée de défense : <b>{loot}</b>",
    "raid.err_stance": "❌ Geste inconnu.",
    "raid.err_self": "🤨 Un raid contre toi-même ? Non.",
    "raid.err_gone": "❌ Cible indisponible.",
    "raid.err_teammate": "🤝 On ne pille pas les siens — c'est quelqu'un de ton équipe.",
    "raid.err_shielded": "🛡 La cible a un bouclier. Choisis-en une autre.",
    "raid.err_revenge_gone": "❌ La fenêtre de revanche est fermée.",
    "raid.err_cooldown": "⏳ Recharge : encore {minutes} min.",
    "raid.err_victim_cooldown": "⏳ Cette cible a déjà été pillée récemment (pause de {hours} h).",
    "raid.err_fuel": "💧 Pas assez d'hydrogène : il en faut {need}, tu en as {have}. Il se récolte dans Plus/Moins.",

    # ---------------- objectifs du jour ----------------
    "goal.header": (
        "🎯 <b>OBJECTIFS DU JOUR</b>\n"
        "..................................................\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 Coffret : <b>+{coins} 🪙</b> et <b>+{res}</b> d'une ressource au hasard\n"
        "🔥 Série : <b>{streak}</b> j. · chaque {every}e jour d'affilée ajoute +{bonus} 🪙 au coffret\n\n"
        "<i>Les objectifs se renouvellent à 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ Boucle les trois et le coffret est à toi.",
    "goal.status_ready": "✅ <b>Tous les objectifs sont bouclés ! Récupère le coffret.</b>",
    "goal.status_claimed": "🎁 Le coffret du jour est déjà récupéré. De nouveaux objectifs demain !",
    "goal.btn_claim": "🎁 RÉCUPÉRER LE COFFRET",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Actualiser",
    "goal.toast": "Coffret ouvert !",
    "goal.chest": "🎁 <b>COFFRET OUVERT !</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 Série : {streak} j.",
    "goal.err_claimed": "🎁 Déjà récupéré aujourd'hui.",
    "goal.err_not_done": "⏳ Tous les objectifs ne sont pas encore bouclés.",
    "goal.win_quiz": "Gagner {n} manches de Quiz",
    "goal.win_rps": "Gagner {n} manches de Chifoumi",
    "goal.win_hl": "Gagner {n} manches de Plus/Moins",
    "goal.win_safe": "Ouvrir le Cyber-Coffre {n} fois",
    "goal.play_rounds": "Jouer {n} manches, tous jeux confondus",
    "goal.duel": "Jouer un duel",
    "goal.bonus": "Récupérer la côtelette du jour à la ferme",
    "goal.craft": "Fabriquer quelque chose à l'atelier",
    "goal.raid": "Lancer un raid",
    "goal.market_deal": "Conclure une transaction à la bourse",
    "goal.donate": "Investir des ressources dans la station d'équipe",

    # ---------------- station d'équipe ----------------
    "st.header": (
        "🛰 <b>STATION DE L'ÉQUIPE « {team} »</b>\n"
        "..................................................\n"
        "Niveau : <b>{level}/{max}</b> → chaque combattant reçoit <b>+{percent}%</b> de minage à la ferme "
        "(+{per_level}% par niveau)\n\n"
        "📦 Jusqu'au prochain niveau :\n{progress}\n\n"
        "🧾 Dernières contributions :\n{feed}\n\n"
        "🧰 Tes ressources : {stock}\n"
        "<i>La station est commune : toute l'équipe la construit, chacun touche le bonus. Qui quitte l'équipe perd le bonus.</i>"
    ),
    "st.max_level": "🏁 Station achevée — niveau maximum !",
    "st.feed_empty": "personne n'a encore contribué — ouvre le bal",
    "st.no_team": "🛰 La station se construit en équipe. Rejoins une équipe ou crée la tienne — et bâtissez ensemble.",
    "st.btn_find_team": "🏆 Équipes et clans",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ Tout : {qty} {icon} {name}",
    "st.btn_refresh": "🔄 Actualiser",
    "st.btn_team": "🏆 Vers l'équipe",
    "st.toast": "Investi +{qty} {icon}",
    "st.level_up": "🛰 <b>La station de l'équipe passe au niveau {level} !</b> Tous les combattants ont maintenant +{percent}% de minage à la ferme.",
    "st.err_qty": "❌ Quantité invalide.",
    "st.err_no_team": "❌ Tu n'es dans aucune équipe.",
    "st.err_max": "🏁 La station est déjà achevée (niveau {max}).",
    "st.err_resources": "🔒 Pas assez de cette ressource : tu en as {have}.",

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
        "..................................................\n"
        "📌 Nom : <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Capitaine de la bande : 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Devise : <i>« {motto} »</i>\n"
        "🔮 Symbole de l'emblème : {symbol}\n\n"
        "👥 Effectif : <b>{members} / {max_members}</b>\n"
        "..................................................\n"
        "👇 <b>NAVIGATION :</b>"
    ),
    "clan.members_only": "🔒 La liste des membres n'est visible que par les membres de cette équipe !",
    "clan.members_gone": "❌ Cette équipe a déjà été dissoute.",
    "clan.members_header": (
        "👥 <b>EFFECTIF DE L'ÉQUIPE « {name} »</b>\n"
        "🧠 — niveau d'intelligence de jeu (progresse uniquement dans /quiz)\n"
        "..................................................\n"
    ),
    "clan.members_footer": (
        "\n..................................................\n"
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
    "md_title": "🧭 Comment veux-tu jouer ?",
    "md_hint": "ROFL HUB est vaste. Choisis par où commencer — tu peux changer de mode à tout moment dans le passeport.",
    "md_full": "🌐 Tout l'écosystème",
    "md_fullText": "Une ferme de robots, le stock, l'atelier, la bourse, les équipes, les raids, les mines et la carte du monde — plus tous les jeux et histoires. Les sections s'ouvrent peu à peu, sur 3 jours, pour ne pas te noyer sous les boutons.",
    "md_puzzle": "🧩 Jeux et histoires",
    "md_puzzleText": "Juste le quiz, les mini-jeux, les quêtes, l'Affaire du jour et les duels entre amis. Pas d'économie, pas d'onglets en trop.",
    "md_later": "La ferme tourne dans tous les modes — les pièces s'accumulent même si tu n'y jettes jamais un œil.",
    "md_toFull": "Activer tout l'écosystème ? La ferme, le stock, la bourse, les équipes et les autres sections apparaîtront.",
    "md_toPuzzle": "Garder seulement les jeux et histoires ? La ferme continue de tourner, les autres onglets se cachent — tu peux les remettre ici même.",
    "md_now": "🧭 Mode : {m} · changer",
    "lk_new": "🎉 Nouvelles sections ouvertes : <b>{t}</b>. Touche pour y jeter un œil !",
    "lk_line": "🔒 {t} — dans {d} j ou dès le niveau 🧠 {l}",
    "lk_title": "Les sections s'ouvrent peu à peu, pour mieux t'y retrouver :",
    "di_title": "⚔️ On te défie en duel !",
    "di_text": "<b>{n}</b> te défie en duel de pierre-feuille-ciseaux.<br>Mise {s} 🪙 · le gagnant remporte {p} 🪙.",
    "di_accept": "⚔️ Relever le défi",
    "di_decline": "Pas maintenant",
    "di_waiting": "On attend ton ami à la table de {s} 🪙…",
    "di_left": "Le défi reste ouvert encore {h} h — ensuite ta mise revient",
    "di_share": "📤 Envoyer le défi à un ami",
    "di_waitHint": "Envoie le lien à un ami. Quand le défi sera accepté, le bot t'écrira dans le chat. Ta mise est déjà sur la table ; si tu changes d'avis, quitte la table et elle te revient.",
    "di_head": "🤝 Défier un ami",
    "di_hint": "Ta propre table par lien : elle ne passe pas par la file et n'attend que ton ami. Un nouveau venu arrivé par le lien devient ton ami.",
    "di_table": "🤝 Défier un ami · table de {s} 🪙",
    "di_shareText": "Je te défie en duel sur ROFL HUB ! Mise {s} 🪙 — on va voir qui gagne 😎",
    "ac_title": "🏅 Mes succès",
    "ac_streak": "🔥 Série d'Affaires du jour : {n}",
    "ac_hint": "Tous tes succès réunis sur une carte — publie-la en story ou envoie-la à un ami.",
    "ac_make": "📸 Créer la carte",
    "ac_cardSub": "mes succès",
    "ac_cardCall": "Tu fais mieux ?",
    "ac_shareText": "Mon score sur ROFL HUB : 🧠 niveau {l}, 🗺 {q} quêtes, 🕵️ {d} affaires, ⚔️ {w} duels gagnés. Tu fais mieux ?",
    "ac_story": "📲 Publier en story",
    "ac_send": "✈️ Envoyer à un ami",
    "ac_save": "💾 Enregistrer l'image",
    "ac_quests": "quêtes terminées",
    "ac_epics": "épopées",
    "ac_cases": "affaires résolues",
    "ac_duels": "duels gagnés",
    "ac_wins": "victoires en jeu",
    "ac_friends": "amis actifs",
    "ac_robots": "robots",
    "ac_days": "jours de jeu",
    "tf_title": "💸 Envoyer des pièces",
    "tf_hint": "À un ami — par @username, ID ou VIP ID. Minimum {m} 🪙, commission {f} %.",
    "tf_locked": "🔒 L'envoi de pièces s'ouvre au niveau 🧠 {l} et après {c} côtelettes du jour récupérées — ainsi les faux comptes ne siphonnent pas les pièces de départ. Recevoir, c'est possible tout de suite.",
    "tf_to": "À",
    "tf_amount": "Combien de 🪙",
    "tf_btn": "💸 Envoyer",
    "tf_ask": "Envoyer {a} 🪙 à {to} ? Commission {f} 🪙, {r} 🪙 seront reçues.",
    "tf_done": "C'est fait ! {to} reçoit {r} 🪙",
    "sq_choose": "Choisis ce que tu crées :",
    "sq_squad": "🛡 Escouade",
    "sq_squadText": "Jusqu'à {n} combattants · {c} 🪙. Pour toi et quelques amis ; plus tard, la tête de l'escouade pourra l'agrandir en équipe.",
    "sq_team": "🏆 Équipe",
    "sq_teamText": "Jusqu'à {n} combattants · {c} 🪙. Une grande équipe pour les batailles et les mines.",
    "sq_createBtn": "Créer une escouade pour {cost} 🪙",
    "sq_created": "Escouade « {n} » créée — c'est toi le capitaine !",
    "sq_label": "Escouade",
    "sq_upHint": "L'escouade est à l'étroit ? Agrandis-la en équipe — jusqu'à {n} combattants.",
    "sq_upBtn": "⬆️ Passer en équipe · {c} 🪙",
    "sq_upAsk": "Agrandir l'escouade en équipe pour {c} 🪙 ? Il y aura {n} places.",
    "sq_upDone": "Ton escouade est devenue une équipe !",
    "cs_title": "🕵️ Affaire du jour",
    "cs_tile": "Une affaire pour tous · 4 suspects · une seule accusation",
    "cs_none": "Pas d'affaire aujourd'hui — reviens demain.",
    "cs_culprit": "coupable",
    "cs_accuse": "👉 Accuser",
    "cs_clueLocked": "Indice {n} — encore caché",
    "cs_more": "🔍 Révéler un autre indice (récompense : {r} 🪙)",
    "cs_rules": "Une seule accusation, une seule fois. Moins il te faut d'indices, plus la récompense est grande :",
    "cs_solved": "🎉 Affaire résolue ! +{r} 🪙",
    "cs_failed": "Raté ! Le coupable était {n}.",
    "cs_bonus": "🔥 Bonus de série : +{b} 🪙",
    "cs_solution": "Solution :",
    "cs_stats": "Résolue aujourd'hui : {s} sur {p} · indices en moyenne : {a}",
    "cs_share": "📤 Frimer",
    "cs_next": "Nouvelle affaire dans {t}",
    "cs_head": "🕵️ Affaire n° {n}",
    "cs_suspects": "👥 Suspects",
    "cs_clues": "🔍 Indices",
    "cs_streak": "🔥 Série d'affaires résolues : {n} · chaque {e}e jour d'affilée +{b} 🪙",
    "cs_accuseAsk": "Accuser {n} ? Une seule accusation — impossible de revenir en arrière.",
    "cs_shareText": "🕵️ Affaire du jour n° {n}\n{s}\n🔥 Série : {k}\nTu la résous plus vite ?",
    "qs_epicPaid": "⚡ avec Illimité",
    "qs_paper": "📝 Astuce : note les détails sur papier — les plus attentifs trouvent plus vite.",
    "qs_total": "📚 Quêtes dans la bibliothèque : {n}",
    "qs_daily": "Nouvelles aujourd’hui : {a}/{b}",
    "qs_dailyUnl": "⚡ Illimité — quêtes sans limite",
    "qs_locked": "🔒 jusqu’à 00:00 UTC",
    "qs_lockedNote": "Tu as terminé {b} nouvelles quêtes aujourd’hui. Les autres s’ouvrent à 00:00 UTC, et tu peux rejouer les quêtes terminées autant que tu veux. ⚡ Illimité lève la limite.",
    "qs_epic": "⭐ ÉPIQUE ·",
    "qr_btn": "⚠️ Signaler la question",
    "qr_title": "Qu’est-ce qui ne va pas ?",
    "qr_answer": "❌ La bonne réponse est fausse",
    "qr_question": "✏️ Erreur ou faute dans la question",
    "qr_dup": "🔁 La question se répète",
    "qr_other": "🤔 Autre (pas clair, discutable)",
    "qr_thanks": "Merci ! La question sera vérifiée et corrigée.",
    "qr_limit": "Assez de signalements pour aujourd’hui — merci pour ton aide !",
    # TODO(перевод 26.10): атмосферы квестов (27.10)
    "qs_fxGallery": "🎨 Atmosphere gallery",
    "qs_fxChoice": "🚪 Step inside",
    "qs_fxSample": "Night. You stand at the entrance and listen to the world around you. Something changes — and the scene answers with light, shadow and motion. Pick an atmosphere below to see how it looks under quest text.",
    # TODO(перевод 26.10): дуэли в приложении (27.10)
    "dl_title": "⚔️ Duels",
    "dl_tile": "A live opponent · tables 10 / 100 / 1000 🪙",
    "dl_intro": "Rock-paper-scissors against a live player. The stake is taken right away; the winner gets {p}% of the bank, {b}% burns. {t} s per gesture, a draw is replayed.",
    "dl_table": "⚔️ Table {s} 🪙 · win +{p} 🪙 and 🪨{r}",
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
    "dl_win": "🎉 Duel won! +{p} 🪙 and 🪨{r}",
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
    "qs_winFirst": "🏆 Quest completed! +{c} 🪙 and {q} of each resource, 🪵 and 🐄",
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
    "subtitle": "ton empire de jeu sur un seul écran",
    "tab_passport": "📋 Passeport",
    "tab_farm": "🚜 Ferme",
    "tab_goals": "🎯 Objectifs",
    "tab_workshop": "🔧 Atelier",
    "tab_raids": "🏴‍☠️ Raids",
    "tab_market": "📈 Bourse",
    "tab_team": "🏆 Équipe",
    "tab_shop": "🏪 Boutique",
    "tab_top": "👑 TOP",
    "passport": "📋 PASSEPORT DU JOUEUR",
    "coins": "🪙",
    "brain": "🧠 Niveau d'intelligence",
    "toNext": "jusqu'au niveau {n} : {left} bonnes réponses au quiz (+{reward} 🪙)",
    "farm": "🚜 CYBER-FERME",
    "robots": "Robots (mineurs / foreurs)",
    "intern": "Robots Stagiaires (1 🪙/h, éternels)",
    "activateIntern": "🚀 ACTIVER LE ROBOT STAGIAIRE",
    "claimIntern": "🎁 RÉCUPÉRER LE STAGIAIRE ({n})",
    "internDone": "🤖 Ton Robot Stagiaire prend son poste !",
    "rank": "🎖 Grade",
    "openFarm": "🏭 OUVRIR LA MINE",
    "farmScene": "🏭 TA FERME",
    "back": "← Retour",
    "minedVisit": "miné pendant cette visite",
    "unit_intern": "Robot Stagiaire",
    "unit_junior": "Robot Mineur",
    "unit_premium": "Cyber-Foreur",
    "eternal": "éternel",
    "fueledAll": "ravitaillés",
    "fueledPart": "{a} sur {b} ravitaillés",
    "license": "licence 30 jours",
    "emptyFarm": "La mine est vide. Active ton Robot Stagiaire ou achète des robots dans la boutique !",
    "madeBy": "Tu veux un bot comme celui-ci pour ton projet ? Écris à @mister_telebot",
    "fueled": "Foreurs ravitaillés",
    "speed": "Vitesse de minage",
    "perHour": "{v} 🪙/h",
    "fridge": "Frigo",
    "inv": "Côtelettes en stock",
    "burnout": "Prochaine expiration",
    "boosts": "Boosts actifs",
    "none": "aucun",
    "resources": "🧰 Ressources",
    "bonusPct": "Bonus de minage permanent",
    "shuttle": "🚀 Navette assemblée",
    "resHint": "Chaque victoire rapporte la ressource de son jeu, avec l'Illimité — sans limites. Dépense-les à l'atelier.",
    "bonusReady": "🎁 RÉCUPÉRER LA CÔTELETTE DU JOUR",
    "bonusWait": "⏳ Bonus dans {h} h {m} min",
    "bonusDone": "🎉 Côtelette ajoutée !",
    "team": "🏆 MON ÉQUIPE",
    "clan": "CLAN",
    "teamLabel": "Équipe",
    "captain": "👑 Tu es capitaine !",
    "members": "Effectif",
    "noTeam": "Pas encore d'équipe : rejoins-en une via la roulette ou la recherche — ou crée la tienne.",
    "tab_faq": "📚 FAQ",
    "tab_rules": "📜 Accord",
    "tm_roulette": "🎲 ROULETTE D'ÉQUIPES",
    "tm_rotate": "🔄 Voir d'autres équipes",
    "tm_noFree": "Aucune équipe libre pour l'instant — crée la tienne !",
    "tm_search": "🔍 TROUVER UNE ÉQUIPE",
    "tm_searchPh": "Nom ou une partie du nom",
    "tm_searchBtn": "Chercher",
    "tm_notFound": "Aucune équipe avec ce nom",
    "tm_join": "💥 Rejoindre",
    "tm_joined": "Tu es dans « {n} » !",
    "tm_create": "🏆 CRÉER UNE ÉQUIPE",
    "tm_hubHint": "Une équipe jusqu'à 50 combattants coûte {cost} 🪙. Dans la boutique, tu peux la faire évoluer en Méga-Clan de 1000 places.",
    "tm_name": "Nom (jusqu'à {n} caractères)",
    "tm_motto": "Devise (jusqu'à {n} caractères)",
    "tm_symbol": "Emblème — un émoji (jusqu'à {n} caractères)",
    "tm_createBtn": "Créer pour {cost} 🪙",
    "tm_created": "L'équipe « {n} » est créée — tu es capitaine !",
    "tm_noMoney": "Il te faut {cost} 🪙, tu as {b} 🪙",
    "tm_roster": "👥 EFFECTIF DE L'ÉQUIPE",
    "tm_mottoL": "💬 Devise",
    "tm_leave": "🚪 Quitter l'équipe",
    "tm_leaveAsk": "Vraiment quitter l'équipe « {n} » ?",
    "tm_leaveAskCaptain": "Tu es capitaine : la couronne passera au vétéran de l'équipe. Vraiment quitter « {n} » ?",
    "tm_left": "Tu n'es plus dans une équipe",
    "mk_scopePublic": "🌐 Bourse commune",
    "mk_scopeTeam": "🏆 Bourse d'équipe",
    "mk_teamHint": "Bourse de l'équipe « {t} » : seuls les coéquipiers voient et achètent ces offres, commission de {f}% seulement.",
    "mk_yourStock": "📦 Tu as",
    "mk_yourCoins": "💰 Tes pièces",
    "tm_market": "🏪 BOURSE D'ÉQUIPE",
    "tm_marketBtn": "Ouvrir la bourse d'équipe",
    "tm_marketHint": "Échange avec tes coéquipiers : commission de {f}% au lieu de {p}% sur la bourse commune. Dans un Méga-Clan — seulement {c}%.",
    "hp_title": "🤝 ENTRAIDE",
    "hp_hint": "Il te manque une ressource ? Demande à ton équipe. Chacun peut offrir jusqu'à {d} ressources par jour.",
    "hp_today": "Offert par toi aujourd'hui : {g} / {d}",
    "hp_empty": "Personne ne demande d'aide pour l'instant",
    "hp_give": "🎁 +{n}",
    "hp_kind": "Ce dont tu as besoin",
    "hp_qty": "Combien (jusqu'à {n})",
    "hp_ask": "🙏 Demander de l'aide",
    "hp_given": "Offert : {q} {k} — merci pour l'esprit d'équipe !",
    "hp_asked": "Ta demande a été envoyée à l'équipe !",
    "tab_storage": "📦 Stock",
    "tab_mines": "⛏ Mines",
    "tab_info": "📚 Info",
    "tab_lab": "🔬 Labo",
    "as_stone": "Pierre",
    "as_wood": "Bois",
    "as_fire": "Feu",
    "as_energy": "Électricité",
    "as_battery": "Piles",
    "as_cow": "Vaches",
    "as_core": "Noyau",
    "tool_1": "Outils rudimentaires",
    "tool_2": "Outils de réglage fin",
    "tool_3": "Calibrage",
    "tool_4": "Nanotechnologies",
    "tech_comm": "COMMUNICATIONS",
    "tech_scout": "RECONNAISSANCE",
    "tech_attack": "ATTAQUE",
    "tech_defense": "DÉFENSE",
    "tech_science": "SCIENCE",
    "ws_needTool": "Requis : {t}",
    "ws_teamItem": "🏆 Objet d'équipe — protège toute l'équipe (pour un Méga-Clan, prix ×{x})",
    "eff_make": "transforme les ressources brutes en matériau dans le stock",
    "eff_cart": "une charrette pour un cheval : +1 lots à la bourse",
    "eff_meds": "aucune maladie en raid ni dans les mines",
    "it_meds": "TROUSSE DE SECOURS",
    "mk_lots": "Lots ouverts : {o} sur {m} (🐎 {h} · 🛒 {c})",
    "badges": "🏅 Récompenses de saison",
    "sk_stable": "🐎 ÉCURIE",
    "sk_lots": "Lots à la bourse : {n}",
    "sk_buyHorse": "🐎 Acheter un cheval : {p} 🪙",
    "sk_stableHint": "Chaque cheval donne +1 lot à la bourse, chaque charrette encore +1 (pas plus de charrettes que de chevaux). Les pièces dépensées pour un cheval sont détruites.",
    "sk_horseBought": "🐎 Un cheval dans l'écurie ! Tu as plus de lots à la bourse.",
    "sk_shuttleCharge": "🚀 CHARGE DE LA NAVETTE",
    "sk_shuttleUntil": "🔋 Navette chargée jusqu'au {t}",
    "sk_shuttleEmpty": "🪫 Navette déchargée — les avantages de la bourse sont suspendus.",
    "sk_chargeBtn": "🔋 Recharger : 1 pile = {d} jours",
    "raid_needTech": "Les raids exigent 📡 communications, 🔭 reconnaissance et ⚔️ attaque niveau 1.",
    "raid_toLab": "🔬 Au Labo",
    "raid_scoutInfo": "La reconnaissance montre des cibles : {n}. Le carburant du raid, c'est l'hydrogène 💧",
    "raid_medsOn": "💊 Trousse de secours jusqu'au {t} : pas de maladie",
    "raid_medsOff": "💊 Sans trousse de secours, 15 % du butin se perd à l'infirmerie",
    "raid_note_sick": "🤒 Sans trousse de secours, une partie du butin s'est perdue à l'infirmerie",
    "mn_mined": "extrait : {n} {i}",
    "mn_left": "fin de l'extraction dans : {t}",
    "mn_commNote": "Le revenu va aux membres avec 📡 communications niv. 1+ ; sans 💊 trousse de secours, chaque 7e heure est perdue.",
    "top_season": "🏆 Saison",
    "top_rich": "💰 Les plus riches",
    "top_seasonTitle": "🏆 SAISON {s}",
    "top_left": "Fin de la saison dans : {t}",
    "top_myPlace": "Ta place : {p} sur {n} · gagné {e} 🪙",
    "top_noPlace": "Tu n'es pas encore au classement — joue et tu y entreras.",
    "top_prizes": "Les récompenses de la saison sont annoncées par l'organisateur. Le TOP 10 reçoit un badge de saison dans son passeport.",
    "top_rules": "On compte les pièces gagnées en jeu durant le mois : ferme, victoires, duels, quêtes, coffret, ventes. Les soldes ne sont jamais remis à zéro.",
    "top_players": "👤 JOUEURS DE LA SAISON",
    "top_teams": "🏆 ÉQUIPES DE LA SAISON",
    "top_empty": "La saison vient de commencer — sois le premier !",
    "top_noTeams": "Aucune bataille cette saison pour l'instant.",
    "top_teamRules": "Points selon la place dans les batailles de la saison : 10 · 7 · 5 · 4 · 3 · 2 · 1.",
    "lab_tools": "🧰 OUTILS",
    "lab_toolsHint": "Les kits ne s'usent jamais — ils débloquent les recettes avancées et les niveaux de technologie.",
    "lab_nextTool": "Kit suivant : {t}",
    "lab_craftTool": "Fabriquer le kit",
    "lab_toolsMax": "🧬 Tous les kits sont fabriqués !",
    "lab_level": "Niveau {l} sur {m}",
    "lab_max": "🏆 Niveau maximal",
    "lab_wait": "⏳ Niveau suivant dans {t}",
    "lab_up": "Étudier le niveau {l}",
    "res_stone_src": "duels, mines, coffre",
    "res_wood_src": "quêtes, mines, coffre",
    "res_fire_src": "Feu de camp à l'atelier",
    "res_energy_src": "chance à chaque victoire, mines, coffre",
    "res_battery_src": "atelier",
    "res_cow_src": "quêtes, coffre du 7e jour, bourse",
    "res_core_src": "mines et récompenses de l'organisateur",
    "sk_items": "🧪 Objets en réserve : {n} / {m} (10 % de la capacité)",
    "sk_cutletsName": "Cyber-côtelettes",
    "it_total": "En réserve : {n} pcs",
    "bt_entry": "🔋 Inscription de l'équipe : {n} / {m}",
    "bt_entered": "✅ L'équipe est inscrite à la bataille des mines",
    "bt_give": "Verser 🔋 (tu en as {n})",
    "bt_info": "Seules les équipes inscrites se battent pour les mines : {f} 🔋, clan — {fc} 🔋. Cotisez-vous en équipe !",
    "bt_notAllowed": "Cette bataille n'est pas ouverte à ton type d'équipe",
    "mn_place": "🏆 prix pour la {p}e place",
    "mn_soonShort": "Début : {d}",
    "top_events": "🎯 Événements",
    "ev_empty": "Aucun événement pour l'instant : reviens plus tard !",
    "ev_my": "Ta place : {p}",
    "ev_noPlace": "Tu n'es pas encore dans le classement : à toi de jouer !",
    "ev_manual": "L'organisateur désignera les gagnants",
    "ev_places": "Places primées : {n}",
    "ev_prizes": "🎁 Prix",
    "ev_leaders": "Leaders",
    "lab_sciGate": "📚 Le niveau {l} s'ouvre quand toutes les technologies sont au niveau {l}",
    "lab_cooldown": "Après l'étude, le niveau suivant s'ouvre dans {d} j.",
    "lab_done": "🔬 Terminé ! Niveau {l}",
    "lab_eff_comm": "Niveau 1 — raids et revenu des mines ; chaque niveau suivant −{c} min de recharge de raid",
    "lab_eff_scout": "Sans elle, pas de raids ; cibles en reconnaissance : 2 + niveau",
    "lab_eff_attack": "Sans elle, pas de raids ; chaque niveau après le premier : +{a} % de butin",
    "lab_eff_defense": "Chaque niveau : −{d} % de ce qu'un pillard peut te prendre",
    "lab_eff_science": "+{s} % de production de la ferme et de butin par niveau. Étude longue, exige ☢️ Noyau",
    "lab_how": "📖 Comment ça marche",
    "lab_rule1": "Les kits se fabriquent une seule fois : ⚒️ → 🛠 → 🔬 → 🧬. Sans le bon kit, impossible de prendre une recette avancée ou un niveau.",
    "lab_rule2": "Après l'étude d'un niveau, le niveau suivant de la même technologie s'ouvre 30 jours plus tard pile : chaque amélioration compte. La science suit les autres technologies.",
    "lab_rule3": "☢️ Le Noyau ne s'obtient qu'en équipe : places sur le podium des batailles et chaque journée passée à tenir une mine.",
    "durDH": "{d} j {h} h",
    "durHM": "{h} h {m} min",
    "durM": "{m} min",
    "ws_locked": "🔒 S'ouvre dans {t}",
    "ws_toStorage": "📦 L'objet ira dans ton stock",
    "eff_camo": "tu es invisible au repérage des raids, mais tu peux attaquer",
    "eff_trap": "un raideur qui échoue te donne le double",
    "eff_drill": "une égalité en défense compte comme un échec du raideur",
    "eff_thermos": "les Foreurs mangent les côtelettes 25% plus lentement",
    "eff_banner": "+5% de minage pour toute ton équipe",
    "eff_dome": "bouclier anti-raids pour toute l'équipe",
    "eff_forsage": "annule la recharge du raid (une fois par jour)",
    "eff_economizer": "le prochain vol sans hydrogène",
    "eff_cargo": "butin du prochain raid ×1,5",
    "eff_stamp": "la prochaine vente en bourse sans commission",
    "it_camo": "CAMOUFLAGE",
    "it_trap": "LEURRE",
    "it_drill": "ENTRAÎNEUR DE POSTURE",
    "it_thermos": "THERMOS À CÔTELETTES",
    "it_banner": "BANNIÈRE D'ÉQUIPE",
    "it_dome": "DÔME D'ÉQUIPE",
    "it_forsage": "POSTCOMBUSTION DU VAISSEAU",
    "it_economizer": "ÉCONOMISEUR",
    "it_cargo": "SOUTE AGRANDIE",
    "it_stamp": "TAMPON DE LA BOURSE",
    "it_oneShot": "usage unique",
    "it_charges": "⚡ Chargé : {n}",
    "it_needTeam": "Objet d'équipe — il faut être dans une équipe.",
    "it_charged": "⚡ Chargé ! Se déclenchera à la prochaine action.",
    "it_forsaged": "🔥 Recharge annulée — tu peux décoller !",
    "raid_armed": "⚡ Prêt : {l}",
    "raid_guardUntil": "{n} jusqu'à {t}",
    "raid_domeOn": "🛡 Dôme d'équipe jusqu'à {t}",
    "raid_forsageBtn": "🔥 Postcombustion : annuler la recharge ({n})",
    "raid_note_economizer": "⛽ Économiseur : vol sans hydrogène",
    "raid_note_cargo": "📦 Soute : butin ×1,5",
    "raid_note_trap": "🪤 Leurre de la cible : tu donnes le double",
    "raid_note_drill": "🎯 Entraîneur de posture de la cible : l'égalité compte comme un échec",
    "mn_title": "⛏ CARTE DES MINES",
    "mn_closed": "🔒 Impossible de partir en mine tant qu'aucune bataille d'équipes ou de clans n'est lancée.",
    "mn_pick": "Appuie sur une mine pour voir les détails.",
    "mn_info": "⛏ MINE",
    "mn_battle": "⚔️ BATAILLE « {t} » POUR LA MINE N°{n}",
    "mn_soon": "⏳ BATAILLE « {t} » POUR LA MINE N°{n} — DÉBUT {d}",
    "mn_nom": "Catégorie : {n}",
    "mn_ends": "Fin : {d}",
    "mn_leaders": "En tête actuellement",
    "mn_noLeaders": "Personne n'a encore marqué de points — ton équipe peut être la première !",
    "mn_myTeam": "🏆 TON ÉQUIPE DANS LES MINES",
    "mn_income": "Production : {n} ressources par heure pour toute l'équipe",
    "mn_noIncome": "Pas encore de mines — gagne une bataille d'équipes et la mine est à toi pendant 72 h.",
    "mn_noTeam": "Les mines se prennent en équipe — rejoins une équipe ou crée la tienne.",
    "mn_teamBtn": "🏆 Vers l'équipe",
    "mn_how": "📖 Comment ça marche",
    "mn_rule1": "Chaque bataille d'équipes et de clans se joue pour une seule mine. L'équipe avec le meilleur résultat cumulé de tous ses combattants dans la catégorie de la bataille l'emporte.",
    "mn_rule2": "Le vainqueur garde la mine {h} h : chaque combattant de l'équipe reçoit {y} ressource de la mine par heure. Plus de combattants, plus de production.",
    "mn_rule3": "Ensuite la mine est libérée, mais on ne peut la reprendre que lors d'une nouvelle bataille.",
    "mn_name": "⛏ MINE N°{n}",
    "mn_res": "Ressource",
    "mn_holder": "Propriétaire",
    "mn_free": "libre",
    "mn_untilL": "Tenue jusqu'au",
    "mn_pumping": "Produit : {n} {i} par heure",
    "mn_targetOf": "⚔️ Une bataille « {t} » est en cours pour cette mine",
    "mn_closedOne": "🔒 On ne peut la prendre que lors d'une bataille d'équipes — surveille les annonces.",
    "raid_noFuel": "⛽ Le vaisseau n'est pas prêt au décollage — il lui faut du carburant",
    "raid_shieldTitle": "🛡 BOUCLIER ANTI-RAIDS",
    "raid_shieldActive": "ACTIF",
    "raid_shieldInactive": "INACTIF",
    "raid_shieldHint": "Tant que le bouclier est actif, personne ne peut te raider. Il s'assemble à l'atelier et va dans ton stock — active-le quand tu veux.",
    "raid_toStorage": "📦 Ouvrir le stock",
    "sk_res": "📦 RESSOURCES EN STOCK",
    "sk_expand": "🔧 Agrandir le stock",
    "sk_cutlets": "🥩 CYBER-CÔTELETTES",
    "sk_cutletsHint": "Carburant des Cyber-Foreurs : 1 côtelette = une journée de travail.",
    "sk_refuel": "🚜 Ravitailler à la ferme",
    "it_nitrogen": "REFROIDISSEMENT À L'AZOTE +40%",
    "it_nuclear": "ACCÉLÉRATION NUCLÉAIRE X5",
    "it_drone": "MAÎTRE-DRONE",
    "it_shield": "BOUCLIER ANTI-RAIDS",
    "it_unlimit": "ILLIMITÉ JEUX",
    "it_unlimitDesc": "victoires aux jeux sans limite quotidienne",
    "it_hours": "{h} h",
    "it_use": "Activer",
    "it_empty": "Vide. Fabrique-en à l'atelier — l'objet atterrira ici.",
    "it_toWorkshop": "🔧 À l'atelier",
    "it_active": "✅ Actif jusqu'à {t}",
    "it_used": "✅ Activé ! Actif jusqu'à {t}",
    "it_stored": "📦 Prêt ! L'objet est dans ton stock — active-le dans l'onglet « Stock » quand tu en as besoin.",
    "sk_shuttle": "🚀 NAVETTE",
    "sk_shuttleOn": "Assemblée : commission de la bourse {f}%, limites d'ordres élargies.",
    "sk_shuttleOff": "Pas encore. S'assemble à l'atelier.",
    "sk_armor": "🦾 CYBER-ARMURE",
    "sk_armorOn": "Niveau {l} sur {m} : +{p}% de minage jusqu'au {t}.",
    "sk_armorOff": "Non équipée. Chaque niveau donne +{p}% de minage pendant 30 jours.",
    "sk_store": "🏗 AGRANDISSEMENT DU STOCK",
    "sk_storeLvl": "Capacité : {c} de chaque ressource.",
    "sk_storeMax": "🏆 Stock au maximum !",
    "hp_who": "Les joueurs à partir du niveau d'intellect {l} avec {c} côtelettes quotidiennes récupérées peuvent offrir.",
    "top": "👑 TOP-100 DES PLUS RICHES DE L'ÉCOSYSTÈME",
    "shop": "🏪 BOUTIQUE",
    "shopFarm": "🚜 POUR LA FERME",
    "shopGames": "🕹️ JEUX",
    "shopHint": "Paiement via les Telegram Stars officiels — ici même, en un tap.",
    "paid": "🎉 Payé ! L'article est déjà sur ton compte.",
    "payFail": "Le paiement n'est pas passé. Réessaie.",
    "oldClient": "Mets à jour Telegram pour acheter depuis l'appli, ou ouvre la boutique dans le chat du bot.",
    "ctaNoRobots": "💤 Ta ferme est presque vide ! Prends un robot plus puissant — les 🪙 tomberont 24h/24.",
    "ctaHungry": "🚨 Les Foreurs ont faim ({n} sans carburant) — le minage est à l'arrêt !",
    "ctaLowFuel": "⚠️ Moins de côtelettes qu'il n'en faut pour une journée de travail des Foreurs.",
    "ctaShopBtn": "🛒 Vers la boutique",
    "footer": "The whole game in one app",
    "noProfile": "Profil introuvable. Ouvre le bot et appuie sur /start !",
    "blocked": "Compte bloqué par l'administration.",
    "deleting": "Ton compte est en cours de suppression. Tu as changé d'avis ? Annule la suppression dans le chat du bot.",
    "error": "Impossible de charger les données. Réessaie plus tard.",
    "outside": "Ouvre cette application depuis le bot Telegram ROFL HUB.",
    "robotsTitle": "🤖 TES ROBOTS",
    "buyMore": "🛒 Acheter",
    "rateShort": "{v} 🪙/h",
    "refuelOne": "🥩 Charger 1",
    "refuelAll": "⚡ Tout charger",
    "refueled": "Chargé : {n} 🥩",
    "res_metal_src": "PFC",
    "res_hydrogen_src": "Plus/Moins",
    "res_crystal_src": "Quiz",
    "res_parts_src": "Cyber-Coffre",
    "resWhere": "où l'obtenir",
    "ws_title": "🔧 ATELIER",
    "ws_hint": "Les ressources des jeux se transforment en améliorations. Assez de ressources ? Appuie sur « Assembler ».",
    "ws_craft": "Assembler",
    "ws_owned": "✅ Déjà acquis",
    "ws_crafted": "C'est fait ! L'amélioration fonctionne déjà.",
    "ws_armor": "🛡 Cyber-Armure",
    "ws_armorLvl": "niveau {l}/{m} · +{p}% par niveau pour 30 jours",
    "ws_shuttleOn": "🚀 Navette assemblée : commission de la bourse {fee}%",
    "ws_shuttleOff": "🚀 Navette non assemblée : commission de la bourse {fee}%",
    "eff_nitrogen": "+40% de minage pour tous les robots",
    "eff_nuclear": "×5 de minage, les Foreurs mangent ×3 côtelettes",
    "eff_drone": "les robots ne vieillissent pas",
    "eff_shield": "personne ne peut te raider",
    "eff_cutlet": "1 cyber-côtelette dans ton stock (cher : le carburant est moins cher à la boutique)",
    "eff_armor": "+10% de minage par niveau pour 30 jours",
    "eff_storage": "plus de place pour les ressources — pour toujours",
    "eff_shuttle": "rien qu'à toi : commission de 5% sur tes ventes et ordres jusqu'à 500 côtelettes — pour toujours",
    "raid_title": "🏴‍☠️ RAIDS",
    "raid_how": "📖 Comment ça marche",
    "raid_rule1": "Tu choisis un geste ; la cible a réglé sa posture de défense à l'avance. Pierre-feuille-ciseaux tranche : c'est un duel de décisions, pas une loterie.",
    "raid_rule2": "Victoire : tu prends {pct}% de chaque ressource de la cible, jusqu'à {cap} par ressource. Échec : tu donnes {fpct}% des tiennes à la cible, jusqu'à {fcap}. Égalité : le carburant est brûlé.",
    "raid_rule3": "Seules les ressources peuvent être pillées. Pièces, robots et côtelettes sont en totale sécurité. Les nouveaux sont protégés {days} jours, les coéquipiers sont intouchables.",
    "raid_rule4": "Un vol coûte {fuel} 💧 d'hydrogène, le suivant dans {cd} h. Si quelqu'un te raide, la revanche est gratuite pendant {rh} h.",
    "raid_fuel": "💧 Hydrogène",
    "raid_ready": "🚀 Vaisseau prêt au décollage",
    "raid_cooldown": "⏳ Recharge : {m} min",
    "raid_shieldOn": "🛡 Bouclier jusqu'à {t}",
    "raid_shieldNewbie": "🛡 Protection des nouveaux",
    "raid_shieldOff": "🛡 Pas de bouclier — assemble-le à l'atelier",
    "raid_stance": "✊ TA POSTURE DE DÉFENSE",
    "raid_stanceHint": "C'est avec elle que tu reçois les raids. Change-la de temps en temps : les prévisibles se font piller plus souvent.",
    "raid_stanceNone": "Aucune posture choisie — elle sera aléatoire",
    "raid_stanceSaved": "Posture enregistrée",
    "raid_stats": "Raids : {a} ({w} réussis) · repoussés : {h} sur {d}",
    "raid_scout": "🔭 RECO : trouver des cibles",
    "raid_targets": "🎯 Choisis une cible",
    "raid_res": "ressources ≈{n}",
    "raid_noTargets": "Aucune cible disponible pour l'instant : boucliers, recharges, nouveaux. Repasse plus tard.",
    "raid_pickMove": "✊ Ton geste contre la posture de {name}",
    "raid_revenge": "⚔️ REVANCHE",
    "raid_revengeBtn": "⚔️ Riposter : {name}",
    "raid_win": "🏴‍☠️ Raid réussi !",
    "raid_draw": "😐 Égalité — le vaisseau est rentré à vide",
    "raid_lose": "💥 La défense a tenu",
    "raid_vs": "{m} contre {s}",
    "raid_loot": "Butin : {l}",
    "raid_lost": "Donné à la cible : {l}",
    "rock": "🪨 Pierre",
    "scissors": "✂️ Ciseaux",
    "paper": "📄 Feuille",
    "mk_title": "📈 BOURSE",
    "mk_stats": "Ordres : {o} · côtelettes : {c} · meilleur prix : {b} 🪙",
    "mk_feeLine": "Une commission de {f}% sur chaque vente est brûlée — bouclier anti-inflation",
    "mk_inv": "🥩 Dans ton stock : {n}",
    "mk_offers": "🛒 OFFRES",
    "mk_empty": "Aucune offre pour l'instant — sois le premier ou la première à vendre !",
    "mk_offer": "{q} 🥩 × {p} 🪙",
    "mk_buyHow": "Combien ?",
    "mk_all": "Tout ({q})",
    "mk_sellTitle": "💰 VENDRE DES CÔTELETTES",
    "mk_qty": "Combien de côtelettes",
    "mk_price": "Prix à l'unité, 🪙",
    "mk_preview": "Transaction {t} 🪙 · tu reçois {g} 🪙 · {f} 🪙 brûlées",
    "mk_sell": "Mettre en vente",
    "mk_limits": "Jusqu'à {q} côtelettes par ordre, jusqu'à {o} ordres ouverts",
    "mk_my": "📋 MES ORDRES",
    "mk_cancel": "Retirer",
    "mk_bought": "Acheté {q} 🥩 pour {t} 🪙",
    "mk_listed": "Ordre en ligne ! Je t'écris dès qu'il est vendu.",
    "mk_cancelledMsg": "Ordre retiré, les côtelettes sont revenues dans ton stock",
    "as_cutlet": "Côtelettes",
    "as_metal": "Métal",
    "as_hydrogen": "Hydrogène",
    "as_crystal": "Cristaux",
    "as_parts": "Composants",
    "mk_index": "📈 INDICE DE LA BOURSE",
    "mk_chart": "📊 PRIX SUR 7 JOURS",
    "mk_noTrades": "Aucune transaction pour l'instant — sois le premier ou la première !",
    "mk_avg": "Prix moyen de la semaine : {p} 🪙 · vendu : {v}",
    "mk_asks": "🛒 À VENDRE",
    "mk_bids": "🙋 À L'ACHAT",
    "mk_noBids": "Aucun ordre d'achat pour l'instant",
    "mk_sellTo": "Vendre",
    "mk_sellHow": "Combien vendre ?",
    "mk_bidTitle": "🙋 ORDRE D'ACHAT",
    "mk_bidHint": "Les pièces sont gelées dans l'ordre jusqu'à la transaction. Tu retires l'ordre, les pièces reviennent.",
    "mk_bid": "Placer l'ordre d'achat",
    "mk_bidPreview": "{t} 🪙 seront gelées",
    "mk_have": "Tu as : {n}",
    "mk_floor": "Une côtelette ne se vend pas moins de {p} 🪙 : le carburant de la boutique en Étoiles est toujours plus avantageux",
    "mk_side_sell": "je vends",
    "mk_side_buy": "j'achète",
    "mk_listedBid": "Ordre d'achat placé ! Les pièces sont gelées jusqu'à la transaction.",
    "mk_sold": "Vendu {q}, reçu {g} 🪙 après commission",
    "mk_shuttleNote": "🚀 Ta Navette : commission de {f}% sur tes ventes",
    "sw_title": "🔄 ÉCHANGE DE RESSOURCES",
    "sw_hint": "Donne ce qui est en trop, reçois ce qu'il te faut. Sans pièces ni commission.",
    "sw_give": "Tu donnes",
    "sw_want": "Tu veux recevoir",
    "sw_qty": "Combien",
    "sw_create": "Proposer un échange",
    "sw_take": "Échanger",
    "shop_info": "ℹ️ Ce que donne chaque article",
    "sw_youGet": "Tu reçois",
    "sw_youGive": "En échange, tu donnes",
    "sw_takeBtn": "Échanger — donner {x}",
    "sw_mineLine": "Tu donnes {g} → tu veux {w}",
    "sw_qtyErr": "Indique une quantité supérieure à zéro dans les deux champs",
    "sw_empty": "Aucune offre d'échange pour l'instant",
    "sw_mine": "Mes offres",
    "sw_done": "Échange conclu !",
    "sw_created": "Offre publiée, ressources mises de côté",
    "sw_cancelled": "Offre retirée, ressources rendues",
    "ws_armorUntil": "🛡 Armure active jusqu'au {t}",
    "st_title": "🛰 STATION D'ÉQUIPE",
    "st_level": "Niveau {l} sur {m}",
    "st_bonus": "+{p}% de minage pour chaque combattant",
    "st_next": "Pour le niveau {n}, il faut {c} de chaque ressource",
    "st_max": "🏁 La station est achevée !",
    "st_feed": "🧾 Derniers dons",
    "st_feedEmpty": "Aucun don pour l'instant — ouvre le bal !",
    "st_donate": "Donner",
    "st_all": "Tout",
    "st_done": "Don effectué !",
    "st_hint": "Toute l'équipe construit, chacun reçoit le bonus. Tu quittes l'équipe, tu perds le bonus.",
    "st_off": "La station est temporairement en maintenance",
    "goals_title": "🎯 OBJECTIFS DU JOUR",
    "goals_chest": "🎁 Coffret pour les trois : +{c} 🪙 et +{r} d'une ressource au hasard",
    "goals_streak": "🔥 Série : {s} j. · chaque {e}e jour d'affilée +{b} 🪙",
    "goals_claim": "🎁 OUVRIR LE COFFRET",
    "goals_claimed": "🎁 Le coffret du jour est récupéré. De nouveaux objectifs demain !",
    "goals_reset": "Les objectifs se renouvellent à 00:00 UTC",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · série {s} j.",
    "featureOff": "⚙️ Section en maintenance",
    "done": "C'est fait !",
    "loading": "⏳ Chargement…",
    "tab_friends": "🤝 Amis",
    "ref_title": "🤝 INVITE TES AMIS",
    "ref_rules": "{q} pour chaque ami actif, une seule fois. Un ami actif a atteint le niveau d'intelligence {l} et récupéré {c} côtelettes quotidiennes.",
    "ref_copy": "📋 Copier",
    "ref_copied": "Lien copié !",
    "ref_share": "📤 Partager",
    "ref_stats": "📊 TON RÉSEAU",
    "ref_invited": "invités",
    "ref_qualified": "actifs",
    "ref_earned": "gagnées",
    "ref_top": "🏆 QUI A LE PLUS D'AMIS",
    "ref_topHint": "✅ — amis actifs, 👥 — tous les invités",
    "ref_empty": "Le classement est encore vide — sois le premier ou la première !",
    "wk_title": "🔥 RECETTES DE LA SEMAINE",
    "wk_hint": "Recettes éphémères : elles apparaissent quand le hub le décide, puis disparaissent. Fabrique-les à temps !",
    "wk_left": "fabrications restantes cette semaine : {n} sur {m}",
    "st_cap": "📦 Stock : jusqu'à {c} de chaque ressource — le surplus de récolte est perdu",
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
    "invite": "🤝 Lien de parrainage : +500 par ami actif",
    "transfer": "🔄 Envoyer des pièces à un joueur",
    "market": "📈 Bourse des côtelettes : acheter ou vendre",
    "sell": "💰 Vendre des côtelettes : /sell quantité prix",
    "my_stats": "📊 Mes statistiques",
    "faq": "📚 Questions fréquentes",
    "rules": "📜 Conditions d'utilisation",
    "paysupport": "🛟 Assistance paiements",
    "workshop": "🔧 Atelier : des ressources en améliorations",
    "raid": "🏴‍☠️ Raids : reco et revanche",
    "goals": "🎯 Objectifs du jour et coffret",
    "station": "🛰 Station d'équipe : projet commun",
}
