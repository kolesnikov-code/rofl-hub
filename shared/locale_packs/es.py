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
        "💸 Recibiste: <b>{balance} 🪙</b>\n"
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
        "• /create_team — Registrar tu propio equipo por 100 000 🪙\n"
        "• /my_team — Panel de la banda y la LISTA DE COMPAÑEROS con niveles 🧠\n"
        "• /all_teams — Ruleta de equipos al azar\n\n"
        "💸 <b>DINERO Y AMIGOS:</b>\n"
        "• /invite — Tu enlace de referido: +500 🪙 por amigo activo\n"
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
        "💸 Una victoria paga: <b>+2 🪙</b> (Ciber-Caja Fuerte: <b>+5</b>)\n"
        "💀 Una derrota o un empate cuesta: <b>-1 🪙</b>\n"
        "🧠 La Trivia tiene cronómetro de 15 segundos y niveles de inteligencia: el nivel 1 son 10 respuestas correctas y <b>+100 🪙</b>; "
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
        "⚔️ Duelos con jugadores reales en mesas de 10/100/1000 🪙.\n"
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
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} 🪙 por la primera victoria\n"
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
    "quest.win_first": "\n\n🏆 <b>¡MISIÓN COMPLETADA! Recompensa: +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>¡Completada otra vez!</b> La recompensa de esta misión ya fue reclamada antes.",
    "quest.fail_footer": "\n\n💀 <i>No fue el mejor final... ¡pero siempre puedes rejugar la historia!</i>",
    "quest.stale": "⏳ Esa escena ya quedó atrás. ¡Seguimos desde el punto actual!",
    "quest.no_coins": "❌ La pista cuesta {cost} 🪙 y tu saldo es menor. ¡Pasa por tu granja!",
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
    "farm.status_no_drills": "💡 Consigue un robot más potente en /shop: tu granja extraerá más.",
    "farm.boost_nuclear": "🔋 Impulso Nuclear x5 hasta el {until} UTC (consumo de chuletas ×3)",
    "farm.boost_nitrogen": "❄️ Enfriamiento de Nitrógeno +40% hasta el {until} UTC",
    "farm.boost_drone": "🛸 El Dron Maestro extiende la vida de los robots hasta el {until} UTC",
    "farm.no_boosts": "No hay mejoras activas; date una vuelta por /shop.",
    "farm.burnout": "🔥 Próximo robot en quemarse: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Activar tu Robot Becario (gratis)",
    "farm.intern_activated": "🤖 ¡Tu Robot Becario entró en turno! +1 🪙 por hora para siempre, sin combustible ni caducidad.",
    "farm.intern_already": "🤖 Tu Robot Becario ya está trabajando.",
    "farm.btn_claim_intern": "🎁 Recoger Robot Becario ({n})",
    "farm.intern_pending": "🎁 Por tus niveles de intelecto te esperan Robots Becarios: <b>{n}</b>. ¡Recógelos con el botón de abajo!",
    "farm.intern_claimed_new": "🤖 ¡Un nuevo Robot Becario entró en turno! +1 🪙 por hora para siempre.",
    "farm.intern_none": "🤖 Aún no hay nuevos Becarios: el siguiente te espera en el nivel de intelecto 10, 20, 30…",
    "games.intern_ready": "🎁 Tu nuevo nivel te da un <b>Robot Becario</b>: ¡recógelo en la granja!",

    "farm.intern_line": "• Robots Becarios ({rate} 🪙/h, eternos): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 ¡Tienes un Robot Becario gratis! Pulsa el botón de abajo y minará 1 🪙 por hora para siempre.",
    "farm.dashboard": (
        "🚜 <b>HUB CENTRAL DE COMBUSTIBLE DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Robots activos en la planta: <b>{total}</b>\n"
        "{intern}• Robots Mineros ({junior_rate} 🪙/h): <code>{junior}</code>\n"
        "• Ciber-Perforadores ({premium_rate} 🪙/h): <code>{premium}</code>\n"
        "{burnout}\n"
        "📊 <b>VELOCIDAD ACTUAL DE TU GRANJA:</b>\n"
        "• Producción por hora: <b>+{speed_hour} 🪙</b>\n"
        "• Producción por día: <b>+{speed_day} 🪙</b>\n\n"
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
        "💰 Monedas ahora mismo: <b>{balance} 🪙</b>\n"
        "🏆 Tu estatus: <b>{team}</b>\n"
        "🧠 Nivel de inteligencia: <b>{level}</b> · para el nivel {next_level}: "
        "<b>{left}</b> respuestas correctas en /quiz (recompensa: +{reward} 🪙)\n\n"
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
    "games.win": "🎉 <b>¡VICTORIA!</b> 🎉\nAcreditado: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>¡DERROTA!</b>\nDescontado: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>¡EMPATE!</b>\nDescontado: <b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>¡Límite diario alcanzado!</b>\n\n"
        "Hoy ya te llevaste {limit} victorias en {game}. El límite se reinicia a las 00:00 UTC.\n\n"
        "⚡ Quitar el límite por 24 horas — 5 ★, por 30 días — 99 ★ (sección «Juegos» en /shop)."
    ),
    "games.no_coins": "❌ Tienes 0 🪙 y no puedes pagar la cuota de la ronda. ¡Recoge los ingresos de tu granja en /farm!",
    "games.balance": "💰 Saldo: <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 ¡Jugar otra vez!",
    "games.btn_hub": "🕹️ Zona de juegos",
    "games.level_up": (
        "🏅 <b>¡SUBISTE AL NIVEL DE INTELIGENCIA {level}!</b> ¡Recompensa: <b>+{bonus} 🪙</b>!\n"
        "Siguiente nivel: {next_required} respuestas correctas → +{next_reward} 🪙."
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
    "quiz.lost_line": "💀 ¡<b>-{penalty} 🪙</b> por la derrota!",
    "quiz.level_line": (
        "🧠 Nivel de inteligencia: <b>{level}</b>\n"
        "Victorias restantes para el nivel {next_level}: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>¡{seconds} segundos para responder!\n"
        "Correcta: +{win} 🪙 a tu saldo\n"
        "Error / sin tiempo: -{penalty} 🪙\n"
        "Límite: {limit} victorias al día</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>CIBER-CAJA FUERTE</b>\n\n"
        "¡Adentro hay un botín de <b>{jackpot} 🪙</b>! La puerta está cerrada con un código del 1 al {codes}. "
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
    "duel.btn_table": "⚔️ Mesa de {stake} 🪙",
    "duel.btn_cancel": "❌ Salir y recuperar la apuesta",
    "duel.btn_move_rock": "🪨 Piedra",
    "duel.btn_move_scissors": "✂️ Tijera",
    "duel.btn_move_paper": "🧻 Papel",
    "duel.waiting": (
        "🪑 <b>Estás en la mesa de {stake} 🪙.</b> Tu apuesta ya está en el pozo.\n"
        "Esperando al segundo combatiente... En cuanto se siente, ¡los dos pasarán a elegir su gesto!\n"
        "<i>La cola vive {ttl} minutos; después tu apuesta vuelve automáticamente.</i>"
    ),
    "duel.cancelled": "🚪 Dejaste la mesa. La apuesta de <b>{stake} 🪙</b> volvió a tu saldo.",
    "duel.expired": "⌛ No apareció ningún rival en la mesa de {stake}. La apuesta de <b>{stake} 🪙</b> fue devuelta.",
    "duel.matched": (
        "⚔️ <b>¡RIVAL ENCONTRADO! Mesa de {stake} 🪙.</b>\n"
        "Pozo: <b>{bank} 🪙</b> · El ganador se lleva: <b>{payout}</b>\n\n"
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
        "💰 Ganancia: <b>+{payout} 🪙</b> · 🔥 Quemado del pozo: {burned}\n"
        "💼 Saldo: <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>DUELO PERDIDO.</b>\n\n"
        "El gesto {winner_move} del rival vence a tu {loser_move}.\n"
        "📉 Tu apuesta de <b>{stake} 🪙</b> se fue al pozo del ganador.\n"
        "¿Revancha?"
    ),
    "duel.reaper_prefix": "⏰ <b>¡Tiempo de la ronda agotado!</b> Los gestos que faltaban los eligió el generador aleatorio.\n\n",
    "duel.bad_table": "❌ Esa mesa no existe.",
    "duel.already_in": "⚠️ ¡Ya estás en una mesa o en pleno combate! Termina primero tu duelo actual.",
    "duel.no_coins": "❌ Para esta mesa necesitas {stake} 🪙 en tu saldo.",
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
    "rank.king": "KING",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>PROGRAMA DE REFERIDOS DE ROFL HUB</b>\n"
        "..................................................\n\n"
        "Invita a tus amigos con tu enlace personal y recibe <b>{bonus}</b> "
        "por cada uno que se convierta en jugador activo.\n\n"
        "🔗 <b>Tu enlace (toca para copiar):</b>\n<code>{link}</code>\n\n"
        "📊 <b>TUS ESTADÍSTICAS:</b>\n"
        "👥 Amigos invitados: <b>{invited}</b>\n"
        "💰 Ganado con referidos: <b>{earned} 🪙</b>\n\n"
        "..................................................\n"
        "<i>Comparte el enlace en los chats de tu clase, con tus amigos y en redes: ¡cuanto más grande sea la banda, más rápido crece tu saldo!</i>"
    ),
    "ref.btn_share": "📣 Compartir el enlace",
    "ref.share_text": "¡Únete al ecosistema de juegos ROFL HUB!",
    "ref.qualified_line": ("✅ <b>Amigo activo</b> es quien llega al <b>nivel de intelecto {level}</b> en la trivia "
                           "y recoge <b>{claims} chuletas diarias</b> en la granja. Entonces recibes <b>{bonus}</b>, "
                           "una sola vez por cada amigo. Registrarse sin jugar no da bonus: así es más justo para todos."),
    "ref.qualified_notify": ("🤝 <b>¡Tu amigo ya es un jugador activo!</b>\n"
                             "Nivel de intelecto {level} y {claims} chuletas diarias: listo. Has ganado <b>{bonus}</b>. "
                             "¡Invita a más!"),

    "team.err_len": "❌ ¡El texto debe tener entre 1 y {max} caracteres!",
    "team.err_link": "🚨 ¡Error de seguridad! ¡Los enlaces, nombres de usuario y teléfonos están estrictamente prohibidos!",
    "team.err_badword": "❌ ¡Se han detectado palabras malsonantes! Respeta las normas del hub.",
    "team.err_already": "⚠️ ¡Ya estás en un equipo o clan! Sal primero de él.",
    "team.err_money": "❌ ¡No tienes suficientes monedas! Crear un equipo cuesta {cost} 🪙 y tú tienes {balance} 🪙.",
    "team.err_captain": "⚠️ ¡Ya eres capitán de otro equipo!",
    "team.err_taken": "⚠️ ¡El nombre «{name}» ya está en uso! Inventa uno único.",
    "team.err_gone": "❌ Este equipo ya no existe.",
    "team.err_full": "📦 ¡Este equipo se ha quedado sin plazas!",
    "team.err_not_member": "❌ No estás en ningún equipo.",
    "mk.err_no_team": "🏆 La bolsa del equipo es para miembros de equipos. Únete a un equipo o crea el tuyo.",
    "mk.err_team_only": "🔒 Este lote es solo para miembros del equipo del vendedor.",
    "help.err_qty": "Puedes pedir de 1 a {max} unidades de un recurso.",
    "help.err_open": "Ya tienes una petición abierta: espera la ayuda o retírala.",
    "help.err_not_found": "Esta petición ya está cerrada.",
    "help.err_self": "No puedes cubrir tu propia petición con un regalo 🙂",
    "help.err_limit": "Hoy ya has regalado {max} recursos: el límite se restablece a las 00:00 UTC.",
    "help.err_not_active": "🔒 Puedes regalar recursos desde el nivel de inteligencia {level} y tras recoger {claims} chuletas diarias.",
    "it.err_none": "Este artículo ya no está en el inventario.",

    # ---------------- eliminación de cuenta ----------------
    "profile.btn_delete": "🗑 Eliminar cuenta",
    "acct.warn": (
        "⚠️ <b>ELIMINACIÓN DE CUENTA</b>\n"
        "..................................................\n\n"
        "Junto con la cuenta desaparecerán <b>para siempre</b>:\n"
        "• monedas, chuletas, recursos y todos los robots de la granja;\n"
        "• boosts, Sin Límite y todo lo comprado con Stars: <b>las Stars no se devuelven</b>;\n"
        "• VIP ID, progreso de la Trivia y de las misiones;\n"
        "• tu lugar en el equipo (el cargo de capitán pasará al veterano del equipo).\n"
        "Las órdenes abiertas en la bolsa se cancelan al instante y los artículos vuelven al inventario.\n\n"
        "⏳ Primero la cuenta se congela durante <b>{days} días</b>: en ese tiempo puedes cambiar de idea con un solo botón. "
        "Después, la eliminación es irreversible. Si vuelves más adelante, empezarás desde cero: el bono inicial no se entrega dos veces.\n\n"
        "<i>El botón de eliminar funcionará dentro de {seconds} segundos: léelo con atención.</i>"
    ),
    "acct.btn_keep": "✅ No, conservar mi cuenta",
    "acct.btn_confirm": "🗑 Sí, eliminar mi cuenta",
    "acct.wait": "⏳ Espera {seconds} s más y lee qué se eliminará exactamente.",
    "acct.kept": "👍 ¡Genial, tu cuenta sigue contigo!",
    "acct.scheduled": (
        "🗑 La cuenta está congelada y se eliminará el <b>{date}</b> (UTC).\n"
        "Las órdenes de la bolsa se han cancelado y los artículos han vuelto al inventario.\n\n"
        "Si cambias de idea, pulsa el botón de abajo y todo volverá a estar como antes."
    ),
    "acct.pending_notice": (
        "⏳ La cuenta está congelada y se eliminará el <b>{date}</b> (UTC).\n"
        "¿Quieres seguir en el juego? Pulsa el botón de abajo."
    ),
    "acct.btn_undo": "↩️ Cancelar eliminación",
    "acct.undone": "🎉 Eliminación cancelada: ¡la cuenta vuelve a ser tuya!",
    "acct.purged": "🗑 Tu cuenta de ROFL HUB ha sido eliminada. ¡Gracias por jugar! Si quieres volver, pulsa /start.",
    "acct.deleted_notice": "La cuenta ha sido eliminada. Pulsa /start para empezar de nuevo.",
    "acct.welcome_back": (
        "👋 <b>¡Bienvenido de nuevo!</b>\n"
        "Tu perfil se ha creado otra vez desde cero. El bono inicial se entrega una sola vez, por eso tu saldo es de 0 🪙. "
        "¡La granja, los juegos y la Trivia te esperan!"
    ),
    "tr.err_not_active": (
        "🔒 Puedes enviar monedas después del nivel de inteligencia {level} y de reclamar {claims} chuletas diarias: "
        "así se protege el ecosistema de las cuentas falsas."
    ),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>TRANSFERENCIA DE MONEDAS A OTRO JUGADOR</b>\n"
        "..................................................\n\n"
        "Formato del comando:\n"
        "<code>/transfer ID cantidad</code> — por ID de Pasaporte (visible en /profile)\n"
        "<code>/transfer @username cantidad</code> — por nombre de usuario\n"
        "<code>/transfer ROFL-HUB-777 cantidad</code> — por un VIP ID de subasta\n\n"
        "Ejemplos:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Cantidad mínima: <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ Destinatario no encontrado. Revisa el ID de Pasaporte o el @username: el jugador debe estar registrado en el bot.",
    "tr.self": "🤨 No puedes transferirte monedas a tu propia cuenta. ¡Eso sería dinero infinito!",
    "tr.blocked": "🚫 Este jugador está bloqueado: las transferencias hacia él no están disponibles.",
    "tr.min": "❌ La transferencia mínima es de {min} 🪙.",
    "tr.insufficient": "❌ ¡No te alcanzan las monedas! Tu saldo: <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ No hay suficientes monedas en tu saldo.",
    "tr.confirm": (
        "🔄 <b>CONFIRMA LA TRANSFERENCIA:</b>\n\n"
        "👤 Destinatario: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Cantidad a descontar: <b>{amount} 🪙</b>{fee_line}\n"
        "💰 El destinatario recibe: <b>{received} 🪙</b>\n\n"
        "<i>Las transferencias no se pueden deshacer. ¡Revisa bien el destinatario!</i>"
    ),
    "tr.fee_line": "\n🔥 Comisión del hub: <b>{fee} 🪙</b> (se quema)",
    "tr.btn_confirm": "✅ CONFIRMAR TRANSFERENCIA",
    "tr.btn_cancel": "❌ Cancelar",
    "tr.cancelled_toast": "Transferencia cancelada",
    "tr.cancelled": "❌ <b>Transferencia cancelada.</b> Tus monedas siguen en su lugar.",
    "tr.not_yours": "🔒 ¡Esta no es tu transferencia!",
    "tr.done_toast": "✅ ¡Transferencia realizada!",
    "tr.done": (
        "✅ <b>¡TRANSFERENCIA REALIZADA!</b>\n\n"
        "💸 Enviado: <b>{amount} 🪙</b> al jugador ID <code>{recipient_id}</code>\n"
        "💰 Tu saldo: <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>¡Te transfirieron {amount} 🪙!</b>\n"
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
    "dlv.coins": "💰 Acreditado: <b>+{amount} 🪙</b>.",
    "dlv.boost_nuclear": "🔋 Impulso Nuclear x5 activo hasta el <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Enfriamiento de Nitrógeno +40% activo hasta el <b>{until} UTC</b>.",
    "dlv.drone": "🛸 El Dron Maestro protege tu granja hasta el <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Límites de victorias quitados hasta el <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Tu equipo recibió el estatus <b>MEGA-CLAN</b>: hasta {max} lugares.",
    "dlv.err_fridge": "Ya tienes un refrigerador de ese tamaño o más grande.",
    "dlv.err_no_team": "Todavía no tienes un equipo creado. Primero créalo con /create_team.",
    "dlv.err_mega": "Tu equipo ya tiene el estatus de Mega-Clan.",
    "dlv.intern_upgrade": "♾ Tu Robot Becario ascendió a <b>Robot Minero ETERNO</b>: ¡5 🪙 por hora sin caducidad!",
    "dlv.err_no_intern": "No tienes un Robot Becario activado: actívalo primero en /farm.",
    "dlv.err_intern_refs": "La mejora necesita {need} amigos activos (las condiciones están en /invite); tienes {have}.",
    "mk.header": "📈 <b>BOLSA DE CHULETAS</b>\n..................................................\n\nÓrdenes abiertas: <b>{orders}</b> · chuletas en venta: <b>{cutlets}</b> · mejor precio: <b>{best}</b>\nComisión del hub: <b>{fee}%</b> por venta (se quema — escudo antiinflación)\n🥩 En tu inventario: <b>{inv}</b> chuletas\n\n{body}\n\n<i>Toca una orden para comprar. Para vender usa /sell.</i>",
    "mk.empty": "Aún no hay ofertas. Sé el primero: /sell cantidad precio",
    "mk.order_line": "🥩 #{id} · <b>{qty} uds.</b> a <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} uds. a {price} 🪙",
    "mk.btn_my": "📋 Mis órdenes",
    "mk.btn_sell_help": "💰 Cómo vender chuletas",
    "mk.btn_refresh": "🔄 Actualizar",
    "mk.btn_back": "← A la bolsa",
    "mk.pick": "🛒 <b>Orden #{id}</b>: {qty} uds. disponibles a {price} 🪙.\n¿Cuántas compras?",
    "mk.btn_qty": "{qty} uds. — {total} 🪙",
    "mk.btn_qty_all": "Todas, {qty} uds. — {total} 🪙",
    "mk.buy_toast": "¡Trato cerrado!",
    "mk.buy_done": "✅ Compraste <b>{qty} chuletas</b> por <b>{total} 🪙</b>. Ya están en tu inventario: ¡alimenta a tus Perforadores!",
    "mk.sold_notify": "💰 <b>Bolsa: ¡vendido!</b> Orden #{id}: {qty} uds. a {price}. Recibiste <b>+{got} 🪙</b> (comisión de {fee} quemada).",
    "mk.sell_help": "💰 <b>CÓMO VENDER CHULETAS</b>\n\nComando: <code>/sell cantidad precio</code>\nEjemplo: <code>/sell 10 250</code> — 10 chuletas a 250 🪙.\n\nLas chuletas salen del inventario y esperan en la orden (puedes retirarla cuando quieras). Hasta {max_qty} uds. por orden y {max_orders} órdenes abiertas. Al vender se quema una comisión del {fee}%. Una chuleta no puede valer menos de {min} 🪙: el combustible de la tienda por Estrellas siempre sale más a cuenta que la bolsa. Recursos, órdenes de compra e intercambios: en la app del juego.",
    "mk.sell_confirm": "📝 ¿Poner a la venta <b>{qty} chuletas</b> a <b>{price}</b> 🪙?\nTotal: {total} · comisión {fee} se quema · recibirás <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ PONER EN LA BOLSA",
    "mk.btn_cancel": "❌ Cancelar",
    "mk.sell_toast": "¡Orden publicada!",
    "mk.sell_done": "✅ Orden <b>#{id}</b> publicada: {qty} uds. a {price} 🪙. Te avisaré cuando se venda.",
    "mk.cancelled_toast": "Cancelado",
    "mk.cancel_text": "❌ <b>Cancelado.</b> Las chuletas siguen en tu inventario.",
    "mk.my_header": "📋 <b>TUS ÓRDENES</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} uds. a {price} 🪙",
    "mk.my_empty": "📋 No tienes órdenes abiertas.",
    "mk.btn_cancel_order": "❌ Retirar orden #{id}",
    "mk.order_cancelled": "↩️ Orden #{id} retirada: <b>{qty} chuletas</b> volvieron a tu inventario.",
    "mk.err_qty": "❌ Cantidad: de 1 a {max} uds. por orden.",
    "mk.err_price": "❌ Precio: de {min} a {max} 🪙 por unidad.",
    "mk.err_no_cutlets": "❌ Solo tienes {have} chuletas en el inventario. Las del refrigerador no se venden — mira /farm.",
    "mk.err_too_many": "❌ Límite: máximo {max} órdenes abiertas. Retira una en «Mis órdenes».",
    "mk.err_not_found": "❌ Esa orden ya está cerrada.",
    "mk.err_own": "🤨 No puedes comprar tu propia orden.",
    "mk.err_insufficient": "❌ No te alcanza: necesitas {total} 🪙.",
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
    "farm.btn_app": "🏭 Granja en la app",
    "menu.btn_app": "🚀 App del juego: granja, taller, asaltos",
    "app.btn_section": "🚀 ABRIR EN LA APP",
    "app.goto_workshop": "🔧 El <b>Taller</b> vive en la app del juego: recursos, recetas y fabricación con un toque.",
    "app.goto_raids": "🏴\u200d☠️ Los <b>Asaltos</b> viven en la app del juego: exploración, postura de defensa y revancha.",
    "app.goto_station": "🛰 La <b>Estación del equipo</b> vive en la app del juego: progreso, aportes y un bono para todo el equipo.",
    "app.goto_market": "📈 La <b>Bolsa de chuletas</b> es más cómoda en la app del juego: ofertas, ventas y tus órdenes en una sola pantalla.",
    "mk.err_asset": "❌ Ese artículo no está en la bolsa.",
    "mk.err_no_resource": "❌ No te alcanza ese recurso: solo tienes {have} en el inventario.",
    "mk.bid_filled_notify": "🙋 <b>Bolsa: ¡orden de compra ejecutada!</b> Orden #{id}: compraste <b>+{qty} {icon}</b> a {price} 🪙.",
    "sw.err_same": "❌ No puedes intercambiar un recurso por el mismo.",
    "sw.err_qty": "❌ En el intercambio indica una cantidad de 1 a {max}, tanto de lo que das como de lo que quieres recibir.",
    "shop.btn_info": "ℹ️ Qué da cada artículo",
    "sw.done_notify": "🔄 <b>¡Intercambio #{id} realizado!</b> Entregado: {give}, recibido: {want}.",
    "ws.err_coins": "🔒 No te alcanzan las monedas: necesitas {need} 🪙 y tienes {have} 🪙.",
    "wk.eff_nitrogen": "❄️ Nitrógeno +40% por {h} h",
    "wk.eff_nuclear": "☢️ Nuclear x5 por {h} h",
    "wk.eff_drone": "🛸 Dron Maestro por {h} h",
    "wk.eff_shield": "🛡 Escudo por {h} h",
    "wk.eff_unlimit": "⚡ Juegos Sin Límite por {h} h",
    "wk.eff_cutlet": "🥩 Chuleta ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ Esta receta de la semana ya no está disponible.",
    "wk.err_limit": "🔒 Se agotó el límite semanal de esta receta ({limit}). La nueva semana empieza el lunes a las 00:00 UTC.",
    "games.resource_full": "📦 El inventario de {icon} está lleno ({cap}): lo que sobra se pierde. Gasta, vende o amplía el inventario en el taller.",
    "mk.err_storage_full": "📦 No hay espacio suficiente en el inventario: quedan {free} libres. Amplía el inventario en el taller.",
    "mk.err_buyer_full": "📦 El inventario del comprador está lleno: el trato no se puede hacer ahora (quedan {free} libres).",
    "ws.recipe_storage": "Ampliar el inventario a {cap}",
    "ws.done_storage": "📦 <b>Inventario ampliado:</b> hasta {cap} de cada recurso. Para siempre.",
    "ws.err_storage_max": "📦 El inventario ya tiene el tamaño máximo.",
    "farm.boost_armor": "🛡 Ciber-Armadura niv. {level}: +{percent}% de extracción hasta el {until} UTC",
    "farm.boost_station": "🛰 Estación del equipo niv. {level}: +{percent}% de extracción",
    "clan.btn_station": "🛰 Estación del equipo",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>TALLER</b>\n"
        "..................................................\n\n"
        "🧰 Tus recursos: {stock}\n"
        "⛏ Metal — PPT y duelos · 💧 Hidrógeno — Mayor/Menor · "
        "💎 Cristales — Trivia · ⚙️ Piezas — Ciber-Caja Fuerte. Las misiones dan un lote.\n\n"
        "🛡 Ciber-Armadura: <b>nivel {armor}/{armor_max}</b> (+{armor_pct}% de extracción por nivel, por 30 días)\n"
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
    "ws.done_armor": "🛡 <b>¡Ciber-Armadura de nivel {level}!</b> Extracción de la granja: <b>+{percent}%</b> por 30 días.",
    "ws.done_shuttle": "🚀 <b>¡Transbordador construido!</b> La comisión de tus ventas ahora es del {fee}% y puedes poner hasta {qty} chuletas por orden. El Transbordador es solo tuyo y para siempre.",
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
        "🎁 Cofre: <b>+{coins} 🪙</b> y <b>+{res}</b> de un recurso al azar\n"
        "🔥 Racha: <b>{streak}</b> días · cada {every}.º día seguido suma +{bonus} 🪙 al cofre\n\n"
        "<i>Las metas se renuevan a las 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ Completa las tres y el cofre es tuyo.",
    "goal.status_ready": "✅ <b>¡Todas las metas completadas! Reclama el cofre.</b>",
    "goal.status_claimed": "🎁 El cofre de hoy ya fue reclamado. ¡Mañana habrá metas nuevas!",
    "goal.btn_claim": "🎁 RECLAMAR EL COFRE",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Actualizar",
    "goal.toast": "¡Cofre abierto!",
    "goal.chest": "🎁 <b>¡COFRE ABIERTO!</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 Racha: {streak} días",
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
    "tab_passport": "📋 Pasaporte",
    "tab_farm": "🚜 Granja",
    "tab_goals": "🎯 Metas",
    "tab_workshop": "🔧 Taller",
    "tab_raids": "🏴‍☠️ Asaltos",
    "tab_market": "📈 Bolsa",
    "tab_team": "🏆 Equipo",
    "tab_friends": "🤝 Amigos",
    "tab_shop": "🏪 Tienda",
    "tab_top": "👑 TOP",
    "passport": "📋 PASAPORTE DEL JUGADOR",
    "coins": "🪙",
    "brain": "🧠 Nivel de inteligencia",
    "toNext": "para el nivel {n}: {left} respuestas correctas en la trivia (+{reward} 🪙)",
    "farm": "🚜 CIBER-GRANJA",
    "robots": "Robots (mineros / perforadores)",
    "intern": "Robots Becarios (1 🪙/h, eternos)",
    "activateIntern": "🚀 ACTIVAR ROBOT BECARIO",
    "claimIntern": "🎁 RECOGER BECARIO ({n})",
    "internDone": "🤖 ¡Tu Robot Becario entró en turno!",
    "rank": "🎖 Rango",
    "openFarm": "🏭 ABRIR LA MINA",
    "farmScene": "🏭 TU GRANJA",
    "back": "← Atrás",
    "minedVisit": "extraído en esta visita",
    "unit_intern": "Robot Becario",
    "unit_junior": "Robot Minero",
    "unit_premium": "Ciber-Perforador",
    "eternal": "eterno",
    "fueledAll": "con combustible",
    "fueledPart": "{a} de {b} con combustible",
    "license": "licencia de 30 días",
    "emptyFarm": "La mina está vacía. ¡Activa tu Robot Becario o consigue robots en la tienda!",
    "madeBy": "¿Quieres un bot así para tu proyecto? Escribe a @mister_telebot",
    "fueled": "Perforadores cargados",
    "speed": "Velocidad de extracción",
    "perHour": "{v} 🪙/h",
    "fridge": "Refrigerador",
    "inv": "Chuletas en inventario",
    "burnout": "Próximo en quemarse",
    "boosts": "Mejoras activas",
    "none": "ninguna",
    "resources": "🧰 Recursos",
    "bonusPct": "Bono permanente de extracción",
    "shuttle": "🚀 Transbordador construido",
    "resHint": "Cada victoria trae el recurso de su juego; con Sin Límite, sin restricciones. Gástalos en el taller.",
    "bonusReady": "🎁 RECLAMAR LA CHULETA DIARIA",
    "bonusWait": "⏳ Bono en {h} h {m} min",
    "bonusDone": "🎉 ¡Chuleta añadida!",
    "team": "🏆 MI EQUIPO",
    "clan": "CLAN",
    "teamLabel": "Equipo",
    "captain": "👑 ¡Estás al mando del equipo!",
    "members": "Plantilla",
    "noTeam": "Todavía no tienes equipo: únete a uno desde la ruleta o la búsqueda, o crea el tuyo.",
    "tab_faq": "📚 FAQ",
    "tab_rules": "📜 Acuerdo",
    "tm_roulette": "🎲 RULETA DE EQUIPOS",
    "tm_rotate": "🔄 Mostrar otros equipos",
    "tm_noFree": "Aún no hay equipos libres: ¡crea el tuyo!",
    "tm_search": "🔍 BUSCAR EQUIPO",
    "tm_searchPh": "Nombre o parte de él",
    "tm_searchBtn": "Buscar",
    "tm_notFound": "No hay equipos con ese nombre",
    "tm_join": "💥 Unirse",
    "tm_joined": "¡Ya estás en «{n}»!",
    "tm_create": "🏆 CREAR EQUIPO",
    "tm_hubHint": "Un equipo de hasta 50 combatientes cuesta {cost} 🪙. En la tienda puedes mejorarlo a Mega-Clan de 1000 plazas.",
    "tm_name": "Nombre (hasta {n} caracteres)",
    "tm_motto": "Lema (hasta {n} caracteres)",
    "tm_symbol": "Emblema: un emoji (hasta {n} caracteres)",
    "tm_createBtn": "Crear por {cost} 🪙",
    "tm_created": "¡Equipo «{n}» creado: eres el capitán!",
    "tm_noMoney": "Necesitas {cost} 🪙 y tienes {b} 🪙",
    "tm_roster": "👥 PLANTILLA DEL EQUIPO",
    "tm_mottoL": "💬 Lema",
    "tm_leave": "🚪 Salir del equipo",
    "tm_leaveAsk": "¿Seguro que quieres salir del equipo «{n}»?",
    "tm_leaveAskCaptain": "Eres el capitán: la corona pasará al veterano del equipo. ¿Seguro que quieres salir de «{n}»?",
    "tm_left": "Ya no estás en ningún equipo",
    "mk_scopePublic": "🌐 Bolsa general", "mk_scopeTeam": "🏆 Bolsa del equipo",
    "mk_teamHint": "Bolsa del equipo «{t}»: solo tus compañeros ven y compran estos lotes, la comisión es de solo {f}%.",
    "mk_yourStock": "📦 Tienes", "mk_yourCoins": "💰 Tus monedas",
    "tm_market": "🏪 BOLSA DEL EQUIPO", "tm_marketBtn": "Abrir la bolsa del equipo",
    "tm_marketHint": "Comercia con tus compañeros: comisión del {f}% en lugar del {p}% de la bolsa general. En un Mega-Clan, solo {c}%.",
    "hp_title": "🤝 AYUDA MUTUA", "hp_hint": "¿Te falta un recurso? Pídeselo al equipo. Cada miembro puede regalar hasta {d} recursos al día.",
    "hp_today": "Has regalado hoy: {g} / {d}", "hp_empty": "Nadie ha pedido ayuda todavía",
    "hp_give": "🎁 +{n}", "hp_kind": "Qué necesitas", "hp_qty": "Cuántos (hasta {n})", "hp_ask": "🙏 Pedir ayuda",
    "hp_given": "Regalado: {q} {k}. ¡Gracias por jugar en equipo!", "hp_asked": "¡Petición enviada al equipo!",
    "tab_storage": "📦 Inventario",
    "raid_noFuel": "⛽ La nave no está lista para despegar: necesita combustible",
    "raid_shieldTitle": "🛡 ESCUDO DE ASALTOS", "raid_shieldActive": "ACTIVO", "raid_shieldInactive": "INACTIVO",
    "raid_shieldHint": "Mientras el escudo esté activo, nadie te asalta. Se fabrica en el taller y va al inventario: actívalo cuando lo necesites.",
    "raid_toStorage": "📦 Abrir inventario",
    "sk_res": "📦 RECURSOS EN EL INVENTARIO", "sk_expand": "🔧 Ampliar inventario",
    "sk_cutlets": "🥩 CIBER-CHULETAS", "sk_cutletsHint": "Combustible para los Ciber-Perforadores: 1 chuleta = un día de trabajo.",
    "sk_refuel": "🚜 Repostar en la granja",
    "it_nitrogen": "ENFRIAMIENTO DE NITRÓGENO +40%", "it_nuclear": "IMPULSO NUCLEAR X5", "it_drone": "DRON MAESTRO",
    "it_shield": "ESCUDO DE ASALTOS", "it_unlimit": "JUEGOS SIN LÍMITE", "it_unlimitDesc": "victorias en los juegos sin límite diario",
    "it_hours": "{h} h", "it_use": "Activar", "it_empty": "Vacío. Fabrícalo en el taller: el artículo aparecerá aquí.",
    "it_toWorkshop": "🔧 Al taller", "it_active": "✅ Activo hasta el {t}", "it_used": "✅ ¡Activado! Activo hasta el {t}",
    "it_stored": "📦 ¡Listo! El artículo está en el inventario: actívalo en la pestaña «Inventario» cuando lo necesites.",
    "sk_shuttle": "🚀 TRANSBORDADOR", "sk_shuttleOn": "Lo tienes: comisión de la bolsa {f}%, límites de órdenes más amplios.", "sk_shuttleOff": "Aún no. Se fabrica en el taller.",
    "sk_armor": "🦾 CIBER-ARMADURA", "sk_armorOn": "Nivel {l} de {m}: +{p}% de extracción hasta el {t}.",
    "sk_armorOff": "Sin equipar. Cada nivel da +{p}% de extracción durante 30 días.",
    "sk_store": "🏗 AMPLIACIÓN DEL INVENTARIO", "sk_storeLvl": "Capacidad: {c} de cada recurso.", "sk_storeMax": "🏆 ¡Inventario al máximo!",
    "hp_who": "Pueden regalar los jugadores desde el nivel de inteligencia {l} con {c} chuletas diarias recogidas.",
    "top": "👑 TOP-100 DE LOS MÁS RICOS DEL ECOSISTEMA",
    "shop": "🏪 TIENDA",
    "shopFarm": "🚜 PARA LA GRANJA",
    "shopGames": "🕹️ JUEGOS",
    "shopHint": "Paga con Telegram Stars oficiales, aquí mismo y en un toque.",
    "paid": "🎉 ¡Pagado! El artículo ya está en tu cuenta.",
    "payFail": "El pago no se completó. Inténtalo de nuevo.",
    "oldClient": "Actualiza Telegram para comprar desde la app o abre la tienda en el chat del bot.",
    "ctaNoRobots": "💤 ¡Tu granja está casi vacía! Consigue un robot más potente y las 🪙 caerán las 24 horas.",
    "ctaHungry": "🚨 ¡Los Perforadores tienen hambre ({n} sin combustible) y la extracción está parada!",
    "ctaLowFuel": "⚠️ Quedan menos chuletas que para un día de trabajo de los Perforadores.",
    "ctaShopBtn": "🛒 A la tienda",
    "footer": "Los juegos y la trivia están en el chat del bot",
    "noProfile": "Perfil no encontrado. ¡Abre el bot y pulsa /start!",
    "blocked": "Cuenta bloqueada por la administración.",
    "deleting": "Tu cuenta está en cola de eliminación. ¿Cambiaste de idea? Cancélala en el chat del bot.",
    "error": "No se pudieron cargar los datos. Inténtalo más tarde.",
    "outside": "Abre esta aplicación desde el bot de Telegram de ROFL HUB.",
    "robotsTitle": "🤖 TUS ROBOTS",
    "buyMore": "🛒 Comprar",
    "rateShort": "{v} 🪙/h",
    "refuelOne": "🥩 Cargar 1",
    "refuelAll": "⚡ Cargar todas",
    "refueled": "Cargadas: {n} 🥩",
    "res_metal_src": "PPT y duelos",
    "res_hydrogen_src": "Mayor/Menor",
    "res_crystal_src": "Trivia",
    "res_parts_src": "Ciber-Caja Fuerte",
    "resWhere": "dónde conseguirlos",
    "ws_title": "🔧 TALLER",
    "ws_hint": "Los recursos de los juegos se convierten en mejoras. Si te alcanzan, pulsa «Fabricar».",
    "ws_craft": "Fabricar",
    "ws_owned": "✅ Ya lo tienes",
    "ws_crafted": "¡Listo! La mejora ya está funcionando.",
    "ws_armor": "🛡 Ciber-Armadura",
    "ws_armorLvl": "nivel {l}/{m} · +{p}% por nivel durante 30 días",
    "ws_shuttleOn": "🚀 Transbordador construido: comisión de la bolsa {fee}%",
    "ws_shuttleOff": "🚀 Sin Transbordador: comisión de la bolsa {fee}%",
    "eff_nitrogen": "+40% de extracción para todos los robots",
    "eff_nuclear": "×5 de extracción, los Perforadores comen ×3 chuletas",
    "eff_drone": "los robots no envejecen",
    "eff_shield": "nadie puede asaltarte",
    "eff_cutlet": "1 ciber-chuleta a tu inventario (caro: el combustible sale más barato en la tienda)",
    "eff_armor": "+10% de extracción por nivel durante 30 días",
    "eff_shuttle": "solo tuyo: comisión del 5% en tus ventas y órdenes de hasta 500 chuletas, para siempre",
    "eff_storage": "más espacio para recursos, para siempre",
    "ref_title": "🤝 INVITA A TUS AMIGOS",
    "ref_rules": "{q} por cada amigo activo, una sola vez. Un amigo activo ha llegado al nivel de intelecto {l} y ha recogido {c} chuletas diarias.",
    "ref_copy": "📋 Copiar",
    "ref_copied": "¡Enlace copiado!",
    "ref_share": "📤 Compartir",
    "ref_stats": "📊 TU RED",
    "ref_invited": "invitados",
    "ref_qualified": "activos",
    "ref_earned": "ganado",
    "ref_top": "🏆 QUIÉN TIENE MÁS AMIGOS",
    "ref_topHint": "✅ — amigos activos, 👥 — todos los invitados",
    "ref_empty": "El ranking aún está vacío: ¡sé quien lo estrene!",
    "wk_title": "🔥 RECETAS DE LA SEMANA",
    "wk_hint": "Recetas temporales: aparecen cuando el hub lo decide y luego desaparecen. ¡Fabrícalas a tiempo!",
    "wk_left": "fabricaciones restantes esta semana: {n} de {m}",
    "st_cap": "📦 Inventario: hasta {c} de cada recurso; lo que sobra de la extracción se pierde",
    "raid_title": "🏴‍☠️ ASALTOS",
    "raid_how": "📖 Cómo funciona",
    "raid_rule1": "Tú eliges un gesto; el objetivo tiene una postura de defensa fijada de antemano. Decide piedra-papel-tijera: es un duelo de decisiones, no una lotería.",
    "raid_rule2": "Victoria: te llevas el {pct}% de cada recurso del objetivo, hasta {cap} por recurso. Fracaso: le das al objetivo el {fpct}% de los tuyos, hasta {fcap}. Empate: el combustible se quemó.",
    "raid_rule3": "Solo se pueden saquear recursos. Las monedas, los robots y las chuletas están totalmente a salvo. Los novatos están protegidos {days} días y a los compañeros no se les puede asaltar.",
    "raid_rule4": "Cada salida cuesta {fuel} 💧 de hidrógeno y la siguiente es en {cd} h. Si alguien te asalta, la revancha es gratis durante {rh} h.",
    "raid_fuel": "💧 Hidrógeno",
    "raid_ready": "🚀 Nave lista para despegar",
    "raid_cooldown": "⏳ Recargando: {m} min",
    "raid_shieldOn": "🛡 Escudo hasta {t}",
    "raid_shieldNewbie": "🛡 Protección de novato",
    "raid_shieldOff": "🛡 Sin escudo: fabrica uno en el taller",
    "raid_stance": "✊ TU POSTURA DE DEFENSA",
    "raid_stanceHint": "Con ella recibes los asaltos ajenos. Cámbiala de vez en cuando: a quien es predecible lo saquean más.",
    "raid_stanceNone": "Sin postura elegida: será al azar",
    "raid_stanceSaved": "Postura guardada",
    "raid_stats": "Asaltos: {a} ({w} con éxito) · defendidos: {h} de {d}",
    "raid_scout": "🔭 EXPLORACIÓN: buscar objetivos",
    "raid_targets": "🎯 Elige un objetivo",
    "raid_res": "recursos ≈{n}",
    "raid_noTargets": "Ahora no hay objetivos disponibles: escudos, recargas, novatos. Vuelve más tarde.",
    "raid_pickMove": "✊ Tu gesto contra la postura de {name}",
    "raid_revenge": "⚔️ REVANCHA",
    "raid_revengeBtn": "⚔️ Responder: {name}",
    "raid_win": "🏴‍☠️ ¡Asalto exitoso!",
    "raid_draw": "😐 Empate: la nave volvió vacía",
    "raid_lose": "💥 La defensa resistió",
    "raid_vs": "{m} contra {s}",
    "raid_loot": "Botín: {l}",
    "raid_lost": "Entregado al objetivo: {l}",
    "rock": "🪨 Piedra",
    "scissors": "✂️ Tijera",
    "paper": "📄 Papel",
    "mk_title": "📈 BOLSA",
    "mk_stats": "Órdenes: {o} · chuletas: {c} · mejor precio: {b} 🪙",
    "mk_feeLine": "La comisión del {f}% por venta se quema: escudo contra la inflación",
    "mk_inv": "🥩 En tu inventario: {n}",
    "mk_offers": "🛒 OFERTAS",
    "mk_empty": "Todavía no hay ofertas: ¡publica la primera!",
    "mk_offer": "{q} 🥩 × {p} 🪙",
    "mk_buyHow": "¿Cuántas compras?",
    "mk_all": "Todas, {q}",
    "mk_sellTitle": "💰 VENDER CHULETAS",
    "mk_qty": "Cuántas chuletas",
    "mk_price": "Precio por unidad, 🪙",
    "mk_preview": "Total {t} 🪙 · recibirás {g} 🪙 · se queman {f} 🪙",
    "mk_sell": "Publicar en la bolsa",
    "mk_limits": "Hasta {q} chuletas por orden y {o} órdenes abiertas",
    "mk_my": "📋 MIS ÓRDENES",
    "mk_cancel": "Retirar",
    "mk_bought": "Compraste {q} 🥩 por {t} 🪙",
    "mk_listed": "¡Orden publicada! Te escribiré cuando se venda.",
    "mk_cancelledMsg": "Orden retirada, las chuletas volvieron a tu inventario",
    "st_title": "🛰 ESTACIÓN DEL EQUIPO",
    "st_level": "Nivel {l} de {m}",
    "st_bonus": "+{p}% de extracción para cada combatiente",
    "st_next": "El nivel {n} requiere {c} de cada recurso",
    "st_max": "🏁 ¡La estación está terminada!",
    "st_feed": "🧾 Últimos aportes",
    "st_feedEmpty": "Nadie ha aportado todavía: ¡sé quien empiece!",
    "st_donate": "Aportar",
    "st_all": "Todo",
    "st_done": "¡Aportado!",
    "st_hint": "La construye todo el equipo y el bono es para cada integrante. Si dejas el equipo, pierdes el bono.",
    "st_off": "La estación está en mantenimiento temporalmente",
    "goals_title": "🎯 METAS DE HOY",
    "goals_chest": "🎁 Cofre por las tres: +{c} 🪙 y +{r} de un recurso al azar",
    "goals_streak": "🔥 Racha: {s} días · cada {e}.º día seguido +{b} 🪙",
    "goals_claim": "🎁 RECLAMAR EL COFRE",
    "goals_claimed": "🎁 El cofre de hoy ya fue reclamado. ¡Mañana, nuevas metas!",
    "goals_reset": "Las metas se renuevan a las 00:00 UTC",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · racha de {s} días",
    "as_cutlet": "Chuletas",
    "as_metal": "Metal",
    "as_hydrogen": "Hidrógeno",
    "as_crystal": "Cristales",
    "as_parts": "Piezas",
    "mk_index": "📈 ÍNDICE DE LA BOLSA",
    "mk_chart": "📊 PRECIO EN 7 DÍAS",
    "mk_noTrades": "Aún no hay tratos: ¡estrena la bolsa!",
    "mk_avg": "Precio medio semanal: {p} 🪙 · vendido: {v}",
    "mk_asks": "🛒 VENDEN",
    "mk_bids": "🙋 COMPRAN",
    "mk_noBids": "Aún no hay órdenes de compra",
    "mk_sellTo": "Vender",
    "mk_sellHow": "¿Cuántas vendes?",
    "mk_bidTitle": "🙋 ORDEN DE COMPRA",
    "mk_bidHint": "Las monedas quedan congeladas en la orden hasta el trato. Si la retiras, las monedas vuelven.",
    "mk_bid": "Publicar orden de compra",
    "mk_bidPreview": "Se congelarán {t} 🪙",
    "mk_have": "Tienes: {n}",
    "mk_floor": "Una chuleta no puede valer menos de {p} 🪙: el combustible de la tienda por Estrellas siempre sale más a cuenta",
    "mk_side_sell": "vendo",
    "mk_side_buy": "compro",
    "mk_listedBid": "¡Orden de compra publicada! Las monedas quedan congeladas hasta el trato.",
    "mk_sold": "Vendiste {q} y recibiste {g} 🪙 tras la comisión",
    "mk_shuttleNote": "🚀 Tu Transbordador: comisión del {f}% en tus ventas",
    "sw_title": "🔄 INTERCAMBIO DE RECURSOS",
    "sw_hint": "Da lo que te sobra y recibe lo que necesitas. Sin monedas y sin comisión.",
    "sw_give": "Tú das",
    "sw_want": "Quieres recibir",
    "sw_qty": "Cuánto",
    "sw_create": "Proponer intercambio",
    "sw_take": "Intercambiar",
    "shop_info": "ℹ️ Qué da cada artículo",
    "sw_youGet": "Recibes",
    "sw_youGive": "A cambio das",
    "sw_takeBtn": "Intercambiar: dar {x}",
    "sw_mineLine": "Das {g} → quieres {w}",
    "sw_qtyErr": "Indica una cantidad mayor que cero en ambos campos",
    "sw_empty": "Aún no hay propuestas de intercambio",
    "sw_mine": "Mis propuestas",
    "sw_done": "¡Intercambio realizado!",
    "sw_created": "Propuesta publicada, recursos reservados",
    "sw_cancelled": "Propuesta retirada, los recursos volvieron",
    "ws_armorUntil": "🛡 Armadura activa hasta el {t}",
    "featureOff": "⚙️ Sección en mantenimiento",
    "done": "¡Listo!",
    "loading": "⏳ Cargando…",
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
    "invite": "🤝 Enlace de referido: +500 por amigo activo",
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
