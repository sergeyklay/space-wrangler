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

from unittest import mock

from swrangler.cli import main
from swrangler.exceptions import Error


def test_main_no_args(monkeypatch):
    """Test calling main with no arguments."""
    monkeypatch.setattr('sys.argv', ['swrangler'])
    with mock.patch('click.core.Context.get_help') as mock_help:
        with mock.patch('sys.stderr', new_callable=mock.MagicMock):
            assert main() == 1
            mock_help.assert_called_once()


def test_main_export(monkeypatch, mocker):
    """Test calling main with export command."""
    monkeypatch.setattr(
        'sys.argv',
        ['swrangler', 'export-space', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch('swrangler.space_exporter.export_space') as command_mock:
        command_mock.return_value = None
        main()
        command_mock.assert_called_once_with('TEST', 'output')


def test_main_pages_metadata(monkeypatch, mocker):
    """Test calling main with pages-metadata command."""
    monkeypatch.setattr(
        'sys.argv',
        ['swrangler', 'pages-metadata', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch('swrangler.page_metadata.export_pages_metadata') as mck:
        mck.return_value = None
        main()
        mck.assert_called_once_with('TEST', 'output')


def test_main_owners_metadata(monkeypatch, mocker):
    """Test calling main with owners-metadata command."""
    monkeypatch.setattr(
        'sys.argv',
        ['swrangler', 'owners-metadata', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch('swrangler.owner_metadata.export_owners_metadata') as mck:
        mck.return_value = None
        main()
        mck.assert_called_once_with('TEST', 'output')


def test_main_keyboard_interrupt(monkeypatch, mocker):
    """Test handling of KeyboardInterrupt."""
    monkeypatch.setattr(
        'sys.argv',
        ['swrangler', 'export-space', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch(
            'swrangler.space_exporter.export_space',
            side_effect=KeyboardInterrupt
    ):
        exit_code = main()
        assert exit_code == 130  # 128 + signal.SIGINT


def test_main_error(monkeypatch, mocker):
    """Test handling of custom Error exception."""
    monkeypatch.setattr(
        'sys.argv',
        ['swrangler', 'export-space', '-s', 'TEST', '-o', 'output']
    )

    with mock.patch(
            'swrangler.space_exporter.export_space',
            side_effect=Error('Test error')
    ):
        exit_code = main()
        assert exit_code == 1
