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

import pytest
from click import BadParameter, core

from swrangler.commands import CommaSeparatedList


def test_comma_separated_list_convert():
    """Test the convert method of CommaSeparatedList."""
    param_type = CommaSeparatedList()
    ctx = core.Context(core.Command(name="test"))

    # Test conversion with a comma-separated string
    value = "key1,key2,key3"
    result = param_type.convert(value, None, ctx)
    assert result == ["key1", "key2", "key3"]

    # Test conversion with an empty string
    value = ""
    with pytest.raises(BadParameter):
        param_type.convert(value, None, ctx)

    # Test conversion with a None value
    value = None
    with pytest.raises(BadParameter):
        param_type.convert(value, None, ctx)

    # Test conversion with a list
    value = ["key1", "key2", "key3"]
    result = param_type.convert(value, None, ctx)
    assert result == ["key1", "key2", "key3"]


def test_comma_separated_list_name():
    """Test the name attribute of CommaSeparatedList."""
    param_type = CommaSeparatedList()
    assert param_type.name == "list"
