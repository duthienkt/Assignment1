import IActivity


class GameScreen(IActivity):
    def __init__(self):
        pass
    def draw(self):
        print("draw")

    def handleEvent(self, events):
        print(events)

