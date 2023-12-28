
from .scene import Scene

class MenuScene(Scene):
    def __init__(self):
        super().__init__()

    def run(self):
        # TODO: Render menu
        for i in range(4):
            # TODO: Control player color
            # TODO: Control active player
            # TODO: Draw tank and colors
            pass

        # TODO: Render text

        # TODO: Only start if there are at least 2 players
        if False:
            return GameStatus.GAME

        # TODO: Quit game on exit
        if False:
            return GameStatus.QUIT

        return GameStatus.MENU
