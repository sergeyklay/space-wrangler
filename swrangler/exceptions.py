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

    This exception is used to indicate that one of the required
    environment variables (CONFLUENCE_API_USER, CONFLUENCE_API_TOKEN,
    and CONFLUENCE_DOMAIN) are not set.

    Attributes:
        user (Optional[str]): The Confluence API user.
        token (Optional[str]): The Confluence API token.
        url (Optional[str]): The Confluence domain.
        message (str): The error message indicating the missing configuration.
    """

    def __init__(
        self, user: Optional[str], token: Optional[str], url: Optional[str]
    ) -> None:
        """
        Initialize the ConfigurationError with the given user and token.

        Args:
            user (Optional[str]): The Confluence API user.
            token (Optional[str]): The Confluence API token.
            url (Optional[str]): The Confluence domain.
        """
        self.user = user
        self.token = token
        self.url = url
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

        # Create a list of missing configurations
        missing = []
        if not is_set(self.user):
            missing.append("CONFLUENCE_API_USER")
        if not is_set(self.token):
            missing.append("CONFLUENCE_API_TOKEN")
        if not is_set(self.url):
            missing.append("CONFLUENCE_DOMAIN")

        # Handle single missing configuration
        if len(missing) == 1:
            config = missing[0]
            return (
                f"{config} is not set. Please set it in the .confluence file "
                f"or directly in the environment."
            )

        # Handle multiple missing configurations
        if missing:
            configs = ", ".join(missing)
            return (
                f"The following environment variables are not set: {configs}."
                f"Please set them in the .confluence file or directly in the "
                f"environment."
            )

        # This should never happen since we check for missing configs above
        return "Unknown configuration error occurred."
