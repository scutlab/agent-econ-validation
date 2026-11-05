# AI 发展是否存在泡沫：理论、证据与 agent 验证路径

- 日期：2026-11-05（v1）
- 检索范围：公开检索（browser.search / browser.open），2023–2026 年文献优先
- 规则：论文来源优先；每个数字注明来源与可信度；拿不到的写"未获可靠来源"；
  拿不到全文的写明"未获全文"并给最好二手来源；区分"泡沫已证实"与
  "泡沫风险论证"，不把一方观点写成定论。
- 注意：本报告只回答"AI 是否泡沫"；用户同时问的"中国利率下行而汇率上行"
  由另一路调研处理。

## 0. 先说结论

这不是二元判断。2026 年严肃文献的主流立场是**分层判断**：

- Wang & Chen（2026，arXiv:2606.01575）："AI 最好被理解为一场真实的
  技术革命，同时带有局部泡沫动态，而不是纯粹的投机狂热或无泡沫的
  生产率奇迹。"
- 一篇 2026 年 4 月的方法论论文（arXiv:2604.25826）指出：通用技术
  采纳会使标准泡沫检测（GSADF）产生严重尺寸扭曲；剔除技术采纳因素后，
  2020–2025 年 AI 行情**没有**投机证据，而互联网泡沫的投机峰只限于
  1999 年 12 月至 2000 年 3 月。
- Caballero（2026，MIT）提出第三种可能：乐观估值即使日后修正，
  也可能留下永久的真实遗产（已安装的资本存量）。
- IMF（2025-10）与英格兰银行（2025-10）警告估值拉伸、存在修正风险，
  但 IMF 明确指出本轮**未由重杠杆驱动**，与互联网泡沫有结构性不同。
  两家机构都没有宣布"泡沫已证实"。

"AI 泡沫"一词在讨论中至少指四件不同的事（须先分清再争论）：
AI 的使用、AI 公司、科技股整体、数据中心与芯片支出。
本报告的证据大多指向第四件（支出）与第二件（模型层公司）的错配，
而非"AI 技术无用"。

## 1. 判断泡沫的理论工具箱

