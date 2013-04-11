#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# Quad/Pi base GUI
#
# Copyright 2013 Michal Belica <devel@beli.sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

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
