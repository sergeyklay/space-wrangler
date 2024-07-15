# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The CLI entry point. Invoke as `confluence' or `python -m confluence'."""

import signal

from dotenv import find_dotenv, load_dotenv

from .args import argparse
from .exceptions import Error
from .logger import setup_logger


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

    args = argparse()
    retval = int(args is None)

    # If arguments are provided, process the command
    if args:
        # Setup logger based on the quiet argument
        logger = setup_logger(args.quiet)

        try:
            if args.command == 'export':
                # Import `export_space` function here to ensure environment
                # variables are loaded before any imports that might use them.
                from .space_exporter import export_space
                export_space(args.space_key, args.output_dir)
            elif args.command == 'pages-metadata':
                # Import `export_pages_metadata` function here for the same
                # reason, as described above.
                from .page_metadata import export_pages_metadata
                export_pages_metadata(args.space_key, args.output_dir)
            elif args.command == 'owners-metadata':
                # Import `export_owners_metadata` function here for the same
                # reason, as described above.
                from .owner_metadata import export_owners_metadata
                export_owners_metadata(args.space_key, args.output_dir)
        except KeyboardInterrupt:  # the user hit control-C
            logger.error('Received keyboard interrupt, terminating.')
            # Control-C is fatal error signal 2, for more see
            # https://tldp.org/LDP/abs/html/exitcodes.html
            retval = 128 + signal.SIGINT
        except Error as err:  # Handle custom application errors
            logger.error(str(err))
            retval = 1

    return retval
