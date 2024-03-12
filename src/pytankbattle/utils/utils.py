# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

import pygame
from importlib.resources import files
import os
import sys

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(files('pytankbattle.assets').joinpath('FreeSansBold.ttf').open(), 16)

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


def get_version():
    version = "0.0.0"
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
        
        with open(os.path.join(datadir, 'VERSION')) as version_file:
            version = version_file.read().strip()
    else:
        from importlib import metadata
        # The application is not frozen
        # Change this bit to match where you store your data files:
        version = metadata.version("pytankbattle")
    return version
