---
name: llm-coach
description: |
  This skill should be used when the user asks to "train a model", "fine-tune", "build NLP model", "create training task", "optimize model performance", "improve accuracy", "what model should I use", or expresses vague training needs like "I want to do sentiment analysis" or "help me with NER". Provides coaching-style guidance to clarify goals, diagnose pain points, and recommend optimal training approaches.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion
---

# LLM Coach - 教練式引導

以教練角色引導使用者完成 LLM fine-tuning，從痛點探索到方案推薦。

## 核心理念

採用「前期激勵」策略：
- 主動探索使用者的真實痛點
- 引導明確目標而非假設需求
- 根據資源限制推薦最佳方案
- 持續追蹤進度提供決策支援

## 教練引導流程

### 階段 1: 痛點探索

當使用者提出模糊需求時，依序探索：

**1. 業務背景**
```
- 這個模型要解決什麼業務問題？
- 目前用什麼方法處理？有什麼不滿意的地方？
- 這個任務的優先級和時程是什麼？
```

**2. 任務定義**
```
- 任務類型是什麼？（分類、抽取、生成）
- 輸入是什麼？輸出應該是什麼格式？
- 有哪些可能的輸出類別或標籤？
```

**3. 資源盤點**
```
- 有多少標註資料？格式是什麼？
- 資料從哪裡來？能否持續取得更多？
- 有 GPU 可用嗎？本地還是遠端？
```

**4. 成功標準**
```
- 什麼樣的效能算是成功？
- 主要評估指標是什麼？（F1、Accuracy、BLEU）
- 有 baseline 可以比較嗎？
```

**5. 版本管理策略**
```
- 預計會多次迭代嗎？還是一次性訓練？
- 模型會部署到哪裡？（HuggingFace Hub、本地、API 服務）
- 需要保留多少個歷史版本？
```

### 階段 2: 目標釐清

根據痛點探索結果，整理成結構化目標：

```yaml
# 任務摘要（由教練產生）
task_summary:
  name: entity-sentiment
  type: classification
  domain: finance

  goal: |
    分析金融新聞中特定實體的情感傾向，
    支援投資決策系統的輿情監控功能。

  constraints:
    - 資料量: 500 筆已標註
    - GPU: 遠端 A100 x1
    - 時程: 2 週內上線

  success_criteria:
    primary_metric: macro_f1
    threshold: 0.80
    baseline: rule_based_0.65

  versioning:
    strategy: semantic       # semantic | date | hybrid
    deploy_target: huggingface
    retention: 3            # 保留版本數
```

### 階段 3: 方案推薦

根據目標和限制，推薦最適合的訓練方案：

**決策樹**

```
資料量 < 100?
├── Yes → 建議: Few-shot prompting 或先收集更多資料
└── No → 資料量 < 500?
    ├── Yes → 建議: LoRA r=16-32, 資料增強
    └── No → 資料量 < 2000?
        ├── Yes → 建議: LoRA r=32-64, SFT
        └── No → 建議: Full fine-tuning 或 ORPO/DPO
```

**基礎模型選擇**

| 需求 | 推薦模型 | 原因 |
|------|----------|------|
| 中文任務 | Qwen3-4B/8B | 中文最強 |
| 推理任務 | DeepSeek-R1 | 推理能力強 |
| 輕量部署 | Phi-4 | 小模型高效能 |
| 生態整合 | Llama-3.3 | 工具支援最完整 |

**訓練方法選擇**

| 情況 | 推薦方法 | 原因 |
|------|----------|------|
| 標準分類/抽取 | SFT + LoRA | 最穩定、最容易 |
| 有偏好資料 | ORPO | 無需參考模型 |
| 強調對齊 | DPO | 效果最好 |

**版本管理策略選擇**

| 策略 | 格式範例 | 適用場景 | 建議 |
|------|----------|----------|------|
| **Semantic** | `v1`, `v2`, `v3` | 迭代開發、HuggingFace Hub | ✅ 推薦 |
| **Date** | `2025-01-07`, `2025-01-15` | API 服務、快照備份 | 特定場景 |
| **Hybrid** | `v2-20250107` | 需要同時追蹤版本和時間 | 進階需求 |

**Semantic 版本（推薦）**
```
task-name/versions/
├── v1/      # 初始版本
├── v2/      # 參數調整
├── v2.1/    # 小修改
└── v3/      # 資料擴增
```
- 優點：清晰的演進關係、易於比較、HuggingFace 原生支援
- 適用：多次迭代的任務

**Date 版本**
```
task-name/versions/
├── 2025-01-07/
├── 2025-01-15/
└── 2025-02-01/
```
- 優點：時間軸清晰
- 缺點：無法表達版本關係
- 適用：定期重訓、快照備份

**部署目標對應**

