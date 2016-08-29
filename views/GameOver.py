
import pygame
from os import path

"""VRS-@Copyright 2016"""

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

"""RESOURCE CLASS"""
class Resource(object):

    ASSETS_DIR = "assets"

    @staticmethod
    def getFolderPath(folderPath):
        return path.join(path.dirname(__file__) + "/../", folderPath)

    @staticmethod
    def getAssetsResFile(fileName):
        filePath = path.join(Resource.getFolderPath(Resource.ASSETS_DIR), fileName);
        return filePath;

"""BASE SPRITE - ANY OTHER SPRITE CLASSES MUST BE DERIVED FROM BaseSprite"""

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, surface, ww, wh):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.ww = ww
        self.wh = wh
        self.background = (0, 0, 0)

"""================================== IMAGE_VIEW================================================"""

"""ImageSprite - SUPPORT FOR RENDERING IMAGE ON SURFACE"""
class ImageSprite(BaseSprite):
    def __init__(self, surface, ww, wh):
        BaseSprite.__init__(self, surface, ww, wh)

    def setImageFileName(self, imgPath):
        self.image = pygame.image.load(Resource.getAssetsResFile(imgPath))
        self.rect = self.image.get_rect()

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def update(self):
        self.draw()

    def scale(self):
        pass
"""================================== END OF IMAGE_VIEW================================================"""

"""================================== TEXT_VIEW================================================"""

"""TEXT BASE CLASS = SUPPORT FOR RENDERING TEXT ON SURFACE"""
class TextBase(BaseSprite):

    def __init__(self, surface, ww, hh):
        BaseSprite.__init__(self, surface, ww, hh)
        self.text = "TextBase"
        self.fontName =  pygame.font.match_font('arial')
        self.fontSize = 22
        self.font = self.getFont()
        self.color = (255, 255, 255) #WHITE
        self.x = 0
        self.y = 0

    def getFont(self):
        self.font = pygame.font.Font(self.fontName, self.fontSize);
        return self.font;

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setText(self, text):
        self.text = text

    def setTextColor(self, color):
        self.color = color

    def configFont(self, font_name, font_size):
        self.fontName =  pygame.font.match_font('arial')
        self.fontSize = font_size
        self.font = self.getFont()

    def getSurfaceRender(self):
        return self.font.render(self.text, True, self.color);

    def draw(self):
        self.textRender = self.getSurfaceRender()
        self.rect = self.textRender.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.surface.blit(self.textRender, self.rect)

    def update(self):
        self.draw()

"""TEXT DRAWABLE == SUPPORT ANIMATION"""
class TextDrawable(TextBase):

    # class OnTextDraw(object):
    #     def onFinished(self):
    #         pass

    def __init__(self, surface, ww, wh):
        TextBase.__init__(self, surface, ww, wh)
        self.step = 2 # character(s) will be appended to draw
        self.slice_time = 100 # millisecond
        self.currentDur = 0
        self.textAll = ""
        self.textLen = 0
        self.lastTime = 0
        self.l = None

    def setOnDrawFinishedListener(self, l):
        self.l = l

    def setSliceTime(self, slice_time):
        self.slice_time = slice_time

    def setText(self, text):
        self.textAll = text
        TextBase.setText(self, "")
        self.textLen = len(self.textAll)

    def draw(self):
        if (pygame.time.get_ticks() - self.lastTime) < self.slice_time:
            TextBase.draw(self)
            return

        if (self.currentDur + self.step) >= self.textLen:
            self.text = self.textAll
            if self.l is not None:
                self.l();
        else:
            self.text += (self.textAll[self.currentDur : self.currentDur + self.step])
        TextBase.draw(self)
        self.currentDur += self.step
        self.lastTime = pygame.time.get_ticks()

"""================================== END OF TEXT_VIEW================================================"""


"""GameOverTile - SUPPORT ANIMATION"""
class GameOverTile(ImageSprite):

    IMG_RES = "defeat.png"

    def __init__(self, surface, ww, wh):
        ImageSprite.__init__(self, surface, ww, wh)
        self.isDrawDone = False
        self.l = None
        self.setImageFileName(GameOverTile.IMG_RES)

    def update(self):
        self.rect.x += 0
        if self.rect.y <= self.wh / 10.0:
            self.rect.y += 4
        elif not self.isDrawDone and self.l is not None:
            self.l()
        self.draw()

    def setOnDrawFinishedListener(self, l):
        self.l = l

"""======================================GAME OVER======================================"""

class GameOver(object):

    HEIGHT = 600;
    WIDTH = 800;

    def __init__(self):
        self.surface = pygame.display.set_mode((800, 600))
        self.sprites = pygame.sprite.Group()
        self.initElements()
        self.FPS = 60
        self.clock = pygame.time.Clock()  ## For syncing the FPS

    def prepare(self):
        pass

    def initElements(self):
        self.govT = GameOverTile(self.surface, self.WIDTH, self.HEIGHT)
        self.govT.setOnDrawFinishedListener(self.onGOVDrawFinished)
        self.sprites.add(self.govT)


        pos_x_base = 80;
        pos_y_base = 320
        text_y_space = 30;

        self.txtScore = self.newTextDrawable("Your Score: 50 point", pos_x_base, pos_y_base)
        self.txtScore.setOnDrawFinishedListener(self.onTextScoreDrawFinished)

        self.txtLevel = self.newTextDrawable("Your Level: 5", pos_x_base, pos_y_base + text_y_space )
        self.txtLevel.setOnDrawFinishedListener(self.onTextLevelDrawFinished)

        self.txtHelp = self.newTextDrawable("Press [Back Space] to back to Home, press [Enter] to retry",
                                             pos_x_base, pos_y_base + text_y_space * 2 )

    def newTextDrawable(self, text, pos_x, pos_y):
        text_size = 26
        text_font = "Stencil";
        text_color = (255, 0, 0)
        slice_time = 0

        new_text = TextDrawable(self.surface, GameOver.WIDTH, GameOver.HEIGHT)
        new_text.setText(text)
        new_text.setTextColor(text_color)
        new_text.setPosition(pos_x, pos_y)
        new_text.setSliceTime(slice_time);
        new_text.configFont(text_font, text_size)
        return new_text

    def onGOVDrawFinished(self):
        self.sprites.add(self.txtScore)
        self.sprites.add(self.txtLevel)
        self.sprites.add(self.txtHelp)

    def onTextScoreDrawFinished(self):
        self.sprites.add(self.txtLevel)

    def onTextLevelDrawFinished(self):
        self.sprites.add(self.txtHelp)

    def draw(self):
        self.sprites.draw(self.surface)

    def update(self):
        self.sprites.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them.
                ## listening for the the X button at the top
                if event.type == pygame.QUIT:
                    running = False

            self.surface.fill(BLACK)
            gameOver.update()
            pygame.display.flip()

            self.clock.tick(self.FPS)
        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    gameOver = GameOver();
    gameOver.run()
