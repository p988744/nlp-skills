# Phase 2: 生成專案

## 概述

根據 `task_definition.yaml` 自動生成完整的專案結構。

## 執行命令

```bash
python scripts/init_project.py \
    --config task_definition.yaml \
    --output tasks/{task_name}
```

## 產出結構

```
tasks/{task_name}/
├── task_definition.yaml      # 任務定義（複製）
├── README.md                 # 專案說明
│
├── scripts/                  # 可執行腳本
│   ├── 01_validate_data.py   # 資料驗證
│   ├── 02_convert_format.py  # 格式轉換
│   ├── 03_train.py           # 訓練腳本
│   ├── 04_evaluate.py        # 評估腳本
│   ├── 05_upload_hf.py       # HuggingFace 上傳
│   └── run_pipeline.sh       # 一鍵執行
│
├── configs/                  # 配置檔
│   ├── training_config.yaml  # 訓練配置
│   └── benchmark_config.yaml # 評估配置
│
├── data/                     # 資料目錄
│   ├── raw/                  # 原始資料
│   ├── chat_format/          # 訓練格式
│   │   ├── train.jsonl
│   │   └── valid.jsonl
│   └── test.jsonl
│
├── models/                   # 模型產出
│   ├── adapter/              # LoRA adapter
│   ├── merged/               # 合併模型
│   └── gguf/                 # GGUF 檔案
│
├── benchmarks/               # 評估結果
│   ├── data/                 # 評估資料
│   └── results/              # 結果報告
│
├── docs/                     # 文件
│   └── integration-guide.md  # 整合指南
│
├── hf_cards/                 # HuggingFace Model Cards
│   ├── adapter_card.md
│   ├── gguf_card.md
│   └── vllm_card.md
│
└── iterations/               # 迭代記錄
    └── v1/                   # 版本 1
```

## 自動生成內容

### 1. training_config.yaml

```yaml
model:
  base_model: "{base_model}"
  trust_remote_code: true

data:
  train_file: data/chat_format/train.jsonl
  valid_file: data/chat_format/valid.jsonl

lora:
  r: {lora_r}
  lora_alpha: {lora_alpha}
  lora_dropout: 0.05
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

training:
  method: {method}
  num_epochs: {epochs}
  learning_rate: {learning_rate}
  per_device_train_batch_size: {batch_size}
  gradient_accumulation_steps: 4
  warmup_ratio: 0.1
  weight_decay: 0.01
  max_seq_length: 2048
  logging_steps: 10
  save_strategy: epoch
  evaluation_strategy: epoch

output:
  output_dir: models/adapter
```

### 2. benchmark_config.yaml

```yaml
evaluation:
  test_file: data/test.jsonl
  metrics:
    primary: {primary_metric}
    secondary:
      - accuracy
      - per_class_f1
  thresholds:
    pass:
      {primary_metric}: {threshold}

output:
  results_dir: benchmarks/results/
```

### 3. 01_validate_data.py

自動根據 task_definition 中的 output_format 生成驗證邏輯。

### 4. integration-guide.md

整合指南模板，包含：
- 模型資訊
- HuggingFace 連結
- 部署方式
- 使用範例

## 客製化調整

生成後可能需要調整：

1. **training_config.yaml**
   - 根據實際 GPU 調整 batch_size
   - 根據資料量調整 epochs

2. **02_convert_format.py**
   - 根據原始資料格式調整轉換邏輯
   - 客製化 system prompt

3. **04_evaluate.py**
   - 新增領域特定的評估指標

## 下一步

完成後進入 [Phase 3: 準備資料](03-prepare-data.md)

---

*更新: 2026-01*
