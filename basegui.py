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

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
SILVER   = ( 192, 192, 192)
GRAY     = ( 127, 127, 127)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def write(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

class Slide:
    H = 0
    V = 1
    def __init__(self, screen, rect, orient = 0, value=0):
        self.screen = screen
        self.rect = rect
        self.inrect = rect.inflate(-2, -2)
        self.orient = orient
        self.value = value
        self.redraw()

    def set_value(self, value):
        self.value = value
        self.redraw()

    def redraw(self):
        pygame.draw.rect(self.screen, BLACK, self.rect, 1)
        pygame.draw.rect(self.screen, SILVER, self.inrect, 0)
        if self.orient == self.H:
            x = int(round(float(self.inrect.width-1) / 1000.0 * float(self.value)))
            pygame.draw.line(self.screen, WHITE,
                    (self.inrect.left + x, self.inrect.top),
                    (self.inrect.left + x, self.inrect.top + self.inrect.height-1),
                    )
        else:
            y = int(round(float(self.inrect.height-1) / 1000.0 * float(self.value)))
            pygame.draw.line(self.screen, WHITE,
                    (self.inrect.left, self.inrect.top + y),
                    (self.inrect.left + self.inrect.width-1, self.inrect.top + y),
                    )

class Slide2D:
    def __init__(self, screen, rect, value=(0,0)):
        self.screen = screen
        self.rect = rect
        self.inrect = rect.inflate(-2, -2)
        self.value = value
        self.redraw()

    def set_value(self, value):
        self.value = value
        self.redraw()

    def redraw(self):
        x = int(round(float(self.inrect.width-1) / 1000.0 * float(self.value[0])))
        y = int(round(float(self.inrect.height-1) / 1000.0 * float(self.value[1])))
        pygame.draw.rect(self.screen, BLACK, self.rect, 1)
        pygame.draw.rect(self.screen, SILVER, self.inrect, 0)
        pygame.draw.line(self.screen, WHITE,
                (self.inrect.left, self.inrect.top + y),
                (self.inrect.left + self.inrect.width-1, self.inrect.top + y),
                )
        pygame.draw.line(self.screen, WHITE,
                (self.inrect.left + x, self.inrect.top),
                (self.inrect.left + x, self.inrect.top + self.inrect.height-1),
                )

class Gauge:
    H = 0
    V = 1

    def __init__(self, screen, rect, orient=0, flip=False, value=0):
        self.screen = screen
        self.rect = rect
        self.inrect = rect.inflate(-2, -2)
        self.orient = orient
        self.flip = flip
        self.value = value
        self.redraw()

    def set_value(self, value):
        self.value = value
        self.redraw()

    def redraw(self):
        if self.orient == self.H:
            fillsize = int(float(self.inrect.width) / 1000.0 * float(self.value))
            fillrect = pygame.Rect(
                    self.inrect.left + self.inrect.width - fillsize if self.flip
                        else self.inrect.left,
                    self.inrect.top,
                    fillsize,
                    self.inrect.height
                    )
        else:
            fillsize = int(float(self.inrect.height) / 1000.0 * float(self.value))
            fillrect = pygame.Rect(
                    self.inrect.left,
                    self.inrect.top if self.flip
                        else self.inrect.top + self.inrect.height - fillsize,
                    self.inrect.width,
                    fillsize
                    )

        pygame.draw.rect(self.screen, BLACK, self.rect, 1)
        pygame.draw.rect(self.screen, SILVER, self.inrect, 0)
        pygame.draw.rect(self.screen, GRAY, fillrect, 0)

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

g1 = Slide2D(screen, pygame.Rect(10, 10, 100, 100))
g2 = Slide(screen, pygame.Rect(10, 115, 100, 20))
g3 = Slide(screen, pygame.Rect(115, 10, 20, 100), orient=Slide.V)

screen.fill(WHITE)

controls_changed = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type in (pygame.JOYAXISMOTION,):
            controls_changed = True
    #screen.fill(WHITE)

    if controls_changed:
        print "cc"
        axisX = joy.get_axis(0)
        axisY = joy.get_axis(1)
        axisZ = joy.get_axis(2)
        thr = joy.get_axis(3)
        g1.set_value((
                ((axisX + 1) * 1000 / 2),
                ((axisY + 1) * 1000 / 2),
                ))
        g2.set_value((axisZ + 1) * 1000 / 2)
        g3.set_value((thr + 1) * 1000 / 2)
        controls_changed = False
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()

