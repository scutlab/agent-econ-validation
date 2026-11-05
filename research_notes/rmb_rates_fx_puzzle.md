# 人民币"利率下行、汇率上行"之谜：理论、最新论文、数据与 agent 验证

- 日期：2026-11-05
- 检索人：后台文献任务（只做公开检索与整理，不跑实验）
- 范围说明：本报告只回答人民币汇率问题。用户同时问的"AI 是否存在泡沫"
  不在本报告内（另题处理）。
- 来源状态：**A** = 论文原文读到；**B** = 论文/预印本转述或摘要；
  **C** = 媒体与机构分析（非论文）；**未获全文** = 明确写明。
  每个数字后注明来源与状态；拿不到的写"未获"，不编造。

## 0. 现象界定：先分清两个阶段，"谜"的程度不一样

用户观察"银行利率不断降低、汇率却不断升高"，首先要分阶段，
因为 2025 年与 2026 年的驱动逻辑不同，"谜"的强度也不同。

**利率端（已核实，官方发布）**：1 年期 LPR 从 2024 年初 3.45%
降至 2024 年 10 月 3.10%（2024 年全年累计 −35bp），2025 年 5 月
再降 10bp 至 3.00%；5 年期以上 LPR 2024 年累计 −60bp 至 3.60%，
2025 年 5 月至 3.50%，此后连续 17 个月未动（截至 2026 年 10 月）
**C**（全国银行间同业拆借中心 / 中国人民银行公告，经多家银行
LPR 表交叉核对）。

**汇率端（已核实，媒体报道 + 官方数据转述）**：

| 时段 | 事实 | 来源 |
|---|---|---|
| 2025 年 4 月 | 在岸人民币一度跌至 7.43 附近（年内低点） | 媒体报道 **C** |
| 2025 年全年 | 美联储降息 3 次；美元指数全年 −9.69% 至 97.97（近 8 年最大单年跌幅）；离岸人民币 12 月 25 日升破 7.0，重回"6 时代"，15 个月新高 | HTX/TechFlowPost 2025-12-25 **C** |
| 2025 年全年 | 中国货物贸易顺差 1.189 万亿美元（创纪录；2024 年 9,920 亿美元），出口 +5.5%（12 月 +6.6%），对美出口 −20%，对非洲 +25.8%、东盟 +13.4%、欧盟 +8.4% | 海关总署数据，经 CNN 2026-01-14 报道 **C** |
| 2026 年 1–9 月 | 在岸人民币对美元升值约 4.1%；10 月 9 日收 6.6921，创 2022 年 6 月 29 日以来新高；同期美元指数 +4%（10 月 9 日 102.21），10 年期中美利差年内走阔 117bp；央行称 2025 年以来人民币累计升值约 9% | 《经济观察报》2026-10-12 **C**；央行 2026-10-08 表态 **C** |
| 2026 年一季度 | 银行代客结售汇：银行买入外汇约 7,660 亿美元、卖出 6,280 亿美元，净结汇近 1,400 亿美元（2025 年一季度为净流出 576 亿美元） | 外汇局数据，经 Sucden Financial 转述 **C** |

**关键判断**：2025 年的升值大半可用美元走弱（美联储降息、美元指数
−9.7%）+ 创纪录顺差 + 结汇来解释，"谜"较弱；真正的谜在 2026 年——
中美 10 年利差走阔到 300bp 以上、美元指数年内转强，人民币仍升值
约 4%，且与美元"同步走强"（2015 年汇改以来罕见）**C**（《经济观察报》
引工银国际首席经济学家程实）。所以验证应以 2026 年的"利差走阔、
美元转强、人民币仍升"为硬靶子，而不是笼统的"降息升值"。

**口径提醒**：2024 年人民币对美元贬值 2.83%，但对一篮子货币
（CFETS 指数 97.4→101.5，+4.16%）是升值的；2025 年人民币对美元
升值约 4%，对欧元却贬值约 9%**C**（第一财经研究院《2024 年人民币
汇率年报》；《经济观察报》2026-10-12）。只看 USD/CNY 会误判。

## 1. 理论：能解释"降息却升值"的机制清单

### 1.1 未抛补利率平价（UIP）失效 / 远期升水之谜 —— 最直接的理论支撑

