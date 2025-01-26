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
