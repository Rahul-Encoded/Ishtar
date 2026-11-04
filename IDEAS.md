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
- **Candidate Languages:** Python (`import socket` only) or C/C++ (`<winsock2.h>` / `<sys/socket.h>`).

### 2. Developer Load, Resource-Limit & Failure-Mode Simulator Library
- **Date Logged:** 2026-10-29
- **Concept:** A developer-friendly library/tool to bombard a service with high-concurrency simulated traffic under strict resource caps (CPU, RAM, connection pools) to observe **when, where, and how** the system breaks.
- **Interesting Twist / Gap to Explore:** Traditional load testers (`k6`, `Locust`, `wrk`) focus on standard REST APIs. Modern apps (especially AI/LLM backends, WebSockets, and database-heavy apps) fail in unique ways: event-loop blocking, connection pool starvation, memory leaks on long-lived streams, and cascading upstream `429` rate limits. A tool that pairs load generation with real-time resource bottleneck & failure-mode diagnostics could be super valuable.

---

## Future Jarvis Ideas & Seeds

### 1. Dogfooding This File into Jarvis's Memory
- Once Jarvis has PostgreSQL + `pgvector` semantic memory and safe file-reading tools, ingest `IDEAS.md` and `RESOURCES.md` as initial personal knowledge so Jarvis knows our ongoing learning goals, references, and project backlog.
