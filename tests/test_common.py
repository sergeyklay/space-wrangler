# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from confluence.common import (
    check_unlicensed_or_deleted,
    CONFLUENCE_BASE_URL,
    format_text,
    get_page_path,
    path,
    people_url,
)


def test_format_text():
    html_content = """\n\n\n
    <p>Test with&nbsp;non-breaking&nbsp;spaces.</p>
    <p>Second paragraph.</p>\n\n\n\n
    """
    expected_output = "Test with non-breaking spaces.\nSecond paragraph."
    assert format_text(html_content) == expected_output


def test_format_text_line_length():
    html_content = "<p>" + "a" * 100 + "</p>"
    output = format_text(html_content)
    lines = output.split('\n')
    assert all(len(line) <= 80 for line in lines)


def test_format_text_with_empty_lines():
    html_content = """
    <p>First paragraph.</p>
    <p></p>
    <p>Second paragraph.</p>
    <p></p>
    <p></p>
    <p>Third paragraph.</p>
    """
    expected_output = (
        "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    )
    assert format_text(html_content) == expected_output


def test_format_text_preserves_single_empty_line():
    html_content = """
    <p>First paragraph.</p>
    <p></p>
    <p>Second paragraph.</p>
    """
    expected_output = "First paragraph.\n\nSecond paragraph."
    assert format_text(html_content) == expected_output


def test_format_text_wrap_long_lines():
    html_content = (
        "<p>This is a very long line that should be wrapped into multiple "
        "lines because it exceeds eighty characters in length.</p>"
    )
    expected_output = (
        "This is a very long line that should be wrapped into multiple "
        "lines because it\nexceeds eighty characters in length."
    )
    assert format_text(html_content) == expected_output


def test_format_text_with_empty_content():
    html_content = "<p></p><p></p>"
    expected_output = ""
    assert format_text(html_content) == expected_output


def test_format_text_with_code_block():
    html_content = """
    <p>Lorem ipsum dolor sit amet,</p>
    <p>consectetur adipiscing elit:</p>
    <ac:structured-macro ac:name="code" ac:macro-id="...">
        <ac:parameter ac:name="language">json</ac:parameter>
        <p>{
        "document":{
            "doc_gen_fields":[],
            "doc_gen_content":[],
            "content":{}
        }</p>
    </ac:structured-macro>
    <p>Sed eu iaculis nisi.</p>
    """
    expected_output = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit:

{
        "document":{
            "doc_gen_fields":[],
            "doc_gen_content":[],
            "content":{}
        }

Sed eu iaculis nisi."""
    assert format_text(html_content) == expected_output


def test_people_url():
    people_id = '5b8e8643632a6b2c8f80b883'
    expected_url = f'{CONFLUENCE_BASE_URL}/people/{people_id}'
    assert people_url(people_id) == expected_url


def test_get_page_path():
    page = {
        'ancestors': [{'title': 'Parent Page'}],
        'title': 'Test Page'
    }
    path = get_page_path('/base/dir', page)
    assert path == '/base/dir/Parent Page/Test Page'


def test_check_unlicensed_or_deleted():
    assert check_unlicensed_or_deleted('John Doe (Unlicensed)') == 'TRUE'
    assert check_unlicensed_or_deleted('Jane Doe (Deleted)') == 'TRUE'
    assert check_unlicensed_or_deleted('John Doe') == 'FALSE'


@pytest.mark.parametrize(
    'search,expected',
    [
        ('a', {'b': {'c': {'d': 42}}}),
        ('a.b', {'c': {'d': 42}}),
        ('a.b.c', {'d': 42}),
        ('a.b.c.d', 42),
        ('a.z.c.d', None),
        ('a.b.c.z', None),
        ('z.y.z', None),
        ('42', None),
    ])
def test_path(search, expected):
    my_dict = {'a': {'b': {'c': {'d': 42}}}}

    if expected is None:
        assert path(my_dict, search) is expected
    else:
        assert path(my_dict, search) == expected
