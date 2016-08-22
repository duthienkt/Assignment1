import pygame
from pygame.locals import *

__author__ = "Pham Quoc Du Thien"
__date__ = "Aug 22, 2016"
__name__ = "__main__"

myImage = None
myImage2 = None

def setting():
    # you must call size(_, _)
    size(800, 900, "Zoombie")
    # to do:
    pass


def setup():
    frame_rate(10)
    global myImage
    global myImage2
    myImage = load_image("ff14.jpg")
    myImage2 = scale_image(myImage, 200, 200)
    pass


def draw():
    draw_image(myImage, 0, 0)
    draw_image(myImage2, 100, 100)
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
caption = "pyGame  template"


def frame_rate(rate):
    global fps
    global duration
    fps = rate
    duration = 1000 // fps


def load_image(path):
    return pygame.image.load(path)


def draw_image(img, x, y):
    graphics.blit(img, (x, y))


def scale_image(surface, w, h):
    return pygame.transform.scale(surface, (w, h))

def draw_line(Surface, color, start_pos, end_pos, width=1):
    pass
def _wait_for_next():
    global lastUpdateTime
    current_time = pygame.time.get_ticks()
    remain_time = duration - current_time + lastUpdateTime
    if (remain_time > 0):
        pygame.time.delay(remain_time)
    lastUpdateTime = pygame.time.get_ticks()


def size(w, h, cap=caption):
    global graphics
    global width
    global height
    width = w
    height = h
    graphics = pygame.display.set_mode((w, h))
    pygame.display.set_caption(cap)


def main():
    global frameCount
    # Initialise screen
    pygame.init()
    setting()
    setup()
    setup()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        update()
        frameCount += 1
        draw()
        _wait_for_next()
        pygame.display.update()


if __name__ == '__main__':
    main()
