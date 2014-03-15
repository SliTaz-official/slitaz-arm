#!/bin/sh
#
# TazBerry CGI Plugin - Skeleton
#

if [ "$(GET skel)" ]; then
	html_header "Skel"
	echo "<h1>Plugin Skel</h1>"
	
	# Let's code!
	date
	
	html_footer
	exit 0
fi
