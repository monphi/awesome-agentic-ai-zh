# Stage 6 — Memory · RAG · Context Engineering

> [繁體中文](./06-memory-rag.md) | [简体中文](./06-memory-rag.zh-Hans.md) | **English**

⏱️ **Estimated time**: 2 weeks (approx. 10 hours)

> 💡 This stage is dense with terminology (**RAG / vector database / embedding / chunking / hybrid search / reranking...**). If you're unfamiliar, first check [`resources/glossary.md` §3](../resources/glossary.md#3-memory--retrieval--rag).

> 📋 **Chapter Outline** (progressive flow, shallow → deep):
>
> 1. **Positioning** — What Context Engineering is + 2 concept comparison tables
> 2. **Goals / Entry** — Learning Objectives → Entry Conditions → Required Reading → Unit Guide
> 3. **RAG Main Track** — 🌐 Basic RAG Pipeline → 🚀 Advanced RAG Techniques (GraphRAG / Contextual Retrieval / Hybrid Search / Query Trans / Self-improving / RAPTOR + **2024-2026 Overview**)
> 4. **Bridge** — 🌉 From RAG to Memory (why RAG isn't enough)
> 5. **Memory Main Track** — 🧠 Short/long-term + 3 patterns + CoALA + Generative Agents + **2024-2026 Overview**
> 6. **Technical Deep Dive** — 🧩 Chunking Details
> 7. **Advanced Reflection / Reasoning** — 🪞 Reflexion (complete) → 🤔 Path 1 prompt-based + **Path 2 trained-in** (o1 / R1 / V4-Pro / Opus 4.7 / GPT-5.5)
> 8. **Practice / Recs / Self-check** — Hands-on Exercises → Recommended Tools → Featured Projects → Self-Check
>
> 🔑 **Key Terms**: See [`resources/glossary.md` §3](../resources/glossary.md#3-memory--retrieval--rag) (memory / RAG / embedding / chunking / reranking)

## 🎯 What is Context Engineering (Positioning First)

**Context Engineering is the discipline of dynamically assembling prompts across multiple LLM calls.** Stage 2 taught you "how to write a **single** prompt," and this stage teaches you "how to manage context **across multiple** calls." When you need to dynamically build a system prompt, pull from memory, insert retrieved chunks, and attach tool definitions, you've entered the realm of context engineering.

**Discipline Lineage** (You are currently at level 2):

| Level | Discipline | What it Solves | Which Stage |
|---|---|---|---|
| 1 | **Prompt Engineering** | How to ask accurately in a single LLM call | [Stage 2](02-prompt-engineering.md) |
| **2** | **Context Engineering**<br>(**This stage**) | **How to dynamically assemble prompts across multiple calls** | **This stage** |
| 3 | **Harness Engineering**¹ | How to package multiple LLM calls into a production runtime | [Stage 7 §Harness Engineering](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程學--本-stage-核心概念) |

> ¹ "Harness Engineering" is not yet an industry-standardized term. This curriculum adopts the usage popularized by Anthropic / Hamel Husain / Simon Willison in 2024–2026 writing (engineering the agent loop / control flow / runtime). Others call the same thing "Agent Runtime," "Agent Loop Engineering," or "Inference Orchestration."

**3 Problem Domains of Context Engineering** (This stage focuses on the first two):

1. **Retrieval** — How to fetch relevant snippets from external knowledge bases (RAG / vector search / GraphRAG / hybrid search)
2. **Memory Management** — How to layer, store, and forget short-term / long-term / episodic / semantic memory
3. **Context Window Budgeting** — How many tokens to allocate for the prompt, history, and retrieval; connects to Stage 7 §Harness.

### 4 Commonly Confused Concepts — A Clear Comparison Table

| Term | What it is (Abstract / Concrete) | Example Tools |
|---|---|---|
| **Memory** | The **ability** of an agent to remember things across conversations/sessions (abstract concept) | LangChain `ConversationBufferMemory` / mem0 / Letta |
| **Embedding** | Converting text into an N-dimensional **vector** to make similarity computable (data transformation) | `sentence-transformers` producing a 768-dim vector / OpenAI `text-embedding-ada-002` |
| **Vector DB** | The **storage layer** for storing and querying embeddings (infrastructure) | Chroma / Qdrant / Weaviate / pgvector |
| **RAG** | The **pattern** of "retrieve relevant snippets → insert into prompt → generate" (architectural pattern) | LlamaIndex / LangChain RAG chain |

→ **Core Distinction**: Memory is an **ability**, Embedding is a **data transformation**, Vector DB is **storage**, and RAG is an **architectural pattern**. These four are often used interchangeably but are concepts at four different layers.

### RAG vs. Long Context vs. Fine-tuning — When to Use What

There are three main ways to make an LLM aware of your private/domain-specific data. **This stage teaches RAG**, but you need to know when not to use it:

| Option | Best for | Not suitable for | Cost |
|---|---|---|---|
| **RAG**<br>(External retrieval) | Large / dynamic / private knowledge bases, requires citations | Tasks needing full-text comprehension, multi-hop reasoning across documents | Latency of one extra vector search per query |
| **Long Context**<br>(Directly in prompt) | Medium-sized docs (< 200k tokens), one-off queries, requires cross-doc reasoning | Large/frequently changing knowledge bases, need for citations | Burns a lot of input tokens per query (even with prompt caching) |
| **Fine-tuning**<br>(Modifying model weights) | Unifying style/format, domain-specific language (medical, legal, code) | Knowledge that changes, need for citations, don't want to train a model | Training cost + maintenance cost + model lock-in |

→ **How to choose**: Start with RAG (lowest cost, easiest to change) → if RAG fails, consider Long Context → if both fail, consider Fine-tuning. **Proceed to Stage 7 to learn about fine-tuning and deployment.**

## 📌 Learning Objectives

- Build a basic RAG pipeline (chunk → embed → store → retrieve → generate)
- Identify where RAG should and should not be used
- Differentiate between short-term, long-term, episodic, and semantic memory
- Understand vector embeddings and similarity search
- Know when to add advanced RAG techniques (GraphRAG / Contextual Retrieval / Hybrid Search) and when not to

## 🚪 Entry Conditions

You should already:
- Have completed Stage 3 (know how to write tool use, call LLM APIs, and understand the ReAct loop)
- Be able to run `pip install` to install Python SDKs (exercises will use `chromadb`, `sentence-transformers`, etc.)
- Be proficient with basic Python structures like lists, dicts, and generators

If not, please return to [Stage 3](03-tool-use-and-hello-agent.md) or [Stage 0 §Environment Setup](00-foundations.md#何時可以跳過這個階段).

## 📚 Required Reading

1. [**LlamaIndex — RAG concepts**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — The clearest introduction.
2. [**LangChain — RAG tutorial**](https://python.langchain.com/docs/tutorials/rag/) — Hands-on practice.
3. [**Pinecone — Learning Center**](https://www.pinecone.io/learn/) — Vector DB fundamentals.
4. [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) — Anthropic's RAG approach with prompt caching.
5. [**LangChain — Text splitters**](https://docs.langchain.com/oss/python/integrations/splitters/index) — Introduction to chunking strategies.

> 🙏 **Special Recommendation for the Memory section: [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)**: This stage covers the concepts and basic implementation of memory. For a **chapter-length deep dive**, please see the corresponding chapters in hello-agents. It provides the most complete explanation of short-term/long-term memory differences, dynamic context engineering, session persistence, and forgetting strategies. This stage is a roadmap; that is the in-depth textbook.

## 🧭 Unit Guide (Progressive Flow)

This chapter follows a **RAG-first, Memory-second** sequence. RAG is the most fundamental and commonly used tool in context engineering, while Memory is the agent's ability to persist knowledge across conversations/sessions. We'll first get a RAG pipeline running, then move to Memory design, and finally circle back to the details of Chunking.

**Recommended Reading Order**:

1. **🌐 Basic RAG Pipeline** (next section) — Build a mental model
2. **🚀 Advanced RAG Techniques** — Production upgrades like GraphRAG / Contextual Retrieval / Hybrid Search
3. **🌉 From RAG to Memory** — Why RAG isn't enough and what Memory adds
4. **🧠 Memory Design** — Short-term vs. long-term, 3 patterns, CoALA framework
5. **🧩 Chunking Details** — Technical deep dive used by both RAG and Memory

As you read this chapter, consider: What application scenarios are not suitable for RAG? In which scenarios is basic RAG insufficient? This will lead to the advanced techniques discussed later, such as GraphRAG, Self-RAG, and RAPTOR.

## 🌐 Basic RAG Pipeline

**RAG (Retrieval-Augmented Generation)** is the pattern of "retrieve relevant snippets → insert into prompt → generate." Think of it as building a library for your agent. You need to organize and shelve the books properly so that when you need to look up information, you can do it quickly and accurately.

**The most basic RAG is split into two pipelines**:

- **Data Preprocessing (ingest once)**: ingest → chunk → embed → store (index). This step builds a searchable knowledge base.
- **Retrieval & Generation (per query)**: retrieve → generate. This step finds relevant content when a user asks a question and then passes it to the LLM for a response.

![RAG Pipeline Overview](../resources/diagrams/rag-pipeline-overview.jpg)

RAG Fusion, query rewrite, and other techniques in the diagram are advanced retrieval skills. **When first learning RAG, focus on understanding the main flow.**

**5-Step Breakdown**:

| Step | What it does | Which pipeline | Technical details in |
|---|---|---|---|
| **1. Ingest** | Load data (PDF / web / DB / conversation logs) | Preprocessing | LlamaIndex / LangChain loaders |
| **2. Chunk** | Split documents into small pieces (500-2000 tokens/chunk) | Preprocessing | See later §🧩 Chunking Details (read the RAG / Memory main tracks first; technical deep dive is parked there) |
| **3. Embed** | Convert each chunk into an N-dimensional vector | Preprocessing | `sentence-transformers` / OpenAI `text-embedding-ada-002` |
| **4. Store** | Store vectors + metadata in a vector DB | Preprocessing | Chroma / Qdrant / pgvector |
| **5. Retrieve + Generate** | Embed the query → top-k semantic search → assemble into prompt → LLM generates | Per query | General LLM API |

This is just the minimal skeleton. **The 3 most common pitfalls**:

- **Chunk size too large/small**: Too large, and retrieved chunks contain only one relevant sentence amidst noise; too small, and you lose context (see §Chunking Details).
- **Wrong embedding model**: Using an English model for Chinese documents will tank retrieval accuracy.
- **Top-k set too high/low**: Too low, you miss relevant chunks; too high, you get more noise and burn tokens.

After mastering the basic skeleton, complete Exercises 1-4 (§Hands-on Exercises) on embeddings, vector DBs, chunking, and the full pipeline to get a feel for it before moving on to the next section, §Advanced RAG Techniques.

## 🚀 Advanced RAG Techniques (Read after completing Basic RAG)

The following six subsections cover the most common levers for production RAG in 2024-2026, grouped by where they fit in the pipeline:
- **After Retrieve** — GraphRAG / Contextual Retrieval / Hybrid Search & Reranking
- **Before Retrieve** (query rewriting) — Query Transformations
- **During Retrieve** (control flow) — Self-improving RAG
- **Index Structure** — RAPTOR
- **2024-2026 Overview** — 17 other techniques worth knowing

**First, get a baseline version with Basic RAG, then come back here.** Otherwise, you'll be tuning parameters without a baseline, never knowing which change brought improvement.

| Technique | Problem Solved | Added to which pipeline layer | Cost |
|---|---|---|---|
| **GraphRAG** | Vanilla RAG can't do multi-hop / cross-document entity-relation reasoning | Before retrieve (build graph) + during retrieve (graph traversal) | High (requires building a KG, needs LLM to extract entities) |
| **Contextual Retrieval** | Chunks lose original document context, leading to incorrect retrieval | After chunk / before embed (add contextual header) | Medium (one-time, 90% cheaper with prompt caching) |
| **Hybrid Search & Reranking** | Pure vector search misses literal matches, top-k is noisy | During retrieve (parallel BM25 search) + after retrieve (cross-encoder rerank) | Low (mature tools are plug-and-play) |

### 🔗 GraphRAG — Knowledge Graphs + RAG

**Mental model**: Vanilla RAG splits documents into chunks and uses embedding similarity to fetch them. But **it doesn't know which entities are the same thing or the relationships between them.** GraphRAG uses an LLM during ingest to extract **(entity, relation, entity)** triplets and build a knowledge graph. During retrieval, in addition to vector comparison, it performs graph traversal to find "related entities of related entities."

**When to use**:
- The task requires **multi-hop reasoning** (A → B → C to answer).
- Multiple documents reference each other's entities (company financial reports, paper citations, investigation reports, legal cases).
- Questions are of the form "What Y did X influence, and what Z is Y connected to?" — vanilla RAG usually only fetches the part about X.

**When not to use**:
- Documents have no entity-relation links (simple FAQs, product manuals are independent).
- Small knowledge base (< 1k chunks) — vanilla RAG is sufficient.
- Tight budget — the token cost of building a KG can be 10-50x that of normal RAG.

**Representative frameworks**:
- [**Microsoft GraphRAG**](https://github.com/microsoft/graphrag) ⭐ — Original reference implementation, Apache-2.0, includes community detection.
- [**HKUDS/LightRAG**](https://github.com/HKUDS/LightRAG) — Lightweight version, EMNLP 2025, KG + vector hybrid, lower cost than Microsoft's version.
- [**gusye1234/nano-graphrag**](https://github.com/gusye1234/nano-graphrag) — Minimal implementation in < 1000 lines, good for understanding the principles first.

**Paper**: [**From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Edge et al. 2024)**](https://arxiv.org/abs/2404.16130) — The original paper for Microsoft GraphRAG, explaining why community summarization can solve global queries.

### 🪶 Contextual Retrieval — Anthropic's Prompt-Caching Solution

**Mental model**: Vanilla chunking loses the original document's context. A chunk like "Q3 revenue grew 15%" doesn't tell you **which company** or **which year's** Q3. Anthropic proposed in 2024: **During ingest, use an LLM to write a 50-100 token contextual header for each chunk** ("This chunk is from ACME Corp 2024 Q3 earnings, discussing the cloud segment...") and prepend it before embedding. Combined with **prompt caching**, this means the "full document + each chunk" prompt is only billed once, with all subsequent chunks sharing the cache.

**When to use**:
- The literal meaning of chunks is distant from the document's main theme (financial reports, research papers, long narrative documents).
- You're willing to pay a one-time ingest cost for higher retrieval accuracy.
- You're already using Claude or want to use prompt caching (other models can run it, just without the cache discount).

**When not to use**:
- Chunks are self-contained (FAQs, product pages, definition entries).
- The knowledge base changes frequently (requires re-ingesting every time).
- Extremely tight budget — even with the cache discount, ingest cost is still higher than vanilla.

**Why it saves 90% cost**: Anthropic reports that prompt caching treats the full document as a cached prefix, and each chunk is only sent as a diff. Compared to sending the full document with each chunk, the cost is reduced to about 1/10. But **this only saves on ingest, not the retrieval stage**.

**Representative implementations**:
- [**Anthropic — Contextual Retrieval blog**](https://www.anthropic.com/news/contextual-retrieval) ⭐ — Official explanation + benchmark (failed retrieval rate dropped from 5.7% to 1.9%).
- [**Anthropic cookbook**](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) — End-to-end Jupyter notebook, including prompt templates.

**Combined technique**: The same Anthropic blog also recommends stacking **Contextual BM25** (feeding contextual chunks to both vector + BM25) + **reranking** — which leads us directly to the next section, §Hybrid Search & Reranking.

### 🎯 Hybrid Search & Reranking — Two Polishes for Production RAG

**Mental model**:
- **Hybrid Search** = vector similarity (semantic similarity) + BM25 / keyword (literal similarity) searched in parallel, with scores fused using something like [RRF (Reciprocal Rank Fusion)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf). This solves the dual blind spots of pure vector search: "query and chunk are synonymous but use different words" and "names/IDs/rare words have weak semantic embeddings."
- **Reranking** = First stage retrieves **top-50** (recall-first, loose retrieval) → then a **cross-encoder reranker** re-scores and sorts to get a **top-5** (precision-first, precise filtering). Cross-encoders (query + chunk go into the model together) are much more accurate than bi-encoders (query/chunk embedded separately) but are too slow, so they are only used in the second stage.

**Why are they "must-add polishes"**: Production RAG evaluations are almost unanimous — adding hybrid search + a reranker typically boosts recall@5 from around 70% to 85-90%, with low marginal cost and mature implementations. **These are the two modifications with the best cost/benefit ratio.**

**When to use**:
- Production RAG (not a demo/exercise).
- Queries contain names, product IDs, technical terms, or rare words (easy for pure vector search to miss).
- Budget allows for an extra 100-300ms of latency per query.

**When you can wait**:
- During the practice/MVP phase (get vanilla RAG working first).
- Extremely tight budget or latency requirements (a reranker is an extra model call).

**Representative tools**:
- **Hybrid search**: [Weaviate](https://github.com/weaviate/weaviate) (built-in BM25 + vector + RRF) / [Qdrant](https://github.com/qdrant/qdrant) (supports sparse + dense vectors) / pgvector + Postgres FTS.
- **Reranker**: [Cohere Rerank API](https://docs.cohere.com/docs/rerank-overview) (commercial, most common) / [BGE Reranker](https://huggingface.co/BAAI/bge-reranker-large) (open-source, HuggingFace, performs well in Chinese) / [Jina Reranker](https://jina.ai/reranker).
- **Built-in framework support**: LlamaIndex's `SentenceTransformerRerank` / LangChain's `ContextualCompressionRetriever`.

**Papers / Getting Started**:
- [**Pinecone — Rerankers and Two-Stage Retrieval**](https://www.pinecone.io/learn/series/rag/rerankers/) — Clearest explanation of the reranker mental model.
- [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) (listed above) — Demonstrates hybrid + reranker together, with benchmarks.

### 🔄 Query Transformations — HyDE / Multi-Query / RAG Fusion

**Mental model**: Vanilla RAG embeds the user query directly for search. But the **wording/style/abstraction level** of the query often differs greatly from the document (user asks "What to do for a stomach ache?", document says "Differential diagnosis of upper abdominal pain"). Query transformations rewrite the query **before** retrieval to make it closer to the document's format.

**3 representative techniques**:

| Technique | How it rewrites | When to use |
|---|---|---|
| **HyDE** (Hypothetical Document Embeddings) | LLM generates a "hypothetical answer" to the query, uses the answer's embedding for search | The wording/style gap between query and chunk is large |
| **Multi-Query** | LLM rewrites the query into N variants, retrieves for each, then unions and deduplicates | The query is too short, vague, or ambiguous |
| **RAG Fusion** | Multi-Query + RRF to fuse the N retrieval results | Same as above, but for more stable ranking |

**When not to use**: When the query is already long and structured (RAG over code, user pastes an error stack trace) — rewriting would introduce noise.

**Papers / Implementations**:
- [**HyDE (Gao et al. 2022)**](https://arxiv.org/abs/2212.10496) — Original paper.
- [**RAG Fusion (Raudaschl 2023)**](https://github.com/Raudaschl/rag-fusion) — Reference implementation for Multi-Query + RRF.
- LangChain has a built-in `MultiQueryRetriever` / LlamaIndex has `HyDEQueryTransform`.

### 🔁 Self-improving RAG — Self-RAG / CRAG / Adaptive RAG (2024's main theme)

**Mental model**: All the RAG techniques above assume a fixed "query comes in → retrieve → generate" pipeline. Self-improving RAG turns this pipeline into an **agentic loop with decision-making capabilities**. The LLM itself decides whether to retrieve, judges the quality of the retrieval, and if it's not good enough, searches again or modifies the query. **This is the main focus of RAG research in 2024.**

| Technique | How it self-corrects | Paper |
|---|---|---|
| **Self-RAG** | Train LLM to output a `[Retrieve]` token to decide whether to search; after retrieval, outputs `[IsRel]/[IsSup]/[IsUse]` to score each snippet | [Asai et al. ICLR 2024](https://arxiv.org/abs/2310.11511) |
| **CRAG** (Corrective RAG) | A retrieval evaluator scores results; high confidence is used directly, low confidence falls back to web search, medium confidence triggers query rewriting | [Yan et al. 2024](https://arxiv.org/abs/2401.15884) |
| **Adaptive RAG** | A classifier first determines query complexity, then routes to one of three strategies: "no retrieval," "single-step," or "multi-step" | [Jeong et al. NAACL 2024](https://arxiv.org/abs/2403.14403) |

**Why this is the 2024 main theme**: A fixed pipeline is suboptimal for both simple queries ("What is the capital of Tokyo?" - no retrieval needed) and complex queries (multi-hop, cross-doc). Letting the LLM route itself solves both extremes.

**When to use**: Production RAG where query types are diverse (from factual questions to reasoning problems), and you're willing to pay a 1.5-3x latency penalty for accuracy.
**When not to use**: Query types are uniform, or budget/latency is extremely tight.

**Implementations**: LangGraph has official cookbooks for [Self-RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/), [CRAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/), and [Adaptive RAG](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/) that can be used directly.

### 🌳 RAPTOR — Recursive Abstractive Processing for Tree-Organized Retrieval (ICLR 2024)

**Mental model**: Vanilla chunking creates flat chunks of a document. But **the main thesis of a book isn't in any single chunk.** RAPTOR recursively clusters and summarizes chunks to build a **multi-level tree**: the bottom level contains original chunks, the middle level contains summaries of related chunks, and the top level is a summary of the entire document. Retrieval can search the whole tree or target a specific level of abstraction.

**Why it's useful**:
- **Abstract queries** can be answered ("What are the main conclusions of this paper?" - this sentence doesn't exist in any original chunk but is in the top-level summary).
- **Detailed queries** are also answerable (preserved in the bottom-level chunks).
- Different from GraphRAG — RAPTOR is a **tree** (hierarchical summarization), while GraphRAG is a **graph** (entity-relation).

**When to use**: Long documents (books, papers, reports) that require queries at different levels of abstraction; narrative, coherent knowledge bases.
**When not to use**: Chunks are independent (FAQs); the knowledge base changes frequently (rebuilding the tree is expensive).

**Paper / Implementation**:
- [**RAPTOR (Sarthi et al. ICLR 2024)**](https://arxiv.org/abs/2401.18059) ⭐ — Original paper.
- [**parthsarthi03/raptor**](https://github.com/parthsarthi03/raptor) — Official reference implementation.
- LlamaIndex has a built-in `RAPTOR pack`.

### 📊 What Else — A Quick Overview of Advanced RAG Techniques

Here are other common techniques in production/research, categorized by use case. **Each line = name + one-sentence description + paper**. To dive deeper, pick one that interests you and go to the original paper. ⭐ **Year** marks the latest works from 2025-2026.

| Technique | One-sentence description | Year / Paper |
|---|---|---|
| **Sentence-Window Retrieval** | Embed a sentence, retrieve it, then return a window of ±N sentences around it | Built into LlamaIndex |
| **Parent-Child / Small-to-Big** | Embed small chunks, return the parent chunk | LangChain `ParentDocumentRetriever` |
| **Multi-Vector Retrieval** | One chunk, multiple embeddings (summary / original text / hypothetical questions) | LangChain `MultiVectorRetriever` |
| **ColBERT / Post-Interaction Retrieval** | Token-level comparison instead of pooled embeddings | [Khattab & Zaharia 2020](https://arxiv.org/abs/2004.12832), [RAGatouille](https://github.com/AnswerDotAI/RAGatouille) |
| **LongRAG** | Large chunks (4k) + a long-context reader to reduce retrieval calls | [Jiang et al. 2024](https://arxiv.org/abs/2406.15319) |
| **HippoRAG 2** (formal title: *From RAG to Memory: Non-Parametric Continual Learning for LLMs*) | Hippocampus-inspired, KG + PageRank, for cross-document multi-hop associations | [Gutiérrez et al. ICML 2025](https://arxiv.org/abs/2502.14802) ⭐ **2025** |
| **MemoRAG** | A memory model compresses the KB into latent memory, retrieved by cues | [Qian et al. 2024](https://arxiv.org/abs/2409.05591) |
| **KAG** (Knowledge-Augmented Generation) | Strict schema KG + logical reasoning, for finance/medical/legal scenarios | [Liang et al. 2024 (Ant Group)](https://arxiv.org/abs/2409.13731) |
| **ColPali** | Directly embed PDF page images, bypassing OCR | [Faysse et al. 2024](https://arxiv.org/abs/2407.01449) |
| **MiA-RAG** (Mindscape-Aware) | First builds a high-level summary mindscape of documents to guide retrieval and answering | [arXiv:2512.17220](https://arxiv.org/abs/2512.17220), [Turing Post 12 types](https://www.turingpost.com/p/12ragtypes) ⭐ **2025-12** |
| **QuCo-RAG** (Quality-Controlled) | Uses pretraining statistics to decide whether to retrieve, triggering on rare entities to reduce hallucination | [arXiv:2512.19134](https://arxiv.org/abs/2512.19134) ⭐ **2025-12** |
| **MegaRAG** | Multimodal KG, extracts entities + relations + visuals from long docs to build a hierarchical graph | [arXiv:2512.20626](https://arxiv.org/abs/2512.20626) ⭐ **2025-12** |
| **TV-RAG** | Training-free time-aware RAG, aligns long videos with subtitles and visuals | [arXiv:2512.23483](https://arxiv.org/abs/2512.23483) ⭐ **2025-12** |
| **A-RAG** (Agentic RAG) | Hierarchical retrieval interfaces; keyword + semantic + chunk read as three tools | [Ayanami0730/arag](https://github.com/Ayanami0730/arag), [arXiv:2602.03442](https://arxiv.org/abs/2602.03442) ⭐ **2026** |
| **SoK: Agentic RAG** (survey) | A 2026 systematic taxonomy: cardinality / control / autonomy / knowledge repr | [arXiv:2603.07379](https://arxiv.org/abs/2603.07379) ⭐ **2026** |
| **RAGPart / RAGMask** | Lightweight defenses against RAG corpus poisoning attacks | [arXiv:2512.24268](https://arxiv.org/abs/2512.24268) ⭐ **2025-12** |
| **Agentic RAG** (general concept) | Retrieval as a tool; the agent decides how many times/how to search | LlamaIndex / LangGraph, main topic of [Stage 7](07-multi-agent-production.md) |
| **DSPy + RAG** | No prompt writing; uses programs + signatures, auto-optimizes | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) |

> 💡 **2025-2026 Trend Watch**:
> - **Fusion of memory, KG, and retrieval** (HippoRAG 2 / A-MEM / KAG / MegaRAG) — Moving from flat vector stores to structured, evolvable architectures.
> - **Multimodal RAG** (ColPali / TV-RAG / MegaRAG) — From text to native retrieval of images, videos, and tables.
> - **Agentic RAG becomes mainstream** (A-RAG / Self-RAG / CRAG) — Retrieval transforms from a fixed pipeline into a tool within an agent loop.
> - **RAG security emerges** (RAGPart / RAGMask) — Corpus poisoning and prompt injection become production concerns.
> - **No more manual prompts** (DSPy / automated optimization) — Systems automatically search for the optimal prompt + retriever combination.

## 🌉 From RAG to Memory — Why RAG Isn't Enough

You can now run a basic RAG pipeline and know a few production levers. But look back at the 3 problem domains in §Context Engineering — you've only tackled **Retrieval**; **Memory management** is still untouched. Why are these two separated?

RAG solves the problem of retrieving relevant snippets from an **external knowledge base**. But an agent also needs to **remember its own experiences** across conversations and sessions. These are not the same problem:

| Dimension | RAG | Memory |
|---|---|---|
| Content Source | **External** (PDFs / documents / web / DB) | **The agent's own conversations/experiences** |
| Write Time | Ingested once, retrieved many times | Written every turn, every task |
| Content Nature | Mostly static facts, document knowledge | Mostly dynamic: user preferences, past interactions, lessons learned |
| Can it replace RAG? | — | No — you wouldn't treat every PDF as "memory" |
| Can RAG replace it? | — | No — RAG doesn't "remember what the user said last time" |

**3 scenarios where RAG falls short** (and Memory steps in):

1. **Remembering user preferences/persona across sessions** — A user tells the agent last week, "I'm vegan." This week, the agent remembers not to recommend meat dishes. A RAG knowledge base doesn't update automatically like this.
2. **Accumulating an agent's past successes and failures** (Reflexion's domain) — An agent fails a task, reflects on "why it failed," stores that reflection, and retrieves it in the prompt for a similar task next time to avoid repeating the mistake. A RAG knowledge base doesn't "remember its own failures."
3. **Maintaining intermediate state in a long-horizon task** — An agent running a 100-step task needs to retain working memory without loss. RAG is not suited for this kind of "short-term, structured, high-frequency write" state.

→ **Conclusion**: RAG and Memory are **complementary**, not substitutes. A production agent typically **needs both**: RAG for external knowledge, Memory to record its own and the user's interactions. The next section, §Memory Design, teaches you how to choose the right memory pattern.

## 🧠 What is Memory & How to Design It

### Short-term vs. Long-term Memory — Establishing a Mental Model

| Aspect | Short-term Memory | Long-term Memory |
|---|---|---|
| Also Known As | Working Memory | Persistent Memory |
| Source | Current conversation content | Information saved across sessions or for long periods |
| Duration | Short, usually limited to the current session | Long, can persist across sessions |
| Technical Basis | Context window / prompt | Memory store / user files / vector database |
| Best for Remembering | Task details, what was just said | Stable preferences, long-term goals, background info |
| Limited by Context Length? | Yes, because there's a limit to how much a model can see at once | Not really, because it can be stored externally and a small part retrieved when needed |
| Real-life Example | A phone verification code you just received, the last sentence in a conversation | Deeply learned knowledge, a library, a knowledge base, books you've read |

Here, a "session" can be understood as a continuous interaction, such as a single chat, a single task, or a single agent execution run.

### 3 Design Patterns (When to Use What) ⭐ Track B Must-Read

**Not all agents need an external memory store. Choosing the wrong memory architecture can cost ten times the tokens for the same effect.**

This is the mental model to establish before the exercises. Exercises 1-5 below use "pattern 3 vector store," but in production, you might not need something that complex.

| Pattern | Best for | How it works | Cost |
|---|---|---|---|
| **1. Naive Buffer**<br>(Stuff everything in context) | Short conversations, ≤ 10 turns, agent doesn't need to remember across sessions | Send the entire history in the prompt every time | Grows linearly, burns tokens fast |
| **2. Summary + Recent**<br>(Summarize old, keep recent N turns) | Medium-long conversations, ~50 turns, want to compress without losing too much | Every N turns, have an LLM summarize the old history; prompt = `summary + last N turns` | Medium, includes LLM summarization cost |
| **3. Vector Store + Retrieval**<br>(External store + semantic search each turn) | Cross-session, knowledge base scenarios, agent needs to "recall" distant events | Embed past messages → store in vector DB → query for relevant snippets each turn to add to prompt | High (vector computation + storage), but token usage is stable |

**How to choose**:

- Conversational chatbot with no cross-session memory → **Pattern 1**
- Agent with long conversations, needs to remember today's chat → **Pattern 2**
- Agent + cross-session + knowledge base (the scenario for this stage's exercises) → **Pattern 3**
- Large-scale production agent → Usually a **hybrid**: Pattern 1/2 for recent, Pattern 3 for long-term

**📚 Deep Dive Resources**:
- [**mem0ai/mem0**](https://github.com/mem0ai/mem0) ⭐ — A production memory layer that automatically routes between recent, long-term, and vector memory.
- [**Letta (formerly MemGPT)**](https://github.com/letta-ai/letta) — OS-style paging memory (treats the context window as RAM, vector store as disk).
- [**LangChain — Memory types**](https://python.langchain.com/docs/concepts/memory/) — A comparison table of memory classes within the framework.
- [**Anthropic — Memory Tool (memory in agents)**](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Anthropic's official tool-based memory implementation.

> 💡 **Track B Spotlight**: In Stage 7, when you build multi-agent systems, each agent will have both "its own memory" and "shared memory" — typically requiring a **hybrid of patterns 2 + 3**. Master all three patterns in this stage so you don't get stuck on multi-agent memory design in Stage 7.

### Advanced: The CoALA Framework — A 4-Layer Taxonomy for Agent Memory

[**Sumers et al. 2023 — Cognitive Architectures for Language Agents**](https://arxiv.org/abs/2309.02427) breaks agent memory into four types, which is now the most commonly used mental model:

| Type | What it Stores | Corresponding Example |
|---|---|---|
| **Working memory** | Context for the current task | The LLM's context window itself |
| **Episodic memory** | Specific experiences from past tasks | Reflexion's reflection records, past trajectories |
| **Semantic memory** | Abstract facts / knowledge | RAG knowledge base, user profile, preferences |
| **Procedural memory** | How-to procedures / skills | Tool definitions, [Skills (Stage 5.3)](05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層) |

→ **Why it's useful**: The three patterns above (buffer / summary / vector) only deal with working and episodic memory. A production agent needs all four layers designed. CoALA is a checklist to see which layer your agent is missing.

### Advanced: Generative Agents — The Three-Factor Scoring (Classic Case Study)

In [**Park et al. 2023 — Generative Agents: Smallville**](https://arxiv.org/abs/2304.03442), the simulated town has 25 NPC agents, each with its own memory stream. Retrieval is weighted by three scores:

- **Importance**: The LLM itself gives each memory an importance score from 1-10 (eating = 2 points, breaking up = 9 points).
- **Recency**: Time-based decay (exponential decay).
- **Relevance**: Embedding similarity to the current query.

Final score = `α·importance + β·recency + γ·relevance`, and the top-k are retrieved. **This is the conceptual backbone of 2024-2025 production memory layers (mem0 / Letta).**

### 2024-2026 Latest Works on Memory — An Overview

⭐ **Year** marker = latest works from 2025-2026.

| Technique | One-sentence description | Year / Paper |
|---|---|---|
| **Anthropic Memory Tool** | Claude's official tool-based memory, called via API, file-based | [Anthropic Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool) 2024 |
| **A-MEM** (Agentic Memory) | Zettelkasten-inspired, automatically creates links between memories, evolves over time | [Xu et al. 2025](https://arxiv.org/abs/2502.12110) ⭐ **2025** |
| **HippoRAG 2** | Hippocampus-inspired, KG + Personalized PageRank, cross-document multi-hop | [Gutiérrez et al. 2025](https://arxiv.org/abs/2502.14802) ⭐ **2025** |
| **MemGPT → Letta GA** | OS-paging memory, dual-layer (working/archival), strong for long sessions | [Packer et al. 2023](https://arxiv.org/abs/2310.08560) → Letta 2024 GA |
| **MemoryBank** | Ebbinghaus forgetting curve; accessed memories are strengthened, unused ones decay | [Zhong et al. 2023](https://arxiv.org/abs/2305.10250) |
| **MemoryLLM** | Self-updatable memory parameters built into the model (in weights, not context) | [Wang et al. 2024](https://arxiv.org/abs/2402.04624) |
| **mem0** (listed above) | Production memory layer, auto fact extraction + forgetting | [mem0ai/mem0](https://github.com/mem0ai/mem0) 2024 |
| **Memory in the Age of AI Agents** (survey) | Systematic survey, 3D taxonomy (temporal scope/substrate/control policy) + benchmark compilation | [Hu et al. arXiv:2512.13564](https://arxiv.org/abs/2512.13564) ⭐ **2025-12** |
| **Memory for Autonomous LLM Agents** (survey) | Formalizes agent memory as a write-manage-read loop, surveyed across 2022-2026 | [arXiv:2603.07670](https://arxiv.org/abs/2603.07670) ⭐ **2026** |
| **From Storage to Experience** (survey) | An evolutionary framework: Storage → Reflection → Experience, analyzing 3 evolutionary drivers | [arXiv:2605.06716](https://arxiv.org/abs/2605.06716) ⭐ **2026** |
| **ScrapMem** | Bio-inspired on-device memory, "**Optical Forgetting**" gradually reduces resolution of old memories | [arXiv:2605.03804](https://arxiv.org/abs/2605.03804) ⭐ **2026-05** |
| **Memory Security survey** | Risks of long-term memory: cross-session poisoning, unauthorized access, internal propagation | [arXiv:2604.16548](https://arxiv.org/abs/2604.16548) ⭐ **2026** |

> 💡 **2025-2026 Trend Watch**:
> - **Structured, evolvable, associative** (A-MEM / HippoRAG 2) — Moving from flat vector stores to brain-inspired architectures.
> - **2026 is the year of memory explosion** — 5 major surveys + ScrapMem on-device memory + the emergence of memory security as a topic.
> - **Memory automation, multimodality, and multi-agent memory** are the new frontiers (see emerging frontiers listed in the [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) survey).
> - **Memory security becomes its own subfield** — As agents run for a long time, their memories can be attacked and need protection (connects to Stage 7 §Security).
>
> If your agent is long-running (on the order of weeks/months), the two 2026 surveys above are must-reads.

## 🧩 Chunking Details (Technical Deep Dive)

Good chunking allows an LLM to generate more accurate and complete answers within a limited context. It's not just about splitting text evenly.

The splitting method depends on the application scenario and document content. It determines the smallest semantic unit the retriever sees.

A good chunk must be two things at once: **complete enough** for the model to understand the context, and **focused enough** to avoid bringing in too much noise during retrieval. Chunks that are too small lose context; chunks that are too large make similarity search less precise.

**Common Strategies**:

- **Fixed-Length**: Split by character or token count. Simple and stable, but can awkwardly cut off paragraphs, sentences, or tables.
- **Sliding Window**: Maintain an overlap between consecutive chunks. Reduces information loss at boundaries but increases the size of the index.
- **Recursive**: Tries to preserve paragraphs first, then falls back to smaller units like sentences or words if the length is still unsuitable. Often a good baseline for starting with RAG.
- **Semantic Chunking**: Splits based on embedding or semantic changes, i.e., when the semantic similarity between the current block and the previous one differs. Good for long documents, but higher cost and complexity.
- **Hybrid**: Mix and match splitting methods based on the document structure and application. For example, a research paper might need to preserve chapters, tables, formulas, and citation context.

![Chunking Strategy Flow](../resources/diagrams/chunking-strategies.jpg)

When you're first doing RAG, don't start with a complex splitting method. The LangChain documentation recommends starting with `RecursiveCharacterTextSplitter` for most scenarios.

First, run a baseline version, then decide whether to change strategies based on the retrieval results.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "This is a very long document content... (one thousand words omitted here)..."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

chunks = splitter.split_text(text)
print(f"Split into {len(chunks)} chunks")
print(chunks[0])
```

**To intuitively judge if your chunking is good**, check two things:

- The answer is missing information or seems incomplete: Usually means chunks are too small or overlap is insufficient.
- The answer contains the correct information but is mixed with irrelevant content: Usually means chunks are too large or top-k is fetching too many.

**Advanced Considerations**:

- Chunking isn't a one-and-done setting; it needs to be iteratively adjusted based on real queries and failure cases.
- Chunk size, overlap, top-k, and the reranker all affect each other. Don't tune one parameter in isolation.
- Think about it: if you were to RAG over a PDF with images or a meeting transcript, what would be the best way to chunk it?
- For advanced variations of chunking (Sentence-Window / Parent-Child / Multi-Vector), see the Advanced RAG Techniques overview table above.

## 🪞 Advanced: Reflexion with Persistent Memory (Complete Version) ⭐ Track B Optional Reading

> **This section is for concept + routing, not an exercise.** It continues from the basic version in [Stage 3 §Reflection](03-tool-use-and-hello-agent.md#-反思reflexion--self-refine-概念--路由) (single-session Actor/Critic loop) and explains why some reflections **require** persistent memory. This version truly belongs to the theme of Stage 6.

**How does the complete Reflexion differ from Self-Refine?**

| Version | What's kept across turns | What's kept across sessions | Memory pattern needed |
|---|---|---|---|
| **Self-Refine** (Madaan 2023) | Last turn's answer + critic feedback | ❌ Nothing | None needed (pattern 1 buffer is enough) |
| **Complete Reflexion** (Shinn 2023) | Same as above | ✅ Saves "reflection summaries" from past trials to episodic memory, retrieves them as lessons for similar tasks in the future | **Needed** (pattern 3 vector store or pattern 2 summary) |

**Why this version needs memory**: The Reflexion paper's verbal reinforcement learning is about the "agent accumulating lessons across trials." The agent tries a task → fails → reflects on "why it failed" and stores it → next time, it retrieves past reflections into the prompt to avoid repeating the mistake. This requires **persistent episodic memory**, which directly connects to the 3 memory patterns discussed earlier in this stage.

**Typical Architecture** (Complete version with persistent memory):

```
Actor → Critic → Actor    (Single-turn loop, same as in Stage 3 §Reflection)
       ↑──────────┘
            ↓
   Reflection summary
            ↓
   Episodic memory store
   (vector / summary pattern, see §Memory Design pattern 3 above)
            ↓
   next task → retrieve relevant past reflections
            → prepend to Actor's prompt
            (accumulate lessons across trials, don't repeat mistakes)
```

→ **Difference from Stage 3 §Reflection**: Stage 3 was a **single-session in-context** loop (no external store). This section is about a **persistent episodic memory store + retrieval** (learning across trials).

### 📚 To get hands-on / dive deeper

**Papers**:
- [**Reflexion (Shinn et al. 2023)**](https://arxiv.org/abs/2303.11366) ⭐ — The **complete version** paper, with Algorithm 1 showing how the memory buffer is used.
- [**Self-Refine (Madaan et al. 2023)**](https://arxiv.org/abs/2303.17651) — The comparison baseline, a version without episodic memory.

**Reference Implementations**:
- [**noahshinn/reflexion**](https://github.com/noahshinn/reflexion) — The first author's reference implementation (including the full episodic memory flow).
- [**LangChain — Reflexion**](https://langchain-ai.github.io/langgraph/tutorials/reflexion/reflexion/) — The LangGraph version, which can be directly connected to the RAG pipeline in exercise 4 of this stage.
- [**mem0**](https://github.com/mem0ai/mem0) (listed above) + [**Letta**](https://github.com/letta-ai/letta) (listed above) — Production memory layers that can serve as the episodic store for Reflexion.

> 💡 **Division of labor with Stage 3 §Reflection**:
> - To understand "how the reflection loop works, how it runs in a single turn" → Stage 3 §Reflection
> - To understand "how reflection accumulates across sessions, how an agent learns from its past" → This section
> - To see how reflection is used in production agents (Cursor / Claude Code) → [Stage 5 §5.6 Harness Internals](05-claude-code-ecosystem.md#56--claude-code-source-解剖reference-harness-implementation-track-b-必看)

## 🤔 Advanced Reasoning / Reflection — 2024-2026 Schools of Thought ⭐ Both tracks should read

Reflexion is **prompt-based reflection** — the LLM corrects itself during inference. In 2024-2025, a **second path** emerged: **training reflection into the model itself** (OpenAI's **o1** / DeepSeek's **R1**). You should know both paths.

### Path 1: Prompt-based reflection / reasoning (Traditional approach)

| Technique | Core Idea | Paper |
|---|---|---|
| **Self-Consistency** | Sample N reasoning paths, take a majority vote — **simplest + most used** | [Wang et al. 2022](https://arxiv.org/abs/2203.11171) |
| **Tree of Thoughts (ToT)** | Reasoning as a tree, can branch and backtrack, good for puzzles/planning | [Yao et al. 2023](https://arxiv.org/abs/2305.10601) |
| **Graph of Thoughts (GoT)** | Not just a tree, can merge branches arbitrarily | [Besta et al. 2023](https://arxiv.org/abs/2308.09687) |
| **Chain-of-Verification (CoVe)** | Generate answer → ask itself verification questions → revise answer | [Dhuliawala et al. 2023](https://arxiv.org/abs/2309.11495) |
| **CRITIC** | Tool-augmented self-critique (verifies with search/calculator) | [Gou et al. 2023](https://arxiv.org/abs/2305.11738) |
| **Self-Discover** | Agent first "discovers" which reasoning structure to use, then executes | [Zhou et al. ICML 2024](https://arxiv.org/abs/2402.03620) ⭐ 2024 |
| **Self-Refine / Reflexion** | Already covered above / in Stage 3 | Stage 3 §Reflection, this stage §Reflexion |

### Path 2: Trained-in reasoning / reflection (The big shift of 2024-2026)

Pioneered by OpenAI's **o1** (Sept 2024), open-sourced by DeepSeek's **R1** (Jan 2025), and now at the frontier with **DeepSeek-V4-Pro** (Apr 2026 preview, agent-focused open-source reasoning), Claude Opus 4.7 (Apr 2026), GPT-5.5 (Apr 2026), and Gemini 3.1 Pro (Feb 2026) — this approach **trains "step-by-step thinking + self-correction" into the model's weights**. During inference, it automatically unfolds a long reasoning chain (thinking tokens). **This is the biggest paradigm shift in LLMs for 2024-2026**, and all current frontier models follow this path. The table below lists only the **current (May 2026) frontier** — historical predecessors (o1/R1/Sonnet 4.5/Gemini 2.5) are omitted; see release dates for lineage.

| Model | Source / Release | Features | Link |
|---|---|---|---|
| **GPT-5.5** | OpenAI Apr 2026 (prev: o1 Sep 2024 → o3 → GPT-5 Aug 2025 → 5.4 Mar 2026) | Closed source, merged reasoning+chat, Thinking budget API, enhanced agent capabilities | [OpenAI](https://openai.com/) |
| **Claude Opus 4.7** | Anthropic 2026 (prev: Sonnet 4.5 / Opus 4.5) | Closed source, controllable thinking budget (API param), **leads on SWE-bench/Terminal-bench** | [Anthropic extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) |
| **Gemini 3.1 Pro** | Google Feb 2026 (prev: Gemini 2.5 Thinking 2025, Gemini 3 Nov 2025) | Closed source, can view thinking trace, **94.3% on GPQA Diamond**, leads in price/speed/multimodality | [Gemini API](https://ai.google.dev/gemini-api/docs/thinking) |
| **DeepSeek-V4 / V4-Pro / V4-Flash** | DeepSeek Apr 2026 preview (prev: R1 Jan 2025 → V3.1) | Open source **MIT license**, agent-focused training, integrates reasoning + tool use + knowledge processing, R-series reasoning merged into mainline | [HF DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [R1 paper (method baseline)](https://arxiv.org/abs/2501.12948), [CNBC report](https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html) |
| **QwQ-32B / QvQ-72B** | Alibaba Qwen Nov 2024 ~ 2026 | Open source **Apache 2.0**, 32B is still the top choice for small-size reasoning, QvQ is the visual version | [QwQ blog](https://qwenlm.github.io/blog/qwq-32b-preview/) |

### How to choose between the two paths

| Your situation | Recommendation |
|---|---|
| Using a general chat model base, want to add reasoning | Path 1 (prompt-based) — ToT / Self-Consistency / CoVe |
| Budget/latency allows, need the strongest reasoning | Path 2 — Pick one from **GPT-5.5 / Opus 4.7 / Gemini 3.1 Pro / V4-Pro** |
| Want to fine-tune your own reasoning model | Path 2 — Read the R1 paper (method baseline), start with R1-Distill / V4 open weights |
| Want on-device / extremely tight budget | **QwQ-32B** (Apache 2.0) or an R-series distill |
| Multi-agent debate / critic scenarios | Path 1 (CRITIC / debate) + [Stage 7 §multi-agent](07-multi-agent-production.md) |

> 💡 **2025-2026 Observations**:
> - Reasoning models are absorbing the Reflexion-style patterns into their weights — but **prompt-based reflection is not obsolete**: an agent loop (to control when/what to reflect on) and multi-agent debate are still necessary.
> - **Open source is closing in on closed source in 2026** — DeepSeek-V4-Pro (Apr 2026 preview, MIT license) folds R1-style reasoning into the main line with agent-focused training; the gap with GPT-5.5 / Gemini 3.1 Pro keeps narrowing.
> - **Agent capability is the new headline** — V4 / Opus 4.7 both feature agent-as-product benchmarks (SWE-bench / Terminal-bench / tool use) as their main selling point. Pure reasoning isn't enough anymore.
> - The two paths will coexist for a long time; production agents use both.

## 🛠 Hands-on Exercises (Basic Illustrative Exercises)

### Exercise 1: Embeddings
Embed 100 sentences and find the nearest neighbor for a given query. Understand the meaning of distance between vectors.

### Exercise 2: Vector DB
Store embeddings in Chroma and perform a semantic query. Compare it with a keyword search to see the difference.

### Exercise 3: Chunking Comparison
Take one document and split it in three ways: fixed-length, paragraph-based, and heading-aware. Use 5 real questions to compare the top-k results and record which splitting method is better at fetching the correct context.

### Exercise 4: Full RAG Pipeline
Take a PDF, chunk it → embed it → retrieve top-k → generate an answer. This is the basic skeleton for most RAG applications.

### Exercise 5: Long-term Memory
Make an agent remember things across multiple conversation turns. You can use `mem0` or build your own with a vector store.

## 🎯 Recommended Memory / RAG Tools (by Use Case)

Don't know where to start? Here are the common pairings in the industry as of late 2025. **Look at "Scenario" to get started, click the link to dive deeper into the repo.**

| Scenario | Recommended Tools | Why |
|---|---|---|
| **First time running RAG** (quickest start) | [Chroma](https://github.com/chroma-core/chroma) + [LlamaIndex](https://github.com/run-llama/llama_index) | Local-first, zero ops, quickstart-friendly. Default for Stage 6 exercises. |
| **Agent long-term memory** (personal assistant / chatbot) | [mem0](https://github.com/mem0ai/mem0) | Auto fact extraction + forgetting + namespaces, a production memory layer. |
| **Cross-session, persona-stable agent** (therapist / tutor / long-term assistant) | [Letta](https://github.com/letta-ai/letta) | OS-style paging memory, dual-layer (working/archival), strong for long sessions. |
| **Production-scale RAG** (millions of docs) | [Qdrant](https://github.com/qdrant/qdrant) + LlamaIndex | A vector DB written in Rust, faster than Chroma at scale. |
| **Existing Postgres environment** | [pgvector](https://github.com/pgvector/pgvector) | A Postgres extension, SQL + vector together, simplest ops. |
| **Enterprise RAG + Web UI** | [RAGFlow](https://github.com/infiniflow/ragflow) | Strong document parsing (incl. OCR/tables/layout), for enterprise, includes a Web UI. |
| **Chinese RAG template** | [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | Most comprehensive in the Chinese community, good local LLM integration (ChatGLM/Qwen/Llama). |
| **Advanced: Contextual Retrieval** | [Anthropic cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | Claude with prompt caching for contextual chunking (**see §Advanced RAG Techniques above**). |
| **Advanced: Knowledge graph reasoning** | [LightRAG](https://github.com/HKUDS/LightRAG) / [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | Knowledge graph + RAG for entity-relation reasoning (**see §Advanced RAG Techniques above**). |
| **Cross-topic tutorial collection** | [ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | A collection of RAG + agent tutorials in Jupyter notebook format. |

**Recommended Adoption Order**:
1. Must-install first: **Chroma + LlamaIndex** (to do the Stage 6 exercises).
2. Agent needs to remember things: Add **mem0** (the simplest memory layer).
3. Starting to scale to production: Switch to **Qdrant** or **pgvector**.
4. Want to upgrade to advanced RAG: See the three subsections in §Advanced RAG Techniques above.

## 🎯 Featured Projects (Templates / Specs / Example Collections)

Categorized by use case, 13 projects in one table. **Look at "Who it's for" to get started, click the link to dive deeper into the repo.**

| Category | Project | ⭐ | Who it's for | Why it's recommended / Notes |
|---|---|---|---|---|
| **RAG framework**<br>(Full pipeline) | [LlamaIndex](https://github.com/run-llama/llama_index) | ⭐⭐⭐⭐⭐ | Document-centric applications | RAG-first design, end-to-end for doc loading/chunking/retrieval/query engine. ★ 49k+ |
| | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | ⭐⭐⭐⭐⭐ | Shipping RAG to non-devs | Production-grade RAG engine, deep doc understanding (layout/tables/OCR) + hybrid retrieval + agent loop + Web UI. ★ 79k+, Apache-2.0 |
| | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | ⭐⭐⭐⭐ | Want to see research-grade graph + long-context memory methods | Graph + vector hybrid retrieval + summarization-based memory, EMNLP 2025 paper-backed. ★ 34k+, MIT. Research-style codebase. |
| **Vector DB**<br>(local-first) | [Chroma](https://github.com/chroma-core/chroma) | ⭐⭐⭐⭐⭐ | Exercises 2 / 4, easiest vector DB to start with | Open-source embedding database, runs locally, in-memory/SQLite backend, zero ops. ★ 27k+, Apache-2.0. **Install**: `pip install chromadb` |
| **Vector DB**<br>(production scale) | [Qdrant](https://github.com/qdrant/qdrant) | ⭐⭐⭐⭐⭐ | When Chroma can't keep up, need production scale | A vector DB written in Rust, has cloud and self-hosted versions. ★ 31k+ |
| **Vector DB**<br>(hybrid) | [Weaviate](https://github.com/weaviate/weaviate) | ⭐⭐⭐⭐ | Production deployment + schema constraints | Built-in modules (text2vec/generative/classification), schema-driven, built-in BM25 + vector hybrid. ★ 16k+ |
| **Vector DB**<br>(existing Postgres) | [pgvector](https://github.com/pgvector/pgvector) | ⭐⭐⭐⭐ | Teams already using Postgres | A Postgres extension, SQL + vector in the same DB, simplest ops. ★ 21k+ |
| **Memory framework**<br>(auto fact extraction) | [mem0ai/mem0](https://github.com/mem0ai/mem0) | ⭐⭐⭐⭐⭐ | Personal assistants / chatbots that need user-level memory | Self-refining memory layer, stores facts across sessions. ★ 54k+ |
| **Memory framework**<br>(OS-paging) | [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | Agents that run for a very long time (months) | Hierarchical memory (working/archival), OS-paging concept. ★ 22k+ |
| **Memory (in-framework)** | [LangChain — Memory](https://python.langchain.com/docs/concepts/memory/) | ⭐⭐⭐ | Already using LangChain | 4 memory abstractions (buffer/summary/vectorstore-backed/entity) |
| **Advanced RAG technique** | [Anthropic — Contextual Retrieval cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | ⭐⭐⭐⭐⭐ | Finished basic RAG and want an upgrade | Claude with prompt caching for contextual chunking, includes a full E2E example. |
| **Chinese RAG template** | [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | ⭐⭐⭐⭐ | Chinese knowledge bases / RAG apps | Widely used in the Chinese community, deployable offline, good Chinese defaults, supports ChatGLM/Qwen/Llama/Ollama. ★ 38k+, Apache-2.0. ⚠️ Last updated Nov 2025 (becoming stale). |
| **Tutorial Collection** | [patchy631/ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | ⭐⭐⭐⭐ | Want to see "how the same concept is implemented in different contexts" | Themed collection of LLM/RAG/agent tutorials in Jupyter notebooks, useful across multiple stages. ★ 34k+, MIT. |


## ✅ Self-Check Before Entering Stage 7

Can you:
- [ ] Write a 50-line RAG pipeline (load → chunk → embed → store → query → answer)?
- [ ] Explain why naive chunking fails on long documents?
- [ ] Design different chunking strategies for API documentation, PDFs, and tables?
- [ ] Choose between Chroma, Qdrant, and pgvector for a given scale?
- [ ] Differentiate between "giving an agent memory" and "using RAG"?
- [ ] Explain what RAG and Memory each bring to the table (from the §From RAG to Memory table above)?

If yes to all → proceed to [Stage 7 — Multi-Agent · Advanced Applications](07-multi-agent-production.md).
