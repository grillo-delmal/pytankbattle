import math
from ..utils.consts import TANK_RADIUS, BULLET_RADIUS, BULLET_SPEED
from .player import Player
from .collidable import Collidable

class Bullet(Collidable):
    def __init__(self, p: Player):
        super().__init__(
            p.t.px + (TANK_RADIUS+BULLET_RADIUS+1) * math.cos(p.t.c.angle),
            p.t.py + (TANK_RADIUS+BULLET_RADIUS+1) * math.sin(p.t.c.angle),
            BULLET_RADIUS
        )
        self.owner = p
        self.del_b = False
        self.angle = p.t.c.angle

    def get_new_pos(self):
        return (
            ( self.px + BULLET_SPEED*math.cos(self.angle) ),
            ( self.py + BULLET_SPEED*math.sin(self.angle) ))
