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

    def draw(self, graphic, delta_time):
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

    v = -0.12
    state = 0

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.logo = pygame.image.load("assets/LOGO.png")
        self.logoX = w / 2 - self.logo.get_width() / 2
        self.logoY = h

    def draw(self, graphics, delta_time):
        if self.state == 0:
            if (self.logoY < self.w / 2.5):
                self.logoY = self.w / 2.5
                self.state = 1
            else:
                self.logoY -= delta_time / 15.0
        elif self.state == 1:
            self.deg += delta_time * 0.006
            self.logoY = self.w / 2.5-math.sin(self.deg)*10

        graphics.blit(self.logo, (self.logoX, self.logoY))


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
