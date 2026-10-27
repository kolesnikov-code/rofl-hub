"""Polska lokalizacja ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> monety
# Младший Майнер -> Młodszy Górnik
# Кибер-Бурильщик -> Cyber-Wiertacz
# кибер-котлета -> cyber-kotlet (кратко: kotlet)
# Холодильник -> Lodówka
# склад -> magazyn
# ферма -> farma
# Ядерный Разгон x5 -> Nuklearne Przyspieszenie x5
# Азотное Охлаждение +40% -> Azotowe Chłodzenie +40%
# Мастер-дрон -> Mistrzowski Dron
# Кибер-Сейф -> Cyber-Sejf
# Мега-Клан -> Mega-Klan
# Безлимит -> zdjęcie limitów (bez limitu)
# дуэли -> pojedynki
# битвы -> bitwy
# квесты -> questy
# уровень интеллекта -> poziom intelektu
# команда/банда -> drużyna/ekipa; бусты -> wzmocnienia
# ресурсы -> surowce: Металл -> Metal, Водород -> Wodór, Кристаллы -> Kryształy, Детали -> Części
# Мастерская -> Warsztat; Кибер-броня -> Cyber-pancerz; Шаттл -> Wahadłowiec
# Налёт -> Najazd; Стойка обороны -> Postawa obronna; Разведка -> Zwiad; Реванш -> Rewanż
# Щит -> Tarcza; Сундук -> Skrzynia; Серия -> Seria; Станция команды -> Stacja drużyny
# КНБ -> Kamień-Papier-Nożyce; Больше/Меньше -> Wyżej/Niżej

BUTTONS: dict[str, str] = {
    "main_menu": "📱 MENU GŁÓWNE",
    "profile": "👤 MÓJ PROFIL",
    "farm": "🚜 MOJA FARMA",
    "games_zone": "🕹️ STREFA GIER",
    "teams": "🏆 DRUŻYNY I KLANY",
    "shop": "🏪 SKLEP",
    "shop_cat_farm": "🚜 DLA FARMY",
    "shop_cat_games": "🕹️ DO GIER",
}

STRINGS: dict[str, str] = {
    "quest.epic_locked": "⭐ Epiki to duże historie na ponad 20 minut — otwierają się z ⚡ Bez limitu.",
    "quest.locked": "🔒 Dzisiejsze {n} nowe questy zaliczone. Pozostałe otworzą się o 00:00 UTC — albo włącz ⚡ Bez limitu. Ukończone questy można powtarzać.",
    # 27.10: «чат — дверь и почтальон», вся игра в приложении
    "app.moved": "🎮 Ta sekcja jest teraz w aplikacji gry — tam jest wygodniej i ładniej. Naciśnij przycisk 👇",
    "app.keyboard_gone": "🧹 Stare przyciski na dole zniknęły: cała gra jest teraz w aplikacji. Możesz ją też otworzyć przyciskiem «🎮 ROFL HUB» obok pola wpisywania.",
    "start.console_app": "🚀 <b>Gotowe!</b> Cała gra jest w aplikacji: naciśnij przycisk poniżej. Później zawsze otworzysz ją przyciskiem «🎮 ROFL HUB» obok pola wpisywania.",
    "start.welcome_back_app": "👋 <b>Witaj ponownie, @{username}!</b> Twoje postępy są zapisane — otwórz grę 👇",
    "menu.app": "📱 <b>ROFL HUB</b>\nCała gra jest w aplikacji 👇\n\n<b>W czacie:</b>\n• /invite — zaproś znajomego\n• /transfer — przelej monety\n• /faq — częste pytania\n• /rules — regulamin\n• /paysupport — pomoc z płatnościami\n• /delete_account — usuń konto",
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
    # ---------------- общее ----------------
    "common.no_profile": "⚠️ Nie znaleziono profilu. Naciśnij /start, aby się zarejestrować.",
    "common.btn_menu": "💿 Menu Główne",
    "common.blocked": "🚫 Twoje konto zostało zablokowane przez administrację ROFL HUB.",
    "common.feature_off": "⚙️ Ta sekcja jest w trakcie konserwacji. Wróć trochę później!",
    "common.maintenance": "🛠 ROFL HUB ma krótką przerwę techniczną. Zaraz wracamy — twoje monety i postępy są bezpieczne!",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>Witaj z powrotem, @{username}!</b>\nTwój postęp jest bezpieczny. Panel nawigacji znajdziesz na dole ekranu.",
    "start.btn_continue": "🛸 DALEJ",
    "start.btn_cutlet": "Co to za cyber-kotlet?🥩🤔",
    "start.btn_fight": "Mów szybko i DO BOJU!",
    "start.console": "🚀 <b>Konsola sterowania aktywowana! Używaj przycisków na dole ekranu.</b>",
    "start.intro1": (
        "👋 <b>Cześć! Jestem ROFL HUB BOT — główny bot ekosystemu gier ROFL HUB. "
        "To hub rozrywki i wiedzy nowej generacji!</b>\n\n"
        "<b>Tutaj możesz:</b>\n"
        "🎮 Grać w gry chatbotowe przeciwko botowi i innym graczom\n"
        "💸 Zdobywać walutę gry za zwycięstwa albo odpalić farmę, która wydobywa ją całą dobę\n"
        "🤼 Założyć drużynę i wbić na szczyt rankingu\n"
        "🏆 Rozwinąć drużynę w klan i walczyć w rankingu międzynarodowym\n"
        "💰 Razem ze swoją ekipą zgarnąć jackpot miliona monet\n"
        "👑 Kupić publikację na stronie głównej w social mediach lub na stronie www, aby wypromować siebie albo swojego bloga\n\n"
        "<b>Ten chatbot potrafi:</b>\n"
        "🎮 Pokazać listę wszystkich gier, kanałów i stron ROFL HUB\n"
        "⚡ Naliczać monety za gry, bitwy drużyn i klanów, osiągnięcia, aktywność i poleconych\n"
        "🔄 Przelewać monety innemu graczowi ROFL HUB\n"
        "💎 Sprzedawać publikacje na stronie i miejsca VIP dla twórców i blogerów\n"
        "🚀 Sprzedawać przyspieszacze, tytuły, statusy i wiele więcej...\n\n"
        "<i>Naciśnij „DALEJ”, a opowiem ci więcej 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>ODBIERZ SWOJE PIERWSZE NAGRODY ZA REJESTRACJĘ!</b>\n"
        "..................................................\n"
        "💸 Naliczono ci: <b>{balance} 🪙</b>\n"
        "🥩 Naliczono ci: <b>{cutlets} cyber-kotlet</b>\n"
        "..................................................\n"
        "To twój bonus startowy za dołączenie do klubu ROFL HUB.\n\n"
        "🔒 <i>Bonus przyznawany jest tylko raz, w momencie rejestracji.</i>\n\n"
        "Monety można wydawać na wiele sposobów — to fundament ekonomii huba. Dbaj o nie...\n\n"
        "⁉️ <b>Ale na pewno masz pytanie:</b> co to za kotlet? Kogo nim karmić?"
    ),
    "start.intro3": (
        "<b>NAJPIERW: DLACZEGO MONETY W GRZE SĄ TAKIE WAŻNE?</b>\n\n"
        "Monety to podstawa całego handlu, rywalizacji i zakupów w <b>ROFL HUB</b>. "
        "To niemal jedyna waluta w świecie gier, którą można wydobywać za darmo!\n"
        "..................................................\n"
        "<b>Można to robić na wiele sposobów:</b>\n"
        "- Zapraszać znajomych przez link polecający\n"
        "- Wygrywać gry przeciwko botowi\n"
        "- Wygrywać pojedynki z innymi graczami\n"
        "- Brać udział w bitwach drużyn i klanów\n"
        "- Odbierać bonus za codzienne wejście i zadania\n"
        "- Zdobyć robota, który wydobywa monety całą dobę (Młodszy Górnik / Cyber-Wiertacz)\n"
        "..................................................\n"
        "<b>Jeśli masz robota drugiego poziomu (Cyber-Wiertacza) — trzeba go karmić codziennie. "
        "Tu właśnie przydaje się cyber-kotlet: paliwo do automatycznego wydobycia, "
        "wydawane za darmo każdego dnia! Twoje zadanie jest proste — wpadnij i nakarm robota.</b>\n\n"
        "Jeśli nie nakarmisz go na czas — robot się rozładuje i wydobycie stanie.\n\n"
        "Młodszy Górnik (pierwszy poziom) nie potrzebuje paliwa. "
        "Ważne! Każdego robota kupujesz na 30 dni — potem trzeba kupić go ponownie albo sprawić sobie Mistrzowskiego Drona. "
        "Ogarniesz to w locie:) Nie rozpraszajmy się.\n\n"
        "Chcę opowiedzieć jeszcze trochę o <b>ROFL HUB</b>, żeby było jasne, jak tu wszystko działa.\n\n"
        "🛑 <b>To ostatnia wiadomość naszego wprowadzenia. Dalej tylko do boju:)</b>"
    ),
    "start.intro4": (
        "<b>W WIELKIM SKRÓCIE. ROFL HUB TO:</b>\n"
        "- Gry chatbotowe na każdy gust\n"
        "- Możliwość założenia drużyny (do 50 osób)\n"
        "- Możliwość rozwinięcia jej w klan (do 1000 osób)\n"
        "- Bitwy drużyn i klanów o nagrody\n"
        "- Strona na Instagramie — rofl_hub_global\n"
        "- Strona rofl-hub.com do rozmów i promocji bez rejestracji\n"
        "- Tysiące graczy z całego świata, wśród których mogą być twoi nowi znajomi!\n"
        "..................................................\n"
        "<b>Jak obiecałem, to wiadomość końcowa. Dalej tylko do boju! Przydatne komendy:</b>\n\n"
        "/menu — szybkie sterowanie funkcjami\n"
        "/games — lista wszystkich gier\n"
        "/faq — najczęściej zadawane pytania\n"
        "/rules — regulamin użytkownika\n"
    ),

    # ---------------- меню и игровая зона ----------------
    "menu.text": (
        "📱 <b>MENU GŁÓWNE EKOSYSTEMU ROFL HUB</b>\n"
        "..................................................\n"
        "👤 <b>PROFIL OSOBISTY I PASZPORT:</b>\n"
        "• /start — Rozpocznij wprowadzenie i zarejestruj konto\n"
        "• /profile — Twój paszport, saldo i drużyna w czasie rzeczywistym\n"
        "• /my_stats — Twoje statystyki historyczne z ostatnich 30 dni\n\n"
        "🚜 <b>CYBER-FARMA I AUTOMATYZACJA:</b>\n"
        "• /farm — Hub paliwowy: tankowanie i tempo wydobycia robotów\n"
        "• /shop — Marketplace: zakup górników, kotletów i ulepszeń huba\n\n"
        "🕹️ <b>POKÓJ GIER:</b>\n"
        "• /games — Inline-hub wszystkich gier przeciwko botowi\n"
        "• /quiz — Quiz na czas: 30 sekund na odpowiedź, poziomy i bonusy\n"
        "• /duel — POJEDYNKI 1 na 1 z żywymi graczami: stoły 10/100/1000\n"
        "• /quests — QUESTY: kryminały, komedie i łamigłówki z nagrodami\n"
        "• /rps, /high_low, /safe — Szybkie gry o monety\n\n"
        "👥 <b>ZARZĄDZANIE EKIPĄ:</b>\n"
        "• /create_team — Zarejestruj własną drużynę za 100 000 🪙\n"
        "• /my_team — Panel ekipy i SKŁAD DRUŻYNY z poziomami 🧠\n"
        "• /all_teams — Ruletka losowych drużyn\n\n"
        "💸 <b>PIENIĄDZE I ZNAJOMI:</b>\n"
        "• /invite — Twój link polecający: +500 🪙 za aktywnego znajomego\n"
        "• /transfer — Przelej monety innemu graczowi\n\n"
        "📚 <b>POMOC I ZASADY:</b>\n"
        "• /faq — Pełny przewodnik po ekosystemie (otwiera się w Mini App)\n"
        "• /rules — Regulamin użytkownika\n"
        "..................................................\n"
        "<i>⚙️ Korzystaj ze stałego dwukolumnowego panelu gry na dole ekranu, aby błyskawicznie nawigować między sekcjami!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>WITAJ W STREFIE GIER ROFL HUB!</b>\n"
        "..................................................\n"
        "Tutaj możesz zmierzyć się z botem w szybkich starciach albo przejść "
        "intelektualny sprint — i zgarnąć pulę albo spłukać się do zera!\n\n"
        "💸 Zwycięstwo daje: <b>+2 🪙</b> (Cyber-Sejf: <b>+5</b>)\n"
        "💀 Porażka lub remis kosztuje: <b>-1 🪙</b>\n"
        "🧠 W Quizie — licznik 30 sekund i poziomy intelektu: 1. poziom to 10 poprawnych odpowiedzi i <b>+100 🪙</b>, "
        "każdy kolejny poziom jest o 10 odpowiedzi dłuższy, ale nagroda rośnie o 100!\n"
        "..................................................\n"
        "👇 <b>KLIKNIJ PRZYCISK PONIŻEJ, ABY NATYCHMIAST ROZPOCZĄĆ RUNDĘ:</b>"
    ),
    "menu.btn_quiz": "🧠 Quiz",
    "menu.btn_rps": "🪨 KPN",
    "menu.btn_hl": "📈 Wyżej/Niżej",
    "menu.btn_safe": "🔐 Cyber-Sejf",
    "menu.btn_duel": "⚔️ POJEDYNKI 1 na 1",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "Paszport, farma, drużyna i top bogaczy — na jednym neonowym ekranie. "
        "Codzienny kotlet możesz odbierać prosto stamtąd!\n\n"
        "👇 Naciśnij przycisk:"
    ),
    "app.btn": "🎮 OTWÓRZ MINI APP",
    "app.unavailable": "⚙️ Mini App wciąż łączy się z serwerami ekosystemu. Zajrzyj trochę później!",
    "faq.teaser": (
        "📚 <b>PRZEWODNIK PO EKOSYSTEMIE ROFL HUB</b>\n"
        "..................................................\n"
        "Najważniejsze w skrócie:\n"
        "🚜 Roboty wydobywają monety całą dobę: Młodszy Górnik — 5/h bez paliwa, "
        "Cyber-Wiertacz — 10/h, a KAŻDY Wiertacz zjada swój własny cyber-kotlet raz na dobę. "
        "Wszystkie roboty żyją 30 dni (Mistrzowski Dron wstrzymuje zużycie).\n"
        "🧠 Quiz: 30 sekund na odpowiedź, poziomy intelektu z rosnącymi nagrodami.\n"
        "⚔️ Pojedynki z żywymi graczami przy stołach 10/100/1000 🪙.\n"
        "🏆 Drużyny do 50 wojowników (Mega-Klan — do 1000) i okazjonalne Bitwy z nagrodami dla każdego.\n"
        "..................................................\n"
        "👇 <b>Pełny przewodnik ze wszystkimi mechanikami — pod przyciskiem:</b>"
    ),
    "faq.btn_open": "📖 OTWÓRZ PEŁNY PRZEWODNIK",
    "rules.teaser": (
        "📜 <b>REGULAMIN UŻYTKOWNIKA ROFL HUB</b>\n"
        "..................................................\n"
        "Najważniejsze w dwóch słowach:\n"
        "🪙 Monety i wszystkie przedmioty w grze to wirtualne elementy rozrywkowe: "
        "nie są pieniędzmi i nie podlegają wymianie na prawdziwe środki.\n"
        "💫 Zakupy — wyłącznie przez oficjalne Telegram Stars; towary cyfrowe dostarczane są "
        "natychmiast, a przy błędzie dostawy Stars wracają automatycznie.\n"
        "🛡️ Nie zbieramy numerów telefonów, lokalizacji ani danych osobowych.\n"
        "🤝 Zakazane są obelgi, sztuczne nabijanie statystyk i multikonta — za naruszenie grozi blokada.\n"
        "..................................................\n"
        "👇 <b>Pełny tekst regulaminu i zastrzeżenia — pod przyciskiem:</b>\n"
        "<i>⚖️ Korzystając z bota, potwierdzasz akceptację warunków.</i>"
    ),
    "rules.btn_open": "📜 OTWÓRZ PEŁNY REGULAMIN",
    "quest.list_header": (
        "🗺️ <b>QUESTY ROFL HUB</b>\n"
        "..................................................\n"
        "Interaktywne historie z wyborami i rozgałęzieniami: kryminały, komedie, łamigłówki. "
        "Pierwsze zwycięstwo w każdym queście daje monety, a powtarzać możesz do woli!\n"
        "🌐 <i>Historie questów są na razie po rosyjsku — polski pakiet już w drodze.</i>\n\n"
        "👇 <b>Wybierz historię:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} 🪙 za pierwsze zwycięstwo\n"
        "..................................................\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>Quest ukończony, nagroda odebrana. Powtarzaj dla przyjemności!</i>",
    "quest.card_progress": "⏯ <i>Masz niedokończone przejście.</i>",
    "quest.card_new": "🆕 <i>Ta historia jest jeszcze przed tobą.</i>",
    "quest.btn_start": "▶️ ROZPOCZNIJ QUEST",
    "quest.btn_restart": "🔄 ZACZNIJ OD NOWA",
    "quest.btn_resume": "⏯ KONTYNUUJ",
    "quest.btn_list": "🗺️ Do listy questów",
    "quest.btn_replay": "🔄 Zagraj jeszcze raz",
    "quest.win_first": "\n\n🏆 <b>QUEST UKOŃCZONY! Nagroda: +{coins} 🪙.</b>",
    "quest.win_repeat": "\n\n✅ <b>Ukończono ponownie!</b> Nagroda za ten quest została już odebrana wcześniej.",
    "quest.fail_footer": "\n\n💀 <i>Nie najlepsze zakończenie... ale historię zawsze można przejść jeszcze raz!</i>",
    "quest.stale": "⏳ Ta scena jest już za tobą — gramy dalej od bieżącego miejsca!",
    "quest.no_coins": "❌ Podpowiedź kosztuje {cost} 🪙, a twoje saldo jest niższe. Zajrzyj na farmę!",
    "quest.not_found": "❌ Nie znaleziono questa.",
    "menu.btn_quests": "🗺️ QUESTY",

    # ---------------- ферма ----------------
    "farm.btn_bonus": "🎁 ODBIERZ BONUS (kotlet co 24 h)",
    "farm.btn_load1": "🥩 Zatankuj 1 szt.",
    "farm.btn_loadall": "⚡ Zatankuj WSZYSTKIE",
    "farm.btn_shop": "🏪 Wejdź do Sklepu",
    "farm.status_all_fueled": "🟢 Wszystkie Cyber-Wiertacze są zatankowane i wydobywają monety!",
    "farm.status_partial": "🟡 Zatankowano {fueled} z {total} Cyber-Wiertaczy. Reszta czeka na kotlety w lodówce!",
    "farm.status_no_fuel": "🔴 Cyber-Wiertacze stanęły! W lodówce brakuje paliwa.",
    "farm.status_no_drills": "💡 Spraw sobie mocniejszego robota w /shop — farma będzie wydobywać więcej.",
    "farm.boost_nuclear": "🔋 Nuklearne Przyspieszenie x5 do {until} UTC (zużycie kotletów ×3)",
    "farm.boost_nitrogen": "❄️ Azotowe Chłodzenie +40% do {until} UTC",
    "farm.boost_drone": "🛸 Mistrzowski Dron przedłuża życie robotów do {until} UTC",
    "farm.no_boosts": "Brak aktywnych wzmocnień — zajrzyj do /shop.",
    "farm.burnout": "🔥 Najbliższe wypalenie robota: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Aktywuj Robota Stażystę (za darmo)",
    "farm.intern_activated": "🤖 Twój Robot Stażysta zaczął zmianę! +1 🪙 na godzinę na zawsze — bez paliwa i bez terminu.",
    "farm.intern_already": "🤖 Twój Robot Stażysta już pracuje.",
    "farm.btn_claim_intern": "🎁 Odbierz Robota Stażystę ({n})",
    "farm.intern_pending": "🎁 Za poziomy intelektu czekają na ciebie Roboty Stażyści: <b>{n}</b> — odbierz je przyciskiem poniżej!",
    "farm.intern_claimed_new": "🤖 Nowy Robot Stażysta wyszedł na zmianę! +1 🪙 na godzinę na zawsze.",
    "farm.intern_none": "🤖 Nowych Stażystów na razie brak — kolejny czeka na ciebie na 10., 20., 30. poziomie intelektu…",
    "games.intern_ready": "🎁 Za nowy poziom czeka na ciebie <b>Robot Stażysta</b> — odbierz go na farmie!",
    "farm.intern_line": "• Roboty Stażyści ({rate} 🪙/h, wieczne): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 Masz darmowego Robota Stażystę! Naciśnij przycisk poniżej — będzie wydobywać 1 🪙 na godzinę na zawsze.",
    "farm.dashboard": (
        "🚜 <b>CENTRALNY HUB PALIWOWY ROFL HUB</b>\n"
        "..................................................\n"
        "🤖 Aktywne roboty w fabryce: <b>{total} szt.</b>\n"
        "{intern}"
        "• Młodsi Górnicy ({junior_rate} 🪙/h): <code>{junior} szt.</code>\n"
        "• Cyber-Wiertacze ({premium_rate} 🪙/h): <code>{premium} szt.</code>\n"
        "{burnout}\n"
        "📊 <b>AKTUALNE TEMPO TWOJEJ FARMY:</b>\n"
        "• Produkcja na godzinę: <b>+{speed_hour} 🪙</b>\n"
        "• Produkcja na dobę: <b>+{speed_day} 🪙</b>\n\n"
        "⚡ <b>WZMOCNIENIA:</b>\n{boosts}\n\n"
        "📋 <b>STATUS TWOJEJ FABRYKI:</b>\n"
        "{status}\n"
        "..................................................\n"
        "📦 <b>STAN AUTOMATYCZNEJ LODÓWKI:</b>\n"
        "🥩 Zapas paliwa: <b>{fridge} / {capacity} szt.</b>\n"
        "💼 Kotlety w magazynie: <code>{inv} szt.</code>\n"
        "..................................................\n"
        "<i>💿 Ważne: roboty żyją 30 dni (Mistrzowski Dron wstrzymuje zużycie). "
        "KAŻDY Cyber-Wiertacz zjada SWÓJ cały kotlet z lodówki na każde "
        "24 godziny pracy: 3 roboty — 3 kotlety na dobę. Pilnuj tankowania!</i>"
    ),
    "farm.bonus_ok": "🎁 Cyber-kotlet trafił do magazynu! Wróć za 24 godziny.",
    "farm.bonus_wait": "⏳ Bonus już odebrany! Następny kotlet za {hours} godz. {minutes} min.",
    "farm.no_inv_cutlets": "❌ Nie masz w magazynie cyber-kotletów! Kup je w /shop",
    "farm.fridge_full": "📦 Twoja Lodówka jest już pełna po brzegi!",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>PANEL GRACZA ROFL HUB</b>\n"
        "..................................................\n"
        "🆔 Twój ID Paszportu: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Monety teraz: <b>{balance} 🪙</b>\n"
        "🏆 Twój status: <b>{team}</b>\n"
        "🧠 Poziom intelektu: <b>{level}</b> · do poziomu {next_level}: "
        "<b>{left}</b> poprawnych odpowiedzi w /quiz (nagroda: +{reward} 🪙)\n"
        "..................................................\n"
        "<i>Tutaj widzisz to, co masz w tej chwili. Używaj przycisków, aby przeskoczyć do innych sekcji!</i>"
    ),
    "profile.no_team": "Brak drużyny",
    "profile.team_label": "Drużyna",
    "profile.clan_label": "Klan",
    "profile.btn_farm": "🚜 Moja Cyber-Farma",
    "profile.btn_shop": "🏪 Sklep",
    "profile.stats": (
        "📊 <b>STATYSTYKI OSIĄGNIĘĆ W GRZE (30 DNI)</b>\n"
        "..................................................\n"
        "🧠 Poziom intelektu w grze: <b>{level}</b> (łącznie poprawnych odpowiedzi: {total})\n"
        "🎮 Rozegranych rund w pojedynkach: <b>{played}</b>\n"
        "🏆 Zwycięstw nad rywalami: <code>{won}</code>\n"
        "👥 Zaproszonych aktywnych znajomych: <b>{refs}</b>\n"
        "..................................................\n"
        "<i>Statystyki przechowują twoje historyczne zasługi i dawne osiągnięcia, nawet jeśli wygrane monety zostały już wydane w markecie!</i>"
    ),
    "img.passport": "ID PASZPORTU: {user_id}",
    "img.owner": "LIDER: @{username}",
    "img.balance": "Saldo: {balance} monet",
    "img.fridge": "W lodówce: {fridge} / {capacity} szt.",
    "img.inv": "Kotlety w magazynie: {inv} szt.",
    "img.junior": "Młodsi Górnicy: {count} szt.",
    "img.premium": "Cyber-Wiertacze: {count} szt.",

    # ---------------- игры: общий движок ----------------
    "games.win": "🎉 <b>ZWYCIĘSTWO!</b> 🎉\nNaliczono: <b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>PORAŻKA!</b>\nPobrano: <b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>REMIS!</b>\nPobrano: <b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>Dzienny limit osiągnięty!</b>\n\n"
        "W grze {game} masz już {limit} zwycięstw na dziś. Limit odnowi się o 00:00 UTC.\n\n"
        "⚡ Zdejmij limit na 24 godziny — 15 ★, na 30 dni — 249 ★ (sekcja „Do gier” w /shop)."
    ),
    "games.no_coins": "❌ Masz 0 🪙 — nie masz czym opłacić rundy. Odbierz dochód z farmy w /farm!",
    "games.balance": "💰 Saldo: <b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 Zagraj jeszcze raz!",
    "games.btn_hub": "🕹️ Strefa gier",
    "games.level_up": (
        "🏅 <b>POZIOM INTELEKTU PODNIESIONY: {level}!</b> Nagroda: <b>+{bonus} 🪙</b>!\n"
        "Następny poziom: {next_required} poprawnych odpowiedzi → +{next_reward} 🪙."
    ),
    "games.name.rps": "Kamień-Papier-Nożyce",
    "games.intern_bonus": "🤖 Poziom {level}! Na farmę przybył kolejny Robot Stażysta — masz ich już {count}.",
    "games.name.hl": "Wyżej/Niżej",
    "games.name.quiz": "Quiz",
    "games.name.safe": "Sejf",
    "games.name.math": "Math",  # TODO(перевод 26.10)
    "games.name.flags": "Flags and capitals",  # TODO(перевод 26.10)
    "games.name.code": "Code breaker",  # TODO(перевод 26.10)
    "games.name.memory": "Memory",  # TODO(перевод 26.10)

    # ---------------- КНБ ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>KAMIEŃ-PAPIER-NOŻYCE</b>\n\n"
        "Zwycięstwo: <b>+{reward}</b> · Porażka/remis: <b>-{penalty}</b>\n"
        "Limit zwycięstw na dobę: <b>{limit}</b>"
    ),
    "rps.rock": "🪨 Kamień",
    "rps.scissors": "✂️ Nożyce",
    "rps.paper": "🧻 Papier",
    "rps.draw": "🤝 <b>Remis!</b> Obie strony wybrały {bot}.",
    "rps.win": "🏆 <b>Zwycięstwo!</b> Twój gest {user} bije {bot}.",
    "rps.lose": "💀 <b>Bot wygrał.</b> Gest bota {bot} bije twój gest {user}.",

    # ---------------- Больше/Меньше ----------------
    "hl.intro": (
        "🎲 <b>WYŻEJ CZY NIŻEJ</b>\n\nBot odkrył liczbę: <b>{base}</b>.\n"
        "Ukryta liczba będzie wyższa czy niższa?\n"
        "Zwycięstwo: <b>+{reward}</b> · Porażka: <b>-{penalty}</b> · Limit: <b>{limit}</b> zwycięstw"
    ),
    "hl.btn_up": "📈 Wyżej",
    "hl.btn_down": "📉 Niżej",
    "hl.result": "🎲 <b>WYNIK RUNDY</b>\n\nLiczba bota: <b>{base}</b> · Ukryta: <b>{secret}</b>",

    # ---------------- викторина ----------------
    "quiz.round": (
        "🧠 <b>QUIZ • {category}</b>\n"
        "🤔 PYTANIE: <b>{question}</b>\n\n"
        "<i>🌐 Pytania są na razie po rosyjsku — polski pakiet już wkrótce!</i>"
    ),
    "quiz.btn_new": "🧠 Nowe pytanie",
    "quiz.timeout": "⌛ <b>CZAS MINĄŁ!</b> ⌛\nPoprawna odpowiedź: <b>{correct}</b>",
    "quiz.stale": "⏳ To pytanie nie jest już aktywne. Odpal nowe!",
    "quiz.stale_alert": "To pytanie nie jest już aktywne. Odpal nowe!",
    "quiz.empty": "⚠️ Baza pytań jest pusta. Zgłoś to administratorowi.",
    "quiz.wrong": "❌ <b>Błąd</b> ❌\nPoprawna odpowiedź: <b>{correct}</b>",
    "quiz.lost_line": "💀 <b>-{penalty} 🪙</b> za przegraną!",
    "quiz.level_line": (
        "🧠 Poziom intelektu: <b>{level}</b>\n"
        "Do poziomu {next_level} brakuje zwycięstw: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>Na odpowiedź masz {seconds} sekund!\n"
        "Poprawnie: +{win} 🪙 na konto\n"
        "Błąd / brak odpowiedzi na czas: -{penalty} 🪙\n"
        "Limit: {limit} zwycięstw na dobę</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>CYBER-SEJF</b>\n\n"
        "W środku — jackpot <b>{jackpot} 🪙</b>! Drzwiczki zamknięte kodem od 1 do {codes}. "
        "Masz jedną próbę.\n"
        "Włamanie: <b>+{jackpot}</b> · Alarm: <b>-{penalty}</b> · Limit: <b>{limit}</b> zwycięstw"
    ),
    "safe.btn_retry": "🔐 Włam się jeszcze raz!",
    "safe.win": "🔓 <b>Sejf otwarty!</b> Kod to: <b>{code}</b>.",
    "safe.lose": "🚨 <b>Alarm uruchomiony!</b> Twój typ: {guess}, a kod to: <b>{code}</b>.",

    # ---------------- дуэли ----------------
    "duel.intro": (
        "⚔️ <b>POJEDYNKI 1 NA 1: KAMIEŃ-PAPIER-NOŻYCE O STAWKĘ</b>\n"
        "..................................................\n"
        "Wybierz stół na swoją kieszeń — jak w pokerze. Stawka schodzi z konta od razu, "
        "a przeciwnikiem jest żywy gracz ROFL HUB!\n\n"
        "💰 Pula = obie stawki. Zwycięzca zabiera <b>{payout_percent}%</b> puli, "
        "<b>{burn_percent}%</b> spala się na zawsze (deflacja!).\n"
        "🤝 Remis — natychmiastowa dogrywka gestów, pula zostaje na stole.\n"
        "⏱ Na gest masz <b>{move_timeout} sekund</b>; milczkowi gest wybierze generator losowości.\n"
        "🏆 Zwycięstwa w pojedynkach liczą się dla twojej drużyny w Bitwach!\n\n"
        "👇 <b>WYBIERZ STÓŁ:</b>"
    ),
    "duel.btn_table": "⚔️ Stół {stake} 🪙",
    "duel.btn_cancel": "❌ Opuść stół (zwrot stawki)",
    "duel.btn_move_rock": "🪨 Kamień",
    "duel.btn_move_scissors": "✂️ Nożyce",
    "duel.btn_move_paper": "🧻 Papier",
    "duel.waiting": (
        "🪑 <b>Siedzisz przy stole {stake} 🪙.</b> Stawka jest w puli.\n"
        "Czekamy na drugiego wojownika... Gdy tylko usiądzie, każdy z was dostanie wybór gestu!\n"
        "<i>Kolejka żyje {ttl} minut, potem stawka wróci automatycznie.</i>"
    ),
    "duel.cancelled": "🚪 Stół opuszczony. Stawka <b>{stake} 🪙</b> wróciła na saldo.",
    "duel.expired": "⌛ Przy stole {stake} nie znalazł się przeciwnik. Stawka <b>{stake} 🪙</b> została zwrócona.",
    "duel.matched": (
        "⚔️ <b>PRZECIWNIK ZNALEZIONY! Stół {stake} 🪙.</b>\n"
        "Pula: <b>{bank} 🪙</b> · Dla zwycięzcy: <b>{payout}</b>\n\n"
        "⏱ Masz <b>{timeout} sekund</b> na wybór gestu!"
    ),
    "duel.move_saved": "✊ Gest przyjęty! Czekamy na gest przeciwnika...",
    "duel.draw_replay": (
        "🤝 <b>REMIS! Runda {round}.</b> Obie strony pokazały ten sam gest.\n"
        "Pula zostaje na stole. ⏱ Znowu {timeout} sekund — wybierz gest:"
    ),
    "duel.win": (
        "🏆 <b>POJEDYNEK JEST TWÓJ!</b>\n\n"
        "Twój gest {winner_move} bije {loser_move}.\n"
        "💰 Wygrana: <b>+{payout} 🪙</b> · 🔥 Spalone z puli: {burned}\n"
        "💼 Saldo: <b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>POJEDYNEK PRZEGRANY.</b>\n\n"
        "Gest przeciwnika {winner_move} bije twój gest {loser_move}.\n"
        "📉 Stawka <b>{stake} 🪙</b> trafiła do puli zwycięzcy.\n"
        "Rewanż?"
    ),
    "duel.reaper_prefix": "⏰ <b>Koniec czasu rundy!</b> Brakujące gesty wybrał generator losowości.\n\n",
    "duel.bad_table": "❌ Taki stół nie istnieje.",
    "duel.already_in": "⚠️ Już siedzisz przy stole albo walczysz! Najpierw dokończ bieżący pojedynek.",
    "duel.no_coins": "❌ Do tego stołu potrzebujesz {stake} 🪙 na koncie.",
    "duel.cancel_impossible": "⚠️ Tej kolejki nie da się już anulować (przeciwnik znaleziony albo stół zamknięty).",
    "duel.not_active": "⌛ Ten pojedynek już się zakończył.",
    "duel.not_participant": "🔒 To nie twój pojedynek!",
    "duel.move_already": "✋ Twój gest w tej rundzie jest już zapisany. Czekamy na przeciwnika!",
    "duel.bad_move": "❌ Nieznany gest.",
    "duel.btn_rematch": "⚔️ Rewanż (do stołów)",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID: <b>{aliases}</b>\n",
    "profile.rank_line": "🎖 Ranga: <b>{rank}</b>\n",
    "rank.rookie": "Nowicjusz",
    "rank.fighter": "Wojownik",
    "rank.legend": "Legenda",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.king": "KING",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>PROGRAM POLECEŃ ROFL HUB</b>\n"
        "..................................................\n"
        "Zapraszaj znajomych przez swój osobisty link i otrzymuj <b>{bonus}</b> "
        "za każdego, kto zostanie aktywnym graczem!\n\n"
        "🔗 <b>Twój link (kliknij, aby skopiować):</b>\n<code>{link}</code>\n\n"
        "📊 <b>TWOJE STATYSTYKI:</b>\n"
        "👥 Zaproszonych znajomych: <b>{invited}</b>\n"
        "💰 Zarobione na poleconych: <b>{earned} 🪙</b>\n"
        "..................................................\n"
        "<i>Podsyłaj link znajomym, wrzucaj na czaty klasowe i do social mediów — im większa ekipa, tym szybciej rośnie twoje saldo!</i>"
    ),
    "ref.btn_share": "📣 Udostępnij link",
    "ref.share_text": "Wbijaj do ekosystemu gier ROFL HUB!",
    "ref.qualified_line": ("✅ <b>Aktywny znajomy</b> to ktoś, kto osiągnął <b>{level}. poziom intelektu</b> w quizie "
                           "i odebrał <b>{claims} codzienne kotlety</b> na farmie. Wtedy dostajesz <b>{bonus}</b>, "
                           "jednorazowo za każdego znajomego. Za samą rejestrację bez gry bonusu nie ma — tak jest uczciwiej dla wszystkich."),
    "ref.qualified_notify": ("🤝 <b>Twój znajomy został aktywnym graczem!</b>\n"
                             "{level}. poziom intelektu i {claims} codzienne kotlety — są. Dostajesz <b>{bonus}</b>. Zapraszaj dalej!"),

    "team.err_len": "❌ Tekst musi mieć od 1 do {max} znaków!",
    "team.err_link": "🚨 Błąd bezpieczeństwa! Linki, nazwy użytkowników i numery telefonów są surowo zabronione!",
    "team.err_badword": "❌ Wykryto wulgaryzmy! Przestrzegaj zasad huba.",
    "team.err_already": "⚠️ Jesteś już w drużynie lub klanie! Najpierw z niej wyjdź.",
    "team.err_money": "❌ Za mało monet! Założenie drużyny kosztuje {cost} 🪙, a masz {balance} 🪙.",
    "team.err_captain": "⚠️ Jesteś już kapitanem innej drużyny!",
    "team.err_taken": "⚠️ Nazwa „{name}” jest już zajęta! Wymyśl niepowtarzalną.",
    "team.err_gone": "❌ Ta drużyna już nie istnieje.",
    "team.err_full": "📦 W tej drużynie nie ma już wolnych miejsc!",
    "team.err_not_member": "❌ Nie jesteś w żadnej drużynie.",
    "mk.err_no_team": "🏆 Giełda drużyny jest dla członków drużyn. Dołącz do drużyny albo stwórz własną.",
    "mk.err_team_only": "🔒 Ta oferta jest tylko dla członków drużyny sprzedającego.",
    "help.err_qty": "Możesz poprosić o od 1 do {max} jednostek surowca.",
    "help.err_open": "Masz już otwartą prośbę — poczekaj na pomoc albo wycofaj ją.",
    "help.err_not_found": "Ta prośba jest już zamknięta.",
    "help.err_self": "Własnej prośby nie zamkniesz prezentem 🙂",
    "help.err_limit": "Dziś podarowano już {max} surowców — limit odnowi się o 00:00 UTC.",
    "help.err_not_active": "🔒 Surowce można dawać od poziomu intelektu {level} i po odebraniu {claims} codziennych kotletów.",
    "it.err_none": "Tego przedmiotu nie ma już w magazynie.",
    # ---------------- usuwanie konta ----------------
    "profile.btn_delete": "🗑 Usuń konto",
    "acct.warn": (
        "⚠️ <b>USUWANIE KONTA</b>\n"
        "..................................................\n"
        "Razem z kontem <b>bezpowrotnie</b> znikną:\n"
        "• monety, kotlety, zasoby i wszystkie roboty farmy;\n"
        "• boosty, Bezlimit i wszystko kupione za Stars — <b>Stars nie podlegają zwrotowi</b>;\n"
        "• VIP ID, postępy w quizie i questach;\n"
        "• miejsce w drużynie (kapitanat przejmie weteran drużyny).\n"
        "Otwarte zlecenia na giełdzie zostaną zdjęte od razu, towar wróci do magazynu.\n\n"
        "⏳ Najpierw konto zostanie zamrożone na <b>{days} dni</b> — w tym czasie możesz się rozmyślić jednym przyciskiem. "
        "Potem usunięcie jest nieodwracalne. Jeśli wrócisz później, zaczniesz od zera — bonus startowy nie jest przyznawany drugi raz.\n\n"
        "<i>Przycisk usuwania zadziała za {seconds} s — przeczytaj uważnie.</i>"
    ),
    "acct.btn_keep": "✅ Nie, zostaw konto",
    "acct.btn_confirm": "🗑 Tak, usuń konto",
    "acct.wait": "⏳ Poczekaj jeszcze {seconds} s — przeczytaj, co dokładnie zostanie usunięte.",
    "acct.kept": "👍 Świetnie, konto zostaje z tobą!",
    "acct.scheduled": (
        "🗑 Konto zostało zamrożone i zostanie usunięte <b>{date}</b> (UTC).\n"
        "Zlecenia na giełdzie zdjęto, towar wrócił do magazynu.\n\n"
        "Jeśli się rozmyślisz, naciśnij przycisk poniżej — wszystko wróci do poprzedniego stanu."
    ),
    "acct.pending_notice": (
        "⏳ Konto jest zamrożone i zostanie usunięte <b>{date}</b> (UTC).\n"
        "Chcesz zostać w grze? Naciśnij przycisk poniżej."
    ),
    "acct.btn_undo": "↩️ Anuluj usunięcie",
    "acct.undone": "🎉 Usunięcie anulowane — konto znów jest twoje!",
    "acct.purged": "🗑 Twoje konto ROFL HUB zostało usunięte. Dzięki za grę! Jeśli zechcesz wrócić, naciśnij /start.",
    "acct.deleted_notice": "Konto zostało usunięte. Naciśnij /start, aby zacząć od nowa.",
    "acct.welcome_back": (
        "👋 <b>Witaj z powrotem!</b>\n"
        "Profil utworzono od nowa, od zera. Bonus startowy przyznawany jest tylko raz, więc saldo wynosi 0 🪙. "
        "Farma, gry i quiz czekają!"
    ),
    "tr.err_not_active": (
        "🔒 Przelewy monet są dostępne po osiągnięciu {level}. poziomu intelektu i odebraniu {claims} codziennych kotletów — "
        "dzięki temu ekosystem jest chroniony przed fałszywymi kontami."
    ),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>PRZELEW MONET DO INNEGO GRACZA</b>\n"
        "..................................................\n"
        "Format komendy:\n"
        "<code>/transfer ID kwota</code> — po ID Paszportu (widoczny w /profile)\n"
        "<code>/transfer @username kwota</code> — po nazwie użytkownika\n"
        "<code>/transfer ROFL-HUB-777 kwota</code> — po VIP ID z aukcji\n\n"
        "Przykłady:\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 Minimalna kwota: <b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ Nie znaleziono odbiorcy. Sprawdź ID Paszportu lub @username — gracz musi być zarejestrowany w bocie.",
    "tr.self": "🤨 Nie możesz przelać monet samemu sobie — to byłoby ekonomiczne perpetuum mobile!",
    "tr.blocked": "🚫 Ten gracz jest zablokowany — przelewy do niego są niedostępne.",
    "tr.min": "❌ Minimalna kwota przelewu to {min} 🪙.",
    "tr.insufficient": "❌ Za mało monet! Twoje saldo: <b>{balance} 🪙</b>.",
    "tr.err_insufficient": "❌ Za mało monet na koncie.",
    "tr.confirm": (
        "🔄 <b>POTWIERDŹ PRZELEW:</b>\n\n"
        "👤 Odbiorca: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Kwota do pobrania: <b>{amount} 🪙</b>{fee_line}\n"
        "💰 Odbiorca otrzyma: <b>{received} 🪙</b>\n\n"
        "<i>Przelewów nie da się cofnąć — sprawdź odbiorcę!</i>"
    ),
    "tr.fee_line": "\n🔥 Prowizja huba: <b>{fee} 🪙</b> (spłonie)",
    "tr.btn_confirm": "✅ POTWIERDŹ PRZELEW",
    "tr.btn_cancel": "❌ Anuluj",
    "tr.cancelled_toast": "Przelew anulowany",
    "tr.cancelled": "❌ <b>Przelew anulowany.</b> Monety zostały na miejscu.",
    "tr.not_yours": "🔒 To nie twój przelew!",
    "tr.done_toast": "✅ Przelew wykonany!",
    "tr.done": (
        "✅ <b>PRZELEW WYKONANY!</b>\n\n"
        "💸 Wysłano: <b>{amount} 🪙</b> do gracza ID <code>{recipient_id}</code>\n"
        "💰 Twoje saldo: <b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>Masz przelew: {amount} 🪙!</b>\n"
        "Nadawca: ID <code>{sender_id}</code>. Saldo już doładowane — sprawdź /profile!"
    ),

    # ---------------- магазин и платежи ----------------
    "shop.header": "🏪 <b>SKLEP ROFL HUB</b>\nZakupy — przez oficjalne Telegram Stars. Wybierz kategorię przyciskami na dole.",
    "shop.cat_farm": (
        "🚜 <b>SKLEP · DLA FARMY</b>\n"
        "..................................................\n"
        "Roboty na 30 dni, paliwo, lodówki, wzmocnienia i Mistrzowski Dron.\n"
        "📦 Twoja lodówka mieści teraz: <b>{capacity} kotletów</b>\n"
        "..................................................\n"
        "👇 <b>Wybierz towar:</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>SKLEP · DO GIER</b>\n"
        "..................................................\n"
        "Zdjęcie limitów zwycięstw, paczki monet i licencja Mega-Klanu.\n"
        "..................................................\n"
        "👇 <b>Wybierz towar:</b>"
    ),
    "pay.invoice_desc": "Natychmiastowa dostawa treści w grze ROFL HUB.",
    "pay.invoice_error": "⚠️ Nie udało się utworzyć rachunku Telegram Stars. Spróbuj później.",
    "pay.success": "🎉 <b>Płatność potwierdzona!</b>\n🧾 <code>{charge}</code>\n💵 Pobrano: <b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 Płatność przeszła, ale dostawa chwilowo się nie udała. Już o tym wiemy.\n"
        "Zachowaj numer płatności: <code>{charge}</code>"
    ),
    "pay.refunded": "💫 Stars wróciły na twoje konto automatycznie.",
    "pay.keep_charge": "Zachowaj numer płatności do zwrotu: <code>{charge}</code>",
    "pay.already": "✅ Ta płatność została już przetworzona, towar wydano wcześniej.",
    "pay.support": (
        "🛟 <b>WSPARCIE PŁATNOŚCI TELEGRAM STARS</b>\n"
        "..................................................\n"
        "Wszystkie towary ROFL HUB są cyfrowe i dostarczane natychmiast po opłaceniu.\n\n"
        "⚙️ <b>Jeśli płatność przeszła, a towar nie dotarł:</b>\n"
        "bot automatycznie zwraca Stars przy błędzie dostawy. Jeśli tak się nie stało — "
        "przyślij tutaj numer płatności (jest na paragonie, format <code>xxxx...</code>) i opisz problem. "
        "Administracja sprawdzi płatność w bazie i rozwiąże sprawę w ciągu 24 godzin.\n\n"
        "💫 <b>Polityka zwrotów:</b>\n"
        "zwrot jest możliwy, jeśli towar nie został dostarczony albo wydano go z błędem. "
        "Poprawnie dostarczone towary cyfrowe nie podlegają zwrotowi.\n"
        "..................................................\n"
        "<i>Ta sekcja to oficjalny punkt wsparcia zakupów zgodnie z zasadami Telegramu.</i>"
    ),

    # ---------------- доставка ----------------
    "dlv.cutlets": "🥩 Dodano do magazynu: <b>{qty} kotletów</b>.",
    "dlv.miner": "🤖 Robot <b>„{name}”</b> dostarczony na twoją farmę.\n⏳ Okres działania: do <b>{until} UTC</b>.",
    "dlv.miner_junior": "Młodszy Górnik",
    "dlv.miner_premium": "Cyber-Wiertacz",
    "dlv.fridge": "📦 Lodówka powiększona do <b>{capacity} kotletów</b>.",
    "dlv.coins": "💰 Naliczono <b>+{amount} 🪙</b>.",
    "dlv.boost_nuclear": "🔋 Nuklearne Przyspieszenie x5 aktywne do <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Azotowe Chłodzenie +40% aktywne do <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Mistrzowski Dron pilnuje farmy do <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limity zwycięstw zdjęte do <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Drużyna otrzymała status <b>MEGA-KLANU</b>: do {max} miejsc.",
    "dlv.err_fridge": "Masz już lodówkę tej lub większej pojemności.",
    "dlv.err_no_team": "Nie masz jeszcze drużyny. Najpierw załóż ją przez /create_team.",
    "dlv.err_mega": "Twoja drużyna ma już status Mega-Klanu.",
    "dlv.intern_upgrade": "♾ Twój Robot Stażysta awansował na <b>WIECZNEGO Młodszego Górnika</b>: 5 🪙 na godzinę, bez terminu!",
    "dlv.err_no_intern": "Brak aktywowanego Robota Stażysty — najpierw aktywuj go w /farm.",
    "dlv.err_intern_refs": "Ulepszenie wymaga {need} aktywnych znajomych (zasady w /invite); masz {have}.",
    "mk.header": "📈 <b>GIEŁDA KOTLETÓW</b>\n..................................................\nOtwarte zlecenia: <b>{orders}</b> · kotletów w ofercie: <b>{cutlets}</b> · najlepsza cena: <b>{best}</b>\nProwizja hubu: <b>{fee}%</b> od sprzedaży (spalana — tarcza antyinflacyjna)\n🥩 W twoim magazynie: <b>{inv}</b> kotletów\n\n{body}\n\n<i>Kliknij zlecenie, aby kupić. Sprzedaż: /sell.</i>",
    "mk.empty": "Nie ma jeszcze ofert. Bądź pierwszy: /sell ilość cena",
    "mk.order_line": "🥩 #{id} · <b>{qty} szt.</b> po <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}: {qty} szt. po {price} 🪙",
    "mk.btn_my": "📋 Moje zlecenia",
    "mk.btn_sell_help": "💰 Jak sprzedać kotlety",
    "mk.btn_refresh": "🔄 Odśwież",
    "mk.btn_back": "← Do giełdy",
    "mk.pick": "🛒 <b>Zlecenie #{id}</b>: dostępne {qty} szt. po {price} 🪙.\nIle kupić?",
    "mk.btn_qty": "{qty} szt. — {total} 🪙",
    "mk.btn_qty_all": "Wszystkie {qty} szt. — {total} 🪙",
    "mk.buy_toast": "Transakcja zamknięta!",
    "mk.buy_done": "✅ Kupiono <b>{qty} kotletów</b> za <b>{total} 🪙</b>. Są już w magazynie — tankuj Wiertacze!",
    "mk.sold_notify": "💰 <b>Giełda: sprzedano!</b> Zlecenie #{id}: {qty} szt. po {price}. Otrzymujesz <b>+{got} 🪙</b> (prowizja {fee} spalona).",
    "mk.sell_help": "💰 <b>JAK SPRZEDAĆ KOTLETY</b>\n\nKomenda: <code>/sell ilość cena</code>\nPrzykład: <code>/sell 10 250</code> — 10 kotletów po 250 🪙.\n\nKotlety schodzą z magazynu i czekają w zleceniu (możesz je wycofać w każdej chwili). Do {max_qty} szt. w zleceniu i do {max_orders} otwartych zleceń. Przy sprzedaży spalana jest prowizja {fee}%. Kotlet nie taniej niż {min} 🪙: paliwo ze sklepu za Gwiazdki zawsze wychodzi korzystniej niż giełda. Surowce, zlecenia kupna i wymiana — w aplikacji gry.",
    "mk.sell_confirm": "📝 Wystawić <b>{qty} kotletów</b> po <b>{price}</b> 🪙?\nSuma: {total} · prowizja {fee} spłonie · dostaniesz <b>{got} 🪙</b>.",
    "mk.btn_confirm_sell": "✅ WYSTAW NA GIEŁDĘ",
    "mk.btn_cancel": "❌ Anuluj",
    "mk.sell_toast": "Zlecenie wystawione!",
    "mk.sell_done": "✅ Zlecenie <b>#{id}</b> na giełdzie: {qty} szt. po {price} 🪙. Dam znać, gdy ktoś kupi.",
    "mk.cancelled_toast": "Anulowano",
    "mk.cancel_text": "❌ <b>Anulowano.</b> Kotlety zostały w magazynie.",
    "mk.my_header": "📋 <b>TWOJE ZLECENIA</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} szt. po {price} 🪙",
    "mk.my_empty": "📋 Nie masz otwartych zleceń.",
    "mk.btn_cancel_order": "❌ Wycofaj zlecenie #{id}",
    "mk.err_newbie_price": "🔒 While your account is new, you can buy at no more than {max} 🪙 apiece. The limit lifts at intelligence level {level} and after {claims} daily cutlets.",
    "mk.err_cancel_room": "📦 Not enough storage room: {free} free. Make room first, then withdraw the lot.",
    "sw.err_ratio": "⚖️ This swap is too uneven: the two sides (valued at the market's minimum prices) may differ by at most {x}×.",
    "mk.order_cancelled": "↩️ Zlecenie #{id} wycofane: <b>{qty} kotletów</b> wróciło do magazynu.",
    "mk.err_qty": "❌ Ilość: od 1 do {max} szt. w zleceniu.",
    "mk.err_price": "❌ Cena: od {min} do {max} 🪙 za sztukę.",
    "mk.err_no_cutlets": "❌ W magazynie masz tylko {have} kotletów. Kotlety z lodówki nie trafiają na giełdę — zobacz /farm.",
    "mk.err_too_many": "❌ Limit: maksymalnie {max} otwartych zleceń. Wycofaj jedno w „Moje zlecenia”.",
    "mk.err_not_found": "❌ To zlecenie jest już zamknięte.",
    "mk.err_own": "🤨 Nie możesz kupić własnego zlecenia.",
    "mk.err_insufficient": "❌ Za mało: potrzeba {total} 🪙.",
    "farm.btn_market": "📈 Giełda kotletów",

    # ---------------- ресурсы (волна 22.10, вечер) ----------------
    "res.metal": "Metal",
    "res.hydrogen": "Wodór",
    "res.crystal": "Kryształy",
    "res.parts": "Części",
    "res.none": "na razie pusto",
    "games.resource_gain": "{icon} Wydobyto: <b>+{qty} {name}</b> (łącznie {total}) → /workshop",
    "duel.metal_gain": "🪨 Trofeum pojedynku: <b>+{metal} Kamień</b> → /workshop",
    "quest.win_resources": "\n📦 Plus zestaw: po <b>{qty}</b> każdego surowca, 🪵 drewno i 🐄 krowa → /workshop",
    "profile.resources_line": "🧰 Surowce: {stock}\n",
    "menu.btn_goals": "🎯 Cele dnia",
    "menu.btn_raids": "🏴‍☠️ Najazdy",
    "menu.btn_workshop": "🔧 Warsztat",
    "farm.btn_workshop": "🔧 Warsztat",
    "farm.btn_app": "🏭 Farma w aplikacji",
    "menu.btn_app": "🚀 Aplikacja gry: farma, warsztat, najazdy",
    "app.btn_section": "🚀 OTWÓRZ W APLIKACJI",
    "app.goto_workshop": "🔧 <b>Warsztat</b> mieszka w aplikacji gry: surowce, receptury i crafting jednym tapnięciem.",
    "app.goto_raids": "🏴‍☠️ <b>Najazdy</b> mieszkają w aplikacji gry: zwiad, postawa obronna i rewanż.",
    "app.goto_station": "🛰 <b>Stacja drużyny</b> mieszka w aplikacji gry: postęp, wkłady i bonus dla całej drużyny.",
    "app.goto_market": "📈 <b>Giełda kotletów</b> jest wygodniejsza w aplikacji gry: oferty, sprzedaż i twoje zlecenia na jednym ekranie.",
    "mk.err_asset": "❌ Nie ma takiego towaru na giełdzie.",
    "mk.err_no_resource": "❌ Za mało surowca: w magazynie masz tylko {have}.",
    "mk.bid_filled_notify": "🙋 <b>Giełda: zlecenie kupna zrealizowane!</b> Zlecenie #{id}: kupiono <b>+{qty} {icon}</b> po {price} 🪙.",
    "sw.err_same": "❌ Nie można wymienić surowca na ten sam.",
    "sw.err_qty": "❌ W wymianie podaj ilość od 1 do {max} — zarówno tego, co oddajesz, jak i tego, co chcesz dostać.",
    "shop.btn_info": "ℹ️ Co daje każdy produkt",
    "sw.done_notify": "🔄 <b>Wymiana #{id} zrealizowana!</b> Oddano {give}, otrzymano {want}.",
    "ws.err_coins": "🔒 Za mało monet: potrzeba {need} 🪙, na koncie masz {have} 🪙.",
    "wk.eff_nitrogen": "❄️ Azot +40% na {h} godz.",
    "wk.eff_nuclear": "☢️ Nuklearne x5 na {h} godz.",
    "wk.eff_drone": "🛸 Mistrzowski Dron na {h} godz.",
    "wk.eff_shield": "🛡 Tarcza na {h} godz.",
    "wk.eff_unlimit": "⚡ Gry bez limitu na {h} godz.",
    "wk.eff_cutlet": "🥩 Kotlet ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ Ten przepis tygodnia jest już niedostępny.",
    "wk.err_limit": "🔒 Limit tego przepisu na ten tydzień wyczerpany ({limit}). Nowy tydzień rusza w poniedziałek o 00:00 UTC.",
    "games.resource_full": "📦 Magazyn {icon} pełny ({cap}) — nadwyżka przepada. Wydawaj, sprzedawaj albo powiększ magazyn w warsztacie.",
    "mk.err_storage_full": "📦 Za mało miejsca w magazynie: wolne {free}. Powiększ magazyn w warsztacie.",
    "mk.err_buyer_full": "📦 Kupujący ma pełny magazyn — tej transakcji nie da się teraz przeprowadzić (wolne {free}).",
    "ws.recipe_storage": "Powiększ magazyn do {cap}",
    "ws.done_storage": "📦 <b>Magazyn powiększony:</b> do {cap} każdego surowca. Na zawsze.",
    "ws.err_storage_max": "📦 Magazyn ma już maksymalny rozmiar.",
    "farm.boost_armor": "🛡 Cyber-pancerz poz. {level}: +{percent}% do wydobycia do {until} UTC",
    "farm.boost_station": "🛰 Stacja drużyny poz. {level}: +{percent}% do wydobycia",
    "clan.btn_station": "🛰 Stacja drużyny",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>WARSZTAT</b>\n"
        "..................................................\n"
        "🧰 Twoje surowce: {stock}\n"
        "⛏ Metal — Kamień-Papier-Nożyce i pojedynki · 💧 Wodór — Wyżej/Niżej · "
        "💎 Kryształy — Quiz · ⚙️ Części — Cyber-Sejf. Questy dają cały zestaw.\n\n"
        "🛡 Cyber-pancerz: <b>poziom {armor}/{armor_max}</b> (+{armor_pct}% do wydobycia za poziom, na 30 dni)\n"
        "🚀 Wahadłowiec: <b>{shuttle}</b> — prowizja giełdy {shuttle_fee}%, do {shuttle_qty} kotletów w zleceniu\n\n"
        "<i>✅ — surowców wystarczy, 🔒 — jeszcze nie. Jedno tapnięcie i gotowe.</i>"
    ),
    "ws.shuttle_yes": "zbudowany",
    "ws.shuttle_no": "niezbudowany",
    "ws.recipe_nitro_6h": "Azotowe Chłodzenie na 6 godz.",
    "ws.recipe_nuclear_3h": "Nuklearne Przyspieszenie na 3 godz.",
    "ws.recipe_drone_24h": "Mistrzowski Dron na dobę",
    "ws.recipe_shield_24h": "Tarcza przed najazdami na dobę",
    "ws.recipe_cutlet": "Synteza cyber-kotleta",
    "ws.recipe_armor": "Cyber-pancerz poz. {level}",
    "ws.recipe_shuttle": "Zbuduj Wahadłowiec",
    "ws.btn_shuttle_owned": "🚀 Wahadłowiec zbudowany",
    "ws.btn_armor_max": "🛡 Cyber-pancerz: maksimum",
    "ws.btn_refresh": "🔄 Odśwież",
    "ws.btn_farm": "🚜 Do farmy",
    "ws.noop": "Już na maksimum",
    "ws.toast": "Gotowe!",
    "ws.done_nitrogen": "❄️ <b>Azotowe Chłodzenie +40%</b> aktywne do {until} UTC.",
    "ws.done_nuclear": "☢️ <b>Nuklearne Przyspieszenie x5</b> aktywne do {until} UTC. Wiertacze zjadają ×3 kotletów!",
    "ws.done_drone": "🛸 <b>Mistrzowski Dron</b> chroni roboty do {until} UTC.",
    "ws.done_shield": "🛡 <b>Tarcza przed najazdami</b> trzyma do {until} UTC. Surowce są bezpieczne.",
    "ws.done_cutlet": "🥩 Zsyntetyzowano: <b>+{qty} cyber-kotlet</b> do magazynu. Tankuj w /farm!",
    "ws.done_armor": "🛡 <b>Cyber-pancerz poziom {level}!</b> Wydobycie farmy: <b>+{percent}%</b> na 30 dni.",
    "ws.done_shuttle": "🚀 <b>Wahadłowiec zbudowany!</b> Prowizja od twoich sprzedaży wynosi teraz {fee}%, w zleceniu do {qty} kotletów. Wahadłowiec jest tylko twój i na zawsze.",
    "ws.err_unknown": "❌ Nie ma takiego przepisu.",
    "ws.err_off": "🔧 Ten przepis jest teraz niedostępny.",
    "ws.err_locked": "🔒 Przepis odblokuje się za {hours} godz. — nowe przepisy otwierają się po jednym na dobę.",
    "ws.recipe_camo_12h": "Kamuflaż na 12 godz.",
    "ws.recipe_trap_24h": "Przynęta na dobę",
    "ws.recipe_drill_24h": "Trener postawy na dobę",
    "ws.recipe_forsage": "Dopalacz statku",
    "ws.recipe_economizer": "Ekonomizer",
    "ws.recipe_cargo": "Powiększona ładownia",
    "ws.recipe_thermos_24h": "Termos na kotlety na dobę",
    "ws.recipe_stamp": "Pieczęć giełdy",
    "ws.recipe_banner_24h": "Sztandar drużyny na dobę",
    "ws.recipe_dome_12h": "Kopuła drużyny na 12 godz.",
    "it.err_no_cooldown": "🚀 Nie ma czego przeładowywać — statek i tak jest gotowy do wylotu.",
    "it.err_forsage_daily": "🔥 Dopalacz już użyty — następny za {hours} godz.",
    "res.stone": "Kamień",
    "res.wood": "Drewno",
    "res.fire": "Ogień",
    "res.energy": "Prąd",
    "res.battery": "Baterie",
    "res.cow": "Krowy",
    "res.core": "Rdzeń",
    "tech.comm": "Łączność",
    "tech.scout": "Zwiad",
    "tech.attack": "Atak",
    "tech.defense": "Obrona",
    "tech.science": "Nauka",
    "tech.err_max": "🏆 To już maksymalny poziom.",
    "tech.err_unknown": "❌ Nie ma takiej technologii.",
    "tech.err_tool": "🧰 Potrzebujesz zestawu narzędzi poziomu {tool} — zbuduj go w Laboratorium.",
    "tech.err_cooldown": "⏳ Kolejny poziom będzie można zbadać za {hours} godz.",
    "tech.err_science": "📚 Naukę na poziomie {level} można zbadać, gdy wszystkie pozostałe technologie osiągną poziom {level}.",
    "ws.err_items_full": "📦 Magazyn przedmiotów jest pełny: najwyżej {max} przedmiotów. Włącz coś albo rozbuduj magazyn.",
    "post.scope_team": "Ranking drużyn",
    "post.scope_clan": "Ranking klanów",
    "post.scope_teams": "Drużyny i klany",
    "post.scope_solo": "Ranking indywidualny",
    "nom.farm_mined": "wyfarmić najwięcej monet",
    "nom.coins_earned": "zarobić najwięcej monet",
    "nom.duel_wins": "wygrać najwięcej pojedynków",
    "nom.duels_played": "rozegrać najwięcej pojedynków",
    "nom.quiz_wins": "dać najwięcej poprawnych odpowiedzi w quizie",
    "nom.rps_wins": "wygrać najwięcej partii w Kamień-Papier-Nożyce",
    "nom.safe_wins": "otworzyć najwięcej Cyber-Sejfów",
    "nom.game_wins_total": "wygrać najwięcej gier z botem",
    "nom.referrals": "przyprowadzić najwięcej aktywnych znajomych",
    "nom.stars_spent": "najbardziej wesprzeć ekosystem (Stars)",
    "nom.insta_reels": "czyj rolka na Instagramie wystrzeli najlepiej",
    "nom.youtube_shorts": "czyj film na YouTube Shorts wystrzeli najlepiej",
    "nom.tiktok": "czyj film na TikToku wystrzeli najlepiej",
    "bt.err_closed": "⏳ Ta bitwa jest już zamknięta.",
    "bt.err_no_entry": "Ta bitwa nie wymaga zgłoszenia.",
    "bt.err_no_team": "🏆 Najpierw dołącz do drużyny.",
    "bt.err_scope": "Ta bitwa nie jest dla twojego typu drużyny.",
    "bt.err_full": "✅ Zgłoszenie drużyny jest już pełne.",
    "bt.err_battery": "🔋 Brak baterii — zbuduj ją w warsztacie.",
    "horse.err_max": "🐎 Stajnia jest pełna — maksymalnie koni: {max}.",
    "horse.err_coins": "🪙 Koń kosztuje {price} 🪙 — na razie za mało.",
    "shuttle.err_none": "🚀 Najpierw zbuduj Wahadłowiec w warsztacie.",
    "cart.err_horse": "🛒 Wóz potrzebuje konia: wozów nie może być więcej niż koni (i więcej niż {max}).",
    "raid.err_need_tech": "🔬 Do najazdu potrzebna jest technologia „{tech}” poziomu 1 — zbadaj ją w Laboratorium.",
    "raid.err_battery": "🔋 Zwiad potrzebuje baterii — zrób ją w warsztacie.",
    "games.energy_gain": "⚡ Szczęście: +1 Prąd!",
    "ws.recipe_bonfire": "Ognisko: ogień z drewna i kamienia",
    "ws.recipe_battery": "Baterie (×2)",
    "ws.recipe_cart": "Wóz",
    "ws.recipe_meds_72h": "Apteczka na 72 godz.",
    "ws.err_resources": "🔒 Za mało: {kind} — potrzeba {need}, masz {have}. Wydobywaj w grach!",
    "ws.err_shuttle_owned": "🚀 Wahadłowiec jest już zbudowany — jeden na gracza.",
    "ws.err_armor_max": "🛡 Pancerz jest już na maksymalnym poziomie ({max}).",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>NAJAZDY</b>\n"
        "..................................................\n"
        "💧 Wodór: <b>{hydrogen}</b> (wylot kosztuje {fuel})\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ Postawa obronna: <b>{stance}</b>\n\n"
        "📊 Najazdów: <b>{attacks}</b> (udanych {attack_wins}) · odpartych: <b>{holds}/{defenses}</b>\n\n"
        "<i>Łup to wyłącznie surowce: {percent}% zapasu celu, nie więcej niż {cap} na surowiec. "
        "Monety, roboty i kotlety są nietykalne. Twój gest przeciwko postawie celu — "
        "decyzja kontra decyzja. Jeden wylot na {cooldown} godz.; rewanż — za darmo.</i>"
    ),
    "raid.ready_line": "Statek gotowy do wylotu",
    "raid.cooldown_line": "Ładowanie: jeszcze {minutes} min",
    "raid.shield_on": "Tarcza aktywna do {until} UTC",
    "raid.shield_newbie": "Ochrona nowicjusza (pierwsze {days} dni)",
    "raid.shield_off": "Brak tarczy — zbuduj ją w /workshop",
    "raid.stance_random": "losowa (wybierz w menu!)",
    "raid.btn_scout": "🔭 ZWIAD: znajdź cele",
    "raid.btn_revenge": "⚔️ Rewanż: {name}",
    "raid.btn_stance": "✊ Postawa obronna",
    "raid.btn_workshop": "🛡 Zbuduj tarczę",
    "raid.btn_refresh": "🔄 Odśwież",
    "raid.btn_back": "← Wstecz",
    "raid.btn_open": "🏴‍☠️ Otwórz najazdy",
    "raid.btn_again": "🏴‍☠️ Do najazdów",
    "raid.stance_pick": "✊ <b>Postawa obronna</b>\nUjawni ją dopiero wynik cudzego najazdu: gest atakującego przeciwko twojej postawie. Zmieniaj ją od czasu do czasu — przewidywalnych się okrada.",
    "raid.stance_saved": "Postawa: {stance}",
    "raid.scout": "🔭 <b>Zwiad znalazł cele.</b> Wylot pobierze {fuel} 💧. Wybieraj:",
    "raid.btn_target": "🎯 {name} · surowców ≈{total}",
    "raid.no_targets": "🔭 Zwiad nikogo nie znalazł: nie ma teraz odpowiednich celów (tarcze, ładowanie, nowicjusze). Zajrzyj później.",
    "raid.pick_move": "✊ <b>Twój gest?</b> Zagra przeciwko postawie obronnej celu. Wylot: −{fuel} 💧.",
    "raid.pick_move_revenge": "⚔️ <b>Rewanż! Twój gest?</b> Wylot jest darmowy i bez ładowania.",
    "raid.result_win": "🏴‍☠️ <b>NAJAZD UDANY!</b>\n{move} przeciwko {stance} u {name}.\nŁup: <b>{loot}</b>",
    "raid.result_draw": "😐 <b>Remis.</b> {move} przeciwko {stance} u {name}. Statek wrócił pusty, paliwo spłonęło.",
    "raid.result_lose": "💥 <b>OBRONA WYTRZYMAŁA.</b> {move} przeciwko {stance} u {name}.\nCel zgarnął: <b>{loot}</b>",
    "raid.result_footer": "<i>Surowce są w /workshop. Tarcza ochroni cię przed odwetem.</i>",
    "raid.victim_lost": "🚨 <b>Najechano cię!</b> {name}: {move} przeciwko twojej postawie {stance}.\nStracono: <b>{loot}</b>\n\n⚔️ Darmowy rewanż w ciągu {hours} godz. Tarcza — w /workshop.",
    "raid.victim_draw": "🛡 <b>Najazd odparty remisem.</b> {name}: {move} przeciwko twojej postawie {stance}. Nic nie stracono.",
    "raid.victim_held": "🛡 <b>Obrona wytrzymała!</b> {name}: {move} przeciwko twojej postawie {stance}.\nTrofeum obrony: <b>{loot}</b>",
    "raid.err_stance": "❌ Nieznany gest.",
    "raid.err_self": "🤨 Najazd na samego siebie? Nie.",
    "raid.err_gone": "❌ Cel niedostępny.",
    "raid.err_teammate": "🤝 Swoich nie okradamy — to ktoś z twojej drużyny.",
    "raid.err_shielded": "🛡 Cel ma tarczę. Wybierz inny.",
    "raid.err_revenge_gone": "❌ Okno rewanżu jest zamknięte.",
    "raid.err_cooldown": "⏳ Ładowanie: jeszcze {minutes} min.",
    "raid.err_victim_cooldown": "⏳ Ten cel był niedawno najechany (pauza {hours} godz.).",
    "raid.err_fuel": "💧 Za mało wodoru: potrzeba {need}, masz {have}. Wydobywa się go w Wyżej/Niżej.",

    # ---------------- ежедневные цели ----------------
    "goal.header": (
        "🎯 <b>CELE NA DZIŚ</b>\n"
        "..................................................\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 Skrzynia: <b>+{coins} 🪙</b> i <b>+{res}</b> losowego surowca\n"
        "🔥 Seria: <b>{streak}</b> dn. · każdy {every}. dzień z rzędu daje +{bonus} 🪙 do skrzyni\n\n"
        "<i>Cele odnawiają się o 00:00 UTC.</i>"
    ),
    "goal.status_progress": "⏳ Zamknij wszystkie trzy — i skrzynia jest twoja.",
    "goal.status_ready": "✅ <b>Wszystkie cele zamknięte! Odbierz skrzynię.</b>",
    "goal.status_claimed": "🎁 Dzisiejsza skrzynia już odebrana. Jutro — nowe cele!",
    "goal.btn_claim": "🎁 ODBIERZ SKRZYNIĘ",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 Odśwież",
    "goal.toast": "Skrzynia otwarta!",
    "goal.chest": "🎁 <b>SKRZYNIA OTWARTA!</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 Seria: {streak} dn.",
    "goal.err_claimed": "🎁 Dziś już odebrano.",
    "goal.err_not_done": "⏳ Jeszcze nie wszystkie cele są zamknięte.",
    "goal.win_quiz": "Wygraj {n} rund quizu",
    "goal.win_rps": "Wygraj {n} rund Kamień-Papier-Nożyce",
    "goal.win_hl": "Wygraj {n} rund Wyżej/Niżej",
    "goal.win_safe": "Otwórz Cyber-Sejf {n} razy",
    "goal.play_rounds": "Zagraj {n} rund w dowolne gry",
    "goal.duel": "Rozegraj pojedynek",
    "goal.bonus": "Odbierz codzienny kotlet na farmie",
    "goal.craft": "Zbuduj coś w warsztacie",
    "goal.raid": "Przeprowadź najazd",
    "goal.market_deal": "Zawrzyj transakcję na giełdzie",
    "goal.donate": "Wnieś surowce do stacji drużyny",

    # ---------------- станция команды ----------------
    "st.header": (
        "🛰 <b>STACJA DRUŻYNY „{team}”</b>\n"
        "..................................................\n"
        "Poziom: <b>{level}/{max}</b> → każdy wojownik dostaje <b>+{percent}%</b> do wydobycia farmy "
        "(+{per_level}% za poziom)\n\n"
        "📦 Do następnego poziomu:\n{progress}\n\n"
        "🧾 Ostatnie wkłady:\n{feed}\n\n"
        "🧰 Twoje surowce: {stock}\n"
        "<i>Stacja jest wspólna: buduje ją cała drużyna, bonus dostaje każdy. Opuścisz drużynę — stracisz bonus.</i>"
    ),
    "st.max_level": "🏁 Stacja ukończona — maksymalny poziom!",
    "st.feed_empty": "nikt jeszcze nic nie wniósł — bądź pierwszy(a)",
    "st.no_team": "🛰 Stację buduje drużyna. Dołącz do drużyny albo załóż własną — i budujcie razem.",
    "st.btn_find_team": "🏆 Drużyny i klany",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ Wszystko: {qty} {icon} {name}",
    "st.btn_refresh": "🔄 Odśwież",
    "st.btn_team": "🏆 Do drużyny",
    "st.toast": "Wniesiono +{qty} {icon}",
    "st.level_up": "🛰 <b>Stacja drużyny osiągnęła poziom {level}!</b> Wszyscy wojownicy mają teraz +{percent}% do wydobycia farmy.",
    "st.err_qty": "❌ Nieprawidłowa ilość.",
    "st.err_no_team": "❌ Nie jesteś w drużynie.",
    "st.err_max": "🏁 Stacja jest już ukończona (poziom {max}).",
    "st.err_resources": "🔒 Za mało surowca: masz {have}.",

    # ---------------- команды/кланы (основные поверхности) ----------------
    "clan.no_team": "⚠️ <b>Nie masz jeszcze drużyny!</b>\n\nMożesz zarejestrować własną ekipę już teraz, naciskając przycisk poniżej.",
    "clan.btn_create": "🏆 Załóż Drużynę za 100k",
    "clan.btn_members": "👥 SKŁAD DRUŻYNY",
    "clan.btn_leave": "🚪 Opuść drużynę",
    "clan.btn_dashboard": "🏆 Panel drużyny",
    "clan.status_clan": "👑 STATUS: KLAN IMPERIUM",
    "clan.status_team": "👥 STATUS: ZWYKŁA DRUŻYNA",
    "clan.dashboard": (
        "🏆 <b>PANEL INFORMACYJNY TWOJEJ DRUŻYNY</b>\n"
        "..................................................\n"
        "📌 Nazwa: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Kapitan ekipy: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Motto: <i>„{motto}”</i>\n"
        "🔮 Symbol emblematu: {symbol}\n\n"
        "👥 Skład: <b>{members} / {max_members} os.</b>\n"
        "..................................................\n"
        "👇 <b>NAWIGACJA:</b>"
    ),
    "clan.members_only": "🔒 Lista członków jest widoczna tylko dla członków tej drużyny!",
    "clan.members_gone": "❌ Drużyna została już rozwiązana.",
    "clan.members_header": (
        "👥 <b>SKŁAD DRUŻYNY „{name}”</b>\n"
        "🧠 — poziom intelektu w grze (rośnie tylko w /quiz)\n"
        "..................................................\n"
    ),
    "clan.members_footer": (
        "\n..................................................\n"
        "📄 Strona <b>{page} / {pages}</b> · Łącznie wojowników: <b>{members}</b>\n"
        "<i>Klikaj w @username kolegi z drużyny, aby do niego napisać, zebrać własny czat "
        "i wezwać ekipę na drużynowe rozgrywki!</i>"
    ),
    "clan.btn_prev": "⬅️ Wstecz",
    "clan.btn_next": "Dalej ➡️",
    "clan.join_ok": (
        "🎉 <b>GRATULACJE, JESTEŚ W GRZE!</b>\n\nDołączenie do drużyny <b>{name}</b> zakończone sukcesem!\n"
        "📍 Wpisz /my_team, aby sprawdzić skład!"
    ),
    "clan.leave_ok": "🚪 Drużyna <b>{name}</b> opuszczona. Jesteś teraz wolnym ptakiem!",
}

MINIAPP: dict[str, str] = {
    "qs_epicPaid": "⚡ z Bez limitu",
    "qs_paper": "📝 Rada: zapisuj szczegóły na kartce — uważni rozwiązują łatwiej.",
    "qs_total": "📚 Questy w bibliotece: {n}",
    "qs_daily": "Nowe dziś: {a}/{b}",
    "qs_dailyUnl": "⚡ Bez limitu — questy bez ograniczeń",
    "qs_locked": "🔒 do 00:00 UTC",
    "qs_lockedNote": "Ukończono dziś {b} nowe questy. Pozostałe otworzą się o 00:00 UTC, a ukończone możesz powtarzać do woli. ⚡ Bez limitu znosi ograniczenie.",
    "qs_epic": "⭐ EPIKA ·",
    "qr_btn": "⚠️ Zgłoś pytanie",
    "qr_title": "Co jest nie tak z pytaniem?",
    "qr_answer": "❌ Poprawna odpowiedź jest błędna",
    "qr_question": "✏️ Błąd lub literówka w pytaniu",
    "qr_dup": "🔁 Pytanie się powtarza",
    "qr_other": "🤔 Inne (niejasne, sporne)",
    "qr_thanks": "Dzięki! Pytanie zostanie sprawdzone i poprawione.",
    "qr_limit": "Na dziś wystarczy zgłoszeń — dzięki za pomoc!",
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
    "subtitle": "twoje growe imperium na jednym ekranie",
    "tab_passport": "📋 Paszport",
    "tab_farm": "🚜 Farma",
    "tab_goals": "🎯 Cele",
    "tab_workshop": "🔧 Warsztat",
    "tab_raids": "🏴‍☠️ Najazdy",
    "tab_market": "📈 Giełda",
    "tab_team": "🏆 Drużyna",
    "tab_friends": "🤝 Znajomi",
    "tab_shop": "🏪 Sklep",
    "tab_top": "👑 TOP",
    "passport": "📋 PASZPORT GRACZA",
    "coins": "🪙",
    "brain": "🧠 Poziom intelektu",
    "toNext": "do poziomu {n}: {left} poprawnych odpowiedzi w quizie (+{reward} 🪙)",
    "farm": "🚜 CYBER-FARMA",
    "robots": "Roboty (górnicy / wiertacze)",
    "intern": "Roboty Stażyści (1 🪙/h, wieczne)",
    "activateIntern": "🚀 AKTYWUJ ROBOTA STAŻYSTĘ",
    "claimIntern": "🎁 ODBIERZ STAŻYSTĘ ({n})",
    "internDone": "🤖 Twój Robot Stażysta zaczął zmianę!",
    "rank": "🎖 Ranga",
    "openFarm": "🏭 OTWÓRZ KOPALNIĘ",
    "farmScene": "🏭 TWOJA FARMA",
    "back": "← Wstecz",
    "minedVisit": "wydobyte podczas tej wizyty",
    "unit_intern": "Robot Stażysta",
    "unit_junior": "Młodszy Górnik",
    "unit_premium": "Cyber-Wiertacz",
    "eternal": "wieczny",
    "fueledAll": "zatankowane",
    "fueledPart": "{a} z {b} zatankowanych",
    "license": "licencja na 30 dni",
    "emptyFarm": "Kopalnia jest pusta. Aktywuj Robota Stażystę albo kup roboty w sklepie!",
    "madeBy": "Chcesz takiego bota dla swojego projektu? Napisz do @mister_telebot",
    "fueled": "Zatankowane wiertacze",
    "speed": "Tempo wydobycia",
    "perHour": "{v} 🪙/h",
    "fridge": "Lodówka",
    "inv": "Kotlety w magazynie",
    "burnout": "Najbliższe wypalenie",
    "boosts": "Aktywne wzmocnienia",
    "none": "brak",
    "resources": "🧰 Surowce",
    "bonusPct": "Stały bonus do wydobycia",
    "shuttle": "🚀 Wahadłowiec zbudowany",
    "resHint": "Każde zwycięstwo przynosi surowiec danej gry, a ze zdjętym limitem — bez ograniczeń. Wydawaj je w warsztacie.",
    "ref_title": "🤝 ZAPRASZAJ ZNAJOMYCH",
    "ref_rules": "{q} za każdego aktywnego znajomego — jednorazowo. Aktywny znajomy osiągnął {l}. poziom intelektu i odebrał {c} codzienne kotlety.",
    "ref_copy": "📋 Kopiuj",
    "ref_copied": "Link skopiowany!",
    "ref_share": "📤 Udostępnij",
    "ref_stats": "📊 TWOJA EKIPA",
    "ref_invited": "zaproszeni",
    "ref_qualified": "aktywni",
    "ref_earned": "zarobione",
    "ref_top": "🏆 KTO MA NAJWIĘCEJ ZNAJOMYCH",
    "ref_topHint": "✅ — aktywni znajomi, 👥 — wszyscy zaproszeni",
    "ref_empty": "Ranking jest jeszcze pusty — bądź pierwszy(-a)!",
    "wk_title": "🔥 PRZEPISY TYGODNIA",
    "wk_hint": "Przepisy czasowe: pojawiają się z decyzji hubu i znikają. Zdąż je stworzyć!",
    "wk_left": "pozostało wytworzeń w tym tygodniu: {n} z {m}",
    "st_cap": "📦 Magazyn: do {c} każdego surowca — nadwyżka wydobycia przepada",
    "bonusReady": "🎁 ODBIERZ CODZIENNY KOTLET",
    "bonusWait": "⏳ Bonus za {h} godz. {m} min",
    "bonusDone": "🎉 Kotlet w magazynie!",
    "team": "🏆 MOJA DRUŻYNA",
    "clan": "KLAN",
    "teamLabel": "Drużyna",
    "captain": "👑 Jesteś kapitanem!",
    "members": "Skład",
    "noTeam": "Nie masz jeszcze drużyny: dołącz do jednej z ruletki lub wyszukiwarki — albo załóż własną.",
    "tab_faq": "📚 FAQ",
    "tab_rules": "📜 Regulamin",
    "tm_roulette": "🎲 RULETKA DRUŻYN",
    "tm_rotate": "🔄 Pokaż inne drużyny",
    "tm_noFree": "Na razie brak wolnych drużyn — załóż własną!",
    "tm_search": "🔍 SZUKAJ DRUŻYNY",
    "tm_searchPh": "Nazwa lub jej fragment",
    "tm_searchBtn": "Szukaj",
    "tm_notFound": "Nie znaleziono drużyn o takiej nazwie",
    "tm_join": "💥 Dołącz",
    "tm_joined": "Jesteś w drużynie „{n}”!",
    "tm_create": "🏆 ZAŁÓŻ DRUŻYNĘ",
    "tm_hubHint": "Drużyna do 50 wojowników kosztuje {cost} 🪙. W sklepie można ją ulepszyć do Mega-Klanu na 1000 miejsc.",
    "tm_name": "Nazwa (do {n} znaków)",
    "tm_motto": "Motto (do {n} znaków)",
    "tm_symbol": "Godło — emoji (do {n} znaków)",
    "tm_createBtn": "Załóż za {cost} 🪙",
    "tm_created": "Drużyna „{n}” założona — jesteś kapitanem!",
    "tm_noMoney": "Potrzeba {cost} 🪙, a masz {b} 🪙",
    "tm_roster": "👥 SKŁAD DRUŻYNY",
    "tm_mottoL": "💬 Motto",
    "tm_leave": "🚪 Wyjdź z drużyny",
    "tm_leaveAsk": "Na pewno wyjść z drużyny „{n}”?",
    "tm_leaveAskCaptain": "Jesteś kapitanem: korona przejdzie na weterana drużyny. Na pewno wyjść z „{n}”?",
    "tm_left": "Nie jesteś już w drużynie",
    "mk_scopePublic": "🌐 Giełda ogólna",
    "mk_scopeTeam": "🏆 Giełda drużyny",
    "mk_teamHint": "Giełda drużyny „{t}”: oferty widzą i kupują tylko koledzy z drużyny, prowizja to zaledwie {f}%.",
    "mk_yourStock": "📦 Masz",
    "mk_yourCoins": "💰 Twoje monety",
    "tm_market": "🏪 GIEŁDA DRUŻYNY",
    "tm_marketBtn": "Otwórz giełdę drużyny",
    "tm_marketHint": "Handluj z kolegami z drużyny: prowizja {f}% zamiast {p}% na giełdzie ogólnej. W Mega-Klanie — tylko {c}%.",
    "hp_title": "🤝 WZAJEMNA POMOC",
    "hp_hint": "Brakuje surowca? Poproś drużynę. Każdy może podarować do {d} surowców na dobę.",
    "hp_today": "Podarowano dziś przez ciebie: {g} / {d}",
    "hp_empty": "Na razie nikt nie prosi o pomoc",
    "hp_give": "🎁 +{n}",
    "hp_kind": "Czego potrzebujesz",
    "hp_qty": "Ile (do {n})",
    "hp_ask": "🙏 Poproś o pomoc",
    "hp_given": "Podarowano: {q} {k} — dzięki za grę zespołową!",
    "hp_asked": "Prośba trafiła do drużyny!",
    "tab_storage": "📦 Magazyn",
    "tab_mines": "⛏ Kopalnie",
    "tab_info": "📚 Info",
    "tab_lab": "🔬 Laboratorium",
    "as_stone": "Kamień",
    "as_wood": "Drewno",
    "as_fire": "Ogień",
    "as_energy": "Prąd",
    "as_battery": "Baterie",
    "as_cow": "Krowy",
    "as_core": "Rdzeń",
    "tool_1": "Surowe narzędzia",
    "tool_2": "Narzędzia precyzyjne",
    "tool_3": "Kalibracja",
    "tool_4": "Nanotechnologie",
    "tech_comm": "ŁĄCZNOŚĆ",
    "tech_scout": "ZWIAD",
    "tech_attack": "ATAK",
    "tech_defense": "OBRONA",
    "tech_science": "NAUKA",
    "ws_needTool": "Potrzeba: {t}",
    "ws_teamItem": "🏆 Wyrób drużynowy — chroni całą drużynę (dla Mega-Klanu cena ×{x})",
    "eff_make": "zamienia surowiec w materiał w magazynie",
    "eff_cart": "wóz do konia: +1 oferty na giełdzie",
    "eff_meds": "bez chorób w najazdach i kopalniach",
    "it_meds": "APTECZKA",
    "mk_lots": "Otwarte oferty: {o} z {m} (🐎 {h} · 🛒 {c})",
    "badges": "🏅 Nagrody sezonów",
    "sk_stable": "🐎 STAJNIA",
    "sk_lots": "Ofert na giełdzie: {n}",
    "sk_buyHorse": "🐎 Kup konia za {p} 🪙",
    "sk_stableHint": "Każdy koń to +1 oferta na giełdzie, każdy wóz — kolejne +1 (wozów nie więcej niż koni). Monety wydane na konie przepadają.",
    "sk_horseBought": "🐎 Koń w stajni! Masz więcej ofert na giełdzie.",
    "sk_shuttleCharge": "🚀 ŁADUNEK WAHADŁOWCA",
    "sk_shuttleUntil": "🔋 Wahadłowiec naładowany do {t}",
    "sk_shuttleEmpty": "🪫 Wahadłowiec jest rozładowany — ulgi giełdowe nie działają.",
    "sk_chargeBtn": "🔋 Naładuj: 1 bateria = {d} dni",
    "raid_needTech": "Do najazdów potrzebne są 📡 łączność, 🔭 zwiad i ⚔️ atak poziomu 1.",
    "raid_toLab": "🔬 Do Laboratorium",
    "raid_scoutInfo": "Zwiad pokazuje cele: {n}. Paliwem najazdu jest wodór 💧",
    "raid_medsOn": "💊 Apteczka do {t}: choroby niestraszne",
    "raid_medsOff": "💊 Bez Apteczki 15% łupu przepada w lazarecie",
    "raid_note_sick": "🤒 Bez Apteczki część łupu przepadła w lazarecie",
    "mn_mined": "wydobyto {n} {i}",
    "mn_left": "do końca wydobycia: {t}",
    "mn_commNote": "Dochód trafia do wojowników z 📡 łącznością 1+; bez 💊 Apteczki co 7. godzina przepada.",
    "top_season": "🏆 Sezon",
    "top_rich": "💰 Najbogatsi",
    "top_seasonTitle": "🏆 SEZON {s}",
    "top_left": "Do końca sezonu: {t}",
    "top_myPlace": "Twoje miejsce: {p} z {n} · zarobiono {e} 🪙",
    "top_noPlace": "Nie ma cię jeszcze w tabeli — zagraj, a miejsce się pojawi.",
    "top_prizes": "Nagrody za sezon ogłasza organizator. TOP-10 dostaje odznakę sezonu w paszporcie.",
    "top_rules": "Liczą się monety zarobione w grze w ciągu miesiąca: farma, wygrane, pojedynki, questy, skrzynia, sprzedaż. Saldo nie jest zerowane.",
    "top_players": "👤 GRACZE SEZONU",
    "top_teams": "🏆 DRUŻYNY SEZONU",
    "top_empty": "Sezon dopiero się zaczął — bądź pierwszy(a)!",
    "top_noTeams": "W tym sezonie nie było jeszcze bitew.",
    "top_teamRules": "Punkty za miejsca w bitwach sezonu: 10 · 7 · 5 · 4 · 3 · 2 · 1.",
    "lab_tools": "🧰 NARZĘDZIA",
    "lab_toolsHint": "Zestawy się nie zużywają — otwierają trudne receptury i poziomy technologii.",
    "lab_nextTool": "Następny zestaw: {t}",
    "lab_craftTool": "Zbuduj zestaw",
    "lab_toolsMax": "🧬 Wszystkie zestawy zbudowane!",
    "lab_level": "Poziom {l} z {m}",
    "lab_max": "🏆 Maksymalny poziom",
    "lab_wait": "⏳ Następny poziom za {t}",
    "lab_up": "Zbadaj poziom {l}",
    "res_stone_src": "pojedynki, kopalnie, skrzynia",
    "res_wood_src": "zadania, kopalnie, skrzynia",
    "res_fire_src": "Ognisko w warsztacie",
    "res_energy_src": "szansa za zwycięstwo, kopalnie, skrzynia",
    "res_battery_src": "warsztat",
    "res_cow_src": "zadania, skrzynia 7. dnia, giełda",
    "res_core_src": "kopalnie i nagrody organizatora",
    "sk_items": "🧪 Przedmioty w magazynie: {n} / {m} (10% pojemności)",
    "sk_cutletsName": "Cyber-kotlety",
    "it_total": "W magazynie: {n} szt.",
    "bt_entry": "🔋 Zgłoszenie drużyny: {n} / {m}",
    "bt_entered": "✅ Drużyna bierze udział w bitwie o kopalnie",
    "bt_give": "Wpłać 🔋 (masz {n})",
    "bt_info": "O kopalnie walczą tylko drużyny ze zgłoszeniem: {f} 🔋, klan — {fc} 🔋. Zrzućcie się całą drużyną!",
    "bt_notAllowed": "Ta bitwa nie jest dla twojego typu drużyny",
    "mn_place": "🏆 nagroda za {p}. miejsce",
    "mn_soonShort": "Start: {d}",
    "top_events": "🎯 Akcje",
    "ev_empty": "Teraz nie ma akcji — zajrzyj później!",
    "ev_my": "Twoje miejsce: {p}",
    "ev_noPlace": "Nie ma cię jeszcze w tabeli — do dzieła!",
    "ev_manual": "Zwycięzców wybierze organizator",
    "ev_places": "Miejsc nagradzanych: {n}",
    "ev_prizes": "🎁 Nagrody",
    "ev_leaders": "Liderzy",
    "lab_sciGate": "📚 Poziom {l} odblokuje się, gdy wszystkie technologie osiągną poziom {l}",
    "lab_cooldown": "Po zbadaniu kolejny poziom odblokuje się za {d} dni.",
    "lab_done": "🔬 Gotowe! Poziom {l}",
    "lab_eff_comm": "Poziom 1 — najazdy i dochód z kopalni; każdy kolejny skraca ładowanie najazdu o {c} min",
    "lab_eff_scout": "Bez niego nie ma najazdów; celów w zwiadzie: 2 + poziom",
    "lab_eff_attack": "Bez niego nie ma najazdów; każdy poziom po pierwszym to +{a}% do łupu",
    "lab_eff_defense": "Każdy poziom to −{d}% do tego, co najeźdźca ci zabierze",
    "lab_eff_science": "+{s}% do wydobycia farmy i łupu za poziom. Długo się bada i wymaga ☢️ Rdzenia",
    "lab_how": "📖 Jak to działa",
    "lab_rule1": "Narzędzia buduje się raz: ⚒️ → 🛠 → 🔬 → 🧬. Bez odpowiedniego zestawu trudnej receptury ani poziomu nie weźmiesz.",
    "lab_rule2": "Po zbadaniu poziomu kolejny poziom tej samej technologii odblokuje się dokładnie po 30 dniach — każde ulepszenie jest cenne. Nauka rośnie za pozostałymi technologiami.",
    "lab_rule3": "☢️ Rdzeń zdobywa się tylko drużynowo: miejsca na podium w bitwach i pełna doba utrzymania kopalni.",
    "durDH": "{d} d {h} godz.",
    "durHM": "{h} godz. {m} min",
    "durM": "{m} min",
    "ws_locked": "🔒 Odblokuje się za {t}",
    "ws_toStorage": "📦 Gotowy przedmiot trafi do magazynu",
    "eff_camo": "nie widać cię w zwiadzie najazdów, a ty możesz atakować",
    "eff_trap": "najeźdźca, który przegra, oddaje ci dwa razy więcej",
    "eff_drill": "remis w obronie liczy się jako porażka najeźdźcy",
    "eff_thermos": "Wiertacze zjadają kotlety o 25% wolniej",
    "eff_banner": "+5% do wydobycia dla całej twojej drużyny",
    "eff_dome": "tarcza przed najazdami dla całej drużyny",
    "eff_forsage": "zeruje przeładowanie najazdu (raz na dobę)",
    "eff_economizer": "następny wylot bez wodoru",
    "eff_cargo": "łup z następnego najazdu ×1,5",
    "eff_stamp": "następna sprzedaż na giełdzie bez prowizji",
    "it_camo": "KAMUFLAŻ",
    "it_trap": "PRZYNĘTA",
    "it_drill": "TRENER POSTAWY",
    "it_thermos": "TERMOS NA KOTLETY",
    "it_banner": "SZTANDAR DRUŻYNY",
    "it_dome": "KOPUŁA DRUŻYNY",
    "it_forsage": "DOPALACZ STATKU",
    "it_economizer": "EKONOMIZER",
    "it_cargo": "POWIĘKSZONA ŁADOWNIA",
    "it_stamp": "PIECZĘĆ GIEŁDY",
    "it_oneShot": "jednorazowy",
    "it_charges": "⚡ Naładowano: {n}",
    "it_needTeam": "Przedmiot drużynowy — musisz należeć do drużyny.",
    "it_charged": "⚡ Naładowano! Zadziała przy następnym działaniu.",
    "it_forsaged": "🔥 Przeładowanie zresetowane — możesz lecieć!",
    "raid_armed": "⚡ W gotowości: {l}",
    "raid_guardUntil": "{n} do {t}",
    "raid_domeOn": "🛡 Kopuła drużyny do {t}",
    "raid_forsageBtn": "🔥 Dopalacz: zresetuj przeładowanie ({n})",
    "raid_note_economizer": "⛽ Ekonomizer: wylot bez wodoru",
    "raid_note_cargo": "📦 Ładownia: łup ×1,5",
    "raid_note_trap": "🪤 Przynęta celu: oddajesz dwa razy więcej",
    "raid_note_drill": "🎯 Trener postawy celu: remis liczy się jako twoja porażka",
    "mn_title": "⛏ MAPA KOPALŃ",
    "mn_closed": "🔒 Wyprawa do kopalni jest niemożliwa, dopóki nie ruszy bitwa drużyn lub klanów.",
    "mn_pick": "Kliknij kopalnię, aby poznać szczegóły.",
    "mn_info": "⛏ KOPALNIA",
    "mn_battle": "⚔️ BITWA „{t}” O KOPALNIĘ NR {n}",
    "mn_soon": "⏳ BITWA „{t}” O KOPALNIĘ NR {n} — START {d}",
    "mn_nom": "Kategoria: {n}",
    "mn_ends": "Koniec: {d}",
    "mn_leaders": "Liderzy teraz",
    "mn_noLeaders": "Nikt jeszcze nie zdobył punktów — twoja drużyna może być pierwsza!",
    "mn_myTeam": "🏆 TWOJA DRUŻYNA W KOPALNIACH",
    "mn_income": "Wydobycie: {n} surowców na godzinę dla całej drużyny",
    "mn_noIncome": "Jeszcze nie masz kopalni — wygraj bitwę drużyn, a kopalnia jest twoja na 72 godz.",
    "mn_noTeam": "Kopalnie zdobywają tylko drużyny — dołącz do drużyny albo załóż własną.",
    "mn_teamBtn": "🏆 Do drużyny",
    "mn_how": "📖 Jak to działa",
    "mn_rule1": "Każda bitwa drużyn i klanów toczy się dokładnie o jedną kopalnię. Wygrywa drużyna z najlepszym łącznym wynikiem wszystkich zawodników w kategorii bitwy.",
    "mn_rule2": "Zwycięzca trzyma kopalnię przez {h} godz.: każdy zawodnik drużyny dostaje {y} surowca z kopalni na godzinę. Więcej zawodników — więcej wydobycia.",
    "mn_rule3": "Potem kopalnia się zwalnia, ale zdobyć ją można tylko w nowej bitwie.",
    "mn_name": "⛏ KOPALNIA NR {n}",
    "mn_res": "Surowiec",
    "mn_holder": "Właściciel",
    "mn_free": "wolna",
    "mn_untilL": "Trzyma do",
    "mn_pumping": "Wydobywa: {n} {i} na godzinę",
    "mn_targetOf": "⚔️ O tę kopalnię trwa bitwa „{t}”",
    "mn_closedOne": "🔒 Zdobyć ją można tylko w bitwie drużyn — śledź ogłoszenia.",
    "raid_noFuel": "⛽ Statek nie jest gotowy do wylotu — potrzebne paliwo",
    "raid_shieldTitle": "🛡 TARCZA PRZED NAJAZDAMI",
    "raid_shieldActive": "AKTYWNA",
    "raid_shieldInactive": "NIEAKTYWNA",
    "raid_shieldHint": "Gdy tarcza działa, nikt cię nie najedzie. Tarczę budujesz w warsztacie, a trafia do magazynu — włączysz ją, kiedy będzie potrzebna.",
    "raid_toStorage": "📦 Otwórz magazyn",
    "sk_res": "📦 SUROWCE W MAGAZYNIE",
    "sk_expand": "🔧 Powiększ magazyn",
    "sk_cutlets": "🥩 CYBER-KOTLETY",
    "sk_cutletsHint": "Paliwo dla Cyber-Wiertaczy: 1 kotlet — doba pracy.",
    "sk_refuel": "🚜 Zatankuj na farmie",
    "it_nitrogen": "AZOTOWE CHŁODZENIE +40%",
    "it_nuclear": "NUKLEARNE PRZYSPIESZENIE X5",
    "it_drone": "MISTRZOWSKI DRON",
    "it_shield": "TARCZA PRZED NAJAZDAMI",
    "it_unlimit": "BEZLIMIT GIER",
    "it_unlimitDesc": "wygrane w grach bez dziennego limitu",
    "it_hours": "{h} godz.",
    "it_use": "Włącz",
    "it_empty": "Pusto. Zbuduj coś w warsztacie — przedmiot trafi tutaj.",
    "it_toWorkshop": "🔧 Do warsztatu",
    "it_active": "✅ Działa do {t}",
    "it_used": "✅ Włączono! Działa do {t}",
    "it_stored": "📦 Gotowe! Przedmiot leży w magazynie — włącz go w zakładce „Magazyn”, gdy będzie potrzebny.",
    "sk_shuttle": "🚀 WAHADŁOWIEC",
    "sk_shuttleOn": "Masz: prowizja giełdy {f}%, szersze limity zleceń.",
    "sk_shuttleOff": "Jeszcze nie masz. Budowany w warsztacie.",
    "sk_armor": "🦾 CYBER-PANCERZ",
    "sk_armorOn": "Poziom {l} z {m}: +{p}% do wydobycia do {t}.",
    "sk_armorOff": "Nie założony. Każdy poziom daje +{p}% do wydobycia na 30 dni.",
    "sk_store": "🏗 POWIĘKSZENIE MAGAZYNU",
    "sk_storeLvl": "Pojemność: {c} każdego surowca.",
    "sk_storeMax": "🏆 Maksymalny magazyn!",
    "hp_who": "Dawać mogą gracze od poziomu intelektu {l} i po {c} codziennych kotletach.",
    "top": "👑 TOP-100 BOGACZY EKOSYSTEMU",
    "shop": "🏪 SKLEP",
    "shopFarm": "🚜 DLA FARMY",
    "shopGames": "🕹️ DO GIER",
    "shopHint": "Płatność oficjalnymi Telegram Stars — tutaj, jednym tapnięciem.",
    "paid": "🎉 Opłacone! Towar jest już na twoim koncie.",
    "payFail": "Płatność nie przeszła. Spróbuj jeszcze raz.",
    "oldClient": "Zaktualizuj Telegram, aby kupować w aplikacji, albo otwórz sklep w czacie bota.",
    "ctaNoRobots": "💤 Farma jest prawie pusta! Spraw sobie mocniejszego robota — 🪙 będą kapać całą dobę.",
    "ctaHungry": "🚨 Wiertacze głodują ({n} bez paliwa) — wydobycie stoi!",
    "ctaLowFuel": "⚠️ Kotletów starczy na mniej niż dobę pracy Wiertaczy.",
    "ctaShopBtn": "🛒 Do sklepu",
    "footer": "The whole game in one app",
    "noProfile": "Nie znaleziono profilu. Otwórz bota i naciśnij /start!",
    "blocked": "Konto zablokowane przez administrację.",
    "deleting": "Twoje konto czeka na usunięcie. Rozmyśliłeś(-aś) się? Anuluj usunięcie w czacie bota.",
    "error": "Nie udało się załadować danych. Spróbuj później.",
    "outside": "Otwórz tę aplikację z Telegram-bota ROFL HUB.",
    "robotsTitle": "🤖 TWOJE ROBOTY",
    "buyMore": "🛒 Kup",
    "rateShort": "{v} 🪙/h",
    "refuelOne": "🥩 Zatankuj 1",
    "refuelAll": "⚡ Zatankuj wszystkie",
    "refueled": "Zatankowano: {n} 🥩",
    "res_metal_src": "PKN",
    "res_hydrogen_src": "Wyżej/Niżej",
    "res_crystal_src": "Quiz",
    "res_parts_src": "Cyber-Sejf",
    "resWhere": "gdzie zdobywać",
    "ws_title": "🔧 WARSZTAT",
    "ws_hint": "Surowce z gier zamieniają się w ulepszenia. Starczy surowców — naciśnij „Zbuduj”.",
    "ws_craft": "Zbuduj",
    "ws_owned": "✅ Już masz",
    "ws_crafted": "Gotowe! Ulepszenie już działa.",
    "ws_armor": "🛡 Cyber-pancerz",
    "ws_armorLvl": "poziom {l}/{m} · +{p}% za poziom na 30 dni",
    "ws_shuttleOn": "🚀 Wahadłowiec zbudowany: prowizja giełdy {fee}%",
    "ws_shuttleOff": "🚀 Brak Wahadłowca: prowizja giełdy {fee}%",
    "eff_nitrogen": "+40% do wydobycia wszystkich robotów",
    "eff_nuclear": "×5 do wydobycia, Wiertacze jedzą ×3 kotletów",
    "eff_drone": "roboty się nie starzeją",
    "eff_shield": "nikt nie może cię najechać",
    "eff_cutlet": "1 cyber-kotlet do magazynu (drogo: paliwo w sklepie wychodzi taniej)",
    "eff_armor": "+10% do wydobycia za poziom na 30 dni",
    "eff_storage": "więcej miejsca na surowce — na zawsze",
    "eff_shuttle": "tylko twój: prowizja 5% od twoich sprzedaży i zlecenia do 500 kotletów — na zawsze",
    "raid_title": "🏴‍☠️ NAJAZDY",
    "raid_how": "📖 Jak to działa",
    "raid_rule1": "Wybierasz gest, a cel ma z góry ustawioną postawę obronną. O wyniku decyduje kamień-papier-nożyce: to pojedynek decyzji, a nie loteria.",
    "raid_rule2": "Zwycięstwo: zabierasz {pct}% każdego surowca celu, do {cap} na surowiec. Porażka: oddajesz celowi {fpct}% swoich, do {fcap}. Remis: paliwo spłonęło.",
    "raid_rule3": "Łupem padają tylko surowce. Monety, roboty i kotlety są całkowicie bezpieczne. Nowicjusze są chronieni przez {days} dni, członków własnej drużyny atakować nie można.",
    "raid_rule4": "Wylot kosztuje {fuel} 💧 wodoru, następny — za {cd} godz. Jeśli ktoś cię najechał, rewanż jest darmowy przez {rh} godz.",
    "raid_fuel": "💧 Wodór",
    "raid_ready": "🚀 Statek gotowy do wylotu",
    "raid_cooldown": "⏳ Przeładowanie: {m} min",
    "raid_shieldOn": "🛡 Tarcza do {t}",
    "raid_shieldNewbie": "🛡 Ochrona nowicjusza",
    "raid_shieldOff": "🛡 Brak tarczy — zbuduj ją w warsztacie",
    "raid_stance": "✊ TWOJA POSTAWA OBRONNA",
    "raid_stanceHint": "Nią odpierasz cudze najazdy. Zmieniaj ją czasem — przewidywalnych okrada się częściej.",
    "raid_stanceNone": "Postawa nie wybrana — będzie losowa",
    "raid_stanceSaved": "Postawa zapisana",
    "raid_stats": "Najazdy: {a} (udane: {w}) · odparte: {h} z {d}",
    "raid_scout": "🔭 ZWIAD: znajdź cele",
    "raid_targets": "🎯 Wybierz cel",
    "raid_res": "surowców ≈{n}",
    "raid_noTargets": "Brak odpowiednich celów: tarcze, przeładowania, nowicjusze. Zajrzyj później.",
    "raid_pickMove": "✊ Twój gest przeciw postawie gracza {name}",
    "raid_revenge": "⚔️ REWANŻ",
    "raid_revengeBtn": "⚔️ Oddaj cios: {name}",
    "raid_win": "🏴‍☠️ Najazd udany!",
    "raid_draw": "😐 Remis — statek wrócił pusty",
    "raid_lose": "💥 Obrona wytrzymała",
    "raid_vs": "{m} przeciw {s}",
    "raid_loot": "Łup: {l}",
    "raid_lost": "Oddano celowi: {l}",
    "rock": "🪨 Kamień",
    "scissors": "✂️ Nożyce",
    "paper": "📄 Papier",
    "mk_title": "📈 GIEŁDA",
    "mk_stats": "Zlecenia: {o} · kotlety: {c} · najlepsza cena: {b} 🪙",
    "mk_feeLine": "Prowizja {f}% od sprzedaży spala się — tarcza przed inflacją",
    "mk_inv": "🥩 W twoim magazynie: {n}",
    "mk_offers": "🛒 OFERTY",
    "mk_empty": "Na razie brak ofert — wystaw swoją jako pierwszy(a)!",
    "mk_offer": "{q} 🥩 × {p} 🪙",
    "mk_buyHow": "Ile kupić?",
    "mk_all": "Wszystkie {q}",
    "mk_sellTitle": "💰 SPRZEDAJ KOTLETY",
    "mk_qty": "Ile kotletów",
    "mk_price": "Cena za sztukę, 🪙",
    "mk_preview": "Transakcja {t} 🪙 · dostaniesz {g} 🪙 · spłonie {f} 🪙",
    "mk_sell": "Wystaw na giełdę",
    "mk_limits": "Do {q} kotletów w zleceniu, do {o} otwartych zleceń",
    "mk_my": "📋 MOJE ZLECENIA",
    "mk_cancel": "Wycofaj",
    "mk_bought": "Kupiono {q} 🥩 za {t} 🪙",
    "mk_listed": "Zlecenie wystawione! Dam znać, gdy ktoś kupi.",
    "mk_cancelledMsg": "Zlecenie wycofane, kotlety wróciły do magazynu",
    "st_title": "🛰 STACJA DRUŻYNY",
    "st_level": "Poziom {l} z {m}",
    "st_bonus": "+{p}% do wydobycia dla każdego członka drużyny",
    "st_next": "Poziom {n} wymaga po {c} każdego surowca",
    "st_max": "🏁 Stacja ukończona!",
    "st_feed": "🧾 Ostatnie wkłady",
    "st_feedEmpty": "Nikt jeszcze nic nie wpłacił — bądź pierwszy(a)",
    "st_donate": "Wpłać",
    "st_all": "Wszystko",
    "st_done": "Wpłacono!",
    "st_hint": "Buduje cała drużyna, bonus dostaje każdy. Wyjście z drużyny — koniec bonusu.",
    "st_off": "Stacja jest chwilowo w przerwie technicznej",
    "goals_title": "🎯 CELE NA DZIŚ",
    "goals_chest": "🎁 Skrzynia za wszystkie trzy: +{c} 🪙 i +{r} losowego surowca",
    "goals_streak": "🔥 Seria: {s} dn. · każdy {e}. dzień z rzędu +{b} 🪙",
    "goals_claim": "🎁 ODBIERZ SKRZYNIĘ",
    "goals_claimed": "🎁 Dzisiejsza skrzynia odebrana. Jutro nowe cele!",
    "goals_reset": "Cele odnawiają się o 00:00 UTC",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · seria {s} dn.",
    "as_cutlet": "Kotlety",
    "as_metal": "Metal",
    "as_hydrogen": "Wodór",
    "as_crystal": "Kryształy",
    "as_parts": "Części",
    "mk_index": "📈 INDEKS GIEŁDY",
    "mk_chart": "📊 CENA Z 7 DNI",
    "mk_noTrades": "Na razie bez transakcji — bądź pierwszy(a)!",
    "mk_avg": "Średnia cena z tygodnia: {p} 🪙 · sprzedano: {v}",
    "mk_asks": "🛒 SPRZEDAJĄ",
    "mk_bids": "🙋 KUPUJĄ",
    "mk_noBids": "Na razie brak zleceń kupna",
    "mk_sellTo": "Sprzedaj",
    "mk_sellHow": "Ile sprzedać?",
    "mk_bidTitle": "🙋 ZLECENIE KUPNA",
    "mk_bidHint": "Monety są zamrożone w zleceniu do transakcji. Wycofasz zlecenie — monety wrócą.",
    "mk_bid": "Złóż zlecenie kupna",
    "mk_bidPreview": "Zostanie zamrożone {t} 🪙",
    "mk_have": "Masz: {n}",
    "mk_floor": "Kotlet nie taniej niż {p} 🪙: paliwo ze sklepu za Gwiazdki zawsze wychodzi korzystniej",
    "mk_side_sell": "sprzedaję",
    "mk_side_buy": "kupuję",
    "mk_listedBid": "Zlecenie kupna złożone! Monety zamrożone do transakcji.",
    "mk_sold": "Sprzedano {q}, otrzymano {g} 🪙 po prowizji",
    "mk_shuttleNote": "🚀 Twój Wahadłowiec: prowizja {f}% od twoich sprzedaży",
    "sw_title": "🔄 WYMIANA SUROWCÓW",
    "sw_hint": "Oddaj nadmiar — weź to, czego potrzebujesz. Bez monet i bez prowizji.",
    "sw_give": "Oddajesz",
    "sw_want": "Chcesz dostać",
    "sw_qty": "Ile",
    "sw_create": "Zaproponuj wymianę",
    "sw_take": "Wymień",
    "shop_info": "ℹ️ Co daje każdy produkt",
    "sw_youGet": "Dostajesz",
    "sw_youGive": "W zamian oddajesz",
    "sw_takeBtn": "Wymień — oddaj {x}",
    "sw_mineLine": "Oddajesz {g} → chcesz dostać {w}",
    "sw_qtyErr": "Podaj ilość większą od zera w obu polach",
    "sw_empty": "Na razie brak propozycji wymiany",
    "sw_mine": "Moje propozycje",
    "sw_done": "Wymiana zrealizowana!",
    "sw_created": "Propozycja wystawiona, surowce odłożone",
    "sw_cancelled": "Propozycja wycofana, surowce wróciły",
    "ws_armorUntil": "🛡 Pancerz działa do {t}",
    "featureOff": "⚙️ Sekcja w przerwie technicznej",
    "done": "Gotowe!",
    "loading": "⏳ Ładowanie…",
}

COMMANDS: dict[str, str] = {
    "app": "🎮 Otwórz Mini App",
    "menu": "📱 Menu główne",
    "profile": "👤 Mój profil i paszport",
    "farm": "🚜 Cyber-farma i tankowanie",
    "shop": "🏪 Sklep (Telegram Stars)",
    "games": "🕹️ Wszystkie gry przeciwko botowi",
    "quiz": "🧠 Quiz: 15 sekund na odpowiedź",
    "duel": "⚔️ Pojedynek 1 na 1 o stawkę",
    "quests": "🗺️ Questy: historie z wyborami",
    "my_team": "🏆 Moja drużyna i skład",
    "invite": "🤝 Link polecający: +500 za aktywnego znajomego",
    "transfer": "🔄 Przelej monety graczowi",
    "market": "📈 Giełda kotletów: kup lub sprzedaj",
    "sell": "💰 Sprzedaj kotlety: /sell ilość cena",
    "my_stats": "📊 Moje statystyki",
    "faq": "📚 Najczęstsze pytania",
    "rules": "📜 Regulamin użytkownika",
    "paysupport": "🛟 Wsparcie płatności",
    "workshop": "🔧 Warsztat: surowce w ulepszenia",
    "raid": "🏴‍☠️ Najazdy: zwiad i rewanż",
    "goals": "🎯 Cele dnia i skrzynia",
    "station": "🛰 Stacja drużyny: wspólny projekt",
}
