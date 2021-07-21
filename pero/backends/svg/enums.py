#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ... enums import *


SVG_LINE_CAP = {
    LINE_CAP_BUTT: 'butt',
    LINE_CAP_SQUARE: 'square',
    LINE_CAP_ROUND: 'round'}

SVG_LINE_JOIN = {
    LINE_JOIN_BEVEL: 'bevel',
    LINE_JOIN_MITER: 'miter',
    LINE_JOIN_ROUND: 'round'}

SVG_LINE_STYLE = {
    LINE_STYLE_CUSTOM: 'custom',
    LINE_STYLE_SOLID: 'solid',
    LINE_STYLE_DOTTED: DASH_VALUES_DOTTED,
    LINE_STYLE_DASHED: DASH_VALUES_DASHED,
    LINE_STYLE_DASHDOTTED: DASH_VALUES_DASHDOTTED}

SVG_FILL_RULE = {
    FILL_RULE_EVENODD: 'evenodd',
    FILL_RULE_WINDING: 'nonzero'}

SVG_FONT_STYLE = {
    FONT_STYLE_NORMAL: 'normal',
    FONT_STYLE_ITALIC: 'italic'}

SVG_FONT_FAMILY = {
    FONT_FAMILY_SERIF: 'serif',
    FONT_FAMILY_SANS: 'sans-serif',
    FONT_FAMILY_MONO: 'monospace'}

SVG_FONT_WEIGHT = {
    FONT_WEIGHT_NORMAL: 'normal',
    FONT_WEIGHT_LIGHT: 'lighter',
    FONT_WEIGHT_BOLD: 'bold',
    FONT_WEIGHT_BLACK: 'bold',
    FONT_WEIGHT_HEAVY: 'bold',
    FONT_WEIGHT_SEMIBOLD: 'bold',
    FONT_WEIGHT_MEDIUM: 'normal',
    FONT_WEIGHT_ULTRALIGHT: 'lighter',
    FONT_WEIGHT_THIN: 'lighter'}

SVG_TEXT_ALIGN = {
    TEXT_ALIGN_LEFT: 'start',
    TEXT_ALIGN_RIGHT: 'end',
    TEXT_ALIGN_CENTER: 'middle'}

SVG_TEXT_BASE = {
    TEXT_BASE_TOP: 'text-before-edge',
    TEXT_BASE_MIDDLE: 'central',
    TEXT_BASE_BOTTOM: 'text-after-edge'}
