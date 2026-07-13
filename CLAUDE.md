# mcp-hello-server — notes for Claude

A minimal MCP server built with **Python / FastMCP** — a good starting point for
a new server or a demo. It exposes two tools: `server_info` (a health/status
check) and `greet` (a friendly greeting in one of a handful of languages,
defaulting to English). Built with **uv**, **FastMCP**, **pytest**, and
**make**; multi-stage Docker on a distroless Chainguard/Wolfi Python base
(`cgr.dev/chainguard/python`) for a near-zero-CVE image. It was scaffolded from the
sibling [`random-mcp-server`](../random-mcp-server) by stripping every tool down
to `server_info` and adding the `greet` demo tool.

## Layout

- `src/mcp_hello_server/greetings.py` — greeting data (`GREETINGS`), language
  resolution (names, aliases, ISO codes), and the `greet()` builder.
- `src/mcp_hello_server/server.py` — the FastMCP server (`mcp`), its tools
  (`server_info`, `greet`), and the `main()` console-script entry point
  (`mcp-hello-server`).
- `tests/` — pytest suite. `test_server.py` drives the tools through an
  **in-memory FastMCP `Client`** (no network, no subprocess); `test_greetings.py`
  unit-tests the resolver/builder; `test_bdd.py` + `tests/features/*.feature` are
  a pytest-bdd layer.

## Conventions

- **Dependencies / venv:** managed by uv. `make install` runs `uv sync` (creates
  `.venv`). `uv.lock` is committed and the Dockerfile installs `--frozen` from it,
  so run `make lock` (or `uv lock`) whenever `pyproject.toml` deps change.
- **Running:** `make run` (stdio, the default MCP transport), `make run-http`
  (streamable HTTP on `PORT`, default 8000), `make dev` (FastMCP Inspector). The
  transport is chosen by `MCP_TRANSPORT` (`stdio` | `http` | `sse`).
- **Tests:** `make test` → `uv run pytest`.
- **Adding a language:** add a row to `GREETINGS` in `greetings.py` (and,
  optionally, an alias / ISO code in `_ALIASES`). `server_info` reports the
  supported set automatically.
- **Docker:** the image defaults to HTTP transport (`MCP_TRANSPORT=http`,
  `HOST=0.0.0.0`, `PORT=8000`) so it's reachable on a published port. The base is
  distroless Chainguard/Wolfi Python (`cgr.dev/chainguard/python`), which already
  runs as the non-root `nonroot` user (uid 65532) and has no shell / package
  manager. The venv is built on the matching `-dev` image so its interpreter
  symlink resolves at runtime. `make scan` should report 0 CRITICAL/HIGH.
- **Releasing:** `make release` (`BUMP=patch|minor|major`, default patch) bumps
  the version, commits, tags `vX.Y.Z`, and pushes — the tag triggers the GHCR +
  Docker Hub publish workflows. `make release` does **not** touch `CHANGELOG.md`,
  so add the new version's entry (Keep a Changelog format, top of the file)
  **before** running it.

## Tools

| Tool                       | Purpose                                                  |
| -------------------------- | -------------------------------------------------------- |
| `server_info()`            | Health/status: app name, version, uptime, languages.     |
| `greet(language?, name?)`  | Greeting in a language (default English); optional name. |

Supported languages: `english`, `spanish`, `french`, `german`, `italian`,
`portuguese`, `japanese`, `hawaiian`. Lookups accept aliases / ISO codes
(`fr`, `Français`, …) case-insensitively.

## Gotchas

- `@mcp.tool` replaces the module-level function with a Tool object; unit-test
  tools through the in-memory `Client`, not by calling the name directly. In
  `server.py` the underlying greeting builder is imported as `_greet` so the
  `greet` tool wrapper can call it.
- **Explicit `version`** is passed to `FastMCP(...)` (read from package
  metadata); without it FastMCP reports its own framework version in the MCP
  handshake / `fastmcp inspect`.
- **Absolute import in `server.py`** (`from mcp_hello_server.greetings import …`,
  not `from .greetings`) so the FastMCP CLI can load the file by path.
