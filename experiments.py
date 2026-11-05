"""Four behavioral experiments (Chinese wording), Horton-replication style.

Each experiment exposes:
  build_prompt(persona, variant, **kw) -> str
  parse(response_text) -> dict | None
  sample_response() -> canned text used by --dry-run

Variants:
  "classic"     -- textbook wording (closest to the published experiment)
  "novel"       -- new cover story, same structure (anti-memorization)
  "adversarial" -- wording where the textbook answer should flip
                   (e.g. a price rise driven by cost, not demand)

All prompts ask for a single JSON object so parsing is mechanical.
"""

import json
import re


def _json_block(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def _ask_json(spec):
    return ("请只用 JSON 回答，格式如下，不要加其他文字：\n" + spec)


# ---------------------------------------------------------------- dictator
def dictator_prompt(persona, variant="classic"):
    if variant == "novel":
        story = ("你和一位陌生人参与一个任务：你手里有 100 个代币，"
                 "你可以决定分给对方任意数量（0 到 100 的整数），"
                 "对方没有决定权，只能接受。")
    else:
        story = ("你和一位陌生人参与一个分配任务：你手里有 100 元，"
                 "你可以决定分给对方任意金额（0 到 100 元的整数），"
                 "对方没有决定权，只能接受。")
    return (persona + "\n" + story +
            "\n你决定分给对方多少？\n" +
            _ask_json('{"give": <整数>, "reason": "<一句话理由>"}'))


def dictator_parse(text):
    d = _json_block(text)
    if d and isinstance(d.get("give"), (int, float)) and 0 <= d["give"] <= 100:
        return {"give": int(d["give"])}
    return None


# ------------------------------------------------------- ultimatum responder
def ultimatum_prompt(persona, variant="classic", offer=20):
    story = (f"一位陌生人提议把 100 元按以下方式分配：他拿 {100 - offer} 元，"
             f"给你 {offer} 元。你可以选择接受（按此分配）或拒绝"
             f"（双方都得 0 元）。")
    return (persona + "\n" + story + "\n你接受还是拒绝？\n" +
            _ask_json('{"accept": <true/false>, "reason": "<一句话理由>"}'))


def ultimatum_parse(text):
    d = _json_block(text)
    if d and isinstance(d.get("accept"), bool):
        return {"accept": d["accept"]}
    return None


# ---------------------------------------------------------------- endowment
def endowment_prompt(persona, variant="classic", arm="owner"):
    if arm == "chooser":
        # KKT-style chooser: binary mug-vs-cash choices at five cash
        # amounts. No price anchor anywhere (noanchor by construction);
        # the grid spans the noanchor WTA/WTP interquartile range.
        story = ("你没有保温杯。现在有人给你一个选择：一个全新的品牌保温杯，"
                 "或者一笔现金。请在以下每种情况下选择你要保温杯还是现金："
                 "现金 50 元、100 元、150 元、200 元、300 元。")
        return (persona + "\n" + story + "\n" +
                _ask_json('{"choices": {"50": <"mug" 或 "cash">, "100": <"mug" 或 "cash">, '
                          '"150": <"mug" 或 "cash">, "200": <"mug" 或 "cash">, '
                          '"300": <"mug" 或 "cash">}, "reason": "<一句话理由>"}'))
    if variant == "noanchor":
        # No price anchor: tests whether the classic 1.24 ratio was
        # compressed by the "market price ~80" anchor.
        if arm == "owner":
            story = ("你拥有一个全新的品牌保温杯，"
                     "现在有人想从你手里买走它。你最低愿意以多少钱卖出？")
        else:
            story = ("你没有保温杯，现在商店里有一个全新的品牌保温杯，"
                     "你最高愿意出多少钱购买？")
    elif arm == "owner":
        story = ("你拥有一个全新的品牌保温杯（市场价约 80 元），"
                 "现在有人想从你手里买走它。你最低愿意以多少钱卖出？")
    else:
        story = ("你没有保温杯，现在商店里有一个全新的品牌保温杯"
                 "（市场价约 80 元），你最高愿意出多少钱购买？")
    return (persona + "\n" + story + "\n" +
            _ask_json('{"price": <数字，单位元>, "reason": "<一句话理由>"}'))


CHOOSER_AMOUNTS = [50, 100, 150, 200, 300]


def endowment_parse(text):
    d = _json_block(text)
    if not d:
        return None
    if isinstance(d.get("price"), (int, float)) and d["price"] >= 0:
        return {"price": float(d["price"])}
    ch = d.get("choices")
    if isinstance(ch, dict):
        vals = {}
        for a in CHOOSER_AMOUNTS:
            v = ch.get(str(a), ch.get(a))
            if v not in ("mug", "cash"):
                return None
            vals[a] = v
        return {"choices": vals}
    return None


# ------------------------------------------------------------- snow shovel
def snow_shovel_prompt(persona, variant="classic"):
    if variant == "novel":
        story = ("暴雨天，一家便利店平时卖雨伞 30 元，暴雨当天涨到 50 元，"
                 "且进货价没有变化。你认为这种涨价公平吗？")
    elif variant == "adversarial":
        story = ("一家五金店平时卖雪铲 150 元，暴雪后涨到 200 元，"
                 "但这是因为雪铲厂家的出厂价同样上涨了 50 元，"
                 "店主只是把成本涨幅传导了下来。你认为这种涨价公平吗？")
    else:
        story = ("一家五金店平时卖雪铲 150 元，暴雪后涨到 200 元，"
                 "且进货价没有变化。你认为这种涨价公平吗？")
    return (persona + "\n" + story + "\n" +
            _ask_json('{"fair": <true/false>, "reason": "<一句话理由>"}'))


def snow_shovel_parse(text):
    d = _json_block(text)
    if d and isinstance(d.get("fair"), bool):
        return {"fair": d["fair"]}
    return None


# ------------------------------------------------------------- status quo
# Samuelson & Zeckhauser (1988) budget allocation, Horton 2026 §2.3.
# Four allocations; one of them is framed as the current (status quo)
# allocation. Runs differ by --sq (auto share of the status quo).
ALLOCATIONS = [(70, 30), (60, 40), (50, 50), (30, 70)]


def status_quo_prompt(persona, variant="classic", sq=60):
    opts = "\n".join(
        f"{i + 1}. 汽车 {a}%，高速公路 {h}%"
        for i, (a, h) in enumerate(ALLOCATIONS))
    story = ("国家公路安全委员会正在决定如何把预算分配给两个安全研究项目："
             "(i) 提高汽车安全性（保险杠、车身、油箱结构、安全带）；"
             "(ii) 提高州际高速公路安全性（护栏、坡度、立交、选择性限速）。"
             f"目前的分配方案是：汽车 {sq}%，高速公路 {100 - sq}%。"
             f"\n请在以下四个方案中选择一个：\n{opts}")
    return (persona + "\n" + story + "\n你选择哪个方案？\n" +
            _ask_json('{"choice": <1-4 的整数>, "reason": "<一句话理由>"}'))


def status_quo_parse(text):
    d = _json_block(text)
    if d and isinstance(d.get("choice"), int) and 1 <= d["choice"] <= 4:
        return {"choice": d["choice"]}
    return None


# -------------------------------------------------------------------- oprea
# Oprea (2024) certainty equivalents, Horton 2026 §2.4.
# 100 boxes, stake 50; p = 0.9 (high) or 0.1 (low); gain or loss framing;
# lottery condition (random box) vs mirror condition (average of all
# boxes, deterministic). Runs differ by --cell and --condition.
# Parsed "ce": sure amount accepted (gains) or sure loss accepted (losses).


def oprea_prompt(persona, variant="classic", cell="gain_high",
                 condition="lottery"):
    p = 0.9 if cell.endswith("high") else 0.1
    n_win = int(100 * p)
    if cell.startswith("gain"):
        if condition == "mirror":
            story = (f"你有 100 个盒子，其中 {n_win} 个装着 50 元，"
                     f"其余 {100 - n_win} 个是空的（0 元）。"
                     "全部打开，你得到所有盒子金额的平均值。"
                     "这是一个确定的金额，没有任何随机性。"
                     "现在有人想用一个确定的金额换走这个平均收益："
                     "你最低愿意接受多少确定金额？")
        else:
            story = (f"你有 100 个盒子，其中 {n_win} 个装着 50 元，"
                     f"其余 {100 - n_win} 个是空的（0 元）。"
                     "随机打开一个盒子，你得到里面的金额。"
                     "现在有人想用一个确定的金额换走你开盒子的机会："
                     "你最低愿意接受多少确定金额？")
    else:
        if condition == "mirror":
            story = (f"你有 100 张卡片，其中 {n_win} 张写着“扣 50 元”，"
                     f"其余 {100 - n_win} 张写着“扣 0 元”。"
                     "全部打开，你实际承担所有卡片扣款的平均值。"
                     "这是一个确定的损失，没有任何随机性。"
                     "现在你可以用一个确定的损失代替这个平均扣款："
                     "你最多能接受的确定损失是多少？")
        else:
            story = (f"你有 100 张卡片，其中 {n_win} 张写着“扣 50 元”，"
                     f"其余 {100 - n_win} 张写着“扣 0 元”。"
                     "随机打开一张卡片，按卡片扣钱。"
                     "现在你可以用一个确定的损失代替这次开卡："
                     "你最多能接受的确定损失是多少？")
    return (persona + "\n" + story + "\n" +
            _ask_json('{"ce": <数字，单位元>, "reason": "<一句话理由>"}'))


def oprea_parse(text):
    d = _json_block(text)
    if d and isinstance(d.get("ce"), (int, float)) and 0 <= d["ce"] <= 50:
        return {"ce": float(d["ce"])}
    return None


# ------------------------------------------------------------------- hiring
# Minimum-wage labor-labor substitution, Horton (2025) / Horton 2026 §2.5.
# Dishwasher hiring: A = 1 year experience, ask = --expask;
# B = 0 years experience, ask = 25. With --minwage 30, asks below 30 are
# forced up to 30 (the employer sees the forced wage).


def hiring_prompt(persona, variant="classic", minwage="none", expask=26):
    mw = None if minwage == "none" else int(minwage)
    eff_a = expask if mw is None else max(expask, mw)
    eff_b = 25 if mw is None else max(25, mw)
    note = "" if mw is None else (
        f"当地最低工资为 {mw} 元/小时，"
        "低于最低工资的要价会被强制提高到最低工资。")
    story = ("你正在为“洗碗工”岗位招聘，必须招一个人。\n"
             f"候选人 A：有 1 年该岗位经验，要价 {eff_a} 元/小时。\n"
             f"候选人 B：无该岗位经验，要价 {eff_b} 元/小时。\n" + note)
    return (persona + "\n" + story + "\n你招谁？\n" +
            _ask_json('{"hire": <"A" 或 "B">, "reason": "<一句话理由>"}'))


def hiring_parse(text):
    d = _json_block(text)
    if d and d.get("hire") in ("A", "B"):
        return {"hire": d["hire"]}
    return None


# ---------------------------------------------------------- volunteering
# Voluntary public goods game (Hauert et al. 2002 Science; Semmann et
# al. 2003 Nature). Optional participation: cooperate (contribute),
# defect (join but contribute nothing) or loner (opt out, fixed payoff).
# Two parameter sets (--params):
#   hauert: Hauert et al. 2002 figure caption, N = 5, r = 3, sigma = 1
#     (investment normalized to 1; here scaled x10: invest 10).
#     c_dom (3C 1D others): C=1.4, D=1.8, L=1.0 -> D
#     d_dom (1C 3D others): C=0.2, D=0.6, L=1.0 -> L
#     l_dom (1C 3L others): S=2, C=2.0, D=1.5, L=1.0 -> C
#   semmann: Semmann et al. 2003 experimental parameters, 6 sampled,
#     pool x3.6, contribution = loner payoff = 1.25 (here x8: 10,
#     endowment 80). Same rotation, verified:
#     c_dom (4C 1D others): C=20, D=24, L=10 -> D
#     d_dom (1C 4D others): C=2, D=6, L=10 -> L
#     l_dom (1C 4L others): S=2, C=26, D=18, L=10 -> C
# The modal rotation D -> L -> C is the single-agent form of the
# papers' Red Queen cycle. Runs differ by --scenario and --params.
SCENARIOS = {
    "hauert": {
        "c_dom": "另外 4 人中：3 人合作、1 人背叛。",
        "d_dom": "另外 4 人中：1 人合作、3 人背叛。",
        "l_dom": "另外 4 人中：1 人合作、3 人退出。",
        "noinfo": "你不知道另外 4 人会怎么选。",
    },
    "semmann": {
        "c_dom": "另外 5 人中：4 人合作、1 人背叛。",
        "d_dom": "另外 5 人中：1 人合作、4 人背叛。",
        "l_dom": "另外 5 人中：1 人合作、4 人退出。",
        "noinfo": "你不知道另外 5 人会怎么选。",
    },
}

RULES = {
    "hauert": ("5 人一组参加公共品任务，每人有 10 元。规则：每人选择三件事之一——"
               "合作：出 10 元进公共池；背叛：参加但不出钱；退出：不参加，"
               "固定得 10 元。公共池里的钱总和乘以 3 后，由所有参加者平分。"
               "如果只有 1 个人参加，他视同退出，固定得 10 元。"),
    "semmann": ("6 人一组参加公共品任务，每人有 80 元。规则：每人选择三件事之一——"
                "合作：出 10 元进公共池；背叛：参加但不出钱；退出：不参加，"
                "固定得 10 元。公共池里的钱总和乘以 3.6 后，由所有参加者平分。"
                "如果只有 1 个人参加，他视同退出，固定得 10 元。"),
}


def volunteering_prompt(persona, variant="classic", scenario="c_dom",
                        params="hauert"):
    story = RULES[params] + "\n" + SCENARIOS[params][scenario]
    return (persona + "\n" + story + "\n你选择合作、背叛还是退出？\n" +
            _ask_json('{"action": <"C"=合作 / "D"=背叛 / "L"=退出>, '
                      '"reason": "<一句话理由>"}'))


def volunteering_parse(text):
    d = _json_block(text)
    if not d:
        return None
    a = d.get("action")
    if isinstance(a, str):
        a = a.strip().upper()
        mapping = {"C": "C", "D": "D", "L": "L",
                   "合作": "C", "背叛": "D", "退出": "L"}
        if a in mapping:
            return {"action": mapping[a]}
    return None


# ------------------------------------------------------------------- carry
# Carry trader (experiment 10, RMB track). Tests the Fama puzzle at
# the agent level: does the agent chase the yield differential
# (buy the high-yield currency) instead of following UIP, which says
# the high-yield currency should depreciate?
# Arms (--spread/--vol/--control):
#   spread inv: China 10y 1.8% vs US 10y 4.8% (inverted, -300bp, the
#     2026 context); pos: China 4.0% vs US 3.0% (+100bp).
#   vol low: annualized FX vol 3%; high: 12%.
#   control none vs controlled (capital controls: cross-border flows
#     need approval and are quota-limited).
# Fama-consistent modal prediction: pos -> buy_cny, inv -> buy_usd.
# High vol and controls should dampen carry (more hold).
SPREADS = {
    "inv": "中国 10 年期国债收益率 1.8%，美国 10 年期国债收益率 4.8%，"
           "中美利差为 -300 个基点（中国利率低于美国）。",
    "pos": "中国 10 年期国债收益率 4.0%，美国 10 年期国债收益率 3.0%，"
           "中美利差为 +100 个基点（中国利率高于美国）。",
}
VOLS = {
    "low": "人民币对美元汇率年化波动率约 3%。",
    "high": "人民币对美元汇率年化波动率约 12%。",
}
CONTROLS = {
    "none": "",
    "controlled": "提示：存在资本管制，资金跨境流动需要审批、额度有限，"
                  "换汇与汇出可能受限。",
}


def carry_prompt(persona, variant="classic", spread="inv",
                 vol="low", control="none"):
    story = ("你是一名外汇投资者，手里有一笔资金，可以自由选择投资方向。\n"
             + SPREADS[spread] + "\n" + VOLS[vol] + "\n"
             + CONTROLS[control]
             + "\n你有三个选择：借美元买人民币资产（做多人民币）、"
               "借人民币买美元资产（做多美元）、或者不动（持有现金）。")
    return (persona + "\n" + story + "\n你选择哪一个？\n" +
            _ask_json('{"action": <"buy_cny"=借美元买人民币资产 / '
                      '"buy_usd"=借人民币买美元资产 / "hold"=不动>, '
                      '"reason": "<一句话理由>"}'))


def carry_parse(text):
    d = _json_block(text)
    if not d:
        return None
    a = d.get("action")
    if isinstance(a, str):
        a = a.strip().lower()
        mapping = {"buy_cny": "buy_cny", "buy_usd": "buy_usd",
                   "hold": "hold", "买人民币": "buy_cny",
                   "买美元": "buy_usd", "不动": "hold"}
        if a in mapping:
            return {"action": mapping[a]}
    return None


# ------------------------------------------------------------------- settle
# Experiment 9: exporter settlement decision (RMB puzzle).
# Portfolio balance + settlement flows (Gabaix & Maggiori 2015).
# 8 arms: expected RMB move (app/dep) x spread (inv/pos, reused from
# carry) x USD index direction (down/up). Firm size cycles
# large/medium/small in the persona (see personas.py).
APPS = {
    "app": "市场普遍预期未来 3 个月人民币兑美元升值 3%（人民币走强）。",
    "dep": "市场普遍预期未来 3 个月人民币兑美元贬值 2%（人民币走弱）。",
}
DXYS = {
    "down": "美元指数过去一个月下跌 3%，美元走弱。",
    "up": "美元指数过去一个月上涨 3%，美元走强。",
}
SIZE_DESC = {
    "large": "大型",
    "medium": "中型",
    "small": "小型",
}


def settle_prompt(persona, variant="classic", spread="inv",
                  app="app", dxy="down", firm_size="medium"):
    story = (f"你是一家{SIZE_DESC[firm_size]}出口企业的财务负责人。公司刚收到"
             "一笔 100 万美元的出口货款，存在美元账户里。现在需要决定："
             "把其中多少比例结汇成人民币。\n"
             + SPREADS[spread] + "\n" + APPS[app] + "\n" + DXYS[dxy]
             + "\n请回答：打算把这笔美元货款的多少比例结汇成人民币"
               "（0–100%），以及结汇节奏：现在全部结汇、继续持汇、"
               "还是分批结汇。")
    return (persona + "\n" + story + "\n" +
            _ask_json('{"settle_pct": <0-100 的数字>, '
                      '"timing": <"now"=现在全部结汇 / "hold"=继续持汇 / '
                      '"tranche"=分批结汇>, "reason": "<一句话理由>"}'))


def settle_parse(text):
    d = _json_block(text)
    if not d:
        return None
    pct = d.get("settle_pct")
    if not isinstance(pct, (int, float)) or not 0 <= pct <= 100:
        return None
    t = d.get("timing")
    if isinstance(t, str):
        t = t.strip().lower()
        mapping = {"now": "now", "hold": "hold", "tranche": "tranche",
                   "现在结汇": "now", "现在全部结汇": "now",
                   "继续持汇": "hold", "分批结汇": "tranche"}
        if t not in mapping:
            return None
        t = mapping[t]
    else:
        return None
    return {"settle_pct": float(pct), "timing": t}


# ------------------------------------------------------------------ fixing
# Experiment 11: central bank fixing agent (RMB puzzle).
# Two-pillar model + countercyclical factor (Jermann, Wei & Yue 2019:
# the two pillars explain ~80% of fixing variation, weights roughly
# equal). 8 arms: previous close move (+/-40bp) x basket-implied move
# (+/-40bp) x countercyclical factor prompt (none/active). The agent
# reports the fixing change in bp vs yesterday's fixing (positive =
# fixing up, RMB weaker) plus the direction. Weights are identified
# from the balanced factorial: w_close = (mean bp | close=+40 minus
# mean bp | close=-40) / 80, likewise w_basket.
CLOSES = {
    "up": "昨日收盘价 6.69，较昨日中间价上升 40 个基点（人民币走弱）。",
    "down": "昨日收盘价 6.61，较昨日中间价下降 40 个基点（人民币走强）。",
}
BASKETS = {
    "up": "按一篮子货币变动测算，今日中间价应较昨日上调 40 个基点。",
    "down": "按一篮子货币变动测算，今日中间价应较昨日下调 40 个基点。",
}
CFIX = {
    "none": "",
    "active": "提示：逆周期因子已启动，报价行可根据市场情况对中间价"
              "进行逆周期调节。",
}


def fixing_prompt(persona, variant="classic", close="up",
                  basket="up", control="none"):
    story = ("你是一家人民币中间价报价行的交易员，今天需要报出美元兑"
             "人民币中间价。昨日中间价 6.65。上月货物贸易顺差约 900 亿美元，"
             "企业结汇意愿稳定（外汇收入结汇率约 65%）。\n"
             + CLOSES[close] + "\n" + BASKETS[basket] + "\n"
             + CFIX[control]
             + "\n请回答：今日中间价较昨日中间价调整多少个基点"
               "（正数=上调中间价，人民币贬值方向；负数=下调中间价，"
               "人民币升值方向；0=不变），以及调整方向。")
    return (persona + "\n" + story + "\n" +
            _ask_json('{"fixing_bp": <数字，基点>, '
                      '"direction": <"up"=上调 / "down"=下调 / '
                      '"unchanged"=不变>, "reason": "<一句话理由>"}'))


def fixing_parse(text):
    d = _json_block(text)
    if not d:
        return None
    bp = d.get("fixing_bp")
    if not isinstance(bp, (int, float)) or not -500 <= bp <= 500:
        return None
    dr = d.get("direction")
    if isinstance(dr, str):
        dr = dr.strip().lower()
        mapping = {"up": "up", "down": "down", "unchanged": "unchanged",
                   "上调": "up", "下调": "down", "不变": "unchanged"}
        if dr not in mapping:
            return None
        dr = mapping[dr]
    else:
        return None
    return {"fixing_bp": float(bp), "direction": dr}


EXPERIMENTS = {
    "dictator": {
        "name": "独裁者博弈",
        "prompt": dictator_prompt,
        "parse": dictator_parse,
        "sample": '{"give": 30, "reason": "对方也需要钱，分一部分比较合理。"}',
        "baseline": "人类被试中，给 0 的是少数，众数常在 0 和对半分之间；"
                    "本试点先看分布形态，定量基线以原文为准。",
    },
    "ultimatum": {
        "name": "最后通牒博弈（响应方）",
        "prompt": ultimatum_prompt,
        "parse": ultimatum_parse,
        "sample": '{"accept": false, "reason": "分得太少，宁可双方都不得。"}',
        "baseline": "人类拒绝率随提议份额下降而上升；"
                    "本试点看拒绝率-提议曲线是否单调。",
    },
    "endowment": {
        "name": "禀赋效应",
        "prompt": endowment_prompt,
        "parse": endowment_parse,
        "sample": '{"price": 100, "reason": "自己的东西舍不得便宜卖。"}',
        "sample_chooser": '{"choices": {"50": "mug", "100": "mug", "150": "cash", "200": "cash", "300": "cash"}, "reason": "150 元现金比保温杯值钱。"}',
        "baseline": "人类卖价（WTA）显著高于买价（WTP）；"
                    "本试点看 WTA/WTP 比值是否显著大于 1。",
    },
    "snow_shovel": {
        "name": "雪铲涨价公平性",
        "prompt": snow_shovel_prompt,
        "parse": snow_shovel_parse,
        "sample": '{"fair": false, "reason": "趁灾涨价不厚道。"}',
        "baseline": "Kahneman 等（1986）原文：82% 的真人被试认为不公平；"
                    "本试点以此为锚，并检验干预倾向梯度。",
    },
    "status_quo": {
        "name": "现状偏见",
        "prompt": status_quo_prompt,
        "parse": status_quo_parse,
        "sample": '{"choice": 2, "reason": "维持目前的方案最稳妥。"}',
        "baseline": "Samuelson & Zeckhauser（1988）：被标为现状的选项更常被选；"
                    "Pilli & Nallur（2026）人类实验：60A40H 被标为现状时"
                    "得票 51%，非现状时 14%，h = 0.79；S&Z 原文效应量"
                    "h = 0.78（据该文引用）。Horton 2026 的 AI 侧："
                    "DeepSeek 现状偏好 logit 系数 0.762。",
    },
    "oprea": {
        "name": "复杂性与四重模式",
        "prompt": oprea_prompt,
        "parse": oprea_parse,
        "sample": '{"ce": 40, "reason": "确定拿到 40 元比赌一把更踏实。"}',
        "baseline": "四重模式（前景理论）：得高概率风险厌恶、得低概率风险寻求、"
                    "失高概率风险寻求、失低概率风险厌恶；"
                    "Oprea 的关键发现是该模式在无风险的 mirror 条件下同样出现。",
    },
    "hiring": {
        "name": "最低工资雇佣替代",
        "prompt": hiring_prompt,
        "parse": hiring_parse,
        "sample": '{"hire": "A", "reason": "有经验的更靠谱，值得多付一点。"}',
        "baseline": "Horton（2025）田野实验：最低工资下雇佣量变化不大，"
                    "但显著转向更有生产力的工人；Horton 2026 的 AI 复现："
                    "雇佣工资 +1.31 美元/小时（无参照工资）、"
                    "雇佣经验 +0.081 年。",
    },
    "volunteering": {
        "name": "自愿公共品（合作起源）",
        "prompt": volunteering_prompt,
        "parse": volunteering_parse,
        "sample": '{"action": "D", "reason": "其他人大多合作，我参加但不出钱能分得最多。"}',
        "baseline": "Hauert 等（2002）Science：自愿参与下合作者与背叛者共存、"
                    "频率循环振荡（Red Queen）；Semmann 等（2003）Nature 人类实验："
                    "操纵初始构成可产生每个预测方向，合作维持在可观水平。"
                    "本设计三臂预测众数：合作盛行→背叛、背叛盛行→退出、"
                    "退出盛行→合作。",
    },
    "carry": {
        "name": "利差交易者（人民币）",
        "prompt": carry_prompt,
        "parse": carry_parse,
        "sample": '{"action": "buy_usd", "reason": "美元利率更高，借人民币买美元资产利差更大。"}',
        "baseline": "Fama 之谜：利差对汇率的解释力弱且不稳定，"
                    "回归斜率常为负——市场行为像在追逐利差而非遵循"
                    "未抛补利率平价。本实验的定量基线为 USD/CNY 的"
                    "Fama 回归（2026-11-05 已算，见 "
                    "research_notes/fama_baseline/fama_baseline.md）："
                    "β(12m)=+0.015（SE 0.746，R²=0.000，n=75），"
                    "β(1m)=−0.468（SE 0.726，t(β=1)=−2.02，R²=0.004，"
                    "n=86）；2024+ 窗口利差与 12 个月汇率变动 corr=−0.596。"
                    "预测众数：正利差→买人民币，倒挂→买美元；"
                    "高波动与资本管制应抑制套利（更多不动）。",
    },
    "settle": {
        "name": "出口商结汇决策（人民币）",
        "prompt": settle_prompt,
        "parse": settle_parse,
        "sample": '{"settle_pct": 60, "timing": "tranche", "reason": "预期升值，先结一部分锁定收益。"}',
        "baseline": "外汇局结汇率方向：2024 年顺差 9,920 亿美元时企业"
                    "囤汇、人民币贬值；2026 年一季度净结汇近 1,400 亿美元、"
                    "人民币升值。本试点看结汇比例是否随预期升值上升、"
                    "随利差倒挂加深下降（定量基线为媒体转述，须复核）。",
    },
    "fixing": {
        "name": "央行中间价 agent（人民币）",
        "prompt": fixing_prompt,
        "parse": fixing_parse,
        "sample": '{"fixing_bp": 20, "direction": "up", "reason": "收盘与篮子都指向贬值，中间价跟随上调一半。"}',
        "baseline": "Jermann, Wei & Yue（2019）：两支柱可解释中间价约"
                    "80% 的变动，两支柱权重大致相等（各约 50%）；"
                    "逆周期因子方向应与市场单边预期相反（Sun 2025 "
                    "用滚动两支柱残差代理测度）。对照为 CFETS 中间价"
                    "实际值。",
    },
}
