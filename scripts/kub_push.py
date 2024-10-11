import os
import sys
import csv
import requests
from html import unescape
from pathlib import Path

URL = 'https://kub-berlin.org/website/admin/'
LANGS = ['de', 'en', 'fr', 'es', 'tr', 'ar', 'fa', 'ru']

root = Path('website')
auth = (os.getenv('KUB_USER'), os.getenv('KUB_PASS'))
headers = {'Cookie': 'csrf_token=' + os.getenv('KUB_CSRF_COOKIE')}


def prepare_body(html):
    lines = html.splitlines()
    assert lines[0] == '<div>'
    assert lines[-1] == '</div>'
    assert lines[1].startswith('<h1>')
    assert lines[1].endswith('</h1>')
    return {
        'title': unescape(lines[1][4:-5]),
        'body': '\n'.join(lines[2:-1]),
    }


with open('website.csv') as fh:
    for id, slug, _txid in csv.reader(fh):
        if len(sys.argv) > 1 and id != sys.argv[1]:
            continue

        key = f'{int(id):03}-{slug}'
        print(key, file=sys.stderr)
        _dir = root / key

        for lang in LANGS:
            path = _dir / f'{lang}.html'
            if not path.exists():
                continue

            requests.post(
                URL,
                params={
                    'action': 'edit-translation',
                    'page': id,
                    'lang': lang,
                },
                data={
                    'csrf_token': os.getenv('KUB_CSRF_DATA'),
                    **prepare_body(path.read_text()),
                },
                auth=auth,
                headers=headers,
            ).raise_for_status()
