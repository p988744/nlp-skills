#!/usr/bin/env python3
"""
初始化 LLM 訓練專案

根據 task_definition.yaml 生成完整的專案結構，
包含腳本、配置、文件模板。

Usage:
    python init_project.py --config task_definition.yaml --output tasks/{task_name}
"""

import argparse
import yaml
import json
from pathlib import Path
from datetime import datetime
from string import Template


def load_task_definition(config_path: str) -> dict:
    """載入任務定義"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_directory_structure(output_dir: Path):
    """建立目錄結構"""
    dirs = [
        'scripts',
        'configs',
        'data/raw',
        'data/chat_format',
        'models/adapter',
        'models/merged',
        'models/gguf',
        'benchmarks/data',
        'benchmarks/results',
        'docs',
        'hf_cards',
        'iterations/v1',
    ]
    for d in dirs:
        (output_dir / d).mkdir(parents=True, exist_ok=True)


def generate_readme(task_def: dict, output_dir: Path):
    """生成 README.md"""
    content = f"""# {task_def['task_name']} 訓練專案

## 任務概述

- **任務類型**: {task_def['task_type']}
- **領域**: {task_def.get('domain', '通用')}
- **語言**: {task_def.get('language', 'zh-TW')}
- **基礎模型**: {task_def.get('training', {}).get('base_model', 'Qwen/Qwen3-4B')}

## 快速開始

### 1. 準備資料

將原始資料放入 `data/raw/`，格式為 JSONL：

```jsonl
{{"text": "範例文本", "label": "標籤"}}
```

### 2. 驗證和轉換資料

```bash
python scripts/01_validate_data.py
python scripts/02_convert_format.py
```

### 3. 訓練模型

```bash
# 本地訓練
python scripts/03_train.py

# 或遠端訓練
REMOTE=true ./scripts/run_pipeline.sh
```

### 4. 評估

```bash
python scripts/04_evaluate.py
```

### 5. 上傳 HuggingFace

```bash
python scripts/05_upload_hf.py
```

## 一鍵執行

```bash
./scripts/run_pipeline.sh
```

## 目錄結構

```
{task_def['task_name']}/
├── task_definition.yaml      # 任務定義
├── scripts/                  # 可執行腳本
├── configs/                  # 訓練配置
├── data/                     # 訓練資料
├── models/                   # 模型產出
├── benchmarks/               # 評估結果
├── docs/                     # 文件
└── hf_cards/                 # HuggingFace Model Cards
```

## 目標指標

| 指標 | 目標 |
|------|------|
| {task_def.get('success_criteria', {}).get('primary_metric', 'macro_f1')} | {task_def.get('success_criteria', {}).get('threshold', 0.80):.0%} |

---

*生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    (output_dir / 'README.md').write_text(content, encoding='utf-8')


def generate_training_config(task_def: dict, output_dir: Path):
    """生成訓練配置"""
    training = task_def.get('training', {})
    lora = training.get('lora', {})

    config = {
        'model': {
            'base_model': training.get('base_model', 'Qwen/Qwen3-4B'),
            'trust_remote_code': True,
        },
        'data': {
            'train_file': 'data/chat_format/train.jsonl',
            'valid_file': 'data/chat_format/valid.jsonl',
        },
        'lora': {
            'r': lora.get('r', 32),
            'lora_alpha': lora.get('alpha', 64),
            'lora_dropout': lora.get('dropout', 0.05),
            'target_modules': [
                'q_proj', 'k_proj', 'v_proj', 'o_proj',
                'gate_proj', 'up_proj', 'down_proj'
            ],
        },
        'training': {
            'method': training.get('method', 'sft'),
            'num_epochs': training.get('epochs', 8),
            'learning_rate': training.get('learning_rate', 1e-5),
            'per_device_train_batch_size': training.get('batch_size', 4),
            'gradient_accumulation_steps': 4,
            'warmup_ratio': 0.1,
            'weight_decay': 0.01,
            'max_seq_length': 2048,
            'logging_steps': 10,
            'save_strategy': 'epoch',
            'evaluation_strategy': 'epoch',
        },
        'output': {
            'output_dir': f"models/adapter",
        },
    }

    config_path = output_dir / 'configs' / 'training_config.yaml'
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def generate_benchmark_config(task_def: dict, output_dir: Path):
    """生成評估配置"""
    criteria = task_def.get('success_criteria', {})

    config = {
        'evaluation': {
            'test_file': 'data/test.jsonl',
            'metrics': {
                'primary': criteria.get('primary_metric', 'macro_f1'),
                'secondary': ['accuracy', 'per_class_f1'],
            },
            'thresholds': {
                'pass': {
                    criteria.get('primary_metric', 'macro_f1'): criteria.get('threshold', 0.80),
                },
            },
        },
        'output': {
            'results_dir': 'benchmarks/results/',
        },
    }

    config_path = output_dir / 'configs' / 'benchmark_config.yaml'
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)


