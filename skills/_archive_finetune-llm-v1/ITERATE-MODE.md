# Iterate Mode: 改善既有任務

本文件引導你分析並改善既有的 LLM 訓練任務。

## 流程總覽

```
Step 1: 載入既有任務
    │
    ▼
Step 2: 分析問題
    │
    ▼
Step 3: 提出改善建議
    │
    ▼
Step 4: 執行改善
    │
    ▼
Step 5: 比較結果
```

---

## Step 1: 載入既有任務

### 掃描可用任務

```bash
ls tasks/
# entity-sentiment/
# stance/
# official-doc/
```

### 讀取任務資訊

載入以下檔案以了解任務現狀：

| 檔案 | 內容 |
|------|------|
| `task_definition.yaml` | 任務定義、目標指標 |
| `configs/training_config.yaml` | 訓練超參數 |
| `benchmarks/results/*.json` | 評估結果 |
| `data/` | 資料統計 |
| `iterations/` | 歷史迭代記錄 |

### 任務狀態摘要

自動生成任務狀態：

```markdown
## 任務: entity-sentiment

### 基本資訊
- 任務類型: 分類（情感分析）
- 基礎模型: Qwen/Qwen3-4B
- 訓練方法: SFT + LoRA r=32

### 目前效能
| 指標 | 分數 | 目標 | 差距 |
|------|------|------|------|
| Macro-F1 | 72.0% | 80.0% | -8.0% |
| Accuracy | 72.0% | 80.0% | -8.0% |

### 各類別表現
| 類別 | F1 | 問題 |
|------|-----|------|
| 正面 | 78% | - |
| 負面 | 72% | - |
| 中立 | 62% | ⚠️ 偏低 |

### 資料統計
- 訓練集: 333 筆
- 類別分佈: 正面 40%, 負面 35%, 中立 25%
```

---

## Step 2: 分析問題

### 自動診斷

根據評估結果自動分析可能問題：

```python
# 診斷邏輯
if macro_f1 < target:
    if min(per_class_f1) < 0.6:
        issues.append("類別不平衡：某類別 F1 過低")
    if train_samples < 500:
        issues.append("資料不足：訓練樣本少於 500")
    if lora_rank < 32:
        issues.append("模型容量：考慮增加 LoRA rank")
```

### 問題分類

| 問題類型 | 症狀 | 參考 |
|----------|------|------|
| **資料問題** | 某類別 F1 低、資料量不足 | [class-imbalance.md](references/troubleshooting/class-imbalance.md) |
| **模型問題** | 整體效能低、欠擬合 | [underfitting.md](references/troubleshooting/underfitting.md) |
| **過擬合** | train loss 低但 eval loss 高 | [overfitting.md](references/troubleshooting/overfitting.md) |
| **輸出格式** | JSON 解析失敗 | [output-format.md](references/troubleshooting/output-format.md) |

### 錯誤案例分析

讀取 `benchmarks/results/` 中的預測結果，分析錯誤模式：

```markdown
## 錯誤分析

### 主要錯誤類型
| 錯誤類型 | 數量 | 佔比 |
|----------|------|------|
| 中立 → 正面 | 15 | 25% |
| 中立 → 負面 | 12 | 20% |
| 負面 → 中立 | 10 | 17% |

### 典型錯誤案例
1. **中立誤判為正面**
   - 輸入: "央行維持利率不變"
   - 預測: 正面
   - 正確: 中立
   - 分析: 模型可能將「維持」解讀為正面訊號
```

---

## Step 3: 提出改善建議

### 建議矩陣

| 問題 | 建議方案 | 預期效果 | 難度 |
|------|----------|----------|------|
| 中立 F1 低 | 增加中立樣本 200+ | +5-10% F1 | 低 |
| 資料量不足 | GPT 輔助生成 + 人工審核 | +5-15% | 中 |
| 類別不平衡 | 過採樣或加權損失 | +3-8% | 低 |
| 整體偏低 | 增加 LoRA rank 到 64 | +2-5% | 低 |
| 過擬合 | 增加 dropout, 減少 epochs | 穩定性 | 低 |

