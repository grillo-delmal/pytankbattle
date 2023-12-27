
from .scene import Scene

class Pause(Scene):
    def __init__(self, data, engine):
        super().__init__(data, engine)

    def run(self):
        # TODO: Pause text

        # TODO: Quit game control
        if False:
            return GameStatus.CREDITS

        # TODO: Return to game control
        if False:
            return GameStatus.GAME
        return GameStatus.PAUSE

