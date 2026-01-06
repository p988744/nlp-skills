---
description: "啟動 LLM fine-tuning 工作流程。支援建立新任務 (create) 或改善既有任務 (iterate)。"
argument-hint: "[create|iterate] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task
---

# LLM Fine-tuning Command

使用者執行了 `/finetune-llm` 命令。請根據以下流程協助使用者。

## 流程

1. **讀取 Skill 文件**
   讀取 `skills/finetune-llm/SKILL.md` 了解完整工作流程。

2. **判斷模式**
   - 如果使用者指定了 `create` 或 `iterate`，直接進入對應模式
   - 如果沒有指定，檢查當前目錄是否有 `tasks/` 資料夾：
     - 有既有任務：詢問使用者要「建立新任務」還是「改善既有任務」
     - 沒有任務：直接進入 CREATE 模式

3. **執行對應模式**
   - **CREATE 模式**: 讀取 `skills/finetune-llm/CREATE-MODE.md`，引導使用者從頭建立新的 fine-tuning 專案
   - **ITERATE 模式**: 讀取 `skills/finetune-llm/ITERATE-MODE.md`，協助改善既有任務的效能

4. **使用知識庫**
   在過程中，根據需要參考 `skills/finetune-llm/references/` 中的知識文件：
   - 模型選擇：`references/models/INDEX.md`
   - 訓練方法：`references/methods/INDEX.md`
   - 問題排解：`references/troubleshooting/INDEX.md`

## 使用範例

```
/finetune-llm                    # 自動判斷模式
/finetune-llm create             # 建立新任務
/finetune-llm iterate sentiment  # 改善 sentiment 任務
```
