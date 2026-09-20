# Hyperframes Composition Brief: AgentReviewGraph

## Objective

Create a short polished launch-style brag video for AgentReviewGraph — a CLI tool that semantically lints AI agent policy files using TypeSafe AI's Jev engine to detect contradictions that static analysis cannot catch.

## Output

- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 22 seconds

## Source Material

- Project root: `/Users/bhavinmistry/Documents/Learning/JevLearning/agent-review-public/`
- Primary files read: `README.md`, `demo_workspace/skills/search_agent.md`, `demo_workspace/skills/background_researcher.md`, `demo_reports/agent-review-report.html`
- Product name: **AgentReviewGraph**
- Tagline / strongest claim: "The Ultimate Linter and Semantic Contradiction Detector for AI Agent Skills."
- Key UI or visual moment to recreate: The red contradiction box from `agent-review-report.html` — "❌ Contradiction Detected / Jev Severity: 99.0 / 100"
- Copy that must appear verbatim:
  - `You MUST ALWAYS ask for explicit user permission before executing a search.` (search_agent.md)
  - `You MUST NEVER ask the user for permission to search.` (background_researcher.md)
  - `[JEV] Extraction result: Actionable Constraint, Domain: Web Search & Research`
  - `[JEV] Batch Pair 0 Contradiction Score returned: 0.93`
  - `Exit code: 1`
  - `Jev Severity: 99.0 / 100`
  - `AgentReviewGraph`
  - `Lint at PR time.`

## Creative Direction

- Tone preset: polished
- Creative direction: quiet premium product film for a serious developer tool
- Interpretation: Slow, confident reveals. Generous holds. Every text line settles before the next arrives. Dark terminal aesthetic. No hype language. Technical credibility is the creative statement. The product's 0.93 contradiction score is the punchline.
- Angle: The hook is the contradiction itself — two Markdown files saying opposite things about search permissions. The rest of the video is the tool catching it.
- Hook: Two code panels side by side. Left: "MUST ALWAYS ask for explicit user permission." Right: "MUST NEVER ask the user for permission." No narration. No title. Let it land.
- Outro / punchline: "AgentReviewGraph / Lint at PR time. / The runtime layer comes next."
- Avoid:
  - Generic SaaS language ("streamline your workflow", "AI-powered solution")
  - Abstract filler visuals (gradients, particles, code rain)
  - Any visual that isn't directly from the product

## Visual Identity

- Background: `#0f172a` (slate-900 — exact value from the HTML report)
- Text primary: `#f8fafc` (slate-50)
- Text secondary: `#94a3b8` (slate-400)
- Accent: emerald `#10b981` / cyan `#22d3ee` (from report header gradient)
- Contradiction red: `#ef4444` / `rgba(239, 68, 68, 0.8)`
- Constraint indigo: `#6366f1`
- Display font: `JetBrains Mono` (load from Google Fonts) — terminal feel, matches developer aesthetic
- Body font: `Inter` (load from Google Fonts) — clean sans-serif for labels
- Visual references from the project:
  - Dark-panel card style from `agent-review-report.html` (border: `#1e293b`, bg: `rgba(15,23,42,0.8)`)
  - The emerald-to-cyan gradient text header ("AgentReviewGraph" in the report)
  - The red contradiction box with red pill badge (`bg-red-500/20`, `text-red-400`, `border border-red-500/50`)
  - The `🧠 Extracted by Jev System One` indigo label style

## Storyboard

Use the storyboard in `brag-output/brag-plan.md` as the creative contract.

Scene summary:
1. **The Contradiction** — 5s — Two Markdown panels side by side. Must show verbatim contradiction constraints from the actual skill files. Red underline connects the conflicting lines.
2. **CLI Run + Score** — 9s — Terminal. Command types in. 3 log lines appear. Domain tag highlights emerald. Contradiction score (`0.93`) reveals red. `⚠ Flagged` label appears.
3. **HTML Report** — 4s — Red contradiction box recreated. "Jev Severity: 99.0 / 100" badge. Must feel like the actual report. Box scale-pops in.
4. **CI/CD Gate** — 2s — Terminal. `--fail-on-contradiction` command + `Exit code: 1` in red.
5. **Outro** — 2s — `AgentReviewGraph` in emerald gradient. `Lint at PR time.` `The runtime layer comes next.` Three staggered fades.

