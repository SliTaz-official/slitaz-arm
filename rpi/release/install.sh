#!/bin/sh
#
# SliTaz Raspberry Pi Release - SD card installation
#
# Copyright (C) 2012-2014 SliTaz ARM - BSD License
# Author: Christophe Lincoln <pankso@slitaz.org>
#

dev="$1"
boot="/media/rpi/boot"
root="/media/rpi/rootfs"

# Only for root
if [ $(id -u) != 0 ]; then
	echo "You must be root to install TazBerry" && exit 0
fi

# Run only in a SliTaz ARM release tarball with boot/ and rootfs/
[ -d "./boot" ] || exit 1
[ -d "./rootfs" ] || exit 1

# Usage: colorize NB "Message"
colorize() {
	echo -e "\\033[1;${1}m${2}\\033[0;39m"
}

separator() {
	echo "================================================================================"
}

status() {
	if [ "$?" = 0 ]; then
		colorize 32 " OK"
	else
		colorize 31 " ERROR"
	fi
}

umount_sd() {
	umount /dev/${dev}1 2>/dev/null || exit 1
	umount /dev/${dev}3 2>/dev/null || exit 1
}

#
# Let's start
#
clear
cat << EOT

$(colorize 35 "SliTaz Raspberry Pi Installation")
$(separator)
Before processing please read the SliTaz ARM/RPi installation howto on: 

  http://arm.slitaz.org/rpi

EOT

# SD card check
[ "$dev" ] || echo -n "SD card device name (ex sdc): "; read dev
[ "$dev" ] || exit 1
if ! fdisk -l | grep -q "/dev/${dev}3"; then
	echo "Unable to find: /dev/${dev}3"; exit 1
fi

# Mount
if mount | grep -q "^/dev/$dev[1-3]"; then
	umount_sd
fi
echo -n "Mounting: /dev/$dev partitions..."
mkdir -p ${boot} ${root}
mount /dev/${dev}1 ${boot} || exit 1
mount /dev/${dev}3 ${root} || exit 1; status

# Clean up
echo -n "Cleaning: filesystem directories..."
for dir in bin dev etc lib media mnt proc sbin sys tmp usr var run
do
	rm -rf ${root}/${dir}
done; status

# Install
echo -n "Installing: boot files..."
cp -a boot/* ${boot}; status
echo -n "Installing: rootfs files..."
cp -a rootfs/* ${root}; status

# Unmount
echo -n "Unmounting: RPi sdcard..."
umount_sd; status
separator
echo "Insert the SD card into your Raspberry Pi and boot!"
echo ""
exit 0
