# TASK

Create a minimalist, voice-synchronized **Option B Cinematic Stage** animated explainer (`Explainers/<topic_folder>/index.html` + `narration.json`) using the single project configuration below, **and** keep the graphics, audio synchronization, and MP4 export code clean and transparent so I can understand, maintain, and extend every part from first principles.

Build a calm, high-clarity visual stage inspired by **Apple keynotes, Linear, and 3Blue1Brown**: **75%+ empty matte obsidian space (`#111110`)**, **only ONE clean focal composition on screen per Act**, crisp geometric silhouettes, causal wire bridges (never leaving connections mysterious), floating borderless captions, and a single sleek pill transport bar below the `16:9` frame.

Deliver:
1. `Explainers/<topic_folder>/narration.json` synthesized offline via `Explainers/tools/build_voiceover.py` using **`Kokoro-82M int8` (`af_bella`)** into gitignored `voiceover.wav` + `voiceover_bundle.js`.
2. `Explainers/<topic_folder>/index.html` (standalone `file://` playable + native `1920 × 1080` MP4 export mixing canvas video + `af_bella` voiceover).
3. Self-contained Side-Pane HTML Artifact in the conversation Artifact folder (with `window.VOICEOVER_DATA` inlined so `srcdoc` playback works immediately without relative file fetches).

Do not install packages into Jarvis's main `.venv` (`pyproject.toml` / `uv.lock`), do not require external paid APIs, and do not clutter the canvas with multi-panel dashboards or neon-cyan boxes.

---

# 1. PROJECT CONFIGURATION — EDIT SETTINGS ONLY HERE

**Topic Folder:** `Explainers/0X_<topic_slug>`
**Topic:** [PASTE SPECIFIC CONCEPT, MECHANISM, OR ARCHITECTURE FLOW HERE]

