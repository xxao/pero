#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from . enum import Enum

# define cursors
CURSOR_BLANK = 'blank'
CURSOR_ARROW = 'arrow'
CURSOR_HAND = 'hand'
CURSOR_SIZEWE = 'size_we'
CURSOR_SIZENS = 'size_ns'

CURSOR = Enum(
    BLANK = CURSOR_BLANK,
    ARROW = CURSOR_ARROW,
    HAND = CURSOR_HAND,
    SIZEWE = CURSOR_SIZEWE,
    SIZENS = CURSOR_SIZENS)
