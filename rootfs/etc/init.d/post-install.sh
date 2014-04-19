#!/bin/sh
#
# /etc/init.d/post-install.sh: SliTaz ARM post installation script
#
# Copyright (C) 2014 SliTaz ARM - BSD License
#
. /lib/libtaz.sh

# Exit fbs
if [ -f "/fbs.fifo" ]; then
	echo "exit" > /fbs.fifo && rm -f /fbs.fifo
	usleep 500000
fi

# Welcome/About
slitaz-config about_post_install

[ -s /etc/keymap.conf ] || tazkeymap
#[ -s /etc/locale.conf ] || tazlocale

slitaz-config root_passwd
slitaz-config add_user
#dialog --yesno "$user account was created. Do you want X autologin ?"
#dialog --yesno "Do you wish to setup a network connection ?"
#slitaz-config network_connection

# No post install on next boot.
mkdir -p /var/lib/slitaz
echo "$ARCH" > /var/lib/slitaz/post-install

# Run packages post_install since when we generate a distro from
# an i486 machine we can't chroot and run ARM binaries. If we don't
# run some post_install we will miss gtk icon, pango modules, etc...
clear && newline
colorize 33 "Reconfiguring all SliTaz packages..."
spk reconf --all
