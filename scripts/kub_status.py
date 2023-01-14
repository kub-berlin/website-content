import sys
import csv
import filecmp
from pathlib import Path

LANGS = ['de', 'en', 'fr', 'es', 'tr', 'ar', 'fa', 'ru']

kubroot = Path('website')
txroot = Path('transifex')

source_missing = []
source_differ = []
translation_differ = []
translation_orphan = []
translation_available = []


def add_orphan(path):
    with open(path) as fh:
        if len(fh.readlines()) > 4:
            translation_orphan.append(path)


with open('website.csv') as fh:
    for id, slug, txid in csv.reader(fh):
        key = f'{int(id):03}-{slug}'

        for lang in LANGS:
            kubpath = kubroot / key / f'{lang}.html'

            if lang == 'de' and not kubpath.exists():
                source_missing.append(kubpath)

            if txid:
                txpath = txroot / txid / f'{lang}.html'

                if lang == 'de':
                    txpath = txroot / txid / f'{lang}.html'
                    if not txpath.exists():
                        source_missing.append(txpath)
                    elif kubpath.exists() and not filecmp.cmp(kubpath, txpath):
                        source_differ.append((kubpath, txpath))
                else:
                    if kubpath.exists() and txpath.exists():
                        if not filecmp.cmp(kubpath, txpath):
                            translation_differ.append((kubpath, txpath))
                    elif kubpath.exists():
                        add_orphan(kubpath)
                    elif txpath.exists():
                        translation_available.append(kubpath)
            else:
                if lang != 'de' and kubpath.exists():
                    add_orphan(kubpath)


for label, paths, color in [
    ('missing source files', source_missing, 0),
    ('different source files', source_differ, 2),
    ('different translations', translation_differ, 2),
    ('translations on website that do not exist in transifex', translation_orphan, 5),
    ('translations on transifex that are not yet on website', translation_available, 1),
]:
    if paths:
        print('>>', label, f'\x1b[{31 + color}m')
        for path in sorted(paths):
            if isinstance(path, tuple):
                print(*path)
            else:
                print(path)
        print('\x1b[0m')

if any([
    source_missing,
    source_differ,
    translation_differ,
    translation_orphan,
    translation_available,
]):
    sys.exit(1)
