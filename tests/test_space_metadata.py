# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from confluence.space_metadata import export_spaces_metadata


def test_export_spaces_metadata(tmpdir, mocker, spaces_response_with_next):
    mock_object = 'confluence.confluence.Confluence.get_all_spaces'
    mock_get_all_spaces = mocker.patch(mock_object)
    response = spaces_response_with_next.json()
    mock_get_all_spaces.return_value = response['results']

    output_dir = tmpdir.mkdir('output')
    export_spaces_metadata(str(output_dir))
    csv_file = output_dir.join('all-spaces.csv')

    assert csv_file.exists()
    assert mock_get_all_spaces.call_count == 1
