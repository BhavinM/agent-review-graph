# AgentReviewGraph 🕵️‍♂️🕸️

**The Ultimate Linter and Semantic Contradiction Detector for AI Agent Skills.**

AgentReviewGraph is a developer-centric CLI tool that acts as a policy linter for your AI agents. It parses your agent Markdown skill files, maps them into a strictly-typed **Semantic Knowledge Graph**, and uses **TypeSafe AI Jev** to detect critical contradictions before they reach production.

## Features

| Feature | Description |
|---|---|
| 🕸️ **Semantic Knowledge Graph** | Parses agent skills into a typed graph of Skill Nodes and Constraint Edges. Graph generation is fully independent of Jev — it works offline too. |
| 🧠 **Jev-Powered Contradiction Detection** | Uses TypeSafe AI's Jev System One engine to semantically evaluate constraints and flag conflicts with a severity score (0.0–1.0). |
| 🏷️ **Canonical Domain Tagging** | Jev tags every constraint with a Domain (e.g., `Security & Auth`, `Billing & Finance`). Only same-domain constraints are compared, eliminating millions of wasteful API calls at scale. |
| ⚡ **Adaptive Batch Requests** | Batches up to 10 constraint pairs into a single Jev request. If a batch fails with a 429, the engine recursively splits the batch in half and retries — self-healing under load. |
| 📊 **Interactive HTML Report** | Generates a stunning flamegraph dashboard highlighting all discovered conflict hotspots with Jev severity scores. |
| 🛑 **CI/CD Gatekeeper** | Fails your pipeline (`exit 1`) if critical contradictions are found. |
| 🤖 **Orchestrator Ready** | Exports a `knowledge_graph.json` that your master routing agent can ingest dynamically. |
| 🔌 **Offline Fallback** | If no API key is present, the tool falls back to fast local heuristics so you can still test your pipelines. |

## How the Knowledge Graph Works

The graph is built in **two independent phases**:

1. **Phase 1 — Structural Graph (Pure Python, no Jev required):**
   The parser reads every Markdown skill file and immediately builds a graph of `SkillNode` and `ConstraintEdge` objects. This skeleton graph is always generated.

2. **Phase 2 — Semantic Enrichment (Jev powered):**
   Jev enriches the graph by: (a) tagging each constraint with a Domain using `Choice`, (b) batching same-domain pairs and scoring their contradiction severity using `Score`, (c) drawing red `Contradiction Edges` on the graph for any pair exceeding the threshold.

## Installation

```bash
pip install agent-review-graph
```

## Usage

```bash
# Basic run (uses local heuristic fallback if no API key)
agent-review ./skills --output-dir ./reports

# Full live Jev run with configurable sensitivity
agent-review ./skills --output-dir ./reports --threshold 0.8 --verbose

# CI/CD strict mode — fails the pipeline if contradictions are found
agent-review ./skills --output-dir ./reports --fail-on-contradiction --threshold 0.9
```

## Live TypeSafe AI Integration

Export your API key to unlock full semantic analysis:

```bash
export TYPESAFE_API_KEY="jev_sk_..."
export TYPESAFE_BASE_URL="https://your-vercel-gateway.vercel.app"  # Optional

agent-review ./skills --output-dir ./reports --threshold 0.8 --verbose
```

## CLI Reference

| Flag | Description | Default |
|---|---|---|
| `target` | Path to a skill file or directory | Required |
| `--output-dir` | Directory for the HTML report and JSON graph | `./reports` |
| `--threshold` | Contradiction severity threshold (0.0–1.0). Lower = more sensitive. | `0.0` |
| `--fail-on-contradiction` | Exit with code 1 if any contradiction is found | `false` |
| `--verbose` | Enable debug logging for every Jev payload and response | `false` |

## Scalability: O(1) Domain Pre-Filtering

Without pre-filtering, comparing N rules requires O(N²) Jev API calls. For an enterprise with 2,500 rules, that is over 3 million comparisons!

**Domain Tagging solves this:** Jev tags each constraint at extraction time with a predefined domain (e.g., `Security & Auth`). The engine then uses an O(1) dictionary lookup to only compare constraints sharing the exact same domain, reducing comparisons by over 90%.

## Usage (GitHub Action)

```yaml
name: Agent Policy Linter
on: [pull_request]

jobs:
  lint-agents:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run AgentReviewGraph
        uses: agent-review-graph/action@v1
        with:
          target: './skills'
          threshold: '0.8'
          fail_on_contradiction: 'true'
          output_dir: './reports'
        env:
          TYPESAFE_API_KEY: ${{ secrets.TYPESAFE_API_KEY }}
```
