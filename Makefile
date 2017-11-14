#Just for building packages.
DESTDIR ?=
INSTALLPATH ?= /lib/budgie-desktop/plugins

budgie-shutdown-applet:
	echo "Nothing to do"
install: budgie-shutdown-applet
	mkdir -p $(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer
	for file in ShutdownTimer/*; \
	do \
		install -m 0755 "$$file" $(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer/; \
	done

