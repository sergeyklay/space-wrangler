# This file is part of the swrangler.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Helper routines and classes to work with exceptions."""

from typing import Optional


class Error(Exception):
    """Base class for exceptions in swrangler module."""


class ConfigurationError(Error):
    """Exception raised for errors in the configuration of the app.

    This exception is used to indicate that one or both of the required
    environment variables (CONFLUENCE_API_USER and CONFLUENCE_API_TOKEN)
    are not set.

    Attributes:
        user (Optional[str]): The Confluence API user.
        token (Optional[str]): The Confluence API token.
        message (str): The error message indicating the missing configuration.
    """

    def __init__(self, user: Optional[str], token: Optional[str]) -> None:
        """
        Initialize the ConfigurationError with the given user and token.

        Args:
            user (Optional[str]): The Confluence API user.
            token (Optional[str]): The Confluence API token.
        """
        self.user = user
        self.token = token
        self.message = self._generate_message()
        super().__init__(self.message)

    def _generate_message(self) -> str:
        """Generate an error message based on the missing configuration.

        Returns:
            str: The error message indicating what is missing and how to fix
                the configuration.
        """
        def is_set(value: Optional[str]) -> bool:
            """Check if the value is set and not empty."""
            return value is not None and len(str(value)) > 0

        if not is_set(self.user) and is_set(self.token):
            return (
                'Confluence API user is not set in environment variables. '
                'Please set CONFLUENCE_API_USER.'
            )

        if not is_set(self.token) and is_set(self.user):
            return (
                'Confluence API token is not set in environment variables. '
                'Please set CONFLUENCE_API_TOKEN.'
            )

        return (
            'Confluence API user and token are not set in environment '
            'variables. Please set both CONFLUENCE_API_USER and '
            'CONFLUENCE_API_TOKEN.'
        )
