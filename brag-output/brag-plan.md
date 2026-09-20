# Brag Plan: AgentReviewGraph

## What is this app?

AgentReviewGraph is a CLI tool that semantically lints AI agent skill files — using TypeSafe AI's Jev engine to detect policy contradictions across agents before they ship to production.

## The angle

Static analysis can't catch this. A human reviewer can't catch this. Two agent skills, both written in plain English, both in your codebase, saying opposite things about search permissions — and neither will be flagged by any linter on the market today. This video shows what catches it.

The hook isn't the tool. The hook is the contradiction.

## Hook (first 2-3 seconds)

Two Markdown files side by side. Left: `search_agent.md` — "MUST ALWAYS ask for explicit user permission before executing a search." Right: `background_researcher.md` — "MUST NEVER ask the user for permission to search." No title. No label. Let the contradiction land on its own.

## Key moments (the middle)

- **The CLI run**: `agent-review ./demo_workspace --output-dir ./demo_reports --threshold 0.8 --verbose` streams logs. The domain tag line flashes: `[JEV] Extraction result: Actionable Constraint, Domain: Web Search & Research`. This is the O(1) trick — same-domain only.
- **The score**: `Batch Pair 0 Contradiction Score returned: 0.93` — Jev calls it a contradiction. Score displayed in red.
- **The HTML report**: The flamegraph dashboard, zoomed into the red contradiction box. "Jev Severity: 99.0 / 100." Two rules. Flagged. Named. Explained.
- **CI/CD gate**: `--fail-on-contradiction` → `Exit code: 1`. Terminal. PR blocked.

## Outro / punchline

"Part one of a two-tool governance stack." AgentReviewGraph name + tagline: "Lint at PR time." Followed by a quiet line: "The runtime layer comes next." No URL. The comment hook does the work.

## User flow worth showing

Entry → CLI run with verbose logs streaming → HTML report contradiction box → CI/CD exit code 1

This is the full working-app flow. No landing page. Every scene shows the product in use.

## Tone
- Preset: polished
- Creative direction: quiet premium product film for a serious developer tool
- Interpretation: Slow reveals. Generous holds. Text appears and settles — never rushed. Dark terminal aesthetic. The product's technical credibility is the creative statement. No hype language. Let the 0.93 score do the talking.

## Format: landscape — 1920x1080
## Duration: 22 seconds

## Visual identity (from the project)

- Background: `#0f172a` (slate-900 — the HTML report background)
- Accent: emerald → `#10b981` / cyan → `#22d3ee` (gradient from report header)
- Text: `#f8fafc` (slate-50 — primary text)
- Contradiction red: `rgba(239, 68, 68, 0.8)` / `#ef4444` (contradiction boxes)
- Constraint indigo: `#6366f1`
- Display font: JetBrains Mono (terminal readability; falls back to `ui-monospace, monospace`)
- Body font: Inter (falls back to `system-ui, sans-serif`)
- Strongest visual element: The red contradiction box with "Jev Severity: 99.0 / 100" badge — this is the video's poster frame candidate

## Share copy (draft)

Introducing AgentReviewGraph: a semantic linter for AI agent policies.
Built with TypeSafe AI Jev. Catches the contradictions no static analyzer sees. Ships with `--fail-on-contradiction` to block your CI/CD pipeline.

## Audio direction
- Role: warm professional bed — steady and clean, supporting without competing with the technical content
- Music: `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` — steady, clean, best for polished/cinematic
- Music treatment: starts at 0s, volume 0.30, gentle fade-out under the final 2s of the outro
- Music cue guidance: bundled preset at `assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json`. Strong cues in window: 8.74s (intensity 0.99), 13.11s (0.98), 17.47s (0.99), 22.93s (1.00). Target the HTML report reveal for the 8.74s strong cue (beat-locked ±0.15s). Target the contradiction score reveal near 13.11s. Target the CLI exit code reveal near 17.47s. Target the outro logo near 22.93s.
- Audio-reactive treatment: subtle; use music RMS/bass to make the terminal background glow breathe softly. Apply a slow, gentle `boxShadow` or `opacity` oscillation on the terminal panel background. No waveform visuals.
- SFX posture: sparse, 2-3 cues. Nothing aggressive. Polished restraint.
- Audio-coupled moments:
  - Terminal logs streaming (Scene 2) — soft key tick sounds (`keyboard/keypress-*.wav`, randomized) at ~8 characters then stop; the full log is the visual
  - The contradiction score appearing (Scene 2) — `interface/bong_001.ogg` at 0.65 volume when the `0.93` number is fully visible
  - The red contradiction box reveal (Scene 3) — `impact/impactBell_heavy_000.ogg` at 0.70 volume when the box snaps in
  - Exit code 1 landing (Scene 4) — `interface/drop_001.ogg` at 0.60 volume
- Restraint rule: music must not overpower the terminal text. If any SFX feels cute rather than functional, drop it. Two well-placed cues are better than five mediocre ones.

---

## Storyboard

### Scene 1 — The Contradiction — 5s

**On screen:** Dark `#0f172a` background. Two code panels side by side, recreated in HTML. 

