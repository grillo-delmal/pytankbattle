# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

class Engine():
    def __init__(self):
        self.screen = None
        self.clock = None
        self.keyboardmouse = None
        self.joysticks = {}
        self.text_print = None

        self.tank_img = None
        self.canon_img = None

        self.font_huge = None
        self.font_big = None
        self.font_normal = None
        self.font_small = None
        self.font_mini = None
