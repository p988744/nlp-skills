# DPO (Direct Preference Optimization)

## 概述

DPO 是經典的偏好對齊方法，通過直接優化偏好來調整模型輸出，無需強化學習。

**核心優勢**: 穩定可控，偏好漂移風險低

## 原理

DPO 將 RLHF 的獎勵建模和策略優化合併為單一目標：

```
L_DPO = -log σ(β * (log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)))

π: 訓練中的模型
π_ref: 參考模型（通常是 SFT 後的模型）
y_w: 偏好回應 (chosen)
y_l: 非偏好回應 (rejected)
β: 溫度參數
```

### 訓練流程

```
1. SFT 訓練 → 得到基礎模型
2. 複製為參考模型 (凍結)
3. DPO 訓練 (使用配對數據)
```

## 資料格式

```jsonl
{"prompt": "問題", "chosen": "優質回應", "rejected": "次優回應"}
```

### 資料準備要點

1. **配對要求**: 同一 prompt 必須有對應的 chosen 和 rejected
2. **品質差異**: 兩者差異應該明確但不極端
3. **覆蓋面**: 涵蓋各種場景和邊界情況

## 訓練配置

### 標準配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"
  # DPO 需要先有 SFT 模型
  sft_model: "path/to/sft_model"

dpo:
  beta: 0.1  # 溫度參數

lora:
  r: 16
  lora_alpha: 32
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

training:
  num_train_epochs: 3
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
  learning_rate: 1e-6  # DPO 需要很低的學習率
  warmup_ratio: 0.1
  max_seq_length: 2048
```

### 使用 TRL

```python
from trl import DPOTrainer, DPOConfig
from peft import LoraConfig
from transformers import AutoModelForCausalLM

# 載入 SFT 模型作為參考
model = AutoModelForCausalLM.from_pretrained("path/to/sft_model")
ref_model = AutoModelForCausalLM.from_pretrained("path/to/sft_model")

# DPO 配置
dpo_config = DPOConfig(
    output_dir="./dpo_output",
    beta=0.1,
    learning_rate=1e-6,  # 很低的學習率
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    warmup_ratio=0.1,
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="epoch",
)

# LoRA 配置
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# 訓練
trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,  # DPO 需要參考模型
    args=dpo_config,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    peft_config=lora_config,
    tokenizer=tokenizer,
)

trainer.train()
```

## 超參數調整

### beta (溫度參數)

| beta 值 | 效果 | 適用場景 |
|---------|------|----------|
| 0.05 | 弱偏好約束 | 細微風格調整 |
| 0.1 | 標準 (預設) | 一般偏好對齊 |
| 0.5 | 強偏好約束 | 嚴格偏好控制 |

**注意**: beta 過高會導致過度正則化

### 學習率

- **推薦**: 1e-6 ~ 5e-6
- 比 SFT/ORPO 更低
- 過高會破壞 SFT 學到的知識

## 與 ORPO 比較

| 特性 | DPO | ORPO |
|------|-----|------|
| 需要 SFT 前置 | ✅ | ❌ |
| 需要參考模型 | ✅ | ❌ |
| 訓練階段 | 2 | 1 |
| 記憶體需求 | 較高 (載入兩個模型) | 較低 |
| 穩定性 | ⭐⭐⭐ | ⭐⭐ |
| 偏好控制精度 | 高 | 中 |

## 常見問題

### 1. 過度正則化

**症狀**: 模型輸出變得過於保守或重複
**原因**: beta 過高或訓練過久
**解決**:
```yaml
dpo:
  beta: 0.05  # 降低 beta
training:
  num_train_epochs: 2  # 減少 epoch
```

### 2. 偏好未生效

**症狀**: 訓練後模型行為變化不大
**原因**: 學習率過低或 beta 過低
**解決**:
- 檢查 chosen/rejected 差異是否明確
- 適度提高學習率或 beta

### 3. 記憶體不足

**症狀**: OOM (Out of Memory)
**原因**: 需要同時載入模型和參考模型
**解決**:
```python
# 使用 PEFT 減少記憶體
trainer = DPOTrainer(
    model=model,
    ref_model=None,  # 使用隱式參考模型
    args=dpo_config,
    peft_config=lora_config,  # 只訓練 LoRA
    ...
)
```

### 4. SFT 知識遺忘

**症狀**: DPO 後基礎能力下降
**解決**:
- 混入部分 SFT 數據
- 降低學習率
- 減少訓練 epoch

## 適用場景

### 推薦使用 DPO

- ✅ 需要精確偏好控制
- ✅ 已有高品質 SFT 模型
- ✅ 有充足計算資源
- ✅ 需要穩定可預測的訓練

### 不推薦 DPO

- ❌ 沒有 SFT 模型
- ❌ 計算資源有限
- ❌ 偏好數據品質不高
- ❌ 簡單分類任務

## 進階技巧

### 1. 混合 SFT Loss

```python
# DPO + SFT 混合訓練
dpo_config = DPOConfig(
    ...
    sft_weight=0.1,  # 加入 SFT 損失
)
```

### 2. Reference-Free DPO

使用 PEFT 時可省略參考模型：

```python
trainer = DPOTrainer(
    model=model,
    ref_model=None,  # TRL 會使用初始 LoRA 作為隱式參考
    peft_config=lora_config,
    ...
)
```

### 3. 多輪 DPO

```
SFT → DPO (輪次 1) → DPO (輪次 2) → ...
```

每輪使用新的偏好數據，逐步改善。

## 相關

- [orpo.md](orpo.md) - 更輕量的替代方案
- [sft.md](../finetuning/sft.md) - DPO 前置步驟
- [lora.md](../peft/lora.md) - 減少記憶體需求

---

*更新: 2026-01*
