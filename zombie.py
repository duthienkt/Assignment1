import pygame
from random import randint
from PIL import Image
from pygame import *
from my_interface import *


class Zombie(IActivity):
    classInitialized = False
    spriteArray = []
    hit = 0
    miss = 0

    @classmethod
    def __init_class__(cls, graphics):
        Zombie.classInitialized = True
        # load sprite sheet
        PILImage = Image.open("assets/diglet_sheet.png")
        PILString = PILImage.convert("RGBA").tobytes("raw", "RGBA")
        spriteSheet = pygame.image.fromstring(PILString, PILImage.size, "RGBA")
        spriteSheet = spriteSheet.convert_alpha()
        spriteWidth, spriteHeight = (105, 93)
        # array chua tung subsurface trong sprite sheet
        for i in range(6):
            Zombie.spriteArray.append(spriteSheet.subsurface((i * spriteWidth, 0), (spriteWidth, spriteHeight)))

    def __init__(self, position, graphics):
        if (not Zombie.classInitialized):
            Zombie.__init_class__(graphics)

        self.position = position
        self.dead = True
        self.index = 0
        self.image = Zombie.spriteArray[self.index]
        self.graphics = graphics
        self.despawnTime = randint(2000, 4000)
        self.DESPAWN_EVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.DESPAWN_EVENT, 500)

    # animation di len di xuong
    def moveUp(self):
        if (self.index < 5):
            self.index += 1
            self.image = Zombie.spriteArray[self.index]

    def moveDown(self):
        if (self.index > 0):
            self.index -= 1
            self.image = Zombie.spriteArray[self.index]

    def reset(self):
        self.despawnTime = randint(2000, 4000)
        self.dead = False

    def handleEvent(self, event):
        if (event.type == self.DESPAWN_EVENT and not self.dead):
            self.despawnTime -= 500
            if self.despawnTime <= 0:
                self.dead = True
                Zombie.miss += 1

        elif (event.type == pygame.MOUSEBUTTONDOWN and not self.dead):
            mousepos = mouse.get_pos()
            (x, y) = self.position
            if ((x, y) <= mousepos <= (x + 105, y + 93)):
                self.dead = True
                Zombie.hit += 1

    def update(self):
        if (self.dead):
            self.moveDown()
        else:
            self.moveUp()

    def draw(self, graphics):
        graphics.blit(self.image, self.position)


class ZombieGroup(IActivity):
    def __init__(self, graphics):
        self.graphics = graphics
        # array chua cac vi tri bat dau xuat hien cua zombie
        self.positionArray = []
        for i in range(4):
            for j in range(3):
                self.positionArray.append((125 + i * 150, 100 + j * 150))

                # list cac zombie instances
            self.zombieList = []
            for i in range(self.positionArray.__len__()):
                self.zombieList.append(Zombie(self.positionArray[i], self.graphics))
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, 1000)

    def handleEvent(self, event):
        if (event.type == self.SPAWN_EVENT):
            rd = randint(0, self.zombieList.__len__() - 1)
            if (self.zombieList[rd].dead):
                self.zombieList[rd].reset()
        else:
            for z in self.zombieList:
                z.handleEvent(event)

    def update(self):
        for z in self.zombieList:
            z.update()

    def draw(self, graphics):
        for z in self.zombieList:
            z.draw(graphics)
