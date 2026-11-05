# Agent 社会行为验证：科学问题、研究现状、研究路线与数据来源

- 日期：2026-11-05（v1）
- 项目：~/workspace/agent-econ-validation/
- 用途：本项目的总纲文档。后续一切结论、报告、基线更新以本文为准绳，
  与本文冲突处以新证据修正本文，不得私下改口径。

## 来源状态说明（全文通用，科研严谨性的执行机制）

每个数字、每条结论后面都带来源状态，缺状态的表述视为未完成：

- **A**：本人直接在该论文正文读到（注明章节/表号）。
- **B**：被另一篇论文/预印本报告或转述（注明转引链）。
- **C**：非论文来源（教学幻灯片、博客、科普），不进入正式基线，
  仅在"待抓取"中记录。
- **自采**：本项目自己跑的调用记录，原始文件 + 复算脚本齐全。
- **待核对**：前期调研线索，尚未在本轮核对原文，
  不得作为基线引用，只能作为下一步抓取目标。

详细审计见 `provenance.md`。引用规范见第 7 节。

## 1. 科学问题

### 1.1 核心问题

大语言模型驱动的 agent（Horton 所称的 *Homo silicus*）能否作为
人类经济行为的可信模拟器——即在没有真人被试的情况下，
用 agent 实验预测人类在经济实验中的行为分布与比较静态？

来源：Horton, Filippas & Manning《Large Language Models as Simulated
Economic Agents》**A**（arXiv:2301.07543v2，§1）。

### 1.2 四个递进子问题

1. **个体决策**：agent 在经典行为实验中是否复现人类的系统性偏离
   （社会偏好、损失厌恶、公平约束）？——本阶段已验证 4 个实验，
   进行中 3 个（第 4 节）。
2. **互动均衡**：多 agent 互动中是否涌现人类式的均衡与合作
   （拍卖、匹配、重复博弈）？——未开始，属第二阶段。
3. **规则设计**：改变规则（机制、价格、约束）时，agent 的比较静态
   是否与人类实验一致（最低工资雇佣替代即属此类）？——进行中 1 个。
4. **验证方法论**：agent 模拟在什么条件下可信——换模型、换措辞、
   换 persona 后结论是否稳定？从"像人"到"预测真人"还差哪一步？
   ——方法论贯穿全程，第 3 阶段专门处理。

### 1.3 可证伪的判定标准（本项目专用，三条缺一不可）

1. 方向一致：agent 结果与人类基线的方向相同。
2. 分布可比：不只均值，分布形态（零点、均分点、尾部）也在人类
   合理范围内。
3. persona 梯度存在：理论预测的方向上，persona 维度能系统性移动选择。

来源：**自采**（本项目 README 设计文档）。

## 2. 研究现状

### 2.1 Horton 路线：单 agent 实验复现（本项目的方法论基线）

Horton 等用 LLM 复现 5 个经典实验 **A**（arXiv:2301.07543v2，
§2 全节；实验清单见该文摘要与 §2 各节标题）：

1. Kahneman 等（1986）雪铲涨价公平性 + 政治梯度 + 剂量反应（§2.1）。
2. Charness & Rabin（2002）二选一分配博弈 + persona 校准混合（§2.2）。
3. Samuelson & Zeckhauser（1988）现状偏见（§2.3）。
4. Oprea（2024）复杂性与四重模式（§2.4）。
5. Horton（2025）最低工资雇佣替代（§2.5）。

关键方法论结论 **A**：

- 无 persona 的 agent 与真人差异大，且模型间不同（§2.2）。
- 理论校准的 persona 混合在样本外二阶段博弈中预测误差约为
  无 persona 模型的一半（MSE 0.094 vs 0.182，§2.2.1）。
- 配套开源工具 EDSL（pypi: edsl），实验可一键复现（§1）。

### 2.2 多 agent 社会模拟路线（前期调研线索，待核对）

以下为前期调研中提及的路线，**待核对**（尚未在本轮核对原文，
不得作为基线引用，仅列为背景与第二阶段选型参考）：

- Generative Agents / Smallville（Stanford + Google）：25 个 agent 的
  小镇涌现行为。
- Concordia（DeepMind）：开源多 agent 社会模拟库。
- AgentSociety（2025）：万级 agent 社会模拟。
- EconAgent：用 agent 复现菲利普斯曲线、奥肯定律等宏观规律。
- TwinMarket：A 股集合竞价模拟。

