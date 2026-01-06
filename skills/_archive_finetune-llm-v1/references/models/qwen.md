# Qwen 系列模型指南

## 概述

Qwen (通義千問) 是阿里巴巴開發的大型語言模型系列，2025 年已超越 Llama 成為 HuggingFace 下載量和微調使用率最高的開源模型。

## 模型一覽

### Qwen3 系列 (2025)

| 模型 | 參數量 | 架構 | 中文 | VRAM | 適用場景 |
|------|--------|------|------|------|----------|
| Qwen3-1.7B | 1.7B | Dense | ⭐⭐ | 4GB | 測試、邊緣 |
| **Qwen3-4B** | 4B | Dense | ⭐⭐⭐ | 8GB | **本專案預設** |
| Qwen3-8B | 8B | Dense | ⭐⭐⭐ | 16GB | 追求效能 |
| Qwen3-30B-A3B | 30B (3B active) | MoE | ⭐⭐⭐ | 24GB | 高效能 |
| Qwen3-235B-A22B | 235B (22B active) | MoE | ⭐⭐⭐ | 80GB+ | 頂尖效能 |

### Qwen2.5 系列

| 模型 | 說明 |
|------|------|
| Qwen2.5-Coder | 程式碼專精 |
| Qwen2.5-Math | 數學專精 |

## LoRA 配置建議

### Qwen3-4B 標準配置

```yaml
lora:
  r: 32
  lora_alpha: 64
  lora_dropout: 0.05
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

# 可訓練參數: ~66M (1.62%)
```

### 訓練超參數

| 參數 | Qwen3-4B | Qwen3-8B |
|------|----------|----------|
| Learning Rate | 1e-5 | 5e-6 |
| Batch Size | 4 | 2 |
| Epochs | 5-8 | 3-5 |
| Max Seq Length | 2048 | 2048 |

## Qwen 特有注意事項

### 1. Thinking Mode（重要）

Qwen3 預設啟用 thinking mode，會輸出 `<think>` 標籤。**必須關閉**：

```python
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    enable_thinking=False  # 重要！
)
```

### 2. Chat Template

```jinja2
<|im_start|>system
{{ system_prompt }}<|im_end|>
<|im_start|>user
{{ user_message }}<|im_end|>
<|im_start|>assistant
```

### 3. 特殊 Token

```python
pad_token = "<|endoftext|>"
eos_token = "<|im_end|>"
```

### 4. Trust Remote Code

```python
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-4B",
    trust_remote_code=True  # 必須
)
```

## 常見問題

### 輸出包含 `<think>` 標籤

```python
# 解決：關閉 thinking mode
enable_thinking=False
```

### 中文顯示異常

```python
# 解決：確保 trust_remote_code
trust_remote_code=True
```

### OOM 記憶體不足

```yaml
# 解決：減少 batch size 或使用 gradient checkpointing
per_device_train_batch_size: 2
gradient_checkpointing: true
```

## HuggingFace 連結

- 模型: https://huggingface.co/Qwen
- GitHub: https://github.com/QwenLM/Qwen

## 本專案使用記錄

| 任務 | 模型 | 效能 |
|------|------|------|
| 情感分析 | Qwen3-4B | 89.8% |
| 實體情感 | Qwen3-4B | 72.0% |
| 立場分析 | Qwen3-4B | 82.3% |
| 公文轉換 | Qwen3-4B (ORPO) | 100% |
| 法律 IE | Qwen3-4B | 66.5% |

---

*更新: 2026-01*
