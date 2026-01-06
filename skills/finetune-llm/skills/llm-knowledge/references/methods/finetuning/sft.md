# SFT (Supervised Fine-Tuning)

## 概述

SFT 是最直接的微調方法，使用輸入-輸出配對資料訓練模型。

## 適用場景

✅ **適合**:
- 分類任務（情感、意圖、主題）
- 結構化輸出（JSON 格式）
- NER、關係抽取
- 有明確正確答案的任務

❌ **不適合**:
- 需要偏好對齊的生成任務
- 開放式創意寫作
- 複雜對話系統

## 資料格式

### Chat Format (推薦)

```jsonl
{
  "messages": [
    {"role": "system", "content": "你是情感分析助手..."},
    {"role": "user", "content": "分析這段文字的情感：台積電股價大漲"},
    {"role": "assistant", "content": "{\"sentiment\": \"正面\"}"}
  ]
}
```

### Instruction Format

```jsonl
{
  "instruction": "分析這段文字的情感",
  "input": "台積電股價大漲",
  "output": "{\"sentiment\": \"正面\"}"
}
```

## 推薦配置

### 基本配置

```yaml
training:
  method: "sft"
  num_epochs: 5-8
  learning_rate: 1e-5
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  warmup_ratio: 0.1
  weight_decay: 0.01
  max_seq_length: 2048
```

### 根據資料量調整

| 資料量 | Epochs | Learning Rate |
|--------|--------|---------------|
| < 500 | 8-10 | 1e-5 |
| 500-2000 | 5-8 | 1e-5 |
| 2000-5000 | 3-5 | 5e-6 |
| > 5000 | 2-3 | 5e-6 |

## 訓練框架

### 使用 TRL SFTTrainer

```python
from trl import SFTTrainer, SFTConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig

# 載入模型
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-4B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")

# LoRA 配置
peft_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
)

# 訓練配置
training_args = SFTConfig(
    output_dir="./output",
    num_train_epochs=5,
    per_device_train_batch_size=4,
    learning_rate=1e-5,
    logging_steps=10,
    save_strategy="epoch",
)

# 訓練
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    peft_config=peft_config,
)

trainer.train()
```

## 常見問題

### 過擬合

**症狀**: train loss 低，eval loss 高

```yaml
# 解決方案
lora_dropout: 0.1        # 增加 dropout
num_epochs: 3            # 減少 epochs
weight_decay: 0.05       # 增加正則化
```

### 欠擬合

**症狀**: train/eval loss 都高

```yaml
# 解決方案
r: 64                    # 增加 LoRA rank
num_epochs: 10           # 增加 epochs
learning_rate: 2e-5      # 提高學習率
```

### 輸出格式錯誤

**症狀**: JSON 解析失敗

```yaml
# 解決方案
# 1. 確保訓練資料格式一致
# 2. 增加相關樣本
# 3. 使用結構化 prompt
```

## 資料量與效能

| 資料量 | 預期效能 | 說明 |
|--------|----------|------|
| 100-500 | 70-80% | 最小可用 |
| 500-2000 | 80-88% | 建議量 |
| 2000-10000 | 88-92% | 生產品質 |
| 10000+ | 92%+ | 頂尖效能 |

## 最佳實踐

1. **資料品質優先**: 5-20K 高品質樣本勝過 200K 嘈雜資料
2. **Chat Template 一致**: 訓練和推理使用相同的模板
3. **混合通用資料**: 防止災難性遺忘
4. **早停**: 監控 eval loss，避免過擬合

## 與其他方法比較

| 方法 | 複雜度 | 資料需求 | 效果 |
|------|--------|----------|------|
| **SFT** | 低 | 輸入-輸出對 | 基礎 |
| SFT + DPO | 中 | + 偏好對 | 更好 |
| ORPO | 中 | 偏好對 | 一步完成 |

## 下一步

- 效果不足？考慮 [ORPO](../alignment/orpo.md) 或 [DPO](../alignment/dpo.md)
- 記憶體不足？參考 [QLoRA](../peft/qlora.md)

---

*更新: 2026-01*