### 2.3 质疑与边界（必须正视的三类反证）

1. **记忆化质疑**：LLM 可能只是复述训练数据中的已知实验结果，
   而非真正模拟。Horton 文中讨论此问题 **A**（§1、§2.1.1、§2.4），
   并引用 Sarkar & Vafa（2024）、Ludwig 等（2025）**B**（转引自 Horton）。
   应对：本项目用 novel/adversarial 变体与未发表过的参数组合
   做稳健性检验（第 3 阶段）。
2. **模型依赖**：换后端模型结论会变。Horton 原文 5 个模型结果
   并不一致 **A**（如现状偏见系数 GPT-4o 0.316 vs GPT-4 0.931，
   §2.3 Table 1）。应对：本项目坚持多模型复核（DeepSeek + Gemini，
   后续扩展见第 6 节）。
3. **宏观假象质疑**：2026 年复现研究指出 EconAgent 类的宏观规律
   可能是会计恒等式而非行为机制 **待核对**（前期调研结论，
   进入宏观阶段前必须先排除此坑，见第 4 节）。
4. **Oprea 争议**：Banki 等（2025）认为 mirror 条件下的四重模式
   源于被试误解指令而非复杂性 **B**（转引自 Horton §2.4）。
   应对：本项目的 mirror 措辞必须明确"确定、无随机性"，
   并把"被试是否理解"作为结果解读的保留项。

### 2.4 本项目的定位与边际贡献

- 不是 Horton 的简单重跑：Horton 用英文、GPT/Claude 系模型；
  本项目用中文提示词、DeepSeek/Gemini、自定义 persona 维度
  （年龄/性别/收入/风险态度/干预倾向），检验结论是否跨语言、
  跨模型、跨 persona 体系成立。
- 不是纯复现：独裁者用连续分配（Horton 用二选一）、
  最后通牒与禀赋效应是 Horton 原文没有的新增实验，
  扩展了 Horton 的实验包。
- 判定标准比 Horton 更严：Horton 多报告定性一致，
  本项目要求方向 + 分布 + persona 梯度三条同时成立。

## 3. 研究路线

### 阶段一：单 agent 验证（进行中）

- 已完成：独裁者、最后通牒响应方、禀赋效应、雪铲（DeepSeek 侧，
  n=200/实验，解析 0 失败）**自采**。
- 进行中：现状偏见、Oprea 四重模式、最低工资雇佣替代
  （DeepSeek + Gemini，18 组 × 200，8 并发重跑中）**自采**。
- 产出：DeepSeek 单边中期对照（已出，见
  `deepseek_vs_horton_interim.md`）→ Gemini 完成后出联合对照报告。

### 阶段二：稳健性（下一批，见第 6 节 W2–W4）

- novel/adversarial 变体（脚手架已支持，试点只跑了 classic）。
- 雪铲多价格点剂量反应（对齐 Horton 的 $16/$20/$40/$100 设计）。
- 最后通牒提议方出价分布（目前只有响应方 20% 一点）。
- 无价格锚点的禀赋效应（排除 80 元锚点对效应量级的压缩）。
- 温度敏感性（1.0 之外至少加一个温度点）与措辞敏感性。

### 阶段三：校准与样本外预测（Horton §2.2.1 方法）

- 用理论 persona 混合拟合人类基线分布，再在结构不同的新博弈
  （如两阶段博弈）中做样本外检验，目标是复现 Horton 的
  "误差减半"结论 **A**（MSE 0.094 vs 0.182）。
- 前置条件：阶段一、二的数据齐全；需用户拍板是否引入
  Charness & Rabin 式二选一博弈作为样本外检验场。

### 阶段四：多 agent 互动（第二阶段方向）

- 拍卖（赢者诅咒、格式比较）、匹配（延迟接受算法收敛性）、
  重复博弈（合作涌现、贴现因子）、市场收敛。
- 前置条件：技术选型（Concordia 或自研轻量框架）需用户拍板；
  宏观规律类实验进入前必须先排除会计恒等式假象（§2.3 第 3 点）。

### 阶段五：应用（A 股处置效应模拟）

- 前置条件：阶段一至三的方法论结论成立（至少方向 + 梯度成立）。
- 与本项目 A 股策略研究衔接，处置效应（盈利早卖、亏损死扛）
  是损失厌恶在交易行为中的直接对应物。

