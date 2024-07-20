# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""CLI commands for the Confluence application."""

from typing import Any

import click

from . import __copyright__, __description__, __version__
from .logger import setup_logger

CONTEXT_SETTINGS = {
    'show_default': True,
    'help_option_names': ['-h', '--help'],
}


class ExportCommand(click.core.Command):
    """A custom command class for export-like commands.

    This class adds additional options for specifying the output directory
    and the Confluence space key.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.params.insert(
            0,
            click.core.Option(
                ('-o', '--output-dir',),
                help='Directory to save the data.',
                type=click.Path(),
                default='output',
            )
        )

        self.params.insert(
            0,
            click.core.Option(
                ('-s', '--space-key',),
                help='Confluence space key to work with.',
                required=True,
            )
        )


def get_version_str() -> str:
    """A helper function to format version info.

    Returns:
        str: Formatted version information.
    """
    return (
        f'''\n%(prog)s %(version)s\n{__copyright__}\n'''
        'This is free software; see the source for copying conditions.  '
        'There is NO\nwarranty; not even for MERCHANTABILITY or FITNESS FOR '
        'A PARTICULAR PURPOSE.'
    )


@click.group(
    context_settings=CONTEXT_SETTINGS,
    invoke_without_command=True,
    help=__description__,
)
@click.version_option(
    __version__,
    '-V', '--version',
    message=get_version_str(),
)
@click.option(
    '-q', '--quiet',
    help='Suppress all output except warnings and errors.',
    is_flag=True,
)
@click.option(
    '--silent',
    help='Synonym for --quiet.',
    is_flag=True,
)
@click.pass_context
def app(ctx: click.core.Context, quiet: bool, silent: bool) -> int:
    """The main CLI application entry point.

    Args:
        ctx (click.core.Context): The Click context object.
        quiet (bool): Flag to suppress all output except warnings and errors.
        silent (bool): Synonym for `quiet`.

    Returns:
        int: An exit code
    """
    # Setup logger based on the quiet argument
    setup_logger(quiet or silent)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        return 1
    return 0


@app.command(
    'spaces-metadata',
    short_help='Export metadata of all spaces.',
    help='Export metadata of all Confluence spaces.',
)
@click.option(
    '-o', '--output-dir',
    help='Directory to save the data.',
    type=click.Path(),
    default='output',
)
def spaces_metadata(**kwargs: str) -> None:
    """Export metadata of all spaces."""
    from .space_metadata import export_spaces_metadata
    export_spaces_metadata(kwargs['output_dir'])


@app.command(
    'export-space',
    short_help='Export all pages from the specified space.',
    help='Export all pages from the specified Confluence space.',
    cls=ExportCommand,
)
def export_space_command(**kwargs: str) -> None:
    """Export all pages from the specified space."""
    from .space_exporter import export_space
    export_space(kwargs['space_key'], kwargs['output_dir'])


@app.command(
    'pages-metadata',
    short_help='Export metadata of pages from the specified space.',
    help='Export metadata of pages from the specified Confluence space.',
    cls=ExportCommand,
)
def pages_metadata(**kwargs: str) -> None:
    """Export metadata of pages from the specified space."""
    from .page_metadata import export_pages_metadata
    export_pages_metadata(kwargs['space_key'], kwargs['output_dir'])


@app.command(
    'owners-metadata',
    short_help='Export metadata of owners from the specified space.',
    help='Export metadata of page owners from the specified Confluence space.',
    cls=ExportCommand,
)
def owners_metadata(**kwargs: str) -> None:
    """Export metadata of owners from the specified space."""
    from .owner_metadata import export_owners_metadata
    export_owners_metadata(kwargs['space_key'], kwargs['output_dir'])
