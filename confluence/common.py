# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Common utilities for Confluence operations.

This module provides shared functions and constants used by other modules.
"""

import logging
import os
import re
import textwrap
from datetime import datetime
from functools import reduce
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

logger = logging.getLogger('confluence')

CONFLUENCE_DOMAIN = 'https://pdffiller.atlassian.net'
CONFLUENCE_BASE_URL = f'{CONFLUENCE_DOMAIN}/wiki'


def people_url(people_id: str) -> str:
    """Generate a Confluence profile URL for a given user ID.

    Args:
        people_id (str): User ID of the Confluence user.

    Returns:
        str: URL to the user's Confluence profile.
    """
    return f'{CONFLUENCE_BASE_URL}/people/{people_id}'


def check_unlicensed_or_deleted(owner_name: str) -> str:
    """Check if the owner is unlicensed or deleted.

    Args:
        owner_name (str): The name of the owner to check.

    Returns:
        str: 'TRUE' if the owner is unlicensed or deleted, 'FALSE' otherwise.
    """
    if re.search(r'\((Unlicensed|Deleted)\)$', owner_name):
        return 'TRUE'
    return 'FALSE'


def get_page_path(base_dir: str, page: Dict[str, Any]) -> str:
    """Generate the full file path for a given page.

    Args:
        base_dir (str): Base directory for the file path.
        page (dict): Confluence page data.

    Returns:
        str: Full file path for the given page.
    """
    ancestors = page['ancestors']
    path_parts = [parent['title'].replace('/', '-') for parent in ancestors]
    path_parts.append(page['title'].replace('/', '-'))

    full_path = os.path.join(base_dir, *path_parts)
    return full_path


def mk_path(
        parent_dir: str,
        space_key: str,
        output_dir: str,
        page: Optional[Dict[str, Any]] = None
) -> str:
    """Create and return the full directory path.

    Constructs the directory path based on the given parameters, including the
    Confluence space key, output directory, and optional page data, creates the
    directories if they do not exist, and returns the full path.

    Args:
        parent_dir (str): Parent directory name.
        space_key (str): Key of the Confluence space.
        output_dir (str): Base output directory.
        page (Optional[Dict[str, Any]]): Optional Confluence page data.

    Returns:
        str: The full path to the directory.
    """
    base_path = os.path.join(output_dir, space_key, parent_dir)
    if page:
        full_path = get_page_path(str(base_path), page)
    else:
        full_path = base_path

    os.makedirs(full_path, exist_ok=True)
    return full_path


def format_date(date_str: str) -> str:
    """Format a date string to mm/dd/yyyy.

    Args:
        date_str (str): Date string in ISO format.

    Returns:
        str: Formatted date string.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_obj.strftime('%m/%d/%Y')


def contains_cyrillic(text: str) -> bool:
    """Check if the given text contains Cyrillic characters.

    Args:
        text (str): Text to check.

    Returns:
        bool: True if the text contains Cyrillic characters, False otherwise.
    """
    return bool(re.search('[\u0400-\u04FF]', text))


def get_structured_title(page: Dict[str, Any]) -> str:
    """Construct a structured title for a page based on its ancestors.

    Args:
        page (dict): Confluence page data.

    Returns:
        str: Structured title for the page.
    """
    ancestors = page['ancestors']
    path_parts = []

    for parent in ancestors:
        path_parts.append('/' + parent['title'].replace('/', '-'))

    path_parts.append('/' + page['title'].replace('/', '-'))

    return ''.join(path_parts)


def format_text(html_content: str) -> str:
    """Extract and format text from HTML content.

    Args:
        html_content (str): Input HTML content.

    Returns:
        str: Formatted plain text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove all <ac:parameter> tags
    for param in soup.find_all('ac:parameter'):
        param.decompose()

    # Find all code blocks and add double newlines before and after them
    for code_block in soup.find_all(
            'ac:structured-macro',
            {'ac:name': 'code'}
    ):
        code_text = code_block.get_text()
        formatted_code_text = f'\n\n{code_text}\n\n'
        code_block.replace_with(formatted_code_text)

    text = soup.get_text().replace('\xa0', ' ')
    lines = text.splitlines()
    new_lines: List[str] = []
    empty_line = False

    for line in lines:
        if line.strip() == '':
            if not empty_line and new_lines:
                new_lines.append('')
            empty_line = True
        else:
            wrapped_lines = textwrap.wrap(line, width=80)
            new_lines.extend(wrapped_lines)
            empty_line = False

    formatted_text = '\n'.join(new_lines).strip()
    return formatted_text


def path(data: dict, item: str, default: Any = None) -> Any:
    """Steps through an item chain to get the ultimate value.

    If ultimate value or path to value does not exist, does not raise
    an exception and instead returns default.

    Args:
        data (dict): Dictionary to search through.
        item (str): Path to the value.
        default (Any, optional): Default value to return if path
            does not exist.
    """
    def getitem(obj: Any, name: str) -> Any:
        if obj is None:
            return default

        try:
            return obj[name]
        except (KeyError, TypeError):
            return default

    return reduce(getitem, item.split('.'), data)
