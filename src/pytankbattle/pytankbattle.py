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

    class Data():
        class State(Enum):
            PAUSE   = auto()
            MENU    = auto()
            GAME    = auto()
            CREDITS = auto()
            QUIT    = auto()

        def __init__(self):
            self.players = []
            self.bullets = []
            self.controllers = []

            self.state = None

    class Engine():
        def __init__(self):
            self.screen = None
            self.clock = None
            self.keyboardmouse = None
            self.joysticks = {}
            self.text_print = None

            self.tank_img = None
            self.canon_img = None

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
        self.data = self.Data()
        self.engine = self.Engine()
        self.scenes = {}

    def start_up(self):
        pygame.init()
        self.engine.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("PyTankBattle")
        self.engine.clock = pygame.time.Clock()
        self.engine.text_print = TextPrint()

        self.engine.tank_img = pygame.image.load(
            files('pytankbattle.assets').joinpath('tank.png').open())
        self.engine.canon_img = pygame.image.load(
            files('pytankbattle.assets').joinpath('canon.png').open())

        self.engine.keyboardmouse = PyGameKeyboardMouse()
        self.data.controllers.append(self.engine.keyboardmouse)

        pcount = pygame.joystick.get_count()

        for i in range(pcount):
            driver = pygame.joystick.Joystick(i)
            driver.init()
            joy = PyGameJoystick(driver)

            self.engine.joysticks[driver.get_instance_id()] = joy 
            self.data.controllers.append(joy)

        # FIXME: Players are not initialized here
        for c in self.data.controllers:
            pi = len(self.data.players)
            p = Player(self.mstps[pi], self.playerColors[pi])
            c.setPlayer(p, Controller.Mode.BOTH) 
            self.data.players.append(p)

        ## Fill rest of players
        #for pi in range(len(self.data.players), 8):
        #    p = Player(self.mstps[pi], self.playerColors[pi])
        #    self.data.players.append(p)

        for p in self.data.players:
            p.reset()

        # FIXME: Prepare Menu, not Game
        self.scenes[self.Data.State.GAME] = GameScene(self.data, self.engine)
        self.data.state = self.Data.State.GAME

    def scan_pads(self):
        # Query keyboard for this frame
        self.engine.keyboardmouse.reset()
        self.engine.keyboardmouse.update()

        # Query joysticks for this frame
        for i in self.engine.joysticks:
            joy = self.engine.joysticks[i]
            joy.reset()
            joy.update()
        
        # Poll for events
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                self.data.state = self.Data.State.QUIT

            if event.type == pygame.JOYBUTTONDOWN:
                joy = self.engine.joysticks[event.instance_id]
                joy.trigger(event.button)

            if event.type == pygame.KEYDOWN:
                self.engine.keyboardmouse.trigger(pygame.KEYDOWN, event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.engine.keyboardmouse.trigger(pygame.MOUSEBUTTONDOWN, event.button)

            # TODO: Handle adding players on menu
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                if joy.get_instance_id() in self.engine.joysticks:
                    self.engine.joysticks[joy.get_instance_id()].driver = joy

            # TODO: Handle removing players on menu
            if event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in self.engine.joysticks:
                    self.engine.joysticks[event.instance_id].driver = None
        
    def update_game(self):
        ret = self.data.state

        if self.data.state != self.Data.State.QUIT:
            ret = self.scenes[self.data.state].run()
        
        pygame.display.flip()
        self.engine.clock.tick(30)

        self.data.state = ret
    
    def stop(self):
        pygame.quit()
    
    def run(self):
        self.start_up()

        if len(self.data.players) <= 0:
            print("not enough players")
            self.data.state = self.Data.State.QUIT

        while self.data.state != self.Data.State.QUIT:
            self.scan_pads()
            self.update_game()

        self.stop()