| 理论 | 核心机制 | 实证标准（怎么算"泡沫"） | 适用 AI 吗 |
|---|---|---|---|
| 1.1 明斯基金融不稳定假说（Minsky 1975《John Maynard Keynes》；1986《Stabilizing an Unstable Economy》；1992 工作论文 No.74） | 稳定滋生不稳定：繁荣期融资结构从对冲融资 → 投机融资（只能还息、靠再融资还本）→ 庞氏融资（连利息都还不起、靠资产升值续命）；"明斯基时刻"即再融资链断裂 | 债务/现金流比、利息保障倍数、杠杆率、融资结构中投机/庞氏占比 | 适用，但须区分：超大规模公司多为现金融资（IMF 指出），庞氏链主要在**新云厂商（neocloud）**一层：借重债买芯片、未来才有收入 |
| 1.2 金德尔伯格五阶段（Kindleberger《Manias, Panics, and Crashes》1978，承袭 Minsky） | 错位（displacement，真实技术冲击）→ 繁荣（信贷扩张）→ 亢奋（价格脱离基本面、"这次不一样"、欺诈丛生）→ 内幕抛售 → 恐慌/厌恶 | 定位当前所处阶段比预测顶部更可行；标志物：信贷增速、新入场者结构、"这次不一样"叙事、欺诈案件 | 适用：错位 = 生成式 AI（2022 年底 ChatGPT）；亢奋的标志物可观测（见 §2.2） |
| 1.3 席勒：叙事经济学 + CAPE（Shiller《Irrational Exuberance》2000；《Narrative Economics》2019；Campbell & Shiller 1988） | 泡沫定义：价格上涨的消息经心理传染扩散，放大"价格会继续涨"的故事，吸引更多投资者，形成自然庞氏结构；CAPE = 股价 / 过去 10 年平均实际盈利，平滑周期 | CAPE 历史分布：均值约 17.7、中位约 16.6；CAPE > 30 后续 10 年实际回报多为负或接近零；2000 年 3 月峰值 47.2（另有口径 44.19），1929 年 32.6 | 适用：CAPE 是最常用的跨周期估值锚；叙事传染（"AI 改变一切"）是本轮的核心机制，可直接用 agent 实验检验（见 §4） |
| 1.4 理性泡沫模型（Blanchard 1979；Blanchard & Watson 1982，NBER WP 945；Tirole 1982, 1985） | 即使理性预期下，价格 = 基本面价值 + 泡沫成分也可成立；泡沫成分是次鞅（期望以贴现率增长），可周期性崩溃后重生；不违反无套利 | 价格-股息比出现爆炸性根（explosive root）；泡沫成分须以贴现率增长 | 适用：为"理性投资者也参与泡沫"提供理论许可；是 GSADF 检测的理论基础 |
| 1.5 戈登增长模型与贴现率敏感性（Gordon & Shapiro 1956，承 Williams 1938） | P = D1 / (r − g)；分母 (r − g) 越小，价格越高、对 r 与 g 越敏感；g 接近 r 时估值发散 | 反推市场隐含的长期增长率 g，与经济长期增速对比；r 上升 1 个百分点对高增长股的杀伤远大于成熟股（如 r=8%、g=6% 时 r→9% 可使价格跌约 1/3） | 非常适用：AI 公司的现金流重心在多年以后（久期极长），是贴现率最敏感的资产；利率路径是本轮估值的第一变量 |
| 1.6 托宾 Q（Kaldor 1966 首提；Tobin 推广） | Q = 公司市值 / 资产重置成本；Q > 1 意味着买公司比新建资产贵，刺激投资；Q < 1 则相反 | 市场整体 Q：2000 年一季度峰值 2.15，2009 年一季度 0.66（据 WSO 转述）；Q 持续 > 1 且走高 = 估值拉伸信号 | 部分适用：对芯片/数据中心等重资产层有效；对模型层（无形资产为主）失效——重置成本无法衡量模型、数据与人才 |
| 1.7 投资驱动型泡沫 / q 理论 + 投机性增长（Caballero 2026，MIT 工作论文） | 高 Q 驱动投资扩张；Caballero 的新模型：乐观估值→投资加速→资本存量扩大→收入向高储蓄的资本所有者转移→利率下降→可能落入自我维持的高资本稳态；若学习（证伪）来得太快，转型失败 | 投资/GDP、资本存量增速、利率反馈；区分三个对象：技术是否真实、峰值估值是否维持、繁荣期安装的资本是否留存 | 适用：这是唯一严肃论证"泡沫也可能留下好遗产"的模型；直接对应 AI 的 capex 之争 |
| 1.8 杠杆周期（Geanakoplos 2003；Geanakoplos & Fostel 2008 AER；Geanakoplos 2022 Cowles DP 2370） | 均衡同时决定利率与杠杆（保证金/抵押率）；乐观者借得越多、资产价格越高；坏消息→波动率上升→保证金收紧→乐观者被迫抛售→价格再跌（财富从乐观者向悲观者再分配） | 保证金/抵押率、杠杆倍数、抵押品稀缺度；价格 = 现值 + 抵押价值（p = PV + CV），抵押价值本身可制造泡沫 | 适用：检测重点是**融资结构**而非股价本身；本轮的观测点是新云厂商债务、超大规模发债、私人信贷（见 §2.2） |
| 1.9 适应性市场假说（Lo 2004 J. Portfolio Management；2005；2017《Adaptive Markets》） | 市场效率是演化的、依赖环境的：竞争、适应、自然选择；行为偏差是曾适应的启发式，在环境剧变时失效；策略会衰减（被模仿耗尽） | 效率随时间与环境变化，不存在永恒有效的策略；用滚动窗口检验回报可预测性的时变 | 适用作元框架：解释为何同一市场在不同时期既可有效又可泡沫；不直接给出泡沫判定数 |
| 1.10 泡沫计量检测：SADF/GSADF + LPPL | Phillips, Wu & Yu（2011）SADF、Phillips, Shi & Yu（2015）GSADF：递归右尾 ADF 检验，检测并标注爆炸性价格行为，无需事先指定基本面；Sornette 的 LPPL：对数周期幂律看超指数增长 + 振荡 | 拒绝单位根原假设 → 至少存在一段亢奋期；BSADF 序列可标注泡沫起止 | 适用但有 2026 年新批评：arXiv:2604.25826 证明通用技术采纳会使基本面价格本身局部爆炸，导致 GSADF 尺寸扭曲；须先做"基本面–投机分解"再检验 |
| 1.11 互联网泡沫对比框架（基准方法） | 以 1995–2000 为参照系，逐项对比：估值倍数、盈利质量、杠杆、集中度、IPO 质量 | 纳斯达克综合市盈率 2000 年 3 月约 175–200 倍；纳斯达克 100 前瞻市盈率 60.1 倍；1999–2000 年上市科技公司 86% 不盈利；纳斯达克峰值后跌 78% | 适用作基准，但须注意口径（前瞻 vs  trailing 市盈率不可混比；见 §2.2 对比表） |

