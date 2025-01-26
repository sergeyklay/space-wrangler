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

"""Load environment variables from various sources in a specified order."""

from pathlib import Path

from dotenv import load_dotenv


class EnvLoader:
    """Class for loading environment variables in a specified order."""

    @staticmethod
    def load_env_variables() -> None:
        """Load env variables from various sources in order of priority.

        1. Variables from the current console session
        2. Variables from .confluence file in the current working directory
        3. Variables from .confluence file in the user's home directory
        """
        # 1. Load environment variables from the current console session
        # (already loaded by default)

        # 2. Load from .confluence in current working directory
        cwd_confluence = Path.cwd() / '.confluence'
        if cwd_confluence.exists():
            load_dotenv(dotenv_path=cwd_confluence, override=False)
            return  # Stop loading from other sources

        # 3. Load from .confluence in the user's home directory
        home_confluence = Path.home() / '.confluence'
        if home_confluence.exists():
            load_dotenv(dotenv_path=home_confluence, override=False)
