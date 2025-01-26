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

"""Logging initialization for the swrangler command-line tool.

This module provides setup for a logger that directs informational messages to
stdout and warnings/errors to stderr. It also supports a quiet mode to suppress
informational messages.
"""

import logging
import sys


class StdOutFilter(logging.Filter):
    """A logging filter that allows only DEBUG and INFO level messages.

    This filter is used to direct DEBUG and INFO messages to stdout.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Determines if the specified record is to be logged.

        Args:
            record (logging.LogRecord): The log record to be filtered.

        Returns:
            bool: True if the record level is DEBUG or INFO, False otherwise.
        """
        return record.levelno in (logging.DEBUG, logging.INFO)


class StdErrFilter(logging.Filter):
    """A logging filter that allows only WARNING, ERROR, and CRITICAL levels.

    This filter is used to direct WARNING, ERROR, and CRITICAL messages
    to stderr.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Determines if the specified record is to be logged.

        Args:
            record (logging.LogRecord): The log record to be filtered.

        Returns:
            bool: True if the record level is WARNING, ERROR, or CRITICAL,
                False otherwise.
        """
        return record.levelno in (
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        )


def setup_logger(quiet: bool = False) -> logging.Logger:
    """Configures and returns the logger for the application.

    This function sets up a logger that directs DEBUG and INFO messages to
    stdout, and WARNING, ERROR, and CRITICAL messages to stderr. If the quiet
    option is enabled, only WARNING and higher level messages will be logged.

    Args:
        quiet (bool): If True, suppresses DEBUG and INFO messages.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger('swrangler')
    logger.setLevel(logging.DEBUG if not quiet else logging.WARNING)

    formatter = logging.Formatter('%(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG if not quiet else logging.WARNING)
    stdout_handler.addFilter(StdOutFilter())
    stdout_handler.setFormatter(formatter)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.addFilter(StdErrFilter())
    stderr_handler.setFormatter(formatter)

    logger.handlers = []
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger
