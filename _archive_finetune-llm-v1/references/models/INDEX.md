# 基礎模型索引

## 快速選擇

| 需求 | 推薦模型 | 理由 |
|------|----------|------|
| 中文任務 | Qwen3-4B/8B | 中文能力頂尖 |
| 推理任務 | DeepSeek-R1 | 專為推理設計 |
| 程式碼 | DeepSeek Coder V2 | 程式碼專精 |
| 邊緣部署 | Phi-4-Mini (3.8B) | 小巧高效 |
| 生態完整 | Llama 3.3 | 工具支援最好 |

## 模型比較表 (2025-2026)

| 模型 | 參數量 | 架構 | 中文 | 授權 | VRAM |
|------|--------|------|------|------|------|
| **Qwen3-4B** | 4B | Dense | ⭐⭐⭐ | Apache 2.0 | 8GB |
| **Qwen3-8B** | 8B | Dense | ⭐⭐⭐ | Apache 2.0 | 16GB |
| **Qwen3-30B** | 30B (3B active) | MoE | ⭐⭐⭐ | Apache 2.0 | 24GB |
| **DeepSeek-V3** | 671B (37B active) | MoE+MLA | ⭐⭐⭐ | MIT | 80GB+ |
| **DeepSeek-R1** | 671B (37B active) | MoE+MLA | ⭐⭐⭐ | MIT | 80GB+ |
| **Llama 3.3** | 70B | Dense | ⭐⭐ | Llama License | 48GB |
| **Phi-4-Mini** | 3.8B | Dense | ⭐⭐ | MIT | 4GB |
| **Phi-4** | 14B | Dense | ⭐⭐ | MIT | 16GB |
| **Mixtral 8x22B** | 141B (39B active) | MoE | ⭐ | Apache 2.0 | 80GB+ |

## 詳細指南

- [qwen.md](qwen.md) - Qwen 系列（推薦中文任務）
- [deepseek.md](deepseek.md) - DeepSeek 系列（推理、程式碼）
- [llama.md](llama.md) - Llama 系列（生態完整）
- [phi.md](phi.md) - Phi 系列（小模型）
- [mistral.md](mistral.md) - Mistral/Mixtral

## 本專案預設

**預設模型**: `Qwen/Qwen3-4B`

理由：
- 中文能力優秀
- 參數量適中（4B），訓練效率高
- 24GB GPU 可訓練 LoRA
- Apache 2.0 開源授權

---

*更新: 2026-01*
