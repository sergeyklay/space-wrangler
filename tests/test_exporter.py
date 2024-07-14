# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from unittest.mock import MagicMock

import pytest

from confluence.exporter import (
    export_pages_metadata,
    export_space,
    get_all_pages_in_space,
    get_page_path,
    save_pages_to_csv,
    save_pages_to_files,
)


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
                    }
                },
                'version': {'by': {'displayName': 'Test User'}},
                '_links': {'webui': '/wiki/pages/viewpage.action?pageId=123'}
            }
        ],
        '_links': {}
    }
    return mock_resp


def test_get_all_pages_in_space(mock_response, mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response
    pages = get_all_pages_in_space('TEST')
    assert len(pages) == 1
    assert pages[0]['title'] == 'Test Page'


def test_get_page_path():
    page = {
        'ancestors': [{'title': 'Parent Page'}],
        'title': 'Test Page'
    }
    path = get_page_path('/base/dir', page)
    assert path == '/base/dir/Parent Page/Test Page'


def test_save_pages_to_files(tmpdir, mock_response):
    pages = mock_response.json()['results']
    output_dir = tmpdir.mkdir('output')
    save_pages_to_files(pages, output_dir=str(output_dir))
    html_file = output_dir.join('html/Parent Page/Test Page.html')
    json_file = output_dir.join('json/Parent Page/Test Page.json')
    assert html_file.exists()
    assert json_file.exists()


def test_save_pages_to_csv(tmpdir, mock_response):
    pages = mock_response.json()['results']
    output_dir = tmpdir.mkdir('output')
    save_pages_to_csv(pages, output_dir=str(output_dir))
    csv_file = output_dir.join('pages-metadata.csv')
    assert csv_file.exists()


def test_export_space(mocker, tmpdir):
    mock_get_all_pages_in_space = mocker.patch(
        'confluence.exporter.get_all_pages_in_space')
    mock_get_all_pages_in_space.return_value = [{
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
    }]
    output_dir = tmpdir.mkdir('output')
    export_space('TEST', output_dir=str(output_dir))
    html_file = output_dir.join('html/Parent Page/Test Page.html')
    json_file = output_dir.join('json/Parent Page/Test Page.json')
    assert html_file.exists()
    assert json_file.exists()


def test_export_pages_metadata(mocker, tmpdir):
    mock_get_all_pages_in_space = mocker.patch(
        'confluence.exporter.get_all_pages_in_space')
    mock_get_all_pages_in_space.return_value = [{
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
    }]
    output_dir = tmpdir.mkdir('output')
    export_pages_metadata('TEST', output_dir=str(output_dir))
    csv_file = output_dir.join('pages-metadata.csv')
    assert csv_file.exists()
