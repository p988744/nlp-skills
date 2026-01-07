# Changelog

All notable changes to the finetune-llm skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.3.1] - 2026-01-07

### Added
- **Model Versioning Strategy**: Added versioning strategy selection to coaching workflow
  - Semantic versioning (v1, v2, v3) - Recommended for iterative development
  - Date versioning (2025-01-07) - For API services and scheduled retraining
  - Hybrid versioning (v2-20250107) - Track both version and timestamp
- Deployment target recommendations (HuggingFace Hub, Ollama, API)
- Model artifact naming conventions for each strategy
- Version retention policy configuration
- Industry examples (Meta, OpenAI, Anthropic conventions)

### Changed
- Updated llm-coach skill with versioning exploration in pain point discovery
- Updated task-manager skill with comprehensive versioning guide
- English README documentation

---

## [0.3.0] - 2026-01-06

### Added
- **教練式引導設計**：從前期激勵到決策支援的完整教練體驗
- **多任務管理**：支援多個訓練任務的版本追蹤和比較
- **資料來源追蹤**：可重現的資料管線配置 (data_source.yaml)
  - 支援資料庫、API、網頁爬取、LLM 生成、檔案匯入
- **4 個專精 Skills**：
  - `llm-coach` - 教練式引導主入口
  - `llm-knowledge` - 獨立知識庫
  - `task-manager` - 多任務管理
  - `data-pipeline` - 資料管線配置
- **7 個快捷 Commands**：
  - `/nlp-skills:coach` - 啟動教練式對話
  - `/nlp-skills:tasks` - 列出所有任務
  - `/nlp-skills:new-task` - 建立新任務
  - `/nlp-skills:data-source` - 配置資料來源
  - `/nlp-skills:generate` - 生成專案結構
  - `/nlp-skills:evaluate` - 執行評估
  - `/nlp-skills:deploy` - 部署模型
- **4 個智能 Agents**：
  - `goal-clarifier` - 主動引導釐清目標
  - `data-source-advisor` - 協助配置資料管線
  - `problem-diagnoser` - 自動診斷問題
  - `result-analyzer` - 分析結果提供決策
- **Hooks 自動化**：
  - 資料來源配置驗證
  - 版本 lineage 追蹤
  - 訓練完成後自動提示評估
  - 評估完成後自動分析結果

### Changed
- 重新設計專案結構：每個任務完全獨立自包含
- 版本追蹤改為完整 lineage（資料、配置、結果全記錄）
- 知識庫移至獨立的 `llm-knowledge` skill
- Commands 採用 `nlp-skills:command` 命名避免衝突

### Removed
- 移除 CREATE-MODE.md / ITERATE-MODE.md（整合到教練式引導）
- 移除單一入口 SKILL.md（拆分為多個專精 skills）
- 移除舊版 phases/ 目錄結構

---

## [0.2.1] - 2026-01-06

### Added
- **Slash Command**: 新增 `/finetune-llm` 命令，支援 `create` 和 `iterate` 參數

---

## [0.2.0] - 2026-01-06

### Added
- **雙模式支援**: Create (建立新任務) 和 Iterate (改善既有任務)
- **Reference 知識庫** (2025-2026 知識截止):
  - architectures/: Dense, MoE 架構比較
  - models/: Qwen, DeepSeek, Llama 模型指南
  - methods/: SFT, LoRA, QLoRA, ORPO, DPO
  - tasks/: 情感分析、NER 任務指南
  - troubleshooting/: 過擬合、類別不平衡、準確率低
- **自動專案生成**: 根據 task_definition.yaml 生成完整專案結構
- **Jinja2 模板**: 訓練腳本、評估腳本、配置檔、Model Cards
- **6 階段工作流程文件**: 定義→生成→準備→訓練→評估→部署
- **CHECKLIST.md**: 完整檢查清單

### Changed
- 重新設計目錄結構，採用 INDEX.md 漸進式展開
- 符合 Claude Code skill best practices

### Removed
- 移除舊版單一流程設計

---

## [0.1.0] - 2026-01-05

### Added
- 初始版本
- 8 階段線性工作流程
- 基本訓練指引

---

## 版本命名規則

- **MAJOR**: 架構重大變更、不相容更新
- **MINOR**: 新增功能、向後相容
- **PATCH**: Bug 修復、文件更新
