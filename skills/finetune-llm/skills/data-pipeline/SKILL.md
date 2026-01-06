---
name: data-pipeline
description: |
  This skill should be used when the user asks to "configure data source", "data from database", "fetch data from API", "scrape web data", "generate training data with LLM", "regenerate data", "data pipeline", "where does data come from", or needs to set up reproducible data collection. Provides data source configuration, reproducibility tracking, and data regeneration capabilities.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebFetch
---

# Data Pipeline - 資料管線配置

配置可重現的資料來源，追蹤資料生成方式，支援後續模型迭代。

## 核心理念

v2 的關鍵特色是**資料可重現性**：

- 記錄資料來源配置（DB、API、爬取、LLM 生成）
- 任何時候都能重新生成相同的資料
- 模型迭代時可以追溯資料來源

## 支援的資料來源

| 來源類型 | 說明 | 適用場景 |
|----------|------|----------|
| `database` | SQL 資料庫查詢 | 既有標註資料 |
| `api` | REST/GraphQL API | 外部資料服務 |
| `web_scrape` | 網頁爬取 | 公開資料收集 |
| `llm_generated` | LLM 生成 | 資料增強、合成資料 |
| `file_import` | 檔案匯入 | 現有 CSV/JSON/JSONL |

## data_source.yaml 規格

### 完整範例

```yaml
# data_source.yaml
version: "1.0"
created: 2026-01-06T10:00:00
updated: 2026-01-06T14:30:00

# 資料來源列表（按順序處理）
sources:
  # 來源 1: 資料庫
  - name: production_annotations
    type: database
    enabled: true
    config:
      driver: postgresql
      host: db.example.com
      port: 5432
      database: nlp_annotations
      # 敏感資訊使用環境變數
      username: ${DB_USER}
      password: ${DB_PASSWORD}
    query: |
      SELECT
        text,
        entity,
        sentiment as label,
        annotator,
        created_at
      FROM annotations
      WHERE status = 'approved'
        AND task_type = 'entity_sentiment'
      ORDER BY created_at
    output:
      format: jsonl
      path: data/raw/db_annotations.jsonl
      fields:
        - text
        - entity
        - label

  # 來源 2: API
  - name: sentiment_api
    type: api
    enabled: true
    config:
      base_url: https://api.dataservice.com/v1
      auth:
        type: bearer
        token: ${API_TOKEN}
    requests:
      - endpoint: /annotations
        method: GET
        params:
          task: entity_sentiment
          status: approved
          limit: 1000
        pagination:
          type: cursor
          cursor_field: next_cursor
    output:
      format: jsonl
      path: data/raw/api_data.jsonl
      transform: |
        {
          "text": item.content,
          "entity": item.target_entity,
          "label": item.sentiment_label
        }

  # 來源 3: 網頁爬取
  - name: finance_news
    type: web_scrape
    enabled: true
    config:
      method: playwright  # 或 requests, scrapy
      urls:
        - https://finance.example.com/news
      selectors:
        title: h1.article-title
        content: div.article-content
        date: span.publish-date
      keywords:
        - 台積電
        - 聯電
        - 金融
      rate_limit: 1  # 每秒請求數
    output:
      format: jsonl
      path: data/raw/scraped_news.jsonl

  # 來源 4: LLM 生成
  - name: synthetic_neutral
    type: llm_generated
    enabled: true
    config:
      model: gpt-4o
      temperature: 0.7
      api_key: ${OPENAI_API_KEY}
    generation:
      prompt_template: |
        生成 {count} 筆金融新聞情感分析的訓練資料。

        要求：
        - 情感標籤：{label}
        - 領域：金融、股票、投資
        - 包含具體的公司或股票名稱作為實體
        - 文本長度：50-200 字

        輸出 JSON 格式：
        {"text": "...", "entity": "...", "label": "{label}"}

        每行一個 JSON，不要其他說明。
      variations:
        - label: 中立
          count: 200
        - label: 正面
          count: 100
        - label: 負面
          count: 100
    output:
      format: jsonl
      path: data/raw/generated_data.jsonl
    validation:
      # 生成後人工審核
      require_review: true
      review_sample: 0.1  # 抽樣 10% 審核

  # 來源 5: 檔案匯入
  - name: existing_dataset
    type: file_import
    enabled: true
    config:
      source_path: /path/to/existing/data.csv
      format: csv
      encoding: utf-8
      delimiter: ","
    mapping:
      text: content_column
      entity: target_column
      label: sentiment_column
    output:
      format: jsonl
      path: data/raw/imported_data.jsonl

# 資料合併設定
merge:
  enabled: true
  output_path: data/raw/merged.jsonl
  deduplication:
    enabled: true
    key: text  # 以 text 欄位去重
  shuffle: true
  random_seed: 42

# 資料分割設定
split:
  enabled: true
  ratios:
    train: 0.7
    valid: 0.15
    test: 0.15
  stratify_by: label  # 按標籤分層抽樣
  random_seed: 42
  output:
    train: data/train.jsonl
    valid: data/valid.jsonl
    test: data/test.jsonl

# 重新生成配置
regeneration:
  script: scripts/01_regenerate_data.py
  last_run: 2026-01-06T10:30:00
  triggers:
    - source_config_changed
    - manual
```

### 各來源類型詳解