Left panel header: `search_agent.md` in emerald. Body shows the constraint in mono: "You MUST ALWAYS ask for explicit user permission before executing a search."

Right panel header: `background_researcher.md` in emerald. Body shows: "You MUST NEVER ask the user for permission to search."

Both panels slide in from left and right respectively, settling centered. No title. No annotation. Let the contradiction speak.

After 2.5s settled: a thin red line traces under both "permission" constraints simultaneously — a visual underline connecting the conflict. Holds.

Sequential/interaction: left panel slides in from left, right panel from right — simultaneous 0.5s slide entrances. Red underline draws after 2s hold.
Audio intent: quiet anticipation — music bed enters softly
Audio-coupled idea: no SFX; let the visual tension do the work
Music: warm bed, fades up from 0 to 0.30 over the first 1s
Transition mood: soft crossfade (0.5s) → Scene 2

---

### Scene 2 — CLI Run + Score — 9s

**On screen:** Full-width dark terminal panel (`#0f172a` background, slightly lighter border). 

Top line: `$ agent-review ./demo_workspace --output-dir ./demo_reports --threshold 0.8 --verbose`

Command types in character by character (0.8s to complete). Then logs stream in 3 lines, appearing one at a time at 0.4s intervals:

```
[INFO] Parsing skill files in ./demo_workspace/skills...
[JEV] Extraction result: Actionable Constraint, Domain: Web Search & Research
[JEV] Batch Pair 0 Contradiction Score returned: 0.93
```

At 5s into scene: The domain tag line (`Domain: Web Search & Research`) gets a soft emerald highlight glow. Holds 1s.

At 7s into scene: The score line (`0.93`) pulses with a red glow. A small label appears below: `⚠ Flagged` in red.

Sequential/interaction: command types out, then logs appear one-by-one. Beat-locked: domain-tag highlight at beat near 5.34s in track (absolute ~10.34s), score reveal at beat near 6.56s (absolute ~11.56s) — both within ±0.10s of beat grid. `// beat-grid: domain-highlight at 5.0s local, score reveal at 7.0s local`
Audio intent: focused attention — this is the technical heart of the product
Audio-coupled idea: soft randomized key ticks during the command typing (keyboard/keypress-*.wav, 8 characters, then stop); bong_001.ogg at 0.65 vol when 0.93 appears and is fully settled
Transition mood: soft crossfade (0.4s) → Scene 3

---

### Scene 3 — HTML Report — 4s

**On screen:** Dark panel recreating the HTML report's contradiction section. The header: "AgentReviewGraph" in the emerald-to-cyan gradient. Below: the red contradiction box.

Red box contents:
- Header: "❌ Contradiction Detected" in red-400
- Badge: "Jev Severity: 99.0 / 100" (red pill)  
- Two rule nodes: `background_researcher.md` vs `search_agent.md`
- Footer text: "Jev System One detected high semantic contradiction."

The red box zooms in slightly (scale 0.85 → 1.0 over 0.5s) and then holds. This is the poster frame moment.

Sequential/interaction: box arrives with a subtle scale pop; severity badge number counts up 0 → 99 over 0.8s. `// beat-locked: box reveal at strong cue ~8.74s absolute`
Audio intent: the payoff — the problem is surfaced
Audio-coupled idea: impactBell_heavy_000.ogg at 0.70 vol when the box fully snaps in
Transition mood: soft crossfade (0.4s) → Scene 4

---

### Scene 4 — CI/CD Gate — 2s

**On screen:** Terminal again. Two lines:

```
$ agent-review ./demo_workspace --fail-on-contradiction --threshold 0.8
Exit code: 1
```

The `Exit code: 1` line appears after 0.8s. Displayed in red text. A subtle red glow on the terminal panel border pulses once.

Sequential/interaction: command appears instantly (no typing — polished, not chaotic). Exit code appears after 0.8s. `// beat-locked: exit code lands near strong cue ~17.47s absolute`
Audio intent: decisive — the pipeline is blocked
Audio-coupled idea: interface/drop_001.ogg at 0.60 vol when "Exit code: 1" appears
Transition mood: soft crossfade (0.5s) → Scene 5

---

### Scene 5 — Outro — 2s

**On screen:** Clean dark background. 

Line 1 (emerald gradient): `AgentReviewGraph`  
Line 2 (slate-400, light weight): `Lint at PR time.`  
Line 3 (slate-500, smaller, appears after 1s hold): `The runtime layer comes next.`

Lines appear with short fade-up reveals (0.3s each, staggered by 0.3s). Hold 1.5s. Music fades out softly over the final 1.5s.

Sequential/interaction: three lines stagger in. `// beat-locked: logo name appears near strong cue ~22.93s absolute`
Audio intent: elegantly resolved — the work is done
Audio-coupled idea: none — let the music bed tail naturally
Transition mood: hold to end

---

**Music mood for this video:** steady and clean, warm corporate
**Audio summary:** Music enters softly under the contradiction reveal and holds steadily through the CLI and report scenes; one bell cue marks the score reveal, one bell marks the contradiction box; music fades cleanly under the outro logo.
