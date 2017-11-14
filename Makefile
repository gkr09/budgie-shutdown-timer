#Just for building packages.
DESTDIR ?=
<<<<<<< HEAD
INSTALLPATH ?= /usr/lib64/budgie-desktop/plugins
=======
INSTALLPATH ?= /lib/budgie-desktop/plugins
>>>>>>> a9b514a6ed0563f10c68f36f01319ba58ea7756f

budgie-shutdown-applet:
	echo "Nothing to do"
install: budgie-shutdown-applet
	mkdir -p $(DESTDIR)/$(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer
	for file in ShutdownTimer/*; \
	do \
		install -m 0755 "$$file" $(DESTDIR)/$(INSTALLPATH)/org.budgie-desktop.applet.shutdowntimer/; \
	done

