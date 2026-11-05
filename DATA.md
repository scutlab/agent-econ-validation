# 数据来源与处理办法

本文件说明本项目用到的全部数据从哪里来、怎么取、怎么处理，
以及哪些数据拿不到。来源状态分五档：**A** = 论文原文读到；
**B** = 论文/预印本转述或摘要；**C** = 媒体与机构分析；
**自采** = 本项目调用记录；**待核对** = 尚未拿到。
每处数字都应能按本文件复查。

## 1. 人类基线：来源总表

人类基线是判定 agent 结果的对照，详见
`provenance.md`、`horton_baselines.md`、`literature_fetch_report.md`。
下表只列出处与获取方式。

| 实验 | 人类基线 | 来源 | 获取方式 | 状态 |
|---|---|---|---|---|
| 独裁者 | Engel 2011：616 处理、20,813 人，均值 28.35%；36.11% 给 0、16.74% 均分 | *Experimental Economics* 14(4), DOI 10.1007/s10683-011-9283-7 | 多源论文转述核实 | B |
| 独裁者 | Horton §2.2：二选一分配博弈向量 v_CR | Horton et al., arXiv:2301.07543v2 | 原文直读 | A |
| 最后通牒 | Camerer 2003 表 2.2/2.3：低于 20% 提议约 50% 被拒 | *Behavioral Game Theory* | 四份独立讲义核实，原书未直读 | B |
| 最后通牒 | Oosterbeek 2004：37 篇/75 结果，平均出价 40%、平均拒绝率 16% | *Experimental Economics* 7(2), DOI 10.1023/B:EXEC.0000026978.14316.74 | 摘要直读 + 转述 | B |
| 禀赋效应 | KKT 1990：mug 实验中位 WTA $5.75 vs WTP $2.25；实验 6 WTA $7.12/chooser $3.12/WTP $2.87 | *JPE* 98(6), DOI 10.1086/261737 | 经 DellaVigna 2009 JEL 综述转述 | B |
| 雪铲 | Kahneman 等 1986：约 82% 判不公平 | 原实验，经 Horton §2.1 转引 | 原文直读（Horton） | A |
| 现状偏见 | S&Z 1988：四选项版 quads 表，60-40 选项 SQ 37% vs NSQ 6%（p=.001） | *J Risk and Uncertainty* 1, 7–59 | JSTOR 经 Internet Archive OCR 直读 | A |
| 现状偏见 | Pilli & Nallur 2026：自有实验 N=1256，两选项版 SQ 51% vs NSQ 14%，h=0.79 | arXiv:2602.05597（预印本） | 预印本直读 | B |
| 现状偏见 | Xiao 等 2021：Phase II N=316，预算总计 SQ 47%/N 25%/NSQ 18% | *Meta-Psychology* 5, DOI 10.15626/MP.2020.2470 | 开放获取全文直读 | A |
| Oprea | Oprea 2024：主实验 N=184，mirror 强度约 lottery 的 97%，λ=1.5–2 | *AER* 114(12), DOI 10.1257/aer.20221227 | 原文直读 | A |
| 雇佣替代 | Horton 2025：约 160,000 招聘帖，最低工资 $0/$2/$3/$4，定性结论 | *AER* 115(1), DOI 10.1257/aer.20170637 | 摘要直读；主文回归系数未获全文（待取） | B |
| 自愿公共品 | Semmann 等 2003：280 人、20 组×14 人、57 轮；后 30 轮 loner≈32%/合作≈30%/背叛≈38% | *Nature* 425, DOI 10.1038/nature01986 | 全文 OCR 直读 | A |
| 自愿公共品 | Hauert 等 2002：模型参数 N=5、r=3、σ=1；N=10、r=5 算例 | *Science* 296(5570), DOI 10.1126/science.1070582 | 摘要 + 作者主页公开全文 | A |

**三处归属纠正**（已落实到各文档，引用时不得写错）：
Pilli & Nallur 的 51% 是他们自己的实验数据，不是 S&Z 原文；
"低于 20% 约 50% 被拒"是 Camerer 的数，不是 Oosterbeek 的；
Horton §2.5 的 +1.314/+1.984 美元/小时是 **AI 模拟数**，
不是 Horton 2025 的田野系数。

## 2. Fama 回归基线（实验 10 的定量对照）

代码与数据：`research_notes/fama_baseline/`（`fama.py`、
`fama_baseline.md`、`fama_output.txt`、`lpr_history.csv`、
`dexchus.csv`、`dgs1.csv`、`dgs1mo.csv`、`dgs10.csv`）。
结论：β(12m)=+0.015（SE 0.746，R²=0.000，n=75），
β(1m)=−0.468（SE 0.726，t(β=1)=−2.02，R²=0.004，n=86）；
2024+ 窗口 corr=−0.596。

