"""Greeting data for the demo ``greet`` tool.

Maps a handful of languages to a greeting word. Lookups are case-insensitive
and also accept common alternate spellings / ISO codes (e.g. ``fr`` or
``Français`` for French). Add a language by adding a row to :data:`GREETINGS`
(and, optionally, an alias below).
"""

from __future__ import annotations

# Canonical language name -> greeting word.
GREETINGS: dict[str, str] = {
    "english": "Hello",
    "spanish": "Hola",
    "french": "Bonjour",
    "german": "Hallo",
    "italian": "Ciao",
    "portuguese": "Olá",
    "japanese": "こんにちは (Konnichiwa)",
    "hawaiian": "Aloha",
}

# Language used when the caller doesn't specify one.
DEFAULT_LANGUAGE = "english"

# Alternate spellings / ISO codes -> canonical language name.
_ALIASES: dict[str, str] = {
    "en": "english",
    "es": "spanish",
    "espanol": "spanish",
    "español": "spanish",
    "fr": "french",
    "francais": "french",
    "français": "french",
    "de": "german",
    "deutsch": "german",
    "it": "italian",
    "italiano": "italian",
    "pt": "portuguese",
    "portugues": "portuguese",
    "português": "portuguese",
    "ja": "japanese",
    "jp": "japanese",
    "nihongo": "japanese",
    "haw": "hawaiian",
}

# The languages this server knows how to greet in, in definition order.
LANGUAGES: tuple[str, ...] = tuple(GREETINGS)


def resolve_language(language: str | None) -> str:
    """Return the canonical language name for ``language``.

    Accepts a canonical name, an alias, or an ISO code (case-insensitive). A
    ``None`` or blank value yields the default (English). Raises ``ValueError``
    for an unknown language, listing the supported set.
    """
    if language is None or not language.strip():
        return DEFAULT_LANGUAGE
    key = language.strip().lower()
    if key in GREETINGS:
        return key
    if key in _ALIASES:
        return _ALIASES[key]
    raise ValueError(
        f"unknown language '{language}'; supported: {', '.join(LANGUAGES)}"
    )


def greet(language: str | None = None, name: str | None = None) -> dict[str, str]:
    """Build a greeting record for ``language`` (default English).

    Pass an optional ``name`` to personalize the message (e.g. ``"Bonjour,
    Alice!"``). Returns ``{language, greeting, message}``.
    """
    canonical = resolve_language(language)
    word = GREETINGS[canonical]
    message = f"{word}, {name.strip()}!" if name and name.strip() else f"{word}!"
    return {"language": canonical, "greeting": word, "message": message}
