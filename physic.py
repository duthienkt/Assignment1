from animation import Animation
from constants import Constant
from processing import *


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

    @abstractproperty
    def on_mouse_press_hit(self):
        """implement this method to handle event"""
        return False


class BubbleExp(Animation):
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
