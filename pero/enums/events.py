#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . enum import Enum

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
EVT_TOUCH = 'evt_touch'
EVT_TOUCH_START = 'evt_touch_start'
EVT_TOUCH_END = 'evt_touch_end'
EVT_TOUCH_MOVE = 'evt_touch_move'
EVT_TOUCH_CANCEL = 'evt_touch_cancel'

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
    RIGHT_DCLICK = EVT_RIGHT_DCLICK,
    TOUCH = EVT_TOUCH,
    TOUCH_START = EVT_TOUCH_START,
    TOUCH_END = EVT_TOUCH_END,
    TOUCH_MOVE = EVT_TOUCH_MOVE,
    TOUCH_CANCEL = EVT_TOUCH_CANCEL)

# define touch states
TOUCH_PRESSED = 'pressed'
TOUCH_RELEASED = 'released'
TOUCH_MOVED = 'moved'
TOUCH_STATIC = 'static'

TOUCH = Enum(
    PRESSED = TOUCH_PRESSED,
    RELEASED = TOUCH_RELEASED,
    MOVED = TOUCH_MOVED,
    STATIC = TOUCH_STATIC)
