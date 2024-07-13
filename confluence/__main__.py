# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The main entry point for confluence.

Invoke as ``confluence`` or ``python -m confluence``.
"""

import sys

from confluence.cli import main


def init() -> None:
    """Run confluence.cli.main() when the file is executed by an interpreter.

    If the file is used as a module, the confluence.cli.main() function will
    not automatically execute. The sys.exit() function is called with a return
    value of confluence.cli.main(), as all good UNIX programs do.
    """
    if __name__ == '__main__':
        sys.exit(main())


init()
