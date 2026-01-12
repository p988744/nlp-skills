# NLP Skills Marketplace

Claude Code plugin for NLP tasks - LLM fine-tuning with coaching-style guidance workflow.

## v0.3 Highlights

- **Coaching-style Guidance**: Explore pain points, clarify goals, recommend optimal solutions
- **Multi-task Management**: Version tracking and comparison for multiple training tasks
- **Data Source Tracking**: Reproducible data pipelines (DB, API, web scraping, LLM generation)
- **Intelligent Agents**: Auto-diagnose issues, analyze results, recommend improvements

## Installation

### Method 1: Via Marketplace (Recommended)

```bash
# Add nlp-skills marketplace
/plugin marketplace add p988744/nlp-skills

# Install
/plugin install nlp-skills
```

### Method 2: Local Directory

```bash
claude --plugin-dir /path/to/nlp-skills
```

## Components

### Skills (7 Specialized Domains)

| Skill | Triggers | Description |
|-------|----------|-------------|
| **llm-coach** | "train model", "fine-tune", "optimize" | Coaching guidance entry point |
| **llm-knowledge** | "what is LoRA", "compare models" | Knowledge base |
| **task-manager** | "list tasks", "compare versions" | Multi-task management |
| **data-pipeline** | "data source", "where does data come from" | Data pipeline configuration |
| **writing-plans** | "write a plan", "create training plan" | Plan-based task tracking |
| **executing-plans** | "execute plan", "run the plan" | Batch execution with checkpoints |
| **finetune-llm** | "fine-tune LLM", "training workflow" | Overview skill |

### Commands (9 Quick Actions)

| Command | Description |
|---------|-------------|
| `/nlp-skills:coach` | Start coaching dialogue |
| `/nlp-skills:tasks` | List all task status |
| `/nlp-skills:new-task` | Create new task |
| `/nlp-skills:data-source` | Configure data sources |
| `/nlp-skills:generate` | Generate project structure |
| `/nlp-skills:write-plan` | Write detailed execution plan |
| `/nlp-skills:execute-plan` | Execute plan with checkpoint reviews |
| `/nlp-skills:evaluate` | Run evaluation analysis |
| `/nlp-skills:deploy` | Deploy model |

### Agents (4 Intelligent Assistants)

| Agent | Trigger | Function |
|-------|---------|----------|
| **goal-clarifier** | Vague requirements | Proactively clarify goals |
| **data-source-advisor** | Data source questions | Help configure data pipelines |
| **problem-diagnoser** | Performance issues | Auto-diagnose and recommend fixes |
| **result-analyzer** | Post-training/evaluation | Analyze results, decision support |

## Usage

### Quick Start

```bash
# Coaching guidance
"I want to train a model"

# Direct creation
/nlp-skills:new-task entity-sentiment

# List tasks
/nlp-skills:tasks
```

### Complete Workflow

```
1. Start coaching        → Clarify goals, pain points, resources
2. Configure data source → Set up DB, API, scraping, LLM generation
3. Generate project      → Create scripts, configs, docs
4. Prepare data          → Run data generation scripts
5. Train model           → Execute training scripts
6. Evaluate performance  → Analyze results, compare versions
7. Deploy                → HuggingFace, Ollama
```

## Task Project Structure

Each task is a fully independent, self-contained project:

```
{task-name}/
├── task.yaml               # Task definition
├── data_source.yaml        # Data source config (reproducible)
├── plans/                  # Execution plans (plan-based tracking)
│   └── YYYY-MM-DD-goal.md
├── versions/               # Version tracking (full lineage)
│   ├── v1/
│   │   ├── config.yaml
│   │   ├── data_snapshot.json
│   │   ├── results.json
│   │   └── lineage.yaml
│   └── v2/
├── data/
├── scripts/
├── configs/
├── models/
└── benchmarks/
```

## Data Source Configuration

Core feature of v0.3 - reproducible data pipelines:

```yaml
# data_source.yaml
sources:
  - type: database
    connection: postgresql://...
    query: "SELECT text, label FROM annotations"

  - type: api
    endpoint: https://api.example.com/data

  - type: web_scrape
    urls: ["https://..."]
    keywords: ["finance", "stock"]

  - type: llm_generated
    model: gpt-4o
    count: 500
```

## Built-in Knowledge Base

Reduce web searches with built-in 2025-2026 knowledge:

| Category | Content |
|----------|---------|
| **Architecture** | Dense vs MoE, MLA |
| **Base Models** | Qwen3, DeepSeek-V3/R1, Llama 3.3 |
| **Training Methods** | SFT, LoRA, QLoRA, ORPO, DPO |
| **Task Types** | Sentiment Analysis, NER, Relation Extraction |
| **Troubleshooting** | Overfitting, Class Imbalance, Low Accuracy |

## Requirements

### Remote Server (Training)
- GPU: NVIDIA GPU (24GB+ VRAM recommended)
- Python: 3.10+

### Local Development
- Claude Code: Latest version

## Development

### Local Testing

```bash
claude --plugin-dir .
claude --debug --plugin-dir .
```

### Validation

```bash
./scripts/validate-plugin.sh
```

## CI/CD

- **GitHub Actions**: Auto-validates on push/PR
- **GitLab CI**: Auto-validates on push/MR

## Version History

See [CHANGELOG.md](skills/finetune-llm/CHANGELOG.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License

## Author

Weifan Liao (weifanliao@eland.com.tw)
