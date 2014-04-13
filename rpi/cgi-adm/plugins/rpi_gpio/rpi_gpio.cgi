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

<pre>
$(ls $sysfs)
</pre>

<h2>Export example</h2>

<pre>
# echo 24 > $sysfs/export
# cat $sysfs/gpio24/direction
</pre>

EOT
	
		html_footer && exit 0 ;;
esac
