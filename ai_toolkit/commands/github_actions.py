import click


@click.group()
def github_actions():
    """Set up GitHub Actions for AI workflows."""
    pass


@github_actions.command()
@click.option("--repo-path", default=".", help="Path to the repository")
def setup_pr_review(repo_path: str):
    """Set up AI-powered PR review GitHub Action."""
    click.echo(f"Setting up PR review action in {repo_path}...")
    click.echo("(Coming soon)")


@github_actions.command()
def list():
    """List available GitHub Actions."""
    click.echo("Available GitHub Actions:")
    click.echo("(Coming soon)")
