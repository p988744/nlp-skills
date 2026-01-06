# Phase 3: 準備資料

## 概述

將原始資料轉換為訓練所需的 chat format。

## 資料流程

```
原始資料 → 驗證 → 轉換 → 分割 → Chat Format
data/raw/    01_validate   02_convert   →   data/chat_format/
```

## 資料格式

### 原始格式 (data/raw/)

```jsonl
{"text": "公司營收創新高", "label": "正面"}
{"text": "股價大跌", "label": "負面"}
```

### Chat Format (data/chat_format/)

```jsonl
{
  "messages": [
    {"role": "system", "content": "你是情感分析專家..."},
    {"role": "user", "content": "請分析：公司營收創新高"},
    {"role": "assistant", "content": "正面"}
  ]
}
```

## 步驟

### Step 1: 驗證資料

```bash
python scripts/01_validate_data.py
```

驗證項目：
- JSON 格式正確性
- 必要欄位存在
- 標籤值合法性
- 類別分佈

輸出範例：
```
📄 data/raw/train.jsonl
   總筆數: 1000
   類別分佈: {'正面': 350, '負面': 330, '中立': 320}
   ✅ 驗證通過
```

### Step 2: 轉換格式

```bash
python scripts/02_convert_format.py
```

核心邏輯：
```python
def convert_to_chat_format(sample):
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"請分析以下文本的情感傾向：\n\n{sample['text']}"},
            {"role": "assistant", "content": sample['label']}
        ]
    }
```

### Step 3: 分割資料

建議比例：
| 資料集 | 比例 | 用途 |
|--------|------|------|
| Train | 70-80% | 訓練 |
| Valid | 10-15% | 驗證（調參、early stopping）|
| Test | 10-15% | 最終評估 |

## Prompt 設計

### 分類任務

```python
SYSTEM_PROMPT = """你是情感分析專家。請分析文本的情感傾向。

只能回答以下類別之一：正面、負面、中立

不要加入任何解釋或其他文字。"""

USER_TEMPLATE = """請分析以下文本的情感傾向：

{text}"""
```

### 抽取任務 (NER)

```python
SYSTEM_PROMPT = """你是命名實體識別專家。請識別文本中的實體。

實體類型：
- PER: 人物
- ORG: 組織
- LOC: 地點

請以 JSON 格式輸出。"""

USER_TEMPLATE = """請識別以下文本中的實體：

{text}"""

# 輸出
ASSISTANT_TEMPLATE = """{"entities": [{"text": "台積電", "type": "ORG"}]}"""
```

### 生成任務

```python
SYSTEM_PROMPT = """你是專業的公文撰寫助手。

請將口語化的文字轉換為正式公文格式。"""

USER_TEMPLATE = """請將以下內容轉換為公文格式：

原文：{text}
公文類型：{doc_type}
層級：{level}"""
```

## 資料品質檢查清單

- [ ] 類別分佈是否平衡？
- [ ] 標籤是否一致？
- [ ] 有無重複樣本？
- [ ] 文本長度分佈合理？
- [ ] 特殊字元處理正確？

## 常見問題

### 類別不平衡

見 [troubleshooting/class-imbalance.md](../references/troubleshooting/class-imbalance.md)

### 標籤不一致

```python
# 標準化標籤
label_mapping = {
    "positive": "正面",
    "正向": "正面",
    "好": "正面",
    # ...
}

def normalize_label(label):
    return label_mapping.get(label.lower(), label)
```

### 文本過長

```python
# 截斷或分段
MAX_LENGTH = 1000

def truncate_text(text, max_length=MAX_LENGTH):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
```

## 資料增強 (可選)

### 過採樣少數類別

```python
from collections import Counter

def oversample(data, target_count):
    label_counts = Counter(d['label'] for d in data)
    augmented = list(data)

    for label, count in label_counts.items():
        if count < target_count:
            samples = [d for d in data if d['label'] == label]
            while len([d for d in augmented if d['label'] == label]) < target_count:
                augmented.append(random.choice(samples))

    return augmented
```

### 同義詞替換

```python
import jieba

def synonym_augment(text, replace_prob=0.1):
    words = list(jieba.cut(text))
    # 隨機替換部分詞為同義詞
    return ''.join(augmented_words)
```

## 驗證轉換結果

```python
# 確認 chat template 正確
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")

with open("data/chat_format/train.jsonl") as f:
    sample = json.loads(f.readline())

prompt = tokenizer.apply_chat_template(
    sample['messages'],
    tokenize=False,
    add_generation_prompt=False
)
print(prompt)
```

## 下一步

資料準備完成後進入 [Phase 4: 訓練模型](04-training.md)

---

*更新: 2026-01*