#### Database 資料庫

```yaml
- name: db_source
  type: database
  config:
    driver: postgresql  # postgresql, mysql, sqlite
    host: localhost
    port: 5432
    database: mydb
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  query: |
    SELECT * FROM table WHERE condition
  output:
    format: jsonl
    path: data/raw/db_data.jsonl
```

**支援的資料庫**:
- PostgreSQL
- MySQL
- SQLite
- SQL Server (需額外 driver)

#### API 串接

```yaml
- name: api_source
  type: api
  config:
    base_url: https://api.example.com
    auth:
      type: bearer  # bearer, basic, api_key
      token: ${API_TOKEN}
  requests:
    - endpoint: /data
      method: GET
      params:
        limit: 100
      pagination:
        type: offset  # offset, cursor, page
        offset_param: offset
        limit_param: limit
```

**認證方式**:
- Bearer Token
- Basic Auth
- API Key (header 或 query param)

#### Web Scrape 爬取

```yaml
- name: scrape_source
  type: web_scrape
  config:
    method: playwright  # playwright, requests
    urls:
      - https://example.com/page1
      - https://example.com/page2
    selectors:
      title: h1
      content: div.content
    rate_limit: 1
```

**注意事項**:
- 遵守 robots.txt
- 設定合理的 rate limit
- 處理動態載入內容用 playwright

#### LLM Generated 生成

```yaml
- name: llm_source
  type: llm_generated
  config:
    model: gpt-4o  # gpt-4o, claude-3, etc.
    temperature: 0.7
  generation:
    prompt_template: |
      生成訓練資料...
    variations:
      - label: 正面
        count: 100
  validation:
    require_review: true
```

**最佳實踐**:
- 生成後抽樣人工審核
- 設定明確的 prompt 格式要求
- 分批生成避免重複

#### File Import 匯入

```yaml
- name: file_source
  type: file_import
  config:
    source_path: /path/to/data.csv
    format: csv  # csv, json, jsonl
    encoding: utf-8
  mapping:
    text: source_column
    label: target_column
```

## 資料生成腳本

### 01_regenerate_data.py

自動生成的重新生成腳本：

```python
#!/usr/bin/env python
"""
根據 data_source.yaml 重新生成所有資料。
自動產生，請勿手動修改。
"""

import yaml
from pathlib import Path
from data_pipeline import (
    DatabaseSource,
    APISource,
    WebScrapeSource,
    LLMGeneratedSource,
    FileImportSource,
    DataMerger,
    DataSplitter
)

def main():
    # 載入配置
    config = yaml.safe_load(open('data_source.yaml'))

    # 處理各資料來源
    for source in config['sources']:
        if not source.get('enabled', True):
            continue

        if source['type'] == 'database':
            DatabaseSource(source).fetch()
        elif source['type'] == 'api':
            APISource(source).fetch()
        elif source['type'] == 'web_scrape':
            WebScrapeSource(source).fetch()
        elif source['type'] == 'llm_generated':
            LLMGeneratedSource(source).generate()
        elif source['type'] == 'file_import':
            FileImportSource(source).import_data()

    # 合併資料
    if config.get('merge', {}).get('enabled'):
        DataMerger(config['merge']).merge()

    # 分割資料
    if config.get('split', {}).get('enabled'):
        DataSplitter(config['split']).split()

    print("資料重新生成完成！")

if __name__ == '__main__':
    main()
```

## 資料驗證

生成資料後自動驗證：

```python
# 驗證項目
validations:
  - format_check:      # JSON 格式正確
  - required_fields:   # 必要欄位存在
  - label_values:      # 標籤值在允許範圍內
  - text_length:       # 文本長度合理
  - duplicate_check:   # 重複檢查
  - distribution:      # 類別分佈統計
```

### 驗證報告

```
資料驗證報告
============

總筆數: 1000
有效筆數: 987 (98.7%)
問題筆數: 13 (1.3%)

問題明細:
- 格式錯誤: 3 筆
- 缺少必要欄位: 5 筆
- 文本過短 (<10字): 5 筆

類別分佈:
- 正面: 380 (38.5%)
- 負面: 335 (33.9%)
- 中立: 272 (27.6%)

建議:
- 中立類別比例偏低，考慮增加合成資料
```

## 最佳實踐

### 敏感資訊處理

```yaml
# 使用環境變數
config:
  password: ${DB_PASSWORD}
  api_key: ${API_KEY}

# .env 檔案（不要 commit）
DB_PASSWORD=secret
API_KEY=sk-xxx
```

### 版本追蹤

每次生成資料時記錄：

```yaml
# data/data_version.yaml
version: "2026-01-06-001"
source_config_hash: abc123
total_records: 1000
class_distribution:
  正面: 380
  負面: 335
  中立: 285
generated_at: 2026-01-06T10:30:00
```

### 增量更新

支援只更新特定來源：

```bash
# 只重新生成 LLM 資料
python scripts/01_regenerate_data.py --source synthetic_neutral

# 重新生成所有
python scripts/01_regenerate_data.py --all
```

## 相關資源

### 指令
- `/nlp-skills:data-source` - 配置資料來源

### 其他 Skills
- [task-manager](../task-manager/SKILL.md) - 任務管理
- [llm-coach](../llm-coach/SKILL.md) - 教練式引導
