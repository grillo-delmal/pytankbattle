#!/usr/bin/env python3

# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

import pygame
import math
import os

from enum import Enum, auto
from importlib.resources import files

from .controller import *
from .map import *
from .entities import *
from .scenes import *
from .utils import *


class PyTankBattle():
    class State(Enum):
        PAUSE   = auto()
        MENU    = auto()
        GAME    = auto()
        CREDITS = auto()
        QUIT    = auto()

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

    playerColors = [
        (0x33, 0xBB, 0x33),
        (0xBB, 0x33, 0x33),
        (0x33, 0x33, 0xBB),
        (0x33, 0xBB, 0xBB),
        (0xBB, 0xBB, 0x33),
        (0xBB, 0x33, 0xBB),
        (0x33, 0x33, 0x33),
        (0xBB, 0xBB, 0xBB),
    ]

    def __init__(self):
        self.players = []
        self.bullets = []
        self.controllers = []

        self.tank_img = None
        self.canon_img = None

        #ENGINE GLOBALS
        self.screen = None
        self.clock = None
        self.keyboardmouse = None
        self.joysticks = {}
        self.text_print = None

        # FIXME: Start on Menu
        self.state = self.State.GAME

    def start_up(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("PyTankBattle")
        self.clock = pygame.time.Clock()
        self.text_print = TextPrint()

        self.tank_img = pygame.image.load(
            files('pytankbattle.assets').joinpath('tank.png').open())
        self.canon_img = pygame.image.load(
            files('pytankbattle.assets').joinpath('canon.png').open())

        self.keyboardmouse = PyGameKeyboardMouse()
        self.controllers.append(self.keyboardmouse)

        pcount = pygame.joystick.get_count()

        for i in range(pcount):
            driver = pygame.joystick.Joystick(i)
            driver.init()
            joy = PyGameJoystick(driver)

            self.joysticks[driver.get_instance_id()] = joy 
            self.controllers.append(joy)

        # FIXME: Prepare for Menu, not Game
        # FIXME: Players are not initialized here
        for c in self.controllers:
            pi = len(self.players)
            p = Player(self.mstps[pi], self.playerColors[pi])
            c.setPlayer(p, Controller.Mode.BOTH) 
            self.players.append(p)

        ## Fill rest of players
        #for pi in range(len(self.players), 8):
        #    p = Player(self.mstps[pi], self.playerColors[pi])
        #    self.players.append(p)

        for p in self.players:
            p.reset()

    def scan_pads(self):
        # Query keyboard for this frame
        self.keyboardmouse.reset()
        self.keyboardmouse.update()

        # Query joysticks for this frame
        for i in self.joysticks:
            joy = joysticks[i]
            joy.reset()
            joy.update()
        
        # Poll for events
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                self.state = self.State.QUIT

            if event.type == pygame.JOYBUTTONDOWN:
                joy = self.joysticks[event.instance_id]
                joy.trigger(event.button)

            if event.type == pygame.KEYDOWN:
                self.keyboardmouse.trigger(pygame.KEYDOWN, event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.keyboardmouse.trigger(pygame.MOUSEBUTTONDOWN, event.button)

            # TODO: Handle adding players on menu
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                if joy.get_instance_id() in self.joysticks:
                    self.joysticks[joy.get_instance_id()].driver = joy

            # TODO: Handle removing players on menu
            if event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in self.joysticks:
                    self.joysticks[event.instance_id].driver = None
        
    def update_game(self):
        ret = self.state

        if self.state == self.State.PAUSE:
            ret = pause(self)
        elif self.state == self.State.MENU:
            ret = menu(self)
        elif self.state == self.State.GAME:
            ret = game(self)
        elif self.state == self.State.CREDITS:
            ret = credits(self)
        else:
            ret = self.State.QUIT
        
        pygame.display.flip()
        self.clock.tick(30)

        self.state = ret
    
    def stop(self):
        pygame.quit()
    
    def run(self):
        self.start_up()

        if len(self.players) <= 0:
            print("not enough players")
            self.state = self.State.QUIT

        while self.state != self.State.QUIT:
            self.scan_pads()
            self.update_game()

        self.stop()

def main():
    # FIXME: START AT MENU

    game = PyTankBattle()
    game.run()


if __name__ == "__main__":
    main()