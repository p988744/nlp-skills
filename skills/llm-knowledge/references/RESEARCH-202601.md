# LLM 領域研究摘要 (2025-01 ~ 2026-01)

本文件整理 2025-2026 年 LLM 領域的最新發展，作為 Reference 知識庫的基礎。

---

## 一、模型架構趨勢

### 1.1 Mixture of Experts (MoE) 成為主流

2025 年起，幾乎所有頂尖開源模型都採用 MoE 架構。

| 架構 | 特點 | 代表模型 |
|------|------|----------|
| **Dense** | 每次推理激活所有參數 | Llama 3.1, Qwen2 |
| **MoE** | 只激活部分專家網路，效率高 | DeepSeek-V3, Mixtral, Qwen3 |
| **MLA** | Multi-head Latent Attention，DeepSeek 創新 | DeepSeek-V2/V3 |

**MoE 優勢：**
- DeepSeek-V3: 671B 總參數，但每 token 只激活 37B
- 訓練成本：DeepSeek-V3 約 $5.6M，Llama 3.1 405B 約 11 倍 GPU 時數
- Artificial Analysis 排行榜 Top 10 開源模型均為 MoE 架構

### 1.2 小型語言模型 (SLM) 崛起

SLM (1B-12B) 在特定任務可媲美大型模型，適合邊緣部署：

| 模型 | 參數量 | 特點 |
|------|--------|------|
| **Phi-4-Mini** | 3.8B | 128K context，MATH 80.4%，函數調用 ≥97% |
| **Phi-4** | 14B | 超越 GPT-4 在 STEM QA，MMLU 84.8% |
| **Gemma-3n-E2B** | ~5B (2B 等效) | 多模態，選擇性參數激活 |
| **Gemma3-4B** | 4B | 多語言多模態 |
| **Ministral 8B** | 8B | 滑動窗口注意力 |

**SLM 適用場景：**
- 邊緣設備 / 本地部署
- 結構化輸出、工具調用
- 微調後在特定任務超越大模型

---

## 二、主流開源模型 (2025-2026)

### 2.1 模型比較表

| 模型 | 組織 | 參數量 | 架構 | 中文能力 | 授權 |
|------|------|--------|------|----------|------|
| **DeepSeek-V3.1** | DeepSeek | 671B (37B active) | MoE + MLA | 優秀 | MIT |
| **DeepSeek-R1** | DeepSeek | 671B (37B active) | MoE + MLA | 優秀 | MIT |
| **Qwen3-235B** | Alibaba | 235B (22B active) | MoE | 頂尖 | Apache 2.0 |
| **Qwen3-30B** | Alibaba | 30B (3B active) | MoE | 頂尖 | Apache 2.0 |
| **Qwen3-4B/8B** | Alibaba | 4B/8B | Dense | 優秀 | Apache 2.0 |
| **Llama 3.3** | Meta | 70B | Dense | 良好 | Llama License |
| **Kimi K2** | Moonshot | - | - | 優秀 | - |
| **Mixtral 8x22B** | Mistral | 141B (39B active) | MoE | 中等 | Apache 2.0 |

### 2.2 DeepSeek 系列詳情

**發展時間線：**
- 2025-01-20: DeepSeek-R1 發布（MIT License）
- 2025-03-24: DeepSeek-V3-0324
- 2025-05-28: DeepSeek-R1-0528（升級版）
- 2025-08-21: DeepSeek-V3.1（混合思考/非思考模式）

**DeepSeek-V3.1 特點：**
- SWE-bench Verified: 66.0%（R1: 44.6%）
- 混合架構：支持 thinking 和 non-thinking 模式
- 推理速度比 R1-0528 更快

**訓練創新：**
- FP8 混合精度訓練（首個大規模驗證）
- 輔助損失-free 負載均衡
- Multi-Token Prediction (MTP)
- 256 個路由專家/層（V2: 160）

### 2.3 Qwen 系列詳情

**Qwen3 特點：**
- HuggingFace 下載量最高、微調最多的基礎模型
- Dense 和 MoE 版本完整
- 4B 到 235B 參數範圍
- Apache 2.0 開源

