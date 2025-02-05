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

"""Tools for exporting owner metadata of Confluence pages.

This module provides functions to save metadata of Confluence page owners to
a CSV file.
"""

import csv
import logging
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, DefaultDict, Dict, List, Tuple

from swrangler.common import (
    check_unlicensed_or_deleted,
    format_date,
    mk_path,
    path,
    people_url,
)
from swrangler.confluence import Confluence

logger = logging.getLogger("swrangler")


class OwnerMetadata:
    """Constants for owner metadata fields and utility methods."""

    OWNER: str = "Owner"
    UNLICENSED: str = "Unlicensed"
    PAGES_OWNED: str = "Pages Owned"
    LAST_CONTRIBUTION: str = "Last Contribution"
    OWNER_URL: str = "Owner URL"

    @classmethod
    def get_fieldnames(cls) -> Tuple[str, ...]:
        """Get the fieldnames for the CSV file.

        Returns:
            tuple: Fieldnames for the CSV file.
        """
        return (
            cls.OWNER,
            cls.UNLICENSED,
            cls.PAGES_OWNED,
            cls.LAST_CONTRIBUTION,
            cls.OWNER_URL,
        )

    @classmethod
    def to_dict(cls, owner: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert owner data to a dictionary for CSV writing.

        Args:
            owner (str): Owner name.
            data (dict): Owner data.

        Returns:
            dict: Dictionary representation of the owner metadata.
        """
        return {
            cls.OWNER: owner,
            cls.UNLICENSED: data[cls.UNLICENSED],
            cls.PAGES_OWNED: data[cls.PAGES_OWNED],
            cls.LAST_CONTRIBUTION: data[cls.LAST_CONTRIBUTION],
            cls.OWNER_URL: data[cls.OWNER_URL],
        }


def save_owners_to_csv(
    owner_data: Dict[str, Any],
    space_key: str,
    output_dir: str,
) -> None:
    """Save metadata of Confluence page owners to a CSV file.

    Args:
        owner_data (dict): Dictionary containing owner metadata.
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the CSV file.
    """
    csv_path = mk_path("csv", space_key, output_dir)
    csv_path = os.path.join(csv_path, "owners-metadata.csv")

    fieldnames = OwnerMetadata.get_fieldnames()

    sorted_data = sorted(
        owner_data.items(),
        key=lambda x: x[1][OwnerMetadata.PAGES_OWNED],
        reverse=True,
    )

    with open(csv_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for owner, data in sorted_data:
            writer.writerow(OwnerMetadata.to_dict(owner, data))

    logger.info(f"CSV file saved to {csv_path}")


def process_pages(
    pages: List[Dict[str, Any]],
    owner_data: Dict[str, Any],
) -> None:
    """Process a list of pages and update owner metadata.

    Args:
        pages (list): List of Confluence pages.
        owner_data (dict): Dictionary to store owner metadata.
    """
    for page in pages:
        owner = path(page, "history.ownedBy.displayName")
        owner_id = path(page, "history.ownedBy.accountId")
        owner_url = people_url(owner_id)
        unlicensed_or_deleted = check_unlicensed_or_deleted(owner)
        last_updated = path(page, "history.lastUpdated.when")
        formatted_last_updated = format_date(last_updated)

        curr_owner = owner_data[owner]
        curr_owner[OwnerMetadata.PAGES_OWNED] += 1
        curr_owner[OwnerMetadata.UNLICENSED] = unlicensed_or_deleted
        curr_owner[OwnerMetadata.OWNER_URL] = owner_url

        parsed_last_updated = datetime.strptime(
            formatted_last_updated, "%m/%d/%Y"
        )
        parsed_last_contribution = datetime.strptime(
            curr_owner[OwnerMetadata.LAST_CONTRIBUTION], "%m/%d/%Y"
        )

        if parsed_last_updated > parsed_last_contribution:
            curr_owner[OwnerMetadata.LAST_CONTRIBUTION] = (
                formatted_last_updated
            )


def export_owners_metadata(space_key: str, output_dir: str) -> None:
    """Export metadata of page owners from a specified Confluence space.

    Args:
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the output files.
    """
    client = Confluence()

    pages = client.get_all_pages_in_space(space_key)
    owner_data: DefaultDict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            OwnerMetadata.PAGES_OWNED: 0,
            OwnerMetadata.LAST_CONTRIBUTION: "01/01/1970",
            OwnerMetadata.OWNER_URL: "",
        }
    )

    process_pages(pages, owner_data)
    save_owners_to_csv(owner_data, space_key, output_dir)

    logger.info(
        (
            f"Metadata for {len(owner_data)} page owners "
            "downloaded and saved to CSV.\n"
        )
    )
