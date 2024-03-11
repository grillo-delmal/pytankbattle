# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

from ..utils.mapstartpos import MapStartPos
from ..utils.consts import WIDTH, HEIGHT
from ..entities.collidable import Collidable
import math

mstps = [ 
    MapStartPos(        50,          50,    math.pi/4),
    MapStartPos(WIDTH - 50,          50,  3*math.pi/4),
    MapStartPos(        50, HEIGHT - 50,   -math.pi/4),
    MapStartPos(WIDTH - 50, HEIGHT - 50, -3*math.pi/4),
    MapStartPos(WIDTH /  2,          50,    math.pi/2),
    MapStartPos(WIDTH - 50, HEIGHT /  2,    math.pi),
    MapStartPos(WIDTH /  2, HEIGHT - 50,   -math.pi/2),
    MapStartPos(        50, HEIGHT /  2,     0),
    ]

def check_map_collision(other:Collidable, fx=None, fy=None):
    if fx is None:
        fx = other.px
    if fy is None:
        fy = other.py

    if not (fx > other.rad and fx < WIDTH - other.rad ):
        return True
    if not (fy > other.rad and fy < HEIGHT - other.rad ):
        return True

    return False
