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

from swrangler.confluence import Confluence
from swrangler.space_exporter import export_space, save_pages_to_files


def test_save_pages_to_files(tmpdir, mock_response):
    pages = mock_response.json()['results']
    output_dir = tmpdir.mkdir('output')

    save_pages_to_files(pages, 'AIR', str(output_dir))

    assert output_dir.join('AIR/html/Parent Page/Test Page.html').exists()
    assert output_dir.join('AIR/json/Parent Page/Test Page.json').exists()
    assert output_dir.join('AIR/txt/Parent Page/Test Page.txt').exists()


def test_export_space(mocker, tmpdir, mock_response):
    mock_get_all_pages_in_space = mocker.patch.object(
        Confluence,
        'get_all_pages_in_space',
        return_value=mock_response.json()['results']
    )
    output_dir = tmpdir.mkdir('output')
    export_space('AIR', str(output_dir))

    assert output_dir.join('AIR/html/Parent Page/Test Page.html').exists()
    assert output_dir.join('AIR/json/Parent Page/Test Page.json').exists()
    assert output_dir.join('AIR/txt/Parent Page/Test Page.txt').exists()

    assert mock_get_all_pages_in_space.call_count == 1
