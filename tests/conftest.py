# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from unittest.mock import MagicMock

import pytest
import requests


@pytest.fixture
def mock_response():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {
        'results': [
            {
                'id': '123',
                'title': 'Test Page',
                'ancestors': [{'title': 'Parent Page'}],
                'body': {'storage': {'value': '<p>Test Content</p>'}},
                'history': {
                    'createdDate': '2024-01-01T12:00:00.000Z',
                    'lastUpdated': {
                        'when': '2024-01-02T12:00:00.000Z',
                        'by': {'displayName': 'Test User'}
                    }
                },
                'version': {'by': {'displayName': 'Test User'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=123'}
            }
        ],
        '_links': {}
    }
    mock_resp.status_code = 200
    return mock_resp


@pytest.fixture
def mock_response_with_next():
    mock_resp1 = MagicMock(spec=requests.Response)
    mock_resp1.json.return_value = {
        'results': [
            {
                'id': '123',
                'title': 'Test Page 1',
                'ancestors': [{'title': 'Parent Page'}],
                'body': {'storage': {'value': '<p>Test Content 1</p>'}},
                'history': {
                    'createdDate': '2024-01-01T12:00:00.000Z',
                    'lastUpdated': {
                        'when': '2024-01-02T12:00:00.000Z',
                        'by': {'displayName': 'Test User 1'}
                    }
                },
                'version': {'by': {'displayName': 'Test User 1'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=123'}
            }
        ],
        '_links': {'next': ('https://pdffiller.atlassian.net'
                            '/wiki/rest/api/content?nextPageStart=2')}
    }
    mock_resp1.status_code = 200

    mock_resp2 = MagicMock(spec=requests.Response)
    mock_resp2.json.return_value = {
        'results': [
            {
                'id': '124',
                'title': 'Test Page 2',
                'ancestors': [{'title': 'Parent Page'}],
                'body': {'storage': {'value': '<p>Test Content 2</p>'}},
                'history': {
                    'createdDate': '2024-01-01T12:00:00.000Z',
                    'lastUpdated': {
                        'when': '2024-01-02T12:00:00.000Z',
                        'by': {'displayName': 'Test User 2'}
                    }
                },
                'version': {'by': {'displayName': 'Test User 2'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=124'}
            }
        ],
        '_links': {}
    }
    mock_resp2.status_code = 200

    return [mock_resp1, mock_resp2]
