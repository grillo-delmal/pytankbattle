import pygame
import math

from ..controller import Controller
from ..entities import Bullet
from ..utils.consts import *

from .scene import Scene

class GameScene(Scene):
    def __init__(self, data, engine):
        super().__init__()
        self.data = data
        self.engine = engine

    def update_ps(self):
        for CD in self.data.controllers:
            p = CD.player

            if Controller.Mode.TANK in CD.mode:
                # Set movement
                if CD.move_magnitude > .3:
                    p.t.angle = CD.move_angle
                    p.t.v = TANK_MAX_SPEED * CD.move_magnitude
                else:
                    p.t.v = 0

            if Controller.Mode.CANON in CD.mode:
                # Aim canon
                if CD.point_magnitude > .3:
                    p.t.c.angle = CD.point_angle

            # Fire bullets
            if CD.btns_d[Controller.Buttons.SHOOT]:
                if p.t.c.bullets > 0 and len(self.data.bullets) < MAX_BULLETS:
                    self.data.bullets.append(Bullet(p))
                    p.t.c.bullets -= 1
                    p.t.c.reload += CANON_RELOAD_TIME

        for p in self.data.players:
            # Update counters
            if p.t.c.reload > 0:
                p.t.c.reload -= 1
                if p.t.c.reload % CANON_RELOAD_TIME == 0:
                    p.t.c.bullets += 1
            
            if p.t.inmune > 0:
                p.t.inmune -= 1

            # Update physics
            fx = ( p.t.px + p.t.v*math.cos(p.t.angle) )
            fy = ( p.t.py + p.t.v*math.sin(p.t.angle) )


            if not (fx > TANK_RADIUS and fx < WIDTH - TANK_RADIUS ):
                fx = p.t.px
                fy = p.t.py
                p.t.v = 0

            if not (fy > TANK_RADIUS and fy < HEIGHT - TANK_RADIUS ):
                fx = p.t.px
                fy = p.t.py
                p.t.v = 0

            for op in self.data.players:
                if op == p:
                    continue

                if op.active and p.t.inmune == 0:
                    if op.t.check_colision(fx, fy):
                        fx = p.t.px
                        fy = p.t.py
                        p.t.v = 0
                        
            p.t.px = fx
            p.t.py = fy

    def update_bs(self):

        dflag = False

        for b in self.data.bullets:
            # Update position
            b.px = ( b.px + BULLET_SPEED*math.cos(b.angle) )
            b.py = ( b.py + BULLET_SPEED*math.sin(b.angle) )

            # Check colisions
            for op in self.data.players:
                if op.active and op != b.owner and op.t.inmune == 0 :
                    if b.check_colision( op.t.px, op.t.py):
                        b.owner.score += 1
                        op.reset_tank()
                        b.del_b = True
                        dflag = True

            # Check for walls
            if b.px < 0 or b.px > WIDTH or b.py < 0 or b.py > HEIGHT:
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
                    self.engine.tank_img, -p.t.angle * 180 / PI)
                rotated_tank.fill(p.t.color, special_flags=pygame.BLEND_ADD)
                rotated_canon = pygame.transform.rotate(
                    self.engine.canon_img, -p.t.c.angle * 180 / PI)
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

        # TODO: Pause control
        if False:
            return self.data.State.PAUSE
        return self.data.State.GAME
