---
name: task-manager
description: |
  This skill should be used when the user asks to "list tasks", "show all tasks", "compare versions", "switch to task X", "task status", "version history", "what tasks do I have", or needs to manage multiple training tasks. Provides multi-task management, version tracking, and performance comparison capabilities.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Task Manager - 多任務管理

管理多個 LLM 訓練任務，追蹤版本歷史，比較效能。

## 核心功能

| 功能 | 說明 |
|------|------|
| 任務列表 | 顯示所有任務、狀態、最新效能 |
| 版本追蹤 | 記錄每次迭代的完整 lineage |
| 版本比較 | 比較同一任務不同版本的效能差異 |
| 任務切換 | 在不同任務之間快速切換工作目錄 |

## 任務生命週期

```
created → configuring → training → evaluating → deployed
                ↑______________|
                    (iterate)
```

| 狀態 | 說明 |
|------|------|
| `created` | 任務已建立，尚未配置 |
| `configuring` | 配置中（資料來源、訓練參數） |
| `training` | 訓練進行中 |
| `evaluating` | 評估中 |
| `deployed` | 已部署上線 |
| `archived` | 已封存（不再使用） |

## 專案結構

每個任務是完全獨立的自包含目錄：

```
{project_root}/
├── entity-sentiment/        # 任務 1
│   ├── task.yaml           # 任務定義
│   ├── data_source.yaml    # 資料來源配置
│   ├── versions/           # 版本追蹤
│   │   ├── v1/
│   │   │   ├── config.yaml
│   │   │   ├── data_snapshot.json
│   │   │   ├── results.json
│   │   │   ├── model_info.json
│   │   │   └── lineage.yaml
│   │   └── v2/
│   ├── data/
│   ├── scripts/
│   ├── models/
│   └── benchmarks/
│
├── stance-detection/        # 任務 2
│   └── ...
│
└── ner-finance/            # 任務 3
    └── ...
```

## 任務定義檔

### task.yaml

```yaml
# 任務基本資訊
task_name: entity-sentiment
version: v2                    # 當前活動版本
status: evaluating

# 任務定義
task_type: classification
domain: finance
language: zh-TW

# 輸入輸出
input_template: |
  分析以下文本對「{entity}」的情感傾向。
  文本：{text}

output_format:
  type: json
  schema:
    sentiment:
      type: string
      enum: ["正面", "負面", "中立"]

# 成功標準
success_criteria:
  primary_metric: macro_f1
  threshold: 0.80

# 執行環境
execution:
  type: remote_ssh
  host: user@gpu-server
  cuda_devices: "0"

# 元資料
created: 2026-01-05T10:00:00
updated: 2026-01-06T14:30:00
```

## 版本追蹤

### lineage.yaml

每個版本記錄完整的 lineage 資訊：

```yaml
version: v2
created: 2026-01-06T14:00:00
parent: v1                     # 前一版本

# 資料資訊
data:
  source_hash: abc123def456    # data_source.yaml 的 hash
  train_count: 700
  valid_count: 140
  test_count: 160
  class_distribution:
    正面: 280
    負面: 245
    中立: 175

# 訓練配置
config:
  base_model: Qwen/Qwen3-4B
  method: sft
  lora:
    r: 64
    alpha: 128
    dropout: 0.05
  epochs: 6
  learning_rate: 1e-5
  batch_size: 4

# 評估結果
results:
  macro_f1: 0.815
  accuracy: 0.82
  per_class:
    正面:
      precision: 0.85
      recall: 0.87
      f1: 0.86
    負面:
      precision: 0.82
      recall: 0.80
      f1: 0.81
    中立:
      precision: 0.78
      recall: 0.79
      f1: 0.785

# 模型資訊
model:
  adapter_path: models/adapter/v2
  merged_path: models/merged/v2
  gguf_path: models/gguf/v2-q8_0.gguf
  hf_repo: org/entity-sentiment-v2

# 變更說明
changes:
  - "LoRA rank 32 → 64"
  - "新增中立樣本 200 筆"
  - "訓練輪數 8 → 6（防止過擬合）"

# 備註
notes: |
  v2 主要針對中立類別的 F1 進行改善。
  透過增加中立樣本和調高 LoRA rank，
  中立 F1 從 62% 提升到 78.5%。
```

