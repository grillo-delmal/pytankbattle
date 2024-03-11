# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

import pygame

from .scene import Scene
from ..controller import Controller
from ..utils.data import GameState

class PauseScene(Scene):
    def __init__(self, engine, data):
        super().__init__()
        self.engine = engine
        self.data = data

    def run(self):
        self.engine.screen.fill("black")
        title_bmp = self.engine.font_big.render(
            "Pause", 
            True, 
            (255, 255, 255))

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
        text_bmp = self.engine.font_normal.render(
            "B / Backspace to quit", 
            True, 
            (255, 255, 255))
        self.engine.screen.blit(
            text_bmp,
            (400 - text_bmp.get_width()/2, 380))


        for CD in self.data.controllers:
            p = CD.player
            if p is None or CD.mode is None:
                continue

            # Return to game control
            if CD.btns_d[Controller.Buttons.A]:
                return GameState.GAME

            # Quit game control
            if CD.btns_d[Controller.Buttons.B]:
                return GameState.CREDITS

        return GameState.PAUSE

