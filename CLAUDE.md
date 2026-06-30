# AI Toolkit Project

## Overview

A learning and tooling repository for AI workflows, MCP server management, and automation utilities. This serves as both a CLI tool and a documentation hub for concepts discovered while researching AI technologies.

## Project Structure

```
ai-toolkit/
├── ai_toolkit/
│   ├── commands/          # CLI command modules
│   │   ├── mcp.py         # MCP server management
│   │   ├── workflows.py   # Multi-agent workflow setup
│   │   └── github_actions.py # GitHub Actions integration
│   ├── utils/             # Shared utilities
│   │   └── mcp_config.py  # MCP configuration handler
│   └── cli.py             # Main CLI entry point
├── docs/                  # Learning materials & guides
├── tests/                 # Test suite
├── pyproject.toml         # Package configuration
└── README.md              # User guide
```

## Core Features

### 1. MCP Server Management (`ai_toolkit/commands/mcp.py`)
- `add` — Add/configure an MCP server
- `list` — Show all configured servers
- `remove` — Remove a server configuration
- `validate` — Validate MCP configuration

**Configuration File**: Reads/writes to Claude Code's `settings.json`, typically at `~/.claude/claude_code/settings.json`

### 2. Multi-Agent Workflows (`ai_toolkit/commands/workflows.py`)
Placeholder for workflow scaffolding and management tools.

### 3. GitHub Actions (`ai_toolkit/commands/github_actions.py`)
Placeholder for GitHub Actions automation (PR review, etc.).

## Development Notes

- **Language**: Python 3.10+
- **CLI Framework**: Click
- **Configuration Format**: JSON (Claude Code compatible)
- **Config Discovery**: Automatically finds Claude Code settings; supports custom paths via `--config-path`

## Next Steps

1. **Test MCP setup** — Verify the `add`, `list`, `remove` commands work
2. **Add more MCP servers** — Build out templates/presets for popular servers
3. **Implement workflows** — Build multi-agent workflow scaffolding
4. **Document learnings** — Add `docs/` with AI/MCP concepts
5. **GitHub Actions** — Create reusable GitHub Actions workflows

## Learning & Documentation

This repo doubles as a learning journal. As you discover new AI concepts, tools, or patterns, document them in `docs/` alongside the tooling:
- `docs/mcp-guide.md` — How MCP works
- `docs/multi-agent-patterns.md` — Common patterns for multi-agent systems
- `docs/ai-concepts.md` — Key concepts and definitions
- etc.

## Useful Commands

```bash
# Install in development mode
pip install -e .

# Test a command
ai-toolkit mcp list

# Format code
black ai_toolkit/

# Run tests
pytest
```
