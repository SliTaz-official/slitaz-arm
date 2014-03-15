# Makefile for SliTaz ARM.
#

PREFIX?=/usr

all:

install:
	install -m 0755 -d $(DESTDIR)$(PREFIX)/bin
	install -m 0755 sat $(DESTDIR)$(PREFIX)/bin
	install -m 0755 sat-rpi $(DESTDIR)$(PREFIX)/bin

install-cgi:
	install -m 0755 -d $(DESTDIR)/var/www/adm
	cp -a cgi-adm/* $(DESTDIR)/var/www/adm

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/sat
	rm -f $(DESTDIR)$(PREFIX)/bin/sat-rpi

uninstall-cgi:
	rm -rf $(DESTDIR)/var/www/adm