**Qwen vs Llama：**
- Qwen 在多語言、長上下文方面領先
- Llama 生態系統更成熟（工具、教程）
- 中文任務建議優先選擇 Qwen

### 2.4 硬體需求參考

| GPU VRAM | 可運行模型 |
|----------|-----------|
| 24GB (RTX 3090/4090) | 4-bit 量化 ~40B 參數 |
| 48-80GB (Pro GPU) | 70B 模型（Llama 3.1, Qwen2 72B）|

---

## 三、訓練方法現狀

### 3.1 PEFT 方法比較

| 方法 | 說明 | 優點 | 適用場景 |
|------|------|------|----------|
| **LoRA** | 低秩分解，W' = W + AB^T | 可堆疊、便宜 | 通用微調 |
| **QLoRA** | 4-bit 量化 + LoRA | 70B 可在 24GB 訓練 | 資源受限 |
| **DoRA** | 權重分解為幅度+方向 | 對 rank 選擇更穩健 | 追求品質 |
| **AdaLoRA** | 自適應 rank 分配 | 自動化 | 不確定最佳 rank |

**最佳實踐：**
- QLoRA 7-8B 在 24GB GPU，序列長度 ~4K 可行
- 從 QLoRA 開始，品質要求高時用 DoRA
- 5-20K 高品質樣本可超越 200K 嘈雜樣本

### 3.2 對齊方法比較

| 方法 | 資料需求 | 需要參考模型 | 特點 |
|------|----------|-------------|------|
| **DPO** | chosen/rejected 對 | 是 | 穩定、基礎方法 |
| **ORPO** | chosen/rejected 對 | 否 | 更輕量、但可能漂移 |
| **KTO** | 不需要配對 | - | 適合嘈雜反饋 |
| **SimPO** | chosen/rejected 對 | 否 | 簡化版，效率高 |
| **GRPO** | 組內相對排序 | 否 | DeepSeek 使用，記憶體效率 |

**選擇建議：**
- 高品質 SFT 常常就夠了
- 需要偏好控制時考慮 DPO/ORPO
- ORPO 無需參考模型，訓練時間約 SFT 的 1.7-2 倍

### 3.3 常見問題

| 問題 | 解決方案 |
|------|----------|
| 災難性遺忘 | 混合通用資料、降低學習率、凍結更多模組 |
| Chat template 錯誤 | 務必使用與推理相同的 tokenizer template |
| DPO 過度正則化 | 減少 beta 或混入 SFT 步驟 |

---

## 四、訓練框架

| 框架 | 特點 | 適用場景 |
|------|------|----------|
| **Unsloth** | 2x+ 加速，記憶體優化 | 資源受限、追求速度 |
| **LLaMA-Factory** | GUI + CLI，支援多種方法 | 入門友好 |
| **Axolotl** | YAML 配置驅動，高度靈活 | 進階用戶 |

**LLaMA-Factory 支援：**
- 預訓練、指令微調、獎勵模型訓練
- PPO、DPO、ORPO
- Full、LoRA、QLoRA (2-8 bit)
- GaLore、BAdam、DoRA、LongLoRA

---

## 五、部署技術

### 5.1 推理框架

| 框架 | 特點 | 適用場景 |
|------|------|----------|
| **vLLM** | PagedAttention、連續批次、張量並行 | 高吞吐量生產環境 |
| **Ollama** | 簡單部署、本地使用 | 開發測試、邊緣部署 |
| **TGI** | HuggingFace 官方 | 雲端部署 |

### 5.2 量化格式

| 格式 | 用途 | 適用框架 |
|------|------|----------|
| **GGUF** | CPU/混合推理 | llama.cpp, Ollama |
| **AWQ** | 4-bit GPU 推理 | vLLM |
| **GPTQ** | 4-bit GPU 推理 | vLLM, Transformers |

**建議：**
- GPU 生產：vLLM + AWQ
- 本地/開發：Ollama + GGUF

---

## 六、中文資源

### 6.1 指令資料集

| 資料集 | 說明 |
|--------|------|
| BELLE | 中文指令微調 |
| Alpaca-Chinese | 中文 Alpaca 翻譯版 |
| Firefly | 中文多任務指令 |

