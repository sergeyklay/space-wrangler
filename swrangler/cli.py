# Copyright (C) 2024-2025 Serghei Iakovlev <gnu@serghei.pl>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

"""The CLI entry point. Invoke as `swrangler' or `python -m swrangler'."""

import logging
import signal

import click

from swrangler.env_loader import EnvLoader
from .exceptions import Error


def main() -> int:
    """Entrypoint function to call confluence from the command line.

    Returns:
        int: An exit code
    """
    # Load environment variables early in the main function to ensure all
    # subsequent imports and operations have access to these variables.
    EnvLoader.load_env_variables()

    try:
        from .commands import app
        # pylint: disable=no-value-for-parameter
        retval = app(standalone_mode=False)
    except click.exceptions.Abort:  # The user hit control-C
        message = 'Received keyboard interrupt, terminating.'
        logging.getLogger('swrangler').error(message)
        # Control-C is fatal error signal 2, for more see
        # https://tldp.org/LDP/abs/html/exitcodes.html
        retval = 128 + signal.SIGINT
    except click.exceptions.ClickException as click_err:  # Handle click errors
        message = click_err.format_message()
        logging.getLogger('swrangler').error(message)
        retval = click_err.exit_code
    except Error as err:  # Handle custom application errors
        logging.getLogger('swrangler').error(str(err))
        retval = 1

    return retval
