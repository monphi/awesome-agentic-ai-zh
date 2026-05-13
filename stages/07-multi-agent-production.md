# Stage 7 — Multi-Agent · 進階應用

> **繁體中文** | [简体中文](./07-multi-agent-production.zh-Hans.md) | [English](./07-multi-agent-production.en.md)

⏱ **時間估算**：2-4 週（約 15-30 小時）

> 💡 用語密度高（multi-agent / handoff / eval / observability / guardrails⋯）→ 翻 [`resources/glossary.md` §4 + §6](../resources/glossary.md#4-multi-agent)。

> 📋 **本章組成**：〔Multi-Agent · 進階應用 是什麼（先定位）+ Discipline lineage + 何時用 multi-agent〕→ 學習目標 → 進入條件 → 必修閱讀 → Harness Engineering（**8 個核心元件含 Cost/Latency**）→ 動手練習（含練習 6 Cost Optimization）→ **Agent Benchmark Landscape + Berkeley Reward-Hacking 警告（2026）** → 常用工具推薦 → 精選 Projects → 自我檢查  
> 🔑 **關鍵名詞**：見 [`resources/glossary.md` §4 + §6](../resources/glossary.md#4-multi-agent)（multi-agent / orchestration / handoff / eval / observability / harness）

最後一個階段。你正從「我會做 agent」走向「我能讓 agent **真的給人穩定用**——多個 agent 協作、有 eval、有 observability、會 deploy」。**「進階應用 / production」 ≠ enterprise scale**——只要 agent 能穩定產出 + 給別人跑、就算進入這 stage 範圍。

## 🎯 Multi-Agent · 進階應用 是什麼（先定位）

**本 stage = 多 agent 怎麼協作 + 把 agent 從 prototype 推到能穩定給人用的程度**。三句話釐清範圍：

- **不是只學 framework**——Stage 4 已教 framework 怎麼挑
- **不一定要 enterprise scale**——只要 agent 能讓別人用、就算 "production"
- **核心是 harness engineering**——8 個 runtime 元件 + eval + observability + cost / latency 控制

**跟前後 stage 的分工**：

- **Stage 4** = 單 agent framework 怎麼挑、ReAct / Plan-Execute 等 pattern
- **本 stage** = **多 agent 協作** + **harness engineering**（runtime 工程）+ **deploy / observability / eval**

**Discipline lineage**（你現在在第 3 層 = 最上層）：

| 層 | Discipline | 解決什麼 | 在哪 stage |
|---|---|---|---|
| 1 | **Prompt Engineering** | 單次 LLM call 怎麼問才準 | [Stage 2](02-prompt-engineering.md) |
| 2 | **Context Engineering** | 跨多次 call 怎麼動態組 prompt | [Stage 6](06-memory-rag.md) |
| **3** | **Harness Engineering**<br>（**本 stage**） | **把多個 LLM call 包成可以給人跑的 runtime** | **本 stage** |

**本 stage 3 個 problem domain**：

1. **Multi-agent 協作** — debate / planner-executor / peer review / handoff / supervisor-worker pattern
2. **Harness Engineering** — agent loop / tool registry / context manager / safety / retry / telemetry / eval / cost（8 個 component、下面詳述）
3. **進階應用**（production-grade）— eval harness / observability / cost & latency 優化 / deploy

**跟 Stage 5 的分工**（避免混淆）：

| 跟誰比 | 那邊講什麼 | 本 stage 講什麼 |
|---|---|---|
| **Stage 5.5 Subagents** | Claude Code 原生 subagent 機制（markdown-based、不寫程式）| 通用 multi-agent framework（autogen / crewAI / langgraph、跨 vendor）|
| **Stage 5.6 Claude Code source** | Claude Code source 解剖（reference harness case study）| Harness engineering 通則（discipline-level、不綁特定 vendor）|

### ⚠ 但你真的需要 multi-agent 嗎？

**Multi-agent 不是 default、是 last resort**。**Anthropic 跟 Cognition 兩家 frontier lab 在 2024-2025 都明白寫過：90% 用例其實不該用 multi-agent**——硬上會付 **3-10× token、debug 困難、context fragmentation 嚴重**。

| 立場 | 來源 | 核心論點 |
|---|---|---|
| **Anthropic** | [Building Effective Agents (2024)](https://www.anthropic.com/engineering/building-effective-agents)、[How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/built-multi-agent-research-system) | 多數場景 simple workflow + single agent 就夠；multi-agent 只在「**研究型 / 並行探索**」任務真的有幫助 |
| **Cognition** | [Don't Build Multi-Agents (2025)](https://cognition.ai/blog/dont-build-multi-agents) | multi-agent 的 context fragmentation 嚴重、shared state 維護痛苦；先窮盡 single-agent + long-context 才考慮 |

**4 個明確訊號**才上 multi-agent（詳見 [Stage 4 §什麼時候真的需要 multi-agent](04-agent-frameworks.md#什麼時候真的需要-multi-agent不要硬上)）：

1. **任務天然分解** — 大任務有清楚子步驟、能 step-by-step 完成 → Sequential / Planner-Executor
2. **Token explosion** — single agent prompt 塞不下所有 tool description / context → Supervisor-Worker
3. **角色衝突** — 同一個 LLM 既當 writer 又當 critic 會 self-justify → Debate / Peer review
4. **平行加速** — 3 個 research 子任務同時跑、wall-clock 1/3 → Parallel / Map-Reduce

**4 個信號都不在？** → single agent + 好 prompt + tool use 就夠、別硬上 multi-agent。**本 stage 的 harness engineering 部分（8 個元件 / eval / observability）即使你最後用 single agent 也都會用到**——所以即使你決定不走 multi-agent、本 stage 仍是必修。

## 📌 學習目標

- 設計 multi-agent orchestration 模式（debate、planner-executor、peer review）
- 為 agent 架一套 evaluation harness
- 加上 observability（tracing、logging、cost tracking）
- 用 Anthropic SDK / OpenAI SDK 做 production deploy（進階功能：streaming、prompt caching、batching）
- 把 agent deploy 到 production（Docker、serverless、monitoring）

## 🚪 進入條件

你應該已經：
- 完成 Stage 4（用過至少一個 agent framework 跑 multi-agent demo）
- 完成 Stage 5（懂 MCP / Skills / Plugins / Subagents 各自角色，並用 §5.6 解剖過 harness 內部）
- 完成 Stage 6（會基本 RAG，能講出 memory pattern 差異）
- 對 Docker / git / CI 基礎熟悉（production deploy 會用到）

沒到的話 → 補完前面幾個 stage。本 stage 是「組合所有前面學到的東西 → 跑 production」，缺一塊都會卡。

## 📚 必修閱讀

1. [**Anthropic — Building Effective Agents**](https://www.anthropic.com/engineering/building-effective-agents) — 用 production 的角度再讀一次
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 90% 成本下降的技巧
3. [**Anthropic — Message Batches API**](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) — 非同步 batch job
4. **任一 eval framework 的文件** — promptfoo 或 LangSmith 或 weave
5. [**ai-boost/awesome-harness-engineering**](https://github.com/ai-boost/awesome-harness-engineering)（★ 780+）— agent harness 的工具 / pattern / eval / memory / MCP / observability 全集合
6. [**ZhangHanDong/harness-engineering-from-cc-to-ai-coding**](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding)（★ 1.3k+）— 從 Claude Code 原始碼學 harness 設計（中文）

## 🏗 Harness Engineering — production agent runtime 的工程學 ⭐ 本 stage 核心概念

### Discipline 定位：prompt → context → harness 三層

把 LLM 用成 production agent 系統、有 3 層**工程學科**（discipline）。每一層 cover 不同問題、後一層假設前一層已經沒問題：

| Discipline | 解決什麼問題 | 主要技巧 | 在哪學 |
|---|---|---|---|
| **1. Prompt Engineering** | 單次 LLM call 怎麼問才會準 | system prompt / few-shot / CoT / structured output | **[Stage 2](02-prompt-engineering.md)** |
| **2. Context Engineering** | 跨多次 call 怎麼動態組裝 prompt | RAG retrieval / memory / context window 管理 / tool description 排序 | **[Stage 6](06-memory-rag.md)** + Stage 2 §進階 |
| **3. Harness Engineering**<br>（**本節**） | 把多個 LLM call 包成 production agent runtime | agent loop / retry / safety / telemetry / observability / cost control | **本 stage** |

→ **2025 後段「harness engineering」才正式成為業界共識詞**（Anthropic / Cursor / Cognition 等 AI coding tool 團隊用得最多）——因為前兩層已經被 prompt eng / context eng 解決得差不多了、production agent 的剩餘複雜度都在 runtime 工程。

### Harness 的 8 個核心元件

**Harness = 把 LLM agent 包成 production 系統的「工具帶」**。一個 production agent runtime 包含這 8 個元件（前 6 個是 runtime 內建、第 7 個 eval 是外掛工具、第 8 個 cost / latency 是 cross-cutting concern 跨所有層）：

| 元件 | 做什麼 | 對應本 stage 練習 |
|---|---|---|
| **Agent loop** | 「LLM → tool → result → LLM」迴圈、穩定處理多輪 | 練習 1 multi-agent 辯論 |
| **Tool registry** | 動態 tool dispatch、permission gate、sandboxing | （在每個 framework / SDK 都有）|
| **Context manager** | message history 管理、context window 控制、auto-compact | Stage 6 + 本 stage 練習 4 SDK |
| **Safety layer** | permission prompts、sandboxed exec、destructive op 攔截 | （Claude Code 內建、SDK 可自訂）|
| **Retry / recovery** | tool fail 怎麼處理（exception vs LLM 自己看 error 反思） | 練習 4 SDK 進階 |
| **Telemetry / Observability** | metrics、logging、token counting、trace export | **練習 3 Observability** |
| **Eval harness** | regression test、quality gate、A/B test | **練習 2 Eval** |
| **Cost / Latency optimization** ⭐ 2024-2026 必修 | prompt caching、model routing、thinking budget、batching、semantic cache | **練習 6 Cost optimization**（新加）|

**Framework vs Harness 關鍵差別**：
- **Framework**（[Stage 4](04-agent-frameworks.md)）規範 **API** — 你呼叫的介面長什麼樣
- **Harness**（本節）規範 **runtime** — 怎麼跑、怎麼 recovery、怎麼觀測

### Reference 實作

想看 production-grade harness 長什麼樣？兩個 reference：

- **Claude Code 整個 runtime** — 是 reference harness 實作。**讀 source 練習見 [Stage 5.6](05-claude-code-ecosystem.md#56--claude-code-source-解剖reference-harness-implementation-track-b-必看)**（clone `claude-agent-sdk-python` 解剖 main loop + 上表前 6 個 runtime 元件位置；第 7 個 Eval harness 是外掛、第 8 個 Cost / Latency 是 cross-cutting、見下方深入段）
- **`anthropics/claude-agent-sdk-python`** source — 上面練習用的具體 repo

→ 本 stage 剩下的 6 個練習（multi-agent / eval / observability / SDK / deploy / cost）每個都是 harness 的一個面向。學完整 stage = 拼出完整的 harness engineering mental model。

### 第 8 個 component 深入 — Cost / Latency Optimization（2024-2026 production 必修）

Production agent 跑久了、**cost / latency 兩條線會吃掉你大半預算與用戶體驗**。2024-2026 frontier model 都把這當 first-class API feature——**會用 = 省 50-90% cost / latency**。

| 技巧 | 怎麼省 | 2026 狀態 |
|---|---|---|
| **Prompt caching** | 重複 prefix（system prompt、long context）一次計費、後續 cache hit 折扣 ~90% | Anthropic / OpenAI / Gemini 全支援、自動或手動標記 |
| **Model routing / cascade** | 簡單 query → 小 model、難 query → frontier model | [RouteLLM](https://github.com/lm-sys/RouteLLM) / [OpenRouter](https://openrouter.ai/) production 內建 |
| **Thinking budget** | reasoning model 可控 thinking token 上限、trade latency / quality | Claude / Gemini API 參數、o-series 預設高 |
| **Speculative decoding** | 小 model 預測 N token、大 model 一次驗證、單 model 速度 ×2-3 | vLLM / TGI 內建、推論層自動 |
| **Batching** | 多 query 並行處理、GPU 利用率高 | vLLM、production inference layer |
| **Semantic caching** | 相似 query 共用回答（不只 exact match）| [GPTCache](https://github.com/zilliztech/GPTCache) / Helicone 內建 |

**Track A 怎麼用**（用 CLI agent 的人）：
- 在 Claude Code / Cursor 設定 prompt caching、daily session 省 50-90% cost
- 用 [RouteLLM](https://github.com/lm-sys/RouteLLM) / [OpenRouter](https://openrouter.ai/) 動態切換 model（簡單問用 Haiku / Flash、難問用 Opus / Pro）
- Claude API 用 `thinking_budget` 參數控 reasoning model 的 token 上限

**Track B 怎麼 build**（自己寫 agent 的人）：
- 自架 cascade router、把 query embedding → classifier → model 對應
- 在 agent loop 內監控 token cost、超 budget 自動降級
- production deploy 整合 semantic cache 層
- [Helicone](https://github.com/Helicone/helicone) / [langfuse](https://github.com/langfuse/langfuse) 等 observability 平台都已內建這幾招、不用自己寫

## 🛠 動手練習（基礎 illustrative 練習）

### 練習 1：Multi-Agent 辯論
兩個 agent 辯論一個題目（例如「該用 Python 還是 Rust 寫 backend」），第三個 agent 當裁判。觀察辯論收斂或分歧的 pattern。

### 練習 2：Eval
替你前面的 agent 寫一份 eval，跑 N 次量成功率。把「我用眼睛看一下」的習慣換掉。

### 練習 3：Observability
把 LangSmith、Helicone、或 weave 接上一個 agent，看完整 trace。理解「沒 observability 的 agent debug = 黑盒」。

### 練習 4：SDK 進階
在同一次呼叫裡用 streaming + prompt caching + tool use。看成本怎麼降下來。

### 練習 5：Deploy
把一個 agent 包進 Docker，deploy 到雲端（任何 provider 都行）。學會把 prototype 變成可以給別人跑的東西。

### 練習 6：Cost Optimization（新加）⭐
量你前面任一個練習 agent 的 token cost、加上 prompt caching、再量一次。觀察 cache hit rate 跟 cost 下降的對應關係。**Bonus**：接 [RouteLLM](https://github.com/lm-sys/RouteLLM) 或 [OpenRouter](https://openrouter.ai/)、做 cascade routing（簡單 query → Haiku / 難 query → Opus），量平均 cost。

## 📊 Agent Benchmark Landscape（2026-05 最新）+ ⚠ Reward-Hacking 警告

挑 model / build agent 之前、你會想看 benchmark 數字——但 **2026-04 UC Berkeley 發現 8 個主流 agent benchmark 全部可被 reward-hack 到 ~100%**。下面是 2026 leaderboard 現況 + 怎麼看不被騙。

### 主流 Agent Benchmark 2026-05 SOTA

| Benchmark | 領域 | 2026-05 SOTA | 領先 Model |
|---|---|---|---|
| [**SWE-bench Verified**](https://www.swebench.com/) | 軟工 / code agent | **87.6%** | Claude Opus 4.7 |
| [**Terminal-Bench**](https://github.com/laude-institute/terminal-bench) | terminal 任務 | 領先 | Claude Opus 4.5 / 4.7 |
| **GAIA** | general assistant | **74.6%** | Claude Sonnet 4.5（Princeton HAL）|
| [**WebArena**](https://github.com/web-arena-x/webarena) | web 導航 | **68.7%** | Claude Mythos Preview |
| [**OSWorld**](https://github.com/xlang-ai/OSWorld) | OS-level 桌面控制 | ~**38%** | （仍困難、有大幅成長空間）|
| [**τ-bench**](https://github.com/sierra-research/tau-bench) | tool use 多輪對話 | （較難 hack）| Anthropic / OpenAI 領先 |
| **RE-bench** | research engineering | （較難 hack、接近人類 baseline）| Frontier model |

→ 詳細排行 + 即時更新：[Agent Benchmark Leaderboard 2026](https://benchmarkingagents.com/agent-benchmarks/)、[Rapid Claw AI Agent Framework Scorecard 2026](https://rapidclaw.dev/blog/ai-agent-benchmarks-2026)

### ⚠ Berkeley 2026-04 Reward-Hacking 警告

[**UC Berkeley RDI 2026-04-12 報告**](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/)：用 automated scanning agent 系統性 audit **8 個主流 benchmark**（SWE-bench / WebArena / OSWorld / GAIA / Terminal-Bench / FieldWorkArena / CAR-bench 等）、**每個都能 reward-hack 到接近 100%、agent 一個 task 都不用真正解**。

意思：leaderboard 上「Claude 87.6% / GPT 85.0%」這種數字、可能其中 X% 是 hack 出來的、不是真的解 task。

### 怎麼看 benchmark 不被騙

| 看數字方式 | 推薦 |
|---|---|
| 只看 leaderboard top | ❌ 上面 8 個都被證實可 hack |
| 看 task-level success rate breakdown | ✅ 多數 hack 集中少數 task |
| 跑你自己的 hold-out test set | ✅✅ 最可靠、production agent 必做 |
| 看 trajectory / log 是否真的解 task | ✅ 區分 reward hacking vs genuine solve |
| 看多個 benchmark + 自己 use case | ✅ 不依賴單一指標 |

**哪些 benchmark 較難 hack（2026-05）**：
- **τ-bench** — 多輪對話 + tool use、reward function 較密集
- **RE-bench** — research engineering 真實任務
- **你自己的 production eval set** ⭐ 永遠是最可靠的

> 💡 **production agent 的 eval 紀律**：
> - 不要把外部 benchmark 數字當 ground truth、它告訴你「上限」不是「真實表現」
> - 你自己的 eval set（內部 hold-out test）才是 production decision 的依據
> - 每次 model upgrade → 跑內部 eval set 驗證、不只看廠商公布的 benchmark 提升
> - 接 [langfuse](https://github.com/langfuse/langfuse) / [promptfoo](https://github.com/promptfoo/promptfoo) 把 eval 自動化、每次 deploy 都跑

## 🎯 常用 Multi-Agent / Production 工具推薦（按用途分類）

不知道從哪挑工具？下面是 2025-2026 業界常用搭配——**挑入口看「場景」、想深入點連結看 repo**：

| 場景 | 推薦工具 | 為什麼 |
|---|---|---|
| **第一次寫 multi-agent**（最快上手）| [crewAI](https://github.com/crewAIInc/crewAI) | role-based、幾行 code 跑起來、production pattern 直接 |
| **想要 group debate / brainstorm pattern** | [AutoGen](https://github.com/microsoft/autogen) | GroupChat 自由辯論、Microsoft 出品 |
| **production 要 audit trail / checkpoint / human-in-loop** | [LangGraph](https://github.com/langchain-ai/langgraph) | state machine、控制最完整 |
| **eval 標準化**（CI / regression 必裝）| [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | YAML config、跨模型比較、★ 20k+ |
| **eval + observability 同平台** | [langfuse](https://github.com/langfuse/langfuse) ⭐ | OSS、tracing + eval + prompt mgmt、★ 26k+ |
| **不改程式、快速 instrumentation** | [Helicone](https://github.com/Helicone/helicone) | proxy 中介、不綁 framework |
| **全 stack 在 LangChain** | [LangSmith](https://www.langchain.com/langsmith)（商業）| LangChain 官方 observability |
| **打造 Claude agent**（programmatic）| [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ | Anthropic 官方 agent SDK、跟 Claude Code 同 runtime |
| **Deploy agent 成 API service** | [BentoML](https://github.com/bentoml/BentoML) | 最完整、Docker + serving |
| **自架開源 LLM**（取代付費 API）| [vLLM](https://github.com/vllm-project/vllm) | 高吞吐量、★ 79k+ |
| **Fine-tune 開源 LLM** | [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | 100+ 模型統一 SFT/DPO/PPO/GRPO、Web UI 零 code、中文社群最廣、★ 70k+ |

**建議入手順序**：
1. 第一個 multi-agent：**crewAI**（role-based、最簡單）
2. 加 eval：**promptfoo**（YAML、CI 整合）
3. 加 observability：**langfuse**（OSS、完整）
4. Production 升級：換 **LangGraph**（control 強）+ **BentoML**（deploy）
5. 進階：自架 LLM 接 **vLLM**、fine-tune 用 **LLaMA-Factory**

## 🎯 精選 Projects（範本 / SDK / 工具 collection）

按用途分類、22 個項目一張表搞定。**挑入口看「適合誰」、想深入點連結看 repo**。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **Multi-Agent Orchestration** | [microsoft/autogen](https://github.com/microsoft/autogen) | ⭐⭐⭐⭐⭐ | 想要 GroupChat 自由 debate pattern | Stage 4 介紹過、production 場景再回頭看 multi-agent 辯論 / brainstorming 模式 |
| | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | ⭐⭐⭐⭐⭐ | 想要 role-based 流水線 | 角色式 multi-agent（research → writer → reviewer），最簡單 production pattern |
| | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | ⭐⭐⭐⭐⭐ | 需要 audit trail / checkpoint / human-in-the-loop | state machine 路線、production 控制最強 |
| **Eval Frameworks** | [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | ⭐⭐⭐⭐⭐ | 把 eval 流程標準化、CI 整合 | YAML config、跨模型比較。★ 20k+、MIT |
| | [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | ⭐⭐⭐⭐ | 學術 benchmark 主張（MMLU / HellaSwag / GSM8K）| 學術等級。★ 12k+、MIT |
| | [openai/evals](https://github.com/openai/evals) | ⭐⭐⭐⭐ | OpenAI 專屬 eval / 想回饋上游 | ★ 18k+ |
| **Observability** | [langfuse](https://github.com/langfuse/langfuse) ⭐ | ⭐⭐⭐⭐⭐ | 自架 production observability | OSS LangSmith 替代、traces + sessions + evals + prompt mgmt。★ 26k+、MIT |
| | [LangSmith](https://www.langchain.com/langsmith)（商業）| ⭐⭐⭐⭐ | 全 stack 在 LangChain / LangGraph 上 | LangChain 官方、只有 hosted 版 |
| | [Helicone](https://github.com/Helicone/helicone) | ⭐⭐⭐⭐ | 不想改程式、快速上 instrumentation | proxy 中介、順便拿到 logging + caching。★ 5k+、Apache 2.0 |
| | [weave (W&B)](https://github.com/wandb/weave) | ⭐⭐⭐⭐ | 團隊已在用 W&B 做 ML 實驗追蹤 | W&B tracing + eval、跟 wandb 整合 |
| **Anthropic SDK 進階** | [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) | ⭐⭐⭐⭐⭐ | 直接基於 Claude API 做應用 | 官方 Python SDK：streaming / async / tool use / prompt caching / batches / files |
| | [anthropic-sdk-typescript](https://github.com/anthropics/anthropic-sdk-typescript) | ⭐⭐⭐⭐ | TypeScript / Node / web app | Python SDK 的 TS 版 |
| | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) ⭐ | ⭐⭐⭐⭐⭐ | 打造 Claude-based agent 而非只 API | 內建 tool use loop / file access / sandbox / subagent 編排；跟 Claude Code 同 runtime、想看內部運作直接讀 source。★ 6k+、MIT |
| | [claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript) | ⭐⭐⭐⭐ | Node / web app 環境 Claude agent | Claude Agent SDK TS 版。★ 1.4k+ |
| | [Anthropic Cookbook（進階）](https://github.com/anthropics/anthropic-cookbook) | ⭐⭐⭐⭐ | 想看官方進階 SDK pattern | 特別是 `prompt_caching.ipynb` / `tool_use/` / `multimodal/` 三個 notebook |
| **Deployment** | [BentoML](https://github.com/bentoml/BentoML) | ⭐⭐⭐⭐ | 把 agent 包成 production API service | Docker + serving framework。★ 8k+、Apache 2.0 |
| | [LangServe](https://github.com/langchain-ai/langserve) | ⭐⭐⭐⭐ | LangChain agent 快速 deploy | 底層 FastAPI |
| | [vLLM](https://github.com/vllm-project/vllm) | ⭐⭐⭐⭐ | 自架開源 LLM 取代付費 API | 高吞吐量 LLM serving、Llama / Qwen 等。★ 79k+、Apache 2.0 |
| **中文 deploy / fine-tune** | [datawhalechina/self-llm](https://github.com/datawhalechina/self-llm) | ⭐⭐⭐⭐ | 中文團隊要自架開源 LLM | training-to-deployment 完整中文指南、Qwen / Llama / GLM / 多模態。★ 30k+、Apache 2.0 |
| | [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | ⭐⭐⭐⭐⭐ | 要 fine-tune 開源 LLM（不只 prompt eng）| 100+ 模型統一 SFT/DPO/PPO/GRPO、Web UI 零 code、中文社群最廣。★ 70k+、Apache 2.0 |
| **Multi-Agent 案例研究** | [geekan/MetaGPT](https://github.com/geekan/MetaGPT) | ⭐⭐⭐⭐⭐ | 想看角色分工 + artifact 交接 pattern | SOP-based PM / Architect / Engineer multi-agent team、PRD → 設計 → code 一路產出。★ 67k+、MIT |
| | [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev) | ⭐⭐⭐⭐ | 想看 agent debate / peer-review pattern | 對話式軟體開發、agents 在 design / code / test 互相辯論。★ 33k+、Apache 2.0、有 zh README |
| | [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent) | ⭐⭐⭐⭐ | 理解為什麼 tool 設計 > prompt tuning | Agent-Computer Interface (ACI) 設計思路、Princeton paper-backed、SWE-Bench 領先方法。★ 19k+、MIT |

> 🌳 **Claude 原生 subagent 機制**（不用 framework 也能 multi-agent）見 [Stage 5.5](05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制)。本 stage 重 framework / production；Stage 5.5 重 markdown-based subagent 編排。

## ✅ Stage 7 之後的自我檢查

你能不能：
- [ ] 設計一個 multi-agent 系統，協作協定講得清楚
- [ ] 在 CI 跑自動 eval pipeline
- [ ] 把 observability（tracing）接到 production agent
- [ ] 在真實 workload 上量測 prompt caching 前後的成本差異
- [ ] 把 agent deploy 到雲端（任何 provider）

如果都可以 → 你已經跑完主路線。挑一個[特化分支](../README.md#️-7-階段學習地圖)，或回過頭來貢獻這份 repo。

## 💡 接下來

你已經有基礎能力了。接下來 6-12 個月應該專注在：
1. **挑一個 production 系統** 從 prototype 推到 production
2. **回饋上游**（LangGraph、AutoGen、MCP servers、Anthropic cookbook）
3. **讀論文**——agent 研究進展很快
4. **做出看得到的東西**——開源一個真的工具，不要再寫教學了
