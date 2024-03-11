from enum import Enum, auto

class GameState(Enum):
    PAUSE   = auto()
    MENU    = auto()
    GAME    = auto()
    RESULT  = auto()
    CREDITS = auto()
    QUIT    = auto()

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

PI = 3.14159265

BULLET_SPEED        = 4
BULLET_RADIUS       = 3.5

TANK_RADIUS         = 16

TANK_MAX_SPEED      = 3
CANON_RELOAD_TIME   = 120
CANON_INMUNE_TIME   = 240

MAX_BULLETS         = 100

HEIGHT              = 300
WIDTH               = 500

SCREEN_MOVE_X       = 70 + 150
SCREEN_MOVE_Y       = 60 + 60
