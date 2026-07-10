"""Tests for the MCP tool layer, driven through an in-memory FastMCP client."""

from __future__ import annotations

import asyncio

from fastmcp import Client

from mcp_hello_server import server


def _call(tool: str, **args):
    """Invoke a tool through an in-memory client and return its structured data."""

    async def run():
        async with Client(server.mcp) as client:
            result = await client.call_tool(tool, args)
            return result.data

    return asyncio.run(run())


def test_tools_are_registered():
    async def run():
        async with Client(server.mcp) as client:
            return {t.name for t in await client.list_tools()}

    names = asyncio.run(run())
    assert names == {"server_info", "greet"}


def test_server_info():
    info = _call("server_info")
    assert info["status"] == "OK"
    assert info["app"] == server.APP_NAME
    assert "english" in info["languages"]
    assert info["default_language"] == "english"
    assert info["source"] == "https://github.com/mitchallen/mcp-hello-server"
    assert info["author"] == "Mitch Allen (https://mitchallen.com)"


def test_greet_defaults_to_english():
    result = _call("greet")
    assert result["language"] == "english"
    assert result["message"] == "Hello!"


def test_greet_in_french():
    result = _call("greet", language="French")
    assert result["language"] == "french"
    assert result["message"] == "Bonjour!"


def test_greet_personalized():
    result = _call("greet", language="spanish", name="Alice")
    assert result["language"] == "spanish"
    assert result["message"] == "Hola, Alice!"


def test_greet_unknown_language_errors():
    try:
        _call("greet", language="klingon")
    except Exception as exc:  # ToolError surfaces as a client-side error
        assert "unknown language" in str(exc)
        return
    raise AssertionError("expected an unknown-language error")
