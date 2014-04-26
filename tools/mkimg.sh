#!/bin/sh
#
# Create slitaz-arm.img
#
. /lib/libtaz.sh

[ "$size" ] || size=80

distro="distro"
. $distro/rootfs/etc/slitaz/flavor.conf || exit 1
flavor="$FLAVOR"
#img="slitaz-$flavor-$(date +%Y%m%d)"
img=slitaz-arm.img

cd ${distro}
echo "Creating disk image..."
dd if=/dev/zero of=${img} bs=1M count=${size}

device=$(kpartx -va $img | sed -E 's/.*(loop[0-9])p.*/\1/g' | head -1)
device="/dev/mapper/${device}"
bootp=${device}p1
rootp=${device}p2
