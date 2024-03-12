#!/usr/bin/env python3

# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

import pygame
import math
import os

from importlib.resources import files

from .controller import *
from .scenes import *
from .utils import *


class PyTankBattle():

    def __init__(self):
        self.data = Data()
        self.engine = Engine()
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

        PyGameJoystick.cur_img = pygame.image.load(
            files('pytankbattle.assets').joinpath('jcur.png').open())
        PyGameKeyboardMouse.cur_img = pygame.image.load(
            files('pytankbattle.assets').joinpath('kmcur.png').open())

        self.engine.font_huge = pygame.font.Font(
            files('pytankbattle.assets').joinpath('FreeSansBold.ttf').open(), 64)
        self.engine.font_big = pygame.font.Font(
            files('pytankbattle.assets').joinpath('FreeSansBold.ttf').open(), 32)
        self.engine.font_normal = pygame.font.Font(
            files('pytankbattle.assets').joinpath('FreeSansBold.ttf').open(), 24)
        self.engine.font_small = pygame.font.Font(
            files('pytankbattle.assets').joinpath('FreeSansBold.ttf').open(), 16)
        self.engine.font_mini = pygame.font.Font(
            files('pytankbattle.assets').joinpath('FreeSansBold.ttf').open(), 10)

        self.engine.version = get_version()

        self.engine.keyboardmouse = PyGameKeyboardMouse()
        self.data.controllers.append(self.engine.keyboardmouse)

        pcount = pygame.joystick.get_count()

        for i in range(pcount):
            driver = pygame.joystick.Joystick(i)
            driver.init()
            joy = PyGameJoystick(driver)

            self.engine.joysticks[driver.get_instance_id()] = joy 
            self.data.controllers.append(joy)

        self.scenes[GameState.MENU] = MenuScene(self.engine, self.data)
        self.scenes[GameState.GAME] = GameScene(self.engine, self.data)
        self.scenes[GameState.PAUSE] = PauseScene(self.engine, self.data)
        self.scenes[GameState.RESULT] = ResultScene(self.engine, self.data)
        self.scenes[GameState.CREDITS] = CreditsScene(self.engine, self.data)
        self.data.state = GameState.MENU

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
                self.data.state = GameState.QUIT

            if event.type == pygame.JOYBUTTONDOWN:
                joy = self.engine.joysticks[event.instance_id]
                joy.trigger(pygame.JOYBUTTONDOWN, event.button)

            if event.type == pygame.JOYHATMOTION:
                joy = self.engine.joysticks[event.instance_id]
                joy.trigger(pygame.JOYHATMOTION, event.value)

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

        if self.data.state != GameState.QUIT:
            ret = self.scenes[self.data.state].run()

        if ret != self.data.state:
            # Reset scene
            self.scenes[self.data.state].reset()
        
        pygame.display.flip()
        self.engine.clock.tick(30)

        self.data.state = ret
    
    def stop(self):
        pygame.quit()
    
    def run(self):
        self.start_up()

        while self.data.state != GameState.QUIT:
            self.scan_pads()
            self.update_game()

        self.stop()
