# Project Ideas, Future Plans & Brainstorms

> **Purpose:** Capture every side-project idea, feature concept, and architectural experiment that comes up while building **Jarvis**.
> 1. Keeps us laser-focused on the current milestone without losing creative sparks.
> 2. Serves as **real personal seed data** later when we test Jarvis's Long-Term Memory and Document Ingestion engine!

---

## Side-Project Ideas (Standalone Repos / Libraries)

### 1. Zero-Library HTTP/1.1 Server from Scratch
- **Date Logged:** 2026-10-29
- **Concept:** Build a working HTTP server from first principles using zero third-party frameworks—pure OS sockets (`socket()`, `bind()`, `listen()`, `accept()`, `recv()`, `send()`).
- **Goal:** Deeply master TCP sockets, raw HTTP byte parsing, routing dictionaries, non-blocking event loops, and the ASGI boundary (separating the socket server from the web framework).
- **Ultimate Boss Test:** Make our homemade server implement the real ASGI 3.0 `await app(scope, receive, send)` contract so it can actually boot and serve a real FastAPI `app` without Uvicorn!
- **Candidate Languages:** Python (`import socket` + `asyncio` only) or C/C++ (`<winsock2.h>` / `<sys/socket.h>`).

### 2. Developer Load, Resource-Limit & Failure-Mode Simulator Library
- **Date Logged:** 2026-10-29
- **Concept:** A developer-friendly library/tool to bombard a service with high-concurrency simulated traffic under strict resource caps (CPU, RAM, connection pools) to observe **when, where, and how** the system breaks.
- **Interesting Twist / Gap to Explore:** Traditional load testers (`k6`, `Locust`, `wrk`) focus on standard REST APIs. Modern apps (especially AI/LLM backends, WebSockets, and database-heavy apps) fail in unique ways: event-loop blocking, connection pool starvation, memory leaks on long-lived streams, and cascading upstream `429` rate limits. A tool that pairs load generation with real-time resource bottleneck & failure-mode diagnostics could be super valuable.

### 3. First-Principles Synth & Chromatic Instrument Tuner Studio (Audio Math Playground)
- **Date Logged:** 2026-11-04
- **Concept:** A zero-sample-file web/desktop audio lab with two halves that teach both directions of digital sound:
  1. **Play Instruments (Synthesis — Math → Speakers):** Generate playable keyboard/guitar/drum sounds purely from oscillation equations ($y(t) = A \sin(2\pi f t)$), waveforms (`sine`, `triangle`, `sawtooth`, `square`), ADSR volume envelopes, filters, and the 20-line Karplus-Strong plucked-string algorithm—visualized live on an oscilloscope canvas.
  2. **Tune Real Instruments (DSP Analysis — Microphone → Math):** Capture live microphone PCM samples, run **FFT / Autocorrelation pitch detection** to identify the exact note and cent deviation (e.g., `A4 = 440.0 Hz`, `-8 cents flat`), and render both Time-Domain (waveform) and Frequency-Domain (spectrum) graphs in real time.
- **Goal:** Demystify digital audio from scratch—sample rates (`44.1 kHz` / `48 kHz`), `Float32Array` PCM buffers, harmonics/timbre, Fourier transforms, and Web Audio API / Python `sounddevice` + `numpy`.
- **Bonus Payoff for Jarvis:** Mastering raw mic streams, PCM chunking, RMS silence/voice detection (VAD), and FFT spectrograms directly prepares us to build Jarvis's real-time Voice Interface (wake-word + STT + live voice waveform UI) without treating audio as a black box.
- **Candidate Stack:** Pure JS (`Web Audio API` + `<canvas>`) for instant browser playability, optionally paired with a Python DSP backend/CLI (`sounddevice` + `numpy.fft`).

### 4. First-Principles Indian Equities Screener, Tranche-Sizing & Quant Backtester
- **Date Logged:** 2026-11-06
- **Origin:** Real portfolio lessons from holding **MCX** (+900% structural monopoly + operating leverage, under-sized due to waiting for dips), **IEX** (regulatory market-coupling moat risk), and **Shree Renuka Sugars** (commodity/policy cyclicality).
- **3-Stage Learning & Build Roadmap:**
  1. **Master Stock & Accounting Parameters:** Understand P&L, Balance Sheet, Cash Flow (`CFO vs PAT`), `ROCE`/`ROE`, Operating Leverage, Valuation (`P/E`, `EV/EBITDA`, `PEG`), and sector nuances (e.g., Banks/NBFCs vs. Exchanges/Manufacturing).
  2. **Personal Systematic Workflow:** Rule-based filtering + 3-tranche *averaging-up* (pyramiding on earnings + strength) + thesis-invalidation exit rules so winners compound and losers stay capped.
  3. **Institutional / Quant Pipeline (Standalone Lab or Jarvis Skill):** Historical NSE backtesting (bias-free, no look-ahead/survivorship traps), Quality + Momentum factor scoring, and automated Screener/filing ingestion inside Jarvis.

---

## Future Jarvis Ideas & Seeds

### 1. Dogfooding This File into Jarvis's Memory
- Once Jarvis has PostgreSQL + `pgvector` semantic memory and safe file-reading tools, ingest `IDEAS.md` and `RESOURCES.md` as initial personal knowledge so Jarvis knows our ongoing learning goals, references, and project backlog.

### 2. Rebuilding Jarvis's Offline Neural Voice Pipeline from First Principles (No Wrapper Magic)
- **Date Logged:** 2026-11-06
- **Why:** In `Explainers/tools/build_voiceover.py`, we used `kokoro-onnx` + `soundfile` pragmatically to narrate explainer videos—but before shipping Voice inside **Jarvis**, we want to understand every byte well enough to write it ourselves without AI or black-box wrappers.
- **4-Step "Zero-Magic" Build Path (When We Reach the Voice Milestone):**
  1. **Raw `.wav` Binary Writer in Pure Python (`struct.pack`, 0 third-party libraries):** Hand-write the 44-byte RIFF/WAVE header + 16-bit signed PCM integers from scratch so audio files stop feeling mysterious.
  2. **Text → Phonemes → Token IDs (`G2P`):** Understand why TTS models consume IPA phonetic symbols (`"enough"` → `ɪˈnʌf` → integer IDs) rather than raw English spelling.
  3. **Direct `onnxruntime.InferenceSession` (Drop the `kokoro-onnx` Wrapper):** Load `kokoro-v1.0.int8.onnx` and `voices-v1.0.bin` directly with `onnxruntime` + `numpy`, inspect the exact input tensors (`tokens`, 256-float `style` voice vector—even blending two voice vectors mathematically!—and `speed`), and capture the raw `float32` waveform array.
  4. **Real-Time Async Sentence Streaming in FastAPI:** Pipe Ollama's streaming text tokens into a sentence splitter + background worker so Jarvis starts speaking Sentence #1 out loud while Sentence #2 is still generating.