def generate_validate_script(task_def: dict, output_dir: Path):
    """生成資料驗證腳本"""
    output_format = task_def.get('output_format', {})
    labels = output_format.get('schema', {}).get(list(output_format.get('schema', {'label': {}}).keys())[0], {}).get('enum', ['正面', '負面', '中立'])

    content = f'''#!/usr/bin/env python3
"""
資料驗證腳本
任務: {task_def['task_name']}
"""

import json
from pathlib import Path
from collections import Counter

EXPECTED_LABELS = {labels}

def validate_file(file_path: str) -> dict:
    """驗證單一檔案"""
    issues = []
    label_counts = Counter()

    with open(file_path, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            try:
                item = json.loads(line)

                # 檢查必要欄位
                if 'text' not in item and 'input' not in item:
                    issues.append(f"Line {{i}}: Missing 'text' or 'input' field")

                if 'label' not in item and 'output' not in item:
                    issues.append(f"Line {{i}}: Missing 'label' or 'output' field")
                else:
                    label = item.get('label') or item.get('output')
                    label_counts[label] += 1

                    if label not in EXPECTED_LABELS:
                        issues.append(f"Line {{i}}: Invalid label '{{label}}'")

            except json.JSONDecodeError:
                issues.append(f"Line {{i}}: Invalid JSON")

    return {{
        'file': file_path,
        'total_lines': i,
        'issues': issues,
        'label_distribution': dict(label_counts),
    }}


def main():
    data_dir = Path('data')

    files_to_check = [
        data_dir / 'train.jsonl',
        data_dir / 'valid.jsonl',
        data_dir / 'test.jsonl',
    ]

    print("=" * 50)
    print("資料驗證報告")
    print("=" * 50)

    all_valid = True

    for file_path in files_to_check:
        if not file_path.exists():
            print(f"\\n⚠️  {{file_path}} 不存在")
            continue

        result = validate_file(str(file_path))

        print(f"\\n📄 {{result['file']}}")
        print(f"   總筆數: {{result['total_lines']}}")
        print(f"   類別分佈: {{result['label_distribution']}}")

        if result['issues']:
            all_valid = False
            print(f"   ❌ 發現 {{len(result['issues'])}} 個問題:")
            for issue in result['issues'][:5]:
                print(f"      - {{issue}}")
            if len(result['issues']) > 5:
                print(f"      ... 還有 {{len(result['issues']) - 5}} 個問題")
        else:
            print("   ✅ 驗證通過")

    print("\\n" + "=" * 50)
    if all_valid:
        print("✅ 所有檔案驗證通過")
    else:
        print("❌ 部分檔案有問題，請修正後重新驗證")
    print("=" * 50)


if __name__ == "__main__":
    main()
'''

    script_path = output_dir / 'scripts' / '01_validate_data.py'
    script_path.write_text(content, encoding='utf-8')
    script_path.chmod(0o755)


def generate_run_pipeline(task_def: dict, output_dir: Path):
    """生成一鍵執行腳本"""
    # 取得伺服器配置（使用者設定或預設值）
    server_config = task_def.get('server', {})
    server_host = server_config.get('host', '${SERVER_HOST}')
    ssh_key = server_config.get('ssh_key', '${SSH_KEY}')
    cuda_devices = server_config.get('cuda_devices', '${CUDA_DEVICES}')
    remote_path = server_config.get('remote_path', '~/tasks')

    content = f'''#!/bin/bash
# {task_def['task_name']} 一鍵執行腳本

set -e

TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$TASK_DIR"

echo "=========================================="
echo "任務: {task_def['task_name']}"
echo "目錄: $TASK_DIR"
echo "=========================================="

# Phase 3: 資料準備
echo ""
echo "=== Phase 3: 資料準備 ==="
python scripts/01_validate_data.py
python scripts/02_convert_format.py

# Phase 4: 訓練
echo ""
echo "=== Phase 4: 訓練模型 ==="
if [ "$REMOTE" = "true" ]; then
    echo "使用遠端訓練..."

    # 讀取伺服器設定（從環境變數或 task_definition.yaml）
    SERVER_HOST="${{SERVER_HOST:-{server_host}}}"
    SSH_KEY="${{SSH_KEY:-{ssh_key}}}"
    CUDA_DEVICES="${{CUDA_DEVICES:-{cuda_devices}}}"

    # 檢查必要設定
    if [ "$SERVER_HOST" = "${{SERVER_HOST}}" ] || [ -z "$SERVER_HOST" ]; then
        echo "❌ 錯誤: 請設定 SERVER_HOST 環境變數或在 task_definition.yaml 中設定 server.host"
        echo "   範例: export SERVER_HOST=user@your-gpu-server"
        exit 1
    fi

    # 同步到遠端
    rsync -avz -e "ssh -i $SSH_KEY" "$TASK_DIR" "$SERVER_HOST":{remote_path}/

    # 遠端執行
    ssh -i "$SSH_KEY" "$SERVER_HOST" \\
        "cd {remote_path}/$(basename $TASK_DIR) && \\
         source ~/.venv/bin/activate && \\
         CUDA_VISIBLE_DEVICES=$CUDA_DEVICES python scripts/03_train.py"

    # 同步結果
    rsync -avz -e "ssh -i $SSH_KEY" "$SERVER_HOST":{remote_path}/$(basename $TASK_DIR)/models/ "$TASK_DIR/models/"
else
    python scripts/03_train.py
fi

# Phase 5: 評估
echo ""
echo "=== Phase 5: 評估效能 ==="
python scripts/04_evaluate.py

echo ""
echo "=========================================="
echo "✅ Pipeline 完成"
echo "評估結果: benchmarks/results/"
echo "=========================================="
'''

    script_path = output_dir / 'scripts' / 'run_pipeline.sh'
    script_path.write_text(content, encoding='utf-8')
    script_path.chmod(0o755)


