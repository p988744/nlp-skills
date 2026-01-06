# Phase 5: 評估效能

## 概述

評估訓練後模型的效能，確認是否達到成功標準。

## 執行評估

```bash
python scripts/04_evaluate.py
```

## 評估流程

```
1. 載入模型
2. 對測試集推理
3. 計算指標
4. 生成報告
5. 判定是否通過
```

## 評估腳本核心

```python
from sklearn.metrics import classification_report, confusion_matrix
import json

def evaluate_model(model, tokenizer, test_data):
    predictions = []
    references = []

    for sample in test_data:
        # 推理
        output = generate(model, tokenizer, sample['input'])

        # 後處理
        prediction = parse_output(output)

        predictions.append(prediction)
        references.append(sample['expected'])

    # 計算指標
    report = classification_report(
        references,
        predictions,
        output_dict=True
    )

    return {
        'macro_f1': report['macro avg']['f1-score'],
        'accuracy': report['accuracy'],
        'per_class': {
            label: report[label]['f1-score']
            for label in set(references)
        },
        'confusion_matrix': confusion_matrix(references, predictions).tolist()
    }
```

## 評估指標

### 分類任務

| 指標 | 說明 | 建議閾值 |
|------|------|----------|
| Macro-F1 | 各類平均 F1 | >= 0.80 |
| Accuracy | 準確率 | >= 0.80 |
| Per-class F1 | 各類別 F1 | >= 0.70 |

### 抽取任務 (NER)

| 指標 | 說明 | 建議閾值 |
|------|------|----------|
| Entity F1 | 實體級 F1 | >= 0.70 |
| Precision | 精確率 | >= 0.70 |
| Recall | 召回率 | >= 0.70 |

### 生成任務

| 指標 | 說明 | 建議閾值 |
|------|------|----------|
| BLEU | 翻譯品質 | 任務相關 |
| ROUGE | 摘要品質 | 任務相關 |
| 人工評估 | 通過率 | >= 90% |

## 評估報告

### 格式

```yaml
# benchmarks/results/evaluation_report.yaml
task_name: financial-sentiment
evaluation_date: "2026-01-06"
model_path: models/adapter

metrics:
  macro_f1: 0.8980
  accuracy: 0.8967
  per_class:
    正面: 0.9119
    負面: 0.8869
    中立: 0.8952

confusion_matrix:
  - [91, 5, 4]   # 正面 → 正面/負面/中立
  - [6, 88, 6]   # 負面 → ...
  - [3, 7, 90]   # 中立 → ...

pass_criteria:
  macro_f1:
    threshold: 0.80
    actual: 0.8980
    passed: true

overall_status: PASSED
```

### 視覺化

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 混淆矩陣熱力圖
plt.figure(figsize=(8, 6))
sns.heatmap(
    confusion_matrix,
    annot=True,
    fmt='d',
    xticklabels=['正面', '負面', '中立'],
    yticklabels=['正面', '負面', '中立']
)
plt.xlabel('預測')
plt.ylabel('實際')
plt.title('混淆矩陣')
plt.savefig('benchmarks/results/confusion_matrix.png')
```

## RGL 評估 (可選)

RGL (Reliability, Generality, Locality) 三維評估：

### R - Reliability (可靠性)

- 主要任務效能
- 對應 Macro-F1

### G - Generality (泛化性)

- 通用能力保持
- 測試基礎模型能力是否下降

### L - Locality (局部性)

- 非目標行為保持
- 確認沒有負面影響

```python
rgl_score = (R * 0.5) + (G * 0.25) + (L * 0.25)
```

## 評估未通過處理

### 效能不足

1. 分析錯誤模式

```python
errors = [
    (sample, pred, ref)
    for sample, pred, ref in zip(test_data, predictions, references)
    if pred != ref
]

# 分析錯誤類型
error_patterns = Counter((ref, pred) for _, pred, ref in errors)
print("常見錯誤：", error_patterns.most_common(5))
```

2. 針對性改善
   - 增加該類型訓練資料
   - 調整 Prompt
   - 調整訓練超參數

### 某類別效能差

見 [troubleshooting/class-imbalance.md](../references/troubleshooting/class-imbalance.md)

## 評估檢查清單

- [ ] 測試集與訓練集無重疊
- [ ] 測試集覆蓋各類別
- [ ] 推理配置與訓練一致
- [ ] 後處理邏輯正確
- [ ] 指標計算正確

## 下一步

評估通過後進入 [Phase 6: 部署上線](06-deployment.md)

評估未通過則返回 Phase 3 或 Phase 4 進行改善。

---

*更新: 2026-01*
