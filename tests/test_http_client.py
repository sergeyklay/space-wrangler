# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from confluence.exceptions import ConfigurationError
from confluence.http_client import ConfluenceClient


def test_get_all_pages_in_space(mock_response, mocker):
    mock_get = mocker.patch('atlassian.Confluence.get_space_content')
    mock_get.return_value = mock_response.json()
    client = ConfluenceClient()
    pages = client.get_all_pages_in_space('TEST')
    assert len(pages) == 1
    assert pages[0]['title'] == 'Test Page'


def test_get_all_pages_in_space_with_next(mock_response_with_next, mocker):
    mock_get = mocker.patch(
        'atlassian.Confluence.get_space_content',
        side_effect=[
            mock_response_with_next[0].json(),
            mock_response_with_next[1].json(),
        ]
    )
    client = ConfluenceClient()
    pages = client.get_all_pages_in_space('TEST')

    assert mock_get.call_count == 2
    assert len(pages) == 2
    assert pages[0]['title'] == 'Test Page 1'
    assert pages[1]['title'] == 'Test Page 2'


def test_get_all_pages_in_space_with_next_2(mock_response_with_next_2, mocker):
    mock_get = mocker.patch(
        'atlassian.Confluence.get_space_content',
        side_effect=[
            mock_response_with_next_2[0].json(),
            mock_response_with_next_2[1].json(),
        ]
    )
    client = ConfluenceClient()
    pages = client.get_all_pages_in_space('TEST')

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
        ConfluenceClient()
    assert 'Confluence API user and token are not set' in str(excinfo.value)
