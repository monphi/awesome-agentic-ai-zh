# Stage 1 — LLM Fundamentals

> [繁體中文](./01-llm-basics.md) | [简体中文](./01-llm-basics.zh-Hans.md) | **English**


⏱ **Time estimate**: 1 week (~5-8 hours)

> 👋 **Coming from [Stage 0](00-foundations.en.md)?** Nice — your toolchain is set. The next 5-8 hours: your first working call to Claude / GPT / Gemini, how token / context window / temperature shape the output, and per-token cost estimation. **Jumped straight here?** Make sure you can run a Python script and have an API key from one provider — if not, head back to [Stage 0](00-foundations.en.md).

> 💡 **Don't recognize a term?** (LLM / token / context window / temperature / RAG / agent / …) → check [`resources/glossary.en.md`](../resources/glossary.en.md) for 30-second definitions.

### 3 Core Terms (memorize these—all later stages use them)

| Term | Chinese | One-liner |
|---|---|---|
| **token** | 詞元 | the unit LLMs use to count text length and price (1 Chinese char ≈ 1.5-2 tokens; 1 English word ≈ 1.3 tokens) |
| **context window** | 上下文視窗 | How many tokens the model sees at once (Claude 1M / GPT ~400k / Gemini 2M) |
| **temperature** | 隨機程度參數 | Controls how stable or creative the output is (0 = deterministic, 1 = creative; use 0.0-0.3 for classification, 0.7-1.0 for creative writing) |

→ These 3 terms run through every later stage. The goal of Stage 1 is to call the API yourself and feel firsthand how they shape the output.

## 📌 Learning Goals

After this stage you will be able to:
- Explain what an LLM is, what tokens are, and what context window means
- Make your first API call to Claude / GPT / Gemini and parse the response
- Compare the four major LLM families (Claude / GPT / Gemini / Llama) on strengths
- Estimate cost per task using per-token pricing

## 🌐 Major LLM Family Comparison (2026-05 snapshot)

"How is Claude different from GPT?" "Can I use Chinese models?" "Which OSS model should I run with Ollama?" This section gives you an **objective side-by-side view**. It does not declare a single "best" model: it compares **strengths / good-fit tasks / weaknesses** and includes **official docs URLs** so you can verify the claims yourself.

> 💡 **First, a few terms**:
> - **Context window** = the amount of conversation an LLM can remember in one pass; it is capped (for example, 200k tokens ~= 150k Chinese characters)
> - **Apache 2.0 / MIT** = open-source terms that permit commercial use, modification, and closed-source redistribution; **Llama Community License** = open-source but with conditions (for example, orgs with >= 700M MAU need a license)
> - **Frontier model** = each provider's strongest flagship; **OSS** = open-source, with weights downloadable for self-hosting

### 🇺🇸 US Commercial Frontier (3 providers)

These 3 are SaaS APIs: you pay per token and cannot self-host them.

