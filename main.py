from garfield import *
from start_game import StartScreen


class MainGame(Garfield):
    def __init__(self):
        super().__init__()
        self.activity = None

    def setup(self):
        self.frame_rate(25)
        self.size((900, 600))
        self.activity = StartScreen(self)
        pass

    def on_mouse_move(self, position, rel, buttons):
        self.activity.on_mouse_move(position, rel, buttons)
        pass

    def on_mouse_pressed(self, button, position):
        self.activity.on_mouse_pressed(button, position)
        pass

    def setting(self):
        pass

    def on_mouse_released(self, button, position):
        self.activity.on_mouse_released(button, position)

    def draw(self, screen=None, position=(0, 0)):
        self.activity.draw(self.deltaTime, self.screen)
        pass


MainGame().__main__()
