# 基线数据来源审计（2026-11-05）

原则（用户拍板）：基线数字优先采用已有论文中报告的数据，便于对比；
每个数字注明来源论文、获取路径、可信度等级与核查方法。
等级：A = 本人直接在该论文正文读到；B = 被另一篇论文/预印本
引用或转述（注明转引链）；C = 非论文来源（教学幻灯片、博客等），
不进入正式基线。

## A 级：Horton 原文（直接读到）

来源：Horton, Filippas & Manning《Large Language Models as Simulated
Economic Agents》，arXiv:2301.07543v2（2026 年 8 月更新版），
同为 NBER Working Paper No. 31122。获取路径：arXiv HTML 全文逐节读到。

| 数字 | 位置 | 核查方法 |
|---|---|---|
| 雪铲：Kahneman 等 1986 原实验约 82% 判不公平 | §2.1 | 打开 arXiv v2 §2.1 首段 |
| 独裁者：Charness & Rabin 真人选 Left 向量 v_CR = (.52, .67, .27, 1, .78, .68) | §2.2 | §2.2.1 文中公式段 |
| 现状偏见 AI logit：DeepSeek 现状系数 0.762，距离系数 -0.029 | §2.3 Table 1 | Table 1 第 2、3 列 |
| Oprea：四重模式在 mirror（无风险）条件下同样出现 | §2.4 | §2.4 全节 |
| 雇佣替代 AI 回归：工资 +1.314（无参照）/+1.984（有参照）美元/小时；经验 +0.081/+0.265 年 | §2.5 Table 2 | Table 2 及正文解读 |

说明：82% 与 v_CR 是 Horton 转引自 Kahneman 等（1986）与
Charness & Rabin（2002）的原文数据，属于"论文转引论文"，
链条完整；如需再上一级核查，应查这两篇原文。

## A 级：Hauert 等 2002（合作起源，自愿公共品）

- 来源：Hauert, De Monte, Hofbauer & Sigmund (2002).
  Volunteering as Red Queen Mechanism for Cooperation in Public Goods
  Games. *Science*, 296(5570), 1129–1132.
  DOI: 10.1126/science.1070582。
- 获取路径：Science 摘要页直读；全文见作者 Karl Sigmund
  维也纳大学主页公开文本（02Sc_hauert.pdf / 1129.htm）。
- 已核实数字：模型 Pd = r·nc/S、Pc = Pd − 1（投资归一化为 1）；
  成立条件 r > 1、0 < σ < r − 1；图注参数 N = 5、r = 1.8/σ = 0.5
  与 r = 3/σ = 1；算例 N = 10、r = 5（A 组 8 合作 2 背叛→
  合作者 3、背叛者 4；B 组 2 合作 8 背叛→合作者 0、背叛者 1；
  平均背叛者 1.6、合作者 2.4，Simpson 悖论）。
- 核查方法：Science 摘要页；或打开作者主页全文核对模型段与图注。

## B 级：被其他论文/预印本报告的数据

### 独裁者博弈：Engel（2011）元分析

- 原论文：Engel, C. (2011). Dictator games: A meta study.
  *Experimental Economics*, 14(4), 583–610.
  DOI: 10.1007/s10683-011-9283-7。
- 数字（2026-11-05 抓取核实）：616 个处理、20,813 名独裁者；
  总均值（未加权）28.35%；随机效应 meta 分析 28.3%；
  分布：36.11% 给 0、16.74% 均分、5.44% 全给。
- 获取路径：Springer（付费墙）；经 Engel 本人讲授幻灯片、
  PMC 同行评议论文、多篇论文转述核实（多源一致），原表未直接读。
- 核查方法：DOI 直达 Springer 原文；或打开 PMC10667727 查转述。
- 注意事项：Engel 的固定效应元分析给出 20.4%，但**仅限 445 个
  有标准误的处理**，引用 20.4% 时必须注明此口径；
  论文数二手来源有 129 篇与 131 篇两种说法，未解决——
  引用时只写"616 处理"，不写论文数。

### 最后通牒博弈：Oosterbeek 与 Camerer 必须分开写（2026-11-05 抓取纠正）

