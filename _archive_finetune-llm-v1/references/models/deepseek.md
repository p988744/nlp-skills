# DeepSeek 系列模型

## 概述

DeepSeek 是中國 AI 公司開發的開源大型語言模型系列，以創新的 MoE 架構和超高訓練效率著稱。2025 年發布的 R1 模型達到 GPT-4 水準，訓練成本僅為同級模型的 1/11。

**亮點**: MIT License 開源、創新架構、極致效率

## 模型版本

| 模型 | 發布日期 | 總參數 | 激活參數 | 特點 |
|------|----------|--------|----------|------|
| **DeepSeek-V3.1** | 2025-08 | 671B | 37B | 混合思考/非思考模式 |
| **DeepSeek-R1** | 2025-01 | 671B | 37B | 推理專精，達 GPT-4 水準 |
| **DeepSeek-R1-0528** | 2025-05 | 671B | 37B | R1 升級版 |
| **DeepSeek-V3-0324** | 2025-03 | 671B | 37B | V3 中期版本 |
| **DeepSeek-V2** | 2024 | 236B | 21B | MLA 首次應用 |
| **DeepSeek Coder V2** | 2024 | 236B | 21B | 程式碼專精 |

## 架構創新

### 1. MoE + MLA

```
輸入 → MLA (低秩 KV) → 細粒度 MoE (256專家) → 輸出
            │                    │
       減少 KV Cache         每 token 只用 8 專家
```

### 2. 細粒度專家 (Fine-grained Experts)

傳統 MoE: N 個專家，每個 FFN 維度 d
DeepSeek: mN 個專家，每個 FFN 維度 d/m

→ 更專精的知識分解

### 3. 共享專家 (Shared Experts)

- 部分專家始終被激活（學習通用知識）
- 其他專家更專注於特定領域

### 4. MLA (Multi-head Latent Attention)

```python
# 傳統 MHA
Q, K, V = separate_projections(x)  # 每個都是 d_model

# MLA
Q = q_projection(x)
KV_compressed = kv_compression(x)  # 低秩壓縮
K, V = decompress(KV_compressed)
```

→ KV Cache 減少 70%+，長序列更高效

## VRAM 需求

| 模型 | 推理 (FP16) | 推理 (INT4) | 說明 |
|------|-------------|-------------|------|
| DeepSeek-V3/R1 | 400GB+ | 100GB+ | 需多卡 |
| DeepSeek-V2 | 150GB+ | 40GB+ | 需多卡 |
| DeepSeek Coder V2 | 150GB+ | 40GB+ | 需多卡 |

**注意**: MoE 模型需載入所有專家權重，即使每次只用部分

## 蒸餾版本

DeepSeek 提供蒸餾到 Dense 模型的版本，更適合資源受限場景：

| 模型 | 參數量 | 基於 | 適用場景 |
|------|--------|------|----------|
| DeepSeek-R1-Distill-Qwen-32B | 32B | Qwen2.5-32B | 高效能推理 |
| DeepSeek-R1-Distill-Qwen-14B | 14B | Qwen2.5-14B | 平衡效能與資源 |
| DeepSeek-R1-Distill-Qwen-7B | 7B | Qwen2.5-7B | 資源受限 |
| DeepSeek-R1-Distill-Qwen-1.5B | 1.5B | Qwen2.5-1.5B | 邊緣部署 |
| DeepSeek-R1-Distill-Llama-70B | 70B | Llama 3.3 | 最高效能 |
| DeepSeek-R1-Distill-Llama-8B | 8B | Llama 3.1 | 通用部署 |

## 微調建議

### 適合微調的版本

1. **蒸餾版本** (推薦): Dense 架構，工具支援完整
2. **DeepSeek Coder V2**: 程式碼任務

### 不建議直接微調

- DeepSeek-V3/R1 原版: 太大、MoE 微調複雜
- 建議使用蒸餾版本或其他 Dense 模型

### 蒸餾版 LoRA 配置

```yaml
# DeepSeek-R1-Distill-Qwen-7B
model:
  base_model: "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
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
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
  learning_rate: 5e-6  # 較低，蒸餾模型已經很好
```

## 效能基準

### DeepSeek-R1

| 基準 | 分數 | 對比 |
|------|------|------|
| MATH-500 | 97.3% | 超越 GPT-4 |
| AIME 2024 | 79.8% | 接近 OpenAI o1 |
| Codeforces | 2029 Elo | 頂尖水準 |
| MMLU | 90.8% | 頂尖水準 |

### DeepSeek-V3.1

| 基準 | 分數 | 說明 |
|------|------|------|
| SWE-bench Verified | 66.0% | R1: 44.6% |
| 推理速度 | 更快 | 比 R1 快 |

## 訓練成本對比

| 模型 | GPU 時數 | 估計成本 |
|------|----------|----------|
| DeepSeek-V3 | 2.8M H800 | ~$5.6M |
| Llama 3.1 405B | 30.8M | ~$60M+ |

→ DeepSeek 效率約 **11 倍**

## 適用場景

| 場景 | 推薦版本 | 說明 |
|------|----------|------|
| 複雜推理 | R1 或蒸餾版 | R1 專為推理設計 |
| 程式碼生成 | Coder V2 | 程式碼專精 |
| 數學問題 | R1 | MATH-500 97.3% |
| 通用任務 | V3.1 或蒸餾版 | 平衡效能 |
| 微調任務 | 蒸餾版 (7B/14B) | Dense 架構易微調 |
| 邊緣部署 | 蒸餾版 1.5B | 最小資源需求 |

## 使用注意事項

### 1. 思考模式

DeepSeek-R1 和 V3.1 支持思考模式：

```python
# 啟用思考 (推理任務)
response = model.generate(
    prompt,
    enable_thinking=True,
    max_thinking_tokens=8192
)

# 禁用思考 (快速回應)
response = model.generate(
    prompt,
    enable_thinking=False
)
```

### 2. API 使用

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",  # 或 deepseek-reasoner
    messages=[{"role": "user", "content": "..."}]
)
```

## 相關

- [moe.md](../architectures/moe.md) - MoE 架構詳解
- [qwen.md](qwen.md) - Qwen 蒸餾基礎
- [llama.md](llama.md) - Llama 蒸餾基礎

---

*更新: 2026-01*
