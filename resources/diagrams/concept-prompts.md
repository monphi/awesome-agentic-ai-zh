# Stage 7.5 概念圖 — ChatGPT image-gen prompts（3 圖 × 3 語言）

> 把下面的 prompt 整段複製貼到 ChatGPT（含 DALL-E / 原生 image-gen model），生成對應的概念圖 PNG。

> 📋 **v2 更新**：加上 icon 描述（每個元素附 emoji icon、視覺辨識度更高）+ 中英文 bilingual 術語（中文 prompt 用「中文 (English)」格式介紹專有詞、英文 prompt 純英文）+ 明確「no source attribution」規則。

> 📂 **批次上傳檔案**：對應的 9 個 `.txt` 在 `C:\Users\wenyu\Downloads\awesome-agentic-ai-zh-images\stage7.5\`、可直接拖進 ChatGPT。

---

## 圖 A — 12 進階概念 cluster map

### zh-TW prompt

```
生成一張清晰的技術示意圖、主題：「12 個進階 Agentic AI 概念分類地圖 (12 Advanced Agentic AI Concepts — Cluster Map)」。

整體設計：簡潔技術 blog 風（參考 Anthropic engineering blog），2D 表格 / grid 結構、配合視覺圖示 (icon) 讓內容好讀。

橫軸（X-axis、由左至右）= 4 個 agent stack 層次、每個加上一個 icon：
  1. Service 層 (Service layer) — 圖示：🎼
  2. Repo 層 (Repo layer) — 圖示：💾
  3. Config 層 (Config layer) — 圖示：⚙️
  4. Types 層 (Types layer) — 圖示：📋

縱軸（Y-axis、由上至下）= 4 個問題類型、每個加 icon + 一句白話副標：
  1. 編排類 (Orchestration) — 🎭、副標「agent 怎麼分工協作 (how agents coordinate)」
  2. 反思類 (Reflection) — 🪞、副標「agent 怎麼自我修正 (how agents self-correct)」
  3. 治理類 (Governance) — 🛡️、副標「agent 自主權邊界 (autonomy boundaries)」
  4. 韌性類 (Resilience) — 💪、副標「agent 預防失敗 (failure prevention)」

在對應格子放概念名稱 + 編號 + 小 icon：
  - Service × 編排：1. Work Boundary (跨層 *) 🌐 / 3. Speculative Parallel ⚡ / 10. Self-organizing Teams 🐝
  - Service × 反思：5. Plan-Act-Reflect 🔁 / 4. Agent-as-Judge ⚖️
  - Service × 治理：6. Hierarchical Task Decomposition 🪜
  - Types × 編排：2. Contract Hand-offs 🤝
  - Types × 反思：11. Spec-driven Development 📐
  - Config × 治理：7. Autonomy Gradients 🎚️ / 12. Graceful Degradation 🛡️↓
  - Config × 韌性：8. Cost-aware Budget Gates 💰 / 9. Failure Injection 💉
  - Repo × 反思 格子註記：「memory 由 Stage 6 提供 (memory provided by Stage 6)」、不放概念名稱

視覺風格：
- Sans-serif 字體（如 Inter）、字夠大易讀
- 配色：2-3 色（hover blue 主色 + neutral grey + 強調 orange）
- Icon 明顯但不擾人、能視覺辨識
- 比例 16:9 適合 README banner
- 留白多、版面不要塞滿

絕對不要 (DO NOT)：
- 不要任何「Source: ...」「by ...」「Credits: ...」「Reference: ...」標籤
- 不要 Anthropic / OpenAI / Cognition 等 vendor logo 或文字
- 不要任何來源 / 出處 / 引用 attribution
- 不要 3D 透視、漸層陰影、卡通插圖
- 不要 emoji 以外的裝飾性 illustration
```

### zh-Hans prompt

```
生成一张清晰的技术示意图、主题：「12 个进阶 Agentic AI 概念分类地图 (12 Advanced Agentic AI Concepts — Cluster Map)」。

整体设计：简洁技术 blog 风（参考 Anthropic engineering blog），2D 表格 / grid 结构、配合视觉图示 (icon) 让内容好读。

横轴（X-axis、由左至右）= 4 个 agent stack 层次、每个加上一个 icon：
  1. Service 层 (Service layer) — 图示：🎼
  2. Repo 层 (Repo layer) — 图示：💾
  3. Config 层 (Config layer) — 图示：⚙️
  4. Types 层 (Types layer) — 图示：📋

