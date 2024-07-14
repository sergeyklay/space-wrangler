# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import sys
from argparse import ArgumentParser
from unittest import mock

from confluence import args


def test_none_args(monkeypatch):
    """Show help message and return None if gstore was called without any
    argument and environment variables were not enough to start gstore.
    """
    monkeypatch.setattr('sys.argv', ['confluence'])
    with mock.patch.object(ArgumentParser, 'print_help') as mock_help:
        assert args.argparse() is None
        mock_help.assert_called_once_with(sys.stderr)
