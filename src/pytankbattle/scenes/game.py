import pygame
import math

from pytankbattle.controller import Controller
from pytankbattle.entities import Bullet
from pytankbattle.utils.consts import *


def update_ps(game):
    for CD in game.controllers:
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
            if p.t.c.bullets > 0 and len(game.bullets) < MAX_BULLETS:
                game.bullets.append(Bullet(p))
                p.t.c.bullets -= 1
                p.t.c.reload += CANON_RELOAD_TIME

    for p in game.players:
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

        for op in game.players:
            if op == p:
                continue

            if op.active and p.t.inmune == 0:
                if op.t.check_colision(fx, fy):
                    fx = p.t.px
                    fy = p.t.py
                    p.t.v = 0
                    
        p.t.px = fx
        p.t.py = fy

def update_bs(game):

    dflag = False

    for b in game.bullets:
        # Update position
        b.px = ( b.px + BULLET_SPEED*math.cos(b.angle) )
        b.py = ( b.py + BULLET_SPEED*math.sin(b.angle) )

        # Check colisions
        for op in game.players:
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
        while j < len(game.bullets):
            if game.bullets[j].del_b:
                del game.bullets[j]
                j -= 1
            j += 1

def draw(game):
    game.screen.fill("black")

    game.text_print.reset()

    # Draw field
    pygame.draw.rect(
        game.screen,
        (255,255,255),
        pygame.Rect(SCREEN_MOVE_X, SCREEN_MOVE_Y, WIDTH, HEIGHT),
        3)
    # Draw players
    for p in game.players:
        if p.t.inmune % 15 < 8:
            rotated_tank = pygame.transform.rotate(
                game.tank_img, -p.t.angle * 180 / PI)
            rotated_tank.fill(p.t.color, special_flags=pygame.BLEND_ADD)
            rotated_canon = pygame.transform.rotate(
                game.canon_img, -p.t.c.angle * 180 / PI)
            rotated_canon.fill(p.t.c.color, special_flags=pygame.BLEND_ADD)
            game.screen.blit(
                rotated_tank, 
                (SCREEN_MOVE_X + p.t.px - rotated_tank.get_width() /2, 
                SCREEN_MOVE_Y + p.t.py - rotated_tank.get_height() /2))
            game.screen.blit(
                rotated_canon, 
                (SCREEN_MOVE_X + p.t.px - rotated_canon.get_width() /2, 
                SCREEN_MOVE_Y + p.t.py - rotated_canon.get_height() /2))

    # Draw bullets
    for b in game.bullets:
        pygame.draw.rect(
            game.screen,
            (255,255,255),
            pygame.Rect(
                SCREEN_MOVE_X + b.px, 
                SCREEN_MOVE_Y + b.py, 
                5, 5),
            1)

    # Draw text
    game.text_print.tprint(game.screen, "Tanks")
    game.text_print.tprint(game.screen, "")

    i = 1
    for p in game.players:
        game.text_print.tprint(game.screen, f"  Player {i}")
        game.text_print.tprint(game.screen, f"    bullets   : {p.t.c.bullets}")
        game.text_print.tprint(game.screen, f"    score     : {p.score}")
        game.text_print.tprint(game.screen, "")
        i += 1

def game(game):
    update_ps(game)
    update_bs(game)
    draw(game)

    # TODO: Pause control
    if False:
        return game.State.PAUSE
    return game.State.GAME
