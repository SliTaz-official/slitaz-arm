#/bin/sh

log=/tmp/slitaz-arm.log

echo "uname:" | tee $log
uname -a | tee -a $log

echo "ls[pci/usb]:" | tee -a $log
lspci | tee -a $log
lsusb 2>&1 | tee -a $log

echo "dmesg:"
dmesg | tee -a $log
