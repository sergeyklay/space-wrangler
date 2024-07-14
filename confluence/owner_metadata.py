# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed с this source code.

"""Tools for exporting owner metadata of Confluence pages.

This module provides functions to save metadata of Confluence page owners to
a CSV file.
"""

import csv
import os
from collections import defaultdict
from datetime import datetime

from .common import (
    check_unlicensed_or_deleted,
    CONFLUENCE_BASE_URL,
    format_date,
    get_all_pages_in_space,
)


def save_owners_to_csv(owner_data, output_dir):
    """Save metadata of Confluence page owners to a CSV file."""
    csv_path = os.path.join(output_dir, 'owners-metadata.csv')

    fieldnames = (
        'Owner',
        'Unlicensed',
        'Current Pages Owned',
        'Archived Pages Owned',
        'Last Contribution',
        'Owner URL'
    )

    sorted_data = sorted(
        owner_data.items(),
        key=lambda x: x[1][fieldnames[2]],
        reverse=True,
    )

    with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for owner, data in sorted_data:
            if data[fieldnames[2]] > 0 or data[fieldnames[3]] > 0:
                writer.writerow({
                    fieldnames[0]: owner,
                    fieldnames[1]: data[fieldnames[1]],
                    fieldnames[2]: data[fieldnames[2]],
                    fieldnames[3]: data[fieldnames[3]],
                    fieldnames[4]: data[fieldnames[4]],
                    fieldnames[5]: data[fieldnames[5]]
                })

    print(f"CSV file saved to {csv_path}")


def process_pages(pages, owner_data, status):
    """Process a list of pages and update owner metadata."""
    for page in pages:
        owner = page['version']['by']['displayName']
        owner_id = page['version']['by']['accountId']
        owner_url = f"{CONFLUENCE_BASE_URL}/people/{owner_id}"
        unlicensed_or_deleted = check_unlicensed_or_deleted(owner)
        last_updated = page['history']['lastUpdated']['when']
        formatted_last_updated = format_date(last_updated)

        if status == 'current':
            owner_data[owner]['Current Pages Owned'] += 1
        elif status == 'archived':
            owner_data[owner]['Archived Pages Owned'] += 1

        owner_data[owner]['Unlicensed'] = unlicensed_or_deleted
        owner_data[owner]['Owner URL'] = owner_url

        parsed_last_updated = datetime.strptime(
            formatted_last_updated, '%m/%d/%Y')
        parsed_last_contribution = datetime.strptime(
            owner_data[owner]['Last Contribution'], '%m/%d/%Y')

        if parsed_last_updated > parsed_last_contribution:
            owner_data[owner]['Last Contribution'] = formatted_last_updated


def export_owners_metadata(space_key, output_dir):
    """Export metadata of page owners from a specified Confluence space."""
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    current_pages = get_all_pages_in_space(space_key, 'current')
    archived_pages = get_all_pages_in_space(space_key, 'archived')

    owner_data = defaultdict(lambda: {
        'Current Pages Owned': 0,
        'Archived Pages Owned': 0,
        'Last Contribution': '01/01/1970',
        'Owner URL': ''
    })

    process_pages(current_pages, owner_data, 'current')
    process_pages(archived_pages, owner_data, 'archived')

    save_owners_to_csv(owner_data, output_dir)
    print('Metadata for page owners downloaded and saved to CSV.')
