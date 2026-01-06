# Llama 系列模型

## 概述

Llama 是 Meta 開發的開源大型語言模型系列，擁有最成熟的生態系統和工具支援。雖然 2025 年後被 Qwen 超越成為下載量第一，但仍是英文任務和研究的首選。

**優勢**: 生態系統成熟、工具支援完整、文件豐富

## 模型版本

| 模型 | 發布日期 | 參數量 | 架構 | 上下文 | 特點 |
|------|----------|--------|------|--------|------|
| **Llama 3.3** | 2024-12 | 70B | Dense | 128K | 最新、效能接近 405B |
| **Llama 3.2** | 2024-09 | 1B/3B/11B/90B | Dense | 128K | 多模態 (11B/90B) |
| **Llama 3.1** | 2024-07 | 8B/70B/405B | Dense | 128K | 405B 旗艦 |
| **Llama 3** | 2024-04 | 8B/70B | Dense | 8K | 基礎版本 |

## Llama 3.3 70B (推薦)

最新的 Llama 版本，單一 70B 模型達到接近 405B 的效能。

### 特點

- 128K 上下文長度
- 多語言支援改善
- 推理能力提升
- 指令遵循更好

### VRAM 需求

| 精度 | 推理 | 訓練 (LoRA) |
|------|------|-------------|
| FP16 | 140GB | 需多卡 |
| INT8 | 70GB | 80GB+ |
| INT4 | 35GB | 48GB+ |

## LoRA 微調配置

### Llama 3.3 70B (多 GPU)

```yaml
model:
  base_model: "meta-llama/Llama-3.3-70B-Instruct"
  trust_remote_code: false

lora:
  r: 16  # 大模型用較小 rank
  lora_alpha: 32
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj
  lora_dropout: 0.05

quantization:
  load_in_4bit: true
  bnb_4bit_compute_dtype: "bfloat16"
  bnb_4bit_quant_type: "nf4"

training:
  per_device_train_batch_size: 1
  gradient_accumulation_steps: 16
  learning_rate: 1e-5
  max_seq_length: 4096
```

### Llama 3.1 8B (單 GPU)

```yaml
model:
  base_model: "meta-llama/Llama-3.1-8B-Instruct"

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
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 2e-5
  max_seq_length: 2048
```

## Chat Template

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
```

### Llama 3 Chat 格式

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello!<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

## 效能基準

### Llama 3.3 70B

| 基準 | 分數 |
|------|------|
| MMLU | 86.0% |
| HumanEval | 88.4% |
| GSM8K | 95.1% |
| MATH | 77.0% |

### Llama 3.1 比較

| 基準 | 8B | 70B | 405B |
|------|-----|-----|------|
| MMLU | 69.4% | 83.6% | 88.6% |
| HumanEval | 72.6% | 80.5% | 89.0% |
| GSM8K | 84.5% | 95.1% | 96.8% |

## 授權條款

**Llama License** (非標準開源):

- ✅ 商業使用允許
- ✅ 修改和分發允許
- ⚠️ 月活超過 7 億需要額外授權
- ⚠️ 不得用於改善其他 LLM

與 Apache 2.0/MIT 不同，需注意授權限制。

## 與 Qwen 比較

| 特性 | Llama | Qwen |
|------|-------|------|
| 中文能力 | 良好 | 頂尖 |
| 英文能力 | 頂尖 | 優秀 |
| 生態系統 | 最成熟 | 快速成長 |
| 工具支援 | 完整 | 完整 |
| 授權 | Llama License | Apache 2.0 |
| 下載量 | 第二 | 第一 |

### 選擇建議

- **中文任務**: Qwen
- **英文任務**: Llama 或 Qwen
- **需要最完整工具支援**: Llama
- **授權靈活性**: Qwen (Apache 2.0)

## 微調注意事項

### 1. 特殊 Token

```python
# Llama 3 使用特殊 token
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"  # 重要！
```

### 2. 系統提示

Llama 對系統提示敏感，微調時保持一致：

```python
system_prompt = "You are a helpful assistant specialized in..."

# 訓練和推理使用相同的 system prompt
```

### 3. 長序列處理

```python
# 啟用 Flash Attention 2 (如果可用)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    attn_implementation="flash_attention_2",
    torch_dtype=torch.bfloat16,
)
```

## 部署配置

### vLLM

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
    --tensor-parallel-size 1 \
    --max-model-len 8192 \
    --port 8000
```

### Ollama

```bash
# 直接使用官方模型
ollama run llama3.1:8b

# 或自定義 Modelfile
FROM llama3.1:8b
SYSTEM "Your custom system prompt"
```

## 相關

- [qwen.md](qwen.md) - 中文任務首選
- [dense.md](../architectures/dense.md) - Dense 架構說明
- [lora.md](../methods/peft/lora.md) - LoRA 微調詳解

---

*更新: 2026-01*
