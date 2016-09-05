from abc import abstractmethod

from garfield import Interactive


class PDrawable:
    @abstractmethod
    def draw(self, delta_time, screen, position=(0, 0)):
        pass


class PActivity(PDrawable, Interactive):
    def __init__(self, context):
        self.context = context
