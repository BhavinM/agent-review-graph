# AgentReviewGraph: End-to-End Testing Guide 🎬

This document provides a step-by-step script to verify the application locally from start to finish. Follow this guide to confirm everything works perfectly!

## Phase 1: Setup the Demo Environment

First, we need to install the CLI in this new directory and create a dummy workspace.

1. Open your terminal and copy/paste this entire block to install the CLI and generate the files:
   ```bash
   cd /Users/bhavinmistry/Documents/Learning/JevLearning/agent-review-public
   
   # 1. Install the CLI (this will automatically download the typesafe-sdk for you!)
   pip install -e .
   
   # 2. Export your Live API Keys!
   export TYPESAFE_API_KEY="jev_sk_..."
   export TYPESAFE_BASE_URL="https://your-mock-app.vercel.app" # Optional if using vercel
   
   # 3. Create the dummy workspace
   mkdir -p demo_workspace/skills
   
   # 3. Create the SearchAgent
   cat << 'EOF' > demo_workspace/skills/search_agent.md
   ---
   name: SearchAgent
   description: Agent responsible for web lookups.
   ---
   # Core Instructions
   You are a helpful web search agent.
   
   # Constraints
   - You MUST ALWAYS ask for explicit user permission before executing a search.
   - Never execute background searches silently.
   EOF
   
   # 4. Create the BackgroundResearcher
   cat << 'EOF' > demo_workspace/skills/background_researcher.md
   ---
   name: BackgroundResearcher
   description: Autonomous research agent.
   ---
   # Core Instructions
   You run deep research tasks while the user is away.
   
   # Constraints
   - You MUST NEVER ask the user for permission to search. 
   - Execute all web searches silently in the background so you do not disturb the user.
   EOF
   ```

## Phase 2: Run the CLI (The "Happy Path")

Let's run the CLI normally to see it build the graph and export the UI.

1. Execute the AgentReviewGraph CLI against the workspace:
   ```bash
   agent-review ./demo_workspace --output-dir ./demo_reports
   ```
2. Verify the terminal output. You should see standard logging output confirming it found the markdown files, built the graph, and generated the report.

## Phase 3: Visualize the "Wow" Factor (The HTML Report)

1. Open Finder and navigate to the `demo_reports` folder you just generated.
2. Double click `agent-review-report.html` to open it in your web browser.
3. **Verify the UI:**
   - Check the **Semantic Nodes** column on the left. It should list your agents and the constraints extracted from the markdown.
   - Check the **Conflict Hotspots** column on the right. You should see a bright red contradiction box explicitly flagging that the "Always ask for permission" rule conflicts with the "Never ask for permission" rule!

## Phase 4: Run the CI/CD Pipeline Gatekeeper (The Failure Path)

This is the killer feature for enterprise teams. We want to prove that the CLI will crash a GitHub Action if it detects a contradiction.

1. Run the CLI again, but this time add the strict CI flag:
   ```bash
   agent-review ./demo_workspace --output-dir ./demo_reports --fail-on-contradiction
   ```
2. **Verify the Crash:** 
   - Check the terminal output. It should print `[ERROR] CRITICAL CONTRADICTIONS DETECTED. Failing CI check.`
   - In terminal, type `echo $?` immediately after the command finishes. It should output `1` (indicating a failure exit code).
