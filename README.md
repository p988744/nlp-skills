# NLP Skills Marketplace

Claude Code skills for NLP tasks - LLM fine-tuning 工作流程與工具集。

## 可用 Skills

| Skill | 說明 |
|-------|------|
| `finetune-llm` | LLM fine-tuning 完整工作流程 |

## 安裝方式

### 方法 1：透過 Marketplace 安裝（推薦）

```bash
# 添加 nlp-skills marketplace
/plugin marketplace add https://github.com/p988744/nlp-skills.git

# 安裝 skill
/plugin install finetune-llm@nlp-skills
```

### 方法 2：直接指定目錄

```bash
claude --plugin-dir /path/to/nlp-skills
```

## finetune-llm Skill

LLM fine-tuning 完整工作流程，自動生成可重現的訓練專案。

### 功能特色

- **雙模式支援**：Create（建立新任務）、Iterate（改善既有任務）
- **自動專案生成**：根據任務定義生成完整腳本、配置、文件
- **內建知識庫**：2025-2026 最新模型、方法、任務指南（減少上網搜尋）
- **多種訓練方法**：SFT、LoRA、QLoRA、DoRA、ORPO、DPO
- **Benchmark 評估**：RGL 指標（Reliability, Generality, Locality）
- **HuggingFace 部署**：Adapter、GGUF、vLLM 多格式支援

### 使用方式

```
/finetune-llm
```

或直接描述你的需求：

```
# 建立新任務
我想訓練一個情感分析模型
幫我 fine-tune 一個 NER 模型

# 改善既有任務
改善 sentiment 模型的準確率
stance 的 F1 太低，怎麼辦
```

### 工作流程

```
Phase 1          Phase 2          Phase 3          Phase 4          Phase 5          Phase 6
定義目標    →    生成專案    →    準備資料    →    訓練模型    →    評估效能    →    部署上線
   │               │               │               │               │               │
   ▼               ▼               ▼               ▼               ▼               ▼
task_def.yaml   tasks/目錄     data/*.jsonl    models/        results/       HuggingFace
```

### 專案產出結構

每個任務生成獨立可重現的資料夾：

```
tasks/{task_name}/
├── README.md                 # 快速開始
├── task_definition.yaml      # 任務定義
├── scripts/                  # 可執行腳本
│   ├── 01_validate_data.py
│   ├── 02_convert_format.py
│   ├── 03_train.py
│   ├── 04_evaluate.py
│   ├── 05_upload_hf.py
│   └── run_pipeline.sh       # 一鍵執行
├── configs/                  # 訓練配置
├── data/                     # 訓練資料
├── models/                   # 模型產出
├── benchmarks/               # 評估結果
├── docs/                     # 整合指南
└── hf_cards/                 # HuggingFace Model Cards
```

### 內建知識庫

減少上網搜尋，內建 2025-2026 最新知識：

| 類別 | 內容 |
|------|------|
| **模型架構** | Dense vs MoE、MLA、DeepSeek 創新 |
| **基礎模型** | Qwen3、DeepSeek-V3/R1、Llama 3.3 |
| **訓練方法** | SFT、LoRA、QLoRA、DoRA、ORPO、DPO |
| **任務類型** | 情感分析、NER、關係抽取、風格轉換 |
| **問題排解** | 過擬合、類別不平衡、準確率低 |

### 環境需求

#### 遠端伺服器（訓練用）
- GPU: NVIDIA GPU（建議 24GB+ VRAM）
- Python: 3.10+
- 設定方式：skill 會在首次使用時詢問伺服器資訊

#### 本地開發
- Python: `uv run python`
- Claude Code: 最新版本

### 支援的任務類型

| 任務 | 訓練方法 | 說明 |
|------|----------|------|
| 情感分析 | SFT | 正面/負面/中立分類 |
| 實體情感 | SFT | 針對特定實體的情感 |
| 立場分析 | SFT | 支持/反對/中立 |
| 公文轉換 | ORPO | 口語→公文格式 |
| NER | SFT | 命名實體識別 |
| 關係抽取 | SFT | 實體間關係 |

## 版本歷史

見 [CHANGELOG.md](skills/finetune-llm/CHANGELOG.md)

## 授權

MIT License

## 作者

Weifan Liao (weifanliao@eland.com.tw)
