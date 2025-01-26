# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

"""Tools for exporting metadata of Confluence spaces.

This module provides functions to save metadata of Confluence spaces to a CSV
file.
"""

import csv
import logging
import os
from typing import Tuple

from .common import CONFLUENCE_BASE_URL, format_date, path
from .confluence import Confluence


logger = logging.getLogger('swrangler')


class SpaceMetadata:
    """Constants for space metadata fields and utility methods."""

    SPACE_KEY: str = 'Space Key'
    SPACE_NAME: str = 'Space Name'
    SPACE_TYPE: str = 'Space Type'
    CREATED_BY: str = 'Created By'
    CREATED_DATE: str = 'Created Date'
    SPACE_URL: str = 'Space URL'

    @classmethod
    def get_fieldnames(cls) -> Tuple[str, ...]:
        """Get the fieldnames for the CSV file.

        Returns:
            tuple: Fieldnames for the CSV file.
        """
        return (
            cls.SPACE_KEY,
            cls.SPACE_NAME,
            cls.SPACE_TYPE,
            cls.CREATED_BY,
            cls.CREATED_DATE,
            cls.SPACE_URL,
        )


def export_spaces_metadata(output_dir: str) -> None:
    """Export metadata of all Confluence spaces.

    Args:
        output_dir (str): Directory to save the CSV file.
    """
    client = Confluence()

    spaces = client.get_all_spaces()

    csv_path = os.path.join(output_dir, 'all-spaces.csv')
    os.makedirs(output_dir, exist_ok=True)

    fieldnames = SpaceMetadata.get_fieldnames()
    with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for space in spaces:
            # 'Demonstration Space' has no 'createdBy' field
            created_by = path(
                space,
                'history.createdBy.displayName',
                'Confluence'
            )

            created_date = format_date(path(space, 'history.createdDate'))
            space_url = CONFLUENCE_BASE_URL + path(space, '_links.webui')

            writer.writerow({
                SpaceMetadata.SPACE_KEY: space['key'],
                SpaceMetadata.SPACE_NAME: space['name'],
                SpaceMetadata.SPACE_TYPE: space['type'],
                SpaceMetadata.CREATED_BY: created_by,
                SpaceMetadata.CREATED_DATE: created_date,
                SpaceMetadata.SPACE_URL: space_url,
            })

    logger.info(f'CSV file saved to {csv_path}')
