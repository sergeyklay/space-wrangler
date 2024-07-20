# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from collections import defaultdict

from confluence.common import people_url
from confluence.confluence import Confluence
from confluence.owner_metadata import (
    export_owners_metadata,
    OwnerMetadata,
    process_pages,
    save_owners_to_csv,
)


def test_process_pages():
    pages = [
        {
            'version': {
                'by': {
                    'displayName': 'John Doe',
                    'accountId': '12345678'
                }
            },
            'history': {
                'lastUpdated': {
                    'when': '2024-01-02T12:00:00.000Z'
                },
                'ownedBy': {
                    'accountId': '5b8e8643632a6b2c8f80b883',
                    'displayName': 'John Doe',
                },
            }
        }
    ]

    owner_data = defaultdict(lambda: {
        OwnerMetadata.PAGES_OWNED: 0,
        OwnerMetadata.LAST_CONTRIBUTION: '01/01/1970',
        OwnerMetadata.OWNER_URL: ''
    })

    # Process pages
    process_pages(pages, owner_data)

    owner_result = owner_data['John Doe']
    assert owner_result[OwnerMetadata.PAGES_OWNED] == 1
    assert owner_result[OwnerMetadata.UNLICENSED] == 'FALSE'
    assert owner_result[OwnerMetadata.OWNER_URL] == people_url(
        '5b8e8643632a6b2c8f80b883')
    assert owner_result[OwnerMetadata.LAST_CONTRIBUTION] == '01/02/2024'


def test_save_owners_to_csv(tmpdir):
    owner_data = {
        'John Doe': {
            OwnerMetadata.UNLICENSED: 'FALSE',
            OwnerMetadata.PAGES_OWNED: 2,
            OwnerMetadata.LAST_CONTRIBUTION: '07/10/2024',
            OwnerMetadata.OWNER_URL: people_url('5b8e8643632a6b2c8f80b883'),
        },
        'Jane Doe (Unlicensed)': {
            OwnerMetadata.UNLICENSED: 'TRUE',
            OwnerMetadata.PAGES_OWNED: 1,
            OwnerMetadata.LAST_CONTRIBUTION: '07/11/2024',
            OwnerMetadata.OWNER_URL: people_url('5b8e8643632a6b2c8f80b884'),
        }
    }
    output_dir = tmpdir.mkdir('output')
    save_owners_to_csv(owner_data, 'AIR', str(output_dir))
    csv_file = output_dir.join('AIR/csv/owners-metadata.csv')
    assert csv_file.exists()


def test_export_owners_metadata(mocker, tmpdir, mock_response_with_account_id):
    mock_get = mocker.patch.object(
        Confluence,
        'get_all_pages_in_space',
        return_value=mock_response_with_account_id.json()['results']
    )

    output_dir = tmpdir.mkdir('output')
    export_owners_metadata('AIR', str(output_dir))
    csv_file = output_dir.join('AIR/csv/owners-metadata.csv')

    assert csv_file.exists()
    assert mock_get.call_count == 1
