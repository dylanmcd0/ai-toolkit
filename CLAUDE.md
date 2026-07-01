# CLAUDE.md

## Project Overview

This repository is a personal AI engineering toolkit. It collects small utilities, setup recipes, prompts, and local scripts for working with AI coding tools such as Claude, Codex, MCP servers, GitHub Actions, and token/context-saving workflows.

The repo should remain docs-first and modular. Avoid turning it into one large CLI unless a workflow has already proven useful as a small script or recipe.

## Structure

- `tools/` — focused utilities, such as MCP config helpers.
- `prompts/` — reusable prompts and review rubrics.
- `recipes/` — Markdown setup guides and operational playbooks.
- `scripts/` — convenience scripts for local setup or context capture.
- `config/` — example configuration files; local config should be ignored.
- `ai_toolkit/` — existing Python CLI package from the initial scaffold; migrate useful behavior gradually.
- `docs/` — background/reference notes from earlier exploration.

## Commands

- Run MCP helper: `python3 tools/mcp/mcp_config.py --help`
- List example MCP config: `python3 tools/mcp/mcp_config.py list --config config/mcp-servers.example.json`
- Install legacy package, if needed: `pip install -e .`
- Run legacy tests, if expanded later: `pytest`

## Coding Preferences

- Prefer small, explicit scripts and Markdown recipes over broad abstractions.
- Do not introduce new dependencies unless they remove meaningful complexity.
- Keep secrets, tokens, and machine-local paths out of git.
- Keep examples copy-pastable and easy to adapt.
- Do not delete the legacy CLI package unless explicitly asked; migrate from it incrementally.

## Review Expectations

- Prioritize correctness, maintainability, and practical usability.
- Flag YAGNI abstractions and framework-heavy changes.
- Suggest the smallest useful improvement.
- Ignore formatting-only issues unless no formatter/linter exists.
