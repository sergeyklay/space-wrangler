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

"""Provides HTML templates for rendering Confluence pages."""


def html_template(title: str, content: str) -> str:
    """Generate an HTML template for a Confluence page.

    Args:
        title (str): Title of the Confluence page.
        content (str): Content of the Confluence page.

    Returns:
        str: HTML template for the Confluence page.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <div>{content}</div>
    </body>
    </html>
    """
