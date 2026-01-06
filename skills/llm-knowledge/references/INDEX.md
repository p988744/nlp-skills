# Reference 知識庫索引

內建 LLM 領域知識（2025-2026），減少上網搜尋時間。

## 快速查找

### 我想了解...

| 需求 | 前往 |
|------|------|
| 該選哪個模型？ | [models/INDEX.md](models/INDEX.md) |
| Dense vs MoE 差異？ | [architectures/INDEX.md](architectures/INDEX.md) |
| SFT 還是 ORPO？ | [methods/INDEX.md](methods/INDEX.md) |
| LoRA 怎麼配置？ | [methods/peft/lora.md](methods/peft/lora.md) |
| 情感分析最佳實踐？ | [tasks/classification/sentiment-analysis.md](tasks/classification/sentiment-analysis.md) |
| 準確率太低怎麼辦？ | [troubleshooting/low-accuracy.md](troubleshooting/low-accuracy.md) |

---

## 知識庫結構

### [architectures/](architectures/INDEX.md) 模型架構

了解不同模型架構的特點和選擇。

| 架構 | 代表模型 | 特點 |
|------|----------|------|
| [Dense](architectures/dense.md) | Llama, Qwen (Dense) | 標準 Transformer，穩定 |
| [MoE](architectures/moe.md) | DeepSeek-V3, Mixtral | 稀疏激活，效率高 |
| [MLA](architectures/mla.md) | DeepSeek-V2/V3 | Multi-head Latent Attention |

### [models/](models/INDEX.md) 基礎模型

各模型系列的詳細指南。

| 模型 | 中文能力 | 推薦場景 |
|------|----------|----------|
| [Qwen](models/qwen.md) | ⭐⭐⭐ | 中文任務首選 |
| [DeepSeek](models/deepseek.md) | ⭐⭐⭐ | 推理、程式碼 |
| [Llama](models/llama.md) | ⭐⭐ | 生態完整 |
| [Phi](models/phi.md) | ⭐⭐ | 小模型、邊緣部署 |

### [methods/](methods/INDEX.md) 訓練方法

訓練方法選擇和配置指南。

```
methods/
├── finetuning/           # 微調
│   └── sft.md            # Supervised Fine-Tuning ⭐
├── peft/                 # 參數高效微調
│   └── lora.md           # LoRA ⭐
└── alignment/            # 對齊方法
    ├── dpo.md            # Direct Preference Optimization ⭐
    └── orpo.md           # ORPO（無需參考模型）⭐
```

### [tasks/](tasks/INDEX.md) NLP 任務類型

各類 NLP 任務的最佳實踐。

```
tasks/
├── classification/       # 分類任務
│   └── sentiment-analysis.md    # 情感分析 ⭐
└── extraction/           # 抽取任務
    └── ner.md            # NER ⭐
```

### [troubleshooting/](troubleshooting/INDEX.md) 問題排解

常見問題和解決方案。

| 問題 | 文件 |
|------|------|
| 過擬合 | [overfitting.md](troubleshooting/overfitting.md) |
| 欠擬合 | [underfitting.md](troubleshooting/underfitting.md) |
| 類別不平衡 | [class-imbalance.md](troubleshooting/class-imbalance.md) |
| 準確率低 | [low-accuracy.md](troubleshooting/low-accuracy.md) |
| OOM | [oom.md](troubleshooting/oom.md) |

---

## 2025-2026 關鍵趨勢

詳見 [RESEARCH-202601.md](../../RESEARCH-202601.md)

1. **MoE 成為主流**: Top 10 開源模型均採用 MoE
2. **DeepSeek 崛起**: R1 達 ChatGPT 水準，成本僅 1/17
3. **Qwen 超越 Llama**: 下載量和微調使用率第一
4. **SLM 實用化**: Phi-4、Gemma 3 在特定任務媲美大模型
5. **對齊方法多元化**: ORPO、KTO、SimPO、GRPO 湧現

---

*知識截止: 2026-01*
