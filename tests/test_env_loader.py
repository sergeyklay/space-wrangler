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

import os
from pathlib import Path
from unittest import mock

from swrangler.env_loader import EnvLoader


def test_load_from_current_console_session(monkeypatch):
    """Test loading variables from the current console session."""

    with mock.patch.dict(
        os.environ,
        {
            "CONFLUENCE_API_USER": "session_user",
            "CONFLUENCE_API_TOKEN": "session_token",
        },
        clear=True,
    ):
        EnvLoader.load_env_variables()

        assert os.getenv("CONFLUENCE_API_USER") == "session_user"
        assert os.getenv("CONFLUENCE_API_TOKEN") == "session_token"


def test_load_from_cwd_confluence(tmpdir, monkeypatch):
    """Test loading variables from .confluence in current working directory."""

    cwd_confluence = tmpdir.join(".confluence")
    credentials = (
        "CONFLUENCE_API_USER=cwd_confluence_user\n"
        "CONFLUENCE_API_TOKEN=cwd_confluence_token\n"
    )
    cwd_confluence.write(credentials)

    monkeypatch.setattr(Path, "cwd", lambda: Path(tmpdir))

    with mock.patch.dict(os.environ, {}, clear=True):
        EnvLoader.load_env_variables()

        assert os.getenv("CONFLUENCE_API_USER") == "cwd_confluence_user"
        assert os.getenv("CONFLUENCE_API_TOKEN") == "cwd_confluence_token"


def test_load_from_home_confluence_as_last_resort(tmpdir, monkeypatch):
    """Test loading variables from .confluence in home directory."""

    home = tmpdir.mkdir("home")
    home_confluence = home.join(".confluence")
    credentials = (
        "CONFLUENCE_API_USER=home_confluence_user\n"
        "CONFLUENCE_API_TOKEN=home_confluence_token\n"
    )
    home_confluence.write(credentials)

    monkeypatch.setattr(Path, "home", lambda: Path(tmpdir) / "home")
    monkeypatch.setattr(Path, "cwd", lambda: Path(tmpdir) / "empty")

    with mock.patch.dict(os.environ, {}, clear=True):
        EnvLoader.load_env_variables()

        assert os.getenv("CONFLUENCE_API_USER") == "home_confluence_user"
        assert os.getenv("CONFLUENCE_API_TOKEN") == "home_confluence_token"


def test_priority_of_env_loading(tmpdir, monkeypatch):
    """Test the priority of loading environment variables."""

    # Setting up all potential sources
    cwd_confluence = tmpdir.join(".confluence")
    cwd_confluence.write(
        "CONFLUENCE_API_USER=cwd_confluence_user\n"
        "CONFLUENCE_API_TOKEN=cwd_confluence_token"
    )

    home_confluence = tmpdir.mkdir("home").join(".confluence")
    home_confluence.write(
        "CONFLUENCE_API_USER=home_confluence_user\n"
        "CONFLUENCE_API_TOKEN=home_confluence_token"
    )

    # Mock paths
    monkeypatch.setattr(Path, "cwd", lambda: Path(tmpdir))
    monkeypatch.setattr(Path, "home", lambda: Path(tmpdir) / "home")

    # Mock environment to test priority
    with mock.patch.dict(
        os.environ,
        {
            "CONFLUENCE_API_USER": "session_user",
            "CONFLUENCE_API_TOKEN": "session_token",
        },
        clear=True,
    ):
        EnvLoader.load_env_variables()

        # Verify that session variables have the highest priority
        assert os.getenv("CONFLUENCE_API_USER") == "session_user"
        assert os.getenv("CONFLUENCE_API_TOKEN") == "session_token"

        # Clear session variables to test next priority
        os.environ.clear()
        EnvLoader.load_env_variables()

        # Verify that cwd .confluence variables are loaded next
        assert os.getenv("CONFLUENCE_API_USER") == "cwd_confluence_user"
        assert os.getenv("CONFLUENCE_API_TOKEN") == "cwd_confluence_token"

        # Remove cwd .confluence to test home .confluence
        cwd_confluence.remove()
        os.environ.clear()
        EnvLoader.load_env_variables()

        # Verify that home .confluence variables are loaded as last resort
        assert os.getenv("CONFLUENCE_API_USER") == "home_confluence_user"
        assert os.getenv("CONFLUENCE_API_TOKEN") == "home_confluence_token"
