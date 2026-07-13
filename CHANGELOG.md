# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security

- Automated container image vulnerability scanning with Trivy. The new
  `image-scan` workflow builds the image and fails the build on **fixable**
  CRITICAL/HIGH vulnerabilities on every pull request and push to `main`, and
  the `publish` / `publish-dockerhub` workflows run the same gate **before**
  pushing so a vulnerable image can't reach GHCR or Docker Hub.
- Added a `scan-scheduled` workflow that re-scans the published `:latest` image
  daily and uploads results (all severities, including unfixed) to the GitHub
  Security tab, catching CVEs disclosed after build time.
- Added a Dependabot config (`.github/dependabot.yml`) opening weekly update PRs
  for the Docker base image, GitHub Actions, and Python dependencies, and
  enabled Dependabot alerts + security updates on the repository.

### Changed

- `make scan` now fails on fixable CRITICAL/HIGH vulnerabilities
  (`--severity CRITICAL,HIGH --ignore-unfixed --exit-code 1`), matching the CI
  gate for local parity.

## [0.1.1] - 2026-07-10

### Documentation

- Add a "Quick start — demo an MCP server in 2 minutes" section to the top of
  the README: a client-driven walkthrough (add → verify → ask → remove) using
  the published Docker Hub image, aimed at someone seeing how an MCP client
  discovers and calls tools for the first time, plus an HTTP alternative.

## [0.1.0] - 2026-07-10

### Added

- Initial release: a minimal FastMCP server with two tools —
  - `server_info()` — a health/status check reporting the app name, version,
    uptime, supported greeting languages, and default language.
  - `greet(language?, name?)` — a friendly greeting in one of a handful of
    languages (english, spanish, french, german, italian, portuguese, japanese,
    hawaiian), defaulting to English. Accepts a language name, alternate
    spelling, or ISO code (case-insensitive), and an optional `name` to
    personalize the message.
- CI test/bdd workflows and GHCR + Docker Hub publish workflows.

[unreleased]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/mitchallen/mcp-hello-server/releases/tag/v0.1.0
