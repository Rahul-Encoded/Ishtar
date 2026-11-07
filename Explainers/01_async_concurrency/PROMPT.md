# TASK

Create a minimalist, voice-synchronized **Option B Cinematic Stage** animated explainer (`Explainers/01_async_concurrency/index.html` + `narration.json`) using the single project configuration below, **and** keep the graphics, audio synchronization, and MP4 export code clean and transparent so I can understand, maintain, and extend every part from first principles.

---

# 1. PROJECT CONFIGURATION — EDIT SETTINGS ONLY HERE

**Topic Folder:** `Explainers/01_async_concurrency`
**Topic:** Single-Threaded Async Concurrency Across Hardware, OS Sockets, RAM Coroutine Frames, and Python `Uvicorn`/`FastAPI`—Covering Both Multi-User Out-of-Order Completion and 1-User Jarvis Tool Approval.

**Core Misconceptions to Break:**
1. *"Multiple users on 1 CPU thread must finish sequentially in chronological arrival order—or else Python must spawn 3 threads."*
2. *"RAM is directly wired to the LLM/Database—or `POST /approve` happens randomly before the LLM asks permission."*
3. *"Only multi-user websites need `async`—a 1-user local Jarvis desktop app can't deadlock itself."*

**Required Causal Proof Points (Must Be Visually Explicit):**
- **Multi-User Out-of-Order Completion (`Acts 1–3`):** Show 3 simultaneous arrivals (`User A` 5s LLM, `User B` 5ms Ping, `User C` 1s DB) on **1 CPU Thread**. Contrast Blocking (User A locks the thread; B & C stall in arrival order) against Async (User A parks a `~1 KB` Coroutine Frame in `RAM`, freeing the exact same 1 thread so **`User B` finishes 1st**, **`User C` finishes 2nd**, and **`User A` finishes 3rd**—completion by speed, not arrival order).
- **Explicit `External I/O -> OS Socket -> CPU -> RAM` Bridge (`Act 3`):** Explicitly show `✕ No direct RAM ↔ LLM wire (RAM is passive)`. Replies from the DB/LLM arrive at OS Sockets (`Socket #7`, `Socket #5`), wake the `CPU`, and the `CPU` reaches up into `RAM` to pull down and resume the matching Coroutine Frame.
- **Causal 1-User Jarvis Tool-Approval Flow (`Act 4`):** Show `LLM` first streaming `"Allow tool?"` over SSE to `You (Jarvis UI)`, `chat` parking in `RAM` (`approved = ?`), leaving `CPU` free to catch `POST /approve (True)` and wake `chat` from `RAM`.
- **Hardware & Timing Finale (`Act 5`):** Show `Network Card (DMA Direct-to-RAM)` -> `OS Kernel (epoll / IOCP)` `O(1)` wakeup -> Two-bar timing race (`4.0s Blocking` vs `2.0s Async (1 Thread)`).

- Audience level: First-Principles Builder (Clear Cause-and-Effect, Behavior-Before-Jargon)
- Aesthetic style: Minimalist Cinematic Stage (Option B — Warm Matte Obsidian `#111110`)
- Visual density: Strict Minimalism (75%+ empty space, 1 focal composition per Act, zero stacked HUD boxes)
- Voiceover: Enabled (`Kokoro-82M int8` offline neural TTS · voice `af_bella`, `101.184s` across 7 cues)
- Voiceover tool: `uv run --offline Explainers/tools/build_voiceover.py --manifest Explainers/01_async_concurrency/narration.json --voice af_bella`
- Subtitles: Enabled (Clean floating 1–2 line captions at bottom of `1920 × 1080` canvas, toggleable via `CC`)
- Format: Horizontal, `16:9` (`1920 × 1080` native canvas, `30 fps` MP4 export, `60 fps` live preview)
- Ambient harmonic bed: Subtle sine chime pad underneath `af_bella`
- Final video format: Native `.mp4` (`avc1` + `mp4a`/`opus`)
- Code walkthrough on request: Enabled

---

*(Sections 2–5 follow the shared invariants in `Explainers/PROMPT_TEMPLATE.md`.)*
