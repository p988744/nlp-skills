# 過擬合 (Overfitting)

## 症狀

- 訓練 Loss 持續下降
- 驗證 Loss 先降後升
- 訓練集效能 >> 測試集效能
- 模型記憶訓練樣本，缺乏泛化能力

## 診斷

```python
# 檢查訓練曲線
import matplotlib.pyplot as plt

plt.plot(train_losses, label='Train')
plt.plot(eval_losses, label='Eval')
plt.legend()
plt.title('Loss Curves')

# 過擬合信號：eval loss 拐點後上升
```

### 過擬合判定標準

| 情況 | 判定 |
|------|------|
| Eval Loss 上升 > 2 epoch | 輕度過擬合 |
| Eval Loss 上升 > 5 epoch | 嚴重過擬合 |
| Train 95% / Eval 70% | 明顯過擬合 |

## 解決方案

### 1. 減少訓練 Epoch

最簡單有效的方法：

```yaml
training:
  num_train_epochs: 3  # 從 8 減到 3
  # 或使用 early stopping
```

### 2. Early Stopping

```python
from transformers import EarlyStoppingCallback

trainer = Trainer(
    ...
    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=3,  # 3 epoch 無改善就停
            early_stopping_threshold=0.01
        )
    ]
)
```

### 3. 降低 LoRA Rank

```yaml
lora:
  r: 16  # 從 32 降到 16
  lora_alpha: 32  # 相應調整
```

| Rank | 參數量 | 過擬合風險 |
|------|--------|------------|
| 8 | 最少 | 低 |
| 16 | 少 | 低-中 |
| 32 | 中 | 中 |
| 64 | 多 | 高 |

### 4. 增加 Dropout

```yaml
lora:
  lora_dropout: 0.1  # 從 0.05 增加到 0.1
```

### 5. 降低學習率

```yaml
training:
  learning_rate: 5e-6  # 從 1e-5 降到 5e-6
```

### 6. 增加訓練數據

根本解決方案：增加更多高品質訓練數據。

```
資料量經驗法則：
- 參數量 / 1000 ≈ 最小資料量
- 4B 模型建議 >= 500 樣本
- 資料品質 > 資料數量
```

### 7. 數據增強

```python
# 同義詞替換
def synonym_augment(text):
    # 隨機替換同義詞
    pass

# 回譯增強
def back_translation_augment(text):
    # 翻譯到其他語言再翻回來
    pass

# 隨機刪除
def random_deletion_augment(text, p=0.1):
    words = text.split()
    return ' '.join([w for w in words if random.random() > p])
```

### 8. 正則化

```yaml
training:
  weight_decay: 0.01  # L2 正則化
  max_grad_norm: 1.0  # 梯度裁剪
```

### 9. 減少訓練目標模組

```yaml
lora:
  target_modules:
    - q_proj
    - v_proj
    # 移除其他模組，減少可訓練參數
```

## 預防措施

### 1. 監控訓練過程

```yaml
training:
  evaluation_strategy: "steps"
  eval_steps: 50  # 頻繁評估
  logging_steps: 10
  save_strategy: "steps"
  save_steps: 50
  load_best_model_at_end: true  # 載入最佳模型
```

### 2. 使用驗證集

**永遠**保留獨立的驗證集：

```
資料切分建議：
- Train: 70-80%
- Valid: 10-15%
- Test: 10-15%
```

### 3. 交叉驗證

對於小數據集：

```python
from sklearn.model_selection import KFold

kfold = KFold(n_splits=5, shuffle=True)
for fold, (train_idx, val_idx) in enumerate(kfold.split(data)):
    # 訓練並記錄每個 fold 的效能
    pass
```

## 配置範本

### 防過擬合配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"

lora:
  r: 16  # 較小的 rank
  lora_alpha: 32
  lora_dropout: 0.1  # 較高的 dropout
  target_modules:
    - q_proj
    - v_proj  # 只訓練必要模組

training:
  num_train_epochs: 3  # 較少 epoch
  learning_rate: 5e-6  # 較低學習率
  weight_decay: 0.01
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  warmup_ratio: 0.1
  evaluation_strategy: "steps"
  eval_steps: 50
  save_strategy: "steps"
  save_steps: 50
  load_best_model_at_end: true
```

## 相關

- [low-accuracy.md](low-accuracy.md) - 欠擬合問題
- [lora.md](../methods/peft/lora.md) - LoRA rank 選擇
- [sft.md](../methods/finetuning/sft.md) - SFT 超參數

---

*更新: 2026-01*