- **核心机制**：UIP 要求 i − i* = E[Δe]，即低利率货币应预期升值
  以补偿利差。但实证中 Fama 回归（Δe 对利差回归）的斜率 β 普遍
  显著小于 1、常为负——高利率货币反而升值，低利率货币反而贬值，
  与 UIP 预测相反。这就是远期升水之谜（Fama, 1984）**A**。
  换言之，"降息却升值"在 UIP 失效的世界里不是反常，而是常态：
  利差对汇率的解释力本来就弱且不稳定。
- **适用条件**：风险中性 + 自由资本流动。任一条件不满足，
  UIP 就不必成立。
- **对中国的适用性**：部分适用。Fama β 在不同时期、不同货币对上
  符号会翻转（Engel 等 2022 的滚动回归：美元-英镑 β 在金融危机
  前强负、危机后转正）**B**（讲义转述）。因此不能拿 UIP 失效
  "解释一切"，必须问：在本轮中，到底是哪个摩擦在起作用——
  这就引向 1.2–1.7。

### 1.2 汇率脱节之谜（Exchange Rate Disconnect）—— 解释"利差解释力弱"

- **核心机制**：Meese & Rogoff (1983) 发现汇率近似随机游走，
  与宏观基本面（包括利差）的同期相关性接近零**A**；
  Obstfeld & Rogoff (2000) 把它列为国际宏观六大谜之一**A**。
  Itskhoki & Mukhin (2021, *JPE* 129(8), 2183–2232，
  DOI 10.1086/714447)**A**：分割的国际金融市场 + 噪声交易者 +
  风险厌恶中介 → 均衡 UIP 偏离；金融市场冲击使汇率呈近鞅过程，
  与消费、产出、通胀、利率的联动都弱。2022 年 Clark 奖表彰词
  概括为："金融市场噪声而非经济基本面，可能是汇率的主要驱动力"
  **B**（AEA 表彰词转述）。
- **适用条件**：金融市场分割、套利受限。完全适用中国
  （资本管制 + 在岸/离岸分割）。
- **对中国的适用性**：强。Chahrour 等（2024, NBER WP 32596）
  进一步发现：美国未来生产率的噪声消息可解释美元/G7 汇率
  一半以上的波动**B**（NBER 工作论文摘要）。对人民币而言，
  这意味着汇率主要由金融市场冲击（风险情绪、噪声交易者
  的组合调整）驱动，利差只是众多冲击之一。

### 1.3 多恩布什超调（Dornbusch 1976）—— 解释短期波动，不解释持续升值

- **核心机制**：价格粘性 + 货币扩张 → 汇率短期超调（贬过头），
  再缓慢回升。Dornbusch (1976, *JPE* 84(6), 1161–1176)**A**。
- **适用性**：只能解释货币政策冲击后的短期动态；对"持续数月、
  利差走阔下的升值"解释力弱。且异质性预期扩展
  （De Grauwe 行为金融框架）表明超调幅度取决于预期策略分布，
  不是固定常数**B**。本谜中列为次要机制。

### 1.4 货币模型 / 购买力平价 / Balassa–Samuelson —— 长期低估论

- **核心机制**：PPP 认为长期汇率由物价比决定；Balassa–Samuelson
  认为生产率增长快的国家实际汇率升值。中国劳动生产率持续提升、
  出口结构转向高端制造 → 长期均衡汇率高于现价，即人民币低估。
  央行原调查统计司司长盛松成 2025 年称：按 PPP 计算汇率甚至可能
  在 1:3.5 附近，长期看人民币明显低估**C**（媒体转述）。
  Goldman Sachs 的 GSDEER 模型称人民币对美元低估近 30%，
  低估程度堪比 2005 年汇改前（当时 8.28，随后十年升至 6.1 附近）
  **C**（媒体转述；GSDEER 方法不公开）。
- **适用条件**：长期视角；PPP 对短期汇率解释力极弱（Rogoff 1996
  的 PPP 之谜：实际汇率持续偏离、半衰期 3–5 年）。
