# 抽取任務索引

## 概述

抽取任務從非結構化文本中提取結構化資訊，包括實體、關係和事件。

## 任務類型

| 任務 | 說明 | 輸出範例 |
|------|------|----------|
| **NER** | 命名實體識別 | [台積電:ORG, 張忠謀:PER] |
| **關係抽取** | 實體間關係 | (張忠謀, 創辦, 台積電) |
| **事件抽取** | 事件及參與者 | Event(投資, Agent=台積電, Target=日本廠) |

## 難度排序

```
NER (⭐) < 關係抽取 (⭐⭐⭐) < 事件抽取 (⭐⭐⭐⭐)
```

## 輸出格式

### 結構化 JSON (推薦)

```json
{
  "entities": [
    {"text": "台積電", "type": "ORG", "start": 0, "end": 3},
    {"text": "張忠謀", "type": "PER", "start": 10, "end": 13}
  ],
  "relations": [
    {"head": "張忠謀", "tail": "台積電", "type": "創辦"}
  ]
}
```

### 簡化格式 (入門)

```
實體：台積電(公司)、張忠謀(人物)
關係：張忠謀-創辦-台積電
```

## 訓練配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"

lora:
  r: 32  # 抽取任務建議較高 rank
  lora_alpha: 64

training:
  method: sft
  num_epochs: 5-8
  learning_rate: 1e-5
  max_seq_length: 2048  # 長文本需要更大
```

## 評估指標

| 任務 | 指標 | 說明 |
|------|------|------|
| NER | Entity F1 | 實體邊界+類型都對 |
| 關係抽取 | Relation F1 | 三元組完全匹配 |
| 事件抽取 | Argument F1 | 事件論元識別 |

## 詳細指南

- [ner.md](ner.md) - 命名實體識別
- [relation.md](relation.md) - 關係抽取
- [event.md](event.md) - 事件抽取

---

*更新: 2026-01*
