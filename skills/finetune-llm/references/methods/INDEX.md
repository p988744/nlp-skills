# 訓練方法索引

## 方法選擇決策樹

```
需要什麼？
│
├── 基礎微調（有明確答案）
│   └── SFT (Supervised Fine-Tuning)
│       └── 資源受限？
│           ├── 是 → QLoRA
│           └── 否 → LoRA 或 Full Fine-tuning
│
└── 偏好對齊（需要控制輸出風格）
    └── 有 chosen/rejected 配對資料？
        ├── 是 → 需要參考模型？
        │       ├── 可以 → DPO
        │       └── 不想要 → ORPO
        └── 否 → KTO（支援非配對資料）
```

## 方法快速比較

| 方法 | 資料需求 | 複雜度 | 適用場景 |
|------|----------|--------|----------|
| **SFT** | 輸入-輸出對 | 低 | 分類、基礎生成 |
| **ORPO** | chosen/rejected | 中 | 偏好對齊（無需參考模型）|
| **DPO** | chosen/rejected | 中 | 偏好對齊（更穩定）|
| **KTO** | 非配對偏好 | 中 | 嘈雜反饋 |

## PEFT 方法比較

| 方法 | 記憶體 | 效果 | 複雜度 | 推薦 |
|------|--------|------|--------|------|
| **LoRA** | 中 | 好 | 低 | ⭐ 通用 |
| **QLoRA** | 低 | 好 | 低 | ⭐ 資源受限 |
| **DoRA** | 中 | 更好 | 中 | 追求品質 |
| Full FT | 高 | 最好 | 低 | 資源充足 |

## 目錄結構

```
methods/
├── pretraining/              # 預訓練（較少使用）
│   ├── continual-pretraining.md
│   └── domain-adaptive.md
│
├── finetuning/               # 微調方法
│   ├── sft.md                # ⭐ 最常用
│   ├── full-finetuning.md
│   └── instruction-tuning.md
│
├── peft/                     # 參數高效微調
│   ├── lora.md               # ⭐ 推薦入門
│   ├── qlora.md              # ⭐ 資源受限首選
│   ├── dora.md               # 追求品質
│   └── adalora.md
│
└── alignment/                # 對齊方法
    ├── dpo.md                # ⭐ 穩定
    ├── orpo.md               # ⭐ 簡單（無需參考模型）
    ├── kto.md                # 非配對資料
    ├── simpo.md
    └── grpo.md               # DeepSeek 使用
```

## 推薦組合

### 入門/快速驗證

```yaml
method: sft
peft: qlora  # 或 lora
```

### 生產品質

```yaml
method: sft
peft: dora  # 或 lora r=64
```

### 需要偏好控制

```yaml
method: orpo  # 一步完成 SFT + 偏好對齊
peft: lora
```

## 詳細文件

- [finetuning/sft.md](finetuning/sft.md) - SFT 詳細指南
- [peft/lora.md](peft/lora.md) - LoRA 配置和技巧
- [peft/qlora.md](peft/qlora.md) - QLoRA 資源受限方案
- [alignment/orpo.md](alignment/orpo.md) - ORPO 偏好對齊
- [alignment/dpo.md](alignment/dpo.md) - DPO 偏好對齊

---

*更新: 2026-01*
