# 部署手册

## 1. 这是什么

本仓库是"LLM agent 社会行为验证"项目的实验脚手架与文档：
用轻量 persona 提示驱动大语言模型，复现已知人类经济行为实验
（Horton《Homo Silicus》路线），并扩展到人民币汇率与 AI 泡沫
两个现实问题。架构刻意保持最小：**实验脚手架只有 Python
标准库依赖**，不依赖任何第三方包。

## 2. 系统要求

| 项目 | 要求 | 实测环境 |
|---|---|---|
| Python | 3.10+ | 3.12.3（Linux） |
| 实验脚手架（`run.py` 等 5 个文件） | 仅标准库 | `argparse/json/os/sys/time/urllib` + 本地模块 |
| Fama 基线（`research_notes/fama_baseline/fama.py`） | numpy | 1.26.4 |
| 磁盘 | 代码 + 文档约 200KB；原始结果文件不进仓库 | — |

```bash
python3 --version   # 应为 3.10+
```

## 3. 获取代码

```bash
git clone https://github.com/scutlab/agent-econ-validation.git
cd agent-econ-validation
```

仓库内容：

```
agent-econ-validation/
├── personas.py        # persona 生成（种子 20261105）
├── experiments.py     # 9 个实验的提示词 / 解析 / 基线
├── run.py             # 运行器（调模型、写 JSONL）
├── analyze.py         # 单目录汇总分析
├── compare.py         # 双模型对照
├── DEPLOYMENT.md      # 本文件
├── USAGE.md           # 使用手册
├── DATA.md            # 数据来源与处理办法
├── research_plan.md   # 项目总纲
├── experiment_design_report.md   # 14 个实验的设计总报告
├── horton_baselines.md / provenance.md / literature_fetch_report.md
├── deepseek_vs_horton_interim.md / deepseek_vs_gemini_joint.md
├── cooperation_volunteering.md    # 自愿公共品实验档案
├── gemini_replication.md / unverified_theories.md
└── research_notes/
    ├── rmb_rates_fx_puzzle.md     # 人民币"利率下行、汇率上行"调研
    ├── ai_bubble.md               # AI 泡沫调研
    └── fama_baseline/             # Fama 回归基线（代码 + 数据 + 报告）
```

**不在仓库里的东西**：`results*/`（各轮原始输出 JSONL，可复跑
生成，体积大且持续增长）、`__pycache__/`、任何密钥文件。
`.gitignore` 已覆盖 `.env`、`*credentials*`、`*secret*`、
`*.pem`、`*.key`。

## 4. 凭据配置（二选一）

### 方式 A：在 Muse 环境中使用（本项目原始方式）

`run.py` 的 `call_model` 不读环境变量、不读密钥文件。
它从 Muse 的连接器目录加载 `dynamic_credentials`：

```python
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request
```

调用时把一个"替身凭证"（surrogate）挂到请求上，
Muse 在已批准的请求到达指定域名时才换成真实凭证。
支持的两个后端：

| 后端 | 端点 | 默认模型 | 注册连接 |
|---|---|---|---|
| DeepSeek（主模型） | `https://api.deepseek.com/v1/chat/completions` | `deepseek-chat` | `custom.deepseek` |
| Gemini（复核模型） | `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-3.8-flash` | `custom.gemini` |

注意：`gemini-2.5-flash` 已不对新用户开放（API 返回 404），
不要用它。`dynamic_credentials` 模块属于 Muse 环境，
**不在本仓库中**，克隆到别处后方式 A 不可用，改用方式 B。

### 方式 B：在普通环境中使用（自备 API Key）

把 `run.py` 中 `call_model` 的凭据部分替换为你自己的 Key。
最小改动示例（仅示意，不要把 Key 写进仓库文件）：

```python
import os
# 从环境变量读 Key，不要写进代码或提交进仓库
key = os.environ["DEEPSEEK_API_KEY"]
req = urllib.request.Request(
    "https://api.deepseek.com/v1/chat/completions",
    data=body,
    headers={"Content-Type": "application/json",
             "Authorization": f"Bearer {key}"})
```

Gemini 同理，把 URL 与 Key 换成你自己的端点与 Key
（Gemini 提供 OpenAI 兼容端点，见上表）。
Key 的保管规则：只放环境变量或密钥管理器，绝不进代码、
日志与 git 历史；`compare.py` 与 `analyze.py` 不碰凭据。

## 5. 验证部署

```bash
# 1) 干跑冒烟：不调 API，验证提示词渲染 + 解析 + 分析链路
python3 run.py --dry-run --n 8 --experiment dictator
python3 analyze.py --in results/dictator_classic.jsonl

# 2) 小规模实跑（8 次调用，确认凭据与端点通）
python3 run.py --experiment dictator --n 8 --variant classic
# 应输出：wrote .../results/dictator_classic.jsonl: parsed_ok=8 parse_fail=0

# 3) Fama 基线复算（需 numpy）
cd research_notes/fama_baseline && python3 fama.py
```

三步都通过，即部署成功。

## 6. 成本与耗时（实测）

- 单次调用延迟：DeepSeek 约 1.3 秒，Gemini 约 5.5 秒
  （Gemini 输出短，但内部思考 token 多约 400 个）。
- 并发：`--workers 8` 时 Gemini 一组 200 次约 2.5 分钟；
  DeepSeek 一组 200 次约 1 分钟。
- 费用（DeepSeek-V3 约 0.27/1.10 美元每百万输入/输出 tokens）：
  200 agent × 4 实验约 0.2 美元；放大 10 倍也只有几美元。
- 失败处理：单次调用失败重试 3 次（指数退避），仍失败只记
  一条空记录，不中断整轮；解析失败计入 `parse_fail`。

## 7. 常见问题

- **429 / 5xx**：`call_with_retry` 会自动重试；频繁出现时
  降低 `--workers`。
- **解析失败率高**：先用 `--dry-run` 检查提示词与解析器
  是否匹配；解析器只接受严格 JSON 块。
- **Gemini 404**：检查模型名是否为 `gemini-3.8-flash`；
  `gemini-2.5-flash` 已不对新用户开放。
- **结果目录混乱**：不同后端、不同轮次用不同的
  `--results-dir`（如 `results_gemini/`、`results_gemini_h3/`），
  不要混写；`compare.py` 靠目录区分双模型。
