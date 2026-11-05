# Agent 社会行为验证 · 试点

目标：验证"DeepSeek + 轻量 persona 提示"这套配置能否复现已知人类行为实验结果。
这是 Horton「Homo Silicus」路线的复现＋扩展，不是照抄：实验集有增减、
后端模型不同、判定标准更硬。

- 部署：见 [DEPLOYMENT.md](DEPLOYMENT.md)（环境、凭据、验证三步）。
- 使用：见 [USAGE.md](USAGE.md)（9 个实验的命令、分析、新增实验四步）。
- 数据：见 [DATA.md](DATA.md)（人类基线来源、Fama 基线、处理办法）。
- 设计总报告：[experiment_design_report.md](experiment_design_report.md)
  （14 个实验：现有 9 个 + 人民币 3 个 + AI 泡沫 2 个 + 多 agent 远期）。

## 实验包（9 个）

| 实验 | 测什么 | 人类基线 |
|---|---|---|
| 独裁者博弈 | 利他分布 | Engel 2011：均值 28.35% |
| 最后通牒博弈（响应方） | 公平偏好与惩罚意愿 | 低于 20% 提议约 50% 被拒 |
| 禀赋效应 | WTA/WTP 缺口 | KKT 1990：卖价显著高于买价 |
| 雪铲涨价公平性 | 公平感知＋干预倾向梯度 | Kahneman 等（1986）：82% 认为不公平 |
| 现状偏见 | 维持现状的启发式 | S&Z 1988：SQ 37% vs NSQ 6% |
| 复杂性与四重模式 | 前景理论是否来自复杂性 | Oprea 2024：mirror 强度约 lottery 的 97% |
| 最低工资雇佣替代 | 规则改变时的比较静态 | Horton 2025：向有经验工人替代 |
| 自愿公共品 | 合作起源（Red Queen 循环） | Semmann 2003：loner≈32%/合作≈30%/背叛≈38% |
| 利差交易者 | Fama 之谜的 agent 版 | Fama 回归 β(12m)=+0.015、β(1m)=−0.468 |

每个实验 3 个版本：classic（教科书表述）、novel（新编故事，同构）、
adversarial（教科书答案应翻转的表述，如成本驱动涨价）。

## 通过标准（三条缺一不可）

1. 方向一致：定性复现人类结果。
2. 分布可比：不只看均值，看整个分布形态。
3. persona 梯度存在：如雪铲实验里干预倾向 1→5 的不公平判断应有单调趋势
   （梯度在，说明不是背教科书答案）。

## 怎么跑

```bash
# 干跑冒烟（不调 API，验证提示词渲染＋解析＋分析链路）
python3 run.py --dry-run --n 8 --experiment dictator
python3 analyze.py --in results/dictator_classic.jsonl

# 试点（通过已连接的 custom.deepseek 调用，Key 不进代码、不进环境变量）
python3 run.py --experiment dictator --n 200 --variant classic
python3 run.py --experiment ultimatum --n 200 --offer 20
python3 run.py --experiment endowment --n 200 --arm owner
python3 run.py --experiment endowment --n 200 --arm buyer
python3 run.py --experiment snow_shovel --n 200 --variant classic
python3 analyze.py --in results/ --all
```

## 成本估算

200 agent × 4 实验，每人约 500 输入 tokens + 100 输出 tokens，
约 40 万输入＋8 万输出 tokens，按 DeepSeek-V3 约 0.27/1.10 美元每百万
tokens 计，约 0.2 美元。放大 10 倍也只有几美元。

## 下一步

试点通过后：第二阶段上 Concordia 做多 agent 互动（拍卖、匹配、
重复博弈）；再之后接 A 股处置效应模拟。