### 6.2 評測基準

| 基準 | 任務 |
|------|------|
| CLUE | 中文語言理解評測 |
| C-Eval | 中文多學科評測 |
| CMMLU | 中文 MMLU |

### 6.3 情感分析資料集

| 資料集 | 說明 |
|--------|------|
| ChnSentiCorp | 中文情感分類 |
| Weibo Sentiment | 微博情感 |
| 電商評論 | 各平台評論資料 |

---

## 七、關鍵發現總結

### 7.1 模型選擇建議

| 場景 | 推薦 |
|------|------|
| 中文任務 | Qwen3-4B/8B（資源有限）、Qwen3-30B（追求效能）|
| 推理任務 | DeepSeek-R1、DeepSeek-V3.1 |
| 程式碼 | DeepSeek Coder V2、Qwen2.5-Coder |
| 本地部署 | Phi-4-Mini、Gemma-3n、Qwen3-4B |
| 生產環境 | Qwen3 MoE、DeepSeek-V3 |

### 7.2 訓練方法建議

| 場景 | 推薦 |
|------|------|
| 入門/快速驗證 | QLoRA + SFT |
| 追求品質 | DoRA + SFT |
| 需要偏好對齊 | ORPO（無需參考模型）或 DPO |
| 資源充足 | Full fine-tuning |

### 7.3 2025 年重大變化

1. **MoE 成為主流**：Top 10 開源模型均採用
2. **DeepSeek 崛起**：R1 達到 ChatGPT 水準，成本僅 1/17
3. **Qwen 超越 Llama**：下載量和微調使用率第一
4. **SLM 實用化**：Phi-4、Gemma 3 在特定任務媲美大模型
5. **對齊方法多元化**：ORPO、KTO、SimPO、GRPO 等新方法湧現

---

## 八、參考來源

### 模型資訊
- [HuggingFace Blog: Open-Source LLMs 2025](https://huggingface.co/blog/daya-shankar/open-source-llms)
- [BentoML: Best Open-Source LLMs 2026](https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models)
- [O-mega: Top 10 Open Source LLMs 2026](https://o-mega.ai/articles/top-10-open-source-llms-the-deepseek-revolution-2026)
- [Interconnects: 2025 Open Models Year in Review](https://www.interconnects.ai/p/2025-open-models-year-in-review)

### DeepSeek
- [CNBC: DeepSeek R1 升級](https://www.cnbc.com/2025/05/29/chinas-deepseek-releases-upgraded-r1-ai-model-in-openai-competition.html)
- [DeepSeek-R1 HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-R1)
- [Fireworks: DeepSeek Architecture](https://fireworks.ai/blog/deepseek-model-architecture)
- [DeepSeek-V3 Technical Report](https://vitalab.github.io/article/2025/02/11/DeepSeekV3.html)

### MoE 架構
- [NVIDIA Blog: MoE Frontier Models](https://blogs.nvidia.com/blog/mixture-of-experts-frontier-models/)
- [Cameron Wolfe: MoE LLMs](https://cameronrwolfe.substack.com/p/moe-llms)
- [Chipstrat: DeepSeek MoE and V2](https://www.chipstrat.com/p/deepseek-moe-and-v2)

### 訓練方法
- [Elysiate: LLM Fine-Tuning Guide 2025](https://www.elysiate.com/blog/llm-fine-tuning-complete-guide-lora-qlora-2025)
- [Unsloth Documentation](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide)
- [Towards AI: Complete LLM Fine-Tuning Guide](https://pub.towardsai.net/the-complete-llm-fine-tuning-guide-from-beginner-to-production-lora-qlora-peft-034dbef4148d)

### SLM
- [HuggingFace Blog: Small Language Models](https://huggingface.co/blog/jjokah/small-language-model)
- [DataCamp: Top 15 SLMs 2026](https://www.datacamp.com/blog/top-small-language-models)
- [BentoML: Best Open-Source SLMs 2026](https://www.bentoml.com/blog/the-best-open-source-small-language-models)

---

*整理日期: 2026-01-06*
*知識截止: 2026-01*
