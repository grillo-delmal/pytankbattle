import math
from pytankbattle.utils.consts import *
from .player import Player

class Bullet():
    def __init__(self, p: Player):
        self.owner = p
        self.del_b = False
        self.px = p.t.px + (TANK_RADIUS+BULLET_RADIUS+1) * math.cos(p.t.c.angle)
        self.py = p.t.py + (TANK_RADIUS+BULLET_RADIUS+1) * math.sin(p.t.c.angle)
        self.angle = p.t.c.angle

    def check_colision(self, tx, ty):
        a = tx - self.px
        b = ty - self.py

        if (a**2 + b**2) < (TANK_RADIUS + BULLET_RADIUS)**2:
            return True
        return False
