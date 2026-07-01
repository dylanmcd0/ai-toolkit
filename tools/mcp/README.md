# MCP Tools

`tools/mcp/mcp_config.py` is a small registry-first CLI.

It does two jobs only:

1. Keep one JSON registry of the MCP servers you actually use.
2. Install those entries into specific clients.

## Registry File

Default registry path: `config/mcp-servers.json`

Tracked example: `config/mcp-servers.example.json`

Shape:

```json
{
  "version": 1,
  "servers": {
    "server-name": {
      "transport": "stdio",
      "command": "command-to-run",
      "args": ["arg1", "arg2"],
      "env": {
        "OPTIONAL_ENV": "value"
      }
    }
  }
}
```

HTTP-style entries use `url` instead of `command` and `args`. Optional `headers` are supported in the registry for Claude and LM Studio installs.

## Commands

Inspect the registry:

```bash
python3 tools/mcp/mcp_config.py list
python3 tools/mcp/mcp_config.py show github
python3 tools/mcp/mcp_config.py validate
```

Add or update a stdio server:

```bash
python3 tools/mcp/mcp_config.py add github \
  --command docker \
  --arg=run \
  --arg=-i \
  --arg=--rm \
  --arg=-e \
  --arg=GITHUB_PERSONAL_ACCESS_TOKEN \
  --arg=ghcr.io/github/github-mcp-server \
  --env GITHUB_PERSONAL_ACCESS_TOKEN='${GITHUB_PERSONAL_ACCESS_TOKEN}'
```

Install to a client:

```bash
python3 tools/mcp/mcp_config.py install github --client codex
python3 tools/mcp/mcp_config.py install github --client claude --scope user
python3 tools/mcp/mcp_config.py install github --client lmstudio
```

Install every registry entry to a client:

```bash
python3 tools/mcp/mcp_config.py install --all --client claude --scope project
```
