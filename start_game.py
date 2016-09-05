import pygame
import math
from processing import *
from animation import *
from constants import *
import random


class StartScreen(PActivity):
    def __init__(self, context):
        super().__init__(context)
        self.backGround = BackGround(context.width, context.height)

    def draw(self, delta_time, screen, position=(0, 0)):
        self.backGround.draw(delta_time, screen)
        pass

    def on_mouse_pressed(self, button, position):
        super().on_mouse_pressed(button, position)

    def on_mouse_move(self, position, rel, buttons):
        super().on_mouse_move(position, rel, buttons)

    def on_mouse_released(self, button, position):
        super().on_mouse_released(button, position)


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
            self.logoY = self.w / 2.5 - math.sin(self.deg) * 10

        graphics.blit(self.logo, (self.logoX, self.logoY))


class BubbleFly(Animation):
    @staticmethod
    def create_random(w, h):
        return BubbleFly(random.randint(0, len(Constant.PATH_BUBBLE) - 1),
                         (random.randint(0, w), random.randint(h, h + 100)), random.randint(3, 7))

    def __init__(self, bubble_type, position, v):
        super().__init__(Constant.DATA_FOLDER + Constant.PATH_BUBBLE[bubble_type], Constant.BUBBLE_FRAME_COUNT, 100)
        self.bubble_type = bubble_type
        self.id = Constant.get_unique_int()
        self.position = position
        self.v = v

    def draw(self, delta_time, screen, position=(0, 0)):
        (x, y) = self.position
        # print(self.position)
        self.position = (x, y - self.v)
        super().draw(delta_time, screen, self.position)

    def is_alive(self):
        (x, y) = self.position
        return y > -self.height


class BubbleExp(Animation):
    @staticmethod
    def create_from_bubble(bubble):
        return BubbleExp(bubble.bubble_type, bubble.position)

    def __init__(self, bubble_type, position):
        super().__init__(Constant.DATA_FOLDER + "be_yellow.png", Constant.BUBBLE_EXP_FRAME_COUNT, 50, False)
        self.id = Constant.get_unique_int()
        self.position = position
        self.bubble_type = bubble_type

    def draw(self, delta_time, screen, position=(0, 0)):
        super().draw(delta_time, screen, self.position)


class BackGround(PDrawable):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.bg = pygame.Surface((w, h))
        self.bg.fill(Constant.BG_COLOR)
        self.bubbles = []

    def draw(self, delta_time, screen, position=(0, 0)):
        screen.blit(self.bg, position)
        if len(self.bubbles) < 17:
            self.bubbles.append(BubbleFly.create_random(self.w, self.h))

        for i in range(len(self.bubbles)):
            j = len(self.bubbles) - 1 - i
            bub = self.bubbles[j]
            bub.draw(delta_time, screen)
            (x, y) = bub.position
            if isinstance(bub, BubbleFly):
                if y < 150:
                    self.bubbles[j] = BubbleExp.create_from_bubble(bub)

        for i in range(len(self.bubbles)):
            j = len(self.bubbles) - 1 - i
            bub = self.bubbles[j]
            if not bub.is_alive():
                self.bubbles.remove(bub)

        pass
