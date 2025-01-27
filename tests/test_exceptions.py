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

import pytest

from swrangler.exceptions import ConfigurationError


def test_configuration_error_all_missing():
    with pytest.raises(ConfigurationError) as excinfo:
        raise ConfigurationError(None, None, None)
    assert "The following environment variables are not set:" in str(
        excinfo.value
    )
    assert "CONFLUENCE_API_USER" in str(excinfo.value)
    assert "CONFLUENCE_API_TOKEN" in str(excinfo.value)
    assert "CONFLUENCE_DOMAIN" in str(excinfo.value)


def test_configuration_error_user_missing():
    with pytest.raises(ConfigurationError) as excinfo:
        raise ConfigurationError(None, "token", "https://acme.atlassian.net")
    assert "CONFLUENCE_API_USER is not set" in str(excinfo.value)


def test_configuration_error_token_missing():
    with pytest.raises(ConfigurationError) as excinfo:
        raise ConfigurationError("user", None, "https://acme.atlassian.net")
    assert "CONFLUENCE_API_TOKEN is not set" in str(excinfo.value)
