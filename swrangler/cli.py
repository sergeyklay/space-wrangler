# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

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
