# 使用手册

## 1. 快速开始

```bash
# 干跑冒烟（不调 API）
python3 run.py --dry-run --n 8 --experiment dictator

# 单实验实跑（DeepSeek，200 次）
python3 run.py --experiment dictator --n 200 --variant classic

# 汇总分析
python3 analyze.py --in results/ --all
```

全局参数：`--n`（每组人数，默认 8）、`--variant`
（classic/novel/adversarial）、`--provider`
（deepseek/gemini）、`--model`、`--temperature`（默认 1.0）、
`--seed`（默认 20261105）、`--workers`（并发数）、
`--results-dir`（默认 `results`）、`--out`（指定输出文件）。

## 2. 实验一览与命令

9 个实验，全部参数见 `run.py --help`。每组默认 n=200。另有禀赋效应的
两个变体（无锚版 `--variant noanchor`、KKT chooser 臂
`--arm chooser`）与实验 9、实验 11，共 11 个实验 + 2 个变体。

| # | 实验 | 命令要点 | 臂/组 | 测什么 |
|---|---|---|---|---|
| 1 | 独裁者博弈 | `--experiment dictator` | classic/novel | 0–100 元连续分配，均值/零点/均分比例 |
| 2 | 最后通牒（响应方） | `--experiment ultimatum --offer 20` | 提议 20 元 | 拒绝率 |
| 3 | 禀赋效应 | `--experiment endowment --arm owner\|buyer` | 卖方/买方 | WTA/WTP 比值 |
| 4 | 雪铲涨价公平性 | `--experiment snow_shovel` | classic/novel/adversarial | 判不公平比例 + 倾向梯度 |
| 5 | 现状偏见 | `--experiment status_quo --sq 70\|60\|50\|30` | 4 种现状表述 | 选现状选项比例 |
| 6 | 复杂性与四重模式 | `--experiment oprea --condition lottery\|mirror --cell gain_high\|gain_low\|loss_high\|loss_low` | 8 组 | 确定性等价偏离期望值的符号 |
| 7 | 最低工资雇佣替代 | `--experiment hiring --minwage none\|30 --expask 26\|30\|34` | 6 组 | 雇有经验者比例、雇佣工资 |
| 8 | 自愿公共品 | `--experiment volunteering --params hauert\|semmann --scenario c_dom\|d_dom\|l_dom\|noinfo` | 8 组 | 合作/背叛/退出选择 |
| 9 | 利差交易者 | `--experiment carry --spread inv\|pos --vol low\|high --control none\|controlled` | 8 组 | 买人民币/买美元/不动 |
| 10 | 出口商结汇 | `--experiment settle --app app\|dep --spread inv\|pos --dxy down\|up` | 8 组 | 结汇比例（0–100%）+ 结汇节奏 |
| 11 | 央行中间价 agent | `--experiment fixing --close up\|down --basket up\|down --cfix none\|active` | 8 组 | 中间价调整（基点）+ 方向 |

示例（Horton 剩下 3 个实验，DeepSeek 串行版）：

```bash
for sq in 70 60 50 30; do
  python3 run.py --experiment status_quo --n 200 --sq $sq || exit 1
done
for cond in lottery mirror; do for cell in gain_high gain_low loss_high loss_low; do
  python3 run.py --experiment oprea --n 200 --condition $cond --cell $cell || exit 1
done; done
for mw in none 30; do for ea in 26 30 34; do
  python3 run.py --experiment hiring --n 200 --minwage $mw --expask $ea || exit 1
done; done
```

示例（利差交易者，8 并发，DeepSeek）：

```bash
for s in inv pos; do for v in low high; do for c in none controlled; do
  python3 run.py --experiment carry --spread $s --vol $v --control $c \
    --n 200 --workers 8 || exit 1
done; done; done
```

## 3. 分析与对照

```bash
# 汇总一个目录下全部实验
python3 analyze.py --in results/ --all

# 只看一个文件
python3 analyze.py --in results/dictator_classic.jsonl

# 双模型对照（a=DeepSeek 目录，b=Gemini 目录；跳过 dry_run 行）
python3 compare.py --a results --b results_gemini
```

`analyze.py` 按实验分组输出：独裁者给均值/中位/给 0 与均分
比例；禀赋效应给 WTA/WTP；雪铲与现状偏见给比例与梯度；
Oprea 给每格的确定性等价偏离；雇佣替代给雇佣比例与工资；
自愿公共品按（参数，场景）分组；利差交易者按 8 臂输出
众数与预测对照（正利差→买人民币，倒挂→买美元）。

## 4. 双模型复核流程

1. 主模型（DeepSeek）跑完，写 `results/`。
2. 复核模型（Gemini）用同样参数跑，写单独目录
   （如 `results_gemini/`、`results_gemini_h3/`），加
   `--workers 8`（Gemini 延迟高，8 并发下一组 200 次约 2.5 分钟）。
3. `python3 compare.py --a results --b results_gemini` 出对照。
4. 判定：单模型结果不得作为定论（教训：最后通牒实验
   DeepSeek 拒绝率 4%、Gemini 40%，差异 p<0.001）。

## 5. 通过标准（三条，缺一不可）

1. **方向一致**：定性复现人类结果。
2. **分布可比**：不只看均值，看整个分布形态。
3. **persona 梯度存在**：如雪铲实验里干预倾向 1→5 的
   不公平判断应有单调趋势（梯度在，说明不是背教科书答案）。
   报告梯度时同时报告幅度（Gemini 的 persona 梯度系统性
   更陡）。泡沫博弈另加一条"均衡识别"
   （有上限无交易均衡下交易率对 0 的偏离度）。

## 6. persona 设定

`personas.py`：种子 20261105；维度为年龄 20–65、性别、
收入三档（高/中等/低）、风险态度（厌恶/中性/偏好）、
干预倾向 1–5（循环均衡分配，每档 n=40）。温度 1.0。
降思考量或改温度会改变模型行为，复核中途禁止换设置。

## 7. 输出文件格式

每轮运行写一个 JSONL 文件，命名规则：
`<实验>_<variant>[_<臂参数>].jsonl`，如
`dictator_classic.jsonl`、`oprea_classic_mirror_gain_high.jsonl`、
`carry_inv_low_none.jsonl`。每行一条记录，字段：

| 字段 | 含义 |
|---|---|
| experiment / variant | 实验名与版本 |
| persona | 该条的 persona（年龄/性别/收入/风险态度/干预倾向） |
| offer / arm / sq / cell / condition / minwage / expask / scenario / params / spread / vol / control / app / dxy / close / basket / cfix | 各实验的臂参数（不适用为 null） |
| provider / model / temperature | 后端、模型、温度 |
| parsed | 解析出的结构化答案（失败为 null） |
| response | 模型原始回复文本 |
| dry_run | 是否干跑 |
| ts | 运行时间 |

解析失败的行 `parsed` 为 null，计入 `parse_fail`，
不删除、不重跑、不中断整轮。

## 8. 新增一个实验（四步）

1. `experiments.py`：加 `<name>_prompt(persona, variant, ...)`、
   `<name>_parse(text)`、一条 `sample`，
   在 `EXPERIMENTS` 里注册并写清人类基线（来源 + 状态）。
2. `run.py`：如需新参数，加 `--xxx` 并在后缀与记录字段里登记。
3. `analyze.py`：加该实验的分支，输出指标与判定对照。
4. 干跑冒烟：`--dry-run --n 4`，确认解析 0 失败后再实跑。
   新实验先小规模（n=20）试跑，确认众数与梯度合理再放大到 200。
