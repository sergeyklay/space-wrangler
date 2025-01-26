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
                "Confluence API user is not set in environment variables. "
                "Please set CONFLUENCE_API_USER."
            )

        if not is_set(self.token) and is_set(self.user):
            return (
                "Confluence API token is not set in environment variables. "
                "Please set CONFLUENCE_API_TOKEN."
            )

        return (
            "Confluence API user and token are not set in environment "
            "variables. Please set both CONFLUENCE_API_USER and "
            "CONFLUENCE_API_TOKEN."
        )
