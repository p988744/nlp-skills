---
name: finetune-llm-v2
description: |
  LLM fine-tuning 教練式引導工作流程 v2。
  核心功能：主動探索使用者痛點、引導明確目標、多任務管理、資料來源追蹤、完整版本 lineage。
  支援：LoRA/QLoRA/DoRA 微調、SFT/ORPO/DPO 對齊、資料準備、Benchmark 評估、HuggingFace 部署。
  特色：教練式引導、可重現的資料管線、多任務版本追蹤。
  觸發詞：「訓練模型」「fine-tune」「微調」「LoRA」「建立新任務」「改善模型」「優化準確率」「資料管線」「任務管理」
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion
---

# Fine-tune LLM v2 - 教練式引導工作流程

自動引導使用者完成 LLM 訓練專案，從痛點探索到模型部署。

## 核心理念

v2 採用「教練式引導」設計：
- **前期激勵**：主動探索使用者痛點和目標
- **主動提問**：引導釐清需求而非假設
- **決策支援**：根據資源和目標推薦最佳方案
- **完整追蹤**：資料來源、配置、模型全程可重現

## 快速開始

### 啟動教練引導
```
「我想訓練一個模型」
「幫我分析這個任務該怎麼做」
→ 觸發 goal-clarifier agent，主動引導釐清目標
```

### 管理多個任務
```
「列出所有任務」
「比較 entity-sentiment v1 和 v2」
→ 使用 /nlp-skills:tasks 指令
```

### 配置資料來源
```
「資料從 PostgreSQL 來」
「用 GPT 生成訓練資料」
→ 觸發 data-source-advisor agent
```

## 組件架構

### Skills (4 個專精領域)

| Skill | 職責 |
|-------|------|
| [llm-coach](skills/llm-coach/SKILL.md) | 教練式引導主入口 |
| [llm-knowledge](skills/llm-knowledge/SKILL.md) | 獨立知識庫 |
| [task-manager](skills/task-manager/SKILL.md) | 多任務管理 |
| [data-pipeline](skills/data-pipeline/SKILL.md) | 資料管線配置 |

### Commands (7 個快捷指令)

| 指令 | 功能 |
|------|------|
| `/nlp-skills:coach` | 啟動教練式對話 |
| `/nlp-skills:tasks` | 列出所有任務狀態 |
| `/nlp-skills:new-task` | 建立新任務 |
| `/nlp-skills:data-source` | 配置資料來源 |
| `/nlp-skills:generate` | 生成專案結構 |
| `/nlp-skills:evaluate` | 執行評估分析 |
| `/nlp-skills:deploy` | 部署模型 |

### Agents (4 個自主助手)

| Agent | 觸發時機 | 功能 |
|-------|----------|------|
| goal-clarifier | 偵測模糊需求 | 主動引導釐清目標 |
| data-source-advisor | 詢問資料來源 | 協助配置資料管線 |
| problem-diagnoser | 效能問題 | 自動診斷推薦改善 |
| result-analyzer | 訓練/評估後 | 分析結果決策建議 |

### Hooks (2 個事件處理)

| Hook | 事件 | 動作 |
|------|------|------|
| data-validation | 資料更新後 | 自動驗證格式分佈 |
| version-tracking | 訓練完成 | 記錄完整 lineage |

## 專案結構

每個任務是完全獨立的自包含專案：

```
{任務名稱}/
├── task.yaml               # 任務定義
├── data_source.yaml        # 資料來源配置（可重現）
├── versions/               # 版本追蹤（完整 lineage）
│   ├── v1/
│   │   ├── config.yaml     # 訓練配置快照
│   │   ├── data_snapshot.json  # 資料版本資訊
│   │   ├── results.json    # 評估結果
│   │   └── model_info.json # 模型資訊
│   └── v2/
├── data/
│   ├── raw/                # 原始資料
│   ├── train.jsonl
│   ├── valid.jsonl
│   └── test.jsonl
├── scripts/                # 執行腳本
│   ├── 01_regenerate_data.py   # 重新生成資料
│   ├── 02_validate_data.py
│   ├── 03_convert_format.py
│   ├── 04_train.py
│   ├── 05_evaluate.py
│   └── 06_upload_hf.py
├── configs/
├── models/
├── benchmarks/
└── docs/
```

## 資料來源配置

v2 的核心特色是可重現的資料管線：

```yaml
# data_source.yaml
sources:
  - type: database
    connection: postgresql://user:pass@host/db
    query: "SELECT text, label FROM annotations"
    snapshot_date: 2026-01-06

  - type: api
    endpoint: https://api.example.com/data
    params:
      limit: 1000

  - type: web_scrape
    urls: ["https://..."]
    keywords: ["金融", "股票"]

  - type: llm_generated
    prompt_template: |
      生成 {count} 筆金融情感分析訓練資料...
    model: gpt-4o
    count: 500

regeneration:
  script: scripts/01_regenerate_data.py
  last_run: 2026-01-06T10:30:00
```

## 版本追蹤

完整的 lineage 追蹤每次迭代：

```yaml
# versions/v2/lineage.yaml
version: v2
created: 2026-01-06T14:00:00
parent: v1

data:
  source_hash: abc123
  train_count: 500
  valid_count: 100
  test_count: 100

config:
  base_model: Qwen/Qwen3-4B
  method: sft
  lora_r: 64
  epochs: 6

results:
  macro_f1: 0.815
  accuracy: 0.82

changes:
  - "增加 LoRA rank 32 → 64"
  - "新增中立樣本 200 筆"
```

## 環境需求

### 本地開發
- Python: `uv run python`
- 模型測試: Ollama

### 遠端訓練
支援混合模式：
- 本地 GPU
- 遠端 SSH 伺服器
- 雲端服務（AWS, GCP, RunPod）

## 相關文件

- [skills/llm-coach/SKILL.md](skills/llm-coach/SKILL.md) - 教練引導
- [skills/llm-knowledge/SKILL.md](skills/llm-knowledge/SKILL.md) - 知識庫
- [skills/task-manager/SKILL.md](skills/task-manager/SKILL.md) - 任務管理
- [skills/data-pipeline/SKILL.md](skills/data-pipeline/SKILL.md) - 資料管線

---

*v2.0.0 - 教練式引導設計*
