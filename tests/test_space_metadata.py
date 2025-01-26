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

from swrangler.space_metadata import export_spaces_metadata


def test_export_spaces_metadata(tmpdir, mocker, spaces_response_with_next):
    mock_object = 'swrangler.confluence.Confluence.get_all_spaces'
    mock_get_all_spaces = mocker.patch(mock_object)
    response = spaces_response_with_next.json()
    mock_get_all_spaces.return_value = response['results']

    output_dir = tmpdir.mkdir('output')
    export_spaces_metadata(str(output_dir))
    csv_file = output_dir.join('all-spaces.csv')

    assert csv_file.exists()
    assert mock_get_all_spaces.call_count == 1
