# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from collections import defaultdict

from confluence.common import people_url
from confluence.http_client import ConfluenceClient
from confluence.owner_metadata import (
    export_owners_metadata,
    OwnerMetadata,
    process_pages,
    save_owners_to_csv,
)


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
        OwnerMetadata.CURRENT_PAGES_OWNED: 0,
        OwnerMetadata.ARCHIVED_PAGES_OWNED: 0,
        OwnerMetadata.LAST_CONTRIBUTION: '01/01/1970',
        OwnerMetadata.OWNER_URL: ''
    })

    # Process current pages
    process_pages(current_pages, owner_data, 'current')

    owner_result = owner_data['John Doe']
    assert owner_result[OwnerMetadata.CURRENT_PAGES_OWNED] == 1
    assert owner_result[OwnerMetadata.ARCHIVED_PAGES_OWNED] == 0
    assert owner_result[OwnerMetadata.UNLICENSED] == 'FALSE'
    assert owner_result[OwnerMetadata.OWNER_URL] == \
           people_url('5b8e8643632a6b2c8f80b883')
    assert owner_result[OwnerMetadata.LAST_CONTRIBUTION] == '01/02/2024'

    # Process archived pages
    process_pages(archived_pages, owner_data, 'archived')

    owner_result = owner_data['Jane Doe (Unlicensed)']
    assert owner_result[OwnerMetadata.CURRENT_PAGES_OWNED] == 0
    assert owner_result[OwnerMetadata.ARCHIVED_PAGES_OWNED] == 1
    assert owner_result[OwnerMetadata.UNLICENSED] == 'TRUE'
    assert owner_result[OwnerMetadata.OWNER_URL] == \
           people_url('5b8e8643632a6b2c8f80b884')
    assert owner_result[OwnerMetadata.LAST_CONTRIBUTION] == '01/04/2024'


def test_save_owners_to_csv(tmpdir):
    owner_data = {
        'John Doe': {
            OwnerMetadata.UNLICENSED: 'FALSE',
            OwnerMetadata.CURRENT_PAGES_OWNED: 2,
            OwnerMetadata.ARCHIVED_PAGES_OWNED: 1,
            OwnerMetadata.LAST_CONTRIBUTION: '07/10/2024',
            OwnerMetadata.OWNER_URL: people_url('5b8e8643632a6b2c8f80b883'),
        },
        'Jane Doe (Unlicensed)': {
            OwnerMetadata.UNLICENSED: 'TRUE',
            OwnerMetadata.CURRENT_PAGES_OWNED: 1,
            OwnerMetadata.ARCHIVED_PAGES_OWNED: 0,
            OwnerMetadata.LAST_CONTRIBUTION: '07/11/2024',
            OwnerMetadata.OWNER_URL: people_url('5b8e8643632a6b2c8f80b884'),
        }
    }
    output_dir = tmpdir.mkdir('output')
    save_owners_to_csv(owner_data, output_dir=str(output_dir))
    csv_file = output_dir.join('owners-metadata.csv')
    assert csv_file.exists()


def test_export_owners_metadata(mocker, tmpdir, mock_response_with_account_id):
    mock_get = mocker.patch.object(
        ConfluenceClient,
        'get_all_pages_in_space',
        return_value=mock_response_with_account_id.json()['results']
    )
    output_dir = tmpdir.mkdir('output')
    export_owners_metadata('TEST', output_dir=str(output_dir))
    csv_file = output_dir.join('owners-metadata.csv')

    assert csv_file.exists()
    assert mock_get.call_count == 2
