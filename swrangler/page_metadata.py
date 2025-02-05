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

"""Tools for exporting metadata of Confluence pages.

This module provides functions to save metadata of Confluence pages to a CSV
file.
"""

import csv
import logging
import os
from typing import Any, Dict, List, Tuple

from swrangler.common import (
    contains_cyrillic,
    format_date,
    get_structured_title,
    mk_path,
    path,
)
from swrangler.confluence import Confluence

logger = logging.getLogger("swrangler")


class PageMetadata:
    """Constants for page metadata fields and utility methods."""

    PAGE_ID: str = "Page ID"
    PAGE_TITLE: str = "Page Title"
    UNIQUE_VIEWERS: str = "Unique Viewers"
    TOTAL_VIEWS: str = "Total Views"
    TITLE_IN_ENGLISH: str = "Title in English"
    CONTENT_IN_ENGLISH: str = "Content in English"
    CREATED_DATE: str = "Created Date"
    LAST_UPDATED_DATE: str = "Last Updated Date"
    LAST_EDITOR: str = "Last Editor"
    CURRENT_OWNER: str = "Current Owner"
    PAGE_URL: str = "Page URL"

    @classmethod
    def get_fieldnames(cls) -> Tuple[str, ...]:
        """Get the fieldnames for the CSV file.

        Returns:
            tuple: Fieldnames for the CSV file.
        """
        return (
            cls.PAGE_ID,
            cls.PAGE_TITLE,
            cls.UNIQUE_VIEWERS,
            cls.TOTAL_VIEWS,
            cls.TITLE_IN_ENGLISH,
            cls.CONTENT_IN_ENGLISH,
            cls.CREATED_DATE,
            cls.LAST_UPDATED_DATE,
            cls.LAST_EDITOR,
            cls.CURRENT_OWNER,
            cls.PAGE_URL,
        )


def save_pages_to_csv(
    pages: List[Dict[str, Any]], space_key: str, output_dir: str
) -> None:
    """Save metadata of Confluence pages to a CSV file.

    Args:
        pages (list): List of Confluence pages.
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the CSV file.
    """
    csv_path = mk_path("csv", space_key, output_dir)
    csv_path = os.path.join(csv_path, "pages-metadata.csv")

    rows = []
    for page in pages:
        content = path(page, "body.storage.value")
        content_is_english = not contains_cyrillic(content)
        title_is_english = not contains_cyrillic(page["title"])
        last_updated = path(page, "history.lastUpdated")
        created_date = path(page, "history.createdDate")
        owner_name = path(page, "history.ownedBy.displayName")

        rows.append(
            {
                PageMetadata.PAGE_ID: page["id"],
                PageMetadata.PAGE_TITLE: get_structured_title(page),
                PageMetadata.UNIQUE_VIEWERS: page.get("viewers", 0),
                PageMetadata.TOTAL_VIEWS: page.get("views", 0),
                PageMetadata.TITLE_IN_ENGLISH: title_is_english,
                PageMetadata.CONTENT_IN_ENGLISH: content_is_english,
                PageMetadata.CREATED_DATE: format_date(created_date),
                PageMetadata.LAST_UPDATED_DATE: format_date(
                    last_updated["when"]
                ),
                PageMetadata.LAST_EDITOR: path(last_updated, "by.displayName"),
                PageMetadata.CURRENT_OWNER: owner_name,
                PageMetadata.PAGE_URL: f"{os.getenv('CONFLUENCE_DOMAIN')}/wiki"
                + path(page, "_links.webui"),
            }
        )

    rows.sort(key=lambda x: x[PageMetadata.PAGE_TITLE])

    with open(csv_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=PageMetadata.get_fieldnames())
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"CSV file saved to {csv_path}")


def export_pages_metadata(space_key: str, output_dir: str) -> None:
    """Export metadata of pages from a specified Confluence space.

    Args:
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the output files.
    """
    client = Confluence()

    pages = client.get_all_pages_in_space(space_key)
    logger.info("Fetch analytics data for specified pages...")

    content_ids = [page["id"] for page in pages]

    viewers_counts = client.get_page_analytics(content_ids, "viewers")

    views_counts = client.get_page_analytics(content_ids, "views")

    for page in pages:
        page_id = page["id"]
        page["viewers"] = viewers_counts.get(page_id, 0)
        page["views"] = views_counts.get(page_id, 0)

    save_pages_to_csv(pages, space_key, output_dir)
    logger.info(
        f"Metadata for {len(pages)} pages downloaded and saved to CSV\n"
    )
