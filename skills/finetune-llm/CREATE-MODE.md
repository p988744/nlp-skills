# Create Mode: 建立新任務

本文件引導你從零開始建立一個完整的 LLM 訓練專案。

## 流程總覽

```
Phase 1: 定義目標 ──→ task_definition.yaml
    │
    ▼
Phase 2: 生成專案 ──→ tasks/{task_name}/ 完整結構
    │
    ▼
Phase 3: 準備資料 ──→ data/*.jsonl
    │
    ▼
Phase 4: 訓練模型 ──→ models/adapter/
    │
    ▼
Phase 5: 評估效能 ──→ benchmarks/results/
    │
    ▼
Phase 6: 部署上線 ──→ HuggingFace + Ollama
```

---

## Phase 1: 定義目標

### 必須收集的資訊

與使用者確認以下問題：

#### 1.1 任務類型

```
□ 分類任務
  ├── 情感分析（整體情感）
  ├── 實體情感分析（特定實體的情感）
  ├── 立場分析（支持/反對觀點）
  ├── 意圖識別
  └── 主題分類

□ 抽取任務
  ├── 命名實體識別（NER）
  ├── 關係抽取
  └── 事件抽取

□ 生成任務
  ├── 文本生成
  ├── 摘要
  ├── 改寫/轉換（如公文轉換）
  └── 翻譯
```

#### 1.2 目標領域

```
□ 金融（股票、財報、投資）
□ 法律（合約、判決、法規）
□ 醫療（病歷、藥品、診斷）
□ 政府公文
□ 社群媒體（PTT、Dcard）
□ 電商評論
□ 通用領域
```

#### 1.3 語言和輸出格式

- 語言：繁體中文 / 簡體中文 / 多語言
- 輸出格式：JSON / 純文本
- 標籤集：（如有）列出所有可能的輸出標籤

#### 1.4 現有資源

- 是否有現有標註資料？數量多少？
- 資料格式是什麼？
- 是否有領域專家可協助標註？

#### 1.5 目標指標

根據任務類型設定：

| 任務類型 | 主要指標 | 建議目標 |
|----------|----------|----------|
| 分類 | Macro-F1 | ≥ 80% |
| NER | Entity F1 | ≥ 70% |
| 生成 | 格式正確率 | ≥ 95% |

### 輸出：task_definition.yaml

```yaml
# 任務基本資訊
task_name: "entity-sentiment"
task_type: "classification"
domain: "finance"
language: "zh-TW"

# 輸入輸出格式
input_format:
  description: "文本和指定實體"
  template: |
    分析以下文本對「{entity}」的情感傾向。
    文本：{text}

output_format:
  type: "json"
  schema:
    entity_sentiment:
      type: "string"
      enum: ["正面", "負面", "中立"]

# 訓練配置
training:
  base_model: "Qwen/Qwen3-4B"
  method: "sft"  # sft, orpo, dpo
  lora:
    r: 32
    alpha: 64
  epochs: 8
  learning_rate: 1e-5

# 目標指標
success_criteria:
  primary_metric: "macro_f1"
  threshold: 0.80

# HuggingFace 配置
huggingface:
  org: "your-hf-org"
  prefix: "your-prefix"
  # 將生成: {prefix}-{task_name}-zh, {prefix}-{task_name}-zh-gguf, etc.

# 遠端伺服器配置（首次會詢問使用者）
server:
  host: "user@your-gpu-server"
  ssh_key: "~/.ssh/id_rsa"
  cuda_devices: "0"
  remote_path: "~/tasks"
```

詳見 [phases/01-define-objective.md](phases/01-define-objective.md)

---

## Phase 2: 生成專案

收集完任務定義後，自動生成完整專案結構。

### 執行生成

```bash
# 生成專案（由 Skill 執行）
python skills/finetune-llm-v2/scripts/init_project.py \
  --config task_definition.yaml \
  --output tasks/{task_name}
```

### 生成內容

```
tasks/{task_name}/
├── README.md                    # 任務說明和快速開始
├── task_definition.yaml         # 任務定義（複製）
│
├── scripts/                     # 已配置的可執行腳本
│   ├── 01_validate_data.py      # 驗證資料格式
│   ├── 02_convert_format.py     # 轉換 chat format
│   ├── 03_train.py              # 訓練腳本
│   ├── 04_evaluate.py           # 評估腳本
│   ├── 05_upload_hf.py          # 上傳 HuggingFace
│   └── run_pipeline.sh          # 一鍵執行全流程
│
├── configs/
│   ├── training_config.yaml     # 訓練超參數
│   └── benchmark_config.yaml    # 評估配置
│
├── data/                        # 資料目錄（待填充）
│   ├── raw/
│   ├── train.jsonl
│   ├── valid.jsonl
│   ├── test.jsonl
│   └── chat_format/
│
├── models/                      # 模型輸出目錄
│   ├── adapter/
│   ├── merged/
│   └── gguf/
│
├── benchmarks/
│   ├── data/
│   └── results/
│
├── docs/                        # 已生成的文件模板
│   ├── integration-guide.md     # 整合指南
│   └── annotation-guide.md      # 標註指南
│
└── hf_cards/                    # HuggingFace Model Cards
    ├── adapter_card.md
    ├── gguf_card.md
    ├── vllm_card.md
    └── dataset_card.md
```

