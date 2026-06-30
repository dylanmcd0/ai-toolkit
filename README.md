# AI Toolkit

A Python CLI toolkit for managing AI workflows, MCP server setup, and GitHub Actions automation.

## Features

- **MCP Server Management**: Install and configure MCP servers for Claude Code and Claude API
- **Multi-Agent Workflows**: Set up and manage multi-agent AI systems (coming soon)
- **GitHub Actions**: Automate AI-powered workflows in your repositories (coming soon)

## Installation

Clone the repository and install in development mode:

```bash
cd ai-toolkit
pip install -e .
```

## Usage

### MCP Server Setup

Add a new MCP server:
```bash
ai-toolkit mcp add
```

List configured servers:
```bash
ai-toolkit mcp list
```

Remove a server:
```bash
ai-toolkit mcp remove --name <server-name>
```

Validate your configuration:
```bash
ai-toolkit mcp validate
```

### Multi-Agent Workflows

Initialize a workflow:
```bash
ai-toolkit workflows init --name my-workflow --agents 3
```

### GitHub Actions

Set up PR review automation:
```bash
ai-toolkit github-actions setup-pr-review
```

## Configuration

MCP server configurations are stored in:
- `~/.claude/claude_code/settings.json` (Claude Code default)
- `.claude/settings.json` (Project-specific)

You can also specify a custom path with `--config-path`.

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black .
```

## Learning & Documentation

See the `docs/` folder for guides on:
- How MCP servers work
- Building multi-agent workflows
- AI concepts and best practices
