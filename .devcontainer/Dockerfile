# syntax=docker/dockerfile:1

# Dev container image for qwikswitch-api.
#
# Everything that is machine-wide and changes rarely is baked here so it survives
# rebuilds without re-running on every container create: system packages and
# standalone global binaries (uv, gitleaks, actionlint), plus per-user CLI tooling
# (Claude Code, MCP Launchpad). Project- and workspace-dependent setup that must run
# against the mounted source (uv sync, pre-commit install) lives in scripts/setup,
# which runs as postCreateCommand.
FROM mcr.microsoft.com/devcontainers/python:3.13

# --- System packages (apt) -------------------------------------------------
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ffmpeg \
        libturbojpeg0 \
        libpcap-dev \
        build-essential \
        procps \
        file \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Standalone global binaries (pinned) -----------------------------------

# uv — Python package & dependency manager (official distroless image).
COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /uvx /usr/local/bin/

# gitleaks — secret scanning; used by the gitleaks-system pre-commit hook.
ARG GITLEAKS_VERSION=8.30.1
RUN curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
    | tar -xz -C /usr/local/bin gitleaks \
    && chmod +x /usr/local/bin/gitleaks

# actionlint — GitHub Actions linting; used by the actionlint-system pre-commit hook.
ARG ACTIONLINT_VERSION=1.7.12
RUN curl -fsSL "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz" \
    | tar -xz -C /usr/local/bin actionlint \
    && chmod +x /usr/local/bin/actionlint

# gh — GitHub CLI; used for PR/issue/API operations against GitHub.
ARG GH_VERSION=2.96.0
RUN curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz" \
    | tar -xz -C /usr/local/bin --strip-components=2 "gh_${GH_VERSION}_linux_amd64/bin/gh" \
    && chmod +x /usr/local/bin/gh

# --- Per-user CLI tooling (baked into the vscode user's home) ---------------
USER vscode

# Claude Code CLI (installs to ~/.local/bin).
RUN curl -fsSL https://claude.ai/install.sh | bash

# MCP Launchpad, installed as a uv tool for the vscode user.
RUN uv tool install https://github.com/kenneth-liao/mcp-launchpad.git

# Ensure user-local tool shims (Claude Code, uv tools) are on PATH.
ENV PATH="/home/vscode/.local/bin:${PATH}"

# Convenience alias, baked once so rebuilds don't append duplicate lines.
RUN echo 'alias cl="claude --dangerously-skip-permissions"' | tee -a ~/.bashrc ~/.zshrc

# --- Homebrew (Linux) + brew-managed tooling --------------------------------
# Homebrew must be installed by a non-root user with passwordless sudo; it lands
# in /home/linuxbrew/.linuxbrew, which is baked into the image. NONINTERACTIVE
# skips the installer's prompts so it runs cleanly during the build.
RUN NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Put brew on PATH for interactive shells (baked once) and for subsequent builds.
RUN echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' | tee -a ~/.bashrc ~/.zshrc ~/.profile
ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:${PATH}"

# lazygit — terminal UI for git; installed via Homebrew.
RUN brew install lazygit

USER root
