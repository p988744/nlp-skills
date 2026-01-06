---
description: 生成任務的專案結構和訓練腳本
argument-hint: [task-name]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
---

根據 task.yaml 和 data_source.yaml 生成完整的專案結構和訓練腳本。

## 參數

- `$1`: 任務名稱

## 生成流程

### 1. 驗證任務

檢查必要檔案存在：
- `$1/task.yaml` - 任務定義
- `$1/data_source.yaml` - 資料來源配置

如果檔案不完整，提示使用者先完成配置。

### 2. 讀取配置

解析 task.yaml 取得：
- task_type: 任務類型
- domain: 領域
- input_template: 輸入模板
- output_format: 輸出格式
- training: 訓練配置
- success_criteria: 成功標準

### 3. 生成腳本

根據任務類型生成對應的腳本：

#### 01_regenerate_data.py
```python
#!/usr/bin/env python
"""根據 data_source.yaml 重新生成資料"""
# 從 data_source.yaml 讀取配置
# 處理各資料來源
# 合併和分割資料
```

#### 02_validate_data.py
```python
#!/usr/bin/env python
"""驗證資料格式和品質"""
# 檢查 JSON 格式
# 驗證必要欄位
# 檢查標籤值
# 統計類別分佈
```

#### 03_convert_format.py
```python
#!/usr/bin/env python
"""轉換為 chat format"""
# 讀取原始資料
# 應用 input_template
# 生成 messages 格式
# 輸出到 data/chat_format/
```

#### 04_train.py
```python
#!/usr/bin/env python
"""執行訓練"""
# 載入配置
# 設定 LoRA/QLoRA
# 執行 SFT/ORPO/DPO
# 儲存 adapter
```

#### 05_evaluate.py
```python
#!/usr/bin/env python
"""評估模型效能"""
# 載入模型
# 推理測試集
# 計算指標
# 生成報告
```

#### 06_upload_hf.py
```python
#!/usr/bin/env python
"""上傳到 HuggingFace"""
# 合併 adapter
# 轉換 GGUF
# 上傳 repos
# 生成 Model Card
```

### 4. 生成配置檔

#### configs/training_config.yaml
```yaml
# 訓練配置
base_model: {from task.yaml}
method: {sft/orpo/dpo}

lora:
  r: {from task.yaml}
  alpha: {alpha}
  dropout: 0.05
  target_modules:
    - q_proj
    - v_proj
    - k_proj
    - o_proj

training:
  epochs: {epochs}
  batch_size: 4
  learning_rate: {lr}
  warmup_ratio: 0.1
  max_seq_length: 2048
  gradient_accumulation_steps: 4
```

#### configs/benchmark_config.yaml
```yaml
# 評估配置
metrics:
  - accuracy
  - macro_f1
  - per_class_f1

output:
  format: json
  path: benchmarks/results/
```

### 5. 生成文件

#### docs/integration-guide.md
```markdown
# {task_name} 整合指南

## 模型資訊
- 基礎模型: {base_model}
- 訓練方法: {method}
- 主要指標: {metric} = {score}

## 使用方式

### Python
...

### Ollama
...

### vLLM
...
```

#### docs/annotation-guide.md
```markdown
# {task_name} 標註指南

## 任務定義
{task description}

## 輸入格式
{input_template}

## 輸出格式
{output_format}

## 標註範例
...
```

### 6. 生成 run_pipeline.sh

```bash
#!/bin/bash
# 一鍵執行全流程

set -e

echo "Step 1: 生成資料"
python scripts/01_regenerate_data.py

echo "Step 2: 驗證資料"
python scripts/02_validate_data.py

echo "Step 3: 轉換格式"
python scripts/03_convert_format.py

echo "Step 4: 訓練模型"
python scripts/04_train.py

echo "Step 5: 評估效能"
python scripts/05_evaluate.py

echo "完成！"
```

### 7. 更新 task.yaml 狀態

```yaml
status: configuring  # 從 created 更新為 configuring
updated: {current_timestamp}
```

## 完成提示

```
專案結構已生成！

{task_name}/
├── scripts/
│   ├── 01_regenerate_data.py   ✓
│   ├── 02_validate_data.py     ✓
│   ├── 03_convert_format.py    ✓
│   ├── 04_train.py             ✓
│   ├── 05_evaluate.py          ✓
│   ├── 06_upload_hf.py         ✓
│   └── run_pipeline.sh         ✓
├── configs/
│   ├── training_config.yaml    ✓
│   └── benchmark_config.yaml   ✓
└── docs/
    ├── integration-guide.md    ✓
    └── annotation-guide.md     ✓

下一步：
1. 準備資料到 data/ 目錄
2. 執行 ./scripts/run_pipeline.sh
3. 或分步執行各腳本
```
