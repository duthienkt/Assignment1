import pygame
from pygame.locals import *

__author__ = "Pham Quoc Du Thien"
__date__ = "Aug 22, 2016"
__name__ = "__main__"
caption = "pyGame  template"


def setting():
    size(800, 900)
    # to do:
    pass


def setup():
    frame_rate(10)
    pass


def draw():
    if (frameCount % fps == 0):
        print(frameCount / fps)
    pygame.time.delay(10)
    pass


def update():
    pass


#########################My library for pyGame, convert it to Processing################################################
width = 800  # default screen width
height = 600  # default screen height
graphics = None
frameCount = 0
fps = 60
duration = 1000 // fps
lastUpdateTime = 0


def frame_rate(rate):
    global fps
    global duration
    fps = rate
    duration = 1000 // fps


def size(w, h, cap=caption):
    global graphics
    global width
    global height
    width = w
    height = h
    graphics = pygame.display.set_mode((w, h))
    pygame.display.set_caption(cap)


def _wait_for_next():
    global lastUpdateTime
    current_time = pygame.time.get_ticks()
    remain_time = duration - current_time + lastUpdateTime
    if (remain_time > 0):
        pygame.time.delay(remain_time)
    lastUpdateTime = pygame.time.get_ticks()


def main():
    global frameCount
    # Initialise screen
    pygame.init()
    setting()

    # Fill background
    # background = pygame.Surface(graphics.get_size())
    # background = background.convert()
    # background.fill((250, 250, 250))

    # Display some text
    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello There", 1, (10, 10, 10))
    # textpos = text.get_rect()
    # textpos.centerx = background.get_rect().centerx
    # background.blit(text, textpos)
    #
    # # Blit everything to the screen
    # graphics.blit(background, (0, 0))
    # graphics.blit(background, (200, 200))
    # pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        update()
        frameCount += 1
        _wait_for_next()
        draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
