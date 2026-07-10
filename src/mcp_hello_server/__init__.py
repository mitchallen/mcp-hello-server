"""mcp-hello-server — a minimal MCP server for demos and scaffolding.

Exposes two tools: ``server_info`` (a health/status check) and ``greet`` (a
friendly greeting in one of a handful of languages, defaulting to English).
"""

from .greetings import GREETINGS, LANGUAGES, greet, resolve_language

__all__ = ["GREETINGS", "LANGUAGES", "greet", "resolve_language"]
