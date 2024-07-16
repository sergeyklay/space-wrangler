# tests/test_space_exporter.py

# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from confluence.confluence import Confluence
from confluence.space_exporter import export_space, save_pages_to_files


def test_save_pages_to_files(tmpdir, mock_response):
    pages = mock_response.json()['results']
    output_dir = tmpdir.mkdir('output')
    save_pages_to_files(pages, output_dir=str(output_dir))
    html_file = output_dir.join('html/Parent Page/Test Page.html')
    json_file = output_dir.join('json/Parent Page/Test Page.json')
    assert html_file.exists()
    assert json_file.exists()


def test_export_space(mocker, tmpdir, mock_response):
    mock_get_all_pages_in_space = mocker.patch.object(
        Confluence,
        'get_all_pages_in_space',
        return_value=mock_response.json()['results']
    )
    output_dir = tmpdir.mkdir('output')
    export_space('TEST', output_dir=str(output_dir))
    html_file = output_dir.join('html/Parent Page/Test Page.html')
    json_file = output_dir.join('json/Parent Page/Test Page.json')

    assert html_file.exists()
    assert json_file.exists()
    assert mock_get_all_pages_in_space.call_count == 1