## 4. 验证理论清单

状态：✅ 已验证 / 🔄 进行中 / ⏳ 待验证。
人类基线与来源状态详见 `provenance.md`；此处只列理论与判定。

### ✅ 已验证（DeepSeek 侧，Gemini 复核待完成）

| 理论 | 来源论文 | 人类基线 | DeepSeek 判定 |
|---|---|---|---|
| 社会偏好（分配权衡） | Charness & Rabin（2002）**B** | Engel 2011 元分析：均值 28.35% **B** | 通过：均值 28.9，分布略偏慷慨 |
| 公平惩罚 / 负互惠 | Güth 等（1982）；Rabin（1993）**B** | 20% 提议约 50% 拒绝（Camerer 2003 表 2.2/2.3 转述；Oosterbeek 2004 平均拒绝率 16%，无曲线表）**B** | 偏离：拒绝率仅 4% |
| 损失厌恶 / 参照依赖 | Thaler（1980）；KKT（1990）**B** | WTA/WTP 约 2.1–2.6 **B** | 方向对、幅度弱（1.24–1.33） |
| 公平约束 / 双重权利 | Kahneman 等（1986）**A**（Horton 转引） | 约 82% 判不公平 **A** | 通过：梯度与 Horton 一致 |

### 🔄 进行中（DeepSeek + Gemini 18 组在跑）

| 理论 | 来源论文 | 人类基线 | 判定待出 |
|---|---|---|---|
| 现状偏见 | Samuelson & Zeckhauser（1988）**B** | Pilli & Nallur（2026）人类实验：SQ 51% vs NSQ 14%，h=0.79 **B**；S&Z 原文 h=0.78（据该文引用） | 待出 |
| 复杂性与四重模式 | Oprea（2024）**A**（Horton §2.4） | 四重模式在 mirror 条件下同样出现 **A** | 待出 |
| 最低工资雇佣替代 | Horton（2025）**A**（Horton §2.5） | 田野：雇佣量变化不大，转向高生产力工人 **A**；AI 复现工资 +1.31 美元/小时 **A** | 待出 |

### ⏳ 待验证（按优先级排序）

1. 框架效应（得失表述翻转）：Kahneman & Tversky 前景理论体系，
   与禀赋效应同源，单 agent 可验，优先。
2. 互惠与信任：两阶段博弈、信任博弈、第三方惩罚、公共品博弈；
   其中两阶段博弈同时是阶段三样本外检验的候选场。
3. 前景理论全貌：概率加权、得失框架下的风险态度翻转、
   心理账户（禀赋效应只验了损失厌恶一角）。
4. 拍卖理论：Milgrom & Wilson（2020）**待核对**；需多 agent。
5. 匹配理论：Roth & Shapley（2012）**待核对**；需多 agent。
6. 重复博弈与合作：Aumann & Schelling（2005）、Nash（1994）
   **待核对**；需多 agent。
7. 市场与宏观规律：价格收敛、资产市场泡沫；菲利普斯曲线、
   奥肯定律类实验进入前必须先排除会计恒等式假象 **待核对**。
8. 有限理性（Simon 1978）**待核对**：启发式、满意化、
   认知负荷下的决策退化（与 Oprea 的复杂性机制直接相关）。
9. **合作起源：自愿公共品（用户 2026-11-05 新增，优先）**：
   Hauert 等（2002）Science **A** + Semmann 等（2003）Nature
   人类实验 **B**。机制：自愿退出（loner）让合作在完全匿名、
   无记忆、随机配对下仍能维持，群体频率呈 Red Queen 循环。
   单 agent 场景版已设计并接入脚手架（4 臂：c_dom/d_dom/l_dom/noinfo，
   N=5、r=3、σ=1，预测众数 D→L→C），待跑；群体频率随时间的
   振荡本身需多 agent 演化模拟，属阶段四。档案见
   `cooperation_volunteering.md`。

## 5. 数据来源

### 5.1 本项目自采数据（原始记录，可复算）

- 设计：persona 种子 20261105；温度 1.0；n=200/组；
  提示词中文；解析规则为单 JSON 对象机械提取。
