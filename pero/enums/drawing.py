#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# load modules
import sys
from .enum import Enum
from .values import *

# define line splitting character
LINE_SPLITTER = "\n"

# define default fonts
FONT_FACE_SERIF = "Times New Roman"
FONT_FACE_SANS = "Arial"
FONT_FACE_MONO = "Courier New"

if sys.platform == 'darwin':
    FONT_FACE_SERIF = "Times"
    FONT_FACE_SANS = "Helvetica"
    FONT_FACE_MONO = "Courier"

# define font families
FONT_FAMILY = Enum(
    SERIF = SERIF,
    SANS = SANS,
    MONO = MONO)

# define font families default names
FONT_FAMILY_NAMES = {
    FONT_FAMILY.SERIF: (FONT_FACE_SERIF, 'times', 'Times', 'Times New Roman'),
    FONT_FAMILY.SANS: (FONT_FACE_SANS, 'arial', 'Arial', 'Helvetica'),
    FONT_FAMILY.MONO: (FONT_FACE_MONO, 'courier', 'Courier', 'Courier New')}

# define font styles
FONT_STYLE = Enum(
    NORMAL = NORMAL,
    ITALIC = ITALIC)

# define font weight
FONT_WEIGHT = Enum(
    NORMAL = NORMAL,
    LIGHT = LIGHT,
    BOLD = BOLD,
    BLACK = BLACK,
    HEAVY = HEAVY,
    SEMIBOLD = SEMIBOLD,
    MEDIUM = MEDIUM,
    ULTRALIGHT = ULTRALIGHT,
    THIN = THIN)

# define font weight light values
FONT_WEIGHT_LIGHT = {
    LIGHT,
    ULTRALIGHT,
    THIN}

# define font weight bold values
FONT_WEIGHT_BOLD = {
    BOLD,
    BLACK,
    HEAVY,
    SEMIBOLD}

# define text align
TEXT_ALIGN = Enum(
    LEFT = LEFT,
    CENTER = CENTER,
    RIGHT = RIGHT)

# define text baseline
TEXT_BASELINE = Enum(
    TOP = TOP,
    MIDDLE = MIDDLE,
    BOTTOM = BOTTOM)

# define polar text rotation
TEXT_ROTATION = Enum(
    NONE = NONE,
    FOLLOW = FOLLOW,
    NATURAL = NATURAL,
    FACEOUT = FACEOUT,
    FACEIN = FACEIN)

# define angle units
ANGLE = Enum(
    DEG = DEG,
    RAD = RAD)

# define line styles
LINE_STYLE = Enum(
    CUSTOM = CUSTOM,
    SOLID = SOLID,
    DOTTED = DOTTED,
    DASHED = DASHED,
    DASHDOTTED = DASHDOTTED)

# define line caps
LINE_CAP = Enum(
    BUTT = BUTT,
    SQUARE = SQUARE,
    ROUND = ROUND)

LINE_JOIN = Enum(
    BEVEL = BEVEL,
    MITER = MITER,
    ROUND = ROUND)

# define line step
LINE_STEP = Enum(
    NONE = NONE,
    BEFORE = BEFORE,
    MIDDLE = MIDDLE,
    AFTER = AFTER)

# define line dash values
DASH_VALUES = Enum(
    DOTTED = (1, 5),
    DASHED = (5, 5),
    DASHDOTTED = (5, 5, 1, 5))

# define fill style
FILL_STYLE = Enum(
    SOLID = SOLID,
    TRANS = TRANS)

# define fill rule
FILL_RULE = Enum(
    EVENODD = EVENODD,
    WINDING = WINDING)

# define orientation
ORIENTATION = Enum(
    HORIZONTAL = HORIZONTAL,
    VERTICAL = VERTICAL)

# define generic positions
POSITION = Enum(
    
    LEFT = LEFT,
    RIGHT = RIGHT,
    
    TOP = TOP,
    BOTTOM = BOTTOM,
    
    CENTER = CENTER,
    MIDDLE = MIDDLE,
    
    START = START,
    END = END,
    
    INSIDE = INSIDE,
    OUTSIDE = OUTSIDE,
    
    N = N,
    NW = NW,
    NE = NE,
    S = S,
    SW = SW,
    SE = SE,
    W = W,
    E = E,
    C = C)

# define specific positions
POSITION_LR = Enum(
    LEFT = LEFT,
    RIGHT = RIGHT)

POSITION_LRC = Enum(
    LEFT = LEFT,
    RIGHT = RIGHT,
    CENTER = CENTER)

POSITION_TB = Enum(
    TOP = TOP,
    BOTTOM = BOTTOM)

POSITION_TBC = Enum(
    TOP = TOP,
    BOTTOM = BOTTOM,
    CENTER = CENTER)

POSITION_LRTB = Enum(
    LEFT = LEFT,
    RIGHT = RIGHT,
    TOP = TOP,
    BOTTOM = BOTTOM)

POSITION_LRTBC = Enum(
    LEFT = LEFT,
    RIGHT = RIGHT,
    TOP = TOP,
    BOTTOM = BOTTOM,
    CENTER = CENTER)

POSITION_IOC = Enum(
    INSIDE = INSIDE,
    OUTSIDE = OUTSIDE,
    CENTER = CENTER)

POSITION_SEM = Enum(
    START = START,
    END = END,
    MIDDLE = MIDDLE)

POSITION_TL = Enum(
    TOP = TOP,
    LEFT = LEFT)

POSITION_TR = Enum(
    TOP = TOP,
    RIGHT = RIGHT)

POSITION_BL = Enum(
    BOTTOM = BOTTOM,
    LEFT = LEFT)

POSITION_BR = Enum(
    BOTTOM = BOTTOM,
    RIGHT = RIGHT)

POSITION_COMPASS = Enum(
    N = N,
    NW = NW,
    NE = NE,
    S = S,
    SW = SW,
    SE = SE,
    W = W,
    E = E,
    C = C)

# define path commands
PATH = Enum(
    CLOSE = 'Z',
    MOVE = 'M',
    LINE = 'L',
    CURVE= 'C')

# define available markers
MARKER = Enum(
    ASTERISK = '*',
    CIRCLE = 'o',
    CROSS = 'x',
    PLUS = '+',
    TRIANGLE = 't',
    SQUARE = 's',
    DIAMOND = 'd',
    PENTAGON = 'p',
    HEXAGON= 'h')

# define available arrows
ARROW = Enum(
    ARC = 'c',
    BOW = ')',
    CONNECT_LINE = 'z',
    CONNECT_CURVE = 's',
    CURVE = '~',
    LINE = '-',
    RAY = '/')

# define available heads
HEAD = Enum(
    CIRCLE = 'o',
    LINE= '|',
    NORMAL = '|>',
    NORMAL_B = '<|',
    OPEN = '>',
    OPEN_B = '<',
    VEE = '>>',
    VEE_B = '<<')
