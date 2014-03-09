#!/bin/sh
#
# Sleep to avoid: "kernel still uses old table: Device or resource busy"
#
. /lib/libtaz.sh
check_root

if [ ! "$dev" ]; then
	echo "Missing: --dev= cmdline option" && exit 1
fi

# Boot
echo -n "Creating partition: /dev/${dev}1 /boot"
fdisk /dev/${dev} >/dev/null << EOF
o
n
p
1
1
+140M
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

# Mkfs 2>&1 >/dev/null
#if fdisk -l /dev/${dev} | grep "^/dev/${dev}1"; then
	#debug "Creating: /boot FAT32 filesystem"
	#mkdosfs -F 32 -v -l -n "RPi-boot" /dev/${dev}1 
#fi
#if fdisk -l /dev/${dev} | grep "^/dev/${dev}2"; then
	#debug "Creating: swap memory filesystem"
	#mkswap -L "RPi-swap" /dev/${dev}2
#fi
#if fdisk -l /dev/${dev} | grep "^/dev/${dev}3"; then
	#debug "Creating: root ext4 filesystem"
	#mkfs.ext4 -L "RPi-root" /dev/${dev}3
#fi
