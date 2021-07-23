#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . enum import Enum

# define keys
KEY_BACK = 8
KEY_TAB = 9
KEY_RETURN = 13

KEY_CTRL = 17
KEY_SHIFT = 16
KEY_ALT = 18

KEY_ESC = 27
KEY_SPACE = 32

KEY_PAGEUP = 33
KEY_PAGEDOWN = 34
KEY_END = 35
KEY_HOME = 36
KEY_LEFT = 37
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40

KEY_DELETE = 46

KEY_F1 = 112
KEY_F2 = 113
KEY_F3 = 114
KEY_F4 = 115
KEY_F5 = 116
KEY_F6 = 117
KEY_F7 = 118
KEY_F8 = 119
KEY_F9 = 120
KEY_F10 = 121
KEY_F11 = 122
KEY_F12 = 123

KEY = Enum(
    
    BACK = KEY_BACK,
    TAB = KEY_TAB,
    RETURN = KEY_RETURN,
    
    CTRL = KEY_CTRL,
    SHIFT = KEY_SHIFT,
    ALT = KEY_ALT,
    
    ESC = KEY_ESC,
    SPACE = KEY_SPACE,
    
    PAGEUP = KEY_PAGEUP,
    PAGEDOWN = KEY_PAGEDOWN,
    END = KEY_END,
    HOME = KEY_HOME,
    LEFT = KEY_LEFT,
    UP = KEY_UP,
    RIGHT = KEY_RIGHT,
    DOWN = KEY_DOWN,
    
    DELETE = KEY_DELETE,
    
    F1 = KEY_F1,
    F2 = KEY_F2,
    F3 = KEY_F3,
    F4 = KEY_F4,
    F5 = KEY_F5,
    F6 = KEY_F6,
    F7 = KEY_F7,
    F8 = KEY_F8,
    F9 = KEY_F9,
    F10 = KEY_F10,
    F11 = KEY_F11,
    F12 = KEY_F12)

MODIFIER_KEYS = {
    KEY_CTRL,
    KEY_SHIFT,
    KEY_ALT}
