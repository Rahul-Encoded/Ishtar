# Engineering Learning Log (Q&A)

A running log of systems engineering questions, mental models, and under-the-hood mechanics explored while building **Jarvis**.

---

## 1. Python Packaging, `uv`, and Environment

### Q: What is the difference between a Python module and a Python package?
- **Module:** Any single `.py` file (e.g., `main.py`). When imported, Python executes it top-to-bottom.
- **Regular Package:** A folder containing an `__init__.py` file (e.g., `src/jarvis/`). It groups related modules together so you can write `from jarvis import main`.
- **Namespace Package (no `__init__.py`):** Allowed since Python 3.3 (PEP 420) for splitting packages across multiple repos, but in normal projects we always include `__init__.py` for explicit intent and faster imports.

### Q: Why is `.venv` in `.gitignore`, while `pyproject.toml` and `uv.lock` are committed?
- `.venv` contains thousands of files and OS/CPU-specific compiled C/Rust binaries (e.g., Windows `x86_64` for Python 3.14). It bloats Git and breaks on other machines/OSes.
- `pyproject.toml` (version rules like `>=0.128.0`) and `uv.lock` (exact pinned versions + cryptographic hashes) are tiny text blueprints that allow `uv sync` to recreate `.venv` identically anywhere.

### Q: Why did `pyproject.toml` need `[tool.pytest.ini_options] pythonpath = ["src"]`?
- Because we use the `src/` layout (`src/jarvis/main.py`). By default, running `pytest` from the project root looks in `./jarvis` instead of `./src/jarvis`. Setting `pythonpath = ["src"]` tells `pytest` where to find the `jarvis` package (just like `--app-dir src` tells Uvicorn).

---

## 2. Python Type Hints & Testing

