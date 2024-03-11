from ..map import MapStartPos
from .tank import Tank
from ..utils.consts import MAX_BULLETS


class Player():
    def __init__(self, mstp: MapStartPos, playerColor):
        self.active = True
        self.t = Tank(playerColor)
        self.score = 0
        self.mstp = mstp

    def reset(self):
        self.score = 0
        self.active = True
        self.reset_tank()

    def reset_tank(self):
        self.t.reset(self.mstp)
