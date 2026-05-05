# Launch checklist

> 這份是 maintainer 內部用的——repo 從 Phase 5 ship 到開始**主動推廣**前要走完的一次性步驟。

---

## ✅ Pre-launch（已完成）

- [x] Phase 1-5 內容 ship（134 entries、style guide、walkthrough、Mermaid 圖）
- [x] `.github/` issue + PR template
- [x] `resources/style-guide.md` zh + en
- [x] `scripts/check-links.py` + `refresh-stars.py` 可跑
- [x] CI lint workflow（zh-CN slip + overclaim 自動檢查；每月跑 link-rot + star-drift）

## 🟡 Pre-launch（一次性手動 setup）

- [ ] **GitHub Pages**：repo Settings → Pages → Source: **GitHub Actions**
  - 啟用後，`.github/workflows/deploy-book.yml` 推 main 會自動 deploy 到 `https://wenyuchiou.github.io/awesome-agentic-ai-zh/`
- [ ] **GitHub Discussions**：repo Settings → Features → enable Discussions
  - Categories 建議：
    - 🙋 Q&A — 學習問題
    - 💡 Project nominations — 推薦新 project（先討論再 PR）
    - 📚 Stage discussion — 每個 stage 一個 thread
    - 🎯 Show & tell — 走完 stage 的人 share 自己的成果
- [ ] **第一次 PDF release**：本地跑 `bash scripts/build-pdf.sh`，把 `dist/awesome-agentic-ai-zh.pdf` 上傳到 GitHub Release v1.0
- [ ] **GitHub Releases**：以 `phase-5` tag 為起點建第一個 release，附 PDF

## 🟢 Soft launch（小範圍宣傳）

- [ ] 跟 `WenyuChiou` 朋友圈分享（內測）
- [ ] 修 1-2 輪內測回饋（issue 處理）

## 🚀 Public launch（推廣）

### 提交到中文社群 awesome list

- [ ] [`AiHubCN/Awesome-Chinese-LLM`](https://github.com/AiHubCN/Awesome-Chinese-LLM) — 開 PR 加進 catalog（教學資源 / 學習路線 section）
- [ ] [`WangRongsheng/awesome-LLM-resources`](https://github.com/WangRongsheng/awesome-LLM-resources) — 開 PR
- [ ] [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — 開 PR（learning resources）
- [ ] [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — 開 PR（learning resources）

### 寫 launch 文章

- [ ] **Threads 短版**（2-3 則）— 重點：134 個 project、跨 stage walkthrough、誠實時程
- [ ] **dev.to 長版**（一篇 1000-1500 字）— 寫「為什麼平鋪 awesome 不夠用、結構化路線怎麼做」
- [ ] （選）**個人部落格** — 同樣內容深度版

### 中文 LLM 社群

- [ ] Datawhale 微信社群（如果有 zh-TW 受眾）
- [ ] Hacker News（zh-TW 故事性夠強的話）
- [ ] r/LocalLLaMA、r/MachineLearning（看 reddit 接受度）

## 🔁 Post-launch（持續）

- [ ] 第一週每天 review issue
- [ ] 每週合併 PR
- [ ] 每月 1 號 CI 自動跑（已設定），檢查 link rot + star drift
- [ ] 每季 review：
  - 加 5-10 個新 entry（保持 130-160 範圍）
  - update stale repos（archived / pushed > 6 months）
  - 看有沒有自薦 stage maintainer 的 issue 要處理
- [ ] 每半年 phase milestone：
  - 內容明顯擴張、有 new audience 訊號 → 規劃 Phase 7

---

## 📊 成功指標（不是目標、是訊號）

排序大致按 fingerprint 強度——前面比後面更可靠。

1. **每月新 issue / PR 數量**（活躍社群訊號）
2. **stage maintainer 自薦數**（深度 engagement）
3. **被引用 / 被收錄到其他 awesome list 數**
4. **Star 數**（弱訊號，容易被刷；只看趨勢、不看絕對值）

---

## 不該做的（deliberate "no"s）

- ❌ 為了上熱門就刷 SEO 關鍵字
- ❌ 為了 star 數加 low-quality entry
- ❌ 把 PR 合進 main 而不 review（即使是 typo 也要 review）
- ❌ 自家 repo 重新加回 catalog（先前刻意移除）
- ❌ 接 sponsor / affiliate link（會影響推薦獨立性）
