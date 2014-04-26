#!/bin/sh
#
# TazBerry CGI SHell Admin tool. Fast, pure SHell, small core with
# plugins support. Auth is done via a HTTP server such as Busybox httpd.
#
# Copyright (C) 2012-2014 SliTaz ARM - BSD License
# Author: Christophe Lincoln <pankso@slitaz.org>
#
. /lib/libtaz.sh
. /usr/lib/slitaz/httphelper.sh

# Only for root
check_root

plugins="$(pwd)/plugins"
script="$SCRIPT_NAME"
data="$(pwd)/data"
cache="$(pwd)/cache"

#
# Functions
#

# Usage: html_header "title"
html_header() {
	header
	cat ${data}/header.html | sed s"/_TITLE_/$1/"
}

html_footer() {
	cat << EOT
</section>
<footer id="footer">
	&copy; $(date +%Y) <a href="http://arm.slitaz.org/">SliTaz ARM</a>
</footer>
</body>
</html>
EOT
}

# Usage: notify [hide|"Message..."]
notify() {
	if [ "$1" == "hide" ]; then
		echo "<style type='text/css'>#notify { display: none !important; }</style>"
	else
		echo "<div id='notify'>$@</div>"
	fi
}

list_plugins() {
	for p in $(ls -1 $plugins)
	do
		. ${plugins}/${p}/${p}.conf
	cat << EOT
<div><b><a href="$script?$p">$PLUGIN</a></b></div>
<pre>
Description : $SHORT_DESC
Website     : <a href="$WEB_SITE">${WEB_SITE#http://}</a>
</pre>
EOT
		unset PLUGIN SHORT_DESC MAINTAINER WEB_SITE
	done
}

# The only sys functions, everything else must go in plugins :-)
sys_tools() {
	ip=$(ifconfig | fgrep -A 1 "encap:Ethernet" | fgrep "inet" | cut -d ":" -f 2)
	#iface=$(ifconfig | fgrep "encap:Ethernet" | awk '{print $1}')
	mem_total=$(free -m | fgrep "Mem:" | awk '{print $2}')
	mem_used=$(free -m | fgrep "Mem:" | awk '{print $3}')
	mem_used_pct=$(( ( ${mem_used} * 100) / ${mem_total} ))
	cat << EOT
<pre>
System time  : $(date)
Time zone    : $(cat /etc/TZ)
Kernel       : $(uname -snrm)
Uptime       : $(uptime | awk '{print $3}' | sed s"/:/h /" | sed s"/,/min/")
Network IP   : $(echo $ip | awk '{print $1}')
CPU heat     : $(awk '{printf "%3.1f C\n", $1/1000}' /sys/class/thermal/thermal_zone0/temp)
Processes    : $(ps | wc -l)
Memory usage : ${mem_used_pct}%
CPU usage    : $(top -n 1 | grep ^CPU: | awk '{print $4}')
</pre>

<div id="actions">
	<form method="get" action="$script">
		<input type="submit" name="reboot" value="Reboot system" />
		<input type="submit" name="halt" value="Halt system" />
		<input type="submit" name="rdate" value="Set system time" />
	</form>
</div>
EOT
}

#
# Handle plugins
#
for p in $(ls -1 plugins)
do
	[ -f "$plugins/$p/$p.conf" ] && . $plugins/$p/$p.conf
	[ -x "$plugins/$p/$p.cgi" ] && . $plugins/$p/$p.cgi
done

#
# Handle GET actions
#

case " $(GET) " in
	*\ reboot\ *) reboot ;;
	*\ halt\ *) halt ;;
	
	*\ plugins\ *)
		html_header "Plugins"
		echo "<h1>Plugins list</h1>"
		list_plugins
		html_footer ;;
	
	*\ rdate\ *)
		html_header "System time"
		echo "<h1>System time</h1>"
		echo "<pre>"
		echo -n "Old date: "; date
		rdate -s tick.greyware.com
		echo -n "New date: "; date 
		echo "</pre>" 
		html_footer && exit 0 ;;
	
	*)
		html_header "Admin"
		echo "<h1>System admin</h1>"
		sys_tools
		html_footer ;;
esac
