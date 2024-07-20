# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from unittest.mock import MagicMock

import pytest

from confluence.confluence import Confluence


@pytest.fixture
def confluence():
    """Fixture to create a Confluence instance."""
    return Confluence()


@pytest.fixture
def mock_response_with_account_id():
    mock_resp = MagicMock()
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
                        'by': {
                            'displayName': 'John Doe',
                            'accountId': '5b8e8643632a6b2c8f80b883',
                        }
                    },
                    'ownedBy': {
                        'accountId': '5b8e8643632a6b2c8f80b883',
                        'displayName': 'John Doe',
                    },
                },
                'version': {'by': {
                    'displayName': 'John Doe',
                    'accountId': '5b8e8643632a6b2c8f80b883',
                }},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=123'}
            },
            {
                'id': '124',
                'title': 'Archived Page',
                'ancestors': [{'title': 'Parent Page'}],
                'body': {'storage': {'value': '<p>Archived Content</p>'}},
                'history': {
                    'createdDate': '2024-01-03T12:00:00.000Z',
                    'lastUpdated': {
                        'when': '2024-01-04T12:00:00.000Z',
                        'by': {
                            'displayName': 'Jane Doe (Unlicensed)',
                            'accountId': '5b8e8643632a6b2c8f80b884',
                        },
                    },
                    'ownedBy': {
                        'accountId': '5b8e8643632a6b2c8f80b884',
                        'displayName': 'Jane Doe (Unlicensed)',
                    },
                },
                'version': {'by': {
                    'displayName': 'Jane Doe (Unlicensed)',
                    'accountId': '5b8e8643632a6b2c8f80b884',
                }},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=124'}
            }
        ],
        '_links': {}
    }
    mock_resp.status_code = 200
    return mock_resp


@pytest.fixture
def mock_response():
    mock_resp = MagicMock()
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
                    },
                    'ownedBy': {
                        'accountId': '123',
                        'displayName': 'Test User',
                    },
                },
                'version': {'by': {'displayName': 'Test User'}},
                'viewers': 1,
                'views': 1,
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=123'}
            }
        ],
        '_links': {}
    }
    mock_resp.status_code = 200
    return mock_resp


@pytest.fixture
def spaces_response_with_next():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
            'results': [
                {
                    'key': 'TEST',
                    'name': 'Test Space',
                    'type': 'global',
                    'history': {
                        'createdBy': {
                            'displayName': 'Test User'
                        },
                        'createdDate': '2024-01-01T12:00:00.000Z'
                    },
                    '_links': {
                        'webui': '/spaces/TEST'
                    }
                },
                {
                    'key': 'ds',
                    'name': 'Demonstration Space',
                    'type': 'global',
                    'history': {
                        'createdDate': '2015-10-20T15:05:06.966Z'
                    },
                    '_links': {
                        'webui': '/spaces/ds'
                    }
                }
            ],
            'start': 0,
            'limit': 100,
            'size': 100,
            '_links': {
                'base': 'https://pdffiller.atlassian.net/wiki',
                'context': '/wiki',
                'next': ('/rest/api/space'
                         '?next=true&expand=history&limit=100'
                         '&start=100&type=global'),
            },
        }
    mock_resp.status_code = 200
    return mock_resp


@pytest.fixture
def mock_response_with_next():
    mock_resp1 = MagicMock()
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
                    },
                    'ownedBy': {
                        'accountId': '123',
                        'displayName': 'Test User 1',
                    },
                },
                'version': {'by': {'displayName': 'Test User 1'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=123'}
            }
        ],
        '_links': {'next': ('https://pdffiller.atlassian.net'
                            '/wiki/rest/api/content?nextPageStart=2')}
    }
    mock_resp1.status_code = 200

    mock_resp2 = MagicMock()
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
                    },
                    'ownedBy': {
                        'accountId': '123',
                        'displayName': 'Test User 2',
                    },
                },
                'version': {'by': {'displayName': 'Test User 2'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=124'}
            }
        ],
        '_links': {}
    }
    mock_resp2.status_code = 200

    return [mock_resp1, mock_resp2]


@pytest.fixture
def mock_response_with_next_2():
    mock_resp1 = MagicMock()
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
                    },
                    'ownedBy': {
                        'accountId': '123',
                        'displayName': 'Test User 1',
                    },
                },
                'version': {'by': {'displayName': 'Test User 1'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=123'}
            }
        ],
        '_links': {'next': ('https://pdffiller.atlassian.net'
                            '/wiki/rest/api/content?key=value1&key=value2')}
    }
    mock_resp1.status_code = 200

    mock_resp2 = MagicMock()
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
                    },
                    'ownedBy': {
                        'accountId': '123',
                        'displayName': 'Test User 2',
                    },
                },
                'version': {'by': {'displayName': 'Test User 2'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=124'}
            }
        ],
        '_links': {}
    }
    mock_resp2.status_code = 200

    return [mock_resp1, mock_resp2]
