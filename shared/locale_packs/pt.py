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
        "• /create_team — Registrar sua equipe por 100.000 🪙\n"
        "• /my_team — Painel da tropa e LISTA DE MEMBROS com níveis 🧠\n"
        "• /all_teams — Roleta de equipes aleatórias\n\n"
        "💸 <b>DINHEIRO E AMIGOS:</b>\n"
        "• /invite — Seu link de indicação: +1000 🪙 por amigo\n"
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
        "💸 Vitória paga: <b>+2 🪙</b> (Ciber-Cofre: <b>+5</b>)\n"
        "💀 Derrota ou empate desconta: <b>-1 🪙</b>\n"
        "🧠 No Quiz há um cronômetro de 15 segundos e níveis de inteligência: o nível 1 pede 10 respostas certas e paga <b>+100 🪙</b>, "
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
        "⚔️ Duelos contra jogadores reais em mesas de 10/100/1000 🪙.\n"
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
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} 🪙 pela primeira vitória\n"
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
    "farm.intern_line": "• Robôs Estagiários ({rate} 🪙/h, eternos): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 Você tem um Robô Estagiário grátis! Toque no botão abaixo e ele vai minerar 1 🪙 por hora para sempre.",
    "farm.dashboard": (
        "🚜 <b>HUB CENTRAL DE COMBUSTÍVEL DO ROFL HUB</b>\n"
        "..................................................\n\n"
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
        "💰 Moedas agora: <b>{balance} 🪙</b>\n"
        "🏆 Seu status: <b>{team}</b>\n"
        "🧠 Nível de inteligência: <b>{level}</b> · até o nível {next_level}: "
        "<b>{left}</b> respostas certas no /quiz (recompensa: +{reward} 🪙)\n\n"
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
    "games.win": "🎉 <b>VITÓRIA!</b> 🎉\nCreditado: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>DERROTA!</b>\nDescontado: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>EMPATE!</b>\nDescontado: <b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>Limite diário atingido!</b>\n\n"
        "Você já pegou {limit} vitórias em {game} hoje. O limite renova às 00:00 UTC.\n\n"
        "⚡ Remover o limite por 24 horas — 5 ★, por 30 dias — 99 ★ (seção “Jogos” no /shop)."
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
    "rank.dead": "DEAD",

    # ---------------- indicações ----------------
    "ref.text": (
        "🤝 <b>PROGRAMA DE INDICAÇÃO DO ROFL HUB</b>\n"
        "..................................................\n\n"
        "Convide amigos e ganhe <b>+{bonus} 🪙</b> por cada um "
        "que se registrar pelo seu link pessoal!\n\n"
        "🔗 <b>Seu link (toque para copiar):</b>\n<code>{link}</code>\n\n"
        "📊 <b>SUAS ESTATÍSTICAS:</b>\n"
        "👥 Amigos convidados: <b>{invited}</b>\n"
        "💰 Ganho com indicações: <b>{earned} 🪙</b>\n\n"
        "..................................................\n"
        "<i>Mande o link nos grupos da escola, para os amigos e nas redes — quanto maior a tropa, mais rápido o saldo cresce!</i>"
    ),
    "ref.btn_share": "📣 Compartilhar o link",
    "ref.share_text": "Entra no ecossistema de jogos ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Recompensa em dobro:</b> quando um amigo convidado jogar "
                           "{rounds} rodadas, você ganha mais <b>+{bonus} 🪙</b>!"),
    "ref.qualified_notify": ("🤝 <b>Seu amigo pegou o gosto: já são {rounds} rodadas!</b>\n"
                             "Você ganhou <b>+{bonus} 🪙</b> por um indicado qualificado. "
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
    "dlv.err_intern_refs": "O upgrade exige {need} amigos qualificados (30 rodadas cada); você tem {have}.",
    "mk.header": "📈 <b>BOLSA DE COSTELETAS</b>\n..................................................\n\nOrdens abertas: <b>{orders}</b> · costeletas à venda: <b>{cutlets}</b> · melhor preço: <b>{best}</b>\nTaxa do hub: <b>{fee}%</b> por venda (queimada — escudo contra inflação)\n🥩 No seu estoque: <b>{inv}</b> costeletas\n\n{body}\n\n<i>Toque numa ordem para comprar. Para vender, use /sell.</i>",
    "mk.empty": "Ainda não há ofertas. Seja o primeiro: /sell quantidade preço",
    "mk.order_line": "🥩 #{id} · <b>{qty} un.</b> a <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} un. a {price} 🪙",
    "mk.btn_my": "📋 Minhas ordens",
    "mk.btn_sell_help": "💰 Como vender costeletas",
    "mk.btn_refresh": "🔄 Atualizar",
    "mk.btn_back": "← Voltar à bolsa",
    "mk.pick": "🛒 <b>Ordem #{id}</b>: {qty} un. disponíveis a {price} 🪙.\nQuantas?",
    "mk.btn_qty": "{qty} un. — {total} 🪙",
    "mk.btn_qty_all": "Todas, {qty} un. — {total} 🪙",
    "mk.buy_toast": "Negócio fechado!",
    "mk.buy_done": "✅ Comprou <b>{qty} costeletas</b> por <b>{total} 🪙</b>. Já estão no estoque — abasteça seus Perfuradores!",
    "mk.sold_notify": "💰 <b>Bolsa: vendido!</b> Ordem #{id}: {qty} un. a {price}. Você recebeu <b>+{got} 🪙</b> (taxa de {fee} queimada).",
    "mk.sell_help": "💰 <b>COMO VENDER COSTELETAS</b>\n\nComando: <code>/sell quantidade preço</code>\nExemplo: <code>/sell 10 50</code> — 10 costeletas a 50 🪙.\n\nAs costeletas saem do estoque e ficam na ordem (cancele quando quiser). Até {max_qty} un. por ordem e {max_orders} ordens abertas. Uma taxa de {fee}% é queimada na venda.",
    "mk.sell_confirm": "📝 Colocar <b>{qty} costeletas</b> a <b>{price}</b> 🪙?\nTotal: {total} · taxa {fee} queima · você recebe <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ COLOCAR NA BOLSA",
    "mk.btn_cancel": "❌ Cancelar",
    "mk.sell_toast": "Ordem publicada!",
    "mk.sell_done": "✅ Ordem <b>#{id}</b> publicada: {qty} un. a {price} 🪙. Aviso quando vender.",
    "mk.cancelled_toast": "Cancelado",
    "mk.cancel_text": "❌ <b>Cancelado.</b> As costeletas continuam no estoque.",
    "mk.my_header": "📋 <b>SUAS ORDENS</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} un. a {price} 🪙",
    "mk.my_empty": "📋 Você não tem ordens abertas.",
    "mk.btn_cancel_order": "❌ Retirar ordem #{id}",
    "mk.order_cancelled": "↩️ Ordem #{id} retirada: <b>{qty} costeletas</b> voltaram ao estoque.",
    "mk.err_qty": "❌ Quantidade: de 1 a {max} costeletas por ordem.",
    "mk.err_price": "❌ Preço: de {min} a {max} 🪙 por costeleta.",
    "mk.err_no_cutlets": "❌ Só há {have} costeletas no estoque. As da geladeira não vão à bolsa — veja /farm.",
    "mk.err_too_many": "❌ Limite: no máximo {max} ordens abertas. Retire uma em «Minhas ordens».",
    "mk.err_not_found": "❌ Essa ordem já foi fechada.",
    "mk.err_own": "🤨 Não dá para comprar a própria ordem.",
    "mk.err_insufficient": "❌ Saldo insuficiente: precisa de {total} 🪙.",
    "farm.btn_market": "📈 Bolsa de costeletas",

    # ---------------- recursos (onda 22.10, noite) ----------------
    "res.metal": "Metal",
    "res.hydrogen": "Hidrogênio",
    "res.crystal": "Cristais",
    "res.parts": "Peças",
    "res.none": "nada por enquanto",
    "games.resource_gain": "{icon} Minerado: <b>+{qty} {name}</b> (total {total}) → /workshop",
    "duel.metal_gain": "⛏ Troféu do duelo: <b>+{metal} Metal</b> → /workshop",
    "quest.win_resources": "\n📦 E mais um kit de recursos: <b>{qty}</b> de cada → /workshop",
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
    "app.goto_market": "📈 A <b>Bolsa de costeletas</b> é mais prática no app do jogo: vitrine, vendas e suas ordens numa tela só.",
    "farm.boost_armor": "🛡 Ciber-Armadura nv. {level}: +{percent}% de mineração para sempre",
    "farm.boost_station": "🛰 Estação da equipe nv. {level}: +{percent}% de mineração",
    "clan.btn_station": "🛰 Estação da equipe",

    # ---------------- oficina ----------------
    "ws.header": (
        "🔧 <b>OFICINA</b>\n"
        "..................................................\n\n"
        "🧰 Seus recursos: {stock}\n"
        "⛏ Metal — PPT e duelos · 💧 Hidrogênio — Maior/Menor · "
        "💎 Cristais — Quiz · ⚙️ Peças — Ciber-Cofre. As missões dão um kit.\n\n"
        "🛡 Ciber-Armadura: <b>nível {armor}/{armor_max}</b> (+{armor_pct}% de mineração por nível, para sempre)\n"
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
    "ws.done_armor": "🛡 <b>Ciber-Armadura nível {level}!</b> Mineração da fazenda: <b>+{percent}%</b> para sempre.",
    "ws.done_shuttle": "🚀 <b>Shuttle montado!</b> A taxa da bolsa agora é {fee}%, até {qty} bifes por ordem. Para sempre.",
    "ws.err_unknown": "❌ Essa receita não existe.",
    "ws.err_resources": "🔒 Faltam recursos: {kind} precisa de {need}, você tem {have}. Minere nos jogos!",
    "ws.err_shuttle_owned": "🚀 O Shuttle já está montado — é um por jogador.",
    "ws.err_armor_max": "🛡 A armadura já está no nível máximo ({max}).",

    # ---------------- saques ----------------
    "raid.header": (
        "🏴‍☠️ <b>SAQUES</b>\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
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
        "..................................................\n\n"
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
    "resHint": "Cada vitória traz o recurso do seu jogo. Gaste-os na oficina.",
    "bonusReady": "🎁 PEGAR O BIFE DIÁRIO",
    "bonusWait": "⏳ Bônus em {h} h {m} min",
    "bonusDone": "🎉 Bife no estoque!",
    "team": "🏆 MINHA EQUIPE",
    "clan": "CLÃ",
    "teamLabel": "Equipe",
    "captain": "👑 Você está no comando!",
    "members": "Elenco",
    "noTeam": "Você ainda está sem equipe. Crie a sua ou entre em outra no chat do bot: «🏆 Equipes e clãs».",
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
    "footer": "Jogos e quiz ficam no chat do bot",
    "noProfile": "Perfil não encontrado. Abra o bot e toque em /start!",
    "blocked": "Conta bloqueada pela administração.",
    "error": "Não foi possível carregar os dados. Tente mais tarde.",
    "outside": "Abra este aplicativo pelo bot ROFL HUB no Telegram.",
    "robotsTitle": "🤖 SEUS ROBÔS",
    "buyMore": "🛒 Comprar",
    "rateShort": "{v} 🪙/h",
    "refuelOne": "🥩 Carregar 1",
    "refuelAll": "⚡ Carregar todos",
    "refueled": "Carregado: {n} 🥩",
    "res_metal_src": "PPT e duelos",
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
    "ws_armorLvl": "nível {l}/{m} · +{p}% de mineração por nível",
    "ws_shuttleOn": "🚀 Shuttle montado: taxa da bolsa {fee}%",
    "ws_shuttleOff": "🚀 Shuttle não montado: taxa da bolsa {fee}%",
    "eff_nitrogen": "+40% de mineração para todos os robôs",
    "eff_nuclear": "×5 de mineração, os Perfuradores comem ×3 bifes",
    "eff_drone": "os robôs não envelhecem",
    "eff_shield": "ninguém pode saquear você",
    "eff_cutlet": "1 ciber-bife no estoque",
    "eff_armor": "+10% de mineração para sempre",
    "eff_shuttle": "taxa da bolsa pela metade, ordens de até 500 bifes — para sempre",
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
    "mk_title": "📈 BOLSA DE BIFES",
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
    "invite": "🤝 Link de indicação: +1000 por amigo",
    "transfer": "🔄 Enviar moedas a um jogador",
    "market": "📈 Bolsa de costeletas: comprar ou vender",
    "sell": "💰 Vender costeletas: /sell quantidade preço",
    "my_stats": "📊 Minhas estatísticas",
    "faq": "📚 Perguntas frequentes",
    "rules": "📜 Termos de uso",
    "paysupport": "🛟 Suporte de pagamentos",
    "workshop": "🔧 Oficina: recursos viram melhorias",
    "raid": "🏴‍☠️ Saques: reconhecimento e revanche",
    "goals": "🎯 Metas diárias e baú",
    "station": "🛰 Estação da equipe: projeto em comum",
}
