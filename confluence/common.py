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
from datetime import datetime

logger = logging.getLogger('confluence')


def people_url(people_id):
    """Generate a Confluence profile URL for a given user ID.

    Args:
        people_id (str): User ID of the Confluence user.

    Returns:
        str: URL to the user's Confluence profile.
    """
    from .http_client import CONFLUENCE_BASE_URL
    return f'{CONFLUENCE_BASE_URL}/people/{people_id}'


def check_unlicensed_or_deleted(owner_name):
    """Check if the owner is unlicensed or deleted.

    Args:
        owner_name (str): The name of the owner to check.

    Returns:
        str: 'TRUE' if the owner is unlicensed or deleted, 'FALSE' otherwise.
    """
    if re.search(r'\((Unlicensed|Deleted)\)$', owner_name):
        return 'TRUE'
    return 'FALSE'


def get_page_path(base_dir, page):
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


def format_date(date_str):
    """Format a date string to mm/dd/yyyy.

    Args:
        date_str (str): Date string in ISO format.

    Returns:
        str: Formatted date string.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_obj.strftime('%m/%d/%Y')


def contains_cyrillic(text):
    """Check if the given text contains Cyrillic characters.

    Args:
        text (str): Text to check.

    Returns:
        bool: True if the text contains Cyrillic characters, False otherwise.
    """
    return bool(re.search('[\u0400-\u04FF]', text))


def get_structured_title(page):
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
