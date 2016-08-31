from zombie import *


class RunningScreen(IActivity):
    # load hinh
    def load(self):
        self.PILImage = Image.open("assets/bg.png")
        self.PILString = self.PILImage.convert("RGBA").tobytes("raw", "RGBA")
        self.backGround = pygame.image.fromstring(self.PILString, self.PILImage.size, "RGBA")

        self.PILImage = Image.open("assets/hammer.png")
        self.PILString = self.PILImage.convert("RGBA").tobytes("raw", "RGBA")
        self.cursor = pygame.image.fromstring(self.PILString, self.PILImage.size, "RGBA")

        self.font = pygame.font.SysFont("monospace", 30, bold=True)

    # thay doi game time trong nay
    def __init__(self, graphics):
        self.graphics = graphics
        self.done = False
        self.nextState = "GAMEOVER"
        self.zGroup = ZombieGroup(graphics)

        # game time
        self.timeLeft = 20

        self.ROUND_TIMER = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ROUND_TIMER, 1000)
        Zombie.hit = 0
        Zombie.miss = 0
        pygame.mouse.set_visible(False)
        self.load()

    def handleEvent(self, event):
        if event.type == self.ROUND_TIMER:
            self.timeLeft -= 1
            if self.timeLeft < 0:
                self.done = True
                return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.cursor = pygame.transform.rotate(self.cursor, 90)
        if event.type == pygame.MOUSEBUTTONUP:
            self.cursor = pygame.transform.rotate(self.cursor, -90)
        self.zGroup.handleEvent(event)

    def update(self):
        self.zGroup.update()

    def drawUI(self, graphics):
        hitText = self.font.render(" HIT: " + str(Zombie.hit), 1, (0, 0, 0))
        missText = self.font.render("MISS: " + str(Zombie.miss), 1, (0, 0, 0))
        countDown = self.font.render("TIME: " + str(self.timeLeft), 1, (0, 0, 0))
        graphics.blit(hitText, (70, 7))
        graphics.blit(missText, (70, 37))
        graphics.blit(countDown, (560, 20))

    def draw(self, graphics):
        graphics.blit(self.backGround, (0, 0))
        self.zGroup.draw(graphics)
        self.drawUI(graphics)
        graphics.blit(self.cursor, pygame.mouse.get_pos())
