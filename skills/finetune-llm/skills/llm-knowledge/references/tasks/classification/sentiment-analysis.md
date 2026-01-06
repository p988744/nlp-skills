# 情感分析 (Sentiment Analysis)

## 概述

情感分析判斷文本的情感傾向，是最常見的 NLP 分類任務之一。

## 任務類型

| 類型 | 說明 | 標籤範例 |
|------|------|----------|
| **文本情感** | 整段文本的情感 | 正面/負面/中立 |
| **實體情感** | 對特定實體的情感 | 台積電:正面, 聯電:負面 |
| **面向情感** | 對特定面向的情感 | 服務:正面, 價格:負面 |

## 資料格式

### 文本情感

```jsonl
{"input": "這家餐廳的食物非常美味，服務也很周到", "output": "正面"}
{"input": "等了一個小時，東西還是冷的", "output": "負面"}
{"input": "價格和品質都還可以接受", "output": "中立"}
```

### 實體情感

```jsonl
{"input": "台積電業績亮眼，但聯電表現令人失望", "entities": ["台積電", "聯電"], "output": {"台積電": "正面", "聯電": "負面"}}
```

## 訓練配置

### 標準配置 (三分類)

```yaml
model:
  base_model: "Qwen/Qwen3-4B"

lora:
  r: 32
  lora_alpha: 64
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

training:
  method: sft
  num_epochs: 8
  learning_rate: 1e-5
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
```

### 資料量建議

| 規模 | 樣本數 | 預期效果 |
|------|--------|----------|
| 小型 | 300-500 | 基本可用 |
| 中型 | 500-1000 | 較好效果 |
| 大型 | 1000-3000 | 穩定高效 |

## 領域適配

不同領域的情感表達差異大：

| 領域 | 特點 | 注意事項 |
|------|------|----------|
| **金融** | 專業術語、數據敏感 | 數字變化≠情感 |
| **產品評論** | 直接表達、面向多 | 注意諷刺 |
| **社群媒體** | 口語化、表情符號 | 網路用語 |
| **新聞** | 客觀為主、隱含立場 | 區分事實與觀點 |

### 金融領域範例

```jsonl
{"input": "公司營收年增 30%，創歷史新高", "output": "正面"}
{"input": "受原物料價格上漲影響，毛利率下滑 2%", "output": "負面"}
{"input": "營收符合市場預期，維持原有展望", "output": "中立"}
```

## Prompt 設計

### 基本 Prompt

```
你是情感分析專家。請分析以下文本的情感傾向。

文本：{text}

請只回答：正面、負面 或 中立
```

### 帶推理的 Prompt

```
你是情感分析專家。請分析以下文本的情感傾向。

文本：{text}

分析步驟：
1. 識別情感關鍵詞
2. 判斷整體傾向
3. 給出結論

情感：
```

## 評估指標

### 主要指標

- **Macro-F1**: 推薦作為主要指標（考慮類別平衡）
- **Per-class F1**: 分析各類別表現

### 評估腳本

```python
from sklearn.metrics import classification_report

report = classification_report(
    y_true,
    y_pred,
    target_names=['正面', '負面', '中立'],
    output_dict=True
)

print(f"Macro-F1: {report['macro avg']['f1-score']:.2%}")
```

## 常見問題

### 1. 中立類別表現差

**原因**: 中立邊界模糊，樣本可能偏少
**解決**:
- 明確中立的定義標準
- 增加中立樣本
- 考慮使用軟標籤

### 2. 諷刺識別錯誤

**症狀**: 諷刺語句被誤判為正面
**範例**: "服務真是好得不得了，等了一小時才來" → 實際負面
**解決**:
- 增加諷刺樣本
- 考慮上下文
- 使用專門的諷刺識別模組

### 3. 領域遷移效果差

**原因**: 不同領域情感表達差異大
**解決**:
- 使用領域內數據微調
- 混合通用 + 領域數據
- 領域適配訓練

## 實際案例

### 金融情感分析

```yaml
# 本專案實際配置
task_name: financial-sentiment
labels: [正面, 負面, 中立]
training_samples: 999
test_samples: 300

results:
  macro_f1: 89.80%
  positive_f1: 91.19%
  negative_f1: 88.69%
  neutral_f1: 89.52%
```

## 資料集資源

### 中文

| 資料集 | 領域 | 規模 |
|--------|------|------|
| ChnSentiCorp | 購物評論 | 10K |
| Weibo Sentiment | 微博 | 100K+ |
| 金融情感 | 財經新聞 | 需自建 |

### 英文

| 資料集 | 領域 | 規模 |
|--------|------|------|
| SST-2 | 電影評論 | 70K |
| Amazon Reviews | 產品評論 | 數百萬 |
| Financial PhraseBank | 金融 | 5K |

## 相關

- [class-imbalance.md](../../troubleshooting/class-imbalance.md) - 類別不平衡處理
- [sft.md](../../methods/finetuning/sft.md) - SFT 訓練方法
- [lora.md](../../methods/peft/lora.md) - LoRA 配置

---

*更新: 2026-01*