- **对中国的适用性**：可作长期方向参考，不可作短期验证靶子。
  且 IMF 2025 年第四条款评估称人民币低估约 12–21%**C**
  （二手转述，IMF 原文未核实），与高盛 30% 的口径并不一致——
  估值方法不同，结论就不同，报告中须并列、不得只取其一。
  央行 2026-10-08 文章《央行对人民币汇率的看法》的三点反驳
  也与此相关：出口强是竞争力而非低估汇率；汇率不只由贸易差额
  决定；没有全球公认的估值标准**C**（Trivium China 播客摘要转述）。

### 1.5 资产组合平衡 / 金融中介模型（Gabaix–Maggiori）—— 流量与存量视角

- **核心机制**：Gabaix & Maggiori (2015, *QJE* 130(3), 1369–1420)
  **A**：国际金融中介风险承担能力有限，汇率由资本流动的供需
  决定；当外国投资者对本币资产需求上升（或本国居民减少外币
  资产配置），本币升值——与利差无关。Kalemli-Özcan & Varela
  （NBER WP 28923，2021 年初版、2026 年 8 月修订）用调查预期
  构建前瞻性 UIP 溢价，发现新兴市场 UIP 溢价主要是"利差现象"、
  与本地政策不确定性挂钩，而发达国家主要是"预期现象"**B**
  （NBER 工作论文摘要）。
- **对中国的适用性**：强，且直接对应本轮的结汇潮：
  2022–2025 年人民币走弱期出口商囤积美元货款，2025–2026 年
  转为集中结汇（2026 年一季度净结汇近 1,400 亿美元）**C**。
  机制：不是利差变了，而是出口商的组合调整（美元资产→人民币
  资产）与预期自我实现。验证靶子应是结售汇数据与汇率的联动，
  而非利差。

### 1.6 三元悖论与资本管制 —— 中国能"降息又升值"的制度前提

- **核心机制**：蒙代尔三元悖论：固定汇率、资本自由流动、
  独立货币政策三者只能取其二。中国选了"管理浮动 + 资本管制 +
  独立货币政策"，因此国内利率可以主要服务于国内稳增长，
  不必跟着美国走；汇率则由管制 + 干预 + 结售汇共同决定。
  资本管制使 UIP 的套利链条断裂（在岸 CNY 与离岸 CNH 之间
  套利受限），利差对汇率的传导被制度性削弱。
- **适用性**：这是中国案例与自由浮动货币的根本区别。
  任何不建模资本管制的理论，用在中国都会系统性误判。
  央行 2026-10-08 明确：市场供求起决定性作用，央行不预设
  目标、不干预长期趋势**C**——但这与逆周期因子等工具的存在
  并不矛盾（见 1.7）。

### 1.7 中国特有制度：管理浮动、两支柱、逆周期因子

- **核心机制**：中间价形成机制"两支柱"（上一日收盘价 + 一篮子
  货币变动）+ 2017 年引入的逆周期因子（ discretionary 调整，
  计算方法不公开）。Jermann, Wei & Yue（2019, NBER 会议论文；
  SSRN 3360617）证明两支柱可解释中间价约 80% 的变动，
  两支柱权重大致相等；模型能预测 2017 年 5 月逆周期因子的引入
  **B**（NBER 会议论文摘要；期刊版未核实）。Sun (2025,
  *J. Int. Financ. Mark. Inst. Money* 101, DOI 10.1016/j.intfin.2025.102144)
  **B**：逆周期因子在第二阶段使用更密集，但第一阶段对降低
  人民币与其他货币联动的效果更显著；初期实施带来明显升值。
- **适用性**：直接适用。这是理解"中间价 vs 即期价"偏离、
  以及汇率"该贬不贬"的关键。逆周期因子不公开 → 定量测度
  只能用滚动估计的两支柱残差代理（Sun 2025 的方法），
  测度本身带误差，验证时须说明。

### 1.8 经常账户 / 贸易顺差与结汇（流量视角）

- **核心机制**：巨额顺差 → 出口商手握美元 → 结汇意愿决定
  外汇市场供求。2025 年顺差 1.189 万亿美元（七个月度顺差
  超 1,000 亿美元）**C**；但顺差不自动等于升值——2024 年
  顺差 9,920 亿美元时人民币对美元仍贬值 2.83%，因为企业
  囤积美元、利差倒挂下持汇收益高**C**（中银证券管涛团队
  2024 年外汇市场分析）。2025–2026 年转折点是：美联储降息
  压缩持汇收益 + 美元走弱改变预期 → 囤积转为集中结汇。
