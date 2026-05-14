# Stage 6 — Memory · RAG · Context Engineering

> [繁體中文](./06-memory-rag.md) | **简体中文** | [English](./06-memory-rag.en.md)

⏱️ **时间估算**：2 周（约 10 小时）

> 💡 这 stage 术语密度高（**RAG / 向量数据库 / embedding / chunking / hybrid search / reranking⋯**）→ 不熟先翻 [`resources/glossary.md` §3](../resources/glossary.md#3-memory--retrieval--rag)。

> 📋 **本章组成**（渐进式 flow、由浅入深）：
>
> 1. **定位** —— Context Engineering 是什么 + 概念对照表 ×2
> 2. **目标 / 入口** —— 学习目标 → 进入条件 → 必修阅读 → 单元指引
> 3. **RAG 主轴** —— 🌐 RAG 基础流水线 → 🚀 进阶 RAG 技巧（GraphRAG / Contextual Retrieval / Hybrid Search / Query Trans / Self-improving / RAPTOR + **2024-2026 纵览**）
> 4. **Bridge** —— 🌉 从 RAG 到 Memory（为什么 RAG 还不够）
> 5. **Memory 主轴** —— 🧠 短/长期 + 3 种 pattern + CoALA + Generative Agents + **2024-2026 纵览**
> 6. **技术深入** —— 🧩 Chunking 细节
> 7. **进阶反思 / 推理** —— 🪞 Reflexion 完整版 → 🤔 Path 1 prompt-based + **Path 2 trained-in**（o1 / R1 / V4-Pro / Opus 4.7 / GPT-5.5）
> 8. **练习 / 推荐 / 自检** —— 动手练习 → 常用工具 → 精选 Projects → 自我检查
>
> 🔑 **关键名词**：见 [`resources/glossary.md` §3](../resources/glossary.md#3-memory--retrieval--rag)（memory / RAG / embedding / chunking / reranking）

## 🎯 Context Engineering 是什么（先定位）

**Context Engineering = 跨多次 LLM call 怎么动态组装 prompt 的工程学科**。Stage 2 教你「**单次** prompt 怎么写」、本 stage 教你「**跨多次** call 怎么管 context」——当你需要动态组 system prompt + 拉 memory + 塞 retrieved chunks + 接 tool definitions 时、就到了 context engineering 领域。

**Discipline lineage**（你现在在第 2 层）：

| 层 | Discipline | 解决什么 | 在哪 stage |
|---|---|---|---|
| 1 | **Prompt Engineering** | 单次 LLM call 怎么问才准 | [Stage 2](02-prompt-engineering.md) |
| **2** | **Context Engineering**<br>（**本 stage**） | **跨多次 call 怎么动态组 prompt** | **本 stage** |
| 3 | **Harness Engineering**¹ | 把多个 LLM call 包成 production runtime | [Stage 7 §Harness Engineering](07-multi-agent-production.md#-harness-engineering--production-agent-runtime-的工程學--本-stage-核心概念) |

> ¹ "Harness Engineering" 还不是业界统一称呼——本教材沿用 Anthropic / Hamel Husain / Simon Willison 等人 2024-2026 写作中的用法（loop / control flow / runtime 的工程化）。其他人可能叫 "Agent Runtime"、"Agent Loop Engineering"、"Inference Orchestration"——指的是同一件事。

**Context Engineering 的 3 个 problem domain**（本 stage 主轴是前两个）：

1. **Retrieval** — 怎么从外部知识库捞相关片段（RAG / vector search / GraphRAG / hybrid search）
2. **Memory 管理** — short-term / long-term / episodic / semantic memory 怎么分层、怎么存、怎么忘
3. **Context window 预算** — 多少 token 给 prompt、多少给 history、多少给 retrieval；接 Stage 7 §Harness 处理

### 4 个常被搞混的概念 — 一张表分清楚

| 词 | 是什么（抽象 / 具体）| 范例工具 |
|---|---|---|
| **Memory** | agent 跨对话 / 跨 session 记事情的**能力**（抽象概念） | LangChain `ConversationBufferMemory` / mem0 / Letta |
| **Embedding** | 把文字转成 N 维**向量**、让相似度可计算（数据转换） | `sentence-transformers` 跑出 768 维向量 / OpenAI `text-embedding-ada-002` |
| **Vector DB** | 存 + 查 embedding 的**存储层**（基础设施） | Chroma / Qdrant / Weaviate / pgvector |
| **RAG** | “retrieve 相关片段 → 塞进 prompt → 生成”这个 **pattern**（架构模式） | LlamaIndex / LangChain RAG chain |

→ **核心区分**：Memory 是**能力**、Embedding 是**数据转换**、Vector DB 是**存储**、RAG 是**架构 pattern**——这 4 个常被混用、实际上是 4 个不同层的概念。

### RAG vs Long Context vs Fine-tuning — 何时用什么

LLM 知道你的私有 / 领域数据、有 3 种主要做法。**本 stage 教 RAG**，但你要知道何时不该用：

| 选择 | 适合 | 不适合 | 成本 |
|---|---|---|---|
| **RAG**<br>（外部 retrieve） | 大型 / 变动 / 私有知识库、需要 citation 引用来源 | 推理需要全文一起看的任务、需要跨文件 multi-hop reasoning | 每 query 多 1 次 vector search 的 latency |
| **Long Context**<br>（直接塞 prompt） | < 200k token 的中型文件、一次性查询、需要 cross-doc reasoning | 知识库大 / 经常变动 / 想要 citation | 每 query 烧大量 input token（即使有 prompt caching）|
| **Fine-tuning**<br>（改 model 权重） | 风格 / 格式统一、特定领域语言（医疗、法律、code）| 知识会变、要 citation、不想练 model | 训练成本 + 维护成本 + 模型 lock-in |

→ **怎么选**：先试 RAG（成本最低、变动最容易）→ RAG 捞不到才考虑 Long Context → 两个都不行才考虑 Fine-tuning。**进 Stage 7 学 fine-tune deploy**。

## 📌 学习目标

- 建一条基本 RAG 流水线（chunk → embed → store → retrieve → generate）
- 看出 RAG 不该用在哪些地方（以及该用在哪些地方）
- 区分 short-term、long-term、episodic、semantic memory
- 理解 vector embedding 与相似度搜索
- 知道进阶 RAG（GraphRAG / Contextual Retrieval / Hybrid Search）何时加、何时不加

## 🚪 进入条件

你应该已经：
- 完成 Stage 3（会写 tool use、会呼叫 LLM API、看得懂 ReAct loop）
- 能跑 Python `pip install` 安装 SDK（后面练习会用到 `chromadb`、`sentence-transformers` 等）
- 对 list / dict / generator 等基础 Python 结构上手

没到的话 → 回 [Stage 3](03-tool-use-and-hello-agent.md) 或 [Stage 0 §环境设定](00-foundations.md#何時可以跳過這個階段)。

## 📚 必修阅读

1. [**LlamaIndex — RAG concepts**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/) — 最清楚的入门
2. [**LangChain — RAG tutorial**](https://python.langchain.com/docs/tutorials/rag/) — 动手做
3. [**Pinecone — Learning Center**](https://www.pinecone.io/learn/) — vector DB 基础
4. [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval) — Anthropic 搭配 prompt caching 的 RAG 写法
5. [**LangChain — Text splitters**](https://docs.langchain.com/oss/python/integrations/splitters/index) — chunking 策略入门

> 🙏 **Memory 章节特别推荐 [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)**：本 stage 探讨 memory 的概念跟初级实作、要 **chapter-length 深入版**请看 hello-agents 对应章节——short-term / long-term memory 的差异、context engineering 怎么动态组装、session 持久化、forgetting strategy 都讲得最完整。本 stage 是路线图、那边是深度教材。

## 🧭 单元指引（渐进式 flow）

本章按 **RAG 先学、Memory 后学** 的顺序走——RAG 是 context engineering 最基础、最常用的工具，Memory 是 agent 跨对话/跨 session 的能力；先把 RAG pipeline 跑通、再带到 Memory 设计，最后回头看 Chunking 细节。

**阅读顺序建议**：

1. **🌐 RAG 基础流水线**（下一节）— 建立 mental model
2. **🚀 进阶 RAG 技巧** — GraphRAG / Contextual Retrieval / Hybrid Search 等 production 升级
3. **🌉 从 RAG 到 Memory** — 为什么 RAG 还不够、需要 Memory 补哪段
4. **🧠 Memory 设计** — 短期 vs 长期、3 种 pattern、CoALA framework
5. **🧩 Chunking 细节** — RAG / Memory 都会用到的技术深入

读这章时可以顺便思考：RAG 不适合哪些应用场景？哪些场景适合 RAG，但基本 RAG 还不够好？这会带到后面的 GraphRAG / Self-RAG / RAPTOR 等进阶技术。

## 🌐 RAG 基础流水线

**RAG（Retrieval-Augmented Generation）**= “retrieve 相关片段 → 塞进 prompt → 生成”这个 pattern。可以想成在帮 agent 盖图书馆——你要先把书放好、分类好，后续要查资料时，才会又快又精准。

**最基础的 RAG 拆成两条流水线**：

- **数据预处理（ingest 一次）**：ingest → chunk → embed → store（index）。这一步是在建立可检索的知识库。
- **检索生成（每次 query）**：retrieve → generate。这一步是在用户提问时，找出相关内容，再交给 LLM 生成回答。

![RAG 流水线总览](../resources/diagrams/rag-pipeline-overview.jpg)

图中的 RAG Fusion、query rewrite 等属于进阶检索技巧。**第一次学 RAG 时，先理解主线流程即可**。

**5 个 step 解读**：

| Step | 做什么 | 在哪一条 pipeline | 技术细节在 |
|---|---|---|---|
| **1. ingest** | 把数据载入（PDF / web / DB / 对话 log） | 预处理 | LlamaIndex / LangChain 各自 loader |
| **2. chunk** | 把文件切成小块（500-2000 token / chunk） | 预处理 | 见后段 §🧩 Chunking 细节（先读 RAG / Memory 主轴、技术深入留到那边） |
| **3. embed** | 每个 chunk 转成 N 维 vector | 预处理 | `sentence-transformers` / OpenAI `text-embedding-ada-002` |
| **4. store** | vector + metadata 存进 vector DB | 预处理 | Chroma / Qdrant / pgvector |
| **5. retrieve + generate** | query 也 embed → top-k semantic search → 拼进 prompt → LLM 生成 | 每次 query | 通用 LLM API |

上面只是最小骨架。**最常踩的坑 3 个**：

- **chunk太大 / 太小**：太大、retrieve 捞到的 chunk 里只有一句相关、其他都是噪声；太小、失去上下文（见 §Chunking 细节）
- **embedding model 选错**：中文文件用英文 model、retrieval 精度直接掉一半
- **top-k 设太大 / 太小**：太小、漏 relevant chunk；太大、噪声高 / token 烧

跑完基本骨架后，跑 §动手练习 1-4（embeddings / vector DB / chunking / 完整 pipeline）建立手感、再进下一节 §进阶 RAG 技巧。

## 🚀 进阶 RAG 技巧（跑完基本 RAG 之后再看）

下面六个 subsection 是 2024-2026 production RAG 最常加上的杠杆，按「加进 pipeline 哪一层」分组：
- **Retrieve 后** —— GraphRAG / Contextual Retrieval / Hybrid Search & Reranking
- **Retrieve 前**（query 改写）—— Query Transformations
- **Retrieve 期间**（control flow）—— Self-improving RAG
- **Index 结构** —— RAPTOR
- **2024-2026 纵览** —— 其他 17 个值得知道的技巧

**先跑完上面 RAG 基础拿到基准版本、再回来看这里**——不然你会在没有基准的情况下调参数，永远不知道是哪个改动带来提升。

| 技巧 | 解决什么问题 | 加在 pipeline 哪一层 | 成本 |
|---|---|---|---|
| **GraphRAG** | vanilla RAG 不会做 multi-hop / 跨文件 entity-relation 推理 | retrieve 前（建 graph）+ retrieve 时（graph traversal）| 高（要先建 KG、需 LLM 抽 entity）|
| **Contextual Retrieval** | chunk 失去原文件 context、retrieval 捞错片段 | chunk 后 / embed 前（加 contextual header）| 中（一次性、搭 prompt caching 后便宜 90%）|
| **Hybrid Search & Reranking** | 纯 vector 漏字面命中、top-k 噪声高 | retrieve 中（并查 BM25）+ retrieve 后（cross-encoder rerank）| 低（成熟工具直接接）|

### 🔗 GraphRAG — 知识图谱 + RAG

**Mental model**：vanilla RAG 把文件切成 chunk、靠 embedding 相似度捞片段——但**它不知道哪些 entity 是同一个东西、entity 之间有什么关系**。GraphRAG 在 ingest 阶段先用 LLM 把文件抽成 **(entity, relation, entity)** 三元组建知识图谱，retrieve 时除了向量比对、还做 graph traversal 捞到“相关 entity 的相关 entity”。

**何时用**：
- 任务需要 **multi-hop reasoning**（A → B → C 才能回答）
- 跨多份文件、entity 互相引用（公司财报、论文引用、调查报告、法律案例）
- 问题形如“X 影响了什么 Y、Y 又连到哪些 Z”——vanilla RAG 通常只捞到 X 那块文件

**何时不用**：
- 文件之间没有 entity-relation 链接（纯 FAQ、产品手册各自独立）
- 知识库小（< 1k chunk）——vanilla RAG 已经够
- 预算紧——建 KG 的 token 成本可能是普通 RAG 的 10-50 倍

**代表 framework**：
- [**Microsoft GraphRAG**](https://github.com/microsoft/graphrag) ⭐ — 原版 reference 实现、Apache-2.0、含 community detection
- [**HKUDS/LightRAG**](https://github.com/HKUDS/LightRAG) — 轻量版、EMNLP 2025、KG + vector hybrid、cost 比 Microsoft 版低
- [**gusye1234/nano-graphrag**](https://github.com/gusye1234/nano-graphrag) — < 1000 行的最小实现、适合先读懂原理

**Paper**：[**From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Edge et al. 2024)**](https://arxiv.org/abs/2404.16130) — Microsoft GraphRAG 的原始 paper、解释 community summarization 为什么能解 global query

### 🪶 Contextual Retrieval — Anthropic 的 prompt-caching 解法

**Mental model**：vanilla chunk 失去原文件 context——“Q3 revenue grew 15%”这个 chunk 抽出来、你不知道是**哪家公司**、**哪一年**的 Q3。Anthropic 2024 提出：**ingest 时用 LLM 为每个 chunk 写一段 50-100 token 的 contextual header**（“This chunk is from ACME Corp 2024 Q3 earnings, discussing the cloud segment...”）拼到 chunk 前面再 embed。搭配 **prompt caching** 让“整份文件 + 每个 chunk”这个 prompt 只计费一次、后面所有 chunk 共用 cache。

**何时用**：
- chunk 字面意思跟原文件主题距离远（财报、研究报告、长 narrative 文件）
- 你愿意一次性付 ingest 成本、换 retrieve 精度
- 已经在用 Claude / 想用 prompt caching（其他 model 也能跑、就是没 cache 折扣）

**何时不用**：
- chunk 本身就是 self-contained（FAQ、产品介绍页、定义条目）
- 知识库经常变动（每改一次就要重 ingest）
- 预算极紧——即便 cache 折扣后、ingest 成本仍比 vanilla 高

**为什么省 90% cost**：Anthropic 报告 prompt caching 把“整份文件当 cached prefix”、每个 chunk 只送差异——比起每 chunk 都喂整份文件、成本降到约 1/10。但**这只省 ingest、不省 retrieve 阶段**。

**代表实现**：
- [**Anthropic — Contextual Retrieval blog**](https://www.anthropic.com/news/contextual-retrieval) ⭐ — 官方说明 + benchmark（failed retrieval rate 从 5.7% 降到 1.9%）
- [**Anthropic cookbook**](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) — 端到端 Jupyter notebook、含 prompt 模板

**搭配技巧**：Anthropic 同篇 blog 还建议叠上 **Contextual BM25**（contextual chunk 同时喂 vector + BM25）+ **reranking**——刚好接到下面 §Hybrid Search & Reranking。

### 🎯 Hybrid Search & Reranking — production RAG 的两个 polish

**Mental model**：
- **Hybrid Search** = vector similarity（语义像）+ BM25 / keyword（字面像）并查、用 [RRF (Reciprocal Rank Fusion)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) 之类融合分数。解决纯 vector search“query 跟 chunk 同义但用词不同没捞到”+“人名 / 编号 / 罕用词语义 embedding 太弱”的双重盲点。
- **Reranking** = 第一阶段 retrieve **top-50**（recall 优先、宽松捞）→ 用 **cross-encoder reranker** 重新打分排成 **top-5**（precision 优先、精准筛）。cross-encoder（query + chunk 一起进 model）比 bi-encoder（query / chunk 分开 embed）精准很多、但太慢、所以只用在第二阶段。

**为什么是“必加 polish”**：production RAG 评测几乎一面倒——加 hybrid + reranker 后 recall@5 通常从 70% 上下提到 85-90%、边际成本低、实现成熟。**这是 cost / benefit 最好的两个改动**。

**何时用**：
- production RAG（不是 demo / 练习）
- query 包含人名、产品编号、技术术语、罕见字（纯 vector 容易漏）
- 预算允许每 query 多 100-300ms latency

**何时可以暂缓**：
- 练习阶段 / MVP（先把 vanilla RAG 跑通）
- 预算极紧 / latency 极敏感（reranker 是额外一次 model call）

**代表工具**：
- **Hybrid search**：[Weaviate](https://github.com/weaviate/weaviate)（内置 BM25 + vector + RRF）/ [Qdrant](https://github.com/qdrant/qdrant)（支持 sparse + dense vector）/ pgvector + Postgres FTS
- **Reranker**：[Cohere Rerank API](https://docs.cohere.com/docs/rerank-overview)（商业、最常用）/ [BGE Reranker](https://huggingface.co/BAAI/bge-reranker-large)(开源、HuggingFace、中文表现好) / [Jina Reranker](https://jina.ai/reranker)
- **Framework 内置**：LlamaIndex 的 `SentenceTransformerRerank` / LangChain 的 `ContextualCompressionRetriever`

**Paper / 入门**：
- [**Pinecone — Rerankers and Two-Stage Retrieval**](https://www.pinecone.io/learn/series/rag/rerankers/) — reranker mental model 讲最清楚
- [**Anthropic — Contextual Retrieval**](https://www.anthropic.com/news/contextual-retrieval)（上面已列）— 同时示范 hybrid + reranker、有 benchmark

### 🔄 Query Transformations — HyDE / Multi-Query / RAG Fusion

**Mental model**：vanilla RAG 把 user query 直接 embed 去查——但 query 跟文件**用词 / 风格 / 抽象层级**经常差太多（user 问“我胃痛怎么办”、文件写“上腹部疼痛之鉴别诊断”）。Query transformations 在 retrieve **前**先改写 query、让改写版本更接近文件形式。

**3 个代表技巧**：

| 技巧 | 怎么改写 | 何时用 |
|---|---|---|
| **HyDE**（Hypothetical Document Embeddings）| 先让 LLM 对 query 生成“假想答案”、用答案 embedding 查 | query 跟 chunk 用词风格差距大 |
| **Multi-Query** | LLM 把 query 改写成 N 个变体分别 retrieve、union 去重 | query 太短 / 模糊 / 多义 |
| **RAG Fusion** | Multi-Query + RRF 融合 N 个 retrieval 结果 | 同上、想要更稳定的排名 |

**何时不用**：query 已经是长 + 结构化（RAG over code、user 直接 paste error stack trace）——改写反而引入噪声。

**Paper / 实现**：
- [**HyDE (Gao et al. 2022)**](https://arxiv.org/abs/2212.10496) — 原始 paper
- [**RAG Fusion (Raudaschl 2023)**](https://github.com/Raudaschl/rag-fusion) — Multi-Query + RRF 的 reference 实现
- LangChain 内置 `MultiQueryRetriever` / LlamaIndex `HyDEQueryTransform`

### 🔁 Self-improving RAG — Self-RAG / CRAG / Adaptive RAG（2024 主轴）

**Mental model**：上面所有 RAG 技巧都假设“query 来 → retrieve → generate”是固定 pipeline。Self-improving RAG 把这个 pipeline 变成**有判断能力的 agent loop**——LLM 自己决定要不要 retrieve、判断 retrieve 品質、不够就再查或改 query。**这是 2024 RAG 研究的主轴**。

| 技巧 | 怎么自我修正 | Paper |
|---|---|---|
| **Self-RAG** | 训练 LLM 输出 `[Retrieve]` token 决定要不要查、retrieve 后输出 `[IsRel]/[IsSup]/[IsUse]` 评分每个片段 | [Asai et al. ICLR 2024](https://arxiv.org/abs/2310.11511) |
| **CRAG**（Corrective RAG）| retrieval evaluator 打分；高信心直接用、低信心 fallback 到 web search、中信心做 query 改写 | [Yan et al. 2024](https://arxiv.org/abs/2401.15884) |
| **Adaptive RAG** | classifier 先判 query 复杂性、routing 到“不 retrieve / single-step / multi-step”三种策略 | [Jeong et al. NAACL 2024](https://arxiv.org/abs/2403.14403) |

**为什么这是 2024 主轴**：固定 pipeline 在简单 query（“Tokyo 首都？”不用 retrieve）+ 复杂 query（multi-hop、cross-doc）两个极端都吃亏。让 LLM 自己 routing → 两个极端都解。

**何时用**：production RAG、query 类型分布广（从事实题到推理题都有）、愿意付 1.5-3 倍 latency 换准确度。
**何时不用**：query 类型单一 / 预算 / latency 极紧。

**实现**：LangGraph 有官方 [Self-RAG cookbook](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/) + [CRAG cookbook](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/) + [Adaptive RAG cookbook](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/)、可直接套。

### 🌳 RAPTOR — 阶层式递回 retrieval（ICLR 2024）

**Mental model**：vanilla chunking 把文件切扁平 chunk——但**整本书的主旨不在任何单一 chunk 里**。RAPTOR 把 chunk 递回聚类 + 摘要、建一棵**多层树**：底层 = 原 chunk、中层 = 一群相关 chunk 的摘要、顶层 = 全文摘要。retrieve 时可选整棵树搜索、或选特定抽象层。

**为什么有用**：
- **抽象 query** 捞得到（“这篇 paper 主要结论？”原 chunk 都没这句、但顶层摘要有）
- **细节 query** 也捞得到（底层 chunk 保留）
- 跟 GraphRAG 不同——RAPTOR 是**树**（hierarchical summarization）、GraphRAG 是**图**（entity-relation）

**何时用**：长文件（书、论文、报告）需要不同抽象层 query、知识库 narrative 连贯。
**何时不用**：chunk 之间独立（FAQ）、知识库经常变动（重建树贵）。

**Paper / 实现**：
- [**RAPTOR (Sarthi et al. ICLR 2024)**](https://arxiv.org/abs/2401.18059) ⭐ — 原始 paper
- [**parthsarthi03/raptor**](https://github.com/parthsarthi03/raptor) — 官方 reference 实现
- LlamaIndex 内置 `RAPTOR pack`

### 📊 还有什么 — RAG 进阶技巧纵览（一张表速查）

下面是其他 production / research 常见技巧、按用途分类。**每行 = 名字 + 一句话 + paper**——想深入挑感兴趣的去原 paper。⭐ **年份**标记表示 2025-2026 最新作品。

| 技巧 | 一句话 | 年份 / Paper |
|---|---|---|
| **Sentence-Window Retrieval** | embed 句子、retrieve 后回传 ± N 句 window | LlamaIndex 内置 |
| **Parent-Child / Small-to-Big** | embed 小 chunk、回传 parent chunk | LangChain `ParentDocumentRetriever` |
| **Multi-Vector Retrieval** | 一个 chunk 多个 embedding（摘要 / 原文 / 假想问题）| LangChain `MultiVectorRetriever` |
| **ColBERT / 后互动 retrieval** | token-level 比对而非 pooled embedding | [Khattab & Zaharia 2020](https://arxiv.org/abs/2004.12832)、[RAGatouille](https://github.com/AnswerDotAI/RAGatouille) |
| **LongRAG** | 大 chunk（4k）+ long-context reader、减少 retrieval 次数 | [Jiang et al. 2024](https://arxiv.org/abs/2406.15319) |
| **HippoRAG 2**（正式题名：*From RAG to Memory: Non-Parametric Continual Learning for LLMs*）| 海马回启发、KG + PageRank、跨文件 multi-hop 联想 | [Gutiérrez et al. ICML 2025](https://arxiv.org/abs/2502.14802) ⭐ **2025** |
| **MemoRAG** | memory model 把 KB 压成 latent memory、retrieve 用线索触发 | [Qian et al. 2024](https://arxiv.org/abs/2409.05591) |
| **KAG**（Knowledge-Augmented Generation） | 严格 schema KG + 逻辑推理、金融 / 医疗 / 法律场景 | [Liang et al. 2024 (Ant Group)](https://arxiv.org/abs/2409.13731) |
| **ColPali** | 直接对 PDF 页面图像 embed、绕过 OCR | [Faysse et al. 2024](https://arxiv.org/abs/2407.01449) |
| **MiA-RAG**（Mindscape-Aware）| 先建文件高层摘要 mindscape、用它引导 retrieval 跟回答 | [arXiv:2512.17220](https://arxiv.org/abs/2512.17220)、[Turing Post 12 types](https://www.turingpost.com/p/12ragtypes) ⭐ **2025-12** |
| **QuCo-RAG**（Quality-Controlled） | 用 pretraining 统计判断该不该 retrieve、罕见 entity 触发查、减 hallucination | [arXiv:2512.19134](https://arxiv.org/abs/2512.19134) ⭐ **2025-12** |
| **MegaRAG** | 多模态 KG、长文件抽 entity + relation + 视觉、建层级图 | [arXiv:2512.20626](https://arxiv.org/abs/2512.20626) ⭐ **2025-12** |
| **TV-RAG** | training-free 时间感知 RAG、长影片 + 字幕 + 视觉对齐 | [arXiv:2512.23483](https://arxiv.org/abs/2512.23483) ⭐ **2025-12** |
| **A-RAG**（Agentic RAG）| hierarchical retrieval interfaces、keyword + semantic + chunk read 三 tool | [Ayanami0730/arag](https://github.com/Ayanami0730/arag)、[arXiv:2602.03442](https://arxiv.org/abs/2602.03442) ⭐ **2026** |
| **SoK: Agentic RAG**（survey）| 2026 系统 taxonomy：cardinality / control / autonomy / knowledge repr | [arXiv:2603.07379](https://arxiv.org/abs/2603.07379) ⭐ **2026** |
| **RAGPart / RAGMask** | 对 RAG corpus poisoning 攻击的轻量防御 | [arXiv:2512.24268](https://arxiv.org/abs/2512.24268) ⭐ **2025-12** |
| **Agentic RAG**（一般概念）| retrieval 当 tool、agent 自己决定查几次 / 怎么查 | LlamaIndex / LangGraph、[Stage 7](07-multi-agent-production.md) 主场 |
| **DSPy + RAG** | 不写 prompt、用 program + signature、auto-optimize | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) |

> 💡 **2025-2026 趋势观察**：
> - **memory + KG + retrieval 融合**（HippoRAG 2 / A-MEM / KAG / MegaRAG）—— 从 flat vector store 往“结构化、可演化”走
> - **multimodal RAG**（ColPali / TV-RAG / MegaRAG）—— 从文字到图像 / 影片 / 表格 native retrieval
> - **agentic RAG 变主流**（A-RAG / Self-RAG / CRAG）—— retrieval 从固定 pipeline 变 agent loop 内的 tool
> - **RAG 安全议题浮现**（RAGPart / RAGMask）—— corpus poisoning / prompt injection 进入 production 考量
> - **不再手写 prompt**（DSPy / 自动化 optimize）—— 系统自动 search 出最佳 prompt + retriever 组合

## 🌉 从 RAG 到 Memory — 为什么 RAG 还不够

读到这你已会跑基本 RAG + 知道几个 production 杠杆。但回头看 §Context Engineering 列的 3 个 problem domain——你只解决了 **Retrieval**，**Memory 管理**还没碰。为什么这两件事要分开？

RAG 解决“从**外部知识库** retrieve 相关片段”——但 agent 还需要“**自己** 跨对话 / 跨 session 记事情”。这两件事不是同一个问题：

| 维度 | RAG | Memory |
|---|---|---|
| 内容来源 | **外部**（PDF / 文件 / web / DB）| **agent 自己的对话 / 经验** |
| 写入时机 | ingest 一次性、后续每次 retrieve | 每轮对话、每次 task 都可能写 |
| 内容性质 | 偏静态事实、文件知识 | 偏动态：user preference、过去互动、累积教训 |
| 取代得了 RAG 吗？| — | 取代不了——你不会把每份 PDF 当“memory” |
| 被 RAG 取代吗？| — | 不会——RAG 不会“记住上次 user 说了什么” |

**3 个 RAG 不够用的场景**（刚好对应到 Memory）：

1. **跨 session 记 user preference / persona**——user 上礼拜跟 agent 说“我是纯素”、这礼拜回来、agent 还记得不能推荐肉食。RAG 知识库不会这样自动更新。
2. **agent 过去成败教训累积**（Reflexion 主场）——agent 第一次跑 task 失败、反思“为什么失败”存起来、下次遇类似 task retrieve 进 prompt 避免重蹈覆辙。RAG 知识库不会“记住自己的失败”。
3. **Long-horizon task 中间状态**——agent 跑 100 step task、中间需要保留 working memory 不丢失。RAG 不适合做这种“短期 + 结构化 + 高频写入”的 state。

→ **结论**：RAG 跟 Memory 是**互补**而非取代。Production agent 通常**两个都要**：RAG 接外部知识、Memory 记自己跟 user 的互动。下节 §Memory 设计 教你怎么挑 memory pattern。

## 🧠 Memory 是什么 + 怎么设计

### 短期 vs 长期 memory — 先建立 mental model

| 比较面向 | Short-term memory（短期记忆） | Long-term memory（长期记忆） |
|---|---|---|
| 中文可称 | 短期记忆 | 长期记忆 |
| 来源 | 当前对话内容 | 跨 session 或长期保存的资讯 |
| 持续时间 | 短，通常限于目前 session | 长，可跨 session |
| 技术基础 | 上下文视窗（context window）/ prompt | 记忆存储层（memory store）/ 用户档案 / 向量数据库 |
| 适合记什么 | 任务细节、刚刚说过的内容 | 稳定偏好、长期目标、背景资料 |
| 是否受 context 长度限制 | 会，因为模型一次能看的内容有限 | 较不会，因为可以先存在外部，需要时再取一小段放回来 |
| 生活例子 | 刚刚收到的手机验证码、正在进行对话的上一句话 | 你深化学会的知识、图书馆、知识库、读过的书 |

这里的工作阶段（session）可以理解成一次连续互动，例如同一段聊天、同一次任务，或同一次 agent 执行。

### 3 种设计 pattern（什么时候用什么）⭐ Track B 必看

**不是所有 agent 都需要外部 memory store。Memory 架构选错会花十倍 token 达同样效果。**

这是进练习前要建立的 mental model——下面练习 1-5 跑的是“pattern 3 vector store”，但 production 你可能不需要这么复杂。

| Pattern | 适合场景 | 怎么跑 | 成本 |
|---|---|---|---|
| **1. Naive buffer**<br>（全塞 context） | 短对话、≤ 10 turn、agent 不需要记跨 session 的东西 | 整段 history 每次都送进 prompt | 线性增长、token 烧得快 |
| **2. Summary + recent**<br>（摘要远的 + 保留近 N 轮） | 中长对话、~ 50 turn、想压缩但别丢太多 | 每 N 轮叫 LLM 把旧 history 摘成 1 段；prompt = `summary + last N turns` | 中等、有 LLM 摘要成本 |
| **3. Vector store + retrieval**<br>（外部 store + 每次 semantic search） | 跨 session、知识库场景、agent 要“想起”久远的事 | embed 过去 message → 存 vector DB → 每回合 query 相关片段拼进 prompt | 高（向量计算 + 存储），但 token 用量稳定 |

**怎么选**：

- 对话 chatbot 没跨 session → **pattern 1**
- agent + 长对话、要记今天聊过什么 → **pattern 2**
- agent + 跨 session + 知识库（本 stage 练习场景）→ **pattern 3**
- production 大型 agent → 通常**混用**：近期 pattern 1/2、长期 pattern 3

**📚 深度资源**：
- [**mem0ai/mem0**](https://github.com/mem0ai/mem0) ⭐ — production memory layer，自动分流近期 / 长期 / vector
- [**Letta（前身 MemGPT）**](https://github.com/letta-ai/letta) — OS-style paging memory（把 context window 当 RAM、vector store 当 disk）
- [**LangChain — Memory types**](https://python.langchain.com/docs/concepts/memory/) — framework 内各 memory class 对比表
- [**Anthropic — Memory Tool (memory in agents)**](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Anthropic 官方 tool-based memory 写法

> 💡 **Track B 重点**：你 Stage 7 写 multi-agent 时，每个 agent 都会有“自己的 memory”+“shared memory”双层——需要的 pattern 通常是 **2 + 3 混用**。先在本 stage 把 3 种 pattern 跑透，到 Stage 7 才不会被 multi-agent memory 设计卡住。

### 进阶：CoALA framework — agent memory 的 4 层 taxonomy

[**Sumers et al. 2023 — Cognitive Architectures for Language Agents**](https://arxiv.org/abs/2309.02427) 把 agent memory 拆成 4 种、是现在最常用的 mental model：

| 类型 | 存什么 | 对应例子 |
|---|---|---|
| **Working memory** | 当前 task 上下文 | LLM context window 本身 |
| **Episodic memory** | 过去 task 的具体经验 | Reflexion 反思记录、past trajectories |
| **Semantic memory** | 抽象事实 / 知识 | RAG 知识库、user profile、preference |
| **Procedural memory** | 怎么做事的程序 / skill | tool definitions、[Skills（Stage 5.3）](05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層) |

→ **为什么有用**：上面 3 种 pattern（buffer / summary / vector）都只在处理 working + episodic。Production agent 4 层都要设计——CoALA 是检查表，看看你的 agent 哪一层缺了。

### 进阶：Generative Agents — 三分数打分（经典案例）

[**Park et al. 2023 — Generative Agents: Smallville**](https://arxiv.org/abs/2304.03442) 的小镇模拟有 25 个 NPC agent、每个都有自己的 memory stream。retrieve 时用三个分数加权：

- **Importance**：LLM 自己帮每个 memory 打 1-10 重要性分（吃饭 = 2 分、分手 = 9 分）
- **Recency**：时间衰减（exponential decay）
- **Relevance**：跟当前 query 的 embedding 相似度

最终分 = `α·importance + β·recency + γ·relevance`、排前 k retrieve。**这是 2024-2025 production memory layer（mem0 / Letta）的概念骨架**。

### 2024-2026 最新 Memory 作品 — 纵览

⭐ **年份**标记 = 2025-2026 最新作品。

| 技巧 | 一句话 | 年份 / Paper |
|---|---|---|
| **Anthropic Memory Tool** | Claude 官方 tool-based memory、API 直接 call、file-based | [Anthropic Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool) 2024 |
| **A-MEM**（Agentic Memory）| Zettelkasten-inspired、memory 之间自动建 link、会演化 | [Xu et al. 2025](https://arxiv.org/abs/2502.12110) ⭐ **2025** |
| **HippoRAG 2** | 海马回启发、KG + Personalized PageRank、跨文件 multi-hop | [Gutiérrez et al. 2025](https://arxiv.org/abs/2502.14802) ⭐ **2025** |
| **MemGPT → Letta GA** | OS-paging memory、working / archival 双层、long session 强项 | [Packer et al. 2023](https://arxiv.org/abs/2310.08560) → Letta 2024 GA |
| **MemoryBank** | Ebbinghaus 遗忘曲线、被存取的 memory 强化、没用的衰减 | [Zhong et al. 2023](https://arxiv.org/abs/2305.10250) |
| **MemoryLLM** | self-updatable memory parameters 内置在 model（在权重而非 context）| [Wang et al. 2024](https://arxiv.org/abs/2402.04624) |
| **mem0**（已在上面列） | production memory layer、auto fact extraction + forgetting | [mem0ai/mem0](https://github.com/mem0ai/mem0) 2024 |
| **Memory in the Age of AI Agents**（survey）| 系统 survey、3 维 taxonomy（temporal scope / substrate / control policy）+ benchmark 汇总 | [Hu et al. arXiv:2512.13564](https://arxiv.org/abs/2512.13564) ⭐ **2025-12** |
| **Memory for Autonomous LLM Agents**（survey）| 把 agent memory 形式化成 write-manage-read loop、跨 2022-2026 整理 | [arXiv:2603.07670](https://arxiv.org/abs/2603.07670) ⭐ **2026** |
| **From Storage to Experience**（survey）| 演化框架：Storage → Reflection → Experience 三阶段、分析 3 个演化驱动力 | [arXiv:2605.06716](https://arxiv.org/abs/2605.06716) ⭐ **2026** |
| **ScrapMem** | bio-inspired on-device memory、"**Optical Forgetting**" 把老 memory 解析度渐降 | [arXiv:2605.03804](https://arxiv.org/abs/2605.03804) ⭐ **2026-05** |
| **Memory Security survey** | long-term memory 被 cross-session poisoning / 未授权存取 / 组织内传播风险 | [arXiv:2604.16548](https://arxiv.org/abs/2604.16548) ⭐ **2026** |

> 💡 **2025-2026 趋势观察**：
> - **结构化、可演化、可联想**（A-MEM / HippoRAG 2）—— 从 flat vector store 往人脑启发架构走
> - **2026 是 memory 大爆发年**——5 个重磅 survey + ScrapMem on-device memory + memory security 议题浮现
> - **memory automation / multimodal / multi-agent memory** 变新前沿（见 [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) survey 列的 emerging frontiers）
> - **memory security 变独立子领域**——agent 跑久了、memory 会被攻击、需要保护（Stage 7 §安全会接到）
>
> 如果你的 agent 跑很久（以周 / 月为单位）、上面两个 2026 survey 必读。

## 🧩 Chunking 细节（技术深入）

好的 chunking 可以让 LLM 在有限 context 内，用更精确、完整的资讯生成回答。它不是把文字平均切开。

切法取决于应用场景与文件内容。它会决定 retriever 看见的最小语义单位。

一个好 chunk 要同时做到两件事：**够完整**，让模型看得懂上下文；**够聚焦**，让检索不带太多噪声。chunk 太小会失去上下文，chunk 太大会让相似度搜索变钝。

**常见策略**：

- **固定长度（Fixed-Length）**：照字符数或 token 数切。优点是简单稳定；缺点是一板一眼，容易切断段落、句子或表格。
- **滑动视窗（Sliding Window）**：每个 chunk 之间保留重叠区块（overlap）。优点是比较不会在边界掉信息；缺点是索引量会变大。
- **递回切割（Recursive）**：先尝试保留段落，如果长度还是不适合，再退到句子、字词等更小单位。通常是入门 RAG 的好基准。
- **语义切割（Semantic Chunking）**：依 embedding 或语义变化切，也就是当前区块与前一个区块的语义相似度出现差异。适合长文件，但成本与复杂度较高。
- **混合策略（Hybrid）**：依照应用场景，思考不同文件结构该怎么混搭切法。例如，一篇论文可能要保留章节、表格、公式与引用脉络。

![Chunking 策略流程](../resources/diagrams/chunking-strategies.jpg)

第一次做 RAG 时，不要一开始就追求复杂切法。LangChain 文件建议多数情境先从 `RecursiveCharacterTextSplitter` 开始。

先跑出基准版本，再用后续 retrieval 结果决定要不要换策略。

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "这是一个很长的文件内容...（此处省略一千字）..."

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

chunks = splitter.split_text(text)
print(f"共切成 {len(chunks)} 个 chunk")
print(chunks[0])
```

**直觉判断 chunking 好不好**，可以先看两件事：

- 回答缺漏信息，或有头无尾：通常是 chunk 太小，或 overlap 不够。
- 回答包含正确信息，但混入无关内容：通常是 chunk 太大，或 top-k 捞太多。

**进阶思考**：

- chunking 不是一次设定好就结束，要配合真实 query 与失败案例反复调整。
- chunk size、overlap、top-k、reranker 会互相影响，不要只单看其中一个参数。
- 想想看，如果今天要 RAG 的数据有含图片的 PDF、会议字幕文件，要如何切割比较好？
- chunking 的进阶变形（Sentence-Window / Parent-Child / Multi-Vector）见 §进阶 RAG 技巧纵览表。

## 🪞 进阶：带持久记忆的 Reflexion 完整版 ⭐ Track B 选读

> **本节是 concept + routing、不是练习**。延续 [Stage 3 §反思](03-tool-use-and-hello-agent.md#-反思reflexion--self-refine-概念--路由) 的基本版（single-session Actor / Critic loop），讲为什么有些反思**需要**持久记忆——这版本才真正属于 Stage 6 主题。

**Reflexion 完整版跟 Self-Refine 差在哪**：

| 版本 | 跨轮保留什么 | 跨 session 保留什么 | 需要 memory pattern |
|---|---|---|---|
| **Self-Refine**（Madaan 2023） | 上一轮的 answer + critic feedback | ❌ 不保留 | 不需（pattern 1 buffer 即可） |
| **完整 Reflexion**（Shinn 2023） | 同上 | ✅ 把过去 trial 的“反思摘要”存进 episodic memory，下次遇到类似 task 时 retrieve 进 prompt 当教训 | **需要**（pattern 3 vector store 或 pattern 2 summary） |

**为什么这个版本要 memory**：Reflexion paper 的 verbal reinforcement learning 是“agent 跨 trial 累积教训”——agent 尝试 task → 失败 → 反思“为什么失败”存起来 → 下次遇到类似 task 时把过去反思 retrieve 进 prompt，避免重蹈覆辙。这就需要 **persistent episodic memory**，跟本 stage 上面讲的 3 种 memory pattern 直接接上。

**典型架构**（持久记忆完整版）：

```
Actor → Critic → Actor    （单回合 loop、跟 Stage 3 §反思 一致）
       ↑──────────┘
            ↓
   Reflection summary
            ↓
   Episodic memory store
   （vector / summary pattern、见上面 §Memory 设计 pattern 3）
            ↓
   next task → retrieve relevant past reflections
            → prepend to Actor's prompt
            （跨 trial 累积教训、不重蹈覆辙）
```

→ **跟 Stage 3 §反思的差别**：Stage 3 是 **single-session in-context** loop（没外部 store）、本节是 **persistent episodic memory store + retrieve**（跨 trial 累积）。

### 📚 想动手 / 想深入

**Paper**：
- [**Reflexion (Shinn et al. 2023)**](https://arxiv.org/abs/2303.11366) ⭐ — **完整版** paper，Algorithm 1 写出 memory buffer 怎么用
- [**Self-Refine (Madaan et al. 2023)**](https://arxiv.org/abs/2303.17651) — 对照 baseline，没 episodic memory 的版本

**Reference 实现**：
- [**noahshinn/reflexion**](https://github.com/noahshinn/reflexion) — paper 第一作者的 reference 实现（含 episodic memory 完整流程）
- [**LangChain — Reflexion**](https://langchain-ai.github.io/langgraph/tutorials/reflexion/reflexion/) — LangGraph 版本，跟本 stage 练习 4 RAG pipeline 直接接得起来
- [**mem0**](https://github.com/mem0ai/mem0)（已在上面列）+ [**Letta**](https://github.com/letta-ai/letta)（已在上面列）— production memory layer，可以直接当 Reflexion 的 episodic store

> 💡 **跟 Stage 3 §反思的分工**：
> - 想理解“反思 loop 怎么运作、单次怎么跑”→ Stage 3 §反思
> - 想理解“反思怎么跨 session 累积、agent 怎么从过去学教训”→ 本节
> - 想看 production agent 内怎么用反思（Cursor / Claude Code）→ [Stage 5 §5.6 Harness Internals](05-claude-code-ecosystem.md#56--claude-code-source-解剖reference-harness-implementation-track-b-必看)

## 🤔 进阶 Reasoning / Reflection — 2024-2026 思潮 ⭐ 两个 track 都看

Reflexion 是 **prompt-based reflection**——LLM 在 inference 时自己改自己。2024-2025 出现了**第二条路**：**训练时就把 reflection 练进 model**（OpenAI **o1** / DeepSeek **R1**）。两条路你都该知道。

### Path 1：Prompt-based reflection / reasoning（传统做法）

| 技巧 | 核心想法 | Paper |
|---|---|---|
| **Self-Consistency** | sample N 条推理、多数决 — **最简单 + 最常用** | [Wang et al. 2022](https://arxiv.org/abs/2203.11171) |
| **Tree of Thoughts (ToT)** | reasoning 变树、可分叉可回溯、适合 puzzle / planning | [Yao et al. 2023](https://arxiv.org/abs/2305.10601) |
| **Graph of Thoughts (GoT)** | 不只树、可任意合并分支 | [Besta et al. 2023](https://arxiv.org/abs/2308.09687) |
| **Chain-of-Verification (CoVe)** | 生答案 → 对自己提验证题 → 改答案 | [Dhuliawala et al. 2023](https://arxiv.org/abs/2309.11495) |
| **CRITIC** | tool-augmented self-critique（用 search / calculator 验）| [Gou et al. 2023](https://arxiv.org/abs/2305.11738) |
| **Self-Discover** | agent 先“发现”该用什么 reasoning structure 再执行 | [Zhou et al. ICML 2024](https://arxiv.org/abs/2402.03620) ⭐ 2024 |
| **Self-Refine / Reflexion** | 已在上面 / Stage 3 讲 | Stage 3 §反思、本 stage §Reflexion |

### Path 2：Trained-in reasoning / reflection（2024-2026 大转折）

OpenAI **o1**（2024-09）开启、DeepSeek **R1**（2025-01）开源化、**DeepSeek-V4-Pro**（2026-04 preview、agent-focused 开源 reasoning）+ Claude Opus 4.7（2026-04）+ GPT-5.5（2026-04）+ Gemini 3.1 Pro（2026-02）为当前 frontier——把“step-by-step thinking + 自我纠错”**训练进 model 权重**、inference 时自动展开长 reasoning chain（thinking tokens）。**这是 2024-2026 LLM 最大典范转移**、目前所有 frontier model 都走这路。下表只列**当前（2026-05）frontier**——历史前身（o1 / R1 / Sonnet 4.5 / Gemini 2.5）省略、想看 lineage 看每家发布日列。

| Model | 来源 / 发布 | 特色 | 链接 |
|---|---|---|---|
| **GPT-5.5** | OpenAI 2026-04（前身：o1 2024-09 → o3 → GPT-5 2025-08 → 5.4 2026-03）| 闭源、reasoning + chat 合并、Thinking budget API、agent 能力强化 | [OpenAI](https://openai.com/) |
| **Claude Opus 4.7** | Anthropic 2026（前身：Sonnet 4.5 / Opus 4.5）| 闭源、可控 thinking budget（API 参数）、**SWE-bench / Terminal-bench 领先** | [Anthropic extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) |
| **Gemini 3.1 Pro** | Google 2026-02（前身：Gemini 2.5 Thinking 2025、Gemini 3 2025-11）| 闭源、可看 thinking trace、**GPQA Diamond 94.3%**、价格 / 速度 / multimodal 领先 | [Gemini API](https://ai.google.dev/gemini-api/docs/thinking) |
| **DeepSeek-V4 / V4-Pro / V4-Flash** | DeepSeek 2026-04 preview（前身：R1 2025-01 → V3.1）| 开源 **MIT license**、agent-focused 训练、推理 + 工具使用 + 知识处理整合、R 系列 reasoning 已并入主线 | [HF DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)、[R1 paper（方法 baseline）](https://arxiv.org/abs/2501.12948)、[CNBC report](https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html) |
| **QwQ-32B / QvQ-72B** | Alibaba Qwen 2024-11 ~ 2026 | 开源 **Apache 2.0**、32B 在小尺寸 reasoning 仍是首选、QvQ 是视觉版本 | [QwQ blog](https://qwenlm.github.io/blog/qwq-32b-preview/) |

### 两条路怎么选

| 你情况 | 建议 |
|---|---|
| 用一般 chat model base、想加 reasoning | Path 1（prompt-based）—— ToT / Self-Consistency / CoVe |
| 预算 / latency 允许、要最强 reasoning | Path 2 —— **GPT-5.5 / Opus 4.7 / Gemini 3.1 Pro / V4-Pro** 任挑一个 |
| 想自己 fine-tune reasoning model | Path 2 —— 读 R1 paper（方法 baseline）、从 R1-Distill / V4 开源权重起步 |
| 想 on-device / 预算极紧 | **QwQ-32B**（Apache 2.0）或 R 系列 distill |
| Multi-agent debate / critic 场景 | Path 1（CRITIC / debate）+ [Stage 7 §multi-agent](07-multi-agent-production.md) |

> 💡 **2025-2026 观察**：
> - reasoning model 把 Reflexion 那套吞进权重——但 **prompt-based reflection 没被取代**：agent loop（控制反思时机 / 内容）+ multi-agent debate 还是必须的
> - **2026 开源逼近闭源**——DeepSeek-V4-Pro（2026-04 preview、MIT license）把 R1 reasoning 并入主线、agent-focused 训练、跟 GPT-5.5 / Gemini 3.1 Pro 差距持续缩小
> - **agent capability 变主诉求**——V4 / Opus 4.7 都把 agent-as-product（SWE-bench / Terminal-bench / tool use）当 headline benchmark、单纯 reasoning 已经不够卖
> - 两条路会长期共存、production agent 两个都用

## 🛠 动手练习（基础 illustrative 练习）

### 练习 1：Embeddings
把 100 个句子做 embedding，找出某个 query 的最近邻。理解 vector 之间的距离意义。

### 练习 2：Vector DB
把 embedding 存进 Chroma，做语义 query。比对“跟 keyword search 差在哪”。

### 练习 3：Chunking 对照
拿同一份文件做三种切法：固定长度、段落切法、heading-aware 切法。用 5 个真实问题比较 top-k 结果，记录哪种切法比较容易捞到正确上下文。

### 练习 4：完整 RAG 流水线
把一份 PDF 切块 → embed → 取 top-k → 生成回答。这是大多数 RAG 应用的基本骨架。

### 练习 5：Long-term Memory
让 agent 在多轮对话之间记得事情。可以用 `mem0` 或自己用 vector store 接。

## 🎯 常用 Memory / RAG 工具推荐（按用途分类）

不知道从哪里开始挑工具？下面是 2025 后段业界常用搭配——**挑入口看“场景”、想深入点链接看 repo**：

| 场景 | 推荐工具 | 为什么 |
|---|---|---|
| **第一次跑 RAG**（最快上手）| [Chroma](https://github.com/chroma-core/chroma) + [LlamaIndex](https://github.com/run-llama/llama_index) | local-first、零 ops、quickstart 友善。Stage 6 练习默认 |
| **agent 长期记忆**（个人助理 / chatbot）| [mem0](https://github.com/mem0ai/mem0) | 自动 fact extraction + forgetting + namespace、production memory layer |
| **跨 session、persona-stable agent**（therapist / tutor / long-term assistant）| [Letta](https://github.com/letta-ai/letta) | OS-style paging memory、working + archival 双层、long session 强项 |
| **production scale RAG**（百万 doc）| [Qdrant](https://github.com/qdrant/qdrant) + LlamaIndex | Rust 写的 vector DB、scale 大时比 Chroma 快 |
| **已有 Postgres 的环境** | [pgvector](https://github.com/pgvector/pgvector) | Postgres 扩充、SQL + vector 一起、运维最简 |
| **企业级 RAG + Web UI** | [RAGFlow](https://github.com/infiniflow/ragflow) | document parsing 强（含 OCR / 表格 / layout）、企业场景、含 Web UI |
| **中文 RAG 范本** | [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | 中文圈最完整、本地 LLM 整合好（ChatGLM / Qwen / Llama）|
| **进阶：Contextual Retrieval** | [Anthropic cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | Claude 搭配 prompt caching 的 contextual chunking（**详见上方 §进阶 RAG 技巧**） |
| **进阶：knowledge graph 推理** | [LightRAG](https://github.com/HKUDS/LightRAG) / [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | knowledge graph + RAG、entity-relation 推理（**详见上方 §进阶 RAG 技巧**） |
| **跨主题 tutorial 集** | [ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | RAG + agent 教学 collection、Jupyter notebook 形式 |

**建议入手顺序**：
1. 第一个必装：**Chroma + LlamaIndex**（跑 Stage 6 练习）
2. agent 要记事：加 **mem0**（最简单的 memory layer）
3. 开始 production-scale：换成 **Qdrant** 或 **pgvector**
4. 想升级到进阶 RAG：看上方 §进阶 RAG 技巧 三个 subsection

## 🎯 精选 Projects（范本 / spec / 范例 collection）

按用途分类、13 个项目一张表搞定。**挑入口看“适合谁”、想深入点链接看 repo**。

| 分类 | Project | ⭐ | 适合谁 | 为什么推荐 / 备注 |
|---|---|---|---|---|
| **RAG framework**<br>（完整流水线） | [LlamaIndex](https://github.com/run-llama/llama_index) | ⭐⭐⭐⭐⭐ | 以文件为主的应用 | 以 RAG 为核心、document loader / chunking / retrieval / query engine 一条龙。★ 49k+ |
| | [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | ⭐⭐⭐⭐⭐ | 要把 RAG 真的 ship 给非开发者用 | production 等级 RAG engine、深度文件理解（layout / 表格 / OCR）+ hybrid retrieval + agent loop + Web UI。★ 79k+、Apache-2.0 |
| | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | ⭐⭐⭐⭐ | 想看研究级 graph + long-context memory 方法 | graph + vector hybrid retrieval + summarization-based memory、EMNLP 2025 paper-backed。★ 34k+、MIT。研究风格 codebase |
| **Vector DB**<br>（local-first） | [Chroma](https://github.com/chroma-core/chroma) | ⭐⭐⭐⭐⭐ | 练习 2 / 4、最容易上手的 vector DB | 开源 embedding 数据库、本机跑、in-memory / SQLite 后端、零 ops。★ 27k+、Apache-2.0。**安装**：`pip install chromadb` |
| **Vector DB**<br>（production scale） | [Qdrant](https://github.com/qdrant/qdrant) | ⭐⭐⭐⭐⭐ | Chroma 跟不上时、需要 production scale | Rust 写的 vector DB、有云端版跟自架版。★ 31k+ |
| **Vector DB**<br>（hybrid） | [Weaviate](https://github.com/weaviate/weaviate) | ⭐⭐⭐⭐ | production 部署 + schema 约束 | 内置模块（text2vec / generative / classification）、schema 驱动、内置 BM25 + vector hybrid。★ 16k+ |
| **Vector DB**<br>（已有 Postgres） | [pgvector](https://github.com/pgvector/pgvector) | ⭐⭐⭐⭐ | 原本就在用 Postgres 的团队 | Postgres 扩充、SQL + vector 同一个 DB、运维最简。★ 21k+ |
| **Memory framework**<br>（auto fact extraction） | [mem0ai/mem0](https://github.com/mem0ai/mem0) | ⭐⭐⭐⭐⭐ | 个人助理 / chatbot 需要 user-level memory | 自我精炼 memory 层、跨 session 存储事实。★ 54k+ |
| **Memory framework**<br>（OS-paging） | [Letta（前身 MemGPT）](https://github.com/letta-ai/letta) | ⭐⭐⭐⭐ | context 要跑很久的 agent（以月为单位） | 阶层式 memory（working / archival）、OS-paging 概念。★ 22k+ |
| **Memory（in-framework）** | [LangChain — Memory](https://python.langchain.com/docs/concepts/memory/) | ⭐⭐⭐ | 已用 LangChain | 4 种 memory 抽象（buffer / summary / vectorstore-backed / entity）|
| **进阶 RAG 技巧** | [Anthropic — Contextual Retrieval cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) | ⭐⭐⭐⭐⭐ | 跑完基本 RAG 想升级 | Claude 搭配 prompt caching 的 contextual chunking、含完整端到端范例 |
| **中文 RAG 样板** | [chatchat-space/Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | ⭐⭐⭐⭐ | 中文知识库 / RAG 应用 | 中文社群最广泛使用、可离线部署、中文预设好、支持 ChatGLM / Qwen / Llama / Ollama。★ 38k+、Apache-2.0。⚠️ 最后更新 2025-11（边缘）|
| **教材合集** | [patchy631/ai-engineering-hub](https://github.com/patchy631/ai-engineering-hub) | ⭐⭐⭐⭐ | 想看“同概念在不同情境怎么实现” | 主题式 LLM / RAG / agent tutorial 集、Jupyter notebook、跨多个 stage 都用得上。★ 34k+、MIT |


## ✅ 进入 Stage 7 前的自我检查

你能不能：
- [ ] 写一条 50 行的 RAG 流水线（load → chunk → embed → store → query → answer）
- [ ] 解释为什么天真的切块在长文件上会失败
- [ ] 针对 API 文件、PDF、表格设计不同的 chunking 策略
- [ ] 在某个规模下，能在 Chroma、Qdrant、pgvector 之间做出选择
- [ ] 区分“给 agent memory”跟“用 RAG”这两件事
- [ ] 解释 RAG 跟 Memory 各补哪段（从上面 §从 RAG 到 Memory 表）

如果都可以 → 前往 [Stage 7 — Multi-Agent · 进阶应用](07-multi-agent-production.md)。
