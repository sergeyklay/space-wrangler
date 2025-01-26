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

from swrangler.confluence import Confluence, DefaultRetryOptions
from swrangler.exceptions import ConfigurationError


def test_get_all_pages_in_space(mock_response, mocker, confluence):
    mock_get = mocker.patch('atlassian.Confluence.get_space_content')
    mock_get.return_value = mock_response.json()
    pages = confluence.get_all_pages_in_space('TEST')
    assert len(pages) == 1
    assert pages[0]['title'] == 'Test Page'


def test_get_all_pages_in_space_with_next(
        mock_response_with_next,
        mocker,
        confluence,
):
    mock_get = mocker.patch(
        'atlassian.Confluence.get_space_content',
        side_effect=[
            mock_response_with_next[0].json(),
            mock_response_with_next[1].json(),
        ]
    )
    pages = confluence.get_all_pages_in_space('TEST')

    assert mock_get.call_count == 2
    assert len(pages) == 2
    assert pages[0]['title'] == 'Test Page 1'
    assert pages[1]['title'] == 'Test Page 2'


def test_get_all_pages_in_space_with_next_2(
        mock_response_with_next_2,
        mocker,
        confluence
):
    mock_get = mocker.patch(
        'atlassian.Confluence.get_space_content',
        side_effect=[
            mock_response_with_next_2[0].json(),
            mock_response_with_next_2[1].json(),
        ]
    )
    pages = confluence.get_all_pages_in_space('TEST')

    assert mock_get.call_count == 2
    assert len(pages) == 2
    assert pages[0]['title'] == 'Test Page 1'
    assert pages[1]['title'] == 'Test Page 2'
    params = mock_get.call_args_list[1][1]
    assert params['key'] == 'value1,value2'


def test_http_client_initialization_error(monkeypatch):
    monkeypatch.delenv('CONFLUENCE_API_USER', raising=False)
    monkeypatch.delenv('CONFLUENCE_API_TOKEN', raising=False)

    with pytest.raises(ConfigurationError) as excinfo:
        from confluence.confluence import Confluence
        Confluence()
    assert 'Confluence API user and token are not set' in str(excinfo.value)


def test_sanitise_retry_options_valid():
    """Test _sanitise_retry_options with valid retry options."""
    confluence = Confluence()

    valid_options = DefaultRetryOptions(jitter_multiplier_range=(0.5, 1.5))
    result = confluence._sanitise_retry_options(valid_options)
    assert result == valid_options


def test_sanitise_retry_options_invalid():
    """Test _sanitise_retry_options with invalid retry options."""
    confluence = Confluence()

    invalid_options = DefaultRetryOptions(jitter_multiplier_range=(1.5, 0.5))
    with pytest.raises(ValueError) as excinfo:
        confluence._sanitise_retry_options(invalid_options)
    assert str(excinfo.value) == 'jitter_multiplier_range must be (min, max).'
