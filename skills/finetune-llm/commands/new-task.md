---
description: 建立新的 LLM 訓練任務
argument-hint: [task-name]
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
model: sonnet
---

建立新的 LLM 訓練任務目錄和配置檔案。

## 參數

- `$1`: 任務名稱（kebab-case，如 `entity-sentiment`）

## 建立流程

### 1. 驗證任務名稱

如果沒有提供 $1：
- 使用 AskUserQuestion 詢問任務名稱
- 建議使用 kebab-case 格式
- 範例：`entity-sentiment`, `ner-finance`, `stance-detection`

### 2. 檢查是否已存在

檢查目錄是否已存在：
```bash
test -d "$1" && echo "EXISTS" || echo "NEW"
```

如果已存在，詢問是否覆蓋或使用其他名稱。

### 3. 建立目錄結構

```bash
mkdir -p $1/{data/{raw,chat_format},scripts,configs,models/{adapter,merged,gguf},benchmarks/{data,results},versions,docs}
```

### 4. 生成 task.yaml

```yaml
# task.yaml
task_name: $1
version: v1
status: created

# 任務定義（待填寫）
task_type: classification  # classification, extraction, generation
domain: general
language: zh-TW

# 輸入輸出（待填寫）
input_template: |
  {instruction}

output_format:
  type: json
  schema: {}

# 成功標準（待填寫）
success_criteria:
  primary_metric: macro_f1
  threshold: 0.80

# 執行環境（待填寫）
execution:
  type: local  # local, remote_ssh, cloud
  # host: user@server
  # cuda_devices: "0"

# 元資料
created: {current_timestamp}
updated: {current_timestamp}
```

### 5. 生成 data_source.yaml

```yaml
# data_source.yaml
version: "1.0"
created: {current_timestamp}

sources: []  # 待配置

merge:
  enabled: false

split:
  enabled: true
  ratios:
    train: 0.7
    valid: 0.15
    test: 0.15
  stratify_by: label
  random_seed: 42

regeneration:
  script: scripts/01_regenerate_data.py
```

### 6. 生成空白腳本

建立以下腳本檔案（空白模板）：
- `scripts/01_regenerate_data.py`
- `scripts/02_validate_data.py`
- `scripts/03_convert_format.py`
- `scripts/04_train.py`
- `scripts/05_evaluate.py`
- `scripts/06_upload_hf.py`

### 7. 建立 README.md

```markdown
# {task_name}

## 快速開始

1. 配置資料來源：編輯 `data_source.yaml`
2. 生成資料：`python scripts/01_regenerate_data.py`
3. 驗證資料：`python scripts/02_validate_data.py`
4. 轉換格式：`python scripts/03_convert_format.py`
5. 訓練模型：`python scripts/04_train.py`
6. 評估效能：`python scripts/05_evaluate.py`
7. 上傳部署：`python scripts/06_upload_hf.py`

## 任務定義

詳見 `task.yaml`

## 資料來源

詳見 `data_source.yaml`
```

### 8. 完成提示

```
任務 $1 已建立！

目錄結構：
$1/
├── task.yaml           # 任務定義
├── data_source.yaml    # 資料來源配置
├── README.md           # 說明文件
├── data/              # 資料目錄
├── scripts/           # 執行腳本
├── configs/           # 訓練配置
├── models/            # 模型輸出
├── benchmarks/        # 評估結果
├── versions/          # 版本追蹤
└── docs/              # 文件

下一步：
1. 使用 /nlp-skills:data-source 配置資料來源
2. 或使用 /nlp-skills:coach 繼續引導
```
