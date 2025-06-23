import os
import sys
import csv
import requests
from pathlib import Path

URL = 'https://kub-berlin.org/website/admin/translatable.php'
LANGS = ['de', 'en', 'fr', 'es', 'tr', 'ar', 'fa', 'ru']

root = Path('website')
headers = {
    'Authorization': f'Bearer {os.getenv("KUB_TOKEN")}',
}

with open('website.csv') as fh:
    for id, slug, _txid in csv.reader(fh):
        key = f'{int(id):03}-{slug}'
        print(key, file=sys.stderr)
        _dir = root / key
        _dir.mkdir(parents=True, exist_ok=True)

        for lang in LANGS:
            r = requests.get(URL, params={'page': id, 'lang': lang}, headers=headers)
            if r.status_code == 404:
                continue
            r.raise_for_status()

            path = _dir / f'{lang}.html'
            path.write_text(r.text)
