#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ...enums import *


MUPDF_LINE_CAP = {
    LINE_CAP.BUTT: 0,
    LINE_CAP.ROUND: 1,
    LINE_CAP.SQUARE: 2}

MUPDF_LINE_JOIN = {
    LINE_JOIN.MITER: 0,
    LINE_JOIN.ROUND: 1,
    LINE_JOIN.BEVEL: 2}

MUPDF_LINE_STYLE = {
    LINE_STYLE.CUSTOM: 'custom',
    LINE_STYLE.SOLID: 'solid',
    LINE_STYLE.DOTTED: DASH_VALUES.DOTTED,
    LINE_STYLE.DASHED: DASH_VALUES.DASHED,
    LINE_STYLE.DASHDOTTED: DASH_VALUES.DASHDOTTED}

MUPDF_FILL_RULE = {
    FILL_RULE.EVENODD: True,
    FILL_RULE.WINDING: False}
