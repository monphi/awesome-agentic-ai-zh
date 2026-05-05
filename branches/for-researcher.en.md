# For Researchers — Specialized Branch

> [← Back to main path README](../README.en.md) · Branching from end of Stage 7. Apply agentic AI to research workflows.

## Use Cases

- Literature triage and matrix building
- Paper memory extraction (claims, figures, citations)
- Multi-agent paper review (peer review patterns)
- NotebookLM brief verification
- Reference management automation

## Curated Projects

### Research Workflow Marketplaces

#### [flonat/claude-research](https://github.com/flonat/claude-research) ⭐⭐⭐

Claude Code infrastructure for PhD researchers — skills, agents, hooks, rules for academic workflows. Strong LaTeX/bibliography focus.

---

### Literature RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 8k+ |
| License | Apache-2.0 |

**What it teaches**: High-accuracy RAG over PDF documents, with grounded sentence-level citations on every answer.

**Best for**: Researchers writing literature reviews who need "every answer must be traceable to its source." More rigorous than generic RAG.

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 27k+ |
| License | Apache-2.0 |

**What it teaches**: Autonomous deep-research agent — planner + multi-source crawl + report synthesis. Give it a research topic, get a markdown / PDF brief out.

**Best for**: Researchers who need to quickly scope new topics and produce research briefs.

---

### Outline & Writing

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 28k+ |
| License | MIT |

**What it teaches**: Multi-perspective outline-then-write pipeline — agent first generates an outline from multiple angles, then expands into Wikipedia-style articles. From Stanford OVAL.

**Best for**: Learning **outline-driven writing**. Great for producing topic briefs from scratch; the closest open-source analog to NotebookLM's structured report flow.

**Notes**: Maintenance pace has slowed (close to or beyond 6 months without a push); double-check the latest commit date before relying on it.

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐ (Chinese readers)

| Field | Value |
|---|---|
| Language | Chinese + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION (custom non-commercial) |

**What it teaches**: Full arXiv workflow for Chinese researchers — paper summary + translation + polishing + review-response generation. Maintained by a Chinese team; defaults are friendly to Chinese-language workflows.

**Best for**: Chinese graduate students looking for a Chinese-friendly entry-level paper workflow tool.

**Notes**: License is custom non-commercial — read the original terms before any use; common practice is research / personal use, but you should verify the terms yourself.

---

### Citation Manager Integrations

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**What it teaches**: A Zotero LLM plugin — chat with your library, summarize selections, generate inline notes.

**Best for**: Heavy Zotero users who want AI inside their reading workflow without switching tools.

**Notes**: AGPL-3.0 license (copyleft) — derivative products that ship modifications must follow the terms.

---

### Multi-Agent for Research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 11k+ |
| License | MIT |

**What it teaches**: Open-source Deep Research — supports both single-agent and supervisor + multi-researcher architectures (the multi-agent path currently lives in `src/legacy/`), parallel search, citation-grounded report synthesis. A solid reference for "LLM agent that auto-produces a cited brief."

**Best for**: Researchers building "agent auto-generates a cited brief" workflows. A solid open-source pick when you want a maintained reference implementation.

**Notes**: Depends on LangGraph + search tools (API key required).

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 6k+ |
| License | The AI Scientist Source Code License (source-available, non-commercial + manuscript-disclosure clause) |

**What it teaches**: End-to-end multi-agent science loop: ideate → code → experiment → write → peer-review. Sakana AI's research implementation of "AI writes a full ML paper."

**Best for**: Researchers who want to see "what does a swarm of agents running a full research lifecycle look like." Architecture reference, not a production tool.

**Notes**: Outputs are demo-level (not field-ready), ML/CS-domain bias. License is a custom source-available term (with a manuscript-disclosure clause) — read the LICENSE file before use.

---

> Still missing: actively-maintained peer-review automation, conference-review pipelines. If you've built or know of one, please open a PR.

## Required Reading

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## Workflows To Master

- **Literature triage**: use `paper-qa` for grounded Q&A over your PDF library, then `gpt-researcher` to auto-generate briefs, output to Obsidian / Notion
- **Outline-driven writing**: use `storm` to auto-generate multi-perspective outlines from a topic, then expand to formal sections by hand
- **Chinese paper workflow**: use `ChatPaper` for summary / translation / polishing, then human review
- **Zotero in-app AI**: install `zotero-gpt` and ask questions or summarize selections directly in your reading flow
