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
ROUNDING_CEIL = CEIL
ROUNDING_FLOOR = FLOOR
ROUNDING_HALFUP = HALFUP

ROUNDING = Enum(
    CEIL = ROUNDING_CEIL,
    FLOOR = ROUNDING_FLOOR,
    HALFUP = ROUNDING_HALFUP)

# define time units
TIME_DAYS = DAYS,
TIME_HOURS = HOURS,
TIME_MINUTES = MINUTES,
TIME_SECONDS = SECONDS,
TIME_MSECONDS = MSECONDS,
TIME_USECONDS = USECONDS,
TIME_NSECONDS = NSECONDS

TIME = Enum(
    DAYS = TIME_DAYS,
    HOURS = TIME_HOURS,
    MINUTES = TIME_MINUTES,
    SECONDS = TIME_SECONDS,
    MSECONDS = TIME_MSECONDS,
    USECONDS = TIME_USECONDS,
    NSECONDS = TIME_NSECONDS)

# define time conversion factors to seconds
TIME_FACTORS = {
    TIME_DAYS: 24*60*60,
    TIME_HOURS: 60*60,
    TIME_MINUTES: 60,
    TIME_SECONDS: 1,
    TIME_MSECONDS: 1e-3,
    TIME_USECONDS: 1e-6,
    TIME_NSECONDS: 1e-9}
