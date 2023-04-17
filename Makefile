.PHONY: status
status: scripts/kub_status.py website.csv
	python3 scripts/kub_status.py

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
	sed -i 's/%C3%B6/ö/g;s/%C3%BC/ü/g;s/o%CC%88/ö/g;s/u%CC%88/ü/g' $$(find transifex website -type f)
	sed -i 's/><\(div\|aside\|h3\|tr\|thead\|p\)/>\n<\1/g' `find transifex -type f`
	sed -i 's/><\/\(div\|aside\|h3\|tr\|thead\)/>\n<\/\1/g' `find transifex -type f`
	sed -i 's/\(.\)<ul>/\1\n<ul>/g' `find transifex -type f`
	sed -i 'H;1h;$$!d;x;s/\n<li>\n/\n<li>/g;s/\n<\/address>\n/<\/address>\n/g' `find transifex -type f`
	sed -i "s/&#039;/'/g" `find transifex website -type f`
	sed -i 's/&quot;/"/g' `find transifex website -type f`

.PHONY: txpull
txpull: .tx/config
	tx pull -a -f

.tx/config:
	tx init
	tx add remote --file-filter 'transifex/<resource_slug>/<lang>.<ext>' https://www.transifex.com/kub/webseite-2/dashboard/
	sed -i 's/minimum_perc  = 0/minimum_perc  = 100/g' .tx/config
	find transifex | xargs dos2unix
