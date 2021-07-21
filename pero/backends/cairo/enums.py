#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import cairo
from ... enums import *


CAIRO_LINE_CAP = {
    LINE_CAP_BUTT: cairo.LineCap.BUTT,
    LINE_CAP_SQUARE: cairo.LineCap.SQUARE,
    LINE_CAP_ROUND: cairo.LineCap.ROUND}

CAIRO_LINE_JOIN = {
    LINE_JOIN_BEVEL: cairo.LineJoin.BEVEL,
    LINE_JOIN_MITER: cairo.LineJoin.MITER,
    LINE_JOIN_ROUND: cairo.LineJoin.ROUND}

CAIRO_LINE_STYLE = {
    LINE_STYLE_CUSTOM: LINE_STYLE_CUSTOM,
    LINE_STYLE_SOLID: LINE_STYLE_SOLID,
    LINE_STYLE_DOTTED: DASH_VALUES_DOTTED,
    LINE_STYLE_DASHED: DASH_VALUES_DASHED,
    LINE_STYLE_DASHDOTTED: DASH_VALUES_DASHDOTTED}

CAIRO_FILL_RULE = {
    FILL_RULE_EVENODD: cairo.FillRule.EVEN_ODD,
    FILL_RULE_WINDING: cairo.FillRule.WINDING}

CAIRO_FONT_STYLE = {
    FONT_STYLE_NORMAL: cairo.FontSlant.NORMAL,
    FONT_STYLE_ITALIC: cairo.FontSlant.ITALIC}

CAIRO_FONT_WEIGHT = {
    FONT_WEIGHT_NORMAL: cairo.FontWeight.NORMAL,
    FONT_WEIGHT_LIGHT: cairo.FontWeight.NORMAL,
    FONT_WEIGHT_BOLD: cairo.FontWeight.BOLD,
    FONT_WEIGHT_BLACK: cairo.FontWeight.BOLD,
    FONT_WEIGHT_HEAVY: cairo.FontWeight.BOLD,
    FONT_WEIGHT_SEMIBOLD: cairo.FontWeight.BOLD,
    FONT_WEIGHT_MEDIUM: cairo.FontWeight.NORMAL,
    FONT_WEIGHT_ULTRALIGHT: cairo.FontWeight.NORMAL,
    FONT_WEIGHT_THIN: cairo.FontWeight.NORMAL}

CAIRO_FONT_FAMILY = {
    FONT_FAMILY_SERIF: FONT_FACE_SERIF,
    FONT_FAMILY_SANS: FONT_FACE_SANS,
    FONT_FAMILY_MONO: FONT_FACE_MONO}

CAIRO_RASTER_TYPES = {
    '.bmp': 'BMP',
    '.gif': 'GIF',
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.png': 'PNG',
    '.tif': 'TIFF',
    '.tiff': 'TIFF'}

CAIRO_VECTOR_TYPES = {
    '.eps': 'EPS',
    '.pdf': 'PDF',
    '.svg': 'SVG'}
