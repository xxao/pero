#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . loader import Qt, QFont
from ... enums import *


QT_LINE_CAP = {
    LINE_CAP_BUTT: Qt.PenCapStyle.FlatCap,
    LINE_CAP_SQUARE: Qt.PenCapStyle.SquareCap,
    LINE_CAP_ROUND: Qt.PenCapStyle.RoundCap}

QT_LINE_JOIN = {
    LINE_JOIN_BEVEL: Qt.PenJoinStyle.BevelJoin,
    LINE_JOIN_MITER: Qt.PenJoinStyle.MiterJoin,
    LINE_JOIN_ROUND: Qt.PenJoinStyle.RoundJoin}

QT_LINE_STYLE = {
    LINE_STYLE_CUSTOM: Qt.PenStyle.CustomDashLine,
    LINE_STYLE_SOLID: Qt.PenStyle.SolidLine,
    LINE_STYLE_DOTTED: DASH_VALUES_DOTTED,
    LINE_STYLE_DASHED: DASH_VALUES_DASHED,
    LINE_STYLE_DASHDOTTED: DASH_VALUES_DASHDOTTED}

QT_FILL_STYLE = {
    FILL_STYLE_TRANS: Qt.BrushStyle.NoBrush,
    FILL_STYLE_SOLID: Qt.BrushStyle.SolidPattern}

QT_FILL_RULE = {
    FILL_RULE_EVENODD: Qt.FillRule.OddEvenFill,
    FILL_RULE_WINDING: Qt.FillRule.WindingFill}

QT_FONT_FAMILY = {
    FONT_FAMILY_SERIF: FONT_FACE_SERIF,
    FONT_FAMILY_SANS: FONT_FACE_SANS,
    FONT_FAMILY_MONO: FONT_FACE_MONO}

QT_FONT_STYLE = {
    FONT_STYLE_NORMAL: QFont.Style.StyleNormal,
    FONT_STYLE_ITALIC: QFont.Style.StyleItalic}

QT_FONT_WEIGHT = {
    FONT_WEIGHT_NORMAL: QFont.Weight.Normal,
    FONT_WEIGHT_LIGHT: QFont.Weight.Light,
    FONT_WEIGHT_BOLD: QFont.Weight.Bold,
    FONT_WEIGHT_BLACK: QFont.Weight.Black,
    FONT_WEIGHT_HEAVY: QFont.Weight.ExtraBold,
    FONT_WEIGHT_SEMIBOLD: QFont.Weight.DemiBold,
    FONT_WEIGHT_MEDIUM: QFont.Weight.Medium,
    FONT_WEIGHT_ULTRALIGHT: QFont.Weight.ExtraLight,
    FONT_WEIGHT_THIN: QFont.Weight.Thin}

QT_CURSORS = {
    CURSOR_BLANK: Qt.CursorShape.BlankCursor,
    CURSOR_ARROW: Qt.CursorShape.ArrowCursor,
    CURSOR_HAND: Qt.CursorShape.OpenHandCursor,
    CURSOR_SIZEWE: Qt.CursorShape.SizeHorCursor,
    CURSOR_SIZENS: Qt.CursorShape.SizeVerCursor}

QT_KEYS = {
    Qt.Key.Key_Backspace: KEY_BACK,
    Qt.Key.Key_Tab: KEY_TAB,
    Qt.Key.Key_Return: KEY_RETURN,
    
    Qt.Key.Key_Shift: KEY_SHIFT,
    Qt.Key.Key_Control: KEY_CTRL,
    Qt.Key.Key_Alt: KEY_ALT,
    
    Qt.Key.Key_Escape: KEY_ESC,
    Qt.Key.Key_Space: KEY_SPACE,
    
    Qt.Key.Key_PageUp: KEY_PAGEUP,
    Qt.Key.Key_PageDown: KEY_PAGEDOWN,
    Qt.Key.Key_End: KEY_END,
    Qt.Key.Key_Home: KEY_HOME,
    Qt.Key.Key_Left: KEY_LEFT,
    Qt.Key.Key_Up: KEY_UP,
    Qt.Key.Key_Right: KEY_RIGHT,
    Qt.Key.Key_Down: KEY_DOWN,
    
    Qt.Key.Key_Delete: KEY_DELETE,
    
    Qt.Key.Key_0: KEY_0,
    Qt.Key.Key_1: KEY_1,
    Qt.Key.Key_2: KEY_2,
    Qt.Key.Key_3: KEY_3,
    Qt.Key.Key_4: KEY_4,
    Qt.Key.Key_5: KEY_5,
    Qt.Key.Key_6: KEY_6,
    Qt.Key.Key_7: KEY_7,
    Qt.Key.Key_8: KEY_8,
    Qt.Key.Key_9: KEY_9,
    
    Qt.Key.Key_A: KEY_A,
    Qt.Key.Key_B: KEY_B,
    Qt.Key.Key_C: KEY_C,
    Qt.Key.Key_D: KEY_D,
    Qt.Key.Key_E: KEY_E,
    Qt.Key.Key_F: KEY_F,
    Qt.Key.Key_G: KEY_G,
    Qt.Key.Key_H: KEY_H,
    Qt.Key.Key_I: KEY_I,
    Qt.Key.Key_J: KEY_J,
    Qt.Key.Key_K: KEY_K,
    Qt.Key.Key_L: KEY_L,
    Qt.Key.Key_M: KEY_M,
    Qt.Key.Key_N: KEY_N,
    Qt.Key.Key_O: KEY_O,
    Qt.Key.Key_P: KEY_P,
    Qt.Key.Key_Q: KEY_Q,
    Qt.Key.Key_R: KEY_R,
    Qt.Key.Key_S: KEY_S,
    Qt.Key.Key_T: KEY_T,
    Qt.Key.Key_U: KEY_U,
    Qt.Key.Key_V: KEY_V,
    Qt.Key.Key_W: KEY_W,
    Qt.Key.Key_X: KEY_X,
    Qt.Key.Key_Y: KEY_Y,
    Qt.Key.Key_Z: KEY_Z,
    
    Qt.Key.Key_F1: KEY_F1,
    Qt.Key.Key_F2: KEY_F2,
    Qt.Key.Key_F3: KEY_F3,
    Qt.Key.Key_F4: KEY_F4,
    Qt.Key.Key_F5: KEY_F5,
    Qt.Key.Key_F6: KEY_F6,
    Qt.Key.Key_F7: KEY_F7,
    Qt.Key.Key_F8: KEY_F8,
    Qt.Key.Key_F9: KEY_F9,
    Qt.Key.Key_F10: KEY_F10,
    Qt.Key.Key_F11: KEY_F11,
    Qt.Key.Key_F12: KEY_F12}

QT_TOUCH_STATE = {
    Qt.TouchPointState.TouchPointPressed: TOUCH_PRESSED,
    Qt.TouchPointState.TouchPointReleased: TOUCH_RELEASED,
    Qt.TouchPointState.TouchPointMoved: TOUCH_MOVED,
    Qt.TouchPointState.TouchPointStationary: TOUCH_STATIC}

QT_RASTER_TYPES = {
    '.bmp',
    '.gif',
    '.jpg',
    '.jpeg',
    '.png'}

QT_VECTOR_TYPES = {
    '.pdf'}
