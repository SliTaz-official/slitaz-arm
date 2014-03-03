#!/bin/sh
#
# /etc/init.d/shutdown.sh: System shutdown or reboot script
#
# Copyright (C) 2012 SliTaz ARM - BSD License
#
. /lib/libtaz.sh
. /etc/rcS.conf

# Messages
newline
boldify "System is going down for reboot or halt..."
colorize 32 $(uptime)

# Store last alsa settings
#if [ -x /usr/sbin/alsactl ]; then
	#alsactl store
#fi

# Stop all daemons started at boot time
if [ "$RUN_DAEMONS" ]; then
	colorize 33 "Stopping all daemons..."
	for daemon in $RUN_DAEMONS; do
		/etc/init.d/$daemon stop
	done
fi

# Sync all filesystems
sync

# Swap off
/sbin/swapoff -a

# Kill all processes
killall5

# Umount filesystems
/bin/umount -a -r 2>/dev/null
