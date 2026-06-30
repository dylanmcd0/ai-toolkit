import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class MCPConfig:
    """Manage MCP server configuration for Claude Code and Claude API."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = self._get_config_path(config_path)
        self._ensure_config_exists()

    def _get_config_path(self, provided_path: Optional[str]) -> Path:
        """Get the Claude Code config path."""
        if provided_path:
            return Path(provided_path)

        # Claude Code config location
        claude_code_path = Path.home() / ".claude" / "claude_code" / "settings.json"
        if claude_code_path.exists():
            return claude_code_path

        # Fallback to local .claude/settings.json
        local_path = Path.cwd() / ".claude" / "settings.json"
        if local_path.exists():
            return local_path

        # Default to user's Claude Code settings
        return claude_code_path

    def _ensure_config_exists(self):
        """Ensure the config file and directories exist."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.config_path.exists():
            default_config = {
                "mcpServers": {}
            }
            with open(self.config_path, "w") as f:
                json.dump(default_config, f, indent=2)

    def _load_config(self) -> Dict:
        """Load the current configuration."""
        with open(self.config_path, "r") as f:
            return json.load(f)

    def _save_config(self, config: Dict):
        """Save configuration to file."""
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

    def add_server(self, name: str, command: str, args: Optional[List[str]] = None):
        """Add or update an MCP server configuration."""
        config = self._load_config()

        if "mcpServers" not in config:
            config["mcpServers"] = {}

        config["mcpServers"][name] = {
            "command": command,
            "args": args or []
        }

        self._save_config(config)

    def remove_server(self, name: str):
        """Remove an MCP server configuration."""
        config = self._load_config()

        if "mcpServers" in config and name in config["mcpServers"]:
            del config["mcpServers"][name]
            self._save_config(config)
        else:
            raise KeyError(f"MCP server '{name}' not found in configuration")

    def list_servers(self) -> Dict:
        """List all configured MCP servers."""
        config = self._load_config()
        return config.get("mcpServers", {})

    def validate(self) -> bool:
        """Validate the MCP configuration."""
        try:
            config = self._load_config()
            if "mcpServers" not in config:
                return False
            return isinstance(config["mcpServers"], dict)
        except Exception:
            return False

    def get_config_path(self) -> Path:
        """Get the path to the configuration file."""
        return self.config_path
