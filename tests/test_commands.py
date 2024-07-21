# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that был distributed with this source code.

import pytest
from click import BadParameter, core

from confluence.commands import CommaSeparatedList


def test_comma_separated_list_convert():
    """Test the convert method of CommaSeparatedList."""
    param_type = CommaSeparatedList()
    ctx = core.Context(core.Command(name='test'))

    # Test conversion with a comma-separated string
    value = 'key1,key2,key3'
    result = param_type.convert(value, None, ctx)
    assert result == ['key1', 'key2', 'key3']

    # Test conversion with an empty string
    value = ''
    with pytest.raises(BadParameter):
        param_type.convert(value, None, ctx)

    # Test conversion with a None value
    value = None
    with pytest.raises(BadParameter):
        param_type.convert(value, None, ctx)

    # Test conversion with a list
    value = ['key1', 'key2', 'key3']
    result = param_type.convert(value, None, ctx)
    assert result == ['key1', 'key2', 'key3']


def test_comma_separated_list_name():
    """Test the name attribute of CommaSeparatedList."""
    param_type = CommaSeparatedList()
    assert param_type.name == 'list'
