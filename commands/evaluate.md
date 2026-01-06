---
description: 執行模型評估並分析結果
argument-hint: [task-name] [version]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
model: sonnet
---

執行模型評估，分析結果，並提供改善建議。

## 參數

- `$1`: 任務名稱
- `$2`: 版本號（可選，預設為當前版本）

## 評估流程

### 1. 確認任務和版本

讀取 `$1/task.yaml` 取得：
- 當前版本
- 成功標準
- 主要評估指標

如果指定 $2，使用該版本；否則使用當前版本。

### 2. 檢查模型檔案

確認模型檔案存在：
- `$1/models/adapter/{version}/` - LoRA adapter
- 或 `$1/models/merged/{version}/` - 合併模型

### 3. 執行評估腳本

```bash
cd $1 && python scripts/05_evaluate.py --version {version}
```

### 4. 讀取評估結果

從 `benchmarks/results/{version}_results.json` 讀取：
- 整體指標（accuracy, macro_f1, etc.）
- 各類別指標
- 混淆矩陣
- 錯誤案例

### 5. 生成評估報告

```markdown
# {task_name} 評估報告 - {version}

## 整體表現

| 指標 | 分數 | 目標 | 狀態 |
|------|------|------|------|
| Accuracy | {acc}% | {target}% | ✅/❌ |
| Macro-F1 | {f1}% | {target}% | ✅/❌ |

## 各類別表現

| 類別 | Precision | Recall | F1 | Support |
|------|-----------|--------|-----|---------|
| ... | ... | ... | ... | ... |

## 混淆矩陣

{confusion_matrix}

## 錯誤分析

### 主要錯誤類型
| 錯誤類型 | 數量 | 佔比 |
|----------|------|------|
| {A} → {B} | N | X% |

### 典型錯誤案例
1. **案例 1**
   - 輸入: "..."
   - 預測: {predicted}
   - 正確: {actual}
   - 分析: ...
```

### 6. 決策建議

根據評估結果提供建議：

**達標情況**：
```
✅ 效能達標！

建議：
1. 進入部署流程 /nlp-skills:deploy
2. 或繼續優化追求更高效能
```

**未達標情況**：
使用 Task 工具觸發 problem-diagnoser agent 進行深入分析，提供具體改善建議。

```
❌ 效能未達標

主要問題：
- {問題1}
- {問題2}

建議改善方向：
1. {建議1}
2. {建議2}

下一步：
- 使用 /nlp-skills:coach 討論改善方案
```

### 7. 記錄版本 lineage

將評估結果記錄到 `versions/{version}/lineage.yaml`：

```yaml
results:
  macro_f1: {score}
  accuracy: {score}
  per_class:
    {class}: {f1}
  evaluated_at: {timestamp}
```

### 8. 版本比較（如果有前一版本）

如果存在前一版本，自動進行比較：

```markdown
## 版本比較: {prev_version} → {version}

| 指標 | {prev_version} | {version} | 變化 |
|------|----------------|-----------|------|
| Macro-F1 | {old}% | {new}% | +X% / -X% |
| ... | ... | ... | ... |

結論：
- {改善/退步}主要在 {類別}
- 原因分析: ...
```

## 完成提示

```
評估完成！

報告: {task_name}/benchmarks/results/{version}_report.md
結果: {task_name}/benchmarks/results/{version}_results.json

效能摘要:
- Macro-F1: {score}% ({target}% 目標)
- 狀態: ✅ 達標 / ❌ 未達標

{建議}
```
