#!/bin/sh

cat website.csv | while read l; do
	txid=$(echo "$l" | cut -d, -f 3)

	if [ "$txid" != "" ]; then
		id=$(echo "$l" | cut -d, -f 1)
		slug=$(echo "$l" | cut -d, -f 2)
		path="$(printf 'website/%03i-%s' "$id" "$slug")"
		txpath="transifex/$txid"

		if [ "$1" = "-v" ]; then
			echo "apply $path" >&2
			rm -rf "$txpath"
			cp -r "$path" "$txpath"
		else
			echo "apply $txpath" >&2
			rm -rf "$path"
			cp -r "$txpath" "$path"
			sed -i 's/ data-tx-separate="false"//g' $(find website -type f)
		fi
	fi
done
