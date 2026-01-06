# Phase 4: 訓練模型

## 概述

使用準備好的資料進行 LoRA 微調訓練。

## 執行訓練

### 本地訓練

```bash
python scripts/03_train.py
```

### 遠端訓練 (GPU 服務器)

```bash
# 同步資料
rsync -avz tasks/{task_name}/ user@server:~/tasks/{task_name}/

# 執行訓練
ssh user@server "cd ~/tasks/{task_name} && \
    source ~/.venv/bin/activate && \
    CUDA_VISIBLE_DEVICES=0 python scripts/03_train.py"

# 同步結果
rsync -avz user@server:~/tasks/{task_name}/models/ tasks/{task_name}/models/
```

## 訓練腳本核心

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

# 載入模型
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-4B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")

# LoRA 配置
lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)

# 訓練參數
training_args = TrainingArguments(
    output_dir="models/adapter",
    num_train_epochs=8,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=1e-5,
    warmup_ratio=0.1,
    weight_decay=0.01,
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="epoch",
    load_best_model_at_end=True,
    bf16=True,
)

# 訓練
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model()
```

## 監控訓練

### 觀察指標

| 指標 | 健康範圍 | 問題信號 |
|------|----------|----------|
| Train Loss | 穩定下降 | 震盪、上升 |
| Eval Loss | 穩定或略降 | 持續上升 |
| Learning Rate | 先升後降 | - |

### TensorBoard

```bash
tensorboard --logdir models/adapter/runs
```

### 訓練日誌分析

```
健康訓練曲線：
Epoch 1: train_loss=2.1, eval_loss=2.0
Epoch 2: train_loss=1.5, eval_loss=1.6
Epoch 3: train_loss=1.2, eval_loss=1.4
Epoch 4: train_loss=1.0, eval_loss=1.3  ← 開始收斂
...

過擬合信號：
Epoch 5: train_loss=0.5, eval_loss=1.3
Epoch 6: train_loss=0.3, eval_loss=1.5  ← eval 上升！
Epoch 7: train_loss=0.2, eval_loss=1.8  ← 過擬合
```

## 常見配置

### 標準 SFT 配置

```yaml
# 4B 模型, 24GB GPU
lora:
  r: 32
  lora_alpha: 64

training:
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 1e-5
  num_train_epochs: 8
```

### 資源受限 QLoRA 配置

```yaml
# 4B 模型, 12GB GPU
quantization:
  load_in_4bit: true
  bnb_4bit_compute_dtype: bfloat16
  bnb_4bit_quant_type: nf4

lora:
  r: 16
  lora_alpha: 32

training:
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
```

### ORPO 配置

```yaml
method: orpo

orpo:
  beta: 0.1

training:
  num_train_epochs: 3
  learning_rate: 5e-6
```

## 訓練問題排查

### CUDA OOM

```python
# 降低 batch size
per_device_train_batch_size: 2

# 增加 gradient accumulation
gradient_accumulation_steps: 16

# 使用 QLoRA
load_in_4bit: true

# 減少序列長度
max_seq_length: 1024
```

### Loss 不下降

見 [troubleshooting/low-accuracy.md](../references/troubleshooting/low-accuracy.md)

### Loss 震盪

```yaml
# 降低學習率
learning_rate: 5e-6

# 增加 warmup
warmup_ratio: 0.2
```

## 訓練產出

```
models/adapter/
├── adapter_config.json     # LoRA 配置
├── adapter_model.safetensors  # LoRA 權重
├── tokenizer.json          # Tokenizer
├── tokenizer_config.json
├── special_tokens_map.json
└── checkpoint-*/           # 各 epoch checkpoints
```

## 驗證訓練結果

```python
# 快速測試
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-4B")
model = PeftModel.from_pretrained(base_model, "models/adapter")

# 測試推理
inputs = tokenizer.apply_chat_template(
    [{"role": "user", "content": "測試輸入"}],
    tokenize=True,
    return_tensors="pt"
)

outputs = model.generate(inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
```

## 下一步

訓練完成後進入 [Phase 5: 評估效能](05-evaluation.md)

---

*更新: 2026-01*
