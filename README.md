# AgentReviewGraph 🕵️‍♂️🕸️

**The Ultimate Linter and Semantic Graph Inspector for AI Agents.**

AgentReviewGraph is a developer-centric CLI tool that acts as a "shovel" in the AI gold rush. It parses your AI agent skill files, maps them into a strictly typed Knowledge Graph, and detects critical semantic contradictions before they reach production.

## Features
- 🚀 **Intelligent AST Parsing:** Accurately extracts rules and YAML metadata while safely ignoring example code blocks.
- ⚡ **O(N²) Clustering Engine:** Employs advanced semantic heuristics to prevent API bottlenecks when scaling to 100+ agents.
- 🛑 **CI/CD Gatekeeper:** Fails your pipeline (`exit 1`) if two agents are given conflicting instructions.
- 📊 **Visual Flamegraph:** Generates a stunning, interactive HTML dashboard to visualize conflict hotspots.
- 🤖 **Orchestrator Ready:** Exports a `knowledge_graph.json` that your master routing agent can ingest dynamically.
- **TypeSafe AI Integration**: Uses the Jev System One engine to parse, map, and rigorously cross-reference agent rules.
- **Configurable Sensitivity**: Tune the contradiction threshold using the `--threshold` flag (0.0 to 1.0).
- **Adaptive API Batching**: Dynamically chunks requests and recursively scales down batch sizes (Self-Healing) under rate-limit pressure to guarantee maximum throughput.
- **Educational UI Report**: Generates a sleek, interactive HTML dashboard highlighting raw skills and Jev-evaluated conflicts.

## Installation

```bash
pip install agent-review-graph
```

## Usage (Local)

Run the CLI against any markdown file or plugin directory:

```bash
agent-review /path/to/skills --output-dir ./reports --threshold 0.8 --verbose
```

### Advanced Usage

```bash
# Fail a CI/CD pipeline if critical contradictions are found
agent-review ./agent_skills --fail-on-contradiction --threshold 0.9

# Run with verbose debugging to see exact Jev payloads and scores
agent-review ./agent_skills --verbose
```

## Live TypeSafe AI Integration

AgentReviewGraph is powered by the **TypeSafe AI Jev** engine (a fast System One model designed for deterministic classification).

To unlock live semantic routing and contradiction detection, export your API key (and an optional Base URL if you are using a mock/Vercel instance):
```bash
export TYPESAFE_API_KEY="jev_sk_..."
export TYPESAFE_BASE_URL="https://your-vercel-mock.vercel.app" # Optional
agent-review ./my-agent-skills/ --fail-on-contradiction
```

*Note: If no API key is detected or the `typesafe` SDK is not installed, the tool safely falls back to a fast local string-matching heuristic so you can still test your CI/CD pipelines!*

## Usage (GitHub Action)

Drop AgentReviewGraph directly into your CI/CD pipeline to block pull requests that break agent constraints!

```yaml
name: Agent Linter
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
          fail_on_contradiction: 'true'
          output_dir: './reports'
```
