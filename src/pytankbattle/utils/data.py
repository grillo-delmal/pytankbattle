# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

from enum import Enum, auto

class GameState(Enum):
    PAUSE   = auto()
    MENU    = auto()
    GAME    = auto()
    RESULT  = auto()
    CREDITS = auto()
    QUIT    = auto()


class Data():

    def __init__(self):
        self.players = []
        self.bullets = []
        self.controllers = []

        self.state = None

