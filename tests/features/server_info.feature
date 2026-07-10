Feature: Server info
  The server_info tool is a health/status check.

  Background:
    Given the MCP server is available

  Scenario: server_info reports a version
    When the server_info tool is called
    Then the result should contain a "version" property

  Scenario: server_info reports status OK
    When the server_info tool is called
    Then the "status" property of the result should be "OK"
