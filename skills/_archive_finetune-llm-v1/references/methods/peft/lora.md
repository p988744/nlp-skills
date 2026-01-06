# LoRA (Low-Rank Adaptation)

## 概述

LoRA 透過低秩分解減少可訓練參數達 99%，讓你在單一 GPU 上微調大型模型。

**核心公式**: `W' = W + AB^T` (rank r << dim)

## 原理

```
原始權重 W (frozen)
      │
      ▼
  ┌───────┐
  │   +   │ ← 新增低秩矩陣 A·B^T
  └───────┘
      │
      ▼
更新後 W' = W + AB^T
```

- **A**: shape (d, r) - 降維
- **B**: shape (r, d) - 升維
- **r**: rank，通常 8-64

## 推薦配置

### 標準配置

```yaml
lora:
  r: 32
  lora_alpha: 64      # 通常 = 2 * r
  lora_dropout: 0.05
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj
```

### Rank 選擇指南

| 任務複雜度 | 建議 Rank | 可訓練參數 |
|-----------|-----------|-----------|
| 簡單（分類）| 16 | ~33M |
| 中等（NER）| 32 | ~66M |
| 複雜（生成）| 64 | ~132M |

### 模型大小 vs Rank

| 模型大小 | 建議 Rank |
|----------|-----------|
| ≤ 4B | 16-32 |
| 7-8B | 32-64 |
| > 14B | 64-128 |

## Target Modules

### Qwen 系列

```yaml
target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj
```

### Llama 系列

```yaml
target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj
```

## 程式碼範例

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    lora_dropout=0.05,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
# trainable params: 66,846,720 || all params: 4,156,878,848 || trainable%: 1.6082
```

## 優點

- ✅ 大幅減少記憶體需求
- ✅ 訓練速度快
- ✅ 可堆疊多個 adapter
- ✅ 推理時可合併，無額外延遲

## 缺點

- ❌ 效果略低於 Full Fine-tuning
- ❌ 需要選擇合適的 rank

## 常見問題

### 效果不如預期

```yaml
# 嘗試增加 rank
r: 64
lora_alpha: 128

# 或增加 target modules
target_modules: all-linear
```

### 過擬合

```yaml
# 增加 dropout
lora_dropout: 0.1

# 或減少 epochs
num_epochs: 3
```

## 與其他方法比較

| 方法 | 記憶體 | 效果 | 速度 |
|------|--------|------|------|
| Full FT | 100% | 最佳 | 慢 |
| **LoRA** | ~20% | 好 | 快 |
| QLoRA | ~10% | 好 | 較慢 |
| DoRA | ~25% | 更好 | 快 |

## 相關

- [qlora.md](qlora.md) - 加入量化進一步減少記憶體
- [dora.md](dora.md) - 改良版 LoRA

---

*更新: 2026-01*
