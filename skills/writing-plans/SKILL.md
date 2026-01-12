---
name: writing-plans
description: |
  This skill should be used when the user asks to "write a plan", "create training plan", "plan my fine-tuning", "make a plan for model training", or when starting a new training task that requires multiple steps. Creates detailed implementation plans with bite-sized tasks for LLM fine-tuning workflows.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# Writing Plans - 訓練計畫撰寫

為 LLM fine-tuning 任務撰寫詳細的執行計畫，每個步驟都是 2-5 分鐘可完成的小任務。

## 核心原則

1. **粒度明確**：每個任務是單一動作（2-5 分鐘）
2. **完整記錄**：包含確切指令、預期輸出、驗證步驟
3. **可追蹤**：每個任務有明確狀態標記
4. **可重現**：任何人拿到計畫都能執行

## 計畫存放位置

```
{task-name}/
├── plans/
│   ├── 2026-01-07-initial-training.md
│   ├── 2026-01-10-improve-accuracy.md
│   └── 2026-01-15-add-data.md
├── task.yaml
└── versions/
```

## 計畫結構模板

```markdown
# {Goal} - 執行計畫

**建立日期**: YYYY-MM-DD
**任務**: {task-name}
**目標版本**: v{n}
**預計時間**: X 小時

## 目標概述

{1-2 句話描述這次迭代要達成什麼}

## 前置條件

- [ ] {條件 1}
- [ ] {條件 2}

## 技術方案

- **基礎模型**: {model}
- **訓練方法**: {method}
- **關鍵配置**: {config highlights}

---

## Tasks

### Task 1: {任務名稱} [pending]

**目標**: {這個任務要完成什麼}

**步驟**:
1. {具體動作}
2. {具體動作}

**驗證**:
- [ ] {驗證條件}

**預期輸出**:
```
{預期的輸出內容}
```

---

### Task 2: {任務名稱} [pending]

...

---

## 完成標準

- [ ] 所有 Tasks 標記為 [completed]
- [ ] 驗證全部通過
- [ ] lineage.yaml 已更新
```

## 任務狀態標記

| 標記 | 說明 |
|------|------|
| `[pending]` | 尚未開始 |
| `[in-progress]` | 執行中 |
| `[completed]` | 已完成 |
| `[blocked]` | 遇到阻礙 |
| `[skipped]` | 跳過（說明原因） |

## 撰寫流程

### 步驟 1: 收集資訊

確認以下資訊後才開始撰寫：

```
- 任務目標是什麼？
- 這是新任務還是迭代？
- 目標版本號？
- 有什麼資源限制？
- 成功標準是什麼？
```

### 步驟 2: 拆解任務

將目標拆解為 2-5 分鐘的小任務：

**LLM Fine-tuning 常見任務拆解**：

```
目標：訓練情感分析模型 v1

Task 1: 檢查資料格式 [pending]
Task 2: 產生訓練配置 [pending]
Task 3: 執行資料前處理 [pending]
Task 4: 啟動訓練腳本 [pending]
Task 5: 監控訓練進度 [pending]
Task 6: 執行評估腳本 [pending]
Task 7: 檢查評估結果 [pending]
Task 8: 更新 lineage.yaml [pending]
Task 9: 決定下一步 [pending]
```

### 步驟 3: 填充細節

每個任務必須包含：

1. **明確目標**：這個任務完成什麼
2. **具體步驟**：確切的指令或動作
3. **驗證條件**：如何確認完成
4. **預期輸出**：應該看到什麼

### 步驟 4: 審核計畫

撰寫完成後檢查：

- [ ] 每個任務都是 2-5 分鐘可完成
- [ ] 步驟足夠具體，不需要額外判斷
- [ ] 驗證條件明確
- [ ] 任務之間有正確的依賴順序

## 範例計畫

```markdown
# 實體情感分析 v1 - 執行計畫

**建立日期**: 2026-01-07
**任務**: entity-sentiment
**目標版本**: v1
**預計時間**: 3 小時

## 目標概述

建立實體情感分析模型的初始版本，目標 Macro-F1 > 0.75。

## 前置條件

- [x] 資料已準備 (500 筆)
- [x] GPU 環境已設定 (A100)
- [x] 依賴套件已安裝

## 技術方案

- **基礎模型**: Qwen/Qwen3-4B
- **訓練方法**: SFT + LoRA (r=32)
- **關鍵配置**: lr=1e-5, epochs=8

---

## Tasks

### Task 1: 驗證資料格式 [pending]

**目標**: 確認訓練資料格式正確

**步驟**:
1. 讀取 data/train.jsonl
2. 檢查欄位：text, entity, sentiment
3. 統計類別分佈

**驗證**:
- [ ] 所有必要欄位存在
- [ ] 無空值或異常值
- [ ] 類別分佈已記錄

**預期輸出**:
```
Total samples: 500
Classes: 正面(180), 負面(170), 中立(150)
Format: OK
```

---

### Task 2: 產生訓練配置 [pending]

**目標**: 建立 training_config.yaml

**步驟**:
1. 複製模板 configs/template.yaml
2. 填入：base_model, lora_r, learning_rate
3. 設定輸出路徑

**驗證**:
- [ ] 配置檔語法正確
- [ ] 路徑存在

---

### Task 3: 執行訓練 [pending]

**目標**: 啟動訓練並監控

**步驟**:
1. 執行: `python scripts/train.py --config configs/v1.yaml`
2. 監控 loss 曲線
3. 等待訓練完成

**驗證**:
- [ ] 訓練無錯誤完成
- [ ] Final loss < 0.5
- [ ] Checkpoint 已儲存

**預期輸出**:
```
Epoch 8/8: loss=0.32
Training completed. Model saved to models/v1/
```

---

### Task 4: 執行評估 [pending]

**目標**: 評估模型效能

**步驟**:
1. 執行: `python scripts/evaluate.py --model models/v1`
2. 檢查各類別 F1

**驗證**:
- [ ] Macro-F1 > 0.75
- [ ] 無類別 F1 < 0.60

---

### Task 5: 更新 Lineage [pending]

**目標**: 記錄版本資訊

**步驟**:
1. 建立 versions/v1/lineage.yaml
2. 填入訓練配置和結果
3. 記錄變更說明

**驗證**:
- [ ] lineage.yaml 格式正確
- [ ] 所有欄位已填寫

---

## 完成標準

- [ ] 所有 Tasks 標記為 [completed]
- [ ] Macro-F1 > 0.75
- [ ] lineage.yaml 已建立
```

## 計畫命名規則

```
YYYY-MM-DD-{goal}.md

範例：
2026-01-07-initial-training.md
2026-01-10-improve-neutral-class.md
2026-01-15-expand-dataset.md
```

## 執行方式

計畫撰寫完成後，有兩種執行方式：

1. **使用 executing-plans skill**：批次執行，每 3 個任務暫停 review
2. **手動逐步執行**：自行按照計畫步驟操作

## 相關資源

- [executing-plans](../executing-plans/SKILL.md) - 批次執行計畫
- [task-manager](../task-manager/SKILL.md) - 任務管理
- [llm-coach](../llm-coach/SKILL.md) - 教練引導
