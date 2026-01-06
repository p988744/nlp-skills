# ORPO (Odds Ratio Preference Optimization)

## 概述

ORPO 是一種高效的偏好對齊方法，在單一訓練階段同時完成 SFT 和偏好對齊。

**核心優勢**: 不需要參考模型，訓練效率高

## 原理

```
傳統流程: SFT → DPO (需要參考模型)
ORPO 流程: 一步完成 (SFT + 偏好對齊)
```

### 損失函數

```
L_ORPO = L_SFT + β * L_OR

L_SFT: 標準 SFT 損失（chosen 樣本）
L_OR: Odds Ratio 損失（偏好對比）
```

Odds Ratio 衡量 chosen 相對於 rejected 的優勢比。

## 資料格式

```jsonl
{"prompt": "請分析這段文字的情感", "chosen": "這段文字表達正面情感...", "rejected": "情感是正的"}
{"prompt": "將以下口語轉換為公文", "chosen": "依據...函請查照", "rejected": "請看一下這個..."}
```

### 資料準備要點

1. **chosen**: 高品質、符合期望的回應
2. **rejected**: 低品質但合理的回應（不是亂碼）
3. **對比明確**: 兩者差異應該清晰

## 訓練配置

### 標準配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"

orpo:
  beta: 0.1  # 偏好損失權重

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
  learning_rate: 5e-6  # 比 SFT 低
  warmup_ratio: 0.1
  max_seq_length: 2048
```

### 使用 TRL

```python
from trl import ORPOTrainer, ORPOConfig
from peft import LoraConfig

# ORPO 配置
orpo_config = ORPOConfig(
    output_dir="./orpo_output",
    beta=0.1,
    learning_rate=5e-6,
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
trainer = ORPOTrainer(
    model=model,
    args=orpo_config,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    peft_config=lora_config,
    tokenizer=tokenizer,
)

trainer.train()
```

## 超參數調整

### beta (偏好權重)

| beta 值 | 效果 | 適用場景 |
|---------|------|----------|
| 0.05 | 弱偏好對齊 | 偏好差異小 |
| 0.1 | 標準 (預設) | 一般任務 |
| 0.2 | 強偏好對齊 | 偏好差異大 |

### 學習率

- 建議: 5e-6 ~ 2e-5
- 比純 SFT 低，避免過度擬合偏好

## 與 DPO 比較

| 特性 | ORPO | DPO |
|------|------|-----|
| 需要參考模型 | ❌ | ✅ |
| 訓練階段 | 1 | 2 (SFT → DPO) |
| 訓練時間 | 較短 | 較長 |
| 穩定性 | 中等 | 高 |
| 記憶體需求 | 較低 | 較高 |
| 偏好漂移風險 | 有 | 低 |

## 常見問題

### 1. 偏好漂移

**症狀**: 訓練後模型「太偏好」某種風格
**解決**: 降低 beta 或增加訓練數據多樣性

### 2. 訓練不穩定

**症狀**: Loss 波動大
**解決**:
- 降低學習率
- 增加 gradient accumulation
- 確保 chosen/rejected 差異明確

### 3. 品質下降

**症狀**: 輸出品質反而下降
**解決**:
- 檢查 rejected 樣本品質（不應是亂碼）
- 增加 SFT 階段比重

## 適用場景

### 推薦使用 ORPO

- ✅ 公文格式轉換（明確對錯標準）
- ✅ 風格控制任務
- ✅ 有配對偏好數據
- ✅ 計算資源有限

### 不推薦 ORPO

- ❌ 分類任務（SFT 就夠）
- ❌ 沒有明確偏好對比
- ❌ 需要極高穩定性

## 實際案例

### 公文轉換 ORPO 訓練

```yaml
# configs/official_doc/orpo_config.yaml
model:
  base_model: "Qwen/Qwen3-4B"

orpo:
  beta: 0.1

data:
  # chosen: 正確公文用語
  # rejected: 錯誤公文用語（但格式合理）
  train_file: "data/official_doc/orpo_train.jsonl"

training:
  num_train_epochs: 3
  learning_rate: 5e-6
```

結果: 公文用語準確率從 60% 提升到 100%

## 相關

- [dpo.md](dpo.md) - 需要更高穩定性時
- [sft.md](../finetuning/sft.md) - 基礎 SFT
- [lora.md](../peft/lora.md) - LoRA 配置

---

*更新: 2026-01*
