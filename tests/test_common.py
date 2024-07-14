# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from confluence.common import (
    check_unlicensed_or_deleted,
    CONFLUENCE_BASE_URL,
    get_all_pages_in_space,
    get_page_path,
    people_url,
)


def test_people_url():
    """Test the people_url function."""
    people_id = '5b8e8643632a6b2c8f80b883'
    expected_url = f'{CONFLUENCE_BASE_URL}/people/{people_id}'
    assert people_url(people_id) == expected_url


def test_get_all_pages_in_space(mock_response, mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response
    pages = get_all_pages_in_space('TEST')
    assert len(pages) == 1
    assert pages[0]['title'] == 'Test Page'


def test_get_all_pages_in_space_with_next(mock_response_with_next, mocker):
    mock_get = mocker.patch(
        'requests.get',
        side_effect=mock_response_with_next
    )
    pages = get_all_pages_in_space('TEST')

    assert mock_get.call_count == 2
    assert len(pages) == 2
    assert pages[0]['title'] == 'Test Page 1'
    assert pages[1]['title'] == 'Test Page 2'


def test_get_page_path():
    page = {
        'ancestors': [{'title': 'Parent Page'}],
        'title': 'Test Page'
    }
    path = get_page_path('/base/dir', page)
    assert path == '/base/dir/Parent Page/Test Page'


def test_check_unlicensed_or_deleted():
    assert check_unlicensed_or_deleted('John Doe (Unlicensed)') == 'TRUE'
    assert check_unlicensed_or_deleted('Jane Doe (Deleted)') == 'TRUE'
    assert check_unlicensed_or_deleted('John Doe') == 'FALSE'
