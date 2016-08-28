from my_interface import IActivity
import pygame
from pygame.locals import *
import math


class StartScreen(IActivity):
    listener = None
    graphics = None

    mouseX = 0
    mouseY = 0
    mousePressed = False

    bg = None
    menu = None

    def __init__(self, graphics, listener):
        self.listener = listener
        self.graphics = graphics
        self.bg = Backgroud(graphics.get_width(), graphics.get_height())
        self.menu = Menu(graphics.get_width(), graphics.get_height())
        pass

    def draw(self, delta_time):
        self.bg.draw(self.graphics, delta_time)
        self.menu.draw(self.graphics, delta_time)

        pass

    def onMousePresse(self, button, x, y):
        self.mousePressed = True
        self.mouseX = x
        self.mouseY = y
        pass

    def onMouseRelease(self, button, x, y):
        self.mousePressed = False
        self.mouseX = x
        self.mouseY = y

        pass

    def onMouseMove(self, x, y, dx, dy):
        self.mouseX = x
        self.mouseY = y
        pass

    def handleEvent(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                (x, y) = event.pos
                self.onMouseRelease(event.button, x, y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = event.pos
                self.onMousePresse(event.button, x, y)

            elif event.type == pygame.MOUSEMOTION:
                (x, y) = event.pos
                (dx, dy) = event.rel
                self.onMouseMove(x, y, dx, dy)


class Menu:
    w = 0
    h = 0
    logo = None
    logoX = 0
    logoY = 0
    deg = 0.0

    gra = 0.08
    pull = 0.16
    v = 0.12

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.logo = pygame.image.load("assets/LOGO.png")
        self.logoX = w / 2 - self.logo.get_width() / 2
        self.logoY = h

    def draw(self, graphics, delta_time):
        delta = 0
        v += (self.pull - self.grav) * delta_time
        if (self.logoY <= self.h / 2):
            self.logoY = self.h / 2
            self.deg += delta_time * 0.003
            delta = -math.sin(self.deg) * 15
        else:
            self.logoY -= v

        graphics.blit(self.logo, (self.logoX, self.logoY + delta))
        pass

    def get_bubble_gra(self, y):
        if (y < self.h / 2):
            return


class Backgroud:
    w = 0
    h = 0
    bg = None

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.bg = pygame.Surface((w, h))
        self.bg.fill(Constant.BG_COLOR)

    def draw(self, graphics, delta_time):
        graphics.blit(self.bg, (0, 0))
        pass


class Constant:
    BG_COLOR = pygame.Color(38, 100, 100, 255)