- Oosterbeek, Sloof & van de Kuilen（2004）元分析
  （*Experimental Economics*, 7(2), 171–188；
  DOI: 10.1023/B:EXEC.0000026978.14316.74）：37 篇论文、75 个结果；
  平均出价 40%、平均拒绝率 16%。该文**没有**"出价→拒绝率"
  曲线表，只给平均数 + 回归方向。获取路径：摘要直读 + 多篇
  同行评议论文转述；全文回归表未直接读。
- "低于 20% 的提议约 50% 被拒"出自 Camerer《Behavioral Game
  Theory》（2003）表 2.2、2.3 的综述，不是 Oosterbeek 的数字；
  原书未获全文，经国立台湾大学、博洛尼亚大学等四份独立讲义
  一致核实（众数/中位出价 40–50%、均值 30–40%）。正式引用
  须写"转引自 Camerer (2003) 表 2.2/2.3，经多份讲义核对"，
  不得写成直读；两处来源不得混写。
- 独立佐证（多源一致）：Meyer（1992）20% 提议拒绝率 68%、
  30% 拒绝率 39%；Sanfey 等（2003）10%/20%/30% 提议拒绝率
  约 60%/50%/10%。报告里写"约 50%"而非精确值。

### 禀赋效应：WTA/WTP 约 2.1–2.6 倍

- 原论文：Kahneman, Knetsch & Thaler (1990). Experimental tests of
  the endowment effect and the Coase theorem.
  *Journal of Political Economy*, 98(6), 1325–1348.
  DOI: 10.1086/261737。
- 数字（2026-11-05 抓取，经 DellaVigna 2009 JEL 综述转述核实，
  JPE 原文未直接读）：中位数 WTA $5.75 vs WTP $2.25
  （比值约 2.6）出自**第一组 mug 实验**（Cornell，卖方 vs 买方，
  无 chooser 组）；WTA $7.12 / chooser $3.12 / WTP $2.87
  （比值约 2.5）出自**实验 6**（Simon Fraser 大学，77 名学生，
  三组设计；预期交易 12.5 笔，实际仅 3 笔）。
- 关键点：chooser（$3.12）接近买方（$2.87）而远低于卖方
  （$7.12），说明差异来自"拥有"而非"对 mug 的偏好"——
  这是该实验的设计精髓，报告中应保留 chooser 这一组，
  不得只报 $7.12/$2.87 两数。
- 变体说明：个别二手复述称 Cornell 实验每轮卖方中位 $5.25、
  买方中位 $2.25–$2.75；与 DellaVigna 的 $5.75 表述不完全一致，
  可能源于论文内不同轮次的数字——引用以 DellaVigna 为准，
  可脚注此变体。
- 获取路径：在 DellaVigna（2009）《Journal of Economic Literature》
  综述中读到对 KKT 实验的转述（同行评议综述，属于论文来源）。
- 核查方法：JEL 综述原文；或 DOI 直达 JPE 原文。

### 自愿公共品人类实验：Semmann 等（2003）

- 原论文：Semmann, Krambeck & Milinski (2003). Volunteering leads
  to rock–paper–scissors dynamics in a public goods game.
  *Nature*, 425, 390–393. DOI: 10.1038/nature01986。
- 已核实（2026-11-05 抓取，Nature 全文 OCR 直读）：
  280 人、20 组 × 14 人、57 轮；每轮随机选 6 人决策；
  起始 €10，loner 与贡献均为 €1.25，池 ×3.6 平分；
  最小组规模 2 人（1 人加入自动转为 loner）。
  操纵检验：第 8 轮三种 staged 方案下预测策略均为最频繁
  （p < 0.004，n = 20 组）；随后 50 轮预测的方向切换显著
  多于非预测切换（p < 0.001，配对 t = 6.588）。
  后 30 轮平均频率：loner ≈ 32%、合作者 ≈ 30%、背叛者 ≈ 38%
  （轮 21–35：32.22/30.11/37.67%；轮 36–50：32.39/29.06/38.56%）。
  与模型预测比较：实测 loner 33% 显著低于模型预期的 ≥42%
  （p = 0.003）；加入者中合作 43.48% 显著高于预期的 38%
  （p = 0.011）；长期平均收益：背叛者 €1.46、合作者 €1.32、
  loner €1.25。