### Q: Does `dict[str, str]` mean a dictionary with only 2 string items?
- **No.** `dict[KeyType, ValueType]` defines the type of **all keys** and **all values** (equivalent to TypeScript's `Record<string, string>`), regardless of whether the dictionary has 1 item or 1,000 items.
- If values can be strings or integers, the type becomes `dict[str, str | int]`—or better yet, a **Pydantic `BaseModel`**.
- Unlike plain Python (which ignores type hints at runtime), **FastAPI** reads return type hints at runtime via Pydantic to validate responses and generate `/docs`.

### Q: Why write `pytest` tests if we already checked the endpoint in the browser? And what happens when an `assert` fails?
- Manual browser checks prove code works *today*; automated `pytest` tests catch regressions *weeks later* in milliseconds when refactoring shared code.
- In Python, `assert x == y` raises an `AssertionError` immediately when `False`. Execution stops inside **that single test function**, while `pytest` still runs all **other** `test_*` functions in the suite.
- Note on dictionaries: `"timestamp" in data` checks **keys** (left side), not values!

---

## 3. HTTP, Uvicorn, ASGI & FastAPI Under the Hood

### Q: What is the difference between `uv`, `uvicorn`, and `FastAPI`?
1. **`uv`** (like `npm`/`npx`): Package manager and `.venv` launcher. Not a server.
2. **`uvicorn`** (like Node's `libuv` + `http.createServer`): The ASGI web server that binds to port `8000`, manages TCP sockets and the `asyncio` event loop, and parses raw HTTP bytes.
3. **`FastAPI`** (like Express.js + Zod): The web framework that routes paths (`/health`) to controller functions (`get_health()`), validates schemas via Pydantic, and returns JSON payloads to Uvicorn.

### Q: What does the actual parsed request look like when Uvicorn hands it to FastAPI?
When a browser sends raw TCP bytes over port `8000`:
```http
GET /health?verbose=true HTTP/1.1\r\n
Host: 127.0.0.1:8000\r\n
User-Agent: Mozilla/5.0\r\n
\r\n
```
Uvicorn parses those bytes and invokes your FastAPI `app` using the **ASGI 3.0 contract**:
```python
await app(scope, receive, send)
```
1. **`scope` (a plain Python `dict` describing connection metadata & headers):**
   ```python
   {
       "type": "http",
       "asgi": {"version": "3.0", "spec_version": "2.4"},
       "http_version": "1.1",
       "method": "GET",
       "scheme": "http",
       "path": "/health",
       "raw_path": b"/health",
       "query_string": b"verbose=true",
       "headers": [
           (b"host", b"127.0.0.1:8000"),
           (b"user-agent", b"Mozilla/5.0"),
       ],
       "client": ("127.0.0.1", 54321),
       "server": ("127.0.0.1", 8000),
   }
   ```
2. **`receive` (an `async` function FastAPI awaits to read request body chunks, e.g. for `POST` JSON):**
   ```python
   event = await receive()
   # Returns: {"type": "http.request", "body": b'{"message": "hello"}', "more_body": False}
   ```
3. **`send` (an `async` function FastAPI calls twice to send status/headers and then the body back to Uvicorn):**
   ```python
   await send({
       "type": "http.response.start",
       "status": 200,
       "headers": [(b"content-type", b"application/json")],
   })
   await send({
       "type": "http.response.body",
       "body": b'{"status":"ok"}',
   })
   ```

### Q: Can I build "ASGI itself" from scratch?
- **ASGI is not an installed library—it is just a specification (a rulebook)** saying *"Servers must call `await app(scope, receive, send)` with those exact dict keys."*
- Building an ASGI system from scratch means writing two small pieces in pure Python (`socket` + `asyncio`):
  1. **Mini-Uvicorn:** Accepts a TCP socket, splits the raw HTTP string on `\r\n`, builds the `scope` dict above, defines `receive()` and `send()` closures over the socket, and runs `await app(scope, receive, send)`.
  2. **Mini-FastAPI:** Defines an `async def __call__(self, scope, receive, send)` class that matches `(scope["method"], scope["path"])` to a Python function and calls `await send(...)` with the JSON bytes.

---

## 4. Concurrency: `async/await` in JavaScript vs. Python (`asyncio`)

### Myth #1: "Adding `async/await` automatically makes chronological steps run in parallel"
- **False in BOTH JS and Python.**
- If Task 1 = 1s, Task 2 = 2s, Task 3 = 1s, and you write:
  ```python
  a = await task1()  # waits 1s
  b = await task2()  # waits 2s
  c = await task3()  # waits 1s
  ```
  That function **still takes 4 seconds** (`1 + 2 + 1`), because each `await` pauses *that function* until the line finishes.
- **So what did `await` actually buy us?** While that function is paused waiting on the network/DB, the server's single thread is **freed up to handle other users' HTTP requests** instead of freezing the entire server!
- **How DO you run all 3 tasks concurrently if they don't depend on each other?**
  - **In JS:** `await Promise.all([task1(), task2(), task3()])` -> finishes in **2 seconds** (`max(1, 2, 1)`).
  - **In Python:** `await asyncio.gather(task1(), task2(), task3())` -> finishes in **2 seconds** (`max(1, 2, 1)`).

### Myth #2: "Python `async` spawns 3 threads to run 3 tasks in parallel"
- **False!** Both Node.js `async/await` and Python `asyncio` (`async/await`) run on **ONE SINGLE THREAD**!
- **How can 1 single thread finish three network calls (`1s`, `2s`, `1s`) in `2s` total?**
  - Think of **1 Waiter (your single CPU thread)** and **3 Ovens in the Kitchen (PostgreSQL, LLM API, Disk)**:
  - **Synchronous code:** The waiter puts Dish 1 in the oven and **stares at the oven door frozen for 1s**, then puts Dish 2 in and stares for 2s, then Dish 3 for 1s = **4s total**.
  - **Multi-threading (`threading`):** You hire **3 separate waiters** (3 OS threads). Costs extra RAM and causes race conditions.
  - **`async/await` (JS & Python `asyncio`):** **Still just 1 waiter!** At `t=0`, the waiter puts Dish 1, Dish 2, and Dish 3 into the ovens at the same time (fires 3 network sockets) and walks away to serve other tables. The *ovens* (external servers/OS network card) cook simultaneously. At `t=2s`, the slowest dish finishes! **Total time: 2s on 1 single thread.**

### The REAL Difference Between JavaScript and Python `async`
- **JavaScript (Node.js) only has ONE world:** Almost all I/O (`fetch`, DB drivers) is non-blocking by default. You rarely block the event loop by accident.
- **Python has TWO worlds living side-by-side:**
  1. **Old Synchronous (blocking) libraries:** `time.sleep(2)`, `requests.get(...)` — these **freeze the waiter**! Never call blocking functions inside `async def`!
  2. **Modern Asynchronous (non-blocking) libraries:** `await asyncio.sleep(2)`, `await httpx.AsyncClient().get(...)` — these yield control back to the event loop just like Node.js!
- **FastAPI's safety trick:**
  - `async def endpoint()`: Runs directly on the single-threaded event loop (just like Express in Node.js). Use this when `await`-ing async DB/LLM calls.
  - `def endpoint()` (no `async`): FastAPI assumes your code might block, so it automatically runs it in a separate background worker threadpool so you don't freeze the server!

### Q: Why does `async` matter if I am the ONLY human user of Jarvis?
Even with **1 human user**, your frontend makes **concurrent requests** to your backend:
- Suppose `POST /chat` is waiting 20 seconds on Ollama—or paused waiting for you to click **"Approve Tool Execution"**.
- If that request blocked the server synchronously, clicking **"Stop Generation"** (`POST /chat/cancel`) or **"Approve"** (`POST /tools/approve`) from your UI would hang at the door—deadlocking your own app!

### Q: Is it Hardware or Software that manages two requests concurrently? (The Full Stack Trace)
It is a **3-layer handoff** between **Hardware**, the **OS Kernel**, and **Uvicorn Software**:
1. **Hardware (Network Interface Card / NIC):** Receives electrical/radio packets from User A and User B, copies the bytes directly into RAM (via DMA), and triggers a CPU hardware interrupt so neither packet is lost even if Python is busy.
2. **OS Kernel (Windows `IOCP` / Linux `epoll`):** Organizes each TCP connection into a numbered **Socket File Descriptor** (like numbered mailboxes: `Socket #5` = User A, `Socket #6` = User B). If your server is synchronous, `Socket #6` sits queued inside the OS Kernel's RAM buffer waiting its turn.
3. **Application Software (`Uvicorn` + Python `asyncio` Event Loop):**
   - Uvicorn runs a `while True:` loop in software.
   - When User A (`Socket #5`) hits `await call_llm()`, Python saves User A's local variables + current line number into a tiny object in RAM (a **coroutine frame**—like a bookmark) and parks it.
   - Uvicorn immediately asks the OS Kernel (`IOCP`/`epoll`): *"Which sockets have bytes ready right now?"* The OS hands over `Socket #6` (User B), so the CPU immediately runs User B's code!
   - When the LLM's reply arrives at the network card, the OS Kernel wakes Uvicorn: *"`Socket #7` has data!"* Uvicorn picks up User A's bookmark from RAM, resumes from the exact line after `await`, and sends the reply out through `Socket #5`.

### Q: When multiple users connect to that 1 CPU thread, do their requests finish sequentially in chronological arrival order?
- **Only in a blocking (synchronous) server—NOT in an async server!**
- Suppose `User A` (5s LLM call), `User B` (5ms health ping), and `User C` (1s DB query) arrive at almost the same moment on **1 CPU thread**:
  - **Blocking (`def` without threadpool / synchronous I/O):** `User A` locks the thread for 5s. `User B` and `User C` wait in arrival line (`A -> B -> C`), so `User B`'s 5ms ping takes `5.005s`!
  - **Async (`async def` + `await`):** `User A` hits `await`, parks a `~1 KB` coroutine frame in RAM, and frees the CPU in microseconds. That **exact same 1 thread** immediately finishes **`User B` 1st** (`5ms`), starts `User C` (which finishes **2nd** at `1s`), and finishes **`User A` 3rd** (`5s`). Requests complete **by I/O speed, not arrival order**.

### Q: What actually IS that "bookmark" in RAM, and is RAM directly connected to the LLM/Database?
- **What the "bookmark" is:** A **Python Coroutine Frame** (`~1 KB` object on the RAM heap) storing the paused function's **current line / bytecode offset** (`f_lasti`) and **local variables** (`f_locals`). Compare that to spawning a full OS thread (`~1–8 MB` stack each).
- **No direct `RAM <-> LLM` wire:** RAM is passive memory—the LLM or PostgreSQL never reaches into your RAM directly! Instead, when the DB or LLM finishes, its TCP reply hits your **Network Card (DMA)** → queues in an **OS Socket (`#7` or `#5`)** → wakes the **CPU** (`Uvicorn` event loop) → and the **CPU** reaches up into **RAM** to pull down and resume the matching Coroutine Frame.

### Q: What is `IOCP` / `epoll`?
- Without OS help, Uvicorn would have to run a wasteful `for` loop checking 10,000 sockets one by one (`O(N)` busy-polling: *"Socket #1 any bytes? No. Socket #2? No..."*).
- **`IOCP`** (*I/O Completion Ports* on Windows) and **`epoll`** (on Linux) are OS kernel notification mechanisms: Uvicorn registers all open sockets with the OS once and goes to sleep (`0%` CPU). The instant bytes arrive on `Socket #7`, the OS kernel taps Uvicorn with **only** the ready socket IDs in **`O(1)` constant time**.

### Q: What is the difference between a TCP Socket and an SSE (`Server-Sent Events`) stream—and how does `POST /approve` fit in?
- **TCP Socket (OS Layer 4):** The raw two-way byte pipe managed by Windows/Linux between your browser/UI and Uvicorn (identified by `IP:Port`, e.g., `Socket #5`). It knows nothing about JSON, routes, or tokens—only raw bytes.
- **SSE (`Server-Sent Events` — `Content-Type: text/event-stream`, Layer 7 HTTP):** Normal HTTP sends one response and closes/finishes the turn. **SSE** is a normal HTTP response kept open over that TCP socket so Uvicorn can keep pushing live chunks (`data: {"token": "Allow tool?"}\n\n`) from Jarvis to your UI in real time.
- **Exact Causal Order of Tool Approval in Jarvis:**
  1. Your UI opens `POST /chat` (kept open as an SSE stream).
  2. The LLM replies *"I want to run `delete_files`—ask permission."*
  3. Uvicorn streams `"Allow tool?"` down the open SSE response to your UI, then your `chat` coroutine hits `await approval_event.wait()` and **parks in RAM** (`approved = ?`), freeing the CPU!
  4. You click **Approve** in the UI → sends a separate quick request `POST /approve (True)` → hits the **free CPU** → flips `approval_event.set()` → wakes the `chat` coroutine from RAM to run the tool and stream the final answer!
