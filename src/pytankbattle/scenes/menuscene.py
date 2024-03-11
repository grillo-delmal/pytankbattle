# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

from enum import Enum, auto

from ..controller import Controller
from ..map import mstps
from ..entities import Player
from .scene import Scene
from ..utils.data import GameState
from ..utils.consts import playerColors

import pygame

class CursorState(Enum):
    ADD_TANK = auto()
    REMOVE_TANK = auto()
    SELECT_TANK = auto()
    SELECTING_TANK = auto()
    SELECT_COLOR = auto()
    SELECTING_COLOR = auto()
    START = auto()


class MenuScene(Scene):
    class FlowStep():
        def __init__(
                self, act, 
                left:CursorState, right:CursorState, 
                b:CursorState=None, a:CursorState=None):
            self.act = act
            self.left = left
            self.right = right
            self.a = a
            self.b = b

    class Cursor():
        def __init__(self, controller:Controller):
            self.controller = controller
            self.pos = CursorState.ADD_TANK

            self.controller_i = 0
            self.tank_i = 0
            self.color_i = 0
            self.color_t = Controller.Mode.BOTH
       
    def __init__(self, engine, data):
        super().__init__()
        self.engine = engine
        self.controllers = data.controllers
        self.players = data.players
        self.data = data

        self.flow = {
            CursorState.ADD_TANK:
                self.FlowStep(
                    self.add_tank, 
                    None, CursorState.REMOVE_TANK),
            CursorState.REMOVE_TANK:     
                self.FlowStep(
                    self.remove_tank, 
                    CursorState.ADD_TANK, CursorState.SELECT_TANK),
            CursorState.SELECT_TANK:
                self.FlowStep(
                    None,
                    CursorState.REMOVE_TANK, CursorState.SELECT_COLOR,
                    a=CursorState.SELECTING_TANK),
            CursorState.SELECTING_TANK: 
                self.FlowStep(
                    self.select_tank, 
                    None, None,
                    b=CursorState.SELECT_TANK),
            CursorState.SELECT_COLOR:
                self.FlowStep(
                    None,
                    CursorState.SELECT_TANK, CursorState.START,
                    a=CursorState.SELECTING_COLOR),
            CursorState.SELECTING_COLOR: 
                self.FlowStep(
                    self.select_color, 
                    None, None,
                    b=CursorState.SELECT_COLOR),
            CursorState.START:
                self.FlowStep(
                    self.start,
                    CursorState.SELECT_COLOR, None)
        }
        self.reset()
    
    def reset(self):
        self.start_game = False
        self.cursors = []

    def add_tank(self, cur):
        if cur.controller.btns_d[Controller.Buttons.A]:
            pi = len(self.players)
            if pi >= len(playerColors):
                return
            if pi >= len(self.controllers):
                return
            p = Player(mstps[pi], playerColors[pi])
            self.players.append(p)
            if cur.controller is None:
                cur.controller.setPlayer(p, Controller.Mode.BOTH)
            else:
                for c in self.controllers:
                    if c.player is None:
                        c.setPlayer(p, Controller.Mode.BOTH)
                        break

    def remove_tank(self, cur):
        if cur.controller.btns_d[Controller.Buttons.A]:
            if len(self.players) == 0:
                return
            rmi = len(self.players) - 1
            rmp = self.players[rmi]

            for c in self.controllers:
                if rmp == c.player:
                    c.player = None

            del self.players[rmi]

    def reset_cursor(self, cur):
        cur.controller_i = 0
        cur.tank_i = -1
        if self.controllers[cur.controller_i].player is not None:
            for i in range(len(self.players)):
                if self.players[i] == self.controllers[cur.controller_i].player:
                    cur.tank_i = i
                    break

    def select_tank(self, cur):
        # LR select tank
        if cur.controller.btns_d[Controller.Buttons.LEFT]:
            cur.tank_i = (cur.tank_i - 1) % (len(self.players) + 1)
            if cur.tank_i < 0 or cur.tank_i >= len(self.players) or len(self.players) == 0:
                self.controllers[cur.controller_i].player = None
            else:
                self.controllers[cur.controller_i].player = self.players[cur.tank_i]
                self.controllers[cur.controller_i].mode = Controller.Mode.BOTH
        elif cur.controller.btns_d[Controller.Buttons.RIGHT]:
            cur.tank_i = (cur.tank_i + 1) % (len(self.players) + 1)
            if cur.tank_i < 0 or cur.tank_i >= len(self.players) or len(self.players) == 0:
                self.controllers[cur.controller_i].player = None
            else:
                self.controllers[cur.controller_i].player = self.players[cur.tank_i]
                self.controllers[cur.controller_i].mode = Controller.Mode.BOTH

        # UD select controller
        elif cur.controller.btns_d[Controller.Buttons.UP]:
            cur.controller_i = (cur.controller_i - 1) % len(self.controllers)
            cur.tank_i = -1
            if self.controllers[cur.controller_i].player is not None:
                for i in range(len(self.players)):
                    if self.players[i] == self.controllers[cur.controller_i].player:
                        cur.tank_i = i
                        break

        elif cur.controller.btns_d[Controller.Buttons.DOWN]:
            cur.controller_i = (cur.controller_i + 1) % len(self.controllers)
            cur.tank_i = -1
            if self.controllers[cur.controller_i].player is not None:
                for i in range(len(self.players)):
                    if self.players[i] == self.controllers[cur.controller_i].player:
                        cur.tank_i = i
                        break

        # A change tank mode
        elif cur.controller.btns_d[Controller.Buttons.A]:
            if self.controllers[cur.controller_i].player is not None:
                old_mode = self.controllers[cur.controller_i].mode
                if old_mode == Controller.Mode.BOTH:
                    self.controllers[cur.controller_i].mode = Controller.Mode.TANK
                elif old_mode == Controller.Mode.TANK:
                    self.controllers[cur.controller_i].mode = Controller.Mode.CANON
                else:
                    self.controllers[cur.controller_i].mode = Controller.Mode.BOTH


    def select_color(self, cur):
        # LR select tank - color
        if len(self.players) == 0:
            return
        cur.tank_i %= len(self.players)

        if cur.controller.btns_d[Controller.Buttons.LEFT]:
            cur.color_i -= 1
            if cur.color_i < 0:
                cur.color_i = 2
                cur.tank_i = (cur.tank_i - 1) % len(self.players)
        elif cur.controller.btns_d[Controller.Buttons.RIGHT]:
            cur.color_i += 1
            if cur.color_i > 2:
                cur.color_i = 0
                cur.tank_i = (cur.tank_i + 1) % len(self.players)

        # UD select color
        elif cur.controller.btns_d[Controller.Buttons.UP]:
            if Controller.Mode.TANK in cur.color_t:
                color = list(self.players[cur.tank_i].t.color) 
                if color[cur.color_i] < 0xCC:
                    color[cur.color_i] += 0x11
                else:
                    color[cur.color_i] = 0xCC
                self.players[cur.tank_i].t.color = tuple(color)
            if Controller.Mode.CANON in cur.color_t:
                color = list(self.players[cur.tank_i].t.c.color) 
                if color[cur.color_i] < 0xCC:
                    color[cur.color_i] += 0x11
                else:
                    color[cur.color_i] = 0xCC
                self.players[cur.tank_i].t.c.color = tuple(color)

        elif cur.controller.btns_d[Controller.Buttons.DOWN]:
            if Controller.Mode.TANK in cur.color_t :
                color = list(self.players[cur.tank_i].t.color) 
                if color[cur.color_i] > 0x22:
                    color[cur.color_i] -= 0x11
                else:
                    color[cur.color_i] = 0x22
                self.players[cur.tank_i].t.color = tuple(color)
            if Controller.Mode.CANON in cur.color_t:
                color = list(self.players[cur.tank_i].t.c.color) 
                if color[cur.color_i] > 0x22:
                    color[cur.color_i] -= 0x11
                else:
                    color[cur.color_i] = 0x22
                self.players[cur.tank_i].t.c.color = tuple(color)

        # A change tank / canon
        elif cur.controller.btns_d[Controller.Buttons.A]:
            old_mode = cur.color_t
            if old_mode == Controller.Mode.BOTH:
                cur.color_t = Controller.Mode.TANK
            elif old_mode == Controller.Mode.TANK:
                cur.color_t = Controller.Mode.CANON
            else:
                cur.color_t = Controller.Mode.BOTH

    def start(self, cur):
        if cur.controller.btns_d[Controller.Buttons.A]:
            if len(self.data.players) < 2:
                return

            for p in self.data.players:
                p.reset()

            self.start_game = True

    def draw(self):

        self.engine.screen.fill("black")
        title_bmp = self.engine.font_big.render(
            "pyTankBattle", 
            True, 
            (255, 255, 255))
        if len(self.cursors) == 0:
            self.engine.screen.blit(
                title_bmp,
                (400 - title_bmp.get_width()/2, 250))
            text_bmp = self.engine.font_normal.render(
                "Press the A / Enter button to continue", 
                True, 
                (255, 255, 255))
            self.engine.screen.blit(
                text_bmp,
                (400 - text_bmp.get_width()/2, 350))
            return

        self.engine.screen.blit(
            title_bmp,
            (400 - title_bmp.get_width()/2, 50))
        
        # Draw buttons
        def add_button(text, pos, size, active):
            pygame.draw.rect(
                self.engine.screen,
                (0x33,0x33,0x33) if not active else (0xBB,0xBB,0xBB),
                pygame.Rect(
                    pos, 
                    size),
                0)

            text_bitmap = self.engine.font_small.render(
                    text, 
                    True, 
                    (255, 255, 255))
            
            self.engine.screen.blit(
                text_bitmap,
                (
                    pos[0] + size[0]/2 - text_bitmap.get_width()/2, 
                    pos[1] + size[1]/2 - text_bitmap.get_height()/2))

        div = 800 / 6

        add_button(
            "Add Tank",
            (div*1 - 120/2, 130), (120 , 50),
            len([cur for cur in self.cursors if (
                cur.pos == CursorState.ADD_TANK)]) > 0)
        add_button(
            "Remove Tank",
            (div*2 - 120/2, 130), (120 , 50),
            len([cur for cur in self.cursors if (
                cur.pos == CursorState.REMOVE_TANK)]) > 0)
        add_button(
            "Tank Controller",
            (div*3 - 120/2, 130), (120 , 50),
            len([cur for cur in self.cursors if (
                cur.pos == CursorState.SELECT_TANK)]) > 0)
        add_button(
            "Tank Color",
            (div*4 - 120/2, 130), (120 , 50),
            len([cur for cur in self.cursors if (
                cur.pos == CursorState.SELECT_COLOR)]) > 0)
        add_button(
            "Start",
            (div*5 - 120/2, 130), (120 , 50),
            len([cur for cur in self.cursors if (
                cur.pos == CursorState.START)]) > 0)

        pygame.draw.rect(
            self.engine.screen,
            (0,0,0,70),
            pygame.Rect(100, 200, 600, 350),
            0)
        pygame.draw.rect(
            self.engine.screen,
            (255,255,255),
            pygame.Rect(100, 200, 600, 350),
            3)
        
        p_area = self.engine.screen.subsurface(
            pygame.Rect(100, 200, 600, 350))
        div = p_area.get_width() / (len(self.players) + 2)

        pos = div * 2
        pi = 0
        for p in self.players:
            # Draw tank
            rotated_tank = pygame.transform.rotate(
                self.engine.tank_img, -90)
            rotated_tank.fill(p.t.color, special_flags=pygame.BLEND_ADD)
            rotated_canon = pygame.transform.rotate(
                self.engine.canon_img, -90)
            rotated_canon.fill(p.t.c.color, special_flags=pygame.BLEND_ADD)
            
            p_area.blit(
                rotated_tank, 
                (pos - rotated_tank.get_width() /2, 30))
            p_area.blit(
                rotated_canon, 
                (pos - rotated_canon.get_width() /2, 30))

            # Draw color bars
            color_cur = [
                cur for cur in self.cursors if (
                    cur.pos == CursorState.SELECTING_COLOR) and
                    cur.tank_i == pi]

            if len(color_cur) > 0:

                # Canon Color
                canon_color_cur = [
                    cur.color_i for cur in color_cur if (
                        Controller.Mode.CANON in cur.color_t)]

                pygame.draw.rect(
                    p_area,
                    (0xFF,0x33,0x33) if (
                        0 in canon_color_cur
                        ) else (0x55,0x33,0x33),
                    pygame.Rect(
                        pos - 13, 10, 
                        6, 20 * p.t.c.color[0] / 255),
                    0)
                pygame.draw.rect(
                    p_area,
                    (0x33,0xFF,0x33) if (
                        1 in canon_color_cur
                        ) else (0x33,0x55,0x33),
                    pygame.Rect(
                        pos - 3, 10, 
                        6, 20 * p.t.c.color[1] / 255),
                    0)
                pygame.draw.rect(
                    p_area,
                    (0x33,0x33,0xFF) if (
                        2 in canon_color_cur
                        ) else (0x33,0x33,0x55),
                    pygame.Rect(
                        pos + 6, 10, 
                        6, 20 * p.t.c.color[2] / 255),
                    0)

                # Tank Color
                tank_color_cur = [
                    cur.color_i for cur in color_cur if (
                        Controller.Mode.TANK in cur.color_t)]
                pygame.draw.rect(
                    p_area,
                    (0xFF,0x33,0x33) if (
                        0 in tank_color_cur
                        ) else (0x55,0x33,0x33),
                    pygame.Rect(
                        pos - 13, 70, 
                        6, 20 * p.t.color[0] / 255),
                    0)
                pygame.draw.rect(
                    p_area,
                    (0x33,0xFF,0x33) if (
                        1 in tank_color_cur
                        ) else (0x33,0x55,0x33),
                    pygame.Rect(
                        pos - 3, 70, 
                        6, 20 * p.t.color[1] / 255),
                    0)
                pygame.draw.rect(
                    p_area,
                    (0x33,0x33,0xFF) if (
                        2 in tank_color_cur
                        ) else (0x33,0x33,0x55),
                    pygame.Rect(
                        pos + 6, 70, 
                        6, 20 * p.t.color[2] / 255),
                    0)

            # Draw controller selector
            ctrl_cur = [
                cur.controller_i for cur in self.cursors if (
                    cur.pos == CursorState.SELECTING_TANK)]

            posy = 90
            ci = 0
            for c in self.controllers:
                if c.player == p and c.mode is not None:
                    pygame.draw.rect(
                        p_area,
                        (0x33,0x33,0x33) if (
                            ci not in ctrl_cur
                            ) else (0xBB,0xBB,0xBB),
                        pygame.Rect(
                            pos - 13, posy, 
                            26, 20),
                        0)
                else:
                    pygame.draw.rect(
                        p_area,
                        (0x33,0x33,0x33) if (
                            ci not in ctrl_cur
                            ) else (0xBB,0xBB,0xBB),
                        pygame.Rect(
                            pos - 13, posy, 
                            26, 20),
                        1)
                posy += 30
                ci += 1

            pos += div
            pi += 1
        
        # Draw icons
        if len(self.players) > 0:
            ctrl_cur = [
                cur.controller_i for cur in self.cursors if (
                    cur.pos == CursorState.SELECTING_TANK)]
            posx = p_area.get_width() / (len(self.players) + 2)
            posy = 90
            ci = 0
            for c in self.controllers:
                ctrl_icon = c.cur_img.copy()
                ctrl_icon.fill(
                    playerColors[ci%8], special_flags=pygame.BLEND_ADD)
                if ci not in ctrl_cur:
                    ctrl_icon.fill(
                    (0x55,0x55,0x55), special_flags=pygame.BLEND_SUB)
                p_area.blit(
                    ctrl_icon,
                    (posx, posy))

                posy += 30
                ci += 1

        #self.debug()

    def debug(self):

        self.engine.text_print.reset()
        
        self.engine.text_print.tprint(self.engine.screen, "Tanks")
        self.engine.text_print.tprint(self.engine.screen, "")

        self.engine.text_print.tprint(self.engine.screen, f"  Controllers {len(self.controllers)}")
        for c in self.controllers:
            self.engine.text_print.tprint(self.engine.screen, f"  Controller {id(c)}: ")
            if c.player is not None:
                self.engine.text_print.tprint(self.engine.screen, f"    Player {id(c.player)} - {c.mode} {c.player.t.color} - {c.player.t.c.color}")
            else:
                self.engine.text_print.tprint(self.engine.screen, f"    Player None")

        self.engine.text_print.tprint(self.engine.screen, "")

        self.engine.text_print.tprint(self.engine.screen, f"  Cursors {len(self.cursors)}")
        i = 1
        for cur in self.cursors:
            self.engine.text_print.tprint(self.engine.screen, f"  Cursor {i}: {id(cur.controller)} - {cur.pos} - {cur.controller_i} - {cur.tank_i} - {cur.color_i}")
            i += 1

        self.engine.text_print.tprint(self.engine.screen, "")

        self.engine.text_print.tprint(self.engine.screen, f"  Players {len(self.players)}")
        for p in self.players:
            self.engine.text_print.tprint(self.engine.screen, f"    Player {id(p)} - {p.t.color} - {p.t.c.color}")

    def run(self):
        # Check nav actions
        i = 0
        while i < len(self.cursors):
            cur = self.cursors[i]
            if self.flow[cur.pos].act is not None:
                # Run current pos if
                self.flow[cur.pos].act(cur)

            if cur.controller.btns_d[Controller.Buttons.LEFT]:
                if self.flow[cur.pos].left is not None:
                    cur.pos = self.flow[cur.pos].left
            elif cur.controller.btns_d[Controller.Buttons.RIGHT]:
                if self.flow[cur.pos].right is not None:
                    cur.pos = self.flow[cur.pos].right
            elif cur.controller.btns_d[Controller.Buttons.A]:
                if self.flow[cur.pos].a is not None:
                    cur.pos = self.flow[cur.pos].a
            elif cur.controller.btns_d[Controller.Buttons.B]:
                if self.flow[cur.pos].b is not None:
                    cur.pos = self.flow[cur.pos].b
                else:
                    if len(self.cursors) == 1:
                        for c in self.controllers:
                            c.player = None
                            c.mode = None
                        while len(self.players) > 0:
                            del self.players[0]

                    del self.cursors[i]
                    i -= 1
            i += 1

        # Check for new controllers
        for c in self.controllers:
            if c.btns_d[Controller.Buttons.A]:
                find_cur = [
                    cur for cur in self.cursors if (
                        c == cur.controller)]

                if len(find_cur) == 0:
                    self.cursors.append(self.Cursor(c))
                    # Add the first tank
                    if len(self.cursors) == 1 and len(self.players) == 0:
                        p = Player(mstps[0], playerColors[0])
                        self.players.append(p)
                        c.setPlayer(p, Controller.Mode.BOTH)

        self.draw()

        if self.start_game:
            return GameState.GAME
        return GameState.MENU