- 获取路径：Nature 摘要页直读；全文经 Academia.edu PDF 文本读取
  （检索 "280"、"32.22"、"1.25"、"3.6"）；数字经正文与 Methods
  两处交叉核对。
- 口径提醒：Semmann 参数（6 人、×3.6、€1.25）与脚手架
  hauert 参数（N=5、r=3、σ=1）不一致；对照报告须写明
  "参数归一化，非原文复现"，或用 semmann 参数臂对照。
  Figure 3 逐轮曲线未取，不影响"循环方向 + 稳定水平"结论。

### 现状偏见：S&Z 1988 原文（2026-11-05 抓取，原文直读）

- 来源：Samuelson & Zeckhauser (1988). Status Quo Bias in Decision
  Making. *Journal of Risk and Uncertainty*, 1(1), 7–59。
  JSTOR: https://www.jstor.org/stable/41760530
- 获取路径：JSTOR 原文经 Internet Archive 公开 OCR 文本
  （检索 "Table 1a"、"Table 1b"、"Table 1c"）；三表交叉核对一致。
- 预算题（60-40 选项）：pairs 版 SQ 61%（11/18）vs NSQ 24%
  （4/17），p = .025；triples 版 SQ 42%（22/53）vs NSQ 19%；
  quads 版 SQ 37%（7/19）vs NSQ 6%（7/109），p = .001。
  50-50 选项：pairs SQ 76% vs NSQ 39%；quads SQ 32% vs NSQ 24%。
- 汇总模型（66 个决策选项 pooled，Table 2b）：
  SQ = .17 + .83·NEUT，加权 R² = .72；31/54 个 SQ vs NSQ 比较
  在 10% 水平显著。
- 口径说明：本试点是四选项版，对应 S&Z 的 quads 表
  （60-40 SQ 37% vs NSQ 6%）；两选项版数字不得直接对四选项版。

### 现状偏见人类数据：Pilli & Nallur（2026）——纠正归属

- 来源：Pilli & Nallur《Emulating Aggregate Human Choice Behavior
  and Biases with GPT Conversational Agents》，预印本
  （arXiv:2602.05597），爱尔兰都柏林大学。
- 数字（**他们自己的人类实验**，N=1256，Prolific 招募，已在 OSF
  预注册，数据公开于 Zenodo 10.5281/zenodo.16541481）：
  预算场景 60A40H vs 50A50H：无负荷时 SQ 26/51（51%）、
  N 14/60（23%）、NSQ 10/73（14%），h = 0.79，p < .001；
  负荷时 SQ 28/59（47%）、N 14/70（20%）、NSQ 10/64（16%），
  h = 0.81；该文引用 S&Z 1988 原文效应量 h = 0.78。
- ⚠️ 归属纠正（2026-11-05 抓取）：51% 是 Pilli & Nallur 自己
  的实验结果，**不是 S&Z 原文数据**；S&Z 原文 60-40 在
  pairs/triples/quads 下是 61%/42%/37%。引用时不得把 51%
  写成"S&Z 原文数据"。
- 获取路径：直接打开该预印本 PDF，Table 2、Table 3 及 §5.1.2 解读段。
- 核查方法：预印本 Table 2/3 的原始计数（分子/分母齐全，
  可独立重算比例与 h）；OSF 预注册与 Zenodo 数据集可复核。
- 等级说明：该文是预印本（尚未同行评议），但它报告的是
  自己的人类实验原始计数，且预注册、数据公开，可信度高于
  二手转述；报告里应注明"预印本"身份。
- 口径说明：该人类基线是两选项版，本试点是 Horton 式的
  四选项版；可比的是现状效应（SQ 相对 NSQ 的提升、效应量 h），
  不是原始得票率。

### 现状偏见复现：Xiao 等（2021）

- 来源：Xiao, Lam, Piara & Feldman (2021). Revisiting the Status
  Quo Bias: Replication of Samuelson and Zeckhauser (1988).
  *Meta-Psychology*, 5, MP.2020.2470. DOI: 10.15626/MP.2020.2470；
  OSF: 10.17605/OSF.IO/WUPF4。开放获取全文，原文直读。
