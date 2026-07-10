"""FastMCP server exposing a health check and a demo greeting tool.

This is a deliberately small MCP server — a good starting point for a new
project or a demo. It exposes two tools:

  * ``server_info`` — health/status of the server.
  * ``greet``       — a friendly greeting in one of a handful of languages,
                      defaulting to English (e.g. "greet in French" -> "Bonjour!").

Environment variables:
  APP_NAME       display name reported by ``server_info`` (default: mcp-hello-server)
  MCP_TRANSPORT  transport for ``main``: stdio (default), http, or sse
  HOST, PORT     bind address for http/sse transports (default: 127.0.0.1:8000)
"""

from __future__ import annotations

import os
import time
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

# Absolute import (not `from .greetings`) so the module also loads when the
# FastMCP CLI (`fastmcp inspect`/`list`/`call`, i.e. `make inspect`) imports this
# file by path rather than as part of the installed package.
from mcp_hello_server.greetings import (
    DEFAULT_LANGUAGE,
    LANGUAGES,
    greet as _greet,
)

APP_NAME = os.environ.get("APP_NAME", "mcp-hello-server")

try:
    APP_VERSION = _pkg_version("mcp-hello-server")
except PackageNotFoundError:  # running from source without an install
    APP_VERSION = "0.0.0"

_START = time.monotonic()


def _uptime_hhmmss() -> str:
    """Server uptime as HH:MM:SS."""
    total = int(time.monotonic() - _START)
    return f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"


mcp = FastMCP(
    name=APP_NAME,
    # Report the package version; without this FastMCP falls back to its own
    # framework version in the MCP handshake / `fastmcp inspect`.
    version=APP_VERSION,
    instructions=(
        "A minimal demo MCP server. Use server_info for a health/status check, "
        "and greet to get a friendly greeting in a given language (english, "
        "spanish, french, german, italian, portuguese, japanese, or hawaiian; "
        "defaults to english). For example, 'greet in French' returns 'Bonjour!'."
    ),
)


@mcp.tool
def server_info() -> dict[str, Any]:
    """Health/status of the server."""
    return {
        "status": "OK",
        "app": APP_NAME,
        "version": APP_VERSION,
        "uptime": _uptime_hhmmss(),
        "languages": list(LANGUAGES),
        "default_language": DEFAULT_LANGUAGE,
        "source": "https://github.com/mitchallen/mcp-hello-server",
        "author": "Mitch Allen (https://mitchallen.com)",
    }


@mcp.tool
def greet(language: str | None = None, name: str | None = None) -> dict[str, str]:
    """Return a friendly greeting in the requested language (default English).

    ``language`` accepts a language name, an alternate spelling, or an ISO code
    (case-insensitive) — e.g. "french", "Français", or "fr". Supported
    languages: english, spanish, french, german, italian, portuguese, japanese,
    hawaiian. Pass an optional ``name`` to personalize the message (e.g.
    "Bonjour, Alice!"). Returns ``{language, greeting, message}``.
    """
    try:
        return _greet(language=language, name=name)
    except ValueError as exc:  # unknown language -> surface as a client error
        raise ToolError(str(exc)) from exc


def main() -> None:
    """Console-script entry point. Honors MCP_TRANSPORT / HOST / PORT."""
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport in ("http", "sse"):
        mcp.run(
            transport=transport,
            host=os.environ.get("HOST", "127.0.0.1"),
            port=int(os.environ.get("PORT", "8000")),
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
