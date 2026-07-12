# syntax=docker/dockerfile:1

# Dev container image for qwikswitch-api.
#
# Everything that is machine-wide and changes rarely is baked here so it survives
# rebuilds without re-running on every container create: system packages,
# standalone global binaries (uv, gitleaks, actionlint, gh), per-user CLI tooling
# (Claude Code, MCP Launchpad), and Homebrew plus its brew-managed tools (lazygit).
# Project- and workspace-dependent setup that must run against the mounted source
# (uv sync, pre-commit install) lives in scripts/setup, which runs as
# postCreateCommand.
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

# Pinned single-binary CLIs installed into /usr/local/bin, merged into one layer
# (S7031: consecutive RUN instructions are merged):
#   gitleaks   — secret scanning (gitleaks-system pre-commit hook)
#   actionlint — GitHub Actions linting (actionlint-system pre-commit hook)
#   gh         — GitHub CLI for PR/issue/API operations
ARG GITLEAKS_VERSION=8.30.1
ARG ACTIONLINT_VERSION=1.7.12
ARG GH_VERSION=2.96.0
RUN curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
        | tar -xz -C /usr/local/bin gitleaks \
    && curl -fsSL "https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz" \
        | tar -xz -C /usr/local/bin actionlint \
    && curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz" \
        | tar -xz -C /usr/local/bin --strip-components=2 "gh_${GH_VERSION}_linux_amd64/bin/gh" \
    && chmod +x /usr/local/bin/gitleaks /usr/local/bin/actionlint /usr/local/bin/gh

# --- Per-user CLI tooling (baked into the vscode user's home) ---------------
USER vscode

# Per-user CLIs, merged into one layer (S7031): Claude Code (installs to
# ~/.local/bin), MCP Launchpad (uv tool), and a convenience alias baked once so
# rebuilds don't append duplicate lines.
RUN curl -fsSL https://claude.ai/install.sh | bash \
    && uv tool install https://github.com/kenneth-liao/mcp-launchpad.git \
    && echo 'alias cl="claude --dangerously-skip-permissions"' | tee -a ~/.bashrc ~/.zshrc

# Ensure user-local tool shims (Claude Code, uv tools) are on PATH.
ENV PATH="/home/vscode/.local/bin:${PATH}"

# --- Homebrew (Linux) + brew-managed tooling --------------------------------
# Homebrew must be installed by a non-root user with passwordless sudo; it lands
# in /home/linuxbrew/.linuxbrew, which is baked into the image. NONINTERACTIVE
# skips the installer's prompts so it runs cleanly during the build.
RUN NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Put brew on PATH for the rest of the build and for every non-interactive
# process (ENV is baked into the image config, so all processes inherit it).
ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:${PATH}"

# lazygit — terminal UI for git; installed via Homebrew.
RUN brew install lazygit

USER root

# Wire Homebrew into interactive/login shells *system-wide*. Build-time edits to
# the per-user ~/.bashrc don't reliably survive container create — a home-dir
# volume or the base image's skel refresh can shadow or regenerate it, which is
# what silently dropped the previous ~/.bashrc brew line. Root-owned system files
# are part of the image and can't be shadowed that way, so brew stays on PATH.
#   /etc/profile.d/homebrew.sh → login shells (sourced via /etc/profile)
#   /etc/bash.bashrc           → interactive non-login bash (the VS Code terminal)
#   /etc/zsh/zshenv            → all zsh shells
# Kept in sync with the equivalent restore block in scripts/setup.
RUN BREW_SHELLENV='eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' \
    && printf '%s\n' "$BREW_SHELLENV" > /etc/profile.d/homebrew.sh \
    && printf '\n# Homebrew\n%s\n' "$BREW_SHELLENV" >> /etc/bash.bashrc \
    && printf '\n# Homebrew\n%s\n' "$BREW_SHELLENV" >> /etc/zsh/zshenv
