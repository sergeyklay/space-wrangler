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

"""Tools for exporting Confluence spaces.

This module provides functions to export Confluence space pages to HTML and
JSON files.
"""

import json
import logging
from typing import Any, Dict, List

from swrangler.common import format_text, mk_path, path
from swrangler.confluence import Confluence
from swrangler.template import html_template

logger = logging.getLogger("swrangler")


def save_pages_to_files(
    pages: List[Dict[str, Any]], space_key: str, output_dir: str
) -> None:
    """Save Confluence pages to HTML, JSON and text files.

    Args:
        pages (list): List of Confluence pages.
        space_key (str): The key of the Confluence space.
        output_dir (str): Directory to save the output files.
    """
    logger.info("Render pages...")
    for page in pages:
        html_path = mk_path("html", space_key, output_dir, page)
        json_path = mk_path("json", space_key, output_dir, page)
        text_path = mk_path("txt", space_key, output_dir, page)

        body_value = path(page, "body.storage.value")
        content = html_template(title=page["title"], content=body_value)

        with open(f"{html_path}.html", "w", encoding="utf-8") as file:
            file.write(content)

        with open(f"{json_path}.json", "w", encoding="utf-8") as file:
            json.dump(page, file, ensure_ascii=False, indent=4)

        plain_text = format_text(body_value)
        with open(f"{text_path}.txt", "w", encoding="utf-8") as file:
            file.write(plain_text)


def export_space(space_key: str, output_dir: str) -> None:
    """Export all pages from a specified Confluence space.

    Args:
        space_key (str): The key of the Confluence space to export.
        output_dir (str): Directory to save the output files.
    """
    client = Confluence()

    pages = client.get_all_pages_in_space(space_key)
    save_pages_to_files(pages, space_key, output_dir)
    logger.info(f"Total {len(pages)} pages downloaded.\n")
