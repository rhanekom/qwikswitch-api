# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python wrapper around the QwikSwitch REST API for controlling home automation devices (relays, dimmers) via a Wi-Fi bridge. Published to PyPI as `qwikswitch-api`.

## Commands

```bash
# Run all tests
pytest tests

# Run a single test file
pytest tests/qsapi/test_control_device.py

# Run tests with coverage
pytest --cov=qwikswitchapi tests

# Lint
ruff check --fix --exit-non-zero-on-fix .

# Format
ruff format .

# Run all pre-commit hooks
pre-commit run --all-files

# Build package
python -m build
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

- Ruff is configured with `select = ["ALL"]` (all rules enabled) minus specific exclusions. Test files have relaxed rules for assertions, private member access, and type annotations.
- Pre-commit hooks run pyupgrade, Black, codespell, and Ruff.
- Target Python version for linting is 3.12 (`.ruff.toml`), though `pyproject.toml` specifies `>=3.8` compatibility.

## Git Workflow

- Always commit all changed and untracked files together. Do not make partial commits.
