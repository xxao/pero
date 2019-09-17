#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ...enums import *


QT_LINE_CAP = {
    LINE_CAP.BUTT: Qt.FlatCap,
    LINE_CAP.SQUARE: Qt.SquareCap,
    LINE_CAP.ROUND: Qt.RoundCap}

QT_LINE_JOIN = {
    LINE_JOIN.BEVEL: Qt.BevelJoin,
    LINE_JOIN.MITER: Qt.MiterJoin,
    LINE_JOIN.ROUND: Qt.RoundJoin}

QT_LINE_STYLE = {
    LINE_STYLE.CUSTOM: Qt.CustomDashLine,
    LINE_STYLE.SOLID: Qt.SolidLine,
    LINE_STYLE.DOTTED: DASH_VALUES.DOTTED,
    LINE_STYLE.DASHED: DASH_VALUES.DASHED,
    LINE_STYLE.DASHDOTTED: DASH_VALUES.DASHDOTTED}

QT_FILL_STYLE = {
    FILL_STYLE.TRANS: Qt.NoBrush,
    FILL_STYLE.SOLID: Qt.SolidPattern}

QT_FILL_RULE = {
    FILL_RULE.EVENODD: Qt.OddEvenFill,
    FILL_RULE.WINDING: Qt.WindingFill}

QT_FONT_FAMILY = {
    FONT_FAMILY.SERIF: FONT_FACE_SERIF,
    FONT_FAMILY.SANS: FONT_FACE_SANS,
    FONT_FAMILY.MONO: FONT_FACE_MONO}

QT_FONT_STYLE = {
    FONT_STYLE.NORMAL: False,
    FONT_STYLE.ITALIC: True}

QT_FONT_WEIGHT = {
    FONT_WEIGHT.NORMAL: QFont.Normal,
    FONT_WEIGHT.LIGHT: QFont.Light,
    FONT_WEIGHT.BOLD: QFont.Bold,
    FONT_WEIGHT.BLACK: QFont.Black,
    FONT_WEIGHT.HEAVY: QFont.Black,
    FONT_WEIGHT.SEMIBOLD: QFont.DemiBold,
    FONT_WEIGHT.MEDIUM: QFont.Normal,
    FONT_WEIGHT.ULTRALIGHT: QFont.Light,
    FONT_WEIGHT.THIN: QFont.Light}

QT_CURSORS = {
    CURSOR.BLANK: Qt.BlankCursor,
    CURSOR.ARROW: Qt.ArrowCursor,
    CURSOR.HAND: Qt.OpenHandCursor,
    CURSOR.SIZEWE: Qt.SizeHorCursor,
    CURSOR.SIZENS: Qt.SizeVerCursor}
