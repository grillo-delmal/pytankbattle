#!/usr/bin/env python3

# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

import pygame
import math
import os

from enum import Enum, auto

#### HELPER ####

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

text_print = None

#### HEADER ####

class GameStatus(Enum):
    PAUSE   = auto()
    MENU    = auto()
    GAME    = auto()
    CREDITS = auto()
    QUIT    = auto()

PI = 3.14159265

BULLET_SPEED        = 4
BULLET_RADIUS       = 3.5

TANK_RADIUS         = 16

TANK_MAX_SPEED      = 3
CANON_RELOAD_TIME   = 120
CANON_INMUNE_TIME   = 240

MAX_BULLETS         = 100

HEIGHT              = 300
WIDTH               = 500

class MapStartPos():
    def __init__(self, px, py, angle):
        self.px = px
        self.py = py
        self.angle = angle

mstps = [ 
    MapStartPos(        50,          50,    PI/4),
    MapStartPos(WIDTH - 50,          50,  3*PI/4),
    MapStartPos(        50, HEIGHT - 50,   -PI/4),
    MapStartPos(WIDTH - 50, HEIGHT - 50, -3*PI/4),
    MapStartPos(WIDTH /  2,          50,    PI/2),
    MapStartPos(WIDTH - 50, HEIGHT /  2,    PI),
    MapStartPos(WIDTH /  2, HEIGHT - 50,   -PI/2),
    MapStartPos(        50, HEIGHT /  2,     0),
    ]

class Controller():
    def __init__(self):
        self.move_angle = 0
        self.move_magnitude = 0
        self.point_angle = 0
        self.move_magnitude = 0
        self.btns_d = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "a": False,
            "b": False,
            "shoot": False
        }


class PyGameJoystick(Controller):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        self.move_magnitude = 0
        for i in self.btns_d:
            self.btns_d[i] = False
    
    def update(self, driver):
        if driver is None:
            return
        jtype = driver.get_name()

        ljoy = [0,0]
        rjoy = [0,0]
        if jtype in ["Playstation 4 Controller", "Nintendo Switch Pro Controller"]:
            ljoy = pygame.math.Vector2(driver.get_axis(0), driver.get_axis(1)).as_polar()
            rjoy = pygame.math.Vector2(driver.get_axis(2), driver.get_axis(3)).as_polar()
        elif jtype in ["Playstation 5 Controller", "Xbox 360 Controller", "Xbox One Controller"]:
            ljoy = pygame.math.Vector2(driver.get_axis(0), driver.get_axis(1)).as_polar()
            rjoy = pygame.math.Vector2(driver.get_axis(3), driver.get_axis(4)).as_polar()

        self.move_magnitude = ljoy[0]
        self.move_angle = ljoy[1] * PI / 180

        self.point_magnitude = rjoy[0]
        self.point_angle = rjoy[1] * PI / 180

    def trigger(self, driver, button):
        if driver is None:
            return
        jtype = driver.get_name()

        if jtype in ["Playstation 4 Controller", "Nintendo Switch Pro Controller"]:
            if button == 9:
                self.btns_d["shoot"] = True
            if button == 10:
                self.btns_d["shoot"] = True
        elif jtype in ["Playstation 5 Controller", "Xbox 360 Controller", "Xbox One Controller"]:
            if button == 4:
                self.btns_d["shoot"] = True
            if button == 5:
                self.btns_d["shoot"] = True


class Canon():
    def __init__(self):
        self.angle = 0.0
        self.bullets = 5
        self.reload = 0
        self.color = "#000000"

    def reset(self, mstp: MapStartPos):
        self.bullets = 5
        self.reload = 0
        self.angle = mstp.angle
        pass


