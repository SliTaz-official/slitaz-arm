#!/bin/sh
#
# TazBerry CGI Plugin - Raspberry Pi Camera tools web interface
#

case " $(GET) " in

	*\ rpi_cam\ *)
		html_header "PiCam"
		export PATH="/opt/vc/bin:/bin:/usr/bin"
		export LD_LIBRARY_PATH="/opt/vc/lib"
		camdir="/var/www/adm/cam"
		mkdir -p ${camdir}
		
		# CSS --> style.css
		cat << EOT
<style type="text/css">
	img { margin: 10px 0; }
</style>
EOT
		# Wen need VC Tools
		if [ ! -x "/opt/vc/bin/raspivid" ]; then
			echo "<p>VideoCore tools are missing. Please use tazberry \
				to setup the PiCam/NoIR</p>" && exit 0
		fi
		
		# raspivid + raspistill
		case " $(GET rpi_cam) " in
			*\ shot\ *)
				notify "Executing raspistill..."
				echo "$(GET options)" > ${camdir}/shot.opts
				raspistill $(GET options) -o ${camdir}/shot.jpg 
				notify hide ;;
			*\ rm_shot\ *)
				rm -f ${camdir}/shot.jpg ;;
		esac
		
		# Get last used options
		if [ -f "${camdir}/shot.opts" ]; then
			shot_opts="$(cat ${camdir}/shot.opts)"
		else
			shot_opts="--width 480 --height 320"
		fi
		
		cat << EOT
<h1>Raspberry Pi Camera</h1>

<div id="actions">
	<form method="get" action="$script">
		<input type="hidden" name="rpi_cam" value="shot" />
		<input type="submit" name="raspistill" value="Take a picture" />
		<input type="text" name="options" value="$shot_opts" />
	</form>
</div>

EOT
		# Display last shot
		if [ -f "${camdir}/shot.jpg" ]; then
			cat << EOT
<h2>Latest shot</h2>
<div class='center'>
	<a href="/adm/cam/shot.jpg"><img src='/adm/cam/shot.jpg' /></a>
	<p><a href="$script?rpi_cam=rm_shot">Remove</a></p>
</div>

EOT
		fi
		html_footer && exit 0 ;;
esac
