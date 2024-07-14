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
    mock_export_space = mocker.patch('confluence.cli.export_space')
    mock_export_space.return_value = None

    assert main() == 0
    mock_export_space.assert_called_once_with('TEST', 'output')


def test_main_pages_metadata(monkeypatch, mocker):
    """Test calling main with pages-metadata command."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'pages-metadata', '-s', 'TEST', '-o', 'output']
    )
    mock_export_pages_metadata = mocker.patch(
        'confluence.cli.export_pages_metadata')
    mock_export_pages_metadata.return_value = None

    assert main() == 0
    mock_export_pages_metadata.assert_called_once_with('TEST', 'output')


def test_main_keyboard_interrupt(monkeypatch, mocker):
    """Test handling of KeyboardInterrupt."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'export', '-s', 'TEST', '-o', 'output']
    )
    mock_export_space = mocker.patch('confluence.cli.export_space',
                                     side_effect=KeyboardInterrupt)

    with mock.patch('sys.stderr.write') as mock_stderr:
        assert main() == 130
        mock_export_space.assert_called_once()
        mock_stderr.assert_called_once_with(
            'Received keyboard interrupt, terminating.\n')


def test_main_error(monkeypatch, mocker):
    """Test handling of custom Error exception."""
    monkeypatch.setattr(
        'sys.argv',
        ['confluence', 'export', '-s', 'TEST', '-o', 'output']
    )
    mock_export_space = mocker.patch('confluence.cli.export_space',
                                     side_effect=Error('Test error'))

    with mock.patch('sys.stderr.write') as mock_stderr:
        assert main() == 1
        mock_export_space.assert_called_once()
        mock_stderr.assert_called_once_with('Test error\n')
