from pytankbattle.utils import MapStartPos


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


