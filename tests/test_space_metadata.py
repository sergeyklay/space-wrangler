# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from confluence.space_metadata import export_spaces_metadata


def test_export_spaces_metadata(tmpdir, mocker):
    mock_get_all_spaces = mocker.patch(
        'atlassian.Confluence.get_all_spaces',
        return_value={
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
            ]
        }
    )

    output_dir = tmpdir.mkdir('output')
    export_spaces_metadata(str(output_dir))
    csv_file = output_dir.join('all-spaces.csv')

    assert csv_file.exists()
    with open(csv_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        assert len(lines) == 3  # Header + 1 row

        line_0 = (
            'Space Key,Space Name,Space Type,Created By,Created Date,Space URL'
        )
        assert line_0 in lines[0]

        line_1 = (
            'TEST,Test Space,global,Test User,01/01/2024,'
            'https://pdffiller.atlassian.net/wiki/spaces/TEST'
        )
        assert line_1 in lines[1]

        line_2 = (
            'ds,Demonstration Space,global,Confluence,10/20/2015,'
            'https://pdffiller.atlassian.net/wiki/spaces/ds'
        )
        assert line_2 in lines[2]

    assert mock_get_all_spaces.call_count == 1
