"""Испанская (нейтральная латиноамериканская) локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> monedas
# Младший Майнер -> Robot Minero
# Кибер-Бурильщик -> Ciber-Perforador
# кибер-котлета -> ciber-chuleta (кратко: chuleta)
# Холодильник -> Refrigerador
# склад (инвентарь) -> inventario
# ферма / Кибер-Ферма -> granja / Ciber-Granja
# Ядерный Разгон x5 -> Impulso Nuclear x5
# Азотное Охлаждение +40% -> Enfriamiento de Nitrógeno +40%
# Мастер-дрон -> Dron Maestro
# Кибер-Сейф -> Ciber-Caja Fuerte
# Мега-Клан -> Mega-Clan
# Безлимит (снятие лимитов) -> Sin Límite / quitar límites
# дуэли -> duelos; банк дуэли -> pozo; ставка -> apuesta; жест -> gesto
# битвы -> Batallas
# квесты -> misiones
# уровень интеллекта -> nivel de inteligencia; викторина -> Trivia
# команда -> equipo; клан -> clan; банда -> banda; тиммейты -> compañeros
# ресурсы (волна 22.10): Металл -> Metal; Водород -> Hidrógeno; Кристаллы -> Cristales; Детали -> Piezas
# Мастерская -> Taller; Кибер-броня -> Ciber-Armadura; Шаттл -> Transbordador
# Налёт -> Asalto; Стойка обороны -> Postura de defensa; Разведка -> Exploración; Реванш -> Revancha
# Щит -> Escudo; Сундук -> Cofre; Серия -> Racha; Станция команды -> Estación del equipo
# добыча (фермы) -> extracción; биржа котлет -> Bolsa de chuletas

BUTTONS: dict[str, str] = {
    "main_menu": "📱 MENÚ PRINCIPAL",
    "profile": "👤 MI PERFIL",
    "farm": "🚜 MI GRANJA",
    "games_zone": "🕹️ ZONA DE JUEGOS",
    "teams": "🏆 EQUIPOS Y CLANES",
    "shop": "🏪 TIENDA",
    "shop_cat_farm": "🚜 PARA LA GRANJA",
    "shop_cat_games": "🕹️ JUEGOS",
}

STRINGS: dict[str, str] = {
    # ---------------- общее ----------------
    "common.no_profile": "⚠️ Perfil no encontrado. Pulsa /start para registrarte.",
    "common.btn_menu": "💿 Menú Principal",
    "common.blocked": "🚫 Tu cuenta fue bloqueada por la administración de ROFL HUB.",
    "common.feature_off": "⚙️ Esta sección está en mantenimiento. ¡Vuelve un poco más tarde!",
    "common.maintenance": "🛠 ROFL HUB está en mantenimiento rápido. ¡Volvemos pronto — tus monedas y tu progreso están a salvo!",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>¡Qué bueno tenerte de vuelta, @{username}!</b>\nTu progreso está a salvo. El panel de navegación está en la parte inferior de la pantalla.",
    "start.btn_continue": "🛸 CONTINUAR",
    "start.btn_cutlet": "¿Qué es una ciber-chuleta?🥩🤔",
    "start.btn_fight": "¡Cuéntame rápido y A LA BATALLA!",
    "start.console": "🚀 <b>¡Consola de control activada! Usa los botones en la parte inferior de la pantalla.</b>",
    "start.intro1": (
        "👋 <b>¡Hola! Soy ROFL HUB BOT, el bot principal del ecosistema de juegos ROFL HUB. "
        "¡Un hub de nueva generación con juegos y conocimiento!</b>\n\n"
        "<b>Aquí puedes:</b>\n"
        "🎮 Jugar partidas de chat contra el bot y contra otros jugadores\n"
        "💸 Ganar moneda del juego por tus victorias o montar una granja que la extrae las 24 horas\n"
        "🤼 Crear un equipo y asaltar el TOP del ranking\n"
        "🏆 Convertir tu equipo en un clan y pelear en el ranking internacional\n"
        "💰 Ganar junto a tu banda un premio de un millón de monedas\n"
        "👑 Comprar una publicación destacada en nuestras redes o en el sitio web para promocionarte a ti o a tu blog\n\n"
        "<b>Este chat-bot puede:</b>\n"
        "🎮 Mostrar la lista de todos los juegos, canales y sitios de ROFL HUB\n"
        "⚡ Otorgar monedas por juegos, batallas de equipos y clanes, logros, actividad y referidos\n"
        "🔄 Transferir monedas del juego a otro jugador de ROFL HUB\n"
        "💎 Vender publicaciones en el sitio web y lugares VIP para personas y blogueros\n"
        "🚀 Vender aceleradores, títulos, estatus y mucho más...\n\n"
        "<i>Pulsa «CONTINUAR» y te cuento más 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>¡AQUÍ TIENES TUS PRIMERAS RECOMPENSAS POR REGISTRARTE!</b>\n"
        "..................................................\n"
        "💸 Recibiste: <b>{balance} monedas</b>\n"
        "🥩 Recibiste: <b>{cutlets} ciber-chuleta</b>\n"
        "..................................................\n"
        "Este es tu bono de bienvenida por unirte al club ROFL HUB.\n\n"
        "🔒 <i>El bono se entrega solo una vez, en el momento del registro.</i>\n\n"
        "Las monedas se pueden gastar de muchas formas: son la base de la economía del hub. Cuídalas bien...\n\n"
        "⁉️ <b>Pero seguro te surge una pregunta:</b> ¿qué es esa chuleta? ¿A quién hay que alimentar?"
    ),
    "start.intro3": (
        "<b>PRIMERO, ¿POR QUÉ SON TAN IMPORTANTES LAS MONEDAS DEL JUEGO?</b>\n\n"
        "Las monedas mueven todo el comercio, las competencias y las compras en <b>ROFL HUB</b>. "
        "¡Es casi la única moneda de juego del mundo que puedes extraer gratis!\n"
        "..................................................\n"
        "<b>Hay muchas formas de conseguirlas:</b>\n"
        "- Invitar amigos con tu enlace de referido\n"
        "- Ganar partidas contra el bot\n"
        "- Ganar duelos contra otros jugadores\n"
        "- Participar en batallas de equipos y clanes\n"
        "- Reclamar el bono diario y completar tareas\n"
        "- Conseguir un robot que extrae monedas 24/7 (Robot Minero / Ciber-Perforador)\n"
        "..................................................\n"
        "<b>Si tienes un robot de nivel dos (el Ciber-Perforador), hay que alimentarlo todos los días. "
        "Ahí entra la ciber-chuleta: el combustible de la minería automática, "
        "¡que se regala gratis cada día! Tu tarea es simple: entrar y alimentar a tu robot.</b>\n\n"
        "Si no lo alimentas a tiempo, el robot se descarga y la extracción se detiene.\n\n"
        "El Robot Minero (nivel uno) no necesita combustible. "
        "¡Importante! Todo robot se compra por 30 días; después hay que comprarlo de nuevo o conseguir un Dron Maestro. "
        "Lo irás entendiendo sobre la marcha:) No nos distraigamos.\n\n"
        "Quiero contarte un poco más sobre <b>ROFL HUB</b> para que entiendas cómo funciona todo aquí.\n\n"
        "🛑 <b>Este es el último mensaje de nuestra presentación. Después, ¡directo a la batalla! :)</b>"
    ),
    "start.intro4": (
        "<b>LA VERSIÓN CORTA. ROFL HUB ES:</b>\n"
        "- Juegos de chat-bot para todos los gustos\n"
        "- La posibilidad de crear un equipo (hasta 50 personas)\n"
        "- La posibilidad de convertirlo en un clan (hasta 1000 personas)\n"
        "- Batallas de equipos y clanes por premios\n"
        "- El canal ROFL HUB CHANNEL con diversión y conocimiento\n"
        "- Página de Instagram — rofl_hub_global\n"
        "- El sitio rofl-hub.com para chatear y promocionarte sin registro\n"
        "- ¡Miles de jugadores en todo el mundo, y entre ellos pueden estar tus nuevos amigos!\n"
        "..................................................\n"
        "<b>Como prometí, este es el mensaje final. ¡Ahora, a la batalla! Comandos útiles:</b>\n\n"
        "/menu — control rápido de las funciones\n"
        "/games — lista de todos los juegos\n"
        "/faq — preguntas frecuentes\n"
        "/rules — acuerdo de usuario\n"
    ),

    # ---------------- меню и игровая зона ----------------
    "menu.text": (
        "📱 <b>MENÚ PRINCIPAL DEL ECOSISTEMA ROFL HUB</b>\n"
        "..................................................\n\n"
        "👤 <b>PERFIL PERSONAL Y PASAPORTE:</b>\n"
        "• /start — Comenzar la presentación y registrar tu cuenta\n"
        "• /profile — Tu pasaporte, saldo y equipo en tiempo real\n"
        "• /my_stats — Tus estadísticas históricas de los últimos 30 días\n\n"
        "🚜 <b>CIBER-GRANJA Y AUTOMATIZACIÓN:</b>\n"
        "• /farm — Hub de combustible: recarga y velocidad de producción de tus robots\n"
        "• /shop — Mercado: compra de mineros, chuletas y mejoras del hub\n\n"
        "🕹️ <b>SALA DE JUEGOS:</b>\n"
        "• /games — Hub con todos los juegos contra el bot\n"
        "• /quiz — Trivia de velocidad: 15 segundos por respuesta, niveles y bonos\n"
        "• /duel — DUELOS 1 contra 1 con jugadores reales: mesas de 10/100/1000\n"
        "• /quests — MISIONES: historias de detectives, comedias y acertijos con recompensas\n"
        "• /rps, /high_low, /safe — Juegos rápidos por monedas\n\n"
        "👥 <b>GESTIÓN DE BANDAS:</b>\n"
        "• /create_team — Registrar tu propio equipo por 100 000 monedas\n"
        "• /my_team — Panel de la banda y la LISTA DE COMPAÑEROS con niveles 🧠\n"
        "• /all_teams — Ruleta de equipos al azar\n\n"
        "💸 <b>DINERO Y AMIGOS:</b>\n"
        "• /invite — Tu enlace de referido: +1000 monedas por amigo\n"
        "• /transfer — Enviar monedas a otro jugador\n\n"
        "📚 <b>AYUDA Y REGLAS:</b>\n"
        "• /faq — La guía completa del ecosistema (se abre en la Mini App)\n"
        "• /rules — Acuerdo de usuario\n"
        "..................................................\n"
        "<i>⚙️ ¡Usa el panel de juego permanente de dos columnas en la parte inferior de la pantalla para navegar al instante!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>¡TE DAMOS LA BIENVENIDA A LA ZONA DE JUEGOS DE ROFL HUB!</b>\n"
        "..................................................\n\n"
        "Aquí puedes enfrentarte al bot en duelos rápidos o ponerte a prueba en el sprint intelectual "
        "para llevarte el premio gordo... ¡o perderlo todo!\n\n"
        "💸 Una victoria paga: <b>+2 monedas</b> (Ciber-Caja Fuerte: <b>+5</b>)\n"
        "💀 Una derrota o un empate cuesta: <b>-1 moneda</b>\n"
        "🧠 La Trivia tiene cronómetro de 15 segundos y niveles de inteligencia: el nivel 1 son 10 respuestas correctas y <b>+100 monedas</b>; "
        "cada nivel siguiente es 10 respuestas más largo, ¡pero la recompensa crece en 100!\n\n"
        "..................................................\n"
        "👇 <b>TOCA UN BOTÓN ABAJO PARA EMPEZAR UNA RONDA AHORA MISMO:</b>"
    ),
    "menu.btn_quiz": "🧠 Trivia",
    "menu.btn_rps": "🪨 PPT",
    "menu.btn_hl": "📈 Mayor/Menor",
    "menu.btn_safe": "🔐 Ciber-Caja Fuerte",
    "menu.btn_duel": "⚔️ DUELOS 1 vs 1",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Tu pasaporte, tu granja, tu equipo y el top de los más ricos, todo en una pantalla de neón. "
        "¡La chuleta diaria se puede reclamar directamente desde ahí!\n\n"
        "👇 Toca el botón:"
    ),
    "app.btn": "🎮 ABRIR LA MINI APP",
    "app.unavailable": "⚙️ La Mini App todavía se está conectando a los servidores del ecosistema. ¡Vuelve en un rato!",
    "faq.teaser": (
        "📚 <b>GUÍA DEL ECOSISTEMA ROFL HUB</b>\n"
        "..................................................\n\n"
        "La versión corta:\n"
        "🚜 Los robots extraen monedas las 24 horas: el Robot Minero — 5/h sin combustible, "
        "el Ciber-Perforador — 10/h, y CADA Perforador come su propia ciber-chuleta al día. "
        "Todos los robots viven 30 días (el Dron Maestro pausa el desgaste).\n"
        "🧠 Trivia: 15 segundos por respuesta, niveles de inteligencia con recompensas crecientes.\n"
        "⚔️ Duelos con jugadores reales en mesas de 10/100/1000 monedas.\n"
        "🏆 Equipos de hasta 50 combatientes (Mega-Clan: hasta 1000) y Batallas especiales con premios para todos.\n\n"
        "..................................................\n"
        "👇 <b>La guía completa con todas las mecánicas, a un toque:</b>"
    ),
    "faq.btn_open": "📖 ABRIR LA GUÍA COMPLETA",
    "rules.teaser": (
        "📜 <b>ACUERDO DE USUARIO DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "Lo esencial en dos palabras:\n"
        "🪙 Las monedas y todos los objetos del juego son elementos virtuales de entretenimiento: "
        "no son dinero y no se cambian por fondos reales.\n"
        "💫 Las compras se hacen solo con Telegram Stars oficiales; los artículos digitales se entregan "
        "al instante y, si la entrega falla, las Stars se devuelven automáticamente.\n"
        "🛡️ No recopilamos teléfonos, geolocalización ni datos personales.\n"
        "🤝 Están prohibidos los insultos, las trampas y las multicuentas: las infracciones pueden terminar en bloqueo.\n\n"
        "..................................................\n"
        "👇 <b>El texto completo del acuerdo y el descargo de responsabilidad, a un toque:</b>\n"
        "<i>⚖️ Al usar el bot confirmas que aceptas las condiciones.</i>"
    ),
    "rules.btn_open": "📜 ABRIR EL ACUERDO COMPLETO",
    "quest.list_header": (
        "🗺️ <b>MISIONES DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "Historias interactivas con decisiones y caminos alternos: detectives, comedias, acertijos. "
        "¡La primera victoria en cada misión paga monedas y puedes rejugarlas cuantas veces quieras!\n"
        "🌐 <i>Por ahora las historias están en ruso; el paquete en español viene en camino.</i>\n\n"
        "👇 <b>Elige una historia:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} monedas por la primera victoria\n"
        "..................................................\n\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Misión completada, recompensa reclamada. ¡Rejuega cuando quieras!</i>",
    "quest.card_progress": "⏯ <i>Tienes una partida sin terminar.</i>",
    "quest.card_new": "🆕 <i>Todavía no has jugado esta historia.</i>",
    "quest.btn_start": "▶️ EMPEZAR LA MISIÓN",
    "quest.btn_restart": "🔄 EMPEZAR DE NUEVO",
    "quest.btn_resume": "⏯ CONTINUAR",
    "quest.btn_list": "🗺️ A la lista de misiones",
    "quest.btn_replay": "🔄 Jugar otra vez",
    "quest.win_first": "\n\n🏆 <b>¡MISIÓN COMPLETADA! Recompensa: +{coins} monedas.</b>",
    "quest.win_repeat": "\n\n✅ <b>¡Completada otra vez!</b> La recompensa de esta misión ya fue reclamada antes.",
    "quest.fail_footer": "\n\n💀 <i>No fue el mejor final... ¡pero siempre puedes rejugar la historia!</i>",
    "quest.stale": "⏳ Esa escena ya quedó atrás. ¡Seguimos desde el punto actual!",
    "quest.no_coins": "❌ No te alcanzan las monedas para la pista ({cost}). ¡Pasa por tu granja!",
    "quest.not_found": "❌ Misión no encontrada.",
    "menu.btn_quests": "🗺️ MISIONES",

    # ---------------- ферма ----------------
    "farm.btn_bonus": "🎁 RECLAMAR BONO (chuleta cada 24 h)",
    "farm.btn_load1": "🥩 Cargar 1 chuleta",
    "farm.btn_loadall": "⚡ Cargar TODAS",
    "farm.btn_shop": "🏪 Ir a la Tienda",
    "farm.status_all_fueled": "🟢 ¡Todos los Ciber-Perforadores están cargados y extrayendo monedas!",
    "farm.status_partial": "🟡 Cargados {fueled} de {total} Ciber-Perforadores. ¡El resto espera chuletas en el refrigerador!",
    "farm.status_no_fuel": "🔴 ¡Los Ciber-Perforadores se detuvieron! No hay suficiente combustible en el refrigerador.",
    "farm.status_no_drills": "💡 Consigue Ciber-Perforadores en /shop para aumentar tus ingresos.",
    "farm.boost_nuclear": "🔋 Impulso Nuclear x5 hasta el {until} UTC (consumo de chuletas ×3)",
    "farm.boost_nitrogen": "❄️ Enfriamiento de Nitrógeno +40% hasta el {until} UTC",
    "farm.boost_drone": "🛸 El Dron Maestro extiende la vida de los robots hasta el {until} UTC",
    "farm.no_boosts": "No hay mejoras activas; date una vuelta por /shop.",
    "farm.burnout": "🔥 Próximo robot en quemarse: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Activar tu Robot Becario (gratis)",
    "farm.intern_activated": "🤖 ¡Tu Robot Becario entró en turno! +1 moneda por hora para siempre, sin combustible ni caducidad.",
    "farm.intern_already": "🤖 Tu Robot Becario ya está trabajando.",
    "farm.intern_line": "🤖 Robots Becarios ({rate} moneda/h, eternos): <code>{count}</code>",
    "farm.intern_hint": "🎁 ¡Tienes un Robot Becario gratis! Pulsa el botón de abajo y minará 1 moneda por hora para siempre.",
    "farm.dashboard": (
        "🚜 <b>HUB CENTRAL DE COMBUSTIBLE DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Robots activos en la planta: <b>{total}</b>\n"
        "• Robots Mineros ({junior_rate} monedas/h): <code>{junior}</code>\n"
        "• Ciber-Perforadores ({premium_rate} monedas/h): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VELOCIDAD ACTUAL DE TU GRANJA:</b>\n"
        "• Producción por hora: <b>+{speed_hour} monedas</b>\n"
        "• Producción por día: <b>+{speed_day} monedas</b>\n\n"
        "⚡ <b>MEJORAS:</b>\n{boosts}\n\n"
        "📋 <b>ESTADO DE LA PLANTA DE JUEGO:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>ESTADO DEL REFRIGERADOR AUTOMÁTICO:</b>\n"
        "🥩 Reserva de combustible: <b>{fridge} / {capacity}</b>\n"
        "💼 Chuletas en el inventario: <code>{inv}</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Importante: los robots viven 30 días (el Dron Maestro pausa el desgaste). "
        "CADA Ciber-Perforador consume SU propia chuleta entera del refrigerador por cada "
        "24 horas de trabajo: 3 robots — 3 chuletas al día. ¡No descuides la recarga!</i>"
    ),
    "farm.bonus_ok": "🎁 ¡Ciber-chuleta añadida a tu inventario! Vuelve en 24 horas.",
    "farm.bonus_wait": "⏳ ¡El bono ya fue reclamado! La próxima chuleta llega en {hours} h {minutes} min.",
    "farm.no_inv_cutlets": "❌ ¡No tienes ciber-chuletas en el inventario! Cómpralas en /shop",
    "farm.fridge_full": "📦 ¡Tu Refrigerador ya está completamente lleno!",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>PANEL PERSONAL DEL JUGADOR DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "🆔 Tu ID de Pasaporte: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Monedas ahora mismo: <b>{balance} monedas</b>\n"
        "🏆 Tu estatus: <b>{team}</b>\n"
        "🧠 Nivel de inteligencia: <b>{level}</b> · para el nivel {next_level}: "
        "<b>{left}</b> respuestas correctas en /quiz (recompensa: +{reward} monedas)\n\n"
        "..................................................\n"
        "<i>Aquí ves lo que tienes ahora mismo. ¡Usa los botones para volar a otras secciones!</i>"
    ),
    "profile.no_team": "Sin equipo",
    "profile.team_label": "Equipo",
    "profile.clan_label": "Clan",
    "profile.btn_farm": "🚜 Mi Ciber-Granja",
    "profile.btn_shop": "🏪 Tienda",
    "profile.stats": (
        "📊 <b>ESTADÍSTICAS DE LOGROS DE JUEGO (30 DÍAS)</b>\n"
        "..................................................\n\n"
        "🧠 Nivel de inteligencia de juego: <b>{level}</b> (respuestas correctas en total: {total})\n"
        "🎮 Rondas de duelos jugadas: <b>{played}</b>\n"
        "🏆 Victorias conseguidas: <code>{won}</code>\n"
        "👥 Amigos activos invitados: <b>{refs}</b>\n\n"
        "..................................................\n"
        "<i>¡Las estadísticas guardan tus méritos históricos y logros pasados aunque las monedas ganadas ya se hayan gastado en el mercado!</i>"
    ),
    "img.passport": "ID DE PASAPORTE: {user_id}",
    "img.owner": "LÍDER: @{username}",
    "img.balance": "Saldo: {balance} monedas",
    "img.fridge": "En el refrigerador: {fridge} / {capacity}",
    "img.inv": "Chuletas en inventario: {inv}",
    "img.junior": "Robots Mineros: {count}",
    "img.premium": "Ciber-Perforadores: {count}",

    # ---------------- игры: общий движок ----------------
    "games.win": "🎉 <b>¡VICTORIA!</b> 🎉\nMonedas acreditadas: <b>+{reward}</b>",
    "games.lose": "💀 <b>¡DERROTA!</b>\nMonedas descontadas: <b>-{penalty}</b>",
    "games.draw": "🤝 <b>¡EMPATE!</b>\nMonedas descontadas: <b>-{penalty}</b>",
    "games.limit": (
        "🛑 <b>¡Límite diario alcanzado!</b>\n\n"
        "Hoy ya te llevaste {limit} victorias en {game}. El límite se reinicia a las 00:00 UTC.\n\n"
        "⚡ Quitar el límite por 24 horas — 5 ★, por 30 días — 99 ★ (sección «Juegos» en /shop)."
    ),
    "games.no_coins": "❌ Tienes 0 monedas y no puedes pagar la cuota de la ronda. ¡Recoge los ingresos de tu granja en /farm!",
    "games.balance": "💰 Saldo: <b>{balance} monedas</b>",
    "games.btn_retry": "🎮 ¡Jugar otra vez!",
    "games.btn_hub": "🕹️ Zona de juegos",
    "games.level_up": (
        "🏅 <b>¡SUBISTE AL NIVEL DE INTELIGENCIA {level}!</b> ¡Recompensa: <b>+{bonus} monedas</b>!\n"
        "Siguiente nivel: {next_required} respuestas correctas → +{next_reward} monedas."
    ),
    "games.name.rps": "Piedra-Papel-Tijera",
    "games.intern_bonus": "🤖 ¡Nivel {level}! Otro Robot Becario llegó a tu granja: ahora tienes {count}.",
    "games.name.hl": "Mayor/Menor",
    "games.name.quiz": "Trivia",
    "games.name.safe": "Caja Fuerte",

    # ---------------- КНБ ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>PIEDRA-PAPEL-TIJERA</b>\n\n"
        "Victoria: <b>+{reward}</b> · Derrota/empate: <b>-{penalty}</b>\n"
        "Límite diario de victorias: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Piedra",
    "rps.scissors": "✂️ Tijera",
    "rps.paper": "🧻 Papel",
    "rps.draw": "🤝 <b>¡Empate!</b> Ambos eligieron {bot}.",
    "rps.win": "🏆 <b>¡Victoria!</b> {user} vence a {bot}.",
    "rps.lose": "💀 <b>Ganó el bot.</b> {bot} vence a {user}.",

    # ---------------- Больше/Меньше ----------------
    "hl.intro": (
        "🎲 <b>MAYOR O MENOR</b>\n\nEl bot puso el número: <b>{base}</b>.\n"
        "¿El número oculto será mayor o menor?\n"
        "Victoria: <b>+{reward}</b> · Derrota: <b>-{penalty}</b> · Límite: <b>{limit}</b> victorias"
    ),
    "hl.btn_up": "📈 Mayor",
    "hl.btn_down": "📉 Menor",
    "hl.result": "🎲 <b>RESULTADO DE LA RONDA</b>\n\nNúmero del bot: <b>{base}</b> · Oculto: <b>{secret}</b>",

    # ---------------- викторина ----------------
    "quiz.round": (
        "🧠 <b>TRIVIA • {category}</b>\n"
        "🤔 PREGUNTA: <b>{question}</b>\n\n"
        "<i>🌐 Por ahora las preguntas están en ruso; ¡el paquete en español viene en camino!</i>"
    ),
    "quiz.btn_new": "🧠 Nueva pregunta",
    "quiz.timeout": "⌛ <b>¡SE ACABÓ EL TIEMPO!</b> ⌛\nRespuesta correcta: <b>{correct}</b>",
    "quiz.stale": "⏳ Esta pregunta ya no está activa. ¡Lanza una nueva!",
    "quiz.stale_alert": "Esta pregunta ya no está activa. ¡Lanza una nueva!",
    "quiz.empty": "⚠️ La base de preguntas está vacía. Avisa al administrador.",
    "quiz.wrong": "❌ <b>Error</b> ❌\nRespuesta correcta: <b>{correct}</b>",
    "quiz.lost_line": "💀 ¡<b>-{penalty} moneda</b> por la derrota!",
    "quiz.level_line": (
        "🧠 Nivel de inteligencia: <b>{level}</b>\n"
        "Victorias restantes para el nivel {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>¡{seconds} segundos para responder!\n"
        "Correcta: +{win} monedas a tu saldo\n"
        "Error / sin tiempo: -{penalty} moneda\n"
        "Límite: {limit} victorias al día</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>CIBER-CAJA FUERTE</b>\n\n"
        "¡Adentro hay un botín de <b>{jackpot} monedas</b>! La puerta está cerrada con un código del 1 al {codes}. "
        "Tienes un solo intento.\n"
        "Si la abres: <b>+{jackpot}</b> · Alarma: <b>-{penalty}</b> · Límite: <b>{limit}</b> victorias"
    ),
    "safe.btn_retry": "🔐 ¡Forzarla otra vez!",
    "safe.win": "🔓 <b>¡Caja fuerte abierta!</b> El código era: <b>{code}</b>.",
    "safe.lose": "🚨 <b>¡Saltó la alarma!</b> Marcaste {guess}, pero el código era: <b>{code}</b>.",

    # ---------------- дуэли ----------------
    "duel.intro": (
        "⚔️ <b>DUELOS 1 CONTRA 1: PIEDRA-PAPEL-TIJERA POR UNA APUESTA</b>\n"
        "..................................................\n\n"
        "Elige una mesa según tu bolsillo, como en el póker. La apuesta se descuenta de inmediato, "
        "¡y tu rival es un jugador real de ROFL HUB!\n\n"
        "💰 El pozo = ambas apuestas. El ganador se lleva el <b>{payout_percent}%</b> del pozo, "
        "el <b>{burn_percent}%</b> se quema para siempre (¡deflación!).\n"
        "🤝 Si hay empate, los gestos se repiten al instante y el pozo queda en la mesa.\n"
        "⏱ Tienes <b>{move_timeout} segundos</b> por gesto; si guardas silencio, el generador aleatorio elige por ti.\n"
        "🏆 ¡Las victorias en duelos cuentan para tu equipo en las Batallas!\n\n"
        "👇 <b>ELIGE UNA MESA:</b>"
    ),
    "duel.btn_table": "⚔️ Mesa de {stake} monedas",
    "duel.btn_cancel": "❌ Salir y recuperar la apuesta",
    "duel.btn_move_rock": "🪨 Piedra",
    "duel.btn_move_scissors": "✂️ Tijera",
    "duel.btn_move_paper": "🧻 Papel",
    "duel.waiting": (
        "🪑 <b>Estás en la mesa de {stake} monedas.</b> Tu apuesta ya está en el pozo.\n"
        "Esperando al segundo combatiente... En cuanto se siente, ¡los dos pasarán a elegir su gesto!\n"
        "<i>La cola vive {ttl} minutos; después tu apuesta vuelve automáticamente.</i>"
    ),
    "duel.cancelled": "🚪 Dejaste la mesa. La apuesta de <b>{stake} monedas</b> volvió a tu saldo.",
    "duel.expired": "⌛ No apareció ningún rival en la mesa de {stake}. La apuesta de <b>{stake} monedas</b> fue devuelta.",
    "duel.matched": (
        "⚔️ <b>¡RIVAL ENCONTRADO! Mesa de {stake} monedas.</b>\n"
        "Pozo: <b>{bank} monedas</b> · El ganador se lleva: <b>{payout}</b>\n\n"
        "⏱ ¡Tienes <b>{timeout} segundos</b> para elegir tu gesto!"
    ),
    "duel.move_saved": "✊ ¡Gesto registrado! Esperando el gesto del rival...",
    "duel.draw_replay": (
        "🤝 <b>¡EMPATE! Ronda {round}.</b> Ambos mostraron el mismo gesto.\n"
        "El pozo sigue en la mesa. ⏱ Otros {timeout} segundos: elige tu gesto:"
    ),
    "duel.win": (
        "🏆 <b>¡EL DUELO ES TUYO!</b>\n\n"
        "Tu {winner_move} vence a {loser_move}.\n"
        "💰 Ganancia: <b>+{payout} monedas</b> · 🔥 Quemado del pozo: {burned}\n"
        "💼 Saldo: <b>{balance} monedas</b>"
    ),
    "duel.lose": (
        "💀 <b>DUELO PERDIDO.</b>\n\n"
        "El gesto {winner_move} del rival vence a tu {loser_move}.\n"
        "📉 Tu apuesta de <b>{stake} monedas</b> se fue al pozo del ganador.\n"
        "¿Revancha?"
    ),
    "duel.reaper_prefix": "⏰ <b>¡Tiempo de la ronda agotado!</b> Los gestos que faltaban los eligió el generador aleatorio.\n\n",
    "duel.bad_table": "❌ Esa mesa no existe.",
    "duel.already_in": "⚠️ ¡Ya estás en una mesa o en pleno combate! Termina primero tu duelo actual.",
    "duel.no_coins": "❌ Para esta mesa necesitas {stake} monedas en tu saldo.",
    "duel.cancel_impossible": "⚠️ Esta cola ya no se puede cancelar (se encontró un rival o la mesa se cerró).",
    "duel.not_active": "⌛ Este duelo ya terminó.",
    "duel.not_participant": "🔒 ¡Este no es tu duelo!",
    "duel.move_already": "✋ Ya mostraste tu gesto en esta ronda. ¡Esperando al rival!",
    "duel.bad_move": "❌ Gesto desconocido.",
    "duel.btn_rematch": "⚔️ Revancha (a las mesas)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 Rango: <b>{rank}</b>\n",
    "rank.rookie": "Novato",
    "rank.fighter": "Luchador",
    "rank.legend": "Leyenda",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.dead": "DEAD",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>PROGRAMA DE REFERIDOS DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "¡Invita a tus amigos y recibe <b>+{bonus} monedas</b> por cada uno "
        "que se registre con tu enlace personal!\n\n"
        "🔗 <b>Tu enlace (toca para copiar):</b>\n<code>{link}</code>\n\n"
        "📊 <b>TUS ESTADÍSTICAS:</b>\n"
        "👥 Amigos invitados: <b>{invited}</b>\n"
        "💰 Ganado con referidos: <b>{earned} monedas</b>\n\n"
        "..................................................\n"
        "<i>Comparte el enlace en los chats de tu clase, con tus amigos y en redes: ¡cuanto más grande sea la banda, más rápido crece tu saldo!</i>"
    ),
    "ref.btn_share": "📣 Compartir el enlace",
    "ref.share_text": "¡Únete al ecosistema de juegos ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Doble recompensa:</b> cuando un amigo invitado juegue {rounds} "
                           "rondas, ¡recibes otras <b>+{bonus} monedas</b>!"),
    "ref.qualified_notify": ("🤝 <b>¡Tu amigo se enganchó: ya lleva {rounds} rondas!</b>\n"
                             "Ganaste <b>+{bonus} monedas</b> por un referido calificado. "
                             "¡Invita a más!"),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>TRANSFERENCIA DE MONEDAS A OTRO JUGADOR</b>\n"
        "..................................................\n\n"
        "Formato del comando:\n"
        "<code>/transfer ID cantidad</code> — por ID de Pasaporte (visible en /profile)\n"
        "<code>/transfer @username cantidad</code> — por nombre de usuario\n"
        "<code>/transfer ROFL-HUB-777 cantidad</code> — por un VIP ID de subasta\n\n"
        "Ejemplos:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Cantidad mínima: <b>{min} monedas</b>"
    ),
    "tr.not_found": "❌ Destinatario no encontrado. Revisa el ID de Pasaporte o el @username: el jugador debe estar registrado en el bot.",
    "tr.self": "🤨 No puedes transferirte monedas a tu propia cuenta. ¡Eso sería dinero infinito!",
    "tr.blocked": "🚫 Este jugador está bloqueado: las transferencias hacia él no están disponibles.",
    "tr.min": "❌ La transferencia mínima es de {min} monedas.",
    "tr.insufficient": "❌ ¡No te alcanzan las monedas! Tu saldo: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ No hay suficientes monedas en tu saldo.",
    "tr.confirm": (
        "🔄 <b>CONFIRMA LA TRANSFERENCIA:</b>\n\n"
        "👤 Destinatario: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Cantidad a descontar: <b>{amount} monedas</b>{fee_line}\n"
        "💰 El destinatario recibe: <b>{received} monedas</b>\n\n"
        "<i>Las transferencias no se pueden deshacer. ¡Revisa bien el destinatario!</i>"
    ),
    "tr.fee_line": "\n🔥 Comisión del hub: <b>{fee} monedas</b> (se quema)",
    "tr.btn_confirm": "✅ CONFIRMAR TRANSFERENCIA",
    "tr.btn_cancel": "❌ Cancelar",
    "tr.cancelled_toast": "Transferencia cancelada",
    "tr.cancelled": "❌ <b>Transferencia cancelada.</b> Tus monedas siguen en su lugar.",
    "tr.not_yours": "🔒 ¡Esta no es tu transferencia!",
    "tr.done_toast": "✅ ¡Transferencia realizada!",
    "tr.done": (
        "✅ <b>¡TRANSFERENCIA REALIZADA!</b>\n\n"
        "💸 Enviado: <b>{amount} monedas</b> al jugador ID <code>{recipient_id}</code>\n"
        "💰 Tu saldo: <b>{balance} monedas</b>"
    ),
    "tr.received": (
        "💰 <b>¡Te transfirieron {amount} monedas!</b>\n"
        "Remitente: ID <code>{sender_id}</code>. Tu saldo ya fue recargado. ¡Revisa /profile!"
    ),

    # ---------------- магазин и платежи ----------------
    "shop.header": "🏪 <b>TIENDA DE ROFL HUB</b>\nLas compras se hacen con Telegram Stars oficiales. Elige una categoría con los botones de abajo.",
    "shop.cat_farm": (
        "🚜 <b>TIENDA · PARA LA GRANJA</b>\n"
        "..................................................\n"
        "Robots por 30 días, combustible, refrigeradores, mejoras y el Dron Maestro.\n"
        "📦 Tu refrigerador actual: <b>{capacity} chuletas</b>\n"
        "..................................................\n"
        "👇 <b>Elige un artículo:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>TIENDA · JUEGOS</b>\n"
        "..................................................\n"
        "Quitar límites de victorias, paquetes de monedas y la licencia de Mega-Clan.\n"
        "..................................................\n"
        "👇 <b>Elige un artículo:</b>"
    ),
    "pay.invoice_desc": "Entrega instantánea de contenido del juego ROFL HUB.",
    "pay.invoice_error": "⚠️ No se pudo generar la factura de Telegram Stars. Inténtalo más tarde.",
    "pay.success": "🎉 <b>¡Pago confirmado!</b>\n🧾 <code>{charge}</code>\n💵 Cobrado: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 El pago se realizó, pero la entrega falló temporalmente. Ya estamos en ello.\n"
        "Guarda el número de pago: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Tus Stars fueron devueltas automáticamente.",
    "pay.keep_charge": "Guarda el número de pago para el reembolso: <code>{charge}</code>",
    "pay.already": "✅ Este pago ya fue procesado; el artículo se entregó antes.",
    "pay.support": (
        "🛟 <b>SOPORTE DE PAGOS DE TELEGRAM STARS</b>\n"
        "..................................................\n\n"
        "Todos los artículos de ROFL HUB son digitales y se entregan al instante tras el pago.\n\n"
        "⚙️ <b>Si pagaste y el artículo no llegó:</b>\n"
        "el bot devuelve las Stars automáticamente cuando la entrega falla. Si eso no ocurrió, "
        "envía aquí el número de pago (está en el recibo, formato <code>xxxx...</code>) y describe el problema. "
        "La administración revisará el pago en la base de datos y resolverá el caso en un plazo de 24 horas.\n\n"
        "💫 <b>Política de reembolsos:</b>\n"
        "el reembolso es posible si el artículo no fue recibido o se entregó con errores. "
        "Los artículos digitales entregados correctamente no admiten reembolso.\n\n"
        "..................................................\n"
        "<i>Esta sección es el punto oficial de soporte de compras según las reglas de Telegram.</i>"
    ),

    # ---------------- доставка ----------------
    "dlv.cutlets": "🥩 Añadidas a tu inventario: <b>{qty} chuletas</b>.",
    "dlv.miner": "🤖 El robot <b>«{name}»</b> fue entregado en tu granja.\n⏳ Vida útil: hasta el <b>{until} UTC</b>.",
    "dlv.miner_junior": "Robot Minero",
    "dlv.miner_premium": "Ciber-Perforador",
    "dlv.fridge": "📦 Refrigerador ampliado a <b>{capacity} chuletas</b>.",
    "dlv.coins": "💰 Acreditadas <b>+{amount} monedas</b>.",
    "dlv.boost_nuclear": "🔋 Impulso Nuclear x5 activo hasta el <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Enfriamiento de Nitrógeno +40% activo hasta el <b>{until} UTC</b>.",
    "dlv.drone": "🛸 El Dron Maestro protege tu granja hasta el <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Límites de victorias quitados hasta el <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Tu equipo recibió el estatus <b>MEGA-CLAN</b>: hasta {max} lugares.",
    "dlv.err_fridge": "Ya tienes un refrigerador de ese tamaño o más grande.",
    "dlv.err_no_team": "Todavía no tienes un equipo creado. Primero créalo con /create_team.",
    "dlv.err_mega": "Tu equipo ya tiene el estatus de Mega-Clan.",
    "dlv.intern_upgrade": "♾ Tu Robot Becario ascendió a <b>Robot Minero ETERNO</b>: ¡5 monedas por hora sin caducidad!",
    "dlv.err_no_intern": "No tienes un Robot Becario activado: actívalo primero en /farm.",
    "dlv.err_intern_refs": "La mejora necesita {need} amigos calificados (30 rondas cada uno); tienes {have}.",
    "mk.header": "📈 <b>BOLSA DE CHULETAS</b>\n..................................................\n\nÓrdenes abiertas: <b>{orders}</b> · chuletas en venta: <b>{cutlets}</b> · mejor precio: <b>{best}</b>\nComisión del hub: <b>{fee}%</b> por venta (se quema — escudo antiinflación)\n🥩 En tu almacén: <b>{inv}</b> chuletas\n\n{body}\n\n<i>Toca una orden para comprar. Para vender usa /sell.</i>",
    "mk.empty": "Aún no hay ofertas. Sé el primero: /sell cantidad precio",
    "mk.order_line": "🥩 #{id} · <b>{qty} uds.</b> a <b>{price}</b> monedas",
    "mk.btn_order": "🛒 #{id}: {qty} uds. a {price} monedas",
    "mk.btn_my": "📋 Mis órdenes",
    "mk.btn_sell_help": "💰 Cómo vender chuletas",
    "mk.btn_refresh": "🔄 Actualizar",
    "mk.btn_back": "← A la bolsa",
    "mk.pick": "🛒 <b>Orden #{id}</b>: {qty} uds. disponibles a {price} monedas.\n¿Cuántas compras?",
    "mk.btn_qty": "{qty} uds. — {total} monedas",
    "mk.btn_qty_all": "Todas, {qty} uds. — {total} monedas",
    "mk.buy_toast": "¡Trato cerrado!",
    "mk.buy_done": "✅ Compraste <b>{qty} chuletas</b> por <b>{total} monedas</b>. Ya están en tu almacén: ¡alimenta a tus Perforadores!",
    "mk.sold_notify": "💰 <b>Bolsa: ¡vendido!</b> Orden #{id}: {qty} uds. a {price}. Recibiste <b>+{got} monedas</b> (comisión de {fee} quemada).",
    "mk.sell_help": "💰 <b>CÓMO VENDER CHULETAS</b>\n\nComando: <code>/sell cantidad precio</code>\nEjemplo: <code>/sell 10 50</code> — 10 chuletas a 50 monedas.\n\nLas chuletas salen del almacén y esperan en la orden (puedes retirarla cuando quieras). Hasta {max_qty} uds. por orden y {max_orders} órdenes abiertas. Al vender se quema una comisión del {fee}%.",
    "mk.sell_confirm": "📝 ¿Poner a la venta <b>{qty} chuletas</b> a <b>{price}</b> monedas?\nTotal: {total} · comisión {fee} se quema · recibirás <b>{got} monedas</b>.",
    "mk.btn_confirm_sell": "✅ PONER EN LA BOLSA",
    "mk.btn_cancel": "❌ Cancelar",
    "mk.sell_toast": "¡Orden publicada!",
    "mk.sell_done": "✅ Orden <b>#{id}</b> publicada: {qty} uds. a {price} monedas. Te avisaré cuando se venda.",
    "mk.cancelled_toast": "Cancelado",
    "mk.cancel_text": "❌ <b>Cancelado.</b> Las chuletas siguen en tu almacén.",
    "mk.my_header": "📋 <b>TUS ÓRDENES</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} uds. a {price} monedas",
    "mk.my_empty": "📋 No tienes órdenes abiertas.",
    "mk.btn_cancel_order": "❌ Retirar orden #{id}",
    "mk.order_cancelled": "↩️ Orden #{id} retirada: <b>{qty} chuletas</b> volvieron a tu almacén.",
    "mk.err_qty": "❌ Cantidad: de 1 a {max} chuletas por orden.",
    "mk.err_price": "❌ Precio: de {min} a {max} monedas por chuleta.",
    "mk.err_no_cutlets": "❌ Solo tienes {have} chuletas en el almacén. Las del frigorífico no se venden — mira /farm.",
    "mk.err_too_many": "❌ Límite: máximo {max} órdenes abiertas. Retira una en «Mis órdenes».",
    "mk.err_not_found": "❌ Esa orden ya está cerrada.",
    "mk.err_own": "🤨 No puedes comprar tu propia orden.",
    "mk.err_insufficient": "❌ Faltan monedas: necesitas {total}.",
    "farm.btn_market": "📈 Bolsa de chuletas",

    # ---------------- ресурсы (волна 22.10, вечер) ----------------
    "res.metal": "Metal",
    "res.hydrogen": "Hidrógeno",
    "res.crystal": "Cristales",
    "res.parts": "Piezas",
    "res.none": "vacío por ahora",
    "games.resource_gain": "{icon} Extraído: <b>+{qty} {name}</b> (total {total}) → /workshop",
    "duel.metal_gain": "⛏ Trofeo del duelo: <b>+{metal} Metal</b> → /workshop",
    "quest.win_resources": "\n📦 Además, un lote de recursos: <b>{qty}</b> de cada uno → /workshop",
    "profile.resources_line": "🧰 Recursos: {stock}\n",
    "menu.btn_goals": "🎯 Metas diarias",
    "menu.btn_raids": "🏴‍☠️ Asaltos",
    "menu.btn_workshop": "🔧 Taller",
    "farm.btn_workshop": "🔧 Taller",
    "farm.boost_armor": "🛡 Ciber-Armadura niv. {level}: +{percent}% de extracción para siempre",
    "farm.boost_station": "🛰 Estación del equipo niv. {level}: +{percent}% de extracción",
    "clan.btn_station": "🛰 Estación del equipo",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>TALLER</b>\n"
        "..................................................\n\n"
        "🧰 Tus recursos: {stock}\n"
        "⛏ Metal — PPT y duelos · 💧 Hidrógeno — Mayor/Menor · "
        "💎 Cristales — Trivia · ⚙️ Piezas — Ciber-Caja Fuerte. Las misiones dan un lote.\n\n"
        "🛡 Ciber-Armadura: <b>nivel {armor}/{armor_max}</b> (+{armor_pct}% de extracción por nivel, para siempre)\n"
        "🚀 Transbordador: <b>{shuttle}</b> — comisión de la bolsa {shuttle_fee}%, hasta {shuttle_qty} chuletas por orden\n\n"
        "<i>✅ — recursos suficientes, 🔒 — todavía no. Un toque y listo.</i>"
    ),
    "ws.shuttle_yes": "construido",
    "ws.shuttle_no": "sin construir",
    "ws.recipe_nitro_6h": "Enfriamiento de Nitrógeno por 6 h",
    "ws.recipe_nuclear_3h": "Impulso Nuclear por 3 h",
    "ws.recipe_drone_24h": "Dron Maestro por 24 h",
    "ws.recipe_shield_24h": "Escudo antiasaltos por 24 h",
    "ws.recipe_cutlet": "Sintetizar una ciber-chuleta",
    "ws.recipe_armor": "Ciber-Armadura niv. {level}",
    "ws.recipe_shuttle": "Construir el Transbordador",
    "ws.btn_shuttle_owned": "🚀 Transbordador construido",
    "ws.btn_armor_max": "🛡 Ciber-Armadura: al máximo",
    "ws.btn_refresh": "🔄 Actualizar",
    "ws.btn_farm": "🚜 A la granja",
    "ws.noop": "Ya está al máximo",
    "ws.toast": "¡Listo!",
    "ws.done_nitrogen": "❄️ <b>Enfriamiento de Nitrógeno +40%</b> activo hasta el {until} UTC.",
    "ws.done_nuclear": "☢️ <b>Impulso Nuclear x5</b> activo hasta el {until} UTC. ¡Los Perforadores comen ×3 chuletas!",
    "ws.done_drone": "🛸 El <b>Dron Maestro</b> cuida a tus robots hasta el {until} UTC.",
    "ws.done_shield": "🛡 El <b>Escudo antiasaltos</b> aguanta hasta el {until} UTC. Tus recursos están protegidos.",
    "ws.done_cutlet": "🥩 Sintetizado: <b>+{qty} ciber-chuleta</b> en tu inventario. ¡Cárgala en /farm!",
    "ws.done_armor": "🛡 <b>¡Ciber-Armadura de nivel {level}!</b> Extracción de la granja: <b>+{percent}%</b> para siempre.",
    "ws.done_shuttle": "🚀 <b>¡Transbordador construido!</b> La comisión de la bolsa ahora es del {fee}% y puedes poner hasta {qty} chuletas por orden. Para siempre.",
    "ws.err_unknown": "❌ Esa receta no existe.",
    "ws.err_resources": "🔒 Falta {kind}: necesitas {need}, tienes {have}. ¡Consíguelo en los juegos!",
    "ws.err_shuttle_owned": "🚀 El Transbordador ya está construido — solo hay uno por jugador.",
    "ws.err_armor_max": "🛡 La armadura ya está en el nivel máximo ({max}).",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>ASALTOS</b>\n"
        "..................................................\n\n"
        "💧 Hidrógeno: <b>{hydrogen}</b> (cada salida cuesta {fuel})\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ Postura de defensa: <b>{stance}</b>\n\n"
        "📊 Asaltos: <b>{attacks}</b> ({attack_wins} con éxito) · defendidos: <b>{holds}/{defenses}</b>\n\n"
        "<i>El botín son solo recursos: el {percent}% de la reserva del objetivo, máximo {cap} por recurso. "
        "Las monedas, los robots y las chuletas son intocables. Tu gesto contra la postura del objetivo: "
        "decisión contra decisión. Una salida cada {cooldown} h; la revancha es gratis.</i>"
    ),
    "raid.ready_line": "Nave lista para despegar",
    "raid.cooldown_line": "Recargando: faltan {minutes} min",
    "raid.shield_on": "Escudo activo hasta el {until} UTC",
    "raid.shield_newbie": "Protección de novato (primeros {days} días)",
    "raid.shield_off": "Sin escudo — constrúyelo en /workshop",
    "raid.stance_random": "aleatoria (¡elígela en el menú!)",
    "raid.btn_scout": "🔭 EXPLORAR: buscar objetivos",
    "raid.btn_revenge": "⚔️ Revancha: {name}",
    "raid.btn_stance": "✊ Postura de defensa",
    "raid.btn_workshop": "🛡 Construir un escudo",
    "raid.btn_refresh": "🔄 Actualizar",
    "raid.btn_back": "← Atrás",
    "raid.btn_open": "🏴‍☠️ Abrir asaltos",
    "raid.btn_again": "🏴‍☠️ A los asaltos",
    "raid.stance_pick": "✊ <b>Postura de defensa</b>\nSolo se revela en el resultado de un asalto ajeno: el gesto del atacante contra tu postura. Cámbiala de vez en cuando — a los predecibles los saquean.",
    "raid.stance_saved": "Postura: {stance}",
    "raid.scout": "🔭 <b>La exploración encontró objetivos.</b> La salida cuesta {fuel} 💧. Elige:",
    "raid.btn_target": "🎯 {name} · recursos ≈{total}",
    "raid.no_targets": "🔭 La exploración no encontró a nadie: ahora mismo no hay objetivos adecuados (escudos, recargas, novatos). Vuelve más tarde.",
    "raid.pick_move": "✊ <b>¿Tu gesto?</b> Jugará contra la postura de defensa del objetivo. Salida: −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>¡Revancha! ¿Tu gesto?</b> La salida es gratis y sin recarga.",
    "raid.result_win": "🏴‍☠️ <b>¡ASALTO EXITOSO!</b>\n{move} contra {stance} de {name}.\nBotín: <b>{loot}</b>",
    "raid.result_draw": "😐 <b>Empate.</b> {move} contra {stance} de {name}. La nave volvió vacía y el combustible se quemó.",
    "raid.result_lose": "💥 <b>LA DEFENSA AGUANTÓ.</b> {move} contra {stance} de {name}.\nEl objetivo se quedó con: <b>{loot}</b>",
    "raid.result_footer": "<i>Los recursos están en /workshop. Un escudo te protege de la respuesta.</i>",
    "raid.victim_lost": "🚨 <b>¡Te han asaltado!</b> {name}: {move} contra tu postura {stance}.\nPerdiste: <b>{loot}</b>\n\n⚔️ Revancha gratis durante {hours} h. El escudo está en /workshop.",
    "raid.victim_draw": "🛡 <b>Asalto rechazado en empate.</b> {name}: {move} contra tu postura {stance}. No perdiste nada.",
    "raid.victim_held": "🛡 <b>¡Tu defensa aguantó!</b> {name}: {move} contra tu postura {stance}.\nTrofeo de defensa: <b>{loot}</b>",
    "raid.err_stance": "❌ Gesto desconocido.",
    "raid.err_self": "🤨 ¿Asaltarte a ti mismo(a)? No.",
    "raid.err_gone": "❌ Objetivo no disponible.",
    "raid.err_teammate": "🤝 A los nuestros no se les roba — es un compañero de equipo.",
    "raid.err_shielded": "🛡 El objetivo tiene escudo. Elige otro.",
    "raid.err_revenge_gone": "❌ La ventana de revancha se cerró.",
    "raid.err_cooldown": "⏳ Recargando: faltan {minutes} min.",
    "raid.err_victim_cooldown": "⏳ A este objetivo ya lo asaltaron hace poco (pausa de {hours} h).",
    "raid.err_fuel": "💧 Falta hidrógeno: necesitas {need}, tienes {have}. Se consigue en Mayor/Menor.",

    # ---------------- ежедневные цели ----------------
    "goal.header": (
        "🎯 <b>METAS DE HOY</b>\n"
        "..................................................\n\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 Cofre: <b>+{coins} monedas</b> y <b>+{res}</b> de un recurso al azar\n"
        "🔥 Racha: <b>{streak}</b> días · cada {every}.º día seguido suma +{bonus} monedas al cofre\n\n"
        "<i>Las metas se renuevan a las 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ Completa las tres y el cofre es tuyo.",
    "goal.status_ready": "✅ <b>¡Todas las metas completadas! Reclama el cofre.</b>",
    "goal.status_claimed": "🎁 El cofre de hoy ya fue reclamado. ¡Mañana habrá metas nuevas!",
    "goal.btn_claim": "🎁 RECLAMAR EL COFRE",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Actualizar",
    "goal.toast": "¡Cofre abierto!",
    "goal.chest": "🎁 <b>¡COFRE ABIERTO!</b>\n💰 +{coins} monedas · {icon} +{qty} {name}\n🔥 Racha: {streak} días",
    "goal.err_claimed": "🎁 Hoy ya lo reclamaste.",
    "goal.err_not_done": "⏳ Todavía no completaste todas las metas.",
    "goal.win_quiz": "Ganar {n} rondas de Trivia",
    "goal.win_rps": "Ganar {n} rondas de PPT",
    "goal.win_hl": "Ganar {n} rondas de Mayor/Menor",
    "goal.win_safe": "Abrir la Ciber-Caja Fuerte {n} veces",
    "goal.play_rounds": "Jugar {n} rondas de cualquier juego",
    "goal.duel": "Jugar un duelo",
    "goal.bonus": "Reclamar la chuleta diaria en la granja",
    "goal.craft": "Construir algo en el taller",
    "goal.raid": "Realizar un asalto",
    "goal.market_deal": "Cerrar un trato en la bolsa",
    "goal.donate": "Aportar recursos a la estación del equipo",

    # ---------------- станция команды ----------------
    "st.header": (
        "🛰 <b>ESTACIÓN DEL EQUIPO «{team}»</b>\n"
        "..................................................\n\n"
        "Nivel: <b>{level}/{max}</b> → cada combatiente recibe <b>+{percent}%</b> de extracción en la granja "
        "(+{per_level}% por nivel)\n\n"
        "📦 Para el siguiente nivel:\n{progress}\n\n"
        "🧾 Últimos aportes:\n{feed}\n\n"
        "🧰 Tus recursos: {stock}\n"
        "<i>La estación es compartida: la construye todo el equipo y el bono lo recibe cada uno. Si sales del equipo, pierdes el bono.</i>"
    ),
    "st.max_level": "🏁 La estación está terminada — ¡nivel máximo!",
    "st.feed_empty": "nadie ha aportado todavía — sé el primero(a)",
    "st.no_team": "🛰 La estación la construye un equipo. Únete a uno o crea el tuyo — y construyan juntos.",
    "st.btn_find_team": "🏆 Equipos y clanes",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ Todo: {qty} {icon} {name}",
    "st.btn_refresh": "🔄 Actualizar",
    "st.btn_team": "🏆 Al equipo",
    "st.toast": "Aportado +{qty} {icon}",
    "st.level_up": "🛰 <b>¡La estación del equipo subió al nivel {level}!</b> Ahora todos los combatientes reciben +{percent}% de extracción en la granja.",
    "st.err_qty": "❌ Cantidad incorrecta.",
    "st.err_no_team": "❌ No estás en un equipo.",
    "st.err_max": "🏁 La estación ya está terminada (nivel {max}).",
    "st.err_resources": "🔒 No te alcanza ese recurso: tienes {have}.",

    # ---------------- команды/кланы (основные поверхности) ----------------
    "clan.no_team": "⚠️ <b>¡Todavía no tienes un equipo creado!</b>\n\nPuedes registrar tu propia banda ahora mismo tocando el botón de abajo.",
    "clan.btn_create": "🏆 Crear Equipo por 100k",
    "clan.btn_members": "👥 LISTA DE COMPAÑEROS",
    "clan.btn_leave": "🚪 Salir del equipo / Dejar la banda",
    "clan.btn_dashboard": "🏆 Panel del equipo",
    "clan.status_clan": "👑 ESTATUS: CLAN DEL IMPERIO",
    "clan.status_team": "👥 ESTATUS: EQUIPO REGULAR",
    "clan.dashboard": (
        "🏆 <b>PANEL INFORMATIVO DE TU EQUIPO</b>\n"
        "..................................................\n\n"
        "📌 Nombre: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Capitán de la banda: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Lema: <i>«{motto}»</i>\n"
        "🔮 Símbolo del emblema: {symbol}\n\n"
        "👥 Integrantes: <b>{members} / {max_members}</b>\n"
        "..................................................\n\n"
        "👇 <b>NAVEGACIÓN:</b>"
    ),
    "clan.members_only": "🔒 ¡La lista de integrantes solo es visible para los miembros de este equipo!",
    "clan.members_gone": "❌ Este equipo ya fue disuelto.",
    "clan.members_header": (
        "👥 <b>PLANTILLA DEL EQUIPO «{name}»</b>\n"
        "🧠 — nivel de inteligencia de juego (solo se entrena en /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
        "📄 Página <b>{page} / {pages}</b> · Combatientes en total: <b>{members}</b>\n"
        "<i>¡Toca el @username de un compañero para escribirle, armar tu propio chat "
        "y llamar a la banda a las competencias de equipos!</i>"
    ),
    "clan.btn_prev": "⬅️ Atrás",
    "clan.btn_next": "Adelante ➡️",
    "clan.join_ok": (
        "🎉 <b>¡FELICIDADES, YA ESTÁS EN EL JUEGO!</b>\n\n¡Te uniste al equipo <b>{name}</b>!\n"
        "📍 ¡Escribe /my_team para revisar la plantilla!"
    ),
    "clan.leave_ok": "🚪 Saliste del equipo <b>{name}</b>. ¡Ahora eres un ave libre!",
}

MINIAPP: dict[str, str] = {
    "subtitle": "tu imperio de juego en una sola pantalla",
    "passport": "📋 PASAPORTE DEL JUGADOR",
    "coins": "monedas",
    "brain": "🧠 Nivel de inteligencia",
    "toNext": "para el nivel {n}: {left} respuestas correctas en la trivia (+{reward} monedas)",
    "farm": "🚜 CIBER-GRANJA",
    "robots": "Robots (mineros / perforadores)",
    "fueled": "Perforadores cargados",
    "speed": "Velocidad de extracción",
    "perHour": "{v} monedas/hora",
    "fridge": "Refrigerador",
    "inv": "Chuletas en inventario",
    "burnout": "Próximo en quemarse",
    "intern": "Robots Becarios (1 moneda/h, eternos)",
    "activateIntern": "🚀 ACTIVAR ROBOT BECARIO",
    "internDone": "🤖 ¡Tu Robot Becario entró en turno!",
    "rank": "🎖 Rango",
    "openFarm": "🏭 ABRIR LA GRANJA",
    "farmScene": "🏭 TU GRANJA",
    "back": "← Atrás",
    "minedVisit": "minado en esta visita",
    "unit_intern": "Robot Becario",
    "unit_junior": "Robot Minero",
    "unit_premium": "Cyber-Perforador",
    "eternal": "eterno",
    "fueledAll": "con combustible",
    "fueledPart": "{a} de {b} con combustible",
    "license": "licencia de 30 días",
    "emptyFarm": "La mina está vacía. ¡Activa tu Robot Becario o consigue robots en la tienda!",
    "madeBy": "¿Quieres un bot así para tu proyecto? Escribe a @mister_telebot",
    "boosts": "Mejoras activas",
    "none": "ninguna",
    "bonusReady": "🎁 RECLAMAR LA CHULETA DIARIA",
    "bonusWait": "⏳ Bono en {h} h {m} min",
    "bonusDone": "🎉 ¡Chuleta añadida!",
    "team": "🏆 MI EQUIPO",
    "clan": "CLAN",
    "teamLabel": "Equipo",
    "captain": "👑 ¡Estás al mando del equipo!",
    "members": "Plantilla",
    "noTeam": "Todavía no tienes equipo. ¡Arma tu banda en el chat del bot!",
    "top": "👑 TOP-100 DE LOS MÁS RICOS DEL ECOSISTEMA",
    "shop": "🏪 TIENDA",
    "shopFarm": "🚜 PARA LA GRANJA",
    "shopGames": "🕹️ JUEGOS",
    "shopHint": "Paga con Telegram Stars oficiales, aquí mismo y en un toque.",
    "paid": "🎉 ¡Pagado! El artículo ya está en tu cuenta.",
    "payFail": "El pago no se completó. Inténtalo de nuevo.",
    "oldClient": "Actualiza Telegram para comprar desde la Mini App o abre la tienda en el chat del bot.",
    "ctaNoRobots": "💤 ¡Tu granja está vacía! Consigue tu primer robot y las monedas caerán las 24 horas.",
    "ctaHungry": "🚨 ¡Los Perforadores tienen hambre ({n} sin combustible) y la extracción está parada!",
    "ctaLowFuel": "⚠️ Quedan menos chuletas que para un día de trabajo de los Perforadores.",
    "ctaShopBtn": "🛒 A la tienda",
    "footer": "El control completo está en el chat del bot: /menu",
    "noProfile": "Perfil no encontrado. ¡Abre el bot y pulsa /start!",
    "blocked": "Cuenta bloqueada por la administración.",
    "error": "No se pudieron cargar los datos. Inténtalo más tarde.",
    "outside": "Abre esta aplicación desde el bot de Telegram de ROFL HUB.",
    "resources": "🧰 Recursos",
    "bonusPct": "Bono permanente de extracción",
    "shuttle": "🚀 Transbordador construido",
    "resHint": "Metal — PPT, hidrógeno — Mayor/Menor, cristales — Trivia, piezas — caja fuerte. Úsalos en el taller, en el chat del bot.",
}

COMMANDS: dict[str, str] = {
    "app": "🎮 Abrir la Mini App",
    "menu": "📱 Menú principal",
    "profile": "👤 Mi perfil y pasaporte",
    "farm": "🚜 Ciber-granja y recarga",
    "shop": "🏪 Tienda (Telegram Stars)",
    "games": "🕹️ Todos los juegos contra el bot",
    "quiz": "🧠 Trivia: 15 segundos por respuesta",
    "duel": "⚔️ Duelo 1 contra 1 con apuesta",
    "quests": "🗺️ Misiones: historias con decisiones",
    "my_team": "🏆 Mi equipo y compañeros",
    "invite": "🤝 Enlace de referido: +1000 por amigo",
    "transfer": "🔄 Enviar monedas a un jugador",
    "market": "📈 Bolsa de chuletas: comprar o vender",
    "sell": "💰 Vender chuletas: /sell cantidad precio",
    "my_stats": "📊 Mis estadísticas",
    "faq": "📚 Preguntas frecuentes",
    "rules": "📜 Acuerdo de usuario",
    "paysupport": "🛟 Soporte de pagos",
    "workshop": "🔧 Taller: recursos en mejoras",
    "raid": "🏴‍☠️ Asaltos: exploración y revancha",
    "goals": "🎯 Metas diarias y cofre",
    "station": "🛰 Estación del equipo: proyecto común",
}