纵轴（Y-axis、由上至下）= 4 个问题类型、每个加 icon + 一句白话副标：
  1. 编排类 (Orchestration) — 🎭、副标「agent 怎么分工协作 (how agents coordinate)」
  2. 反思类 (Reflection) — 🪞、副标「agent 怎么自我修正 (how agents self-correct)」
  3. 治理类 (Governance) — 🛡️、副标「agent 自主权边界 (autonomy boundaries)」
  4. 韧性类 (Resilience) — 💪、副标「agent 预防失败 (failure prevention)」

在对应格子放概念名称 + 编号 + 小 icon：
  - Service × 编排：1. Work Boundary (跨层 *) 🌐 / 3. Speculative Parallel ⚡ / 10. Self-organizing Teams 🐝
  - Service × 反思：5. Plan-Act-Reflect 🔁 / 4. Agent-as-Judge ⚖️
  - Service × 治理：6. Hierarchical Task Decomposition 🪜
  - Types × 编排：2. Contract Hand-offs 🤝
  - Types × 反思：11. Spec-driven Development 📐
  - Config × 治理：7. Autonomy Gradients 🎚️ / 12. Graceful Degradation 🛡️↓
  - Config × 韧性：8. Cost-aware Budget Gates 💰 / 9. Failure Injection 💉
  - Repo × 反思 格子注记：「memory 由 Stage 6 提供 (memory provided by Stage 6)」、不放概念名称

视觉风格：
- Sans-serif 字体（如 Inter）、字够大易读
- 配色：2-3 色（hover blue 主色 + neutral grey + 强调 orange）
- Icon 明显但不扰人、能视觉辨识
- 比例 16:9 适合 README banner
- 留白多、版面不要塞满

绝对不要 (DO NOT)：
- 不要任何「Source: ...」「by ...」「Credits: ...」「Reference: ...」标签
- 不要 Anthropic / OpenAI / Cognition 等 vendor logo 或文字
- 不要任何来源 / 出处 / 引用 attribution
- 不要 3D 透视、渐层阴影、卡通插图
- 不要 emoji 以外的装饰性 illustration
```

### en prompt

```
Generate a clean technical diagram titled "12 Advanced Agentic AI Concepts — Cluster Map".

Overall design: clean tech blog aesthetic (reference Anthropic engineering blog), 2D table/grid layout with visual icons to aid scanning.

X-axis (left to right) = 4 agent stack layers, each with an icon:
  1. Service layer — icon: 🎼
  2. Repo layer — icon: 💾
  3. Config layer — icon: ⚙️
  4. Types layer — icon: 📋

Y-axis (top to bottom) = 4 problem categories, each with an icon + plain-language subtitle:
  1. Orchestration — 🎭, subtitle "how agents coordinate"
  2. Reflection — 🪞, subtitle "how agents self-correct"
  3. Governance — 🛡️, subtitle "autonomy boundaries"
  4. Resilience — 💪, subtitle "failure prevention"

Place concept names + numbers + small icons in the matching cells:
  - Service × Orchestration: 1. Work Boundary (cross-layer *) 🌐 / 3. Speculative Parallel ⚡ / 10. Self-organizing Teams 🐝
  - Service × Reflection: 5. Plan-Act-Reflect 🔁 / 4. Agent-as-Judge ⚖️
  - Service × Governance: 6. Hierarchical Task Decomposition 🪜
  - Types × Orchestration: 2. Contract Hand-offs 🤝
  - Types × Reflection: 11. Spec-driven Development 📐
  - Config × Governance: 7. Autonomy Gradients 🎚️ / 12. Graceful Degradation 🛡️↓
  - Config × Resilience: 8. Cost-aware Budget Gates 💰 / 9. Failure Injection 💉
  - Repo × Reflection cell annotation: "memory provided by Stage 6" (no concept name)

Visual style:
- Sans-serif typography (e.g., Inter), font size large enough to read
- Color palette: 2-3 colors (primary hover blue + neutral grey + accent orange)
- Icons clear but not intrusive, visually identifiable
- 16:9 aspect ratio, suitable as a README banner
- Generous whitespace, do not pack the layout

DO NOT:
- No "Source: ..." / "by ..." / "Credits: ..." / "Reference: ..." labels
- No vendor logos or names (Anthropic / OpenAI / Cognition / etc.)
- No attribution or citation of any kind
- No 3D perspective, gradient shadows, or cartoon illustration
- No decorative illustration beyond the listed emoji icons
```

---

## 圖 B — Reading decision tree

### zh-TW prompt

```
生成一張清晰的技術示意圖、主題：「Agentic AI 進階閱讀決策樹 (Advanced Reading Decision Tree)」。

