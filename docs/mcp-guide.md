# MCP (Model Context Protocol) Guide

## What is MCP?

MCP is a standardized protocol for connecting AI models (especially Claude) to external tools and data sources. It allows Claude to interact with:
- APIs and web services
- File systems and databases
- Custom applications and workflows
- Real-time data sources

## How MCP Works

1. **Server**: A process that provides tools, resources, or information
2. **Client**: Claude Code, Claude API, or other clients that use those tools
3. **Protocol**: Standardized communication via JSON-RPC over stdio or HTTP

## Configuration in Claude Code

MCP servers are configured in Claude Code's `settings.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["-m", "mcp_server_module"]
    }
  }
}
```

The config typically lives at:
- **User level**: `~/.claude/claude_code/settings.json`
- **Project level**: `.claude/settings.json` (optional, overrides user settings)

## Common MCP Servers

### File Operations
- `filesystem` — Read, write, and manage files

### Web & APIs
- `brave-search` — Web search capabilities
- `postgresql` — Database queries
- `slack` — Slack workspace integration

### Development
- `git` — Git repository operations
- `bash` — Shell command execution

## Using ai-toolkit for MCP Setup

Instead of manually editing `settings.json`, use:

```bash
# Add a server
ai-toolkit mcp add --name github --command python --args "-m mcp_server_github"

# List all servers
ai-toolkit mcp list

# Validate configuration
ai-toolkit mcp validate
```

## Building Custom MCP Servers

MCP servers can be built in any language. A minimal Python server:

```python
from mcp.server import Server
from mcp.types import Tool

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "add":
        return str(arguments["a"] + arguments["b"])
```

## Learning Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [Claude API Integration](https://docs.anthropic.com)
- [ai-toolkit README](../README.md)
