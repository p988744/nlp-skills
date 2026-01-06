# Contributing to NLP Skills

感謝你有興趣貢獻 NLP Skills！

## 如何貢獻

### 回報問題

1. 先搜尋是否已有相同 issue
2. 使用 [GitHub Issues](https://github.com/p988744/nlp-skills/issues) 回報
3. 提供清楚的重現步驟

### 提交 Pull Request

1. Fork 這個 repository
2. 建立 feature branch: `git checkout -b feature/your-feature`
3. Commit 你的改動: `git commit -m "feat: add your feature"`
4. Push 到 branch: `git push origin feature/your-feature`
5. 開啟 Pull Request

### Commit 訊息格式

使用 [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]
```

Types:
- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文件更新
- `refactor`: 程式碼重構
- `test`: 測試相關
- `chore`: 其他雜項

## 新增 Skill

### 目錄結構

```
skills/
└── your-skill-name/
    ├── .claude-plugin/
    │   └── plugin.json      # Skill 配置
    ├── SKILL.md             # Skill 入口（必要）
    ├── CHANGELOG.md         # 版本歷史
    ├── phases/              # 階段文件（可選）
    ├── references/          # 知識庫（可選）
    └── templates/           # 模板（可選）
```

### SKILL.md 格式

```markdown
---
name: your-skill-name
description: |
  Skill 描述...
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Your Skill Name

Skill 內容...
```

### 更新 Marketplace

新增 skill 後，更新 `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    // 現有 plugins...
    {
      "name": "your-skill-name",
      "source": "./skills/your-skill-name",
      "description": "...",
      "version": "1.0.0",
      "category": "your-category",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

## 版本號規則

遵循 [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): 不相容的 API 變更
- **MINOR** (0.X.0): 向後相容的新功能
- **PATCH** (0.0.X): 向後相容的 Bug 修復

## 程式碼風格

- Markdown: 使用 CommonMark
- JSON: 2 spaces 縮排
- Python: 遵循 PEP 8

## 授權

貢獻的程式碼將採用 MIT License。
