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
from typing import Any, Dict, List, Optional, Union
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

CONFLUENCE_BASE_URL = 'https://pdffiller.atlassian.net/wiki'
CONFLUENCE_BASE_API_URL = f"{CONFLUENCE_BASE_URL}/rest/api"

load_dotenv()
logger = logging.getLogger('confluence')


class ConfluenceClient:
    """Client for interacting with Confluence API.

    This client handles authentication and provides methods to perform
    various API requests to the Confluence server.
    """

    def __init__(self, timeout: int = 10) -> None:
        """Initialize the ConfluenceClient with authentication and base URL.

        Args:
            timeout (int, optional): Timeout for HTTP requests in seconds
               (default is 10).

        Raises:
            ValueError: If the Confluence API user or token is not set in
                environment variables.
        """
        self.base_url = CONFLUENCE_BASE_API_URL
        user = os.getenv('CONFLUENCE_API_USER')
        token = os.getenv('CONFLUENCE_API_TOKEN')

        if user is None or token is None:
            raise ValueError(
                'Confluence API user or token not set in environment variables'
            )

        self.auth = HTTPBasicAuth(user, token)
        self.headers = {'Accept': 'application/json'}
        self.timeout = timeout

    def get(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform a GET request to the Confluence API.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (dict, optional): Optional query parameters to include in
               the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an
               unsuccessful status code.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_all_pages_in_space(
            self,
            space_key: str,
            status_filter: str = 'current',
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Retrieve all pages for a given space key from Confluence.

        Args:
            space_key (str): The key of the Confluence space.
            status_filter (str, optional): Filter for the status of the pages
               ('current' or 'archived').
            limit (int, optional): Number of pages to retrieve per request
               (default is 100).

        Returns:
            list: List of pages in the specified Confluence space.
        """
        endpoint = '/content'
        params: Dict[str, Union[str, int]] = {
            'spaceKey': space_key,
            'expand': 'body.storage,ancestors,history.lastUpdated,version',
            'limit': str(limit),
            'status': status_filter,
        }

        all_pages = []
        logger.info(
            f'Fetch space {status_filter} pages '
            f'({limit} pages per request)...'
        )
        while True:
            data = self.get(endpoint, params=params)
            all_pages.extend(data['results'])
            if 'next' in data['_links']:
                next_url = data['_links']['next']
                parsed_url = urlparse(next_url)
                query_params = parse_qs(parsed_url.query)
                for key, value in query_params.items():
                    if len(value) == 1:
                        params[key] = value[0]
                    else:
                        params[key] = ','.join(value)
            else:
                break
        return all_pages
