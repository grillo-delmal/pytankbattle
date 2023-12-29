import pygame
import math

from .controller import Controller
from ..utils.consts import WIDTH, HEIGHT, SCREEN_MOVE_X, SCREEN_MOVE_Y, PI

class PyGameKeyboardMouse(Controller):
    def __init__(self):
        super().__init__()

    def update(self):
        keys = pygame.key.get_pressed()

        # UPDATE direction
        if keys[pygame.K_w] and keys[pygame.K_s]:
            self.move_magnitude = 0
        elif keys[pygame.K_a] and keys[pygame.K_d]:
            self.move_magnitude = 0
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            self.move_angle = -3*PI/4
            self.move_magnitude = 1
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            self.move_angle = -PI/4
            self.move_magnitude = 1
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.move_angle = 3*PI/4
            self.move_magnitude = 1
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.move_angle = PI/4
            self.move_magnitude = 1
        elif keys[pygame.K_w]:
            self.move_angle = -PI/2
            self.move_magnitude = 1
        elif keys[pygame.K_s]:
            self.move_angle = PI/2
            self.move_magnitude = 1
        elif keys[pygame.K_a]:
            self.move_angle = PI
            self.move_magnitude = 1
        elif keys[pygame.K_d]:
            self.move_angle = 0
            self.move_magnitude = 1

        # UPDATE canon direction
        if self.player is None:
            return
        
        mxpos = pygame.mouse.get_pos()
        self.cx = max(0, min(WIDTH, mxpos[0] - SCREEN_MOVE_X))
        self.cy = max(0, min(HEIGHT, mxpos[1] - SCREEN_MOVE_Y))

        #FIXME if mouse over tank, mag 0
        self.point_magnitude = 1
        self.point_angle = math.atan2(  self.cy - self.player.t.py, self.cx - (self.player.t.px) )

    def trigger(self, event_type, button):
        if event_type == pygame.KEYDOWN:
            if button in (pygame.K_w, pygame.K_UP):
                self.btns_d[Controller.Buttons.UP] = True
            if button in (pygame.K_s, pygame.K_DOWN):
                self.btns_d[Controller.Buttons.DOWN] = True
            if button in (pygame.K_a, pygame.K_LEFT):
                self.btns_d[Controller.Buttons.LEFT] = True
            if button in (pygame.K_d, pygame.K_RIGHT):
                self.btns_d[Controller.Buttons.RIGHT] = True
            if button == pygame.K_RETURN:
                self.btns_d[Controller.Buttons.A] = True
            if button == pygame.K_BACKSPACE:
                self.btns_d[Controller.Buttons.B] = True

        if event_type == pygame.MOUSEBUTTONDOWN:
            if button == 1 or button == 3:
                self.btns_d[Controller.Buttons.SHOOT] = True

