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
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests
from atlassian import Confluence as Client
from atlassian.errors import ApiError
from requests.auth import HTTPBasicAuth

from .common import CONFLUENCE_BASE_URL, CONFLUENCE_DOMAIN, path
from .exceptions import ConfigurationError, Error

logger = logging.getLogger('swrangler')


@dataclass(frozen=True)
class DefaultRetryOptions:
    """Default configuration options for retry logic in API requests.

    Attributes:
        max_retries (int): The maximum number of retry attempts. Default is 4.
        last_retry_delay (int): The delay before the last retry attempt, in
            milliseconds. Default is 5000 ms.
        max_retry_delay (int): The maximum delay between retry attempts, in
            milliseconds. Default is 30000 ms.
        jitter_multiplier_range (Tuple[float, float]): A tuple specifying the
            range for jitter multiplier. The first element is the minimum
            multiplier, and the second element is the maximum multiplier.
            Default is (0.7, 1.3).
    """

    max_retries: int = 4
    last_retry_delay: int = 5000
    max_retry_delay: int = 30000
    jitter_multiplier_range: Tuple[float, float] = (0.7, 1.3)


@dataclass
class ProcessContext:
    """Context for multiprocessing pool initialization.

    Holds configuration and authentication parameters for initializing
    process-specific context.

    Attributes:
        base_url (str): The base URL for the API requests.
        headers (Dict[str, str]): The HTTP headers to include in requests.
        auth (HTTPBasicAuth): The authentication object containing user
            credentials.
        timeout (int): The timeout for HTTP requests in seconds.
        retry_options (DefaultRetryOptions): Configuration options for
            retry logic.
    """

    base_url: str
    headers: Dict[str, str]
    auth: HTTPBasicAuth
    timeout: int
    retry_options: DefaultRetryOptions


