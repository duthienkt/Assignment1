from zombie import *


class GameOverScreen(IActivity):
    # load assets
    def load(self):
        self.PILImage = Image.open("assets/bg.png")
        self.PILString = self.PILImage.convert("RGBA").tobytes("raw", "RGBA")
        self.backGround = pygame.image.fromstring(self.PILString, self.PILImage.size, "RGBA")

        self.PILImage = Image.open("assets/gameover.png")
        self.PILString = self.PILImage.convert("RGBA").tobytes("raw", "RGBA")
        self.retryImage = pygame.image.fromstring(self.PILString, self.PILImage.size, "RGBA")

        self.PILImage = Image.open("assets/retry2.png")
        self.PILString = self.PILImage.convert("RGBA").tobytes("raw", "RGBA")
        self.retryImage2 = pygame.image.fromstring(self.PILString, self.PILImage.size, "RGBA")

        self.PILImage = Image.open("assets/hammer.png")
        self.PILString = self.PILImage.convert("RGBA").tobytes("raw", "RGBA")
        self.cursor = pygame.image.fromstring(self.PILString, self.PILImage.size, "RGBA")

        self.font = pygame.font.SysFont("monospace", 30, bold=True)

    def __init__(self, graphics):
        self.graphics = graphics
        self.done = False
        self.nextState = "RUNNING"
        pygame.mouse.set_visible(False)
        self.load()

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.cursor = pygame.transform.rotate(self.cursor, 90)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.cursor = pygame.transform.rotate(self.cursor, -90)

    def update(self):
        pass

    def drawUI(self, graphics):
        hitText = self.font.render(" HIT: " + str(Zombie.hit), 1, (0, 0, 0))
        missText = self.font.render("MISS: " + str(Zombie.miss), 1, (0, 0, 0))
        graphics.blit(hitText, (320, 160))
        graphics.blit(missText, (320, 190))
        retryText = self.font.render("Press any key to retry", 1, (0, 0, 0))
        graphics.blit(retryText, (200, 300))

    def draw(self, graphics):
        graphics.blit(self.backGround, (0, 0))
        graphics.blit(self.retryImage2, (250, 150))
        graphics.blit(self.retryImage, (0, 280))
        self.drawUI(graphics)
        graphics.blit(self.cursor, pygame.mouse.get_pos())
