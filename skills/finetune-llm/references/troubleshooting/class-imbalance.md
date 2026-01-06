# 類別不平衡問題

## 症狀

- 某個類別的 F1 明顯低於其他類別
- 少數類別的 Recall 特別低
- 模型傾向預測多數類別

## 診斷

### 檢查類別分佈

```python
import json
from collections import Counter

with open('data/train.jsonl') as f:
    labels = [json.loads(line)['label'] for line in f]

distribution = Counter(labels)
print("類別分佈:", distribution)

# 計算不平衡比例
max_count = max(distribution.values())
min_count = min(distribution.values())
imbalance_ratio = max_count / min_count

print(f"不平衡比例: {imbalance_ratio:.1f}x")

if imbalance_ratio > 3:
    print("⚠️ 類別不平衡嚴重")
```

### 不平衡程度判斷

| 比例 | 嚴重程度 | 建議處理 |
|------|----------|----------|
| < 2x | 輕微 | 可不處理 |
| 2-5x | 中等 | 過採樣或加權 |
| > 5x | 嚴重 | 必須處理 |

## 解決方案

### 方案 1: 過採樣 (Oversampling)

適用：不平衡 < 5x

```python
import random
from collections import Counter

def oversample(data, target_count=None):
    """過採樣少數類別"""
    labels = [item['label'] for item in data]
    distribution = Counter(labels)

    if target_count is None:
        target_count = max(distribution.values())

    result = []
    for label in distribution:
        items = [d for d in data if d['label'] == label]
        # 重複採樣直到達到目標數量
        while len(items) < target_count:
            items.append(random.choice([d for d in data if d['label'] == label]))
        result.extend(items[:target_count])

    random.shuffle(result)
    return result

# 使用
balanced_data = oversample(train_data)
```

### 方案 2: 加權損失函數

適用：不平衡 3-10x

```python
import torch
from torch import nn

# 計算類別權重（反比於數量）
class_counts = torch.tensor([count_pos, count_neg, count_neutral])
weights = 1.0 / class_counts
weights = weights / weights.sum()  # 正規化

criterion = nn.CrossEntropyLoss(weight=weights)
```

或在配置中指定：

```yaml
training:
  class_weights:
    正面: 1.0
    負面: 1.2
    中立: 1.5  # 少數類別給更高權重
```

### 方案 3: 資料增強 (GPT 生成)

適用：不平衡 > 10x

```python
def generate_minority_samples(seed_samples, target_class, num_new=100):
    """使用 GPT 生成少數類別樣本"""

    prompt = f"""根據以下「{target_class}」類別的範例，生成新的類似樣本：

範例：
{json.dumps(seed_samples[:5], ensure_ascii=False, indent=2)}

請生成 {num_new} 個新樣本，確保：
1. 保持相同的類別（{target_class}）
2. 內容多樣化
3. 符合真實場景

以 JSONL 格式回覆，每行一個樣本。"""

    # 調用 GPT API 生成
    # ... (需人工審核)
```

### 方案 4: Focal Loss

適用：極度不平衡

```python
class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        return focal_loss.mean()
```

## 效果預期

| 方案 | 預期提升 | 複雜度 |
|------|----------|--------|
| 過採樣 | +3-8% F1 | 低 |
| 加權損失 | +2-5% F1 | 低 |
| GPT 生成 | +5-15% F1 | 中 |
| Focal Loss | +3-8% F1 | 中 |

## 驗證改善

```python
from sklearn.metrics import classification_report

# 處理前
print("處理前:")
print(classification_report(y_true, y_pred_before))

# 處理後
print("處理後:")
print(classification_report(y_true, y_pred_after))

# 重點關注少數類別的 F1 變化
```

## 注意事項

1. **過採樣風險**: 可能導致過擬合，建議配合 dropout
2. **GPT 生成**: 必須人工審核品質
3. **權重設定**: 過高權重可能影響多數類別效能
4. **混合使用**: 可同時使用多種方案

## 相關

- [low-accuracy.md](low-accuracy.md) - 其他準確率問題
- [overfitting.md](overfitting.md) - 過採樣可能導致過擬合

---

*更新: 2026-01*
