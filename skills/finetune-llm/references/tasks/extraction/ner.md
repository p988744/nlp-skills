# 命名實體識別 (Named Entity Recognition)

## 概述

NER 從文本中識別命名實體（人名、地名、組織等）及其類型。

## 常見實體類型

### 通用類型

| 類型 | 縮寫 | 範例 |
|------|------|------|
| 人物 | PER | 張忠謀、馬斯克 |
| 組織 | ORG | 台積電、蘋果公司 |
| 地點 | LOC | 台北、矽谷 |
| 時間 | TIME | 2025年、下週一 |
| 金額 | MONEY | 1000萬、$500 |

### 領域特定類型

**法律領域**:
| 類型 | 說明 | 範例 |
|------|------|------|
| PARTY | 當事人 | 原告王大明 |
| COURT | 法院 | 臺北地方法院 |
| JUDGE | 法官 | 審判長李小華 |
| LAW | 法條 | 刑法第339條 |

**金融領域**:
| 類型 | 說明 | 範例 |
|------|------|------|
| STOCK | 股票 | 2330台積電 |
| INDEX | 指數 | 台股加權指數 |
| INDICATOR | 財務指標 | EPS、毛利率 |

## 資料格式

### JSON 格式 (推薦)

```jsonl
{
  "input": "台積電董事長張忠謀宣布將在日本建廠",
  "output": {
    "entities": [
      {"text": "台積電", "type": "ORG", "start": 0, "end": 3},
      {"text": "張忠謀", "type": "PER", "start": 5, "end": 8},
      {"text": "日本", "type": "LOC", "start": 13, "end": 15}
    ]
  }
}
```

### Chat 格式

```jsonl
{
  "messages": [
    {"role": "system", "content": "你是NER專家，請識別文本中的實體。"},
    {"role": "user", "content": "請識別：台積電董事長張忠謀宣布將在日本建廠"},
    {"role": "assistant", "content": "{\"entities\": [{\"text\": \"台積電\", \"type\": \"ORG\"}, {\"text\": \"張忠謀\", \"type\": \"PER\"}, {\"text\": \"日本\", \"type\": \"LOC\"}]}"}
  ]
}
```

## 訓練配置

### 標準配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"

lora:
  r: 32
  lora_alpha: 64
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

training:
  method: sft
  num_epochs: 5
  learning_rate: 1e-5
  per_device_train_batch_size: 2
  max_seq_length: 2048
```

### 資料量建議

| 實體類型數 | 建議樣本數 | 說明 |
|------------|------------|------|
| 3-5 類 | 500-1000 | 常見類型 |
| 5-10 類 | 1000-2000 | 領域特定 |
| 10+ 類 | 2000-5000 | 複雜場景 |

## Prompt 設計

### 簡單 Prompt

```
識別以下文本中的命名實體，包括人物(PER)、組織(ORG)、地點(LOC)。

文本：{text}

以 JSON 格式輸出。
```

### 詳細 Prompt (帶說明)

```
你是命名實體識別專家。請識別以下文本中的實體。

實體類型定義：
- PER (人物): 人名、稱謂
- ORG (組織): 公司、政府機構、組織
- LOC (地點): 國家、城市、地址

文本：{text}

請以 JSON 格式輸出：{"entities": [{"text": "實體文字", "type": "類型"}]}
```

## 評估指標

### 標準評估

```python
def evaluate_ner(predictions, references):
    """
    實體級別的 F1 評估
    要求：實體文字和類型都必須匹配
    """
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for pred, ref in zip(predictions, references):
        pred_set = set((e['text'], e['type']) for e in pred['entities'])
        ref_set = set((e['text'], e['type']) for e in ref['entities'])

        true_positives += len(pred_set & ref_set)
        false_positives += len(pred_set - ref_set)
        false_negatives += len(ref_set - pred_set)

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    f1 = 2 * precision * recall / (precision + recall)

    return {'precision': precision, 'recall': recall, 'f1': f1}
```

### 評估層級

| 層級 | 說明 | 嚴格度 |
|------|------|--------|
| 精確匹配 | 文字+類型都對 | 最嚴格 |
| 類型匹配 | 允許邊界偏移 | 中等 |
| 部分匹配 | 重疊即可 | 寬鬆 |

## 常見問題

### 1. 實體邊界錯誤

**症狀**: "台積電公司" vs "台積電"
**解決**:
- 統一標註標準
- 增加相似樣本
- 在 prompt 中明確邊界規則

### 2. 嵌套實體

**範例**: "台北市政府" (地點+組織)
**解決**:
- 定義優先級規則
- 使用多標籤格式
- 分開識別不同層級

### 3. 新實體識別差

**症狀**: 訓練集沒出現的實體識別不到
**解決**:
- 增加實體多樣性
- 使用實體替換增強
- 考慮 few-shot 提示

### 4. JSON 格式錯誤

**症狀**: 輸出 JSON 格式不合法
**解決**:
- 增加格式範例
- 後處理修復
- 驗證並重試

## 資料增強

### 實體替換

```python
def augment_by_entity_swap(sample, entity_dict):
    """將實體替換為同類型的其他實體"""
    text = sample['input']
    for entity in sample['output']['entities']:
        if entity['type'] in entity_dict:
            replacement = random.choice(entity_dict[entity['type']])
            text = text.replace(entity['text'], replacement)
    return text
```

### 上下文擴展

```python
def augment_by_context(sample, templates):
    """添加上下文模板"""
    text = sample['input']
    template = random.choice(templates)
    return template.format(text=text)
```

## 資料集資源

### 中文

| 資料集 | 領域 | 實體類型 |
|--------|------|----------|
| MSRA NER | 新聞 | PER, LOC, ORG |
| Weibo NER | 社群 | PER, LOC, ORG, GPE |
| Resume NER | 履歷 | 學歷、技能等 |
| CLUENER | 多領域 | 10 類 |

### 英文

| 資料集 | 領域 | 實體類型 |
|--------|------|----------|
| CoNLL-2003 | 新聞 | PER, LOC, ORG, MISC |
| OntoNotes | 多領域 | 18 類 |
| Few-NERD | Few-shot | 66 細類 |

## 相關

- [relation.md](relation.md) - 關係抽取（NER 的下一步）
- [sft.md](../../methods/finetuning/sft.md) - SFT 訓練
- [class-imbalance.md](../../troubleshooting/class-imbalance.md) - 實體類型不平衡

---

*更新: 2026-01*
