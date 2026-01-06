---
name: finetune-llm
description: |
  LLM fine-tuning 完整工作流程，自動生成可重現的訓練專案。
  功能：LoRA/QLoRA/DoRA 微調、SFT/ORPO/DPO 對齊、資料準備、Benchmark 評估、HuggingFace 部署。
  支援模式：建立新任務 (Create)、改善既有任務 (Iterate)。
  內建知識庫：模型架構、訓練方法、任務類型、中文資料集、問題排解。
  觸發詞：「訓練模型」「fine-tune」「微調」「LoRA」「建立新任務」「改善模型」「優化準確率」「提升 F1」「重新訓練」
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task
---

# Fine-tune LLM Skill

自動生成可重現的 LLM 訓練專案，包含完整腳本、配置和文件。

## 快速開始

### 建立新任務
```
「我想訓練一個金融情感分析模型」
「幫我建立一個 NER 任務」
「fine-tune 一個中文分類模型」
```
→ 進入 [CREATE-MODE.md](CREATE-MODE.md)

### 改善既有任務
```
「改善 entity-sentiment 的準確率」
「entity-sentiment 的 F1 太低，怎麼辦」
「重新訓練 stance 模型」
```
→ 進入 [ITERATE-MODE.md](ITERATE-MODE.md)

## 模式選擇流程

```
啟動 Skill
    │
    ▼
┌─────────────────────────┐
│ 檢查 tasks/ 是否有既有任務 │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ 詢問使用者意圖            │
│ □ 建立新任務             │
│ □ 改善既有任務           │
└─────────────────────────┘
    │
    ├── 建立新任務 ──→ CREATE-MODE.md
    │
    └── 改善既有 ──→ ITERATE-MODE.md
```

## 專案產出結構

每個任務生成獨立可重現的資料夾：

```
tasks/{task_name}/
├── README.md                 # 快速開始
├── task_definition.yaml      # 任務定義
├── scripts/                  # 可執行腳本
│   ├── 01_validate_data.py
│   ├── 02_convert_format.py
│   ├── 03_train.py
│   ├── 04_evaluate.py
│   ├── 05_upload_hf.py
│   └── run_pipeline.sh       # 一鍵執行
├── configs/                  # 訓練配置
├── data/                     # 訓練資料
├── models/                   # 模型產出
├── benchmarks/               # 評估結果
├── docs/                     # 整合指南、標註指南
└── hf_cards/                 # HuggingFace Model Cards
```

## 知識庫

內建最新 LLM 知識（2025-2026），減少上網搜尋：

- [模型架構](references/architectures/INDEX.md) - Dense, MoE, MLA
- [基礎模型](references/models/INDEX.md) - Qwen, Llama, DeepSeek
- [訓練方法](references/methods/INDEX.md) - SFT, LoRA, ORPO, DPO
- [任務類型](references/tasks/INDEX.md) - 分類、抽取、生成
- [中文資料集](references/datasets/INDEX.md) - 情感、NER、指令
- [問題排解](references/troubleshooting/INDEX.md) - 過擬合、類別不平衡

詳見 [references/INDEX.md](references/INDEX.md)

## 工作流程總覽

詳見 [phases/INDEX.md](phases/INDEX.md)

```
Phase 1: 定義目標
    │
    ▼
Phase 2: 生成專案（腳本、配置、文件）
    │
    ▼
Phase 3: 準備資料
    │
    ▼
Phase 4: 訓練模型
    │
    ▼
Phase 5: 評估效能
    │
    ├── 達標 ──→ Phase 6: 部署
    │
    └── 未達標 ──→ 調整後重新訓練
```

## 環境需求

### 本地開發
- Python: `uv run python`
- 模型測試: Ollama

### 遠端訓練
首次使用時會詢問以下資訊，並儲存至 `task_definition.yaml`：
- GPU Server Host（如 `user@server-ip`）
- SSH Key Path（如 `~/.ssh/id_rsa`）
- CUDA Device（如 `0` 或 `0,1`）

## 相關文件

- [CREATE-MODE.md](CREATE-MODE.md) - 建立新任務完整流程
- [ITERATE-MODE.md](ITERATE-MODE.md) - 改善既有任務流程
- [phases/INDEX.md](phases/INDEX.md) - 各階段詳細指引
- [references/INDEX.md](references/INDEX.md) - 知識庫索引
- [CHECKLIST.md](CHECKLIST.md) - 進度追蹤模板
