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
        "- Kanał rozrywki i wiedzy ROFL HUB CHANNEL\n"
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
        "..................................................\n\n"
        "👤 <b>PROFIL OSOBISTY I PASZPORT:</b>\n"
        "• /start — Rozpocznij wprowadzenie i zarejestruj konto\n"
        "• /profile — Twój paszport, saldo i drużyna w czasie rzeczywistym\n"
        "• /my_stats — Twoje statystyki historyczne z ostatnich 30 dni\n\n"
        "🚜 <b>CYBER-FARMA I AUTOMATYZACJA:</b>\n"
        "• /farm — Hub paliwowy: tankowanie i tempo wydobycia robotów\n"
        "• /shop — Marketplace: zakup górników, kotletów i ulepszeń huba\n\n"
        "🕹️ <b>POKÓJ GIER:</b>\n"
        "• /games — Inline-hub wszystkich gier przeciwko botowi\n"
        "• /quiz — Quiz na czas: 15 sekund na odpowiedź, poziomy i bonusy\n"
        "• /duel — POJEDYNKI 1 na 1 z żywymi graczami: stoły 10/100/1000\n"
        "• /quests — QUESTY: kryminały, komedie i łamigłówki z nagrodami\n"
        "• /rps, /high_low, /safe — Szybkie gry o monety\n\n"
        "👥 <b>ZARZĄDZANIE EKIPĄ:</b>\n"
        "• /create_team — Zarejestruj własną drużynę za 100 000 🪙\n"
        "• /my_team — Panel ekipy i SKŁAD DRUŻYNY z poziomami 🧠\n"
        "• /all_teams — Ruletka losowych drużyn\n\n"
        "💸 <b>PIENIĄDZE I ZNAJOMI:</b>\n"
        "• /invite — Twój link polecający: +1000 🪙 za znajomego\n"
        "• /transfer — Przelej monety innemu graczowi\n\n"
        "📚 <b>POMOC I ZASADY:</b>\n"
        "• /faq — Pełny przewodnik po ekosystemie (otwiera się w Mini App)\n"
        "• /rules — Regulamin użytkownika\n"
        "..................................................\n"
        "<i>⚙️ Korzystaj ze stałego dwukolumnowego panelu gry na dole ekranu, aby błyskawicznie nawigować między sekcjami!</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>WITAJ W STREFIE GIER ROFL HUB!</b>\n"
        "..................................................\n\n"
        "Tutaj możesz zmierzyć się z botem w szybkich starciach albo przejść "
        "intelektualny sprint — i zgarnąć pulę albo spłukać się do zera!\n\n"
        "💸 Zwycięstwo daje: <b>+2 🪙</b> (Cyber-Sejf: <b>+5</b>)\n"
        "💀 Porażka lub remis kosztuje: <b>-1 🪙</b>\n"
        "🧠 W Quizie — licznik 15 sekund i poziomy intelektu: 1. poziom to 10 poprawnych odpowiedzi i <b>+100 🪙</b>, "
        "każdy kolejny poziom jest o 10 odpowiedzi dłuższy, ale nagroda rośnie o 100!\n\n"
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
        "..................................................\n\n"
        "Najważniejsze w skrócie:\n"
        "🚜 Roboty wydobywają monety całą dobę: Młodszy Górnik — 5/h bez paliwa, "
        "Cyber-Wiertacz — 10/h, a KAŻDY Wiertacz zjada swój własny cyber-kotlet raz na dobę. "
        "Wszystkie roboty żyją 30 dni (Mistrzowski Dron wstrzymuje zużycie).\n"
        "🧠 Quiz: 15 sekund na odpowiedź, poziomy intelektu z rosnącymi nagrodami.\n"
        "⚔️ Pojedynki z żywymi graczami przy stołach 10/100/1000 🪙.\n"
        "🏆 Drużyny do 50 wojowników (Mega-Klan — do 1000) i okazjonalne Bitwy z nagrodami dla każdego.\n\n"
        "..................................................\n"
        "👇 <b>Pełny przewodnik ze wszystkimi mechanikami — pod przyciskiem:</b>"
    ),
    "faq.btn_open": "📖 OTWÓRZ PEŁNY PRZEWODNIK",
    "rules.teaser": (
        "📜 <b>REGULAMIN UŻYTKOWNIKA ROFL HUB</b>\n"
        "..................................................\n\n"
        "Najważniejsze w dwóch słowach:\n"
        "🪙 Monety i wszystkie przedmioty w grze to wirtualne elementy rozrywkowe: "
        "nie są pieniędzmi i nie podlegają wymianie na prawdziwe środki.\n"
        "💫 Zakupy — wyłącznie przez oficjalne Telegram Stars; towary cyfrowe dostarczane są "
        "natychmiast, a przy błędzie dostawy Stars wracają automatycznie.\n"
        "🛡️ Nie zbieramy numerów telefonów, lokalizacji ani danych osobowych.\n"
        "🤝 Zakazane są obelgi, sztuczne nabijanie statystyk i multikonta — za naruszenie grozi blokada.\n\n"
        "..................................................\n"
        "👇 <b>Pełny tekst regulaminu i zastrzeżenia — pod przyciskiem:</b>\n"
        "<i>⚖️ Korzystając z bota, potwierdzasz akceptację warunków.</i>"
    ),
    "rules.btn_open": "📜 OTWÓRZ PEŁNY REGULAMIN",
    "quest.list_header": (
        "🗺️ <b>QUESTY ROFL HUB</b>\n"
        "..................................................\n\n"
        "Interaktywne historie z wyborami i rozgałęzieniami: kryminały, komedie, łamigłówki. "
        "Pierwsze zwycięstwo w każdym queście daje monety, a powtarzać możesz do woli!\n"
        "🌐 <i>Historie questów są na razie po rosyjsku — polski pakiet już w drodze.</i>\n\n"
        "👇 <b>Wybierz historię:</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} 🪙 za pierwsze zwycięstwo\n"
        "..................................................\n\n"
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
    "farm.intern_line": "• Roboty Stażyści ({rate} 🪙/h, wieczne): <code>{count}</code>\n",
    "farm.intern_hint": "🎁 Masz darmowego Robota Stażystę! Naciśnij przycisk poniżej — będzie wydobywać 1 🪙 na godzinę na zawsze.",
    "farm.dashboard": (
        "🚜 <b>CENTRALNY HUB PALIWOWY ROFL HUB</b>\n"
        "..................................................\n\n"
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
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>STAN AUTOMATYCZNEJ LODÓWKI:</b>\n"
        "🥩 Zapas paliwa: <b>{fridge} / {capacity} szt.</b>\n"
        "💼 Kotlety w magazynie: <code>{inv} szt.</code>\n\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
        "🆔 Twój ID Paszportu: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Monety teraz: <b>{balance} 🪙</b>\n"
        "🏆 Twój status: <b>{team}</b>\n"
        "🧠 Poziom intelektu: <b>{level}</b> · do poziomu {next_level}: "
        "<b>{left}</b> poprawnych odpowiedzi w /quiz (nagroda: +{reward} 🪙)\n\n"
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
        "..................................................\n\n"
        "🧠 Poziom intelektu w grze: <b>{level}</b> (łącznie poprawnych odpowiedzi: {total})\n"
        "🎮 Rozegranych rund w pojedynkach: <b>{played}</b>\n"
        "🏆 Zwycięstw nad rywalami: <code>{won}</code>\n"
        "👥 Zaproszonych aktywnych znajomych: <b>{refs}</b>\n\n"
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
        "⚡ Zdejmij limit na 24 godziny — 5 ★, na 30 dni — 99 ★ (sekcja „Do gier” w /shop)."
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
        "..................................................\n\n"
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
    "rank.dead": "DEAD",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>PROGRAM POLECEŃ ROFL HUB</b>\n"
        "..................................................\n\n"
        "Zapraszaj znajomych i otrzymuj <b>+{bonus} 🪙</b> za każdego, "
        "kto zarejestruje się przez twój osobisty link!\n\n"
        "🔗 <b>Twój link (kliknij, aby skopiować):</b>\n<code>{link}</code>\n\n"
        "📊 <b>TWOJE STATYSTYKI:</b>\n"
        "👥 Zaproszonych znajomych: <b>{invited}</b>\n"
        "💰 Zarobione na poleconych: <b>{earned} 🪙</b>\n\n"
        "..................................................\n"
        "<i>Podsyłaj link znajomym, wrzucaj na czaty klasowe i do social mediów — im większa ekipa, tym szybciej rośnie twoje saldo!</i>"
    ),
    "ref.btn_share": "📣 Udostępnij link",
    "ref.share_text": "Wbijaj do ekosystemu gier ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Podwójna nagroda:</b> gdy zaproszony znajomy rozegra {rounds} "
                           "rund, dostajesz kolejne <b>+{bonus} 🪙</b> i <b>{cutlets} 🥩 cyber-kotlet</b>!"),
    "ref.qualified_notify": ("🤝 <b>Twój znajomy wkręcił się: już {rounds} rund!</b>\n"
                             "Za kwalifikowanego poleconego dostajesz <b>+{bonus} 🪙</b> i <b>{cutlets} 🥩 cyber-kotlet</b> do magazynu. "
                             "Zapraszaj dalej!"),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>PRZELEW MONET DO INNEGO GRACZA</b>\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
        "Wszystkie towary ROFL HUB są cyfrowe i dostarczane natychmiast po opłaceniu.\n\n"
        "⚙️ <b>Jeśli płatność przeszła, a towar nie dotarł:</b>\n"
        "bot automatycznie zwraca Stars przy błędzie dostawy. Jeśli tak się nie stało — "
        "przyślij tutaj numer płatności (jest na paragonie, format <code>xxxx...</code>) i opisz problem. "
        "Administracja sprawdzi płatność w bazie i rozwiąże sprawę w ciągu 24 godzin.\n\n"
        "💫 <b>Polityka zwrotów:</b>\n"
        "zwrot jest możliwy, jeśli towar nie został dostarczony albo wydano go z błędem. "
        "Poprawnie dostarczone towary cyfrowe nie podlegają zwrotowi.\n\n"
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
    "dlv.err_intern_refs": "Ulepszenie wymaga {need} kwalifikowanych znajomych (po 30 rund); masz {have}.",
    "mk.header": "📈 <b>GIEŁDA KOTLETÓW</b>\n..................................................\n\nOtwarte zlecenia: <b>{orders}</b> · kotletów w ofercie: <b>{cutlets}</b> · najlepsza cena: <b>{best}</b>\nProwizja hubu: <b>{fee}%</b> od sprzedaży (spalana — tarcza antyinflacyjna)\n🥩 W twoim magazynie: <b>{inv}</b> kotletów\n\n{body}\n\n<i>Kliknij zlecenie, aby kupić. Sprzedaż: /sell.</i>",
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
    "mk.order_cancelled": "↩️ Zlecenie #{id} wycofane: <b>{qty} kotletów</b> wróciło do magazynu.",
    "mk.err_qty": "❌ Ilość: od 1 do {max} kotletów w zleceniu.",
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
    "duel.metal_gain": "⛏ Trofeum pojedynku: <b>+{metal} Metal</b> → /workshop",
    "quest.win_resources": "\n📦 Plus zestaw surowców: po <b>{qty}</b> każdego → /workshop",
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
        "..................................................\n\n"
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
    "ws.err_resources": "🔒 Za mało: {kind} — potrzeba {need}, masz {have}. Wydobywaj w grach!",
    "ws.err_shuttle_owned": "🚀 Wahadłowiec jest już zbudowany — jeden na gracza.",
    "ws.err_armor_max": "🛡 Pancerz jest już na maksymalnym poziomie ({max}).",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>NAJAZDY</b>\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
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
        "..................................................\n\n"
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
        "..................................................\n\n"
        "📌 Nazwa: <b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 Kapitan ekipy: 🧠{captain_level} · <b>{captain}</b>\n"
        "💬 Motto: <i>„{motto}”</i>\n"
        "🔮 Symbol emblematu: {symbol}\n\n"
        "👥 Skład: <b>{members} / {max_members} os.</b>\n"
        "..................................................\n\n"
        "👇 <b>NAWIGACJA:</b>"
    ),
    "clan.members_only": "🔒 Lista członków jest widoczna tylko dla członków tej drużyny!",
    "clan.members_gone": "❌ Drużyna została już rozwiązana.",
    "clan.members_header": (
        "👥 <b>SKŁAD DRUŻYNY „{name}”</b>\n"
        "🧠 — poziom intelektu w grze (rośnie tylko w /quiz)\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
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
    "ref_rules": "Za każdego znajomego od razu +{s} 🪙. Gdy znajomy rozegra {r} rund — kolejne +{q} 🪙 i {c} 🥩 cyber-kotlet.",
    "ref_copy": "📋 Kopiuj",
    "ref_copied": "Link skopiowany!",
    "ref_share": "📤 Udostępnij",
    "ref_stats": "📊 TWOJA EKIPA",
    "ref_invited": "zaproszeni",
    "ref_qualified": "aktywni",
    "ref_earned": "zarobione",
    "ref_cutlets": "🥩 Kotlety otrzymane za aktywnych znajomych: {n}",
    "ref_top": "🏆 KTO MA NAJWIĘCEJ ZNAJOMYCH",
    "ref_topHint": "✅ — aktywni znajomi (rozegrali 30 rund), 👥 — wszyscy zaproszeni",
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
    "noTeam": "Nie masz jeszcze drużyny. Załóż własną albo dołącz do innej w czacie bota: „🏆 DRUŻYNY I KLANY”.",
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
    "footer": "Gry i quiz — w czacie bota",
    "noProfile": "Nie znaleziono profilu. Otwórz bota i naciśnij /start!",
    "blocked": "Konto zablokowane przez administrację.",
    "error": "Nie udało się załadować danych. Spróbuj później.",
    "outside": "Otwórz tę aplikację z Telegram-bota ROFL HUB.",
    "robotsTitle": "🤖 TWOJE ROBOTY",
    "buyMore": "🛒 Kup",
    "rateShort": "{v} 🪙/h",
    "refuelOne": "🥩 Zatankuj 1",
    "refuelAll": "⚡ Zatankuj wszystkie",
    "refueled": "Zatankowano: {n} 🥩",
    "res_metal_src": "Kamień-Papier-Nożyce i pojedynki",
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
    "sw_give": "Oddaję",
    "sw_want": "Chcę dostać",
    "sw_qty": "Ile",
    "sw_create": "Zaproponuj wymianę",
    "sw_take": "Wymień",
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
    "invite": "🤝 Link polecający: +1000 za znajomego",
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
