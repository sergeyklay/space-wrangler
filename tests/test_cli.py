# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

from unittest import mock

from confluence.cli import main
from confluence.exceptions import Error


def test_main_no_args(monkeypatch):
    """Test calling main with no arguments."""
    monkeypatch.setattr('sys.argv', ['confluence'])
    with mock.patch('argparse.ArgumentParser.print_help') as mock_help:
        with mock.patch('sys.stderr', new_callable=mock.MagicMock):
            assert main() == 1
            mock_help.assert_called_once()


def test_main_export(monkeypatch, mocker):
    """Test calling main with export command."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'export', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch('confluence.space_exporter.export_space') as mck:
        mck.return_value = None
        main()
        mck.assert_called_once_with('TEST', 'output')


def test_main_pages_metadata(monkeypatch, mocker):
    """Test calling main with pages-metadata command."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'pages-metadata', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch('confluence.page_metadata.export_pages_metadata') as mck:
        mck.return_value = None
        main()
        mck.assert_called_once_with('TEST', 'output')


def test_main_owners_metadata(monkeypatch, mocker):
    """Test calling main with owners-metadata command."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'owners-metadata', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch('confluence.owner_metadata.export_owners_metadata') as mck:
        mck.return_value = None
        main()
        mck.assert_called_once_with('TEST', 'output')


def test_main_keyboard_interrupt(monkeypatch, mocker):
    """Test handling of KeyboardInterrupt."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'export', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch(
            'confluence.space_exporter.export_space',
            side_effect=KeyboardInterrupt
    ):
        exit_code = main()
        assert exit_code == 130  # 128 + signal.SIGINT


def test_main_error(monkeypatch, mocker):
    """Test handling of custom Error exception."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'export', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch(
            'confluence.space_exporter.export_space',
            side_effect=Error('Test error')
    ):
        exit_code = main()
        assert exit_code == 1
