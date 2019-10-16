#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..enums import *
from ..properties import *
from ..drawing import ParallelGrid
from ..scales import ContinuousScale, LinScale
from ..tickers import Ticker, LinTicker
from .graphics import InGraphics


class Grid(InGraphics):
    """
    Grid is drawn as a series of horizontal or vertical parallel lines used for
    Cartesian plots. It typically extends ticks of specific plot axis to a whole
    size of the plot. Therefore the same instances of the 'scale' and 'ticker'
    should be provided as those used for the axis itself.
    
    Unlike other graphics, a grid is not drawn at once but sequentially to avoid
    unwanted visible cross-sections of perpendicular lines. The drawing starts
    with minor grid lines for all defined grid instances, followed by major grid
    lines. Corresponding methods should be overwritten in derived classes.
    
    Properties:
        
        show_major_lines: bool
            Specifies whether the major lines should be displayed.
        
        show_minor_lines: bool
            Specifies whether the minor lines should be displayed.
        
        scale: pero.ContinuousScale
            Specifies the scale providing actual range to use and to
            re-calculate the ticks values into final coordinates.
        
        ticker: pero.Ticker
            Specifies the ticks generator to provide lines positions.
        
        orientation: str
            Specifies the lines orientation as any item from the
            pero.ORIENTATION enum.
        
        major_line properties:
            Includes pero.LineProperties to specify the major line.
        
        minor_line properties:
            Includes pero.LineProperties to specify the minor line.
    """
    
    scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    ticker = Property(UNDEF, types=(Ticker,), dynamic=False)
    
    orientation = EnumProperty(HORIZONTAL, enum=ORIENTATION, dynamic=False)
    
    show_major_lines = BoolProperty(True, dynamic=False)
    show_minor_lines = BoolProperty(True, dynamic=False)
    
    major_line = Include(LineProperties, prefix="major_", dynamic=False, line_color="#e6e6e6ff")
    minor_line = Include(LineProperties, prefix="minor_", dynamic=False, line_color="#f5f5f5ff")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Grid."""
        
        super(Grid, self).__init__(**overrides)
        
        # init scale
        if self.scale is UNDEF:
            self.scale = LinScale()
        
        # init ticker
        if self.ticker is UNDEF:
            self.ticker = LinTicker()
        
        # init glyph
        self._glyph = ParallelGrid()
    
    
    def initialize(self, canvas, plot):
        """
        This method is automatically called by parent plot to set specific
        properties and perform necessary initialization steps.
        """
        
        # get axis
        axes = plot.get_obj_axes(self.tag)
        if not axes:
            return
        
        axis = plot.get_obj(axes[0])
        
        # set coords
        if axis.position in (LEFT, RIGHT):
            self.orientation = HORIZONTAL
        else:
            self.orientation = VERTICAL
        
        # set ticker
        self.ticker = axis.ticker
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the grid."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        self.draw_minor(canvas, source, **overrides)
        self.draw_major(canvas, source, **overrides)
    
    
    def draw_major(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw major lines of the grid."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # check if enabled
        if not self.get_property('show_major_lines', source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        scale = self.get_property('scale', source, overrides)
        ticker = self.get_property('ticker', source, overrides)
        frame = self.get_property('frame', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        
        # get ticks
        ticker(start=scale.in_range[0], end=scale.in_range[1])
        ticks = tuple(map(scale.scale, ticker.major_ticks()))
        
        # finalize tag
        tag = tag + "_major" if tag else None
        
        # get coords
        if orientation == HORIZONTAL:
            x = frame.x
            y = 0
            length = frame.width
        else:
            x = 0
            y = frame.y
            length = frame.height
        
        # update glyph
        self._glyph.set_properties_from(self, "major_", source=source, overrides=overrides)
        
        # draw grid
        self._glyph.draw(canvas,
            tag = tag,
            x = x,
            y = y,
            ticks = ticks,
            length = length,
            orientation = orientation)
    
    
    def draw_minor(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw minor lines of the grid."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # check if enabled
        if not self.get_property('show_minor_lines', source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        scale = self.get_property('scale', source, overrides)
        ticker = self.get_property('ticker', source, overrides)
        frame = self.get_property('frame', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        
        # get ticks
        ticker(start=scale.in_range[0], end=scale.in_range[1])
        ticks = tuple(map(scale.scale, ticker.minor_ticks()))
        
        # finalize tag
        tag = tag + "_minor" if tag else None
        
        # get coords
        if orientation == HORIZONTAL:
            x = frame.x
            y = 0
            length = frame.width
        else:
            x = 0
            y = frame.y
            length = frame.height
        
        # update glyph
        self._glyph.set_properties_from(self, "minor_", source=source, overrides=overrides)
        
        # draw grid
        self._glyph.draw(canvas,
            tag = tag,
            x = x,
            y = y,
            ticks = ticks,
            length = length,
            orientation = orientation)
