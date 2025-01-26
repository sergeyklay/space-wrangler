# This file is part of the swrangler.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The main entry point for swrangler.

Invoke as ``swrangler`` or ``python -m swrangler``.
"""

import sys

from swrangler.cli import main


def init() -> None:
    """Run swrangler.cli.main() when the file is executed by an interpreter.

    If the file is used as a module, the swrangler.cli.main() function will
    not automatically execute. The sys.exit() function is called with a return
    value of swrangler.cli.main(), as all good UNIX programs do.
    """
    if __name__ == '__main__':
        sys.exit(main())


init()
