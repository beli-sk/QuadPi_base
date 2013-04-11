#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# Quad/Pi Base communication
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

import socket
import struct

class CommError(Exception):
    pass
class ProtocolError(CommError):
    pass

class BaseComm(object):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERR = 4
    prio = {1: 'DEBUG', 2: 'INFO', 3: 'WARN', 4: 'ERR'}
    addr = ('127.0.0.1', 31512)

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.controls = (0, 0, 0, 0)
        self.tele = (0, 0, 0, 0)

    def transmit(self):
        s = self.controls = struct.pack('<bbbb',
                self.controls[0],
                self.controls[1],
                self.controls[2],
                self.controls[3]
                )
        self.sock.sendall(s)

    #def contact(self):
    #    self.sock.connect(self.addr)
    #    self.sock.sendall('Quad/Pi P1\n')
    #    s = self.sock.recv(3)
    #    if s != 'OK\n':
    #        raise ProtocolError('Handshake fail')
    #    self.sock.setblocking(0)

