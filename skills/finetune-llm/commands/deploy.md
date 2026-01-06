---
description: 部署模型到 HuggingFace 和 Ollama
argument-hint: [task-name] [version]
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
model: sonnet
---

將訓練好的模型部署到 HuggingFace Hub 和本地 Ollama。

## 參數

- `$1`: 任務名稱
- `$2`: 版本號（可選，預設為當前版本）

## 部署流程

### 1. 確認部署條件

檢查：
- 模型檔案存在（adapter 或 merged）
- 評估報告存在
- 效能達標（可選，可強制部署）

如果效能未達標：
```
⚠️ 效能未達標

當前: Macro-F1 = 72%
目標: Macro-F1 ≥ 80%

確定要繼續部署嗎？
□ 是，強制部署
□ 否，返回改善
```

### 2. 確認部署目標

使用 AskUserQuestion 詢問：
```
要部署到哪些平台？

□ HuggingFace Hub - 上傳 LoRA adapter
□ HuggingFace Hub - 上傳合併模型（vLLM 用）
□ HuggingFace Hub - 上傳 GGUF（Ollama 用）
□ HuggingFace Hub - 上傳資料集
□ 本地 Ollama - 建立本地模型
```

### 3. HuggingFace 配置

如果選擇 HuggingFace，確認配置：

```yaml
huggingface:
  org: your-org         # HF 組織或使用者名稱
  prefix: your-prefix   # 模型前綴

# 將生成的 repo 名稱:
# - {prefix}-{task_name}-adapter
# - {prefix}-{task_name}-vllm
# - {prefix}-{task_name}-gguf
# - {prefix}-{task_name}-data
```

詢問使用者確認或修改這些設定。

### 4. 執行部署

#### 4.1 合併 Adapter（如需要）

```bash
python scripts/06_upload_hf.py --merge-adapter
```

#### 4.2 轉換 GGUF（如需要）

```bash
python scripts/06_upload_hf.py --convert-gguf --quantization q8_0
```

量化選項：
- `q8_0`: 8-bit 量化（推薦，品質/大小平衡）
- `q4_k_m`: 4-bit 量化（更小，略有品質損失）
- `f16`: 半精度（最大，最高品質）

#### 4.3 上傳 HuggingFace

```bash
# 上傳 adapter
python scripts/06_upload_hf.py --upload adapter

# 上傳合併模型
python scripts/06_upload_hf.py --upload merged

# 上傳 GGUF
python scripts/06_upload_hf.py --upload gguf

# 上傳資料集
python scripts/06_upload_hf.py --upload dataset
```

#### 4.4 生成 Model Cards

為每個 repo 生成對應的 Model Card：

```markdown
# {model_name}

## Model Description
{description}

## Training Details
- Base Model: {base_model}
- Method: {method}
- Dataset: {dataset_size} examples

## Performance
| Metric | Score |
|--------|-------|
| Macro-F1 | {score}% |

## Usage
...
```

#### 4.5 本地 Ollama 部署

```bash
# 建立 Modelfile
cd $1/models/gguf
cat > Modelfile << EOF
FROM ./{model_name}-q8_0.gguf
SYSTEM "{system_prompt}"
EOF

# 建立 Ollama 模型
ollama create {task_name} -f Modelfile

# 測試
ollama run {task_name} "測試輸入"
```

### 5. 更新任務狀態

更新 task.yaml：
```yaml
status: deployed
deployed_at: {timestamp}
deployment:
  huggingface:
    adapter: {repo_url}
    gguf: {repo_url}
    vllm: {repo_url}
    dataset: {repo_url}
  ollama:
    model_name: {task_name}
```

### 6. 記錄版本 lineage

更新 `versions/{version}/lineage.yaml`：
```yaml
deployment:
  deployed_at: {timestamp}
  huggingface:
    adapter: {repo_url}
    gguf: {repo_url}
  ollama:
    model_name: {task_name}
```

## 完成提示

```
部署完成！

HuggingFace:
- Adapter: https://huggingface.co/{org}/{prefix}-{task}-adapter
- GGUF: https://huggingface.co/{org}/{prefix}-{task}-gguf
- vLLM: https://huggingface.co/{org}/{prefix}-{task}-vllm
- Dataset: https://huggingface.co/datasets/{org}/{prefix}-{task}-data

Ollama:
- 模型名稱: {task_name}
- 測試: ollama run {task_name} "你的輸入"

整合指南: {task_name}/docs/integration-guide.md
```

## 注意事項

- 確保已登入 HuggingFace: `huggingface-cli login`
- 確保已安裝 Ollama: `ollama --version`
- GGUF 轉換需要足夠的記憶體
- 大模型上傳可能需要較長時間
