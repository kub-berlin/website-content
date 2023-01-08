.PHONY: txpull
txpull: .tx/config
	tx pull -a --use-git-timestamps

.tx/config:
	tx init
	tx add remote --file-filter 'transifex/<resource_slug>/<lang>.<ext>' https://www.transifex.com/kub/webseite-2/dashboard/
	sed -i 's/minimum_perc  = 0/minimum_perc  = 100/g' .tx/config
	find transifex | xargs dos2unix
