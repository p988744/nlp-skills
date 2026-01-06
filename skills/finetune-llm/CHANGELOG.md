# Changelog

All notable changes to the finetune-llm skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.0.0] - 2026-01-06

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

## [1.0.0] - 2026-01-05

### Added
- 初始版本
- 8 階段線性工作流程
- 基本訓練指引

---

## 版本命名規則

- **MAJOR**: 架構重大變更、不相容更新
- **MINOR**: 新增功能、向後相容
- **PATCH**: Bug 修復、文件更新
