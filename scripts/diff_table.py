import csv
import html
import re
from pathlib import Path

LANGS = ['de', 'en', 'fr', 'es', 'tr', 'ar', 'fa', 'ru']


def html_strip(s):
    return re.sub('<[^<]+?>', '', s)


kubroot = Path('website')
txroot = Path('transifex')

for lang in LANGS:
    dir = 'rtl' if lang in ['ar', 'fa'] else 'ltr'

    with open('website.csv') as fh:
        print(f'<h1>{lang}</h1>')
        print('<table border="1">')
        for id, slug, txid in csv.reader(fh):
            if not txid:
                continue

            key = f'{int(id):03}-{slug}'
            depath = kubroot / key / 'de.html'
            if not depath.exists():
                continue

            key = f'{int(id):03}-{slug}'
            kubpath = kubroot / key / f'{lang}.html'
            if not kubpath.exists():
                continue

            txpath = txroot / txid / f'{lang}.html'
            if not txpath.exists():
                continue

            with depath.open() as fh:
                c = fh.readlines()
            with kubpath.open() as fh:
                a = fh.readlines()
            with txpath.open() as fh:
                b = fh.readlines()

            if len(a) != len(b) or len(a) != len(c):
                continue

            for s_de, s_kub, s_tx in zip(c, a, b):
                s_kub = html_strip(s_kub)
                s_de = html_strip(s_de)
                s_tx = html_strip(s_tx)
                if s_kub != s_tx:
                    print('<tr>')
                    print(f'<td dir="{dir}">{s_kub}</td>')
                    print(f'<td dir="{dir}">{s_tx}</td>')
                    print(f'<td>{s_de}</td>')
                    print('</tr>')
        print('</table>')
