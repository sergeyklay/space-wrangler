# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Command line argument parsing methods for confluence."""

import os
import sys
import textwrap as _textwrap
from argparse import ArgumentParser, HelpFormatter, Namespace, SUPPRESS

from . import __copyright__, __version__


class LineBreaksFormatter(HelpFormatter):
    """
    ArgParse help formatter that allows line breaks in the usage messages
    and argument help strings.

    Normally to include newlines in the help output of argparse, you have
    use argparse.RawDescriptionHelpFormatter. However, this means raw text is
    enabled everywhere, and not just for specific help entries where we may
    need it.

    This help formatter allows for you to optional enable/toggle raw text on
    individual menu items by prefixing the help string with 'n|'."""
    def _fill_text(self, text, width, indent) -> str:
        text = self._whitespace_matcher.sub(' ', text).strip()
        paragraphs = text.split('|n ')

        multiline_text = ''

        for paragraph in paragraphs:
            formatted_paragraph = _textwrap.fill(
                paragraph,
                width,
                initial_indent=indent,
                subsequent_indent=indent
            ) + '\n'

            multiline_text = multiline_text + formatted_paragraph

        return multiline_text


def get_version_str() -> str:
    """A helper function to format version info."""
    # pylint: disable=consider-using-f-string
    version = '''
    {prog}s {version}|n
    {copy}.|n
    This is free software; see the source for copying conditions.  There is NO|n
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    '''.format(  # noqa E501
        prog='%(prog)',
        version=__version__,
        copy=__copyright__,
    )
    return version


def parser_add_positionals(parser: ArgumentParser) -> ArgumentParser:
    """Add positional parameters group to a parser."""
    subparsers = parser.add_subparsers(dest='command', title='Commands')

    export_parser = subparsers.add_parser(
        'export',
        help='Export all pages from the specified Confluence space')
    parser_add_export_options(export_parser)

    metadata_parser = subparsers.add_parser(
        'pages-metadata',
        help='Export pages metadata of pages from the specified Confluence space')
    parser_add_metadata_options(metadata_parser)

    return parser


def parser_add_export_options(subparser: ArgumentParser) -> ArgumentParser:
    """Add options for the export command."""
    subparser.add_argument('-s', '--space-key', type=str, required=True,
                           help='Confluence space key to export pages')
    subparser.add_argument('-o', '--output-dir', type=str,
                           default=os.path.join(os.getcwd(), 'output'),
                           help='Directory to save the output files (default: ./output)')
    return subparser


def parser_add_metadata_options(subparser: ArgumentParser) -> ArgumentParser:
    """Add options for the metadata command."""
    subparser.add_argument('-s', '--space-key', type=str, required=True,
                           help='Confluence space key to export metadata')
    subparser.add_argument('-o', '--output-dir', type=str,
                           default=os.path.join(os.getcwd(), 'output'),
                           help='Directory to save the output files (default: ./output)')
    return subparser


def parser_add_options(parser: ArgumentParser) -> ArgumentParser:
    """Add options group to a parser."""
    ogroup = parser.add_argument_group('Options')

    ogroup.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Print this help message and quit')

    ogroup.add_argument('-V', '--version', action='version',
                        help="Print program's version information and quit",
                        version=get_version_str())

    return parser


def parse_args() -> Namespace or None:
    parser = ArgumentParser(
        description='Simple Confluence maintenance tools.',
        usage='%(prog)s [command] [options]',
        formatter_class=LineBreaksFormatter,
        add_help=False,
    )

    parser_add_positionals(parser)
    parser_add_options(parser)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return None

    return parser.parse_args()
