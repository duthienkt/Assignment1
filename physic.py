from animation import Animation
from constants import Constant
from processing import *
from garfield import garfield_load_image, garfield_pick_color, garfield_sound_play
import random
import math


class Bubble(Animation, Interactive):
    def __init__(self, bubble_type, position):
        super().__init__(Constant.DATA_FOLDER + Constant.PATH_BUBBLE[bubble_type], Constant.BUBBLE_FRAME_COUNT, 100)
        self.bubble_type = bubble_type
        self.id = Constant.get_unique_int()
        self.position = position

    def draw(self, delta_time, screen, position=(0, 0)):
        super().draw(delta_time, screen, self.position)

    def on_mouse_pressed(self, button, position):
        (x, y) = position
        (x0, y0) = self.position
        x -= x0
        y -= y0
        c = self.pick_color((x, y))
        if c is not None:
            (r, g, b, a) = c
            if a > 10:
                return self.on_mouse_press_hit()
        return False

    @abstractmethod
    def on_mouse_press_hit(self):
        """implement this method to handle event"""
        return False


class BubbleExp(Animation, Interactive):
    @staticmethod
    def create_from_bubble(bubble):
        return BubbleExp(bubble.bubble_type, bubble.position)

    def __init__(self, bubble_type, position):
        super().__init__(Constant.DATA_FOLDER + Constant.PATH_BUBBLE_EXP[bubble_type], Constant.BUBBLE_EXP_FRAME_COUNT,
                         30, False)
        self.id = Constant.get_unique_int()
        self.position = position
        self.bubble_type = bubble_type

    def draw(self, delta_time, screen, position=(0, 0)):
        super().draw(delta_time, screen, self.position)


class Button(PActivity):
    def __init__(self, context, position, path1, path2):
        super().__init__(context)
        self.image = garfield_load_image(path1)
        self.pressedImage = garfield_load_image(path2)
        self.currentImage = self.image
        self.position = position

    def draw(self, delta_time, screen, position=(0, 0)):
        screen.blit(self.currentImage, self.position)

    def on_mouse_pressed(self, button, position):
        (x, y) = position
        (x0, y0) = self.position
        c = garfield_pick_color(self.currentImage, (x - x0, y - y0))
        if c is not None:
            (r, g, b, a) = c
            if a > 50:
                self.currentImage = self.pressedImage
                return True
        return False

    def on_mouse_released(self, button, position):
        if not self.currentImage == self.pressedImage:
            return
        self.currentImage = self.image
        (x, y) = position
        (x0, y0) = self.position
        c = garfield_pick_color(self.currentImage, (x - x0, y - y0))
        if c is not None:
            (r, g, b, a) = c
            if a > 50:
                return True
        return False


class NormalCursor(Animation, Interactive):
    def __init__(self):
        super().__init__(Constant.PATH_NORMAL_CURSOR, Constant.NORMAL_CURSOR_FRAME_COUNT, 300)
        self.position = (0, 0)

    def on_mouse_move(self, position, rel, buttons):
        self.position = position

    def draw(self, delta_time, screen, position=(0, 0)):
        super().draw(delta_time, screen, self.position)


class ButtonFly(Button):
    def __init__(self, context, position0, position1, path1, path2):
        super().__init__(context, position0, path1, path2)
        self.position0 = position0
        self.position1 = position1
        self.clicked = False

    def draw(self, delta_time, screen, position=(0, 0)):
        (vx0, vy0) = self.position
        (vx1, vy1) = self.position1
        dx = vx1 - vx0
        dy = vy1 - vy0
        l = math.sqrt(dx * dx + dy * dy)

        if self.clicked and l < 1:
            self.clicked = False
            self.on_click()
        elif l >= 1:

            dx /= l
            dy /= l
            l = delta_time / 20.0 * math.log(1 + l / 5.0)
            dx *= l
            dy *= l
            self.position = (vx0 + dx, vy0 + dy)
        super().draw(delta_time, screen, self.position)

    def on_mouse_released(self, button, position):
        res = super().on_mouse_released(button, position)
        if res and not self.clicked:
            t = self.position0
            self.position0 = self.position1
            self.position1 = t
            self.clicked = True
        return res

    def on_click(self):

        pass


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
        if y < -self.height:
            self.alive = False
            return
        self.position = (x, y - self.v)
        super().draw(delta_time, screen)

    def is_alive(self):
        return self.alive

    def on_mouse_press_hit(self):
        self.alive = False
        garfield_sound_play(Constant.DATA_FOLDER + "pop.ogg")
        return True
