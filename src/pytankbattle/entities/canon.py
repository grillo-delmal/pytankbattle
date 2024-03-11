from ..map import MapStartPos
from ..utils.consts import CANON_RELOAD_TIME, MAX_BULLETS


class Canon():
    def __init__(self, color):
        self.angle = 0.0
        self.bullets = 5
        self.reload = 0
        self.color = color

    def reset(self, mstp: MapStartPos):
        self.bullets = 5
        self.reload = 0
        self.angle = mstp.angle
        pass

    def apply_control(self, CD):
        if CD.point_magnitude > .3:
            self.angle = CD.point_angle

    def shoot_canon(self, bullet_cant):
        if self.bullets > 0 and bullet_cant < MAX_BULLETS:
            self.bullets -= 1
            self.reload += CANON_RELOAD_TIME
            return True
        return False
    
    def update_counters(self):
        if self.reload > 0:
            self.reload -= 1
            if self.reload % CANON_RELOAD_TIME == 0:
                self.bullets += 1

