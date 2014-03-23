# ~/.xinitrc: Executed by Slim/LXDM login manager to startx X session.
# You can use F1 with Slim to change your window manager or configure
# it permanently with your personal applications.conf file.
#
. $HOME/.config/slitaz/applications.conf

[ "$1" ] && WINDOW_MANAGER="$1"

case "$WINDOW_MANAGER" in
	openbox|lxde*|xfce4|compiz|karmen|dwm|fluxbox*)
		exec ${WINDOW_MANAGER%-session}-session ;;
	razor*)
		exec razor-session ;;
	enlightenment)
		exec enlightenment_start ;;
	*)
		exec $WINDOW_MANAGER ;;
esac