### 2.1 数据来源与获取方式

| 数据 | 来源 | 获取命令 | 状态 |
|---|---|---|---|
| DEXCHUS（USD/CNY 日度） | FRED | `curl -sL "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXCHUS"`，无 key | ✅ 1981–2026-10-30，11,957 行 |
| DGS1（美 1 年期） | FRED | 同上，`id=DGS1` | ✅ 1962–2026-11-03 |
| DGS1MO（美 1 个月，备用） | FRED | 同上，`id=DGS1MO` | ✅ 2001–2026-11-03 |
| DGS10（美 10 年期） | FRED | 同上，`id=DGS10` | ✅ 2026-11-03 为 4.95% |
| 1 年期 LPR 全表 | 广州农商行 LPR 表（2025-05-20 发布）+ 央行公告交叉核实 | 搜索 + 原文直读，见 `lpr_history.csv` | ✅ 13 次调整（2019-08-20 4.25% → 2025-05-20 3.00%） |
| 中国 10 年期国债收益率 | — | 见 2.3 | ❌ 不可得 |

### 2.2 处理办法

1. **月度聚合**：FRED 日度序列取每月最后一个观测值
   （月末值），不用月均值。
2. **汇率变换**：S 取自然对数，S = 人民币/美元
   （S 上升 = 人民币贬值）。
3. **LPR 展开**：13 个调整日构成阶梯函数，按月展开
   （每月 20 日前后以当月生效值为准）。
4. **回归式**（Fama 1984）：Δln S_{t+h} = α + β·(i_t − i*_t) + ε，
   h=12 个月（与 1 年期利率期限匹配）与 h=1 个月（经典形式，
   年化利差除以 12）各一式。
5. **标准误**：重叠观测用 Newey-West（Bartlett 核），
   12 个月期限滞后 11 期，1 个月期限滞后 3 期。
6. **样本**：2019-08..2026-10，共 87 个月（LPR 改革后才有数据）。
7. 复算：`cd research_notes/fama_baseline && python3 fama.py`
   （需 numpy）。

### 2.3 中国 10 年期收益率：为什么没算

2026-11-05 实测四路免费渠道均失败：
FRED 的 OECD 序列 IRLTLT01CNM156N 经 fredgraph.csv 返回错误页、
系列页 403；Yahoo Finance 无 CN10Y 代码；Eastmoney push2his
接口连接失败；worldgovernmentbonds.com 为 JS 渲染、文本抓取
无数据。因此 10 年期利差的 Fama 回归**无法用免费数据复算**，
报告中只给时点值：中国 10 年期约 1.7%
（TradingView TVC-CN10Y，2026 年内 1.63–1.88%），
美国 10 年期 4.95%（DGS10，2026-11-03），利差约 −320bp。

### 2.4 局限

- 样本短（87 个月），LPR 为阶梯利率、变异极小，
  12 个月期限的 β 标准误达 0.75，基本无信息量。
- 期限错配：经典 Fama 回归用 1 个月利率，本基线用 1 年期利率。
- 未控制结汇流、美元指数、风险情绪等变量。
- 2024+ 窗口 corr=−0.596 为描述性统计（n=22，重叠），
  未附标准误，不得当作回归结论引用。

## 3. 人民币与 AI 泡沫调研的数据

`research_notes/rmb_rates_fx_puzzle.md` 与 `ai_bubble.md`
的数字分三档：论文原文（A）、论文摘要/预印本（B）、
媒体与机构分析（C）。其中多处关键数字（DXY、顺差、结汇、
GSDEER 与 IMF 的低估估计、OpenAI 收入与亏损、Sequoia 缺口）
为媒体转述 **C 级**，须以海关总署/外汇局/CFETS 或公司财报
等官方发布复核后才能进正式基线，原文已逐处标注。

## 4. 实验输出数据的处理办法

- 原始输出为 JSONL，每行一条记录（字段见 USAGE.md 第 7 节），
  保存在 `results*/`，**不进仓库**（可复跑生成）。
- 解析失败：`parsed` 为 null，计入 `parse_fail`，不删除、
  不重跑、不中断整轮；失败率先报用户再谈结论。
- `compare.py` 跳过 `dry_run` 行，只对照真实调用。
- 温度、种子、模型名固定（温度 1.0、种子 20261105，
  DeepSeek `deepseek-chat`、Gemini `gemini-3.8-flash`），
  复核中途禁止换设置（降思考量会改变模型行为）。
- 统计口径：均值/中位/分布比例直接由 `analyze.py` 计算；
  双模型差异用两比例 z 检验；Fama 回归用 Newey-West 标准误。
