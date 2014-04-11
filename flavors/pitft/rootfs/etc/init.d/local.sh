#!/bin/sh
#
# /etc/init.d/local.sh: Local startup commands
#
# All commands here will be executed at boot time.
#

echo "Setting up PiTFP screen..."
modprobe -v fbtft_device name=adafruitts rotate=90
export FRAMEBUFFER=/dev/fb1
startd slim
