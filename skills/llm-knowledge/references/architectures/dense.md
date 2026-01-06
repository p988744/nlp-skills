# Dense 模型架構

## 概述

Dense 模型是標準的 Transformer 架構，每次推理時激活所有參數。這是最成熟、生態最完整的架構。

## 架構特點

```
輸入 → Embedding → [Transformer Block × N] → Output
                         │
                    ┌────┴────┐
                    │ Attention │ ← 所有參數都參與計算
                    │   FFN    │
                    └─────────┘
```

**每次推理激活**: 100% 參數

## 代表模型

| 模型 | 參數量 | 特點 |
|------|--------|------|
| **Qwen3-4B** | 4B | 中文頂尖，本專案預設 |
| **Qwen3-8B** | 8B | 更強能力 |
| **Llama 3.3** | 70B | 生態最完整 |
| **Phi-4** | 14B | 小模型高效能 |
| **Gemma 2** | 2B-27B | Google 出品 |

## 優點

✅ **訓練穩定**: 收斂快、調參簡單
✅ **工具支援**: 幾乎所有框架都支援
✅ **部署簡單**: 不需要特殊處理
✅ **記憶體可預測**: 固定的 VRAM 需求

## 缺點

❌ **推理成本高**: 所有參數都參與計算
❌ **擴展受限**: 參數量增加時成本線性增長
❌ **大模型困難**: 70B+ 需要多 GPU

## VRAM 需求

### 推理

| 模型大小 | FP16 | INT8 | INT4 |
|----------|------|------|------|
| 4B | 8GB | 4GB | 2GB |
| 7-8B | 16GB | 8GB | 4GB |
| 14B | 28GB | 14GB | 7GB |
| 70B | 140GB | 70GB | 35GB |

### 訓練 (LoRA)

| 模型大小 | LoRA r=32 | QLoRA |
|----------|-----------|-------|
| 4B | 16GB | 8GB |
| 7-8B | 24GB | 12GB |
| 14B | 48GB | 24GB |

## 訓練配置

### Qwen3-4B 標準配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"
  trust_remote_code: true

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
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 1e-5
```

## 適用場景

| 場景 | 是否適合 | 說明 |
|------|----------|------|
| 分類任務 | ✅ | 最佳選擇 |
| NER/IE | ✅ | 穩定可靠 |
| 簡單生成 | ✅ | 效果好 |
| 複雜推理 | ⚠️ | 考慮更大模型或 MoE |
| 即時對話 | ⚠️ | 視模型大小 |

## 與 MoE 比較

| 特性 | Dense | MoE |
|------|-------|-----|
| 訓練難度 | 低 | 高 |
| 推理成本 | 高 | 低 |
| 工具支援 | 完整 | 部分 |
| 效能/參數比 | 低 | 高 |

## 相關

- [moe.md](moe.md) - 需要更高效能時的替代方案
- [models/qwen.md](../models/qwen.md) - Qwen 系列詳細指南

---

*更新: 2026-01*
