# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The CLI entry point. Invoke as `confluence' or `python -m confluence'."""

import logging
import signal

import click
from dotenv import find_dotenv, load_dotenv

from .exceptions import Error


def load_env_variables() -> None:
    """Load environment variables from .env file if it exists.

    This function uses `find_dotenv` to locate the .env file. If the .env file
    is found, it loads the environment variables from this file into the
    environment. If the .env file is not found, it will load any existing
    environment variables. Using `usecwd=True` ensures that the search for
    the .env file starts from the current working directory.
    """
    # Use find_dotenv to locate the .env file, ensuring it is found
    # in the current working directory.
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        # Load environment variables from the found .env file.
        load_dotenv(dotenv_path)
    else:
        # Fallback: load environment variables from
        # the default .env file location.
        load_dotenv()


def main() -> int:
    """Entrypoint function to call confluence from the command line.

    Returns:
        int: An exit code
    """
    # Load environment variables early in the main function to ensure all
    # subsequent imports and operations have access to these variables.
    load_env_variables()

    try:
        from .commands import app
        # pylint: disable=no-value-for-parameter
        retval = app(standalone_mode=False)
    except click.exceptions.Abort:  # The user hit control-C
        message = 'Received keyboard interrupt, terminating.'
        logging.getLogger('confluence').error(message)
        # Control-C is fatal error signal 2, for more see
        # https://tldp.org/LDP/abs/html/exitcodes.html
        retval = 128 + signal.SIGINT
    except click.exceptions.ClickException as click_err:  # Handle click errors
        message = click_err.format_message()
        logging.getLogger('confluence').error(message)
        retval = click_err.exit_code
    except Error as err:  # Handle custom application errors
        logging.getLogger('confluence').error(str(err))
        retval = 1

    return retval
