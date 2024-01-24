import click

from .make_template import make_template
from .remove_trash import remove_trash


@click.group
def cli():
    pass


cli.add_command(make_template)
cli.add_command(remove_trash)

if __name__ == "__main__":
    cli()
