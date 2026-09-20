# Agent Review Graph

A CLI linter and semantic contradiction detector for AI agent skill files, powered by TypeSafe AI Jev.

Agent Review Graph parses Markdown skill files used by AI agents, constructs a typed Semantic Knowledge Graph, and evaluates rule pairs for semantic contradictions before deployment.

## Features

- **Semantic Knowledge Graph**: Parses agent Markdown files into a graph of skill nodes and constraint edges. Works offline without external API dependencies.
- **Semantic Contradiction Detection**: Uses TypeSafe AI's Jev engine to evaluate rule pairs for semantic conflicts with severity scoring (0.0 to 1.0).
- **Canonical Domain Pre-Filtering**: Classifies constraints into logical domains (e.g. `Security & Auth`, `Billing & Finance`, `Web Search`). Compares only rules sharing the same domain, reducing API calls by over 90%.
- **Adaptive Batching**: Groups constraint pairs into batch requests, automatically splitting batches under rate limits.
- **HTML Report Generation**: Generates an interactive HTML flamegraph dashboard displaying rule conflicts, severity scores, and Jev reasoning.
- **CI/CD Integration**: Supports `--fail-on-contradiction` to exit with code 1, allowing automated pipeline gating on pull requests or pre-commit checks.
- **JSON Knowledge Graph Export**: Exports `knowledge_graph.json` for consumption by routing agents or external tooling.

## How It Works

Knowledge graph construction occurs in two phases:

1. **Structural Analysis (Local)**: Parses Markdown files to extract frontmatter metadata, headers, bullet points, and rule constraints. Constructs local `SkillNode` and `ConstraintEdge` structures without network calls.
2. **Semantic Enrichment (Jev Engine)**: Categorizes constraints by domain and evaluates same-domain constraint pairs for semantic contradictions, populating severity scores and conflict edges.

## Installation

```bash
pip install agent-review-graph
```

## Quickstart

```bash
# Analyze a skills directory (local fallback mode if no API key is set)
agent-review ./skills --output-dir ./reports

# Run with Jev semantic evaluation enabled
export TYPESAFE_API_KEY="jev_sk_..."
agent-review ./skills --output-dir ./reports --threshold 0.8 --verbose

# Run in strict mode (exits 1 on contradiction)
agent-review ./skills --output-dir ./reports --fail-on-contradiction --threshold 0.8
```

## CLI Reference

| Flag | Description | Default |
|---|---|---|
| `target` | Path to a skill file or directory | Required |
| `--output-dir` | Output directory for the HTML report and JSON graph | `./reports` |
| `--threshold` | Severity score threshold for flagging contradictions (0.0–1.0) | `0.0` |
| `--fail-on-contradiction` | Exit with status code 1 if any contradiction is detected | `false` |
| `--verbose` | Enable verbose logging for API payloads and internal events | `false` |

## Domain Pre-Filtering Performance

Comparing $N$ rules naively requires $O(N^2)$ pairwise checks. For 2,500 rules, this would require over 3 million API evaluations.

Agent Review Graph assigns each constraint to a canonical domain at extraction time. An $O(1)$ lookup isolates comparisons strictly to same-domain rule pairs, reducing comparison complexity by over 90%.

## GitHub Action Integration

```yaml
name: Agent Policy Linter

on: [pull_request]

jobs:
  lint-agents:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Agent Review Graph
        uses: agent-review-graph/action@v1
        with:
          target: './skills'
          threshold: '0.8'
          fail_on_contradiction: 'true'
          output_dir: './reports'
        env:
          TYPESAFE_API_KEY: ${{ secrets.TYPESAFE_API_KEY }}
```

## License

Licensed under the PolyForm Noncommercial License 1.0.0. See [LICENSE](LICENSE) for details.
