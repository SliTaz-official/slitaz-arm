#!/bin/sh
#
# Tiny CGI SHell example for SliTaz ARM
#
# $ startd httpd
# URL: http://rpi.ip/adm/
#
echo "Content type: text/plain"
echo ""

# Only for root
[ $(id -u) == 0 ] || exit 1

cpu_temp() {
	awk '{printf "%3.1f C", $1/1000}' \
		/sys/class/thermal/thermal_zone0/temp
}

# tazberry rpi_stats
cat << EOT
SliTaz Raspberry Pi Stats
-------------------------

Kernel   : $(uname -snrm)
Uptime   :$(uptime | cut -d "," -f 1,2)
CPU Temp : $(cpu_temp)

Memory and filesystem usages
----------------------------
$(free -m)

$(df -h)

Network interfaces
------------------
$(ifconfig)
EOT
