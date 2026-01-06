# 準確率過低 (Low Accuracy / Underfitting)

## 症狀

- 訓練和測試效能都低
- Loss 下降緩慢或停滯
- 模型輸出品質差、不穩定

## 診斷

### 快速診斷清單

1. **資料問題**
   - [ ] 資料格式正確？
   - [ ] 標籤品質高？
   - [ ] 資料量足夠？

2. **模型問題**
   - [ ] 模型載入正確？
   - [ ] Chat template 正確？
   - [ ] LoRA 配置合適？

3. **訓練問題**
   - [ ] 學習率合適？
   - [ ] Epoch 數足夠？
   - [ ] 沒有梯度消失/爆炸？

## 解決方案

### 1. 檢查資料格式

最常見的問題！

```python
# 驗證 chat template
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")

messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "測試"},
    {"role": "assistant", "content": "回應"}
]

# 確認格式正確
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=False
)
print(prompt)
```

### 2. Qwen3 Thinking Mode 問題

**症狀**: 輸出包含 `<think>` 標籤
**解決**:

```python
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False  # 關閉思考模式！
)
```

### 3. 增加訓練 Epoch

```yaml
training:
  num_train_epochs: 10  # 從 5 增加到 10
```

觀察 loss 曲線：
- 還在下降 → 繼續訓練
- 停滯 → 其他問題

### 4. 提高學習率

```yaml
training:
  learning_rate: 2e-5  # 從 1e-5 提高
```

### 5. 增加 LoRA Rank

```yaml
lora:
  r: 64  # 從 32 增加到 64
  lora_alpha: 128
```

### 6. 擴大訓練目標

```yaml
lora:
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj
    - embed_tokens  # 加入 embedding
    - lm_head       # 加入 output head
```

### 7. 降低 Dropout

```yaml
lora:
  lora_dropout: 0.0  # 從 0.05 降到 0
```

### 8. 增加資料量

```
效能 vs 資料量經驗：
300 樣本 → 基本可用 (~70%)
500 樣本 → 較好效果 (~80%)
1000 樣本 → 穩定效能 (~85%)
2000+ 樣本 → 高效能 (~90%+)
```

### 9. 改善資料品質

> 5-20K 高品質樣本可超越 200K 嘈雜樣本

**品質檢查點**:
- 標籤是否一致？
- 有無矛盾樣本？
- 覆蓋所有情況？

### 10. 改善 Prompt

```python
# 差的 prompt
{"role": "user", "content": "分類：這個產品很好"}

# 好的 prompt
{"role": "system", "content": "你是情感分析專家..."},
{"role": "user", "content": """請分析以下文本的情感傾向。

文本：這個產品很好

請只回答：正面、負面 或 中立"""}
```

### 11. 檢查基礎模型能力

先測試基礎模型（無微調）的 zero-shot 能力：

```python
# 如果基礎模型 zero-shot 就很差，考慮：
# 1. 換更大/更強的模型
# 2. 增加更多範例 (few-shot in prompt)
# 3. 簡化任務定義
```

## 配置範本

### 追求準確率配置

```yaml
model:
  base_model: "Qwen/Qwen3-4B"

lora:
  r: 64  # 較大的 rank
  lora_alpha: 128
  lora_dropout: 0.0
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj

training:
  num_train_epochs: 10
  learning_rate: 2e-5  # 較高學習率
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  warmup_ratio: 0.1
  max_seq_length: 2048
  evaluation_strategy: "epoch"
  save_strategy: "epoch"
  load_best_model_at_end: true
```

## 特定問題排查

### 某類別效能特別差

見 [class-imbalance.md](class-imbalance.md)

### 長文本效能差

```yaml
training:
  max_seq_length: 4096  # 增加序列長度

model:
  # 或使用支援更長上下文的模型
  base_model: "Qwen/Qwen3-8B"  # 8B 支援更長
```

### JSON 輸出格式錯誤

```python
# 在 prompt 中加入格式範例
system_prompt = """
輸出必須是有效的 JSON 格式：
{"result": "值"}

不要加入任何其他文字。
"""

# 後處理
import json

def parse_output(text):
    try:
        # 嘗試提取 JSON
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass
    return None
```

## 效能提升路線圖

```
1. 確認資料格式正確 (最重要！)
   ↓
2. 檢查 chat template 和 thinking mode
   ↓
3. 增加訓練 epoch (觀察 loss)
   ↓
4. 調整學習率和 LoRA rank
   ↓
5. 增加/改善訓練資料
   ↓
6. 考慮更大的模型
```

## 相關

- [overfitting.md](overfitting.md) - 過擬合問題
- [class-imbalance.md](class-imbalance.md) - 類別不平衡
- [sft.md](../methods/finetuning/sft.md) - SFT 配置
- [qwen.md](../models/qwen.md) - Qwen 特殊注意事項

---

*更新: 2026-01*
