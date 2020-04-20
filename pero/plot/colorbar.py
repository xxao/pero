#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. import colors
from ..enums import *
from ..properties import *
from ..drawing import ColorBar as ColorBarGlyph
from ..scales import ContinuousScale, LinScale
from .graphics import OutGraphics


class ColorBar(OutGraphics):
    """
    ColorBar provides a simple wrapper for the pero.ColorBar glyph to visualize
    a color gradient range used to colorize data within a plot. It is typically
    displayed together with additional axis next to it and sharing the scale
    with it.
    
    ColorBar can also be used directly as a gradient scale to convert input
    values into colors by calling the 'convert' method.
    
    Properties:
        
        scale: pero.ContinuousScale
            Specifies the scale providing actual data range and to normalize
            input values for gradient.
        
        gradient: pero.Gradient, pero.Palette, tuple, str or callable
            Specifies the color gradient as a sequence of colors,
            pero.Palette, palette name or pero.Gradient. Note that the
            gradient is expected to be normalized to range 0-1.
        
        thickness: int or float
            Specifies the bar thickness.
        
        steps: int
            Specifies the number of color steps to use to draw the gradient.
        
        line properties:
            Includes pero.LineProperties to specify the outline.
        
        fill properties:
            Includes pero.FillProperties to specify the background fill.
    """
    
    scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    gradient = GradientProperty(UNDEF, dynamic=False)
    
    thickness = NumProperty(20, dynamic=False)
    steps = NumProperty(128, dynamic=False)
    
    line = Include(LineProperties, line_color="#000")
    fill = Include(FillProperties, fill_color="#fff")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of ColorBar."""
        
        # init scale
        if 'scale' not in overrides:
            overrides['scale'] = LinScale()
        
        # init gradient
        if 'gradient' not in overrides:
            overrides['gradient'] = colors.YlOrBr
        
        # init base
        super().__init__(**overrides)
        
        # init glyph
        self._glyph = ColorBarGlyph()
    
    
    def get_extent(self, canvas):
        """
        This method is automatically called by parent plot to get amount of
        logical space needed to draw the object.
        """
        
        return self.thickness
    
    
    def draw(self, canvas, source=None, **overrides):
        """Uses given canvas to draw color bar."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        
        # get orientation
        orientation = ORI_VERTICAL
        if position in (POS_TOP, POS_BOTTOM):
            orientation = ORI_HORIZONTAL
        
        # get length
        length = frame.height if orientation == ORI_VERTICAL else frame.height
        
        # update glyph
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # draw bar
        self._glyph.draw(canvas,
            x = frame.x,
            y = frame.y,
            orientation = orientation,
            reverse = orientation == ORI_VERTICAL,
            length = length)
    
    
    def convert(self, value):
        """
        Converts given value into color according to current gradient and scale.
        
        Args:
            value: float
                Value to convert in real data units.
        
        Returns:
            pero.Color
                Corresponding color.
        """
        
        # normalize value by current scale
        norm = self.scale.normalize(value)
        
        # convert normalized value into color
        return self.gradient.color_at(norm)
