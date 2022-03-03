#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . enum import Enum

# define keys
KEY_BACK = 8
KEY_TAB = 9
KEY_RETURN = 13

KEY_SHIFT = 16
KEY_CTRL = 17
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

KEY_0 = 48
KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_4 = 52
KEY_5 = 53
KEY_6 = 54
KEY_7 = 55
KEY_8 = 56
KEY_9 = 57

KEY_A = 65
KEY_B = 66
KEY_C = 67
KEY_D = 68
KEY_E = 69
KEY_F = 70
KEY_G = 71
KEY_H = 72
KEY_I = 73
KEY_J = 74
KEY_K = 75
KEY_L = 76
KEY_M = 77
KEY_N = 78
KEY_O = 79
KEY_P = 80
KEY_Q = 81
KEY_R = 82
KEY_S = 83
KEY_T = 84
KEY_U = 85
KEY_V = 86
KEY_W = 87
KEY_X = 88
KEY_Y = 89
KEY_Z = 90

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
    
    SHIFT = KEY_SHIFT,
    CTRL = KEY_CTRL,
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
    
    KEY_0 = KEY_0,
    KEY_1 = KEY_1,
    KEY_2 = KEY_2,
    KEY_3 = KEY_3,
    KEY_4 = KEY_4,
    KEY_5 = KEY_5,
    KEY_6 = KEY_6,
    KEY_7 = KEY_7,
    KEY_8 = KEY_8,
    KEY_9 = KEY_9,
    
    KEY_A = KEY_A,
    KEY_B = KEY_B,
    KEY_C = KEY_C,
    KEY_D = KEY_D,
    KEY_E = KEY_E,
    KEY_F = KEY_F,
    KEY_G = KEY_G,
    KEY_H = KEY_H,
    KEY_I = KEY_I,
    KEY_J = KEY_J,
    KEY_K = KEY_K,
    KEY_L = KEY_L,
    KEY_M = KEY_M,
    KEY_N = KEY_N,
    KEY_O = KEY_O,
    KEY_P = KEY_P,
    KEY_Q = KEY_Q,
    KEY_R = KEY_R,
    KEY_S = KEY_S,
    KEY_T = KEY_T,
    KEY_U = KEY_U,
    KEY_V = KEY_V,
    KEY_W = KEY_W,
    KEY_X = KEY_X,
    KEY_Y = KEY_Y,
    KEY_Z = KEY_Z,
    
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
