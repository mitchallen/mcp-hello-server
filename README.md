# mcp-hello-server

[![GitHub tag](https://img.shields.io/github/v/tag/mitchallen/mcp-hello-server?sort=semver&label=version)](https://github.com/mitchallen/mcp-hello-server/tags) [![Docker Hub](https://img.shields.io/docker/v/mitchallen/mcp-hello-server?sort=date&label=docker%20hub)](https://hub.docker.com/r/mitchallen/mcp-hello-server) [![Docker image size](https://img.shields.io/docker/image-size/mitchallen/mcp-hello-server/latest?label=image%20size)](https://hub.docker.com/r/mitchallen/mcp-hello-server/tags) [![Docker pulls](https://img.shields.io/docker/pulls/mitchallen/mcp-hello-server?label=pulls)](https://hub.docker.com/r/mitchallen/mcp-hello-server) [![test](https://github.com/mitchallen/mcp-hello-server/actions/workflows/test.yml/badge.svg)](https://github.com/mitchallen/mcp-hello-server/actions/workflows/test.yml) [![bdd](https://github.com/mitchallen/mcp-hello-server/actions/workflows/bdd.yml/badge.svg)](https://github.com/mitchallen/mcp-hello-server/actions/workflows/bdd.yml) [![image-scan](https://github.com/mitchallen/mcp-hello-server/actions/workflows/image-scan.yml/badge.svg)](https://github.com/mitchallen/mcp-hello-server/actions/workflows/image-scan.yml)

A minimal [MCP](https://modelcontextprotocol.io) server built with Python and
[FastMCP](https://gofastmcp.com) — a good starting point for a new server or a
demo. It exposes just two tools:

- **`server_info`** — a health/status check.
- **`greet`** — a friendly greeting in one of a handful of languages, defaulting
  to English. Ask it to "greet in French" and it replies `Bonjour!`.

Built with **Python**, **[uv](https://docs.astral.sh/uv/)**, **FastMCP**, and
**make**. It was scaffolded from the sibling
[`random-mcp-server`](../random-mcp-server) by stripping it down to
`server_info` and adding the `greet` demo tool.

* * *

## Quick start — demo an MCP server in 2 minutes

New to MCP? This is a tiny, safe server for **seeing how an MCP client discovers
and calls tools**. Every tool is a harmless in-memory lookup, so it's a good
sandbox. All you need is **[Docker](https://docs.docker.com/get-docker/)** and an
MCP client — the steps below use **[Claude Code](https://claude.com/claude-code)**
and the published Docker Hub image (nothing to build or install).

**1. Add the server.** Claude Code launches the container per session and talks
to it over stdio:

```sh
claude mcp add hello -- docker run -i --rm -e MCP_TRANSPORT=stdio mitchallen/mcp-hello-server:latest
```

**2. Confirm it connected:**

```sh
claude mcp list        # "hello" should report ✔ Connected
```

**3. Ask in plain language** — Claude discovers the tools and picks one (the tool
it calls is in parentheses):

- "Is the hello server up? What version is it?" → (`server_info`)
- "Greet me in French." → (`greet` → **Bonjour!**)
- "Say hello in Japanese to Alice." → (`greet` → **こんにちは (Konnichiwa), Alice!**)
- "What languages can you greet in?" → (`server_info`, reads `languages`)

That round trip — the client listing tools, then calling one with arguments and
getting structured JSON back — *is* MCP. Peek at the tool schemas the client sees
with `make dev` (the FastMCP Inspector), or read [Tools](#tools) below.

**4. Remove it when you're done:**

```sh
claude mcp remove hello
```

> **Prefer HTTP?** Run it as a long-lived server instead:
> ```sh
> docker run --rm -p 8000:8000 mitchallen/mcp-hello-server:latest
> claude mcp add --transport http hello http://localhost:8000/mcp
> ```
> See [Using a published image or a remote server](#using-a-published-image-or-a-remote-server)
> for other clients and the `mcp-remote` bridge.

> **No Docker?** The server is published to
> [PyPI](https://pypi.org/p/mcp-hello-server) as `mcp-hello-server`, so you can
> run it straight from Python:
> ```sh
> uvx mcp-hello-server                    # run over stdio, no install
> # or install it as a tool / into a venv:
> pipx install mcp-hello-server           # then: mcp-hello-server
> claude mcp add hello -- uvx mcp-hello-server
> ```

* * *

## Tools

| Tool                        | Purpose                                                        |
| --------------------------- | ------------------------------------------------------------- |
| `server_info()`             | Health/status: app name, version, uptime, supported languages |
| `greet(language?, name?)`   | Greeting in `language` (default English); optional `name`     |

### `greet`

`greet` takes two optional arguments:

- **`language`** — a language name, an alternate spelling, or an ISO code
  (case-insensitive). Omit it to default to English. Supported: `english`,
  `spanish`, `french`, `german`, `italian`, `portuguese`, `japanese`,
  `hawaiian` (e.g. `french`, `Français`, or `fr` all work).
- **`name`** — optional; personalizes the message (`Bonjour, Alice!`).

It returns `{ language, greeting, message }`:

```jsonc
// greet(language="french")
{ "language": "french", "greeting": "Bonjour", "message": "Bonjour!" }

// greet(language="spanish", name="Alice")
{ "language": "spanish", "greeting": "Hola", "message": "Hola, Alice!" }

// greet()  -> { "language": "english", "greeting": "Hello", "message": "Hello!" }
```

An unknown language returns an error listing the supported set.

### Add a language

Add a row to `GREETINGS` in `src/mcp_hello_server/greetings.py` (and, optionally,
an alias / ISO code in `_ALIASES`). `server_info` reports the supported set
automatically.

* * *

## Quick start

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```sh
make install     # create .venv and sync deps
make test        # run the test suite
make run         # run the server over stdio
```

`make help` lists every target.

* * *

## Running the server

### stdio (default — for MCP clients that launch the server)

```sh
uv run mcp-hello-server
# or
make run
```

### Streamable HTTP (for networked clients / containers)

```sh
make run-http            # PORT defaults to 8000
PORT=9000 make run-http
```

### Inspect the server

```sh
make inspect             # print a summary: name, version, tool count
make dev                 # launch the interactive FastMCP Inspector (web UI)
```

* * *

## Configuration

All configuration is via environment variables:

| Variable        | Default            | Purpose                                    |
| --------------- | ------------------ | ------------------------------------------ |
| `APP_NAME`      | `mcp-hello-server` | Name reported by `server_info`             |
| `MCP_TRANSPORT` | `stdio`            | `stdio`, `http`, or `sse`                  |
| `HOST`          | `127.0.0.1`        | Bind address for `http`/`sse`              |
| `PORT`          | `8000`             | Bind port for `http`/`sse`                 |

* * *

## Using with an MCP client — local development (from source)

Point a stdio-based client (e.g. Claude Desktop, Claude Code) at the console
script. Example `claude_desktop_config.json` entry using uv:

```jsonc
{
  "mcpServers": {
    "hello": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/mcp-hello-server", "mcp-hello-server"]
    }
  }
}
```

With Claude Code:

```sh
claude mcp add hello -- uv run --directory "$PWD" mcp-hello-server
```

Confirm it's connected with `claude mcp list` (or `/mcp` inside a session).

### Example prompts (Claude Code)

Once the server is added, just ask in plain language — Claude picks the right
tool. The tool it invokes is shown in parentheses.

- "Is the hello server up? What version is it?" → (`server_info`)
- "Greet me." → (`greet`, defaults to English → "Hello!")
- "Greet in French." → (`greet` with `language="french"` → "Bonjour!")
- "Say hello in Japanese to Alice." → (`greet` with `language="japanese"`, `name="Alice"`)
- "What languages can you greet in?" → (`server_info`, then read `languages`)

* * *

## Using a published image or a remote server

**This section is for consumers who are not building from source** — you have the
published Docker image, or someone has deployed the server for you.

### Option A — Docker image, client launches it (stdio)

The client starts a fresh container per session and talks to it over stdio. Use
`-i` (keep stdin open) and force the stdio transport, since the image defaults to
HTTP. The image is published to two registries, so pick one:

```jsonc
// GitHub Container Registry (GHCR)
{
  "mcpServers": {
    "hello": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "MCP_TRANSPORT=stdio",
               "ghcr.io/mitchallen/mcp-hello-server:latest"]
    }
  }
}
```

```jsonc
// Docker Hub
{
  "mcpServers": {
    "hello": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "MCP_TRANSPORT=stdio",
               "mitchallen/mcp-hello-server:latest"]
    }
  }
}
```

Claude Code equivalent — again, pick a registry:

```sh
# GitHub Container Registry (GHCR)
claude mcp add hello -- docker run -i --rm -e MCP_TRANSPORT=stdio ghcr.io/mitchallen/mcp-hello-server:latest

# Docker Hub
claude mcp add hello -- docker run -i --rm -e MCP_TRANSPORT=stdio mitchallen/mcp-hello-server:latest
```

(Pin a version like `:0.1.2` in place of `:latest` for a reproducible setup. Add
`--scope user` to register the server for every project on your machine.)

### Option B — Long-running container over HTTP (local)

Start the container once (it serves HTTP by default) from either registry, then
point an HTTP-capable client at it:

```sh
# GitHub Container Registry (GHCR)
docker run -d --rm -p 8000:8000 --name mcp-hello ghcr.io/mitchallen/mcp-hello-server:latest

# Docker Hub
docker run -d --rm -p 8000:8000 --name mcp-hello mitchallen/mcp-hello-server:latest
```

Claude Code (native HTTP transport):

```sh
claude mcp add --transport http hello http://localhost:8000/mcp
```

For clients that only speak **stdio**, bridge to the HTTP endpoint with
[`mcp-remote`](https://www.npmjs.com/package/mcp-remote):

```jsonc
{
  "mcpServers": {
    "hello": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:8000/mcp"]
    }
  }
}
```

### Option C — Remote deployment (HTTP)

If the server is hosted elsewhere, use its public URL — everything else matches
Option B:

```sh
claude mcp add --transport http hello https://mcp-hello.example.com/mcp
```

Notes for remote use:

- Prefer **HTTPS** so traffic is encrypted in transit.
- This server ships **no authentication**. If you expose it beyond localhost, put
  it behind a reverse proxy, gateway, or network policy — or add
  [FastMCP auth](https://gofastmcp.com/servers/auth/authentication).
- The endpoint path is `/mcp` (no trailing slash). Requesting `/mcp/` works too
  but returns a 307 redirect to `/mcp`.

* * *

## Docker

Published multi-platform (`linux/amd64`, `linux/arm64`) images are available
from two registries:

- **GitHub Container Registry:** `ghcr.io/mitchallen/mcp-hello-server`
- **Docker Hub:** `mitchallen/mcp-hello-server`

The image runs the server over **streamable HTTP** by default (`MCP_TRANSPORT=http`,
`HOST=0.0.0.0`, `PORT=8000`) so it's reachable on a published port.

It's built on a **distroless [Chainguard/Wolfi](https://images.chainguard.dev/directory/image/python/versions)
Python base** — no shell or package manager, runs as a non-root user, and scans
**0 known vulnerabilities**. Every build is gated by a Trivy scan
(fails on fixable CRITICAL/HIGH) and the published `:latest` is re-scanned daily;
see [CI / Publish](#ci--publish).

### Pull and run

```sh
# GitHub Container Registry (GHCR)
docker pull ghcr.io/mitchallen/mcp-hello-server:latest
docker run --rm -p 8000:8000 --name mcp-hello ghcr.io/mitchallen/mcp-hello-server:latest

# Docker Hub
docker pull mitchallen/mcp-hello-server:latest
docker run --rm -p 8000:8000 --name mcp-hello mitchallen/mcp-hello-server:latest
```

Pin a specific release instead of `:latest` for a reproducible setup, e.g.
`ghcr.io/mitchallen/mcp-hello-server:0.1.2`. Then connect an HTTP MCP client to
`http://localhost:8000/mcp`.

### Test a published release with make

Convenience targets pull and run the **published** image in your local Docker
environment — handy for smoke-testing a release without a local build:

```sh
make docker-test               # up + smoke + down in one shot (exits non-zero on failure)

make docker-up                 # pull + run ghcr.io/mitchallen latest, detached
make docker-smoke              # MCP `initialize` handshake — passes if the server responds
make docker-down               # stop it

make docker-up TAG=0.1.2                         # pin a version
make docker-up REGISTRY=docker.io/mitchallen     # pull from Docker Hub instead
make docker-up HTTP_PORT=9000                    # publish on a different host port
```

### Build locally

```sh
make docker-build        # docker build -t mcp-hello-server .
make docker-run          # serves http on localhost:8000
```

* * *

## CI / Publish

Three kinds of GitHub Actions workflows live in `.github/workflows/`:

- **`test`** — runs on every push/PR to `main`: the unit suite
  (`pytest --ignore=tests/test_bdd.py`).
- **`bdd`** — runs the **pytest-bdd** scenarios (`pytest tests/test_bdd.py`) in
  its own workflow so it passes/badges independently of the unit suite.
- **`publish`** / **`publish-dockerhub`** — triggered by pushing a `v*` tag.
  Build a multi-platform image and push it to GHCR and Docker Hub, then run
  `make docker-test` against the just-published image as a post-publish smoke
  check. The Docker Hub job needs `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`
  repository secrets and a pre-created `mitchallen/mcp-hello-server` repo.
- **`publish-pypi`** — also triggered by the `v*` tag (and can be run manually
  via `workflow_dispatch`). Runs the suite on Python 3.11–3.13, then builds and
  uploads the sdist + wheel to [PyPI](https://pypi.org/p/mcp-hello-server) using
  **trusted publishing** (OIDC — no stored token). It needs a matching PyPI
  publisher configured for this repo, workflow `publish-pypi.yml`, and a `pypi`
  GitHub environment.

To cut a release, use the `release` target — it bumps `version` in
`pyproject.toml` (and `uv.lock`), commits, tags, and pushes, which triggers all
three publish workflows (GHCR, Docker Hub, PyPI):

```sh
make release              # patch bump (default)
make release BUMP=minor   # or minor / major
```

The target refuses to run unless the working tree is clean and you're on `main`.

* * *

## Development

- Source: `src/mcp_hello_server/`
  - `greetings.py` — greeting data + language resolution (`greet`)
  - `server.py` — FastMCP tools + entry point (`main`)
- Tests: `tests/`, run with `make test` (`uv run pytest`), driven through an
  in-memory FastMCP client. Layers:
  - `test_greetings.py` — plain pytest unit tests for the resolver/builder.
  - `test_server.py` — the tools through the in-memory client.
  - `test_bdd.py` + `tests/features/*.feature` — a **pytest-bdd** layer.
- `make build` produces a wheel/sdist via `uv build`.
- **Dependencies:** `uv.lock` is committed and the Docker build installs from it
  with `--frozen`. Whenever you change dependencies in `pyproject.toml`, run
  `make lock` (or `uv lock`) to refresh the lockfile and commit it.

* * *

## License

MIT © Mitch Allen
