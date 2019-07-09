#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# load modules
from .enum import Enum

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
    
    PROPERTY_CHANGED = 'evt_prop',
    
    PEN_CHANGED = 'evt_pen',
    BRUSH_CHANGED = 'evt_brush',
    TEXT_CHANGED = 'evt_text',
    
    SIZE = 'evt_size',
    ZOOM = 'evt_zoom',
    
    KEY = 'evt_key',
    KEY_DOWN = 'evt_key_down',
    KEY_UP = 'evt_key_up',
    
    MOUSE = 'evt_mouse',
    MOUSE_MOTION = 'evt_motion',
    MOUSE_SCROLL = 'evt_scroll',
    
    MOUSE_ENTER ='evt_enter',
    MOUSE_LEAVE = 'evt_leave',
    
    LEFT_DOWN = 'evt_left_down',
    LEFT_UP = 'evt_left_up',
    LEFT_DCLICK = 'evt_left_dclick',
    
    MIDDLE_DOWN = 'evt_middle_down',
    MIDDLE_UP = 'evt_middle_up',
    MIDDLE_DCLICK = 'evt_middle_dclick',
    
    RIGHT_DOWN = 'evt_right_down',
    RIGHT_UP = 'evt_right_up',
    RIGHT_DCLICK = 'evt_right_dclick')

# define cursors
CURSOR = Enum(
    BLANK = 'blank',
    ARROW = 'arrow',
    HAND = 'hand',
    SIZEWE = 'size_we',
    SIZENS = 'size_ns')
