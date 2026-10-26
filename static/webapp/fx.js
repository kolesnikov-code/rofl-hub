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
    neonrain: { n: 45, from: "top", vx: [-20, 0], vy: [500, 750], size: [10, 20], colors: ["rgba(255,60,200,.6)", "rgba(40,230,255,.6)"], shape: "streak", w: 1.3, glow: 6 },
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
    neon:       { g: "city", ru: "🌃 Неоновый дождь", en: "🌃 Neon rain", back: ["fx-clubbg"], parts: ["neonrain"] },
    siren:      { g: "city", ru: "🚓 Сирена", en: "🚓 Siren", back: ["fx-noir"], front: ["fx-sirenL", "fx-sirenR"] },
    alarm:      { g: "city", ru: "🚨 Тревога", en: "🚨 Alarm", back: ["fx-alarmbg"], front: ["fx-beacon"] },
    noir:       { g: "city", ru: "🕵️ Жалюзи", en: "🕵️ Blinds", back: ["fx-noir", "fx-blinds", "fx-headl"], parts: ["dust"] },
    headlights: { g: "city", ru: "🚗 Фары за окном", en: "🚗 Passing headlights", back: ["fx-noir", "fx-headl"] },
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

  function start(stage, moods) {
    stop();
    if (!stage) return;
    const back = stage.querySelector(".fx-back");
    if (!back) return;
    back.innerHTML = "";
    const list = (Array.isArray(moods) ? moods : (moods ? [moods] : [])).filter(m => FX[m]).slice(0, 2);
    if (!list.length || !enabled()) return;
    injectCss();
    const still = reduceMotion();
    state = { raf: 0, timers: [], timeouts: [], front: [], parts: [], special: [], torch: false };
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
      film = state.special.indexOf("film") >= 0;
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
          cols[i] += 14 * dt * 9;
          if (cols[i] > H + rnd(0, 200)) cols[i] = rnd(-40, 0);
        }
      } else ctx.clearRect(0, 0, W, H);
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
      if (state.torch) {   // 🔦 фонарик дрожит в руке
        torchT += dt;
        back.style.setProperty("--fx-x", (50 + Math.sin(torchT * .7) * 22 + Math.sin(torchT * 3.1) * 2) + "%");
        back.style.setProperty("--fx-y", (45 + Math.cos(torchT * .5) * 18 + Math.cos(torchT * 2.7) * 2) + "%");
      }
      state.raf = requestAnimationFrame(frame);
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
