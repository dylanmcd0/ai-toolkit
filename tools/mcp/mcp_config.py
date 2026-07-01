#!/usr/bin/env python3
"""Manage simple MCP server JSON config files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"mcpServers": {}}

    with path.open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)

    if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
        raise SystemExit(f"{path} must contain an object named 'mcpServers'.")

    return data


def save_config(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as config_file:
        json.dump(data, config_file, indent=2)
        config_file.write("\n")


def parse_env(values: list[str]) -> dict[str, str]:
    env: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Environment value must be KEY=VALUE: {value}")
        key, env_value = value.split("=", 1)
        if not key:
            raise SystemExit(f"Environment key cannot be empty: {value}")
        env[key] = env_value
    return env


def add_server(args: argparse.Namespace) -> None:
    path = Path(args.config)
    data = load_config(path)
    data["mcpServers"][args.name] = {
        "command": args.command,
        "args": args.arg,
        "env": parse_env(args.env),
    }
    save_config(path, data)
    print(f"Added MCP server '{args.name}' to {path}")


def list_servers(args: argparse.Namespace) -> None:
    path = Path(args.config)
    data = load_config(path)
    servers = data["mcpServers"]

    if not servers:
        print("No MCP servers configured.")
        return

    for name, server in sorted(servers.items()):
        command = server.get("command", "")
        server_args = " ".join(server.get("args", []))
        print(f"{name}: {command} {server_args}".rstrip())


def remove_server(args: argparse.Namespace) -> None:
    path = Path(args.config)
    data = load_config(path)

    if args.name not in data["mcpServers"]:
        raise SystemExit(f"MCP server not found: {args.name}")

    del data["mcpServers"][args.name]
    save_config(path, data)
    print(f"Removed MCP server '{args.name}' from {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage MCP server config files.")
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    add_parser = subparsers.add_parser("add", help="Add or replace an MCP server.")
    add_parser.add_argument("--config", required=True, help="Path to MCP config JSON.")
    add_parser.add_argument("--name", required=True, help="MCP server name.")
    add_parser.add_argument("--command", required=True, help="Command used to start the server.")
    add_parser.add_argument("--arg", action="append", default=[], help="Command argument. Repeat for multiple args.")
    add_parser.add_argument("--env", action="append", default=[], help="Environment variable as KEY=VALUE. Repeat as needed.")
    add_parser.set_defaults(func=add_server)

    list_parser = subparsers.add_parser("list", help="List MCP servers.")
    list_parser.add_argument("--config", required=True, help="Path to MCP config JSON.")
    list_parser.set_defaults(func=list_servers)

    remove_parser = subparsers.add_parser("remove", help="Remove an MCP server.")
    remove_parser.add_argument("--config", required=True, help="Path to MCP config JSON.")
    remove_parser.add_argument("--name", required=True, help="MCP server name.")
    remove_parser.set_defaults(func=remove_server)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