- 设计：两次预注册 MTurk 收集，Phase I N=311，Phase II N=316；
  预算、投资、大学工作三场景成功复现，马车色场景失败。
- Phase II 预算总计：SQ 118/251（47%）、N 65/260（25%）、
  NSQ 133/753（18%），h = 0.644 / 0.464。
- 马车色失败细节：SQ 30% vs N 25% vs NSQ 23%，Silver 的 NSQ
  （54%）甚至高于 SQ（50%），SQ vs N 全部不显著。

### 复杂性与四重模式：Oprea（2024）原文

- 来源：Oprea, R. (2024). Decisions under Risk Are Decisions under
  Complexity. *American Economic Review*, 114(12), 3789–3811.
  DOI: 10.1257/aer.20221227。原文直读（AER PDF 镜像）。
- 设计：12 个任务（$25 赌注，p ∈ {0.1, 0.25, 0.5, 0.75, 0.9}，
  得/失/混合）；100 盒表述；lottery = 随机开 1 盒，
  mirror = 开全部 100 盒、按平均值支付（= 期望值，确定性）。
- 样本：主 MPL 实验 N=184（Prolific）；总计 673 人含稳健性组。
- 核心结果：mirror 中四重模式强度约为 lottery 的 97%；
  损失厌恶约为 lottery 的 80%，λ 估计 1.5 至近 2；
  跨被试相关 0.68 / 0.62。
- 口径差异：Oprea 用 $25 赌注、5 个概率点；本项目用 50 元、
  仅 p=0.9/0.1——是子集改编，不是精确复现，报告中应写明。
- 争议未决：Banki 等（2025）称 75% 被试未通过理解题、其噪声
  驱动了 mirror 结果；Zhang（2026）称在消除混淆的设计下
  四重模式在 mirror 中依然稳健。H3 的 mirror 结论应附此 caveat。

### 最低工资雇佣替代：Horton（2025）田野实验（部分）

- 来源：Horton, J. J. (2025). Price Floors and Employer Preferences:
  Evidence from a Minimum Wage Experiment. *American Economic Review*,
  115(1), 117–146. DOI: 10.1257/aer.20170637。
- 已核实（摘要直读 + 多源二手一致）：在线劳动力市场 RCT，
  雇主发帖时被随机分配最低工资 $0/$2/$3/$4（4 档），
  约 160,000 个招聘帖；四点定性结论：被雇工人工资上升、
  足够高的最低工资下雇佣概率下降（降幅不大）、工作小时数
  大幅下降（较低档即出现）、小时数下降可部分由高生产力工人
  替代低生产力工人解释。
- 未获：主文回归系数（AER 付费墙；SSRN 工作论文 PDF 未能
  经文本抓取获得；在线附录只含稳健性表）。待机构权限补入。
- ⚠️ 区分：Homo Silicus §2.5 Table 2 的"雇佣工资 +1.314/
  +1.984 美元/小时、雇佣经验 +0.081/+0.265 年"是 **AI 模拟**
  的结果，不是田野实验的系数，两者不得混写。

## C 级：已从基线撤下的数据

- S&Z 1988 两选项版 53%→62%：出自两份独立的教学幻灯片
  （Scribd、SlideShare），数字互相一致，但始终未在论文中
  找到原文出处。按"论文来源优先"原则，已从 horton_baselines.md
  的正式基线中撤下，仅在此记录备查；如需恢复，必须先在
  S&Z 1988 原文（*Journal of Risk and Uncertainty*, 1, 7–59）
  或引用它的论文中找到出处。

## 本项目数据的来源（与基线区分）

- DeepSeek / Gemini 试点数据：本项目自己跑的调用记录，
  原始文件在 results/ 与 results_gemini* 目录（JSONL，
  含 persona、提示词对应的解析结果与模型原始回复），
  任何人可用 analyze.py 重算全部汇总数字。
- 判定标准（三条：方向一致、分布可比、persona 梯度存在）
  出自本项目 README 设计文档，非外部论文。
