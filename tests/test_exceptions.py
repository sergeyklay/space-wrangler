# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from confluence.exceptions import ConfigurationError


def test_configuration_error_both_missing():
    with pytest.raises(ConfigurationError) as excinfo:
        raise ConfigurationError(None, None)
    assert 'Confluence API user and token are not set' in str(excinfo.value)
    message = 'Please set both CONFLUENCE_API_USER and CONFLUENCE_API_TOKEN'
    assert message in str(excinfo.value)


def test_configuration_error_user_missing():
    with pytest.raises(ConfigurationError) as excinfo:
        raise ConfigurationError(None, 'token')
    assert 'Confluence API user is not set' in str(excinfo.value)
    assert 'Please set CONFLUENCE_API_USER' in str(excinfo.value)


def test_configuration_error_token_missing():
    with pytest.raises(ConfigurationError) as excinfo:
        raise ConfigurationError('user', None)
    assert 'Confluence API token is not set' in str(excinfo.value)
    assert 'Please set CONFLUENCE_API_TOKEN' in str(excinfo.value)
