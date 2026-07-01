# AI Toolkit

A personal AI engineering toolkit for repeatable setup, prompt patterns, and small helper tools.

This repo is intentionally **docs-first and modular**. It is not meant to become one large CLI app. Instead, it collects practical building blocks:

- `tools/` — small focused utilities, starting with MCP server configuration helpers.
- `prompts/` — reusable prompts and review rubrics.
- `recipes/` — step-by-step setup guides for workflows and integrations.
- `scripts/` — installers and convenience scripts for local environments.
- `config/` — example configuration files and local config conventions.
- `ai_toolkit/` — existing Python CLI package from the first scaffold; useful pieces can be migrated into `tools/` over time.

## Current Focus

1. Standardize how MCP servers are added and stored.
2. Capture RTK/token-saving setup patterns for Claude and Codex.
3. Document code review workflows and good `CLAUDE.md` practices.
4. Keep everything easy to copy, adapt, and extend.

## Repository Layout

```text
ai-toolkit/
  config/
    mcp-servers.example.json
  prompts/
    code-review-yagni.md
  recipes/
    claude-code-review.md
    claude-md-practices.md
    rtk-token-saving.md
  scripts/
    install-rtk-for-claude.sh
    save-codex-token-context.sh
  tools/
    mcp/
      README.md
      mcp_config.py
  ai_toolkit/
    existing Python CLI package
```

## Quick Start: MCP Config

Create a local MCP config from the example:

```bash
cp config/mcp-servers.example.json config/mcp-servers.local.json
```

Add an MCP server:

```bash
python3 tools/mcp/mcp_config.py add \
  --config config/mcp-servers.local.json \
  --name filesystem \
  --command npx \
  --arg "-y" \
  --arg "@modelcontextprotocol/server-filesystem" \
  --arg "$HOME/Documents"
```

List configured MCP servers:

```bash
python3 tools/mcp/mcp_config.py list --config config/mcp-servers.local.json
```

## Included Starters

- `prompts/code-review-yagni.md` — review prompt focused on YAGNI, correctness, and maintainability.
- `recipes/claude-code-review.md` — practical Claude code review setup notes.
- `recipes/claude-md-practices.md` — guidance and template for repository `CLAUDE.md` files.
- `recipes/rtk-token-saving.md` — token/context-saving workflow outline.
- `scripts/save-codex-token-context.sh` — local context snapshot helper.

## Principles

- Prefer plain Markdown over hidden automation.
- Prefer small scripts over framework-heavy tooling.
- Keep secrets and machine-local paths out of git.
- Make every workflow copy-pastable before making it clever.
- Promote CLI behavior only after the recipe/script has proven useful.
