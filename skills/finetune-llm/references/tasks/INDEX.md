# 任務類型索引

## 任務分類

```
tasks/
├── classification/          # 分類任務
│   ├── sentiment-analysis   # 情感分析
│   ├── topic-classification # 主題分類
│   └── intent-detection     # 意圖識別
│
├── extraction/              # 抽取任務
│   ├── ner                  # 命名實體識別
│   ├── relation-extraction  # 關係抽取
│   └── event-extraction     # 事件抽取
│
├── generation/              # 生成任務
│   ├── summarization        # 摘要
│   ├── style-transfer       # 風格轉換
│   └── document-formatting  # 文件格式化
│
├── understanding/           # 理解任務
│   ├── reading-comprehension # 閱讀理解
│   ├── qa                   # 問答
│   └── stance-detection     # 立場分析
│
└── dialogue/                # 對話任務
    ├── chatbot              # 聊天機器人
    └── task-oriented        # 任務型對話
```

## 快速選擇

| 任務 | 推薦方法 | 資料量建議 | 難度 |
|------|----------|------------|------|
| 情感分析 | SFT + LoRA | 500-2000 | ⭐ |
| NER | SFT + LoRA | 500-2000 | ⭐⭐ |
| 主題分類 | SFT + LoRA | 300-1000 | ⭐ |
| 風格轉換 | ORPO | 200-500 配對 | ⭐⭐ |
| 關係抽取 | SFT + LoRA | 1000-3000 | ⭐⭐⭐ |

## 詳細指南

### 分類任務
- [classification/sentiment-analysis.md](classification/sentiment-analysis.md) - 情感分析
- [classification/topic.md](classification/topic.md) - 主題分類
- [classification/intent.md](classification/intent.md) - 意圖識別

### 抽取任務
- [extraction/ner.md](extraction/ner.md) - 命名實體識別
- [extraction/relation.md](extraction/relation.md) - 關係抽取
- [extraction/event.md](extraction/event.md) - 事件抽取

### 生成任務
- [generation/style-transfer.md](generation/style-transfer.md) - 風格轉換
- [generation/document-formatting.md](generation/document-formatting.md) - 文件格式化

### 理解任務
- [understanding/stance-detection.md](understanding/stance-detection.md) - 立場分析

## 任務特點

### 分類 vs 生成

| 特性 | 分類任務 | 生成任務 |
|------|----------|----------|
| 輸出形式 | 固定標籤 | 自由文本 |
| 評估指標 | F1, Accuracy | BLEU, ROUGE, 人工 |
| 訓練複雜度 | 低 | 中-高 |
| 資料需求 | 相對少 | 相對多 |
| 對齊需求 | 通常不需要 | 可能需要 |

### 本專案已實現任務

| 任務 | 狀態 | 效能 |
|------|------|------|
| 金融情感分析 | ✅ | 89.8% |
| 公文格式轉換 | ✅ | 100% |
| 立場分析 | ✅ | 82.3% |
| 實體情感 | ✅ | 72.0% |
| 法律資訊抽取 | ✅ | 66.5% |

---

*更新: 2026-01*
