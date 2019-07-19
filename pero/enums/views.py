#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# load modules
from .enum import Enum
from .values import *

# define keys
KEY = Enum(
    
    BACK = 8,
    TAB = 9,
    RETURN = 13,
    
    CTRL = 17,
    SHIFT = 16,
    ALT = 18,
    
    ESC = 27,
    SPACE = 32,
    
    PAGEUP = 33,
    PAGEDOWN = 34,
    END = 35,
    HOME = 36,
    LEFT = 37,
    UP = 38,
    RIGHT = 39,
    DOWN = 40,
    
    DELETE = 46,
    
    F1 = 112,
    F2 = 113,
    F3 = 114,
    F4 = 115,
    F5 = 116,
    F6 = 117,
    F7 = 118,
    F8 = 119,
    F9 = 120,
    F10 = 121,
    F11 = 122,
    F12 = 123)

MODIFIER_KEYS = {
    KEY.CTRL,
    KEY.SHIFT,
    KEY.ALT}

# define events
EVENT = Enum(
    PROPERTY_CHANGED = EVT_PROPERTY_CHANGED,
    PEN_CHANGED = EVT_PEN_CHANGED,
    BRUSH_CHANGED = EVT_BRUSH_CHANGED,
    TEXT_CHANGED = EVT_TEXT_CHANGED,
    VIEW = EVT_VIEW,
    SIZE = EVT_SIZE,
    ZOOM = EVT_ZOOM,
    KEY = EVT_KEY,
    KEY_DOWN = EVT_KEY_DOWN,
    KEY_UP = EVT_KEY_UP,
    MOUSE = EVT_MOUSE,
    MOUSE_MOTION = EVT_MOUSE_MOTION,
    MOUSE_SCROLL = EVT_MOUSE_SCROLL,
    MOUSE_ENTER = EVT_MOUSE_ENTER,
    MOUSE_LEAVE = EVT_MOUSE_LEAVE,
    LEFT_DOWN = EVT_LEFT_DOWN,
    LEFT_UP = EVT_LEFT_UP,
    LEFT_DCLICK = EVT_LEFT_DCLICK,
    MIDDLE_DOWN = EVT_MIDDLE_DOWN,
    MIDDLE_UP = EVT_MIDDLE_UP,
    MIDDLE_DCLICK = EVT_MIDDLE_DCLICK,
    RIGHT_DOWN = EVT_RIGHT_DOWN,
    RIGHT_UP = EVT_RIGHT_UP,
    RIGHT_DCLICK = EVT_RIGHT_DCLICK)

# define cursors
CURSOR = Enum(
    BLANK = 'blank',
    ARROW = 'arrow',
    HAND = 'hand',
    SIZEWE = 'size_we',
    SIZENS = 'size_ns')
