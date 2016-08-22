from my_interface import IActivity
import pygame
from pygame.locals import *

class StartScreen(IActivity):
    listener = None
    def __init__(self, listener):
        self.listener = listener
        pass
    def draw(self):
        print("draw")

    def handleEvent(self, events):
        for event in  events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.listener.onClick(None)
            else:
                self.listener.onClick(StartScreen(self.listener))


        print(events)

