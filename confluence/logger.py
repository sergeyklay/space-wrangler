# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Logging initialization for the confluence command-line tool.

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

    def filter(self, record):
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

    def filter(self, record):
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


def setup_logger(quiet=False):
    """Configures and returns the logger for the application.

    This function sets up a logger that directs DEBUG and INFO messages to
    stdout, and WARNING, ERROR, and CRITICAL messages to stderr. If the quiet
    option is enabled, only WARNING and higher level messages will be logged.

    Args:
        quiet (bool): If True, suppresses DEBUG and INFO messages.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger('confluence')
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
