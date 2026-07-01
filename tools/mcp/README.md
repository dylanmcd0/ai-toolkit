# MCP Tools

Small utilities for managing Model Context Protocol server configuration.

The goal is to standardize the boring parts:

- where MCP server definitions live
- how new servers are added
- how local machine-specific values stay out of git
- how configs can be copied into Claude, Codex, or other clients

## Config Shape

This toolkit uses the common `mcpServers` object:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2"],
      "env": {
        "OPTIONAL_ENV": "value"
      }
    }
  }
}
```

## Commands

Create or update a local MCP config:

```bash
python3 tools/mcp/mcp_config.py add \
  --config config/mcp-servers.local.json \
  --name server-name \
  --command command-to-run \
  --arg arg1 \
  --arg arg2
```

Add environment variables:

```bash
python3 tools/mcp/mcp_config.py add \
  --config config/mcp-servers.local.json \
  --name github \
  --command npx \
  --arg "-y" \
  --arg "@modelcontextprotocol/server-github" \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=your-token
```

List servers:

```bash
python3 tools/mcp/mcp_config.py list --config config/mcp-servers.local.json
```

Remove a server:

```bash
python3 tools/mcp/mcp_config.py remove --config config/mcp-servers.local.json --name github
```
