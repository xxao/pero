#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# load modules
import math
from .enum import Enum
from .values import *

# define pi
PI = math.pi  # 180
PI2 = math.pi/2  # 90
PI3 = math.pi/3  # 60
PI4 = math.pi/4  # 45
PI6 = math.pi/6  # 30
PI12 = math.pi/12  # 15

# define engineering prefixes
ENG_PREFIXES = {
    "y": -24,
    "z": -21,
    "a": -18,
    "f": -15,
    "p": -12,
    "n": -9,
    "u": -6,
    "m": -3,
    "": 0,
    "k": 3,
    "M": 6,
    "G": 9,
    "T": 12,
    "P": 15,
    "E": 18,
    "Z": 21,
    "Y": 24}

# define rounding
ROUNDING = Enum(
    CEIL = 'ceil',
    FLOOR = 'floor',
    HALFUP = 'halfup')

# define time units
TIME = Enum(
    DAYS = DAYS,
    HOURS = HOURS,
    MINUTES = MINUTES,
    SECONDS = SECONDS,
    MSECONDS = MSECONDS,
    USECONDS = USECONDS,
    NSECONDS = NSECONDS)

# define time conversion factors to seconds
TIME_FACTORS = {
    DAYS: 24*60*60,
    HOURS: 60*60,
    MINUTES: 60,
    SECONDS: 1,
    MSECONDS: 1e-3,
    USECONDS: 1e-6,
    NSECONDS: 1e-9}
