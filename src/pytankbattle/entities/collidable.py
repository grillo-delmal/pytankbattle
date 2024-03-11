# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

class Collidable():
    def __init__(self, px, py, rad):
        self.px = px
        self.py = py
        self.rad = rad

    def check_colision(self, other, fx=None, fy=None):
        if fx is None:
            fx = other.px
        if fy is None:
            fy = other.py
        a = fx - self.px
        b = fy - self.py

        if (a**2 + b**2) < (self.rad + other.rad)**2:
            return True
        return False

