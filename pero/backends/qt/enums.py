#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ... enums import *


QT_LINE_CAP = {
    LINE_CAP_BUTT: Qt.FlatCap,
    LINE_CAP_SQUARE: Qt.SquareCap,
    LINE_CAP_ROUND: Qt.RoundCap}

QT_LINE_JOIN = {
    LINE_JOIN_BEVEL: Qt.BevelJoin,
    LINE_JOIN_MITER: Qt.MiterJoin,
    LINE_JOIN_ROUND: Qt.RoundJoin}

QT_LINE_STYLE = {
    LINE_STYLE_CUSTOM: Qt.CustomDashLine,
    LINE_STYLE_SOLID: Qt.SolidLine,
    LINE_STYLE_DOTTED: DASH_VALUES_DOTTED,
    LINE_STYLE_DASHED: DASH_VALUES_DASHED,
    LINE_STYLE_DASHDOTTED: DASH_VALUES_DASHDOTTED}

QT_FILL_STYLE = {
    FILL_STYLE_TRANS: Qt.NoBrush,
    FILL_STYLE_SOLID: Qt.SolidPattern}

QT_FILL_RULE = {
    FILL_RULE_EVENODD: Qt.OddEvenFill,
    FILL_RULE_WINDING: Qt.WindingFill}

QT_FONT_FAMILY = {
    FONT_FAMILY_SERIF: FONT_FACE_SERIF,
    FONT_FAMILY_SANS: FONT_FACE_SANS,
    FONT_FAMILY_MONO: FONT_FACE_MONO}

QT_FONT_STYLE = {
    FONT_STYLE_NORMAL: False,
    FONT_STYLE_ITALIC: True}

QT_FONT_WEIGHT = {
    FONT_WEIGHT_NORMAL: QFont.Normal,
    FONT_WEIGHT_LIGHT: QFont.Light,
    FONT_WEIGHT_BOLD: QFont.Bold,
    FONT_WEIGHT_BLACK: QFont.Black,
    FONT_WEIGHT_HEAVY: QFont.Black,
    FONT_WEIGHT_SEMIBOLD: QFont.DemiBold,
    FONT_WEIGHT_MEDIUM: QFont.Normal,
    FONT_WEIGHT_ULTRALIGHT: QFont.Light,
    FONT_WEIGHT_THIN: QFont.Light}

QT_CURSORS = {
    CURSOR_BLANK: Qt.BlankCursor,
    CURSOR_ARROW: Qt.ArrowCursor,
    CURSOR_HAND: Qt.OpenHandCursor,
    CURSOR_SIZEWE: Qt.SizeHorCursor,
    CURSOR_SIZENS: Qt.SizeVerCursor}

QT_RASTER_TYPES = {
    '.bmp',
    '.gif',
    '.jpg',
    '.jpeg',
    '.png'}

QT_VECTOR_TYPES = {
    '.pdf'}

QT_TOUCH_STATE = {
    Qt.TouchPointPressed: TOUCH_PRESSED,
    Qt.TouchPointReleased: TOUCH_RELEASED,
    Qt.TouchPointMoved: TOUCH_MOVED,
    Qt.TouchPointStationary: TOUCH_STATIC}
