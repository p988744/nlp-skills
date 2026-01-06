# 問題排解索引

## 快速診斷

### 我的問題是...

| 症狀 | 可能原因 | 解決方案 |
|------|----------|----------|
| 準確率/F1 低 | 資料、模型或配置問題 | [low-accuracy.md](low-accuracy.md) |
| 某類別 F1 特別低 | 類別不平衡 | [class-imbalance.md](class-imbalance.md) |
| Train loss 低但 eval loss 高 | 過擬合 | [overfitting.md](overfitting.md) |
| Train/eval loss 都高 | 欠擬合 | [underfitting.md](underfitting.md) |
| CUDA OOM | 記憶體不足 | [oom.md](oom.md) |
| JSON 解析失敗 | 輸出格式錯誤 | [output-format.md](output-format.md) |
| 訓練 loss 震盪 | 學習率過高 | [training-instability.md](training-instability.md) |

## 問題分類

### 效能問題

| 問題 | 文件 |
|------|------|
| 整體效能低 | [low-accuracy.md](low-accuracy.md) |
| 類別不平衡 | [class-imbalance.md](class-imbalance.md) |
| 過擬合 | [overfitting.md](overfitting.md) |
| 欠擬合 | [underfitting.md](underfitting.md) |

### 訓練問題

| 問題 | 文件 |
|------|------|
| 記憶體不足 | [oom.md](oom.md) |
| 訓練不穩定 | [training-instability.md](training-instability.md) |

### 輸出問題

| 問題 | 文件 |
|------|------|
| 格式錯誤 | [output-format.md](output-format.md) |

## 通用診斷步驟

### 1. 檢查資料

```bash
# 資料量
wc -l data/train.jsonl data/valid.jsonl data/test.jsonl

# 類別分佈
python -c "
import json
from collections import Counter
with open('data/train.jsonl') as f:
    labels = [json.loads(l)['label'] for l in f]
print(Counter(labels))
"
```

### 2. 檢查訓練曲線

```python
# 查看 loss 變化
# train loss 應該平穩下降
# eval loss 不應該持續上升
```

### 3. 檢查預測結果

```python
# 分析錯誤模式
from collections import Counter
errors = [(p['expected'], p['prediction']) for p in predictions if p['expected'] != p['prediction']]
print(Counter(errors))
```

## 常見解決方案摘要

| 方案 | 效果 | 適用問題 |
|------|------|----------|
| 增加資料 | +5-15% | 資料不足 |
| 過採樣 | +3-8% | 類別不平衡 |
| 增加 LoRA rank | +2-5% | 欠擬合 |
| 減少 epochs | 穩定 | 過擬合 |
| 增加 dropout | 穩定 | 過擬合 |
| 降低 learning rate | 穩定 | 訓練不穩定 |
| 使用 QLoRA | 可執行 | OOM |

---

*更新: 2026-01*
