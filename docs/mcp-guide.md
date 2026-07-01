# MCP Guide

This repo does not treat MCP config as a one-off edit inside each client anymore. The workflow is:

1. Keep your server definitions in one registry file.
2. Install from that registry into Codex, Claude Code, or LM Studio.
3. Let each client keep its own native config format.

## Registry First

The tracked example lives at `config/mcp-servers.example.json`. Your working file should be `config/mcp-servers.json`.

Registry shape:

```json
{
  "version": 1,
  "servers": {
    "filesystem": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
      "env": {}
    }
  }
}
```

Use the CLI directly:

```bash
python3 tools/mcp/mcp_config.py list
python3 tools/mcp/mcp_config.py show filesystem
python3 tools/mcp/mcp_config.py validate
```

Add a server to the registry:

```bash
python3 tools/mcp/mcp_config.py add filesystem \
  --command npx \
  --arg=-y \
  --arg=@modelcontextprotocol/server-filesystem \
  --arg=/Users/you/Documents
```

## Install Targets

The installer is intentionally client-specific:

- `codex`: calls `codex mcp add` and `codex mcp remove`
- `claude`: calls `claude mcp add` and `claude mcp remove`
- `lmstudio`: updates `~/.lmstudio/mcp.json` directly

Examples:

```bash
python3 tools/mcp/mcp_config.py install filesystem --client codex
python3 tools/mcp/mcp_config.py install filesystem --client claude --scope user
python3 tools/mcp/mcp_config.py install filesystem --client lmstudio
python3 tools/mcp/mcp_config.py install --all --client claude --scope project
```

Use `--dry-run` first if you want to inspect the generated install command or JSON change:

```bash
python3 tools/mcp/mcp_config.py install filesystem --client codex --dry-run
```

## Why This Shape

The original scaffold mixed two different ideas:

- a reusable server registry
- a generic all-in-one AI toolkit package

That made the MCP part harder to evolve. The new shape keeps the useful piece only: one small registry CLI under `tools/mcp`.

## Client Notes

- `codex` stores MCP servers in `~/.codex/config.toml` under `mcp_servers`.
- `claude` can manage MCP servers through `claude mcp ...`, with scope support.
- `lmstudio` keeps MCP definitions in `~/.lmstudio/mcp.json`.

## Next Step

Once the registry format settles, the next useful additions are presets and export helpers. Until then, keep the file explicit and small.
