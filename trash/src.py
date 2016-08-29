import numpy
import pygame
import random
import sys
from pygame.locals import *

pygame.init()

# thay doi dc
FPS = 60
blockColumn = 5
blockRow = 5
spriteSize = 128
hit = 0
miss = 0
zombieSpawnTime = 1000  # zombie spawn moi 1s
remainingRoundTime = 10  # 20s thi het game


# initialize
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
oneSecond = 1000
# dat ten game event
round_timer_event = pygame.USEREVENT + 1
zombie_spawn_event = pygame.USEREVENT + 2
# tao matrix
zMatrix = numpy.zeros((blockRow,blockColumn))
# ve man hinh
screen = pygame.display.set_mode((spriteSize * (blockColumn + 1), spriteSize * blockRow))
pygame.display.set_caption('Zombie Game')
# game clock
fpsClock = pygame.time.Clock()
# font chu
font = pygame.font.SysFont('arial', 20)
# start/try again rectangle
startButton = Rect(250, 250, 100, 30)
# gameState 0: start screen, 1: game running, 2: game over
gameState = 0


class Zombie:
    def __init__(self, block_x, block_y):
        self.block_x = block_x
        self.block_y = block_y
        self.rectangle = Rect(block_x * spriteSize, block_y * spriteSize, spriteSize, spriteSize)


zombieList = set()


def UpdateGameState(newState):
    global gameState
    gameState = newState


def ResetGame():
    global remainingRoundTime
    global hit
    global miss
    global zombieList
    global zMatrix
    remainingRoundTime = 30
    hit = 0
    miss = 0
    zombieList = set()
    zMatrix = numpy.zeros((blockRow, blockColumn))


def DrawStartScreen():
    screen.fill(WHITE)
    textSurface = font.render('START', True, BLACK)
    screen.blit(textSurface, (250, 250))


def DrawGameOverScreen():
    screen.fill(WHITE)
    textSurface = font.render('HIT: ' + str(hit), True, BLACK)
    screen.blit(textSurface, (250, 180))
    textSurface = font.render('MISS: ' + str(miss), True, BLACK)
    screen.blit(textSurface, (250, 200))
    textSurface = font.render('TRY AGAIN', True, BLACK)
    screen.blit(textSurface, (250, 250))


def DrawGameScreen():
    screen.fill(WHITE)
    # ve zombie
    for z in zombieList:
        pygame.draw.rect(screen, BLACK, z.rectangle)
    # ve time hit miss
    textSurface = font.render('TIME: ' + str(remainingRoundTime), True, BLACK)
    screen.blit(textSurface, (spriteSize * blockColumn, 20))
    textSurface = font.render('HIT: ' + str(hit), True, BLACK)
    screen.blit(textSurface, (spriteSize * blockColumn, 40))
    textSurface = font.render('MISS: ' + str(miss), True, BLACK)
    screen.blit(textSurface, (spriteSize * blockColumn, 60))


def DrawScreen():
    if gameState == 0:
        DrawStartScreen()
    elif gameState == 1:
        DrawGameScreen()
    else:
        DrawGameOverScreen()
    pygame.display.update()


def UpdateScore(mouse_x, mouse_y):
    #neu click chuot ra ngoai man hinh thi khong tinh
    if (mouse_x < 0 or mouse_x > spriteSize*blockColumn or mouse_y < 0 or mouse_y > spriteSize*blockRow):
        return
    #else
    global hit
    global miss
    scored = False
    for z in zombieList:
        if z.rectangle.collidepoint(mouse_x, mouse_y):
            zombieList.remove(z)
            hit += 1
            scored = True
            break
    if not scored:
        miss += 1


def HandleInputAndEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if gameState == 0 or gameState == 2:
                if startButton.collidepoint(mouse_x, mouse_y):
                    ResetGame()
                    UpdateGameState(1)
                    pygame.time.set_timer(round_timer_event, oneSecond)
                    pygame.time.set_timer(zombie_spawn_event, zombieSpawnTime)
            else:
                UpdateScore(mouse_x, mouse_y)
        elif event.type == zombie_spawn_event:
            x = random.randint(0, blockColumn - 1)
            y = random.randint(0, blockRow - 1)
            global zMatrix
            if zMatrix.item(x,y) == 0:
                zMatrix.itemset((x,y),1)
                zombieList.add(Zombie(x,y))
        elif event.type == round_timer_event:
            global remainingRoundTime
            remainingRoundTime -= 1
            # het thoi gian thi chuyen gamestate = 2
            if remainingRoundTime <= 0:
                UpdateGameState(2)
                # disable cac timer
                pygame.time.set_timer(zombie_spawn_event, 0)
                pygame.time.set_timer(round_timer_event, 0)


while True:
    DrawScreen()
    HandleInputAndEvent()
    fpsClock.tick(FPS)


#a = StartScreen()
#a.draw()


