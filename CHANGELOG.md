# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.3] - 2026-08-05

### Changed

- **Releases now go through a PR.** `make release` opens a `release/vX.Y.Z` PR
  carrying the version bump and the CHANGELOG section, waits for main's required
  checks, merges it, and only then cuts the tag. It previously committed the bump
  straight to main, which succeeded only because branch protection let admins
  bypass it — so the release commit reached main without running `unit`/`bdd`,
  and the published tag was built from a commit no check had ever seen. The
  target is re-runnable: a stopped run resumes its existing release branch
  instead of bumping the version again.
- `make release` now accepts an uncommitted `CHANGELOG.md`, carrying that edit
  into the release PR so the notes and the version land in one commit.
- `make release` waits for the PR's check runs to register before watching them.
  `gh pr checks --watch` fails immediately with "no checks reported" if it is
  called in the gap between opening the PR and the workflows appearing, which
  aborted the first run of this flow.

### Fixed

- Branch protection on `main` no longer exempts administrators
  (`enforce_admins`), closing the bypass that let release commits skip the
  required checks.
- The Trivy image scan (`scan`) is now a **required** check alongside `unit` and
  `bdd`, so a fixable CRITICAL/HIGH can no longer merge to main — previously it
  only turned main red after the fact, which is how a HIGH-severity cryptography
  CVE sat on the default branch.

## [0.4.2] - 2026-08-05

### Security

- Bumped the transitive `cryptography` dependency from 49.0.0 to 50.0.0, which
  fixes **CVE-2026-69247** (HIGH): PKCS#7 decryption exposed distinguishable
  errors and timing when unwrapping a `RecipientInfo`'s `encryptedKey`, usable
  as a Bleichenbacher oracle. The published image had been failing the
  `image-scan` Trivy gate on this CVE until the bump landed.

### Fixed

- Dependabot never checked this project's Python dependencies. The config
  declared `package-ecosystem: pip`, which does not pick up `uv.lock`, so the
  weekly Python update opened **zero** PRs from the day it was added — every
  Dependabot PR to date had been `github-actions` or `docker`. The one Python
  bump that did land arrived as a *security* alert, which detects the package
  manager itself and ignores the config. Switched the entry to
  `package-ecosystem: uv`.
- `dependabot-auto-merge.yml` matched only the `docker` and `pip` ecosystems, so
  even once uv PRs began arriving they would never auto-merge. Added `uv` to the
  minor/patch auto-merge allowlist (`pip` kept as a fallback). Major bumps still
  stay manual.

### Changed

- `fastmcp` 3.4.4 → 3.4.5 — the first Python dependency PR the weekly schedule
  has ever produced, opened and auto-merged within minutes of the fix above.
- `github/codeql-action` pinned from `4` to `4.37.4`.

## [0.4.1] - 2026-07-15

### Fixed

- README version badges (PyPI, Python versions) could display a stale version or
  "not found" — their images were cached by GitHub's camo proxy at first render,
  before the package existed on PyPI. Appended `cacheSeconds` to the shields.io
  URLs to change the proxy cache key and force a fresh fetch.

### Added

- Note under the badge row explaining that the version badges are cached images
  (shields.io and PyPI's own image proxy) that may briefly lag a fresh release,
  pointing to the release/tag, the PyPI page heading, and the `server_info` tool
  for the authoritative version.

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

[unreleased]: https://github.com/mitchallen/mcp-hello-server/compare/v0.4.3...HEAD
[0.4.3]: https://github.com/mitchallen/mcp-hello-server/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/mitchallen/mcp-hello-server/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/mitchallen/mcp-hello-server/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/mitchallen/mcp-hello-server/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/mitchallen/mcp-hello-server/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/mitchallen/mcp-hello-server/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/mitchallen/mcp-hello-server/releases/tag/v0.1.0
