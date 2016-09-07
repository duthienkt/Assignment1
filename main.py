from constants import Constant
from garfield import *
from start_game import StartScreen
from physic import NormalCursor, ButtonPower


class MainGame(Garfield):
    def __init__(self):
        super().__init__()
        self.activity = None
        self.cursor = NormalCursor()
        pygame.mouse.set_visible(False)
        self.powerOff = None

    def setup(self):
        self.frame_rate(25)
        self.size((800, 600))
        self.activity = StartScreen(self)
        garfield_music_load(Constant.PATH_BACKGROUND_SOUND)
        garfield_music_play(-1)
        self.powerOff = ButtonPower(self, (self.width - 80, self.height - 80))
        pass

    def on_mouse_move(self, position, rel, buttons):
        self.powerOff.on_mouse_move(position, rel, buttons)
        self.cursor.on_mouse_move(position, rel, buttons)
        self.activity.on_mouse_move(position, rel, buttons)
        pass

    def on_mouse_pressed(self, button, position):
        if self.powerOff.on_mouse_pressed(button, position):
            return
        self.activity.on_mouse_pressed(button, position)
        pass

    def setting(self):
        pass

    def on_mouse_released(self, button, position):
        if self.powerOff.on_mouse_released(button, position):
            return
        self.activity.on_mouse_released(button, position)

    def draw(self, screen=None, position=(0, 0)):
        self.activity.draw(self.deltaTime, self.screen)
        self.powerOff.draw(self.deltaTime, self.screen)
        self.cursor.draw(self.deltaTime, self.screen)
        pass

    def start_activity(self, act):
        self.activity = act

    def set_cursor(self, cursor):
        self.cursor = cursor

    def exit(self):
        garfield_music_stop()
        super().exit()


MainGame().__main__()