- **适用性**：强。验证的关键变量是结售汇差额与结汇率，
  不是顺差本身。

### 1.9 美元因素与利差交易平仓

- **核心机制**：汇率是相对价格。2025 年美元指数 −9.69%
  是人民币对美元升值的主因之一（跷跷板）；2026 年美元指数
  转强但人民币仍升，说明美元因素已非主因，转向国内结汇
  与预期。利差交易平仓机制可参考 2024 年 8 月日元套息交易
  平仓事件（类比，非本币证据）：利差收窄 → 套息头寸平仓 →
  资金回流 → 本币升值。当前中美利差倒挂下，境内主体
  借美元、持人民币的反向套息同样存在，平仓方向决定汇率。
- **适用性**：作为机制类比可用；直接证据需结售汇与跨境
  资本流动数据（见第 3 节）。

### 1.10 有限理性 / 行为金融模型 —— 为 agent 验证搭桥

- **核心机制**：Kolasa 等（2025, *J. Int. Econ.* 155, 104087,
  DOI 10.1016/j.jinteco.2025.104087）**B**：在开放经济模型中
  加入 Gabaix (2020) 式有限理性（认知折扣），可缓解远期指引
  汇率之谜；UIP 溢价冲击仍是汇率的主要驱动。De Grauwe &
  Grimaldi（2006, CESifo WP 1849 及同名专著）**B**：agent 在
  基本面、外推、动量三类预测规则间切换，汇率可在基本面均衡
  与非基本面（泡沫）均衡间跳变，对初始条件与风险感知敏感。
  Frankel & Froot (1986) 的三类 agent（基本面派、图表派、
  组合管理者）是异质性预期汇率模型的源头**B**（转引）。
- **适用性**：这是 agent 验证的理论入口（见第 4 节）。

## 2. 最新论文（2023–2026，人民币 / 利率-汇率 / 资本流动）

| # | 论文（完整引用） | 一句话结论 | 状态 |
|---|---|---|---|
| 1 | Chahrour, R., Cormun, V., De Leo, P., Guerrón-Quintana, P. A., & Valchev, R. (2024). Exchange Rate Disconnect Revisited. NBER Working Paper No. 32596. https://www.nber.org/papers/w32596 | 美国未来生产率的噪声消息可解释美元/G7 汇率一半以上的波动，汇率主要由金融冲击而非宏观基本面驱动。 | **B**（工作论文摘要直读；未同行评议） |
| 2 | Kalemli-Özcan, Ş., & Varela, L. (2021, rev. Aug 2026). Five Facts about the UIP Premium. NBER Working Paper No. 28923. https://www.nber.org/papers/w28923 | 新兴市场 UIP 溢价主要是利差现象、与本地政策不确定性挂钩；发达国家主要是预期现象、与全球风险挂钩。 | **B**（工作论文摘要直读；未同行评议） |
| 3 | Ma, C., Rebucci, A., & Zhou, S. (2025). A Nascent International Financial Channel of China's Monetary Policy Transmission. NBER Working Paper No. 34291. https://www.nber.org/papers/w34291 | 用 QDII 基金颗粒数据识别出中国货币政策经组合股权流出向全球股市传导的新渠道，统计显著但经济量级尚小；中国海外组合股权持有 2023 年已超 5,000 亿美元。 | **B**（工作论文摘要直读；未同行评议） |
| 4 | Liu, Y., Shi, J., & Li, Y. (2026). The Impact of Federal Reserve Monetary Policy Adjustments on RMB Exchange Rate Fluctuations. *International Journal of Finance & Economics*, 31(3), 4073–4090. DOI: 10.1002/ijfe.70135 | 2012–2025 月度 TVP-VAR：美元指数影响最持久且随全球不确定性上升而增强；利率冲击的影响取决于政策环境；CNH 比 CNY 反应更快更强；2015 汇改与逆周期因子改变了传导方式。 | **B**（期刊摘要直读；全文未获） |
| 5 | Sun, Y. (2025). The effects of the counter-cyclical factor on renminbi co-movements. *Journal of International Financial Markets, Institutions and Money*, 101. DOI: 10.1016/j.intfin.2025.102144 | 用滚动估计两支柱模型测度逆周期因子强度：第二阶段使用更密集，但第一阶段对降低人民币联动的效果更显著；初期实施带来明显升值。 | **B**（期刊摘要直读；全文未获） |
| 6 | Jiang, Z. (2026, rev. Aug 2026). Financial Interdependence and Currency Internationalization. NBER Working Paper No. 35541. https://www.nber.org/papers/w35541 | 资产需求模型：中美金融相互依存下，人民币国际化存在非单调转换动态与多重均衡；金融制裁加速转换。 | **B**（工作论文摘要直读；未同行评议） |
| 7 | Kolasa, M., Ravgotra, S., & ? (2025). Monetary policy and exchange rate dynamics in a behavioral open economy model. *Journal of International Economics*, 155, 104087. DOI: 10.1016/j.jinteco.2025.104087 | 加入有限理性（认知折扣）可缓解远期指引汇率之谜；UIP 溢价冲击仍是汇率的主要驱动。 | **B**（期刊摘要直读；全文未获。注：作者名单以 DOI 页为准，检索摘要未完整显示） |

