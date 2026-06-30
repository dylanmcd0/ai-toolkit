import click
import json
import os
from pathlib import Path
from ai_toolkit.utils.mcp_config import MCPConfig


@click.group()
def mcp():
    """Manage MCP server setup and configuration."""
    pass


@mcp.command()
@click.option("--name", prompt="MCP server name", help="Name of the MCP server")
@click.option("--command", prompt="Command to run", help="Command to start the MCP server")
@click.option("--args", default="", help="Arguments to pass to the command")
@click.option("--config-path", default=None, help="Path to Claude Code config (auto-detected if not provided)")
def add(name: str, command: str, args: str, config_path: str):
    """Add a new MCP server configuration."""
    config = MCPConfig(config_path)

    try:
        config.add_server(name, command, args.split() if args else [])
        click.secho(f"✓ MCP server '{name}' added successfully", fg="green")
        click.echo(f"  Command: {command}")
        if args:
            click.echo(f"  Args: {args}")
    except Exception as e:
        click.secho(f"✗ Error adding MCP server: {e}", fg="red")
        raise


@mcp.command()
@click.option("--config-path", default=None, help="Path to Claude Code config")
def list(config_path: str):
    """List all configured MCP servers."""
    config = MCPConfig(config_path)
    servers = config.list_servers()

    if not servers:
        click.echo("No MCP servers configured.")
        return

    click.echo("Configured MCP servers:")
    for name, details in servers.items():
        click.echo(f"  • {name}")
        click.echo(f"    Command: {details.get('command', 'N/A')}")


@mcp.command()
@click.option("--name", prompt="Server name to remove", help="Name of the MCP server")
@click.option("--config-path", default=None, help="Path to Claude Code config")
def remove(name: str, config_path: str):
    """Remove an MCP server configuration."""
    config = MCPConfig(config_path)

    try:
        config.remove_server(name)
        click.secho(f"✓ MCP server '{name}' removed successfully", fg="green")
    except Exception as e:
        click.secho(f"✗ Error removing MCP server: {e}", fg="red")
        raise


@mcp.command()
@click.option("--config-path", default=None, help="Path to Claude Code config")
def validate(config_path: str):
    """Validate MCP server configurations."""
    config = MCPConfig(config_path)

    try:
        is_valid = config.validate()
        if is_valid:
            click.secho("✓ MCP configuration is valid", fg="green")
        else:
            click.secho("✗ MCP configuration has issues", fg="red")
    except Exception as e:
        click.secho(f"✗ Error validating config: {e}", fg="red")
        raise
