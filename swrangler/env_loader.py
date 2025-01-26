# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

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
