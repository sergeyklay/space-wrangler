# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provides HTML templates for rendering Confluence pages."""


def html_template(title, content):
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
