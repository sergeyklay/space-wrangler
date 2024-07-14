# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from collections import defaultdict

from confluence.common import CONFLUENCE_BASE_URL
from confluence.owner_metadata import (
    export_owners_metadata,
    process_pages,
    save_owners_to_csv,
)


def people_url(people_id):
    return f'{CONFLUENCE_BASE_URL}/people/{people_id}'


def test_process_pages():
    # Sample page data
    current_pages = [
        {
            'version': {
                'by': {
                    'displayName': 'John Doe',
                    'accountId': '5b8e8643632a6b2c8f80b883'
                }
            },
            'history': {
                'lastUpdated': {
                    'when': '2024-01-02T12:00:00.000Z'
                }
            }
        }
    ]

    archived_pages = [
        {
            'version': {
                'by': {
                    'displayName': 'Jane Doe (Unlicensed)',
                    'accountId': '5b8e8643632a6b2c8f80b884'
                }
            },
            'history': {
                'lastUpdated': {
                    'when': '2024-01-04T12:00:00.000Z'
                }
            }
        }
    ]

    owner_data = defaultdict(lambda: {
        'Current Pages Owned': 0,
        'Archived Pages Owned': 0,
        'Last Contribution': '01/01/1970',
        'Owner URL': ''
    })

    # Process current pages
    process_pages(current_pages, owner_data, 'current')

    owner_result = owner_data['John Doe']
    assert owner_result['Current Pages Owned'] == 1
    assert owner_result['Archived Pages Owned'] == 0
    assert owner_result['Unlicensed'] == 'FALSE'
    assert owner_result['Owner URL'] == people_url('5b8e8643632a6b2c8f80b883')
    assert owner_result['Last Contribution'] == '01/02/2024'

    # Process archived pages
    process_pages(archived_pages, owner_data, 'archived')

    owner_result = owner_data['Jane Doe (Unlicensed)']
    assert owner_result['Current Pages Owned'] == 0
    assert owner_result['Archived Pages Owned'] == 1
    assert owner_result['Unlicensed'] == 'TRUE'
    assert owner_result['Owner URL'] == people_url('5b8e8643632a6b2c8f80b884')
    assert owner_result['Last Contribution'] == '01/04/2024'


def test_save_owners_to_csv(tmpdir):
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
