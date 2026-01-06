---
description: 配置任務的資料來源
argument-hint: [task-name]
allowed-tools: Read, Write, Edit, AskUserQuestion, Grep, Glob
model: sonnet
---

配置 LLM 訓練任務的資料來源，支援資料庫、API、爬取、LLM 生成等多種來源。

## 參數

- `$1`: 任務名稱（如果未提供，掃描現有任務供選擇）

## 配置流程

### 1. 確認任務

如果沒有提供 $1：
- 掃描所有 `*/task.yaml` 檔案
- 列出可選任務供使用者選擇

### 2. 詢問資料來源類型

使用 AskUserQuestion 詢問資料來源：

```
資料從哪裡來？

□ database - 資料庫查詢（PostgreSQL, MySQL, SQLite）
□ api - API 串接（REST, GraphQL）
□ web_scrape - 網頁爬取
□ llm_generated - LLM 生成合成資料
□ file_import - 匯入現有檔案（CSV, JSON, JSONL）
```

可選擇多個來源。

### 3. 依類型收集配置

#### Database 資料庫

詢問：
- 資料庫類型（PostgreSQL, MySQL, SQLite）
- 連線資訊（host, port, database）
- 查詢語句（SELECT ...）
- 欄位對應（text, label 等）

生成配置：
```yaml
- name: db_annotations
  type: database
  enabled: true
  config:
    driver: postgresql
    host: ${DB_HOST}
    port: 5432
    database: ${DB_NAME}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  query: |
    SELECT text, label FROM annotations
    WHERE status = 'approved'
  output:
    format: jsonl
    path: data/raw/db_data.jsonl
```

#### API 串接

詢問：
- API 端點 URL
- 認證方式（Bearer Token, API Key）
- 查詢參數
- 分頁方式

生成配置：
```yaml
- name: api_data
  type: api
  enabled: true
  config:
    base_url: https://api.example.com
    auth:
      type: bearer
      token: ${API_TOKEN}
  requests:
    - endpoint: /data
      method: GET
      params:
        limit: 1000
```

#### Web Scrape 爬取

詢問：
- 目標 URL 列表
- 爬取方式（requests 或 playwright）
- 關鍵字過濾
- rate limit

生成配置：
```yaml
- name: web_data
  type: web_scrape
  enabled: true
  config:
    method: playwright
    urls:
      - https://example.com/page1
    keywords:
      - 金融
      - 股票
    rate_limit: 1
```

#### LLM Generated 生成

詢問：
- 使用哪個模型（gpt-4o, claude-3 等）
- 要生成哪些標籤的資料
- 每個標籤生成多少筆
- 是否需要人工審核

生成配置：
```yaml
- name: synthetic_data
  type: llm_generated
  enabled: true
  config:
    model: gpt-4o
    temperature: 0.7
    api_key: ${OPENAI_API_KEY}
  generation:
    prompt_template: |
      生成 {count} 筆訓練資料...
    variations:
      - label: 正面
        count: 100
  validation:
    require_review: true
```

#### File Import 匯入

詢問：
- 檔案路徑
- 檔案格式（CSV, JSON, JSONL）
- 欄位對應

生成配置：
```yaml
- name: imported_data
  type: file_import
  enabled: true
  config:
    source_path: /path/to/data.csv
    format: csv
  mapping:
    text: content_column
    label: sentiment_column
```

### 4. 配置資料合併

詢問是否需要合併多個來源：
- 去重方式（按 text 欄位）
- 是否打亂順序
- 隨機種子

### 5. 配置資料分割

確認分割比例：
- train: 70%
- valid: 15%
- test: 15%
- 分層抽樣依據（label）

### 6. 生成 data_source.yaml

將所有配置寫入 `{task_name}/data_source.yaml`

### 7. 生成重新生成腳本

自動生成 `scripts/01_regenerate_data.py`，包含從各來源取得資料的邏輯。

### 8. 環境變數提醒

列出需要設定的環境變數：
```
需要設定的環境變數：
- DB_HOST: 資料庫主機
- DB_USER: 資料庫使用者
- DB_PASSWORD: 資料庫密碼
- API_TOKEN: API 認證 Token
- OPENAI_API_KEY: OpenAI API Key

建議使用 .env 檔案管理，並加入 .gitignore
```

## 完成提示

```
資料來源配置完成！

配置檔案: {task_name}/data_source.yaml
重新生成腳本: {task_name}/scripts/01_regenerate_data.py

下一步：
1. 設定環境變數
2. 執行 python scripts/01_regenerate_data.py 生成資料
3. 執行 python scripts/02_validate_data.py 驗證資料
```
