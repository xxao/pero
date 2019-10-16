#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..enums import Enum

# constants
PLOT_TAG = 'plot'
GRID_Z = 0
TITLE_Z = 100
SERIES_Z = 1000
LABELS_Z = 2000
ANNOTS_Z = 3000
LEGEND_Z = 4000

ZOOM_X = 'x'
ZOOM_Y = 'y'
ZOOM_XY = 'xy'
ZOOM_AUTO = 'auto'

MEASURE_X = 'x'
MEASURE_Y = 'y'
MEASURE_AUTO = 'auto'

# define zoom tool modes
ZOOM_MODE = Enum(
    X = ZOOM_X,
    Y = ZOOM_Y,
    XY = ZOOM_XY,
    AUTO = ZOOM_AUTO)

# define measurement tool mode
MEASURE_MODE = Enum(
    X = MEASURE_X,
    Y = MEASURE_Y,
    AUTO = MEASURE_AUTO)
