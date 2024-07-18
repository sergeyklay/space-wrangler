# tests/test_page_metadata.py

# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from confluence.page_metadata import export_pages_metadata, save_pages_to_csv


def test_save_pages_to_csv(tmpdir, mock_response):
    pages = mock_response.json()['results']
    output_dir = tmpdir.mkdir('output')
    save_pages_to_csv(pages, output_dir=str(output_dir))
    csv_file = output_dir.join('pages-metadata.csv')
    assert csv_file.exists()


def test_export_pages_metadata(mocker, tmpdir, mock_response):
    mock_object = 'confluence.confluence.Confluence.get_all_pages_in_space'
    mock_get = mocker.patch(mock_object)
    mock_get.return_value = mock_response.json()['results']

    output_dir = tmpdir.mkdir('output')
    export_pages_metadata('TEST', output_dir=str(output_dir))
    csv_file = output_dir.join('pages-metadata.csv')

    assert csv_file.exists()
    assert mock_get.call_count == 1
