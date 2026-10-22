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
        "💸 Naliczono ci: <b>{balance} monet</b>\n"
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
        "• /create_team — Zarejestruj własną drużynę za 100 000 monet\n"
        "• /my_team — Panel ekipy i SKŁAD DRUŻYNY z poziomami 🧠\n"
        "• /all_teams — Ruletka losowych drużyn\n\n"
        "💸 <b>PIENIĄDZE I ZNAJOMI:</b>\n"
        "• /invite — Twój link polecający: +1000 monet za znajomego\n"
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
        "💸 Zwycięstwo daje: <b>+2 monety</b> (Cyber-Sejf: <b>+5</b>)\n"
        "💀 Porażka lub remis kosztuje: <b>-1 monetę</b>\n"
        "🧠 W Quizie — licznik 15 sekund i poziomy intelektu: 1. poziom to 10 poprawnych odpowiedzi i <b>+100 monet</b>, "
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
        "⚔️ Pojedynki z żywymi graczami przy stołach 10/100/1000 monet.\n"
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
        "🎭 {genre} · ⏱ {minutes} min · 🏆 +{reward} monet za pierwsze zwycięstwo\n"
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
    "quest.win_first": "\n\n🏆 <b>QUEST UKOŃCZONY! Nagroda: +{coins} monet.</b>",
    "quest.win_repeat": "\n\n✅ <b>Ukończono ponownie!</b> Nagroda za ten quest została już odebrana wcześniej.",
    "quest.fail_footer": "\n\n💀 <i>Nie najlepsze zakończenie... ale historię zawsze można przejść jeszcze raz!</i>",
    "quest.stale": "⏳ Ta scena jest już za tobą — gramy dalej od bieżącego miejsca!",
    "quest.no_coins": "❌ Za mało monet na podpowiedź ({cost}). Zajrzyj na farmę!",
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
    "farm.status_no_drills": "💡 Spraw sobie Cyber-Wiertacze w /shop, aby zwiększyć dochód.",
    "farm.boost_nuclear": "🔋 Nuklearne Przyspieszenie x5 do {until} UTC (zużycie kotletów ×3)",
    "farm.boost_nitrogen": "❄️ Azotowe Chłodzenie +40% do {until} UTC",
    "farm.boost_drone": "🛸 Mistrzowski Dron przedłuża życie robotów do {until} UTC",
    "farm.no_boosts": "Brak aktywnych wzmocnień — zajrzyj do /shop.",
    "farm.burnout": "🔥 Najbliższe wypalenie robota: <b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 Aktywuj Robota Stażystę (za darmo)",
    "farm.intern_activated": "🤖 Twój Robot Stażysta zaczął zmianę! +1 moneta na godzinę na zawsze — bez paliwa i bez terminu.",
    "farm.intern_already": "🤖 Twój Robot Stażysta już pracuje.",
    "farm.intern_line": "🤖 Roboty Stażyści ({rate} moneta/h, wieczne): <code>{count}</code>",
    "farm.intern_hint": "🎁 Masz darmowego Robota Stażystę! Naciśnij przycisk poniżej — będzie wydobywać 1 monetę na godzinę na zawsze.",
    "farm.dashboard": (
        "🚜 <b>CENTRALNY HUB PALIWOWY ROFL HUB</b>\n"
        "..................................................\n\n"
        "🤖 Aktywne roboty w fabryce: <b>{total} szt.</b>\n"
        "• Młodsi Górnicy ({junior_rate} monet/h): <code>{junior} szt.</code>\n"
        "• Cyber-Wiertacze ({premium_rate} monet/h): <code>{premium} szt.</code>\n"
        "{burnout}\n"
        "📊 <b>AKTUALNE TEMPO TWOJEJ FARMY:</b>\n"
        "• Produkcja na godzinę: <b>+{speed_hour} monet</b>\n"
        "• Produkcja na dobę: <b>+{speed_day} monet</b>\n\n"
        "⚡ <b>WZMOCNIENIA:</b>\n{boosts}\n\n"
        "📋 <b>STATUS TWOJEJ FABRYKI:</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>STAN AUTOMATYCZNEJ LODÓWKI:</b>\n"
        "🥩 Zapas paliwa: <b>{fridge} / {capacity} szt.</b>\n"
        "💼 Kotlety w magazynie ekwipunku: <code>{inv} szt.</code>\n\n"
        "..................................................\n\n"
        "<i>💿 Ważne: roboty żyją 30 dni (Mistrzowski Dron wstrzymuje zużycie). "
        "KAŻDY Cyber-Wiertacz zjada SWÓJ cały kotlet z lodówki na każde "
        "24 godziny pracy: 3 roboty — 3 kotlety na dobę. Pilnuj tankowania!</i>"
    ),
    "farm.bonus_ok": "🎁 Cyber-kotlet trafił do magazynu! Wróć za 24 godziny.",
    "farm.bonus_wait": "⏳ Bonus już odebrany! Następny kotlet za {hours} godz. {minutes} min.",
    "farm.no_inv_cutlets": "❌ Nie masz w ekwipunku cyber-kotletów! Kup je w /shop",
    "farm.fridge_full": "📦 Twoja Lodówka jest już pełna po brzegi!",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>PANEL GRACZA ROFL HUB</b>\n"
        "..................................................\n\n"
        "🆔 Twój ID Paszportu: <code>{user_id}</code>\n"
        "{vip}"
        "💰 Monety teraz: <b>{balance} monet</b>\n"
        "🏆 Twój status: <b>{team}</b>\n"
        "🧠 Poziom intelektu: <b>{level}</b> · do poziomu {next_level}: "
        "<b>{left}</b> poprawnych odpowiedzi w /quiz (nagroda: +{reward} monet)\n\n"
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
    "games.win": "🎉 <b>ZWYCIĘSTWO!</b> 🎉\nNaliczono monet: <b>+{reward}</b>",
    "games.lose": "💀 <b>PORAŻKA!</b>\nPobrano monet: <b>-{penalty}</b>",
    "games.draw": "🤝 <b>REMIS!</b>\nPobrano monet: <b>-{penalty}</b>",
    "games.limit": (
        "🛑 <b>Dzienny limit osiągnięty!</b>\n\n"
        "W grze {game} masz już {limit} zwycięstw na dziś. Limit odnowi się o 00:00 UTC.\n\n"
        "⚡ Zdejmij limit na 24 godziny — 5 ★, na 30 dni — 99 ★ (sekcja „Do gier” w /shop)."
    ),
    "games.no_coins": "❌ Masz 0 monet — nie masz czym opłacić rundy. Odbierz dochód z farmy w /farm!",
    "games.balance": "💰 Saldo: <b>{balance} monet</b>",
    "games.btn_retry": "🎮 Zagraj jeszcze raz!",
    "games.btn_hub": "🕹️ Strefa gier",
    "games.level_up": (
        "🏅 <b>POZIOM INTELEKTU PODNIESIONY: {level}!</b> Nagroda: <b>+{bonus} monet</b>!\n"
        "Następny poziom: {next_required} poprawnych odpowiedzi → +{next_reward} monet."
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
    "quiz.lost_line": "💀 <b>-{penalty} moneta</b> za przegraną!",
    "quiz.level_line": (
        "🧠 Poziom intelektu: <b>{level}</b>\n"
        "Do poziomu {next_level} brakuje zwycięstw: <b>{left}</b>"
    ),
    "quiz.rules": (
        "<i>Na odpowiedź masz {seconds} sekund!\n"
        "Poprawnie: +{win} monety na konto\n"
        "Błąd / brak odpowiedzi na czas: -{penalty} moneta\n"
        "Limit: {limit} zwycięstw na dobę</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>CYBER-SEJF</b>\n\n"
        "W środku — jackpot <b>{jackpot} monet</b>! Drzwiczki zamknięte kodem od 1 do {codes}. "
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
    "duel.btn_table": "⚔️ Stół {stake} monet",
    "duel.btn_cancel": "❌ Opuść stół (zwrot stawki)",
    "duel.btn_move_rock": "🪨 Kamień",
    "duel.btn_move_scissors": "✂️ Nożyce",
    "duel.btn_move_paper": "🧻 Papier",
    "duel.waiting": (
        "🪑 <b>Siedzisz przy stole {stake} monet.</b> Stawka jest w puli.\n"
        "Czekamy na drugiego wojownika... Gdy tylko usiądzie, każdy z was dostanie wybór gestu!\n"
        "<i>Kolejka żyje {ttl} minut, potem stawka wróci automatycznie.</i>"
    ),
    "duel.cancelled": "🚪 Stół opuszczony. Stawka <b>{stake} monet</b> wróciła na saldo.",
    "duel.expired": "⌛ Przy stole {stake} nie znalazł się przeciwnik. Stawka <b>{stake} monet</b> została zwrócona.",
    "duel.matched": (
        "⚔️ <b>PRZECIWNIK ZNALEZIONY! Stół {stake} monet.</b>\n"
        "Pula: <b>{bank} monet</b> · Dla zwycięzcy: <b>{payout}</b>\n\n"
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
        "💰 Wygrana: <b>+{payout} monet</b> · 🔥 Spalone z puli: {burned}\n"
        "💼 Saldo: <b>{balance} monet</b>"
    ),
    "duel.lose": (
        "💀 <b>POJEDYNEK PRZEGRANY.</b>\n\n"
        "Gest przeciwnika {winner_move} bije twój gest {loser_move}.\n"
        "📉 Stawka <b>{stake} monet</b> trafiła do puli zwycięzcy.\n"
        "Rewanż?"
    ),
    "duel.reaper_prefix": "⏰ <b>Koniec czasu rundy!</b> Brakujące gesty wybrał generator losowości.\n\n",
    "duel.bad_table": "❌ Taki stół nie istnieje.",
    "duel.already_in": "⚠️ Już siedzisz przy stole albo walczysz! Najpierw dokończ bieżący pojedynek.",
    "duel.no_coins": "❌ Do tego stołu potrzebujesz {stake} monet na koncie.",
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
        "Zapraszaj znajomych i otrzymuj <b>+{bonus} monet</b> za każdego, "
        "kto zarejestruje się przez twój osobisty link!\n\n"
        "🔗 <b>Twój link (kliknij, aby skopiować):</b>\n<code>{link}</code>\n\n"
        "📊 <b>TWOJE STATYSTYKI:</b>\n"
        "👥 Zaproszonych znajomych: <b>{invited}</b>\n"
        "💰 Zarobione na poleconych: <b>{earned} monet</b>\n\n"
        "..................................................\n"
        "<i>Podsyłaj link znajomym, wrzucaj na czaty klasowe i do social mediów — im większa ekipa, tym szybciej rośnie twoje saldo!</i>"
    ),
    "ref.btn_share": "📣 Udostępnij link",
    "ref.share_text": "Wbijaj do ekosystemu gier ROFL HUB!",
    "ref.qualified_line": ("⭐ <b>Podwójna nagroda:</b> gdy zaproszony znajomy rozegra {rounds} "
                           "rund, dostajesz kolejne <b>+{bonus} monet</b>!"),
    "ref.qualified_notify": ("🤝 <b>Twój znajomy wkręcił się: już {rounds} rund!</b>\n"
                             "Za kwalifikowanego poleconego dostajesz <b>+{bonus} monet</b>. "
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
        "📌 Minimalna kwota: <b>{min} monet</b>"
    ),
    "tr.not_found": "❌ Nie znaleziono odbiorcy. Sprawdź ID Paszportu lub @username — gracz musi być zarejestrowany w bocie.",
    "tr.self": "🤨 Nie możesz przelać monet samemu sobie — to byłoby ekonomiczne perpetuum mobile!",
    "tr.blocked": "🚫 Ten gracz jest zablokowany — przelewy do niego są niedostępne.",
    "tr.min": "❌ Minimalna kwota przelewu to {min} monet.",
    "tr.insufficient": "❌ Za mało monet! Twoje saldo: <b>{balance}</b>.",
    "tr.err_insufficient": "❌ Za mało monet na koncie.",
    "tr.confirm": (
        "🔄 <b>POTWIERDŹ PRZELEW:</b>\n\n"
        "👤 Odbiorca: <b>{recipient}</b> (ID <code>{recipient_id}</code>)\n"
        "💸 Kwota do pobrania: <b>{amount} monet</b>{fee_line}\n"
        "💰 Odbiorca otrzyma: <b>{received} monet</b>\n\n"
        "<i>Przelewów nie da się cofnąć — sprawdź odbiorcę!</i>"
    ),
    "tr.fee_line": "\n🔥 Prowizja huba: <b>{fee} monet</b> (spłonie)",
    "tr.btn_confirm": "✅ POTWIERDŹ PRZELEW",
    "tr.btn_cancel": "❌ Anuluj",
    "tr.cancelled_toast": "Przelew anulowany",
    "tr.cancelled": "❌ <b>Przelew anulowany.</b> Monety zostały na miejscu.",
    "tr.not_yours": "🔒 To nie twój przelew!",
    "tr.done_toast": "✅ Przelew wykonany!",
    "tr.done": (
        "✅ <b>PRZELEW WYKONANY!</b>\n\n"
        "💸 Wysłano: <b>{amount} monet</b> do gracza ID <code>{recipient_id}</code>\n"
        "💰 Twoje saldo: <b>{balance} monet</b>"
    ),
    "tr.received": (
        "💰 <b>Masz przelew: {amount} monet!</b>\n"
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
    "dlv.coins": "💰 Naliczono <b>+{amount} monet</b>.",
    "dlv.boost_nuclear": "🔋 Nuklearne Przyspieszenie x5 aktywne do <b>{until} UTC</b>.",
    "dlv.boost_nitrogen": "❄️ Azotowe Chłodzenie +40% aktywne do <b>{until} UTC</b>.",
    "dlv.drone": "🛸 Mistrzowski Dron pilnuje farmy do <b>{until} UTC</b>.",
    "dlv.unlimit": "⚡ Limity zwycięstw zdjęte do <b>{until} UTC</b>.",
    "dlv.clan": "🏆 Drużyna otrzymała status <b>MEGA-KLANU</b>: do {max} miejsc.",
    "dlv.err_fridge": "Masz już lodówkę tej lub większej pojemności.",
    "dlv.err_no_team": "Nie masz jeszcze drużyny. Najpierw załóż ją przez /create_team.",
    "dlv.err_mega": "Twoja drużyna ma już status Mega-Klanu.",
    "dlv.intern_upgrade": "♾ Twój Robot Stażysta awansował na <b>WIECZNEGO Robota Górnika</b>: 5 monet na godzinę, bez terminu!",
    "dlv.err_no_intern": "Brak aktywowanego Robota Stażysty — najpierw aktywuj go w /farm.",
    "dlv.err_intern_refs": "Ulepszenie wymaga {need} kwalifikowanych znajomych (po 30 rund); masz {have}.",
    "mk.header": "📈 <b>GIEŁDA KOTLETÓW</b>\n..................................................\n\nOtwarte zlecenia: <b>{orders}</b> · kotletów w ofercie: <b>{cutlets}</b> · najlepsza cena: <b>{best}</b>\nProwizja hubu: <b>{fee}%</b> od sprzedaży (spalana — tarcza antyinflacyjna)\n🥩 W twoim magazynie: <b>{inv}</b> kotletów\n\n{body}\n\n<i>Kliknij zlecenie, aby kupić. Sprzedaż: /sell.</i>",
    "mk.empty": "Nie ma jeszcze ofert. Bądź pierwszy: /sell ilość cena",
    "mk.order_line": "🥩 #{id} · <b>{qty} szt.</b> po <b>{price}</b> monet",
    "mk.btn_order": "🛒 #{id}: {qty} szt. po {price} monet",
    "mk.btn_my": "📋 Moje zlecenia",
    "mk.btn_sell_help": "💰 Jak sprzedać kotlety",
    "mk.btn_refresh": "🔄 Odśwież",
    "mk.btn_back": "← Do giełdy",
    "mk.pick": "🛒 <b>Zlecenie #{id}</b>: dostępne {qty} szt. po {price} monet.\nIle kupić?",
    "mk.btn_qty": "{qty} szt. — {total} monet",
    "mk.btn_qty_all": "Wszystkie {qty} szt. — {total} monet",
    "mk.buy_toast": "Transakcja zamknięta!",
    "mk.buy_done": "✅ Kupiono <b>{qty} kotletów</b> za <b>{total} monet</b>. Są już w magazynie — tankuj Wiertła!",
    "mk.sold_notify": "💰 <b>Giełda: sprzedano!</b> Zlecenie #{id}: {qty} szt. po {price}. Otrzymujesz <b>+{got} monet</b> (prowizja {fee} spalona).",
    "mk.sell_help": "💰 <b>JAK SPRZEDAĆ KOTLETY</b>\n\nKomenda: <code>/sell ilość cena</code>\nPrzykład: <code>/sell 10 50</code> — 10 kotletów po 50 monet.\n\nKotlety schodzą z magazynu i czekają w zleceniu (możesz je wycofać w każdej chwili). Do {max_qty} szt. w zleceniu i do {max_orders} otwartych zleceń. Przy sprzedaży spalana jest prowizja {fee}%.",
    "mk.sell_confirm": "📝 Wystawić <b>{qty} kotletów</b> po <b>{price}</b> monet?\nSuma: {total} · prowizja {fee} spłonie · dostaniesz <b>{got} monet</b>.",
    "mk.btn_confirm_sell": "✅ WYSTAW NA GIEŁDĘ",
    "mk.btn_cancel": "❌ Anuluj",
    "mk.sell_toast": "Zlecenie wystawione!",
    "mk.sell_done": "✅ Zlecenie <b>#{id}</b> na giełdzie: {qty} szt. po {price} monet. Dam znać, gdy ktoś kupi.",
    "mk.cancelled_toast": "Anulowano",
    "mk.cancel_text": "❌ <b>Anulowano.</b> Kotlety zostały w magazynie.",
    "mk.my_header": "📋 <b>TWOJE ZLECENIA</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} szt. po {price} monet",
    "mk.my_empty": "📋 Nie masz otwartych zleceń.",
    "mk.btn_cancel_order": "❌ Wycofaj zlecenie #{id}",
    "mk.order_cancelled": "↩️ Zlecenie #{id} wycofane: <b>{qty} kotletów</b> wróciło do magazynu.",
    "mk.err_qty": "❌ Ilość: od 1 do {max} kotletów w zleceniu.",
    "mk.err_price": "❌ Cena: od {min} do {max} monet za kotlet.",
    "mk.err_no_cutlets": "❌ W magazynie masz tylko {have} kotletów. Kotlety z lodówki nie trafiają na giełdę — zobacz /farm.",
    "mk.err_too_many": "❌ Limit: maksymalnie {max} otwartych zleceń. Wycofaj jedno w „Moje zlecenia”.",
    "mk.err_not_found": "❌ To zlecenie jest już zamknięte.",
    "mk.err_own": "🤨 Nie możesz kupić własnego zlecenia.",
    "mk.err_insufficient": "❌ Za mało monet: potrzeba {total}.",
    "farm.btn_market": "📈 Giełda kotletów",

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
    "passport": "📋 PASZPORT GRACZA",
    "coins": "monet",
    "brain": "🧠 Poziom intelektu",
    "toNext": "do poziomu {n}: {left} poprawnych odpowiedzi w quizie (+{reward} monet)",
    "farm": "🚜 CYBER-FARMA",
    "robots": "Roboty (górnicy / wiertacze)",
    "fueled": "Zatankowane wiertacze",
    "speed": "Tempo wydobycia",
    "perHour": "{v} monet/godz.",
    "fridge": "Lodówka",
    "inv": "Kotlety w magazynie",
    "burnout": "Najbliższe wypalenie",
    "intern": "Roboty Stażyści (1 moneta/h, wieczne)",
    "activateIntern": "🚀 AKTYWUJ ROBOTA STAŻYSTĘ",
    "internDone": "🤖 Twój Robot Stażysta zaczął zmianę!",
    "rank": "🎖 Ranga",
    "openFarm": "🏭 OTWÓRZ FARMĘ",
    "farmScene": "🏭 TWOJA FARMA",
    "back": "← Wstecz",
    "minedVisit": "wydobyte podczas tej wizyty",
    "unit_intern": "Robot Stażysta",
    "unit_junior": "Robot Górnik",
    "unit_premium": "Cyber-Wiertło",
    "eternal": "wieczny",
    "fueledAll": "zatankowane",
    "fueledPart": "{a} z {b} zatankowanych",
    "license": "licencja na 30 dni",
    "emptyFarm": "Kopalnia jest pusta. Aktywuj Robota Stażystę albo kup roboty w sklepie!",
    "madeBy": "Chcesz takiego bota dla swojego projektu? Napisz do @mister_telebot",
    "boosts": "Aktywne wzmocnienia",
    "none": "brak",
    "bonusReady": "🎁 ODBIERZ CODZIENNY KOTLET",
    "bonusWait": "⏳ Bonus za {h} godz. {m} min",
    "bonusDone": "🎉 Kotlet w magazynie!",
    "team": "🏆 MOJA DRUŻYNA",
    "clan": "KLAN",
    "teamLabel": "Drużyna",
    "captain": "👑 Jesteś kapitanem!",
    "members": "Skład",
    "noTeam": "Nie masz jeszcze drużyny — zbierz ekipę w czacie bota!",
    "top": "👑 TOP-100 BOGACZY EKOSYSTEMU",
    "shop": "🏪 SKLEP",
    "shopFarm": "🚜 DLA FARMY",
    "shopGames": "🕹️ DO GIER",
    "shopHint": "Płatność oficjalnymi Telegram Stars — tutaj, jednym tapnięciem.",
    "paid": "🎉 Opłacone! Towar jest już na twoim koncie.",
    "payFail": "Płatność nie przeszła. Spróbuj jeszcze raz.",
    "oldClient": "Zaktualizuj Telegram, aby kupować z poziomu Mini App, albo otwórz sklep w czacie bota.",
    "ctaNoRobots": "💤 Farma jest pusta! Spraw sobie pierwszego robota — monety będą kapać całą dobę.",
    "ctaHungry": "🚨 Wiertacze głodują ({n} bez paliwa) — wydobycie stoi!",
    "ctaLowFuel": "⚠️ Kotletów starczy na mniej niż dobę pracy Wiertaczy.",
    "ctaShopBtn": "🛒 Do sklepu",
    "footer": "Pełne sterowanie — w czacie bota: /menu",
    "noProfile": "Nie znaleziono profilu. Otwórz bota i naciśnij /start!",
    "blocked": "Konto zablokowane przez administrację.",
    "error": "Nie udało się załadować danych. Spróbuj później.",
    "outside": "Otwórz tę aplikację z Telegram-bota ROFL HUB.",
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
}