- 位置：`results/`（DeepSeek）、`results_gemini/`（Gemini 原 4）、
  `results_gemini_h3/`（Gemini H3）；备份在
  `results_gemini_backup_sequential/`、`results_gemini_h3_backup_sequential/`。
- 复算：`analyze.py --in <目录> --all` 输出全部汇总数字；
  `compare.py --a results --b results_gemini` 做双模型对照。
- 模型：DeepSeek `deepseek-chat`、Gemini `gemini-3.8-flash`
  （注：`gemini-2.5-flash` 已不对新用户开放，见 API 报错原文，
  故用 3.8-flash，**自采**）。

### 5.2 文献基线数据（分级审计，见 provenance.md）

- A 级：Horton 原文全部数字（雪铲 82%、v_CR、现状偏见 Table 1、
  Oprea 设计、雇佣替代 Table 2）。
- B 级：Engel 2011（DOI 10.1007/s10683-011-9283-7）、
  KKT 1990（DOI 10.1086/261737，经 DellaVigna 2009 JEL 综述转述）、
  Oosterbeek 2004 + Camerer 2003（经 PLOS ONE 转述）、
  Pilli & Nallur 2026 预印本（arXiv:2602.05597，OSF 预注册，
  Zenodo 数据 10.5281/zenodo.16541481）。
- C 级（已撤下，不用）：S&Z 1988 的 53%→62%（教学幻灯片来源）。

### 5.3 待抓取的数据（编号 D，见第 6 节配套）

| 编号 | 数据 | 用途 | 获取路径 | 状态（2026-11-05 抓取后） |
|---|---|---|---|---|
| D1 | S&Z 1988 原文表（J. Risk Uncertainty 1:7–59） | 恢复现状偏见人类基线的原始出处 | JSTOR 经 Internet Archive 公开 OCR 文本 | ✅ 原文直读：60-40 pairs 61%/triples 42%/quads 37%；汇总 SQ=.17+.83·NEUT，R²=.72 |
| D2 | Oprea 2024 原文 CE 数据与 mirror 设计细节 | 核对四重模式的原始效应量与措辞 | AER PDF 镜像直读 | ✅ 原文直读：N=184；mirror 强度约 lottery 的 97%；λ=1.5–2；Banki/Zhang 争议附 caveat |
| D3 | Horton 2025 田野实验原文 | 核对雇佣替代的田野效应量 | AER 摘要 + SSRN 工作论文 | ⚠️ 部分：设计与定性结论已核实（约 160,000 帖、$0/$2/$3/$4）；主文回归系数未获全文 |
| D4 | Xiao 等 2021 S&Z 在线复现数据 | 现状偏见的第二个人类数据源 | OSF 开放获取全文 | ✅ 原文直读：Phase II N=316，预算总计 SQ 47%/N 25%/NSQ 18%；马车色失败 |
| D5 | Engel 2011 原文表 | 确认 28.35% 与固定效应 20.4% 的完整口径 | 多源论文转述核实 | ✅ 转述核实：616 处理/20,813 人；28.35% 总均值；20.4% 固定效应仅限 445 处理；论文数 129/131 未解决，只写 616 |
| D6 | KKT 1990 原文表 | 确认 $5.75/$2.25 与 $7.12/$2.87 出自哪两个实验 | DellaVigna 2009 JEL 综述转述 | ✅ 转述核实：$5.75/$2.25 为第一组实验；$7.12/$3.12/$2.87 为实验 6（77 人，含 chooser） |
| D7 | Oosterbeek 2004 元分析全文 | 最后通牒拒绝率曲线的完整数据 | 摘要 + 多源转述 | ✅ 摘要直读：37 篇/75 结果，平均出价 40%，平均拒绝率 16%；**无拒绝率曲线表**，"约 50%"属 Camerer |
| D8 | Camerer 2003 表 2.2/2.3 | 提议分布与拒绝率的教科书级数据 | 四份独立讲义一致核实 | ⚠️ 部分：原书未获全文；众数/中位 40–50%、均值 30–40%、<20% 约 50% 被拒；引用须写"转引自表 2.2/2.3" |
| D9 | 多模型复核数据 | 目前仅 DeepSeek + Gemini；Horton 用 5 模型 | 需用户拍板新增模型（注意：Qwen 已被用户否决用于当前复核） | 待拍板 |
| D10 | 本项目待跑数据 | 稳健性变体、剂量反应、提议方、无锚禀赋、参照工资、数学能力 persona | 脚手架内生成，无需外采 | 高 |
| D11 | Semmann 等 2003 Nature 全文定量数据 | 逐轮 C/D/L 频率、合作维持水平、样本量与收益参数 | Nature 全文 OCR 直读 | ✅ 原文直读：280 人/20 组/57 轮；后 30 轮 L≈32%/C≈30%/D≈38%；loner 实测 33% 低于模型预期 ≥42% |

