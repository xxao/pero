#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# load modules
from .enum import Enum
from .values import *


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
    KEY.CTRL,
    KEY.SHIFT,
    KEY.ALT}

# define events
EVT_PROPERTY_CHANGED = 'evt_prop_changed'
EVT_PEN_CHANGED = 'evt_pen_changed'
EVT_BRUSH_CHANGED = 'evt_brush_changed'
EVT_TEXT_CHANGED = 'evt_text_changed'
EVT_VIEW = 'evt_view'
EVT_SIZE = 'evt_size'
EVT_ZOOM = 'evt_zoom'
EVT_KEY = 'evt_key'
EVT_KEY_DOWN = 'evt_key_down'
EVT_KEY_UP = 'evt_key_up'
EVT_MOUSE = 'evt_mouse'
EVT_MOUSE_MOTION = 'evt_mouse_motion'
EVT_MOUSE_SCROLL = 'evt_mouse_scroll'
EVT_MOUSE_ENTER = 'evt_mouse_enter'
EVT_MOUSE_LEAVE = 'evt_mouse_leave'
EVT_LEFT_DOWN = 'evt_left_down'
EVT_LEFT_UP = 'evt_left_up'
EVT_LEFT_DCLICK = 'evt_left_dclick'
EVT_MIDDLE_DOWN = 'evt_middle_down'
EVT_MIDDLE_UP = 'evt_middle_up'
EVT_MIDDLE_DCLICK = 'evt_middle_dclick'
EVT_RIGHT_DOWN = 'evt_right_down'
EVT_RIGHT_UP = 'evt_right_up'
EVT_RIGHT_DCLICK = 'evt_right_dclick'

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
CURSOR_BLANK = 'blank'
CURSOR_ARROW = 'arrow'
CURSOR_HAND = 'hand'
CURSOR_SIZEWE = 'size_we'
CURSOR_SIZENS = 'size_ns'

CURSOR = Enum(
    BLANK = CURSOR_BLANK,
    ARROW = CURSOR_ARROW,
    HAND = CURSOR_HAND,
    SIZEWE = CURSOR_SIZEWE,
    SIZENS = CURSOR_SIZENS)