## Audio

- Audio role: warm professional bed — steady and clean
- Audio arc: music fades in softly under Scene 1, holds constant through Scenes 2-4, fades out gently under Scene 5
- Music: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`
- Music treatment: `data-volume="0.30"`, starts at 0s, gentle fade-out from t=20s to t=22s
- Music cue guidance: bundled preset JSON at `/Users/bhavinmistry/.agents/skills/brag/assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json`. Strong cues: 8.74s (0.99), 13.11s (0.98), 17.47s (0.99), 22.93s (1.00). Target HTML report box reveal near 8.74s. Target score highlight near 13.11s. Target exit-code line near 17.47s. Target outro logo near 22.93s.
- Audio-reactive treatment: subtle; drive soft `boxShadow` glow pulsing on the terminal panel backgrounds using music RMS/bass. Amplitude range should be barely perceptible — 2-4px shadow spread variation. No waveform visuals. Not wired to text elements.
- Audio-coupled moments:
  - Scene 2 command typing — `keyboard/keypress-*.wav` randomized across ~8 characters; stop after the command is complete
  - Scene 2 contradiction score (0.93) fully visible — `interface/bong_001.ogg` at 0.65 volume
  - Scene 3 red contradiction box snap-in — `impact/impactBell_heavy_000.ogg` at 0.70 volume
  - Scene 4 exit code "1" landing — `interface/drop_001.ogg` at 0.60 volume
- SFX selection guidance: choose only the cues above. One sound per moment. No stacking. Each SFX fires at the moment the visual lands, not before.
- SFX analysis guidance: `/Users/bhavinmistry/.agents/skills/brag/assets/sfx/sfx-analysis.md` — prefer low HF-risk files; `bong_001` and `impactBell_heavy_000` are both appropriate for polished moments.
- Exact SFX choice: Hyperframes should choose timing and volume based on the implemented animation.
- Audio files: copy music and selected SFX into `brag-output/composition/assets/`

## Hyperframes Instructions

Load `hyperframes-core`, `hyperframes-animation`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-cli`. This is a `/brag` workflow — do not enter the `hyperframes` entry-point intent interview and do not route into any generic promo/launch-video workflow. Prefer native Hyperframes conventions.

**Critical requirements:**

1. All text shown on screen must be verbatim from the source project (see "Copy that must appear verbatim" above). Do not paraphrase the constraint text.
2. The font families used must match the developer aesthetic: JetBrains Mono for terminal/code content, Inter for labels and headings. Load both from Google Fonts.
3. The dark panel card style must match the HTML report's visual: `#0f172a` background, `#1e293b` card background, emerald-400 skill file names, indigo-400 "Extracted by Jev" labels, red-400 contradiction headings.
4. Scene 1: the two panels must appear simultaneously, sliding in from opposite sides. The red underline should draw after a 2s hold. This is the "show the thing" scene.
5. Scene 3: the red contradiction box must scale-pop into place (`scale: 0.85 → 1.0`, `back.out(1.2)` ease, ~0.5s). The severity badge number must count up from 0 to 99. This is the best-frame poster candidate — it must be visually impactful at any frozen frame.
6. Run `hyperframes check` before render — fix all errors including WCAG contrast failures. Terminal copy on `#0f172a` must meet contrast requirements (use `#e2e8f0` or lighter for log text if needed).
7. Total duration is exactly 22 seconds.
8. Do not use abstract filler: every scene must contain copy, code, or visual elements directly from the source project.
9. For the audio-reactive treatment, use the `extract-audio-data.py` helper from the `hyperframes-creative/scripts/` skill directory to pre-extract per-frame audio bands. Wire the bass band to a gentle `boxShadow` oscillation on the terminal panel. If extraction is unavailable, note it and skip — do not block the render.
10. For beat sync: the HTML report box reveal should be beat-locked to the strong cue at 8.74s (±0.15s). Mark it `// beat-locked: 8.74s`. For the sequential log lines in Scene 2, snap each to consecutive beats near the scene's midpoint — mark `// beat-grid`.
