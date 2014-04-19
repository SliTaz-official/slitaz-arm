#!/bin/sh
#
# TazBerry CGI Plugin - Raspberry Pi GPIO settings
#

case " $(GET) " in

	*\ rpi_gpio\ *)
		sysfs="/sys/class/gpio"
		html_header "GPIO pins"
		cat << EOT
<h1>Raspberry Pi GPIO pins</h1>

<p>
	The R-Pi offers GPIO lower-level interfaces intended to connect 
	more directly with chips and subsystem modules. Documentation on the:
	<a href="http://elinux.org/RPi_Low-level_peripherals">Official Wiki</a>
</p>

<h2>$sysfs</h2>
<pre>
$(ls -1p $sysfs)
</pre>

<h2>Export example</h2>

<pre>
# echo 24 > $sysfs/export
# cat $sysfs/gpio24/direction
</pre>

EOT
	
		html_footer && exit 0 ;;
esac
