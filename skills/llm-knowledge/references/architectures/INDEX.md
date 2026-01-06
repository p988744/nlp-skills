# 模型架構索引

## 快速選擇

| 需求 | 推薦架構 | 理由 |
|------|----------|------|
| 通用任務、穩定性 | Dense | 生態完整、工具支援好 |
| 超大模型、控制成本 | MoE | 稀疏激活、推理成本低 |
| 長序列處理 | SSM/Mamba | 線性複雜度 |

## 架構比較表

| 架構 | 代表模型 | 參數效率 | 推理速度 | 訓練難度 | 生態 |
|------|----------|----------|----------|----------|------|
| **Dense** | Llama, Qwen (4B/8B) | 中 | 中 | 低 | ⭐⭐⭐ |
| **MoE** | DeepSeek-V3, Mixtral, Qwen3 MoE | 高 | 快 | 高 | ⭐⭐ |
| **MLA** | DeepSeek-V2/V3 | 高 | 快 | 高 | ⭐ |
| **SSM** | Mamba, RWKV | 高 | 很快 | 高 | ⭐ |

## 2025-2026 趨勢

> **MoE 成為主流**: Artificial Analysis 排行榜 Top 10 開源模型均採用 MoE 架構

## 詳細文件

- [dense.md](dense.md) - 標準 Transformer (Dense)
- [moe.md](moe.md) - Mixture of Experts
- [mla.md](mla.md) - Multi-head Latent Attention (DeepSeek)

## 本專案建議

**預設使用 Dense 模型 (Qwen3-4B)**

理由：
- 訓練穩定、工具支援完整
- 4B 參數在 24GB GPU 可訓練
- 對於大多數任務效能足夠

MoE 模型適用於：
- 需要更強推理能力
- 有足夠 GPU 資源
- 推理吞吐量要求高

---

*更新: 2026-01*
