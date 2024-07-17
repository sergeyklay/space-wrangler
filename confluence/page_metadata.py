# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Tools for exporting metadata of Confluence pages.

This module provides functions to save metadata of Confluence pages to a CSV
file.
"""

import csv
import logging
import os
from typing import Any, Dict, List, Tuple

from .common import (
    contains_cyrillic,
    format_date,
    get_structured_title,
)
from .confluence import Confluence, CONFLUENCE_BASE_URL

logger = logging.getLogger('confluence')


class PageMetadata:
    """Constants for page metadata fields and utility methods."""

    PAGE_ID: str = 'Page ID'
    PAGE_TITLE: str = 'Page Title'
    TITLE_IN_ENGLISH: str = 'Title in English'
    CONTENT_IN_ENGLISH: str = 'Content in English'
    CREATED_DATE: str = 'Created Date'
    LAST_UPDATED_DATE: str = 'Last Updated Date'
    LAST_EDITOR: str = 'Last Editor'
    CURRENT_OWNER: str = 'Current Owner'
    PAGE_URL: str = 'Page URL'

    @classmethod
    def get_fieldnames(cls) -> Tuple[str, ...]:
        """Get the fieldnames for the CSV file.

        Returns:
            tuple: Fieldnames for the CSV file.
        """
        return (
            cls.PAGE_ID,
            cls.PAGE_TITLE,
            cls.TITLE_IN_ENGLISH,
            cls.CONTENT_IN_ENGLISH,
            cls.CREATED_DATE,
            cls.LAST_UPDATED_DATE,
            cls.LAST_EDITOR,
            cls.CURRENT_OWNER,
            cls.PAGE_URL,
        )


def save_pages_to_csv(pages: List[Dict[str, Any]], output_dir: str) -> None:
    """Save metadata of Confluence pages to a CSV file.

    Args:
        pages (list): List of Confluence pages.
        output_dir (str): Directory to save the CSV file.
    """
    csv_path = os.path.join(output_dir, 'pages-metadata.csv')

    rows = []
    for page in pages:
        content = page['body']['storage']['value']
        content_is_english = not contains_cyrillic(content)
        title_is_english = not contains_cyrillic(page['title'])
        last_updated = page['history']['lastUpdated']
        created_date = page['history']['createdDate']
        owner_name = page['history']['ownedBy']['displayName']

        rows.append({
            PageMetadata.PAGE_ID: page['id'],
            PageMetadata.PAGE_TITLE: get_structured_title(page),
            PageMetadata.TITLE_IN_ENGLISH: title_is_english,
            PageMetadata.CONTENT_IN_ENGLISH: content_is_english,
            PageMetadata.CREATED_DATE: format_date(created_date),
            PageMetadata.LAST_UPDATED_DATE: format_date(last_updated['when']),
            PageMetadata.LAST_EDITOR: last_updated['by']['displayName'],
            PageMetadata.CURRENT_OWNER: owner_name,
            PageMetadata.PAGE_URL:
                CONFLUENCE_BASE_URL + page['_links']['webui'],
        })

    rows.sort(key=lambda x: x[PageMetadata.PAGE_TITLE])

    with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=PageMetadata.get_fieldnames())
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f'CSV file saved to {csv_path}')


def export_pages_metadata(space_key: str, output_dir: str) -> None:
    """Export metadata of pages from a specified Confluence space.

    Args:
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the output files.
    """
    client = Confluence()

    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    pages = client.get_all_pages_in_space(space_key)
    save_pages_to_csv(pages, output_dir)
    logger.info(
        f'Metadata for {len(pages)} pages downloaded and saved to CSV')