## 6. 后续工作清单

| 编号 | 工作 | 前置条件 | 产出 | 状态 |
|---|---|---|---|---|
| W1 | Gemini 两路跑完 → 联合对照报告（前 4）+ H3 对照报告 | 两路后台进程完成 | 两份对照报告 | 进行中（后台跑） |
| W2 | 稳健性变体：novel/adversarial（4 实验） | W1 完成 | 稳健性表 | 待开始 |
| W3 | 雪铲多价格点剂量反应 | W1 完成 | 剂量反应曲线 vs Horton | 待开始 |
| W4 | 最后通牒提议方、无锚禀赋、参照工资、数学能力 persona | W1 完成 | 4 项补实验 | 待开始 |
| W5 | 抓取 D1–D8 文献数据，补齐 provenance.md | 无（可并行） | 审计表升级为全 A/B 级 | 待开始 |
| W6 | 阶段三：校准 persona 混合 + 两阶段博弈样本外检验 | W1–W4 完成；用户拍板检验场 | 样本外预测误差 vs 无 persona 基线 | 待拍板 |
| W7 | 多模型扩展（D9） | 用户拍板模型选择 | 第三个模型复核 | 待拍板 |
| W8 | 阶段四技术选型（Concordia 或自研） | W6 完成 | 选型文档 + 最小多 agent  demo | 待拍板 |
| W9 | README 更新为 7 实验设计文档 | W1 完成 | 与脚手架一致的设计文档 | 待开始 |
| W10 | 阶段五：A 股处置效应模拟 | 阶段一至三结论成立 | 处置效应模拟报告 | 远期 |
| W11 | 自愿公共品实验开跑（DeepSeek + Gemini，4 臂 × 200） | D11 可有可无（模型预测已齐）；用户拍板开跑 | 4 臂众数 vs 预测 + noinfo 分布 | 待拍板 |

## 7. 方法学规范（本项目科研严谨性的硬性规定）

1. **论文优先**：基线数字必须来自论文（原文或论文转述），
   幻灯片、博客、科普一律不进入基线；预印本必须注明身份。
2. **转引注明**：凡经他人转述的数字，必须写明转引链
   （如"KKT 1990，经 DellaVigna 2009 JEL 综述转述"），
   不得把转述写成直读。
3. **口径声明**：每个结论注明模型、温度、n、persona 体系、
   提示词语种、量表形式；量表、币种、博弈形式不同的对照
   只比方向与梯度，不逐数等同。
4. **可复算**：全部自采数据保留原始 JSONL（含模型原始回复），
   汇总数字必须能用 `analyze.py` 重算；解析失败数必须报告，
   不得静默丢弃。
5. **失败与偏离先行**：偏离项先查提示词敏感性与温度，
   再归因模型差异；方法学 caveat（如禀赋效应的 80 元锚点、
   雪铲的二值量表压缩）必须写进报告，不得只报有利结果。
6. **版本控制**：基线、口径、判定标准变更时同步更新
   `horton_baselines.md`、`provenance.md`、本文与 `MEMORY.md`，
   旧口径注明作废原因与日期。

## 参考文献（按文中出现顺序；转引关系如实标注）

[1] Horton, J. J., Filippas, A., & Manning, B. S. Large Language Models
as Simulated Economic Agents: What Can We Learn from Homo Silicus?
arXiv:2301.07543v2（2026 年 8 月更新版）；NBER Working Paper No. 31122。
**A**（全文直读）。

[2] Kahneman, D., Knetsch, J. L., & Thaler, R. H. (1986). 雪铲涨价
公平性实验（约 82% 判不公平），转引自 [1] §2.1。**B**。

[3] Charness, G., & Rabin, M. (2002). Understanding Social Preferences
with Simple Tests. 真人选 Left 向量 v_CR，转引自 [1] §2.2。**B**。

