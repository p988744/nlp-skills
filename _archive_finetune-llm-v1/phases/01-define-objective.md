# Phase 1: 定義目標

## 概述

與使用者對話，釐清任務需求並生成 `task_definition.yaml`。

## 必要資訊

### 1. 基本資訊

```yaml
task_name: sentiment-analysis  # 英文、無空格
description: 金融新聞情感分析
domain: finance  # 領域
language: zh-TW  # 語言
```

### 2. 任務類型

| 類型 | 說明 | 範例 |
|------|------|------|
| classification | 分類任務 | 情感分析、主題分類 |
| extraction | 抽取任務 | NER、關係抽取 |
| generation | 生成任務 | 摘要、風格轉換 |
| qa | 問答任務 | 閱讀理解 |

### 3. 輸入輸出規格

```yaml
input_format:
  fields:
    - name: text
      type: string
      description: 待分析文本
      required: true

output_format:
  type: single_label  # 或 multi_label, json, text
  schema:
    label:
      type: enum
      enum: [正面, 負面, 中立]
```

### 4. 成功標準

```yaml
success_criteria:
  primary_metric: macro_f1
  threshold: 0.80
  secondary_metrics:
    - accuracy
    - per_class_f1
```

### 5. 訓練配置 (可選)

```yaml
training:
  base_model: Qwen/Qwen3-4B
  method: sft
  lora:
    r: 32
    alpha: 64
```

## 對話引導範本

### 開場

```
您好！我將協助您建立 LLM 微調任務。

請問您想完成什麼任務？例如：
- 分析文本情感（正面/負面/中立）
- 從文本中抽取實體（人名、組織等）
- 將文本轉換成特定格式
```

### 確認任務類型

```
了解，這是一個 {classification/extraction/generation} 任務。

請問：
1. 輸入是什麼？（文本、對話、文件...）
2. 期望的輸出格式？
3. 有多少類別/實體類型？
```

### 確認成功標準

```
請問您對模型效能的期望是？

建議標準：
- 分類任務：Macro-F1 >= 80%
- NER 任務：Entity F1 >= 70%
- 生成任務：人工評估通過率
```

### 確認資源

```
關於訓練資源：
1. 您有多少訓練資料？
2. 可用的 GPU 資源？（決定模型大小和訓練方法）
3. 預期的完成時間？
```

## 完整 task_definition.yaml 範本

```yaml
# ===========================================
# LLM 微調任務定義
# ===========================================

# === 基本資訊 ===
task_name: financial-sentiment
description: 金融新聞情感分析模型
version: "1.0"
created: "2026-01-06"

# === 任務規格 ===
domain: finance
language: zh-TW
task_type: classification

# === 輸入規格 ===
input_format:
  fields:
    - name: text
      type: string
      description: 金融新聞文本
      required: true
      max_length: 1000

# === 輸出規格 ===
output_format:
  type: single_label
  schema:
    label:
      type: enum
      enum:
        - 正面
        - 負面
        - 中立
      description: 情感類別

# === 成功標準 ===
success_criteria:
  primary_metric: macro_f1
  threshold: 0.80
  secondary_metrics:
    - accuracy
    - per_class_f1

# === 訓練配置 ===
training:
  base_model: Qwen/Qwen3-4B
  method: sft
  lora:
    r: 32
    alpha: 64
    dropout: 0.05
  epochs: 8
  learning_rate: 1e-5
  batch_size: 4

# === 資料規格 ===
data:
  estimated_train_samples: 1000
  estimated_test_samples: 300
  data_source: 財經新聞資料庫

# === 部署配置 ===
deployment:
  hf_repo_base: {your-hf-org}/{prefix}-{task_name}-zh
  formats:
    - adapter  # LoRA adapter
    - gguf     # Ollama
    - vllm     # vLLM merged

# === 備註 ===
notes:
  - 訓練資料需涵蓋各類財經新聞
  - 注意中立類別的定義和邊界
```

## 驗證清單

生成 task_definition.yaml 後，確認：

- [ ] task_name 是英文、無空格
- [ ] 輸入輸出格式明確
- [ ] 類別/標籤定義清楚
- [ ] 成功標準合理
- [ ] 訓練資源符合需求

## 下一步

完成後進入 [Phase 2: 生成專案](02-generate-project.md)

---

*更新: 2026-01*
