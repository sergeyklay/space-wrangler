# Copyright (C) 2024-2025 Serghei Iakovlev <gnu@serghei.pl>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

from collections import defaultdict

from swrangler.common import people_url
from swrangler.confluence import Confluence
from swrangler.owner_metadata import (
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
