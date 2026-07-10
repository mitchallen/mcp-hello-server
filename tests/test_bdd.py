"""pytest-bdd layer describing the server's behavior in Gherkin.

Scenarios live under ``tests/features/`` and cover the ``server_info`` health
check and the ``greet`` tool (default language, a specific language, a
personalized message, and the unknown-language error). Steps drive the tools
through an in-memory FastMCP client — the same approach as ``test_server.py``.
"""

from __future__ import annotations

import asyncio

import pytest
from fastmcp import Client
from pytest_bdd import given, parsers, scenarios, then, when

from mcp_hello_server import server

# Bind every .feature file under tests/features/.
scenarios("features")


def _call(tool: str, **args):
    """Invoke a tool through an in-memory client and return its structured data."""

    async def run():
        async with Client(server.mcp) as client:
            return (await client.call_tool(tool, args)).data

    return asyncio.run(run())


@pytest.fixture
def context() -> dict:
    return {}


# --- Given -----------------------------------------------------------------


@given("the MCP server is available")
def server_available(context):
    assert server.mcp is not None


# --- When ------------------------------------------------------------------


@when("the server_info tool is called")
def call_server_info(context):
    context["result"] = _call("server_info")


@when("the greet tool is called with no language")
def greet_default(context):
    context["result"] = _call("greet")


@when(parsers.parse('the greet tool is called with language "{language}"'))
def greet_language(context, language):
    context["result"] = _call("greet", language=language)


@when(parsers.parse('the greet tool is called with language "{language}" and name "{name}"'))
def greet_language_and_name(context, language, name):
    context["result"] = _call("greet", language=language, name=name)


@when(parsers.parse('the greet tool is called with language "{language}" expecting an error'))
def greet_expecting_error(context, language):
    try:
        _call("greet", language=language)
    except Exception as exc:  # captured for the assertion in the Then step
        context["error"] = exc


# --- Then ------------------------------------------------------------------


@then(parsers.parse('the result should contain a "{prop}" property'))
def result_contains_property(context, prop):
    result = context["result"]
    assert prop in result
    assert result[prop] not in (None, "")


@then(parsers.parse('the "{prop}" property of the result should be "{value}"'))
def result_property_equals(context, prop, value):
    assert context["result"][prop] == value


@then("an unknown-language error should be raised")
def unknown_language_error_raised(context):
    assert "error" in context, "expected an error to be raised"
    assert "unknown language" in str(context["error"])
