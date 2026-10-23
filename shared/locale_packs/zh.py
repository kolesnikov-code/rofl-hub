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
        "- 益智娱乐频道 ROFL HUB CHANNEL\n"
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
        "..................................................\n\n"
        "👤 <b>个人资料与护照：</b>\n"
        "• /start — 开始了解并注册账号\n"
        "• /profile — 你的护照、余额和战队实时信息\n"
        "• /my_stats — 你最近 30 天的历史统计\n\n"
        "🚜 <b>赛博农场与自动化：</b>\n"
        "• /farm — 燃料中心：加油与机器人产出速度\n"
        "• /shop — 交易市场：购买矿工、肉排和中心升级\n\n"
        "🕹️ <b>游戏室：</b>\n"
        "• /games — 所有对战机器人游戏的快捷中心\n"
        "• /quiz — 限时竞答：15 秒作答，等级与奖励\n"
        "• /duel — 与真人玩家 1对1 对决：10/100/1000 🪙 桌\n"
        "• /quests — 冒险任务：侦探、喜剧和谜题，通关有奖\n"
        "• /rps, /high_low, /safe — 赚金币的快速小游戏\n\n"
        "👥 <b>战队管理：</b>\n"
        "• /create_team — 花 10 万 🪙 注册自己的战队\n"
        "• /my_team — 战队仪表盘和带 🧠 等级的队友名单\n"
        "• /all_teams — 随机战队轮盘\n\n"
        "💸 <b>金钱与朋友：</b>\n"
        "• /invite — 你的邀请链接：每位好友 +1000 🪙\n"
        "• /transfer — 给其他玩家转账金币\n\n"
        "📚 <b>帮助与规则：</b>\n"
        "• /faq — 完整生态系统指南（在 Mini App 中打开）\n"
        "• /rules — 用户协议\n"
        "..................................................\n"
        "<i>⚙️ 使用屏幕底部常驻的双列游戏面板，在各版块间瞬间切换！</i>"
    ),
    "menu.games_hub": (
        "🕹️ <b>欢迎来到 ROFL HUB 游戏区！</b>\n"
        "..................................................\n\n"
        "在这里你可以和机器人快速过招，或挑战智力冲刺测验，"
        "赢个盆满钵满——或者输个精光！\n\n"
        "💸 获胜奖励：<b>+2 🪙</b>（赛博保险箱：<b>+5</b>）\n"
        "💀 失败或平局扣除：<b>-1 🪙</b>\n"
        "🧠 竞答有 15 秒倒计时和智力等级：1 级需要答对 10 题，奖励 <b>+100 🪙</b>，"
        "之后每级多 10 题，但奖励也每级多 100！\n\n"
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
        "..................................................\n\n"
        "重点速览：\n"
        "🚜 机器人全天候挖金币：初级矿工——每小时 5 枚、免燃料；"
        "赛博钻机——每小时 10 枚，而且每台钻机每天要吃掉自己的 1 份赛博肉排。"
        "所有机器人寿命 30 天（大师无人机可暂停损耗）。\n"
        "🧠 竞答：15 秒作答，智力等级越高奖励越高。\n"
        "⚔️ 在 10/100/1000 🪙 的桌上与真人玩家对决。\n"
        "🏆 战队最多 50 名成员（超级公会——最多 1000），还有人人有奖的大作战活动。\n\n"
        "..................................................\n"
        "👇 <b>包含全部机制的完整指南——点按按钮：</b>"
    ),
    "faq.btn_open": "📖 打开完整指南",
    "rules.teaser": (
        "📜 <b>ROFL HUB 用户协议</b>\n"
        "..................................................\n\n"
        "要点一览：\n"
        "🪙 金币和所有游戏物品都是虚拟娱乐元素："
        "它们不是货币，也不能兑换成真实资金。\n"
        "💫 购买仅通过官方 Telegram Stars 进行；数字商品即时送达，"
        "若发货失败，Stars 将自动退回。\n"
        "🛡️ 我们不收集手机号、地理位置和个人数据。\n"
        "🤝 禁止辱骂、刷分和多开账号——违规可能导致封禁。\n\n"
        "..................................................\n"
        "👇 <b>完整协议文本与免责声明——点按按钮：</b>\n"
        "<i>⚖️ 使用本机器人即表示你同意这些条款。</i>"
    ),
    "rules.btn_open": "📜 打开完整协议",
    "quest.list_header": (
        "🗺️ <b>ROFL HUB 冒险任务</b>\n"
        "..................................................\n\n"
        "带有选择和分支的互动故事：侦探、喜剧、谜题。"
        "每个任务的首次通关都能赢得金币，而且想重玩多少次都行！\n"
        "🌐 <i>任务故事暂时为俄语——翻译版即将推出。</i>\n\n"
        "👇 <b>选择一个故事：</b>"
    ),
    "quest.card": (
        "{title}\n"
        "🎭 {genre} · ⏱ {minutes} 分钟 · 🏆 首次通关 +{reward} 🪙\n"
        "..................................................\n\n"
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
    "farm.intern_line": "• 实习机器人（每小时 {rate} 🪙，永久）：<code>{count} 台</code>\n",
    "farm.intern_hint": "🎁 你有一台免费的实习机器人！点下方按钮，它将永久每小时挖 1 🪙。",
    "farm.dashboard": (
        "🚜 <b>ROFL HUB 中央燃料中心</b>\n"
        "..................................................\n\n"
        "🤖 工厂里的在役机器人：<b>{total} 台</b>\n"
        "{intern}• 初级矿工（每小时 {junior_rate} 🪙）：<code>{junior} 台</code>\n"
        "• 赛博钻机（每小时 {premium_rate} 🪙）：<code>{premium} 台</code>\n"
        "{burnout}\n"
        "📊 <b>你农场的当前速度：</b>\n"
        "• 每小时产出：<b>+{speed_hour} 🪙</b>\n"
        "• 每天产出：<b>+{speed_day} 🪙</b>\n\n"
        "⚡ <b>强化：</b>\n{boosts}\n\n"
        "📋 <b>游戏工厂状态：</b>\n"
        "{status}\n\n"
        "..................................................\n\n"
        "📦 <b>自动冰箱状态：</b>\n"
        "🥩 燃料储备：<b>{fridge} / {capacity} 份</b>\n"
        "💼 仓库里的肉排：<code>{inv} 份</code>\n\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
        "🆔 你的护照 ID：<code>{user_id}</code>\n"
        "{vip}"
        "💰 当前余额：<b>{balance} 🪙</b>\n"
        "🏆 你的身份：<b>{team}</b>\n"
        "🧠 智力等级：<b>{level}</b> · 距离 {next_level} 级：还需在 /quiz 中答对 "
        "<b>{left}</b> 题（奖励：+{reward} 🪙）\n\n"
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
        "..................................................\n\n"
        "🧠 游戏智力等级：<b>{level}</b>（累计正确回答：{total}）\n"
        "🎮 对决场次：<b>{played} 局</b>\n"
        "🏆 击败对手次数：<code>{won} 次</code>\n"
        "👥 邀请的活跃好友：<b>{refs} 人</b>\n\n"
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
        "⚡ 解除上限：24 小时 5 ★，30 天 99 ★（/shop 的「游戏专区」）。"
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
        "..................................................\n\n"
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
    "rank.dead": "DEAD",

    # ---------------- рефералка ----------------
    "ref.text": (
        "🤝 <b>ROFL HUB 邀请计划</b>\n"
        "..................................................\n\n"
        "邀请好友，每有一人通过你的专属链接注册，"
        "你就能获得 <b>+{bonus} 🪙</b>！\n\n"
        "🔗 <b>你的链接（点按复制）：</b>\n<code>{link}</code>\n\n"
        "📊 <b>你的统计：</b>\n"
        "👥 已邀请好友：<b>{invited} 人</b>\n"
        "💰 邀请奖励累计：<b>{earned} 🪙</b>\n\n"
        "..................................................\n"
        "<i>把链接发到班级群、朋友圈和社交网络——队伍越大，你的余额涨得越快！</i>"
    ),
    "ref.btn_share": "📣 分享链接",
    "ref.share_text": "快来加入 ROFL HUB 游戏生态系统！",
    "ref.qualified_line": "⭐ <b>双重奖励：</b>受邀好友玩满 {rounds} 局后，你再得 <b>+{bonus} 🪙</b>！",
    "ref.qualified_notify": ("🤝 <b>你的好友玩上瘾了：已经 {rounds} 局！</b>\n"
                             "合格推荐奖励 <b>+{bonus} 🪙</b> 已到账。继续邀请吧！"),

    # ---------------- переводы ----------------
    "tr.help": (
        "🔄 <b>给其他玩家转账金币</b>\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
        "ROFL HUB 的所有商品均为数字商品，付款后即时送达。\n\n"
        "⚙️ <b>如果付款成功但商品没有到账：</b>\n"
        "发货失败时，机器人会自动退回 Stars。如果没有退回——"
        "请把付款编号发到这里（在收据里，格式为 <code>xxxx...</code>）并描述问题。"
        "管理员会在数据库中核对付款，并在 24 小时内解决。\n\n"
        "💫 <b>退款政策：</b>\n"
        "若商品未收到或发放有误，可以退款。"
        "已正确送达的数字商品不支持退款。\n\n"
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
    "dlv.err_intern_refs": "升级需要 {need} 位合格好友（各玩 30 局），你目前有 {have} 位。",
    "mk.header": "📈 <b>肉饼交易所</b>\n..................................................\n\n挂单：<b>{orders}</b> · 在售肉饼：<b>{cutlets}</b> · 最低价：<b>{best}</b>\n平台手续费：每笔成交 <b>{fee}%</b>（销毁——抗通胀）\n🥩 你仓库里的肉饼：<b>{inv}</b>\n\n{body}\n\n<i>点击挂单即可购买。出售请用 /sell。</i>",
    "mk.empty": "暂时没有挂单。抢先出售：/sell 数量 价格",
    "mk.order_line": "🥩 #{id} · <b>{qty} 块</b>，单价 <b>{price}</b> 🪙",
    "mk.btn_order": "🛒 #{id}：{qty} 块，单价 {price} 🪙",
    "mk.btn_my": "📋 我的挂单",
    "mk.btn_sell_help": "💰 如何出售肉饼",
    "mk.btn_refresh": "🔄 刷新",
    "mk.btn_back": "← 返回交易所",
    "mk.pick": "🛒 <b>挂单 #{id}</b>：可买 {qty} 块，单价 {price} 🪙。\n买几块？",
    "mk.btn_qty": "{qty} 块 — {total} 🪙",
    "mk.btn_qty_all": "全部 {qty} 块 — {total} 🪙",
    "mk.buy_toast": "成交！",
    "mk.buy_done": "✅ 以 <b>{total} 🪙</b> 买入 <b>{qty} 块肉饼</b>，已入仓库——快给钻机加燃料！",
    "mk.sold_notify": "💰 <b>交易所：已售出！</b> 挂单 #{id}：售出 {qty} 块，单价 {price}。你收到 <b>+{got} 🪙</b>（手续费 {fee} 已销毁）。",
    "mk.sell_help": "💰 <b>如何出售肉饼</b>\n\n命令：<code>/sell 数量 价格</code>\n示例：<code>/sell 10 50</code> —— 10 块肉饼，每块 50 🪙。\n\n肉饼从仓库转入挂单等待买家（随时可撤回）。每单最多 {max_qty} 块，最多 {max_orders} 个挂单。成交时销毁 {fee}% 手续费。",
    "mk.sell_confirm": "📝 以单价 <b>{price}</b> 🪙挂出 <b>{qty} 块肉饼</b>？\n总额 {total} · 手续费 {fee} 将销毁 · 你将收到 <b>{got} 🪙</b>。",
    "mk.btn_confirm_sell": "✅ 挂到交易所",
    "mk.btn_cancel": "❌ 取消",
    "mk.sell_toast": "挂单成功！",
    "mk.sell_done": "✅ 挂单 <b>#{id}</b> 已上架：{qty} 块，单价 {price} 🪙。成交后会通知你。",
    "mk.cancelled_toast": "已取消",
    "mk.cancel_text": "❌ <b>已取消。</b> 肉饼仍在仓库。",
    "mk.my_header": "📋 <b>你的挂单</b>\n\n",
    "mk.my_line": "🥩 #{id} · {qty} 块，单价 {price} 🪙",
    "mk.my_empty": "📋 你没有未成交的挂单。",
    "mk.btn_cancel_order": "❌ 撤回挂单 #{id}",
    "mk.order_cancelled": "↩️ 挂单 #{id} 已撤回：<b>{qty} 块肉饼</b>已返回仓库。",
    "mk.err_qty": "❌ 数量：每单 1 到 {max} 块。",
    "mk.err_price": "❌ 价格：每块 {min} 到 {max} 🪙。",
    "mk.err_no_cutlets": "❌ 仓库里只有 {have} 块肉饼。冰箱里的肉饼不能上架——见 /farm。",
    "mk.err_too_many": "❌ 上限：最多 {max} 个挂单。请在「我的挂单」中撤回一个。",
    "mk.err_not_found": "❌ 该挂单已关闭。",
    "mk.err_own": "🤨 不能购买自己的挂单。",
    "mk.err_insufficient": "❌ 余额不足：需要 {total} 🪙。",
    "farm.btn_market": "📈 肉饼交易所",

    # ---------------- ресурсы (волна 22.10, вечер) ----------------
    "res.metal": "金属",
    "res.hydrogen": "氢气",
    "res.crystal": "晶体",
    "res.parts": "零件",
    "res.none": "暂时为空",
    "games.resource_gain": "{icon} 获得资源：<b>+{qty} {name}</b>（共 {total}）→ /workshop",
    "duel.metal_gain": "⛏ 对决战利品：<b>+{metal} 金属</b> → /workshop",
    "quest.win_resources": "\n📦 另有一套资源：每种 <b>{qty}</b> → /workshop",
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
    "farm.boost_armor": "🛡 赛博装甲 {level} 级：产量永久 +{percent}%",
    "farm.boost_station": "🛰 战队空间站 {level} 级：产量 +{percent}%",
    "clan.btn_station": "🛰 战队空间站",

    # ---------------- мастерская ----------------
    "ws.header": (
        "🔧 <b>工坊</b>\n"
        "..................................................\n\n"
        "🧰 你的资源：{stock}\n"
        "⛏ 金属——石头剪刀布与对决 · 💧 氢气——比大小 · "
        "💎 晶体——竞答 · ⚙️ 零件——赛博保险箱。冒险任务送一整套。\n\n"
        "🛡 赛博装甲：<b>{armor}/{armor_max} 级</b>（每级产量永久 +{armor_pct}%）\n"
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
    "ws.done_armor": "🛡 <b>赛博装甲 {level} 级！</b>农场产量：永久 <b>+{percent}%</b>。",
    "ws.done_shuttle": "🚀 <b>穿梭机建成！</b>交易所手续费降为 {fee}%，每单最多 {qty} 份肉排。永久有效。",
    "ws.err_unknown": "❌ 没有这个配方。",
    "ws.err_resources": "🔒 资源不足：{kind} 需要 {need}，现有 {have}。去游戏里挖吧！",
    "ws.err_shuttle_owned": "🚀 穿梭机已建成——每位玩家只能有一艘。",
    "ws.err_armor_max": "🛡 装甲已达最高级（{max}）。",

    # ---------------- налёты ----------------
    "raid.header": (
        "🏴‍☠️ <b>突袭</b>\n"
        "..................................................\n\n"
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
        "..................................................\n\n"
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
        "..................................................\n\n"
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
        "..................................................\n\n"
        "📌 名称：<b>{name}</b>\n"
        "⚡ {status}\n"
        "👤 队长：🧠{captain_level} · <b>{captain}</b>\n"
        "💬 口号：<i>「{motto}」</i>\n"
        "🔮 队徽符号：{symbol}\n\n"
        "👥 成员：<b>{members} / {max_members} 人</b>\n"
        "..................................................\n\n"
        "👇 <b>导航：</b>"
    ),
    "clan.members_only": "🔒 成员名单只有本战队成员才能查看！",
    "clan.members_gone": "❌ 该战队已经解散。",
    "clan.members_header": (
        "👥 <b>战队「{name}」成员名单</b>\n"
        "🧠 — 游戏智力等级（只能在 /quiz 中提升）\n"
        "..................................................\n\n"
    ),
    "clan.members_footer": (
        "\n\n..................................................\n"
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
    "passport": "📋 玩家护照",
    "coins": "🪙",
    "brain": "🧠 智力等级",
    "toNext": "距离 {n} 级：还需在竞答中答对 {left} 题（+{reward} 🪙）",
    "farm": "🚜 赛博农场",
    "robots": "机器人（矿工 / 钻机）",
    "intern": "实习机器人（每小时 1 🪙，永久）",
    "activateIntern": "🚀 激活实习机器人",
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
    "resHint": "每次获胜都会带来对应游戏的资源。在工坊里使用它们。",
    "bonusReady": "🎁 领取每日肉排",
    "bonusWait": "⏳ {h} 小时 {m} 分钟后可领",
    "bonusDone": "🎉 肉排已入仓库！",
    "team": "🏆 我的战队",
    "clan": "公会",
    "teamLabel": "战队",
    "captain": "👑 你是队长！",
    "members": "成员",
    "noTeam": "你还没有战队。去机器人聊天里点「🏆 战队与公会」，创建自己的战队或加入别人的。",
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
    "footer": "游戏和竞答在机器人聊天里",
    "noProfile": "未找到个人资料。打开机器人并点按 /start！",
    "blocked": "账号已被管理员封禁。",
    "error": "数据加载失败。稍后再试。",
    "outside": "请从 ROFL HUB 的 Telegram 机器人打开此应用。",
    "robotsTitle": "🤖 你的机器人",
    "buyMore": "🛒 购买",
    "rateShort": "{v} 🪙/小时",
    "refuelOne": "🥩 加 1 份",
    "refuelAll": "⚡ 全部加满",
    "refueled": "已加注：{n} 🥩",
    "res_metal_src": "石头剪刀布和对决",
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
    "ws_armorLvl": "等级 {l}/{m} · 每级产量 +{p}%",
    "ws_shuttleOn": "🚀 穿梭机已建成：交易所手续费 {fee}%",
    "ws_shuttleOff": "🚀 尚未建成穿梭机：交易所手续费 {fee}%",
    "eff_nitrogen": "所有机器人产量 +40%",
    "eff_nuclear": "产量 ×5，钻机吃肉排 ×3",
    "eff_drone": "机器人不会老化",
    "eff_shield": "没人能突袭你",
    "eff_cutlet": "1 份赛博肉排入仓库",
    "eff_armor": "产量永久 +10%",
    "eff_shuttle": "交易所手续费减半，挂单最多 500 份肉排——永久",
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
    "mk_title": "📈 肉排交易所",
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
    "invite": "🤝 邀请链接：每位好友 +1000",
    "transfer": "🔄 给玩家转账金币",
    "market": "📈 肉饼交易所：买入或卖出",
    "sell": "💰 出售肉饼：/sell 数量 价格",
    "my_stats": "📊 我的统计",
    "faq": "📚 常见问题",
    "rules": "📜 用户协议",
    "paysupport": "🛟 付款支持",
    "workshop": "🔧 工坊：资源换强化",
    "raid": "🏴‍☠️ 突袭：侦察与复仇战",
    "goals": "🎯 每日目标与宝箱",
    "station": "🛰 战队空间站：共同项目",
}
