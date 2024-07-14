# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from confluence.common import CONFLUENCE_BASE_URL
from confluence.owner_metadata import export_owners_metadata, save_owners_to_csv


def test_save_owners_to_csv(tmpdir):
    def people_url(people_id):
        return f'{CONFLUENCE_BASE_URL}/people/{people_id}'

    owner_data = {
        'John Doe': {
            'Unlicensed': 'FALSE',
            'Current Pages Owned': 2,
            'Archived Pages Owned': 1,
            'Last Contribution': '07/10/2024',
            'Owner URL': people_url('5b8e8643632a6b2c8f80b883'),
        },
        'Jane Doe (Unlicensed)': {
            'Unlicensed': 'TRUE',
            'Current Pages Owned': 1,
            'Archived Pages Owned': 0,
            'Last Contribution': '07/11/2024',
            'Owner URL': people_url('5b8e8643632a6b2c8f80b884'),
        }
    }
    output_dir = tmpdir.mkdir('output')
    save_owners_to_csv(owner_data, output_dir=str(output_dir))
    csv_file = output_dir.join('owners-metadata.csv')
    assert csv_file.exists()


def test_export_owners_metadata(mocker, tmpdir, mock_response_with_account_id):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response_with_account_id
    output_dir = tmpdir.mkdir('output')
    export_owners_metadata('TEST', output_dir=str(output_dir))
    csv_file = output_dir.join('owners-metadata.csv')
    assert csv_file.exists()
