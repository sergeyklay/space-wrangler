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
    limit = 100
    params = {
        'spaceKey': space_key,
        'expand': 'body.storage,ancestors,history.lastUpdated,version',
        'limit': str(limit),
        'status': 'current'
    }

    all_pages = []
    print(f'Download pages ({limit} pages per request):')
    while True:
        print('.', end='', flush=True)
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

    print('')
    print('')
    return all_pages


def get_page_path(base_dir, page):
    ancestors = page['ancestors']
    path_parts = [ancestor['title'].replace('/', '-') for ancestor in ancestors]
    path_parts.append(page['title'].replace('/', '-'))

    full_path = os.path.join(base_dir, *path_parts)
    return full_path


def save_pages_to_files(pages):
    output_dir = os.path.join(os.path.dirname(__file__), 'output')

    template_path = os.path.join(os.path.dirname(__file__), 'template.html')
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template = template_file.read()

    print('Render pages:')
    for page in pages:
        html_path = get_page_path(os.path.join(output_dir, 'html'), page)
        json_path = get_page_path(os.path.join(output_dir, 'json'), page)

        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

        content = template.format(title=page['title'], content=page['body']['storage']['value'])

        with open(f"{html_path}.html", 'w', encoding='utf-8') as file:
            file.write(content)

        with open(f"{json_path}.json", 'w', encoding='utf-8') as file:
            json.dump(page, file, ensure_ascii=False, indent=4)

        print('.', end='', flush=True)
    print('')
    print('')


if __name__ == "__main__":
    result = get_all_pages_in_space(os.getenv('CONFLUENCE_SPACE_KEY'))
    save_pages_to_files(result)
    print(f"Total {len(result)} pages downloaded.")
