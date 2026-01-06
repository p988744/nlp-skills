# LLM 微調檢查清單

完整的 LLM 微調工作流程檢查清單，確保每個步驟都正確執行。

---

## Phase 1: 定義目標

### 任務定義
- [ ] task_name 使用英文、無空格
- [ ] 任務類型明確 (classification/extraction/generation)
- [ ] 輸入格式定義完整
- [ ] 輸出格式定義完整
- [ ] 標籤/類別定義清楚

### 成功標準
- [ ] 主要指標選定 (macro_f1/accuracy/entity_f1)
- [ ] 閾值設定合理 (建議 >= 0.80)
- [ ] 次要指標列出

### 資源評估
- [ ] 預估資料量
- [ ] 確認 GPU 資源
- [ ] 選定基礎模型

**產出**: `task_definition.yaml`

---

## Phase 2: 生成專案

### 專案結構
- [ ] 執行 `init_project.py`
- [ ] 目錄結構完整
- [ ] README.md 生成
- [ ] 配置檔案生成

### 驗證
- [ ] `training_config.yaml` 參數正確
- [ ] `benchmark_config.yaml` 指標正確
- [ ] 腳本可執行

**產出**: 完整專案目錄

---

## Phase 3: 準備資料

### 資料收集
- [ ] 原始資料放入 `data/raw/`
- [ ] 資料格式為 JSONL
- [ ] 涵蓋所有類別/情境

### 資料驗證
- [ ] 執行 `01_validate_data.py`
- [ ] JSON 格式正確
- [ ] 必要欄位存在
- [ ] 標籤值合法
- [ ] 類別分佈檢查

### 類別平衡
- [ ] 各類別樣本數檢查
- [ ] 不平衡比例 < 3:1 (建議)
- [ ] 必要時進行過採樣/增強

### 格式轉換
- [ ] 執行 `02_convert_format.py`
- [ ] Chat format 正確
- [ ] System prompt 適當
- [ ] 訓練/驗證/測試分割

### 最終檢查
- [ ] `data/chat_format/train.jsonl` 存在
- [ ] `data/chat_format/valid.jsonl` 存在
- [ ] `data/test.jsonl` 存在
- [ ] 測試集與訓練集無重疊

**產出**: `data/chat_format/` 和 `data/test.jsonl`

---

## Phase 4: 訓練模型

### 訓練前
- [ ] GPU 可用 (`nvidia-smi`)
- [ ] 記憶體充足
- [ ] 配置檔案確認
- [ ] 虛擬環境啟動

### 訓練配置
- [ ] 基礎模型正確
- [ ] LoRA 參數合適
- [ ] 學習率合理 (1e-5 ~ 2e-5)
- [ ] Epoch 數適當 (5-10)
- [ ] Batch size 符合記憶體

### 訓練監控
- [ ] Loss 穩定下降
- [ ] Eval loss 沒有持續上升
- [ ] 無 CUDA OOM
- [ ] 無 NaN loss

### 訓練問題處理
- [ ] 過擬合 → 減少 epoch/增加 dropout
- [ ] 欠擬合 → 增加 epoch/提高學習率
- [ ] OOM → 減少 batch size/使用 QLoRA

**產出**: `models/adapter/`

---

## Phase 5: 評估效能

### 評估執行
- [ ] 執行 `04_evaluate.py`
- [ ] 使用獨立測試集
- [ ] 推理配置與訓練一致

### 效能檢查
- [ ] 主要指標達標
- [ ] 各類別 F1 檢查
- [ ] 混淆矩陣分析
- [ ] 錯誤樣本分析

### 評估報告
- [ ] 報告已生成
- [ ] 指標記錄完整
- [ ] 錯誤樣本記錄

### 未達標處理
- [ ] 分析錯誤模式
- [ ] 增加/改善訓練資料
- [ ] 調整超參數
- [ ] 重新訓練

**產出**: `benchmarks/results/evaluation_report.yaml`

---

## Phase 6: 部署上線

### 模型合併 (vLLM)
- [ ] 執行合併腳本
- [ ] 合併模型可載入
- [ ] 推理測試通過

### GGUF 轉換 (Ollama)
- [ ] 執行轉換腳本
- [ ] GGUF 檔案生成
- [ ] Modelfile 正確
- [ ] Ollama 測試通過

### HuggingFace 上傳
- [ ] HF 登入成功
- [ ] Adapter 上傳
- [ ] GGUF 上傳
- [ ] vLLM merged 上傳
- [ ] Model cards 更新

### 文件更新
- [ ] Integration guide 更新
- [ ] README 更新
- [ ] task_definition 標記完成

### 驗證部署
- [ ] Ollama 推理測試
- [ ] vLLM API 測試
- [ ] 效能符合預期

**產出**: HuggingFace 三個儲存庫

---

## 完成確認

### 最終檢查
- [ ] 所有階段完成
- [ ] 效能達到目標
- [ ] 文件完整
- [ ] 部署驗證通過

### 歸檔
- [ ] 專案目錄保存
- [ ] 迭代版本記錄
- [ ] 知識文件更新

---

## 快速參考

### 常見問題速查

| 問題 | 解決方案 |
|------|----------|
| 效能低 | 檢查資料格式、增加資料、調整超參數 |
| 某類別差 | 過採樣、增加該類資料 |
| 過擬合 | 減少 epoch、增加 dropout |
| OOM | 減少 batch、使用 QLoRA |
| 輸出格式錯 | 改善 prompt、後處理 |

### 推薦配置

| GPU | 模型 | 方法 | Batch |
|-----|------|------|-------|
| 24GB | 4B | LoRA | 4 |
| 24GB | 8B | QLoRA | 2 |
| 48GB | 8B | LoRA | 4 |
| 80GB | 14B | LoRA | 4 |

---

*更新: 2026-01*
