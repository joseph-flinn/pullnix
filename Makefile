INSTALL ?= install

install:
	$(INSTALL) -D pullnix-sh/pullnix $(DESTDIR)$(PREFIX)/bin/pullnix
	$(INSTALL) -D pullnix-sh/pullnix-switch $(DESTDIR)$(PREFIX)/bin/pullnix-switch
