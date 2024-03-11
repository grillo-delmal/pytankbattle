from enum import Enum, auto

class GameState(Enum):
    PAUSE   = auto()
    MENU    = auto()
    GAME    = auto()
    RESULT  = auto()
    CREDITS = auto()
    QUIT    = auto()


class Data():

    def __init__(self):
        self.players = []
        self.bullets = []
        self.controllers = []

        self.state = None

