# Makefile for SliTaz ARM.
#

PREFIX?=/usr

all:

install:
	install -m 0755 -d $(DESTDIR)$(PREFIX)/bin
	install -m 0755 sat $(DESTDIR)$(PREFIX)/bin

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/sat
