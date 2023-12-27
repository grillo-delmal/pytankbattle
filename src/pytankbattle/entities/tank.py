from pytankbattle.utils import MapStartPos
from pytankbattle.utils.consts import CANON_INMUNE_TIME, TANK_RADIUS
from .canon import Canon

class Tank():
    def __init__(self, color):
        self.px = 0.0
        self.py = 0.0
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
    
    def check_colision(self, fx, fy):
        ## PX PY fx fy TR TR
        a = fx - self.px
        b = fy - self.py

        if (a**2 + b**2) < (TANK_RADIUS*2)**2:
            return True
        return False
