
from enum import Enum, Flag, auto
from pytankbattle.entities import Player


class Controller():
    class Mode(Flag):
        TANK   = auto()
        CANON  = auto()
        BOTH   = TANK | CANON

    class Buttons(Enum):
        UP    = auto()
        DOWN  = auto()
        LEFT  = auto()
        RIGHT = auto()
        A     = auto()
        B     = auto()
        SHOOT = auto()

    def __init__(self):
        self.move_angle = 0
        self.move_magnitude = 0
        self.point_angle = 0
        self.point_magnitude = 0
        self.btns_d = {
            self.Buttons.UP: False,
            self.Buttons.DOWN: False,
            self.Buttons.LEFT: False,
            self.Buttons.RIGHT: False,
            self.Buttons.A: False,
            self.Buttons.B: False,
            self.Buttons.SHOOT: False
        }

        self.player = None
        self.mode = None

    def reset(self):
        self.move_magnitude = 0
        for i in self.btns_d:
            self.btns_d[i] = False
    
    def setPlayer(self, player: Player, mode: Mode):
        self.player = player
        self.mode = mode

