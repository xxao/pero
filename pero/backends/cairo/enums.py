#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import cairo
from ...enums import *


CAIRO_LINE_CAP = {
    LINE_CAP.BUTT: cairo.LineCap.BUTT,
    LINE_CAP.SQUARE: cairo.LineCap.SQUARE,
    LINE_CAP.ROUND: cairo.LineCap.ROUND}

CAIRO_LINE_JOIN = {
    LINE_JOIN.BEVEL: cairo.LineJoin.BEVEL,
    LINE_JOIN.MITER: cairo.LineJoin.MITER,
    LINE_JOIN.ROUND: cairo.LineJoin.ROUND}

CAIRO_LINE_STYLE = {
    LINE_STYLE.CUSTOM: LINE_STYLE.CUSTOM,
    LINE_STYLE.SOLID: LINE_STYLE.SOLID,
    LINE_STYLE.DOTTED: DASH_VALUES.DOTTED,
    LINE_STYLE.DASHED: DASH_VALUES.DASHED,
    LINE_STYLE.DASHDOTTED: DASH_VALUES.DASHDOTTED}

CAIRO_FILL_RULE = {
    FILL_RULE.EVENODD: cairo.FillRule.EVEN_ODD,
    FILL_RULE.WINDING: cairo.FillRule.WINDING}

CAIRO_FONT_STYLE = {
    FONT_STYLE.NORMAL: cairo.FontSlant.NORMAL,
    FONT_STYLE.ITALIC: cairo.FontSlant.ITALIC}

CAIRO_FONT_WEIGHT = {
    FONT_WEIGHT.NORMAL: cairo.FontWeight.NORMAL,
    FONT_WEIGHT.LIGHT: cairo.FontWeight.NORMAL,
    FONT_WEIGHT.BOLD: cairo.FontWeight.BOLD,
    FONT_WEIGHT.BLACK: cairo.FontWeight.BOLD,
    FONT_WEIGHT.HEAVY: cairo.FontWeight.BOLD,
    FONT_WEIGHT.SEMIBOLD: cairo.FontWeight.BOLD,
    FONT_WEIGHT.MEDIUM: cairo.FontWeight.NORMAL,
    FONT_WEIGHT.ULTRALIGHT: cairo.FontWeight.NORMAL,
    FONT_WEIGHT.THIN: cairo.FontWeight.NORMAL}

CAIRO_FONT_FAMILY = {
    FONT_FAMILY.SERIF: FONT_FACE_SERIF,
    FONT_FAMILY.SANS: FONT_FACE_SANS,
    FONT_FAMILY.MONO: FONT_FACE_MONO}

CAIRO_RASTER_TYPES = {
    '.bmp': 'BMP',
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.png': 'PNG',
    '.tif': 'TIFF',
    '.tiff': 'TIFF',
    '.gif': 'GIF'}

CAIRO_VECTOR_TYPES = {
    '.svg': 'SVG',
    '.pdf': 'PDF',
    '.eps': 'EPS'}
