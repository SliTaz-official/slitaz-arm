#!/bin/sh
#
# SliTaz ARM CGI Plugin - System configs and options
#

if [ "$(GET status)" ]; then
	html_header "Status"
	cat << EOT
<h1>System Status</h1>
<p>
	Uptime: $(uptime)
</p>

<h2>Disk usage</h2>
<pre>
Filesystem                Size      Used Available Use% Mounted on
--------------------------------------------------------------------------------
$(df -h | grep ^/dev)
</pre>

<h2>Memory usage</h2>
<pre>
Type         total         used         free       shared      buffers
--------------------------------------------------------------------------------
$(free -m | sed "/total/d")
</pre>

<h2>Routing table</h2>
<pre>
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
--------------------------------------------------------------------------------
$(route | grep [0-9])
</pre>

<h2>Kernel messages</h2>
<pre>
Last dmesg output
--------------------------------------------------------------------------------
$(dmesg | tail -n 15)
</pre>

<h2>Kernel modules</h2>
<pre>
Module                  Size  Used by    Tainted: G
--------------------------------------------------------------------------------
$(lsmod | sed "/^Module/d")
</pre>

EOT
	html_footer && exit 0
fi
