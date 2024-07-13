# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The CLI entry point. Invoke as `confluence' or `python -m confluence'."""

import os
import signal
import sys

from dotenv import load_dotenv

from .args import parse_args
from .exceptions import Error
from .exporter import export_metadata, export_space


def main() -> int:
    """Entrypoint function to call confluence from the command line.

    :return: An exit code
    :rtype: int
    """
    dotenv_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        load_dotenv()

    args = parse_args()
    retval = int(args is None)

    if args:
        try:
            if args.command == 'export':
                export_space(args.space_key, args.output_dir)
            elif args.command == 'metadata':
                export_metadata(args.space_key, args.output_dir)
        except KeyboardInterrupt:  # the user hit control-C
            sys.stderr.write('Received keyboard interrupt, terminating.\n')
            sys.stderr.flush()
            # Control-C is fatal error signal 2, for more see
            # https://tldp.org/LDP/abs/html/exitcodes.html
            retval = 128 + signal.SIGINT
        except Error as err:
            sys.stderr.write(f'{err}\n')
            retval = 1

    return retval