## 操作指南

### 列出所有任務

掃描當前目錄下的所有任務：

```python
# 掃描邏輯
for dir in current_directory:
    if exists(dir/task.yaml):
        tasks.append(parse_task(dir/task.yaml))
```

輸出格式：

```
┌─────────────────────┬────────────┬─────────┬───────────┬───────────────┐
│ 任務名稱            │ 狀態       │ 版本    │ Macro-F1  │ 更新時間      │
├─────────────────────┼────────────┼─────────┼───────────┼───────────────┤
│ entity-sentiment    │ evaluating │ v2      │ 81.5%     │ 2026-01-06    │
│ stance-detection    │ training   │ v1      │ -         │ 2026-01-06    │
│ ner-finance         │ deployed   │ v3      │ 76.2%     │ 2026-01-05    │
└─────────────────────┴────────────┴─────────┴───────────┴───────────────┘
```

### 查看版本歷史

顯示特定任務的所有版本：

```
任務: entity-sentiment
當前版本: v2

版本歷史:
┌─────────┬───────────────┬───────────┬──────────────────────────────┐
│ 版本    │ 建立時間      │ Macro-F1  │ 主要變更                     │
├─────────┼───────────────┼───────────┼──────────────────────────────┤
│ v2 (*)  │ 2026-01-06    │ 81.5%     │ LoRA↑, 中立樣本↑             │
│ v1      │ 2026-01-05    │ 72.0%     │ 初始版本                     │
└─────────┴───────────────┴───────────┴──────────────────────────────┘
```

### 版本比較

比較兩個版本的差異：

```
比較: entity-sentiment v1 → v2

配置變更:
┌──────────────────┬─────────┬─────────┬─────────┐
│ 配置項           │ v1      │ v2      │ 變化    │
├──────────────────┼─────────┼─────────┼─────────┤
│ LoRA r           │ 32      │ 64      │ +100%   │
│ epochs           │ 8       │ 6       │ -25%    │
│ train_count      │ 500     │ 700     │ +40%    │
└──────────────────┴─────────┴─────────┴─────────┘

效能比較:
┌──────────────────┬─────────┬─────────┬─────────┐
│ 指標             │ v1      │ v2      │ 變化    │
├──────────────────┼─────────┼─────────┼─────────┤
│ Macro-F1         │ 72.0%   │ 81.5%   │ +9.5%   │
│ Accuracy         │ 72.0%   │ 82.0%   │ +10.0%  │
│ 正面 F1          │ 78%     │ 86%     │ +8%     │
│ 負面 F1          │ 72%     │ 81%     │ +9%     │
│ 中立 F1          │ 62%     │ 78.5%   │ +16.5%  │
└──────────────────┴─────────┴─────────┴─────────┘

結論: v2 顯著提升，建議採用。
```

### 建立新版本

當開始新一輪迭代時：

1. 複製前一版本的 config 作為基礎
2. 記錄變更說明
3. 執行訓練
4. 自動記錄結果到 lineage.yaml

```bash
# 建立新版本目錄
mkdir -p entity-sentiment/versions/v3

# 複製配置
cp entity-sentiment/versions/v2/config.yaml \
   entity-sentiment/versions/v3/config.yaml

# 編輯配置後執行訓練
# ...

# 訓練完成後自動更新 lineage.yaml
```

### 回滾版本

如果新版本效能下降，可以回滾：

```yaml
# 更新 task.yaml
version: v1  # 從 v2 回滾到 v1

# 模型路徑自動切換到 v1
```

## 版本管理策略

### 策略選擇指南

| 策略 | 格式 | 適用場景 | 業界案例 |
|------|------|----------|----------|
| **Semantic** | `v1`, `v2`, `v3` | 迭代開發、HuggingFace | Meta Llama-3.3, Qwen3 |
| **Date** | `2025-01-07` | API 服務、快照備份 | OpenAI gpt-4o-2024-08-06 |
| **Hybrid** | `v2-20250107` | 同時追蹤版本和時間 | Anthropic claude-3-5-sonnet-20241022 |

