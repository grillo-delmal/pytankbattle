
from .scene import Scene

class PauseScene(Scene):
    def __init__(self):
        super().__init__()

    def run(self):
        # TODO: Pause text

        # TODO: Quit game control
        if False:
            return GameStatus.CREDITS

        # TODO: Return to game control
        if False:
            return GameStatus.GAME
        return GameStatus.PAUSE

