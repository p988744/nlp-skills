---
description: 啟動教練式對話，引導釐清 LLM 訓練目標和痛點
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Task
model: sonnet
---

以教練角色開始引導使用者完成 LLM fine-tuning 規劃。

## 引導流程

### 第一步：理解背景

使用 AskUserQuestion 工具詢問：

1. **業務問題**
   - 這個模型要解決什麼業務問題？
   - 目前用什麼方法處理？效果如何？

2. **任務類型**
   - 是分類、資訊抽取、還是生成任務？
   - 輸入是什麼？期望輸出是什麼格式？

3. **資源現況**
   - 有多少已標註的資料？
   - 資料從哪裡來？能持續取得嗎？
   - 有 GPU 可用嗎？

### 第二步：釐清目標

根據回答，整理成結構化目標：

```yaml
task_summary:
  name: {任務名稱}
  type: {分類/抽取/生成}
  domain: {領域}

  goal: |
    {具體目標描述}

  constraints:
    - 資料量: {數量}
    - GPU: {可用資源}
    - 時程: {預期時間}

  success_criteria:
    primary_metric: {主要指標}
    threshold: {目標值}
```

### 第三步：推薦方案

根據目標和限制，推薦訓練方案：

**決策依據**：
- 資料量 < 500：建議 LoRA r=16-32
- 資料量 500-2000：建議 LoRA r=32-64
- 資料量 > 2000：可考慮 full fine-tuning

**模型選擇**：
- 中文任務 → Qwen3
- 推理任務 → DeepSeek-R1
- 輕量部署 → Phi-4

### 第四步：確認執行

整理完整的 task.yaml 配置，請使用者確認後繼續。

## 注意事項

- 每個問題都要等使用者回答後再繼續
- 不要假設使用者的需求，多問確認
- 提供具體的推薦理由，不只是結論
- 如果使用者不確定，提供選項和建議
