#!/bin/sh
#
# TazBerry CGI Plugin - Boot configs and options
#

case " $(GET) " in

	*\ rdate\ *)
		html_header "System time"
		echo "<h1>System time</h1>"
		echo "<pre>"
		echo -n "Old date:"; date
		rdate -s tick.greyware.com
		echo -n "New date:"; date 
		echo "</pre>" 
		html_footer && exit 0 ;;
	
	*\ oclock\ *)
		html_header "Overclocking"
		cat << EOT
<h1>RPi Overclocking</h1>

<pre>
$(/home/pankso/Projects/slitaz-arm/rpi/tazberry rpi_oclock)
</pre>

<h2>Current settings:</h2>
<pre>
$(fgrep _freq /boot/config.txt)
$(fgrep over_voltage /boot/config.txt)
</pre>

<a href='$script?editor&amp;file=/boot/config.txt'>Edit boot configuration</a>
EOT
		html_footer && exit 0 ;;
	
	*\ rpi_config\ *)
		html_header "Raspberry Pi"
		echo "<h1>SliTaz Raspberry Pi</h1>"
	
		cat << EOT

<p>
	Remotely configure your SliTaz Raspberry Pi device.
</p>

<div id="actions">
	<form method="get" action="$script">
		<input type="submit" name="rdate" value="Set system time" />
		<input type="submit" name="oclock" value="Overclocking" />
	</form>
</div>

<h2>Kernel boot parameters</h2>
<p>
	File path: /boot/cmdline.txt 
	[ <a href="$script?editor&amp;file=/boot/cmdline.txt">Edit</a> ]
</p>
<pre>
$(cat /boot/cmdline.txt 2>/dev/null)
</pre>

<h2>Boot configuration file</h2>
<p>
	File path: /boot/config.txt 
	[ <a href="$script?editor&amp;file=/boot/config.txt">Edit</a> ]
</p>
<pre>
$(cat /boot/config.txt 2>/dev/null)
</pre>

EOT
	
		html_footer && exit 0 ;;
esac
