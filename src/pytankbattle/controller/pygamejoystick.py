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

    def trigger(self, event_type, button):
        if self.driver is None:
            return
        jtype = self.driver.get_name()

        if event_type == pygame.JOYHATMOTION:
            if button[0] < 0:
                self.btns_d[Controller.Buttons.LEFT] = True
            if button[0] > 0:
                self.btns_d[Controller.Buttons.RIGHT] = True
            if button[1] < 0:
                self.btns_d[Controller.Buttons.DOWN] = True
            if button[1] > 0:
                self.btns_d[Controller.Buttons.UP] = True

        if event_type == pygame.JOYBUTTONDOWN:
            if jtype in ["Playstation 4 Controller", "Nintendo Switch Pro Controller"]:
                if button == 0:
                    self.btns_d[Controller.Buttons.A] = True
                if button == 1:
                    self.btns_d[Controller.Buttons.B] = True
                if button == 9:
                    self.btns_d[Controller.Buttons.SHOOT] = True
                if button == 10:
                    self.btns_d[Controller.Buttons.SHOOT] = True
                if button == 11:
                    self.btns_d[Controller.Buttons.UP] = True
                if button == 12:
                    self.btns_d[Controller.Buttons.DOWN] = True
                if button == 13:
                    self.btns_d[Controller.Buttons.LEFT] = True
                if button == 14:
                    self.btns_d[Controller.Buttons.RIGHT] = True
            elif jtype in ["Playstation 5 Controller", "Xbox 360 Controller", "Xbox One Controller"]:
                if button == 0:
                    self.btns_d[Controller.Buttons.A] = True
                if button == 1:
                    self.btns_d[Controller.Buttons.B] = True
                if button == 4:
                    self.btns_d[Controller.Buttons.SHOOT] = True
                if button == 5:
                    self.btns_d[Controller.Buttons.SHOOT] = True

