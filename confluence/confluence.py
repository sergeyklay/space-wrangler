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
import multiprocessing
import os
import random
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse

import requests
from atlassian import Confluence as Client
from requests.auth import HTTPBasicAuth

from .exceptions import ConfigurationError

CONFLUENCE_DOMAIN = 'https://pdffiller.atlassian.net'
CONFLUENCE_BASE_URL = f'{CONFLUENCE_DOMAIN}/wiki'

# Default values for jitter multiplier range.
# Used for exponential backoff with jitter.
DEFAULT_JITTER = (0.7, 1.3)

logger = logging.getLogger('confluence')


class Confluence:
    """Client for interacting with Confluence API.

    This client handles authentication and provides methods to perform
    various API requests to the Confluence server.
    """

    def __init__(
            self,
            timeout: int = 75,
            jitter: Optional[Tuple[float, float]] = DEFAULT_JITTER
    ) -> None:
        """Initialize the Confluence with authentication and base URL.

        Args:
            timeout (int, optional): Timeout for HTTP requests in seconds
               (default is 10).
            jitter (tuple, optional): Jitter multiplier range for exponential
                backoff (default is DEFAULT_JITTER).

        Raises:
            ValueError: If the Confluence API user or token is not set in
                environment variables.
        """
        user = os.getenv('CONFLUENCE_API_USER')
        token = os.getenv('CONFLUENCE_API_TOKEN')

        if user is None or token is None:
            raise ConfigurationError(user, token)

        self.client = Client(
            url=CONFLUENCE_DOMAIN,
            username=user,
            password=token,
            timeout=timeout,
            cloud=True
        )

        # We use auth, headers and jitter for requests that are not covered by
        # the atlassian library. These variables are used exclusively for
        # our own requests.
        self.auth = HTTPBasicAuth(user, token)
        self.headers = {'Accept': 'application/json'}
        self.jitter = jitter

    def _initial_params(self, limit: int) -> Dict[str, str]:
        """Initialize the query parameters."""
        expand = (
            'body.storage,'
            'ancestors,'
            'history.ownedBy,'
            'history.lastUpdated,'
            'version'
        )
        return {
            'depth': 'all',
            'start': '0',
            'limit': str(limit),
            'expand': expand,
            'content_type': 'page',   # How about blogpost?
        }

    def _update_params_with_next(
            self,
            next_url: str,
            params: Dict[str, str]
    ) -> Dict[str, str]:
        """Update query parameters with the next page's parameters."""
        parsed_url = urlparse(next_url)
        query_params = parse_qs(parsed_url.query)
        for key, value in query_params.items():
            if key == 'next':
                continue
            params[key] = value[0] if len(value) == 1 else ','.join(value)
        return params

    def _has_next_page(self, data: Dict[str, Any]) -> bool:
        """Check if there is a next page."""
        return 'next' in data['_links']

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

        params = self._initial_params(limit)
        while True:
            data = self.client.get_space_content(space_key, **params)
            all_pages.extend(data['results'])
            if not self._has_next_page(data):
                break
            params = self._update_params_with_next(
                data['_links']['next'],
                params
            )

        return all_pages

    def exponential_backoff(
            self,
            retry_count: int,
            base_delay: int,
            max_retry_delay: int,
    ) -> float:
        """Calculate the backoff delay with jitter."""
        delay = min((2 ** retry_count) * base_delay, max_retry_delay)
        jitter = delay * random.uniform(*self.jitter)
        return delay + jitter

    def fetch_page_views(
            self,
            content_id: Union[str, int],
            retry_count: int = 0,
            last_retry_delay: Union[int, float] = 1,
            max_retry_delay: int = 30,
            max_retries: int = 4
    ):
        """Fetch the number of page views for the specified page."""
        url = (
            f'{CONFLUENCE_BASE_URL}'
            f'/rest/api/analytics/content/{content_id}/viewers'
        )

        try:
            response = requests.get(url, headers=self.headers, auth=self.auth)
            if response.status_code == 200:
                data = response.json()
                return content_id, data['count']
            elif response.status_code == 429:
                retry_after = response.headers.get(
                    'Retry-After',
                    last_retry_delay
                )
                retry_after = int(retry_after)

                # Rate limited. Retry after the specified delay.
                if retry_count < max_retries:
                    time.sleep(retry_after)
                    delay = self.exponential_backoff(
                        retry_count,
                        last_retry_delay,
                        max_retry_delay
                    )
                    time.sleep(delay)

                    return self.fetch_page_views(
                        content_id,
                        retry_count + 1,
                        delay
                    )
            elif response.status_code == 500:
                # Internal Server Error. Retry after backoff.
                if retry_count < max_retries:
                    delay = self.exponential_backoff(
                        retry_count,
                        last_retry_delay,
                        max_retry_delay
                    )
                    time.sleep(delay)

                    return self.fetch_page_views(
                        content_id,
                        retry_count + 1,
                        delay
                    )
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            message = f'Failed to fetch data for content ID {content_id}: {e}'
            logger.error(message)
            return content_id, None

    def _init_process_context(self, base_url, headers, auth):
        """Initialize process-specific context."""
        logger.info('Initializing process...')
        self.base_url = base_url
        self.headers = headers
        self.auth = auth

    def _fetch_page_views_chunk(self, content_ids_chunk):
        """Fetch page views for a chunk of content IDs."""
        chunk_results = {}
        for content_id in content_ids_chunk:
            content_id, views = self.fetch_page_views(content_id)
            chunk_results[content_id] = views
        return chunk_results

    def get_page_analytics(self, content_ids: List[str]):
        """Get analytics for the specified Confluence pages.

        Args:
            content_ids (list): List of Confluence page IDs.

        Returns:
            dict: Dictionary with page IDs as keys and list of viewers as values.
        """
        logger.info('Fetch viewers for the specified pages...')

        jobs = multiprocessing.cpu_count()
        logger.info(f'Select the number of jobs: {jobs}')

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        content_id_chunks = chunks(content_ids, len(content_ids) // jobs)

        with multiprocessing.Pool(
                processes=jobs,
                initializer=self._init_process_context,
                initargs=(CONFLUENCE_DOMAIN, self.headers, self.auth)) as pool:
            results = pool.map(
                self._fetch_page_views_chunk,
                content_id_chunks,
            )

        page_views = {}
        for result in results:
            page_views.update(result)

        return page_views
