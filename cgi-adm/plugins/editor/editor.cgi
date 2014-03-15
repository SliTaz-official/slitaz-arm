#!/bin/sh
#
# TazBerry CGI Plugin - Editor
#

case " $(GET) " in
		*\ editor\ *)
			case " $(GET) " in
				*\ file\ *)
					file=$(GET file)
					html_header "Editor"
					echo "<h1>Editor: $file</h1>"
					cat << EOT
<div id="actions">
	<form method="get" action="$script">
		<input type="hidden" name="editor" />
		<input type="hidden" name="save" value="$file" />
		<textarea name="content">$(cat "$file" 2>/dev/null)</textarea>
		<input type="submit" value="Save file" />
	</form>
</div>
EOT
					;;
				
				*\ save\ *)
					html_header "Editor"
					echo "<h1>Editor</h1>"
					echo '<pre>'
					echo "Saving file : $(GET save)"
					sed "s/$(echo -en '\r') /\n/g" > $(GET save) << EOT
$(GET content)
EOT
					echo "File size   : $(du -h $(GET save) | awk '{print $1}')"
					echo '</pre>'
					echo "<p><a href='$script?editor'>Editor</a></p>"
					if [ -d "$cache" ]; then
						echo "" >> ${cache}/editor.log
					fi ;;
				
				*)
					html_header "Editor"
					echo "<h1>Editor</h1>"
					cat << EOT
<div id="actions">
	<form method="get" action="$script">
		<input type="hidden" name="editor" />
		<input type="text" name="file" value="$file" placeholder="File path" />
		<input type="submit" value="View or edit" />
	</form>
</div>
EOT
					;;
			esac
			
		html_footer
		exit 0 ;;
esac
