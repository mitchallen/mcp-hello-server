"""Unit tests for the greeting resolver and builder."""

from __future__ import annotations

import pytest

from mcp_hello_server.greetings import (
    DEFAULT_LANGUAGE,
    GREETINGS,
    greet,
    resolve_language,
)


def test_default_language_is_english():
    assert DEFAULT_LANGUAGE == "english"
    assert resolve_language(None) == "english"
    assert resolve_language("") == "english"
    assert resolve_language("   ") == "english"


def test_resolve_is_case_insensitive():
    assert resolve_language("French") == "french"
    assert resolve_language("  SPANISH  ") == "spanish"


@pytest.mark.parametrize(
    ("value", "expected"),
    [("fr", "french"), ("es", "spanish"), ("jp", "japanese"), ("Français", "french")],
)
def test_resolve_accepts_aliases_and_codes(value, expected):
    assert resolve_language(value) == expected


def test_resolve_unknown_language_raises():
    with pytest.raises(ValueError) as exc:
        resolve_language("klingon")
    # The error lists the supported languages so a caller can recover.
    assert "supported" in str(exc.value)
    assert "english" in str(exc.value)


def test_greet_defaults_to_english():
    result = greet()
    assert result["language"] == "english"
    assert result["greeting"] == "Hello"
    assert result["message"] == "Hello!"


def test_greet_in_french():
    result = greet("French")
    assert result["language"] == "french"
    assert result["greeting"] == GREETINGS["french"]
    assert result["message"] == "Bonjour!"


def test_greet_personalized():
    result = greet("french", name="Alice")
    assert result["message"] == "Bonjour, Alice!"