补充经典文献（理论地基，均为标准引用）：Fama (1984, *JME* 14(3),
319–338)；Meese & Rogoff (1983, *JIE* 14(1–2), 3–24)；
Dornbusch (1976, *JPE* 84(6), 1161–1176)；Obstfeld & Rogoff (2000,
NBER Macro Annual 15, 339–390)；Gabaix & Maggiori (2015, *QJE* 130(3),
1369–1420)；Itskhoki & Mukhin (2021, *JPE* 129(8), 2183–2232，
DOI 10.1086/714447)；Mundell (1963, *Can. J. Econ. Polit. Sci.* 29(4),
475–485)；Balassa (1964, *JPE* 72(6), 584–596)；Jermann, Wei & Yue
(2019, NBER 会议论文，SSRN 3360617；期刊版未核实)。

## 3. 数据清单：验证该问题需要的具体数据

| 指标 | 来源机构 | 频率 | 是否公开可得 |
|---|---|---|---|
| USD/CNY 中间价与即期收盘价 | 中国外汇交易中心 CFETS（chinamoney.com.cn） | 日 | 免费公开 |
| USD/CNH 离岸即期 | 香港市场；Wind/彭博（付费）；Investing 等免费终端有延迟数据 | 日 | 半公开（免费版延迟/不完整） |
| CFETS 人民币汇率指数（一篮子） | 中国外汇交易中心 | 周 | 免费公开 |
| 1 年期 / 5 年期以上 LPR | 中国人民银行授权全国银行间同业拆借中心（pbc.gov.cn） | 月（20 日） | 免费公开 |
| 7 天回购利率 DR007、SHIBOR | 全国银行间同业拆借中心 | 日 | 免费公开 |
| 10 年期国债收益率（中债） | 中央结算公司 ChinaBond（chinabond.com.cn） | 日 | 免费公开 |
| 10 年期美债收益率、联邦基金利率 | FRED（DGS10、DFF、FEDFUNDS） | 日/月 | 免费公开 |
| 中美利差（10 年、1 年、政策利率） | 由上计算 | 日 | 可自行计算 |
| 美元指数 DXY | ICE（Wind/彭博付费；FRED 提供贸易加权美元指数 DTWEXBGS 免费） | 日 | DXY 本身付费；贸易加权版免费 |
| 货物贸易差额、出口/进口 | 海关总署（customs.gov.cn） | 月 | 免费公开 |
| 国际收支（经常账户、资本与金融账户） | 国家外汇管理局 SAFE（safe.gov.cn） | 季 | 免费公开 |
| 银行代客结售汇、结汇率/售汇率 | 外汇局月度新闻发布会 | 月 | 免费公开 |
| 外汇储备 | 中国人民银行 / 外汇局 | 月 | 免费公开 |
| 跨境证券投资流动（债券通、股票通、QDII） | 外汇局、港交所、中国结算；QDII 基金持仓（Ma 等 2025 用） | 月/季 | 部分公开、颗粒数据需申请 |
| 远期点数、NDF、期权隐含波动率 | CFETS、彭博（付费） | 日 | 付费为主 |
| 汇率预期调查（Consensus Forecasts） | Consensus Economics（Kalemli-Özcan & Varela 的 UIP 溢价测度所用） | 月 | 付费 |
| 逆周期因子强度 | 不公开；Sun (2025) 用滚动两支柱模型残差代理 | — | 须自行估计 |
| GSDEER 均衡汇率估值 | Goldman Sachs 专有模型 | — | 不公开（只有媒体转述的结论） |
| IMF 第四条款汇率评估 | IMF（2025 Article IV） | 年 | 报告公开；底层模型细节有限 |