### 優先順序

1. **快速見效**：類別平衡、超參數調整
2. **中期改善**：增加資料
3. **長期優化**：資料品質提升、模型架構調整

---

## Step 4: 執行改善

### 4.1 更新配置

```yaml
# configs/training_config.yaml (v2)

lora:
  r: 64          # 從 32 增加到 64
  alpha: 128

training:
  epochs: 6      # 從 8 減少到 6（防止過擬合）
  class_weights:
    正面: 1.0
    負面: 1.2
    中立: 1.5    # 增加中立類別權重
```

### 4.2 增加資料（如需要）

```bash
# 使用 GPT 生成更多中立類別樣本
python scripts/generate_data_gpt.py \
  --target_class "中立" \
  --num_samples 200 \
  --output data/raw/generated_neutral.jsonl
```

### 4.3 重新訓練

```bash
cd tasks/{task_name}

# 執行訓練（版本 2）
python scripts/03_train.py --version v2

# 或一鍵執行
./scripts/run_pipeline.sh --version v2
```

### 4.4 記錄迭代

自動記錄到 `iterations/v2/`：

```
iterations/
├── v1/
│   ├── config_snapshot.yaml
│   ├── results.json
│   └── notes.md
└── v2/
    ├── config_snapshot.yaml
    ├── results.json
    ├── notes.md
    └── changes.md            # 相對 v1 的改動
```

---

## Step 5: 比較結果

### 版本比較報告

```markdown
# 版本比較: v1 → v2

## 改動摘要
- LoRA rank: 32 → 64
- Epochs: 8 → 6
- 新增中立樣本: 200 筆
- 啟用類別權重

## 效能比較

| 指標 | v1 | v2 | 變化 |
|------|-----|-----|------|
| Macro-F1 | 72.0% | 81.5% | +9.5% ✅ |
| Accuracy | 72.0% | 82.0% | +10.0% ✅ |

## 各類別比較

| 類別 | v1 F1 | v2 F1 | 變化 |
|------|-------|-------|------|
| 正面 | 78% | 85% | +7% |
| 負面 | 72% | 80% | +8% |
| 中立 | 62% | 79% | +17% ✅ |

## 決策

✅ v2 達標，採用為新的正式版本
```

### 決策選項

1. **採用新版**：效能達標，更新部署
2. **繼續調整**：仍有改善空間，進行 v3 迭代
3. **回滾舊版**：新版效能下降，維持舊版

---

## 常見改善策略

### 策略 1: 資料增強

適用：資料量不足、類別不平衡

```bash
# 過採樣少數類別
python scripts/oversample.py --target_count 500

# GPT 輔助生成
python scripts/generate_data_gpt.py --num_samples 300
```

### 策略 2: 超參數調整

適用：模型容量不足或過擬合

| 問題 | 調整 |
|------|------|
| 欠擬合 | 增加 LoRA rank, epochs |
| 過擬合 | 減少 epochs, 增加 dropout |
| 訓練不穩定 | 降低 learning rate |

### 策略 3: 訓練方法升級

適用：SFT 效果有限

```yaml
# 從 SFT 升級到 ORPO
training:
  method: "orpo"
  beta: 0.1
```

需要準備 chosen/rejected 配對資料。

### 策略 4: 模型升級

適用：需要更強能力

| 升級路徑 | 效果 | 成本 |
|----------|------|------|
| Qwen3-4B → Qwen3-8B | +3-5% | 2x VRAM |
| Dense → MoE | +5-10% | 需要適配 |

---

## 迭代最佳實踐

1. **一次只改一個變數**：方便定位效果來源
2. **保留完整記錄**：所有迭代都記錄到 `iterations/`
3. **設定明確目標**：每次迭代有具體的改善目標
4. **快速驗證**：先在小資料集測試，再全量訓練
5. **定期清理**：移除明確失敗的迭代版本

---

## 相關資源

- [references/troubleshooting/](references/troubleshooting/) - 問題排解
- [references/methods/](references/methods/) - 訓練方法比較
- [CREATE-MODE.md](CREATE-MODE.md) - 如需從頭建立
