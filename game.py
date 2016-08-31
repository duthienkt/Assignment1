import sys
from start_game import *
from running_game import *
from game_over import *

"""
    Simple State Machine
    ---------------------
    Chuyen state, goi cac draw, handleEvent, update cua cac state

"""


class Game:
    def __init__(self, graphics):
        self.graphics = graphics
        self.clock = pygame.time.Clock()
        self.stateList = {"START", "RUNNING", "GAMEOVER"}

        self.fps = 60
        self.duration = 1000 // 60
        self.lastUpdateTime = 0

        self.currentState = RunningScreen(self.graphics)  # doi thanh START state

    # set & get state
    def setState(self, nextState):
        if nextState == "START":
            self.currentState = StartScreen(self.graphics)
        elif nextState == "RUNNING":
            self.currentState = RunningScreen(self.graphics)
        elif nextState == "GAMEOVER":
            self.currentState = GameOverScreen(self.graphics)

    def getState(self):
        return self.currentState

    def handleEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == QUIT:
                sys.exit()
            else:
                self.currentState.handleEvent(event)

    # Check for state change
    # currentState.done = True de chuyen sang nextState
    # set currentState.nextState = "START" hoac "RUNNING" hoac "GAMEOVER"
    def update(self):

        if self.currentState.done:
            nextState = self.currentState.nextState
            self.setState(nextState)
        else:
            self.currentState.update()

    def draw(self):
        self.currentState.draw(self.graphics)

    def _wait_for_next(self):
        current_time = pygame.time.get_ticks()
        remain_time = self.duration - current_time + self.lastUpdateTime
        if (remain_time > 0):
            pygame.time.delay(remain_time)
        current_time = pygame.time.get_ticks()
        self.deltaTime = current_time - self.lastUpdateTime
        self.lastUpdateTime = current_time

    # gameloop trong nay
    def run(self):
        while 1:
            self.handleEvent()
            self.update()
            self.draw()
            pygame.display.flip()
            # self.clock.tick(self.fps)
            self._wait_for_next()
