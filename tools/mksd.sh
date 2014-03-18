#!/bin/sh
#
# Sleep to avoid: "kernel still uses old table: Device or resource busy"
#
# TODO: handle part number: --part=3 since Raspberry Pi needs 3 parts with
# a first FAT32 and Cubie Board only 2 (with / swap) or 1 single part.
#
. /lib/libtaz.sh
check_root

dev="$1"
[ ! "$dev" ] && echo "Missing device name: $0 dev" && exit 1
if ! fdisk -l | grep -q "/dev/${dev}"; then
	echo "Unable to find: /dev/${dev}"; exit 1
fi

# Boot: min 33Mb for FAT32
echo -n "Creating partition: /dev/${dev}1 /boot"
fdisk /dev/${dev} >/dev/null << EOF
o
n
p
1
1
+40M
w
EOF
status

# Swap
echo -n "Creating partition: /dev/${dev}2 swap"
sleep 2
fdisk /dev/${dev} 2>&1 >/dev/null  << EOF
n
p
2

+420M
w
EOF
status

# Root
echo -n "Creating partition: /dev/${dev}3 / (root)"
sleep 2
fdisk /dev/${dev} 2>&1 >/dev/null << EOF
n
p
3


w
EOF
status

# Boot flag
echo -n "Setting boot flag on: /dev/${dev}1"
sleep 2
fdisk /dev/${dev} 2>&1 >/dev/null << EOF
a
1
w
EOF
status

[ "$nofs" ] && exit 0

# Mkfs: Buggy fat32
if fdisk -l /dev/${dev} | grep -q "^/dev/${dev}1"; then
	echo -n "Creating: /boot FAT32 filesystem"
	mkfs.fat -v -F32 -I -n "           " /dev/${dev}1 \
		2>>/tmp/mksd.log >/tmp/mksd.log; status
fi
if fdisk -l /dev/${dev} | grep -q "^/dev/${dev}2"; then
	echo -n "Creating: swap memory filesystem"
	mkswap /dev/${dev}2 >>/tmp/mksd.log; status
fi
if fdisk -l /dev/${dev} | grep -q "^/dev/${dev}3"; then
	fs="ext4"
	[ "$btrfs" ] && fs="btrfs -f" 
	echo -n "Creating: root $fs filesystem"
	mkfs.${fs} -L "SliTazSD" /dev/${dev}3 \
		2>>/tmp/mksd.log >>/tmp/mksd.log
	status
fi

exit 0
