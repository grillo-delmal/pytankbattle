import pygame
import math

from ..controller import Controller
from ..entities import Bullet
from ..map import check_map_collision
from ..utils.consts import SCREEN_MOVE_X, SCREEN_MOVE_Y, WIDTH, HEIGHT
from ..utils.data import GameState

from .scene import Scene

class GameScene(Scene):
    def __init__(self, engine, data):
        super().__init__()
        self.engine = engine
        self.data = data
        self.pause = False

    def reset(self):
        self.pause = False

    def update_ps(self):
        for CD in self.data.controllers:
            p = CD.player
            if p is None or CD.mode is None:
                continue

            # Check for pause
            if CD.btns_d[Controller.Buttons.PAUSE]:
                self.pause = True

            if Controller.Mode.TANK in CD.mode:
                # Set movement
                p.t.apply_control(CD)

            if Controller.Mode.CANON in CD.mode:
                # Aim canon
                p.t.c.apply_control(CD)

            # Fire bullets
            if CD.btns_d[Controller.Buttons.SHOOT]:
                if p.t.c.shoot_canon(len(self.data.bullets)):
                    self.data.bullets.append(Bullet(p))

        for p in self.data.players:
            # Update counters
            p.t.update_counters()

            # Update physics
            fx, fy = p.t.get_new_pos()
            if check_map_collision(p.t, fx, fy):
                fx = p.t.px
                fy = p.t.py
                p.t.v = 0

            for op in self.data.players:
                if op == p:
                    continue

                if op.active and p.t.inmune == 0:
                    if op.t.check_colision(p.t, fx, fy):
                        fx = p.t.px
                        fy = p.t.py
                        p.t.v = 0
                        
            p.t.px = fx
            p.t.py = fy

    def update_bs(self):
        dflag = False

        for b in self.data.bullets:
            # Update position
            b.px, b.py = b.get_new_pos()

            # Check colisions
            for op in self.data.players:
                if op.active and op != b.owner and op.t.inmune == 0 :
                    if b.check_colision(op.t):
                        b.owner.score += 1
                        op.reset_tank()
                        b.del_b = True
                        dflag = True

            # Check for walls
            if check_map_collision(b):
                b.del_b = True
                dflag = True

        if dflag:
            j = 0
            while j < len(self.data.bullets):
                if self.data.bullets[j].del_b:
                    del self.data.bullets[j]
                    j -= 1
                j += 1

    def draw(self):
        self.engine.screen.fill("black")

        self.engine.text_print.reset()

        # Draw field
        pygame.draw.rect(
            self.engine.screen,
            (255,255,255),
            pygame.Rect(SCREEN_MOVE_X, SCREEN_MOVE_Y, WIDTH, HEIGHT),
            3)
        # Draw players
        for p in self.data.players:
            if p.t.inmune % 15 < 8:
                rotated_tank = pygame.transform.rotate(
                    self.engine.tank_img, -p.t.angle * 180 / math.pi)
                rotated_tank.fill(p.t.color, special_flags=pygame.BLEND_ADD)
                rotated_canon = pygame.transform.rotate(
                    self.engine.canon_img, -p.t.c.angle * 180 / math.pi)
                rotated_canon.fill(p.t.c.color, special_flags=pygame.BLEND_ADD)
                self.engine.screen.blit(
                    rotated_tank, 
                    (SCREEN_MOVE_X + p.t.px - rotated_tank.get_width() /2, 
                    SCREEN_MOVE_Y + p.t.py - rotated_tank.get_height() /2))
                self.engine.screen.blit(
                    rotated_canon, 
                    (SCREEN_MOVE_X + p.t.px - rotated_canon.get_width() /2, 
                    SCREEN_MOVE_Y + p.t.py - rotated_canon.get_height() /2))

        # Draw bullets
        for b in self.data.bullets:
            pygame.draw.rect(
                self.engine.screen,
                (255,255,255),
                pygame.Rect(
                    SCREEN_MOVE_X + b.px, 
                    SCREEN_MOVE_Y + b.py, 
                    5, 5),
                1)

        # Draw text
        self.engine.text_print.tprint(self.engine.screen, "Tanks")
        self.engine.text_print.tprint(self.engine.screen, "")

        i = 1
        for p in self.data.players:
            self.engine.text_print.tprint(self.engine.screen, f"  Player {i}")
            self.engine.text_print.tprint(self.engine.screen, f"    bullets   : {p.t.c.bullets}")
            self.engine.text_print.tprint(self.engine.screen, f"    score     : {p.score}")
            self.engine.text_print.tprint(self.engine.screen, "")
            i += 1

    def run(self):
        self.update_ps()
        self.update_bs()
        self.draw()

        for p in self.data.players:
            if p.score == 10:
                return GameState.RESULT

        # Pause control
        if self.pause:
            self.pause = False
            return GameState.PAUSE
        return GameState.GAME
