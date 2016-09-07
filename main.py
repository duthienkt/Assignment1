from garfield import *
from start_game import StartScreen
from physic import NormalCursor

class MainGame(Garfield):
    def __init__(self):
        super().__init__()
        self.activity = None
        self.cursor = NormalCursor()
        pygame.mouse.set_visible(False)

    def setup(self):
        self.frame_rate(25)
        self.size((900, 600))
        self.activity = StartScreen(self)
        garfield_music_load("assets/background.mp3")
        garfield_music_play(-1)
        pass

    def on_mouse_move(self, position, rel, buttons):
        self.cursor.on_mouse_move(position, rel, buttons)
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
