# Makefile for SliTaz ARM.
#

PREFIX?=/usr

all:

install:
	install -m 0755 -d $(DESTDIR)$(PREFIX)/bin
	#install -m 0755 -d $(DESTDIR)$(PREFIX)/share/slitaz-arm
	install -m 0755 sat $(DESTDIR)$(PREFIX)/bin
	install -m 0755 sat-rpi $(DESTDIR)$(PREFIX)/bin
	install -m 0755 rpi/tazberry $(DESTDIR)$(PREFIX)/bin

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/sat
	rm -f $(DESTDIR)$(PREFIX)/bin/sat-rpi
	rm -f $(DESTDIR)$(PREFIX)/bin/tazberry
