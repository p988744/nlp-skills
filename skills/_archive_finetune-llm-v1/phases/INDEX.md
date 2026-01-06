# 工作流程階段索引

## 流程總覽

```
Phase 1          Phase 2          Phase 3          Phase 4          Phase 5          Phase 6
定義目標    →    生成專案    →    準備資料    →    訓練模型    →    評估效能    →    部署上線
   │               │               │               │               │               │
   ▼               ▼               ▼               ▼               ▼               ▼
task_def.yaml   tasks/目錄     data/*.jsonl    models/        results/       HuggingFace
```

## 階段詳情

| 階段 | 文件 | 輸入 | 輸出 | 預估時間 |
|------|------|------|------|----------|
| **Phase 1** | [01-define-objective.md](01-define-objective.md) | 使用者需求 | task_definition.yaml | 30 分鐘 |
| **Phase 2** | [02-generate-project.md](02-generate-project.md) | task_definition.yaml | 完整專案結構 | 自動 |
| **Phase 3** | [03-prepare-data.md](03-prepare-data.md) | 原始資料 | data/*.jsonl | 視資料量 |
| **Phase 4** | [04-training.md](04-training.md) | chat_format 資料 | LoRA adapter | 1-4 小時 |
| **Phase 5** | [05-evaluation.md](05-evaluation.md) | 模型 + 測試集 | 評估報告 | 10-30 分鐘 |
| **Phase 6** | [06-deployment.md](06-deployment.md) | 模型產出 | HuggingFace repos | 30 分鐘 |

## 快速導航

### 我想...

| 需求 | 前往 |
|------|------|
| 定義新任務 | [Phase 1: 定義目標](01-define-objective.md) |
| 了解資料格式 | [Phase 3: 準備資料](03-prepare-data.md) |
| 執行訓練 | [Phase 4: 訓練模型](04-training.md) |
| 查看評估指標 | [Phase 5: 評估效能](05-evaluation.md) |
| 上傳 HuggingFace | [Phase 6: 部署上線](06-deployment.md) |
| 改善既有模型 | [ITERATE-MODE.md](../ITERATE-MODE.md) |

## 相關資源

- [CREATE-MODE.md](../CREATE-MODE.md) - 完整建立流程
- [ITERATE-MODE.md](../ITERATE-MODE.md) - 改善既有任務
- [references/INDEX.md](../references/INDEX.md) - 知識庫