def generate_integration_guide(task_def: dict, output_dir: Path):
    """生成整合指南模板"""
    task_name = task_def['task_name']
    hf_config = task_def.get('huggingface', {})
    hf_org = hf_config.get('org', '{your-hf-org}')
    hf_prefix = hf_config.get('prefix', 'eland')

    content = f"""# {task_name} 整合指南

本文件提供 {task_name} 模型的整合指南，供下游服務串接使用。

## 模型資訊

| 項目 | 說明 |
|------|------|
| 模型名稱 | {hf_prefix}-{task_name}-zh |
| 基礎模型 | {task_def.get('training', {}).get('base_model', 'Qwen/Qwen3-4B')} |
| 支援語言 | {task_def.get('language', '繁體中文')} |
| 授權條款 | Apache 2.0 |

## HuggingFace 儲存庫

| 用途 | 連結 |
|------|------|
| LoRA Adapter | https://huggingface.co/{hf_org}/{hf_prefix}-{task_name}-zh |
| vLLM 部署 | https://huggingface.co/{hf_org}/{hf_prefix}-{task_name}-zh-vllm |
| Ollama/GGUF | https://huggingface.co/{hf_org}/{hf_prefix}-{task_name}-zh-gguf |

## 部署方式

### Ollama (推薦本地部署)

```bash
# 下載並建立模型
huggingface-cli download {hf_org}/{hf_prefix}-{task_name}-zh-gguf \\
    {hf_prefix}-{task_name}-zh-q8_0.gguf Modelfile --local-dir ./

ollama create {hf_prefix}-{task_name}-zh -f Modelfile
ollama run {hf_prefix}-{task_name}-zh "測試輸入"
```

### vLLM (生產環境)

```bash
vllm serve {hf_org}/{hf_prefix}-{task_name}-zh-vllm --port 8000
```

## 使用範例

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={{
        "model": "{hf_prefix}-{task_name}-zh",
        "messages": [
            {{"role": "user", "content": "測試輸入"}}
        ]
    }}
)
print(response.json())
```

---

*生成時間: {datetime.now().strftime('%Y-%m-%d')}*
"""

    (output_dir / 'docs' / 'integration-guide.md').write_text(content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='初始化 LLM 訓練專案')
    parser.add_argument('--config', required=True, help='task_definition.yaml 路徑')
    parser.add_argument('--output', required=True, help='輸出目錄')
    args = parser.parse_args()

    # 載入配置
    task_def = load_task_definition(args.config)
    output_dir = Path(args.output)

    print(f"初始化專案: {task_def['task_name']}")
    print(f"輸出目錄: {output_dir}")

    # 建立目錄結構
    create_directory_structure(output_dir)
    print("✅ 目錄結構已建立")

    # 複製 task_definition.yaml
    import shutil
    shutil.copy(args.config, output_dir / 'task_definition.yaml')
    print("✅ task_definition.yaml 已複製")

    # 生成檔案
    generate_readme(task_def, output_dir)
    print("✅ README.md 已生成")

    generate_training_config(task_def, output_dir)
    print("✅ training_config.yaml 已生成")

    generate_benchmark_config(task_def, output_dir)
    print("✅ benchmark_config.yaml 已生成")

    generate_validate_script(task_def, output_dir)
    print("✅ 01_validate_data.py 已生成")

    generate_run_pipeline(task_def, output_dir)
    print("✅ run_pipeline.sh 已生成")

    generate_integration_guide(task_def, output_dir)
    print("✅ integration-guide.md 已生成")

    print()
    print("=" * 50)
    print(f"✅ 專案初始化完成: {output_dir}")
    print()
    print("下一步:")
    print(f"  1. 將資料放入 {output_dir}/data/")
    print(f"  2. 執行 python {output_dir}/scripts/01_validate_data.py")
    print(f"  3. 執行 {output_dir}/scripts/run_pipeline.sh")
    print("=" * 50)


if __name__ == "__main__":
    main()
'''

    script_path = output_dir / 'scripts' / 'init_project.py'
    script_path.write_text(content, encoding='utf-8')
    script_path.chmod(0o755)
