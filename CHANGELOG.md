# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-07-15

### Added

- **Published to PyPI** as
  [`mcp-hello-server`](https://pypi.org/project/mcp-hello-server/) — run it with
  no Docker and no clone via `uvx mcp-hello-server`, or install it with
  `pipx install mcp-hello-server` / `pip install mcp-hello-server`.
- `publish-pypi` GitHub Actions workflow: tests on Python 3.11–3.13, then builds
  and uploads the sdist + wheel via **trusted publishing** (OIDC, no stored
  token). It fires on the same `v*` tag as the GHCR / Docker Hub publishes, so a
  single `make release` fans out to all three registries.
- `LICENSE` file (MIT) — now shipped inside both the sdist and the wheel.
- Trove `classifiers` and an `Issues` project URL in the package metadata.

### Changed

- README reworked to be **dual-runtime**: the PyPI/`uvx` path and the Docker path
  are presented as equal first-class options (badges, intro, and quick start),
  rather than leading with Docker — so PyPI visitors aren't steered into a
  container they don't need.
- The sdist now ships a lean source/tests/metadata allowlist (108 KB → 12 KB),
  excluding local tooling (`.claude/`, `CLAUDE.md`) and the Docker/CI files that
  the previous build leaked.

## [0.3.0] - 2026-07-13

### Changed

- `make release` now verifies that `CHANGELOG.md` has a `## [X.Y.Z]` section for
  the version being released **before** it bumps, tags, or pushes anything. The
  target version is computed with `uv version --dry-run` (no mutation), and the
  release aborts early with a helpful message if the entry is missing — so a
  release can no longer be cut with empty auto-generated GitHub Release notes.

## [0.2.0] - 2026-07-13

### Changed

- `make release` now creates the matching **GitHub Release** automatically
  (`gh release create`) after pushing the tag, using that version's
  `CHANGELOG.md` section as the release notes (extracted with `awk`).
  Previously the target only pushed the tag, so the Releases page drifted
  behind the tags and published images — `v0.1.2` had a tag and images but no
  Release object until it was created after the fact.

### Documentation

- Refreshed the Docker badges and image pull instructions in the README.

## [0.1.2] - 2026-07-13

### Changed

- Switched the Docker base image from `python:3.12-slim-bookworm` (Debian) to a
  distroless **Chainguard/Wolfi** Python base (`cgr.dev/chainguard/python`). The
  Debian base carried 4 CRITICAL + 17 HIGH OS-package CVEs with **no upstream
  fix available** (perl, zlib, sqlite, util-linux, ncurses); the Wolfi image
  ships those packages away entirely and scans **0 vulnerabilities at every
  severity**. The venv is built on the matching `-dev` image so its interpreter
  resolves at runtime; the runtime is smaller (231 MB vs 341 MB) and still runs
  as a non-root user. The previous `apt-get upgrade` and `useradd` steps are
  gone (no package manager / already non-root).
- `make scan` now fails on fixable CRITICAL/HIGH vulnerabilities
  (`--severity CRITICAL,HIGH --ignore-unfixed --exit-code 1`), matching the CI
  gate for local parity.

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

[unreleased]: https://github.com/mitchallen/mcp-hello-server/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/mitchallen/mcp-hello-server/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/mitchallen/mcp-hello-server/releases/tag/v0.1.0
