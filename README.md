# NLP Skills Marketplace

Claude Code skills for NLP tasks - LLM fine-tuning 教練式引導工作流程。

## v3.0 新特色

- **教練式引導**：主動探索痛點，引導明確目標，推薦最佳方案
- **多任務管理**：支援多個訓練任務的版本追蹤和比較
- **資料來源追蹤**：可重現的資料管線（DB、API、爬取、LLM 生成）
- **智能 Agents**：自動診斷問題、分析結果、推薦改善

## 安裝方式

### 方法 1：透過 Marketplace 安裝（推薦）

```bash
# 添加 nlp-skills marketplace
/plugin marketplace add p988744/nlp-skills

# 安裝
/plugin install nlp-skills
```

### 方法 2：直接指定目錄

```bash
claude --plugin-dir /path/to/nlp-skills
```

## 組件架構

### Skills (4 個專精領域)

| Skill | 觸發詞 | 說明 |
|-------|--------|------|
| **llm-coach** | 「訓練模型」「fine-tune」「優化效能」 | 教練式引導主入口 |
| **llm-knowledge** | 「什麼是 LoRA」「模型比較」 | 獨立知識庫 |
| **task-manager** | 「列出任務」「版本比較」 | 多任務管理 |
| **data-pipeline** | 「資料來源」「資料從哪裡來」 | 資料管線配置 |

### Commands (7 個快捷指令)

| 指令 | 說明 |
|------|------|
| `/coach` | 啟動教練式對話 |
| `/tasks` | 列出所有任務狀態 |
| `/new-task` | 建立新任務 |
| `/data-source` | 配置資料來源 |
| `/generate` | 生成專案結構 |
| `/evaluate` | 執行評估分析 |
| `/deploy` | 部署模型 |

### Agents (4 個自主助手)

| Agent | 觸發時機 | 功能 |
|-------|----------|------|
| **goal-clarifier** | 模糊需求 | 主動引導釐清目標 |
| **data-source-advisor** | 詢問資料來源 | 協助配置資料管線 |
| **problem-diagnoser** | 效能問題 | 自動診斷推薦改善 |
| **result-analyzer** | 訓練/評估後 | 分析結果決策建議 |

## 使用方式

### 快速開始

```
# 教練引導
我想訓練一個模型

# 直接建立
/new-task entity-sentiment

# 列出任務
/tasks
```

### 完整流程

```
1. 啟動教練引導          → 釐清目標、痛點、資源
2. 配置資料來源          → 設定 DB、API、爬取、LLM 生成
3. 生成專案              → 產生腳本、配置、文件
4. 準備資料              → 執行資料生成腳本
5. 訓練模型              → 執行訓練腳本
6. 評估效能              → 分析結果、版本比較
7. 部署上線              → HuggingFace、Ollama
```

## 專案結構

每個任務是完全獨立的自包含專案：

```
{任務名稱}/
├── task.yaml               # 任務定義
├── data_source.yaml        # 資料來源配置（可重現）
├── versions/               # 版本追蹤（完整 lineage）
│   ├── v1/
│   │   ├── config.yaml
│   │   ├── data_snapshot.json
│   │   ├── results.json
│   │   └── lineage.yaml
│   └── v2/
├── data/
├── scripts/
├── configs/
├── models/
└── benchmarks/
```

## 資料來源配置

v3 的核心特色是可重現的資料管線：

```yaml
# data_source.yaml
sources:
  - type: database
    connection: postgresql://...
    query: "SELECT text, label FROM annotations"

  - type: api
    endpoint: https://api.example.com/data

  - type: web_scrape
    urls: ["https://..."]
    keywords: ["金融", "股票"]

  - type: llm_generated
    model: gpt-4o
    count: 500
```

## 內建知識庫

減少上網搜尋，內建 2025-2026 最新知識：

| 類別 | 內容 |
|------|------|
| **模型架構** | Dense vs MoE、MLA |
| **基礎模型** | Qwen3、DeepSeek-V3/R1、Llama 3.3 |
| **訓練方法** | SFT、LoRA、QLoRA、ORPO、DPO |
| **任務類型** | 情感分析、NER、關係抽取 |
| **問題排解** | 過擬合、類別不平衡、準確率低 |

## 環境需求

### 遠端伺服器（訓練用）
- GPU: NVIDIA GPU（建議 24GB+ VRAM）
- Python: 3.10+

### 本地開發
- Python: `uv run python`
- Claude Code: 最新版本

## 版本歷史

見 [CHANGELOG.md](skills/finetune-llm/CHANGELOG.md)

## 授權

MIT License

## 作者

Weifan Liao (weifanliao@eland.com.tw)
