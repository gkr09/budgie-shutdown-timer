#!/bin/bash
#Budgie Shutdown Timer Applet
#Gopikrishnan.R
#This script basically just copies the files to approproate directories.

APPLETDIR=/lib/budgie-desktop/plugins

ICONDIR=/usr/share/icons/hicolor/scalable/apps

echo "Installing Shutdown Timer Applet....."

mkdir $APPLETDIR/org.budgie-desktop.applet.shutdowntimer

for file in ShutdownTimer/*;do

    install -m 0755 "$file" $APPLETDIR/org.budgie-desktop.applet.shutdowntimer/

done

for file in icons/*;do

    install -m 0755 "$file" $ICONDIR/

done

echo "Finished Installing Applet. Restart or Re-login to find the applet in Budgie."
