import math
from animation import *
from constants import *
import random
from physic import *


class StartScreen(PActivity):
    def __init__(self, context):
        super().__init__(context)
        self.backGround = BackGround(context)
        self.menu = Menu(context)

    def draw(self, delta_time, screen, position=(0, 0)):
        self.backGround.draw(delta_time, screen)
        self.menu.draw(delta_time, screen)
        pass

    def on_mouse_pressed(self, button, position):
        self.backGround.on_mouse_pressed(button, position)
        pass

    def on_mouse_move(self, position, rel, buttons):
        pass

    def on_mouse_released(self, button, position):
        pass


class Menu(PActivity):
    def __init__(self, context):
        super().__init__(context)
        self.w = context.width
        self.h = context.height
        self.logo = garfield_load_image(Constant.PATH_LOGO)
        self.logoX = self.w / 2 - self.logo.get_width() / 2
        self.logoY = self.h
        self.deg = 0.0
        self.v = -0.12
        self.state = 0

    def draw(self, delta_time, screen, position=(0, 0)):
        des = self.h / 4
        if self.state == 0:
            if self.logoY < des:
                self.logoY = des
                self.state = 1
            else:
                self.logoY -= delta_time / 15.0
        elif self.state == 1:
            self.deg += delta_time * 0.006
            self.logoY = des - math.sin(self.deg) * 10

        screen.blit(self.logo, (self.logoX, self.logoY))


class BubbleFly(Bubble, Interactive):
    @staticmethod
    def create_random(w, h):
        return BubbleFly(random.randint(0, len(Constant.PATH_BUBBLE) - 1),
                         (random.randint(0, w), random.randint(h, h + 100)), random.randint(3, 7))

    def __init__(self, bubble_type, position, v):
        super().__init__(bubble_type, position)
        self.v = v
        self.alive = True

    def draw(self, delta_time, screen, position=(0, 0)):
        (x, y) = self.position
        self.position = (x, y - self.v)
        super().draw(delta_time, screen)

    def is_alive(self):
        return self.alive

    def on_mouse_press_hit(self):
        self.alive = False
        return True


class BackGround(PActivity):
    def __init__(self, context):
        super().__init__(context)
        self.w = context.width
        self.h = context.height
        self.bg = pygame.Surface((self.w, self.h))
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

        for i in range(len(self.bubbles)):
            j = len(self.bubbles) - 1 - i
            bub = self.bubbles[j]
            if not bub.is_alive():
                if isinstance(bub, BubbleFly):
                    self.bubbles[j] = BubbleExp.create_from_bubble(bub)
                else:
                    self.bubbles.remove(bub)
        pass

    def on_mouse_pressed(self, button, position):
        for i in range(len(self.bubbles)):
            bub = self.bubbles[i]
            if bub.on_mouse_pressed(button, position):
                return True
        return False
