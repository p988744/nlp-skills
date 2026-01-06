# NLP Skills Marketplace - Claude Code 專案指引

## 專案概述

Claude Code skill marketplace，提供 NLP 相關工作流程。

- **Repository**: https://github.com/p988744/nlp-skills
- **當前版本**: 2.0.0

## 專案結構

```
nlp-skills/
├── .claude-plugin/
│   ├── plugin.json         # Plugin 配置（含版本號）
│   └── marketplace.json    # Marketplace 配置
├── skills/
│   └── finetune-llm/       # LLM Fine-tuning Skill
│       ├── SKILL.md        # Skill 入口
│       ├── CHANGELOG.md    # 版本歷史
│       ├── CHECKLIST.md    # 檢查清單
│       ├── CREATE-MODE.md  # 建立新任務流程
│       ├── ITERATE-MODE.md # 改善既有任務流程
│       ├── phases/         # 6 階段詳細文件
│       ├── references/     # 知識庫
│       ├── scripts/        # 專案生成腳本
│       └── templates/      # Jinja2 模板
├── README.md               # Marketplace 說明
└── CLAUDE.md               # 本文件
```

## 可用 Skills

| Skill | 說明 |
|-------|------|
| `finetune-llm` | LLM fine-tuning 完整工作流程 |

## 版本控制

### 版本號位置

更新版本時需修改以下檔案：

| 檔案 | 欄位 |
|------|------|
| `.claude-plugin/plugin.json` | `version` |
| `.claude-plugin/marketplace.json` | `metadata.version` |
| `.claude-plugin/marketplace.json` | `plugins[0].version` |
| `skills/finetune-llm/CHANGELOG.md` | 新增版本記錄 |

### 發布流程

```bash
# 1. 修改 skill 檔案

# 2. 更新 CHANGELOG.md
# 記錄 Added/Changed/Removed/Fixed

# 3. 更新版本號（plugin.json, marketplace.json）

# 4. Commit
git add -A
git commit -m "release: vX.Y.Z

- 變更摘要
"

# 5. 建立 tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# 6. 推送
git push origin main --tags
```

### 版本命名規則

遵循 Semantic Versioning：

- **MAJOR** (X.0.0): 架構重大變更、不相容更新
- **MINOR** (0.X.0): 新增功能、向後相容
- **PATCH** (0.0.X): Bug 修復、文件更新

## 開發指引

### 新增 Skill

1. 在 `skills/` 建立新目錄
2. 建立 `SKILL.md` 作為入口
3. 更新 `.claude-plugin/marketplace.json` 的 `plugins` 陣列
4. 更新 `README.md` 的可用 Skills 列表

### 新增 Reference（finetune-llm）

1. 在 `skills/finetune-llm/references/` 對應目錄新增 `.md` 檔案
2. 更新該目錄的 `INDEX.md`
3. 必要時更新 `references/INDEX.md`

### 新增 Template（finetune-llm）

1. 在 `skills/finetune-llm/templates/` 對應目錄新增 `.j2` 檔案
2. 更新 `templates/INDEX.md`
3. 更新 `scripts/init_project.py` 的渲染邏輯

## Git 分支策略

- `main`: 穩定版本，直接推送或 PR
- `feature/*`: 功能開發分支
- `fix/*`: Bug 修復分支

## 相關資源

- [Claude Code 文件](https://docs.anthropic.com/en/docs/claude-code)
- HuggingFace Models: 依 `task_definition.yaml` 中的 `huggingface.org` 設定
