import pygame

from enum import Enum, auto
from .controller import Controller
from ..utils.consts import PI

class PyGameJoystick(Controller):
    class CtrlType(Enum):
        PS4     = auto()
        PS5     = auto()
        NSwPro  = auto()
        Xbox360 = auto()
        XboxOne = auto()

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        match self.driver.get_name():
            case "Playstation 4 Controller":
                self.jtype = self.CtrlType.PS4
            case "Playstation 5 Controller":
                self.jtype = self.CtrlType.PS5
            case "Nintendo Switch Pro Controller":
                self.jtype = self.CtrlType.NSwPro
            case "Xbox 360 Controller":
                self.jtype = self.CtrlType.Xbox360
            case "Xbox One Controller":
                self.jtype = self.CtrlType.XboxOne
        self.reset()

    def update(self):
        if self.driver is None:
            return

        ljoy = [0,0]
        rjoy = [0,0]
        if self.jtype in [self.CtrlType.PS4, self.CtrlType.NSwPro]:
            ljoy = pygame.math.Vector2(self.driver.get_axis(0), self.driver.get_axis(1)).as_polar()
            rjoy = pygame.math.Vector2(self.driver.get_axis(2), self.driver.get_axis(3)).as_polar()
        elif self.jtype in [self.CtrlType.PS5, self.CtrlType.Xbox360, self.CtrlType.XboxOne]:
            ljoy = pygame.math.Vector2(self.driver.get_axis(0), self.driver.get_axis(1)).as_polar()
            rjoy = pygame.math.Vector2(self.driver.get_axis(3), self.driver.get_axis(4)).as_polar()

        self.move_magnitude = ljoy[0]
        self.move_angle = ljoy[1] * PI / 180

        self.point_magnitude = rjoy[0]
        self.point_angle = rjoy[1] * PI / 180

    def trigger(self, event_type, button):
        if self.driver is None:
            return

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
            if self.jtype in [self.CtrlType.PS4, self.CtrlType.NSwPro]:
                if button == 0:
                    self.btns_d[Controller.Buttons.A] = True
                if button == 1:
                    self.btns_d[Controller.Buttons.B] = True
                if button == 6:
                    self.btns_d[Controller.Buttons.PAUSE] = True
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
            if self.jtype in [self.CtrlType.PS5, self.CtrlType.Xbox360, self.CtrlType.XboxOne]:
                if button == 0:
                    self.btns_d[Controller.Buttons.A] = True
                if button == 1:
                    self.btns_d[Controller.Buttons.B] = True
                if button == 4:
                    self.btns_d[Controller.Buttons.SHOOT] = True
                if button == 5:
                    self.btns_d[Controller.Buttons.SHOOT] = True
            
            # Other
            if self.jtype == self.CtrlType.PS5:
                if button == 9:
                    self.btns_d[Controller.Buttons.PAUSE] = True
            if self.jtype in [self.CtrlType.Xbox360, self.CtrlType.XboxOne]:
                if button == 7:
                    self.btns_d[Controller.Buttons.PAUSE] = True

