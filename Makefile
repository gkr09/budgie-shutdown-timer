#Just for building packages. (eopkg for solus)
include ../Makefile.common

DESTDIR ?=

INSTALLPATH ?= /usr/lib64/budgie-desktop/plugins

ICONPATH ?= /usr/share/icons/hicolor/scalable/apps

budgie-shutdown-applet:
	echo "Nothing to do"
install: budgie-shutdown-applet
	mkdir -p $(DESTDIR)$(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer
	mkdir -p $(DESTDIR)$(ICONPATH)
	#rm -f $(ICONDIR)/icon-theme.cache
	for file in ShutdownTimer/*; \
	do \
		install -m 0755 "$$file" $(DESTDIR)$(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer/; \
	done
	for file in icons/*; \
	do \
		install -m 0755 "$$file" $(DESTDIR)$(ICONPATH)/; \
	done
