#!/bin/sh
#
# TazBerry CGI Plugin - Raspberry Pi configuration
#

case " $(GET) " in

	*\ leds\ *)
		trigger="/sys/class/leds/led0/trigger"
		brightness="/sys/class/leds/led0/brightness"
		html_header "Leds"
		case " $(GET leds) " in
			*\ act_test\ *) 
				echo "1" > ${brightness} 
				sleep 2; echo "0" > ${brightness} ;;
			*\ act_on\ *) 
				echo "1" > ${brightness} ;;
			*\ act_off\ *) 
				echo "0" > ${brightness} ;;
		esac
		cat << EOT
<h1>Leds</h1>
<pre>
Trigger    : $(cat $trigger)
Brightness : $(cat $brightness)
</pre>
<div class="button">
	<a href="$script?leds=act_on">ACT Test</a>
	<a href="$script?leds=act_on">ACT On</a>
	<a href="$script?leds=act_off">ACT Off</a>
</div>
EOT
		html_footer && exit 0 ;;
	
	*\ rdate\ *)
		html_header "System time"
		echo "<h1>System time</h1>"
		echo "<pre>"
		echo -n "Old date: "; date
		rdate -s tick.greyware.com
		echo -n "New date: "; date 
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
<div class="button">
	<a href='$script?editor&amp;file=/boot/config.txt'>Edit boot configuration</a>
<div>
EOT
		html_footer && exit 0 ;;
	
	*\ rpi_config\ *)
		html_header "Raspberry Pi"
		cat << EOT
<h1>SliTaz Raspberry Pi</h1>

<p>
	Remotely configure your SliTaz Raspberry Pi device.
</p>

<div id="actions">
	<form method="get" action="$script">
		<input type="submit" name="rdate" value="Set system time" />
		<input type="submit" name="oclock" value="Overclocking" />
		<input type="submit" name="leds" value="Leds" />
	</form>
</div>

<h2>Kernel boot parameters</h2>
<p>
	This file provide the Linux Kernel boot time parameter and SliTaz
	boot time options.
</p>
<pre>
$(cat /boot/cmdline.txt 2>/dev/null)
</pre>
<div class="button">
	<a href="$script?editor&amp;file=/boot/cmdline.txt">Edit cmdline.txt</a>
</div>

<h2>Boot configuration file</h2>
<p>
	The Raspberry Pi boot time configuration file
</p>
<pre>
$(cat /boot/config.txt 2>/dev/null)
</pre>
<div class="button">
	<a href="$script?editor&amp;file=/boot/config.txt">Edit config.txt</a>
</div>
EOT
	
		html_footer && exit 0 ;;
esac
