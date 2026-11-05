# Gemini 复核方案

目的：检验 DeepSeek 试点结论是否依赖单一模型。同一实验、同一批 persona、
同一温度，换 Gemini 再跑一遍；结论一致才算稳，不一致本身就是发现
（模型依赖），不是失败。

（此前准备的 Qwen 方案已废弃，用户改用 Gemini 复核。）

## 复核模型

- 模型：`gemini-3.8-flash`（Google AI Studio API，OpenAI 兼容接口；
  注：2026-11-05 实测，`gemini-2.5-flash` 已不对新用户开放，
  API 报错明确建议改用 `gemini-3.8-flash`，故默认模型定为后者）
- 端点：`POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`
- 认证：Bearer API Key（Google AI Studio 即 aistudio.google.com/apikey 获取），
  走已连接的 `custom.gemini`
- 备选：`--model` 可换更新的 Gemini 名称；换模型即换复核对象，
  需在报告里写明实际用的模型名

## 配对协议（关键）

- 同一种子：`--seed 20261105`（默认值），保证两边 persona 完全相同
- 同一温度：`--temperature 1.0`
- 同一实验集、同一版本：classic 先行；novel/adversarial 视 classic 结果再定
- 结果分目录：DeepSeek 写 `results/`，Gemini 写 `results_gemini/`，互不覆盖

## 跑法

```bash
# Gemini 侧（需 custom.gemini 已连接）
python3 run.py --provider gemini --experiment dictator --n 200 --variant classic --results-dir results_gemini
python3 run.py --provider gemini --experiment ultimatum --n 200 --offer 20 --results-dir results_gemini
python3 run.py --provider gemini --experiment endowment --n 200 --arm owner --results-dir results_gemini
python3 run.py --provider gemini --experiment endowment --n 200 --arm buyer --results-dir results_gemini
python3 run.py --provider gemini --experiment snow_shovel --n 200 --variant classic --results-dir results_gemini

# 对照
python3 compare.py --a results --b results_gemini
```

## 判定标准（复核通过需全部满足）

1. 方向一致：4 个实验的定性结论在两边都成立
   （独裁者给钱非零为主、最后通牒拒绝率随提议下降而上升、
   禀赋效应 WTA > WTP、雪铲多数认为不公平）。
2. 分布差距在容忍带内：独裁者均值差 ≤ 10 元；
   雪铲不公平比例差 ≤ 0.15；禀赋效应两边比值都 > 1。
3. persona 梯度同向：雪铲实验里干预倾向梯度在两边方向相同
   （不要求斜率相等）。

## 分歧怎么处理

- 只有个别实验分歧：先查提示词敏感性（换 novel 版本重跑），
  再查温度（降温到 0.7 看是否收敛），最后才归因于模型差异。
- 系统性分歧（多实验同向偏离）：结论记为"模型依赖"，
  后续社会模拟需双模型并行，不以单模型结论为准。

## 成本

与 DeepSeek 试点同量级（1000 次短调用）；Gemini API 有免费额度，
实际费用以 Google AI Studio 定价页为准，跑之前先确认余额。
