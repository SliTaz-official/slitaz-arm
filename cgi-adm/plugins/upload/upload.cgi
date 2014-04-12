#!/bin/sh
#
# TazBerry CGI Plugin - File upload
#

case " $(POST) " in
	*\ upload\ *)
		[ "$updir" ] || updir="/var/cache/uploads"
		[ -d "$updir" ] || mkdir -p ${updir}
		upload="true"
		name=$(FILE file name)
		tmpname=$(FILE file tmpname)
		# Move/Overwrite files to the cloud and set permissions
		if ! mv -f ${tmpname} ${updir}/${name}; then
			echo "ERROR: ${name}" && exit 1
		fi
		chmod a+r ${updir}/${name}
		rm -rf /tmp/httpd_post* ;;
esac

if [ "$(GET upload)" ] || [ "$upload" ]; then
	[ "$updir" ] || updir="/var/cache/uploads"
	html_header "File Upload"
	echo "<h1>File Upload</h1>"
	cat << EOT
<div id="actions">
	<form method="post" action="$script" enctype="multipart/form-data">
		<input type="hidden" name="upload" />
		<input type="file" name="file" size="50" />
		<p><input type="submit" value="Upload to $(hostname)" /></p>
	</form>
</div>

<h2>Default upload directory: $updir</h2>
<pre>
$(ls -l ${updir})
</pre>
EOT
	html_footer && exit 0
fi
