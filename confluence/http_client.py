# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""HTTP Client module for Confluence API interactions.

This module provides a client for interacting with the Confluence API,
handling authentication and HTTP requests.
"""

import logging
import os
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

from atlassian import Confluence

from .exceptions import ConfigurationError

CONFLUENCE_DOMAIN = 'https://pdffiller.atlassian.net'
CONFLUENCE_BASE_URL = f'{CONFLUENCE_DOMAIN}/wiki'
CONFLUENCE_BASE_API_URL = f"{CONFLUENCE_BASE_URL}/rest/api"

logger = logging.getLogger('confluence')


class ConfluenceClient:
    """Client for interacting with Confluence API.

    This client handles authentication and provides methods to perform
    various API requests to the Confluence server.
    """

    def __init__(self, timeout: int = 75) -> None:
        """Initialize the ConfluenceClient with authentication and base URL.

        Args:
            timeout (int, optional): Timeout for HTTP requests in seconds
               (default is 10).

        Raises:
            ValueError: If the Confluence API user or token is not set in
                environment variables.
        """
        self.base_url = CONFLUENCE_BASE_API_URL  # DO I need this?
        user = os.getenv('CONFLUENCE_API_USER')
        token = os.getenv('CONFLUENCE_API_TOKEN')

        if user is None or token is None:
            raise ConfigurationError(user, token)

        self.confluence = Confluence(
            url=CONFLUENCE_DOMAIN,
            username=user,
            password=token,
            timeout=timeout,
            cloud=True
        )

    def get_all_pages_in_space(
            self,
            space_key: str,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Retrieve all pages for a given space key from Confluence.

        Args:
            space_key (str): The key of the Confluence space.
            limit (int, optional): Number of pages to retrieve per request
               (default is 100).

        Returns:
            list: List of pages in the specified Confluence space.
        """
        all_pages = []
        logger.info(f'Fetch space pages ({limit} pages per request)...')

        params = {
            'depth': 'all',
            'start': '0',
            'limit': str(limit),
            'expand': 'body.storage,ancestors,history.lastUpdated,version',
            'content_type': 'page',  # How about blogpost?
        }

        while True:
            data = self.confluence.get_space_content(space_key, **params)
            all_pages.extend(data['results'])
            if 'next' in data['_links']:
                next_url = data['_links']['next']
                parsed_url = urlparse(next_url)
                query_params = parse_qs(parsed_url.query)
                for key, value in query_params.items():
                    if key == 'next':
                        continue
                    if len(value) == 1:
                        params[key] = value[0]
                    else:
                        params[key] = ','.join(value)
            else:
                break

        return all_pages