class Tank():
    def __init__(self):
        self.px = 0.0
        self.py = 0.0
        self.v = 0.0
        self.angle = 0
        self.inmune = 0
        self.color = "#000000"
        self.c = Canon()

    def reset(self, mstp: MapStartPos):
        self.v = 0.0
        self.inmune = CANON_INMUNE_TIME

        self.px = mstp.px
        self.py = mstp.py
        self.angle = mstp.angle
        self.c.reset(mstp)
    
    def check_colision(self, fx, fy):
        ## PX PY fx fy TR TR
        a = fx - self.px
        b = fy - self.py

        if (a**2 + b**2) < (TANK_RADIUS*2)**2:
            return True
        return False


class Player():
    def __init__(self, mstp: MapStartPos):
        self.active = True
        self.t = Tank()
        self.CD = None
        self.score = 0
        self.mstp = mstp

    def reset(self):
        self.score = 0
        self.active = True
        self.reset_tank()

    def reset_tank(self):
        self.t.reset(self.mstp)


class Bullet():
    def __init__(self, p: Player):
        self.owner = p
        self.del_b = False
        self.px = p.t.px + (TANK_RADIUS+BULLET_RADIUS+1) * math.cos(p.t.c.angle)
        self.py = p.t.py + (TANK_RADIUS+BULLET_RADIUS+1) * math.sin(p.t.c.angle)
        self.angle = p.t.c.angle

    def check_colision(self, tx, ty):
        a = tx - self.px
        b = ty - self.py

        if (a**2 + b**2) < (TANK_RADIUS + BULLET_RADIUS)**2:
            return True
        return False


#### HEADER END ####
players = []
bullets = []

tank_img = None
canon_img = None

#ENGINE GLOBALS
screen = None
clock = None
joysticks = {}

def reset():
    # Reset game
    for p in players:
        p.reset()

def start_up():
    global screen, clock, text_print, tank_img, canon_img

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PyTankBattle")
    clock = pygame.time.Clock()
    text_print = TextPrint()

    tank_img = pygame.image.load(
        os.path.join('assets', 'tank.png'))
    canon_img = pygame.image.load(
        os.path.join('assets', 'canon.png'))

    # FIXME: Initialize for MENU, not GAME
    pcount = pygame.joystick.get_count()
    if pcount == 0:
        return

    for i in range(pcount):
        joy = {
            "driver": pygame.joystick.Joystick(i),
            "controller": PyGameJoystick()
        }        
        joy["driver"].init()
        joysticks[joy["driver"].get_instance_id()] = joy 

        p = Player(mstps[i])
        p.CD = joy["controller"]
        players.append(p)

    reset()

def scan_pads(status):

    # Query joysticks for this frame
    for i in joysticks:
        joy = joysticks[i]
        joy["controller"].reset()
        joy["controller"].update(joy["driver"])
    
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            return GameStatus.QUIT

        if event.type == pygame.JOYBUTTONDOWN:
            joy = joysticks[event.instance_id]
            joy["controller"].trigger(joy["driver"], event.button)

        # TODO: Handle adding players on menu
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            if joy.get_instance_id() in joysticks:
                joysticks[joy.get_instance_id()]["driver"] = joy

        # TODO: Handle removing players on menu
        if event.type == pygame.JOYDEVICEREMOVED:
            if event.instance_id in joysticks:
                joysticks[event.instance_id]["driver"] = None
    

    return status

def menu():
    # TODO: Render menu
    for i in range(4):
        # TODO: Control player color
        # TODO: Control active player
        # TODO: Draw tank and colors
        pass

    # TODO: Render text

    # TODO: Only start if there are at least 2 players
    if False:
        return GameStatus.GAME

    # TODO: Quit game on exit
    if False:
        return GameStatus.QUIT

    return GameStatus.MENU