**最少可用数据集（免费路线）**：CFETS 中间价/即期 + LPR +
中债 10 年 + FRED 美债 10 年/DFF + 海关贸易差额 + 外汇局结售汇与
外汇储备 + CFETS 指数。以上即可做利差-汇率回归、Fama 回归、
结售汇-汇率联动三项核心检验。

## 4. Agent / ABM 验证：能不能用 agent 验证？初步判断

### 4.1 已有的方法与理论（找得到）

- **异质性 agent 汇率模型（非 LLM，理论成熟）**：De Grauwe &
  Grimaldi (2006) 的行为金融汇率模型是现成框架——agent 在
  基本面/外推/动量三类规则间按收益切换，可产生基本面均衡与
  非基本面（泡沫）均衡的跳变；Chiarella 等的异质性预期模型
  （UTS  repository 全文）证明利差 + 有限理性组合管理者能生成
  多重均衡、偏离基本面与波动聚集；Jongen 等 (2012, *JEDC* 36(5),
  719–735, DOI 10.1016/j.jedc.2012.01.005) 用调查预期估计异质性
  agent 模型，权重随市场环境调整，样本外优于随机游走。
- **LLM agent 用于货币政策与市场（最接近的先例）**：Collodel
  (2025, arXiv:2508.13635)**B**：30 个异质 LLM 交易员（不同风险
  偏好、认知偏差、解读风格）读欧洲央行发布会文本、预测欧元
  利率互换，283 场发布会（1998–2025）模拟分歧与实际 OIS 波动
  的 Spearman 相关约 0.5（提示词优化后 0.6）。这是"LLM agent
  模拟市场对央行沟通的反应"的直接范式，可平移为"LLM agent
  模拟市场对央行中间价/降息的反应"。
- **LLM + ABM 双边市场**：Vidler & Walsh (2025, AAMAS 2025,
  arXiv:2503.00320)**B**：TRIBE 模型用 LLM 增强 ABM，模拟
  澳大利亚国债 OTC 市场的双边交易与风险厌恶、模糊厌恶。
  证明 LLM agent 可嵌入 ABM 的决策层。
- **RL 交易 agent（非 LLM）**：Monaco 等 (2024, arXiv:2410.23294)
  用 Fitted Natural Actor-Critic 做外汇日内交易；TS-Agent (2025,
  arXiv:2508.13915) 用 LLM agent 做金融时序建模，含外汇数据集。
  这些是"交易策略"层面的工作，不是"汇率决定"层面的验证。

### 4.2 直接针对人民币的 LLM agent 研究：未找到

检索未发现用 LLM agent 研究人民币汇率决定、中美利差传导、
资本管制下汇率形成的论文。最接近的是上述 Collodel (2025)
的欧元区研究与 TRIBE 的债券市场研究。结论：**该方向是空白，
不是已有结论的复现**。这既是机会（可做首创性探索），也是风险
（没有现成对照基线，判定标准须自己立）。

### 4.3 拟议的验证设计（与本项目脚手架风格一致，供拍板）

**单 agent 实验（可直接接入现有脚手架）**：

1. **出口商结汇决策**：给 agent 一笔美元货款 + 当前利差、
   汇率预期、美元指数，问"现在结汇 / 继续持汇 / 分批结汇"。
   操纵变量：利差（倒挂程度）、预期升值幅度、美元指数方向。
   判定：结汇比例是否随"预期升值"上升、随"利差倒挂加深"下降，
   且 persona（企业规模、风险态度）有梯度。对照：外汇局
   实际结汇率的时间序列方向。
