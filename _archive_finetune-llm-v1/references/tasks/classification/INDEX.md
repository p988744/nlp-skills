# 分類任務索引

## 概述

分類任務將輸入映射到預定義的標籤集合，是最常見也最容易上手的 NLP 任務。

## 任務類型

| 任務 | 說明 | 標籤範例 |
|------|------|----------|
| **情感分析** | 判斷文本情感傾向 | 正面/負面/中立 |
| **主題分類** | 分類文本主題 | 財經/科技/體育/娛樂 |
| **意圖識別** | 識別用戶意圖 | 查詢/投訴/購買/諮詢 |
| **垃圾郵件檢測** | 識別垃圾郵件 | 正常/垃圾 |

## 通用配置

### 資料格式

```jsonl
{"input": "這個產品真的很棒！", "output": "正面"}
{"input": "服務態度很差", "output": "負面"}
{"input": "產品還可以吧", "output": "中立"}
```

### 訓練配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"

lora:
  r: 32
  lora_alpha: 64

training:
  method: sft
  num_epochs: 5-8
  learning_rate: 1e-5
  per_device_train_batch_size: 4
```

## 評估指標

| 指標 | 說明 | 使用場景 |
|------|------|----------|
| **Accuracy** | 整體準確率 | 類別平衡時 |
| **Macro-F1** | 各類別 F1 平均 | 類別不平衡時（推薦）|
| **Weighted-F1** | 加權 F1 | 重視大類別 |
| **Per-class F1** | 各類別單獨 F1 | 分析弱點 |

## 常見問題

### 類別不平衡

見 [troubleshooting/class-imbalance.md](../../troubleshooting/class-imbalance.md)

### 預測偏向某類

- 檢查訓練數據分布
- 考慮加權採樣
- 調整 class weights

## 詳細指南

- [sentiment-analysis.md](sentiment-analysis.md) - 情感分析
- [topic.md](topic.md) - 主題分類
- [intent.md](intent.md) - 意圖識別

---

*更新: 2026-01*