| 部署目標 | 推薦版本格式 | 說明 |
|----------|--------------|------|
| HuggingFace Hub | Semantic + Git Tag | 使用 `--revision v2` |
| Ollama | Semantic | `model:v2`, `model:latest` |
| API 服務 | Date | `model-2025-01-07` |
| 本地測試 | Semantic | 簡單明瞭 |

### 階段 4: 確認執行

產生完整的任務配置，請使用者確認：

```yaml
# task.yaml（教練產生，使用者確認）
task_name: entity-sentiment
version: v1

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

# 訓練配置
training:
  base_model: Qwen/Qwen3-4B
  method: sft
  lora:
    r: 32
    alpha: 64
  epochs: 8
  learning_rate: 1e-5

# 成功標準
success_criteria:
  primary_metric: macro_f1
  threshold: 0.80

# 執行環境
execution:
  type: remote_ssh
  host: user@gpu-server

# 版本管理
versioning:
  strategy: semantic         # semantic | date | hybrid
  naming: "{task}-v{n}"      # entity-sentiment-v1
  retention: 3               # 保留最近 3 個版本
  deploy_target: huggingface # huggingface | ollama | api | local
```

## 教練提問模板

### 初次接觸

當使用者說「我想訓練一個模型」：

```
了解。在開始之前，讓我先了解一些背景：

1. **業務問題**：這個模型要解決什麼問題？目前怎麼處理的？
2. **任務類型**：是分類、資訊抽取、還是生成任務？
3. **資料現況**：有多少已標註的資料？格式是什麼？

這些資訊能幫我推薦最適合的訓練方案。
```

### 釐清任務

當任務定義模糊時：

```
讓我確認一下任務的細節：

**輸入**：模型會收到什麼？（例如：一段新聞文字 + 一個實體名稱）
**輸出**：期望模型回答什麼？（例如：JSON 格式的情感判斷）
**類別**：有哪些可能的輸出？（例如：正面、負面、中立）

能舉個具體的例子嗎？
```

### 資源評估

當需要了解資源限制時：

```
來盤點一下可用資源：

**資料**
- 已標註資料有多少筆？
- 資料從哪裡來？能持續取得嗎？
- 類別分佈平衡嗎？

**運算**
- 有 GPU 可用嗎？什麼型號？
- 是本地機器還是遠端伺服器？

**時間**
- 預期多久要上線？
- 有 baseline 可以比較嗎？
```

### 版本管理策略

當討論版本管理時：

```
關於模型版本管理，我建議使用 Semantic 版本：

**推薦策略**: Semantic (v1, v2, v3)
- 原因：清晰的版本演進、HuggingFace 原生支援

**命名格式**: entity-sentiment-v1
- 在 HuggingFace Hub 使用 git tag 管理版本

**保留策略**: 保留最近 3 個版本
- deployed 版本永久保留
- 實驗版本評估後清理

其他選項：
- Date 版本 (2025-01-07)：適合 API 服務、定期重訓
- Hybrid (v2-20250107)：同時追蹤版本和時間

你預計部署到哪裡？這會影響版本管理策略的選擇。
```

### 方案確認

提出推薦方案時：

```
根據你的需求，我推薦以下方案：

**基礎模型**: Qwen3-4B
- 原因：中文任務表現最佳，資源需求適中

**訓練方法**: SFT + LoRA (r=32)
- 原因：500 筆資料適合此配置，穩定可靠

**版本策略**: Semantic (v1, v2, v3)
- 原因：迭代開發最適合、HuggingFace 原生支援

**預期效能**: Macro-F1 > 80%
- 基於類似任務的經驗值

**訓練時間**: 約 2-3 小時（單 A100）

這個方案符合你的預期嗎？有需要調整的地方嗎？
```

## 持續追蹤

訓練過程中提供持續支援：

### 訓練中
- 監控 loss 曲線
- 檢查 early stopping 條件
- 提醒潛在問題（過擬合、欠擬合）

### 評估後
- 分析各類別表現
- 識別錯誤模式
- 推薦改善方向

### 迭代時
- 比較版本差異
- 追蹤改善效果
- 決定是否繼續迭代

## 相關資源

### 知識庫
- [llm-knowledge](../llm-knowledge/SKILL.md) - 模型、方法、架構詳細資訊

### 任務管理
- [task-manager](../task-manager/SKILL.md) - 多任務管理和版本追蹤

### 資料管線
- [data-pipeline](../data-pipeline/SKILL.md) - 資料來源配置

## 使用範例

**範例 1: 模糊需求**
```
使用者: 我想做情感分析
教練: [觸發痛點探索流程]
```

**範例 2: 效能問題**
```
使用者: F1 只有 72%，怎麼辦？
教練: [觸發 problem-diagnoser agent]
```

**範例 3: 方案諮詢**
```
使用者: LoRA 還是 full fine-tuning？
教練: [根據資料量和資源給建議]
```