2. **利差交易者**：给 agent 中美利差与汇率波动率，问"借美元
   买人民币资产 / 反向 / 不动"。操纵：利差符号翻转。
   判定：是否出现与 Fama 之谜一致的行为（利差大时仍做多
   高息货币）。
3. **央行中间价 agent**：给 agent 上日收盘、一篮子变动、
   顺差与结汇数据，问"中间价较模型值上调/下调/不变"。
   操纵：是否提示"逆周期因子启动"。判定：是否复现
   Jermann 等的两支柱权重（约各 50%）与逆周期因子的
   逆周期方向。对照：CFETS 中间价实际值。

**多 agent 模拟（第二阶段）**：De Grauwe 式切换模型 + LLM agent
替代规则库：基本面派（看利差与顺差）、图表派（看趋势）、
结汇驱动派（看结售汇流），在模拟市场中出清汇率；检验
"利差走阔下人民币仍升"能否在模型中涌现，以及哪类 agent
权重变化是关键驱动。

**判定标准（沿用本项目三条）**：方向一致（与实际结汇率/
汇率方向同向）、分布可比（agent 结汇比例分布 vs 实际结汇率
分布）、persona 梯度存在。另加一条：**与 Fama 回归对照**——
agent 行为隐含的 β 是否与实际 USD/CNY 的 Fama β 同号
（该 β 须先用免费数据算出，作为基线）。

**前置工作**：① 用第 3 节免费数据算 USD/CNY 的 Fama 回归
（β、R²）与利差-汇率滚动相关；② 抓 PBOC 2026-10-08 文章
全文与 IMF 2025 Article IV 原文；③ 拍板先做单 agent 三实验
中的哪一个。

## 5. 未解决项

1. **D3 的主文系数类比**：本报告多处关键数字来自媒体转述
   （DXY、顺差、结汇、GSDEER 30%、IMF 低估 12–21%），
   须以官方发布（海关总署、外汇局、CFETS）逐项复核后才能
   进入正式基线；媒体数字只作线索。
2. **逆周期因子不公开**：只能用 Sun (2025) 的滚动残差法代理，
   测度误差须在报告中说明。
3. **Fama β（USD/CNY）未算**：须先用免费数据算出，作为
   agent 验证的定量基线；目前只有"利差与汇率相关性极低"的
   定性说法（Longbridge 文章转述）。
4. **PBOC 2026-10-08 文章全文未读**：目前只有 Trivium 播客
   摘要转述；全文是理解官方立场的一手来源，应抓取。
5. **IMF 2025 Article IV 原文未核实**：低估 12–21% 为二手转述。
6. **Jermann, Wei & Yue 的期刊版未核实**：目前引用为 2019 年
   NBER 会议论文（SSRN 3360617）。
7. **Kolasa 等（2025）作者名单不完整**：检索摘要未完整显示
   全部作者，以 DOI 页为准补全。
8. **人民币专用的 LLM agent 研究是空白**：无现成对照基线，
   若立项，判定标准与基线须在设计文档中先行立好，不得事后拼凑。

## 参考文献（按文中出现顺序；状态如实标注）