#/************************* Game *************************
def update_p(p: Player):
    # TODO: Implement pointer controller
    if isinstance(p.CD, PyGameJoystick):
        # Set movement
        if p.CD.move_magnitude > .3:
            p.t.angle = p.CD.move_angle
            p.t.v = TANK_MAX_SPEED * p.CD.move_magnitude
        else:
            p.t.v = 0

        # Aim canon
        if p.CD.point_magnitude > .3:
            p.t.c.angle = p.CD.point_angle

        # Fire bullets
        if p.CD.btns_d["shoot"]:
            if p.t.c.bullets > 0 and len(bullets) < MAX_BULLETS:
                bullets.append(Bullet(p))
                p.t.c.bullets -= 1
                p.t.c.reload += CANON_RELOAD_TIME
        
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

    for op in players:
        if op == p:
            continue

        if op.active and p.t.inmune == 0:
            if op.t.check_colision(fx, fy):
                fx = p.t.px
                fy = p.t.py
                p.t.v = 0
                
    p.t.px = fx
    p.t.py = fy

def update_bs():

    dflag = False

    for b in bullets:
        # Update position
        b.px = ( b.px + BULLET_SPEED*math.cos(b.angle) )
        b.py = ( b.py + BULLET_SPEED*math.sin(b.angle) )

        # Check colisions
        for op in players:
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
        while j < len(bullets):
            if bullets[j].del_b:
                del bullets[j]
                j -= 1
            j += 1

def draw():
    text_print.reset()

    SCREEN_MOVE_X       = 70 + 150
    SCREEN_MOVE_Y       = 60 + 60

    # Draw field
    pygame.draw.rect(
        screen,
        (255,255,255),
        pygame.Rect(SCREEN_MOVE_X, SCREEN_MOVE_Y, WIDTH, HEIGHT),
        3)
    # Draw players
    for p in players:
        if p.t.inmune % 15 < 8:
            rotated_tank = pygame.transform.rotate(
                tank_img, -p.t.angle * 180 / PI)
            rotated_canon = pygame.transform.rotate(
                canon_img, -p.t.c.angle * 180 / PI)
            screen.blit(
                rotated_tank, 
                (SCREEN_MOVE_X + p.t.px - rotated_tank.get_width() /2, 
                SCREEN_MOVE_Y + p.t.py - rotated_tank.get_height() /2))
            screen.blit(
                rotated_canon, 
                (SCREEN_MOVE_X + p.t.px - rotated_canon.get_width() /2, 
                SCREEN_MOVE_Y + p.t.py - rotated_canon.get_height() /2))

    # Draw bullets
    for b in bullets:
        pygame.draw.rect(
            screen,
            (255,255,255),
            pygame.Rect(
                SCREEN_MOVE_X + b.px, 
                SCREEN_MOVE_Y + b.py, 
                5, 5),
            1)

    # Draw text
    text_print.tprint(screen, "Tanks")
    text_print.tprint(screen, "")

    i = 1
    for p in players:
        text_print.tprint(screen, f"  Player {i}")
        text_print.tprint(screen, f"    bullets   : {p.t.c.bullets}")
        text_print.tprint(screen, f"    score     : {p.score}")
        text_print.tprint(screen, "")
        i += 1

def game():
    for p in players:
        update_p(p)
    update_bs()
    draw()

    # TODO: Pause control
    if False:
        return GameStatus.PAUSE
    return GameStatus.GAME

def pause():
    draw()
    # TODO: Pause text

    # TODO: Quit game control
    if False:
        return GameStatus.CREDITS

    # TODO: Return to game control
    if False:
        return GameStatus.GAME
    return GameStatus.PAUSE

def credits():
    # TODO: Lots of Text!!
    pass

def update_game(status: GameStatus) -> GameStatus:
    screen.fill("black")
    ret = status

    if status == GameStatus.PAUSE:
        ret = pause()
    elif status == GameStatus.MENU:
        ret = menu()
    elif status == GameStatus.GAME:
        ret = game()
    elif status == GameStatus.CREDITS:
        ret = credits()
    else:
        ret = GameStatus.QUIT
    
    pygame.display.flip()
    clock.tick(30)

    return ret

def main():
    # FIXME: START AT MENU
    status = GameStatus.GAME

    start_up()

    if len(players) <= 0:
        print("not enough players")
        status = GameStatus.QUIT

    while status != GameStatus.QUIT:
        status = scan_pads(status)
        status = update_game(status)

    pygame.quit()

if __name__ == "__main__":
    main()