### Semantic 版本（推薦）

適用於大多數 fine-tuning 專案：

```
versions/
├── v1/          # 初始版本
├── v2/          # 參數調整
├── v2.1/        # v2 的小修改
├── v3/          # 資料擴增
└── v3-exp/      # 實驗性版本
```

**命名規則**：
```
v{major}           - 主要版本（資料或架構變更）
v{major}.{minor}   - 次要版本（參數調整）
v{major}-exp       - 實驗版本（待驗證）
```

**部署整合**：
```bash
# HuggingFace Hub - 使用 git tag
huggingface-cli upload org/model ./model --revision v2

# Ollama - 使用 tag
ollama push org/model:v2

# 模型命名
{task_name}-v{n}  # entity-sentiment-v2
```

### Date 版本

適用於 API 服務和定期重訓：

```
versions/
├── 2025-01-07/
├── 2025-01-15/
└── 2025-02-01/
```

**命名規則**：
```
YYYY-MM-DD                 # 日期
YYYYMMDD                   # 緊湊格式
{task_name}-YYYY-MM-DD     # 帶任務名
```

**部署整合**：
```bash
# API 服務
model-2025-01-07

# 版本回滾
curl -X POST /api/v1/rollback?version=2025-01-07
```

### Hybrid 版本

同時追蹤版本演進和時間點：

```
versions/
├── v1-20250105/
├── v2-20250107/
└── v3-20250115/
```

**命名規則**：
```
v{n}-YYYYMMDD    # v2-20250107
v{n}_{timestamp} # v2_1736236800
```

### 模型產出物命名

```yaml
# lineage.yaml 中的模型路徑
model:
  # Semantic 策略
  adapter_path: models/adapter/v2
  merged_path: models/merged/v2
  gguf_path: models/gguf/entity-sentiment-v2-q8_0.gguf
  hf_repo: org/entity-sentiment  # 使用 git tag: v2

  # Date 策略
  adapter_path: models/adapter/2025-01-07
  merged_path: models/merged/2025-01-07
  gguf_path: models/gguf/entity-sentiment-2025-01-07-q8_0.gguf
  hf_repo: org/entity-sentiment-2025-01-07

  # Hybrid 策略
  adapter_path: models/adapter/v2-20250107
  merged_path: models/merged/v2-20250107
  gguf_path: models/gguf/entity-sentiment-v2-20250107-q8_0.gguf
  hf_repo: org/entity-sentiment  # 使用 git tag: v2-20250107
```

### 版本保留策略

```yaml
# task.yaml
versioning:
  strategy: semantic
  retention:
    keep_recent: 3           # 保留最近 3 個版本
    keep_deployed: true      # 永久保留已部署版本
    keep_best: true          # 保留效能最佳版本
    cleanup_exp_after: 7d    # 實驗版本 7 天後清理
```

**清理規則**：
1. 永遠保留：`deployed` 狀態的版本
2. 永遠保留：歷史最佳效能版本
3. 保留最近 N 個版本（預設 3）
4. 實驗版本：成功則合併，失敗則清理

## 最佳實踐

### 版本命名

```
v1      - 初始版本
v2      - 第二次迭代
v2.1    - v2 的小修改
v3-exp  - 實驗性版本
```

### 變更說明

每次版本更新都應記錄清晰的變更說明：

```yaml
changes:
  - "具體改動1"
  - "具體改動2"

# 好的範例
changes:
  - "LoRA rank 32 → 64"
  - "新增中立樣本 200 筆"
  - "learning_rate 1e-5 → 5e-6"

# 不好的範例
changes:
  - "調整參數"
  - "增加資料"
```

### 清理策略

定期清理不需要的版本：

- 保留所有 deployed 的版本
- 保留最近 3 個版本
- 實驗性版本成功後合併，失敗後刪除

## 相關資源

### 指令
- `/nlp-skills:tasks` - 列出所有任務
- `/nlp-skills:new-task` - 建立新任務

### 其他 Skills
- [data-pipeline](../data-pipeline/SKILL.md) - 資料來源配置
- [llm-coach](../llm-coach/SKILL.md) - 教練式引導
