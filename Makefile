INSTALL ?= install

install:
	$(INSTALL) -D bin/pullnix $(DESTDIR)$(PREFIX)/bin/pullnix