class Confluence:
    """Client for interacting with Confluence API.

    This client handles authentication and provides methods to perform
    various API requests to the Confluence server.
    """

    def __init__(
            self,
            timeout: int = 75,
            retry_options: Optional[DefaultRetryOptions] = None
    ) -> None:
        """Initialize the Confluence with authentication and base URL.

        Args:
            timeout (int, optional): Timeout for HTTP requests in seconds
               (default is 10).
            retry_options (DefaultRetryOptions, optional): Retry options for
                handling rate limits and server errors (default is None).

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

        # We use the following for requests that are not covered by
        # the atlassian library. These variables are used exclusively for
        # our own requests.
        self.auth = HTTPBasicAuth(user, token)
        self.headers = {'Accept': 'application/json'}
        self.timeout = timeout
        self.base_url = CONFLUENCE_BASE_URL
        self.retry_options = retry_options or DefaultRetryOptions()

    def _sanitise_retry_options(
            self,
            retry_options: DefaultRetryOptions
    ) -> DefaultRetryOptions:
        min_jitter, max_jitter = retry_options.jitter_multiplier_range
        if max_jitter <= min_jitter:
            raise ValueError('jitter_multiplier_range must be (min, max).')
        return retry_options

    def _update_params_with_next(
            self,
            next_url: str,
            params: Dict[str, Any],
            ignore_list: Optional[List] = None
    ) -> Dict[str, Any]:
        """Update query parameters with the next page's parameters."""
        ignore_list = ignore_list or []
        parsed_url = urlparse(next_url)
        query_params = parse_qs(parsed_url.query)
        for key, value in query_params.items():
            if key in ignore_list:
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
        logger.info(
            f'Fetch {space_key} space pages ({limit} pages per request)...'
        )

        expand = (
            'body.storage,'
            'ancestors,'
            'history.ownedBy,'
            'history.lastUpdated,'
            'version'
        )
        params = {
            'depth': 'all',
            'start': 0,
            'limit': limit,
            'expand': expand,
            'content_type': 'page',  # How about blogpost?
        }

        while True:
            try:
                data = self.client.get_space_content(space_key, **params)
            except ApiError as exc:
                raise Error(
                    f'Failed to fetch pages for {space_key}: {exc}'
                ) from exc

            all_pages.extend(data['results'])
            if not self._has_next_page(data):
                break
            params = self._update_params_with_next(
                path(data, '_links.next'),
                params,
                ['next']
            )

        return all_pages

    def get_all_spaces(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve all spaces from Confluence.

        Returns:
            list: List of spaces in Confluence.
        """
        all_spaces = []
        logger.info(f'Fetch spaces ({limit} spaces per request)...')

        params = {
            'start': 0,
            'limit': limit,
            'space_status': 'current',
            'expand': 'history',
        }

        while True:
            data = self.client.get_all_spaces(**params)
            all_spaces.extend(data['results'])
            if not self._has_next_page(data):
                break
            params = self._update_params_with_next(
                path(data, '_links.next'),
                params,
                ['next', 'type', 'status']
            )

        return all_spaces

    def exponential_backoff(
            self,
            retry_count: int,
            base_delay: int,
            max_retry_delay: int,
    ) -> int:
        """Calculate the backoff delay with jitter."""
        delay = min((2 ** retry_count) * base_delay, max_retry_delay)
        jitter = delay * random.uniform(
            *self.retry_options.jitter_multiplier_range
        )
        return int(delay + jitter)

    def fetch_page_views(
            self,
            content_id: str,
            views_type: str,
            retry_count: int = 0
    ) -> Tuple[str, Optional[int]]:
        """Fetch the number of views for the specified page."""
        url = (
            f'{self.base_url}'
            f'/rest/api/analytics/content/{content_id}/{views_type}'
        )
        retry_options = self._sanitise_retry_options(self.retry_options)
        result = (content_id, None)

        try:
            response = requests.get(
                url,
                headers=self.headers,
                auth=self.auth,
                timeout=self.timeout,
            )
            if response.status_code == 200:
                data = response.json()
                result = (content_id, data['count'])
            elif response.status_code == 429:
                retry_after = response.headers.get(
                    'Retry-After',
                    retry_options.last_retry_delay / 1000
                )

                # Rate limited. Retry after the specified delay.
                if retry_count < retry_options.max_retries:
                    time.sleep(int(retry_after))
                    delay = self.exponential_backoff(
                        retry_count,
                        int(retry_after),
                        retry_options.max_retry_delay
                    )

                    time.sleep(delay / 1000)
                    return self.fetch_page_views(
                        content_id,
                        views_type,
                        retry_count + 1,
                    )

                # Exceeded max retries.
                message = (
                    f'Exceeded max retries for content ID {content_id} '
                    'after being rate limited.'
                )
                logger.error(message)
            elif response.status_code == 500:
                # Internal Server Error. Retry after backoff.
                if retry_count < retry_options.max_retries:
                    delay = self.exponential_backoff(
                        retry_count,
                        retry_options.last_retry_delay,
                        retry_options.max_retry_delay
                    )
                    time.sleep(delay / 1000)
                    return self.fetch_page_views(
                        content_id,
                        views_type,
                        retry_count + 1,
                    )

                # Exceeded max retries.
                message = (
                    f'Exceeded max retries for content ID {content_id} '
                    'after server error.'
                )
                logger.error(message)
            else:
                # Other errors.
                response.raise_for_status()
        except requests.RequestException as e:
            message = f'Failed to fetch data for content ID {content_id}: {e}'
            logger.error(message)

        return result

    def _fetch_page_views_chunk(
            self,
            content_ids: List[str],
            views_type: str
    ) -> Dict[str, Optional[int]]:
        """Fetch page views for a chunk of content IDs."""
        chunk_results = {}
        for content_id in content_ids:
            content_id, views = self.fetch_page_views(content_id, views_type)
            chunk_results[content_id] = views
        return chunk_results

    def get_page_analytics(
            self,
            content_ids: List[str],
            views_type: str
    ) -> Dict[str, Optional[int]]:
        """Get analytics for the specified Confluence pages.

        Args:
            content_ids (list): List of Confluence page IDs.
            views_type (str): The type of analytics (viewers or views).

        Returns:
            dict: Dictionary with page IDs as keys and list of viewers as
               values.
        """
        logger.info(f'Fetch {views_type} for the specified pages...')

        jobs = multiprocessing.cpu_count() or 1
        logger.info(f'Select the number of jobs: {jobs}')

        def chunks(lst: List, n: int) -> Generator:
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n or 1):  # 1 for tests
                yield lst[i:i + n]

        content_id_chunks = chunks(content_ids, len(content_ids) // jobs)

        with multiprocessing.Pool(processes=jobs) as pool:
            results = pool.starmap(
                self._fetch_page_views_chunk,
                [(chunk, views_type) for chunk in content_id_chunks],
            )

        page_views = {}
        for result in results:
            page_views.update(result)

        return page_views
