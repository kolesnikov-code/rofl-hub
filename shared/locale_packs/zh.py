"""Китайский упрощённый (简体中文) — локализация ROFL HUB."""
# Глоссарий (консистентность терминов):
# монеты -> 金币
# Младший Майнер -> 初级矿工
# Кибер-Бурильщик -> 赛博钻机
# кибер-котлета -> 赛博肉排 (кратко: 肉排)
# Холодильник -> 冰箱
# склад -> 仓库
# ферма -> 农场 (кибер-ферма: 赛博农场)
# Ядерный Разгон x5 -> 核能加速 x5
# Азотное Охлаждение +40% -> 液氮冷却 +40%
# Мастер-дрон -> 大师无人机
# Кибер-Сейф -> 赛博保险箱
# Мега-Клан -> 超级公会
# Безлимит -> 解除上限
# дуэли -> 对决 (1-на-1: 1对1 对决)
# битвы -> 大作战
# квесты -> 冒险任务
# викторина -> 竞答
# уровень интеллекта -> 智力等级
# команда -> 战队 · клан -> 公会 · ставка -> 押注 · банк -> 奖池
# биржа котлет -> 肉排交易所
# ресурсы (волна 22.10): Металл -> 金属 · Водород -> 氢气 · Кристаллы -> 晶体 · Детали -> 零件
# Мастерская -> 工坊 · Кибер-броня -> 赛博装甲 · Шаттл -> 穿梭机 · Щит -> 护盾
# Налёт -> 突袭 · Стойка обороны -> 防御姿态 · Разведка -> 侦察 · Реванш -> 复仇战
# Сундук -> 宝箱 · Серия -> 连续（天数） · Станция команды -> 战队空间站 · добыча -> 产量

BUTTONS = {
    "main_menu": "📱 主菜单",
    "profile": "👤 我的资料",
    "farm": "🚜 我的农场",
    "games_zone": "🕹️ 游戏区",
    "teams": "🏆 战队与公会",
    "shop": "🏪 商店",
    "shop_cat_farm": "🚜 农场专区",
    "shop_cat_games": "🕹️ 游戏专区",
}

