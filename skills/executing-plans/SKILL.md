---
name: executing-plans
description: |
  This skill should be used when the user asks to "execute plan", "run the plan", "start executing", "continue plan execution", or has a plan file ready to execute. Manages phased implementation with batch execution and checkpoint reviews.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Executing Plans - 計畫執行

批次執行訓練計畫，每 3 個任務暫停進行 checkpoint review。

## 核心原則

1. **批次執行**：預設每 3 個任務為一批
2. **Checkpoint Review**：每批完成後暫停，報告進度，等待回饋
3. **嚴格遵循**：按計畫步驟執行，不自行判斷
4. **遇阻即停**：遇到問題立即停止，請求協助

## 執行流程

```
Phase 1: 載入計畫
    ↓
Phase 2: 審核計畫
    ↓
Phase 3: 批次執行 (3 tasks)
    ↓
Phase 4: Checkpoint 報告
    ↓
Phase 5: 等待回饋
    ↓
[重複 Phase 3-5 直到完成]
    ↓
Phase 6: 最終完成
```

## Phase 1: 載入計畫

```markdown
請提供計畫檔案路徑，或指定任務名稱：

1. 指定檔案：`entity-sentiment/plans/2026-01-07-initial-training.md`
2. 指定任務：自動尋找最新計畫
```

載入後顯示計畫摘要：

```
📋 計畫載入完成

任務: entity-sentiment
目標: 初始訓練 v1
建立日期: 2026-01-07

Tasks 總數: 5
- [pending] 4 個
- [completed] 1 個

準備開始執行？
```

## Phase 2: 審核計畫

**在執行前必須審核計畫**：

1. 閱讀目標概述
2. 檢查前置條件是否滿足
3. 確認技術方案合理
4. 如有疑慮，先提出討論

```
⚠️ 計畫審核

前置條件檢查：
- [x] 資料已準備 (500 筆)
- [x] GPU 環境已設定
- [ ] 依賴套件已安裝 ← 需要先安裝

建議：先執行 pip install -r requirements.txt

是否繼續？還是先處理前置條件？
```

## Phase 3: 批次執行

### 執行規則

1. 預設每批 3 個任務（可調整）
2. 依序執行，不跳過
3. 每個任務：
   - 標記 `[in-progress]`
   - 執行步驟
   - 執行驗證
   - 標記 `[completed]` 或 `[blocked]`
4. 更新計畫檔案中的狀態

### 執行格式

```
🔄 開始批次 1/2 (Task 1-3)

---
▶️ Task 1: 驗證資料格式 [in-progress]

執行中...
✓ 讀取 data/train.jsonl
✓ 檢查欄位完整
✓ 統計類別分佈

驗證結果：
✓ 所有必要欄位存在
✓ 無空值或異常值
✓ 類別分佈已記錄

輸出：
Total samples: 500
Classes: 正面(180), 負面(170), 中立(150)

✅ Task 1: 驗證資料格式 [completed]

---
▶️ Task 2: 產生訓練配置 [in-progress]
...
```

## Phase 4: Checkpoint 報告

每批完成後，產生 checkpoint 報告：

```
📊 Checkpoint Report - 批次 1/2 完成

已完成 Tasks:
✅ Task 1: 驗證資料格式
✅ Task 2: 產生訓練配置
✅ Task 3: 執行訓練

結果摘要：
- 資料格式正確，500 筆樣本
- 配置檔已產生：configs/v1.yaml
- 訓練完成，final loss = 0.32

待執行 Tasks:
⏳ Task 4: 執行評估
⏳ Task 5: 更新 Lineage

---
🛑 暫停等待回饋

請確認目前進度，回覆後繼續執行：
- 輸入 "continue" 或 "繼續" → 執行下一批
- 輸入 "stop" 或 "停止" → 結束執行
- 提供其他指示 → 調整後繼續
```

## Phase 5: 等待回饋

**必須等待使用者回應後才能繼續**：

| 回應 | 動作 |
|------|------|
| `continue` / `繼續` | 執行下一批 |
| `stop` / `停止` | 結束執行，保留進度 |
| `skip task N` | 跳過指定任務 |
| `redo task N` | 重新執行指定任務 |
| 其他指示 | 根據指示調整 |

## Phase 6: 最終完成

所有任務完成後：

```
🎉 計畫執行完成！

執行摘要：
- 總任務數: 5
- 已完成: 5
- 跳過: 0
- 阻塞: 0

成果：
- 模型已訓練：models/v1/
- Macro-F1: 0.78
- Lineage 已更新

下一步建議：
1. 檢查 versions/v1/lineage.yaml
2. 如需改善，使用 /nlp-skills:write-plan 建立新計畫
3. 部署模型使用 /nlp-skills:deploy
```

## 遇阻處理

### 立即停止的情況

遇到以下情況必須立即停止，請求協助：

1. **執行錯誤**：腳本報錯、指令失敗
2. **驗證失敗**：無法通過驗證條件
3. **計畫不清**：步驟描述不明確
4. **缺少依賴**：檔案不存在、套件未安裝
5. **結果異常**：輸出與預期差異過大

### 阻塞報告格式

```
🚫 Task 3 執行阻塞

問題：訓練腳本報錯
錯誤訊息：
```
CUDA out of memory. Tried to allocate 2.00 GiB
```

可能原因：
1. batch_size 太大
2. 模型太大
3. GPU 記憶體不足

建議解決方案：
1. 降低 batch_size 從 8 改為 4
2. 啟用 gradient checkpointing
3. 使用更小的模型

請指示如何處理？
```

## 配置選項

### 調整批次大小

```
預設每批 3 個任務。如需調整：

"使用批次大小 5 執行計畫"
"每完成 1 個任務就暫停"
```

### 跳過 Checkpoint

```
如需連續執行不暫停（不建議）：

"連續執行所有任務不暫停"
```

## 計畫檔案更新

執行過程中會即時更新計畫檔案：

```markdown
### Task 1: 驗證資料格式 [completed]  ← 更新狀態

**完成時間**: 2026-01-07 14:30        ← 新增
**實際輸出**:                         ← 新增
```
Total samples: 500
Classes: 正面(180), 負面(170), 中立(150)
```
```

## 最佳實踐

### Do

- ✅ 執行前先審核計畫
- ✅ 每個 checkpoint 確認進度
- ✅ 遇到問題立即報告
- ✅ 保持計畫檔案更新

### Don't

- ❌ 跳過 checkpoint review
- ❌ 自行判斷跳過任務
- ❌ 忽略驗證失敗
- ❌ 修改計畫而不通知

## 相關資源

- [writing-plans](../writing-plans/SKILL.md) - 撰寫計畫
- [task-manager](../task-manager/SKILL.md) - 任務管理
- [problem-diagnoser](../../agents/problem-diagnoser.md) - 問題診斷
