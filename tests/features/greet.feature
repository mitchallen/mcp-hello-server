Feature: Greet
  The greet tool returns a friendly greeting in one of a handful of languages,
  defaulting to English.

  Background:
    Given the MCP server is available

  Scenario: Greeting defaults to English
    When the greet tool is called with no language
    Then the "message" property of the result should be "Hello!"

  Scenario: Greeting in French
    When the greet tool is called with language "French"
    Then the "language" property of the result should be "french"
    And the "message" property of the result should be "Bonjour!"

  Scenario: Greeting by ISO code
    When the greet tool is called with language "es"
    Then the "message" property of the result should be "Hola!"

  Scenario: Personalized greeting
    When the greet tool is called with language "italian" and name "Alice"
    Then the "message" property of the result should be "Ciao, Alice!"

  Scenario: Unknown language is rejected
    When the greet tool is called with language "klingon" expecting an error
    Then an unknown-language error should be raised
