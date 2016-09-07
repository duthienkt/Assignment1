import math
from animation import *
from constants import *
import random
from physic import *


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
        self.buttons = []

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
            if len(self.buttons) < 2:
                self.buttons.append(ExitButton(self.context, self.buttons))
                self.buttons.append(PlayButton(self.context, self.buttons))

        screen.blit(self.logo, (self.logoX, self.logoY))
        for button in self.buttons:
            button.draw(delta_time, screen)

    def on_mouse_pressed(self, button, position):
        for button in self.buttons:
            if button.on_mouse_pressed(button, position):
                return True

        (x, y) = position
        c = garfield_pick_color(self.logo, (x - self.logoX, y - self.logoY))
        if c is not None:
            (r, g, b, a) = c
            if a > 200:
                return True
        return False

    def on_mouse_released(self, button, position):
        for button in self.buttons:
            if button.on_mouse_released(button, position):
                return True
        return super().on_mouse_released(button, position)


class MenuButton(ButtonFly):
    def __init__(self, context, button_list, button_id, y):
        self.buttonList = button_list
        im = garfield_load_image(Constant.DATA_FOLDER + Constant.PATH_BUTTON_UP[button_id])
        super().__init__(context, ((context.width - im.get_width()) / 2, context.height + y),
                         ((context.width - im.get_width()) / 2, context.height / 3 + y * 2),
                         Constant.DATA_FOLDER + Constant.PATH_BUTTON_UP[button_id],
                         Constant.DATA_FOLDER + Constant.PATH_BUTTON_DOWN[button_id])

    def on_mouse_released(self, button, position):
        if super().on_mouse_released(button, position):
            for other in self.buttonList:
                if not other == self:
                    (x, y) = other.position
                    other.position1 = (x + 1000, y)


class ExitButton(MenuButton):
    def __init__(self, context, button_list):
        super().__init__(context, button_list, Constant.BUTTON_EXIT, 150)

    def on_click(self):
        self.context.exit()


class PlayButton(MenuButton):
    def __init__(self, context, button_list):
        super().__init__(context, button_list, Constant.BUTTON_PLAY, 60)


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
            if isinstance(bub, BubbleFly) and bub.on_mouse_pressed(button, position):
                return True
        return False


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
        if self.menu.on_mouse_pressed(button, position):
            return True
        self.backGround.on_mouse_pressed(button, position)

    def on_mouse_move(self, position, rel, buttons):
        pass

    def on_mouse_released(self, button, position):
        self.menu.on_mouse_released(button, position)
        pass
