# AI Toolkit

This repo is a docs-first set of small AI workflow utilities. The current priority is `tools/mcp`: a small Python CLI for keeping one MCP server registry and installing entries into the clients you actually use.

## Current Shape

- `tools/mcp/` stores the MCP registry CLI and usage notes.
- `config/` holds tracked examples only; your real registry lives in `config/mcp-servers.json`.
- `recipes/`, `prompts/`, and `scripts/` stay as independent building blocks instead of being folded into one package.

## MCP Workflow

Copy the example registry:

```bash
cp config/mcp-servers.example.json config/mcp-servers.json
```

List the servers in your registry:

```bash
python3 tools/mcp/mcp_config.py list
```

Install one into Claude Code:

```bash
python3 tools/mcp/mcp_config.py install filesystem --client claude --scope user
```

Install one into Codex:

```bash
python3 tools/mcp/mcp_config.py install filesystem --client codex
```

Install one into LM Studio:

```bash
python3 tools/mcp/mcp_config.py install filesystem --client lmstudio
```

If you want a console command, install the repo in editable mode:

```bash
pip install -e .
mcp-tool list
```

## Included Pieces

- `tools/mcp/README.md` explains the registry format and client install behavior.
- `docs/mcp-guide.md` is the focused guide for the MCP workflow in this repo.
- `scripts/install-rtk-for-claude.sh` and `scripts/install-rtk-for-codex.sh` stay separate from the MCP tool.
- `recipes/` and `prompts/` remain docs-only until a script proves necessary.

## Principles

- Prefer one small registry over one config file per client.
- Use client-native install commands when they exist.
- Keep secrets and machine-local values out of git.
- Add automation only after the manual workflow is clear.
