#!/usr/bin/python

from gi.repository import Gtk
import sys
import signal

class BaseGUI(object):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui/main.ui")
        builder.connect_signals(self)
        self.win = builder.get_object('windowMain')
        self.tbLog = builder.get_object('tbLog')
        self.win.show_all()

    def on_windowMain_destroy(self, widget):
        print 'Destroy'
        sys.exit(0)

    def on_swEngine_active_notify(self, widget, data):
        msg = 'Engine switch %s' % ('ON' if widget.get_active() else 'OFF')
        print msg
        self.tbLog.insert(self.tbLog.get_end_iter(), msg+'\n')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_IGN) # FIXME ctrl-c makes app freeze
    gui = BaseGUI()
    Gtk.main()
