#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from . values import *
from . enum import Enum

# define pi
PI2X = math.pi*2  # 360
PI = math.pi  # 180
PI2 = math.pi/2  # 90
PI3 = math.pi/3  # 60
PI4 = math.pi/4  # 45
PI6 = math.pi/6  # 30
PI12 = math.pi/12  # 15

# define angle units
ANGLE_DEG = DEG
ANGLE_RAD = RAD

ANGLE = Enum(
    DEG = ANGLE_DEG,
    RAD = ANGLE_RAD)

# define rounding
ROUND_CEIL = CEIL
ROUND_FLOOR = FLOOR
ROUND_HALFUP = HALFUP

ROUNDING = Enum(
    CEIL = ROUND_CEIL,
    FLOOR = ROUND_FLOOR,
    HALFUP = ROUND_HALFUP)
