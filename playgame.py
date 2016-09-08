from physic import *
from garfield import  garfield_add_music

class PlayGame(PActivity, PListener):
    def __init__(self, context):
        super().__init__(context)
        self.bgPlay = [garfield_load_image(Constant.DATA_FOLDER + Constant.PATH_PLAY_IMAGE[0]),
                       garfield_load_image(Constant.DATA_FOLDER + Constant.PATH_PLAY_IMAGE[1]),
                       garfield_load_image(Constant.DATA_FOLDER + Constant.PATH_PLAY_IMAGE[2]),
                       garfield_load_image(Constant.DATA_FOLDER + Constant.PATH_PLAY_IMAGE[3])]

        self.scoreBoard = ScoreBoard()
        self.bubbles = []
        self.isOver = False
        for i in range(16):
            self.bubbles.append(BubblePlay.create_random(Constant.AXIS_BOX[i], self.scoreBoard))
        self.overBT = GameOver(self.context)
        context.set_cursor(ArrowCursor())

    def on_mouse_pressed(self, button, position):
        if self.overBT.on_mouse_pressed(button, position):
            return True
        (x, y) = position
        y -= 535
        c = garfield_pick_color(self.bgPlay[3], (x, y))

        if c is not None:
            return True

        for i in range(11, 16):
            if self.bubbles[i].on_mouse_pressed(button, position):
                return True
        (x, y) = position
        y -= 488
        c = garfield_pick_color(self.bgPlay[2], (x, y))
        if c is not None:
            return True

        for i in range(5, 11):
            if self.bubbles[i].on_mouse_pressed(button, position):
                return True
        (x, y) = position
        y -= 456
        c = garfield_pick_color(self.bgPlay[2], (x, y))
        if c is not None:
            return True

        for i in range(5):
            if self.bubbles[i].on_mouse_pressed(button, position):
                return True

    def on_mouse_move(self, position, rel, buttons):
        self.overBT.on_mouse_move(position, rel, buttons)
        super().on_mouse_move(position, rel, buttons)

    def draw(self, delta_time, screen, position=(0, 0)):

        screen.blit(self.bgPlay[0], (0, 0))

        for i in range(5):
            self.bubbles[i].draw(delta_time, screen)

        screen.blit(self.bgPlay[1], (0, 456))
        for i in range(5, 11):
            self.bubbles[i].draw(delta_time, screen)

        screen.blit(self.bgPlay[2], (0, 488))
        for i in range(11, 16):
            self.bubbles[i].draw(delta_time, screen)

        screen.blit(self.bgPlay[3], (0, 535))

        (x, y) = self.overBT.position
        y += self.overBT.height
        self.scoreBoard.draw(delta_time, screen, (100, max(30, y)))
        if not self.isOver:
            if self.scoreBoard.miss >= 99:
                self.game_over()
        else:
            self.overBT.draw(delta_time, screen)
        for i in range(len(self.bubbles)):
            if not self.bubbles[i].is_alive():
                if not isinstance(self.bubbles[i], BubbleExp):
                    self.bubbles[i] = BubbleExp.create_from_bubble(self.bubbles[i])
                else:
                    if not self.isOver:
                        self.bubbles[i] = BubblePlay.create_random(Constant.AXIS_BOX[i], self.scoreBoard)
                    else:
                        self.bubbles[i] = BubbleFly.create_random_from_box(Constant.AXIS_BOX[i])

    def on_mouse_released(self, button, position):
        return self.overBT.on_mouse_released(button, position)

    def game_over(self):
        garfield_add_music(Constant.PATH_BACKGROUND_SOUND[0])
        self.bubbles = []
        self.isOver = True
        for i in range(16):
            self.bubbles.append(BubbleFly.create_random_from_box(Constant.AXIS_BOX[i]))

    def onHandle(self):
        if self.isOver:
            self.context.start_activity("start")
        self.game_over()


class GameOver(ButtonFly):
    def on_click(self):
        self.context.start_activity("play")
        garfield_add_music(Constant.PATH_BACKGROUND_SOUND[random.randint(0, 10000)% 3])

    def __init__(self, context):
        im = garfield_load_image(Constant.DATA_FOLDER + Constant.PATH_BUTTON_UP[Constant.BUTTON_OVER])
        self.width = im.get_width()
        self.height = im.get_height()
        x = (context.width - self.width) / 2
        super().__init__(context, (x, -self.height - 200), (x, 100),
                         Constant.DATA_FOLDER + Constant.PATH_BUTTON_UP[Constant.BUTTON_OVER],
                         Constant.DATA_FOLDER + Constant.PATH_BUTTON_DOWN[Constant.BUTTON_OVER])

    def on_mouse_move(self, position, rel, buttons):
        (x, y) = position
        (x0, y0) = self.position
        c = garfield_pick_color(self.currentImage, (x - x0, y - y0))
        if c is not None:
            (r, g, b, a) = c
            if a > 50:
                self.currentImage = self.pressedImage
                return
        self.currentImage = self.image
