from animation import Animation
from constants import Constant
from processing import *
from garfield import garfield_load_image, garfield_pick_color, garfield_sound_play, garfield_font
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

    def on_mouse_pressed(self, button, position):
        return False

    def on_mouse_released(self, button, position):
        return False

    def on_mouse_move(self, position, rel, buttons):
        pass


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

    def on_mouse_released(self, button, position):
        return False

    def on_mouse_pressed(self, button, position):
        return False


class ArrowCursor(Animation, Interactive):
    def __init__(self):
        super().__init__(Constant.PATH_ARROW_CURSOR, Constant.ARROW_CURSOR_FRAME_COUNT, 50)
        self.position = (0, 0)
        self.isLoop = False
        self.go = False

    def on_mouse_move(self, position, rel, buttons):
        self.position = position

    def draw(self, delta_time, screen, position=(0, 0)):
        (x, y) = self.position
        x -= 11
        y -= 14
        if self.go:
            super().draw(delta_time, screen, (x, y))
        if not self.is_alive():
            self.restart()
            self.go = False
        if not self.go:
            super().draw(0, screen, (x, y))

    def on_mouse_released(self, button, position):

        return False

    def on_mouse_pressed(self, button, position):
        self.go = True
        self.restart()
        return False


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

    @staticmethod
    def create_random_from_box(position):
        return BubbleFly(random.randint(0, len(Constant.PATH_BUBBLE) - 1),
                         position, random.randint(3, 7))

    def __init__(self, bubble_type, position, v):
        super().__init__(bubble_type, position)
        (x, y) = position
        x -= self.width / 2
        self.position = (x, y)
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


class ButtonPower(Button):
    def __init__(self, context, position):
        super().__init__(context, position, Constant.DATA_FOLDER + Constant.PATH_BUTTON_UP[Constant.BUTTON_POWER],
                         Constant.DATA_FOLDER + Constant.PATH_BUTTON_DOWN[Constant.BUTTON_POWER])
        self.isPressed = False

    def on_mouse_pressed(self, button, position):
        self.isPressed = super().on_mouse_pressed(button, position)
        return self.isPressed

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

    def on_mouse_released(self, button, position):
        if super().on_mouse_released(button, position):
            if self.isPressed:
                self.isPressed = False
                self.context.activity.onHandle()
            return True
        return False


class ScoreBoard(PDrawable):
    def __init__(self):
        self.fontPath = Constant.DATA_FOLDER + "ka1.ttf"
        self.hit = 0
        self.miss = 0
        self.font = garfield_font(self.fontPath, 60)
        self.hitIm = self.font.render("Hit  " + str(self.hit), True, Constant.COLOR_BLUE)
        self.missIm = self.font.render("Miss " + str(self.miss), True, Constant.COLOR_RED)

    def draw(self, delta_time, screen, position=(0, 0)):
        screen.blit(self.hitIm, position)
        (x, y) = position
        screen.blit(self.missIm, (x + 370, y))

    def set_hit(self, hit):
        self.hit = hit
        self.hitIm = self.font.render("Hit  " + str(self.hit), True, Constant.COLOR_BLUE)

    def set_miss(self, miss):
        self.miss = miss
        self.missIm = self.font.render("Miss " + str(self.miss), True, Constant.COLOR_RED)

    def inc_hit(self, delta):
        self.set_hit(self.hit + delta)

    def inc_miss(self, delta):
        self.set_miss(self.miss + delta)


class BubblePlay(Bubble):
    def __init__(self, bubble_type, position, score_board):
        super().__init__(bubble_type, (0, 0))
        self.scoreBoard = score_board
        (x, y) = position
        x -= self.width / 2
        self.position = (x, y)
        self.position0 = self.position
        self.alive = True
        c = max(16000 - score_board.hit * 500 + score_board.miss * 250, 2000)
        self.hideTime = random.randint(200, c + 3000)
        self.stayTime = self.hideTime / 4
        self.delta = 0
        self.waitTime = 0
        self.v = 50
        self.willLost = False

    @staticmethod
    def create_random(position, score_board):
        return BubblePlay(random.randint(0, len(Constant.PATH_BUBBLE) - 1), position, score_board)

    def on_mouse_pressed(self, button, position):
        return super().on_mouse_pressed(button, position)

    def draw(self, delta_time, screen, position=(0, 0)):
        if self.v > 0:
            if self.delta >= 0:
                if self.willLost:
                    self.willLost = False
                    self.scoreBoard.inc_miss(1)
                self.waitTime += delta_time
                if self.waitTime > self.hideTime:
                    self.waitTime = 0
                    self.v = -50
            else:
                self.delta += self.v * delta_time / 1000.0
                self.willLost = True

        else:
            if self.delta <= -self.height / 1.5:
                self.waitTime += delta_time
                if self.waitTime > self.stayTime:
                    self.waitTime = 0
                    self.v = 50
            else:
                self.delta += self.v * delta_time / 1000.0

        (x, y) = self.position0

        self.position = (x, y + self.delta)
        super().draw(delta_time, screen)

    def on_mouse_press_hit(self):
        self.scoreBoard.inc_hit(1)
        self.alive = False
        garfield_sound_play(Constant.DATA_FOLDER + "pop.ogg")
        return True

    def is_alive(self):
        return self.alive
