from .mapstartpos import MapStartPos
from ..utils.consts import *

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

