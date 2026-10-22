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
        "💸 Você recebeu: <b>{balance} moedas</b>\n"
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
        "- O canal de diversão e conhecimento ROFL HUB CHANNEL\n"
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
        "..................................................\n\n"
        "👤 <b>PERFIL PESSOAL E PASSAPORTE:</b>\n"
        "• /start — Começar a apresentação e registrar a conta\n"
        "• /profile — Seu passaporte, saldo e equipe em tempo real\n"
        "• /my_stats — Seu histórico de estatísticas dos últimos 30 dias\n\n"
        "🚜 <b>CIBER-FAZENDA E AUTOMAÇÃO:</b>\n"
        "• /farm — Hub de combustível: abastecimento e velocidade de produção dos robôs\n"
        "• /shop — Marketplace: compra de mineradores, bifes e melhorias do hub\n\n"
        "🕹️ <b>SALA DE JOGOS:</b>\n"
        "• /games — Hub inline de todos os jogos contra o bot\n"
        "• /quiz — Quiz de velocidade: 15 segundos por resposta, níveis e bônus\n"
        "• /duel — DUELOS 1x1 com jogadores reais: mesas 10/100/1000\n"
        "• /quests — MISSÕES: histórias de detetive, comédias e enigmas com recompensas\n"
        "• /rps, /high_low, /safe — Jogos rápidos valendo moedas\n\n"
        "👥 <b>GESTÃO DA TROPA:</b>\n"
        "• /create_team — Registrar sua equipe por 100.000 moedas\n"
        "• /my_team — Painel da tropa e LISTA DE MEMBROS com níveis 🧠\n"
        "• /all_teams — Roleta de equipes aleatórias\n\n"
        "💸 <b>DINHEIRO E AMIGOS:</b>\n"
        "• /invite — Seu link de indicação: +1000 moedas por amigo\n"
        "• /transfer — Enviar moedas a outro jogador\n\n"
        "📚 <b>GUIA E REGRAS:</b>\n"
        "• /faq — Guia completo do ecossistema (abre no Mini App)\n"
        "• /rules — Termos de uso\n"
        "..................................................\n"
        "<i>⚙️ Use o painel de jogo fixo de duas colunas na parte de baixo da tela para navegar na hora!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>BOAS-VINDAS À ZONA DE JOGOS DO ROFL HUB!</b>\n"
        "..................................................\n\n"
        "Aqui você pode enfrentar o bot em duelos rápidos ou encarar o "
        "teste relâmpago de inteligência para faturar alto — ou zerar o saldo!\n\n"
        "💸 Vitória paga: <b>+2 moedas</b> (Ciber-Cofre: <b>+5</b>)\n"
        "💀 Derrota ou empate desconta: <b>-1 moeda</b>\n"
        "🧠 No Quiz há um cronômetro de 15 segundos e níveis de inteligência: o nível 1 pede 10 respostas certas e paga <b>+100 moedas</b>, "
        "cada nível seguinte é 10 respostas mais longo — mas a recompensa cresce em 100!\n\n"
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
        "..................................................\n\n"
        "O resumo do que importa:\n"
        "🚜 Os robôs mineram moedas 24 horas por dia: Robô Minerador — 5/h sem combustível, "
        "Ciber-Perfurador — 10/h, e CADA Perfurador come o próprio ciber-bife por dia. "
        "Todos os robôs duram 30 dias (o Drone Mestre pausa o desgaste).\n"
        "🧠 Quiz: 15 segundos por resposta, níveis de inteligência com recompensas crescentes.\n"
        "⚔️ Duelos contra jogadores reais em mesas de 10/100/1000 moedas.\n"
        "🏆 Equipes de até 50 guerreiros (Mega-Clã — até 1000) e eventos de Batalha com prêmios para todos.\n\n"
        "..................................................\n"
        "👇 <b>O guia completo com todas as mecânicas — a um toque:</b>"
    ),
    "faq.btn_open": "📖 ABRIR O GUIA COMPLETO",
    "rules.teaser": (
        "📜 <b>TERMOS DE USO DO ROFL HUB</b>\n"
        "..................................................\n\n"
        "O essencial em poucas palavras:\n"
        "🪙 Moedas e todos os itens do jogo são elementos virtuais de entretenimento: "
        "não são dinheiro e não podem ser trocados por valores reais.\n"
        "💫 Compras somente via Telegram Stars oficiais; itens digitais são entregues "
        "na hora e, se a entrega falhar, as Stars são devolvidas automaticamente.\n"
        "🛡️ Não coletamos telefones, localização nem dados pessoais.\n"
        "🤝 Ofensas, esquemas de trapaça e multicontas são proibidos — violações podem levar a bloqueio.\n\n"
        "..................................................\n"
        "👇 <b>O texto completo dos termos e o aviso de isenção — a um toque:</b>\n"
        "<i>⚖️ Ao usar o bot, você confirma que aceita as condições.</i>"
    ),
    "rules.btn_open": "📜 ABRIR OS TERMOS COMPLETOS",
    "quest.list_header": (
        "🗺️ <b>MISSÕES DO ROFL HUB</b>\n"
        "..................................................\n\n"
        "Histórias interativas com escolhas e caminhos diferentes: detetives, comédias, enigmas. "
        "A primeira vitória em cada missão paga moedas, e você pode rejogar quantas vezes quiser!\n"
        "🌐 <i>Por enquanto as histórias das missões estão em russo — novos idiomas chegam em breve.</i>\n\n"
        "👇 <b>Escolha uma história:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} moedas pela primeira vitória\n"
        "..................................................\n\n"
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
    "quest.win_first": "\n\n🏆 <b>MISSÃO CONCLUÍDA! Recompensa: +{coins} moedas.</b>",
    "quest.win_repeat": "\n\n✅ <b>Concluída de novo!</b> A recompensa desta missão já foi recebida antes.",
    "quest.fail_footer": "\n\n💀 <i>Não foi o melhor dos finais... mas a história sempre pode ser rejogada!</i>",
    "quest.stale": "⏳ Essa cena já ficou para trás — seguindo do ponto atual!",
    "quest.no_coins": "❌ Moedas insuficientes para a dica ({cost}). Dê um pulo na fazenda!",
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
    "farm.status_no_drills": "💡 Compre Ciber-Perfuradores no /shop para aumentar sua renda.",
    "farm.boost_nuclear": "🔋 Boost Nuclear x5 até {until} UTC (consumo de bifes ×3)",
    "farm.boost_nitrogen": "❄️ Resfriamento a Nitrogênio +40% até {until} UTC",
    "farm.boost_drone": "🛸 O Drone Mestre prolonga a vida dos robôs até {until} UTC",
    "farm.no_boosts": "Nenhum boost ativo — dê uma olhada no /shop.",
    "farm.burnout": "🔥 Próxima queima de robô: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Ativar seu Robô Estagiário (grátis)",
    "farm.intern_activated": "🤖 Seu Robô Estagiário entrou no turno! +1 moeda por hora para sempre, sem combustível e sem validade.",
    "farm.intern_already": "🤖 Seu Robô Estagiário já está trabalhando.",
    "farm.intern_line": "🤖 Robôs Estagiários ({rate} moeda/h, eternos): <code>{count}</code>",
    "farm.intern_hint": "🎁 Você tem um Robô Estagiário grátis! Toque no botão abaixo e ele vai minerar 1 moeda por hora para sempre.",
    "farm.dashboard": (
        "🚜 <b>HUB CENTRAL DE COMBUSTÍVEL DO ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Robôs ativos na usina: <b>{total}</b>\n"
        "• Robôs Mineradores ({junior_rate} moedas/h): <code>{junior}</code>\n"
        "• Ciber-Perfuradores ({premium_rate} moedas/h): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VELOCIDADE ATUAL DA SUA FAZENDA:</b>\n"
        "• Produção por hora: <b>+{speed_hour} moedas</b>\n"
        "• Produção por dia: <b>+{speed_day} moedas</b>\n\n"
        "⚡ <b>BOOSTS:</b>\n{boosts}\n\n"
        "📋 <b>STATUS DA USINA DO JOGO:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>ESTADO DA GELADEIRA AUTOMÁTICA:</b>\n"
        "🥩 Reserva de combustível: <b>{fridge} / {capacity}</b>\n"
        "💼 Bifes no estoque do inventário: <code>{inv}</code>\n\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
        "🆔 Seu ID de Passaporte: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Moedas agora: <b>{balance} moedas</b>\n"
        "🏆 Seu status: <b>{team}</b>\n"
        "🧠 Nível de inteligência: <b>{level}</b> · até o nível {next_level}: "
        "<b>{left}</b> respostas certas no /quiz (recompensa: +{reward} moedas)\n\n"
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
        "..................................................\n\n"
        "🧠 Nível de inteligência no jogo: <b>{level}</b> (total de respostas certas: {total})\n"
        "🎮 Rodadas de duelo jogadas: <b>{played}</b>\n"
        "🏆 Vitórias conquistadas: <code>{won}</code>\n"
        "👥 Amigos ativos convidados: <b>{refs}</b>\n\n"
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
    "games.win": "🎉 <b>VITÓRIA!</b> 🎉\nMoedas creditadas: <b>+{reward}</b>",
    "games.lose": "💀 <b>DERROTA!</b>\nMoedas descontadas: <b>-{penalty}</b>",
    "games.draw": "🤝 <b>EMPATE!</b>\nMoedas descontadas: <b>-{penalty}</b>",
    "games.limit": (
        "🛑 <b>Limite diário atingido!</b>\n\n"
        "Você já pegou {limit} vitórias em {game} hoje. O limite renova às 00:00 UTC.\n\n"
        "⚡ Remover o limite por 24 horas — 5 ★, por 30 dias — 99 ★ (seção “Jogos” no /shop)."
    ),
    "games.no_coins": "❌ Você tem 0 moedas — nada para pagar a taxa da rodada. Colete a renda da fazenda no /farm!",
    "games.balance": "💰 Saldo: <b>{balance} moedas</b>",
    "games.btn_retry": "🎮 Jogar de novo!",
    "games.btn_hub": "🕹️ Zona de jogos",
    "games.level_up": (
        "🏅 <b>NÍVEL DE INTELIGÊNCIA AUMENTOU: {level}!</b> Recompensa: <b>+{bonus} moedas</b>!\n"
        "Próximo nível: {next_required} respostas certas → +{next_reward} moedas."
    ),
    "games.name.rps": "Pedra-Papel-Tesoura",
    "games.intern_bonus": "🤖 Nível {level}! Mais um Robô Estagiário chegou à sua fazenda: agora são {count}.",
    "games.name.hl": "Maior/Menor",
    "games.name.quiz": "Quiz",
    "games.name.safe": "Cofre",

    # ---------------- PPT ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>PEDRA-PAPEL-TESOURA</b>\n\n"
        "Vitória: <b>+{reward}</b> · Derrota/empate: <b>-{penalty}</b>\n"
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
        "<i>🌐 Por enquanto as perguntas estão em russo — o pacote em português chega em breve!</i>"
    ),
    "quiz.btn_new": "🧠 Nova pergunta",
    "quiz.timeout": "⌛ <b>TEMPO ESGOTADO!</b> ⌛\nResposta certa: <b>{correct}</b>",
    "quiz.stale": "⏳ Esta pergunta não está mais ativa. Comece uma nova!",
    "quiz.stale_alert": "Esta pergunta não está mais ativa. Comece uma nova!",
    "quiz.empty": "⚠️ O banco de perguntas está vazio. Avise o administrador.",
    "quiz.wrong": "❌ <b>Errou</b> ❌\nResposta certa: <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} moeda</b> pela derrota!",
    "quiz.level_line": (
        "🧠 Nível de inteligência: <b>{level}</b>\n"
        "Vitórias restantes até o nível {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>{seconds} segundos para responder!\n"
        "Certa: +{win} moedas no saldo\n"
        "Errou / não deu tempo: -{penalty} moeda\n"
        "Limite: {limit} vitórias por dia</i>"
    ),



    # ---------------- Cofre ----------------
    "safe.intro": (
        "🔐 <b>CIBER-COFRE</b>\n\n"
        "Lá dentro tem um prêmio de <b>{jackpot} moedas</b>! A porta está trancada com um código de 1 a {codes}. "
        "Você tem só uma tentativa.\n"
        "Abriu: <b>+{jackpot}</b> · Alarme: <b>-{penalty}</b> · Limite: <b>{limit}</b> vitórias"
    ),
    "safe.btn_retry": "🔐 Arrombar de novo!",
    "safe.win": "🔓 <b>Cofre aberto!</b> O código era: <b>{code}</b>.",
    "safe.lose": "🚨 <b>O alarme disparou!</b> Você digitou {guess}, e o código era: <b>{code}</b>.",

    # ---------------- duelos ----------------
    "duel.intro": (
        "⚔️ <b>DUELOS 1x1: PEDRA-PAPEL-TESOURA VALENDO APOSTA</b>\n"
        "..................................................\n\n"
        "Escolha a mesa que cabe no seu bolso — igual no pôquer. A aposta é descontada na hora, "
        "e o adversário é um jogador real do ROFL HUB!\n\n"
        "💰 O pote = as duas apostas. O vencedor leva <b>{payout_percent}%</b> do pote, "
        "<b>{burn_percent}%</b> queima para sempre (deflação!).\n"
        "🤝 Empate — nova rodada na hora, com o pote na mesa.\n"
        "⏱ São <b>{move_timeout} segundos</b> por jogada; quem ficar calado tem a jogada sorteada automaticamente.\n"
        "🏆 Vitórias em duelos contam para a sua equipe nas Batalhas!\n\n"
        "👇 <b>ESCOLHA UMA MESA:</b>"
    ),
    "duel.btn_table": "⚔️ Mesa de {stake} moedas",
    "duel.btn_cancel": "❌ Sair da mesa (devolver a aposta)",
    "duel.btn_move_rock": "🪨 Pedra",
    "duel.btn_move_scissors": "✂️ Tesoura",
    "duel.btn_move_paper": "🧻 Papel",
    "duel.waiting": (
        "🪑 <b>Você está na mesa de {stake} moedas.</b> Sua aposta está no pote.\n"
        "Esperando o segundo guerreiro... Assim que ele sentar, vocês dois escolhem a jogada!\n"
        "<i>A fila dura {ttl} minutos; depois a aposta volta automaticamente.</i>"
    ),
    "duel.cancelled": "🚪 Você saiu da mesa. A aposta de <b>{stake} moedas</b> voltou para o seu saldo.",
    "duel.expired": "⌛ Nenhum adversário apareceu na mesa de {stake}. A aposta de <b>{stake} moedas</b> foi devolvida.",
    "duel.matched": (
        "⚔️ <b>ADVERSÁRIO ENCONTRADO! Mesa de {stake} moedas.</b>\n"
        "Pote: <b>{bank} moedas</b> · O vencedor leva: <b>{payout}</b>\n\n"
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
        "💰 Prêmio: <b>+{payout} moedas</b> · 🔥 Queimado do pote: {burned}\n"
        "💼 Saldo: <b>{balance} moedas</b>"
    ),
    "duel.lose": (
        "💀 <b>DUELO PERDIDO.</b>\n\n"
        "A jogada {winner_move} do adversário vence a sua {loser_move}.\n"
        "📉 A aposta de <b>{stake} moedas</b> foi para o pote do vencedor.\n"
        "Revanche?"
    ),
    "duel.reaper_prefix": "⏰ <b>Tempo da rodada esgotado!</b> As jogadas que faltavam foram sorteadas automaticamente.\n\n",
    "duel.bad_table": "❌ Essa mesa não existe.",
    "duel.already_in": "⚠️ Você já está em uma mesa ou em combate! Termine o duelo atual primeiro.",
    "duel.no_coins": "❌ Para esta mesa você precisa de {stake} moedas no saldo.",
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
    "rank.dead": "DEAD",

    # ---------------- indicações ----------------
    "ref.text": (
        "🤝 <b>PROGRAMA DE INDICAÇÃO DO ROFL HUB</b>\n"
        "..................................................\n\n"
        "Convide amigos e ganhe <b>+{bonus} moedas</b> por cada um "
        "que se registrar pelo seu link pessoal!\n\n"
        "🔗 <b>Seu link (toque para copiar):</b>\n<code>{link}</code>\n\n"
        "📊 <b>SUAS ESTATÍSTICAS:</b>\n"
        "👥 Amigos convidados: <b>{invited}</b>\n"
        "💰 Ganho com indicações: <b>{earned} moedas</b>\n\n"
        "..................................................\n"
        "<i>Mande o link nos grupos da escola, para os amigos e nas redes — quanto maior a tropa, mais rápido o saldo cresce!</i>"
    ),
    "ref.btn_share": "📣 Compartilhar o link",
    "ref.share_text": "Entra no ecossistema de jogos ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Recompensa em dobro:</b> quando um amigo convidado jogar "
                           "{rounds} rodadas, você ganha mais <b>+{bonus} moedas</b>!"),
    "ref.qualified_notify": ("🤝 <b>Seu amigo pegou o gosto: já são {rounds} rodadas!</b>\n"
                             "Você ganhou <b>+{bonus} moedas</b> por um indicado qualificado. "
                             "Convide mais!"),

    # ---------------- transferências ----------------
    "tr.help": (
        "🔄 <b>TRANSFERÊNCIA DE MOEDAS PARA OUTRO JOGADOR</b>\n"
        "..................................................\n\n"
        "Formato do comando:\n"
        "<code>/transfer ID quantia</code> — pelo ID de Passaporte (aparece no /profile)\n"
        "<code>/transfer @username quantia</code> — pelo nome de usuário\n"
        "<code>/transfer ROFL-HUB-777 quantia</code> — por um VIP ID de leilão\n\n"
        "Exemplos:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Quantia mínima: <b>{min} moedas</b>"
    ),
    "tr.not_found": "❌ Destinatário não encontrado. Confira o ID de Passaporte ou o @username — o jogador precisa estar registrado no bot.",
    "tr.self": "🤨 Não dá para transferir moedas para você mesmo — isso seria uma economia infinita!",
    "tr.blocked": "🚫 Este jogador está bloqueado — transferências para ele estão indisponíveis.",
    "tr.min": "❌ A transferência mínima é de {min} moedas.",
    "tr.insufficient": "❌ Moedas insuficientes! Seu saldo: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Moedas insuficientes no saldo.",
    "tr.confirm": (
        "🔄 <b>CONFIRME A TRANSFERÊNCIA:</b>\n\n"
        "👤 Destinatário: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Quantia a debitar: <b>{amount} moedas</b>{fee_line}\n"
        "💰 O destinatário recebe: <b>{received} moedas</b>\n\n"
        "<i>Transferências não podem ser desfeitas — confira o destinatário!</i>"
    ),
    "tr.fee_line": "\n🔥 Taxa do hub: <b>{fee} moedas</b> (queimada)",
    "tr.btn_confirm": "✅ CONFIRMAR TRANSFERÊNCIA",
    "tr.btn_cancel": "❌ Cancelar",
    "tr.cancelled_toast": "Transferência cancelada",
    "tr.cancelled": "❌ <b>Transferência cancelada.</b> As moedas ficaram no lugar.",
    "tr.not_yours": "🔒 Esta transferência não é sua!",
    "tr.done_toast": "✅ Transferência concluída!",
    "tr.done": (
        "✅ <b>TRANSFERÊNCIA CONCLUÍDA!</b>\n\n"
        "💸 Enviado: <b>{amount} moedas</b> para o jogador ID <code>{recipient_id}</code>\n"
        "💰 Seu saldo: <b>{balance} moedas</b>"
    ),
    "tr.received": (
        "💰 <b>Você recebeu {amount} moedas!</b>\n"
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
        "..................................................\n\n"
        "Todos os itens do ROFL HUB são digitais e entregues na hora após o pagamento.\n\n"
        "⚙️ <b>Se você pagou e o item não chegou:</b>\n"
        "o bot devolve as Stars automaticamente quando a entrega falha. Se isso não aconteceu — "
        "envie aqui o número do pagamento (está no recibo, formato <code>xxxx...</code>) e descreva o problema. "
        "A administração vai conferir o pagamento no banco de dados e resolver em até 24 horas.\n\n"
        "💫 <b>Política de reembolso:</b>\n"
        "o reembolso é possível se o item não foi recebido ou foi entregue com erro. "
        "Itens digitais entregues corretamente não são reembolsáveis.\n\n"
        "..................................................\n"
        "<i>Esta seção é o ponto oficial de suporte a compras conforme as regras do Telegram.</i>"
    ),

    # ---------------- entrega ----------------
    "dlv.cutlets": "🥩 Adicionado ao estoque: <b>{qty} bifes</b>.",
    "dlv.miner": "🤖 O robô <b>“{name}”</b> foi entregue na sua fazenda.\n⏳ Vida útil: até <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robô Minerador",
    "dlv.miner_premium": "Ciber-Perfurador",
    "dlv.fridge": "📦 Geladeira ampliada para <b>{capacity} bifes</b>.",
    "dlv.coins": "💰 Creditado <b>+{amount} moedas</b>.",
    "dlv.boost_nuclear": "🔋 Boost Nuclear x5 ativo até <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Resfriamento a Nitrogênio +40% ativo até <b>{until} UTC</b>.",
    "dlv.drone": "🛸 O Drone Mestre protege a fazenda até <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limites de vitórias removidos até <b>{until} UTC</b>.",
    "dlv.clan": "🏆 A equipe recebeu o status de <b>MEGA-CLÃ</b>: até {max} vagas.",
    "dlv.err_fridge": "Você já tem uma geladeira desse tamanho ou maior.",
    "dlv.err_no_team": "Você ainda não criou uma equipe. Crie primeiro com /create_team.",
    "dlv.err_mega": "Sua equipe já tem o status de Mega-Clã.",
    "dlv.intern_upgrade": "♾ Seu Robô Estagiário foi promovido a <b>Robô Minerador ETERNO</b>: 5 moedas por hora, sem validade!",
    "dlv.err_no_intern": "Nenhum Robô Estagiário ativado: ative-o primeiro em /farm.",
    "dlv.err_intern_refs": "O upgrade exige {need} amigos qualificados (30 rodadas cada); você tem {have}.",

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
        "..................................................\n\n"
        "📌 Nome: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Capitão da tropa: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Lema: <i>“{motto}”</i>\n"
        "🔮 Símbolo do emblema: {symbol}\n\n"
        "👥 Membros: <b>{members} / {max_members}</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVEGAÇÃO:</b>"
    ),
    "clan.members_only": "🔒 A lista de membros só é visível para quem faz parte desta equipe!",
    "clan.members_gone": "❌ Esta equipe já foi dissolvida.",
    "clan.members_header": (
        "👥 <b>ELENCO DA EQUIPE “{name}”</b>\n"
        "🧠 — nível de inteligência no jogo (só evolui no /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
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
    "subtitle": "seu império de jogos em uma única tela",
    "passport": "📋 PASSAPORTE DO JOGADOR",
    "coins": "moedas",
    "brain": "🧠 Nível de inteligência",
    "toNext": "até o nível {n}: {left} respostas certas no quiz (+{reward} moedas)",
    "farm": "🚜 CIBER-FAZENDA",
    "robots": "Robôs (mineradores / perfuradores)",
    "fueled": "Perfuradores abastecidos",
    "speed": "Velocidade de mineração",
    "perHour": "{v} moedas/hora",
    "fridge": "Geladeira",
    "inv": "Bifes no estoque",
    "burnout": "Próxima queima",
    "intern": "Robôs Estagiários (1 moeda/h, eternos)",
    "activateIntern": "🚀 ATIVAR ROBÔ ESTAGIÁRIO",
    "internDone": "🤖 Seu Robô Estagiário entrou no turno!",
    "rank": "🎖 Patente",
    "openFarm": "🏭 ABRIR A FAZENDA",
    "farmScene": "🏭 SUA FAZENDA",
    "back": "← Voltar",
    "minedVisit": "minerado nesta visita",
    "unit_intern": "Robô Estagiário",
    "unit_junior": "Robô Minerador",
    "unit_premium": "Cyber-Perfurador",
    "eternal": "eterno",
    "fueledAll": "abastecidos",
    "fueledPart": "{a} de {b} abastecidos",
    "license": "licença de 30 dias",
    "emptyFarm": "A mina está vazia. Ative seu Robô Estagiário ou compre robôs na loja!",
    "madeBy": "Quer um bot assim para o seu projeto? Fale com @mister_telebot",
    "boosts": "Boosts ativos",
    "none": "nenhum",
    "bonusReady": "🎁 PEGAR O BIFE DIÁRIO",
    "bonusWait": "⏳ Bônus em {h} h {m} min",
    "bonusDone": "🎉 Bife no estoque!",
    "team": "🏆 MINHA EQUIPE",
    "clan": "CLÃ",
    "teamLabel": "Equipe",
    "captain": "👑 Você está no comando!",
    "members": "Elenco",
    "noTeam": "Você ainda está sem equipe — monte sua tropa no chat do bot!",
    "top": "👑 TOP-100 MAIS RICOS DO ECOSSISTEMA",
    "shop": "🏪 LOJA",
    "shopFarm": "🚜 PARA A FAZENDA",
    "shopGames": "🕹️ JOGOS",
    "shopHint": "Pagamento com Telegram Stars oficiais — aqui mesmo, em um toque.",
    "paid": "🎉 Pago! O item já está na sua conta.",
    "payFail": "O pagamento não foi concluído. Tente de novo.",
    "oldClient": "Atualize o Telegram para comprar pelo Mini App, ou abra a loja no chat do bot.",
    "ctaNoRobots": "💤 A fazenda está vazia! Compre seu primeiro robô — as moedas vão pingar 24 horas por dia.",
    "ctaHungry": "🚨 Os Perfuradores estão com fome ({n} sem combustível) — a mineração parou!",
    "ctaLowFuel": "⚠️ Os bifes não duram nem um dia de trabalho dos Perfuradores.",
    "ctaShopBtn": "🛒 Ir à loja",
    "footer": "Controle total — no chat do bot: /menu",
    "noProfile": "Perfil não encontrado. Abra o bot e toque em /start!",
    "blocked": "Conta bloqueada pela administração.",
    "error": "Não foi possível carregar os dados. Tente mais tarde.",
    "outside": "Abra este aplicativo pelo bot ROFL HUB no Telegram.",
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
    "invite": "🤝 Link de indicação: +1000 por amigo",
    "transfer": "🔄 Enviar moedas a um jogador",
    "my_stats": "📊 Minhas estatísticas",
    "faq": "📚 Perguntas frequentes",
    "rules": "📜 Termos de uso",
    "paysupport": "🛟 Suporte de pagamentos",
}
