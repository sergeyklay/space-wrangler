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
from typing import Any, Dict, List

from .common import (
    contains_cyrillic,
    format_date,
    get_structured_title,
)
from .http_client import CONFLUENCE_BASE_URL, ConfluenceClient

logger = logging.getLogger('confluence')


def save_pages_to_csv(pages: List[Dict[str, Any]], output_dir: str) -> None:
    """Save metadata of Confluence pages to a CSV file.

    Args:
        pages (list): List of Confluence pages.
        output_dir (str): Directory to save the CSV file.
    """
    csv_path = os.path.join(output_dir, 'pages-metadata.csv')

    rows = []
    fieldnames = (
        'Page ID',
        'Page Title',
        'Title in English',
        'Content in English',
        'Created Date',
        'Last Updated Date',
        'Last Editor',
        'Current Owner',
        'Page URL',
    )

    for page in pages:
        content = page['body']['storage']['value']
        content_is_english = not contains_cyrillic(content)
        title_is_english = not contains_cyrillic(page['title'])
        last_updated = page['history']['lastUpdated']

        rows.append({
            fieldnames[0]: page['id'],
            fieldnames[1]: get_structured_title(page),
            fieldnames[2]: title_is_english,
            fieldnames[3]: content_is_english,
            fieldnames[4]: format_date(page['history']['createdDate']),
            fieldnames[5]: format_date(last_updated['when']),
            fieldnames[6]: last_updated['by']['displayName'],
            fieldnames[7]: page['version']['by']['displayName'],
            fieldnames[8]: CONFLUENCE_BASE_URL + page['_links']['webui']
        })

    rows.sort(key=lambda x: x[fieldnames[1]])

    with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f'CSV file saved to {csv_path}')


def export_pages_metadata(space_key: str, output_dir: str) -> None:
    """Export metadata of pages from a specified Confluence space.

    Args:
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the output files.
    """
    client = ConfluenceClient()

    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    result = client.get_all_pages_in_space(space_key)
    save_pages_to_csv(result, output_dir)
    logger.info(
        f'Metadata for {len(result)} pages downloaded and saved to CSV')
