# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Tools for exporting Confluence spaces.

This module provides functions to export Confluence space pages to HTML and
JSON files.
"""

import json
import logging
import os
from typing import Any, Dict, List

from .common import get_page_path
from .confluence import Confluence
from .template import html_template

logger = logging.getLogger('confluence')


def save_pages_to_files(
        pages: List[Dict[str, Any]],
        output_dir: str = './output'
) -> None:
    """Save Confluence pages to HTML and JSON files.

    Args:
        pages (list): List of Confluence pages.
        output_dir (str): Directory to save the output files.
    """
    logger.info('Render pages...')
    for page in pages:
        html_path = get_page_path(os.path.join(output_dir, 'html'), page)
        json_path = get_page_path(os.path.join(output_dir, 'json'), page)

        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

        content = html_template(
            title=page['title'],
            content=page['body']['storage']['value'])

        with open(f"{html_path}.html", 'w', encoding='utf-8') as file:
            file.write(content)

        with open(f"{json_path}.json", 'w', encoding='utf-8') as file:
            json.dump(page, file, ensure_ascii=False, indent=4)


def export_space(space_key: str, output_dir: str) -> None:
    """Export all pages from a specified Confluence space.

    Args:
        space_key (str): The key of the Confluence space to export.
        output_dir (str): Directory to save the output files.
    """
    client = Confluence()

    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    pages = client.get_all_pages_in_space(space_key)
    save_pages_to_files(pages, output_dir)
    logger.info(f'Total {len(pages)} pages downloaded.')
