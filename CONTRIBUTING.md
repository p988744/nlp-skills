# Contributing to NLP Skills

Thank you for your interest in contributing to NLP Skills!

## Getting Started

### Prerequisites

- Claude Code (latest version)
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/p988744/nlp-skills.git
cd nlp-skills

# Test locally with Claude Code
claude --plugin-dir .

# Debug mode for troubleshooting
claude --debug --plugin-dir .
```

## How to Contribute

### Reporting Issues

1. Search existing issues first
2. Use [GitHub Issues](https://github.com/p988744/nlp-skills/issues) to report
3. Provide clear reproduction steps
4. Include Claude Code version and OS

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test locally: `claude --plugin-dir .`
5. Commit: `git commit -m "feat: add your feature"`
6. Push: `git push origin feature/your-feature`
7. Open a Pull Request

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

## Plugin Structure

```
nlp-skills/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest (required)
│   └── marketplace.json     # Marketplace config
├── commands/                # Slash commands (.md files)
│   └── command-name.md
├── agents/                  # Subagents (.md files)
│   └── agent-name.md
├── skills/                  # Skills (directories with SKILL.md)
│   └── skill-name/
│       ├── SKILL.md         # Required
│       └── references/      # Optional
├── hooks/
│   └── hooks.json           # Event handlers
└── README.md
```

## Adding Components

### Adding a Command

Create `commands/your-command.md`:

```markdown
---
description: What this command does
argument-hint: [optional-args]
allowed-tools: Read, Write, Edit, Bash
model: sonnet
---

Command instructions for Claude...
```

### Adding an Agent

Create `agents/your-agent.md`:

```markdown
---
name: your-agent-name
description: |
  When to use this agent. Include trigger examples:

  <example>
  user: "example trigger phrase"
  assistant: "[Uses Task tool to launch your-agent-name]"
  </example>

model: inherit
tools: Read, Write, Grep, Glob
---

Agent system prompt and instructions...
```

### Adding a Skill

Create `skills/your-skill/SKILL.md`:

```markdown
---
name: your-skill-name
description: |
  This skill should be used when the user asks to "trigger phrase 1",
  "trigger phrase 2", or needs help with specific task.
allowed-tools: Read, Write, Grep, Glob
---

# Your Skill Name

Skill instructions and knowledge...
```

### Adding a Hook

Edit `hooks/hooks.json`:

```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "matcher": {
        "toolName": "Write",
        "pathPattern": "**/*.yaml"
      },
      "type": "prompt",
      "prompt": "Validation prompt for Claude..."
    }
  ]
}
```

## Updating plugin.json

After adding components, update `.claude-plugin/plugin.json`:

```json
{
  "commands": [
    "./commands/existing.md",
    "./commands/your-command.md"
  ],
  "agents": [
    "./agents/existing.md",
    "./agents/your-agent.md"
  ]
}
```

Note: Skills are auto-discovered from `./skills` directory.

## Testing

### Validate Plugin Structure

```bash
claude plugin validate .
```

### Test Commands

```bash
claude --plugin-dir .
# Then run: /nlp-skills:your-command
```

### Test Agents

```bash
claude --plugin-dir .
# Then run: /agents to see available agents
# Or trigger with natural language that matches agent description
```

### Test Skills

Skills are triggered automatically based on their description. Test by:
1. Start Claude Code with the plugin
2. Ask questions that match the skill's trigger phrases
3. Verify the skill activates and provides correct guidance

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

Current version: 0.x.x (early development)

## Code Style

- Markdown: CommonMark format
- JSON: 2-space indentation
- YAML: 2-space indentation
- Python: PEP 8

## Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md for all changes
- Use English for code comments and documentation

## License

Contributions are licensed under MIT License.

## Questions?

- GitHub Issues: https://github.com/p988744/nlp-skills/issues
- Author: Weifan Liao (weifanliao@eland.com.tw)
