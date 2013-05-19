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

import sys
import pygame
from basecomm import BaseComm
from guicontrols import *

GAIN = (1, 0.2, 0.2, 0.2) # thr, x, y, z

def apply_gain(c):
    return (
            int(round(c[0] * GAIN[0])),
            int(round(c[1] * GAIN[1])),
            int(round(c[2] * GAIN[2])),
            int(round(c[3] * GAIN[3])),
            )

pygame.init()

size = [500, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Quad/Pi Base Station")

done = False

clock = pygame.time.Clock()

textPrint = TextPrint()

pygame.joystick.init()
if pygame.joystick.get_count() != 1:
    print 'There are %d joystics. What now?' % pygame.joystick.get_count()
    sys.exit(1)
joy = pygame.joystick.Joystick(0)
joy.init()
print 'Using joystick %s with %d axes, %d buttons, %d hats and %d balls.' % (joy.get_name(), joy.get_numaxes(), joy.get_numbuttons(), joy.get_numhats(), joy.get_numballs())

screen.fill(cBG)

g1 = Slide2D(screen, pygame.Rect(10, 10, 100, 100))
g2 = Slide(screen, pygame.Rect(10, 115, 100, 20))
g3 = Slide(screen, pygame.Rect(115, 10, 20, 100), orient=Slide.V)

motors = [
    Gauge(screen, pygame.Rect(10, 140, 20, 100), orient=Gauge.V),
    Gauge(screen, pygame.Rect(35, 140, 20, 100), orient=Gauge.V),
    Gauge(screen, pygame.Rect(60, 140, 20, 100), orient=Gauge.V),
    Gauge(screen, pygame.Rect(85, 140, 20, 100), orient=Gauge.V),
    ]
engine = False

b1 = Bulb(screen, pygame.Rect(115, 115, 20, 20), {False: RED, True: GREEN}, value=0)

controls_changed = True

comm = BaseComm()
comm.contact()

while not done:
    comm.receive()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.JOYAXISMOTION:
            controls_changed = True
        if event.type == pygame.JOYBUTTONDOWN:
            if joy.get_button(10):
                engine = False
                controls_changed = True
            elif joy.get_button(11):
                engine = True
                controls_changed = True

    if controls_changed:
        axisX = joy.get_axis(0)*1000
        axisY = joy.get_axis(1)*1000
        axisZ = joy.get_axis(2)*1000
        thr = (-joy.get_axis(3)+1)*1000/2
        screen.lock()
        g1.set_value((
                ((axisX + 1000) / 2),
                ((axisY + 1000) / 2),
                ))
        g2.set_value((axisZ + 1000) / 2)
        g3.set_value(thr)
        b1.set_value(engine)
        screen.unlock()
        controls_changed = False

        xthr = thr+1 if engine else 0
        comm.controls = apply_gain((xthr, axisX, axisY, axisZ))
        comm.transmit()

    for i in range(len(motors)):
        motors[i].set_value(comm.motors[i])
    
    pygame.display.flip()
    clock.tick(25)

pygame.quit()