詳見 [phases/02-generate-project.md](phases/02-generate-project.md)

---

## Phase 3: 準備資料

### 資料格式要求

#### 原始格式 (JSONL)

```jsonl
{"text": "台積電營收創新高", "entity": "台積電", "label": "正面"}
{"text": "聯電表現令人失望", "entity": "聯電", "label": "負面"}
```

#### Chat Format（訓練用）

```jsonl
{
  "messages": [
    {"role": "system", "content": "你是情感分析助手..."},
    {"role": "user", "content": "分析以下文本對「台積電」的情感...\n\n文本：台積電營收創新高"},
    {"role": "assistant", "content": "{\"entity_sentiment\": \"正面\"}"}
  ]
}
```

### 執行步驟

```bash
cd tasks/{task_name}

# 1. 放入原始資料到 data/raw/

# 2. 驗證資料格式
python scripts/01_validate_data.py

# 3. 轉換為 chat format
python scripts/02_convert_format.py
```

### 資料量建議

| 資料量 | 預期效能 | 說明 |
|--------|----------|------|
| 100-500 | 70-80% | 最小可用（PoC） |
| 500-2000 | 80-88% | 建議量 |
| 2000+ | 88%+ | 生產品質 |

詳見 [phases/03-prepare-data.md](phases/03-prepare-data.md)

---

## Phase 4: 訓練模型

### 本地訓練（有 GPU）

```bash
cd tasks/{task_name}
python scripts/03_train.py
```

### 遠端訓練

使用 `task_definition.yaml` 中設定的伺服器資訊：

```bash
cd tasks/{task_name}

# 讀取設定（由 run_pipeline.sh 自動處理）
# SERVER_HOST=user@your-gpu-server
# SSH_KEY=~/.ssh/id_rsa
# CUDA_DEVICES=0

# 同步到遠端
rsync -avz -e "ssh -i $SSH_KEY" . $SERVER_HOST:~/tasks/{task_name}/

# SSH 執行訓練
ssh -i $SSH_KEY $SERVER_HOST \
  "cd ~/tasks/{task_name} && \
   source ~/.venv/bin/activate && \
   CUDA_VISIBLE_DEVICES=$CUDA_DEVICES python scripts/03_train.py"

# 同步結果回本地
rsync -avz -e "ssh -i $SSH_KEY" $SERVER_HOST:~/tasks/{task_name}/models/ ./models/
```

> **Note**: 首次使用時，skill 會詢問伺服器資訊並儲存至 `task_definition.yaml`

### 訓練產出

```
models/
├── adapter/                  # LoRA adapter
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── tokenizer files
├── merged/                   # 合併後完整模型
└── gguf/                     # GGUF 格式（Ollama 用）
    └── model-q8_0.gguf
```

詳見 [phases/04-training.md](phases/04-training.md)

---

## Phase 5: 評估效能

### 執行評估

```bash
cd tasks/{task_name}
python scripts/04_evaluate.py
```

### 評估報告

生成於 `benchmarks/results/v1_report.md`：

```markdown
# {Task Name} 評估報告

## 整體表現

| 指標 | 分數 | 目標 | 狀態 |
|------|------|------|------|
| Accuracy | 85.0% | 80% | ✅ |
| Macro-F1 | 83.5% | 80% | ✅ |

## 各類別表現

| 類別 | Precision | Recall | F1 |
|------|-----------|--------|-----|
| 正面 | 88% | 85% | 86% |
| 負面 | 82% | 80% | 81% |
| 中立 | 80% | 85% | 82% |

## 決策

✅ 達標，進入部署階段
```

### 未達標處理

若未達標，參考：
- [references/troubleshooting/low-accuracy.md](references/troubleshooting/low-accuracy.md)
- [references/troubleshooting/class-imbalance.md](references/troubleshooting/class-imbalance.md)
- [ITERATE-MODE.md](ITERATE-MODE.md) - 進入改善流程

詳見 [phases/05-evaluation.md](phases/05-evaluation.md)

---

## Phase 6: 部署上線

### 上傳 HuggingFace

```bash
cd tasks/{task_name}
python scripts/05_upload_hf.py
```

### 上傳項目

| 項目 | Repository | 用途 |
|------|------------|------|
| LoRA Adapter | eland-{task}-zh | PEFT 載入 |
| GGUF | eland-{task}-zh-gguf | Ollama |
| Merged | eland-{task}-zh-vllm | vLLM |
| Dataset | eland-{task}-zh-data | 資料共享 |

### 本地 Ollama 部署

```bash
# 建立模型
cd tasks/{task_name}/models/gguf
ollama create {task_name} -f Modelfile

# 測試
ollama run {task_name} "測試輸入"
```

詳見 [phases/06-deployment.md](phases/06-deployment.md)

---

## 一鍵執行

完成資料準備後，可一鍵執行完整流程：

```bash
cd tasks/{task_name}
./scripts/run_pipeline.sh
```

或指定遠端訓練：

```bash
REMOTE=true ./scripts/run_pipeline.sh
```

---

## 下一步

- 部署完成後，更新主專案的 `CLAUDE.md`
- 如需改善效能，參考 [ITERATE-MODE.md](ITERATE-MODE.md)
