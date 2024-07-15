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
import logging
import os
from collections import defaultdict
from datetime import datetime

from .common import (
    check_unlicensed_or_deleted,
    format_date,
    get_all_pages_in_space,
    people_url,
)

logger = logging.getLogger('confluence')


class OwnerMetadata:
    """Constants for owner metadata fields and utility methods."""

    OWNER = 'Owner'
    UNLICENSED = 'Unlicensed'
    CURRENT_PAGES_OWNED = 'Current Pages Owned'
    ARCHIVED_PAGES_OWNED = 'Archived Pages Owned'
    LAST_CONTRIBUTION = 'Last Contribution'
    OWNER_URL = 'Owner URL'

    @classmethod
    def get_fieldnames(cls):
        """Get the fieldnames for the CSV file.

        Returns:
            tuple: Fieldnames for the CSV file.
        """
        return (
            cls.OWNER,
            cls.UNLICENSED,
            cls.CURRENT_PAGES_OWNED,
            cls.ARCHIVED_PAGES_OWNED,
            cls.LAST_CONTRIBUTION,
            cls.OWNER_URL
        )

    @classmethod
    def to_dict(cls, owner, data):
        """Convert owner data to a dictionary for CSV writing.

        Args:
            owner (str): Owner name.
            data (dict): Owner metadata.

        Returns:
            dict: Dictionary representation of the owner metadata.
        """
        return {
            cls.OWNER: owner,
            cls.UNLICENSED: data[cls.UNLICENSED],
            cls.CURRENT_PAGES_OWNED: data[cls.CURRENT_PAGES_OWNED],
            cls.ARCHIVED_PAGES_OWNED: data[cls.ARCHIVED_PAGES_OWNED],
            cls.LAST_CONTRIBUTION: data[cls.LAST_CONTRIBUTION],
            cls.OWNER_URL: data[cls.OWNER_URL]
        }


def save_owners_to_csv(owner_data, output_dir):
    """Save metadata of Confluence page owners to a CSV file.

    Args:
        owner_data (dict): Dictionary containing owner metadata.
        output_dir (str): Directory to save the CSV file.
    """
    csv_path = os.path.join(output_dir, 'owners-metadata.csv')
    fieldnames = OwnerMetadata.get_fieldnames()

    sorted_data = sorted(
        owner_data.items(),
        key=lambda x: x[1][OwnerMetadata.CURRENT_PAGES_OWNED],
        reverse=True,
    )

    with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for owner, data in sorted_data:
            if data[fieldnames[2]] > 0 or data[fieldnames[3]] > 0:
                writer.writerow(OwnerMetadata.to_dict(owner, data))

    logger.info('CSV file saved to {}'.format(csv_path))


def process_pages(pages, owner_data, status):
    """Process a list of pages and update owner metadata.

    Args:
        pages (list): List of Confluence pages.
        owner_data (dict): Dictionary to store owner metadata.
        status (str): Status of the pages ('current' or 'archived').
    """
    for page in pages:
        owner = page['version']['by']['displayName']
        owner_id = page['version']['by']['accountId']
        owner_url = people_url(owner_id)
        unlicensed_or_deleted = check_unlicensed_or_deleted(owner)
        last_updated = page['history']['lastUpdated']['when']
        formatted_last_updated = format_date(last_updated)

        curr_owner = owner_data[owner]

        if status == 'current':
            curr_owner[OwnerMetadata.CURRENT_PAGES_OWNED] += 1
        elif status == 'archived':
            curr_owner[OwnerMetadata.ARCHIVED_PAGES_OWNED] += 1

        curr_owner[OwnerMetadata.UNLICENSED] = unlicensed_or_deleted
        curr_owner[OwnerMetadata.OWNER_URL] = owner_url

        parsed_last_updated = datetime.strptime(
            formatted_last_updated, '%m/%d/%Y')
        parsed_last_contribution = datetime.strptime(
            curr_owner[OwnerMetadata.LAST_CONTRIBUTION], '%m/%d/%Y')

        if parsed_last_updated > parsed_last_contribution:
            curr_owner[OwnerMetadata.LAST_CONTRIBUTION] = \
                formatted_last_updated


def export_owners_metadata(space_key, output_dir):
    """Export metadata of page owners from a specified Confluence space.

    Args:
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the output files.
    """
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    current_pages = get_all_pages_in_space(space_key, 'current')
    archived_pages = get_all_pages_in_space(space_key, 'archived')

    owner_data = defaultdict(lambda: {
        OwnerMetadata.CURRENT_PAGES_OWNED: 0,
        OwnerMetadata.ARCHIVED_PAGES_OWNED: 0,
        OwnerMetadata.LAST_CONTRIBUTION: '01/01/1970',
        OwnerMetadata.OWNER_URL: ''
    })

    process_pages(current_pages, owner_data, 'current')
    process_pages(archived_pages, owner_data, 'archived')

    save_owners_to_csv(owner_data, output_dir)
    logger.info('Metadata for page owners downloaded and saved to CSV.')
