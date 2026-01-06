# 模板索引

## 概述

本目錄包含用於生成專案檔案的 Jinja2 模板。

## 模板清單

```
templates/
├── scripts/
│   ├── train.py.j2         # 訓練腳本模板
│   ├── evaluate.py.j2      # 評估腳本模板
│   ├── convert.py.j2       # 格式轉換模板
│   └── upload_hf.py.j2     # HF 上傳模板
│
├── configs/
│   ├── training_config.yaml.j2  # 訓練配置模板
│   └── benchmark_config.yaml.j2 # 評估配置模板
│
├── docs/
│   └── integration-guide.md.j2  # 整合指南模板
│
└── hf_cards/
    ├── adapter_card.md.j2   # LoRA adapter model card
    ├── gguf_card.md.j2      # GGUF model card
    └── vllm_card.md.j2      # vLLM model card
```

## 變數說明

### 通用變數

| 變數 | 說明 | 範例 |
|------|------|------|
| `task_name` | 任務名稱 | `sentiment-analysis` |
| `description` | 任務描述 | `金融新聞情感分析` |
| `generated_date` | 生成日期 | `2026-01-06` |

### 模型變數

| 變數 | 說明 | 範例 |
|------|------|------|
| `base_model` | 基礎模型 | `Qwen/Qwen3-4B` |
| `model_family` | 模型家族 | `qwen3` |
| `language` | 語言 | `繁體中文` |
| `language_code` | 語言代碼 | `zh` |

### LoRA 變數

| 變數 | 說明 | 預設 |
|------|------|------|
| `lora_r` | LoRA rank | `32` |
| `lora_alpha` | LoRA alpha | `64` |
| `lora_dropout` | Dropout | `0.05` |
| `target_modules` | 目標模組 | `[q_proj, ...]` |

### 訓練變數

| 變數 | 說明 | 預設 |
|------|------|------|
| `method` | 訓練方法 | `sft` |
| `epochs` | 訓練輪數 | `8` |
| `batch_size` | Batch size | `4` |
| `learning_rate` | 學習率 | `1e-5` |
| `max_seq_length` | 最大序列長度 | `2048` |

### 任務變數

| 變數 | 說明 | 範例 |
|------|------|------|
| `task_type` | 任務類型 | `classification` |
| `labels` | 標籤列表 | `['正面', '負面', '中立']` |
| `system_prompt` | 系統提示 | `你是情感分析專家...` |
| `primary_metric` | 主要指標 | `macro_f1` |
| `threshold` | 通過閾值 | `0.80` |

### 部署變數

| 變數 | 說明 | 範例 |
|------|------|------|
| `hf_org` | HF 組織 | `your-hf-username` |
| `tags` | 標籤列表 | `['sentiment', 'lora']` |
| `pipeline_tag` | Pipeline | `text-classification` |

## 使用方式

```python
from jinja2 import Environment, FileSystemLoader

# 載入模板環境
env = Environment(loader=FileSystemLoader('templates'))

# 渲染模板
template = env.get_template('scripts/train.py.j2')
content = template.render(
    task_name='sentiment-analysis',
    base_model='Qwen/Qwen3-4B',
    lora_r=32,
    # ... 其他變數
)

# 寫入檔案
with open('output/train.py', 'w') as f:
    f.write(content)
```

## 自訂模板

可根據需要修改模板或新增自訂模板。

### 新增模板

1. 建立 `.j2` 檔案
2. 使用 Jinja2 語法
3. 在 `init_project.py` 中新增渲染邏輯

### Jinja2 語法速查

```jinja
{# 註解 #}

{{ variable }}  {# 變數 #}

{% if condition %}  {# 條件 #}
{% endif %}

{% for item in list %}  {# 迴圈 #}
{% endfor %}

{{ "%.2f"|format(value) }}  {# 格式化 #}
```

---

*更新: 2026-01*
