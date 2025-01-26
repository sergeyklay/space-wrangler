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

import logging

from swrangler.logger import StdErrFilter, StdOutFilter, setup_logger


def test_stdout_filter():
    """Test StdOutFilter only allows DEBUG and INFO level messages."""
    stdout_filter = StdOutFilter()

    debug_record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="",
        lineno=0,
        msg="debug",
        args=(),
        exc_info=None,
    )
    info_record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="info",
        args=(),
        exc_info=None,
    )
    warning_record = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname="",
        lineno=0,
        msg="warning",
        args=(),
        exc_info=None,
    )
    error_record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname="",
        lineno=0,
        msg="error",
        args=(),
        exc_info=None,
    )

    assert stdout_filter.filter(debug_record) is True
    assert stdout_filter.filter(info_record) is True
    assert stdout_filter.filter(warning_record) is False
    assert stdout_filter.filter(error_record) is False


def test_stderr_filter():
    """Test StdErrFilter only allows proper level messages."""
    stderr_filter = StdErrFilter()

    debug_record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="",
        lineno=0,
        msg="debug",
        args=(),
        exc_info=None,
    )
    info_record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="info",
        args=(),
        exc_info=None,
    )
    warning_record = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname="",
        lineno=0,
        msg="warning",
        args=(),
        exc_info=None,
    )
    error_record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname="",
        lineno=0,
        msg="error",
        args=(),
        exc_info=None,
    )

    assert stderr_filter.filter(debug_record) is False
    assert stderr_filter.filter(info_record) is False
    assert stderr_filter.filter(warning_record) is True
    assert stderr_filter.filter(error_record) is True


def test_setup_logger_default(capsys):
    """Test setup_logger with default settings (quiet=False)."""
    logger = setup_logger()

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    captured = capsys.readouterr()
    assert "This is a debug message" in captured.out
    assert "This is an info message" in captured.out
    assert "This is a warning message" in captured.err
    assert "This is an error message" in captured.err


def test_setup_logger_quiet(capsys):
    """Test setup_logger with quiet=True setting."""
    logger = setup_logger(quiet=True)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    captured = capsys.readouterr()
    assert "This is a debug message" not in captured.out
    assert "This is an info message" not in captured.out
    assert "This is a warning message" in captured.err
    assert "This is an error message" in captured.err


def test_logger_handlers_count():
    """Test that setup_logger does not add multiple handlers."""
    logger = setup_logger()
    initial_handler_count = len(logger.handlers)

    logger = setup_logger()
    assert len(logger.handlers) == initial_handler_count


def test_logger_stdout_level_change(capsys):
    """Test logger stdout level changes with quiet setting."""
    logger = setup_logger()
    logger.debug("This should appear")
    captured = capsys.readouterr()
    assert "This should appear" in captured.out

    logger = setup_logger(quiet=True)
    logger.debug("This should not appear")
    captured = capsys.readouterr()
    assert "This should not appear" not in captured.out


def test_logger_stderr_level_unchanged(capsys):
    """Test logger stderr level remains consistent."""
    logger = setup_logger()
    logger.error("This should appear in stderr")
    captured = capsys.readouterr()
    assert "This should appear in stderr" in captured.err

    logger = setup_logger(quiet=True)
    logger.error("This should still appear in stderr")
    captured = capsys.readouterr()
    assert "This should still appear in stderr" in captured.err
