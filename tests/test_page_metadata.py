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

from swrangler.page_metadata import export_pages_metadata, save_pages_to_csv


def test_save_pages_to_csv(tmpdir, mock_response):
    pages = mock_response.json()["results"]
    output_dir = tmpdir.mkdir("output")
    save_pages_to_csv(pages, "AIR", str(output_dir))
    csv_file = output_dir.join("AIR/csv/pages-metadata.csv")
    assert csv_file.exists()


def test_export_pages_metadata(mocker, tmpdir, mock_response):
    mock_object = "swrangler.confluence.Confluence.get_all_pages_in_space"
    mock_get_all_pages_in_space = mocker.patch(mock_object)
    mock_get_all_pages_in_space.return_value = mock_response.json()["results"]

    output_dir = tmpdir.mkdir("output")
    export_pages_metadata("AIR", str(output_dir))
    csv_file = output_dir.join("AIR/csv/pages-metadata.csv")

    assert csv_file.exists()
    assert mock_get_all_pages_in_space.call_count == 1
