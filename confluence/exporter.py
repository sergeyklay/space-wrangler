# This file is part of the confluence.
#
# Copyright (c) 2024 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import csv
import json
import os
import re
from datetime import datetime
from urllib.parse import parse_qs, urlparse

import requests
from requests.auth import HTTPBasicAuth

from .template import html_template

base_url = 'https://pdffiller.atlassian.net/wiki/rest/api'


def get_all_pages_in_space(space_key):
    """Retrieve all pages for a given space key from Confluence."""
    url = f"{base_url}/content"
    limit = 100

    headers = {
        'Accept': 'application/json',
    }

    params = {
        'spaceKey': space_key,
        'expand': 'body.storage,ancestors,history.lastUpdated,version',
        'limit': str(limit),
        'status': 'current',
    }

    auth = HTTPBasicAuth(
        os.getenv('CONFLUENCE_API_USER'),
        os.getenv('CONFLUENCE_API_TOKEN'),
    )

    all_pages = []
    print(f'Fetch space pages ({limit} pages per request):')
    while True:
        print('.', end='', flush=True)
        response = requests.get(url, params=params, auth=auth, headers=headers)
        response.raise_for_status()
        data = response.json()

        all_pages.extend(data['results'])

        if 'next' in data['_links']:
            next_url = data['_links']['next']
            parsed_url = urlparse(next_url)
            query_params = parse_qs(parsed_url.query)

            for key, value in query_params.items():
                params.update({key: value[0] if len(value) == 1 else value})
        else:
            break

    print('')
    print('')
    return all_pages


def get_page_path(base_dir, page):
    ancestors = page['ancestors']
    path_parts = [parent['title'].replace('/', '-') for parent in ancestors]
    path_parts.append(page['title'].replace('/', '-'))

    full_path = os.path.join(base_dir, *path_parts)
    return full_path


def save_pages_to_files(pages, output_dir='./output'):
    print('Render pages:')
    for page in pages:
        html_path = get_page_path(os.path.join(output_dir, 'html'), page)
        json_path = get_page_path(os.path.join(output_dir, 'json'), page)

        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

        content = html_template(
            title=page['title'],
            content=page['body']['storage']['value'])

        with open(f"{html_path}.html", 'w', encoding='utf-8') as file:
            file.write(content)

        with open(f"{json_path}.json", 'w', encoding='utf-8') as file:
            json.dump(page, file, ensure_ascii=False, indent=4)

        print('.', end='', flush=True)
    print('')
    print('')


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_obj.strftime('%m/%d/%Y')


def contains_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))


def get_structured_title(page):
    ancestors = page['ancestors']
    path_parts = []

    for parent in ancestors:
        path_parts.append('/' + parent['title'].replace('/', '-'))

    path_parts.append('/' + page['title'].replace('/', '-'))

    return ''.join(path_parts)


def save_pages_to_csv(pages, output_dir):
    csv_path = os.path.join(output_dir, 'pages-metadata.csv')

    rows = []
    for page in pages:
        page_id = page['id']
        title = get_structured_title(page)
        created_date = format_date(page['history']['createdDate'])
        last_updated_date = format_date(page['history']['lastUpdated']['when'])
        last_editor = page['history']['lastUpdated']['by']['displayName']
        current_owner = page['version']['by']['displayName']
        page_url = base_url.replace('/rest/api', '') + page['_links']['webui']

        content = page['body']['storage']['value']
        content_is_english = not contains_cyrillic(content)
        title_is_english = not contains_cyrillic(page['title'])

        rows.append({
            'Page ID': page_id,
            'Page Title': title,
            'Title in English': title_is_english,
            'Content in English': content_is_english,
            'Created Date': created_date,
            'Last Updated Date': last_updated_date,
            'Last Editor': last_editor,
            'Current Owner': current_owner,
            'Page URL': page_url
        })

    rows.sort(key=lambda x: x['Page Title'])

    fieldnames = [
        'Page ID',
        'Page Title',
        'Title in English',
        'Content in English',
        'Created Date',
        'Last Updated Date',
        'Last Editor',
        'Current Owner',
        'Page URL',
    ]

    with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file saved to {csv_path}")


def export_space(space_key, output_dir):
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    result = get_all_pages_in_space(space_key)
    save_pages_to_files(result, output_dir)
    print(f"Total {len(result)} pages downloaded.")


def export_pages_metadata(space_key, output_dir):
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    result = get_all_pages_in_space(space_key)
    save_pages_to_csv(result, output_dir)
    print(f"Metadata for {len(result)} pages downloaded and saved to CSV.")