整體設計：top-down 決策樹、配合視覺圖示讓 5 條分支好辨識。

頂端標題（icon 🤔）：「你現在卡什麼問題？ (What problem are you stuck on right now?)」

往下分出 5 條分支、橫向排列、每條獨特顏色 + icon：

1. 紅色分支 🌱
   問題：「不知道 agent 怎麼開始 (Don't know how to start with agents)」
   ↓
   📖 Anthropic Building Effective Agents (~20 min)

2. 綠色分支 🤝
   問題：「multi-agent 要不要用、怎麼開 (Multi-agent: when and how)」
   ↓
   📖 Cognition Don't Build Multi-Agents (~10 min)

3. 黃色分支 🧠
   問題：「context 沒效率 (Context inefficient)」
   ↓
   📖 Anthropic Skills + CLAUDE.md memory docs (~15 min)

4. 藍色分支 🧪
   問題：「eval 怎麼寫 / 自動驗證 (How to write evals / auto-verify)」
   ↓
   📖 Hamel Husain Evals blog (~15 min)

5. 紫色分支 🚀
   問題：「想跟上 frontier 現況 (Catch up on frontier)」
   ↓
   📖 LangGraph Plan-Execute / Voyager / Self-Discover paper (~30 min/篇)

底部小字：「規則 (Rule)：每分支最多挑 2 篇深讀、不要 broad-scan (pick at most 2 per branch)」

視覺風格：
- 方框 + 連線、不要過多圓角
- 文章名稱用粗體、加 📖 icon
- Sans-serif、比例 4:3 或正方形
- 5 條分支顏色明顯區分
- 每條分支頂端的 icon 視覺辨識度高（不只是 emoji 文字）

絕對不要 (DO NOT)：
- 不要任何「Source: ...」「by Anthropic / Cognition AI / Hamel Husain / LangGraph」等 attribution
- 不要 vendor logo / 公司商標
- 不要 mind-map 那種繽紛樹枝樹葉風格
- 不要 emoji 之外的卡通插圖
- 不要 3D 渲染、漸層陰影
```

### zh-Hans prompt

```
生成一张清晰的技术示意图、主题：「Agentic AI 进阶阅读决策树 (Advanced Reading Decision Tree)」。

整体设计：top-down 决策树、配合视觉图示让 5 条分支好辨识。

顶端标题（icon 🤔）：「你现在卡什么问题？ (What problem are you stuck on right now?)」

往下分出 5 条分支、横向排列、每条独特颜色 + icon：

1. 红色分支 🌱
   问题：「不知道 agent 怎么开始 (Don't know how to start with agents)」
   ↓
   📖 Anthropic Building Effective Agents (~20 min)

2. 绿色分支 🤝
   问题：「multi-agent 要不要用、怎么开 (Multi-agent: when and how)」
   ↓
   📖 Cognition Don't Build Multi-Agents (~10 min)

3. 黄色分支 🧠
   问题：「context 没效率 (Context inefficient)」
   ↓
   📖 Anthropic Skills + CLAUDE.md memory docs (~15 min)

4. 蓝色分支 🧪
   问题：「eval 怎么写 / 自动验证 (How to write evals / auto-verify)」
   ↓
   📖 Hamel Husain Evals blog (~15 min)

5. 紫色分支 🚀
   问题：「想跟上 frontier 现况 (Catch up on frontier)」
   ↓
   📖 LangGraph Plan-Execute / Voyager / Self-Discover paper (~30 min/篇)

底部小字：「规则 (Rule)：每分支最多挑 2 篇深读、不要 broad-scan (pick at most 2 per branch)」

视觉风格：
- 方框 + 连线、不要过多圆角
- 文章名称用粗体、加 📖 icon
- Sans-serif、比例 4:3 或正方形
- 5 条分支颜色明显区分
- 每条分支顶端的 icon 视觉辨识度高（不只是 emoji 文字）

绝对不要 (DO NOT)：
- 不要任何「Source: ...」「by Anthropic / Cognition AI / Hamel Husain / LangGraph」等 attribution
- 不要 vendor logo / 公司商标
- 不要 mind-map 那种缤纷树枝树叶风格
- 不要 emoji 之外的卡通插图
- 不要 3D 渲染、渐层阴影
```

### en prompt

```
Generate a clean technical diagram titled "Agentic AI Advanced Reading Decision Tree".

Overall design: top-down decision tree with visual icons making the 5 branches easy to distinguish.

Top heading (with icon 🤔): "What problem are you stuck on right now?"

Branch down into 5 columns, laid out horizontally, each with a distinct color + icon:

1. Red branch 🌱
   Problem: "Don't know how to start with agents"
   ↓
   📖 Anthropic Building Effective Agents (~20 min)

2. Green branch 🤝
   Problem: "Multi-agent: when and how"
   ↓
   📖 Cognition Don't Build Multi-Agents (~10 min)

3. Yellow branch 🧠
   Problem: "Context inefficient"
   ↓
   📖 Anthropic Skills + CLAUDE.md memory docs (~15 min)

4. Blue branch 🧪
   Problem: "How to write evals / auto-verify"
   ↓
   📖 Hamel Husain Evals blog (~15 min)

5. Purple branch 🚀
   Problem: "Catch up on the frontier"
   ↓
   📖 LangGraph Plan-Execute / Voyager / Self-Discover paper (~30 min each)

Footer: "Rule: pick at most 2 papers per branch — do not broad-scan."

Visual style:
- Rectangular boxes + lines, minimal rounded corners
- Article names in bold, with a 📖 icon
- Sans-serif, 4:3 or square aspect ratio
- The 5 branches have distinct colors
- Branch-top icons are visually identifiable (not just emoji as plain text)

DO NOT:
- No "Source: ..." / "by Anthropic" / "Cognition AI" / "Hamel Husain" / "LangGraph" attribution
- No vendor logos / company marks
- No colorful mind-map style with tree-branch / leaf illustrations
- No cartoon illustrations beyond the listed emoji icons
- No 3D rendering, gradient shadows
```

---

## 圖 C — F11-F14 failure-mode lifecycle

### zh-TW prompt

```
生成一張清晰的技術示意圖、主題：「Agent failure mode 進化循環 (Failure-Mode Evolution Cycle)」。

整體設計：左/中央 5 步驟循環 (cycle / loop) + 右側 F14 具體例子、每個步驟有獨特 icon。

主圖（左 / 中央）：5 步驟循環、順時針或從上往下：

  ① 💥 發現 incident (Discover incident)
     — dogfood 或 production fail
            ↓
  ② 📝 文件化 (Document)
     — docs/observed-failure-modes.md
     — 命名為 F-N (named F-N、如 F11 / F12 / F13 / F14)
            ↓
  ③ 📋 加進 preset YAML check (Codify)
     — acceptance-gate preset YAML
            ↓
  ④ 🤖✅ 自動 catch (Auto-catch)
     — 下次同樣情境自動被抓
            ↓
  ⑤ 📜 mandatory rule (Mandatory invocation rule)
     — CLAUDE.md / SKILL.md 規則

從 ⑤ 拉一條箭頭回到 ①、循環持續、加註「持續循環 (continuous loop)」。

中間或側邊加文字：「不是寫死所有規則、是每出一次包就 codify 一次 (codify each incident once, don't pre-write every rule)」。

右側獨立框：F14 具體例子（直線箭頭）：
  💥 F14 incident (2026-05-13)
  ↓
  📝 observed-failure-modes.md F14
  ↓
  📋 multi-locale-mirror-sync.yml + check
  ↓
  🤖✅ Retrospective test → 9+ real drift caught
  ↓
  📜 CLAUDE.md mandatory rule

視覺風格：
- 主圖（5-step loop）+ F14 線性 example 右側、用線分隔
- 配色：incident 紅、document blue、preset green、auto-catch orange、CLAUDE.md purple
- Sans-serif、比例 16:9
- 簡潔 tech blog 風

絕對不要 (DO NOT)：
- 不要任何「Source: ...」「by agent-collab-skills」「Anthropic Skills 機制」等 attribution
- 不要 vendor logo / 公司商標
- 不要齒輪 / 發條 / 鐘錶 visual metaphor
- 不要 emoji 之外的卡通插圖
- 不要 3D 渲染、漸層陰影
```

### zh-Hans prompt

```
生成一张清晰的技术示意图、主题：「Agent failure mode 进化循环 (Failure-Mode Evolution Cycle)」。

整体设计：左/中央 5 步骤循环 (cycle / loop) + 右侧 F14 具体例子、每个步骤有独特 icon。

主图（左 / 中央）：5 步骤循环、顺时针或从上往下：

  ① 💥 发现 incident (Discover incident)
     — dogfood 或 production fail
            ↓
  ② 📝 文档化 (Document)
     — docs/observed-failure-modes.md
     — 命名为 F-N (named F-N、如 F11 / F12 / F13 / F14)
            ↓
  ③ 📋 加进 preset YAML check (Codify)
     — acceptance-gate preset YAML
            ↓
  ④ 🤖✅ 自动 catch (Auto-catch)
     — 下次同样情境自动被抓
            ↓
  ⑤ 📜 mandatory rule (Mandatory invocation rule)
     — CLAUDE.md / SKILL.md 规则

从 ⑤ 拉一条箭头回到 ①、循环持续、加注「持续循环 (continuous loop)」。

中间或侧边加文字：「不是写死所有规则、是每出一次包就 codify 一次 (codify each incident once, don't pre-write every rule)」。

右侧独立框：F14 具体例子（直线箭头）：
  💥 F14 incident (2026-05-13)
  ↓
  📝 observed-failure-modes.md F14
  ↓
  📋 multi-locale-mirror-sync.yml + check
  ↓
  🤖✅ Retrospective test → 9+ real drift caught
  ↓
  📜 CLAUDE.md mandatory rule

视觉风格：
- 主图（5-step loop）+ F14 线性 example 右侧、用线分隔
- 配色：incident 红、document blue、preset green、auto-catch orange、CLAUDE.md purple
- Sans-serif、比例 16:9
- 简洁 tech blog 风

绝对不要 (DO NOT)：
- 不要任何「Source: ...」「by agent-collab-skills」「Anthropic Skills 机制」等 attribution
- 不要 vendor logo / 公司商标
- 不要齿轮 / 发条 / 钟表 visual metaphor
- 不要 emoji 之外的卡通插图
- 不要 3D 渲染、渐层阴影
```

### en prompt

```
Generate a clean technical diagram titled "Agent Failure-Mode Evolution Cycle".

Overall design: 5-step cycle / loop on the left/center + F14 concrete example on the right, each step with a distinct icon.

Main diagram (left / center): 5-step cycle, clockwise or top-down:

  (1) 💥 Discover incident
      — from dogfood or production failure
            ↓
  (2) 📝 Document
      — in docs/observed-failure-modes.md
      — name it F-N (e.g. F11 / F12 / F13 / F14)
            ↓
  (3) 📋 Codify as preset YAML check
      — in the acceptance-gate preset YAML
            ↓
  (4) 🤖✅ Auto-catch
      — the next time the same situation appears, it is caught automatically
            ↓
  (5) 📜 Mandatory invocation rule
      — written into CLAUDE.md / SKILL.md

An arrow from (5) back to (1), with the caption "continuous loop".

Side caption (between or beside the loop): "Codify each incident once — don't pre-write every rule."

Right-side separate box: F14 concrete example (linear arrows):
  💥 F14 incident (2026-05-13)
  ↓
  📝 observed-failure-modes.md F14
  ↓
  📋 multi-locale-mirror-sync.yml + new check
  ↓
  🤖✅ Retrospective test → 9+ real drifts caught
  ↓
  📜 CLAUDE.md mandatory rule

Visual style:
- Main 5-step loop + linear F14 example on the right, separated by a divider line
- Color palette: incident red, document blue, preset green, auto-catch orange, CLAUDE.md purple
- Sans-serif typography
- 16:9 aspect ratio
- Clean tech blog aesthetic

DO NOT:
- No "Source: ..." / "by agent-collab-skills" / "Anthropic Skills mechanism" attribution
- No vendor logos / company marks
- No gear / clockwork / clock visual metaphors
- No cartoon illustration beyond the listed emoji icons
- No 3D rendering, gradient shadows
```

---

## 用法建議

1. 開 ChatGPT（DALL-E 或任何有 image gen 能力的 model）
2. 把對應語言的 prompt **整段**複製貼上、或把 9 個 `.txt` 拖進去叫它 batch 處理
3. 生成後存成 `resources/diagrams/concept-cluster.<locale>.png` / `reading-decision-tree.<locale>.png` / `failure-lifecycle.<locale>.png`
4. 嵌入 Stage 7.5 對應 section（取代或補充既有 ASCII 圖）

> 💡 **生成不滿意？** prompt 末尾「不要」list 加新項目（例如「不要藍色」「字太小、再放大」）regenerate。通常 2-3 次能拿到可用版本。
