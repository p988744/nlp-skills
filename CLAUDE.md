# NLP Skills Marketplace - Claude Code Project Guide

## Project Overview

Claude Code plugin for NLP tasks - LLM fine-tuning coaching-style workflow.

- **Version**: 0.3.0
- **GitHub**: https://github.com/p988744/nlp-skills
- **GitLab**: https://gitting.eland.com.tw/rd2/claude-skills/nlp-skills

## Git Remotes

```bash
origin  https://github.com/p988744/nlp-skills.git
gitlab  https://gitting.eland.com.tw/rd2/claude-skills/nlp-skills.git
```

Push to both:
```bash
git push origin main --tags && git push gitlab main --tags
```

## Project Structure

```
nlp-skills/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest (version here)
│   └── marketplace.json     # Marketplace config (version here)
├── commands/                # 7 slash commands
│   ├── coach.md
│   ├── tasks.md
│   ├── new-task.md
│   ├── data-source.md
│   ├── generate.md
│   ├── evaluate.md
│   └── deploy.md
├── agents/                  # 4 intelligent agents
│   ├── goal-clarifier.md
│   ├── data-source-advisor.md
│   ├── problem-diagnoser.md
│   └── result-analyzer.md
├── skills/                  # 5 specialized skills
│   ├── llm-coach/
│   ├── llm-knowledge/
│   ├── task-manager/
│   ├── data-pipeline/
│   └── finetune-llm/
├── hooks/
│   └── hooks.json           # 4 event hooks
├── README.md
├── CONTRIBUTING.md
└── CLAUDE.md
```

## Components

### Commands (7)
| Command | Description |
|---------|-------------|
| `/nlp-skills:coach` | Start coaching dialogue |
| `/nlp-skills:tasks` | List all tasks |
| `/nlp-skills:new-task` | Create new task |
| `/nlp-skills:data-source` | Configure data sources |
| `/nlp-skills:generate` | Generate project structure |
| `/nlp-skills:evaluate` | Run evaluation |
| `/nlp-skills:deploy` | Deploy model |

### Agents (4)
| Agent | Trigger |
|-------|---------|
| `goal-clarifier` | Vague training requests |
| `data-source-advisor` | Data source questions |
| `problem-diagnoser` | Performance issues |
| `result-analyzer` | Post-training analysis |

### Skills (5)
| Skill | Purpose |
|-------|---------|
| `llm-coach` | Coaching guidance entry point |
| `llm-knowledge` | Knowledge base |
| `task-manager` | Multi-task management |
| `data-pipeline` | Data source configuration |
| `finetune-llm` | Overview skill |

## Version Control

### Version Locations

Update these files when releasing:

| File | Field |
|------|-------|
| `.claude-plugin/plugin.json` | `version` |
| `.claude-plugin/marketplace.json` | `plugins[0].version` |
| `skills/finetune-llm/CHANGELOG.md` | Add version entry |

### Release Process

```bash
# 1. Update version in plugin.json, marketplace.json

# 2. Update CHANGELOG.md

# 3. Commit
git add -A
git commit -m "release: vX.Y.Z - Description"

# 4. Create tag (English release notes)
git tag -a vX.Y.Z -m "Release vX.Y.Z

## New Features
- Feature 1
- Feature 2
"

# 5. Push to both remotes
git push origin main --tags
git push gitlab main --tags
```

### Version Naming

Semantic Versioning (currently 0.x.x - early development):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features
- **PATCH** (0.0.X): Bug fixes

## Development

### Local Testing

```bash
# Test plugin locally
claude --plugin-dir .

# Debug mode
claude --debug --plugin-dir .

# Validate structure
claude plugin validate .
```

### Adding Components

**Command**: Create `commands/name.md` with frontmatter (description, allowed-tools, model)

**Agent**: Create `agents/name.md` with frontmatter (name, description, tools, model)

**Skill**: Create `skills/name/SKILL.md` with frontmatter (name, description, allowed-tools)

**Hook**: Edit `hooks/hooks.json`

After adding, update `plugin.json` arrays for commands/agents.

### plugin.json Format

Commands and agents must use explicit file paths:
```json
{
  "commands": ["./commands/file1.md", "./commands/file2.md"],
  "agents": ["./agents/file1.md", "./agents/file2.md"],
  "skills": "./skills",
  "hooks": "./hooks/hooks.json"
}
```

## Resources

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guide
