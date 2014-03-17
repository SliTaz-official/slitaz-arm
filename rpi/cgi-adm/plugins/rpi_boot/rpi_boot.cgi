#!/bin/sh
#
# TazBerry CGI Plugin - Boot configs and options
#

if [ "$(GET rpi_boot)" ]; then
	html_header "Boot"
	echo "<h1>SliTaz Raspberry Pi Boot</h1>"
	
	cat << EOT
<p>
	The Raspberry Pi uses 2 config files to boot. The default SliTaz RPi 
	Linux kernel image is: /boot/kernel.img
</p>

<pre>

Kernel boot parameters [ <a href="$script?editor&amp;file=/boot/cmdline.txt">Edit</a> ]
--------------------------------------------------------------------------------
$(cat /boot/cmdline.txt 2>/dev/null)


RPi configuration file [ <a href="$script?editor&amp;file=/boot/config.txt">Edit</a> ]
--------------------------------------------------------------------------------
$(cat /boot/config.txt 2>/dev/null)


Boot files
--------------------------------------------------------------------------------
$(ls -1 /boot)
</pre>

EOT
	
	html_footer
	exit 0
fi
