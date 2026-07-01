#!/usr/bin/env python3
"""Manage a small MCP server registry and install entries into local clients."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_REGISTRY = Path("config/mcp-servers.json")
DEFAULT_LMSTUDIO_CONFIG = Path.home() / ".lmstudio" / "mcp.json"
SUPPORTED_TRANSPORTS = {"stdio", "http", "sse"}


def parse_key_value_pairs(values: list[str], label: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit(f"{label} must be KEY=VALUE: {value}")
        key, raw_value = value.split("=", 1)
        if not key:
            raise SystemExit(f"{label} key cannot be empty: {value}")
        parsed[key] = raw_value
    return parsed


def default_registry() -> dict[str, Any]:
    return {"version": 1, "servers": {}}


def normalize_registry(data: dict[str, Any], source: Path) -> dict[str, Any]:
    if "servers" in data and isinstance(data["servers"], dict):
        normalized = {"version": data.get("version", 1), "servers": data["servers"]}
        return normalized

    if "mcpServers" in data and isinstance(data["mcpServers"], dict):
        converted: dict[str, Any] = {}
        for name, server in data["mcpServers"].items():
            if not isinstance(server, dict):
                raise SystemExit(f"{source} has invalid server entry for '{name}'.")
            converted[name] = {
                "transport": server.get("transport", "stdio"),
                "command": server.get("command"),
                "args": server.get("args", []),
                "env": server.get("env", {}),
                "headers": server.get("headers", {}),
                "url": server.get("url"),
            }
        return {"version": 1, "servers": converted}

    raise SystemExit(f"{source} must contain a top-level 'servers' object.")


def validate_server(name: str, server: dict[str, Any]) -> None:
    transport = server.get("transport", "stdio")
    if transport not in SUPPORTED_TRANSPORTS:
        raise SystemExit(f"Server '{name}' has unsupported transport '{transport}'.")

    for key in ("args",):
        value = server.get(key, [])
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            raise SystemExit(f"Server '{name}' field '{key}' must be a list of strings.")

    for key in ("env", "headers"):
        value = server.get(key, {})
        if not isinstance(value, dict) or any(
            not isinstance(item_key, str) or not isinstance(item_value, str)
            for item_key, item_value in value.items()
        ):
            raise SystemExit(f"Server '{name}' field '{key}' must be an object of strings.")

    if "description" in server and not isinstance(server["description"], str):
        raise SystemExit(f"Server '{name}' field 'description' must be a string.")

    if "cwd" in server and not isinstance(server["cwd"], str):
        raise SystemExit(f"Server '{name}' field 'cwd' must be a string.")

    if transport == "stdio":
        command = server.get("command")
        if not isinstance(command, str) or not command:
            raise SystemExit(f"Server '{name}' must define a non-empty 'command'.")
    else:
        url = server.get("url")
        if not isinstance(url, str) or not url:
            raise SystemExit(f"Server '{name}' must define a non-empty 'url'.")


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_registry()

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    registry = normalize_registry(data, path)
    for name, server in registry["servers"].items():
        validate_server(name, server)
    return registry


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def get_server(registry: dict[str, Any], name: str) -> dict[str, Any]:
    server = registry["servers"].get(name)
    if server is None:
        raise SystemExit(f"MCP server not found in registry: {name}")
    return server


def build_stdio_server(args: argparse.Namespace) -> dict[str, Any]:
    server = {
        "description": args.description,
        "transport": "stdio",
        "command": args.command,
        "args": args.arg,
        "env": parse_key_value_pairs(args.env, "Environment value"),
        "headers": {},
    }
    if args.cwd:
        server["cwd"] = args.cwd
    return server


def build_network_server(args: argparse.Namespace) -> dict[str, Any]:
    server = {
        "description": args.description,
        "transport": args.transport,
        "url": args.url,
        "args": [],
        "env": parse_key_value_pairs(args.env, "Environment value"),
        "headers": parse_key_value_pairs(args.header, "Header"),
    }
    return server


def add_server(args: argparse.Namespace) -> None:
    registry_path = Path(args.registry)
    registry = load_registry(registry_path)

    if args.transport == "stdio":
        server = build_stdio_server(args)
    else:
        server = build_network_server(args)

    validate_server(args.name, server)
    registry["servers"][args.name] = server
    save_json(registry_path, registry)
    print(f"Saved MCP server '{args.name}' in {registry_path}")


def list_servers(args: argparse.Namespace) -> None:
    registry = load_registry(Path(args.registry))
    servers = registry["servers"]

    if not servers:
        print("No MCP servers in registry.")
        return

    for name in sorted(servers):
        server = servers[name]
        transport = server.get("transport", "stdio")
        location = server.get("command") if transport == "stdio" else server.get("url")
        print(f"{name}: {transport} {location}")


def show_server(args: argparse.Namespace) -> None:
    registry = load_registry(Path(args.registry))
    server = get_server(registry, args.name)
    print(json.dumps(server, indent=2, sort_keys=True))


def remove_server(args: argparse.Namespace) -> None:
    registry_path = Path(args.registry)
    registry = load_registry(registry_path)

    if args.name not in registry["servers"]:
        raise SystemExit(f"MCP server not found in registry: {args.name}")

    del registry["servers"][args.name]
    save_json(registry_path, registry)
    print(f"Removed MCP server '{args.name}' from {registry_path}")


def validate_registry(args: argparse.Namespace) -> None:
    registry = load_registry(Path(args.registry))
    print(f"Registry is valid: {len(registry['servers'])} server(s)")


def run_command(command: list[str], dry_run: bool) -> None:
    print("$ " + " ".join(command))
    if dry_run:
        return

    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def try_remove(command: list[str], dry_run: bool) -> None:
    if dry_run:
        print("$ " + " ".join(command))
        return

    subprocess.run(command, check=False)


def install_codex(name: str, server: dict[str, Any], dry_run: bool) -> None:
    try_remove(["codex", "mcp", "remove", name], dry_run)

    transport = server["transport"]
    add_command = ["codex", "mcp", "add", name]

    if transport == "stdio":
        for key, value in server.get("env", {}).items():
            add_command.extend(["--env", f"{key}={value}"])
        add_command.extend(["--", server["command"], *server.get("args", [])])
        run_command(add_command, dry_run)
        return

    if transport != "http":
        raise SystemExit(f"Codex install only supports stdio or http servers, not '{transport}'.")

    add_command.extend(["--url", server["url"]])
    run_command(add_command, dry_run)


def install_claude(name: str, server: dict[str, Any], scope: str, dry_run: bool) -> None:
    try_remove(["claude", "mcp", "remove", "-s", scope, name], dry_run)

    add_command = ["claude", "mcp", "add", "-s", scope]
    for key, value in server.get("env", {}).items():
        add_command.extend(["-e", f"{key}={value}"])

    transport = server["transport"]
    if transport == "stdio":
        add_command.extend([name, "--", server["command"], *server.get("args", [])])
        run_command(add_command, dry_run)
        return

    add_command.extend(["-t", transport])
    for key, value in server.get("headers", {}).items():
        add_command.extend(["-H", f"{key}: {value}"])
    add_command.extend([name, server["url"]])
    run_command(add_command, dry_run)


def load_lmstudio_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"mcpServers": {}}

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
        data["mcpServers"] = {}
    return data


def install_lmstudio(name: str, server: dict[str, Any], config_path: Path, dry_run: bool) -> None:
    data = load_lmstudio_config(config_path)
    entry: dict[str, Any] = {"env": server.get("env", {})}

    if server["transport"] == "stdio":
        entry["command"] = server["command"]
        entry["args"] = server.get("args", [])
    else:
        entry["transport"] = server["transport"]
        entry["url"] = server["url"]
        if server.get("headers"):
            entry["headers"] = server["headers"]

    data["mcpServers"][name] = entry

    if dry_run:
        print(f"Would update {config_path}")
        print(json.dumps({name: entry}, indent=2, sort_keys=True))
        return

    save_json(config_path, data)
    print(f"Installed '{name}' into {config_path}")


def install_servers(args: argparse.Namespace) -> None:
    registry = load_registry(Path(args.registry))
    names = sorted(registry["servers"]) if args.all else args.name

    if not names:
        raise SystemExit("Provide one or more server names, or use --all.")

    for name in names:
        server = get_server(registry, name)
        if args.client == "codex":
            install_codex(name, server, args.dry_run)
        elif args.client == "claude":
            install_claude(name, server, args.scope, args.dry_run)
        else:
            install_lmstudio(name, server, Path(args.lmstudio_config), args.dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage an MCP registry and install entries into local AI clients.")
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_REGISTRY),
        help=f"Path to the MCP registry JSON. Default: {DEFAULT_REGISTRY}",
    )
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    add_parser = subparsers.add_parser("add", help="Add or replace an MCP server in the registry.")
    add_parser.add_argument("name", help="MCP server name.")
    add_parser.add_argument(
        "--transport",
        choices=sorted(SUPPORTED_TRANSPORTS),
        default="stdio",
        help="Server transport. Default: stdio.",
    )
    add_parser.add_argument("--description", default="", help="Optional short description.")
    add_parser.add_argument("--command", help="Command used to start a stdio server.")
    add_parser.add_argument("--url", help="URL used by an http or sse server.")
    add_parser.add_argument("--arg", action="append", default=[], help="Command argument. Repeat for multiple args.")
    add_parser.add_argument("--env", action="append", default=[], help="Environment variable as KEY=VALUE.")
    add_parser.add_argument("--header", action="append", default=[], help="HTTP header as KEY=VALUE.")
    add_parser.add_argument("--cwd", help="Optional working directory for stdio servers.")
    add_parser.set_defaults(func=add_server)

    list_parser = subparsers.add_parser("list", help="List registry entries.")
    list_parser.set_defaults(func=list_servers)

    show_parser = subparsers.add_parser("show", help="Show one registry entry as JSON.")
    show_parser.add_argument("name", help="MCP server name.")
    show_parser.set_defaults(func=show_server)

    remove_parser = subparsers.add_parser("remove", help="Remove a registry entry.")
    remove_parser.add_argument("name", help="MCP server name.")
    remove_parser.set_defaults(func=remove_server)

    validate_parser = subparsers.add_parser("validate", help="Validate the registry file.")
    validate_parser.set_defaults(func=validate_registry)

    install_parser = subparsers.add_parser("install", help="Install one or more registry entries into a client.")
    install_parser.add_argument("name", nargs="*", help="Registry server names to install.")
    install_parser.add_argument("--all", action="store_true", help="Install every server in the registry.")
    install_parser.add_argument(
        "--client",
        required=True,
        choices=["codex", "claude", "lmstudio"],
        help="Client to install into.",
    )
    install_parser.add_argument(
        "--scope",
        default="local",
        choices=["local", "user", "project"],
        help="Claude scope. Ignored for other clients.",
    )
    install_parser.add_argument(
        "--lmstudio-config",
        default=str(DEFAULT_LMSTUDIO_CONFIG),
        help=f"LM Studio config path. Default: {DEFAULT_LMSTUDIO_CONFIG}",
    )
    install_parser.add_argument("--dry-run", action="store_true", help="Print the planned install without changing anything.")
    install_parser.set_defaults(func=install_servers)

    return parser


def validate_add_arguments(args: argparse.Namespace) -> None:
    if args.command_name != "add":
        return

    if args.transport == "stdio":
        if not args.command:
            raise SystemExit("--command is required for stdio servers.")
        if args.url:
            raise SystemExit("--url is not valid for stdio servers.")
    else:
        if not args.url:
            raise SystemExit("--url is required for http and sse servers.")
        if args.command or args.arg or args.cwd:
            raise SystemExit("--command, --arg, and --cwd are only valid for stdio servers.")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    validate_add_arguments(args)
    args.func(args)


if __name__ == "__main__":
    main()
