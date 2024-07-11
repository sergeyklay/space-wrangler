import json
import os
from urllib.parse import urlparse, parse_qs

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

base_url = 'https://pdffiller.atlassian.net/wiki/rest/api'
auth = HTTPBasicAuth(
    os.getenv('CONFLUENCE_API_USER'),
    os.getenv('CONFLUENCE_API_TOKEN'),
)


def get_all_pages_in_space(space_key):
    url = f"{base_url}/content"
    params = {
        'spaceKey': space_key,
        'expand': 'body.storage',
        'limit': '100',
        'status': 'current'
    }

    all_pages = []
    while True:
        response = requests.get(url, params=params, auth=auth)
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

    return all_pages


def save_pages_to_files(pages):
    output_dir = os.path.join(os.path.dirname(__file__), 'output')

    html_dir = os.path.join(output_dir, 'html')
    os.makedirs(html_dir, exist_ok=True)

    json_dir = os.path.join(output_dir, 'json')
    os.makedirs(json_dir, exist_ok=True)

    for page in pages:
        title = page['title']
        content = page['body']['storage']['value']

        html_filename = os.path.join(html_dir, f"{title}.html".replace('/', '-'))
        json_filename = os.path.join(json_dir, f"{title}.json".replace('/', '-'))

        with open(html_filename, 'w', encoding='utf-8') as file:
            file.write(content)

        with open(json_filename, 'w', encoding='utf-8') as file:
            json.dump(page, file, ensure_ascii=False, indent=4)

        print('.', end='', flush=True)
    print('')


if __name__ == "__main__":
    result = get_all_pages_in_space('AIR')
    save_pages_to_files(result)
    print(f"Total {len(result)} pages downloaded.")
