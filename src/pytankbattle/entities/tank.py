from ..map import MapStartPos
from ..utils.consts import CANON_INMUNE_TIME, TANK_RADIUS, TANK_MAX_SPEED
from .canon import Canon
from .collidable import Collidable

import math

class Tank(Collidable):
    def __init__(self, color):
        super().__init__(0, 0, TANK_RADIUS)

        self.v = 0.0
        self.angle = 0
        self.inmune = 0
        self.color = color
        self.c = Canon(color)

    def reset(self, mstp: MapStartPos):
        self.v = 0.0
        self.inmune = CANON_INMUNE_TIME

        self.px = mstp.px
        self.py = mstp.py
        self.angle = mstp.angle
        self.c.reset(mstp)

    def apply_control(self, CD):
        if CD.move_magnitude > .3:
            self.angle = CD.move_angle
            self.v = TANK_MAX_SPEED * CD.move_magnitude
        else:
            self.v = 0

    def get_new_pos(self):
        return (
            ( self.px + self.v*math.cos(self.angle) ),
            ( self.py + self.v*math.sin(self.angle) ))

    def update_counters(self):
        self.c.update_counters()
        
        if self.inmune > 0:
            self.inmune -= 1