## 2. 最新论文与实证证据

### 2.1 论文与严肃分析（2023–2026）

| # | 文献 | 性质 | 一句话结论 |
|---|---|---|---|
| 1 | Wang, Q. & Chen, Z. (2026). Boom, Bubble, or Buildout? A Multi-Method Evaluation of Whether Artificial Intelligence Is in an Ongoing Financial Bubble. arXiv:2606.01575（2026-06-01 提交） | 预印本（未同行评议） | 提出五支柱诊断框架（基本面估值、残差亢奋检验、SADF/GSADF、LPPL/HLPPL、情绪与发行、capex 回收）；结论：真实技术革命 + 局部泡沫动态；美国私人 AI 投资 2025 年达 2859 亿美元（Stanford AI Index 2026）；高盛模型：AI capex 2026 年约 7650 亿美元，2031 年约 1.6 万亿美元 |
| 2 | Caballero, R. J. (2026). Speculative Growth and the AI "Bubble". MIT 工作论文（初稿 2025-12-17） | 工作论文（MIT/NBER 作者） | 提出第三种可能：乐观估值即使日后修正，也可能留下永久真实遗产；区分技术是否真实、峰值估值是否维持、繁荣期安装的资本是否留存三个不同问题 |
| 3 | General-Purpose Technology and Speculative Bubble Detection (2026-04-29). arXiv:2604.25826 | 预印本 | 通用技术采纳使 GSADF 检测严重尺寸扭曲；做基本面–投机分解后，2020–2025 年 AI 行情无投机证据，互联网泡沫的投机峰只限 1999-12 至 2000-03 |
| 4 | Cao, C. (2025). Bubbles Detection of Asset Price Based on GSADF Method: A Case Study of NVIDIA. Springer, ICEMGD 2024 会议论文集 | 会议论文（摘要级，未获全文） | 2024 年 2–3 月 NVDA 股价与市盈率出现偏离基本面的泡沫行为，但作者认为源于 AI 转型的新历史阶段、经济上合理 |
| 5 | Eteman (2024). The speculative bubble effect of artificial intelligence on the stocks of the "Magnificent Seven"（据 2026 年综述转述） | 期刊论文（转述） | GSADF + 波动溢出分析：NVDA 与 Tesla 出现 AI 驱动的投机泡沫，并向其他科技股溢出波动 |
| 6 | AI Bubbles with Large Language Models (2026-03-16). CUHK 工作论文，SSRN 6426761 | 工作论文 | LLM agent 参与理性与非理性泡沫：Moinas-Pouget 泡沫博弈中，即使存在唯一无交易均衡，agent 仍做投机交易；推理能力增强减少但不消除非理性泡沫；agent 因简化预期形成错误信念、对框架敏感 |
| 7 | TwinMarket: A Scalable Behavioral and Social Simulation for Financial Markets (2025). arXiv:2502.01506 | 预印本 | LLM 多 agent 股市模拟：个体行为经社交互动涌现泡沫与衰退等集体现象；BDI（信念-欲望-意图）框架组织 agent 认知 |
| 8 | Hansen et al. (2025). Financial Stability Implications of Generative AI: Taming the Animal Spirits. Dallas Fed 会议论文（初步未完成稿） | 央行会议论文 | LLM agent 复现 Cipriani & Guarino（2009）羊群实验：agent 的羊群行为少于人类，提示 AI 建议普及可能减少由羊群导致的泡沫；但 agent 未能充分计入私人信息的累积 |
| 9 | Cividino, D., Westphal, R. & Sornette, D. (2023). Multiasset financial bubbles in an agent-based model with noise traders' herding. *Physical Review Research* 5, 013009 | 同行评议期刊 | 多资产 ABM：基本面交易者 + 追随趋势的模仿型噪声交易者（Ising 模型）；模仿倾向超过临界值后，内生泡沫出现并可跨资产级联 |
| 10 | Mayanga, K. (2026). Big Tech Companies' Massive Capex Spending. *Scientia Moralitas* 11(1) | 低级别多学科期刊（注明） | 七巨头 2025 年 AI 投资超 4000 亿美元，2026 年预计近 7000 亿美元；支出与回报之间存在显著缺口，存在过度投资风险 |
| 11 | Cahn, D. (2024). AI's $600 Billion Question. Sequoia Capital | 业界分析（非学术） | 方法：NVDA 数据中心收入 run rate ×2（数据中心总成本）×2（客户所需毛利）= AI 行业需产生的年收入；2023 年底缺口 $200B，2024 年中 $600B；实际 AI 收入当时约 $100B |
| 12 | MIT NANDA (2025). The GenAI Divide: State of AI in Business 2025 | 机构报告（初步发现） | 约 95% 企业生成式 AI 试点未产生可衡量的损益回报；主因是"学习鸿沟"（工具未嵌入工作流）而非模型质量。**但该数字受质疑**：Wiblin（2026，80,000 Hours）逐行重读指出约 80% 受访组织根本没跑过定制试点，分母有误；McKinsey 2026 跟进显示 37–39% 大企业报告了 EBIT 影响——95% 作为"试点失败率"是错的，但"回报慢于预期"的诊断大致成立 |
| 13 | IMF (2025-10). Global Financial Stability Report, "Shifting Ground beneath the Calm"；IMF (2026-10). GFSR | 机构报告 | 2025-10：美股相对公允价值模型高估约 10 个百分点；IT 行业占标普 500 的 35%（与互联网泡沫相当），Mag 7 占 33%；但 AI 投资自 2022 年以来仅增不到 GDP 的 0.4%（互联网泡沫 1995–2000 年为 1.2%），且主要由现金充裕企业出资、未由重杠杆驱动。2026-10：14 笔交易中，超大规模向较弱 AI 公司投入约 3000 亿美元股权 + 约 6500 亿美元债务，换取 1.4 万亿美元未来收入承诺；Mag 7 占标普 500 超 35% |
| 14 | Bank of England, Financial Policy Committee (2025-10-08 会议记录） | 央行 | 股票估值拉伸；CAPE 隐含的收益率接近 25 年最低，与互联网泡沫峰值相当；标普 500 前五大公司占比近 30%，为 50 年最高；AI 预期转向、电力/数据/商品供应链瓶颈或概念突破都可能冲击估值 |
| 15 | Federal Reserve (2025-11). Financial Stability Report | 央行 | 资产估值高企；"AI 情绪转向"被市场联系人列为最常提及的风险之一 |

### 2.2 关键实证数据点（每个数字带来源；快照日期注明）

**估值与集中度**

| 指标 | 数值 | 来源与可信度 |
|---|---|---|
| 标普 500 CAPE | 约 40.7（2026-10-01）；历史均值约 17.7；2000 年峰值 44.19（1999-12） | 多源一致（Shiller 数据库经多家转述）；CAPE 本身是公开指标 |
| 纳斯达克 100 前瞻市盈率 | 约 60.1 倍（2000-03 峰值）vs 约 19.5–22.4 倍（2026-10-30） | FactSet 经多家转述；注意前瞻口径与 trailing 不可混比 |
| 纳斯达克综合 trailing 市盈率 | 约 175–200 倍（2000 年峰值，口径有争议：WSJ 称 175 倍，"200 倍"为约数） | 历史数据，多源一致 |
| 科技板块前瞻市盈率 | 约 30 倍（2026 年）vs 约 50 倍（2000 年峰值） | 行业转述 |
| 标普 500 集中度 | Mag 7 占约 33–35%；IT 行业占 35%；前 10 大公司占 36–40%，高于互联网泡沫时期的 27% | IMF GFSR 2025-10 / 2026-10；多源一致 |
| NVDA | 市值约 4.93 万亿美元；市盈率约 25.6 倍；股价约 200 美元，52 周 164–243 美元；近一个月 −14.5%（Finnhub，2026-11-05 检索时快照） | Finnhub 实时数据；快照价，非收盘定值 |
| NVDA 盈利 | FY2026 净利润超 1200 亿美元（据 itmagazine 报道） | 弱来源（行业媒体转述），需财报核对 |
| Cisco 对比 | 2000 年峰值市值约 5000–5550 亿美元，净利润仅 26.7 亿美元，市盈率约 130–200 倍（口径不同）；峰值后跌约 86–88% | 多源一致的历史数据 |

**支出与收入缺口**

| 指标 | 数值 | 来源与可信度 |
|---|---|---|
| 五大超大规模 capex | 2026 年合计指引约 7200–7450 亿美元，2025 年约 4100 亿美元；Alphabet 单家 2026 年指引 1950–2050 亿美元 | 公司指引经多家转述 |
| 高盛 AI capex 模型 | 2026 年约 7650 亿美元，2031 年约 1.6 万亿美元 | Wang & Chen（2026）引高盛 Global Institute 2026 |
| 数据中心总需求 | 到 2030 年约 7 万亿美元（McKinsey 2025） | 转述 |
| 美国私人 AI 投资 | 2025 年 2859 亿美元，超中国 23 倍 | Stanford AI Index 2026（经 Wang & Chen 2026 引用） |
| Sequoia 缺口 | 2024 年中约 $600B；据 Substack 转述，Cahn 2025 年底更新至约 $840B | 原文 $600B 可靠（Sequoia 官网）；$840B 更新为弱来源转述 |
| OpenAI 收入 | 2025 年入账收入 13.07 亿美元，经营亏损约 20.92 亿美元；2026 年 9 月底年化收入约 500 亿美元（净口径；此前流传的 700 亿美元为毛口径，已纠正）；2026 年收入计划约 360 亿美元 | FT / WSJ / Bloomberg 经多家转述；OpenAI 未公布经审计财报 |
| OpenAI 现金流与估值 | 2026–2030 年负自由现金流计划 2780 亿美元；累计现金消耗到 2030 年约 6650 亿美元（WSJ/The Information 转述）；2026 年 3 月融资 1220 亿美元、估值 8520 亿美元；估值谈判约 1.2–1.4 万亿美元 | 转述，未经审计；谈判价非成交价 |
| OpenAI 支出承诺 | 约 1.4 万亿美元数据中心承诺（8 年期） | 多家转述 |
| Anthropic | 2026 年 Q3 收入 16.8 亿美元、环比约 +45%、调整后经营利润率 11% | 弱来源（Substack 报道），需核对 |
| xAI | 2025 年收入 32 亿美元、经营亏损 63.5 亿美元（SpaceX S-1 披露） | 弱来源（Medium 转述 S-1），需核对 |

**融资结构与信贷（杠杆周期视角）**

| 指标 | 数值 | 来源与可信度 |
|---|---|---|
| CoreWeave | 债务约 500 亿美元；2030 年债券收益率约 16%（2026-10，单周跳升 500bp）；2025 年收入 51 亿美元、净亏损 12 亿美元；收入积压 1042 亿美元（2026 年 Q2 末）+ Q3 初新增超 250 亿美元；从未盈利（LSEG） | Reuters 2026-10-16 报道；可靠 |
| Gartner 新云厂商 | 约 100 家新云厂商中最暴露于"收入–支出失衡"；预计到 2030 年 80% 将停止独立运营 | Gartner（经 Reuters 转述） |
| 循环融资 | NVDA：向 OpenAI 投资 300 亿美元 + 俄亥俄数据中心担保最高 1050 亿美元；向 Anthropic 最高 100 亿美元；向 CoreWeave 投资 20 亿美元 + 兜底购买未售产能至 2032 年 4 月 | Reuters / The Conversation 2026-10；多源一致 |
| 超大规模发债 | 2025 年超大规模债券发行总额超 1000 亿美元，多为 5 年以上期限 | BIS（经新闻分析转述） |
| 信贷利差（高收益债 OAS 等） | 未获可靠来源 | 本次检索未拿到可引用的时点数字，需 FRED（ICE BofA 指数）另查 |
| IPO 与一级市场热度 | OpenAI 2026 年 3 月融资 1220 亿美元；IPO 数量/破发率等系统性数字未获 | 部分有来源；系统性 IPO 数据未获可靠来源 |

**官方与市场人士表态（2025–2026）**

- Sam Altman（2025-08，The Verge 首报）："投资者整体对 AI 过度兴奋"，"泡沫发生时，聪明人会对一个真实内核过度兴奋"；部分初创估值"疯狂"。
- Sundar Pichai（2025-11，BBC）："市场存在非理性因素"，谷歌也无法免疫。
- Jerome Powell（2025-10）：将 AI 与互联网泡沫年代类比（据转述）。
- Ray Dalio（2026-01）：AI 繁荣处于"泡沫早期阶段"。
- Jeremy Grantham（GMO，2026-01）：美股符合该公司对泡沫的定义，拿 AI 类比铁路（变革性技术仍可崩盘）。
- Michael Burry（据 Substack 报道其观点）：超大规模按 5–6 年折旧 GPU，经济寿命实为 2–3 年，2026–2028 年利润高估约 1760 亿美元（**弱来源**：二手转述其论点，需原文核对）。

### 2.3 正反两方小结

**泡沫论的证据**：capex 增速远超可观测变现（Sequoia 缺口 6 倍）；模型层亏损巨大
（OpenAI 2025 年经营亏损约 209 亿美元、累计现金消耗计划 6650 亿美元）；
循环融资使"真实需求"难以辨别；新云厂商高杠杆 + 债券收益率 16%；
CAPE 约 40.7 为 155 年第二高；集中度超互联网泡沫时期；MIT 95% 试点
回报落空（虽数字受质疑，回报慢的诊断大致成立）。

**非泡沫论的证据**：头部公司真实盈利（NVDA FY2026 净利润超 1200 亿美元，
Cisco 2000 年仅 26.7 亿美元）；前瞻市盈率约 20 倍 vs 2000 年 60 倍；
AI 投资占 GDP 不到 0.4%（互联网泡沫 1.2%）；主要由现金出资、杠杆低；
剔除通用技术采纳后 GSADF 无投机证据（arXiv:2604.25826）；
收入增速极快（OpenAI 年化收入 9 个月从 200 亿升至 500 亿美元）。

**学界共识句**：没有哪篇严肃论文宣布"泡沫已证实"；也没有哪篇证明
"绝无泡沫"。共识是**分层、分环节判断**：半导体与超大规模层有真实盈利
支撑，模型层与新云厂商层的财务可持续性最可疑，系统性风险取决于
杠杆与集中度，而非单一估值倍数。

## 3. 验证"AI 是否泡沫"需要的数据清单

| 指标 | 来源 | 频率 | 公开可得 |
|---|---|---|---|
| 个股与指数价格、市盈率、市销率 | Finnhub / 雅虎财经 / WRDS CRSP | 日 | 是（前者免费层有限） |
| CAPE 与 10 年实际盈利 | Shiller Yale 数据库（econ.yale.edu） | 月 | 是 |
| 超大规模 capex、自由现金流、折旧年限 | 公司 10-Q/10-K、财报电话会 | 季 | 是 |
| AI 收入拆分（云 AI、订阅、API） | 财报、The Information、公司披露 | 季 | 部分（多为转述） |
| GPU 出货量、利用率、价格 | NVDA 财报、TrendForce、Dell'Oro | 季 | 部分 |
| 数据中心在建面积、电力签约 | McKinsey、IEA、Dell'Oro、公司披露 | 年/季 | 部分付费 |
| 信贷利差（高收益 OAS、投资级 OAS） | FRED（ICE BofA 指数） | 日 | 是 |
| 新云厂商债务、债券收益率、CDS | 公司财报、TRACE、Markit CDS | 日 | 部分 |
| 一级市场融资额与估值 | PitchBook、Crunchbase | 持续 | 付费为主 |
| IPO 数量、募资额、破发率 | Renaissance Capital、Jay Ritter 数据 | 月 | 是 |
| 叙事/情绪 | 新闻文本、Google Trends、AAII 情绪调查 | 日/周 | 是 |
| 期权隐含波动率、卖空、保证金 | CBOE、FINRA、NYSE | 日/月 | 是 |
| 生产率与 GDP 贡献 | BLS、BEA | 季 | 是 |
| 泡沫检测复算 | 自行跑 SADF/GSADF（R 包 exuber / Python pysadf）+ LPPL | — | 代码开源 |

## 4. Agent / ABM 验证路径：初步判断

### 4.1 已有的方法与结论

- **ABM 经典路线**：Brock & Hommes（1998）信念切换模型（基本面交易者
  vs 趋势追随者，内生切换可产生类泡沫的混沌价格）；Lux（1995）、
  Cont & Bouchaud（2000）异质性 agent 产生肥尾收益；Santa Fe 人工股市
  （Palmer et al. 1994；LeBaron et al. 1999）；Cividino et al.（2023）
  多资产 Ising 羊群模型（见 §2.1 #9）。
- **实验室实验**：Smith, Suchanek & Williams（1988）经典泡沫实验
  （已知基本面下仍出现泡沫与崩盘）；Moinas & Pouget（2013, 2016）
  泡沫博弈（基本面为零的资产，分离理性与非理性泡沫）；
  Cipriani & Guarino（2009）羊群实验。
- **LLM agent（2025–2026 已有人做）**：
  - "AI Bubbles with LLMs"（2026）：LLM agent 参与理性与非理性泡沫；
    推理能力增强减少但不消除非理性泡沫；agent 因简化预期形成错误信念、
    对框架敏感；能识别多重均衡并协调到投机均衡。
  - TwinMarket（2025）：LLM 多 agent 股市模拟涌现泡沫与衰退。
  - Dallas Fed Hansen et al.（2025）：LLM agent 羊群行为**少于**人类，
    提示 AI 建议普及可能减少泡沫；但 agent 未充分计入私人信息累积。
  - 行为一致性验证（arXiv:2602.07023，2026）：LLM agent 的交易风格切换
    与行为金融理论只有部分一致。
  - 结论：**"用 LLM agent 研究泡沫"不是空白，已有 2025–2026 年的
    直接先例，且结论并不一致**（一派发现 agent 也会泡沫，另一派发现
    agent 比人更少羊群）——这正是值得复现的点。

### 4.2 本项目可做的三层设计（初步判断，非执行承诺）

- **第一层（单 agent，可立即做，与现有脚手架兼容）**：
  复现 Moinas-Pouget 泡沫博弈（照搬 CUHK 2026 设计）：基本面为零的资产，
  agent 决定是否以价格 P 买入，买入后以 10P 转售；有价格上限时存在唯一
  无交易均衡（任何交易 = 非理性泡沫），无上限时允许多重均衡。
  判定：有上限臂的交易率、推理链中的投机/羊群理由占比；
  对照 CUHK 的 LLM 结果与 Moinas-Pouget 的人类结果。
  可直接用现有 persona × DeepSeek/Gemini 跑，成本与现有实验相当。
- **第二层（单 agent，叙事传染）**：Shiller 叙事实验——同一资产，
  不同叙事框架（"AI 改变一切" vs 中性基本面描述 vs 悲观叙事），
  测出价/持有意愿与叙事强度梯度；另设"朋友致富"社会信息臂
  （Kindleberger 引言的操作化）。判定：叙事是否系统性移动出价，
  且移动幅度是否超过基本面信息臂。
- **第三层（多 agent，阶段四）**：TwinMarket 路线——LLM agent 在模拟股市
  中交易 + 社交网络互动，看泡沫/崩盘是否涌现；与 ABM 基线
  （Brock-Hommes 信念切换）对照。此层需要技术选型，用户另行拍板。

### 4.3 局限与诚实说明

- LLM 参与泡沫博弈 ≠ 人类泡沫：agent 可能复述已知的泡沫史（记忆化），
  需 novel 变体（改写资产、改写叙事）做稳健性检验。
- 单 agent 实验验的是**信念形成**，不是价格形成；价格形成需要市场
  微观结构（做市商、订单簿、杠杆、保证金），缺失会低估崩盘机制。
- 判定标准建议：沿用项目三条（方向一致、分布可比、persona 梯度存在），
  再加一条"均衡识别"（有上限无交易均衡下交易率对 0 的偏离度）。
- 泡沫的最终判定是计量问题（GSADF/LPPL/基本面分解），agent 实验
  只能回答"信念与羊群机制是否成立"，不能单独定论"AI 是泡沫"。

## 5. 未解决项

1. 信贷利差（高收益 OAS、投资级 OAS）的时点数字未获——需查 FRED。
2. IPO 数量、募资额、破发率的系统性数字未获——需 Renaissance Capital / Ritter 数据。
3. NVDA FY2026 净利润"超 1200 亿美元"为弱来源，需财报核对。
4. Anthropic 2026 年 Q3 收入、xAI 2025 年收入、Burry 折旧论点（$176B）、
   Sequoia $840B 更新，均为二手转述，需原文核对。
5. Cao（2025）GSADF 论 NVDA 只读到摘要——需全文核对检验窗口与结论。
6. Wang & Chen（2026）五支柱框架的逐项复算未做（需股价、财报、情绪数据，
   见 §3 清单）。
7. Eteman（2024）只经综述转述——需原文核对样本期与检验方法。

## 参考文献

[1] Wang, Q. & Chen, Z. (2026). Boom, Bubble, or Buildout? arXiv:2606.01575.
预印本（摘要直读）。
[2] Caballero, R. J. (2026). Speculative Growth and the AI "Bubble".
MIT 工作论文（摘要直读）。
[3] General-Purpose Technology and Speculative Bubble Detection (2026).
arXiv:2604.25826（摘要直读）。
[4] Cao, C. (2025). Bubbles Detection of Asset Price Based on GSADF Method:
A Case Study of NVIDIA. Springer, ICEMGD 2024 会议论文集（摘要直读）。
[5] Eteman (2024). The speculative bubble effect of AI on Mag-7 stocks
（经 2026 年综述转述，未获全文）。
[6] AI Bubbles with Large Language Models (2026). CUHK 工作论文，
SSRN 6426761（摘要与正文节选直读）。
[7] TwinMarket (2025). arXiv:2502.01506（摘要直读）。
[8] Hansen et al. (2025). Financial Stability Implications of Generative AI.
Dallas Fed 会议论文（摘要直读）。
[9] Cividino, D., Westphal, R. & Sornette, D. (2023). *Physical Review
Research* 5, 013009（摘要直读）。
[10] Mayanga, K. (2026). Big Tech Companies' Massive Capex Spending.
*Scientia Moralitas* 11(1)（摘要直读；低级别期刊）。
[11] Cahn, D. (2024). AI's $600 Billion Question. Sequoia Capital（业界分析）。
[12] MIT NANDA (2025). The GenAI Divide: State of AI in Business 2025
（机构报告；95% 数字受 Wiblin 2026 批评，见正文）。
[13] IMF (2025-10; 2026-10). Global Financial Stability Report（机构报告）。
[14] Bank of England (2025-10-08). Financial Policy Committee 会议记录。
[15] Federal Reserve (2025-11). Financial Stability Report。
[16] Minsky, H. P. (1986). *Stabilizing an Unstable Economy*；
Minsky (1992). The Financial Instability Hypothesis, Working Paper No. 74.
[17] Kindleberger, C. P. (1978). *Manias, Panics, and Crashes*.
[18] Shiller, R. J. (2000). *Irrational Exuberance*；Shiller (2019).
*Narrative Economics*；Campbell, J. Y. & Shiller, R. J. (1988).
[19] Blanchard, O. J. (1979)；Blanchard, O. J. & Watson, M. W. (1982).
Bubbles, Rational Expectations and Financial Markets. NBER WP 945.
[20] Gordon, M. J. & Shapiro, E. (1956)；Williams, J. B. (1938).
*The Theory of Investment Value*.
[21] Tobin, J.；Kaldor, N. (1966)（Q 比率首提）。
[22] Geanakoplos, J. (2003)；Geanakoplos, J. & Fostel, A. (2008).
Leverage Cycles and the Anxious Economy. *American Economic Review*；
Geanakoplos, J. (2022). Cowles DP 2370.
[23] Lo, A. W. (2004). The Adaptive Markets Hypothesis. *Journal of
Portfolio Management*；Lo (2017). *Adaptive Markets*.
[24] Phillips, P. C. B., Shi, S. & Yu, J. (2015). Testing for Multiple
Bubbles. *International Economic Review*；Phillips, P. C. B., Wu, Y.
& Yu, J. (2011). Explosive Behavior in the 1990s NASDAQ. *Journal of
Econometrics*.
[25] Brock, W. A. & Hommes, C. H. (1998). Heterogeneous Beliefs and
Routes to Chaos in a Simple Asset Pricing Model. *Journal of Economic
Dynamics and Control*；Smith, V. L., Suchanek, G. L. & Williams, A. W.
(1988). Bubbles, Crashes, and Endogenous Expectations. *Econometrica*；
Moinas, S. & Pouget, S. (2013, 2016)（泡沫博弈）。
