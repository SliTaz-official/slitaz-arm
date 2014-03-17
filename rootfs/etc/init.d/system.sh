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
if [ -d /proc/asound ]; then
	if [ -s /var/lib/alsa/asound.state ]; then
		echo -n "Restoring sound configuration..."
		alsactl restore; status
	else
		echo -n "Initializing sound card..."
		alsactl init
	fi
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

# Xorg configuration: $HOME is not yet set
if [ ! -s /etc/X11/xorg.conf ] && [ -x /usr/bin/Xorg ]; then
	echo "Configuring Xorg server..." && HOME="/root"
	tazx config-xorg 2>/var/log/xorg.configure.log
fi
