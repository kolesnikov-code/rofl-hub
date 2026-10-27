/*
 * ✨ QuestFX — атмосфера сцен квестов (27.10, идея владельца: «вода — блики бассейна, дым — из-за угла, огонь — тени
 * от костра в пещере… клуб — диско-шар и лазеры»). Без видео: CSS-слои + один холст частиц на сцену.
 *
 * Сцена квеста помечается "mood" (строка или список до 2 меток) — data/quests/*.json. Эффект = набор слоёв:
 *   back  — CSS-слои ПОД текстом сцены (внутри карточки),
 *   front — лёгкий слой поверх экрана (виньетки, сирена, вспышка; pointer-events: none),
 *   parts — частицы на холсте (дождь, снег, искры, пыль, светлячки…), matrix/arcs — особые режимы холста,
 *   once  — разовое событие при входе в сцену (толчок, вспышка магния).
 * Безопасность: никаких стробоскопов и частых вспышек (≤ 2 вспышки подряд, редко), «уменьшить движение» в системе —
 * только статичные подложки; игрок может выключить эффекты (localStorage fx_off). Холст — DPR ≤ 1.5, пауза в фоне.
 */
(function () {
  "use strict";
  // 🌐 надписи эффектов на языке игрока (14 языков экосистемы); новый текстовый эффект — новая пара ключей здесь
  const FX_WORDS = {
    ru: { open: "ОТКРЫТО", error: "ОШИБКА" }, en: { open: "OPEN", error: "ERROR" }, uz: { open: "OCHIQ", error: "XATO" },
    es: { open: "ABIERTO", error: "ERROR" }, fr: { open: "OUVERT", error: "ERREUR" }, pt: { open: "ABERTO", error: "ERRO" },
    de: { open: "OFFEN", error: "FEHLER" }, it: { open: "APERTO", error: "ERRORE" }, pl: { open: "OTWARTE", error: "BŁĄD" },
    id: { open: "TERBUKA", error: "SALAH" }, zh: { open: "已开启", error: "错误" }, hi: { open: "खुला", error: "त्रुटि" },
    bn: { open: "খোলা", error: "ভুল" }, ar: { open: "مفتوح", error: "خطأ" },
  };
  const RUNES = "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ☉☽✶⟁⌬";
  const MATRIX = "01ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄ0123456789";
  const reduceMotion = () => window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const rnd = (a, b) => a + Math.random() * (b - a);
  const pick = arr => arr[Math.floor(Math.random() * arr.length)];
  const range = v => Array.isArray(v) ? rnd(v[0], v[1]) : (v || 0);

  // ---------------------------------------------------------------- CSS всех слоёв
  const CSS = `
  .qs-stage{position:relative;overflow:hidden;isolation:isolate}
  .qs-stage>*:not(.fx-back){position:relative;z-index:1}
  .qs-stage .qs-text{text-shadow:0 1px 3px rgba(0,0,0,.95),0 0 10px rgba(0,0,0,.6)}
  .fx-back{position:absolute;inset:0;z-index:0;pointer-events:none;overflow:hidden;border-radius:inherit}
  .fx-back canvas{position:absolute;inset:0;width:100%;height:100%}
  #fxFront{position:fixed;inset:0;z-index:40;pointer-events:none;overflow:hidden}
  .fxl{position:absolute;inset:0;pointer-events:none}
  .fx-fade{animation:fxIn 1.2s ease-out both}
  @keyframes fxIn{from{opacity:0}to{opacity:1}}
  @keyframes fxDrift{from{transform:translateX(-25%)}to{transform:translateX(5%)}}
  @keyframes fxDriftR{from{transform:translateX(5%)}to{transform:translateX(-25%)}}
  @keyframes fxRise{from{transform:translateY(40%) scale(.8);opacity:0}30%{opacity:1}to{transform:translateY(-60%) scale(1.3);opacity:0}}
  @keyframes fxSpin{to{transform:rotate(360deg)}}
  @keyframes fxSpinR{to{transform:rotate(-360deg)}}
  @keyframes fxPulse{0%,100%{opacity:.55}50%{opacity:1}}
  @keyframes fxHue{to{filter:hue-rotate(360deg)}}
  /* 🌫 туман */
  .fx-fog{background:radial-gradient(ellipse at 20% 60%,rgba(210,220,230,.22),transparent 55%),radial-gradient(ellipse at 70% 30%,rgba(200,210,225,.18),transparent 50%),radial-gradient(ellipse at 50% 90%,rgba(220,225,235,.2),transparent 60%);width:160%;filter:blur(22px);animation:fxDrift 38s ease-in-out infinite alternate}
  .fx-fog2{animation:fxDriftR 52s ease-in-out infinite alternate;opacity:.8;top:20%}
  /* 💧 блики бассейна */
  .fx-pool{background:linear-gradient(180deg,rgba(0,60,90,.55),rgba(0,30,60,.7))}
  .fx-caust{inset:-35%;background-size:300px 300px;mix-blend-mode:screen;opacity:.5;filter:blur(.6px) drop-shadow(0 0 3px rgba(120,240,255,.8));animation:fxCaust 9s ease-in-out infinite alternate}
  .fx-caust2{background-size:380px 380px;animation-duration:13s;animation-direction:alternate-reverse;opacity:.35}
  @keyframes fxCaust{0%{transform:translate(0,0) rotate(0) scale(1)}50%{transform:translate(-18px,12px) rotate(3deg) scale(1.08)}100%{transform:translate(14px,-10px) rotate(-2deg) scale(.96)}}
  .fx-ripple{background:repeating-linear-gradient(170deg,transparent 0 22px,rgba(160,250,255,.08) 24px 26px,transparent 28px 46px);filter:blur(2px);animation:fxRipple 6s linear infinite}
  @keyframes fxRipple{to{background-position:0 92px}}
  /* 🌊 под водой */
  .fx-deep{background:linear-gradient(180deg,rgba(0,70,110,.55),rgba(0,10,40,.85))}
  .fx-rays{inset:-20% -40%;background:repeating-linear-gradient(100deg,transparent 0 40px,rgba(160,230,255,.10) 55px 75px,transparent 90px 130px);filter:blur(8px);transform-origin:50% 0;animation:fxRays 12s ease-in-out infinite alternate;mask-image:linear-gradient(180deg,#000,transparent 85%);-webkit-mask-image:linear-gradient(180deg,#000,transparent 85%)}
  @keyframes fxRays{from{transform:skewX(-8deg) translateX(-20px)}to{transform:skewX(8deg) translateX(20px)}}
  .fx-abyss{background:radial-gradient(ellipse at 50% 120%,rgba(0,40,70,.6),rgba(0,0,10,.9))}
  .fx-swamp{background:linear-gradient(180deg,rgba(10,30,15,.6),rgba(30,70,20,.65));}
  .fx-swampglow{background:radial-gradient(ellipse at 50% 110%,rgba(120,255,90,.28),transparent 60%);animation:fxPulse 5s ease-in-out infinite}
  /* 🔥 костёр в пещере */
  .fx-cave{background:radial-gradient(ellipse at 50% 115%,rgba(255,140,40,.5),rgba(120,40,10,.35) 45%,rgba(10,5,5,.75) 80%)}
  .fx-flicker{background:radial-gradient(ellipse at 50% 105%,rgba(255,190,90,.45),transparent 60%);mix-blend-mode:screen;animation:fxFlick 2.6s steps(1) infinite}
  @keyframes fxFlick{0%{opacity:.75;transform:scale(1)}13%{opacity:.95;transform:scale(1.03)}21%{opacity:.7}34%{opacity:1;transform:scale(1.05)}47%{opacity:.8;transform:scale(.99)}58%{opacity:.92}71%{opacity:.72;transform:scale(1.02)}86%{opacity:.98}}
  .fx-shadows{background:radial-gradient(ellipse 90px 260px at 18% 40%,rgba(0,0,0,.55),transparent 70%),radial-gradient(ellipse 110px 280px at 82% 45%,rgba(0,0,0,.5),transparent 70%),radial-gradient(ellipse 70px 200px at 50% 20%,rgba(0,0,0,.35),transparent 70%);transform-origin:50% 100%;animation:fxSway 3.1s ease-in-out infinite alternate}
  @keyframes fxSway{0%{transform:skewX(-6deg) scaleY(1)}35%{transform:skewX(4deg) scaleY(1.05)}70%{transform:skewX(-2deg) scaleY(.97)}100%{transform:skewX(7deg) scaleY(1.03)}}
  .fx-blaze{background:linear-gradient(0deg,rgba(0,0,0,.8),rgba(60,10,0,.45) 40%,rgba(255,90,20,.18) 100%)}
  .fx-lava{background:radial-gradient(ellipse at 50% 120%,rgba(255,80,0,.45),rgba(20,5,5,.85) 70%)}
  .fx-cracks{background:linear-gradient(115deg,transparent 30%,rgba(255,110,20,.55) 31%,transparent 33%),linear-gradient(70deg,transparent 55%,rgba(255,80,0,.45) 56%,transparent 58%),linear-gradient(160deg,transparent 70%,rgba(255,140,40,.5) 71%,transparent 73%),linear-gradient(30deg,transparent 15%,rgba(255,90,10,.4) 16%,transparent 18%);filter:blur(1.5px) drop-shadow(0 0 6px rgba(255,90,0,.9));animation:fxPulse 4s ease-in-out infinite}
  .fx-candle{background:radial-gradient(ellipse at 50% 55%,rgba(255,190,100,.22),rgba(0,0,0,.2) 45%,rgba(0,0,0,.82) 85%);animation:fxCandle 3.3s ease-in-out infinite}
  @keyframes fxCandle{0%,100%{opacity:.9}23%{opacity:1}41%{opacity:.82}67%{opacity:.97}82%{opacity:.86}}
  /* 💨 дым, пар, смог */
  .fx-smoke{background:radial-gradient(circle at 30% 50%,rgba(170,170,175,.35),transparent 40%),radial-gradient(circle at 60% 40%,rgba(150,150,155,.3),transparent 45%),radial-gradient(circle at 80% 70%,rgba(180,180,185,.3),transparent 40%);width:200%;left:-100%;filter:blur(28px);animation:fxSmoke 24s linear infinite}
  .fx-smoke2{animation-duration:34s;animation-delay:-12s;top:25%;opacity:.8}
  @keyframes fxSmoke{0%{transform:translateX(0);opacity:0}15%{opacity:1}85%{opacity:.9}100%{transform:translateX(60%);opacity:0}}
  .fx-steam{background:radial-gradient(ellipse 70px 120px at 25% 100%,rgba(255,255,255,.35),transparent 70%),radial-gradient(ellipse 90px 140px at 65% 100%,rgba(255,255,255,.3),transparent 70%);filter:blur(16px);animation:fxRise 6s ease-out infinite}
  .fx-steam2{animation-delay:-3s;left:12%}
  .fx-smog{background:linear-gradient(180deg,rgba(120,110,70,.35),rgba(70,65,50,.55))}
  /* 🌙 ночь, космос, сияние */
  .fx-night{background:radial-gradient(circle at 82% 12%,rgba(220,230,255,.22),transparent 18%),linear-gradient(180deg,rgba(5,10,35,.75),rgba(10,15,40,.55))}
  .fx-space{background:radial-gradient(ellipse at 25% 30%,rgba(120,60,200,.28),transparent 50%),radial-gradient(ellipse at 75% 70%,rgba(0,140,200,.22),transparent 55%),rgba(0,0,15,.75);animation:fxHue 40s linear infinite}
  .fx-aurora{background:linear-gradient(170deg,transparent 10%,rgba(60,255,160,.35) 25%,transparent 40%),linear-gradient(185deg,transparent 20%,rgba(150,90,255,.3) 35%,transparent 50%);filter:blur(14px);inset:-10% -20% 40% -20%;animation:fxAur 10s ease-in-out infinite alternate}
  @keyframes fxAur{from{transform:skewX(-10deg) translateX(-20px)}to{transform:skewX(12deg) translateX(25px)}}
  .fx-magic{background:radial-gradient(ellipse at 50% 100%,rgba(170,80,255,.3),transparent 65%),rgba(15,5,30,.45)}
  .fx-glowgold{background:radial-gradient(ellipse at 50% 60%,rgba(255,210,90,.12),transparent 70%),rgba(5,15,8,.45)}
  .fx-dark{background:rgba(0,0,0,.6)}
  .fx-void{background:radial-gradient(ellipse at 50% 110%,rgba(40,0,60,.35),transparent 60%),#000}
  .fx-ghost{background:radial-gradient(ellipse at 50% 50%,rgba(120,255,200,.08),rgba(0,10,10,.65) 75%)}
  /* 🪩 клуб: диско-шар и лазеры (без стробоскопа) */
  .fx-clubbg{background:radial-gradient(circle at 50% 0%,rgba(255,60,200,.18),transparent 50%),rgba(10,0,25,.6);animation:fxHue 16s linear infinite}
  .fx-lasers{inset:-60%;background:conic-gradient(from 0deg at 50% 100%,transparent 0 8deg,rgba(255,40,180,.35) 8.5deg 9.5deg,transparent 10deg 30deg,rgba(40,220,255,.35) 30.5deg 31.5deg,transparent 32deg 52deg,rgba(120,255,80,.3) 52.5deg 53.5deg,transparent 54deg 360deg);transform-origin:50% 100%;mix-blend-mode:screen;filter:blur(.6px) drop-shadow(0 0 4px rgba(255,255,255,.6));animation:fxLaser 7s ease-in-out infinite alternate}
  .fx-lasers2{animation-duration:9s;animation-direction:alternate-reverse;opacity:.8}
  @keyframes fxLaser{from{transform:rotate(-40deg)}to{transform:rotate(25deg)}}
  /* 🚨 сирена, тревога */
  .fx-sirenL{background:radial-gradient(ellipse at 0% 50%,rgba(255,30,40,.55),transparent 55%);animation:fxSirA 1.3s ease-in-out infinite}
  .fx-sirenR{background:radial-gradient(ellipse at 100% 50%,rgba(40,90,255,.55),transparent 55%);animation:fxSirA 1.3s ease-in-out infinite;animation-delay:-.65s}
  @keyframes fxSirA{0%,100%{opacity:.1}50%{opacity:1}}
  .fx-beacon{inset:-50%;background:conic-gradient(from 0deg,rgba(255,30,30,.32),transparent 60deg,transparent 360deg);animation:fxSpin 3s linear infinite}
  /* 🕵️ нуар: жалюзи, фары, фонарик */
  .fx-noir{background:rgba(5,5,10,.55)}
  .fx-blinds{background:repeating-linear-gradient(180deg,rgba(255,240,200,.13) 0 16px,rgba(0,0,0,.25) 16px 34px);transform:skewY(-12deg) scale(1.3);mask-image:radial-gradient(ellipse at 70% 40%,#000,transparent 75%);-webkit-mask-image:radial-gradient(ellipse at 70% 40%,#000,transparent 75%);animation:fxBlind 14s ease-in-out infinite alternate}
  @keyframes fxBlind{from{transform:skewY(-12deg) scale(1.3) translateX(-20px)}to{transform:skewY(-12deg) scale(1.3) translateX(25px)}}
  .fx-headl{background:linear-gradient(100deg,transparent 35%,rgba(255,250,220,.35) 48%,transparent 60%);filter:blur(10px);transform:translateX(-120%);animation:fxHead 11s ease-in-out infinite}
  @keyframes fxHead{0%,70%{transform:translateX(-120%);opacity:0}72%{opacity:1}86%{transform:translateX(120%);opacity:.9}87%,100%{transform:translateX(120%);opacity:0}}
  .fx-torch{background:radial-gradient(circle 130px at var(--fx-x,50%) var(--fx-y,45%),rgba(255,240,190,.26),rgba(255,230,170,.08) 35%,rgba(0,0,0,.6) 60%,rgba(0,0,0,.9) 100%)}
  /* 💻 техно */
  .fx-holo{background:repeating-linear-gradient(180deg,rgba(0,255,230,.06) 0 2px,transparent 2px 4px),linear-gradient(180deg,rgba(0,40,60,.5),rgba(0,20,40,.6))}
  .fx-sweep{background:linear-gradient(180deg,transparent,rgba(120,255,240,.22),transparent);height:22%;animation:fxSweep 4.5s linear infinite}
  @keyframes fxSweep{from{transform:translateY(-110%)}to{transform:translateY(560%)}}
  .fx-scan{background:linear-gradient(180deg,transparent,rgba(0,255,200,.9),transparent);height:2px;box-shadow:0 0 14px rgba(0,255,200,.8);animation:fxSweep2 5s ease-in-out infinite alternate}
  @keyframes fxSweep2{from{top:2%}to{top:96%}}
  .fx-matrixbg{background:rgba(0,10,0,.7)}
  .fx-glitch{background:linear-gradient(90deg,rgba(255,0,90,.25),rgba(0,255,230,.25));mix-blend-mode:screen;opacity:0;animation:fxGlitch 6s steps(1) infinite}
  @keyframes fxGlitch{0%,88%,100%{opacity:0;clip-path:inset(0 0 100% 0)}89%{opacity:1;clip-path:inset(12% 0 70% 0);transform:translateX(-10px)}91%{opacity:1;clip-path:inset(55% 0 30% 0);transform:translateX(12px)}93%{opacity:1;clip-path:inset(80% 0 8% 0);transform:translateX(-6px)}95%{opacity:0}}
  .fx-film{background:radial-gradient(ellipse,transparent 55%,rgba(0,0,0,.55)),rgba(60,45,25,.35);animation:fxFilm .18s steps(2) infinite}
  @keyframes fxFilm{0%{opacity:.92}50%{opacity:1}}
  .fx-vhs{background:linear-gradient(180deg,transparent 0 45%,rgba(255,255,255,.1) 46%,transparent 48%);animation:fxVhs 7s linear infinite}
  @keyframes fxVhs{from{transform:translateY(-60%)}to{transform:translateY(80%)}}
  .fx-radar{background:radial-gradient(circle,transparent 0 24%,rgba(0,255,120,.18) 24.5% 25%,transparent 25.5% 49%,rgba(0,255,120,.18) 49.5% 50%,transparent 50.5% 74%,rgba(0,255,120,.18) 74.5% 75%,transparent 75.5%),rgba(0,25,10,.6)}
  .fx-radarsweep{inset:-50%;background:conic-gradient(from 0deg,rgba(0,255,120,.4),rgba(0,255,120,.05) 50deg,transparent 60deg 360deg);animation:fxSpin 4s linear infinite}
  .fx-fan{inset:-40%;background:conic-gradient(from 0deg,rgba(0,0,0,.45) 0 30deg,transparent 30deg 120deg,rgba(0,0,0,.45) 120deg 150deg,transparent 150deg 240deg,rgba(0,0,0,.45) 240deg 270deg,transparent 270deg);filter:blur(3px);animation:fxSpin 5s linear infinite}
  .fx-fanlight{background:radial-gradient(circle at 50% 40%,rgba(255,230,180,.25),transparent 60%)}
  .fx-gears{background-repeat:no-repeat;opacity:.13}
  .fx-gearA{width:220px;height:220px;inset:auto;left:-60px;top:-40px;animation:fxSpin 22s linear infinite}
  .fx-gearB{width:160px;height:160px;inset:auto;right:-30px;bottom:-30px;animation:fxSpinR 15s linear infinite}
  /* 🏚 подземелье, пыль, плесень */
  .fx-dungeon{background:radial-gradient(ellipse at 50% 50%,rgba(20,30,25,.3),rgba(0,0,0,.8) 80%),linear-gradient(0deg,rgba(40,70,30,.25),transparent 30%)}
  .fx-beam{background:linear-gradient(118deg,transparent 20%,rgba(255,235,180,.16) 32%,rgba(255,235,180,.05) 45%,transparent 52%);filter:blur(6px);animation:fxPulse 9s ease-in-out infinite}
  .fx-attic{background:rgba(20,15,10,.5)}
  /* 💓 состояния героя (поверх экрана) */
  .fx-heart{box-shadow:inset 0 0 90px rgba(200,0,20,.55);animation:fxHeart 1.25s ease-in-out infinite}
  @keyframes fxHeart{0%,100%{opacity:.35}12%{opacity:1}24%{opacity:.5}36%{opacity:.9}55%{opacity:.35}}
  .fx-panic{box-shadow:inset 0 0 140px 30px rgba(0,0,0,.85);animation:fxPanic 1.6s ease-in-out infinite}
  @keyframes fxPanic{0%,100%{box-shadow:inset 0 0 120px 20px rgba(0,0,0,.8)}50%{box-shadow:inset 0 0 190px 70px rgba(0,0,0,.92)}}
  .fx-poison{background:linear-gradient(135deg,rgba(80,255,60,.22),rgba(180,0,255,.2));animation:fxHue 8s linear infinite}
  .fx-dream{background:linear-gradient(120deg,rgba(255,170,220,.25),rgba(170,160,255,.25),rgba(255,220,150,.22));background-size:300% 300%;filter:blur(4px);animation:fxDream 14s ease-in-out infinite alternate}
  @keyframes fxDream{from{background-position:0 0}to{background-position:100% 100%}}
  .fx-frost{box-shadow:inset 0 0 70px 18px rgba(200,235,255,.55);background:radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(220,245,255,.25) 100%);animation:fxIn 4s ease-out both}
  .fx-shadowfront{background:radial-gradient(ellipse 140px 220px at 0% 60%,rgba(0,0,0,.75),transparent 70%),radial-gradient(ellipse 140px 200px at 100% 30%,rgba(0,0,0,.7),transparent 70%);animation:fxCreep 7s ease-in-out infinite alternate}
  @keyframes fxCreep{from{transform:scaleX(.8);opacity:.6}to{transform:scaleX(1.25);opacity:1}}
  .fx-rings{border:2px solid rgba(255,240,180,.55);border-radius:50%;inset:auto;left:50%;top:50%;width:20px;height:20px;transform:translate(-50%,-50%);animation:fxRing 3s ease-out infinite}
  .fx-rings2{animation-delay:-1.5s}
  @keyframes fxRing{from{width:20px;height:20px;opacity:1}to{width:520px;height:520px;opacity:0}}
  .fx-ink{background:radial-gradient(circle at 30% 40%,rgba(5,5,25,.9),transparent 22%),radial-gradient(circle at 70% 65%,rgba(5,5,25,.85),transparent 18%),radial-gradient(circle at 55% 20%,rgba(5,5,25,.8),transparent 14%);filter:blur(6px);animation:fxInk 14s ease-in-out infinite alternate}
  @keyframes fxInk{from{transform:scale(.6);opacity:.4}to{transform:scale(1.5);opacity:.95}}
  .fx-sand{background:linear-gradient(180deg,rgba(200,150,70,.3),rgba(120,80,30,.45))}
  .fx-forest{background:linear-gradient(180deg,rgba(20,60,20,.35),rgba(10,30,10,.55))}
  .fx-dapple{inset:-20%;background:radial-gradient(circle 40px at 20% 30%,rgba(255,250,200,.22),transparent),radial-gradient(circle 55px at 60% 20%,rgba(255,250,200,.18),transparent),radial-gradient(circle 35px at 80% 60%,rgba(255,250,200,.2),transparent),radial-gradient(circle 50px at 35% 75%,rgba(255,250,200,.17),transparent);background-size:280px 260px;filter:blur(5px);animation:fxCaust 8s ease-in-out infinite alternate}
  .fx-beach{background:linear-gradient(180deg,rgba(255,200,120,.2),rgba(0,120,160,.35))}
  .fx-foam{top:auto;height:40%;background:radial-gradient(ellipse 60px 14px at 10% 10%,rgba(255,255,255,.55),transparent 70%),radial-gradient(ellipse 80px 16px at 45% 20%,rgba(255,255,255,.5),transparent 70%),radial-gradient(ellipse 70px 14px at 80% 8%,rgba(255,255,255,.5),transparent 70%);background-size:300px 60px;filter:blur(2px);animation:fxFoam 5s ease-in-out infinite}
  @keyframes fxFoam{0%,100%{transform:translateY(40%);opacity:.4}50%{transform:translateY(0);opacity:1}}
  .fx-desert{background:linear-gradient(180deg,rgba(255,180,80,.25),rgba(150,90,30,.35));animation:fxPulse 6s ease-in-out infinite}
  .fx-ash{background:linear-gradient(180deg,rgba(70,90,60,.45),rgba(40,40,40,.65))}
  .fx-cell{background:repeating-linear-gradient(90deg,rgba(0,0,0,.55) 0 10px,transparent 10px 60px),rgba(10,10,15,.45)}
  .fx-train{background:linear-gradient(180deg,rgba(10,10,25,.7),rgba(30,25,40,.6))}
  .fx-tunnel{background:radial-gradient(circle,rgba(0,0,0,.2),rgba(0,0,10,.85))}
  .fx-alarmbg{background:rgba(40,0,0,.45)}
  /* разовые события */
  .fx-shake{animation:fxShake .7s cubic-bezier(.36,.07,.19,.97) both}
  @keyframes fxShake{10%,90%{transform:translate(-2px,1px)}20%,80%{transform:translate(3px,-2px)}30%,50%,70%{transform:translate(-5px,2px) rotate(-.5deg)}40%,60%{transform:translate(5px,-1px) rotate(.5deg)}}
  .fx-flash{background:#fff;animation:fxFlash 1.4s ease-out forwards}
  @keyframes fxFlash{0%{opacity:.85}100%{opacity:0}}
  .fx-after{background:radial-gradient(circle at 50% 45%,rgba(0,0,0,.5),transparent 25%);animation:fxAfter 4s ease-out forwards}
  @keyframes fxAfter{0%{opacity:0}20%{opacity:1}100%{opacity:0}}
  .fx-bolt{background:rgba(210,225,255,.55);opacity:0}
  .fx-bolt.on{animation:fxBolt .55s ease-out}
  @keyframes fxBolt{0%{opacity:0}8%{opacity:1}22%{opacity:.15}34%{opacity:.75}100%{opacity:0}}
  @media (prefers-reduced-motion:reduce){.fxl{animation:none!important}}
  `;

  // ---------------------------------------------------------------- частицы (пресеты)
  const P = {
    rain: { n: 60, from: "top", vx: [-40, -10], vy: [700, 950], size: [10, 22], colors: ["rgba(170,200,255,.55)"], shape: "streak", w: 1.1 },
    glassrain: { n: 14, from: "top", vx: [-4, 4], vy: [25, 70], size: [3, 7], colors: ["rgba(200,230,255,.45)"], shape: "drop", wobble: [3, 1.5] },
    neonrain: { n: 50, from: "top", vx: [-16, 0], vy: [400, 600], size: [12, 24], colors: ["rgba(255,80,215,.95)", "rgba(60,240,255,.95)", "rgba(190,120,255,.9)"], shape: "streak", w: 1.7, glow: 16 },
    snow: { n: 45, from: "top", vx: [-15, 15], vy: [25, 60], size: [1.5, 3.5], colors: ["rgba(255,255,255,.85)"], shape: "dot", wobble: [18, .6] },
    blizzard: { n: 90, from: "right", vx: [-900, -600], vy: [40, 120], size: [8, 24], colors: ["rgba(255,255,255,.5)", "rgba(220,235,255,.35)"], shape: "streak", w: 1.2 },
    sand: { n: 110, from: "right", vx: [-520, -340], vy: [80, 170], size: [2, 6], colors: ["rgba(230,190,110,.55)", "rgba(200,160,90,.45)"], shape: "streak", w: 1.4 },
    leaves: { n: 9, from: "top", vx: [-25, 25], vy: [30, 60], size: [6, 11], colors: ["#c8642a", "#d99a2b", "#a33b1f", "#8a6d1f"], shape: "leaf", wobble: [30, .5], spin: [1, 3] },
    petals: { n: 12, from: "top", vx: [-20, 20], vy: [18, 40], size: [4, 7], colors: ["rgba(255,200,230,.85)", "rgba(255,255,255,.8)"], shape: "leaf", wobble: [25, .4], spin: [1, 2] },
    embers: { n: 24, from: "bottom", vx: [-15, 15], vy: [-90, -40], size: [1.2, 2.6], colors: ["#ffb347", "#ff7b22", "#ffd36b"], shape: "glow", glow: 8, wobble: [10, 1.3], life: [2, 4.5] },
    sparks: { n: 55, from: "bottom", vx: [-30, 30], vy: [-180, -90], size: [1, 2.4], colors: ["#ff9a3c", "#ffcf5c", "#ff5a1f"], shape: "glow", glow: 6, wobble: [14, 2], life: [1.2, 3] },
    ash: { n: 30, from: "top", vx: [-12, 12], vy: [18, 45], size: [1.5, 4], colors: ["rgba(180,180,180,.7)", "rgba(120,120,120,.7)"], shape: "flake", wobble: [20, .5], spin: [.5, 1.5] },
    fireash: { n: 18, from: "bottom", vx: [-20, 20], vy: [-50, -25], size: [1.5, 3.5], colors: ["rgba(90,90,90,.7)", "rgba(140,140,140,.6)"], shape: "flake", wobble: [18, .6], spin: [.5, 1.5], life: [3, 6] },
    dust: { n: 30, from: "any", vx: [-6, 6], vy: [-6, 6], size: [.8, 2], colors: ["rgba(255,235,180,.7)"], shape: "dot", brown: 12, twinkle: 1.2 },
    stars: { n: 60, from: "any", vx: [0, 0], vy: [0, 0], size: [.6, 1.6], colors: ["#fff", "#cfe0ff", "#ffe9c4"], shape: "dot", twinkle: 1.5 },
    starfield: { n: 70, from: "any", vx: [-6, -2], vy: [-2, 2], size: [.6, 1.8], colors: ["#fff", "#cfe0ff"], shape: "dot", twinkle: .8 },
    magic: { n: 26, from: "bottom", vx: [-10, 10], vy: [-45, -20], size: [1.5, 3.2], colors: ["#c77dff", "#7df9ff", "#ff7de9", "#fff59d"], shape: "glow", glow: 10, wobble: [14, .8], life: [3, 6], hue: 40 },
    fireflies: { n: 16, from: "any", vx: [-10, 10], vy: [-10, 10], size: [1.6, 2.8], colors: ["#e8ff6b", "#ffe36b"], shape: "glow", glow: 12, brown: 20, twinkle: .7 },
    plankton: { n: 40, from: "any", vx: [-5, 5], vy: [-8, 2], size: [.8, 2], colors: ["#3ef6ff", "#33ffb0", "#5c9dff"], shape: "glow", glow: 8, brown: 8, twinkle: .9 },
    bubbles: { n: 14, from: "bottom", vx: [-6, 6], vy: [-70, -30], size: [2, 6], colors: ["rgba(200,240,255,.6)"], shape: "ring", wobble: [8, 1.5] },
    swampbubbles: { n: 8, from: "bottom", vx: [-3, 3], vy: [-30, -14], size: [3, 7], colors: ["rgba(160,255,120,.55)"], shape: "ring", wobble: [5, 1], life: [2, 5] },
    souls: { n: 7, from: "bottom", vx: [-8, 8], vy: [-35, -18], size: [10, 18], colors: ["rgba(120,255,200,.25)", "rgba(190,140,255,.25)"], shape: "wisp", glow: 16, wobble: [26, .4], life: [5, 9] },
    runes: { n: 7, from: "any", vx: [0, 0], vy: [0, 0], size: [16, 28], colors: ["#ff9f43", "#9ff0ff", "#c38bff"], shape: "char", chars: RUNES, glow: 14, life: [3, 6] },
    glints: { n: 9, from: "any", vx: [0, 0], vy: [0, 0], size: [5, 11], colors: ["#fff", "#ffe08a", "#bff4ff"], shape: "star", glow: 10, life: [1, 2.6] },
    eyes: { n: 4, from: "any", vx: [-3, 3], vy: [0, 0], size: [1.8, 2.6], colors: ["#ff3b30", "#ffd60a", "#b6ff3b"], shape: "eye", glow: 8, life: [2.5, 5] },
    disco: { n: 40, from: "any", vx: [0, 0], vy: [0, 0], size: [1.5, 3.5], colors: ["#fff", "#ff7de9", "#7df9ff", "#fff59d"], shape: "glow", glow: 6, orbit: .25 },
    portal: { n: 60, from: "any", vx: [0, 0], vy: [0, 0], size: [1, 2.4], colors: ["#ffd36b", "#fff", "#c77dff"], shape: "glow", glow: 6, spiral: 1 },
    warp: { n: 70, from: "center", vx: [0, 0], vy: [0, 0], size: [1, 2], colors: ["#fff", "#bfe9ff"], shape: "warp", radial: 1 },
    trainlights: { n: 12, from: "right", vx: [-1600, -900], vy: [0, 0], size: [40, 120], colors: ["rgba(255,220,150,.55)", "rgba(200,220,255,.45)"], shape: "streak", w: 2, glow: 8 },
    drips: { n: 6, from: "top", vx: [0, 0], vy: [0, 0], size: [1.5, 2.5], colors: ["rgba(180,220,255,.7)"], shape: "drop", gravity: 420, life: [2, 5], delay: 1 },
    papers: { n: 7, from: "top", vx: [-25, 25], vy: [20, 45], size: [9, 14], colors: ["#f3ead2", "#e8dcc0", "#fffaf0"], shape: "paper", wobble: [35, .35], spin: [.4, 1.2] },
    coins: { n: 14, from: "top", vx: [-6, 6], vy: [60, 110], size: [5, 8], colors: ["#ffd34d", "#f5b82e", "#ffe27a"], shape: "coin", spin: [3, 6], glow: 6 },
    cards: { n: 8, from: "top", vx: [-20, 20], vy: [25, 55], size: [10, 14], colors: ["#fff"], shape: "card", chars: "♠♥♦♣", wobble: [30, .3], spin: [.5, 1.5] },
    // 😀 эмодзи-частицы (владелец 27.10: «как падающая бумага и карты — шедеврально»)
    letters: { from: "top", vx: [-20, 20], vy: [25, 50], size: [16, 22], colors: ["#fff"], shape: "emoji", chars: ["✉️", "📩", "💌"], wobble: [30, .35], spin: [.3, .9], n: 8 },
    money: { from: "top", vx: [-25, 25], vy: [35, 70], size: [16, 22], colors: ["#fff"], shape: "emoji", chars: ["💵", "💸", "💶"], wobble: [35, .4], spin: [.5, 1.4], n: 10 },
    gems: { from: "any", vx: [0, 0], vy: [0, 0], size: [14, 22], colors: ["#fff"], shape: "emoji", chars: ["💎", "💍", "✨"], life: [2, 4], n: 7 },
    keys: { from: "top", vx: [-10, 10], vy: [30, 55], size: [16, 22], colors: ["#fff"], shape: "emoji", chars: ["🗝️", "🔑"], spin: [.8, 2], n: 6 },
    ghostsE: { from: "bottom", vx: [-10, 10], vy: [-35, -15], size: [20, 30], colors: ["#fff"], shape: "emoji", chars: ["👻"], wobble: [28, .3], life: [5, 9], alpha: .45, n: 4 },
    bats: { from: "right", vx: [-160, -90], vy: [-15, 15], size: [16, 24], colors: ["#fff"], shape: "emoji", chars: ["🦇"], wobble: [40, 1.6], n: 6 },
    notes: { from: "bottom", vx: [-12, 12], vy: [-55, -30], size: [16, 24], colors: ["#fff"], shape: "emoji", chars: ["🎵", "🎶", "🎼"], wobble: [22, .6], life: [3, 6], n: 9 },
    hearts: { from: "bottom", vx: [-10, 10], vy: [-45, -25], size: [14, 22], colors: ["#fff"], shape: "emoji", chars: ["💖", "💕", "❤️", "💗"], wobble: [20, .5], life: [3, 6], n: 9 },
    confetti: { from: "top", vx: [-30, 30], vy: [50, 90], size: [16, 22], colors: ["#fff"], shape: "emoji", chars: ["🎉", "🎊", "🥳", "✨"], wobble: [30, .8], spin: [1, 3], n: 12 },
    balloons: { from: "bottom", vx: [-8, 8], vy: [-50, -25], size: [22, 32], colors: ["#fff"], shape: "emoji", chars: ["🎈"], wobble: [16, .3], n: 6 },
    snowE: { from: "top", vx: [-12, 12], vy: [25, 50], size: [12, 20], colors: ["#fff"], shape: "emoji", chars: ["❄️", "❅", "❆"], wobble: [20, .5], spin: [.3, 1], n: 12 },
    autumn: { from: "top", vx: [-25, 25], vy: [30, 55], size: [16, 24], colors: ["#fff"], shape: "emoji", chars: ["🍁", "🍂"], wobble: [40, .45], spin: [1, 2.5], n: 10 },
    gearsE: { from: "top", vx: [-8, 8], vy: [35, 60], size: [16, 26], colors: ["#fff"], shape: "emoji", chars: ["⚙️", "🔩", "🔧"], spin: [1, 3], n: 8 },
    butterflies: { from: "any", vx: [-15, 15], vy: [-15, 15], size: [16, 22], colors: ["#fff"], shape: "emoji", chars: ["🦋"], brown: 30, n: 5 },
    fish: { from: "left", vx: [30, 70], vy: [-6, 6], size: [18, 26], colors: ["#fff"], shape: "emoji", chars: ["🐟", "🐠", "🐡"], wobble: [10, .5], flip: 1, n: 6 },
    ufo: { from: "left", vx: [40, 80], vy: [-8, 8], size: [22, 30], colors: ["#fff"], shape: "emoji", chars: ["🛸", "🚀", "🛰️"], wobble: [25, .5], flip: 1, n: 3 },
    sparkle: { from: "any", vx: [0, 0], vy: [0, 0], size: [12, 20], colors: ["#fff"], shape: "emoji", chars: ["✨", "⭐", "🌟"], life: [1.5, 3.5], n: 10 },
    zzz: { from: "bottom", vx: [-6, 6], vy: [-30, -15], size: [16, 26], colors: ["#fff"], shape: "emoji", chars: ["💤"], wobble: [18, .4], life: [4, 7], alpha: .7, n: 4 },
    question: { from: "any", vx: [-4, 4], vy: [-8, -2], size: [18, 30], colors: ["#fff"], shape: "emoji", chars: ["❓", "❔", "🔍"], life: [2.5, 5], alpha: .75, n: 6 },
    clocks: { from: "any", vx: [0, 0], vy: [0, 0], size: [16, 26], colors: ["#fff"], shape: "emoji", chars: ["⏰", "⌛", "⏳", "🕰️"], life: [2, 4], n: 6 },
    food: { from: "top", vx: [-20, 20], vy: [40, 75], size: [18, 26], colors: ["#fff"], shape: "emoji", chars: ["🍕", "🍔", "🌭", "🍩", "🧁", "🍟"], spin: [.8, 2.2], n: 10 },
    skulls: { from: "any", vx: [0, 0], vy: [-4, 4], size: [16, 24], colors: ["#fff"], shape: "emoji", chars: ["💀"], life: [3, 6], alpha: .4, n: 4 },
    spiders: { from: "top", vx: [0, 0], vy: [10, 22], size: [16, 22], colors: ["#fff"], shape: "emoji", chars: ["🕷️"], life: [5, 9], thread: 1, n: 4 },
    pumpkins: { from: "any", vx: [0, 0], vy: [0, 0], size: [20, 30], colors: ["#fff"], shape: "emoji", chars: ["🎃"], life: [3, 6], twinkle: .5, n: 5 },
    candlesE: { from: "any", vx: [0, 0], vy: [0, 0], size: [18, 26], colors: ["#fff"], shape: "emoji", chars: ["🕯️"], twinkle: .9, n: 7 },
    paws: { from: "any", vx: [0, 0], vy: [0, 0], size: [14, 20], colors: ["#fff"], shape: "emoji", chars: ["🐾"], life: [2, 4], alpha: .6, n: 7 },
    dice: { from: "top", vx: [-15, 15], vy: [50, 90], size: [16, 24], colors: ["#fff"], shape: "emoji", chars: ["🎲"], spin: [2, 5], n: 7 },
    popcorn: { from: "bottom", vx: [-30, 30], vy: [-140, -90], size: [14, 20], colors: ["#fff"], shape: "emoji", chars: ["🍿"], gravity: 140, spin: [1, 3], life: [2, 3.5], n: 8 },
    bolts: { from: "any", vx: [0, 0], vy: [0, 0], size: [16, 26], colors: ["#fff"], shape: "emoji", chars: ["⚡"], life: [.8, 1.8], n: 5 },
    flowers: { from: "top", vx: [-18, 18], vy: [22, 45], size: [14, 22], colors: ["#fff"], shape: "emoji", chars: ["🌸", "🌼", "🌷", "🌺"], wobble: [30, .4], spin: [.5, 1.5], n: 10 },
    hourglass: { n: 5, from: "top", vx: [0, 0], vy: [70, 110], size: [1, 1.6], colors: ["rgba(230,200,140,.7)"], shape: "stream" },
  };

  // ---------------------------------------------------------------- эффекты
  // g — группа для галереи; back/front — CSS-классы слоёв; parts — пресеты частиц; special — режимы холста; once — событие
  const FX = {
    fog:        { g: "nature", ru: "🌫 Туман", en: "🌫 Fog", back: ["fx-dark", "fx-fog", "fx-fog fx-fog2"] },
    rain:       { g: "nature", ru: "🌧 Дождь", en: "🌧 Rain", back: ["fx-night"], parts: ["rain"] },
    storm:      { g: "nature", ru: "⛈ Гроза", en: "⛈ Storm", back: ["fx-night", "fx-fog"], parts: ["rain"], lightning: true },
    glassrain:  { g: "nature", ru: "🪟 Дождь по стеклу", en: "🪟 Rain on glass", back: ["fx-night"], parts: ["glassrain", "rain"] },
    snow:       { g: "nature", ru: "❄️ Снег", en: "❄️ Snow", back: ["fx-night"], parts: ["snow"] },
    blizzard:   { g: "nature", ru: "🌨 Буран", en: "🌨 Blizzard", back: ["fx-night", "fx-fog"], parts: ["blizzard", "snow"], front: ["fx-frost"] },
    frost:      { g: "nature", ru: "🥶 Мороз", en: "🥶 Frost", back: ["fx-night"], parts: ["snow"], front: ["fx-frost"] },
    sandstorm:  { g: "nature", ru: "🏜 Песчаная буря", en: "🏜 Sandstorm", back: ["fx-sand"], parts: ["sand"] },
    desert:     { g: "nature", ru: "☀️ Зной", en: "☀️ Heat", back: ["fx-desert"], parts: ["dust"] },
    leaves:     { g: "nature", ru: "🍂 Листопад", en: "🍂 Falling leaves", back: ["fx-forest"], parts: ["leaves"] },
    forest:     { g: "nature", ru: "🌳 Свет сквозь листву", en: "🌳 Light through leaves", back: ["fx-forest", "fx-dapple"], parts: ["fireflies"] },
    beach:      { g: "nature", ru: "🏝 Пляж", en: "🏝 Beach", back: ["fx-beach", "fx-foam"] },
    water:      { g: "water", ru: "💧 Ночной бассейн", en: "💧 Night pool", back: ["fx-pool", "fx-caust", "fx-caust fx-caust2", "fx-ripple"] },
    underwater: { g: "water", ru: "🌊 Под водой", en: "🌊 Underwater", back: ["fx-deep", "fx-rays"], parts: ["bubbles"] },
    abyss:      { g: "water", ru: "🦑 Бездна", en: "🦑 Abyss", back: ["fx-abyss"], parts: ["plankton"] },
    swamp:      { g: "water", ru: "🐸 Болото", en: "🐸 Swamp", back: ["fx-swamp", "fx-swampglow", "fx-fog"], parts: ["swampbubbles"] },
    fire:       { g: "fire", ru: "🔥 Костёр в пещере", en: "🔥 Campfire cave", back: ["fx-cave", "fx-flicker", "fx-shadows"], parts: ["embers"] },
    blaze:      { g: "fire", ru: "🧯 Пожар", en: "🧯 Blaze", back: ["fx-blaze"], parts: ["sparks", "fireash"] },
    lava:       { g: "fire", ru: "🌋 Лава", en: "🌋 Lava", back: ["fx-lava", "fx-cracks"], parts: ["embers"] },
    candle:     { g: "fire", ru: "🕯 Свеча", en: "🕯 Candle", back: ["fx-candle"], parts: ["dust"] },
    smoke:      { g: "smoke", ru: "💨 Дым из-за угла", en: "💨 Drifting smoke", back: ["fx-dark", "fx-smoke", "fx-smoke fx-smoke2"] },
    smog:       { g: "smoke", ru: "🏭 Смог фабрики", en: "🏭 Factory smog", back: ["fx-smog", "fx-smoke", "fx-smoke fx-smoke2"], parts: ["ash"] },
    steam:      { g: "smoke", ru: "♨️ Пар", en: "♨️ Steam", back: ["fx-dark", "fx-steam", "fx-steam fx-steam2"] },
    ash:        { g: "smoke", ru: "☢️ Ядерная зима", en: "☢️ Nuclear winter", back: ["fx-ash", "fx-aurora"], parts: ["ash"] },
    night:      { g: "sky", ru: "🌙 Ночь", en: "🌙 Night", back: ["fx-night"], parts: ["stars"] },
    space:      { g: "sky", ru: "🌌 Космос", en: "🌌 Space", back: ["fx-space"], parts: ["starfield"] },
    aurora:     { g: "sky", ru: "🌠 Северное сияние", en: "🌠 Aurora", back: ["fx-night", "fx-aurora"], parts: ["stars"] },
    warp:       { g: "sky", ru: "🚀 Гиперпрыжок", en: "🚀 Warp speed", back: ["fx-tunnel"], parts: ["warp"] },
    portal:     { g: "mystic", ru: "🌀 Портал времени", en: "🌀 Time portal", back: ["fx-magic"], parts: ["portal"] },
    magic:      { g: "mystic", ru: "✨ Магия", en: "✨ Magic", back: ["fx-magic"], parts: ["magic"] },
    fireflies:  { g: "mystic", ru: "🧚 Светлячки", en: "🧚 Fireflies", back: ["fx-glowgold"], parts: ["fireflies"] },
    runes:      { g: "mystic", ru: "ᚱ Живые руны", en: "ᚱ Living runes", back: ["fx-dark"], parts: ["runes", "dust"] },
    treasure:   { g: "mystic", ru: "💎 Сокровищница", en: "💎 Treasure", back: ["fx-glowgold"], parts: ["glints"] },
    ghosts:     { g: "mystic", ru: "👻 Души", en: "👻 Spirits", back: ["fx-ghost"], parts: ["souls"] },
    dream:      { g: "mystic", ru: "💭 Сон", en: "💭 Dream", back: ["fx-dream"], parts: ["petals"] },
    insight:    { g: "mystic", ru: "💡 Озарение", en: "💡 Insight", back: ["fx-dark", "fx-rings", "fx-rings fx-rings2"] },
    club:       { g: "city", ru: "🪩 Клуб", en: "🪩 Club", back: ["fx-clubbg", "fx-lasers", "fx-lasers fx-lasers2"], parts: ["disco"] },
    neon:       { g: "city", ru: "🌃 Неоновый дождь", en: "🌃 Neon rain", back: ["fx-void"], parts: ["neonrain"] },
    siren:      { g: "city", ru: "🚓 Сирена", en: "🚓 Siren", back: ["fx-noir"], front: ["fx-sirenL", "fx-sirenR"] },
    alarm:      { g: "city", ru: "🚨 Тревога", en: "🚨 Alarm", back: ["fx-alarmbg"], front: ["fx-beacon"] },
    noir:       { g: "city", ru: "🕵️ Жалюзи", en: "🕵️ Blinds", back: ["fx-noir", "fx-blinds", "fx-headl"], parts: ["dust"] },
    headlights: { g: "city", ru: "🚗 Фары навстречу", en: "🚗 Oncoming headlights", back: ["fx-noir"], special: "carlights" },
    flashlight: { g: "city", ru: "🔦 Фонарик", en: "🔦 Flashlight", back: ["fx-torch"], parts: ["dust"], torch: true },
    train:      { g: "city", ru: "🚇 Поезд", en: "🚇 Train", back: ["fx-train"], parts: ["trainlights"] },
    hologram:   { g: "tech", ru: "🛰 Голограмма", en: "🛰 Hologram", back: ["fx-holo", "fx-sweep"] },
    scanner:    { g: "tech", ru: "📡 Сканер", en: "📡 Scanner", back: ["fx-holo", "fx-scan"] },
    matrix:     { g: "tech", ru: "🟩 Цифровой водопад", en: "🟩 Digital rain", back: ["fx-matrixbg"], special: "matrix" },
    glitch:     { g: "tech", ru: "📺 Сбой", en: "📺 Glitch", back: ["fx-holo", "fx-glitch"] },
    vhs:        { g: "tech", ru: "📼 Старая плёнка", en: "📼 Old film", back: ["fx-film", "fx-vhs"], special: "film" },
    radar:      { g: "tech", ru: "🎯 Радар", en: "🎯 Radar", back: ["fx-radar", "fx-radarsweep"] },
    electric:   { g: "tech", ru: "⚡ Высокое напряжение", en: "⚡ High voltage", back: ["fx-dark"], special: "arcs" },
    fan:        { g: "tech", ru: "🌀 Вентилятор", en: "🌀 Fan", back: ["fx-fanlight", "fx-fan"], parts: ["dust"] },
    gears:      { g: "tech", ru: "⚙️ Шестерёнки", en: "⚙️ Gears", back: ["fx-attic", "fx-gears fx-gearA", "fx-gears fx-gearB"] },
    dungeon:    { g: "dark", ru: "🕳 Подземелье", en: "🕳 Dungeon", back: ["fx-dungeon"], parts: ["drips"] },
    attic:      { g: "dark", ru: "🏚 Пыль в лучах", en: "🏚 Dust in light", back: ["fx-attic", "fx-beam"], parts: ["dust"] },
    prison:     { g: "dark", ru: "⛓ Камера", en: "⛓ Cell", back: ["fx-cell", "fx-beam"] },
    eyes:       { g: "dark", ru: "👀 Глаза во тьме", en: "👀 Eyes in the dark", back: ["fx-dark"], parts: ["eyes"] },
    shadows:    { g: "dark", ru: "🫥 Тени по краям", en: "🫥 Creeping shadows", back: ["fx-dark"], front: ["fx-shadowfront"] },
    ink:        { g: "dark", ru: "🖋 Чернильный омут", en: "🖋 Ink", back: ["fx-ink"] },
    oil:        { g: "detective", ru: "🛢 Лужа под фонарём", en: "🛢 Puddle under a torch", back: ["fx-torch"], special: "oil", torch: true },
    steps:      { g: "detective", ru: "👣 Следы шагов", en: "👣 Footsteps", back: ["fx-noir"], special: "steps" },
    papers:     { g: "detective", ru: "📄 Летящие бумаги", en: "📄 Flying papers", back: ["fx-noir", "fx-headl"], parts: ["papers"] },
    coins:      { g: "detective", ru: "🪙 Золотой дождь", en: "🪙 Golden rain", back: ["fx-glowgold"], parts: ["coins"] },
    cards:      { g: "detective", ru: "🃏 Карты казино", en: "🃏 Casino cards", back: ["fx-clubbg"], parts: ["cards"] },
    letters:    { g: "detective", ru: "✉️ Летящие письма", en: "✉️ Flying letters", back: ["fx-noir"], parts: ["letters"] },
    money:      { g: "heist", ru: "💸 Денежный дождь", en: "💸 Money rain", back: ["fx-glowgold"], parts: ["money"] },
    gems:       { g: "heist", ru: "💎 Сокровищница", en: "💎 Treasure vault", back: ["fx-dark"], parts: ["gems"] },
    keys:       { g: "heist", ru: "🗝 Ключи и замки", en: "🗝 Keys and locks", back: ["fx-noir"], parts: ["keys"] },
    ghostsE:    { g: "dark", ru: "👻 Призраки", en: "👻 Ghosts", back: ["fx-dark", "fx-fog"], parts: ["ghostsE"] },
    bats:       { g: "dark", ru: "🦇 Летучие мыши", en: "🦇 Bats", back: ["fx-night"], parts: ["bats"] },
    spiders:    { g: "dark", ru: "🕷 Пауки на паутинке", en: "🕷 Spiders on threads", back: ["fx-attic"], parts: ["spiders"] },
    skulls:     { g: "dark", ru: "💀 Черепа во тьме", en: "💀 Skulls in the dark", back: ["fx-dungeon"], parts: ["skulls"] },
    pumpkins:   { g: "dark", ru: "🎃 Тыквенная ночь", en: "🎃 Pumpkin night", back: ["fx-night"], parts: ["pumpkins"] },
    candlesE:   { g: "dark", ru: "🕯 Свечи во мраке", en: "🕯 Candles in the dark", back: ["fx-void"], special: "candles" },
    keypad:     { g: "detective", ru: "🔢 Кодовый замок: набор", en: "🔢 Code lock: typing", back: ["fx-dark"], special: "keypad" },
    keypadok:   { g: "detective", ru: "🔢 Кодовый замок: открыт", en: "🔢 Code lock: open", back: ["fx-dark"], special: "keypad", lock: "open" },
    keypadno:   { g: "detective", ru: "🔢 Кодовый замок: ошибка", en: "🔢 Code lock: error", back: ["fx-dark"], special: "keypad", lock: "error" },
    notes:      { g: "fun", ru: "🎵 Музыка", en: "🎵 Music", back: ["fx-clubbg"], parts: ["notes"] },
    hearts:     { g: "fun", ru: "💖 Сердечки", en: "💖 Hearts", back: ["fx-dream"], parts: ["hearts"] },
    confetti:   { g: "fun", ru: "🎉 Конфетти", en: "🎉 Confetti", back: ["fx-glowgold"], parts: ["confetti"] },
    balloons:   { g: "fun", ru: "🎈 Воздушные шары", en: "🎈 Balloons", back: ["fx-dream"], parts: ["balloons"] },
    food:       { g: "fun", ru: "🍕 Еда с неба", en: "🍕 Food from the sky", back: ["fx-dream"], parts: ["food"] },
    popcorn:    { g: "fun", ru: "🍿 Попкорн", en: "🍿 Popcorn", back: ["fx-film"], parts: ["popcorn"] },
    dice:       { g: "fun", ru: "🎲 Кости", en: "🎲 Dice", back: ["fx-clubbg"], parts: ["dice"] },
    zzz:        { g: "mind", ru: "💤 Сон", en: "💤 Sleep", back: ["fx-night"], parts: ["zzz"] },
    question:   { g: "mind", ru: "❓ Загадка", en: "❓ Mystery", back: ["fx-noir"], parts: ["question"] },
    clocks:     { g: "mind", ru: "⏰ Время уходит", en: "⏰ Time is running out", back: ["fx-dark"], parts: ["clocks"] },
    autumn:     { g: "nature", ru: "🍁 Кленовые листья", en: "🍁 Maple leaves", back: ["fx-forest"], parts: ["autumn"] },
    flowers:    { g: "nature", ru: "🌸 Цветочный дождь", en: "🌸 Flower rain", back: ["fx-forest"], parts: ["flowers"] },
    butterflies:{ g: "nature", ru: "🦋 Бабочки", en: "🦋 Butterflies", back: ["fx-forest"], parts: ["butterflies"] },
    snowE:      { g: "nature", ru: "❄️ Снежинки", en: "❄️ Snowflakes", back: ["fx-night"], parts: ["snowE"] },
    paws:       { g: "nature", ru: "🐾 Следы зверя", en: "🐾 Animal tracks", back: ["fx-forest"], parts: ["paws"] },
    fish:       { g: "water", ru: "🐠 Рыбы", en: "🐠 Fish", back: ["fx-deep", "fx-caust"], parts: ["fish"] },
    gearsE:     { g: "tech", ru: "⚙️ Шестерёнки", en: "⚙️ Gears", back: ["fx-dark"], parts: ["gearsE"] },
    ufo:        { g: "sky", ru: "🛸 Тарелки и ракеты", en: "🛸 Saucers and rockets", back: ["fx-space"], parts: ["ufo"] },
    sparkle:    { g: "mystic", ru: "✨ Звёздная пыль", en: "✨ Stardust", back: ["fx-dark"], parts: ["sparkle"] },
    bolts:      { g: "tech", ru: "⚡ Разряды", en: "⚡ Sparks", back: ["fx-dark"], parts: ["bolts"] },
    handprints: { g: "dark", ru: "🖐 Руки на стекле", en: "🖐 Hands on the glass", back: ["fx-dark", "fx-fog"], special: "hands" },
    mirror:     { g: "dark", ru: "🪞 Зеркало: фигура", en: "🪞 Mirror: a figure", back: ["fx-dark"], special: "mirror" },
    mirrorface: { g: "dark", ru: "🪞 Зеркало: лицо", en: "🪞 Mirror: a face", back: ["fx-dark"], special: "mirror", draw: "face" },
    mirrortext: { g: "dark", ru: "🪞 Зеркало: надпись", en: "🪞 Mirror: writing", back: ["fx-dark"], special: "mirror", text: "НЕ ОБОРАЧИВАЙСЯ" },
    hourglass:  { g: "dark", ru: "⏳ Песок времени", en: "⏳ Sands of time", back: ["fx-attic"], parts: ["hourglass", "dust"] },
    heartbeat:  { g: "mind", ru: "💓 Биение сердца", en: "💓 Heartbeat", front: ["fx-heart"] },
    panic:      { g: "mind", ru: "😱 Паника", en: "😱 Panic", back: ["fx-dark"], front: ["fx-panic"] },
    poison:     { g: "mind", ru: "🧪 Отравление", en: "🧪 Poison", back: ["fx-poison"], parts: ["swampbubbles"] },
    quake:      { g: "action", ru: "🌋 Толчок", en: "🌋 Tremor", back: ["fx-attic"], parts: ["ash"], once: "shake" },
    flash:      { g: "action", ru: "📸 Вспышка", en: "📸 Flash", back: ["fx-dark"], once: "flash" },
  };

  // ---------------------------------------------------------------- состояние
  let state = null;
  const OFF_KEY = "fx_off";
  function enabled() { try { return localStorage.getItem(OFF_KEY) !== "1"; } catch (e) { return true; } }
  function setEnabled(on) { try { localStorage.setItem(OFF_KEY, on ? "0" : "1"); } catch (e) { /* приватный режим */ } }

  function injectCss() {
    if (document.getElementById("fxCss")) return;
    const st = document.createElement("style");
    st.id = "fxCss"; st.textContent = CSS;
    document.head.appendChild(st);
  }
  function frontLayer() {
    let f = document.getElementById("fxFront");
    if (!f) { f = document.createElement("div"); f.id = "fxFront"; f.setAttribute("aria-hidden", "true"); document.body.appendChild(f); }
    return f;
  }
  function layer(parent, cls, noFade) {
    const d = document.createElement("div");
    d.className = "fxl " + (noFade ? "" : "fx-fade ") + cls;
    parent.appendChild(d);
    return d;
  }
  const GEAR = (c) => "url(\"data:image/svg+xml," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-50 -50 100 100"><g fill="' + c + '">' +
    Array.from({ length: 10 }, (_, i) => '<rect x="-6" y="-48" width="12" height="16" transform="rotate(' + i * 36 + ')"/>').join("") +
    '<circle r="36"/></g><circle r="12" fill="#000"/></svg>') + "\")";

  // 💧 текстура бликов воды: фрактальный шум, тонкие светлые «прожилки» — рисуется браузером один раз (картинкой),
  // движутся только два слоя (transform) — дёшево даже на слабых телефонах
  const CAUST = seed => "url(\"data:image/svg+xml," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256"><filter id="f" x="0" y="0" width="1" height="1">' +
    '<feTurbulence type="turbulence" baseFrequency="0.022" numOctaves="2" seed="' + seed + '" stitchTiles="stitch"/>' +
    '<feColorMatrix type="matrix" values="0 0 0 0 0.62 0 0 0 0 0.97 0 0 0 0 1 -11 0 0 0 1.05"/></filter>' +
    '<rect width="256" height="256" filter="url(#f)"/></svg>') + "\")";

  // ---------------------------------------------------------------- старт / стоп
  function stop() {
    if (!state) return;
    cancelAnimationFrame(state.raf);
    state.timers.forEach(clearInterval);
    state.timeouts.forEach(clearTimeout);
    if (state.onVis) document.removeEventListener("visibilitychange", state.onVis);
    if (state.ro) state.ro.disconnect();
    state.front.forEach(n => n.remove());
    state = null;
  }

  function start(stage, moods, opts) {
    stop();
    if (!stage) return;
    const back = stage.querySelector(".fx-back");
    if (!back) return;
    back.innerHTML = "";
    const list = (Array.isArray(moods) ? moods : (moods ? [moods] : [])).filter(m => FX[m]).slice(0, 2);
    if (!list.length || !enabled()) return;
    injectCss();
    const still = reduceMotion();
    state = { raf: 0, timers: [], timeouts: [], front: [], parts: [], special: [], torch: false,
      text: String((opts && opts.text) || list.map(id => FX[id].text).find(Boolean) || "").toUpperCase().slice(0, 32),
      draw: ((opts && opts.draw) || list.map(id => FX[id].draw).find(Boolean)) === "face" ? "face" : "figure",
      lock: ["open", "error"].indexOf(opts && opts.lock) >= 0 ? opts.lock : list.map(id => FX[id].lock).find(Boolean) || "",
      words: FX_WORDS[(opts && opts.lang) || ""] || FX_WORDS.en };
    const front = frontLayer();
    list.forEach(id => {
      const fx = FX[id];
      (fx.back || []).forEach(cls => {
        const el = layer(back, cls);
        if (cls.indexOf("fx-gears") >= 0) el.style.backgroundImage = GEAR(cls.indexOf("fx-gearB") >= 0 ? "#d9b46a" : "#9fb4c8");
        if (cls.indexOf("fx-caust") >= 0) el.style.backgroundImage = CAUST(cls.indexOf("fx-caust2") >= 0 ? 7 : 3);
      });
      (fx.front || []).forEach(cls => state.front.push(layer(front, cls)));
      if (still) return;   // «уменьшить движение»: только статичные подложки
      (fx.parts || []).forEach(p => state.parts.push(P[p]));
      if (fx.special) state.special.push(fx.special);
      if (fx.torch) state.torch = true;
      if (fx.lightning) lightning(front);
      if (fx.once === "shake") { stage.classList.remove("fx-shake"); void stage.offsetWidth; stage.classList.add("fx-shake"); }
      if (fx.once === "flash") { state.front.push(layer(front, "fx-flash", true), layer(front, "fx-after", true)); }
    });
    if (!still && (state.parts.length || state.special.length || state.torch)) canvasLoop(stage, back);
  }

  // ⛈ молния: редкая двойная вспышка (не чаще раза в 6 с — без эффекта стробоскопа)
  function lightning(front) {
    const bolt = layer(front, "fx-bolt", true);
    state.front.push(bolt);
    const strike = () => {
      bolt.classList.remove("on"); void bolt.offsetWidth; bolt.classList.add("on");
      state.timeouts.push(setTimeout(strike, rnd(6000, 14000)));
    };
    state.timeouts.push(setTimeout(strike, rnd(1500, 4000)));
  }

  // ---------------------------------------------------------------- холст
  function canvasLoop(stage, back) {
    const cv = document.createElement("canvas");
    back.appendChild(cv);
    const ctx = cv.getContext("2d");
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    let W = 0, H = 0;
    const size = () => {
      W = back.clientWidth; H = back.clientHeight;
      cv.width = Math.max(1, W * dpr); cv.height = Math.max(1, H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    size();
    if (window.ResizeObserver) { state.ro = new ResizeObserver(size); state.ro.observe(back); }
    const area = Math.max(1, (W * H) / 100000);
    const parts = [];
    const spawn = (cfg, first) => {
      const p = { cfg: cfg, size: range(cfg.size), color: pick(cfg.colors), vx: range(cfg.vx), vy: range(cfg.vy),
        t: 0, life: cfg.life ? range(cfg.life) : 0, ph: Math.random() * 6.28, rot: Math.random() * 6.28,
        spin: cfg.spin ? range(cfg.spin) * (Math.random() < .5 ? -1 : 1) : 0, ch: cfg.chars ? pick(cfg.chars) : "", wait: 0 };
      if (cfg.shape === "emoji" && !cfg.spin) p.rot = 0;
      const f = cfg.from;
      p.x = f === "left" ? -20 : f === "right" ? W + 20 : f === "center" ? W / 2 : Math.random() * W;
      p.y = f === "top" ? -20 : f === "bottom" ? H + 20 : f === "center" ? H / 2 : Math.random() * H;
      if (first && (f === "top" || f === "bottom" || f === "left" || f === "right")) {   // сразу по всей сцене, а не с края
        p.x = Math.random() * W; p.y = Math.random() * H;
      }
      if (cfg.radial) { const a = Math.random() * 6.28; p.ang = a; p.r = rnd(2, Math.max(W, H) * .5); }
      if (cfg.spiral) { p.ang = Math.random() * 6.28; p.r = rnd(Math.max(W, H) * .2, Math.max(W, H) * .7); }
      if (cfg.orbit) { p.ang = Math.random() * 6.28; p.r = rnd(20, Math.max(W, H) * .6); }
      if (cfg.delay && !first) p.wait = rnd(0, cfg.delay * 2);
      return p;
    };
    state.parts.forEach(cfg => {
      const n = Math.max(3, Math.min(160, Math.round(cfg.n * area)));
      for (let i = 0; i < n; i++) parts.push(spawn(cfg, true));
    });
    const matrix = state.special.indexOf("matrix") >= 0, arcs = state.special.indexOf("arcs") >= 0,
      film = state.special.indexOf("film") >= 0, car = state.special.indexOf("carlights") >= 0,
      oil = state.special.indexOf("oil") >= 0, steps = state.special.indexOf("steps") >= 0,
      hands = state.special.indexOf("hands") >= 0, mirror = state.special.indexOf("mirror") >= 0;
    const mirrorText = state.text, mirrorDraw = state.draw, lockResult = state.lock, words = state.words;
    const candles = state.special.indexOf("candles") >= 0, keypad = state.special.indexOf("keypad") >= 0;
    let clock = 0;
    const smoke = [];
    const cols = matrix ? Array.from({ length: Math.ceil(W / 14) }, () => Math.random() * -H) : [];
    let arc = null, arcNext = 1.2;
    let torchT = 0;
    let last = performance.now(), paused = false;
    state.onVis = () => { paused = document.hidden; last = performance.now(); if (!paused) state.raf = requestAnimationFrame(frame); };
    document.addEventListener("visibilitychange", state.onVis);

    function drawP(p, cfg, a) {
      ctx.globalAlpha = Math.max(0, Math.min(1, a));
      ctx.fillStyle = ctx.strokeStyle = p.color;
      ctx.shadowBlur = cfg.glow || 0; ctx.shadowColor = p.color;
      const s = p.size;
      switch (cfg.shape) {
        case "streak": {
          const len = s, sp = Math.hypot(p.vx, p.vy) || 1;
          ctx.lineWidth = cfg.w || 1; ctx.beginPath(); ctx.moveTo(p.x, p.y);
          ctx.lineTo(p.x - p.vx / sp * len, p.y - p.vy / sp * len); ctx.stroke(); break;
        }
        case "stream": ctx.fillRect(p.x, p.y, s, 14); break;
        case "warp": {
          const x2 = W / 2 + Math.cos(p.ang) * p.r, y2 = H / 2 + Math.sin(p.ang) * p.r, len = p.r * .12;
          ctx.lineWidth = s; ctx.beginPath(); ctx.moveTo(x2, y2);
          ctx.lineTo(x2 - Math.cos(p.ang) * len, y2 - Math.sin(p.ang) * len); ctx.stroke(); break;
        }
        case "leaf": case "flake":
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot);
          ctx.beginPath(); ctx.ellipse(0, 0, s, s * (cfg.shape === "leaf" ? .45 : .7), 0, 0, 6.28); ctx.fill(); ctx.restore(); break;
        case "paper":
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.shadowBlur = 0;
          ctx.fillRect(-s * .7, -s, s * 1.4, s * 2);
          ctx.fillStyle = "rgba(60,60,80,.35)";
          for (let k = -2; k <= 2; k++) ctx.fillRect(-s * .5, k * s * .35, s * (k === 2 ? .6 : 1), 1);
          ctx.restore(); break;
        case "coin": {   // монета вращается: ширина = |cos(угла)|
          const w = Math.max(.15, Math.abs(Math.cos(p.rot)));
          ctx.beginPath(); ctx.ellipse(p.x, p.y, s * w, s, 0, 0, 6.28); ctx.fill();
          ctx.shadowBlur = 0; ctx.strokeStyle = "rgba(150,100,0,.6)"; ctx.lineWidth = 1; ctx.stroke(); break;
        }
        case "card":
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.shadowBlur = 0;
          ctx.fillStyle = "#fbfbf7"; ctx.fillRect(-s * .7, -s, s * 1.4, s * 2);
          ctx.fillStyle = (p.ch === "♥" || p.ch === "♦") ? "#d22" : "#111"; ctx.font = Math.round(s) + "px serif";
          ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(p.ch, 0, 1);
          ctx.restore(); break;
        case "emoji": {
          ctx.shadowBlur = 0; ctx.globalAlpha = Math.max(0, Math.min(1, a * (cfg.alpha || 1)));
          if (cfg.thread) {   // 🕷 паук спускается на паутинке
            ctx.strokeStyle = "rgba(220,220,230,.45)"; ctx.lineWidth = .8;
            ctx.beginPath(); ctx.moveTo(p.x, 0); ctx.lineTo(p.x, p.y - s * .4); ctx.stroke();
          }
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot);
          if (cfg.flip) ctx.scale(-1, 1);   // рыбы и тарелки «смотрят» по ходу движения
          ctx.font = Math.round(s) + 'px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';
          ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(p.ch, 0, 0);
          ctx.restore(); break;
        }
        case "ring": ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(p.x, p.y, s, 0, 6.28); ctx.stroke(); break;
        case "drop": ctx.beginPath(); ctx.ellipse(p.x, p.y, s * .6, s, 0, 0, 6.28); ctx.fill(); break;
        case "star":
          ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(p.x - s, p.y); ctx.lineTo(p.x + s, p.y);
          ctx.moveTo(p.x, p.y - s); ctx.lineTo(p.x, p.y + s); ctx.stroke(); break;
        case "char": ctx.font = Math.round(s) + "px serif"; ctx.fillText(p.ch, p.x, p.y); break;
        case "eye": ctx.beginPath(); ctx.arc(p.x - 5, p.y, s, 0, 6.28); ctx.arc(p.x + 5, p.y, s, 0, 6.28); ctx.fill(); break;
        case "wisp": {
          const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, s);
          g.addColorStop(0, p.color); g.addColorStop(1, "transparent");
          ctx.shadowBlur = 0; ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(p.x, p.y, s * .6, s, 0, 0, 6.28); ctx.fill(); break;
        }
        default: ctx.beginPath(); ctx.arc(p.x, p.y, s, 0, 6.28); ctx.fill();
      }
    }

    function frame(now) {
      if (!state || paused) return;
      if (!back.isConnected) { stop(); return; }
      const dt = Math.min(.05, (now - last) / 1000); last = now;
      ctx.shadowBlur = 0; ctx.globalAlpha = 1;
      if (matrix) {   // цифровой водопад: шлейф за счёт полупрозрачной заливки
        ctx.fillStyle = "rgba(0,10,0,.12)"; ctx.fillRect(0, 0, W, H);
        ctx.font = "13px monospace"; ctx.fillStyle = "#3dff7a";
        for (let i = 0; i < cols.length; i++) {
          if (Math.random() < .6) ctx.fillText(pick(MATRIX), i * 14, cols[i]);
          cols[i] += 14 * dt * 4.5;   // вдвое медленнее (владелец: «разглядеть во всей красе»)
          if (cols[i] > H + rnd(0, 200)) cols[i] = rnd(-40, 0);
        }
      } else ctx.clearRect(0, 0, W, H);
      if (mirror) drawMirror(clock);
      if (candles) drawCandles(clock);
      if (keypad) drawKeypad(clock, dt);
      if (hands) drawHands(clock, dt);
      for (const p of parts) {
        const c = p.cfg;
        if (p.wait > 0) { p.wait -= dt; continue; }
        p.t += dt;
        if (c.radial) { p.r += p.r * 1.6 * dt + 20 * dt; if (p.r > Math.max(W, H)) { Object.assign(p, spawn(c)); p.r = rnd(2, 30); } }
        else if (c.spiral) {
          p.ang += dt * (60 / Math.max(30, p.r)); p.r -= dt * 22;
          p.x = W / 2 + Math.cos(p.ang) * p.r; p.y = H / 2 + Math.sin(p.ang) * p.r * .6;
          if (p.r < 6) Object.assign(p, spawn(c));
        } else if (c.orbit) {
          p.ang += dt * c.orbit; p.x = W / 2 + Math.cos(p.ang) * p.r; p.y = H * .35 + Math.sin(p.ang) * p.r * .55;
        } else {
          if (c.gravity) p.vy += c.gravity * dt;
          if (c.brown) { p.vx += rnd(-c.brown, c.brown) * dt * 4; p.vy += rnd(-c.brown, c.brown) * dt * 4; p.vx *= .98; p.vy *= .98; }
          p.x += p.vx * dt + (c.wobble ? Math.sin(p.t * c.wobble[1] * 6.28 + p.ph) * c.wobble[0] * dt : 0);
          p.y += p.vy * dt;
          p.rot += p.spin * dt;
          const out = p.x < -60 || p.x > W + 60 || p.y < -60 || p.y > H + 60;
          if (c.brown && out) { p.x = (p.x + W) % W; p.y = (p.y + H) % H; }
          else if (out || (p.life && p.t > p.life)) { Object.assign(p, spawn(c)); continue; }
        }
        let a = 1;
        if (p.life) { const k = p.t / p.life; a = k < .2 ? k / .2 : k > .75 ? (1 - k) / .25 : 1; }
        if (c.twinkle) a *= .55 + .45 * Math.sin(p.t * c.twinkle * 6.28 + p.ph);
        if (c.shape === "eye") a *= (Math.sin(p.t * 1.7 + p.ph) > -.85 ? 1 : 0);   // моргают
        drawP(p, c, a);
      }
      if (arcs) {   // ⚡ редкий разряд между краями (короткий и небольшой — не вспышка на весь экран)
        arcNext -= dt;
        if (arcNext <= 0 && !arc) { arc = { t: 0, pts: jag(rnd(0, W), 0, rnd(0, W), H) }; arcNext = rnd(1.5, 4); }
        if (arc) {
          arc.t += dt;
          ctx.globalAlpha = arc.t < .12 ? 1 : Math.max(0, 1 - (arc.t - .12) * 4);
          ctx.strokeStyle = "#bdf6ff"; ctx.shadowColor = "#4fd8ff"; ctx.shadowBlur = 14; ctx.lineWidth = 1.6;
          ctx.beginPath(); arc.pts.forEach((q, i) => i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1])); ctx.stroke();
          if (arc.t > .4) arc = null;
        }
      }
      if (film) {   // 📼 царапины и пылинки старой плёнки
        ctx.shadowBlur = 0; ctx.globalAlpha = .35; ctx.fillStyle = "#000";
        for (let i = 0; i < 4; i++) ctx.fillRect(Math.random() * W, Math.random() * H, rnd(1, 3), rnd(1, 3));
        if (Math.random() < .25) { ctx.fillStyle = "rgba(255,255,255,.5)"; ctx.fillRect(Math.random() * W, 0, 1, H); }
      }
      clock += dt;
      if (car) drawCar(clock % CAR_CYCLE);
      if (oil) drawOil(clock);
      if (steps) drawSteps(clock);
      if (state.torch) {   // 🔦 фонарик дрожит в руке
        torchT += dt;
        back.style.setProperty("--fx-x", (50 + Math.sin(torchT * .7) * 22 + Math.sin(torchT * 3.1) * 2) + "%");
        back.style.setProperty("--fx-y", (45 + Math.cos(torchT * .5) * 18 + Math.cos(torchT * 2.7) * 2) + "%");
      }
      state.raf = requestAnimationFrame(frame);
    }
    // 🚗 две фары появляются вдали, растут и проносятся мимо зрителя; на пике свет плавно (не вспышкой!) заливает
    // сцену, потом — ночь и дым от проехавшей машины. Цикл CAR_CYCLE секунд.
    const CAR_CYCLE = 13;
    function drawCar(t) {
      const ease = k => k * k * (3 - 2 * k);
      ctx.shadowBlur = 0;
      if (t > 1 && t < 6.2) {
        const k = Math.min(1, (t - 1) / 4.6), e = k * k * k;          // приближение ускоряется
        const cx = W * (.18 + .74 * e), cy = H * (.32 + .34 * e);      // из дальнего угла — к ближнему
        const gap = 6 + e * W * .55, r = 2 + e * Math.max(W, H) * .32;
        for (const sx of [-1, 1]) {
          const x = cx + sx * gap / 2, g = ctx.createRadialGradient(x, cy, 0, x, cy, r);
          g.addColorStop(0, "rgba(255,255,240,1)"); g.addColorStop(.15, "rgba(255,245,210,.85)");
          g.addColorStop(.5, "rgba(255,230,170,.25)"); g.addColorStop(1, "rgba(255,220,150,0)");
          ctx.globalAlpha = Math.min(1, .25 + k); ctx.fillStyle = g;
          ctx.beginPath(); ctx.arc(x, cy, r, 0, 6.28); ctx.fill();
        }
        if (k > .75) { const glare = ease((k - .75) / .25) * .8;     // почти ослепляет — нарастает за ~1,2 с
          ctx.globalAlpha = glare; ctx.fillStyle = "#fff8e6"; ctx.fillRect(0, 0, W, H); }
      }
      if (t >= 6.2 && t < 8) {                                         // фары ушли — свет гаснет плавно
        ctx.globalAlpha = .8 * (1 - ease((t - 6.2) / 1.8)); ctx.fillStyle = "#fff8e6"; ctx.fillRect(0, 0, W, H);
      }
      if (t > 6.1 && t < 6.25 && smoke.length < 14) for (let i = 0; i < 14; i++)
        smoke.push({ x: W * rnd(.55, 1.05), y: H * rnd(.55, .95), r: rnd(30, 70), vx: rnd(-14, -4), vy: rnd(-10, -3), a: rnd(.18, .32) });
      for (let i = smoke.length - 1; i >= 0; i--) {                    // дым от проехавшей машины
        const m = smoke[i];
        m.x += m.vx * .016; m.y += m.vy * .016; m.r += .25; m.a -= .0009;
        if (m.a <= 0 || t < 1) { smoke.splice(i, 1); continue; }
        const g = ctx.createRadialGradient(m.x, m.y, 0, m.x, m.y, m.r);
        g.addColorStop(0, "rgba(170,170,180," + m.a + ")"); g.addColorStop(1, "rgba(170,170,180,0)");
        ctx.globalAlpha = 1; ctx.fillStyle = g; ctx.beginPath(); ctx.arc(m.x, m.y, m.r, 0, 6.28); ctx.fill();
      }
    }
    // 🛢 лужа масла медленно растекается и «дышит» краями; под лучом фонаря — ярче, с бликом
    function drawOil(t) {
      const R = Math.min(W, H) * (.12 + .2 * (1 - Math.exp(-t / 9))), cx = W * .5, cy = H * .62;
      ctx.shadowBlur = 0; ctx.globalAlpha = 1;
      ctx.beginPath();
      for (let i = 0; i <= 48; i++) {
        const a = i / 48 * 6.28;
        const rr = R * (1 + .16 * Math.sin(3 * a + t * .35) + .09 * Math.sin(5 * a - t * .5) + .05 * Math.sin(8 * a + t * .8));
        const x = cx + Math.cos(a) * rr * 1.35, y = cy + Math.sin(a) * rr * .7;
        i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
      }
      ctx.closePath();
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 1.4);
      g.addColorStop(0, "rgba(40,22,8,.92)"); g.addColorStop(.7, "rgba(70,40,14,.85)"); g.addColorStop(1, "rgba(90,55,20,.6)");
      ctx.fillStyle = g; ctx.fill();
      ctx.save(); ctx.clip();                                          // свет фонаря на поверхности масла
      const tx = W * (parseFloat(back.style.getPropertyValue("--fx-x")) || 50) / 100,
        ty = H * (parseFloat(back.style.getPropertyValue("--fx-y")) || 45) / 100;
      const lg = ctx.createRadialGradient(tx, ty, 0, tx, ty, 120);
      lg.addColorStop(0, "rgba(255,210,140,.55)"); lg.addColorStop(.35, "rgba(170,120,255,.18)");
      lg.addColorStop(.6, "rgba(80,200,255,.10)"); lg.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = lg; ctx.fillRect(0, 0, W, H);                    // радужная плёнка — как у настоящего масла
      ctx.restore();
    }
    // 👣 цепочка следов: проступают по одному и медленно тают
    const STEP_EVERY = .7, STEP_LIFE = 5;
    function drawSteps(t) {
      const n = Math.floor(t / STEP_EVERY), total = 14;
      ctx.shadowBlur = 0; ctx.fillStyle = "rgba(200,190,170,1)";
      for (let i = Math.max(0, n - 8); i <= n; i++) {
        const age = t - i * STEP_EVERY;
        if (age < 0 || age > STEP_LIFE) continue;
        const j = i % total, k = j / total, side = j % 2 ? 1 : -1;
        const x = W * (.1 + .8 * k), y = H * (.85 - .55 * k) + side * 9, ang = Math.atan2(-.55 * H, .8 * W) + Math.PI / 2;
        ctx.globalAlpha = .45 * Math.min(1, age / .4) * (1 - age / STEP_LIFE);
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
        ctx.beginPath(); ctx.ellipse(0, -6, 5, 8, 0, 0, 6.28); ctx.fill();
        ctx.beginPath(); ctx.ellipse(0, 7, 4, 4.5, 0, 0, 6.28); ctx.fill();
        ctx.restore();
      }
    }
    // 🖐 следы ладоней проступают на запотевшем стекле одна за другой, чуть сползают вниз и тают
    const prints = [];
    let printNext = .6;
    function drawHands(t, dt) {
      printNext -= dt;
      if (printNext <= 0 && prints.length < 7) {
        const pair = Math.random() < .35, x = rnd(.15, .85) * W, y = rnd(.2, .75) * H, s = rnd(.9, 1.35);
        prints.push({ x: x, y: y, s: s, rot: rnd(-.35, .35), left: Math.random() < .5, t: 0, life: rnd(6, 9), drip: rnd(25, 60) });
        if (pair) prints.push({ x: x + 70 * s, y: y + rnd(-15, 15), s: s, rot: rnd(-.35, .35), left: true, t: -.5, life: rnd(6, 9), drip: rnd(25, 60) });
        printNext = rnd(1.4, 2.6);
      }
      ctx.shadowBlur = 0;
      for (let i = prints.length - 1; i >= 0; i--) {
        const h = prints[i];
        h.t += dt;
        if (h.t <= 0) continue;
        if (h.t > h.life) { prints.splice(i, 1); continue; }
        const k = h.t / h.life, a = (k < .1 ? k / .1 : k > .7 ? (1 - k) / .3 : 1) * .33, slide = Math.min(10, h.t * 1.6);
        ctx.save(); ctx.translate(h.x, h.y + slide); ctx.rotate(h.rot); ctx.scale(h.left ? -h.s : h.s, h.s);
        ctx.fillStyle = "rgba(225,240,245," + a + ")";
        ctx.shadowColor = "rgba(225,240,245," + a + ")"; ctx.shadowBlur = 8;
        ctx.beginPath(); ctx.ellipse(0, 0, 15, 18, 0, 0, 6.28); ctx.fill();                        // ладонь
        [[-11, -30, 4.2, 12, -.18], [-3.5, -36, 4.4, 14, -.05], [4.5, -35, 4.3, 13.5, .06], [11.5, -28, 3.8, 10.5, .2]]
          .forEach(f => { ctx.beginPath(); ctx.ellipse(f[0], f[1], f[2], f[3], f[4], 0, 6.28); ctx.fill(); });   // пальцы
        ctx.beginPath(); ctx.ellipse(-19, -2, 4.4, 10, -.9, 0, 6.28); ctx.fill();                  // большой палец
        ctx.shadowBlur = 0; ctx.strokeStyle = "rgba(225,240,245," + (a * .8) + ")"; ctx.lineWidth = 1.6;   // капли стекают
        const dl = Math.min(h.drip, h.t * 9);
        ctx.beginPath(); ctx.moveTo(-6, 16); ctx.lineTo(-6, 16 + dl); ctx.moveTo(7, 15); ctx.lineTo(7, 15 + dl * .6); ctx.stroke();
        ctx.restore();
      }
    }
    // 🪞 зеркало запотевает, на нём проступает надпись «пальцем» (текст — из сцены квеста), от букв бегут капли,
    // потом пар снова затягивает стекло. Цикл MIRROR_CYCLE секунд. Без резких вспышек и скримеров.
    const MIRROR_CYCLE = 16;
    let fogTex = null, mc = null, mctx = null, mirrorDrips = null;
    function fogTexture() {
      const c = document.createElement("canvas"); c.width = Math.max(1, W); c.height = Math.max(1, H);
      const g = c.getContext("2d");
      g.fillStyle = "rgb(150,162,172)"; g.fillRect(0, 0, W, H);
      for (let i = 0; i < W * H / 90; i++) {   // мелкие капельки конденсата
        g.fillStyle = "rgba(255,255,255," + rnd(.05, .25) + ")";
        g.beginPath(); g.arc(Math.random() * W, Math.random() * H, rnd(.5, 2.2), 0, 6.28); g.fill();
      }
      const v = g.createRadialGradient(W / 2, H / 2, Math.min(W, H) * .2, W / 2, H / 2, Math.max(W, H) * .75);
      v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(30,35,45,.45)");
      g.fillStyle = v; g.fillRect(0, 0, W, H);
      return c;
    }
    function mirrorLines(fs) {
      const words = mirrorText.split(/\s+/).filter(Boolean);
      mctx.font = "bold " + fs + 'px "Segoe Print","Comic Sans MS","Marker Felt",cursive';
      if (mctx.measureText(mirrorText).width < W * .74 || words.length < 2) return [mirrorText];
      let best = [mirrorText], bestW = Infinity;
      for (let i = 1; i < words.length; i++) {
        const a = words.slice(0, i).join(" "), b = words.slice(i).join(" ");
        const w = Math.max(mctx.measureText(a).width, mctx.measureText(b).width);
        if (w < bestW) { bestW = w; best = [a, b]; }
      }
      return best;
    }
    function drawMirror(t) {
      if (!mc || mc.width !== Math.max(1, W)) {
        mc = document.createElement("canvas"); mc.width = Math.max(1, W); mc.height = Math.max(1, H);
        mctx = mc.getContext("2d"); fogTex = fogTexture(); mirrorDrips = null;
      }
      const c = t % MIRROR_CYCLE, ease = k => k * k * (3 - 2 * k);
      const fogA = .62 * ease(Math.min(1, c / 2.5));
      const mx = W * .07, my = H * .44, mw = W * .86, mh = H * .5, rr = 18;
      const frame = g => { g.beginPath(); g.moveTo(mx + rr, my); g.arcTo(mx + mw, my, mx + mw, my + mh, rr);
        g.arcTo(mx + mw, my + mh, mx, my + mh, rr); g.arcTo(mx, my + mh, mx, my, rr); g.arcTo(mx, my, mx + mw, my, rr); g.closePath(); };
      mctx.globalCompositeOperation = "source-over"; mctx.globalAlpha = 1;
      mctx.clearRect(0, 0, W, H);
      mctx.save(); frame(mctx); mctx.clip();
      mctx.globalAlpha = fogA; mctx.drawImage(fogTex, 0, 0);
      if (!mirrorText) { drawMirrorShape(c, mx, my, mw, mh, fogA); mctx.restore(); finishMirror(c, frame); return; }
      let fs = Math.min(46, Math.max(22, mw / 8));
      let lines = mirrorLines(fs);
      while (fs > 18 && Math.max.apply(null, lines.map(l => mctx.measureText(l).width)) > mw * .88) { fs -= 2; mctx.font = "bold " + fs + 'px "Segoe Print","Comic Sans MS","Marker Felt",cursive'; }
      const lh = fs * 1.25, top = my + mh * .4 - (lines.length - 1) * lh / 2;
      const widths = lines.map(l => mctx.measureText(l).width), total = widths.reduce((x, y) => x + y, 0);
      const write = Math.max(0, Math.min(1, (c - 2.8) / 3.6));           // «пишут пальцем» 3,6 с
      const refog = c > 12.5 ? ease(Math.min(1, (c - 12.5) / 3)) : 0;   // пар снова затягивает надпись
      if (!mirrorDrips) mirrorDrips = Array.from({ length: 7 }, () => ({ u: Math.random(), len: rnd(25, 80), line: Math.floor(Math.random() * lines.length) }));
      mctx.globalCompositeOperation = "destination-out";
      mctx.globalAlpha = (1 - refog) * .92;
      mctx.lineWidth = Math.max(3, fs * .14); mctx.lineJoin = mctx.lineCap = "round";
      mctx.textBaseline = "middle"; mctx.textAlign = "left"; mctx.strokeStyle = mctx.fillStyle = "#000";
      let done = 0;
      lines.forEach((l, i) => {
        const x0 = (W - widths[i]) / 2, y = top + i * lh, shown = Math.max(0, Math.min(widths[i], write * total - done));
        done += widths[i];
        if (shown <= 0) return;
        mctx.save(); mctx.beginPath(); mctx.rect(x0 - 6, y - lh, shown + 6, lh * 2); mctx.clip();
        mctx.strokeText(l, x0, y); mctx.fillText(l, x0, y); mctx.restore();
        mirrorDrips.filter(d => d.line === i && d.u * widths[i] < shown).forEach(d => {     // капли от букв
          const grow = Math.min(1, Math.max(0, (c - 3 - d.u * 3.6) / 4));
          mctx.lineWidth = 2.2; mctx.beginPath(); mctx.moveTo(x0 + d.u * widths[i], y + fs * .35);
          mctx.lineTo(x0 + d.u * widths[i], y + fs * .35 + d.len * grow); mctx.stroke();
        });
      });
      mctx.restore();
      finishMirror(c, frame);
    }
    function finishMirror(c, frame) {
      mctx.globalCompositeOperation = "source-over";
      mctx.globalAlpha = .55; mctx.lineWidth = 3; mctx.strokeStyle = "#8a7550"; frame(mctx); mctx.stroke();   // рама
      if (c < .05) mirrorDrips = null;
      ctx.shadowBlur = 0; ctx.globalAlpha = 1; ctx.drawImage(mc, 0, 0, W, H);
    }
    // контуры для «рисунка пальцем»: координаты 0..1 внутри квадрата/прямоугольника рисунка
    const ellipsePts = (cx, cy, rx, ry, n, wob) => Array.from({ length: n + 1 }, (_, i) => {
      const a = i / n * 6.28 - 1.57, w = 1 + (wob || 0) * Math.sin(i * 2.7);
      return [cx + Math.cos(a) * rx * w, cy + Math.sin(a) * ry * w];
    });
    const SHAPES = {
      // высокая тонкая фигура без лица: голова, длинная шея, узкие плечи, руки ниже колен с длинными пальцами
      figure: { box: [.42, 1], strokes: [
        { pts: ellipsePts(.5, .1, .1, .085, 22) },
        { pts: [[.5, .19], [.5, .26]] },
        { pts: [[.3, .29], [.5, .26], [.7, .29]] },
        { pts: [[.5, .26], [.5, .58]] },
        { pts: [[.3, .29], [.24, .5], [.2, .72], [.18, .8]] },
        { pts: [[.18, .8], [.12, .9]] }, { pts: [[.18, .8], [.17, .92]] }, { pts: [[.18, .8], [.22, .9]] },
        { pts: [[.7, .29], [.76, .5], [.8, .72], [.82, .8]] },
        { pts: [[.82, .8], [.78, .9]] }, { pts: [[.82, .8], [.83, .92]] }, { pts: [[.82, .8], [.88, .9]] },
        { pts: [[.5, .58], [.42, .78], [.4, .99]] },
        { pts: [[.5, .58], [.58, .78], [.6, .99]] },
      ], drips: [[.5, .19], [.18, .92], [.83, .92], [.4, .99]] },
      // лицо духа: неровный овал, пустые глазницы, длинный зубастый рот
      face: { box: [1, 1], strokes: [
        { pts: ellipsePts(.5, .5, .3, .42, 34, .05) },
        { pts: ellipsePts(.38, .4, .075, .055, 14), fill: 1 },
        { pts: ellipsePts(.62, .4, .075, .055, 14), fill: 1 },
        { pts: [[.47, .52], [.5, .58], [.53, .52]] },
        { pts: [[.3, .68], [.34, .74], [.38, .67], [.42, .75], [.46, .67], [.5, .76], [.54, .67], [.58, .75], [.62, .67], [.66, .74], [.7, .68]] },
      ], drips: [[.38, .46], [.62, .46], [.42, .75], [.58, .75]] },
    };
    function drawMirrorShape(c, mx, my, mw, mh, fogA) {
      const sh = SHAPES[mirrorDraw] || SHAPES.figure;
      const bh = mh * .92, bw = Math.min(mw * .9, bh * sh.box[0] / sh.box[1]);
      const bx = mx + (mw - bw) / 2, by = my + (mh - bh) / 2;
      const P = q => [bx + q[0] * bw, by + q[1] * bh];
      const lens = sh.strokes.map(st => st.pts.reduce((L, q, i) => i ? L + Math.hypot((q[0] - st.pts[i - 1][0]) * bw, (q[1] - st.pts[i - 1][1]) * bh) : 0, 0));
      const total = lens.reduce((a, b) => a + b, 0);
      const draw = Math.max(0, Math.min(1, (c - 2.8) / 5.5)) * total;         // палец рисует ~5,5 с
      const refog = c > 12.5 ? (k => k * k * (3 - 2 * k))(Math.min(1, (c - 12.5) / 3)) : 0;
      mctx.globalCompositeOperation = "destination-out";
      mctx.globalAlpha = (1 - refog) * .92;
      mctx.lineWidth = Math.max(4, bw * .035); mctx.lineJoin = mctx.lineCap = "round"; mctx.strokeStyle = mctx.fillStyle = "#000";
      let left = draw;
      sh.strokes.forEach((st, si) => {
        if (left <= 0) return;
        const pts = st.pts.map(P);
        mctx.beginPath(); mctx.moveTo(pts[0][0], pts[0][1]);
        let rest = left;
        for (let i = 1; i < pts.length && rest > 0; i++) {
          const seg = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]), k = Math.min(1, rest / seg);
          mctx.lineTo(pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * k, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * k);
          rest -= seg;
        }
        mctx.stroke();
        if (st.fill && left >= lens[si]) { mctx.beginPath(); pts.forEach((q, i) => i ? mctx.lineTo(q[0], q[1]) : mctx.moveTo(q[0], q[1])); mctx.fill(); }
        left -= lens[si];
      });
      if (draw >= total) {                                                   // дорисовал — по стеклу бегут капли
        const grow = Math.min(1, (c - 8.3) / 4);
        mctx.lineWidth = 2.2;
        sh.drips.forEach((q, i) => { const p = P(q); mctx.beginPath(); mctx.moveTo(p[0], p[1]); mctx.lineTo(p[0], p[1] + (18 + i * 9) * grow); mctx.stroke(); });
      }
      mctx.globalCompositeOperation = "source-over";
    }
    // 🕯 свечи: живые язычки (сумма медленных синусов, без мигания), дыхание тёплого ореола, тонкий дымок
    let candleSet = null;
    function drawCandles(t) {
      if (!candleSet) candleSet = Array.from({ length: 6 }, (_, i) => {
        const y = rnd(.55, .92); return { x: (i + .5) / 6 + rnd(-.05, .05), y: y, s: .55 + y * .7, ph: rnd(0, 6.28), ph2: rnd(0, 6.28), h: rnd(.7, 1.2) };
      });
      ctx.shadowBlur = 0;
      candleSet.forEach(cd => {
        const x = cd.x * W, base = cd.y * H, s = cd.s, bodyH = 34 * s * cd.h, top = base - bodyH;
        const breathe = .16 + .07 * Math.sin(t * .7 + cd.ph);
        const halo = ctx.createRadialGradient(x, top - 8 * s, 0, x, top - 8 * s, 90 * s);
        halo.addColorStop(0, "rgba(255,190,110," + breathe + ")"); halo.addColorStop(1, "rgba(255,150,60,0)");
        ctx.globalAlpha = 1; ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(x, top - 8 * s, 90 * s, 0, 6.28); ctx.fill();
        const body = ctx.createLinearGradient(x - 6 * s, 0, x + 6 * s, 0);
        body.addColorStop(0, "rgba(120,100,80,.9)"); body.addColorStop(.5, "rgba(235,222,195,.95)"); body.addColorStop(1, "rgba(120,100,80,.9)");
        ctx.fillStyle = body; ctx.fillRect(x - 6 * s, top, 12 * s, bodyH);
        const fl = 1 + .12 * Math.sin(t * 2.3 + cd.ph) + .06 * Math.sin(t * 5.1 + cd.ph2);
        const sway = 1.6 * s * Math.sin(t * 1.3 + cd.ph2), fh = 16 * s * fl, fx = x + sway, fy = top - 2 * s;
        const flame = ctx.createRadialGradient(fx, fy - fh * .35, 0, fx, fy - fh * .35, fh * .75);
        flame.addColorStop(0, "rgba(255,255,235,1)"); flame.addColorStop(.35, "rgba(255,210,120,.95)");
        flame.addColorStop(.75, "rgba(255,130,40,.55)"); flame.addColorStop(1, "rgba(255,90,20,0)");
        ctx.fillStyle = flame; ctx.beginPath();
        ctx.moveTo(fx, fy - fh); ctx.quadraticCurveTo(fx + 5.5 * s, fy - fh * .35, fx, fy); ctx.quadraticCurveTo(fx - 5.5 * s, fy - fh * .35, fx, fy - fh); ctx.fill();
        ctx.strokeStyle = "rgba(200,200,210,.10)"; ctx.lineWidth = 1;                  // дымок вьётся вверх
        ctx.beginPath(); ctx.moveTo(fx, fy - fh);
        for (let k = 1; k <= 8; k++) ctx.lineTo(fx + Math.sin(t * 1.1 + k * .8 + cd.ph) * k * 1.6 * s, fy - fh - k * 9 * s);
        ctx.stroke();
      });
    }
    // 🔢 кодовый замок: невидимая рука набирает код, клавиши мягко подсвечиваются разными цветами,
    // на табло растут звёздочки; потом спокойное «ОТКРЫТО» или «ОШИБКА» — и снова. Без вспышек.
    const KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "✱", "0", "#"];
    const KEY_COLORS = ["120,220,255", "255,190,90", "200,140,255", "120,255,170", "255,130,170"];
    let kp = null;
    function drawKeypad(t, dt) {
      if (!kp) kp = { phase: "wait", tm: 1, code: [], typed: 0, lit: [], ok: false };
      kp.tm -= dt;
      if (kp.tm <= 0) {
        if (kp.phase === "wait") { kp.phase = "type"; kp.code = Array.from({ length: 4 + Math.floor(Math.random() * 3) }, () => Math.floor(Math.random() * 12)); kp.typed = 0; kp.tm = .2; }
        else if (kp.phase === "type") {
          if (kp.typed < kp.code.length) { kp.lit.push({ k: kp.code[kp.typed], t: .45, c: pick(KEY_COLORS) }); kp.typed++; kp.tm = rnd(.45, .8); }
          else if (lockResult) { kp.phase = "result"; kp.ok = lockResult === "open"; kp.tm = 4.5; }
          else { kp.phase = "clear"; kp.tm = .9; }
        } else { kp.phase = "wait"; kp.typed = 0; kp.tm = 1.2; }
      }
      if (Math.random() < dt * .8) kp.lit.push({ k: Math.floor(Math.random() * 12), t: .3, c: pick(KEY_COLORS), dim: 1 });   // случайные огоньки
      const cell = Math.min(44, W * .12, H * .55 / 5.3), kw = cell * 3, kh = cell * 4, x0 = W - kw - 22, y0 = (H - kh) / 2 + cell * .5;   // справа, фоном под текстом
      ctx.shadowBlur = 0; ctx.lineWidth = 1;
      ctx.globalAlpha = .55; ctx.fillStyle = "rgba(10,14,24,.75)"; ctx.fillRect(x0 - 10, y0 - cell * .95, kw + 20, kh + cell + 6);
      ctx.strokeStyle = "rgba(140,170,200,.35)"; ctx.strokeRect(x0 - 10, y0 - cell * .95, kw + 20, kh + cell + 6);
      // табло
      ctx.globalAlpha = 1; ctx.fillStyle = "rgba(0,0,0,.6)"; ctx.fillRect(x0, y0 - cell * .8, kw, cell * .55);
      ctx.font = "bold " + Math.round(cell * .32) + "px monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      const msg = kp.phase === "result" ? (kp.ok ? words.open : words.error) : "✱".repeat(kp.phase === "clear" ? 0 : kp.typed).padEnd(6, "·");
      const mc = kp.phase === "result" ? (kp.ok ? "rgba(120,255,160," : "rgba(255,110,110,") : "rgba(140,220,255,";
      ctx.fillStyle = mc + (kp.phase === "result" ? (.55 + .25 * Math.sin(t * 3)) : .8) + ")";
      ctx.fillText(msg, x0 + kw / 2, y0 - cell * .52);
      kp.lit.forEach(l => { l.t -= dt; });
      kp.lit = kp.lit.filter(l => l.t > 0);
      KEYS.forEach((k, i) => {
        const cx = x0 + (i % 3 + .5) * cell, cy = y0 + (Math.floor(i / 3) + .5) * cell, r = cell * .36;
        const lit = kp.lit.filter(l => l.k === i).pop();
        const a = lit ? Math.min(1, lit.t / .2) * (lit.dim ? .25 : .55) : 0;
        if (a > 0) {
          const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 1.5);
          g.addColorStop(0, "rgba(" + lit.c + "," + a + ")"); g.addColorStop(1, "rgba(" + lit.c + ",0)");
          ctx.globalAlpha = 1; ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, r * 1.5, 0, 6.28); ctx.fill();
        }
        ctx.globalAlpha = .7; ctx.strokeStyle = a > 0 ? "rgba(" + lit.c + ",.8)" : "rgba(150,180,210,.35)";
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, 6.28); ctx.stroke();
        ctx.fillStyle = a > 0 ? "rgba(255,255,255,.9)" : "rgba(170,190,215,.55)"; ctx.font = Math.round(r * .9) + "px sans-serif";
        ctx.fillText(k, cx, cy + 1);
      });
    }
    function jag(x1, y1, x2, y2) {
      const pts = [[x1, y1]], n = 12;
      for (let i = 1; i < n; i++) pts.push([x1 + (x2 - x1) * i / n + rnd(-18, 18), y1 + (y2 - y1) * i / n]);
      pts.push([x2, y2]);
      return pts;
    }
    state.raf = requestAnimationFrame(frame);
  }

  window.QuestFX = {
    list: Object.keys(FX).map(id => ({ id: id, g: FX[id].g, ru: FX[id].ru, en: FX[id].en })),
    has: id => !!FX[id], start: start, stop: stop, enabled: enabled, setEnabled: setEnabled,
  };
})();
