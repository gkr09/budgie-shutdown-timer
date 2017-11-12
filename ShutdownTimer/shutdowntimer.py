#!/usr/bin/env python3

# Copyright (C) 2017 Gopikrishnan R

"""
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from threading import Timer
import subprocess,time


import gi.repository
gi.require_version('Budgie','1.0')
gi.require_version('Gtk','3.0')
from gi.repository import Budgie, GObject, Gtk



class BudgieShutdownTimer(GObject.GObject, Budgie.Plugin):

    __gtype_name__ = "BudgieShutdownTimer"

    def __init__(self):

        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):

        return BudgieShutdownTimerApplet(uuid)


class BudgieShutdownTimerApplet(Budgie.Applet):
  
    box = Gtk.EventBox()
    action = Gtk.ComboBoxText()                      # To Select Shutdown, Reboot etc.
    spin1 = Gtk.SpinButton()                         # Hours
    spin2 = Gtk.SpinButton()                         # Minutes
    stack = Gtk.Stack()                              # Stack to switch between Timer setting and Timer running screens.
    t = None                                         # To store the timer object created in start(). It needed to be -
                                                     # -global to cancel the timer from another func.
    timetext = Gtk.Label()                           # Displays time of action in the applet.
    timetext.set_justify(Gtk.Justification.CENTER)
    selection = ""                                   # Stores the user selected action.
    timestr = ""                                     # Store the calculated time of action.

    def __init__(self,uuid):

        Budgie.Applet.__init__(self)
        self.initUI()
        
    def initUI(self):

        """ Drawing the Applet UI """

        self.popover = Budgie.Popover.new(self.box)
        self.img = Gtk.Image.new_from_icon_name("appointment-missed-symbolic", Gtk.IconSize.BUTTON)
        self.label2 = Gtk.Label("in")
        self.button = Gtk.Button(label="Start")
        context_start = self.button.get_style_context()
        self.button_cancel = Gtk.Button(label="Cancel")
        context_cancel = self.button_cancel.get_style_context()
        self.label_hours = Gtk.Label(":")

        self.adjustment1 = Gtk.Adjustment(value=0, lower=0, upper=500, step_incr=1, page_incr=0, page_size=0)
        """Had to set upper=500 as I don't know how to make it accept any value, 500 seemed acceptable """

        self.adjustment2 = Gtk.Adjustment(value=30, lower=1, upper=59, step_incr=1, page_incr=0, page_size=0)

        self.separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.vbox_action = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0) # VBox just to make the combobox center aligned.
        self.vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)       # VBox for the Timer Running Screen.

        self.box.set_tooltip_text("Shutdown Timer")
        
        self.box.add(self.img)
        self.add(self.box)
        self.box.connect("button-press-event", self.on_press)

        self.action.append_text("Shutdown")
        self.action.append_text("Reboot")
        self.action.append_text("Hibernate")
        self.action.append_text("Suspend")
        self.action.set_active(0)
      
        context_start.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        self.button.connect("clicked", self.start)

        context_cancel.add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)

        self.button_cancel.connect("clicked", self.cancel)

        
        self.spin1.set_orientation(Gtk.Orientation.VERTICAL)
        
        self.spin2.set_orientation(Gtk.Orientation.VERTICAL)


        self.spin1.set_adjustment(self.adjustment1)
        self.spin2.set_adjustment(self.adjustment2)

        """ Default Screen """
        self.vbox_action.set_center_widget(self.action)
        self.hbox.pack_start(self.vbox_action,False,False,5)
        self.hbox.pack_start(self.label2,False,False,5)
        self.hbox.pack_start(self.spin1,False,False,5)
        self.hbox.pack_start(self.label_hours,False,False,5)
        self.hbox.pack_start(self.spin2,False,False,5)
        self.vbox.pack_start(self.hbox,True,True,5)
        self.vbox.pack_start(self.separator,False,True,5)
        self.vbox.pack_start(self.button,True,True,0)

        """ Timer Running Screen """
        self.vbox2.pack_start(self.timetext,True,True,0)
        self.vbox2.pack_start(self.button_cancel,False,True,0)

        self.stack.add_named(self.vbox,"vbox")
        self.stack.add_named(self.vbox2,"vbox2")

        self.popover.add(self.stack)

        self.popover.get_child().show_all()

        self.box.show_all()

        self.show_all()


    def	on_press(self, box, e):

        if e.button != 1:
            return Gdk.EVENT_PROPAGATE

        if self.popover.get_visible():
            self.popover.hide()

        else:
            self.manager.show_popover(self.box)

    def do_update_popovers(self, manager):

    	self.manager = manager
    	self.manager.register_popover(self.box, self.popover)

    def execute(self):
        """ Execute the Action with systemctl """

        try:
            if self.selection=="Shutdown":
                subprocess.run(['systemctl', "poweroff"])

            elif self.selection=="Reboot":
                subprocess.run(['systemctl', "reboot"])

            elif self.selection=="Hibernate":
                self.box.set_tooltip_text("Shutdown Timer")        # Reset the tooltip.
                self.stack.set_visible_child_name("vbox")          # Reset the stack to initial screen.
                subprocess.run(['systemctl', "hibernate"]) 

            elif self.selection=="Suspend":
                self.box.set_tooltip_text("Shutdown Timer")
                self.stack.set_visible_child_name("vbox")
                subprocess.run(['systemctl', "suspend"])

        except subprocess.CalledProcessError:                      # Command returned a non-zero exit code.
            subprocess.Popen(['notify-send','Shutdown Timer: Error !','-i','appointment-missed-symbolic'])

    def get_time_formatted(self,secs):
        """ Return the Time of Action Execution as a String to display on the tooltip and widget screen. """

        days = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

        x = time.localtime(time.time()+secs)                       # Localtime + user selected duration in secs.

        """ Return the string used to display in the tooltip and timer started screen """
        return str(x.tm_hour)+":"+'{:2d}'.format(x.tm_min)+" on "+str(x.tm_mday)+"th "+days[x.tm_mon]+" "+str(x.tm_zone)

    def start(self,button):
        """ Get the time and start the Timer. """

        hrs = self.spin1.get_value_as_int()
        min = self.spin2.get_value_as_int()
        secs = hrs*3600+min*60
        self.timestr = self.get_time_formatted(secs)
        self.selection = self.action.get_active_text()

        self.t = Timer(secs, self.execute)

        self.timetext.set_text(self.selection+" scheduled at \n"+self.timestr)              # Text on Timer Running Screen.
        self.box.set_tooltip_text(self.selection+" scheduled at "+self.timestr)
        self.stack.set_visible_child_name("vbox2")
        self.t.start()                                                                      # Timer started.

        subprocess.Popen(['notify-send', "{} at {}".format(self.selection,self.timestr),'-i','appointment-missed-symbolic'])   # Send Notification.

    def cancel(self,button):

        self.t.cancel()                                            # Cancel the timer.

        self.stack.set_visible_child_name("vbox")                  # Reset the stack to initial screen.
        subprocess.Popen(['notify-send', "Scheduled {} cancelled".format(self.selection),'-i','appointment-missed-symbolic'])
        self.box.set_tooltip_text("Shutdown Timer")                # Reset the tooltip.

#END