STRINGS = {
    # 27.10: «чат — дверь и почтальон», вся игра в приложении
    "app.moved": "🎮 此板块已移至游戏应用内——那里更方便、更好看。点击下方按钮 👇",
    "app.keyboard_gone": "🧹 底部的旧按钮已移除：整个游戏现在都在应用里。你也可以点输入框旁的「🎮 ROFL HUB」按钮打开它。",
    "start.console_app": "🚀 <b>准备就绪！</b>整个游戏都在应用里：点击下方按钮。之后随时可以点输入框旁的「🎮 ROFL HUB」按钮打开。",
    "start.welcome_back_app": "👋 <b>欢迎回来，@{username}！</b>你的进度都在——打开游戏 👇",
    "menu.app": "📱 <b>ROFL HUB</b>\n整个游戏都在应用里 👇\n\n<b>聊天中:</b>\n• /invite — 邀请好友\n• /transfer — 转账金币\n• /faq — 常见问题\n• /rules — 用户协议\n• /paysupport — 支付帮助\n• /delete_account — 删除账号",
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
    "common.no_profile": "⚠️ 未找到个人资料。点按 /start 注册。",
    "common.btn_menu": "💿 主菜单",
    "common.blocked": "🚫 你的账号已被 ROFL HUB 管理员封禁。",
    "common.feature_off": "⚙️ 该板块正在维护中，请稍后再来！",
    "common.maintenance": "🛠 ROFL HUB 正在快速维护，马上回来——你的金币和进度都安然无恙！",

    # ---------------- /start ----------------
    "start.welcome_back": "👋 <b>欢迎回来，@{username}！</b>\n你的进度都还在。导航面板在屏幕底部。",
    "start.btn_continue": "🛸 继续",
    "start.btn_cutlet": "赛博肉排是什么？🥩🤔",
    "start.btn_fight": "快说完，马上开战！",
    "start.console": "🚀 <b>控制台已激活！请使用屏幕底部的按钮。</b>",
    "start.intro1": (
        "👋 <b>你好！我是 ROFL HUB BOT——ROFL HUB 游戏生态系统的主机器人。"
        "这是新一代的益智娱乐中心！</b>\n\n"
        "<b>在这里你可以：</b>\n"
        "🎮 在聊天机器人游戏中挑战机器人和其他玩家\n"
        "💸 靠胜利赚取游戏货币，或开一座农场全天候挖矿\n"
        "🤼 创建战队，冲进排行榜前列\n"
        "🏆 把战队升级成公会，征战国际排名\n"
        "💰 和你的伙伴们一起赢下百万金币大奖\n"
        "👑 购买我们社交主页或官网上的推广位，宣传自己或自己的博客\n\n"
        "<b>这个聊天机器人还能：</b>\n"
        "🎮 展示 ROFL HUB 所有游戏、频道和网站的列表\n"
        "⚡ 为游戏、战队与公会大作战、成就、活跃度和邀请好友发放金币\n"
        "🔄 把游戏金币转给其他 ROFL HUB 玩家\n"
        "💎 出售网站推广位以及达人和博主的 VIP 席位\n"
        "🚀 出售加速器、称号、身份标识等各种好东西……\n\n"
        "<i>点按「继续」，我再细细道来 👇</i>"
    ),
    "start.intro2": (
        "🎁 <b>收下你的注册首批奖励！</b>\n"
        "..................................................\n"
        "💸 已到账：<b>{balance} 🪙</b>\n"
        "🥩 已到账：<b>{cutlets} 份赛博肉排</b>\n"
        "..................................................\n"
        "这是你加入 ROFL HUB 俱乐部的新手奖励。\n\n"
        "🔒 <i>该奖励仅在注册时发放一次。</i>\n\n"
        "金币的用途多种多样，它是整个中心经济的基石。好好珍惜……\n\n"
        "⁉️ <b>不过你一定想问：</b>这块肉排是什么？要拿去喂谁？"
    ),
    "start.intro3": (
        "<b>首先要明白，游戏金币为什么这么重要？</b>\n\n"
        "金币是 <b>ROFL HUB</b> 里所有交易、比赛和购买的基础。"
        "它几乎是世界上唯一可以免费开采的游戏货币！\n"
        "..................................................\n"
        "<b>赚取方式多种多样：</b>\n"
        "- 用邀请链接拉好友入伙\n"
        "- 在对战机器人的游戏中获胜\n"
        "- 在与其他玩家的对决中获胜\n"
        "- 参加战队与公会大作战\n"
        "- 领取每日登录奖励并完成任务\n"
        "- 养一台 24 小时挖矿的机器人（初级矿工 / 赛博钻机）\n"
        "..................................................\n"
        "<b>如果你养了二级机器人（赛博钻机）——它每天都要吃饭。"
        "赛博肉排就派上用场了：它是自动挖矿的燃料，而且每天免费发放！"
        "你的任务很简单——上线喂机器人。</b>\n\n"
        "要是没按时喂——机器人就会断电，挖矿随之停止。\n\n"
        "初级矿工（一级）不需要燃料。"
        "注意！任何机器人的使用期都是 30 天——之后要重新购买，或者配一台大师无人机。"
        "玩着玩着你就懂了:) 咱们别跑题。\n\n"
        "我再讲一点 <b>ROFL HUB</b> 的事，好让你明白这里的运作方式。\n\n"
        "🛑 <b>这是我们相识环节的最后一条消息。接下来就只有战斗了:)</b>"
    ),
    "start.intro4": (
        "<b>长话短说。ROFL HUB 就是：</b>\n"
        "- 各种口味的聊天机器人游戏\n"
        "- 创建自己的战队（最多 50 人）\n"
        "- 把它升级成公会（最多 1000 人）\n"
        "- 有奖的战队与公会大作战\n"
        "- Instagram 主页 — rofl_hub_global\n"
        "- 无需注册即可交流和推广的网站 rofl-hub.com\n"
        "- 全球成千上万的玩家，说不定就有你的新朋友！\n"
        "..................................................\n"
        "<b>说好了，这是最后一条消息。接下来开战！实用命令：</b>\n\n"
        "/menu — 功能快捷操作\n"
        "/games — 所有游戏列表\n"
        "/faq — 常见问题\n"
        "/rules — 用户协议\n"
    ),

    # ---------------- меню и игровая зона ----------------
    "menu.text": (
        "📱 <b>ROFL HUB 生态系统主菜单</b>\n"
        "..................................................\n"
        "👤 <b>个人资料与护照：</b>\n"
        "• /start — 开始了解并注册账号\n"
        "• /profile — 你的护照、余额和战队实时信息\n"
        "• /my_stats — 你最近 30 天的历史统计\n\n"
        "🚜 <b>赛博农场与自动化：</b>\n"
        "• /farm — 燃料中心：加油与机器人产出速度\n"
        "• /shop — 交易市场：购买矿工、肉排和中心升级\n\n"
        "🕹️ <b>游戏室：</b>\n"
        "• /games — 所有对战机器人游戏的快捷中心\n"
        "• /quiz — 限时竞答：30 秒作答，等级与奖励\n"
        "• /duel — 与真人玩家 1对1 对决：10/100/1000 🪙 桌\n"
        "• /quests — 冒险任务：侦探、喜剧和谜题，通关有奖\n"
        "• /rps, /high_low, /safe — 赚金币的快速小游戏\n\n"
        "👥 <b>战队管理：</b>\n"
        "• /create_team — 花 10 万 🪙 注册自己的战队\n"
        "• /my_team — 战队仪表盘和带 🧠 等级的队友名单\n"
        "• /all_teams — 随机战队轮盘\n\n"
        "💸 <b>金钱与朋友：</b>\n"
        "• /invite — 你的邀请链接：每位活跃好友 +500 🪙\n"
        "• /transfer — 给其他玩家转账金币\n\n"
        "📚 <b>帮助与规则：</b>\n"
        "• /faq — 完整生态系统指南（在 Mini App 中打开）\n"
        "• /rules — 用户协议\n"
        "..................................................\n"
        "<i>⚙️ 使用屏幕底部常驻的双列游戏面板，在各版块间瞬间切换！</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>欢迎来到 ROFL HUB 游戏区！</b>\n"
        "..................................................\n"
        "在这里你可以和机器人快速过招，或挑战智力冲刺测验，"
        "赢个盆满钵满——或者输个精光！\n\n"
        "💸 获胜奖励：<b>+2 🪙</b>（赛博保险箱：<b>+5</b>）\n"
        "💀 失败或平局扣除：<b>-1 🪙</b>\n"
        "🧠 竞答有 30 秒倒计时和智力等级：1 级需要答对 10 题，奖励 <b>+100 🪙</b>，"
        "之后每级多 10 题，但奖励也每级多 100！\n"
        "..................................................\n"
        "👇 <b>点按下方按钮，立刻开始一局：</b>"
    ),
    "menu.btn_quiz": "🧠 竞答",
    "menu.btn_rps": "🪨 石头剪刀布",
    "menu.btn_hl": "📈 比大小",
    "menu.btn_safe": "🔐 赛博保险箱",
    "menu.btn_duel": "⚔️ 1对1 对决",
    "app.open": (
        "🎮 <b>ROFL HUB MINI APP</b>\n\n"
        "护照、农场、战队和富豪榜——都在一块霓虹屏幕上。"
        "每日肉排也能直接在那里领取！\n\n"
        "👇 点按按钮："
    ),
    "app.btn": "🎮 打开 MINI APP",
    "app.unavailable": "⚙️ Mini App 仍在连接生态系统服务器。稍后再来看看吧！",
    "faq.teaser": (
        "📚 <b>ROFL HUB 生态系统指南</b>\n"
        "..................................................\n"
        "重点速览：\n"
        "🚜 机器人全天候挖金币：初级矿工——每小时 5 枚、免燃料；"
        "赛博钻机——每小时 10 枚，而且每台钻机每天要吃掉自己的 1 份赛博肉排。"
        "所有机器人寿命 30 天（大师无人机可暂停损耗）。\n"
        "🧠 竞答：30 秒作答，智力等级越高奖励越高。\n"
        "⚔️ 在 10/100/1000 🪙 的桌上与真人玩家对决。\n"
        "🏆 战队最多 50 名成员（超级公会——最多 1000），还有人人有奖的大作战活动。\n"
        "..................................................\n"
        "👇 <b>包含全部机制的完整指南——点按按钮：</b>"
    ),
    "faq.btn_open": "📖 打开完整指南",
    "rules.teaser": (
        "📜 <b>ROFL HUB 用户协议</b>\n"
        "..................................................\n"
        "要点一览：\n"
        "🪙 金币和所有游戏物品都是虚拟娱乐元素："
        "它们不是货币，也不能兑换成真实资金。\n"
        "💫 购买仅通过官方 Telegram Stars 进行；数字商品即时送达，"
        "若发货失败，Stars 将自动退回。\n"
        "🛡️ 我们不收集手机号、地理位置和个人数据。\n"
        "🤝 禁止辱骂、刷分和多开账号——违规可能导致封禁。\n"
        "..................................................\n"
        "👇 <b>完整协议文本与免责声明——点按按钮：</b>\n"
        "<i>⚖️ 使用本机器人即表示你同意这些条款。</i>"
    ),
    "rules.btn_open": "📜 打开完整协议",
    "quest.list_header": (
        "🗺️ <b>ROFL HUB 冒险任务</b>\n"
        "..................................................\n"
        "带有选择和分支的互动故事：侦探、喜剧、谜题。"
        "每个任务的首次通关都能赢得金币，而且想重玩多少次都行！\n"
        "🌐 <i>任务故事暂时为俄语——翻译版即将推出。</i>\n\n"
        "👇 <b>选择一个故事：</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} 分钟 · 🏆 首次通关 +{reward} 🪙\n"
        "..................................................\n"
        "{teaser}\n\n{status}"
    ),
    "quest.card_done": "✅ <i>任务已通关，奖励已领取。想重玩随时来！</i>",
    "quest.card_progress": "⏯ <i>你有一段冒险还没玩完。</i>",
    "quest.card_new": "🆕 <i>你还没玩过这个故事。</i>",
    "quest.btn_start": "▶️ 开始任务",
    "quest.btn_restart": "🔄 重新开始",
    "quest.btn_resume": "⏯ 继续",
    "quest.btn_list": "🗺️ 返回任务列表",
    "quest.btn_replay": "🔄 再玩一次",
    "quest.win_first": "\n\n🏆 <b>任务通关！奖励：+{coins} 🪙。</b>",
    "quest.win_repeat": "\n\n✅ <b>再次通关！</b>这个任务的奖励之前已经领过了。",
    "quest.fail_footer": "\n\n💀 <i>这个结局不算完美……不过故事随时可以重来！</i>",
    "quest.stale": "⏳ 这个场景已经过去了——从当前位置继续！",
    "quest.no_coins": "❌ 提示需要 {cost} 🪙，你的余额不够。去农场转转吧！",
    "quest.not_found": "❌ 未找到该任务。",
    "menu.btn_quests": "🗺️ 冒险任务",

    # ---------------- ферма ----------------
    "farm.btn_bonus": "🎁 领取奖励（每 24 小时 1 份肉排）",
    "farm.btn_load1": "🥩 装填 1 份",
    "farm.btn_loadall": "⚡ 全部装填",
    "farm.btn_shop": "🏪 进入商店",
    "farm.status_all_fueled": "🟢 所有赛博钻机都已加满燃料，正在挖金币！",
    "farm.status_partial": "🟡 {total} 台赛博钻机中已装填 {fueled} 台。其余的还在等冰箱里的肉排！",
    "farm.status_no_fuel": "🔴 赛博钻机全停了！冰箱里的燃料不够。",
    "farm.status_no_drills": "💡 到 /shop 添置更强的机器人——农场会挖得更多。",
    "farm.boost_nuclear": "🔋 核能加速 x5 持续到 {until} UTC（肉排消耗 ×3）",
    "farm.boost_nitrogen": "❄️ 液氮冷却 +40% 持续到 {until} UTC",
    "farm.boost_drone": "🛸 大师无人机延长机器人寿命，持续到 {until} UTC",
    "farm.no_boosts": "暂无生效的强化——去 /shop 看看吧。",
    "farm.burnout": "🔥 下一次机器人报废：<b>{until} UTC</b>\n",
    "farm.btn_activate_intern": "🚀 激活实习机器人（免费）",
    "farm.intern_activated": "🤖 实习机器人上岗了！永久每小时 +1 🪙——不吃燃料，没有期限。",
    "farm.intern_already": "🤖 你的实习机器人已经在工作了。",
    "farm.btn_claim_intern": "🎁 领取实习机器人（{n}）",
    "farm.intern_pending": "🎁 你的智力等级为你赢得了实习机器人：<b>{n}</b> 台——点下方按钮领取！",
    "farm.intern_claimed_new": "🤖 新的实习机器人上岗了！永久每小时 +1 🪙。",
    "farm.intern_none": "🤖 暂时没有新的实习机器人——下一个在智力等级 10、20、30…级等你。",
    "games.intern_ready": "🎁 新等级为你赢得了一台<b>实习机器人</b>——去农场领取吧！",
    "farm.intern_line": "• 实习机器人（每小时 {rate} 🪙，永久）：<code>{count} 台</code>\n",
    "farm.intern_hint": "🎁 你有一台免费的实习机器人！点下方按钮，它将永久每小时挖 1 🪙。",
    "farm.dashboard": (
        "🚜 <b>ROFL HUB 中央燃料中心</b>\n"
        "..................................................\n"
        "🤖 工厂里的在役机器人：<b>{total} 台</b>\n"
        "{intern}• 初级矿工（每小时 {junior_rate} 🪙）：<code>{junior} 台</code>\n"
        "• 赛博钻机（每小时 {premium_rate} 🪙）：<code>{premium} 台</code>\n"
        "{burnout}\n"
        "📊 <b>你农场的当前速度：</b>\n"
        "• 每小时产出：<b>+{speed_hour} 🪙</b>\n"
        "• 每天产出：<b>+{speed_day} 🪙</b>\n\n"
        "⚡ <b>强化：</b>\n{boosts}\n\n"
        "📋 <b>游戏工厂状态：</b>\n"
        "{status}\n"
        "..................................................\n"
        "📦 <b>自动冰箱状态：</b>\n"
        "🥩 燃料储备：<b>{fridge} / {capacity} 份</b>\n"
        "💼 仓库里的肉排：<code>{inv} 份</code>\n"
        "..................................................\n"
        "<i>💿 注意：机器人寿命 30 天（大师无人机可暂停损耗）。"
        "每台赛博钻机每工作 24 小时都会从冰箱吃掉自己的一整份肉排："
        "3 台机器人——每天 3 份。盯紧燃料！</i>"
    ),
    "farm.bonus_ok": "🎁 赛博肉排已入仓库！24 小时后再来。",
    "farm.bonus_wait": "⏳ 奖励已经领过了！下一份肉排还要等 {hours} 小时 {minutes} 分钟。",
    "farm.no_inv_cutlets": "❌ 你的仓库里没有赛博肉排！去 /shop 买一些吧！",
    "farm.fridge_full": "📦 你的冰箱已经塞满了！",

    # ---------------- профиль ----------------
    "profile.caption": (
        "📋 <b>ROFL HUB 玩家个人中心</b>\n"
        "..................................................\n"
        "🆔 你的护照 ID：<code>{user_id}</code>\n"
        "{vip}"
        "💰 当前余额：<b>{balance} 🪙</b>\n"
        "🏆 你的身份：<b>{team}</b>\n"
        "🧠 智力等级：<b>{level}</b> · 距离 {next_level} 级：还需在 /quiz 中答对 "
        "<b>{left}</b> 题（奖励：+{reward} 🪙）\n"
        "..................................................\n"
        "<i>这里显示的是你此刻拥有的一切。用按钮飞往其他版块吧！</i>"
    ),
    "profile.no_team": "暂无战队",
    "profile.team_label": "战队",
    "profile.clan_label": "公会",
    "profile.btn_farm": "🚜 我的赛博农场",
    "profile.btn_shop": "🏪 商店",
    "profile.stats": (
        "📊 <b>游戏成就统计（30 天）</b>\n"
        "..................................................\n"
        "🧠 游戏智力等级：<b>{level}</b>（累计正确回答：{total}）\n"
        "🎮 对决场次：<b>{played} 局</b>\n"
        "🏆 击败对手次数：<code>{won} 次</code>\n"
        "👥 邀请的活跃好友：<b>{refs} 人</b>\n"
        "..................................................\n"
        "<i>统计会保存你的历史功绩——哪怕赢来的金币早已在市场上花掉了！</i>"
    ),
    "img.passport": "护照 ID：{user_id}",
    "img.owner": "领袖：@{username}",
    "img.balance": "余额：{balance} 金币",
    "img.fridge": "冰箱：{fridge} / {capacity} 份",
    "img.inv": "仓库肉排：{inv} 份",
    "img.junior": "初级矿工：{count} 台",
    "img.premium": "赛博钻机：{count} 台",

    # ---------------- игры: общий движок ----------------
    "games.win": "🎉 <b>胜利！</b> 🎉\n已到账：<b>+{reward} 🪙</b>",
    "games.lose": "💀 <b>落败！</b>\n已扣除：<b>-{penalty} 🪙</b>",
    "games.draw": "🤝 <b>平局！</b>\n已扣除：<b>-{penalty} 🪙</b>",
    "games.limit": (
        "🛑 <b>已达每日上限！</b>\n\n"
        "今天你在「{game}」里已经拿满 {limit} 场胜利。上限将于 00:00 UTC 重置。\n\n"
        "⚡ 解除上限：24 小时 15 ★，30 天 249 ★（/shop 的「游戏专区」）。"
    ),
    "games.no_coins": "❌ 你只有 0 🪙——付不起本局费用。去 /farm 领取农场收入吧！",
    "games.balance": "💰 余额：<b>{balance} 🪙</b>",
    "games.btn_retry": "🎮 再来一局！",
    "games.btn_hub": "🕹️ 游戏区",
    "games.level_up": (
        "🏅 <b>智力等级提升：{level}！</b>奖励：<b>+{bonus} 🪙</b>！\n"
        "下一级：答对 {next_required} 题 → +{next_reward} 🪙。"
    ),
    "games.name.rps": "石头剪刀布",
    "games.intern_bonus": "🤖 {level} 级！又一台实习机器人加入你的农场——现在共有 {count} 台。",
    "games.name.hl": "比大小",
    "games.name.quiz": "竞答",
    "games.name.safe": "保险箱",
    "games.name.math": "Math",  # TODO(перевод 26.10)
    "games.name.flags": "Flags and capitals",  # TODO(перевод 26.10)
    "games.name.code": "Code breaker",  # TODO(перевод 26.10)
    "games.name.memory": "Memory",  # TODO(перевод 26.10)

    # ---------------- КНБ ----------------
    "rps.intro": (
        "🪨✂️🧻 <b>石头剪刀布</b>\n\n"
        "获胜：<b>+{reward}</b> · 失败/平局：<b>-{penalty}</b>\n"
        "每日胜场上限：<b>{limit}</b>"
    ),
    "rps.rock": "🪨 石头",
    "rps.scissors": "✂️ 剪刀",
    "rps.paper": "🧻 布",
    "rps.draw": "🤝 <b>平局！</b>双方都出了{bot}。",
    "rps.win": "🏆 <b>胜利！</b>{user} 克制 {bot}。",
    "rps.lose": "💀 <b>机器人赢了。</b>{bot} 克制 {user}。",

    # ---------------- Больше/Меньше ----------------
    "hl.intro": (
        "🎲 <b>比大小</b>\n\n机器人亮出数字：<b>{base}</b>。\n"
        "隐藏数字会更大还是更小？\n"
        "获胜：<b>+{reward}</b> · 失败：<b>-{penalty}</b> · 上限：<b>{limit}</b> 场胜利"
    ),
    "hl.btn_up": "📈 更大",
    "hl.btn_down": "📉 更小",
    "hl.result": "🎲 <b>本局结果</b>\n\n机器人的数字：<b>{base}</b> · 隐藏数字：<b>{secret}</b>",

    # ---------------- викторина ----------------
    "quiz.round": (
        "🧠 <b>竞答 • {category}</b>\n"
        "🤔 问题：<b>{question}</b>\n\n"
        "<i>🌐 题目暂时为俄语——中文题库即将上线！</i>"
    ),
    "quiz.btn_new": "🧠 新题目",
    "quiz.timeout": "⌛ <b>时间到！</b> ⌛\n正确答案：<b>{correct}</b>",
    "quiz.stale": "⏳ 这道题已经失效。开始新的一题吧！",
    "quiz.stale_alert": "这道题已经失效。开始新的一题吧！",
    "quiz.empty": "⚠️ 题库是空的。请告知管理员。",
    "quiz.wrong": "❌ <b>答错了</b> ❌\n正确答案：<b>{correct}</b>",
    "quiz.lost_line": "💀 落败扣除 <b>-{penalty} 🪙</b>！",
    "quiz.level_line": (
        "🧠 智力等级：<b>{level}</b>\n"
        "距离 {next_level} 级还差 <b>{left}</b> 场胜利"
    ),
    "quiz.rules": (
        "<i>限时 {seconds} 秒作答！\n"
        "答对：余额 +{win} 🪙\n"
        "答错 / 超时：扣除 -{penalty} 🪙\n"
        "上限：每日 {limit} 场胜利</i>"
    ),



    # ---------------- Сейф ----------------
    "safe.intro": (
        "🔐 <b>赛博保险箱</b>\n\n"
        "里面装着 <b>{jackpot} 🪙</b>大奖！箱门用 1 到 {codes} 的密码锁着。"
        "你只有一次机会。\n"
        "破解成功：<b>+{jackpot}</b> · 触发警报：<b>-{penalty}</b> · 上限：<b>{limit}</b> 场胜利"
    ),
    "safe.btn_retry": "🔐 再撬一次！",
    "safe.win": "🔓 <b>保险箱开了！</b>密码是：<b>{code}</b>。",
    "safe.lose": "🚨 <b>警报响了！</b>你按的是 {guess}，密码其实是：<b>{code}</b>。",

    # ---------------- дуэли ----------------
    "duel.intro": (
        "⚔️ <b>1对1 对决：押注版石头剪刀布</b>\n"
        "..................................................\n"
        "像打扑克一样，挑一张适合你钱包的桌子。押注立刻扣除，"
        "对手是真实的 ROFL HUB 玩家！\n\n"
        "💰 奖池 = 双方押注之和。胜者拿走奖池的 <b>{payout_percent}%</b>，"
        "<b>{burn_percent}%</b> 永久销毁（通缩！）。\n"
        "🤝 平局立即重出手势，奖池留在桌上。\n"
        "⏱ 每次出手势限时 <b>{move_timeout} 秒</b>，不出手就由随机生成器替你选。\n"
        "🏆 对决胜利会计入你战队在大作战中的成绩！\n\n"
        "👇 <b>选择一张桌：</b>"
    ),
    "duel.btn_table": "⚔️ {stake} 🪙 桌",
    "duel.btn_cancel": "❌ 离桌（退回押注）",
    "duel.btn_move_rock": "🪨 石头",
    "duel.btn_move_scissors": "✂️ 剪刀",
    "duel.btn_move_paper": "🧻 布",
    "duel.waiting": (
        "🪑 <b>你已坐上 {stake} 🪙 桌。</b>押注已入奖池。\n"
        "正在等待第二位选手……对方一落座，你们双方就会收到选择手势的提示！\n"
        "<i>排队保留 {ttl} 分钟，之后押注会自动退回。</i>"
    ),
    "duel.cancelled": "🚪 你已离桌。<b>{stake} 🪙</b>押注已退回余额。",
    "duel.expired": "⌛ {stake} 🪙 桌上一直没等到对手。<b>{stake} 🪙</b>押注已退回。",
    "duel.matched": (
        "⚔️ <b>找到对手了！{stake} 🪙 桌。</b>\n"
        "奖池：<b>{bank} 🪙</b> · 胜者可得：<b>{payout}</b>\n\n"
        "⏱ 你有 <b>{timeout} 秒</b>来选择手势！"
    ),
    "duel.move_saved": "✊ 手势已提交！等待对手出招……",
    "duel.draw_replay": (
        "🤝 <b>平局！第 {round} 回合。</b>双方出了同样的手势。\n"
        "奖池留在桌上。⏱ 再给 {timeout} 秒——选择手势："
    ),
    "duel.win": (
        "🏆 <b>你赢下了这场对决！</b>\n\n"
        "你的 {winner_move} 克制 {loser_move}。\n"
        "💰 赢得：<b>+{payout} 🪙</b> · 🔥 奖池销毁：{burned}\n"
        "💼 余额：<b>{balance} 🪙</b>"
    ),
    "duel.lose": (
        "💀 <b>对决失利。</b>\n\n"
        "对手的 {winner_move} 克制你的 {loser_move}。\n"
        "📉 <b>{stake} 🪙</b>押注进了胜者的奖池。\n"
        "要复仇吗？"
    ),
    "duel.reaper_prefix": "⏰ <b>回合超时！</b>缺少的手势已由随机生成器代选。\n\n",
    "duel.bad_table": "❌ 没有这张桌子。",
    "duel.already_in": "⚠️ 你已经在桌上或战斗中了！先打完当前这场对决。",
    "duel.no_coins": "❌ 坐上这张桌需要余额里有 {stake} 🪙。",
    "duel.cancel_impossible": "⚠️ 这次排队已无法取消（已匹配到对手或该桌已关闭）。",
    "duel.not_active": "⌛ 这场对决已经结束。",
    "duel.not_participant": "🔒 这不是你的对决！",
    "duel.move_already": "✋ 本回合你已经出过手势了。等对手吧！",
    "duel.bad_move": "❌ 未知手势。",
    "duel.btn_rematch": "⚔️ 复仇（回到选桌）",

    # ---------------- VIP ID ----------------
    "profile.vip_line": "💎 VIP ID：<b>{aliases}</b>\n",
    "profile.rank_line": "🎖 称号：<b>{rank}</b>\n",
    "rank.rookie": "新手",
    "rank.fighter": "战士",
    "rank.legend": "传奇",
    "rank.rofl": "ROFL",
    "rank.lmao": "LMAO",
    "rank.king": "KING",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>ROFL HUB 邀请计划</b>\n"
        "..................................................\n"
        "通过你的专属链接邀请好友，每有一人成为活跃玩家，"
        "你就能获得 <b>{bonus}</b>！\n\n"
        "🔗 <b>你的链接（点按复制）：</b>\n<code>{link}</code>\n\n"
        "📊 <b>你的统计：</b>\n"
        "👥 已邀请好友：<b>{invited} 人</b>\n"
        "💰 邀请奖励累计：<b>{earned} 🪙</b>\n"
        "..................................................\n"
        "<i>把链接发到班级群、朋友圈和社交网络——队伍越大，你的余额涨得越快！</i>"
    ),
    "ref.btn_share": "📣 分享链接",
    "ref.share_text": "快来加入 ROFL HUB 游戏生态系统！",
    "ref.qualified_line": "✅ <b>活跃好友</b>是指在问答中达到 <b>{level} 级智力等级</b>、并在农场领取过 <b>{claims} 次每日肉排</b>的人。此时你可获得 <b>{bonus}</b>，每位好友仅一次。仅注册、不玩游戏没有奖励——这样对大家更公平。",
    "ref.qualified_notify": ("🤝 <b>你的好友成为了活跃玩家！</b>\n"
                             "智力等级 {level} 级、每日肉排领取 {claims} 次——均已达成。你获得 <b>{bonus}</b>。继续邀请吧！"),

    "team.err_len": "❌ 文字长度必须在 1 到 {max} 个字符之间！",
    "team.err_link": "🚨 安全警告！严禁出现链接、用户名和电话号码！",
    "team.err_badword": "❌ 检测到不文明用语！请遵守大厅规则。",
    "team.err_already": "⚠️ 你已经在某个战队或公会里了！请先退出。",
    "team.err_money": "❌ 金币不足！创建战队需要 {cost} 🪙，你有 {balance} 🪙。",
    "team.err_captain": "⚠️ 你已经是另一个战队的队长了！",
    "team.err_taken": "⚠️ 名称「{name}」已被占用！换一个独一无二的吧。",
    "team.err_gone": "❌ 这个战队已不存在。",
    "team.err_full": "📦 这个战队已经满员了！",
    "team.err_not_member": "❌ 你不在任何战队里。",
    "mk.err_no_team": "🏆 战队交易所仅限战队成员。请加入战队或创建自己的战队。",
    "mk.err_team_only": "🔒 该挂单仅限卖家所在战队的成员。",
    "help.err_qty": "每次可请求 1 到 {max} 个资源。",
    "help.err_open": "你已有一条未完成的请求——请等待支援或撤回。",
    "help.err_not_found": "该请求已关闭。",
    "help.err_self": "不能用礼物来满足自己的请求 🙂",
    "help.err_limit": "今天你已赠送 {max} 个资源——额度将在 UTC 00:00 重置。",
    "help.err_not_active": "🔒 达到智力等级 {level} 并领取 {claims} 次每日肉排后，才能赠送资源。",
    "it.err_none": "仓库里已经没有这件物品了。",

    "profile.btn_delete": "🗑 删除账号",
    "acct.warn": (
        "⚠️ <b>删除账号</b>\n"
        "..................................................\n"
        "账号删除后，以下内容将<b>永久消失</b>：\n"
        "• 金币、肉排、资源和农场的全部机器人；\n"
        "• 加成、解除上限以及所有用 Stars 购买的内容——<b>Stars 不予退还</b>；\n"
        "• VIP ID、竞答和冒险任务进度；\n"
        "• 你在战队中的位置（队长职位将移交给战队老成员）。\n"
        "交易所中未完成的挂单会立即撤销，商品退回仓库。\n\n"
        "⏳ 账号会先冻结 <b>{days} 天</b>，期间只需点一下按钮即可反悔。"
        "之后删除不可恢复。若以后回来，将从零开始，起始奖励不会再次发放。\n\n"
        "<i>删除按钮将在 {seconds} 秒后生效——请仔细阅读。</i>"
    ),
    "acct.btn_keep": "✅ 不，保留账号",
    "acct.btn_confirm": "🗑 是，删除账号",
    "acct.wait": "⏳ 请再等 {seconds} 秒——先看清究竟会删除什么。",
    "acct.kept": "👍 太好了，账号继续留在你身边！",
    "acct.scheduled": (
        "🗑 账号已冻结，将于 <b>{date}</b>（UTC）删除。\n"
        "交易所挂单已撤销，商品已退回仓库。\n\n"
        "改变主意了？点下方按钮，一切恢复原样。"
    ),
    "acct.pending_notice": (
        "⏳ 账号已冻结，将于 <b>{date}</b>（UTC）删除。\n"
        "想继续留在游戏里？点下方按钮。"
    ),
    "acct.btn_undo": "↩️ 取消删除",
    "acct.undone": "🎉 已取消删除——账号重新属于你！",
    "acct.purged": "🗑 你的 ROFL HUB 账号已删除。感谢你的参与！想回来的话，点 /start。",
    "acct.deleted_notice": "账号已删除。点 /start 重新开始。",
    "acct.welcome_back": (
        "👋 <b>欢迎回来！</b>\n"
        "个人资料已从零重新创建。起始奖励只发放一次，所以余额为 0 🪙。"
        "农场、游戏和竞答在等你！"
    ),
    "tr.err_not_active": (
        "🔒 达到 {level} 级智力等级并领取 {claims} 次每日肉排后，才能转账金币——"
        "这样可以保护生态系统免受虚假账号侵扰。"
    ),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>给其他玩家转账金币</b>\n"
        "..................................................\n"
        "命令格式：\n"
        "<code>/transfer ID 金额</code> — 按护照 ID（见 /profile）\n"
        "<code>/transfer @username 金额</code> — 按用户名\n"
        "<code>/transfer ROFL-HUB-777 金额</code> — 按拍卖的 VIP ID\n\n"
        "示例：\n<code>/transfer 123456789 500</code>\n<code>/transfer @friend 100</code>\n\n"
        "📌 最低金额：<b>{min} 🪙</b>"
    ),
    "tr.not_found": "❌ 未找到收款人。请检查护照 ID 或 @username——对方必须已在机器人中注册。",
    "tr.self": "🤨 不能给自己转账金币——不然就成永动机经济了！",
    "tr.blocked": "🚫 该玩家已被封禁——无法向其转账。",
    "tr.min": "❌ 最低转账金额为 {min} 🪙。",
    "tr.insufficient": "❌ 金币不足！你的余额：<b>{balance} 🪙</b>。",
    "tr.err_insufficient": "❌ 余额中的金币不足。",
    "tr.confirm": (
        "🔄 <b>确认转账：</b>\n\n"
        "👤 收款人：<b>{recipient}</b>（ID <code>{recipient_id}</code>）\n"
        "💸 扣除金额：<b>{amount} 🪙</b>{fee_line}\n"
        "💰 对方将收到：<b>{received} 🪙</b>\n\n"
        "<i>转账无法撤销——仔细核对收款人！</i>"
    ),
    "tr.fee_line": "\n🔥 中心手续费：<b>{fee} 🪙</b>（将销毁）",
    "tr.btn_confirm": "✅ 确认转账",
    "tr.btn_cancel": "❌ 取消",
    "tr.cancelled_toast": "转账已取消",
    "tr.cancelled": "❌ <b>转账已取消。</b>金币原封不动。",
    "tr.not_yours": "🔒 这不是你的转账！",
    "tr.done_toast": "✅ 转账完成！",
    "tr.done": (
        "✅ <b>转账完成！</b>\n\n"
        "💸 已发送：<b>{amount} 🪙</b>（收款人 ID <code>{recipient_id}</code>）\n"
        "💰 你的余额：<b>{balance} 🪙</b>"
    ),
    "tr.received": (
        "💰 <b>有人给你转了 {amount} 🪙！</b>\n"
        "发送方：ID <code>{sender_id}</code>。金币已到账——快去 /profile 看看！"
    ),

    # ---------------- магазин и платежи ----------------
    "shop.header": "🏪 <b>ROFL HUB 商店</b>\n购买通过官方 Telegram Stars 完成。用下方按钮选择专区。",
    "shop.cat_farm": (
        "🚜 <b>商店 · 农场专区</b>\n"
        "..................................................\n"
        "使用期 30 天的机器人、燃料、冰箱、强化和大师无人机。\n"
        "📦 你的冰箱当前容量：<b>{capacity} 份肉排</b>\n"
        "..................................................\n"
        "👇 <b>选择商品：</b>"
    ),
    "shop.cat_games": (
        "🕹️ <b>商店 · 游戏专区</b>\n"
        "..................................................\n"
        "解除胜场上限、金币礼包和超级公会许可证。\n"
        "..................................................\n"
        "👇 <b>选择商品：</b>"
    ),
    "pay.invoice_desc": "ROFL HUB 游戏内容即时送达。",
    "pay.invoice_error": "⚠️ 无法生成 Telegram Stars 账单。稍后再试。",
    "pay.success": "🎉 <b>付款已确认！</b>\n🧾 <code>{charge}</code>\n💵 已扣除：<b>{stars} ★</b>\n\n{text}",
    "pay.crash": (
        "🚨 付款成功，但发货暂时失败。我们已经在处理了。\n"
        "请保存付款编号：<code>{charge}</code>"
    ),
    "pay.refunded": "💫 Stars 已自动退回你的账户。",
    "pay.keep_charge": "请保存付款编号以便退款：<code>{charge}</code>",
    "pay.already": "✅ 该笔付款已处理过，商品此前已发放。",
    "pay.support": (
        "🛟 <b>TELEGRAM STARS 付款支持</b>\n"
        "..................................................\n"
        "ROFL HUB 的所有商品均为数字商品，付款后即时送达。\n\n"
        "⚙️ <b>如果付款成功但商品没有到账：</b>\n"
        "发货失败时，机器人会自动退回 Stars。如果没有退回——"
        "请把付款编号发到这里（在收据里，格式为 <code>xxxx...</code>）并描述问题。"
        "管理员会在数据库中核对付款，并在 24 小时内解决。\n\n"
        "💫 <b>退款政策：</b>\n"
        "若商品未收到或发放有误，可以退款。"
        "已正确送达的数字商品不支持退款。\n"
        "..................................................\n"
        "<i>本版块是符合 Telegram 规则的官方购买支持入口。</i>"
    ),

    # ---------------- доставка ----------------
    "dlv.cutlets": "🥩 已加入仓库：<b>{qty} 份肉排</b>。",
    "dlv.miner": "🤖 机器人<b>「{name}」</b>已送达你的农场。\n⏳ 使用期限：至 <b>{until} UTC</b>。",
    "dlv.miner_junior": "初级矿工",
    "dlv.miner_premium": "赛博钻机",
    "dlv.fridge": "📦 冰箱已扩容至 <b>{capacity} 份肉排</b>。",
    "dlv.coins": "💰 已到账 <b>+{amount} 🪙</b>。",
    "dlv.boost_nuclear": "🔋 核能加速 x5 生效至 <b>{until} UTC</b>。",
    "dlv.boost_nitrogen": "❄️ 液氮冷却 +40% 生效至 <b>{until} UTC</b>。",
    "dlv.drone": "🛸 大师无人机守护你的农场至 <b>{until} UTC</b>。",
    "dlv.unlimit": "⚡ 胜场上限已解除，有效期至 <b>{until} UTC</b>。",
    "dlv.clan": "🏆 你的战队获得<b>超级公会</b>身份：席位上限 {max}。",
    "dlv.err_fridge": "你已经拥有同容量或更大的冰箱了。",
    "dlv.err_no_team": "你还没有创建战队。先用 /create_team 创建一个吧。",
    "dlv.err_mega": "你的战队已经是超级公会了。",
    "dlv.intern_upgrade": "♾ 实习机器人晋升为<b>永久初级矿工</b>：每小时 5 🪙，没有期限！",
    "dlv.err_no_intern": "还没有激活的实习机器人——先在 /farm 里激活它。",
    "dlv.err_intern_refs": "升级需要 {need} 位活跃好友（条件见 /invite），你目前有 {have} 位。",
    "mk.header": "📈 <b>肉排交易所</b>\n..................................................\n挂单：<b>{orders}</b> · 在售肉排：<b>{cutlets}</b> · 最低价：<b>{best}</b>\n平台手续费：每笔成交 <b>{fee}%</b>（销毁——抗通胀）\n🥩 你仓库里的肉排：<b>{inv}</b>\n\n{body}\n\n<i>点击挂单即可购买。出售请用 /sell。</i>",
    "mk.empty": "暂时没有挂单。抢先出售：/sell 数量 价格",
    "mk.order_line": "🥩 #{id} · <b>{qty} 块</b>，单价 <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}：{qty} 块，单价 {price} 🪙",
    "mk.btn_my": "📋 我的挂单",
    "mk.btn_sell_help": "💰 如何出售肉排",
    "mk.btn_refresh": "🔄 刷新",
    "mk.btn_back": "← 返回交易所",
    "mk.pick": "🛒 <b>挂单 #{id}</b>：可买 {qty} 块，单价 {price} 🪙。\n买几块？",
    "mk.btn_qty": "{qty} 块 — {total} 🪙",
    "mk.btn_qty_all": "全部 {qty} 块 — {total} 🪙",
    "mk.buy_toast": "成交！",
    "mk.buy_done": "✅ 以 <b>{total} 🪙</b> 买入 <b>{qty} 块肉排</b>，已入仓库——快给钻机加燃料！",
    "mk.sold_notify": "💰 <b>交易所：已售出！</b> 挂单 #{id}：售出 {qty} 块，单价 {price}。你收到 <b>+{got} 🪙</b>（手续费 {fee} 已销毁）。",
    "mk.sell_help": "💰 <b>如何出售肉排</b>\n\n命令：<code>/sell 数量 价格</code>\n示例：<code>/sell 10 250</code> —— 10 块肉排，每块 250 🪙。\n\n肉排从仓库转入挂单等待买家（随时可撤回）。每单最多 {max_qty} 块，最多 {max_orders} 个挂单。成交时销毁 {fee}% 手续费。每块肉排不低于 {min} 🪙：用星星在商店买燃料永远比交易所划算。资源、求购单和交换都在游戏应用里。",
    "mk.sell_confirm": "📝 以单价 <b>{price}</b> 🪙挂出 <b>{qty} 块肉排</b>？\n总额 {total} · 手续费 {fee} 将销毁 · 你将收到 <b>{got} 🪙</b>。",
    "mk.btn_confirm_sell": "✅ 挂到交易所",
    "mk.btn_cancel": "❌ 取消",
    "mk.sell_toast": "挂单成功！",
    "mk.sell_done": "✅ 挂单 <b>#{id}</b> 已上架：{qty} 块，单价 {price} 🪙。成交后会通知你。",
    "mk.cancelled_toast": "已取消",
    "mk.cancel_text": "❌ <b>已取消。</b> 肉排仍在仓库。",
    "mk.my_header": "📋 <b>你的挂单</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} 块，单价 {price} 🪙",
    "mk.my_empty": "📋 你没有未成交的挂单。",
    "mk.btn_cancel_order": "❌ 撤回挂单 #{id}",
    "mk.err_newbie_price": "🔒 While your account is new, you can buy at no more than {max} 🪙 apiece. The limit lifts at intelligence level {level} and after {claims} daily cutlets.",
    "mk.err_cancel_room": "📦 Not enough storage room: {free} free. Make room first, then withdraw the lot.",
    "sw.err_ratio": "⚖️ This swap is too uneven: the two sides (valued at the market's minimum prices) may differ by at most {x}×.",
    "mk.order_cancelled": "↩️ 挂单 #{id} 已撤回：<b>{qty} 块肉排</b>已返回仓库。",
    "mk.err_qty": "❌ 数量：每单 1 到 {max} 件。",
    "mk.err_price": "❌ 价格：每件 {min} 到 {max} 🪙。",
    "mk.err_no_cutlets": "❌ 仓库里只有 {have} 块肉排。冰箱里的肉排不能上架——见 /farm。",
    "mk.err_too_many": "❌ 上限：最多 {max} 个挂单。请在「我的挂单」中撤回一个。",
    "mk.err_not_found": "❌ 该挂单已关闭。",
    "mk.err_own": "🤨 不能购买自己的挂单。",
    "mk.err_insufficient": "❌ 余额不足：需要 {total} 🪙。",
    "farm.btn_market": "📈 肉排交易所",

    # ---------------- ресурсы (волна 22.10, вечер) ----------------
    "res.metal": "金属",
    "res.hydrogen": "氢气",
    "res.crystal": "晶体",
    "res.parts": "零件",
    "res.none": "暂时为空",
    "games.resource_gain": "{icon} 获得资源：<b>+{qty} {name}</b>（共 {total}）→ /workshop",
    "duel.metal_gain": "🪨 对决战利品：<b>+{metal} 石头</b> → /workshop",
    "quest.win_resources": "\n📦 另有一套奖励：每种资源各 <b>{qty}</b>，外加 🪵 木材和 🐄 奶牛 → /workshop",
    "profile.resources_line": "🧰 资源：{stock}\n",
    "menu.btn_goals": "🎯 每日目标",
    "menu.btn_raids": "🏴‍☠️ 突袭",
    "menu.btn_workshop": "🔧 工坊",
    "farm.btn_workshop": "🔧 工坊",
    "farm.btn_app": "🏭 在应用中打开农场",
    "menu.btn_app": "🚀 游戏应用：农场、工坊、突袭",
    "app.btn_section": "🚀 在应用中打开",
    "app.goto_workshop": "🔧 <b>工坊</b>在游戏应用里：资源、配方，一键制造。",
    "app.goto_raids": "🏴\u200d☠️ <b>突袭</b>在游戏应用里：侦察、防御姿态和复仇战。",
    "app.goto_station": "🛰 <b>战队空间站</b>在游戏应用里：进度、捐献和全队加成。",
    "app.goto_market": "📈 <b>肉排交易所</b>在游戏应用里更方便：报价、出售和你的挂单尽在一屏。",
    "mk.err_asset": "❌ 交易所没有这种商品。",
    "mk.err_no_resource": "❌ 资源不足：仓库里只有 {have}。",
    "mk.bid_filled_notify": "🙋 <b>交易所：求购单已成交！</b> 求购单 #{id}：以单价 {price} 🪙 买入 <b>+{qty} {icon}</b>。",
    "sw.err_same": "❌ 不能用资源交换同一种资源。",
    "sw.err_qty": "❌ 交换数量需为 1 到 {max}，付出和想要的都要填写。",
    "shop.btn_info": "ℹ️ 各商品有什么用",
    "sw.done_notify": "🔄 <b>交换 #{id} 已完成！</b>付出 {give}，获得 {want}。",
    "ws.err_coins": "🔒 金币不足：需要 {need} 🪙，余额 {have} 🪙。",
    "wk.eff_nitrogen": "❄️ 液氮 +40% {h} 小时",
    "wk.eff_nuclear": "☢️ 核能 x5 {h} 小时",
    "wk.eff_drone": "🛸 大师无人机 {h} 小时",
    "wk.eff_shield": "🛡 护盾 {h} 小时",
    "wk.eff_unlimit": "⚡ 无限畅玩 {h} 小时",
    "wk.eff_cutlet": "🥩 肉排 ×{n}",
    "wk.eff_resource": "{icon} +{n}",
    "wk.err_gone": "⏳ 这个本周配方已下架。",
    "wk.err_limit": "🔒 本周该配方的次数已用完（{limit}）。新的一周从周一 00:00 UTC 开始。",
    "games.resource_full": "📦 {icon} 仓库已满（{cap}）——多出的资源会丢失。去使用、出售，或在工坊扩建仓库。",
    "mk.err_storage_full": "📦 仓库空间不足：剩余 {free}。请在工坊扩建仓库。",
    "mk.err_buyer_full": "📦 买家的仓库已满——暂时无法成交（剩余 {free}）。",
    "ws.recipe_storage": "仓库扩建至 {cap}",
    "ws.done_storage": "📦 <b>仓库已扩建：</b>每种资源最多 {cap}。永久有效。",
    "ws.err_storage_max": "📦 仓库已达最大容量。",
    "farm.boost_armor": "🛡 赛博装甲 {level} 级：产量 +{percent}%，有效期至 {until} UTC",
    "farm.boost_station": "🛰 战队空间站 {level} 级：产量 +{percent}%",
    "clan.btn_station": "🛰 战队空间站",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>工坊</b>\n"
        "..................................................\n"
        "🧰 你的资源：{stock}\n"
        "⛏ 金属——石头剪刀布与对决 · 💧 氢气——比大小 · "
        "💎 晶体——竞答 · ⚙️ 零件——赛博保险箱。冒险任务送一整套。\n\n"
        "🛡 赛博装甲：<b>{armor}/{armor_max} 级</b>（每级产量 +{armor_pct}%，有效期 30 天）\n"
        "🚀 穿梭机：<b>{shuttle}</b>——交易所手续费 {shuttle_fee}%，每单最多 {shuttle_qty} 份肉排\n\n"
        "<i>✅ ——资源足够，🔒 ——暂时不够。一键即成。</i>"
    ),
    "ws.shuttle_yes": "已建成",
    "ws.shuttle_no": "未建成",
    "ws.recipe_nitro_6h": "液氮冷却 6 小时",
    "ws.recipe_nuclear_3h": "核能加速 3 小时",
    "ws.recipe_drone_24h": "大师无人机 24 小时",
    "ws.recipe_shield_24h": "突袭护盾 24 小时",
    "ws.recipe_cutlet": "合成赛博肉排",
    "ws.recipe_armor": "赛博装甲 {level} 级",
    "ws.recipe_shuttle": "建造穿梭机",
    "ws.btn_shuttle_owned": "🚀 穿梭机已建成",
    "ws.btn_armor_max": "🛡 赛博装甲：已满级",
    "ws.btn_refresh": "🔄 刷新",
    "ws.btn_farm": "🚜 去农场",
    "ws.noop": "已经是最高级",
    "ws.toast": "完成！",
    "ws.done_nitrogen": "❄️ <b>液氮冷却 +40%</b> 生效至 {until} UTC。",
    "ws.done_nuclear": "☢️ <b>核能加速 x5</b> 生效至 {until} UTC。钻机的肉排消耗 ×3！",
    "ws.done_drone": "🛸 <b>大师无人机</b>守护机器人至 {until} UTC。",
    "ws.done_shield": "🛡 <b>突袭护盾</b>持续至 {until} UTC。资源受到保护。",
    "ws.done_cutlet": "🥩 合成完毕：<b>+{qty} 份赛博肉排</b>已入仓库。去 /farm 加燃料吧！",
    "ws.done_armor": "🛡 <b>赛博装甲 {level} 级！</b>农场产量：<b>+{percent}%</b>，有效期 30 天。",
    "ws.done_shuttle": "🚀 <b>穿梭机建成！</b>你出售时的手续费降为 {fee}%，每单最多 {qty} 份肉排。穿梭机只属于你，永久有效。",
    "ws.err_unknown": "❌ 没有这个配方。",
    "ws.err_off": "🔧 这个配方暂时不可用。",
    "ws.err_locked": "🔒 配方将在 {hours} 小时后解锁——新配方每天解锁一个。",
    "ws.recipe_camo_12h": "伪装 12 小时",
    "ws.recipe_trap_24h": "诱饵 24 小时",
    "ws.recipe_drill_24h": "姿态训练器 24 小时",
    "ws.recipe_forsage": "飞船加力",
    "ws.recipe_economizer": "节能器",
    "ws.recipe_cargo": "扩容货舱",
    "ws.recipe_thermos_24h": "肉排保温壶 24 小时",
    "ws.recipe_stamp": "交易所印章",
    "ws.recipe_banner_24h": "战队旗帜 24 小时",
    "ws.recipe_dome_12h": "战队穹顶 12 小时",
    "it.err_no_cooldown": "🚀 无需跳过冷却——飞船已经可以出击。",
    "it.err_forsage_daily": "🔥 加力今天已用过——{hours} 小时后可再次使用。",
    "res.stone": "石头",
    "res.wood": "木材",
    "res.fire": "火种",
    "res.energy": "电力",
    "res.battery": "电池",
    "res.cow": "奶牛",
    "res.core": "核心",
    "tech.comm": "通讯",
    "tech.scout": "侦察",
    "tech.attack": "进攻",
    "tech.defense": "防御",
    "tech.science": "科研",
    "tech.err_max": "🏆 已是最高等级。",
    "tech.err_unknown": "❌ 没有这项技术。",
    "tech.err_tool": "🧰 需要 {tool} 级工具套装——请到实验室制作。",
    "tech.err_cooldown": "⏳ {hours} 小时后可研究下一级。",
    "tech.err_science": "📚 当其他所有技术都达到 {level} 级时，才能研究 {level} 级科学。",
    "ws.err_items_full": "📦 物品仓库已满：最多 {max} 件物品。请启用一些或扩建仓库。",
    "post.scope_team": "战队榜",
    "post.scope_clan": "公会榜",
    "post.scope_teams": "战队与公会",
    "post.scope_solo": "个人榜",
    "nom.farm_mined": "用农场挖到最多金币",
    "nom.coins_earned": "赚到最多金币",
    "nom.duel_wins": "赢得最多对决",
    "nom.duels_played": "进行最多对决",
    "nom.quiz_wins": "知识问答答对最多",
    "nom.rps_wins": "石头剪刀布赢得最多",
    "nom.safe_wins": "破解最多赛博保险箱",
    "nom.game_wins_total": "对战机器人赢得最多游戏",
    "nom.referrals": "带来最多活跃好友",
    "nom.stars_spent": "最多支持生态（Stars）",
    "nom.insta_reels": "谁的 Instagram 短视频最火",
    "nom.youtube_shorts": "谁的 YouTube Shorts 视频最火",
    "nom.tiktok": "谁的 TikTok 视频最火",
    "bt.err_closed": "⏳ 这场大作战已结束。",
    "bt.err_no_entry": "这场大作战无需报名。",
    "bt.err_no_team": "🏆 请先加入战队。",
    "bt.err_scope": "这场大作战不适用于你的战队类型。",
    "bt.err_full": "✅ 战队报名已满。",
    "bt.err_battery": "🔋 没有电池——去工坊制作一个。",
    "horse.err_max": "🐎 马厩里已有 {max} 匹马，装不下更多了。",
    "horse.err_coins": "🪙 一匹马要 {price} 🪙——金币还不够。",
    "shuttle.err_none": "🚀 请先在工坊建造穿梭机。",
    "cart.err_horse": "🛒 马车需要马：马车数不能超过马的数量（且不超过 {max} 辆）。",
    "raid.err_need_tech": "🔬 突袭需要 1 级「{tech}」技术——请到实验室研究。",
    "raid.err_battery": "🔋 侦察需要一块电池——请在工坊制作。",
    "games.energy_gain": "⚡ 好运：+1 电力！",
    "ws.recipe_bonfire": "篝火：用木材和石头生火",
    "ws.recipe_battery": "电池（×2）",
    "ws.recipe_cart": "马车",
    "ws.recipe_meds_72h": "急救包 72 小时",
    "ws.err_resources": "🔒 资源不足：{kind} 需要 {need}，现有 {have}。去游戏里挖吧！",
    "ws.err_shuttle_owned": "🚀 穿梭机已建成——每位玩家只能有一艘。",
    "ws.err_armor_max": "🛡 装甲已达最高级（{max}）。",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>突袭</b>\n"
        "..................................................\n"
        "💧 氢气：<b>{hydrogen}</b>（每次出击消耗 {fuel}）\n"
        "🚀 {ready}\n"
        "🛡 {shield}\n"
        "✊ 防御姿态：<b>{stance}</b>\n\n"
        "📊 突袭：<b>{attacks}</b> 次（成功 {attack_wins} 次）· 守住：<b>{holds}/{defenses}</b>\n\n"
        "<i>战利品只有资源：目标库存的 {percent}%，每种资源最多 {cap}。"
        "金币、机器人和肉排不受影响。你的手势对阵目标的防御姿态——"
        "决策对决策。每 {cooldown} 小时可出击一次；复仇战免费。</i>"
    ),
    "raid.ready_line": "飞船已准备好出击",
    "raid.cooldown_line": "冷却中：还需 {minutes} 分钟",
    "raid.shield_on": "护盾生效至 {until} UTC",
    "raid.shield_newbie": "新手保护（前 {days} 天）",
    "raid.shield_off": "没有护盾——去 /workshop 建造",
    "raid.stance_random": "随机（在菜单里选一个！）",
    "raid.btn_scout": "🔭 侦察：寻找目标",
    "raid.btn_revenge": "⚔️ 复仇战：{name}",
    "raid.btn_stance": "✊ 防御姿态",
    "raid.btn_workshop": "🛡 建造护盾",
    "raid.btn_refresh": "🔄 刷新",
    "raid.btn_back": "← 返回",
    "raid.btn_open": "🏴‍☠️ 打开突袭",
    "raid.btn_again": "🏴‍☠️ 回到突袭",
    "raid.stance_pick": "✊ <b>防御姿态</b>\n只有别人突袭你的结果才会揭示它：对方的手势对阵你的姿态。偶尔换一换——太好猜的人容易被抢。",
    "raid.stance_saved": "姿态：{stance}",
    "raid.scout": "🔭 <b>侦察发现了目标。</b>出击消耗 {fuel} 💧。选一个：",
    "raid.btn_target": "🎯 {name} · 资源 ≈{total}",
    "raid.no_targets": "🔭 侦察一无所获：目前没有合适的目标（护盾、冷却、新手）。稍后再来。",
    "raid.pick_move": "✊ <b>你出什么手势？</b>它将对阵目标的防御姿态。出击：−{fuel} 💧。",
    "raid.pick_move_revenge": "⚔️ <b>复仇战！你出什么手势？</b>本次出击免费，不计冷却。",
    "raid.result_win": "🏴‍☠️ <b>突袭成功！</b>\n对 {name}：{move} 对阵 {stance}。\n战利品：<b>{loot}</b>",
    "raid.result_draw": "😐 <b>平局。</b>对 {name}：{move} 对阵 {stance}。飞船空手而归，燃料已烧掉。",
    "raid.result_lose": "💥 <b>防御守住了。</b>对 {name}：{move} 对阵 {stance}。\n目标反而获得：<b>{loot}</b>",
    "raid.result_footer": "<i>资源在 /workshop。护盾可防对方报复。</i>",
    "raid.victim_lost": "🚨 <b>你被突袭了！</b>{name}：{move} 对阵你的姿态 {stance}。\n损失：<b>{loot}</b>\n\n⚔️ {hours} 小时内可免费复仇。护盾——见 /workshop。",
    "raid.victim_draw": "🛡 <b>突袭打成平局。</b>{name}：{move} 对阵你的姿态 {stance}。没有损失。",
    "raid.victim_held": "🛡 <b>防御守住了！</b>{name}：{move} 对阵你的姿态 {stance}。\n防御战利品：<b>{loot}</b>",
    "raid.err_stance": "❌ 未知手势。",
    "raid.err_self": "🤨 突袭自己？不行。",
    "raid.err_gone": "❌ 目标不可用。",
    "raid.err_teammate": "🤝 自己人不抢——那是队友。",
    "raid.err_shielded": "🛡 目标有护盾。换一个吧。",
    "raid.err_revenge_gone": "❌ 复仇窗口已关闭。",
    "raid.err_cooldown": "⏳ 冷却中：还需 {minutes} 分钟。",
    "raid.err_victim_cooldown": "⏳ 该目标最近刚被抢过（暂停 {hours} 小时）。",
    "raid.err_fuel": "💧 氢气不足：需要 {need}，现有 {have}。氢气在比大小中获得。",

    # ---------------- ежедневные цели ----------------
    "goal.header": (
        "🎯 <b>今日目标</b>\n"
        "..................................................\n"
        "{goals}\n\n"
        "{status}\n"
        "🎁 宝箱：<b>+{coins} 🪙</b>和 <b>+{res}</b> 随机资源\n"
        "🔥 连续：<b>{streak}</b> 天 · 每连续第 {every} 天宝箱额外 +{bonus} 🪙\n\n"
        "<i>目标在 00:00 UTC 刷新。</i>"
    ),
    "goal.status_progress": "⏳ 完成全部三项——宝箱就是你的。",
    "goal.status_ready": "✅ <b>全部目标完成！快领宝箱。</b>",
    "goal.status_claimed": "🎁 今天的宝箱已经领过了。明天有新目标！",
    "goal.btn_claim": "🎁 领取宝箱",
    "goal.btn_go": "→ {goal}",
    "goal.btn_refresh": "🔄 刷新",
    "goal.toast": "宝箱已打开！",
    "goal.chest": "🎁 <b>宝箱已打开！</b>\n💰 +{coins} 🪙 · {icon} +{qty} {name}\n🔥 连续：{streak} 天",
    "goal.err_claimed": "🎁 今天已经领过了。",
    "goal.err_not_done": "⏳ 还有目标没完成。",
    "goal.win_quiz": "赢得 {n} 局竞答",
    "goal.win_rps": "赢得 {n} 局石头剪刀布",
    "goal.win_hl": "赢得 {n} 局比大小",
    "goal.win_safe": "打开赛博保险箱 {n} 次",
    "goal.play_rounds": "任意游戏玩 {n} 局",
    "goal.duel": "打一场对决",
    "goal.bonus": "在农场领取每日肉排",
    "goal.craft": "在工坊里造点什么",
    "goal.raid": "发动一次突袭",
    "goal.market_deal": "在交易所完成一笔交易",
    "goal.donate": "向战队空间站投入资源",

    # ---------------- станция команды ----------------
    "st.header": (
        "🛰 <b>战队空间站「{team}」</b>\n"
        "..................................................\n"
        "等级：<b>{level}/{max}</b> → 每位队员农场产量 <b>+{percent}%</b>"
        "（每级 +{per_level}%）\n\n"
        "📦 距下一级：\n{progress}\n\n"
        "🧾 最近投入：\n{feed}\n\n"
        "🧰 你的资源：{stock}\n"
        "<i>空间站属于全队：大家一起建，人人享加成。退出战队——加成消失。</i>"
    ),
    "st.max_level": "🏁 空间站已建成——最高级！",
    "st.feed_empty": "还没有人投入——做第一个吧",
    "st.no_team": "🛰 空间站由战队共同建造。加入一支战队或创建自己的——一起来建。",
    "st.btn_find_team": "🏆 战队与公会",
    "st.btn_donate": "➕ {qty} {icon} {name}",
    "st.btn_donate_all": "➕ 全部：{qty} {icon} {name}",
    "st.btn_refresh": "🔄 刷新",
    "st.btn_team": "🏆 回到战队",
    "st.toast": "已投入 +{qty} {icon}",
    "st.level_up": "🛰 <b>战队空间站升到 {level} 级！</b>全体队员农场产量现在 +{percent}%。",
    "st.err_qty": "❌ 数量无效。",
    "st.err_no_team": "❌ 你不在任何战队。",
    "st.err_max": "🏁 空间站已建成（{max} 级）。",
    "st.err_resources": "🔒 资源不足：现有 {have}。",

    # ---------------- команды/кланы (основные поверхности) ----------------
    "clan.no_team": "⚠️ <b>你还没有自己的战队！</b>\n\n点按下方按钮，现在就注册属于你的队伍。",
    "clan.btn_create": "🏆 创建战队（10 万 🪙）",
    "clan.btn_members": "👥 队友名单",
    "clan.btn_leave": "🚪 离开战队 / 退出队伍",
    "clan.btn_dashboard": "🏆 战队仪表盘",
    "clan.status_clan": "👑 身份：帝国公会",
    "clan.status_team": "👥 身份：普通战队",
    "clan.dashboard": (
        "🏆 <b>你的战队信息仪表盘</b>\n"
        "..................................................\n"
        "📌 名称：<b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 队长：🧠{captain_level} · <b>{captain}</b>\n"
        "💬 口号：<i>「{motto}」</i>\n"
        "🔮 队徽符号：{symbol}\n\n"
        "👥 成员：<b>{members} / {max_members} 人</b>\n"
        "..................................................\n"
        "👇 <b>导航：</b>"
    ),
    "clan.members_only": "🔒 成员名单只有本战队成员才能查看！",
    "clan.members_gone": "❌ 该战队已经解散。",
    "clan.members_header": (
        "👥 <b>战队「{name}」成员名单</b>\n"
        "🧠 — 游戏智力等级（只能在 /quiz 中提升）\n"
        "..................................................\n"
    ),
    "clan.members_footer": (
        "\n..................................................\n"
        "📄 第 <b>{page} / {pages}</b> 页 · 总成员：<b>{members}</b>\n"
        "<i>点按队友的 @username 给对方发消息、拉个自己的群聊，"
        "带上全队参加团队比赛！</i>"
    ),
    "clan.btn_prev": "⬅️ 上一页",
    "clan.btn_next": "下一页 ➡️",
    "clan.join_ok": (
        "🎉 <b>恭喜，你入队了！</b>\n\n你已成功加入战队 <b>{name}</b>！\n"
        "📍 发送 /my_team 查看成员名单！"
    ),
    "clan.leave_ok": "🚪 你已退出战队 <b>{name}</b>。现在你是自由身啦！",
}

