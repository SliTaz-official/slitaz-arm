#!/bin/sh
#
# SliTaz ARM CGI Plugin - System configs and options
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
	
	*\ config\ *)
		html_header "Configuration"
		cat << EOT
<h1>System Config</h1>

<p>
	Remotly configure your SliTaz ARM device.
</p>

<div id="actions">
	<form method="get" action="$script">
		<input type="submit" name="rdate" value="Set system time" />
	</form>
</div>

EOT
		html_footer && exit 0
esac
