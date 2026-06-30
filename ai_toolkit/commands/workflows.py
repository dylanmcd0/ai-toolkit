import click


@click.group()
def workflows():
    """Set up and manage multi-agent workflows."""
    pass


@workflows.command()
@click.option("--name", prompt="Workflow name", help="Name of the workflow")
@click.option("--agents", default=2, help="Number of agents in the workflow")
def init(name: str, agents: int):
    """Initialize a new multi-agent workflow."""
    click.echo(f"Initializing workflow '{name}' with {agents} agents...")
    click.echo("(Coming soon)")


@workflows.command()
def list():
    """List available workflows."""
    click.echo("Available workflows:")
    click.echo("(Coming soon)")
