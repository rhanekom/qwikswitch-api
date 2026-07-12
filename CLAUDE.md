# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python wrapper around the QwikSwitch REST API for controlling home automation devices (relays, dimmers) via a Wi-Fi bridge. Published to PyPI as `qwikswitch-api`.

## Commands

The project uses [uv](https://docs.astral.sh/uv/) for environment and dependency management. Prefix Python tooling with `uv run` so it resolves against the locked environment.

```bash
# Sync the environment (runtime + dev dependency groups) from uv.lock
uv sync

# Run all tests
uv run pytest tests

# Run a single test file
uv run pytest tests/qsapi/test_control_device.py

# Run a single test
uv run pytest tests/qsapi/test_control_device.py::test_generates_keys

# Run tests with coverage
uv run pytest --cov=qwikswitchapi tests

# Lint (with autofix)
uv run ruff check --fix --exit-non-zero-on-fix .

# Format
uv run ruff format .

# Run all pre-commit hooks
uv run pre-commit run --all-files

# Build the package
uv build
```

## Architecture

The package lives in `qwikswitchapi/`. The central class is `QSClient` (`client.py`), which wraps all API operations: key generation/deletion, device control, and device status queries.

### Key patterns

- **Decorator-based cross-cutting concerns**: `QSClient` uses two internal decorators — `@_ensure_authenticated` (auto-generates API keys before authenticated calls) and `@_handle_request_failure` (catches `RequestException` and raises domain exceptions).
- **Entity parsing via `from_resp` classmethods**: Each entity (`ApiKeys`, `ControlResult`, `DeviceStatuses`) has a `from_resp(resp)` classmethod that validates the HTTP response status, checks for error indicators in JSON, and constructs the object.
- **Static utility classes**: `UrlBuilder` constructs API endpoint URLs; `ResponseParser` raises typed exceptions from failed responses.
- **Exception hierarchy**: `QSError` is the base. Subtypes: `QSAuthError`, `QSRequestFailedError`, `QSRequestError`, `QSResponseParseError` (extends `QSRequestError`).

### Testing

Tests use `pytest` with `requests-mock` for HTTP mocking. Shared fixtures in `tests/conftest.py` provide `mock_request`, `mock_api_keys`, `api_client`, and `authenticated_api_client`. Tests are organized per API operation under `tests/qsapi/`.

## Code Quality

- Ruff is configured with `select = ["ALL"]` (all rules enabled) minus specific exclusions in `.ruff.toml`. Test files have relaxed rules for assertions, private member access, and type annotations.
- **Prefer inline suppression over global ignores**: when a specific warning genuinely needs silencing, add an inline `# noqa: <RULE>` (with a short reason) at the offending line rather than adding the rule to the global `ignore` list in `.ruff.toml`. Blanket/per-directory suppression is acceptable only for the `tests/` and `scripts/` directories (via `per-file-ignores`); everywhere else, suppress at the point of use so the exception stays visible and scoped. (Genuine formatter-incompatibility rules — e.g. `COM812`, `ISC001`, `D203`, `D212` — legitimately remain global.)
- Pre-commit hooks (`.pre-commit-config.yaml`) enforce file hygiene, secret/key detection, spell-check, Ruff lint + format, markdown/shell/GitHub-Actions linting, and a dependency vulnerability audit. Ruff (with the `UP` rules) supersedes standalone pyupgrade, and `ruff-format` supersedes Black, so neither runs separately.
- Target Python version for linting is 3.12 (`.ruff.toml`), though `pyproject.toml` specifies `>=3.8` compatibility.

## Working Conventions

- **Never auto-commit or push** — always ask first.
- **Don't branch automatically** — the user handles branching.
- **No self-attribution** — do not add "Authored by / Generated with Claude Code" or `Co-Authored-By` lines to commits, PRs, or any artifact.
- **Commit the complete change set** — when committing, include all changed and new files (`git add -A`). Never make partial commits.
- **Before finalizing a commit, scan for secrets and accidental files** — check the staged diff for credentials/keys and for anything that shouldn't be committed (virtualenvs, config artifacts, scratch files) and stop if found. (`gitleaks` and `detect-private-key` back this up as pre-commit hooks.)
- **Code must be accompanied by tests** — new functionality or behaviour changes must land with corresponding tests. Don't commit production code changes without them; the `pytest` pre-commit hook and CI run the suite on every relevant change.
- **Don't let issues hang** — surface problems proactively; fix low-impact ones directly, ask before fixing high-impact ones. Never bypass failing checks, broken tests, or other issues just to keep going.
- **Research, don't assume** — verify options (including via web search) rather than assuming APIs/libraries behave as described.
- **If something can be caught by a pre-commit hook, add it** — prefer enforcing a rule mechanically over relying on memory.

## Documentation & Source of Truth

- Keep an authoritative design/spec doc and a canonical TODO list; treat them as the source of truth for design decisions and next actions, and keep them current as work lands.
- Record **why** decisions were taken, not just what — so future work doesn't re-litigate settled choices.

## Dependencies

- **Single source of truth**: dependencies live in `pyproject.toml`, pinned by `uv.lock`. There is no `requirements.txt`.
- **Separate runtime from dev/tooling**: runtime dependencies go in `[project.dependencies]`; test, docs, and tooling dependencies go in `[dependency-groups]` (the `dev` group, installed by default via `uv sync`, aggregates the `test` and `docs` groups). Keep each in its designated place — don't mix them.
- When a dependency is added or bumped, run `uv lock` so the lockfile and every consumer (tests, linters, CI) resolve the same versions.
- **Scope vulnerability scanning to code we control**: the `pip-audit` pre-commit hook audits only the runtime dependency tree (`uv export --no-dev`), deliberately excluding the large dev/tooling transitive tree.

## Dev Environment

Setup is split by scope so frequently-run setup stays fast:

- **`.devcontainer/Dockerfile`** — machine-wide, rarely-changing installs baked into the image: system (apt) packages and standalone global binaries (`uv`, `gitleaks`, `actionlint`, `gh`), per-user CLI tooling (Claude Code, MCP Launchpad), and Homebrew plus its brew-managed tools (`lazygit`). Every globally-installed tool's primary install belongs here so it survives rebuilds.
- **`.devcontainer/scripts/setup`** — project- and workspace-specific setup that must run against the mounted source (`uv sync`, `pre-commit install`), invoked as the `postCreateCommand`. It also carries **idempotent ensure-installed fallbacks** for the developer CLIs (`gh`, `lazygit`) that re-install them only if the baked copy is missing; these must stay no-ops when the tools already exist.

The Dockerfile is the source of truth for global tools — never rely on an ad-hoc install that vanishes on the next rebuild. The setup-script fallbacks are a safety net, not the primary install, and must be kept in sync with the Dockerfile (e.g. `GH_VERSION`).

## MCP / External Capabilities

When a task needs a capability outside the current tools, check the MCP gateway first. `mcpl` is a unified CLI for discovering and executing tools across all configured MCP servers.

Always discover before calling — never guess tool names. Search for the tool, inspect its schema, then call it.

```bash
mcpl search "<query>"              # Find tools across all servers (shows required params)
mcpl list <server>                 # List a server's tools
mcpl inspect <server> <tool> --example   # Full schema + ready-to-use example call
mcpl call <server> <tool> '{"param": "value"}'   # Execute a tool
```

## Tooling Baseline

- **Linting/formatting**: run format + lint-with-autofix locally (`uv run ruff format .`, `uv run ruff check --fix`). CI (`.github/workflows/ci.yml`) runs check-only — `uv run pre-commit run --all-files` (no autofix) plus the test suite across the supported Python range (3.8/3.11/3.13). The gitleaks/actionlint binary versions are kept in sync between the Dockerfile, pre-commit config, and CI; the `gh` version (`GH_VERSION`) is kept in sync between the Dockerfile and the setup-script fallback.
- **Pre-commit hooks standardized on** (all active in `.pre-commit-config.yaml`): file hygiene (JSON/YAML/TOML validation, whitespace, line endings, private-key + AWS-credential detection), spell-check (codespell), Ruff lint + format, markdown lint (markdownlint-cli2), shell lint (shellcheck), GitHub Actions lint (actionlint), secret scanning (gitleaks), and a dependency vuln audit (pip-audit, runtime tree only).
- **Testing**: `uv run pytest tests` runs everything; a single file is `uv run pytest tests/qsapi/test_control_device.py`; a single test appends `::test_name`.

## Git Workflow

- Always commit all changed and untracked files together (`git add -A`). Do not make partial commits.
