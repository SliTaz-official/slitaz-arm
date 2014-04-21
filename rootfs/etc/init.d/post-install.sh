#!/bin/sh
#
# /etc/init.d/post-install.sh: SliTaz ARM post installation script
#
# Copyright (C) 2014 SliTaz ARM - BSD License
#
. /lib/libtaz.sh

# Be sure fbs is not running
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

# Wireless ?
if ifconfig -a | grep "wlan[0-9]"; then
	dialog --title "{ Network config }" \
		--yesno "\nDo you wish to setup a Wi-Fi network connection ?" 10 72
	opt=$?
	echo $opt
	[ "$?" == "0" ] && slitaz-config wifi_setup
fi

# No post install on next boot.
mkdir -p /var/lib/slitaz
echo "$ARCH" > /var/lib/slitaz/post-install

# Run packages post_install since when we generate a distro from
# an i486 machine we can't chroot and run ARM binaries. If we don't
# run some post_install we will miss gtk icon, pango modules, etc...
# Keep it here since reconf can be run from cmdline and advanced users.
# Anyway, after a this post install is finish everthing will be handle
# by spk or tazpkg.
#
{
	echo "XXX" && echo 0
	echo -e "\nPreparing packages config...\n"
	echo "XXX" && sleep 1
	db=/var/lib/tazpkg/installed
	installed=$(ls $db | wc -l)
	
	# Get the % alocated for each pkgs and split % left. We use 4% to 
	# start so 96% is for packages.
	echo "XXX" && echo 5
	echo -e "\nInstalled packages to check: \Zb\Z2$installed"
	echo "XXX"
	total=$(grep "^post_install" ${db}/*/receipt | wc -l)
	pkgpct=$((100 / ${total}))
	left=$((100 - (${pkgpct} * ${total})))
	split=$((${left} / 2))
	[ "$pkgpct" == 0 ] && pkgpct=1 # If too much installed pkgs
	sleep 2
	
	# Show pkgs to configure a few sec
	echo "XXX" && echo ${split}
	echo -e "\nPackages to configure: \Zb\Z2$total"
	echo "XXX" && sleep 3
	
	# Run all these post_install
	pct="$split"
	for pkg in ${db}/*
	do
		receipt="$pkg/receipt"
		[ ! -f "$receipt" ] && continue
		if grep -q ^post_install ${receipt}; then
			# If we run on a system with <1000 packages...
			[ "$pct" == 100 ] && pct=0
			pct=$(($pct + $pkgpct))
			echo "XXX" && echo ${pct}
			echo -e "\nConfiguring: $(basename $pkg)"
			echo "XXX"
			. ${receipt}
			post_install >/dev/null 2>&1
			#usleep 250000
		fi
	done
	
	echo "XXX" && echo 100
	echo -e "\nAll packages are configured..."
	echo "XXX" && sleep 2
} | dialog --title "{ Packages Post Install }" --colors --gauge "" 8 72 0

exit 0