**Core Misconceptions to Break:**
1. [Misconception #1 — e.g., naive sequential/blocking mental model]
2. [Misconception #2 — e.g., hidden OS/memory/protocol handoff]

**Required Causal Proof Points (Must Be Visually Explicit):**
- [Point 1]
- [Point 2]
- [Point 3]

- Audience level: First-Principles Builder (Clear Cause-and-Effect, Behavior-Before-Jargon)
- Aesthetic style: Minimalist Cinematic Stage (Option B — Warm Matte Obsidian `#111110`)
- Visual density: Strict Minimalism (75%+ empty space, 1 focal composition per Act, zero stacked HUD boxes)
- Voiceover: Enabled (`Kokoro-82M int8` offline neural TTS · voice `af_bella`)
- Voiceover tool: `uv run --offline Explainers/tools/build_voiceover.py --manifest Explainers/0X_<topic_slug>/narration.json --voice af_bella`
- Subtitles: Enabled (Clean floating 1–2 line captions at bottom of `1920 × 1080` canvas, toggleable via `CC`)
- Format: Horizontal, `16:9` (`1920 × 1080` native canvas, `30 fps` MP4 export, `60 fps` live preview)
- Ambient harmonic bed: Subtle sine chime pad underneath `af_bella` (never overpowering speech)
- Final video format: Native `.mp4` (`avc1` + `mp4a`/`opus`, fallback `.webm` only if browser lacks MP4 `MediaRecorder`)
- Code walkthrough on request: Enabled

**This is the only editable project-input section.** Derive all narration cues, Act choreography, visual silhouettes, labels, and causal flows strictly from Section 1. Sections 2–6 below are universal design and engineering invariants shared across every explainer in `Explainers/`.

---

# 2. MINIMALIST CINEMATIC STAGE & PALETTE INVARIANTS (OPTION B)

Enforce this restrained, editorial color palette across every explainer:
- **Outer page backdrop:** `#0B0B0A`
- **16:9 Canvas stage ground:** `#111110` (flat matte obsidian—no noisy grids or harsh radial neon glows)
- **Subtle card / memory shelf fill:** `#181816` with `#2B2A27` hairline stroke
- **Primary strokes, active rings & headings:** Warm Ivory `#F4F1EA`
- **Quiet structural wires & secondary labels:** Muted Ash `#827E76` / Faint `#2B2A27`
- **Stalls, locks, naive bottlenecks & broken assumptions:** Warm Coral `#E57A44`
- **Free execution, wakeups & verified completions:** Sage Jade `#5EBA8D`
- **Saved state, memory frames, vectors, or queued kernel buffers:** Soft Indigo `#8492EE`

Typography & spacing rules:
- Use clean system sans-serif (`ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`) for headings/captions and crisp monospace (`ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`) for code/identifiers.
- Never render any HTML or Canvas text smaller than `12px`.
- Leave **75%+ of the `1920 × 1080` canvas empty**. Never display a 9-box dashboard; cross-fade cleanly (`ease(...)`) between distinct Acts when shifting abstraction layers.

---

# 3. PEDAGOGICAL & CAUSAL CLARITY LAWS

1. **Explicit Cause-and-Effect Bridges (Zero Magical Jumps):**
   - Never let state appear in RAM, wake up on a CPU, or arrive at a client without showing **what triggered it** and **which wire carried it**. If two components do *not* talk directly (e.g., External LLM and passive RAM), make the real intermediary (e.g., `OS Socket -> CPU -> RAM`) visually unmistakable.
2. **Strict Shape Grammar ("Never Make Everything a Box"):**
   - **Active Worker / CPU / Pointer:** Concentric ring + orbital arc (if 1 thread, draw literally **1** ring/core).
   - **Moving Requests / Signals / Packets:** Crisp circular dots or directional pulses (`r = 8–9px`) with short labels.
   - **Saved State / Frames / Payloads in Memory:** Rounded pills (`roundRect`) showing key internal fields.
   - **External I/O / Timers:** Circular progress dials (`arc` filling `-π/2 -> 3π/2`).
3. **Misconception Contrast First:**
   - Open by dramatizing why the naive mental model stalls or breaks (`#E57A44` coral), then show how the real mechanism resolves it on the exact same stage (`#5EBA8D` jade + `#8492EE` indigo).

---

# 4. OFFLINE `af_bella` VOICEOVER & EXACT CUE SYNCHRONIZATION

1. **Author `narration.json` (`6–8` conversational cues, `~75–110s` total):**
   ```json
   {
     "voice": "af_bella",
     "speed": 1.0,
     "leadIn": 0.5,
     "tailOut": 1.4,
     "cues": [
       { "id": 1, "act": 1, "pauseAfter": 0.7, "text": "..." }
     ]
   }
   ```
   Write natural spoken phrasing (spell out symbols where helpful for pronunciation, e.g., `"one-kilobyte"` instead of `"~1 KB"` in spoken text).
2. **Synthesize Offline via `build_voiceover.py`:**
   - Run `uv run --offline Explainers/tools/build_voiceover.py --manifest Explainers/0X_<topic_slug>/narration.json --voice af_bella`.
   - Read back the exact measured `{ start, voiceEnd, end }` cue timestamps printed by `build_voiceover.py` and lock every visual transition in `renderAt(sec)` to those exact timestamps!
3. **Dual-Target Delivery (`file://` Repo File + Antigravity `srcdoc` Artifact):**
   - In `Explainers/0X_<topic_slug>/index.html`, load `<script src="./voiceover_bundle.js"></script>` (plus `FALLBACK_CUES` so captions & visuals still work even before audio is generated).
   - In the Antigravity Artifact copy (`<artifactDir>/0X_<topic_slug>_explainer.html`), replace `<script src="./voiceover_bundle.js"></script>` with an inline `<script>window.VOICEOVER_DATA = ...;</script>` (optionally resampled to `16 kHz` 16-bit mono WAV for snappy Side-Pane loading) and decode via `AudioContext.decodeAudioData`.

---

# 5. DETERMINISTIC ENGINE, SLEEK TRANSPORT BAR & NATIVE MP4 EXPORT

Structure `index.html` with 5 clean, readable sections:
1. `// 1. CONFIG, PALETTE & VOICE-LOCKED TIMELINE CUES`
2. `// 2. MATH, EASING & MINIMALIST DRAWING PRIMITIVES`
3. `// 3. VOICE-SYNCHRONIZED CINEMATIC ACTS`
4. `// 4. SYNCED VOICEOVER + AMBIENT WEB AUDIO ENGINE`
5. `// 5. TRANSPORT CONTROLS & NATIVE 1080p MP4 EXPORT`

Technical invariants:
- **Pure `renderAt(sec)`:** Every frame is a pure function of `sec` (`0 .. DURATION`). During playback, advance `sec` from `AudioContext.currentTime` (`playAnchorOffset + (ctx.currentTime - playAnchorAudioTime)`) so canvas motion never drifts even a millisecond from `af_bella`'s voiceover.
- **Sleek Pill Bar Only:** `▶ Play`, clickable Act jump pills (`1 · ...`, `2 · ...`), hairline range scrubber, `m:ss / m:ss` monospace timer, `CC On/Off`, `🔊 Bella` mute toggle, and `Export MP4`.
- **True Audio+Video MP4 Export:** Route `masterGain` to both `speakerGain -> ctx.destination` and `ctx.createMediaStreamDestination()`. Combine `stage.captureStream(30)` video tracks + `audio.dest.stream.getAudioTracks()` into `MediaRecorder` preferring `video/mp4;codecs="avc1.640028,mp4a.40.2"` at `10 Mbps` video / `192 kbps` audio. Smoke-test `renderAt(t)` across `0 .. DURATION` in Node VM before finishing.