| Model family | Flagship (2026-05) | Context | Strengths | Best for | Official docs |
|---|---|---|---|---|---|
| **Claude** (Anthropic) | Opus 4.7 / Sonnet 4.6 / Haiku 4.5 | 1M (Haiku 4.5 is 200k) | long-form / coding / agent / safety alignment | writing papers / code review / agent runtime | [platform.claude.com/docs](https://platform.claude.com/docs/en/about-claude/models/overview) |
| **GPT** (OpenAI) | GPT-5.5 / GPT-5 / o-series | ~400k | general-purpose / function calling / broadest ecosystem | broad queries / function-call frameworks / GPTs ecosystem | [platform.openai.com/docs/models](https://platform.openai.com/docs/models) |
| **Gemini** (Google) | 3.1 Pro / Flash | **2M** (Pro series; Flash is 1M) | long context / native multimodal / Google integration | PDF / video and audio / large document sets / Google Workspace | [ai.google.dev](https://ai.google.dev/gemini-api/docs/models/gemini) |

### 🇨🇳 Chinese Commercial + Open-Source Frontier (7 providers)

These are the main choices for Chinese-language work. Some are API-only (DeepSeek / Kimi / Hunyuan); others also release **OSS weights** (Qwen / GLM-5.1 / Yi can run through Ollama).

| Model family | Flagship (2026-05) | Context | Strengths | Best for | License | Official |
|---|---|---|---|---|---|---|
| **DeepSeek** | V3 (`deepseek-chat`) / R1 (`deepseek-reasoner`) ⚠️ V4-series weights are open-source; consumer API is not fully public yet | 128k | reasoning / coding / **lowest cost** | high-token workloads / code generation / math | API proprietary; some weights OSS on HF | [api-docs.deepseek.com](https://api-docs.deepseek.com/zh-cn/) |
| **Qwen** (Alibaba) | Qwen3 (cloud DashScope + Apache 2.0 OSS) | 128k+ | **strongest Chinese OSS** / multimodal / agent | Chinese long-form writing / agent / self-host | Apache 2.0 (OSS) + proprietary (cloud) | [qwen.ai](https://qwen.ai/) · [DashScope](https://help.aliyun.com/zh/dashscope/) |
| **Kimi** (Moonshot) | K2.6 multimodal + Agent | **very long context (1M+)** | long context / Chinese long-form writing | whole-book reading / literature triage | Proprietary | [platform.moonshot.cn](https://platform.moonshot.cn/) |
| **GLM** (Zhipu) | GLM-5 proprietary / GLM-5.1 Apache 2.0 | 128k | Chinese / tool use / agent | Chinese agents / multi-turn chat | proprietary + Apache 2.0 (5.1) | [open.bigmodel.cn](https://open.bigmodel.cn/) · [chatglm.cn](https://chatglm.cn/) |
| **Hunyuan** (Tencent) | T1 (deep-thinking, Transformer-Mamba MoE) + TurboS | 128k | **DeepSeek R1-comparable reasoning**, Chinese | Chinese reasoning / Tencent ecosystem | Proprietary | [hunyuan.tencent.com](https://hunyuan.tencent.com/) |
| **MiniMax** | abab6.5 + M2.7 | 200k | multimodal / Chinese long prose | Chinese writing / video and audio multimodal | Proprietary | [platform.minimax.io](https://platform.minimax.io/) |
| **Yi** (01.AI / Kai-Fu Lee) | Yi-Lightning (new API flagship) / Yi-34B-Chat (OSS, 200k context) | 200k | **Chinese OSS** alternative to Llama | Chinese self-host / Chinese API | Apache 2.0 (OSS) / proprietary (Lightning) | [01.ai](https://01.ai/) · [GitHub](https://github.com/01-ai/Yi) |

> ⚠️ **Xiaomi MiMo** is listed in [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md) for Hermes Agent routing, but as of 2026-05 there is no authoritative official source to verify it, so it is not included in this table. To try it, connect through [Hermes Agent](https://github.com/NousResearch/hermes-agent) 200+ provider routing.

### 🌍 Western Open-Source (4 providers, self-host defaults)

These are the main choices for running on your own hardware, avoiding API fees, or handling privacy-sensitive work. You can install them in one command through [Ollama](https://ollama.com/).

| Model family | Active size | License | Strengths | Best for | Official |
|---|---|---|---|---|---|
| **Llama** (Meta) | 3.3 70B (**Llama 4 not yet released as of 2026-05**) | Llama Community License | general-purpose / broadest ecosystem / Ollama default | self-hosting intro / fine-tune base | [llama.com](https://www.llama.com/) · [HF Meta](https://huggingface.co/meta-llama) |
| **Gemma** (Google) | Gemma 4 26B MoE + 31B dense (released 2026-04; Arena #3) | Apache 2.0 | **small and efficient** / strong Apple MLX integration / multimodal | edge / mobile / 4-8 GB RAM machines | [ai.google.dev/gemma](https://ai.google.dev/gemma) |
| **Mistral** (Mistral AI) | 7B / Mixtral 8x7B / Codestral | Apache 2.0 (OSS parts) | strongest open-source 7B class | commercial self-host / EU sovereignty | [mistral.ai](https://mistral.ai/) · [HF Mistral](https://huggingface.co/mistralai) |
| **Phi** (Microsoft) | Phi-4 14B reasoning + Phi-4-multimodal-instruct (multimodal version) | MIT | **small but strong** / reasoning / edge-friendly | 4 GB+ RAM / mobile / reasoning intro | [HF microsoft](https://huggingface.co/microsoft) |

### 🎯 Which One Should I Pick? (by scenario)

| Your scenario | Pick + why |
|---|---|
| First time learning an LLM API, prioritize complete tutorials | **Claude** — Anthropic Cookbook + Courses are widely considered the most complete |
| Long-form writing / papers / code review | **Claude Sonnet** — long-form prose is a core strength |
| Multimodal (PDF / video and audio / images) | **Gemini** or **Kimi** — native multimodal |
| Broad queries + function calling frameworks | **GPT** — broadest ecosystem and deepest SDK integration |
| **Chinese scenarios + commercial API** | **Kimi** (strong long context; can fit whole books), **DeepSeek** (lowest cost), or **GLM** (agent-friendly) |
| **Chinese scenarios + open-source self-host** | **Qwen 3** (Apache 2.0; currently the strongest Chinese OSS) |
| Reasoning / math (reasoning model) | **DeepSeek R1** / **Hunyuan T1** / **OpenAI o-series** |
| Privacy / offline / no API fees | **Llama 3.3** / **Gemma 4** / **Qwen 3 OSS** via [Ollama](https://ollama.com/) |
| Edge / 4 GB RAM machine | **Gemma 4** / **Phi-4** / **Qwen 3 (`qwen3-3B` or smaller variants)** |
| 100k+ token large documents | **Gemini 3.1** (2M context) or **Kimi K2.6** (1M+) |
| **Want the lowest cost** (API-bill sensitive) | **DeepSeek V4-Flash** — lowest token price among same-tier English models |

### 📊 Neutral Benchmark Resources (verify for yourself; do not rely on one source)

| Resource | Use | URL | 2026-05 status |
|---|---|---|---|
| **Artificial Analysis** | Third-party benchmarks plus price/latency aggregation, including Chinese models | https://artificialanalysis.ai/ | ✓ Active |
| **Arena AI** (formerly LMSYS Chatbot Arena) | Human blind-test ELO leaderboard | https://arena.ai/leaderboard/text | ✓ Active |
| **Vellum LLM leaderboard** | Aggregates multiple benchmarks | https://www.vellum.ai/llm-leaderboard | ✓ Active |
| **HuggingFace OpenLLM Leaderboard** | Open-source model rankings | https://huggingface.co/spaces/open-llm-leaderboard | ⚠️ Occasional runtime errors as of 2026-05; use the [Arena AI](https://arena.ai/) open-source tab as fallback |
| **SuperCLUE** | Authoritative benchmark for Chinese-language scenarios | https://www.superclueai.com/ | ✓ Active |

### ⚠️ Important Caveats

- ⚠️ **Benchmark != production performance**: run a small eval on your specific task (for example, paste 10 real prompts and see which model answers closest to what you need); **do not pick only from rankings**
- ⚠️ **Frontier changes every 6 months**: all numbers above are a **2026-05 snapshot**; afterward, rely on **official docs** / [Artificial Analysis](https://artificialanalysis.ai/)
- ⚠️ **"Strength" is relative, not absolute**: every frontier model can handle basic tasks; differences matter at the margin
- ⚠️ **For Chinese scenarios, check [SuperCLUE](https://www.superclueai.com/)**: general international benchmarks such as MMLU are English-heavy, and Chinese-language performance may diverge

## 🚪 Entry Conditions

You should already:
- Be able to run a Python script
- Know what HTTP / REST is conceptually
- Have an API key from at least one provider (Anthropic / OpenAI / Google)

If not — go back to Stage 0 first.

## 📚 Required Reading

1. [**Anthropic — Claude Model Overview**](https://docs.claude.com/en/about-claude/models/overview) — official model family overview, including 2026's latest Opus 4.7 / Sonnet 4.6 / Haiku 4.5
2. [**anthropics/courses — Anthropic API Fundamentals**](https://github.com/anthropics/courses) ⭐⭐⭐⭐⭐ ★ 21k+ — Anthropic's official 5-course umbrella; **module 1 "Anthropic API Fundamentals" maps to this stage**. Jupyter notebooks, runs on Claude 3 Haiku (cheapest), hands-on walkthrough of API essentials.
3. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) — first API call walkthrough
4. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) — Hugging Face's intro
5. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) — read the pricing table, calculate cost for 1k input + 1k output

## 🛠 Hands-on Exercises (foundational, illustrative)

> 🦙 **This stage defaults to Ollama** (cost-driven; `gemma4:e4b` runs locally for $0/run). Every exercise has Path A (Ollama, default) + Path B (Anthropic, optional — use it when you want to see cloud-quality answers). Full three-path trade-off in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).
>
> 💰 **Stage 1 budget estimate** (all 6 exercises, 3-5 runs each): **all local = $0**, **all haiku ≈ $0.30**, **all sonnet ≈ $0.90**. Full model list + Stage 1-7 total budget: [`examples/README.en.md#recommended-llm-list`](../examples/README.en.md#recommended-llm-list-local--cloud-user-perspective).
>
> 💡 **No Ollama yet?** Each exercise also ships a Path B Anthropic version — pick one. To enable Path A in one step: [`pip install openai && ollama pull gemma4:e4b`](https://ollama.com).

### Exercise 1: LLM API (hello world)
Five-line Python script that calls an LLM and prints the response. **Defaults to local Ollama (free, offline)**; switch to Path B Anthropic when you want cloud-quality answers. Details in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).

<details open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_1.py</code> and run <code>python practice_1.py</code>)</summary>

```python
# Requires: pip install openai      (OpenAI-compatible SDK talks to Ollama)
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't check this — anything works
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # swap to qwen2.5:3b / llama3.2:3b if preferred
    max_tokens=100,
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)

# === Self-check ===
text = r.choices[0].message.content
print("Response:", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"unexpected finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "response should not be empty"
assert r.usage.completion_tokens > 0, "output token count should be > 0"
print("✅ Exercise 1 passed — local Ollama gemma4:e4b answered for $0")
```

**How slow?** Gemma 4B on CPU: ~5-30 s/answer; on GPU (RTX 3060+): <2 s. For speed use `gemma3:1b`; for quality use `qwen2.5:14b` / `llama3.3:8b` (needs 8 GB+ VRAM).

</details>

<details>
<summary>📋 <b>Starter code — Path B (Anthropic API, optional, when you want cloud quality)</b> (copy to <code>practice_1_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
# Env: export ANTHROPIC_API_KEY=sk-ant-...
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",  # haiku = cheapest; switch to sonnet by changing this line
    max_tokens=100,
    messages=[{"role": "user", "content": "Introduce yourself in one sentence."}],
)

# === Self-check ===
text = msg.content[0].text
print("Response:", text)
print("usage:", msg.usage)

assert msg.stop_reason in ("end_turn", "max_tokens"), f"unexpected stop_reason: {msg.stop_reason}"
assert len(text) > 0, "response should not be empty"
assert msg.usage.input_tokens > 0 and msg.usage.output_tokens > 0, "token counts should be > 0"
print("✅ Exercise 1 passed — Anthropic API is reachable from your machine")
```

**Cost**: ~$0.001/run (haiku) or ~$0.004/run (sonnet); this hello-world is also 5-15× faster than Ollama.

</details>

### Exercise 2: Tokens
Run the same prompt 100 times and watch token counts vary.
- Notice: `temperature ≠ 0` produces variation
- Notice: token count for the SAME English vs Chinese sentence

<details open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_2.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "Chinese": "用一句話描述一隻貓在做什麼。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # local is slower; start small
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=80,
            temperature=1.0,  # high temp to amplify variance
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === Self-check ===
assert max(output_tokens) > min(output_tokens), "with temperature=1.0, output length should vary"
print("\n✅ Exercise 2 passed — observed temperature → token variance, $0/run")
print("💡 Chinese prompts typically use MORE input tokens (one Chinese character ≈ 2 tokens)")
```

</details>

<details>
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_2_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()
PROMPTS = {"Chinese": "用一句話描述一隻貓在做什麼。", "English": "Describe in one sentence what a cat is doing."}

for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(20):
        msg = client.messages.create(model="claude-haiku-4-5", max_tokens=80, temperature=1.0,
                                     messages=[{"role": "user", "content": prompt}])
        output_tokens.append(msg.usage.output_tokens)
    print(f"[{label}] input={msg.usage.input_tokens} output min/max/mean={min(output_tokens)}/{max(output_tokens)}/{sum(output_tokens)/len(output_tokens):.1f}")
```

**Key SDK diffs**: `messages.create` → `chat.completions.create`; `usage.output_tokens` → `usage.completion_tokens`; `usage.input_tokens` → `usage.prompt_tokens`. **Cost**: 40 runs ≈ $0.01.

</details>

### Exercise 3: Pricing / Latency
**Cost-sensitive work required**: compute how long and how much it takes to run 1000 hello-world inferences. Local Ollama is $0 but has latency cost; cloud LLMs cost money but are faster. **Knowing this trade-off is how you pick the right model**.

<details open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, measure latency)</b> (copy to <code>practice_3.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

latencies = []
for _ in range(5):
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": "Hi! Please introduce yourself."}],
    )
    latencies.append(time.time() - t0)

avg_latency = sum(latencies) / len(latencies)
out_tok_avg = r.usage.completion_tokens
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b (local)")
print(f"5 latencies (sec): min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens, ~{tps:.1f} tokens/sec")
print(f"\n1000-run cost: $0 (local); projected duration: {avg_latency * 1000 / 60:.1f} minutes")

# === Self-check ===
assert avg_latency > 0, "latency should be > 0"
assert out_tok_avg > 0, "output token count should be > 0"
print(f"\n✅ Exercise 3 passed — local model is $0 but takes ~{avg_latency * 1000 / 60:.0f} min for 1000 runs")
print("💡 Compare Path B Anthropic: 1000 runs is ~10-20 min at $0.25 (haiku)")
```

</details>

<details>
<summary>📋 <b>Starter code — Path B (Anthropic API, compute $ cost)</b> (copy to <code>practice_3_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

# Anthropic public pricing 2026 Q2 (per 1M tokens, USD) — verify at https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-4-6":  {"input": 3.00, "output": 15.00},
    "claude-opus-4-7":    {"input": 5.00, "output": 25.00},  # Opus 4.7 (April 2026) price reduced to 5/25
}

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"
msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "Hi! Please introduce yourself."}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

assert cost_one > 0, "Cloud LLM always has a cost"
print(f"\n✅ Exercise 3 passed (Anthropic) — 1000 runs: haiku ≈ $0.25, sonnet 4.6 ≈ $0.76, opus 4.7 ≈ $1.27")
```

**Expected output**:
```
model: claude-haiku-4-5
single: input=14 output=48 → $0.000254
1000 calls cost across model tiers:
  claude-haiku-4-5       $0.2540
  claude-sonnet-4-6      $0.7620
  claude-opus-4-7        $1.2700
```

**Trade-off**: local Ollama is $0 for 1000 runs but takes ~2 hr; Anthropic haiku is ~10 min for $0.25; sonnet ~10 min for $0.76. **Use cloud only for production; learning / experiments / debug stay local.**

</details>

### Exercise 4: Cross-Provider Comparison
Send the same prompt to Claude, GPT, and Gemini simultaneously, compare their responses. Notice "why does the same input produce different answers" — answer style, length, and judgment all differ. Use the OpenAI, Anthropic, and Google SDKs side-by-side.

→ **Starter template** → [`examples/stage-1/04-cross-provider/`](../examples/stage-1/04-cross-provider/) (parallel calls to all three SDKs + comparison table; missing keys are skipped gracefully; illustrative, **not a chapter-length tutorial**)

### Exercise 5: Error Handling
Trigger error conditions deliberately and write retry logic:
- Wrong API key → see how it raises
- Over-long prompt → what happens when the context window is full
- Network drop → write a retry wrapper with exponential backoff

This is foundational for Stage 3-7's production agent code.

→ **Starter template** → [`examples/stage-1/05-error-handling/`](../examples/stage-1/05-error-handling/) (mock-based tests so you can verify the retry logic without unplugging your ethernet cable; illustrative, **not a chapter-length tutorial**)

### Exercise 6: Local LLM
**No API fees, runs on your machine**: use Ollama to pull a small model (recommend `llama3.2:3b` or `qwen2.5:3b`), call it via OpenAI-compatible API.

```bash
# 1. Install Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # default port 11434
```

<details>
<summary>📋 <b>Starter code</b> (copy to <code>practice_6.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: Ollama is running, qwen2.5:3b is pulled
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't check this — anything works
)

r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "Explain ReAct in 3 sentences."}],
)

text = r.choices[0].message.content
print("Response:", text)

# === Self-check ===
assert len(text) > 10, "response is too short — Ollama may not be running"
print(f"✅ Exercise 6 passed — local Ollama reachable through the OpenAI-compatible API")
print(f"💡 This run cost you $0 (except for electricity)")
```

**Why do this**: once you can run local LLMs, Stage 3-6 experiments aren't bottlenecked on API costs; privacy-sensitive work also stays offline.

</details>

## 🎯 Curated Projects

### [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 42k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: How to call Claude API for every common pattern — chat, tools, citations, multi-modal, prompt caching.

**Best for**: Anyone starting with Claude. The notebooks walk you through every API feature with runnable examples.

**Notes**: Treat this as your reference manual. Don't try to read it cover-to-cover; use as needed when you hit a specific question.

**Run it**:
```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook/skills/classification
pip install -r requirements.txt
jupyter notebook guide.ipynb
```

---

### [Anthropic Courses](https://github.com/anthropics/courses)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 21k+ |
| License | NOASSERTION (no SPDX upstream; check LICENSE before use) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Anthropic's official educational course series — API fundamentals, prompt evaluation, real-world prompting, tool use, Claude with Excel. Each course is a Jupyter notebook you can read and run.

**Best for**: Anyone starting with the Claude API. Complements the Cookbook: Cookbook is a "how do I do X?" lookup, Courses is a "learn it from zero, end-to-end" tutorial.

**Notes**: Start with `anthropic_api_fundamentals` and `prompt_engineering_interactive_tutorial`.

---

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 73k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Same as Anthropic Cookbook but for GPT family. Massive collection of recipes, structured outputs, tool use, embeddings.

**Best for**: Anyone using OpenAI API. The structured outputs and function calling examples are particularly strong.

**Notes**: Larger than Anthropic's cookbook. Use the search heavily — don't browse linearly.

---

### [LangChain Academy](https://academy.langchain.com/)

| Field | Value |
|---|---|
| Format | Free online courses |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: LLM fundamentals, embeddings, RAG, agents — taught through LangChain. Good even if you don't end up using LangChain.

**Best for**: Visual learners who want video walkthroughs.

**Notes**: Some lessons are LangChain-marketing-heavy. Skip those, take the conceptual lessons.

---

### [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 29k+ |
| License | Custom |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build LLM from scratch — Chinese-language equivalent of Karpathy's "Zero to Hero" course. Chapters 1-4 cover LLM principles bottom-up, then practical applications.

**Best for**: Chinese-speaking learners who want to truly understand how LLMs work, not just call APIs. Direct counterpart to Hugging Face's LLM Course but in Chinese.

---

### [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 12k+ |
| License | NOASSERTION |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: A beginner-friendly LLM application development tutorial in Chinese. Covers API basics, knowledge bases, RAG, advanced techniques.

**Best for**: Chinese-speaking beginners who want to *build something* with LLM (vs. just understand them).

---

### [jingyaogong/minimind](https://github.com/jingyaogong/minimind)

| Field | Value |
|---|---|
| Language | 中文 + Python |
| Stars | ★ 48k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Train a 64M-parameter LLM from scratch in 2 hours — the most popular Chinese hands-on "build LLM from scratch" project. Pretrain + SFT + LoRA + DPO + RLHF all in one repo.

**Best for**: After watching Karpathy's video, run this to actually feel each training stage on real data. The pedagogical value is exceptional.

---

### [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook)

| Field | Value |
|---|---|
| Language | 中文 (zh-Hans) |
| Stars | ★ 23k+ |
| Last update | ⚠️ Stale (Jun 2025; ~1 year inactive) |
| License | Custom (CC BY-NC-SA) |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Andrew Ng's prompt engineering / building systems / fine-tuning courses translated and adapted for Chinese learners. Hands-on notebooks.

**Best for**: Chinese-speaking beginners who want a guided LLM curriculum.

**Notes**: zh-Hans content (Datawhale uses simplified Chinese) — but technical content transfers fine. Excellent free Chinese-language entry point.

---

### [Hugging Face — Large Language Model Course](https://huggingface.co/learn/llm-course)

| Field | Value |
|---|---|
| Format | Free online course + notebooks |
| License | Apache 2.0 |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: How LLMs actually work (tokenization, transformers, fine-tuning) with Hugging Face ecosystem.

**Best for**: Readers who want to understand what's happening inside, not just the API surface.

---

### 🖥️ Running LLMs Locally (no API fees)

The four entries below are tools to **run LLMs on your own machine** — useful after Exercise: Local LLM, and the answer for privacy-sensitive work, cost-sensitive experiments, or offline scenarios.

---

### [ollama/ollama](https://github.com/ollama/ollama)

| Field | Value |
|---|---|
| Language | Go |
| Stars | ★ 170k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: The easiest local LLM runner — one `ollama pull qwen2.5:3b` and you have a working model with built-in OpenAI-compatible API (`http://localhost:11434/v1`); existing OpenAI SDK code barely needs to change.

**Best for**: First-time local LLM users. Also useful as fallback in agent dev — main path on Claude, cost-sensitive parts on Ollama.

**Run it**:
```bash
# Download from https://ollama.com
ollama pull qwen2.5:3b   # ~2GB, decent Chinese support
ollama run qwen2.5:3b    # interactive chat
ollama serve             # start API server
```

---

### [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

| Field | Value |
|---|---|
| Language | C++ |
| Stars | ★ 108k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: The inference engine that Ollama and many local LLM tools use under the hood. Understand quantization (GGUF format, what Q4_K_M / Q5_K_S mean), KV cache, CPU/GPU offloading.

**Best for**: People who want to know "why can a 7B model fit in 8GB RAM?" If Ollama is enough for you, skip; come back when you need fine-grained control.

---

### [mudler/LocalAI](https://github.com/mudler/LocalAI)

| Field | Value |
|---|---|
| Language | Go |
| Stars | ★ 46k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: Drop-in OpenAI API replacement — same OpenAI SDK code, point `base_url` at LocalAI, and run LLM, embedding, image generation, TTS, STT all locally.

**Best for**: Teams with compliance / data-privacy requirements that need to replace the entire OpenAI stack with local alternatives. Broader scope than Ollama (not just chat).

---

### [ml-explore/mlx](https://github.com/ml-explore/mlx)

| Field | Value |
|---|---|
| Language | C++ / Python |
| Stars | ★ 25k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐ |

**What it teaches**: Apple's ML framework purpose-built for Apple Silicon (M1/M2/M3/M4 chips). On Macs, often faster than llama.cpp with better memory efficiency.

**Best for**: Mac developers wanting to squeeze maximum performance from Apple Silicon. Linux / Windows users can skip.

**Notes**: Pair it with the `mlx-lm` package for the easiest path.

**Notes**: More academic than cookbooks. Covers training, not just inference.

---

### [karpathy/LLM101n](https://github.com/karpathy/LLM101n)

| Field | Value |
|---|---|
| Status | ⚠️ Archived (last update Aug 2024); outline only — never built out |
| Recommendation | ⭐⭐ |

**What it teaches**: Originally pitched as a build-from-scratch "Storyteller AI LLM" course in Karpathy's signature pedagogical style.

**Best for**: Watch Karpathy's "Let's build GPT from scratch" YouTube video instead — that one is complete and excellent.

**Notes**: The repo is just an outline; the course was never built out. Listed for historical reference only.

---

### [Anthropic — Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started)

| Field | Value |
|---|---|
| Format | Documentation |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: The Claude API official documentation.

**Best for**: Direct reference. Bookmark this.

---

### [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)

| Field | Value |
|---|---|
| Format | YouTube video (2 hours) |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build a transformer-based GPT from scratch in PyTorch. Foundational understanding of how LLMs work internally.

**Best for**: Anyone who wants to understand WHY LLMs behave the way they do, not just HOW to call them.

**Notes**: 2 hours of dense content. Pause and code along — don't passively watch.

---

### [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)

| Field | Value |
|---|---|
| Language | Python / Jupyter |
| Stars | ★ 91k+ |
| License | Apache-2.0 |
| Recommendation | ⭐⭐⭐⭐⭐ |

**What it teaches**: Build a GPT-style LLM end-to-end in PyTorch — tokenizer → attention → pretraining → finetuning, paired with Sebastian Raschka's book. Complete notebooks + code, chapter-aligned with the book.

**Best for**: Anyone who wants to truly understand what tokens, attention, and weights are. Complementary to Karpathy's video — that's a 2-hour fly-by, this is the slow read-the-book version.

**Notes**: Companion code to the book (Apache-2.0); free to fork and modify.

---

## ✅ Self-Check Before Stage 2

Can you:
- [ ] Make a Claude API call from Python in 5 lines
- [ ] Explain why "你好" might use 2 tokens but "Hello" uses 1
- [ ] Quote roughly the per-token price for Claude Sonnet vs Opus
- [ ] Name one strength of Claude vs GPT vs Gemini vs Llama

If yes → proceed to [Stage 2 — Prompt Engineering](02-prompt-engineering.en.md).

If no → re-read the Anthropic Quickstart + run all 3 hello-X projects above.

---

> ✅ **Done with Stage 1?** Next, [**Stage 2 — Prompt Engineering**](02-prompt-engineering.en.md) takes 5-12 hours to walk you through writing reusable structured prompts, using few-shot and chain-of-thought for reasoning tasks, and learning to quantify prompt improvement with evals. **Keep going →**
