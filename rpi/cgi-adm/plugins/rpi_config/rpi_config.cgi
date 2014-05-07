#!/bin/sh
#
# TazBerry CGI Plugin - Raspberry Pi configuration
#

case " $(GET) " in
	*\ audio\ *)
		html_header "Audio Control"
		case " $(GET audio) " in
			*\ auto\ *|*\ analog\ *|*\ hdmi\ *) 
				amixer -q cset numid=3  $(GET cset) ;;
			*\ vol\ *)
				amixer -q cset numid=1 "$(GET cset)%" ;;
			*\ mute\ *)
				amixer -q cset numid=1 mute ;;
			*\ play\ *)
				notify "Playing MP3 system sound..."
				mpg123 /usr/share/sounds/ready.mp3 2>/dev/null 
				notify hide ;;
		esac
		cat << EOT
<h1>Audio Mixer</h1>
<div class="button">
	<a href="$script?audio=play">Play sound</a>
	<a href="$script?audio=mute">Mute</a>
	<a href="$script?audio=vol&amp;cset=100">Vol 100%</a>
	<a href="$script?audio=vol&amp;cset=75">Vol 75%</a>
</div>
<pre>
$(amixer)
</pre>

<h2>Audio Output</h2>
<p>
	The Raspberry Pi has two audio output modes: HDMI and headphone jack.
	You can switch between these modes at any time.
</p>
<div class="button">
	<a href="$script?audio=auto&amp;cset=0">Auto</a>
	<a href="$script?audio=analog&amp;cset=1">Headphone</a>
	<a href="$script?audio=hdmi&amp;cset=2">HDMI</a>
</div>

<h2>Controls</h2>
<pre>
$(amixer controls)
</pre>

<h2>Contents</h2>
<pre>
$(amixer contents)
</pre>

EOT
		html_footer && exit 0 ;;

	*\ leds\ *)
		trigger="/sys/class/leds/led0/trigger"
		brightness="/sys/class/leds/led0/brightness"
		html_header "Leds"
		case " $(GET leds) " in
			*\ act_test\ *)
				notify "ACT Led turned on for 5 sec..."
				echo "1" > ${brightness}
				sleep 5
				echo "0" > ${brightness} 
				notify hide ;;
			*\ act_on\ *)
				echo "0" > ${brightness}; usleep 50000
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
	<a href="$script?leds=act_test">ACT Led test</a>
	<a href="$script?leds=act_on">ACT Led on</a>
	<a href="$script?leds=act_off">ACT Led off</a>
</div>
EOT
		html_footer && exit 0 ;;
	
	*\ i2c\ *)
		html_header "I2C Bus"
		modprobe -q i2c-bcm2708
		modprobe -q i2c-dev
		echo '<h1>Raspberry Pi I2C Bus</h1>'
		if [ ! -x "/usr/sbin/i2cdetect" ]; then
			echo "<div id='error'>Missing package: i2c-tools</div>"
			html_footer && exit 0
		fi
		cat << EOT
<p>
	I2C kernel modules: i2c-bcm2708 + i2c-dev
</p>

<h2>I2C Detect</h2>
<pre>
$(i2cdetect -y 1)
</pre>
EOT
		html_footer && exit 0 ;;
	
	*\ oclock\ *)
		cur_freq=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)
		cur=$(($cur_freq / 1000))
		html_header "Overclocking"
		cat << EOT
<h1>RPi Overclocking</h1>

<p>
	Current CPU freq scaling value: $cur MHz
</p>

<pre>
$(tazberry rpi_oclock)
</pre>

<h2>Current settings:</h2>
<pre>
$(fgrep _freq /boot/config.txt)
$(fgrep over_voltage /boot/config.txt)
</pre>
<div class="button">
	<a href='$script?editor&amp;file=/boot/config.txt&amp;from=?rpi_config'>Edit boot configuration</a>
<div>
EOT
		html_footer && exit 0 ;;
	
	*\ rpi_config\ *)
		blacklist="/etc/modprobe.d/rpi-blacklist.conf"
		html_header "Raspberry Pi"
		cat << EOT
<h1>SliTaz Raspberry Pi</h1>

<p>
	Remotely configure your SliTaz Raspberry Pi device.
</p>

<div id="actions">
	<form method="get" action="$script">
		<input type="submit" name="audio" value="Audio control" />
		<input type="submit" name="oclock" value="Overclocking" />
		<input type="submit" name="leds" value="Leds" />
		<input type="submit" name="i2c" value="I2C Bus" />
	</form>
</div>

<h2>Kernel boot parameters</h2>
<p>
	This file provides the Linux Kernel boot time parameters and SliTaz
	boot time options.
</p>
<pre>
$(cat /boot/cmdline.txt 2>/dev/null)
</pre>
<div class="button">
	<a href="$script?editor&amp;file=/boot/cmdline.txt&amp;from=?rpi_config">Edit cmdline.txt</a>
</div>

<h2>Boot configuration file</h2>
<p>
	The Raspberry Pi boot time configuration file
</p>
<pre>
$(cat /boot/config.txt 2>/dev/null)
</pre>
<div class="button">
	<a href="$script?editor&amp;file=/boot/config.txt&amp;from=?rpi_config">Edit config.txt</a>
</div>

<h2>Blacklisted Kernel modules</h2>
<p>
	List of the Linux Kernel modules that should not be loaded on boot
	time to save resources and speed up your Raspberry Pi.
</p>
<pre>
$(cat $blacklist 2>/dev/null)
</pre>
<div class="button">
	<a href="$script?editor&amp;file=$blacklist&amp;from=?rpi_config">Edit $(basename $blacklist)</a>
</div>
EOT
	
		html_footer && exit 0 ;;
esac
