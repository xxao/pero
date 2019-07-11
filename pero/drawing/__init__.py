#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# prepare modules
from . import np

# import main objects
from .fonts import Font, FontManager, FONTS
from .frame import Frame
from .graphics import Graphics
from .canvas import Canvas
from .matrix import Matrix
from .bezier import Bezier
from .path import Path
from .layout import Layout, Row, Column, Cell

# import utils
from .utils import *

# import glyphs
from .glyphs import Glyph, Annulus, Arc, Bar, Ellipse, Line, Polygon, Ray, Rect, Shape, Text, Textbox, Wedge
from .markers import Marker, Asterisk, Circle, Cross, Diamond, Plus, Triangle, Square, Symbol
from .arrows import Arrow, ArcArrow, BowArrow, ConnectorArrow, CurveArrow, LineArrow, PathArrow, RayArrow
from .heads import Head, CircleHead, LineHead, NormalHead, OpenHead, SymbolHead, VeeHead
from .grid import Grid, ParallelGrid, RayGrid, RadialGrid
from .axes import Axis, StraitAxis, RadialAxis
from .gauge import Gauge, StraitGauge, RadialGauge
from .colorbar import ColorBar
from .pather import Pather
from .framer import Framer
from .profile import Profile, Band
from .labels import Label, Labels, TextLabel
from .tooltip import Tooltip, TextTooltip

# register new properties
from .frame import FrameProperty
from .markers import MarkerProperty
from .heads import HeadProperty

from .. import properties
properties.FrameProperty = FrameProperty
properties.MarkerProperty = MarkerProperty
properties.HeadProperty = HeadProperty
