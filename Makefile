.PHONY: kubpull
kubpull: scripts/kub_pull.py .env website.csv
	env $$(cat .env | xargs) python3 scripts/kub_pull.py
	find website | xargs dos2unix

.PHONY: kubpush
kubpush: scripts/kub_push.py .env website.csv
	env $$(cat .env | xargs) python3 scripts/kub_push.py

.PHONY: normalize
normalize:
	find transifex website -type f | xargs dos2unix
	sed -i 's/%C3%B6/ö/g;s/%C3%BC/ü/g;s/o%CC%88/ö/g;s/u%CC%88/ü/g' $$(find transifex website -type f)

.PHONY: txpull
txpull: .tx/config
	tx pull -a --use-git-timestamps

.tx/config:
	tx init
	tx add remote --file-filter 'transifex/<resource_slug>/<lang>.<ext>' https://www.transifex.com/kub/webseite-2/dashboard/
	sed -i 's/minimum_perc  = 0/minimum_perc  = 100/g' .tx/config
	find transifex | xargs dos2unix
