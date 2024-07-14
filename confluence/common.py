# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Common utilities for Confluence operations.

This module provides shared functions and constants used by other modules.
"""

import os
import re
from datetime import datetime
from urllib.parse import parse_qs, urlparse

import requests
from requests.auth import HTTPBasicAuth

CONFLUENCE_BASE_URL = 'https://pdffiller.atlassian.net/wiki'
CONFLUENCE_BASE_API_URL = f"{CONFLUENCE_BASE_URL}/rest/api"


def people_url(people_id):
    """Generate a Confluence profile URL for a given user ID."""
    return f'{CONFLUENCE_BASE_URL}/people/{people_id}'


def get_all_pages_in_space(space_key, status_filter=None):
    """Retrieve all pages for a given space key from Confluence."""
    url = f"{CONFLUENCE_BASE_API_URL}/content"

    limit = 100
    headers = {'Accept': 'application/json'}
    params = {
        'spaceKey': space_key,
        'expand': 'body.storage,ancestors,history.lastUpdated,version',
        'limit': str(limit),
        'status': status_filter or 'current',
    }

    auth = HTTPBasicAuth(
        os.getenv('CONFLUENCE_API_USER'),
        os.getenv('CONFLUENCE_API_TOKEN'),
    )

    all_pages = []
    print(f'Fetch space pages ({limit} pages per request):')
    while True:
        print('.', end='', flush=True)
        response = requests.get(
            url,
            params=params,
            auth=auth,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        all_pages.extend(data['results'])

        if 'next' in data['_links']:
            next_url = data['_links']['next']
            parsed_url = urlparse(next_url)
            query_params = parse_qs(parsed_url.query)

            for key, value in query_params.items():
                params.update({key: value[0] if len(value) == 1 else value})
        else:
            break

    print('')
    print('')
    return all_pages


def check_unlicensed_or_deleted(owner_name):
    """Check if the owner is unlicensed or deleted.

    This function checks if the owner name ends with '(Unlicensed)'
    or '(Deleted)'.

    :param owner_name: The name of the owner to check.
    :type owner_name: str
    :return: 'TRUE' if the owner is unlicensed or deleted, 'FALSE' otherwise.
    :rtype: str
    """
    if re.search(r'\((Unlicensed|Deleted)\)$', owner_name):
        return 'TRUE'
    return 'FALSE'


def get_page_path(base_dir, page):
    """Generate the full file path for a given page."""
    ancestors = page['ancestors']
    path_parts = [parent['title'].replace('/', '-') for parent in ancestors]
    path_parts.append(page['title'].replace('/', '-'))

    full_path = os.path.join(base_dir, *path_parts)
    return full_path


def format_date(date_str):
    """Format a date string to mm/dd/yyyy."""
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_obj.strftime('%m/%d/%Y')


def contains_cyrillic(text):
    """Check if the given text contains Cyrillic characters."""
    return bool(re.search('[\u0400-\u04FF]', text))


def get_structured_title(page):
    """Construct a structured title for a page based on its ancestors."""
    ancestors = page['ancestors']
    path_parts = []

    for parent in ancestors:
        path_parts.append('/' + parent['title'].replace('/', '-'))

    path_parts.append('/' + page['title'].replace('/', '-'))

    return ''.join(path_parts)
