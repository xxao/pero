#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ...enums import *


SVG_LINE_CAP = {
    LINE_CAP.BUTT: 'butt',
    LINE_CAP.SQUARE: 'square',
    LINE_CAP.ROUND: 'round'}

SVG_LINE_JOIN = {
    LINE_JOIN.BEVEL: 'bevel',
    LINE_JOIN.MITER: 'miter',
    LINE_JOIN.ROUND: 'round'}

SVG_LINE_STYLE = {
    LINE_STYLE.CUSTOM: 'custom',
    LINE_STYLE.SOLID: 'solid',
    LINE_STYLE.DOTTED: DASH_VALUES.DOTTED,
    LINE_STYLE.DASHED: DASH_VALUES.DASHED,
    LINE_STYLE.DASHDOTTED: DASH_VALUES.DASHDOTTED}

SVG_FILL_RULE = {
    FILL_RULE.EVENODD: 'evenodd',
    FILL_RULE.WINDING: 'nonzero'}

SVG_FONT_STYLE = {
    FONT_STYLE.NORMAL: 'normal',
    FONT_STYLE.ITALIC: 'italic'}

SVG_FONT_FAMILY = {
    FONT_FAMILY.SERIF: 'serif',
    FONT_FAMILY.SANS: 'sans-serif',
    FONT_FAMILY.MONO: 'monospace'}

SVG_FONT_WEIGHT = {
    FONT_WEIGHT.NORMAL: 'normal',
    FONT_WEIGHT.LIGHT: 'lighter',
    FONT_WEIGHT.BOLD: 'bold',
    FONT_WEIGHT.BLACK: 'bold',
    FONT_WEIGHT.HEAVY: 'bold',
    FONT_WEIGHT.SEMIBOLD: 'bold',
    FONT_WEIGHT.MEDIUM: 'normal',
    FONT_WEIGHT.ULTRALIGHT: 'lighter',
    FONT_WEIGHT.THIN: 'lighter'}

SVG_TEXT_ALIGN = {
    TEXT_ALIGN.LEFT: 'start',
    TEXT_ALIGN.RIGHT: 'end',
    TEXT_ALIGN.CENTER: 'middle'}

SVG_TEXT_BASELINE = {
    TEXT_BASELINE.TOP: 'text-before-edge',
    TEXT_BASELINE.MIDDLE: 'central',
    TEXT_BASELINE.BOTTOM: 'text-after-edge'}
