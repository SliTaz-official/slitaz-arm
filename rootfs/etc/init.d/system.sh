#!/bin/sh
#
# /etc/init.d/system.sh : SliTaz ARM hardware configuration
#
# This script configures the sound card and screen. It also configures
# system language, keyboard and TZ.
#
. /etc/init.d/rc.functions
. /etc/rcS.conf

# Activate swap partition
if fgrep -q "swap" /etc/fstab; then
	swapon -a
fi

# Sound configuration: restore or init
if [ -d "/proc/asound" ] && [ -x "/usr/sbin/alsactl" ]; then
	echo "Initializing sound card..."
	alsactl init
fi

# Locale config
[ -s "/etc/locale.conf" ] || echo "LANG=C" > /etc/locale.conf
. /etc/locale.conf
echo -n "Setting system locale: $LANG"
export LC_ALL=${LANG}; status

# Keymap config
[ -s "/etc/keymap.conf" ] || echo "us" > /etc/keymap.conf
kmap=$(cat /etc/keymap.conf)
echo -n "Loading console keymap: $kmap"
tazkeymap $kmap >/dev/null; status

# Timezone config
[ -s "/etc/TZ" ] || echo "UTC" > /etc/TZ
tz=$(cat /etc/TZ)
echo -n "Setting time zone to: $tz"
export TZ=${tz}; status

# For device without HW clock
if [ "$NTPD_HOST" ]; then
	echo "Syncing system time..."
	ntpd -q -p ${NTPD_HOST}; status
fi
