#Just for building packages. (eopkg for solus)

DESTDIR ?=

INSTALLPATH ?= /usr/lib64/budgie-desktop/plugins

budgie-shutdown-applet:
	echo "Nothing to do"
install: budgie-shutdown-applet
	mkdir -p $(DESTDIR)/$(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer
	for file in ShutdownTimer/*; \
	do \
		install -m 0755 "$$file" $(DESTDIR)/$(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer/; \
	done

