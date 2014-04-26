#!/bin/sh
#
# TazBerry CGI Plugin - Raspberry Pi GPIO settings
#

case " $(GET) " in

	*\ rpi_gpio\ *)
		sysfs="/sys/class/gpio"

		case " $(GET rpi_gpio) " in
			*\ export\ *)
				sysfs="/sys/class/gpio"
				pin="$(GET pin)"
				set="$(GET set)"
				[ "$set" == "unexport" ] || html_header "GPIO pin: $pin"
				if [ ! -d "$sysfs/gpio${pin}" ]; then
					echo ${pin} > ${sysfs}/export
				fi
				# in/out
				case "$set" in
					in)
						echo "0" > ${sysfs}/gpio${pin}/value
						echo "in" > ${sysfs}/gpio${pin}/direction ;;
					out)
						echo "out" > ${sysfs}/gpio${pin}/direction ;;
					write)
						echo "out" > ${sysfs}/gpio${pin}/direction
						echo "1" > ${sysfs}/gpio${pin}/value ;;
					unexport)
						echo "$pin" > ${sysfs}/unexport ;;
				esac
				[ "$set" == "unexport" ] || cat << EOT
<h1>Raspberry Pi GPIO pin: $pin</h1>

<pre>
Direction : $(cat $sysfs/gpio${pin}/direction)
Value     : $(cat $sysfs/gpio${pin}/value)
</pre>

<div class="button">
	<a href='$script?rpi_gpio=export&amp;pin=$pin&amp;set=in'>in</a>
	<a href='$script?rpi_gpio=export&amp;pin=$pin&amp;set=out'>out</a>
	<a href='$script?rpi_gpio=export&amp;pin=$pin&amp;set=write'>Write output</a>
	<a href='$script?rpi_gpio=export&amp;pin=$pin&amp;set=unexport'>Unexport</a>
</div>

EOT
			html_footer && [ "$set" == "unexport" ] || exit 0 ;;
		esac

		# Main page
		html_header "GPIO pins"
		
		cat << EOT
<h1>Raspberry Pi GPIO pins</h1>

<p>
	The R-Pi offers GPIO lower-level interfaces intended to connect 
	more directly with chips and subsystem modules. Documentation on:
	<a href="http://elinux.org/RPi_Low-level_peripherals">the Official Wiki</a>
</p>

<h2>$sysfs</h2>
<pre>
$(ls -1p $sysfs)
</pre>

<h2>Export GPIO pin</h2>
<div class="button">
EOT
for pin in 0 1 4 7 8 9 10 11 14 15 17 18 21 22 23 24 25
do
	echo -n "<a href='$script?rpi_gpio=export&amp;pin=$pin'>${pin}</a> "
done
		echo '<div>'
		html_footer && exit 0 ;;
esac
