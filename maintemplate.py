import pygame
from pygame.locals import *
from start_game import *
from my_interface import *
from game import *

graphics = None
__name__ = "__main__"
width = 800  # default screen width
height = 600  # default screen height
fps = 45
duration = 1000 // fps
lastUpdateTime = 0
deltaTime = 0


class StateChangeListener(OnClicktListener):
    def onClick(self, act):
        global currentState
        currentState = act


currentState = None


def frame_rate(rate):
    global fps
    global duration
    fps = rate
    duration = 1000 // fps


'''
#Moved to game.py


def _wait_for_next():
    global lastUpdateTime
    global deltaTime
    current_time = pygame.time.get_ticks()
    remain_time = duration - current_time + lastUpdateTime
    if (remain_time > 0):
        pygame.time.delay(remain_time)
    current_time = pygame.time.get_ticks()
    deltaTime = current_time - lastUpdateTime
    lastUpdateTime = current_time
'''

def init_windows(w, h, cap="Assignment 1"):
    global graphics
    global width
    global height
    pygame.init()
    width = w
    height = h
    graphics = pygame.display.set_mode((w, h))
    pygame.display.set_caption(cap)


def main():
    init_windows(800, 600)

    '''
    #Moved to game.py

    currentState = StartScreen(graphics, StateChangeListener())
    while 1:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                return
        currentState.handleEvent(events)
        currentState.draw(deltaTime)
        pygame.display.update() #pygame.display.flip() tot hon
        _wait_for_next()
    '''

    game = Game(graphics)
    game.run()

if __name__ == '__main__':
    main()
