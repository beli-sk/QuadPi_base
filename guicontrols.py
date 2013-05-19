#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# Quad/Pi base GUI controls
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
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GRAY80   = ( 204, 204, 204)
GRAY66   = ( 170, 170, 170)
GRAY50   = ( 128, 128, 128)
GRAY33   = (  84,  84,  84)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
DARKGREEN= (   0, 180,   0)
BLUE     = (   0,   0, 255)

cBG = BLACK;
cBORDER = GRAY50
cINDICATOR = DARKGREEN
cGAUGEBG = GRAY33

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

class Bulb(object):
    def __init__(self, screen, rect, colormap, value=0):
        self.screen = screen
        self.rect = rect
        self.colormap = colormap
        self.value = value
        if 0 not in self.colormap.keys():
            self.colormap[0] = cGAUGEBG
        self.redraw()

    def set_value(self, value):
        self.value = value
        self.redraw()

    def redraw(self):
        pygame.draw.ellipse(self.screen, self.colormap[self.value], self.rect, 0)
        pygame.draw.ellipse(self.screen, cBORDER, self.rect, 1)

class Slide(object):
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
        pygame.draw.rect(self.screen, cBORDER, self.rect, 1)
        pygame.draw.rect(self.screen, cGAUGEBG, self.inrect, 0)
        if self.orient == self.H:
            x = int(round(float(self.inrect.width-1) / 1000.0 * float(self.value)))
            pygame.draw.line(self.screen, cINDICATOR,
                    (self.inrect.left + self.inrect.width - x, self.inrect.top),
                    (self.inrect.left + self.inrect.width - x, self.inrect.top + self.inrect.height-1),
                    )
        else:
            y = int(round(float(self.inrect.height-1) / 1000.0 * float(self.value)))
            pygame.draw.line(self.screen, cINDICATOR,
                    (self.inrect.left, self.inrect.top + self.inrect.height - y),
                    (self.inrect.left + self.inrect.width-1, self.inrect.top + self.inrect.height - y),
                    )

class Slide2D(object):
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
        pygame.draw.rect(self.screen, cBORDER, self.rect, 1)
        pygame.draw.rect(self.screen, cGAUGEBG, self.inrect, 0)
        pygame.draw.line(self.screen, cINDICATOR,
                (self.inrect.left, self.inrect.top + y),
                (self.inrect.left + self.inrect.width-1, self.inrect.top + y),
                )
        pygame.draw.line(self.screen, cINDICATOR,
                (self.inrect.left + x, self.inrect.top),
                (self.inrect.left + x, self.inrect.top + self.inrect.height-1),
                )

class Gauge(object):
    H = 0
    V = 1

    def __init__(self, screen, rect, orient=0, flip=False, color=cINDICATOR, value=0):
        self.screen = screen
        self.rect = rect
        self.inrect = rect.inflate(-2, -2)
        self.orient = orient
        self.flip = flip
        self.value = value
        self.color = cINDICATOR
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
            fillsize = int(float(self.inrect.height) / 1000.0
                    * float(self.value if self.value <= 1000 else 1000))
            fillrect = pygame.Rect(
                    self.inrect.left,
                    self.inrect.top if self.flip
                        else self.inrect.top + self.inrect.height - fillsize,
                    self.inrect.width,
                    fillsize
                    )

        pygame.draw.rect(self.screen, cGAUGEBG, self.inrect, 0)
        if self.value > 0:
            pygame.draw.rect(self.screen, self.color, fillrect, 0)
        if self.value > 1000:
            pygame.draw.rect(self.screen, RED, self.inrect, 2)
        else:
            pygame.draw.rect(self.screen, cBORDER, self.rect, 1)
