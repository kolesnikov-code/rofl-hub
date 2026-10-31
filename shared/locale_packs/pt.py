"""Португальская (бразильская) локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> moedas
# Младший Майнер -> Robô Minerador
# Кибер-Бурильщик -> Ciber-Perfurador
# кибер-котлета -> ciber-bife (кратко: bife)
# Холодильник -> Geladeira
# склад (инвентарь) -> estoque
# ферма / Кибер-ферма -> fazenda / Ciber-Fazenda
# Ядерный Разгон x5 -> Boost Nuclear x5
# Азотное Охлаждение +40% -> Resfriamento a Nitrogênio +40%
# Мастер-дрон -> Drone Mestre
# Кибер-Сейф -> Ciber-Cofre
# Мега-Клан -> Mega-Clã
# Безлимит -> Sem Limite
# дуэли -> duelos (жест -> jogada, стол -> mesa, банк -> pote, ставка -> aposta)
# битвы -> Batalhas
# квесты -> Missões
# уровень интеллекта -> nível de inteligência
# команда / клан / банда -> equipe / clã / tropa
# ресурсы: Металл / Водород / Кристаллы / Детали -> Metal / Hidrogênio / Cristais / Peças
# Мастерская -> Oficina; Кибер-броня -> Ciber-Armadura; Шаттл -> Shuttle
# Налёт -> Saque (налёты -> Saques); Стойка обороны -> Postura de defesa
# Разведка -> Reconhecimento; Реванш -> Revanche; Щит -> Escudo
# Сундук -> Baú; Серия -> Sequência; Станция команды -> Estação da equipe

BUTTONS = {
    "main_menu": "📱 MENU PRINCIPAL",
    "profile": "👤 MEU PERFIL",
    "farm": "🚜 MINHA FAZENDA",
    "games_zone": "🕹️ ZONA DE JOGOS",
    "teams": "🏆 EQUIPES E CLÃS",
    "shop": "🏪 LOJA",
    "shop_cat_farm": "🚜 PARA A FAZENDA",
    "shop_cat_games": "🕹️ JOGOS",
}

STRINGS = {
    "quest.btn_answer_app": "🔐 Digitar a resposta no app",
    'duel.invite_msg': '⚔️ <b>{name}</b> te desafia para um duelo!\nAposta {stake} 🪙, o vencedor leva {payout} 🪙. O desafio vale por {hours} h.',
    'duel.invite_btn': '⚔️ Aceitar o desafio',
    'duel.invite_gone': '⌛ Este desafio não é mais válido: foi aceito, cancelado ou expirou.',
    'duel.invite_self': '😅 Esse é o seu próprio desafio — envie o link para um amigo.',
    'team.err_not_squad': '⚠️ Só um esquadrão pode ser ampliado.',
    'team.err_not_captain': '⚠️ Só o capitão pode fazer isso.',
    "quest.epic_locked": "⭐ As épicas são grandes histórias de 20+ minutos e abrem com o ⚡ Ilimitado.",
    "quest.locked": "🔒 Você já fez suas {n} missões novas de hoje. As outras abrem às 00:00 UTC — ou ative o ⚡ Ilimitado. As concluídas podem ser jogadas de novo.",
    # 27.10: «чат — дверь и почтальон», вся игра в приложении
    "app.moved": "🎮 Esta seção agora fica no app do jogo — lá é mais prático e bonito. Toque no botão 👇",
    "app.keyboard_gone": "🧹 Os botões antigos de baixo foram removidos: agora o jogo inteiro está no app. Você também pode abri-lo pelo botão «🎮 ROFL HUB» ao lado do campo de texto.",
    "start.console_app": "🚀 <b>Pronto!</b> O jogo inteiro está no app: toque no botão abaixo. Depois, você sempre pode abri-lo pelo botão «🎮 ROFL HUB» ao lado do campo de texto.",
    "start.welcome_back_app": "👋 <b>Que bom te ver de novo, @{username}!</b> Seu progresso está salvo — abra o jogo 👇",
    "menu.app": "📱 <b>ROFL HUB</b>\nO jogo inteiro está no app 👇\n\n<b>No chat:</b>\n• /invite — convidar um amigo\n• /transfer — enviar moedas\n• /faq — perguntas frequentes\n• /rules — termos de uso\n• /paysupport — ajuda com pagamentos\n• /delete_account — excluir a conta",
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
    # ---------------- geral ----------------
    "common.no_profile": "⚠️ Perfil não encontrado. Toque em /start para se registrar.",
    "common.btn_menu": "💿 Menu Principal",
    "common.blocked": "🚫 Sua conta foi bloqueada pela administração do ROFL HUB.",
    "common.feature_off": "⚙️ Esta seção está em manutenção. Volte um pouco mais tarde!",
    "common.maintenance": "🛠 O ROFL HUB está em manutenção rápida. Voltamos logo — suas moedas e seu progresso estão seguros!",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Que bom te ver de volta, @{username}!</b>\nSeu progresso está intacto. O painel de navegação fica na parte de baixo da tela.",
    "start.btn_continue": "🛸 CONTINUAR",
    "start.btn_cutlet": "Que ciber-bife é esse?🥩🤔",
    "start.btn_fight": "Conta logo e PARTIU BATALHA!",
    "start.console": "🚀 <b>Console de controle ativado! Use os botões na parte de baixo da tela.</b>",
    "start.intro1": (
        "👋 <b>Oi! Eu sou o ROFL HUB BOT — o bot principal do ecossistema de jogos ROFL HUB. "
        "Um hub de jogos e conhecimento de nova geração!</b>\n\n"
        "<b>Aqui você pode:</b>\n"
        "🎮 Jogar games de chat contra o bot e contra outros jogadores\n"
        "💸 Ganhar moedas do jogo com vitórias ou montar uma fazenda que minera 24 horas por dia\n"
        "🤼 Criar uma equipe e invadir o TOP do ranking\n"
        "🏆 Evoluir sua equipe para clã e disputar o ranking internacional\n"
        "💰 Faturar o prêmio de um milhão de moedas junto com a sua tropa\n"
        "👑 Comprar uma publicação em destaque nas nossas redes ou no site para divulgar você ou seu blog\n\n"
        "<b>Este chat-bot sabe:</b>\n"
        "🎮 Mostrar a lista de todos os jogos, canais e sites do ROFL HUB\n"
        "⚡ Creditar moedas por jogos, batalhas de equipes e clãs, conquistas, atividade e indicações\n"
        "🔄 Transferir moedas do jogo para outro jogador do ROFL HUB\n"
        "💎 Vender publicações no site e lugares VIP para personalidades e blogueiros\n"
        "🚀 Vender aceleradores, títulos, status e muito mais...\n\n"
        "<i>Toque em “CONTINUAR” e eu te conto mais detalhes 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>PEGUE AQUI SUAS PRIMEIRAS RECOMPENSAS DE REGISTRO!</b>\n"
        "..................................................\n"
        "💸 Você recebeu: <b>{balance} 🪙</b>\n"
        "🥩 Você recebeu: <b>{cutlets} ciber-bife</b>\n"
        "..................................................\n"
        "Esse é o seu bônus de boas-vindas por entrar no clube ROFL HUB.\n\n"
        "🔒 <i>O bônus é dado uma única vez, no momento do registro.</i>\n\n"
        "As moedas podem ser gastas de várias formas — elas são a base da economia do hub. Cuide bem delas...\n\n"
        "⁉️ <b>Mas com certeza ficou uma dúvida:</b> que bife é esse? Quem devo alimentar com ele?"
    ),
    "start.intro3": (
        "<b>PRIMEIRO, POR QUE AS MOEDAS DO JOGO SÃO TÃO IMPORTANTES?</b>\n\n"
        "As moedas movem todo o comércio, as competições e as compras no <b>ROFL HUB</b>. "
        "É quase a única moeda de jogo do mundo que dá para minerar de graça!\n"
        "..................................................\n"
        "<b>Há várias formas de consegui-las:</b>\n"
        "- Convidar amigos pelo seu link de indicação\n"
        "- Vencer jogos contra o bot\n"
        "- Vencer duelos contra outros jogadores\n"
        "- Participar de batalhas de equipes e clãs\n"
        "- Pegar o bônus diário de login e cumprir tarefas\n"
        "- Ter um robô que minera moedas 24/7 (Robô Minerador / Ciber-Perfurador)\n"
        "..................................................\n"
        "<b>Se você tem um robô de nível dois (o Ciber-Perfurador), ele precisa ser alimentado todo dia. "
        "É aí que entra o ciber-bife: o combustível da mineração automática, "
        "distribuído de graça todos os dias! Sua tarefa é simples — entrar e alimentar o robô.</b>\n\n"
        "Se esquecer de alimentar, o robô desliga e a mineração para.\n\n"
        "O Robô Minerador (nível um) não precisa de combustível. "
        "Importante! Todo robô é comprado por 30 dias — depois é preciso comprá-lo de novo ou ter um Drone Mestre. "
        "Você vai pegando o jeito pelo caminho:) Sem perder o foco.\n\n"
        "Quero contar só mais um pouco sobre o <b>ROFL HUB</b>, para você entender como tudo funciona por aqui.\n\n"
        "🛑 <b>Esta é a última mensagem da nossa apresentação. Depois disso, só batalha:)</b>"
    ),
    "start.intro4": (
        "<b>A VERSÃO CURTA. O ROFL HUB É:</b>\n"
        "- Jogos de chat-bot para todos os gostos\n"
        "- A chance de criar sua equipe (até 50 pessoas)\n"
        "- A chance de evoluí-la para clã (até 1000 pessoas)\n"
        "- Batalhas de equipes e clãs valendo prêmios\n"
        "- Página no Instagram — rofl_hub_global\n"
        "- O site rofl-hub.com para conversar e se divulgar sem cadastro\n"
        "- Milhares de jogadores no mundo todo — seus novos amigos podem estar entre eles!\n"
        "..................................................\n"
        "<b>Como prometido, esta é a mensagem final. Agora, só batalha! Comandos úteis:</b>\n\n"
        "/menu — controle rápido das funções\n"
        "/games — lista de todos os jogos\n"
        "/faq — perguntas frequentes\n"
        "/rules — termos de uso\n"
    ),

    # ---------------- menu e zona de jogos ----------------
    "menu.text": (
        "📱 <b>MENU PRINCIPAL DO ECOSSISTEMA ROFL HUB</b>\n"
        "..................................................\n"
        "👤 <b>PERFIL PESSOAL E PASSAPORTE:</b>\n"
        "• /start — Começar a apresentação e registrar a conta\n"
        "• /profile — Seu passaporte, saldo e equipe em tempo real\n"
        "• /my_stats — Seu histórico de estatísticas dos últimos 30 dias\n\n"
        "🚜 <b>CIBER-FAZENDA E AUTOMAÇÃO:</b>\n"
        "• /farm — Hub de combustível: abastecimento e velocidade de produção dos robôs\n"
        "• /shop — Marketplace: compra de mineradores, bifes e melhorias do hub\n\n"
        "🕹️ <b>SALA DE JOGOS:</b>\n"
        "• /games — Hub inline de todos os jogos contra o bot\n"
        "• /quiz — Quiz de velocidade: 30 segundos por resposta, níveis e bônus\n"
        "• /duel — DUELOS 1x1 com jogadores reais: mesas 10/100/1000\n"
        "• /quests — MISSÕES: histórias de detetive, comédias e enigmas com recompensas\n"
        "• /rps, /high_low, /safe — Jogos rápidos valendo moedas\n\n"
        "👥 <b>GESTÃO DA TROPA:</b>\n"
        "• /create_team — Registrar sua equipe por 100.000 🪙\n"
        "• /my_team — Painel da tropa e LISTA DE MEMBROS com níveis 🧠\n"
        "• /all_teams — Roleta de equipes aleatórias\n\n"
        "💸 <b>DINHEIRO E AMIGOS:</b>\n"
        "• /invite — Seu link de indicação: +500 🪙 por amigo ativo\n"
        "• /transfer — Enviar moedas a outro jogador\n\n"
        "📚 <b>GUIA E REGRAS:</b>\n"
        "• /faq — Guia completo do ecossistema (abre no Mini App)\n"
        "• /rules — Termos de uso\n"
        "..................................................\n"
        "<i>⚙️ Use o painel de jogo fixo de duas colunas na parte de baixo da tela para navegar na hora!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>BOAS-VINDAS À ZONA DE JOGOS DO ROFL HUB!</b>\n"
        "..................................................\n"
        "Aqui você pode enfrentar o bot em duelos rápidos ou encarar o "
        "teste relâmpago de inteligência para faturar alto — ou zerar o saldo!\n\n"
        "💸 Vitória paga: <b>+2 🪙</b> (Ciber-Cofre: <b>+5</b>)\n"
        "💀 Derrota desconta: <b>-1 🪙</b>, empate não custa nada\n"
        "🧠 No Quiz há um cronômetro de 30 segundos e níveis de inteligência: o nível 1 pede 10 respostas certas e paga <b>+100 🪙</b>, "
        "cada nível seguinte é 10 respostas mais longo — mas a recompensa cresce em 100!\n"
        "..................................................\n"
        "👇 <b>TOQUE EM UM BOTÃO ABAIXO PARA COMEÇAR UMA RODADA AGORA:</b>"
    ),
    "menu.btn_quiz": "🧠 Quiz",
    "menu.btn_rps": "🪨 Jokenpô",
    "menu.btn_hl": "📈 Maior/Menor",
    "menu.btn_safe": "🔐 Ciber-Cofre",
    "menu.btn_duel": "⚔️ DUELOS 1x1",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Passaporte, fazenda, equipe e o top dos mais ricos — em uma única tela neon. "
        "Dá até para pegar o bife diário direto por lá!\n\n"
        "👇 Toque no botão:"
    ),
    "app.btn": "🎮 ABRIR O MINI APP",
    "app.unavailable": "⚙️ O Mini App ainda está se conectando aos servidores do ecossistema. Volte daqui a pouco!",
    "faq.teaser": (
        "📚 <b>GUIA DO ECOSSISTEMA ROFL HUB</b>\n"
        "..................................................\n"
        "O resumo do que importa:\n"
        "🚜 Os robôs mineram moedas 24 horas por dia: Robô Minerador — 5/h sem combustível, "
        "Ciber-Perfurador — 10/h, e CADA Perfurador come o próprio ciber-bife por dia. "
        "Todos os robôs duram 30 dias (o Drone Mestre pausa o desgaste).\n"
        "🧠 Quiz: 30 segundos por resposta, níveis de inteligência com recompensas crescentes.\n"
        "⚔️ Duelos contra jogadores reais em mesas de 10/100/1000 🪙.\n"
        "🏆 Equipes de até 50 guerreiros (Mega-Clã — até 1000) e eventos de Batalha com prêmios para todos.\n"
        "..................................................\n"
        "👇 <b>O guia completo com todas as mecânicas — a um toque:</b>"
    ),
    "faq.btn_open": "📖 ABRIR O GUIA COMPLETO",
    "rules.teaser": (
        "📜 <b>TERMOS DE USO DO ROFL HUB</b>\n"
        "..................................................\n"
        "O essencial em poucas palavras:\n"
        "🪙 Moedas e todos os itens do jogo são elementos virtuais de entretenimento: "
        "não são dinheiro e não podem ser trocados por valores reais.\n"
        "💫 Compras somente via Telegram Stars oficiais; itens digitais são entregues "
        "na hora e, se a entrega falhar, as Stars são devolvidas automaticamente.\n"
        "🛡️ Não coletamos telefones, localização nem dados pessoais.\n"
        "🤝 Ofensas, esquemas de trapaça e multicontas são proibidos — violações podem levar a bloqueio.\n"
        "..................................................\n"
        "👇 <b>O texto completo dos termos e o aviso de isenção — a um toque:</b>\n"
        "<i>⚖️ Ao usar o bot, você confirma que aceita as condições.</i>"
    ),
    "rules.btn_open": "📜 ABRIR OS TERMOS COMPLETOS",
    "quest.list_header": (
        "🗺️ <b>MISSÕES DO ROFL HUB</b>\n"
        "..................................................\n"
        "Histórias interativas com escolhas e caminhos diferentes: detetives, comédias, enigmas. "
        "A primeira vitória em cada missão paga moedas, e você pode rejogar quantas vezes quiser!\n"
        "🌐 <i>Por enquanto as histórias das missões estão em russo — novos idiomas chegam em breve.</i>\n\n"
        "👇 <b>Escolha uma história:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} 🪙 pela primeira vitória\n"
        "..................................................\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Missão concluída, recompensa recebida. Rejogue à vontade!</i>",
    "quest.card_progress": "⏯ <i>Você parou no meio desta história.</i>",
    "quest.card_new": "🆕 <i>Você ainda não jogou esta história.</i>",
    "quest.btn_start": "▶️ COMEÇAR A MISSÃO",
    "quest.btn_restart": "🔄 RECOMEÇAR",
    "quest.btn_resume": "⏯ CONTINUAR",
    "quest.btn_list": "🗺️ Lista de missões",
    "quest.btn_replay": "🔄 Jogar de novo",
    "quest.win_first": "\n\n🏆 <b>MISSÃO CONCLUÍDA! Recompensa: +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>Concluída de novo!</b> A recompensa desta missão já foi recebida antes.",
    "quest.fail_footer": "\n\n💀 <i>Não foi o melhor dos finais... mas a história sempre pode ser rejogada!</i>",
    "quest.stale": "⏳ Essa cena já ficou para trás — seguindo do ponto atual!",
    "quest.no_coins": "❌ A dica custa {cost} 🪙 e seu saldo é menor. Dê um pulo na fazenda!",
    "quest.not_found": "❌ Missão não encontrada.",
    "menu.btn_quests": "🗺️ MISSÕES",

    # ---------------- fazenda ----------------
    "farm.btn_bonus": "🎁 PEGAR BÔNUS (um bife a cada 24 h)",
    "farm.btn_load1": "🥩 Carregar 1 bife",
    "farm.btn_loadall": "⚡ Carregar TODOS",
    "farm.btn_shop": "🏪 Entrar na Loja",
    "farm.status_all_fueled": "🟢 Todos os Ciber-Perfuradores estão abastecidos e minerando moedas!",
    "farm.status_partial": "🟡 {fueled} de {total} Ciber-Perfuradores abastecidos. Os outros esperam bifes na geladeira!",
    "farm.status_no_fuel": "🔴 Os Ciber-Perfuradores pararam! Falta combustível na geladeira.",
    "farm.status_no_drills": "💡 Pegue um robô mais forte no /shop — sua fazenda vai minerar mais.",
    "farm.boost_nuclear": "🔋 Boost Nuclear x5 até {until} UTC (consumo de bifes ×3)",
    "farm.boost_nitrogen": "❄️ Resfriamento a Nitrogênio +40% até {until} UTC",
    "farm.boost_drone": "🛸 O Drone Mestre prolonga a vida dos robôs até {until} UTC",
    "farm.no_boosts": "Nenhum boost ativo — dê uma olhada no /shop.",
    "farm.burnout": "🔥 Próxima queima de robô: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Ativar seu Robô Estagiário (grátis)",
    "farm.intern_activated": "🤖 Seu Robô Estagiário entrou no turno! +1 🪙 por hora para sempre, sem combustível e sem validade.",
    "farm.intern_already": "🤖 Seu Robô Estagiário já está trabalhando.",
    "farm.btn_claim_intern": "🎁 Resgatar Robô Estagiário ({n})",
    "farm.intern_pending": "🎁 Robôs Estagiários ganhos com seus níveis de intelecto: <b>{n}</b> — resgate no botão abaixo!",
    "farm.intern_claimed_new": "🤖 Um novo Robô Estagiário entrou em campo! +1 🪙 por hora para sempre.",
    "farm.intern_none": "🤖 Ainda não há novos Estagiários — o próximo espera você no nível de intelecto 10, 20, 30…",
    "games.intern_ready": "🎁 Seu novo nível rendeu um <b>Robô Estagiário</b> — resgate na sua fazenda!",
    "farm.intern_line": "• Robôs Estagiários ({rate} 🪙/h, eternos): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 Você tem um Robô Estagiário grátis! Toque no botão abaixo e ele vai minerar 1 🪙 por hora para sempre.",
    "farm.dashboard": (
        "🚜 <b>HUB CENTRAL DE COMBUSTÍVEL DO ROFL HUB</b>\n"
        "..................................................\n"
        "🤖 Robôs ativos na usina: <b>{total}</b>\n"
        "{intern}"
        "• Robôs Mineradores ({junior_rate} 🪙/h): <code>{junior}</code>\n"
        "• Ciber-Perfuradores ({premium_rate} 🪙/h): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VELOCIDADE ATUAL DA SUA FAZENDA:</b>\n"
        "• Produção por hora: <b>+{speed_hour} 🪙</b>\n"
        "• Produção por dia: <b>+{speed_day} 🪙</b>\n\n"
        "⚡ <b>BOOSTS:</b>\n{boosts}\n\n"
        "📋 <b>STATUS DA USINA DO JOGO:</b>\n"
        "{status}\n"
        "..................................................\n"
        "📦 <b>ESTADO DA GELADEIRA AUTOMÁTICA:</b>\n"
        "🥩 Reserva de combustível: <b>{fridge} / {capacity}</b>\n"
        "💼 Bifes no estoque: <code>{inv}</code>\n"
        "..................................................\n"
        "<i>💿 Importante: os robôs duram 30 dias (o Drone Mestre pausa o desgaste). "
        "CADA Ciber-Perfurador gasta o PRÓPRIO bife inteiro da geladeira a cada "
        "24 horas de trabalho: 3 robôs — 3 bifes por dia. Fique de olho no abastecimento!</i>"
    ),
    "farm.bonus_ok": "🎁 Ciber-bife creditado no estoque! Volte em 24 horas.",
    "farm.bonus_wait": "⏳ O bônus já foi pego! Próximo bife em {hours} h {minutes} min.",
    "farm.no_inv_cutlets": "❌ Você não tem ciber-bifes no estoque! Compre no /shop",
    "farm.fridge_full": "📦 Sua Geladeira já está completamente cheia!",

    # ---------------- perfil ----------------
    "profile.caption": (
        "📋 <b>PAINEL DO JOGADOR ROFL HUB</b>\n"
        "..................................................\n"
        "🆔 Seu ID de Passaporte: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Moedas agora: <b>{balance} 🪙</b>\n"
        "🏆 Seu status: <b>{team}</b>\n"
        "🧠 Nível de inteligência: <b>{level}</b> · até o nível {next_level}: "
        "<b>{left}</b> respostas certas no /quiz (recompensa: +{reward} 🪙)\n"
        "..................................................\n"
        "<i>Aqui aparece o que você tem neste exato momento. Use os botões para voar até as outras seções!</i>"
    ),
    "profile.no_team": "Sem equipe",
    "profile.team_label": "Equipe",
    "profile.clan_label": "Clã",
    "profile.btn_farm": "🚜 Minha Ciber-Fazenda",
    "profile.btn_shop": "🏪 Loja",
    "profile.stats": (
        "📊 <b>ESTATÍSTICAS DE CONQUISTAS (30 DIAS)</b>\n"
        "..................................................\n"
        "🧠 Nível de inteligência no jogo: <b>{level}</b> (total de respostas certas: {total})\n"
        "🎮 Rodadas de duelo jogadas: <b>{played}</b>\n"
        "🏆 Vitórias conquistadas: <code>{won}</code>\n"
        "👥 Amigos ativos convidados: <b>{refs}</b>\n"
        "..................................................\n"
        "<i>As estatísticas guardam suas conquistas históricas mesmo que as moedas ganhas já tenham sido gastas no mercado!</i>"
    ),
    "img.passport": "ID DO PASSAPORTE: {user_id}",
    "img.owner": "LÍDER: @{username}",
    "img.balance": "Saldo: {balance} moedas",
    "img.fridge": "Na geladeira: {fridge} / {capacity}",
    "img.inv": "Bifes no estoque: {inv}",
    "img.junior": "Robôs Mineradores: {count}",
    "img.premium": "Ciber-Perfuradores: {count}",

    # ---------------- jogos: motor comum ----------------
    "games.win": "🎉 <b>VITÓRIA!</b> 🎉\nCreditado: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>DERROTA!</b>\nDescontado: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>EMPATE!</b>\nNenhuma moeda descontada.",
    "games.limit": (
        "🛑 <b>Limite diário atingido!</b>\n\n"
        "Você já pegou {limit} vitórias em {game} hoje. O limite renova às 00:00 UTC.\n\n"
        "⚡ Remover o limite por 24 horas — 15 ★, por 30 dias — 249 ★ (seção “Jogos” no /shop)."
    ),
    "games.no_coins": "❌ Você tem 0 🪙 — nada para pagar a taxa da rodada. Colete a renda da fazenda no /farm!",
    "games.balance": "💰 Saldo: <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 Jogar de novo!",
    "games.btn_hub": "🕹️ Zona de jogos",
    "games.level_up": (
        "🏅 <b>NÍVEL DE INTELIGÊNCIA AUMENTOU: {level}!</b> Recompensa: <b>+{bonus} 🪙</b>!\n"
        "Próximo nível: {next_required} respostas certas → +{next_reward} 🪙."
    ),
    "games.name.rps": "Pedra-Papel-Tesoura",
    "games.intern_bonus": "🤖 Nível {level}! Mais um Robô Estagiário chegou à sua fazenda: agora são {count}.",
    "games.name.hl": "Maior/Menor",
    "games.name.quiz": "Quiz",
    "games.name.safe": "Cofre",
    "games.name.math": "Math",  # TODO(перевод 26.10)
    "games.name.flags": "Flags and capitals",  # TODO(перевод 26.10)
    "games.name.code": "Code breaker",  # TODO(перевод 26.10)
    "games.name.memory": "Memory",  # TODO(перевод 26.10)

    # ---------------- PPT ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>PEDRA-PAPEL-TESOURA</b>\n\n"
        "Vitória: <b>+{reward}</b> · Derrota: <b>-{penalty}</b> · Empate: <b>0</b>\n"
        "Limite de vitórias por dia: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Pedra",
    "rps.scissors": "✂️ Tesoura",
    "rps.paper": "🧻 Papel",
    "rps.draw": "🤝 <b>Empate!</b> Os dois escolheram {bot}.",
    "rps.win": "🏆 <b>Vitória!</b> {user} vence {bot}.",
    "rps.lose": "💀 <b>O bot venceu.</b> {bot} vence {user}.",

    # ---------------- Maior/Menor ----------------
    "hl.intro": (
        "🎲 <b>MAIOR OU MENOR</b>\n\nO bot definiu o número: <b>{base}</b>.\n"
        "O número escondido será maior ou menor?\n"
        "Vitória: <b>+{reward}</b> · Derrota: <b>-{penalty}</b> · Limite: <b>{limit}</b> vitórias"
    ),
    "hl.btn_up": "📈 Maior",
    "hl.btn_down": "📉 Menor",
    "hl.result": "🎲 <b>RESULTADO DA RODADA</b>\n\nNúmero do bot: <b>{base}</b> · Escondido: <b>{secret}</b>",

    # ---------------- quiz ----------------
    "quiz.round": (
        "🧠 <b>QUIZ • {category}</b>\n"
        "🤔 PERGUNTA: <b>{question}</b>\n\n"
        "<i>🌐 Por enquanto as perguntas estão em inglês — o pacote em português chega em breve!</i>"
    ),
    "quiz.btn_new": "🧠 Nova pergunta",
    "quiz.timeout": "⌛ <b>TEMPO ESGOTADO!</b> ⌛\nResposta certa: <b>{correct}</b>",
    "quiz.stale": "⏳ Esta pergunta não está mais ativa. Comece uma nova!",
    "quiz.stale_alert": "Esta pergunta não está mais ativa. Comece uma nova!",
    "quiz.empty": "⚠️ O banco de perguntas está vazio. Avise o administrador.",
    "quiz.wrong": "❌ <b>Errou</b> ❌\nResposta certa: <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} 🪙</b> pela derrota!",
    "quiz.level_line": (
        "🧠 Nível de inteligência: <b>{level}</b>\n"
        "Vitórias restantes até o nível {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} segundos para responder!\n"
        "Certa: +{win} 🪙 no saldo\n"
        "Errou / não deu tempo: -{penalty} 🪙\n"
        "Limite: {limit} vitórias por dia</i>"
    ),



    # ---------------- Cofre ----------------
    "safe.intro": (
        "🔐 <b>CIBER-COFRE</b>\n\n"
        "Lá dentro tem um prêmio de <b>{jackpot} 🪙</b>! A porta está trancada com um código de 1 a {codes}. "
        "Você tem só uma tentativa.\n"
        "Abriu: <b>+{jackpot}</b> · Alarme: <b>-{penalty}</b> · Limite: <b>{limit}</b> vitórias"
    ),
    "safe.btn_retry": "🔐 Arrombar de novo!",
    "safe.win": "🔓 <b>Cofre aberto!</b> O código era: <b>{code}</b>.",
    "safe.lose": "🚨 <b>O alarme disparou!</b> Você digitou {guess}, e o código era: <b>{code}</b>.",

    # ---------------- duelos ----------------
    "duel.intro": (
        "⚔️ <b>DUELOS 1x1: PEDRA-PAPEL-TESOURA VALENDO APOSTA</b>\n"
        "..................................................\n"
        "Escolha a mesa que cabe no seu bolso — igual no pôquer. A aposta é descontada na hora, "
        "e o adversário é um jogador real do ROFL HUB!\n\n"
        "💰 O pote = as duas apostas. O vencedor leva <b>{payout_percent}%</b> do pote, "
        "<b>{burn_percent}%</b> queima para sempre (deflação!).\n"
        "🤝 Empate — nova rodada na hora, com o pote na mesa.\n"
        "⏱ São <b>{move_timeout} segundos</b> por jogada; quem ficar calado tem a jogada sorteada automaticamente.\n"
        "🏆 Vitórias em duelos contam para a sua equipe nas Batalhas!\n\n"
        "👇 <b>ESCOLHA UMA MESA:</b>"
    ),
    "duel.btn_table": "⚔️ Mesa de {stake} 🪙",
    "duel.btn_cancel": "❌ Sair da mesa (devolver a aposta)",
    "duel.btn_move_rock": "🪨 Pedra",
    "duel.btn_move_scissors": "✂️ Tesoura",
    "duel.btn_move_paper": "🧻 Papel",
    "duel.waiting": (
        "🪑 <b>Você está na mesa de {stake} 🪙.</b> Sua aposta está no pote.\n"
        "Esperando o segundo guerreiro... Assim que ele sentar, vocês dois escolhem a jogada!\n"
        "<i>A fila dura {ttl} minutos; depois a aposta volta automaticamente.</i>"
    ),
    "duel.cancelled": "🚪 Você saiu da mesa. A aposta de <b>{stake} 🪙</b> voltou para o seu saldo.",
    "duel.expired": "⌛ Nenhum adversário apareceu na mesa de {stake}. A aposta de <b>{stake} 🪙</b> foi devolvida.",
    "duel.matched": (
        "⚔️ <b>ADVERSÁRIO ENCONTRADO! Mesa de {stake} 🪙.</b>\n"
        "Pote: <b>{bank} 🪙</b> · O vencedor leva: <b>{payout}</b>\n\n"
        "⏱ Você tem <b>{timeout} segundos</b> para escolher a jogada!"
    ),
    "duel.move_saved": "✊ Jogada registrada! Esperando a jogada do adversário...",
    "duel.draw_replay": (
        "🤝 <b>EMPATE! Rodada {round}.</b> Os dois mostraram a mesma jogada.\n"
        "O pote fica na mesa. ⏱ Mais {timeout} segundos — escolha a jogada:"
    ),
    "duel.win": (
        "🏆 <b>O DUELO É SEU!</b>\n\n"
        "Sua jogada {winner_move} vence {loser_move}.\n"
        "💰 Prêmio: <b>+{payout} 🪙</b> · 🔥 Queimado do pote: {burned}\n"
        "💼 Saldo: <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>DUELO PERDIDO.</b>\n\n"
        "A jogada {winner_move} do adversário vence a sua {loser_move}.\n"
        "📉 A aposta de <b>{stake} 🪙</b> foi para o pote do vencedor.\n"
        "Revanche?"
    ),
    "duel.reaper_prefix": "⏰ <b>Tempo da rodada esgotado!</b> As jogadas que faltavam foram sorteadas automaticamente.\n\n",
    "duel.bad_table": "❌ Essa mesa não existe.",
    "duel.already_in": "⚠️ Você já está em uma mesa ou em combate! Termine o duelo atual primeiro.",
    "duel.no_coins": "❌ Para esta mesa você precisa de {stake} 🪙 no saldo.",
    "duel.cancel_impossible": "⚠️ Esta fila não pode mais ser cancelada (adversário encontrado ou mesa fechada).",
    "duel.not_active": "⌛ Este duelo já terminou.",
    "duel.not_participant": "🔒 Este duelo não é seu!",
    "duel.move_already": "✋ Você já mostrou sua jogada nesta rodada. Esperando o adversário!",
    "duel.bad_move": "❌ Jogada desconhecida.",
    "duel.btn_rematch": "⚔️ Revanche (voltar às mesas)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 Patente: <b>{rank}</b>\n",
    "rank.rookie": "Novato",
    "rank.fighter": "Lutador",
    "rank.legend": "Lenda",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.king": "KING",

    # ---------------- indicações ----------------
    "ref.text": (
        "🤝 <b>PROGRAMA DE INDICAÇÃO DO ROFL HUB</b>\n"
        "..................................................\n"
        "Convide amigos pelo seu link pessoal e ganhe <b>{bonus}</b> "
        "por cada um que virar jogador ativo!\n\n"
        "🔗 <b>Seu link (toque para copiar):</b>\n<code>{link}</code>\n\n"
        "📊 <b>SUAS ESTATÍSTICAS:</b>\n"
        "👥 Amigos convidados: <b>{invited}</b>\n"
        "💰 Ganho com indicações: <b>{earned} 🪙</b>\n"
        "..................................................\n"
        "<i>Mande o link nos grupos da escola, para os amigos e nas redes — quanto maior a tropa, mais rápido o saldo cresce!</i>"
    ),
    "ref.btn_share": "📣 Compartilhar o link",
    "ref.share_text": "Entra no ecossistema de jogos ROFL HUB!",
    "ref.qualified_line": ("✅ <b>Amigo ativo</b> é quem chegou ao <b>nível de intelecto {level}</b> no quiz "
                           "e pegou <b>{claims} bifes diários</b> na fazenda. Aí você ganha <b>{bonus}</b>, "
                           "uma vez por amigo. Cadastro sem jogar não rende bônus — é mais justo para todos."),
    "ref.qualified_notify": ("🤝 <b>Seu amigo virou jogador ativo!</b>\n"
                             "Nível de intelecto {level} e {claims} bifes diários — feito. Você ganhou <b>{bonus}</b>. "
                             "Convide mais!"),

    "team.err_len": "❌ O texto deve ter de 1 a {max} caracteres!",
    "team.err_link": "🚨 Erro de segurança! Links, nomes de usuário e telefones são estritamente proibidos!",
    "team.err_badword": "❌ Palavrões detectados! Respeite as regras do hub.",
    "team.err_already": "⚠️ Você já está em uma equipe ou clã! Saia dela primeiro.",
    "team.err_money": "❌ Moedas insuficientes! Criar uma equipe custa {cost} 🪙, você tem {balance} 🪙.",
    "team.err_captain": "⚠️ Você já é capitão de outra equipe!",
    "team.err_taken": "⚠️ O nome «{name}» já está em uso! Invente um nome único.",
    "team.err_gone": "❌ Esta equipe não existe mais.",
    "team.err_full": "📦 Esta equipe não tem mais vagas!",
    "team.err_not_member": "❌ Você não está em uma equipe.",
    "mk.err_no_team": "🏆 A bolsa da equipe é para membros de equipes. Entre em uma equipe ou crie a sua.",
    "mk.err_team_only": "🔒 Este lote é só para membros da equipe do vendedor.",
    "help.err_qty": "Você pode pedir de 1 a {max} unidades de recurso.",
    "help.err_open": "Você já tem um pedido aberto — espere a ajuda ou cancele-o.",
    "help.err_not_found": "Este pedido já foi encerrado.",
    "help.err_self": "Não dá para atender o próprio pedido com um presente 🙂",
    "help.err_limit": "Hoje você já presenteou {max} recursos — o limite renova às 00:00 UTC.",
    "help.err_not_active": "🔒 Presentear recursos é possível a partir do nível {level} de inteligência e depois de {claims} ciber-bifes diários.",
    "it.err_none": "Esse item não está mais no seu estoque.",

    "acct.warn": (
        "⚠️ <b>EXCLUSÃO DA CONTA</b>\n"
        "..................................................\n"
        "Junto com a conta, isto será apagado <b>para sempre</b>:\n"
        "• moedas, bifes, recursos e todos os robôs da fazenda;\n"
        "• boosts, Sem Limite e tudo o que foi comprado com Stars — <b>as Stars não são devolvidas</b>;\n"
        "• VIP ID, progresso no quiz e nas missões;\n"
        "• sua vaga na equipe (a liderança passa ao veterano da equipe).\n"
        "As ordens abertas na bolsa são canceladas na hora e os itens voltam ao estoque.\n\n"
        "⏳ Primeiro a conta fica congelada por <b>{days} dias</b> — nesse período você pode desistir com um único botão. "
        "Depois, a exclusão é irreversível. Se voltar mais tarde, você começa do zero e o bônus inicial não é dado uma segunda vez.\n\n"
        "<i>O botão de exclusão funcionará em {seconds} segundos — leia com atenção.</i>"
    ),
    "profile.btn_delete": "🗑 Excluir conta",
    "acct.btn_keep": "✅ Não, manter a conta",
    "acct.btn_confirm": "🗑 Sim, excluir a conta",
    "acct.wait": "⏳ Aguarde mais {seconds} s — leia o que exatamente será apagado.",
    "acct.kept": "👍 Ótimo, a conta continua com você!",
    "acct.scheduled": (
        "🗑 A conta está congelada e será excluída em <b>{date}</b> (UTC).\n"
        "As ordens na bolsa foram canceladas e os itens voltaram ao estoque.\n\n"
        "Se mudar de ideia, toque no botão abaixo e tudo volta como era."
    ),
    "acct.pending_notice": (
        "⏳ A conta está congelada e será excluída em <b>{date}</b> (UTC).\n"
        "Quer continuar no jogo? Toque no botão abaixo."
    ),
    "acct.btn_undo": "↩️ Cancelar exclusão",
    "acct.undone": "🎉 Exclusão cancelada — a conta voltou a ser sua!",
    "acct.purged": "🗑 Sua conta ROFL HUB foi excluída. Obrigado por jogar! Se quiser voltar, toque em /start.",
    "acct.deleted_notice": "A conta foi excluída. Toque em /start para recomeçar.",
    "acct.welcome_back": (
        "👋 <b>Bem-vindo de volta!</b>\n"
        "Seu perfil foi criado de novo, do zero. O bônus inicial é dado uma única vez, por isso o saldo é 0 🪙. "
        "A fazenda, os jogos e o quiz esperam por você!"
    ),
    "tr.err_not_active": (
        "🔒 Você só pode enviar moedas depois do nível de inteligência {level} e de {claims} bifes diários resgatados — "
        "assim o ecossistema fica protegido contra contas falsas."
    ),

    # ---------------- transferências ----------------
    "tr.help": (
        "🔄 <b>TRANSFERÊNCIA DE MOEDAS PARA OUTRO JOGADOR</b>\n"
        "..................................................\n"
        "Formato do comando:\n"
        "<code>/transfer ID quantia</code> — pelo ID de Passaporte (aparece no /profile)\n"
        "<code>/transfer @username quantia</code> — pelo nome de usuário\n"
        "<code>/transfer ROFL-HUB-777 quantia</code> — por um VIP ID de leilão\n\n"
        "Exemplos:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Quantia mínima: <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ Destinatário não encontrado. Confira o ID de Passaporte ou o @username — o jogador precisa estar registrado no bot.",
    "tr.self": "🤨 Não dá para transferir moedas para você mesmo — isso seria uma economia infinita!",
    "tr.blocked": "🚫 Este jogador está bloqueado — transferências para ele estão indisponíveis.",
    "tr.min": "❌ A transferência mínima é de {min} 🪙.",
    "tr.insufficient": "❌ Moedas insuficientes! Seu saldo: <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ Moedas insuficientes no saldo.",
    "tr.confirm": (
        "🔄 <b>CONFIRME A TRANSFERÊNCIA:</b>\n\n"
        "👤 Destinatário: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Quantia a debitar: <b>{amount} 🪙</b>{fee_line}\n"
        "💰 O destinatário recebe: <b>{received} 🪙</b>\n\n"
        "<i>Transferências não podem ser desfeitas — confira o destinatário!</i>"
    ),
    "tr.fee_line": "\n🔥 Taxa do hub: <b>{fee} 🪙</b> (queimada)",
    "tr.btn_confirm": "✅ CONFIRMAR TRANSFERÊNCIA",
    "tr.btn_cancel": "❌ Cancelar",
    "tr.cancelled_toast": "Transferência cancelada",
    "tr.cancelled": "❌ <b>Transferência cancelada.</b> As moedas ficaram no lugar.",
    "tr.not_yours": "🔒 Esta transferência não é sua!",
    "tr.done_toast": "✅ Transferência concluída!",
    "tr.done": (
        "✅ <b>TRANSFERÊNCIA CONCLUÍDA!</b>\n\n"
        "💸 Enviado: <b>{amount} 🪙</b> para o jogador ID <code>{recipient_id}</code>\n"
        "💰 Seu saldo: <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>Você recebeu {amount} 🪙!</b>\n"
        "Remetente: ID <code>{sender_id}</code>. O saldo já foi atualizado — confira no /profile!"
    ),

    # ---------------- loja e pagamentos ----------------
    "shop.header": "🏪 <b>LOJA ROFL HUB</b>\nCompras via Telegram Stars oficiais. Escolha uma categoria com os botões abaixo.",
    "shop.cat_farm": (
        "🚜 <b>LOJA · PARA A FAZENDA</b>\n"
        "..................................................\n"
        "Robôs por 30 dias, combustível, geladeiras, boosts e o Drone Mestre.\n"
        "📦 Sua geladeira agora comporta: <b>{capacity} bifes</b>\n"
        "..................................................\n"
        "👇 <b>Escolha um item:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>LOJA · JOGOS</b>\n"
        "..................................................\n"
        "Remoção dos limites de vitórias, pacotes de moedas e a licença de Mega-Clã.\n"
        "..................................................\n"
        "👇 <b>Escolha um item:</b>"
    ),
    "pay.invoice_desc": "Entrega instantânea de conteúdo do jogo ROFL HUB.",
    "pay.invoice_error": "⚠️ Não foi possível gerar a fatura do Telegram Stars. Tente mais tarde.",
    "pay.success": "🎉 <b>Pagamento confirmado!</b>\n🧾 <code>{charge}</code>\n💵 Debitado: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 O pagamento passou, mas a entrega falhou temporariamente. Já estamos cuidando disso.\n"
        "Guarde o número do pagamento: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Suas Stars foram devolvidas automaticamente.",
    "pay.keep_charge": "Guarde o número do pagamento para o reembolso: <code>{charge}</code>",
    "pay.already": "✅ Este pagamento já foi processado, o item foi entregue antes.",
    "pay.support": (
        "🛟 <b>SUPORTE DE PAGAMENTOS TELEGRAM STARS</b>\n"
        "..................................................\n"
        "Todos os itens do ROFL HUB são digitais e entregues na hora após o pagamento.\n\n"
        "⚙️ <b>Se você pagou e o item não chegou:</b>\n"
        "o bot devolve as Stars automaticamente quando a entrega falha. Se isso não aconteceu — "
        "envie aqui o número do pagamento (está no recibo, formato <code>xxxx...</code>) e descreva o problema. "
        "A administração vai conferir o pagamento no banco de dados e resolver em até 24 horas.\n\n"
        "💫 <b>Política de reembolso:</b>\n"
        "o reembolso é possível se o item não foi recebido ou foi entregue com erro. "
        "Itens digitais entregues corretamente não são reembolsáveis.\n"
        "..................................................\n"
        "<i>Esta seção é o ponto oficial de suporte a compras conforme as regras do Telegram.</i>"
    ),

    # ---------------- entrega ----------------
    "dlv.cutlets": "🥩 Adicionado ao estoque: <b>{qty} bifes</b>.",
    "dlv.miner": "🤖 O robô <b>“{name}”</b> foi entregue na sua fazenda.\n⏳ Vida útil: até <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robô Minerador",
    "dlv.miner_premium": "Ciber-Perfurador",
    "dlv.fridge": "📦 Geladeira ampliada para <b>{capacity} bifes</b>.",
    "dlv.coins": "💰 Creditado <b>+{amount} 🪙</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nuclear x5 ativo até <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Resfriamento a Nitrogênio +40% ativo até <b>{until} UTC</b>.",
    "dlv.drone": "🛸 O Drone Mestre protege a fazenda até <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limites de vitórias removidos até <b>{until} UTC</b>.",
    "dlv.clan": "🏆 A equipe recebeu o status de <b>MEGA-CLÃ</b>: até {max} vagas.",
    "dlv.err_fridge": "Você já tem uma geladeira desse tamanho ou maior.",
    "dlv.err_no_team": "Você ainda não criou uma equipe. Crie primeiro com /create_team.",
    "dlv.err_mega": "Sua equipe já tem o status de Mega-Clã.",
    "dlv.intern_upgrade": "♾ Seu Robô Estagiário foi promovido a <b>Robô Minerador ETERNO</b>: 5 🪙 por hora, sem validade!",
    "dlv.err_no_intern": "Nenhum Robô Estagiário ativado: ative-o primeiro em /farm.",
    "dlv.err_intern_refs": "O upgrade exige {need} amigos ativos (as condições estão em /invite); você tem {have}.",
    "mk.header": "📈 <b>BOLSA DE BIFES</b>\n..................................................\nOrdens abertas: <b>{orders}</b> · bifes à venda: <b>{cutlets}</b> · melhor preço: <b>{best}</b>\nTaxa do hub: <b>{fee}%</b> por venda (queimada — escudo contra inflação)\n🥩 No seu estoque: <b>{inv}</b> bifes\n\n{body}\n\n<i>Toque numa ordem para comprar. Para vender, use /sell.</i>",
    "mk.empty": "Ainda não há ofertas. Seja o primeiro: /sell quantidade preço",
    "mk.order_line": "🥩 #{id} · <b>{qty} un.</b> a <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} un. a {price} 🪙",
    "mk.btn_my": "📋 Minhas ordens",
    "mk.btn_sell_help": "💰 Como vender bifes",
    "mk.btn_refresh": "🔄 Atualizar",
    "mk.btn_back": "← Voltar à bolsa",
    "mk.pick": "🛒 <b>Ordem #{id}</b>: {qty} un. disponíveis a {price} 🪙.\nQuantas?",
    "mk.btn_qty": "{qty} un. — {total} 🪙",
    "mk.btn_qty_all": "Todas, {qty} un. — {total} 🪙",
    "mk.buy_toast": "Negócio fechado!",
    "mk.buy_done": "✅ Comprou <b>{qty} bifes</b> por <b>{total} 🪙</b>. Já estão no estoque — abasteça seus Perfuradores!",
    "mk.sold_notify": "💰 <b>Bolsa: vendido!</b> Ordem #{id}: {qty} un. a {price}. Você recebeu <b>+{got} 🪙</b> (taxa de {fee} queimada).",
    "mk.sell_help": "💰 <b>COMO VENDER BIFES</b>\n\nComando: <code>/sell quantidade preço</code>\nExemplo: <code>/sell 10 250</code> — 10 bifes a 250 🪙 cada.\n\nOs bifes saem do estoque e ficam na ordem (cancele quando quiser). Até {max_qty} un. por ordem e {max_orders} ordens abertas. Uma taxa de {fee}% é queimada na venda. Um bife não sai por menos de {min} 🪙: o combustível da loja por Estrelas é sempre mais vantajoso que a bolsa. Recursos, ordens de compra e trocas ficam no app do jogo.",
    "mk.sell_confirm": "📝 Colocar <b>{qty} bifes</b> a <b>{price}</b> 🪙?\nTotal: {total} · taxa {fee} queima · você recebe <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ COLOCAR NA BOLSA",
    "mk.btn_cancel": "❌ Cancelar",
    "mk.sell_toast": "Ordem publicada!",
    "mk.sell_done": "✅ Ordem <b>#{id}</b> publicada: {qty} un. a {price} 🪙. Aviso quando vender.",
    "mk.cancelled_toast": "Cancelado",
    "mk.cancel_text": "❌ <b>Cancelado.</b> As bifes continuam no estoque.",
    "mk.my_header": "📋 <b>SUAS ORDENS</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} un. a {price} 🪙",
    "mk.my_empty": "📋 Você não tem ordens abertas.",
    "mk.btn_cancel_order": "❌ Retirar ordem #{id}",
    "mk.err_newbie_price": "🔒 While your account is new, you can buy at no more than {max} 🪙 apiece. The limit lifts at intelligence level {level} and after {claims} daily cutlets.",
    "mk.err_cancel_room": "📦 Not enough storage room: {free} free. Make room first, then withdraw the lot.",
    "sw.err_ratio": "⚖️ This swap is too uneven: the two sides (valued at the market's minimum prices) may differ by at most {x}×.",
    "mk.order_cancelled": "↩️ Ordem #{id} retirada: <b>{qty} bifes</b> voltaram ao estoque.",
    "mk.err_qty": "❌ Quantidade: de 1 a {max} un. por ordem.",
    "mk.err_price": "❌ Preço: de {min} a {max} 🪙 por unidade.",
    "mk.err_no_cutlets": "❌ Só há {have} bifes no estoque. As da geladeira não vão à bolsa — veja /farm.",
    "mk.err_too_many": "❌ Limite: no máximo {max} ordens abertas. Retire uma em «Minhas ordens».",
    "mk.err_not_found": "❌ Essa ordem já foi fechada.",
    "mk.err_own": "🤨 Não dá para comprar a própria ordem.",
    "mk.err_insufficient": "❌ Saldo insuficiente: precisa de {total} 🪙.",
    "farm.btn_market": "📈 Bolsa de bifes",

    # ---------------- recursos (onda 22.10, noite) ----------------
    "res.metal": "Metal",
    "res.hydrogen": "Hidrogênio",
    "res.crystal": "Cristais",
    "res.parts": "Peças",
    "res.none": "nada por enquanto",
    "games.resource_gain": "{icon} Minerado: <b>+{qty} {name}</b> (total {total}) → /workshop",
    "quest.win_resources": "\n📦 E mais 🪨 pedra: <b>{qty}</b> → /workshop",
    "profile.resources_line": "🧰 Recursos: {stock}\n",
    "menu.btn_goals": "🎯 Metas diárias",
    "menu.btn_raids": "🏴‍☠️ Saques",
    "menu.btn_workshop": "🔧 Oficina",
    "farm.btn_workshop": "🔧 Oficina",
    "farm.btn_app": "🏭 Fazenda no app",
    "menu.btn_app": "🚀 App do jogo: fazenda, oficina, saques",
    "app.btn_section": "🚀 ABRIR NO APP",
    "app.goto_workshop": "🔧 A <b>Oficina</b> fica no app do jogo: recursos, receitas e fabricação com um toque.",
    "app.goto_raids": "🏴‍☠️ Os <b>Saques</b> ficam no app do jogo: reconhecimento, postura de defesa e revanche.",
    "app.goto_station": "🛰 A <b>Estação da equipe</b> fica no app do jogo: progresso, contribuições e bônus para a equipe toda.",
    "app.goto_market": "📈 A <b>Bolsa de bifes</b> é mais prática no app do jogo: vitrine, vendas e suas ordens numa tela só.",
    "mk.err_asset": "❌ Esse item não existe na bolsa.",
    "mk.err_no_resource": "❌ Recurso insuficiente: no estoque há só {have}.",
    "mk.bid_filled_notify": "🙋 <b>Bolsa: ordem de compra executada!</b> Ordem #{id}: você comprou <b>+{qty} {icon}</b> a {price} 🪙.",
    "sw.err_same": "❌ Não dá para trocar um recurso por ele mesmo.",
    "sw.err_qty": "❌ Na troca, informe uma quantidade de 1 a {max}, tanto do que você dá quanto do que quer receber.",
    "shop.btn_info": "ℹ️ O que cada item dá",
    "sw.done_notify": "🔄 <b>Troca #{id} concluída!</b> Entregue: {give}, recebido: {want}.",
    "ws.err_coins": "🔒 Moedas insuficientes: precisa de {need} 🪙, você tem {have} 🪙.",
    "wk.eff_nitrogen": "❄️ Nitrogênio +40% por {h} h",
    "wk.eff_nuclear": "☢️ Nuclear x5 por {h} h",
    "wk.eff_drone": "🛸 Drone Mestre por {h} h",
    "wk.eff_shield": "🛡 Escudo por {h} h",
    "wk.eff_unlimit": "⚡ Sem Limite de jogos por {h} h",
    "wk.eff_cutlet": "🥩 Bife ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ Esta receita da semana não está mais disponível.",
    "wk.err_limit": "🔒 O limite semanal desta receita acabou ({limit}). A nova semana começa segunda-feira às 00:00 UTC.",
    "games.resource_full": "📦 O estoque de {icon} está cheio ({cap}) — o excedente se perde. Gaste, venda ou amplie o estoque na oficina.",
    "mk.err_storage_full": "📦 Falta espaço no estoque: livre {free}. Amplie o estoque na oficina.",
    "mk.err_buyer_full": "📦 O estoque do comprador está cheio — não dá para fechar o negócio agora (livre {free}).",
    "ws.recipe_storage": "Ampliar o estoque para {cap}",
    "ws.done_storage": "📦 <b>Estoque ampliado:</b> até {cap} de cada recurso. Para sempre.",
    "ws.err_storage_max": "📦 O estoque já está no tamanho máximo.",
    "farm.boost_armor": "🛡 Ciber-Armadura nv. {level}: +{percent}% de mineração até {until} UTC",
    "farm.boost_station": "🛰 Estação da equipe nv. {level}: +{percent}% de mineração",
    "clan.btn_station": "🛰 Estação da equipe",

    # ---------------- oficina ----------------
    "ws.header": (
        "🔧 <b>OFICINA</b>\n"
        "..................................................\n"
        "🧰 Seus recursos: {stock}\n"
        "⛏ Metal — PPT e duelos · 💧 Hidrogênio — Maior/Menor · "
        "💎 Cristais — Quiz · ⚙️ Peças — Ciber-Cofre. As missões dão um kit.\n\n"
        "🛡 Ciber-Armadura: <b>nível {armor}/{armor_max}</b> (+{armor_pct}% de mineração por nível, por 30 dias)\n"
        "🚀 Shuttle: <b>{shuttle}</b> — taxa da bolsa {shuttle_fee}%, até {shuttle_qty} bifes por ordem\n\n"
        "<i>✅ — recursos suficientes, 🔒 — ainda não. Um toque e pronto.</i>"
    ),
    "ws.shuttle_yes": "montado",
    "ws.shuttle_no": "não montado",
    "ws.recipe_nitro_6h": "Resfriamento a Nitrogênio por 6 h",
    "ws.recipe_nuclear_3h": "Boost Nuclear por 3 h",
    "ws.recipe_drone_24h": "Drone Mestre por 24 h",
    "ws.recipe_shield_24h": "Escudo contra saques por 24 h",
    "ws.recipe_cutlet": "Sintetizar um ciber-bife",
    "ws.recipe_armor": "Ciber-Armadura nv. {level}",
    "ws.recipe_shuttle": "Montar o Shuttle",
    "ws.btn_shuttle_owned": "🚀 Shuttle montado",
    "ws.btn_armor_max": "🛡 Ciber-Armadura: máximo",
    "ws.btn_refresh": "🔄 Atualizar",
    "ws.btn_farm": "🚜 Para a fazenda",
    "ws.noop": "Já está no máximo",
    "ws.toast": "Pronto!",
    "ws.done_nitrogen": "❄️ <b>Resfriamento a Nitrogênio +40%</b> ativo até {until} UTC.",
    "ws.done_nuclear": "☢️ <b>Boost Nuclear x5</b> ativo até {until} UTC. Os Perfuradores comem ×3 bifes!",
    "ws.done_drone": "🛸 O <b>Drone Mestre</b> protege os robôs até {until} UTC.",
    "ws.done_shield": "🛡 O <b>Escudo contra saques</b> aguenta até {until} UTC. Seus recursos estão protegidos.",
    "ws.done_cutlet": "🥩 Sintetizado: <b>+{qty} ciber-bife</b> no estoque. Abasteça em /farm!",
    "ws.done_armor": "🛡 <b>Ciber-Armadura nível {level}!</b> Mineração da fazenda: <b>+{percent}%</b> por 30 dias.",
    "ws.done_shuttle": "🚀 <b>Shuttle montado!</b> A taxa sobre as suas vendas agora é {fee}%, até {qty} bifes por ordem. O Shuttle é só seu, para sempre.",
    "ws.err_unknown": "❌ Essa receita não existe.",
    "ws.err_off": "🔧 Essa receita não está disponível no momento.",
    "ws.err_locked": "🔒 A receita abre em {hours} h — novas receitas abrem uma por dia.",
    "ws.recipe_camo_12h": "Camuflagem por 12 h",
    "ws.recipe_trap_24h": "Isca por 24 h",
    "ws.recipe_drill_24h": "Treino de postura por 24 h",
    "ws.recipe_forsage": "Pós-combustor da nave",
    "ws.recipe_economizer": "Economizador",
    "ws.recipe_cargo": "Porão ampliado",
    "ws.recipe_thermos_24h": "Térmica de bifes por 24 h",
    "ws.recipe_stamp": "Selo da bolsa",
    "ws.recipe_banner_24h": "Bandeira da equipe por 24 h",
    "ws.recipe_dome_12h": "Cúpula da equipe por 12 h",
    "it.err_no_cooldown": "🚀 Não há recarga a pular — a nave já está pronta para decolar.",
    "it.err_forsage_daily": "🔥 Pós-combustor já usado — o próximo em {hours} h.",
    "res.stone": "Pedra",
    "res.wood": "Madeira",
    "res.fire": "Fogo",
    "res.energy": "Eletricidade",
    "res.battery": "Baterias",
    "res.cow": "Vacas",
    "res.core": "Núcleo",
    "tech.comm": "Comunicação",
    "tech.scout": "Reconhecimento",
    "tech.attack": "Ataque",
    "tech.defense": "Defesa",
    "tech.science": "Ciência",
    "tech.err_max": "🏆 Este já é o nível máximo.",
    "tech.err_unknown": "❌ Essa tecnologia não existe.",
    "tech.err_tool": "🧰 Você precisa do kit de ferramentas de nível {tool} — monte-o no Laboratório.",
    "tech.err_cooldown": "⏳ O próximo nível pode ser estudado em {hours} h.",
    "tech.err_science": "📚 A ciência de nível {level} abre quando todas as outras tecnologias estiverem no nível {level}.",
    "ws.err_items_full": "📦 O armazém de itens está cheio: no máximo {max} itens. Ative algum ou amplie o armazém.",
    "post.scope_team": "Ranking de equipes",
    "post.scope_clan": "Ranking de clãs",
    "post.scope_teams": "Equipes e clãs",
    "post.scope_solo": "Ranking individual",
    "nom.farm_mined": "minerar mais moedas na fazenda",
    "nom.coins_earned": "ganhar mais moedas",
    "nom.duel_wins": "vencer mais duelos",
    "nom.duels_played": "jogar mais duelos",
    "nom.quiz_wins": "dar mais respostas certas no Quiz",
    "nom.rps_wins": "vencer mais partidas de pedra, papel e tesoura",
    "nom.safe_wins": "abrir mais Ciber-Cofres",
    "nom.game_wins_total": "vencer mais jogos contra o bot",
    "nom.referrals": "trazer mais amigos ativos",
    "nom.stars_spent": "apoiar mais o ecossistema (Stars)",
    "nom.insta_reels": "cujo reel no Instagram vai bombar mais",
    "nom.youtube_shorts": "cujo vídeo no YouTube Shorts vai bombar mais",
    "nom.tiktok": "cujo vídeo no TikTok vai bombar mais",
    "bt.err_closed": "⏳ Esta batalha já foi encerrada.",
    "bt.err_no_entry": "Esta batalha não exige inscrição.",
    "bt.err_no_team": "🏆 Entre em uma equipe primeiro.",
    "bt.err_scope": "Esta batalha não é para o seu tipo de equipe.",
    "bt.err_full": "✅ A inscrição da equipe já está completa.",
    "bt.err_battery": "🔋 Sem bateria — monte uma na oficina.",
    "horse.err_max": "🐎 O estábulo já tem {max} cavalos — não cabe mais.",
    "horse.err_coins": "🪙 Um cavalo custa {price} 🪙 — ainda falta.",
    "shuttle.err_none": "🚀 Monte primeiro o Shuttle na oficina.",
    "cart.err_horse": "🛒 A carroça precisa de um cavalo: no máximo tantas carroças quanto cavalos (e não mais que {max}).",
    "raid.err_need_tech": "🔬 Para um saque você precisa da tecnologia «{tech}» no nível 1 — estude-a no Laboratório.",
    "raid.err_battery": "🔋 O reconhecimento precisa de uma bateria — monte uma na oficina.",
    "games.energy_gain": "⚡ Sorte: +1 Eletricidade!",
    "ws.recipe_bonfire": "Fogueira: fogo de madeira e pedra",
    "ws.recipe_battery": "Baterias (×2)",
    "ws.recipe_cart": "Carroça",
    "ws.recipe_meds_72h": "Kit de primeiros socorros por 72 h",
    "ws.err_resources": "🔒 Faltam recursos: {kind} precisa de {need}, você tem {have}. Minere nos jogos!",
    "ws.err_shuttle_owned": "🚀 O Shuttle já está montado — é um por jogador.",
    "ws.err_armor_max": "🛡 A armadura já está no nível máximo ({max}).",

    # ---------------- saques ----------------
    "raid.header": (
        "🏴‍☠️ <b>SAQUES</b>\n"
        "..................................................\n"
        "💧 Hidrogênio: <b>{hydrogen}</b> (cada voo custa {fuel})\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ Postura de defesa: <b>{stance}</b>\n\n"
        "📊 Saques: <b>{attacks}</b> ({attack_wins} bem-sucedidos) · defesas seguradas: <b>{holds}/{defenses}</b>\n\n"
        "<i>O butim é só de recursos: {percent}% do estoque do alvo, no máximo {cap} por recurso. "
        "Moedas, robôs e bifes são intocáveis. Sua jogada contra a postura do alvo — "
        "decisão contra decisão. Um voo a cada {cooldown} h; a revanche é de graça.</i>"
    ),
    "raid.ready_line": "Nave pronta para decolar",
    "raid.cooldown_line": "Recarregando: faltam {minutes} min",
    "raid.shield_on": "Escudo ativo até {until} UTC",
    "raid.shield_newbie": "Proteção de novato (primeiros {days} dias)",
    "raid.shield_off": "Sem escudo — monte um em /workshop",
    "raid.stance_random": "aleatória (escolha uma no menu!)",
    "raid.btn_scout": "🔭 RECONHECIMENTO: achar alvos",
    "raid.btn_revenge": "⚔️ Revanche: {name}",
    "raid.btn_stance": "✊ Postura de defesa",
    "raid.btn_workshop": "🛡 Montar um escudo",
    "raid.btn_refresh": "🔄 Atualizar",
    "raid.btn_back": "← Voltar",
    "raid.btn_open": "🏴‍☠️ Abrir os saques",
    "raid.btn_again": "🏴‍☠️ Voltar aos saques",
    "raid.stance_pick": "✊ <b>Postura de defesa</b>\nSó o resultado de um saque alheio vai revelá-la: a jogada do atacante contra a sua postura. Mude de vez em quando — quem é previsível acaba saqueado.",
    "raid.stance_saved": "Postura: {stance}",
    "raid.scout": "🔭 <b>O reconhecimento achou alvos.</b> O voo desconta {fuel} 💧. Escolha:",
    "raid.btn_target": "🎯 {name} · recursos ≈{total}",
    "raid.no_targets": "🔭 O reconhecimento não achou ninguém: não há alvos adequados agora (escudos, recargas, novatos). Volte mais tarde.",
    "raid.pick_move": "✊ <b>Sua jogada?</b> Ela joga contra a postura de defesa do alvo. Voo: −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>Revanche! Sua jogada?</b> O voo é de graça e sem recarga.",
    "raid.result_win": "🏴‍☠️ <b>SAQUE BEM-SUCEDIDO!</b>\n{move} contra {stance} de {name}.\nButim: <b>{loot}</b>",
    "raid.result_draw": "😐 <b>Empate.</b> {move} contra {stance} de {name}. A nave voltou vazia, o combustível foi embora.",
    "raid.result_lose": "💥 <b>A DEFESA SEGUROU.</b> {move} contra {stance} de {name}.\nO alvo ficou com: <b>{loot}</b>",
    "raid.result_footer": "<i>Os recursos estão em /workshop. O escudo protege contra o troco.</i>",
    "raid.victim_lost": "🚨 <b>Você foi saqueado(a)!</b> {name}: {move} contra a sua postura {stance}.\nPerdido: <b>{loot}</b>\n\n⚔️ Revanche de graça por {hours} h. Escudo — em /workshop.",
    "raid.victim_draw": "🛡 <b>Saque terminou em empate.</b> {name}: {move} contra a sua postura {stance}. Nada perdido.",
    "raid.victim_held": "🛡 <b>Sua defesa segurou!</b> {name}: {move} contra a sua postura {stance}.\nTroféu da defesa: <b>{loot}</b>",
    "raid.err_stance": "❌ Jogada desconhecida.",
    "raid.err_self": "🤨 Saquear a si mesmo(a)? Não.",
    "raid.err_gone": "❌ Alvo indisponível.",
    "raid.err_teammate": "🤝 Não saqueamos os nossos — esse é um colega de equipe.",
    "raid.err_shielded": "🛡 O alvo tem escudo. Escolha outro.",
    "raid.err_revenge_gone": "❌ A janela de revanche fechou.",
    "raid.err_cooldown": "⏳ Recarregando: faltam {minutes} min.",
    "raid.err_victim_cooldown": "⏳ Esse alvo já foi saqueado há pouco (pausa de {hours} h).",
    "raid.err_fuel": "💧 Hidrogênio insuficiente: precisa de {need}, você tem {have}. Ele é minerado no Maior/Menor.",

    # ---------------- metas diárias ----------------
    "goal.header": (
        "🎯 <b>METAS DE HOJE</b>\n"
        "..................................................\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 Baú: <b>+{coins} 🪙</b> e <b>+{res}</b> de um recurso aleatório\n"
        "🔥 Sequência: <b>{streak}</b> dias · a cada {every}º dia seguido, +{bonus} 🪙 no baú\n\n"
        "<i>As metas são renovadas às 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ Feche as três — e o baú é seu.",
    "goal.status_ready": "✅ <b>Todas as metas fechadas! Pegue o baú.</b>",
    "goal.status_claimed": "🎁 O baú de hoje já foi pego. Amanhã tem metas novas!",
    "goal.btn_claim": "🎁 PEGAR O BAÚ",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Atualizar",
    "goal.toast": "Baú aberto!",
    "goal.chest": "🎁 <b>BAÚ ABERTO!</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 Sequência: {streak} dias",
    "goal.err_claimed": "🎁 Você já pegou o de hoje.",
    "goal.err_not_done": "⏳ Ainda faltam metas por fechar.",
    "goal.win_quiz": "Vencer {n} rodadas do quiz",
    "goal.win_rps": "Vencer {n} rodadas de PPT",
    "goal.win_hl": "Vencer {n} rodadas de Maior/Menor",
    "goal.win_safe": "Abrir o Ciber-Cofre {n} vezes",
    "goal.play_rounds": "Jogar {n} rodadas de qualquer jogo",
    "goal.duel": "Jogar um duelo",
    "goal.bonus": "Pegar o bife diário na fazenda",
    "goal.craft": "Montar algo na oficina",
    "goal.raid": "Fazer um saque",
    "goal.market_deal": "Fechar um negócio na bolsa",
    "goal.donate": "Investir recursos na estação da equipe",

    # ---------------- estação da equipe ----------------
    "st.header": (
        "🛰 <b>ESTAÇÃO DA EQUIPE “{team}”</b>\n"
        "..................................................\n"
        "Nível: <b>{level}/{max}</b> → cada guerreiro ganha <b>+{percent}%</b> de mineração na fazenda "
        "(+{per_level}% por nível)\n\n"
        "📦 Para o próximo nível:\n{progress}\n\n"
        "🧾 Últimas contribuições:\n{feed}\n\n"
        "🧰 Seus recursos: {stock}\n"
        "<i>A estação é de todos: a equipe inteira constrói, cada um recebe o bônus. Saiu da equipe — perdeu o bônus.</i>"
    ),
    "st.max_level": "🏁 Estação concluída — nível máximo!",
    "st.feed_empty": "ninguém contribuiu ainda — seja a primeira pessoa",
    "st.no_team": "🛰 A estação é construída pela equipe. Entre numa equipe ou crie a sua — e construam juntos.",
    "st.btn_find_team": "🏆 Equipes e clãs",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ Tudo: {qty} {icon} {name}",
    "st.btn_refresh": "🔄 Atualizar",
    "st.btn_team": "🏆 Para a equipe",
    "st.toast": "Investido +{qty} {icon}",
    "st.level_up": "🛰 <b>A estação da equipe subiu para o nível {level}!</b> Agora todos os guerreiros ganham +{percent}% de mineração na fazenda.",
    "st.err_qty": "❌ Quantidade inválida.",
    "st.err_no_team": "❌ Você não está em uma equipe.",
    "st.err_max": "🏁 A estação já está concluída (nível {max}).",
    "st.err_resources": "🔒 Recurso insuficiente: você tem {have}.",

    # ---------------- equipes/clãs (superfícies principais) ----------------
    "clan.no_team": "⚠️ <b>Você ainda não criou uma equipe!</b>\n\nVocê pode registrar sua própria tropa agora mesmo tocando no botão abaixo.",
    "clan.btn_create": "🏆 Criar Equipe por 100k",
    "clan.btn_members": "👥 LISTA DE MEMBROS",
    "clan.btn_leave": "🚪 Sair da equipe / Deixar a tropa",
    "clan.btn_dashboard": "🏆 Painel da equipe",
    "clan.status_clan": "👑 STATUS: CLÃ DO IMPÉRIO",
    "clan.status_team": "👥 STATUS: EQUIPE COMUM",
    "clan.dashboard": (
        "🏆 <b>PAINEL DE INFORMAÇÕES DA SUA EQUIPE</b>\n"
        "..................................................\n"
        "📌 Nome: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Capitão da tropa: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Lema: <i>“{motto}”</i>\n"
        "🔮 Símbolo do emblema: {symbol}\n\n"
        "👥 Membros: <b>{members} / {max_members}</b>\n"
        "..................................................\n"
        "👇 <b>NAVEGAÇÃO:</b>"
    ),
    "clan.members_only": "🔒 A lista de membros só é visível para quem faz parte desta equipe!",
    "clan.members_gone": "❌ Esta equipe já foi dissolvida.",
    "clan.members_header": (
        "👥 <b>ELENCO DA EQUIPE “{name}”</b>\n"
        "🧠 — nível de inteligência no jogo (só evolui no /quiz)\n"
        "..................................................\n"
    ),
    "clan.members_footer": (
        "\n..................................................\n"
        "📄 Página <b>{page} / {pages}</b> · Total de guerreiros: <b>{members}</b>\n"
        "<i>Toque no @username de um colega para falar com ele, montar seu próprio chat "
        "e chamar a tropa para as competições de equipe!</i>"
    ),
    "clan.btn_prev": "⬅️ Voltar",
    "clan.btn_next": "Avançar ➡️",
    "clan.join_ok": (
        "🎉 <b>PARABÉNS, VOCÊ ESTÁ NO JOGO!</b>\n\nVocê entrou na equipe <b>{name}</b>!\n"
        "📍 Use o comando /my_team para conferir o elenco!"
    ),
    "clan.leave_ok": "🚪 Você saiu da equipe <b>{name}</b>. Agora você está livre como um pássaro!",
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
    "ps_artsActive": "💠 Artefatos no cinto:",
    "ps_sellHow": "Para vender uma peça ou um artefato, toque nele na bolsa acima → «Vender». Só peças de nível Básico podem ser anunciadas.",
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
    "qs_fiction": "Todos os personagens, nomes e acontecimentos destas histórias são fictícios. Qualquer semelhança com pessoas reais, vivas ou falecidas, ou com fatos reais é mera coincidência.",
    "qs_check": "Verificar",
    "qs_tries": "Tentativas: {n}",
    "qs_wrong": "❌ Errado. Tentativas restantes: {n}",
    "qs_timeUp": "⏱ O tempo acabou!",
    "qs_timer": "⏱ Tempo para decidir",
    "qs_answerPh": "Sua resposta",
    "news_season": "🏁 Encerrados desde o dia 1: todo mês é uma nova temporada e as chances de todos voltam a ser iguais.",
    "qs_fxOff": "desligar efeitos:",
    "qs_fxOn": "ligar efeitos:",
    "tab_guide": "🧭 Como jogar",
    "dl_premOn": "⚡ You have Unlimited — the winnings fee is {b}% instead of {a}%.",
    "dl_premOff": "⚡ With Unlimited the winnings fee is {b}% instead of {a}%.",
    "md_title": "🧭 Como você quer jogar?",
    "md_hint": "O ROFL HUB é grande. Escolha por onde começar — dá para trocar de modo quando quiser no passaporte.",
    "md_full": "🌐 Todo o ecossistema",
    "md_fullText": "Fazenda de robôs, estoque, oficina, bolsa, equipes, saques, minas e o mapa do mundo — além de todos os jogos e histórias. Todas as seções ficam abertas desde o início.",
    "md_puzzle": "🧩 Jogos e histórias",
    "md_puzzleText": "Só o quiz, os minijogos, os quests, o Caso do dia e os duelos com amigos. Sem economia, sem abas extras.",
    "md_later": "A fazenda funciona em qualquer modo — as moedas se acumulam mesmo que você nunca dê uma olhada.",
    "md_toFull": "Ativar todo o ecossistema? A fazenda, o estoque, a bolsa, as equipes e as outras seções vão aparecer.",
    "md_toPuzzle": "Ficar só com jogos e histórias? A fazenda continua funcionando e as outras abas somem — dá para trazê-las de volta aqui mesmo.",
    "md_now": "🧭 Modo: {m} · trocar",
    "lk_new": "🎉 Novas seções abertas: <b>{t}</b>. Toque para dar uma olhada!",
    "di_title": "⚔️ Desafiaram você para um duelo!",
    "di_text": "<b>{n}</b> desafia você para um duelo de pedra, papel e tesoura.<br>Aposta {s} 🪙 · quem vencer leva {p} 🪙.",
    "di_accept": "⚔️ Aceitar o desafio",
    "di_decline": "Agora não",
    "di_waiting": "Esperando seu amigo na mesa de {s} 🪙…",
    "di_left": "O desafio vale por mais {h} h — depois a aposta volta",
    "di_share": "📤 Enviar o desafio a um amigo",
    "di_waitHint": "Envie o link a um amigo. Quando o desafio for aceito, o bot avisa você no chat. A aposta já está na mesa; mudou de ideia — saia da mesa e ela volta.",
    "di_head": "🤝 Desafiar um amigo",
    "di_hint": "Sua própria mesa por link: não entra na fila e espera só o seu amigo. Quem chegar novo pelo link vira seu amigo.",
    "di_table": "🤝 Desafiar um amigo · mesa de {s} 🪙",
    "di_shareText": "Desafio você para um duelo no ROFL HUB! Aposta {s} 🪙 — vamos ver quem ganha 😎",
    "ac_title": "🏅 Minhas conquistas",
    "ac_streak": "🔥 Sequência de Casos do dia: {n}",
    "ac_hint": "Todas as suas conquistas reunidas num cartão — poste no seu story ou envie a um amigo.",
    "ac_make": "📸 Criar o cartão",
    "ac_cardSub": "minhas conquistas",
    "ac_cardCall": "Consegue fazer melhor?",
    "ac_shareText": "Meu placar no ROFL HUB: 🧠 nível {l}, 🗺 {q} quests, 🕵️ {d} casos, ⚔️ {w} duelos vencidos. Consegue fazer melhor?",
    "ac_story": "📲 Postar no story",
    "ac_send": "✈️ Enviar a um amigo",
    "ac_save": "💾 Salvar a imagem",
    "ac_quests": "quests concluídos",
    "ac_epics": "épicos",
    "ac_cases": "casos resolvidos",
    "ac_duels": "duelos vencidos",
    "ac_wins": "vitórias em jogos",
    "ac_friends": "amigos ativos",
    "ac_robots": "robôs",
    "ac_days": "dias no jogo",
    "tf_title": "💸 Enviar moedas",
    "tf_hint": "Para um amigo — por @username, ID ou VIP ID. Mínimo {m} 🪙, taxa {f}%.",
    "tf_locked": "🔒 Enviar moedas libera no nível 🧠 {l} e depois de pegar {c} bifes diários — assim contas falsas não drenam as moedas iniciais. Receber já funciona.",
    "tf_to": "Para",
    "tf_amount": "Quantas 🪙",
    "tf_btn": "💸 Enviar",
    "tf_ask": "Enviar {a} 🪙 para {to}? Taxa {f} 🪙, chegam {r} 🪙.",
    "tf_done": "Pronto! {to} recebe {r} 🪙",
    "sq_choose": "Escolha o que criar:",
    "sq_squad": "🛡 Esquadrão",
    "sq_squadText": "Até {n} lutadores · {c} 🪙. Para você e alguns amigos; depois, quem comanda pode ampliar para equipe.",
    "sq_team": "🏆 Equipe",
    "sq_teamText": "Até {n} lutadores · {c} 🪙. Uma equipe grande para batalhas e minas.",
    "sq_createBtn": "Criar esquadrão por {cost} 🪙",
    "sq_created": "Esquadrão “{n}” criado — você está no comando!",
    "sq_label": "Esquadrão",
    "sq_upHint": "O esquadrão ficou apertado? Amplie para equipe — até {n} lutadores.",
    "sq_upBtn": "⬆️ Ampliar para equipe · {c} 🪙",
    "sq_upAsk": "Ampliar o esquadrão para equipe por {c} 🪙? Serão {n} vagas.",
    "sq_upDone": "Seu esquadrão agora é uma equipe!",
    "cs_title": "🕵️ Caso do dia",
    "cs_tile": "Um caso para todos · 4 suspeitos · uma só acusação",
    "cs_none": "Hoje não tem caso — volte amanhã.",
    "cs_culprit": "culpado",
    "cs_accuse": "👉 Acusar",
    "cs_clueLocked": "Pista {n} — ainda oculta",
    "cs_more": "🔍 Revelar outra pista (a recompensa vira {r} 🪙)",
    "cs_rules": "Dá para acusar só um suspeito e só uma vez. Quanto menos pistas precisar, maior a recompensa:",
    "cs_solved": "🎉 Caso resolvido! +{r} 🪙",
    "cs_failed": "Errou! O culpado era {n}.",
    "cs_bonus": "🔥 Bônus de sequência: +{b} 🪙",
    "cs_solution": "Solução:",
    "cs_stats": "Resolvido hoje: {s} de {p} · média de pistas: {a}",
    "cs_share": "📤 Exibir",
    "cs_next": "Novo caso em {t}",
    "cs_head": "🕵️ Caso nº {n}",
    "cs_suspects": "👥 Suspeitos",
    "cs_clues": "🔍 Pistas",
    "cs_streak": "🔥 Sequência de casos resolvidos: {n} · a cada {e}º dia seguido +{b} 🪙",
    "cs_accuseAsk": "Acusar {n}? Só existe uma acusação — não dá para voltar atrás.",
    "cs_shareText": "🕵️ Caso do dia nº {n}\n{s}\n🔥 Sequência: {k}\nConsegue resolver mais rápido?",
    "qs_epicPaid": "⚡ com Ilimitado",
    "qs_paper": "📝 Dica: anote os detalhes no papel — quem presta atenção resolve mais fácil.",
    "qs_total": "📚 Missões na biblioteca: {n}",
    "qs_daily": "Novas hoje: {a}/{b}",
    "qs_dailyUnl": "⚡ Ilimitado — missões sem limite",
    "qs_locked": "🔒 até 00:00 UTC",
    "qs_lockedNote": "Você concluiu {b} missões novas hoje. As outras abrem às 00:00 UTC, e as concluídas dá para jogar de novo quantas vezes quiser. ⚡ Ilimitado remove o limite.",
    "qs_epic": "⭐ ÉPICA ·",
    "qr_btn": "⚠️ Denunciar a pergunta",
    "qr_title": "O que há de errado na pergunta?",
    "qr_answer": "❌ A resposta certa está errada",
    "qr_question": "✏️ Erro ou erro de digitação na pergunta",
    "qr_dup": "🔁 A pergunta se repete",
    "qr_other": "🤔 Outro (confusa, discutível)",
    "qr_thanks": "Valeu! A pergunta será verificada e corrigida.",
    "qr_limit": "Já são denúncias suficientes por hoje — obrigado pela ajuda!",
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
    "subtitle": "seu império de jogos em uma única tela",
    "tab_passport": "📋 Passaporte",
    "tab_farm": "🚜 Fazenda",
    "tab_goals": "🎯 Metas",
    "tab_workshop": "🔧 Oficina",
    "tab_raids": "🏴‍☠️ Saques",
    "tab_market": "📈 Bolsa",
    "tab_team": "🏆 Equipe",
    "tab_shop": "🏪 Loja",
    "tab_top": "👑 TOP",
    "passport": "📋 PASSAPORTE DO JOGADOR",
    "coins": "🪙",
    "brain": "🧠 Nível de inteligência",
    "toNext": "até o nível {n}: {left} respostas certas no quiz (+{reward} 🪙)",
    "farm": "🚜 CIBER-FAZENDA",
    "robots": "Robôs (mineradores / perfuradores)",
    "intern": "Robôs Estagiários (1 🪙/h, eternos)",
    "activateIntern": "🚀 ATIVAR ROBÔ ESTAGIÁRIO",
    "claimIntern": "🎁 RESGATAR ESTAGIÁRIO ({n})",
    "internDone": "🤖 Seu Robô Estagiário entrou no turno!",
    "rank": "🎖 Patente",
    "openFarm": "🏭 ABRIR A MINA",
    "farmScene": "🏭 SUA FAZENDA",
    "back": "← Voltar",
    "minedVisit": "minerado nesta visita",
    "unit_intern": "Robô Estagiário",
    "unit_junior": "Robô Minerador",
    "unit_premium": "Ciber-Perfurador",
    "eternal": "eterno",
    "fueledAll": "abastecidos",
    "fueledPart": "{a} de {b} abastecidos",
    "license": "licença de 30 dias",
    "emptyFarm": "A mina está vazia. Ative seu Robô Estagiário ou compre robôs na loja!",
    "madeBy": "Quer um bot assim para o seu projeto? Fale com @mister_telebot",
    "fueled": "Perfuradores abastecidos",
    "speed": "Velocidade de mineração",
    "perHour": "{v} 🪙/h",
    "fridge": "Geladeira",
    "inv": "Bifes no estoque",
    "burnout": "Próxima queima",
    "boosts": "Boosts ativos",
    "none": "nenhum",
    "resources": "🧰 Recursos",
    "bonusPct": "Bônus permanente de mineração",
    "shuttle": "🚀 Shuttle montado",
    "resHint": "Cada vitória traz o recurso do seu jogo, com Sem Limite — sem restrições. Gaste-os na oficina.",
    "bonusReady": "🎁 PEGAR O BIFE DIÁRIO",
    "bonusWait": "⏳ Bônus em {h} h {m} min",
    "bonusDone": "🎉 Bife no estoque!",
    "team": "🏆 MINHA EQUIPE",
    "clan": "CLÃ",
    "teamLabel": "Equipe",
    "captain": "👑 Você está no comando!",
    "members": "Elenco",
    "noTeam": "Você ainda está sem equipe: entre em uma pela roleta ou pela busca — ou crie a sua.",
    "tab_faq": "📚 FAQ",
    "tab_rules": "📜 Termos",
    "tm_roulette": "🎲 ROLETA DE EQUIPES",
    "tm_rotate": "🔄 Mostrar outras equipes",
    "tm_noFree": "Ainda não há equipes livres — crie a sua!",
    "tm_search": "🔍 BUSCAR EQUIPE",
    "tm_searchPh": "Nome ou parte dele",
    "tm_searchBtn": "Buscar",
    "tm_notFound": "Nenhuma equipe com esse nome",
    "tm_join": "💥 Entrar",
    "tm_joined": "Você está na equipe «{n}»!",
    "tm_create": "🏆 CRIAR EQUIPE",
    "tm_hubHint": "Uma equipe de até 50 guerreiros custa {cost} 🪙. Na loja ela pode ser ampliada para Mega-Clã com 1000 vagas.",
    "tm_name": "Nome (até {n} caracteres)",
    "tm_motto": "Lema (até {n} caracteres)",
    "tm_symbol": "Emblema — um emoji (até {n} caracteres)",
    "tm_createBtn": "Criar por {cost} 🪙",
    "tm_created": "Equipe «{n}» criada — você é o capitão!",
    "tm_noMoney": "Você precisa de {cost} 🪙, tem {b} 🪙",
    "tm_roster": "👥 ELENCO DA EQUIPE",
    "tm_mottoL": "💬 Lema",
    "tm_leave": "🚪 Sair da equipe",
    "tm_leaveAsk": "Sair mesmo da equipe «{n}»?",
    "tm_leaveAskCaptain": "Você é o capitão: a coroa passa ao veterano da equipe. Sair mesmo de «{n}»?",
    "tm_left": "Você não está mais em uma equipe",
    "mk_scopePublic": "🌐 Bolsa geral",
    "mk_scopeTeam": "🏆 Bolsa da equipe",
    "mk_teamHint": "Bolsa da equipe «{t}»: só colegas de equipe veem e compram os lotes, a taxa é de apenas {f}%.",
    "mk_yourStock": "📦 Você tem",
    "mk_yourCoins": "💰 Suas moedas",
    "tm_market": "🏪 BOLSA DA EQUIPE",
    "tm_marketBtn": "Abrir a bolsa da equipe",
    "tm_marketHint": "Negocie com colegas de equipe: taxa de {f}% em vez de {p}% na bolsa geral. No Mega-Clã — só {c}%.",
    "hp_title": "🤝 AJUDA MÚTUA",
    "hp_hint": "Falta um recurso? Peça à equipe. Cada um pode presentear até {d} recursos por dia.",
    "hp_today": "Presenteado por você hoje: {g} / {d}",
    "hp_empty": "Ninguém pediu ajuda por enquanto",
    "hp_give": "🎁 +{n}",
    "hp_kind": "O que você precisa",
    "hp_qty": "Quanto (até {n})",
    "hp_ask": "🙏 Pedir ajuda",
    "hp_given": "Presenteado: {q} {k} — valeu pelo jogo em equipe!",
    "hp_asked": "Pedido enviado à equipe!",
    "tab_storage": "📦 Estoque",
    "tab_mines": "⛏ Minas",
    "tab_info": "📚 Info",
    "tab_lab": "🔬 Laboratório",
    "as_stone": "Pedra",
    "as_wood": "Madeira",
    "as_fire": "Fogo",
    "as_energy": "Eletricidade",
    "as_battery": "Baterias",
    "as_cow": "Vacas",
    "as_core": "Núcleo",
    "tool_1": "Ferramentas rústicas",
    "tool_2": "Ferramentas de ajuste fino",
    "tool_3": "Calibragem",
    "tool_4": "Nanotecnologia",
    "tech_comm": "COMUNICAÇÃO",
    "tech_scout": "RECONHECIMENTO",
    "tech_attack": "ATAQUE",
    "tech_defense": "DEFESA",
    "tech_science": "CIÊNCIA",
    "ws_needTool": "Precisa de: {t}",
    "ws_teamItem": "🏆 Item de equipe — protege a equipe toda (para Mega-Clã o preço é ×{x})",
    "eff_make": "transforma matéria-prima em material no estoque",
    "eff_cart": "uma carroça para o cavalo: +1 lotes na bolsa",
    "eff_meds": "sem doenças nos saques e nas minas",
    "it_meds": "KIT DE PRIMEIROS SOCORROS",
    "mk_lots": "Lotes abertos: {o} de {m} (🐎 {h} · 🛒 {c})",
    "badges": "🏅 Prêmios das temporadas",
    "sk_stable": "🐎 ESTÁBULO",
    "sk_lots": "Lotes na bolsa: {n}",
    "sk_buyHorse": "🐎 Comprar cavalo por {p} 🪙",
    "sk_stableHint": "Cada cavalo dá +1 lote na bolsa e cada carroça mais +1 (não mais carroças que cavalos). As moedas pagas pelo cavalo são queimadas.",
    "sk_horseBought": "🐎 Cavalo no estábulo! Agora você tem mais lotes na bolsa.",
    "sk_shuttleCharge": "🚀 CARGA DO SHUTTLE",
    "sk_shuttleUntil": "🔋 Shuttle carregado até {t}",
    "sk_shuttleEmpty": "🪫 Shuttle descarregado — as vantagens da bolsa não valem.",
    "sk_chargeBtn": "🔋 Carregar: 1 bateria = {d} dias",
    "raid_needTech": "Para os saques você precisa de 📡 comunicação, 🔭 reconhecimento e ⚔️ ataque no nível 1.",
    "raid_toLab": "🔬 Ao Laboratório",
    "raid_scoutInfo": "A exploração mostra alvos: {n}. O combustível do ataque é hidrogênio 💧",
    "raid_medsOn": "💊 Kit de primeiros socorros até {t}: sem medo de doenças",
    "raid_medsOff": "💊 Sem o kit, 15% do espólio se perde na enfermaria",
    "raid_note_sick": "🤒 Sem o kit, parte do espólio se perdeu na enfermaria",
    "mn_mined": "extraído {n} {i}",
    "mn_left": "até o fim da extração: {t}",
    "mn_commNote": "A renda vai para quem tem 📡 comunicação 1+; sem o 💊 kit, toda 7ª hora se perde.",
    "top_season": "🏆 Temporada",
    "top_rich": "💰 Ricos",
    "top_seasonTitle": "🏆 TEMPORADA {s}",
    "top_left": "Fim da temporada em: {t}",
    "top_myPlace": "Sua posição: {p} de {n} · ganhou {e} 🪙",
    "top_noPlace": "Você ainda não está na tabela — jogue e a posição aparece.",
    "top_prizes": "Os prêmios da temporada são anunciados pelo organizador. O TOP-10 ganha um selo da temporada no passaporte.",
    "top_rules": "Contam as moedas ganhas no jogo no mês: fazenda, vitórias, duelos, missões, baú, vendas. O saldo não é zerado.",
    "top_players": "👤 JOGADORES DA TEMPORADA",
    "top_teams": "🏆 EQUIPES DA TEMPORADA",
    "top_empty": "A temporada acabou de começar — seja o primeiro!",
    "top_noTeams": "Ainda não houve batalhas nesta temporada.",
    "top_teamRules": "Pontos por posição nas batalhas da temporada: 10 · 7 · 5 · 4 · 3 · 2 · 1.",
    "lab_tools": "🧰 FERRAMENTAS",
    "lab_toolsHint": "Os kits não se gastam — eles liberam montagens avançadas e níveis de tecnologia.",
    "lab_nextTool": "Próximo kit: {t}",
    "lab_craftTool": "Montar o kit",
    "lab_toolsMax": "🧬 Todos os kits montados!",
    "lab_level": "Nível {l} de {m}",
    "lab_max": "🏆 Nível máximo",
    "lab_wait": "⏳ Próximo nível em {t}",
    "lab_up": "Estudar nível {l}",
    "res_stone_src": "missões, minas, baú",
    "res_wood_src": "minas, baú",
    "res_fire_src": "Fogueira na oficina",
    "res_energy_src": "chance por vitória, minas, baú",
    "res_battery_src": "oficina",
    "res_cow_src": "baú do 7º dia, bolsa",
    "res_core_src": "minas e prêmios do organizador",
    "sk_items": "🧪 Itens no armazém: {n} / {m} (10% da capacidade)",
    "sk_cutletsName": "Ciber-costeletas",
    "it_total": "No armazém: {n} un.",
    "bt_entry": "🔋 Inscrição da equipe: {n} / {m}",
    "bt_entered": "✅ A equipe está na batalha pelas minas",
    "bt_give": "Contribuir com 🔋 (você tem {n})",
    "bt_info": "Só equipes inscritas disputam as minas: {f} 🔋, clã — {fc} 🔋. Juntem-se, toda a equipe!",
    "bt_notAllowed": "Esta batalha não é para o seu tipo de equipe",
    "mn_place": "🏆 prêmio pelo {p}º lugar",
    "mn_soonShort": "Início: {d}",
    "top_events": "🎯 Ações",
    "ev_empty": "Nenhuma ação no momento — volte mais tarde!",
    "ev_my": "Sua posição: {p}",
    "ev_noPlace": "Você ainda está fora da tabela — vamos lá!",
    "ev_manual": "Os vencedores serão definidos pelo organizador",
    "ev_places": "Lugares premiados: {n}",
    "ev_prizes": "🎁 Prêmios",
    "ev_leaders": "Líderes",
    "lab_sciGate": "📚 O nível {l} abre quando todas as tecnologias estiverem no nível {l}",
    "lab_cooldown": "Depois de estudar, o próximo nível abre em {d} d.",
    "lab_done": "🔬 Pronto! Nível {l}",
    "lab_eff_comm": "Nível 1 — saques e renda das minas; cada nível seguinte −{c} min na recarga do saque",
    "lab_eff_scout": "Sem ele não há saques; alvos no reconhecimento: 2 + nível",
    "lab_eff_attack": "Sem ele não há saques; cada nível após o primeiro dá +{a}% de espólio",
    "lab_eff_defense": "Cada nível −{d}% no que o invasor leva de você",
    "lab_eff_science": "+{s}% na produção da fazenda e no espólio por nível. Demora a estudar e exige ☢️ Núcleo",
    "lab_how": "📖 Como funciona",
    "lab_rule1": "Os kits são montados uma vez: ⚒️ → 🛠 → 🔬 → 🧬. Sem o kit certo, receita avançada ou nível ficam bloqueados.",
    "lab_rule2": "Depois de estudar um nível, o próximo nível da mesma tecnologia abre exatamente 30 dias depois — cada melhoria vale muito. A ciência cresce depois das outras tecnologias.",
    "lab_rule3": "☢️ Núcleo só vem do jogo em equipe: posições de prêmio nas batalhas e dias segurando uma mina.",
    "durDH": "{d} d {h} h",
    "durHM": "{h} h {m} min",
    "durM": "{m} min",
    "ws_locked": "🔒 Abre em {t}",
    "ws_toStorage": "📦 O item pronto vai para o estoque",
    "eff_camo": "você some do reconhecimento de saques, mas ainda pode atacar",
    "eff_trap": "um saqueador que falha entrega o dobro a você",
    "eff_drill": "empate na defesa conta como falha do saqueador",
    "eff_thermos": "os Perfuradores comem bifes 25% mais devagar",
    "eff_banner": "+5% de mineração para toda a sua equipe",
    "eff_dome": "escudo contra saques para toda a equipe",
    "eff_forsage": "pula a recarga do saque (uma vez por dia)",
    "eff_economizer": "a próxima decolagem sem hidrogênio",
    "eff_cargo": "butim do próximo saque ×1,5",
    "eff_stamp": "a próxima venda na bolsa sem taxa",
    "it_camo": "CAMUFLAGEM",
    "it_trap": "ISCA",
    "it_drill": "TREINO DE POSTURA",
    "it_thermos": "TÉRMICA DE BIFES",
    "it_banner": "BANDEIRA DA EQUIPE",
    "it_dome": "CÚPULA DA EQUIPE",
    "it_forsage": "PÓS-COMBUSTOR DA NAVE",
    "it_economizer": "ECONOMIZADOR",
    "it_cargo": "PORÃO AMPLIADO",
    "it_stamp": "SELO DA BOLSA",
    "it_oneShot": "único",
    "it_charges": "⚡ Carregado: {n}",
    "it_needTeam": "Item de equipe — você precisa estar em uma equipe.",
    "it_charged": "⚡ Carregado! Dispara na sua próxima ação.",
    "it_forsaged": "🔥 Recarga pulada — pode decolar!",
    "raid_armed": "⚡ Pronto: {l}",
    "raid_guardUntil": "{n} até {t}",
    "raid_domeOn": "🛡 Cúpula da equipe até {t}",
    "raid_forsageBtn": "🔥 Pós-combustor: pular recarga ({n})",
    "raid_note_economizer": "⛽ Economizador: decolagem sem hidrogênio",
    "raid_note_cargo": "📦 Porão: butim ×1,5",
    "raid_note_trap": "🪤 Isca do alvo: você entrega o dobro",
    "raid_note_drill": "🎯 Treino de postura do alvo: o empate conta como sua falha",
    "mn_title": "⛏ MAPA DAS MINAS",
    "mn_closed": "🔒 Não dá para atacar minas até começar uma batalha de equipes ou clãs.",
    "mn_pick": "Toque em uma mina para ver os detalhes.",
    "mn_info": "⛏ MINA",
    "mn_battle": "⚔️ BATALHA «{t}» PELA MINA Nº {n}",
    "mn_soon": "⏳ BATALHA «{t}» PELA MINA Nº {n} — COMEÇA {d}",
    "mn_nom": "Categoria: {n}",
    "mn_ends": "Fim: {d}",
    "mn_leaders": "Líderes agora",
    "mn_noLeaders": "Ninguém pontuou ainda — sua equipe pode ser a primeira!",
    "mn_myTeam": "🏆 SUA EQUIPE NAS MINAS",
    "mn_income": "Produção: {n} recursos por hora para toda a equipe",
    "mn_noIncome": "Ainda sem minas — vença uma batalha de equipes e a mina é sua por 72 h.",
    "mn_noTeam": "Minas só são conquistadas em equipe — entre em uma equipe ou crie a sua.",
    "mn_teamBtn": "🏆 Para a equipe",
    "mn_how": "📖 Como funciona",
    "mn_rule1": "Cada batalha de equipes e clãs é por exatamente uma mina. Vence a equipe com o melhor resultado somado de todos os combatentes na categoria da batalha.",
    "mn_rule2": "O vencedor mantém a mina por {h} h: cada membro da equipe recebe {y} do recurso da mina por hora. Mais combatentes — mais produção.",
    "mn_rule3": "Depois a mina fica livre de novo, mas só pode ser conquistada em uma nova batalha.",
    "mn_name": "⛏ MINA Nº {n}",
    "mn_res": "Recurso",
    "mn_holder": "Dono",
    "mn_free": "livre",
    "mn_untilL": "Mantida até",
    "mn_pumping": "Produz: {n} {i} por hora",
    "mn_targetOf": "⚔️ A batalha «{t}» é por esta mina",
    "mn_closedOne": "🔒 Só dá para conquistar em uma batalha de equipes — fique de olho nos anúncios.",
    "raid_noFuel": "⛽ A nave não está pronta para decolar — falta combustível",
    "raid_shieldTitle": "🛡 ESCUDO CONTRA SAQUES",
    "raid_shieldActive": "ATIVO",
    "raid_shieldInactive": "INATIVO",
    "raid_shieldHint": "Com o escudo ativo, ninguém pode te saquear. Ele é montado na oficina e vai para o estoque — ative quando precisar.",
    "raid_toStorage": "📦 Abrir o estoque",
    "sk_res": "📦 RECURSOS NO ESTOQUE",
    "sk_expand": "🔧 Ampliar o estoque",
    "sk_cutlets": "🥩 CIBER-BIFES",
    "sk_cutletsHint": "Combustível dos Ciber-Perfuradores: 1 bife = um dia de trabalho.",
    "sk_refuel": "🚜 Abastecer na fazenda",
    "it_nitrogen": "RESFRIAMENTO A NITROGÊNIO +40%",
    "it_nuclear": "BOOST NUCLEAR X5",
    "it_drone": "DRONE MESTRE",
    "it_shield": "ESCUDO CONTRA SAQUES",
    "it_unlimit": "SEM LIMITE DE JOGOS",
    "it_unlimitDesc": "vitórias nos jogos sem o limite diário",
    "it_hours": "{h} h",
    "it_use": "Ativar",
    "it_empty": "Vazio. Monte na oficina — o item virá parar aqui.",
    "it_toWorkshop": "🔧 Para a oficina",
    "it_active": "✅ Ativo até {t}",
    "it_used": "✅ Ativado! Vale até {t}",
    "it_stored": "📦 Pronto! O item está no seu estoque — ative-o na aba Estoque quando precisar.",
    "sk_shuttle": "🚀 SHUTTLE",
    "sk_shuttleOn": "Você tem: taxa da bolsa {f}%, limites de ordens maiores.",
    "sk_shuttleOff": "Ainda não. Montado na oficina.",
    "sk_armor": "🦾 CIBER-ARMADURA",
    "sk_armorOn": "Nível {l} de {m}: +{p}% de mineração até {t}.",
    "sk_armorOff": "Não equipada. Cada nível dá +{p}% de mineração por 30 dias.",
    "sk_store": "🏗 AMPLIAÇÃO DO ESTOQUE",
    "sk_storeLvl": "Capacidade: {c} de cada recurso.",
    "sk_storeMax": "🏆 Estoque no máximo!",
    "hp_who": "Podem presentear jogadores a partir do nível {l} de inteligência e com {c} ciber-bifes diários resgatados.",
    "top": "👑 TOP-100 MAIS RICOS DO ECOSSISTEMA",
    "shop": "🏪 LOJA",
    "shopFarm": "🚜 PARA A FAZENDA",
    "shopGames": "🕹️ JOGOS",
    "shopHint": "Pagamento com Telegram Stars oficiais — aqui mesmo, em um toque.",
    "paid": "🎉 Pago! O item já está na sua conta.",
    "payFail": "O pagamento não foi concluído. Tente de novo.",
    "oldClient": "Atualize o Telegram para comprar pelo app, ou abra a loja no chat do bot.",
    "ctaNoRobots": "💤 A fazenda está quase vazia! Pegue um robô mais forte — as 🪙 vão pingar 24 horas por dia.",
    "ctaHungry": "🚨 Os Perfuradores estão com fome ({n} sem combustível) — a mineração parou!",
    "ctaLowFuel": "⚠️ Os bifes não duram nem um dia de trabalho dos Perfuradores.",
    "ctaShopBtn": "🛒 Ir à loja",
    "footer": "The whole game in one app",
    "noProfile": "Perfil não encontrado. Abra o bot e toque em /start!",
    "blocked": "Conta bloqueada pela administração.",
    "deleting": "Sua conta está na fila de exclusão. Mudou de ideia? Cancele no chat do bot.",
    "error": "Não foi possível carregar os dados. Tente mais tarde.",
    "outside": "Abra este aplicativo pelo bot ROFL HUB no Telegram.",
    "robotsTitle": "🤖 SEUS ROBÔS",
    "buyMore": "🛒 Comprar",
    "rateShort": "{v} 🪙/h",
    "refuelOne": "🥩 Carregar 1",
    "refuelAll": "⚡ Carregar todos",
    "refueled": "Carregado: {n} 🥩",
    "res_metal_src": "PPT",
    "res_hydrogen_src": "Maior/Menor",
    "res_crystal_src": "Quiz",
    "res_parts_src": "Ciber-Cofre",
    "resWhere": "onde conseguir",
    "ws_title": "🔧 OFICINA",
    "ws_hint": "Os recursos dos jogos viram melhorias. Recursos suficientes? Toque em «Montar».",
    "ws_craft": "Montar",
    "ws_owned": "✅ Já tem",
    "ws_crafted": "Pronto! A melhoria já está funcionando.",
    "ws_armor": "🛡 Ciber-Armadura",
    "ws_armorLvl": "nível {l}/{m} · +{p}% por nível por 30 dias",
    "ws_shuttleOn": "🚀 Shuttle montado: taxa da bolsa {fee}%",
    "ws_shuttleOff": "🚀 Shuttle não montado: taxa da bolsa {fee}%",
    "eff_nitrogen": "+40% de mineração para todos os robôs",
    "eff_nuclear": "×5 de mineração, os Perfuradores comem ×3 bifes",
    "eff_drone": "os robôs não envelhecem",
    "eff_shield": "ninguém pode saquear você",
    "eff_cutlet": "1 ciber-bife no estoque (caro: o combustível sai mais barato na loja)",
    "eff_armor": "+10% de mineração por nível por 30 dias",
    "eff_storage": "mais espaço para recursos — para sempre",
    "eff_shuttle": "só seu: taxa de 5% nas suas vendas e ordens de até 500 bifes — para sempre",
    "tab_friends": "🤝 Amigos",
    "ref_title": "🤝 CONVIDE AMIGOS",
    "ref_rules": "{q} por cada amigo ativo — uma vez só. Amigo ativo é quem chegou ao nível de intelecto {l} e pegou {c} bifes diários.",
    "ref_copy": "📋 Copiar",
    "ref_copied": "Link copiado!",
    "ref_share": "📤 Compartilhar",
    "ref_stats": "📊 SUA REDE",
    "ref_invited": "convidados",
    "ref_qualified": "ativos",
    "ref_earned": "ganho",
    "ref_top": "🏆 QUEM TEM MAIS AMIGOS",
    "ref_topHint": "✅ — amigos ativos, 👥 — todos os convidados",
    "ref_empty": "O ranking ainda está vazio — seja o primeiro lugar!",
    "wk_title": "🔥 RECEITAS DA SEMANA",
    "wk_hint": "Receitas temporárias: aparecem quando o hub decide e depois somem. Monte a tempo!",
    "wk_left": "montagens restantes nesta semana: {n} de {m}",
    "st_cap": "📦 Estoque: até {c} de cada recurso — o excedente da mineração se perde",
    "raid_title": "🏴‍☠️ SAQUES",
    "raid_how": "📖 Como funciona",
    "raid_rule1": "Você escolhe uma jogada; o alvo já deixou uma postura de defesa definida. Quem decide é o pedra-papel-tesoura: um duelo de decisões, não uma loteria.",
    "raid_rule2": "Vitória: você leva {pct}% de cada recurso do alvo, até {cap} por recurso. Fracasso: você entrega ao alvo {fpct}% dos seus, até {fcap}. Empate: o combustível queimou.",
    "raid_rule3": "Só recursos podem ser saqueados. Moedas, robôs e bifes estão totalmente seguros. Novatos ficam protegidos por {days} dias, e colegas de equipe são intocáveis.",
    "raid_rule4": "Cada voo custa {fuel} 💧 de hidrogênio, o próximo só em {cd} h. Se alguém saquear você, a revanche é grátis por {rh} h.",
    "raid_fuel": "💧 Hidrogênio",
    "raid_ready": "🚀 Nave pronta para decolar",
    "raid_cooldown": "⏳ Recarregando: {m} min",
    "raid_shieldOn": "🛡 Escudo até {t}",
    "raid_shieldNewbie": "🛡 Proteção de novato",
    "raid_shieldOff": "🛡 Sem escudo — monte um na oficina",
    "raid_stance": "✊ SUA POSTURA DE DEFESA",
    "raid_stanceHint": "É com ela que você recebe os saques dos outros. Troque de vez em quando — quem é previsível é saqueado mais vezes.",
    "raid_stanceNone": "Nenhuma postura escolhida — será aleatória",
    "raid_stanceSaved": "Postura salva",
    "raid_stats": "Saques: {a} ({w} com sucesso) · defendidos: {h} de {d}",
    "raid_scout": "🔭 RECONHECIMENTO: achar alvos",
    "raid_targets": "🎯 Escolha um alvo",
    "raid_res": "recursos ≈{n}",
    "raid_noTargets": "Nenhum alvo disponível agora: escudos, recargas, novatos. Volte mais tarde.",
    "raid_pickMove": "✊ Sua jogada contra a postura de {name}",
    "raid_revenge": "⚔️ REVANCHE",
    "raid_revengeBtn": "⚔️ Revidar: {name}",
    "raid_win": "🏴‍☠️ Saque bem-sucedido!",
    "raid_draw": "😐 Empate — a nave voltou vazia",
    "raid_lose": "💥 A defesa segurou",
    "raid_vs": "{m} contra {s}",
    "raid_loot": "Espólio: {l}",
    "raid_lost": "Entregue ao alvo: {l}",
    "rock": "🪨 Pedra",
    "scissors": "✂️ Tesoura",
    "paper": "📄 Papel",
    "mk_title": "📈 BOLSA",
    "mk_stats": "Ordens: {o} · bifes: {c} · melhor preço: {b} 🪙",
    "mk_feeLine": "A taxa de {f}% por venda é queimada — proteção contra a inflação",
    "mk_inv": "🥩 No seu estoque: {n}",
    "mk_offers": "🛒 OFERTAS",
    "mk_empty": "Ainda não há ofertas — anuncie antes de todo mundo!",
    "mk_offer": "{q} 🥩 × {p} 🪙",
    "mk_buyHow": "Quantos comprar?",
    "mk_all": "Todos os {q}",
    "mk_sellTitle": "💰 VENDER BIFES",
    "mk_qty": "Quantos bifes",
    "mk_price": "Preço por unidade, 🪙",
    "mk_preview": "Negócio {t} 🪙 · você recebe {g} 🪙 · queimam {f} 🪙",
    "mk_sell": "Anunciar na bolsa",
    "mk_limits": "Até {q} bifes por ordem, até {o} ordens abertas",
    "mk_my": "📋 MINHAS ORDENS",
    "mk_cancel": "Retirar",
    "mk_bought": "Comprou {q} 🥩 por {t} 🪙",
    "mk_listed": "Ordem anunciada! Mando uma mensagem quando vender.",
    "mk_cancelledMsg": "Ordem retirada, os bifes voltaram para o estoque",
    "as_cutlet": "Bifes",
    "as_metal": "Metal",
    "as_hydrogen": "Hidrogênio",
    "as_crystal": "Cristais",
    "as_parts": "Peças",
    "mk_index": "📈 ÍNDICE DA BOLSA",
    "mk_chart": "📊 PREÇO EM 7 DIAS",
    "mk_noTrades": "Ainda não houve negócios — seja a primeira pessoa!",
    "mk_avg": "Preço médio da semana: {p} 🪙 · vendidos: {v}",
    "mk_asks": "🛒 VENDENDO",
    "mk_bids": "🙋 COMPRANDO",
    "mk_noBids": "Ainda não há ordens de compra",
    "mk_sellTo": "Vender",
    "mk_sellHow": "Quantos vender?",
    "mk_bidTitle": "🙋 ORDEM DE COMPRA",
    "mk_bidHint": "As moedas ficam congeladas na ordem até o negócio. Retirou a ordem — as moedas voltam.",
    "mk_bid": "Criar ordem de compra",
    "mk_bidPreview": "Serão congeladas {t} 🪙",
    "mk_have": "Você tem: {n}",
    "mk_floor": "Um bife não sai por menos de {p} 🪙: o combustível da loja por Estrelas é sempre mais vantajoso",
    "mk_side_sell": "vendo",
    "mk_side_buy": "compro",
    "mk_listedBid": "Ordem de compra criada! As moedas ficam congeladas até o negócio.",
    "mk_sold": "Vendidos {q}, recebidas {g} 🪙 após a taxa",
    "mk_shuttleNote": "🚀 Seu Shuttle: taxa de {f}% nas suas vendas",
    "sw_title": "🔄 TROCA DE RECURSOS",
    "sw_hint": "Dê o que sobra — receba o que falta. Sem moedas e sem taxa.",
    "sw_give": "Você dá",
    "sw_want": "Você quer receber",
    "sw_qty": "Quantos",
    "sw_create": "Propor troca",
    "sw_take": "Trocar",
    "shop_info": "ℹ️ O que cada item dá",
    "sw_youGet": "Você recebe",
    "sw_youGive": "Em troca, você dá",
    "sw_takeBtn": "Trocar — dar {x}",
    "sw_mineLine": "Você dá {g} → quer receber {w}",
    "sw_qtyErr": "Informe uma quantidade maior que zero nos dois campos",
    "sw_empty": "Ainda não há propostas de troca",
    "sw_mine": "Minhas propostas",
    "sw_done": "Troca concluída!",
    "sw_created": "Proposta publicada, recursos reservados",
    "sw_cancelled": "Proposta retirada, os recursos voltaram",
    "ws_armorUntil": "🛡 Armadura ativa até {t}",
    "st_title": "🛰 ESTAÇÃO DA EQUIPE",
    "st_level": "Nível {l} de {m}",
    "st_bonus": "+{p}% de mineração para cada membro",
    "st_next": "O nível {n} pede {c} de cada recurso",
    "st_max": "🏁 A estação está completa!",
    "st_feed": "🧾 Últimas contribuições",
    "st_feedEmpty": "Ninguém contribuiu ainda — seja a primeira pessoa",
    "st_donate": "Contribuir",
    "st_all": "Tudo",
    "st_done": "Contribuído!",
    "st_hint": "A equipe toda constrói, cada um ganha o bônus. Saiu da equipe — perdeu o bônus.",
    "st_off": "A estação está temporariamente em manutenção",
    "goals_title": "🎯 METAS DE HOJE",
    "goals_chest": "🎁 Baú pelas três: +{c} 🪙 e +{r} de um recurso aleatório",
    "goals_streak": "🔥 Sequência: {s} dias · a cada {e}º dia seguido +{b} 🪙",
    "goals_claim": "🎁 PEGAR O BAÚ",
    "goals_claimed": "🎁 O baú de hoje já foi aberto. Amanhã tem novas metas!",
    "goals_reset": "As metas renovam às 00:00 UTC",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · sequência de {s} dias",
    "featureOff": "⚙️ Seção em manutenção",
    "done": "Pronto!",
    "loading": "⏳ Carregando…",
}

COMMANDS = {
    "app": "🎮 Abrir o Mini App",
    "menu": "📱 Menu principal",
    "profile": "👤 Meu perfil e passaporte",
    "farm": "🚜 Ciber-fazenda e abastecimento",
    "shop": "🏪 Loja (Telegram Stars)",
    "games": "🕹️ Todos os jogos contra o bot",
    "quiz": "🧠 Quiz: 15 segundos por resposta",
    "duel": "⚔️ Duelo 1x1 valendo aposta",
    "quests": "🗺️ Missões: histórias com escolhas",
    "my_team": "🏆 Minha equipe e colegas",
    "invite": "🤝 Link de indicação: +500 por amigo ativo",
    "transfer": "🔄 Enviar moedas a um jogador",
    "market": "📈 Bolsa de bifes: comprar ou vender",
    "sell": "💰 Vender bifes: /sell quantidade preço",
    "my_stats": "📊 Minhas estatísticas",
    "faq": "📚 Perguntas frequentes",
    "rules": "📜 Termos de uso",
    "paysupport": "🛟 Suporte de pagamentos",
    "workshop": "🔧 Oficina: recursos viram melhorias",
    "raid": "🏴‍☠️ Saques: reconhecimento e revanche",
    "goals": "🎯 Metas diárias e baú",
    "station": "🛰 Estação da equipe: projeto em comum",
}
