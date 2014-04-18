#!/bin/sh
#
# Create SliTaz PiTFT Linux Kernel package
#
# See: https://github.com/adafruit/adafruit-rpi-fbtft/
#
. /lib/libtaz.sh

cache="rpi/cache"
kvers="3.6.11"
tarball="linux-$kvers.tar.xz"
kurl="ftp://www.kernel.org/pub/linux/kernel/v3.x/$tarball"
install="$cache/linux-$vers-install"
: ${arch=arm}

cd ${cache} || exit 1

# Get source
echo "Checking for: $tarball"
[ -f "$tarball" ] || wget ${kurl}
[ -d "linux-$kvers" ] || tar xJf ${tarball}
cd linux-$kvers

# FBtft drivers
if [ ! -d "drivers/video/fbtft" ]; then
	cd drivers/video
	git clone git://github.com/notro/fbtft.git
	cd ../..
	echo 'source "drivers/video/fbtft/Kconfig"' >> drivers/video/Kconfig
	echo 'obj-y += fbtft/' >> drivers/video/Makefile
fi

export PATH=$PATH:/cross/${arch}/tools/bin
export HOST_SYSTEM=${arch}-slitaz-linux-gnueabi

# Clean source and get config
#make mrproper &&
#cp -f ../../data/linux-pitft.config .config || exit 1
#yes "" | make ARCH=arm oldconfig

# Handle --gconfig
[ "$gconfig" ] && make ARCH=arm gconfig

# Cook it!
make ARCH=arm CROSS_COMPILE=${HOST_SYSTEM}- zImage &&
make ARCH=arm CROSS_COMPILE=${HOST_SYSTEM}- modules &&
make ARCH=arm CROSS_COMPILE=${HOST_SYSTEM}- \
	INSTALL_MOD_PATH=${install} modules_install || exit 1
mkdir -p ${install}/boot
cp -a arch/arm/boot/zImage ${install}/boot/kernel.img

# Pack it!

exit 0
