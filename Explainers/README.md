# Explainers — Minimalist Visual Engineering & Voiceover Archive

This directory houses interactive **minimalist cinematic explainers** generated while building **Jarvis** from first principles. Every explainer serves two goals:
1. **Systems Mastery:** Visually prove how hardware, OS kernels, protocols, and Python runtimes actually behave—breaking naive mental models before writing code in `src/jarvis/`.
2. **Graphics & Audio Engineering:** Keep every animation deterministic (`renderAt(sec)`), cleanly readable in ~300–1,000 lines of vanilla Canvas + Web Audio JS, and exportable to native `1920 × 1080` MP4 with offline neural narration.

---

## Directory Architecture

Each explainer lives in its own numbered folder alongside a shared offline voiceover tool:

```text
Explainers/
├── README.md                          # Architecture & workflow conventions (this file)
├── PROMPT_TEMPLATE.md                 # Reusable master prompt (edit Section 1 per topic)
├── .tts_models/                       # [gitignored] Cached Kokoro-82M int8 ONNX + voices.bin (~115 MB)
├── tools/
│   └── build_voiceover.py             # Reusable PEP-723 `uv` script (isolated from Jarvis `.venv`)
├── 01_async_concurrency/              # Topic #1: Multi-User & 1-User Single-Threaded Async
│   ├── PROMPT.md                      # Configured prompt for this topic
│   ├── narration.json                 # Spoken cues + pauses for `af_bella`
│   ├── index.html                     # Minimalist 1080p Canvas player + MP4 exporter
│   ├── voiceover.wav                  # [gitignored] Generated 24 kHz mono WAV
│   └── voiceover_bundle.js            # [gitignored] Cue timestamps + base64 WAV for file:// playback
└── 02_<next_topic_slug>/
    ├── PROMPT.md
    ├── narration.json
    └── index.html
```

---

## Design & Engineering Standards

1. **Minimalist Cinematic Stage (Option B — Apple / Linear / 3Blue1Brown Vibe):**
   - **75%+ empty matte obsidian space (`#111110`)**—never crowd 9 boxes onto one screen.
   - **One focal composition per Act**, warm ivory strokes (`#F4F1EA`), quiet ash labels (`#827E76`), and three restrained semantic accents: coral (`#E57A44` = blocked/stall), sage jade (`#5EBA8D` = free/out-of-order completion), and soft indigo (`#8492EE` = saved state / RAM frames).
   - **Single sleek pill bar** below the `16:9` frame (`▶ Play`, Act pills, hairline scrubber, `CC`, `🔊 Bella`, `Export MP4`).

2. **100% Offline Neural Voiceover (`af_bella` via `Kokoro-82M int8`):**
   - `Explainers/tools/build_voiceover.py` uses PEP-723 inline `uv` metadata (`onnxruntime` + `kokoro-onnx`), keeping **zero TTS dependencies** inside Jarvis's main `pyproject.toml` or `.venv`.
   - Once `.tts_models/` is cached locally, synthesize or tweak any explainer's narration 100% offline:
     ```powershell
     uv run --offline Explainers/tools/build_voiceover.py --manifest Explainers/0X_<topic>/narration.json --voice af_bella
     ```
   - `index.html` loads `<script src="./voiceover_bundle.js"></script>` (which works directly over `file://` in Chrome/Edge with zero CORS server needed) and locks `renderAt(sec)` to `AudioContext.currentTime` (`VO.cues` timestamps).
   - When rendering inside Antigravity's Side-Pane Artifact viewer (`srcdoc`), inline `window.VOICEOVER_DATA` directly into the Artifact copy so relative paths aren't needed.

3. **Git Hygiene (Commit Code, Ignore Heavy Audio/Model/Video Binaries):**
   - Commit `PROMPT.md`, `narration.json`, `index.html`, and `tools/build_voiceover.py` (~30–50 KB of clean text).
   - `.gitignore` excludes `Explainers/.tts_models/`, `Explainers/**/*.mp4`, `Explainers/**/*.wav`, and `Explainers/**/voiceover_bundle.js`.

4. **Workflow for Every Future Concept (`02_`, `03_`, ...):**
   - Copy `PROMPT_TEMPLATE.md` to `Explainers/0X_<topic_slug>/PROMPT.md` and edit **Section 1 (`PROJECT CONFIGURATION`)**.
   - Author `narration.json` -> run `build_voiceover.py` (`af_bella`) -> lock `index.html` visual Act transitions to the exact measured cue timestamps in `voiceover_bundle.js`.
