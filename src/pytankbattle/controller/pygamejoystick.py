import pygame

from .controller import Controller
from ..utils.consts import PI

class PyGameJoystick(Controller):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.reset()

    def update(self):
        if self.driver is None:
            return
        jtype = self.driver.get_name()

        ljoy = [0,0]
        rjoy = [0,0]
        if jtype in ["Playstation 4 Controller", "Nintendo Switch Pro Controller"]:
            ljoy = pygame.math.Vector2(self.driver.get_axis(0), self.driver.get_axis(1)).as_polar()
            rjoy = pygame.math.Vector2(self.driver.get_axis(2), self.driver.get_axis(3)).as_polar()
        elif jtype in ["Playstation 5 Controller", "Xbox 360 Controller", "Xbox One Controller"]:
            ljoy = pygame.math.Vector2(self.driver.get_axis(0), self.driver.get_axis(1)).as_polar()
            rjoy = pygame.math.Vector2(self.driver.get_axis(3), self.driver.get_axis(4)).as_polar()

        self.move_magnitude = ljoy[0]
        self.move_angle = ljoy[1] * PI / 180

        self.point_magnitude = rjoy[0]
        self.point_angle = rjoy[1] * PI / 180

    def trigger(self, button):
        if self.driver is None:
            return
        jtype = self.driver.get_name()

        if jtype in ["Playstation 4 Controller", "Nintendo Switch Pro Controller"]:
            if button == 9:
                self.btns_d[Controller.Buttons.SHOOT] = True
            if button == 10:
                self.btns_d[Controller.Buttons.SHOOT] = True
        elif jtype in ["Playstation 5 Controller", "Xbox 360 Controller", "Xbox One Controller"]:
            if button == 4:
                self.btns_d[Controller.Buttons.SHOOT] = True
            if button == 5:
                self.btns_d[Controller.Buttons.SHOOT] = True

