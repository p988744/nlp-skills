---
name: llm-knowledge
description: |
  This skill should be used when the user asks "what is LoRA", "compare models", "which model is best for Chinese", "SFT vs DPO", "how to handle overfitting", "class imbalance solution", "model architecture", "training method comparison", or needs reference information about LLM fine-tuning. Provides structured knowledge base for models, methods, architectures, and troubleshooting.
allowed-tools: Read, Grep, Glob
---

# LLM Knowledge - 知識庫

提供 LLM fine-tuning 相關的結構化知識，減少上網搜尋時間。

## 知識範圍

本知識庫涵蓋以下領域（知識截止：2026-01）：

| 領域 | 內容 |
|------|------|
| 模型架構 | Dense, MoE, MLA |
| 基礎模型 | Qwen, DeepSeek, Llama, Phi |
| 訓練方法 | SFT, LoRA, QLoRA, DoRA |
| 對齊方法 | DPO, ORPO, KTO, SimPO |
| 任務類型 | 分類、NER、生成 |
| 問題排解 | 過擬合、欠擬合、類別不平衡 |

## 快速查詢

### 模型選擇

| 需求 | 推薦模型 | 說明 |
|------|----------|------|
| 中文任務 | Qwen3-4B/8B | 中文能力最強 |
| 推理任務 | DeepSeek-R1 | 推理鏈能力強 |
| 輕量部署 | Phi-4 | 14B 效能媲美 70B |
| 生態整合 | Llama-3.3 | 工具支援最完整 |
| 成本優先 | DeepSeek-V3 | API 成本僅 1/17 |

### 訓練方法選擇

| 情況 | 推薦方法 | 原因 |
|------|----------|------|
| 標準監督學習 | SFT | 最穩定基礎方法 |
| 資源有限 | LoRA (r=32) | 僅訓練 0.1% 參數 |
| 極低資源 | QLoRA | 4-bit 量化 + LoRA |
| 有偏好資料 | ORPO | 無需參考模型 |
| 強調對齊 | DPO | 需要 chosen/rejected 對 |

### LoRA 配置建議

| 資料量 | LoRA r | alpha | 說明 |
|--------|--------|-------|------|
| <500 | 16 | 32 | 保守配置，防過擬合 |
| 500-2000 | 32 | 64 | 建議配置 |
| 2000-5000 | 64 | 128 | 充足資料 |
| >5000 | 128+ | 256+ | 可考慮 full fine-tuning |

### 常見問題速查

| 症狀 | 可能原因 | 解決方案 |
|------|----------|----------|
| 整體 F1 低 | 資料不足/模型太小 | 增加資料、換大模型 |
| 某類別 F1 低 | 類別不平衡 | 過採樣、類別權重 |
| Train loss 低但 eval 高 | 過擬合 | 減少 epochs、增加 dropout |
| Loss 不下降 | 學習率問題 | 調整 learning rate |
| 輸出格式錯誤 | 訓練資料格式不一致 | 檢查 chat format |

## 詳細知識

### 模型架構

#### Dense 架構
- **代表模型**: Llama, Qwen (非-MoE), Phi
- **特點**: 標準 Transformer，所有參數都參與計算
- **優點**: 穩定、工具支援完整
- **缺點**: 計算成本高

#### MoE (Mixture of Experts)
- **代表模型**: DeepSeek-V3, Mixtral, Qwen-MoE
- **特點**: 稀疏激活，只有部分專家參與計算
- **優點**: 效率高，相同效能下成本更低
- **缺點**: 部署複雜，需要更多記憶體

#### MLA (Multi-head Latent Attention)
- **代表模型**: DeepSeek-V2/V3
- **特點**: 壓縮 KV cache，降低推理成本
- **優點**: 長序列效率高
- **應用**: 適合長文本任務

### 訓練方法詳解

#### SFT (Supervised Fine-Tuning)
```yaml
適用場景:
  - 標準分類、抽取任務
  - 有充足標註資料
  - 需要穩定可預測的結果

配置建議:
  epochs: 3-8
  learning_rate: 1e-5 ~ 5e-5
  batch_size: 4-16
  warmup_ratio: 0.1
```

#### LoRA (Low-Rank Adaptation)
```yaml
適用場景:
  - 資源有限（GPU 記憶體不足）
  - 需要快速迭代
  - 保留基礎模型能力

配置建議:
  r: 16-64 (根據資料量)
  alpha: 2 * r
  dropout: 0.05-0.1
  target_modules: [q_proj, v_proj, k_proj, o_proj]
```

#### QLoRA
```yaml
適用場景:
  - 極低資源環境
  - 消費級 GPU (RTX 3090, 4090)
  - 大模型微調

配置建議:
  quantization: 4-bit (nf4)
  lora_r: 32-64
  compute_dtype: bfloat16
```

#### DPO (Direct Preference Optimization)
```yaml
適用場景:
  - 有 chosen/rejected 配對資料
  - 需要對齊人類偏好
  - 生成任務品質優化

配置建議:
  beta: 0.1-0.5
  需要資料: chosen/rejected pairs
  通常在 SFT 後進行
```

#### ORPO (Odds Ratio Preference Optimization)
```yaml
適用場景:
  - 有偏好資料但不想用參考模型
  - 簡化訓練流程
  - 效率優先

配置建議:
  beta: 0.1
  lambda: 0.1
  無需參考模型
```

### 任務類型最佳實踐

#### 情感分析
```yaml
推薦配置:
  base_model: Qwen3-4B
  method: SFT + LoRA
  output: JSON (sentiment field)

注意事項:
  - 處理類別不平衡
  - 中立類別通常最難
  - 考慮 aspect-based 需求
```

#### 命名實體識別 (NER)
```yaml
推薦配置:
  base_model: Qwen3-8B
  method: SFT + LoRA
  output: JSON (entities array)

注意事項:
  - 實體邊界標註一致性
  - 考慮巢狀實體
  - 評估用 entity-level F1
```

#### 文本生成
```yaml
推薦配置:
  base_model: 依需求選擇
  method: SFT → ORPO/DPO
  output: 自然語言

注意事項:
  - 先 SFT 建立基礎能力
  - 再用對齊方法提升品質
  - 評估指標多元化
```

## 2025-2026 關鍵趨勢

1. **MoE 成為主流**: Top 10 開源模型均採用 MoE 架構
2. **DeepSeek 崛起**: R1 達 ChatGPT 水準，API 成本僅 1/17
3. **Qwen 超越 Llama**: HuggingFace 下載量和微調使用率第一
4. **SLM 實用化**: Phi-4、Gemma 3 在特定任務媲美大模型
5. **對齊方法多元化**: ORPO、KTO、SimPO、GRPO 湧現

## 相關資源

### 參考文件

詳細的技術文件和進階指南請參考：

- **`references/models/`** - 各模型系列詳細指南
- **`references/methods/`** - 訓練方法深入解析
- **`references/architectures/`** - 模型架構技術細節
- **`references/troubleshooting/`** - 問題排解完整指南
- **`references/tasks/`** - 各任務類型最佳實踐

### 查詢方式

需要更詳細資訊時，可以查詢 references 目錄：

```
「Qwen 模型詳細資訊」→ references/models/qwen.md
「LoRA 進階配置」→ references/methods/peft/lora.md
「過擬合解決方案」→ references/troubleshooting/overfitting.md
```

---

*知識截止: 2026-01*
