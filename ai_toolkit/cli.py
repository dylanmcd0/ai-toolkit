import click
from ai_toolkit.commands import mcp, workflows, github_actions


@click.group()
@click.version_option()
def main():
    """AI Toolkit - CLI for AI workflows, MCP setup, and automation."""
    pass


main.add_command(mcp.mcp)
main.add_command(workflows.workflows)
main.add_command(github_actions.github_actions)


if __name__ == "__main__":
    main()
