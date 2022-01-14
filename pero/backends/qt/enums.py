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

QT_RASTER_TYPES = {
    '.bmp',
    '.gif',
    '.jpg',
    '.jpeg',
    '.png'}

QT_VECTOR_TYPES = {
    '.pdf'}

QT_TOUCH_STATE = {
    Qt.TouchPointState.TouchPointPressed: TOUCH_PRESSED,
    Qt.TouchPointState.TouchPointReleased: TOUCH_RELEASED,
    Qt.TouchPointState.TouchPointMoved: TOUCH_MOVED,
    Qt.TouchPointState.TouchPointStationary: TOUCH_STATIC}
