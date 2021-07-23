#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . values import *
from . enum import Enum

# define orientation
ORI_HORIZONTAL = HORIZONTAL
ORI_VERTICAL = VERTICAL

ORIENTATION = Enum(
    HORIZONTAL = ORI_HORIZONTAL,
    VERTICAL = ORI_VERTICAL)

# define generic positions
POS_LEFT = LEFT
POS_RIGHT = RIGHT

POS_TOP = TOP
POS_BOTTOM = BOTTOM

POS_CENTER = CENTER
POS_MIDDLE = MIDDLE

POS_START = START
POS_END = END

POS_INSIDE = INSIDE
POS_OUTSIDE = OUTSIDE

POS_N = N
POS_NW = NW
POS_NE = NE
POS_S = S
POS_SW = SW
POS_SE = SE
POS_W = W
POS_E = E
POS_C = C

POSITION = Enum(
    
    LEFT = POS_LEFT,
    RIGHT = POS_RIGHT,
    
    TOP = POS_TOP,
    BOTTOM = POS_BOTTOM,
    
    CENTER = POS_CENTER,
    MIDDLE = POS_MIDDLE,
    
    START = POS_START,
    END = POS_END,
    
    INSIDE = POS_INSIDE,
    OUTSIDE = POS_OUTSIDE,
    
    N = POS_N,
    NW = POS_NW,
    NE = POS_NE,
    S = POS_S,
    SW = POS_SW,
    SE = POS_SE,
    W = POS_W,
    E = POS_E,
    C = POS_C)

# define specific positions
POSITION_LR = Enum(
    LEFT = POS_LEFT,
    RIGHT = POS_RIGHT)

POSITION_LRC = Enum(
    LEFT = POS_LEFT,
    RIGHT = POS_RIGHT,
    CENTER = POS_CENTER)

POSITION_TB = Enum(
    TOP = POS_TOP,
    BOTTOM = POS_BOTTOM)

POSITION_TBC = Enum(
    TOP = POS_TOP,
    BOTTOM = POS_BOTTOM,
    CENTER = POS_CENTER)

POSITION_LRTB = Enum(
    LEFT = POS_LEFT,
    RIGHT = POS_RIGHT,
    TOP = POS_TOP,
    BOTTOM = POS_BOTTOM)

POSITION_LRTBC = Enum(
    LEFT = POS_LEFT,
    RIGHT = POS_RIGHT,
    TOP = POS_TOP,
    BOTTOM = POS_BOTTOM,
    CENTER = POS_CENTER)

POSITION_IOC = Enum(
    INSIDE = POS_INSIDE,
    OUTSIDE = POS_OUTSIDE,
    CENTER = POS_CENTER)

POSITION_SEM = Enum(
    START = POS_START,
    END = POS_END,
    MIDDLE = POS_MIDDLE)

POSITION_TL = Enum(
    TOP = POS_TOP,
    LEFT = POS_LEFT)

POSITION_TR = Enum(
    TOP = POS_TOP,
    RIGHT = POS_RIGHT)

POSITION_BL = Enum(
    BOTTOM = POS_BOTTOM,
    LEFT = POS_LEFT)

POSITION_BR = Enum(
    BOTTOM = POS_BOTTOM,
    RIGHT = POS_RIGHT)

POSITION_COMPASS = Enum(
    N = POS_N,
    NW = POS_NW,
    NE = POS_NE,
    S = POS_S,
    SW = POS_SW,
    SE = POS_SE,
    W = POS_W,
    E = POS_E,
    C = POS_C)

POSITION_COMPASS_LEFT = Enum(
    NW = POS_NW,
    SW = POS_SW,
    W = POS_W)

POSITION_COMPASS_RIGHT = Enum(
    NE = POS_NE,
    SE = POS_SE,
    E = POS_E)

POSITION_COMPASS_TOP = Enum(
    N = POS_N,
    NW = POS_NW,
    NE = POS_NE)

POSITION_COMPASS_BOTTOM = Enum(
    S = POS_S,
    SW = POS_SW,
    SE = POS_SE)

POSITION_COMPASS_CENTER = Enum(
    N = POS_N,
    S = POS_S,
    C = POS_C)

POSITION_COMPASS_MIDDLE = Enum(
    W = POS_W,
    E = POS_E,
    C = POS_C)