[1] Fama, E. F. (1984). Forward and spot exchange rates.
*Journal of Monetary Economics*, 14(3), 319–338。**A**（标准引用）。
[2] Meese, R. A., & Rogoff, K. (1983). Empirical exchange rate
models of the seventies: Do they fit out of sample?
*Journal of International Economics*, 14(1–2), 3–24。**A**（标准引用）。
[3] Dornbusch, R. (1976). Expectations and exchange rate dynamics.
*Journal of Political Economy*, 84(6), 1161–1176。**A**（标准引用）。
[4] Obstfeld, M., & Rogoff, K. (2000). The six major puzzles in
international macroeconomics: Is there a common cause?
*NBER Macroeconomics Annual*, 15, 339–390。**A**（标准引用）。
[5] Gabaix, X., & Maggiori, M. (2015). International liquidity
and exchange rate dynamics. *Quarterly Journal of Economics*,
130(3), 1369–1420。**A**（标准引用）。
[6] Itskhoki, O., & Mukhin, D. (2021). Exchange rate disconnect
in general equilibrium. *Journal of Political Economy*, 129(8),
2183–2232. DOI: 10.1086/714447。**A**（LSE 全文直读）。
[7] Mundell, R. A. (1963). Capital mobility and stabilization
policy under fixed and flexible exchange rates.
*Canadian Journal of Economics and Political Science*, 29(4),
475–485。**A**（标准引用）。
[8] Balassa, B. (1964). The purchasing-power parity doctrine:
A reappraisal. *Journal of Political Economy*, 72(6), 584–596。
**A**（标准引用）。
[9] Chahrour, R., Cormun, V., De Leo, P., Guerrón-Quintana, P. A.,
& Valchev, R. (2024). Exchange Rate Disconnect Revisited.
NBER Working Paper No. 32596。**B**（摘要直读）。
[10] Kalemli-Özcan, Ş., & Varela, L. (2021, rev. Aug 2026).
Five Facts about the UIP Premium. NBER Working Paper No. 28923。
**B**（摘要直读）。
[11] Ma, C., Rebucci, A., & Zhou, S. (2025). A Nascent
International Financial Channel of China's Monetary Policy
Transmission. NBER Working Paper No. 34291。**B**（摘要直读）。
[12] Liu, Y., Shi, J., & Li, Y. (2026). The Impact of Federal
Reserve Monetary Policy Adjustments on RMB Exchange Rate
Fluctuations. *International Journal of Finance & Economics*,
31(3), 4073–4090. DOI: 10.1002/ijfe.70135。**B**（摘要直读）。
[13] Sun, Y. (2025). The effects of the counter-cyclical factor
on renminbi co-movements. *Journal of International Financial
Markets, Institutions and Money*, 101. DOI: 10.1016/j.intfin.2025.102144。
**B**（摘要直读）。
[14] Jiang, Z. (2026, rev. Aug 2026). Financial Interdependence
and Currency Internationalization. NBER Working Paper No. 35541。
**B**（摘要直读）。
[15] Kolasa, M., et al. (2025). Monetary policy and exchange
rate dynamics in a behavioral open economy model.
*Journal of International Economics*, 155, 104087.
DOI: 10.1016/j.jinteco.2025.104087。**B**（摘要直读；作者名单待补全）。
[16] Jermann, U., Wei, B., & Yue, V. Z. (2019). The Two-Pillar
Policy for the RMB. NBER Conference Paper, March 26, 2019.
SSRN 3360617。**B**（摘要直读；期刊版未核实）。
[17] De Grauwe, P., & Grimaldi, M. (2006). A Behavioral Finance
Model of the Exchange Rate with Many Forecasting Rules.
CESifo Working Paper No. 1849。**B**（摘要直读）。
[18] Jongen, R., Verschoor, W. F. C., Wolff, C. C. P., &
Zwinkels, R. C. J. (2012). Explaining dispersion in foreign
exchange expectations: A heterogeneous agent approach.
*Journal of Economic Dynamics and Control*, 36(5), 719–735.
DOI: 10.1016/j.jedc.2012.01.005。**B**（摘要直读）。
[19] Collodel, U. (2025). Interpreting the Interpreter: Can We
Model post-ECB Conferences Volatility with LLM Agents?
arXiv:2508.13635。**B**（摘要直读）。
[20] Vidler, A., & Walsh, T. (2025). Shifting Power: Leveraging
LLMs to Simulate Human Aversion in ABMs of Bilateral Financial
Exchanges, A bond market study. Proc. AAMAS 2025.
arXiv:2503.00320。**B**（摘要直读）。
[21] Frankel, J. A., & Froot, K. A. (1986). Understanding the
US dollar in the eighties: The expectations of chartists and
fundamentalists. *Economic Record*, 62, 24–38。**B**（转引）。
[22] Engel, C. (1996). The forward discount anomaly and the risk
premium: A survey of recent evidence. *Journal of Empirical
Finance*, 3(2), 123–192。**A**（标准引用）。
[23] Rogoff, K. (1996). The purchasing power parity puzzle.
*Journal of Economic Literature*, 34(2), 647–668。**A**（标准引用）。
