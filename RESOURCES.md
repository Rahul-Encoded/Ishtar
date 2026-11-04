# Engineering Resources & Deep-Dive References

A curated list of foundational documentation, specifications, and guides referenced while building **Jarvis** from first principles.

---

## 1. ASGI, Uvicorn & FastAPI Internals

### The Node.js to Python Mental Model
| Role | Node.js Equivalent | Python Equivalent |
| :--- | :--- | :--- |
| **Language Runtime** | V8 | CPython (`python.exe`) |
| **Event Loop & HTTP Server** | `libuv` + built-in `node:http` (`http.createServer`) | **Uvicorn** (`asyncio` event loop + TCP/HTTP parser) |
| **Server-to-Framework Contract** | `(req, res) => {}` callback | **ASGI** (`async def app(scope, receive, send)`) |
| **Web Framework & Routing** | Express.js / Fastify | **FastAPI** (built on **Starlette**) |
| **Schema Validation** | Zod / TypeScript | **Pydantic v2** |

### Core Reading
- **[Official ASGI Specification & Introduction](https://asgi.readthedocs.io/en/latest/introduction.html)**
  - Best starting point to understand the `scope`, `receive`, and `send` interface that connects Uvicorn to FastAPI.
  - Read the **Introduction** and **Specs: ASGI (HTTP & WebSocket)** sections (~15 mins).
- **[Starlette ASGI Documentation](https://www.starlette.io/asgi/)**
  - FastAPI inherits its entire HTTP routing, middleware, and ASGI handling directly from Starlette.
- **[Uvicorn Documentation](https://www.uvicorn.org/)**
  - Explains how Uvicorn manages the `asyncio` event loop, worker processes, and HTTP parsing (`h11` / `httptools`).
- **[FastAPI Official Tutorial — User Guide](https://fastapi.tiangolo.com/tutorial/)**
  - Reference for path/query parameters, Pydantic models, and dependency injection (`Depends`).

---

## 2. Building an HTTP Server from Scratch (Future Side Project)

- **[Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)**
  - The classic, gold-standard free book on OS sockets (`socket()`, `bind()`, `listen()`, `accept()`, `recv()`, `send()`) in C.
- **[Python `socket` Library Documentation](https://docs.python.org/3/library/socket.html)**
  - Python's built-in thin wrapper over OS-level TCP/IP sockets.
- **[RFC 9110 (HTTP Semantics)](https://httpwg.org/specs/rfc9110.html) & [RFC 9112 (HTTP/1.1)](https://httpwg.org/specs/rfc9112.html)**
  - The official IETF specifications defining how HTTP/1.1 text messages (`GET /path HTTP/1.1\r\n...`) are formatted over TCP.

---

## 3. Python Packaging & Toolchain

- **[uv Documentation (Astral)](https://docs.astral.sh/uv/)**
  - Reference for managing virtual environments (`.venv`), lockfiles (`uv.lock`), dependencies (`pyproject.toml`), and Python versions (`uv python`).
