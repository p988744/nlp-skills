# Phase 6: 部署上線

## 概述

將訓練好的模型打包並上傳到 HuggingFace，支援多種部署方式。

## 部署格式

| 格式 | 用途 | 適用場景 |
|------|------|----------|
| LoRA Adapter | 研究、進一步微調 | 需要合併或堆疊 |
| GGUF | Ollama 本地部署 | 開發、邊緣部署 |
| vLLM Merged | 生產環境 | 高吞吐量服務 |

## Step 1: 合併模型 (vLLM 用)

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# 載入基礎模型
base_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-4B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# 載入 LoRA
model = PeftModel.from_pretrained(base_model, "models/adapter")

# 合併
merged_model = model.merge_and_unload()

# 儲存
merged_model.save_pretrained("models/merged")
tokenizer.save_pretrained("models/merged")
```

## Step 2: 轉換 GGUF (Ollama 用)

```bash
# 安裝 llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# 轉換 (使用 Qwen 專用轉換)
python convert_hf_to_gguf.py \
    --outfile models/gguf/model-q8_0.gguf \
    --outtype q8_0 \
    models/merged
```

### Modelfile

```dockerfile
FROM ./model-q8_0.gguf

SYSTEM """你是情感分析專家。請分析文本的情感傾向。

只能回答以下類別之一：正面、負面、中立"""

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER num_predict 10
```

## Step 3: 上傳 HuggingFace

### 建立儲存庫

```bash
# 登入
huggingface-cli login

# 建立儲存庫
huggingface-cli repo create {repo_name} --type model
```

### 上傳 Adapter

```bash
# {hf_org} 和 {prefix} 來自 task_definition.yaml 的 huggingface 設定
huggingface-cli upload {hf_org}/{prefix}-{task_name}-zh models/adapter .
```

### 上傳 GGUF

```bash
huggingface-cli upload {hf_org}/{prefix}-{task_name}-zh-gguf \
    models/gguf/model-q8_0.gguf \
    models/gguf/Modelfile
```

### 上傳 vLLM

```bash
huggingface-cli upload {hf_org}/{prefix}-{task_name}-zh-vllm models/merged .
```

## Step 4: 更新 Model Cards

### Adapter Card (hf_cards/adapter_card.md)

```markdown
---
license: apache-2.0
base_model: Qwen/Qwen3-4B
language: zh
tags:
  - sentiment-analysis
  - lora
  - peft
---

# eland-{task_name}-zh

## 模型說明
{description}

## 效能
| 指標 | 分數 |
|------|------|
| Macro-F1 | {macro_f1} |

## 使用方式
```python
from peft import PeftModel
model = PeftModel.from_pretrained("Qwen/Qwen3-4B", "{hf_org}/{prefix}-{task_name}-zh")
```
```

### GGUF Card

```markdown
# {prefix}-{task_name}-zh-gguf

## Ollama 使用

```bash
huggingface-cli download {hf_org}/{prefix}-{task_name}-zh-gguf \
    model-q8_0.gguf Modelfile --local-dir ./

ollama create {prefix}-{task_name} -f Modelfile
ollama run {prefix}-{task_name}
```
```

### vLLM Card

```markdown
# {prefix}-{task_name}-zh-vllm

## vLLM 部署

```bash
vllm serve {hf_org}/{prefix}-{task_name}-zh-vllm --port 8000
```
```

## Step 5: 更新整合指南

更新 `docs/integration-guide.md`：

1. HuggingFace 連結
2. 使用範例
3. 效能指標
4. 部署方式

## 驗證部署

### Ollama 測試

```bash
ollama run eland-{task_name} "測試文本"
```

### vLLM 測試

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "eland-{task_name}-zh-vllm",
    "messages": [{"role": "user", "content": "測試文本"}]
  }'
```

## 部署檢查清單

- [ ] Adapter 上傳成功
- [ ] GGUF 轉換正確
- [ ] vLLM merged 可載入
- [ ] Model cards 完整
- [ ] Integration guide 更新
- [ ] 各格式驗證通過

## 專案歸檔

部署完成後，更新專案狀態：

```yaml
# task_definition.yaml 新增
status: deployed
deployed_date: "2026-01-06"
hf_repos:
  adapter: {hf_org}/{prefix}-{task_name}-zh
  gguf: {hf_org}/{prefix}-{task_name}-zh-gguf
  vllm: {hf_org}/{prefix}-{task_name}-zh-vllm
```

## 完成

恭喜！任務已完成部署。

如需改善模型效能，請使用 [ITERATE-MODE](../ITERATE-MODE.md)。

---

*更新: 2026-01*