[4] Samuelson, W., & Zeckhauser, R. (1988). Status Quo Bias in Decision
Making. *Journal of Risk and Uncertainty*, 1, 7–59。原文表待抓取（D1）；
效应量 h=0.78 据 [11] 引用。**B**（效应量）。

[5] Oprea, R. (2024). 复杂性与四重模式实验，转引自 [1] §2.4；
原文数据待抓取（D2）。**B**。

[6] Horton, J. J. (2025). 最低工资雇佣替代田野实验，
转引自 [1] §2.5；原文待抓取（D3）。**B**。

[7] Engel, C. (2011). Dictator Games: A Meta Study. *Experimental
Economics*, 14(4), 583–610. DOI: 10.1007/s10683-011-9283-7。
经 PMC 同行评议论文转述核对。**B**。

[8] Kahneman, D., Knetsch, J. L., & Thaler, R. H. (1990). Experimental
Tests of the Endowment Effect and the Coase Theorem. *Journal of
Political Economy*, 98(6), 1325–1348. DOI: 10.1086/261737。
经 DellaVigna (2009) JEL 综述转述。**B**。

[9] Oosterbeek, H., Sloof, R., & van de Kuilen, G. (2004).
最后通牒元分析（37 篇论文），经 PLOS ONE 同行评议论文转述。**B**。

[10] Camerer, C. (2003). *Behavioral Game Theory*. 表 2.2、2.3
（提议分布与拒绝率），经 PLOS ONE 及讲义转述；原文表待抓取（D8）。**B**。

[11] Pilli, S., & Nallur, V. (2026). Emulating Aggregate Human Choice
Behavior and Biases with GPT Conversational Agents. 预印本，
arXiv:2602.05597；OSF 预注册 10.17605/OSF.IO/PSXVF；
数据 Zenodo 10.5281/zenodo.16541481。**B**（预印本，人类实验原始计数）。

[12] DellaVigna, S. (2009). Psychology and Economics: Evidence from
the Field. *Journal of Economic Literature*（综述，含 KKT 实验转述）。
**B**。

[13] Güth, W., Schmittberger, R., & Schwarze, B. (1982).
最后通牒博弈原始实验。**B**（标准引用，细节待与原文核对）。

[14] Thaler, R. (1980). 禀赋效应术语来源。**B**（标准引用）。

[15] Manning, B. S., & Horton, J. J. (2025). 校准 persona 混合方法，
转引自 [1] §2.2.1。**B**。

[16] Sarkar, A., & Vafa, K. (2024)；Ludwig, J., 等（2025）；
Banki, 等（2025）. 对 LLM 模拟的质疑文献，均转引自 [1]。**B**。

[17] Generative Agents、Concordia、AgentSociety、EconAgent、
TwinMarket 等多 agent 路线：前期调研线索，完整引用待核对，
不得作为基线引用。**待核对**。

[18] Hauert, C., De Monte, S., Hofbauer, J., & Sigmund, K. (2002).
Volunteering as Red Queen Mechanism for Cooperation in Public Goods
Games. *Science*, 296(5570), 1129–1132. DOI: 10.1126/science.1070582。
**A**（Science 摘要页 + 作者维也纳大学主页公开全文文本）。

[19] Semmann, D., Krambeck, H.-J., & Milinski, M. (2003).
Volunteering Leads to Rock–Paper–Scissors Dynamics in a Public Goods
Game. *Nature*, 425, 390–393. DOI: 10.1038/nature01986。
**A**（Nature 全文 OCR 直读，2026-11-05 抓取）。

[20] Xiao, Q., Lam, C. S., Piara, M., & Feldman, G. (2021).
Revisiting the Status Quo Bias: Replication of Samuelson and
Zeckhauser (1988). *Meta-Psychology*, 5, MP.2020.2470.
DOI: 10.15626/MP.2020.2470。**A**（开放获取全文直读）。

[21] Oprea, R. (2024). Decisions under Risk Are Decisions under
Complexity. *American Economic Review*, 114(12), 3789–3811.
DOI: 10.1257/aer.20221227。**A**（原文直读）。

[22] Horton, J. J. (2025). Price Floors and Employer Preferences:
Evidence from a Minimum Wage Experiment. *American Economic Review*,
115(1), 117–146. DOI: 10.1257/aer.20170637。
**B**（摘要直读 + 多源二手一致；主文回归系数未获全文）。
