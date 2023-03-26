INSTALL ?= install

install:
	$(INSTALL) -D pullnix-sh/pullnix $(DESTDIR)$(PREFIX)/bin/pullnix
