# 給開發者 — 專業分支

> [English](./for-developer.en.md) | **繁體中文**

> [← 回主路線 README](../README.md) · 從 Stage 7 結尾分支出來。把 agentic AI 應用到開發流程上。

## 使用情境

- AI 結對程式設計（Cursor、Aider、Claude Code、Cline、Continue）
- Code review 自動化
- 測試生成
- Multi-agent coding 任務（規劃 + 執行）
- IDE 整合與 CI 規範

## 精選 Projects

### Coding Agents

#### [Cursor](https://www.cursor.com/) ⭐⭐⭐⭐⭐
編輯器整合的 AI 結對程式設計工具。AI 輔助 coding 的業界標準。

#### [Aider-AI/aider](https://github.com/Aider-AI/aider) ⭐⭐⭐⭐⭐
★ 44k+ · Apache-2.0 — git-aware 的 CLI pair-programmer。直接編輯你 repo 中的檔案，commit 都自動寫好。**「git-native AI 編輯流程」的開源範本**。模型不限。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 120k+ — Anthropic 官方的 agentic coding 助理。有 Skills + plugin 生態系。

#### [cline/cline](https://github.com/cline/cline) ⭐⭐⭐⭐⭐
★ 61k+ · Apache-2.0 — VS Code extension，autonomous in-IDE agent：tool use、browser、step-by-step approval。**VS Code 使用者要 IDE-native agentic dev 的好選項**。

#### [continuedev/continue](https://github.com/continuedev/continue) ⭐⭐⭐⭐
★ 33k+ · Apache-2.0 — source-controlled AI checks，可以在 CI 強制執行。代表「**團隊 / governance**」這條角度的 coding agent。

#### [OpenHands (前身為 OpenDevin)](https://github.com/All-Hands-AI/OpenHands) ⭐⭐⭐⭐
Open source 的自主軟體開發 agent。

#### [block/goose](https://github.com/block/goose) ⭐⭐⭐⭐
★ 43k+ · Apache-2.0 — 開源、可擴充的 AI agent，超出純 code suggestion——能 install / execute / edit / test，搭配任何 LLM。**provider-agnostic + MCP-native**，提供 desktop app、CLI、API 三種介面。（repo 現指向 `aaif-goose/goose`。）

#### [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) ⭐⭐⭐⭐
★ 23k+ · Apache-2.0 — VS Code 的 coding agent，採用「**多種專業 mode**」的設計，跟 Cline 的單一 agent flow 不同。VS Code 使用者要 multi-mode 替代方案的選擇。

### Code Review

#### [obra/superpowers](https://github.com/obra/superpowers) ⭐⭐⭐⭐
20+ 個經過實戰驗證的 skill，包括 TDD 模式、debug、協作模式。設計 code-review skill 時的好參考。

## 必練流程

- **AI 結對程式設計**：日常工作用 Claude Code、Cursor、或 Cline 任一個
- **Git-native AI 編輯**：用 Aider 跑一週，習慣「AI 編輯 → commit → review」這個節奏
- **CI 上的 AI check**：用 Continue 把 AI 檢查接到 PR pipeline
- **測試生成**：寫一個 skill / prompt，從 function signature 生出 pytest 測試
- **Code review 自動化**：在每一個 PR 上呼叫 Claude API 的 GitHub Action
