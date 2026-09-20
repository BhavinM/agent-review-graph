# AgentReviewGraph: End-to-End Testing Guide 🎬

This guide walks through every feature of the CLI from setup to a full live Jev run, covering verbose logging, domain tagging, adaptive batching, and the CI/CD gatekeeper mode.

---

## Phase 1: Setup

```bash
cd /Users/bhavinmistry/Documents/Learning/JevLearning/agent-review-public

# Install the CLI in editable mode
pip install -e .

# Export your Live TypeSafe AI credentials
export TYPESAFE_API_KEY="jev_sk_..."
export TYPESAFE_BASE_URL="https://your-vercel-gateway.vercel.app"  # Optional
```

The `demo_workspace/skills/` directory should already contain 4 agent skill files:
- `search_agent.md` — Web search agent (Web Search & Research domain)
- `background_researcher.md` — Autonomous research agent (Web Search & Research domain)
- `billing_agent.md` — Handles payments and refunds (Billing & Finance domain)
- `security_agent.md` — Authentication and data access (Security & Auth domain)

---

## Phase 2: Basic Run (Verify Graph Generation Works Offline)

Temporarily unset the API key to verify the graph generates without Jev:

```bash
unset TYPESAFE_API_KEY
agent-review ./demo_workspace --output-dir ./demo_reports
```

✅ **Expected:** The CLI completes successfully, printing a warning that it is running in local fallback mode. The `demo_reports/` directory contains `agent-review-report.html` and `knowledge_graph.json`.

This confirms the Knowledge Graph is **independent of Jev** — Phase 1 always runs.

---

## Phase 3: Full Live Jev Run with Verbose Logging

Re-export the API key and run with full verbose debugging:

```bash
export TYPESAFE_API_KEY="jev_sk_..."
agent-review ./demo_workspace --output-dir ./demo_reports --threshold 0.8 --verbose
```

✅ **Expected terminal output (in order):**

1. `[INFO] Discovered 4 markdown files in directory.`
2. `[DEBUG] [JEV] Sending constraint extraction payload for: ...` — Jev classifying each text chunk.
3. `[DEBUG] [JEV] Extraction result: Actionable Constraint, Domain: Web Search & Research` — Domain tag assigned.
4. `[DEBUG] [JEV] Sending Batch Evaluation for X pairs...` — Adaptive batching in action.
5. `[DEBUG] [JEV] Batch Pair 0 Contradiction Score returned: 0.93` — Jev severity score.
6. `[INFO] Report generated: demo_reports/agent-review-report.html`

---

## Phase 4: Verify Domain Tagging (O(1) Pre-Filtering)

Inspect the generated `knowledge_graph.json` to confirm domain tags were assigned correctly:

```bash
cat demo_reports/knowledge_graph.json | python3 -m json.tool | grep domain_tag
```

✅ **Expected:** Each constraint node has a `domain_tag` field (e.g., `"Web Search & Research"`, `"Security & Auth"`).

Confirm the CLI only compared same-domain constraints by checking the verbose logs. You should NOT see `Billing & Finance` constraints being compared against `Web Search & Research` constraints.

---

## Phase 5: Verify Adaptive Batching (Self-Healing)

Temporarily simulate rate-limit pressure by running with an intentionally very low semaphore. You can also do this by watching the verbose logs — if a 429 occurs:

✅ **Expected log output when a batch fails:**
```
[WARNING] [JEV] Batch of 10 failed (Rate Limit/Error). Splitting into 5 and retrying...
```
The CLI will continue without crashing, splitting the batch recursively until all pairs are evaluated.

---

## Phase 6: Configurable Sensitivity Threshold

Run with a low threshold to see maximum contradictions surfaced:

```bash
agent-review ./demo_workspace --output-dir ./demo_reports --threshold 0.0 --verbose
```

Then run with a high threshold to filter out everything except the most severe conflicts:

```bash
agent-review ./demo_workspace --output-dir ./demo_reports --threshold 0.9 --verbose
```

✅ **Expected:** The HTML report's "Conflict Hotspots" section has significantly more/fewer entries depending on the threshold.

---

## Phase 7: CI/CD Gatekeeper (The Failure Path)

This is the killer enterprise feature — failing a pipeline when contradictions are found.

```bash
agent-review ./demo_workspace --output-dir ./demo_reports --fail-on-contradiction --threshold 0.8
echo "Exit code: $?"
```

✅ **Expected:**
- Terminal prints: `[ERROR] CRITICAL CONTRADICTIONS DETECTED. Failing CI check.`
- `echo $?` outputs `1` — confirming a non-zero exit code that will fail any CI/CD pipeline.

---

## Phase 8: Verify the HTML Report

Open the generated report:

```bash
open demo_reports/agent-review-report.html
```

✅ **Verify the UI:**
- **Left column (Semantic Nodes):** Lists all 4 agents and their extracted constraints, each with a Domain Tag badge.
- **Right column (Conflict Hotspots):** Shows red contradiction boxes between same-domain rules, with Jev severity scores.
