#!/bin/sh
#
# TazBerry CGI Plugin - Editor
#

case " $(GET) " in
	*\ editor\ *)
		case " $(GET) " in
			*\ file\ *)
				file=$(GET file)
				from=$(GET from)
				html_header "Editor"
				echo "<h1>Editor: $file</h1>"
				cat << EOT
<div id="actions">
	<form method="get" action="$script">
		<input type="hidden" name="editor" />
		<input type="hidden" name="from" value="$from" />
		<input type="hidden" name="save" value="$file" />
		<textarea name="content">$(cat "$file" 2>/dev/null)</textarea>
		<input type="submit" value="Save file" />
	</form>
</div>
EOT
				;;
				
			*\ save\ *)
				file="$(GET save)"
				from=$(GET from)
				logfile="$cache/editor.log"
				html_header "Editor"
				mkdir -p ${cache} && touch ${logfile}
				echo "<h1>Editor</h1>"
				echo '<pre>'
				echo "Saving file : $file"
				sed "s/$(echo -en '\r') /\n/g" > ${file} << EOT
$(GET content)
EOT
				echo "Md5sum      : $(md5sum $file | awk '{print $1}')"
				echo "File size   : $(du -h $file | awk '{print $1}')"
				echo '</pre>'
				echo "<p><a href='$script?editor'>Editor</a> -"
				[ "$from" ] && echo "Back to: <a href='$script${from}'>${from#?}</a>"
				echo '</p>'
				echo "<a href='$script?editor&amp;file=$file'>$file</a>" >> ${logfile} ;;
				
			*)
				logfile="$cache/editor.log"
				html_header "Editor"
				[ "$(GET editor)" == "clean_log" ] && rm -f ${logfile}
				mkdir -p ${cache} && touch ${logfile}
				echo "<h1>Editor</h1>"
				cat << EOT
<div id="actions">
	<form method="get" action="$script">
		<input type="hidden" name="editor" />
		<input type="text" name="file" value="$file" placeholder="File path" />
		<input type="submit" value="View or edit" />
	</form>
</div>

<h2>Latest edits</h2>
<pre>
$(tac $logfile | head -n 8)
</pre>
<div class="button">
	<a href="$script?editor=clean_log">Clean logs</a>
</div>

EOT
				;;
		esac	
		html_footer
		exit 0 ;;
esac
