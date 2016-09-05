import pygame
from pygame.locals import *

from garfield import *


class PDrawable:
    def draw(self, delta_time, screen, position=(0, 0)):
        pass


class PActivity(PDrawable, Interactive):
    def __init__(self, context):
        self.context = context
