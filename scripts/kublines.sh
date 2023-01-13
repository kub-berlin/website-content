#!/bin/sh

ls website | while read d; do
	lines=$(wc -l "website/$d/de.html" | cut -d' ' -f 1)
	ls "website/$d/" | while read f; do
		lines2=$(wc -l "website/$d/$f" | cut -d' ' -f 1)
		if [ $lines != $lines2 ] && [ $lines2 -gt 4 ]; then
			echo "website/$d/$f"
		fi
	done
done