MINIAPP = {
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
    "subtitle": "一屏掌控你的游戏帝国",
    "tab_passport": "📋 护照",
    "tab_farm": "🚜 农场",
    "tab_goals": "🎯 目标",
    "tab_workshop": "🔧 工坊",
    "tab_raids": "🏴‍☠️ 突袭",
    "tab_market": "📈 交易所",
    "tab_team": "🏆 战队",
    "tab_shop": "🏪 商店",
    "tab_top": "👑 排行",
    "tab_friends": "🤝 好友",
    "passport": "📋 玩家护照",
    "coins": "🪙",
    "brain": "🧠 智力等级",
    "toNext": "距离 {n} 级：还需在竞答中答对 {left} 题（+{reward} 🪙）",
    "farm": "🚜 赛博农场",
    "robots": "机器人（矿工 / 钻机）",
    "intern": "实习机器人（每小时 1 🪙，永久）",
    "activateIntern": "🚀 激活实习机器人",
    "claimIntern": "🎁 领取实习机器人（{n}）",
    "internDone": "🤖 实习机器人上岗了！",
    "rank": "🎖 称号",
    "openFarm": "🏭 打开矿井",
    "farmScene": "🏭 你的农场",
    "back": "← 返回",
    "minedVisit": "本次访问已挖到",
    "unit_intern": "实习机器人",
    "unit_junior": "初级矿工",
    "unit_premium": "赛博钻机",
    "eternal": "永久",
    "fueledAll": "燃料充足",
    "fueledPart": "{b} 台中 {a} 台有燃料",
    "license": "30 天许可",
    "emptyFarm": "矿井空空如也。激活实习机器人，或去商店购买机器人！",
    "madeBy": "想为自己的项目做一个这样的机器人？联系 @mister_telebot",
    "fueled": "已装填的钻机",
    "speed": "挖矿速度",
    "perHour": "{v} 🪙/小时",
    "fridge": "冰箱",
    "inv": "仓库肉排",
    "burnout": "下次报废",
    "boosts": "生效中的强化",
    "none": "无",
    "resources": "🧰 资源",
    "bonusPct": "永久产量加成",
    "shuttle": "🚀 穿梭机已建成",
    "resHint": "每次获胜都会带来对应游戏的资源，开通无限畅玩则不受限制。在工坊里使用它们。",
    "bonusReady": "🎁 领取每日肉排",
    "bonusWait": "⏳ {h} 小时 {m} 分钟后可领",
    "bonusDone": "🎉 肉排已入仓库！",
    "team": "🏆 我的战队",
    "clan": "公会",
    "teamLabel": "战队",
    "captain": "👑 你是队长！",
    "members": "成员",
    "noTeam": "你还没有战队：从战队轮盘或搜索里加入一个——或者自己创建。",
    "tab_faq": "📚 FAQ",
    "tab_rules": "📜 协议",
    "tm_roulette": "🎲 战队轮盘",
    "tm_rotate": "🔄 换一批战队",
    "tm_noFree": "暂时没有空位战队——自己创建一个吧！",
    "tm_search": "🔍 搜索战队",
    "tm_searchPh": "战队名称或其中一部分",
    "tm_searchBtn": "搜索",
    "tm_notFound": "没有找到该名称的战队",
    "tm_join": "💥 加入",
    "tm_joined": "你已加入「{n}」！",
    "tm_create": "🏆 创建战队",
    "tm_hubHint": "最多 50 名成员的战队需要 {cost} 🪙。在商店里可升级为 1000 个席位的 超级公会。",
    "tm_name": "名称（最多 {n} 个字符）",
    "tm_motto": "口号（最多 {n} 个字符）",
    "tm_symbol": "队徽——一个表情（最多 {n} 个字符）",
    "tm_createBtn": "花 {cost} 🪙 创建",
    "tm_created": "战队「{n}」已创建——你是队长！",
    "tm_noMoney": "需要 {cost} 🪙，你有 {b} 🪙",
    "tm_roster": "👥 战队成员",
    "tm_mottoL": "💬 口号",
    "tm_leave": "🚪 退出战队",
    "tm_leaveAsk": "确定退出战队「{n}」吗？",
    "tm_leaveAskCaptain": "你是队长：队长之位将传给战队元老。确定退出「{n}」吗？",
    "tm_left": "你已不在战队中",
    "mk_scopePublic": "🌐 公共交易所",
    "mk_scopeTeam": "🏆 战队交易所",
    "mk_teamHint": "「{t}」战队交易所：只有队友能看到并购买这些挂单，手续费仅 {f}%。",
    "mk_yourStock": "📦 你拥有",
    "mk_yourCoins": "💰 你的金币",
    "tm_market": "🏪 战队交易所",
    "tm_marketBtn": "打开战队交易所",
    "tm_marketHint": "与队友交易：手续费 {f}%，公共交易所为 {p}%。超级公会仅 {c}%。",
    "hp_title": "🤝 互助",
    "hp_hint": "缺资源？向战队求助。每人每天最多可赠送 {d} 个资源。",
    "hp_today": "你今天已赠送：{g} / {d}",
    "hp_empty": "暂时没有人求助",
    "hp_give": "🎁 +{n}",
    "hp_kind": "需要什么",
    "hp_qty": "数量（最多 {n}）",
    "hp_ask": "🙏 请求支援",
    "hp_given": "已赠送：{q} {k}——感谢团队协作！",
    "hp_asked": "请求已发送给战队！",
    "tab_storage": "📦 仓库",
    "tab_mines": "⛏ 矿区",
    "tab_info": "📚 资讯",
    "tab_lab": "🔬 实验室",
    "as_stone": "石头",
    "as_wood": "木材",
    "as_fire": "火种",
    "as_energy": "电力",
    "as_battery": "电池",
    "as_cow": "奶牛",
    "as_core": "核心",
    "tool_1": "粗制工具",
    "tool_2": "精调工具",
    "tool_3": "校准仪器",
    "tool_4": "纳米技术",
    "tech_comm": "通讯",
    "tech_scout": "侦察",
    "tech_attack": "进攻",
    "tech_defense": "防御",
    "tech_science": "科研",
    "ws_needTool": "需要：{t}",
    "ws_teamItem": "🏆 战队道具——保护全队（超级公会价格 ×{x}）",
    "eff_make": "把原料加工成仓库里的材料",
    "eff_cart": "为马配马车：交易所 +1 个挂单位",
    "eff_meds": "突袭和矿区中不会生病",
    "it_meds": "急救包",
    "mk_lots": "已挂单：{o}/{m}（🐎 {h} · 🛒 {c}）",
    "badges": "🏅 赛季奖章",
    "sk_stable": "🐎 马厩",
    "sk_lots": "交易所挂单数：{n}",
    "sk_buyHorse": "🐎 花 {p} 🪙 买一匹马",
    "sk_stableHint": "每匹马让交易所 +1 个挂单位，每辆马车再 +1（马车数不超过马匹数）。买马花的金币会被销毁。",
    "sk_horseBought": "🐎 马厩里多了一匹马！交易所挂单位增加了。",
    "sk_shuttleCharge": "🚀 穿梭机电量",
    "sk_shuttleUntil": "🔋 穿梭机电量可用至 {t}",
    "sk_shuttleEmpty": "🪫 穿梭机没电了——交易所优惠暂停。",
    "sk_chargeBtn": "🔋 充电：1 块电池 = {d} 天",
    "raid_needTech": "突袭需要 1 级 📡 通讯、🔭 侦察和 ⚔️ 进攻。",
    "raid_toLab": "🔬 去实验室",
    "raid_scoutInfo": "侦察显示目标：{n}。突袭燃料是氢 💧",
    "raid_medsOn": "💊 急救包生效至 {t}：不怕生病",
    "raid_medsOff": "💊 没有急救包，15% 的战利品会损失在医务室",
    "raid_note_sick": "🤒 没有急救包：部分战利品损失在医务室",
    "mn_mined": "已开采 {n} {i}",
    "mn_left": "距开采结束：{t}",
    "mn_commNote": "收益只发给 1 级以上 📡 通讯的成员；没有 💊 急救包，每第 7 小时的产出会损失。",
    "top_season": "🏆 赛季",
    "top_rich": "💰 富豪榜",
    "top_seasonTitle": "🏆 赛季 {s}",
    "top_left": "距赛季结束：{t}",
    "top_myPlace": "你的名次：第 {p} 名，共 {n} 人 · 已赚 {e} 🪙",
    "top_noPlace": "你还不在榜上——玩几局就会上榜。",
    "top_prizes": "赛季奖励由主办方公布。前 10 名会在护照中获得赛季徽章。",
    "top_rules": "统计本月在游戏中赚到的金币：农场、胜利、对决、冒险任务、宝箱、出售。余额不会清零。",
    "top_players": "👤 赛季玩家",
    "top_teams": "🏆 赛季战队",
    "top_empty": "赛季刚刚开始——来当第一名吧！",
    "top_noTeams": "本赛季还没有对战。",
    "top_teamRules": "赛季战斗名次积分：10 · 7 · 5 · 4 · 3 · 2 · 1。",
    "lab_tools": "🧰 工具",
    "lab_toolsHint": "工具套装不会消耗——它们用来解锁高级配方和技术等级。",
    "lab_nextTool": "下一套：{t}",
    "lab_craftTool": "制作套装",
    "lab_toolsMax": "🧬 所有套装已制作完成！",
    "lab_level": "等级 {l}/{m}",
    "lab_max": "🏆 最高等级",
    "lab_wait": "⏳ {t}后可升下一级",
    "lab_up": "研究 {l} 级",
    "res_stone_src": "决斗、矿场、宝箱",
    "res_wood_src": "任务、矿场、宝箱",
    "res_fire_src": "工坊里的篝火",
    "res_energy_src": "每次获胜有几率、矿场、宝箱",
    "res_battery_src": "工坊",
    "res_cow_src": "任务、第 7 天宝箱、交易所",
    "res_core_src": "矿场和主办方奖励",
    "sk_items": "🧪 仓库中的物品：{n} / {m}（容量的 10%）",
    "sk_cutletsName": "赛博肉排",
    "it_total": "仓库中：{n} 件",
    "bt_entry": "🔋 战队报名：{n} / {m}",
    "bt_entered": "✅ 战队已参加矿区大作战",
    "bt_give": "投入 🔋（你有 {n}）",
    "bt_info": "只有已报名的战队才能争夺矿区：{f} 🔋，公会——{fc} 🔋。全队一起凑！",
    "bt_notAllowed": "这场大作战不适用于你的战队类型",
    "mn_place": "🏆 第 {p} 名奖励",
    "mn_soonShort": "开始：{d}",
    "top_events": "🎯 活动",
    "ev_empty": "目前没有活动——稍后再来看看！",
    "ev_my": "你的名次：{p}",
    "ev_noPlace": "你还没上榜——加油！",
    "ev_manual": "获奖者由主办方决定",
    "ev_places": "奖励名次：{n}",
    "ev_prizes": "🎁 奖品",
    "ev_leaders": "领先者",
    "lab_sciGate": "📚 当所有技术都研究到 {l} 级时，开放第 {l} 级",
    "lab_cooldown": "研究完成后，{d} 天后开放下一级。",
    "lab_done": "🔬 完成！等级 {l}",
    "lab_eff_comm": "1 级——开启突袭和矿区收益；之后每升一级，突袭冷却 −{c} 分钟",
    "lab_eff_scout": "没有它就无法突袭；侦察目标数：2 + 等级",
    "lab_eff_attack": "没有它就无法突袭；第 1 级之后每级战利品 +{a}%",
    "lab_eff_defense": "每级使突袭者从你这里拿走的战利品 −{d}%",
    "lab_eff_science": "每级农场产量和战利品 +{s}%。研究耗时长，且需要 ☢️ 核心",
    "lab_how": "📖 玩法说明",
    "lab_rule1": "工具套装只需制作一次：⚒️ → 🛠 → 🔬 → 🧬。没有对应套装，就无法获得高级配方或等级。",
    "lab_rule2": "研究完一级后，同一技术的下一级正好 30 天后开放——每次升级都很珍贵。科学跟随其他技术成长。",
    "lab_rule3": "☢️ 核心只能靠战队获得：对战的获奖名次，以及占领矿区满一天。",
    "durDH": "{d} 天 {h} 时",
    "durHM": "{h} 时 {m} 分",
    "durM": "{m} 分",
    "ws_locked": "🔒 {t}后解锁",
    "ws_toStorage": "📦 成品会存入仓库",
    "eff_camo": "突袭侦察看不到你，但你仍可发动突袭",
    "eff_trap": "突袭失败的人会多给你一倍",
    "eff_drill": "防守平局算突袭者失败",
    "eff_thermos": "钻机吃肉排的速度慢 25%",
    "eff_banner": "全战队产量 +5%",
    "eff_dome": "全战队获得突袭护盾",
    "eff_forsage": "跳过突袭冷却（每天一次）",
    "eff_economizer": "下次出击不消耗氢气",
    "eff_cargo": "下次突袭战利品 ×1.5",
    "eff_stamp": "下次交易所出售免手续费",
    "it_camo": "伪装",
    "it_trap": "诱饵",
    "it_drill": "姿态训练器",
    "it_thermos": "肉排保温壶",
    "it_banner": "战队旗帜",
    "it_dome": "战队穹顶",
    "it_forsage": "飞船加力",
    "it_economizer": "节能器",
    "it_cargo": "扩容货舱",
    "it_stamp": "交易所印章",
    "it_oneShot": "一次性",
    "it_charges": "⚡ 已充能：{n}",
    "it_needTeam": "战队道具——需要先加入战队。",
    "it_charged": "⚡ 已充能！下次行动时触发。",
    "it_forsaged": "🔥 冷却已跳过——可以出击了！",
    "raid_armed": "⚡ 待命：{l}",
    "raid_guardUntil": "{n}，至 {t}",
    "raid_domeOn": "🛡 战队穹顶生效至 {t}",
    "raid_forsageBtn": "🔥 加力：跳过冷却（{n}）",
    "raid_note_economizer": "⛽ 节能器：出击不耗氢气",
    "raid_note_cargo": "📦 货舱：战利品 ×1.5",
    "raid_note_trap": "🪤 目标有诱饵：你要多给一倍",
    "raid_note_drill": "🎯 目标有姿态训练器：平局算你失败",
    "mn_title": "⛏ 矿区地图",
    "mn_closed": "🔒 战队或联盟对战开始前，无法进攻矿区。",
    "mn_pick": "点按矿区查看详情。",
    "mn_info": "⛏ 矿区",
    "mn_battle": "⚔️ 对战「{t}」争夺 {n} 号矿区",
    "mn_soon": "⏳ 对战「{t}」争夺 {n} 号矿区——{d} 开始",
    "mn_nom": "项目：{n}",
    "mn_ends": "结束：{d}",
    "mn_leaders": "当前领先",
    "mn_noLeaders": "还没有人得分——你的战队可以拔得头筹！",
    "mn_myTeam": "🏆 你的战队矿区",
    "mn_income": "产出：全战队每小时 {n} 个资源",
    "mn_noIncome": "暂无矿区——赢下战队对战，矿区归你 72 小时。",
    "mn_noTeam": "矿区只有战队才能占领——加入战队或创建自己的战队。",
    "mn_teamBtn": "🏆 前往战队",
    "mn_how": "📖 玩法说明",
    "mn_rule1": "每场战队或联盟对战只争夺一座矿区。在对战项目中，全体成员总成绩最好的战队获胜。",
    "mn_rule2": "获胜者占有矿区 {h} 小时：战队每位成员每小时获得 {y} 个该矿区资源。成员越多，产出越多。",
    "mn_rule3": "之后矿区重新空出，但只能通过新的对战夺取。",
    "mn_name": "⛏ {n} 号矿区",
    "mn_res": "资源",
    "mn_holder": "持有者",
    "mn_free": "空闲",
    "mn_untilL": "占有至",
    "mn_pumping": "产出：每小时 {n} {i}",
    "mn_targetOf": "⚔️ 对战「{t}」正在争夺这座矿区",
    "mn_closedOne": "🔒 只能通过战队对战夺取——请留意公告。",
    "raid_noFuel": "⛽ 飞船无法起飞——需要燃料",
    "raid_shieldTitle": "🛡 突袭护盾",
    "raid_shieldActive": "生效中",
    "raid_shieldInactive": "未生效",
    "raid_shieldHint": "护盾生效期间，没人能突袭你。护盾在工坊建造后会存入仓库——需要时再启用。",
    "raid_toStorage": "📦 打开仓库",
    "sk_res": "📦 仓库资源",
    "sk_expand": "🔧 扩建仓库",
    "sk_cutlets": "🥩 赛博肉排",
    "sk_cutletsHint": "赛博钻机的燃料：1 块肉排 = 工作一天。",
    "sk_refuel": "🚜 去农场加料",
    "it_nitrogen": "液氮冷却 +40%",
    "it_nuclear": "核能加速 X5",
    "it_drone": "大师无人机",
    "it_shield": "突袭护盾",
    "it_unlimit": "解除上限",
    "it_unlimitDesc": "游戏获胜不受每日次数限制",
    "it_hours": "{h} 小时",
    "it_use": "启用",
    "it_empty": "空空如也。去工坊建造——成品会存到这里。",
    "it_toWorkshop": "🔧 去工坊",
    "it_active": "✅ 生效至 {t}",
    "it_used": "✅ 已启用！生效至 {t}",
    "it_stored": "📦 完成！成品已存入仓库——需要时到「仓库」页启用。",
    "sk_shuttle": "🚀 穿梭机",
    "sk_shuttleOn": "已拥有：交易所手续费 {f}%，订单上限更高。",
    "sk_shuttleOff": "尚未拥有。可在工坊建造。",
    "sk_armor": "🦾 赛博装甲",
    "sk_armorOn": "等级 {l}/{m}：产量 +{p}%，有效期至 {t}。",
    "sk_armorOff": "未穿戴。每级可使产量 +{p}%，持续 30 天。",
    "sk_store": "🏗 仓库扩建",
    "sk_storeLvl": "容量：每种资源 {c}。",
    "sk_storeMax": "🏆 仓库已达最大容量！",
    "hp_who": "智力等级达到 {l} 且已领取 {c} 次每日肉排的玩家才能赠送。",
    "top": "👑 生态系统富豪榜 TOP-100",
    "shop": "🏪 商店",
    "shopFarm": "🚜 农场专区",
    "shopGames": "🕹️ 游戏专区",
    "shopHint": "使用官方 Telegram Stars 付款——就在这里，一键搞定。",
    "paid": "🎉 已付款！商品已发放到你的账户。",
    "payFail": "付款没有成功。再试一次吧。",
    "oldClient": "请更新 Telegram 以便在应用内购买，或在机器人聊天里打开商店。",
    "ctaNoRobots": "💤 农场几乎空了！添置更强的机器人——🪙 就会全天候入账。",
    "ctaHungry": "🚨 钻机在挨饿（{n} 台没燃料）——挖矿停了！",
    "ctaLowFuel": "⚠️ 肉排不够钻机工作一天了。",
    "ctaShopBtn": "🛒 去商店",
    "footer": "The whole game in one app",
    "noProfile": "未找到个人资料。打开机器人并点按 /start！",
    "blocked": "账号已被管理员封禁。",
    "deleting": "账号正在排队删除。改变主意了？请在机器人聊天中取消删除。",
    "error": "数据加载失败。稍后再试。",
    "outside": "请从 ROFL HUB 的 Telegram 机器人打开此应用。",
    "robotsTitle": "🤖 你的机器人",
    "buyMore": "🛒 购买",
    "rateShort": "{v} 🪙/小时",
    "refuelOne": "🥩 加 1 份",
    "refuelAll": "⚡ 全部加满",
    "refueled": "已加注：{n} 🥩",
    "res_metal_src": "石头剪刀布",
    "res_hydrogen_src": "比大小",
    "res_crystal_src": "竞答",
    "res_parts_src": "赛博保险箱",
    "resWhere": "获取途径",
    "ws_title": "🔧 工坊",
    "ws_hint": "游戏里的资源可以变成强化。资源够了就点「制造」。",
    "ws_craft": "制造",
    "ws_owned": "✅ 已拥有",
    "ws_crafted": "完成！强化已经生效。",
    "ws_armor": "🛡 赛博装甲",
    "ws_armorLvl": "等级 {l}/{m} · 每级 +{p}%，有效期 30 天",
    "ws_shuttleOn": "🚀 穿梭机已建成：交易所手续费 {fee}%",
    "ws_shuttleOff": "🚀 尚未建成穿梭机：交易所手续费 {fee}%",
    "eff_nitrogen": "所有机器人产量 +40%",
    "eff_nuclear": "产量 ×5，钻机吃肉排 ×3",
    "eff_drone": "机器人不会老化",
    "eff_shield": "没人能突袭你",
    "eff_cutlet": "1 份赛博肉排入仓库（较贵：商店里的燃料更划算）",
    "eff_armor": "每级产量 +10%，有效期 30 天",
    "eff_shuttle": "只属于你：你出售时手续费 5%，挂单最多 500 份肉排——永久",
    "eff_storage": "资源空间更大——永久",
    "ref_title": "🤝 邀请好友",
    "ref_rules": "每位活跃好友 {q}，仅一次。活跃好友是指达到 {l} 级智力等级、并领取过 {c} 次每日肉排的人。",
    "ref_copy": "📋 复制",
    "ref_copied": "链接已复制！",
    "ref_share": "📤 分享",
    "ref_stats": "📊 你的人脉",
    "ref_invited": "已邀请",
    "ref_qualified": "活跃",
    "ref_earned": "已赚取",
    "ref_top": "🏆 谁的好友最多",
    "ref_topHint": "✅ — 活跃好友，👥 — 全部受邀者",
    "ref_empty": "排行榜还是空的——快来当第一名！",
    "wk_title": "🔥 本周配方",
    "wk_hint": "限时配方：由中心决定上架，随后消失。抓紧合成！",
    "wk_left": "本周剩余合成次数：{n} / {m}",
    "st_cap": "📦 仓库：每种资源最多 {c}——多出的产出会丢失",
    "raid_title": "🏴‍☠️ 突袭",
    "raid_how": "📖 玩法说明",
    "raid_rule1": "你选择手势，目标事先设好了防御姿态。胜负由石头剪刀布决定：这是决策的较量，不是抽奖。",
    "raid_rule2": "获胜：拿走目标每种资源的 {pct}%，每种最多 {cap}。失败：把自己的 {fpct}% 交给目标，最多 {fcap}。平局：燃料白烧了。",
    "raid_rule3": "只能掠夺资源。金币、机器人和肉排绝对安全。新手有 {days} 天保护期，队友不能突袭。",
    "raid_rule4": "出击消耗 {fuel} 💧 氢气，下一次要等 {cd} 小时。如果有人突袭你，{rh} 小时内可免费复仇。",
    "raid_fuel": "💧 氢气",
    "raid_ready": "🚀 飞船准备出击",
    "raid_cooldown": "⏳ 冷却中：{m} 分钟",
    "raid_shieldOn": "🛡 护盾有效至 {t}",
    "raid_shieldNewbie": "🛡 新手保护",
    "raid_shieldOff": "🛡 没有护盾——去工坊制造一个",
    "raid_stance": "✊ 你的防御姿态",
    "raid_stanceHint": "它用来迎接别人的突袭。时不时换一换——太好猜的人更容易被抢。",
    "raid_stanceNone": "未选择姿态——将随机出招",
    "raid_stanceSaved": "姿态已保存",
    "raid_stats": "突袭：{a} 次（成功 {w}）· 守住：{h}/{d}",
    "raid_scout": "🔭 侦察：寻找目标",
    "raid_targets": "🎯 选择目标",
    "raid_res": "资源 ≈{n}",
    "raid_noTargets": "现在没有合适的目标：护盾、冷却、新手保护。稍后再来看看。",
    "raid_pickMove": "✊ 你的手势 vs {name} 的姿态",
    "raid_revenge": "⚔️ 复仇战",
    "raid_revengeBtn": "⚔️ 反击：{name}",
    "raid_win": "🏴‍☠️ 突袭成功！",
    "raid_draw": "😐 平局——飞船空手而归",
    "raid_lose": "💥 对方守住了",
    "raid_vs": "{m} 对 {s}",
    "raid_loot": "战利品：{l}",
    "raid_lost": "交给目标：{l}",
    "rock": "🪨 石头",
    "scissors": "✂️ 剪刀",
    "paper": "📄 布",
    "mk_title": "📈 交易所",
    "mk_stats": "挂单：{o} · 肉排：{c} · 最低价：{b} 🪙",
    "mk_feeLine": "每笔成交销毁 {f}% 手续费——抵御通胀",
    "mk_inv": "🥩 你的仓库：{n}",
    "mk_offers": "🛒 在售挂单",
    "mk_empty": "还没有挂单——来当第一个卖家吧！",
    "mk_offer": "{q} 🥩 × {p} 🪙",
    "mk_buyHow": "买多少？",
    "mk_all": "全部 {q}",
    "mk_sellTitle": "💰 出售肉排",
    "mk_qty": "肉排数量",
    "mk_price": "单价，🪙",
    "mk_preview": "成交 {t} 🪙 · 你得 {g} 🪙 · 销毁 {f} 🪙",
    "mk_sell": "挂到交易所",
    "mk_limits": "每单最多 {q} 份肉排，最多 {o} 个挂单",
    "mk_my": "📋 我的挂单",
    "mk_cancel": "撤回",
    "mk_bought": "已用 {t} 🪙 买入 {q} 🥩",
    "mk_listed": "挂单已上架！成交后会通知你。",
    "mk_cancelledMsg": "挂单已撤回，肉排已回到仓库",
    "as_cutlet": "肉排",
    "as_metal": "金属",
    "as_hydrogen": "氢气",
    "as_crystal": "晶体",
    "as_parts": "零件",
    "mk_index": "📈 交易所指数",
    "mk_chart": "📊 7 天价格",
    "mk_noTrades": "还没有成交——来做第一笔吧！",
    "mk_avg": "本周均价：{p} 🪙 · 成交量：{v}",
    "mk_asks": "🛒 出售中",
    "mk_bids": "🙋 求购中",
    "mk_noBids": "还没有求购单",
    "mk_sellTo": "卖出",
    "mk_sellHow": "卖多少？",
    "mk_bidTitle": "🙋 求购单",
    "mk_bidHint": "金币会冻结在求购单里直到成交。撤回求购单，金币就会退回。",
    "mk_bid": "发布求购单",
    "mk_bidPreview": "将冻结 {t} 🪙",
    "mk_have": "你有：{n}",
    "mk_floor": "每块肉排不低于 {p} 🪙：用星星在商店买燃料永远更划算",
    "mk_side_sell": "出售",
    "mk_side_buy": "求购",
    "mk_listedBid": "求购单已发布！金币已冻结至成交。",
    "mk_sold": "已售出 {q}，扣除手续费后获得 {g} 🪙",
    "mk_shuttleNote": "🚀 你的穿梭机：你出售时手续费 {f}%",
    "sw_title": "🔄 资源交换",
    "sw_hint": "拿出多余的，换来需要的。不用金币，没有手续费。",
    "sw_give": "你付出",
    "sw_want": "你想要",
    "sw_qty": "数量",
    "sw_create": "发起交换",
    "sw_take": "交换",
    "shop_info": "ℹ️ 各商品有什么用",
    "sw_youGet": "你得到",
    "sw_youGive": "你需付出",
    "sw_takeBtn": "交换——付出 {x}",
    "sw_mineLine": "你付出 {g} → 想要 {w}",
    "sw_qtyErr": "两个数量都需大于零",
    "sw_empty": "还没有交换提议",
    "sw_mine": "我的提议",
    "sw_done": "交换完成！",
    "sw_created": "提议已发布，资源已预留",
    "sw_cancelled": "提议已撤回，资源已退回",
    "ws_armorUntil": "🛡 装甲有效期至 {t}",
    "st_title": "🛰 战队空间站",
    "st_level": "等级 {l} / {m}",
    "st_bonus": "每位成员产量 +{p}%",
    "st_next": "升到 {n} 级需要每种资源各 {c}",
    "st_max": "🏁 空间站已建成！",
    "st_feed": "🧾 最近的捐献",
    "st_feedEmpty": "还没有人捐献——来当第一个吧",
    "st_donate": "捐献",
    "st_all": "全部",
    "st_done": "已捐献！",
    "st_hint": "全队一起建造，人人享受加成。退出战队——加成就没了。",
    "st_off": "空间站暂时在维护中",
    "goals_title": "🎯 今日目标",
    "goals_chest": "🎁 完成全部三项的宝箱：+{c} 🪙 和 +{r} 随机资源",
    "goals_streak": "🔥 连续：{s} 天 · 每连续第 {e} 天额外 +{b} 🪙",
    "goals_claim": "🎁 领取宝箱",
    "goals_claimed": "🎁 今天的宝箱已领取。明天有新目标！",
    "goals_reset": "目标在 00:00 UTC 刷新",
    "goals_got": "🎁 +{c} 🪙 · +{q} {n} · 连续 {s} 天",
    "featureOff": "⚙️ 该板块正在维护中",
    "done": "完成！",
    "loading": "⏳ 加载中…",
}

COMMANDS = {
    "app": "🎮 打开 Mini App",
    "menu": "📱 主菜单",
    "profile": "👤 我的资料与护照",
    "farm": "🚜 赛博农场与燃料补给",
    "shop": "🏪 商店（Telegram Stars）",
    "games": "🕹️ 对战机器人的所有游戏",
    "quiz": "🧠 竞答：15 秒作答",
    "duel": "⚔️ 1对1 押注对决",
    "quests": "🗺️ 冒险任务：互动分支故事",
    "my_team": "🏆 我的战队与队友",
    "invite": "🤝 邀请链接：每位活跃好友 +500",
    "transfer": "🔄 给玩家转账金币",
    "market": "📈 肉排交易所：买入或卖出",
    "sell": "💰 出售肉排：/sell 数量 价格",
    "my_stats": "📊 我的统计",
    "faq": "📚 常见问题",
    "rules": "📜 用户协议",
    "paysupport": "🛟 付款支持",
    "workshop": "🔧 工坊：资源换强化",
    "raid": "🏴‍☠️ 突袭：侦察与复仇战",
    "goals": "🎯 每日目标与宝箱",
    "station": "🛰 战队空间站：共同项目",
}
