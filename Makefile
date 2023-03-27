INSTALL ?= install

install:
	$(INSTALL) -D bin/pullnix $(DESTDIR)$(PREFIX)/bin/pullnix
	$(INSTALL) -D bin/pullnix-switch $(DESTDIR)$(PREFIX)/bin/pullnix-switch
