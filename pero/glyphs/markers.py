#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from .. drawing import Matrix, Path
from . glyph import Glyph


class Marker(Glyph):
    """
    Abstract base class for various types of markers, typically used to draw
    individual points of plotted series etc. They are simple glyphs defined by
    size and drawn at specified position.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the center.
        
        y: int, float or callable
            Specifies the y-coordinate of the center.
        
        size: int, float or callable
            Specifies the size.
        
        line properties:
            Includes pero.LineProperties to specify the marker outline.
        
        fill properties:
            Includes pero.FillProperties to specify the marker fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    size = NumProperty(8)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    @staticmethod
    def create(symbol, **overrides):
        """
        Initializes a new instance of specified marker.
        
        Args:
            symbol: str
                Marker symbol.
        
        Returns:
            pero.Marker
                Initialized marker.
        """
        
        # convert from symbol
        if symbol == MARKER_ASTERISK:
            return Asterisk(**overrides)
        
        elif symbol == MARKER_CIRCLE:
            return Circle(**overrides)
        
        elif symbol == MARKER_CROSS:
            return Cross(**overrides)
        
        elif symbol == MARKER_PLUS:
            return Plus(**overrides)
        
        elif symbol == MARKER_TRIANGLE:
            return Triangle(**overrides)
        
        elif symbol == MARKER_SQUARE:
            return Square(**overrides)
        
        elif symbol == MARKER_DIAMOND:
            return Diamond(**overrides)
        
        elif symbol == MARKER_PENTAGON:
            return Symbol(path=Path.make_ngon(5), **overrides)
        
        elif symbol == MARKER_HEXAGON:
            return Symbol(path=Path.make_ngon(6), **overrides)
        
        raise ValueError("Unknown marker symbol! -> '%s'" % symbol)


class Asterisk(Marker):
    """Defines an asterisk marker."""
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        
        # get radii
        radius1 = 0.5*size
        radius2 = radius1*0.5*numpy.sqrt(2)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_line(x-radius1, y, x+radius1, y)
        canvas.draw_line(x, y-radius1, x, y+radius1)
        canvas.draw_line(x-radius2, y-radius2, x+radius2, y+radius2)
        canvas.draw_line(x-radius2, y+radius2, x+radius2, y-radius2)


class Circle(Marker):
    """Defines a circular marker."""
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_circle(x, y, 0.5*size)


class Cross(Marker):
    """Defines a cross marker."""
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        
        # get radius
        radius = 0.5*size
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_line(x-radius, y-radius, x+radius, y+radius)
        canvas.draw_line(x+radius, y-radius, x-radius, y+radius)


class Diamond(Marker):
    """Defines a diamond marker."""
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        
        # get radius
        radius = 0.5*size
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_polygon((
            (x, y-radius),
            (x+radius, y),
            (x, y+radius),
            (x-radius, y)))


class Plus(Marker):
    """Defines a plus marker."""
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        
        # get radius
        radius = 0.5*size
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_line(x-radius, y, x+radius, y)
        canvas.draw_line(x, y-radius, x, y+radius)


class Triangle(Marker):
    """Defines a triangle marker."""
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        
        # get factor
        f = (size/2.)/(numpy.sqrt(3)/2.)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_polygon((
            (x, y-f),
            (x+0.5*size, y+f*0.5),
            (x-0.5*size, y+f*0.5)))


class Square(Marker):
    """Defines a square marker."""
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_rect(x-0.5*size, y-0.5*size, size, size)


class Symbol(Marker):
    """
    Defines a custom path marker. The path must be a 'symbol-path' i.e. centered
    at 0,0 and scaled to fit into 1x1 square. This can be created from any path
    by calling the 'symbol' method.
    
    Properties:
        
        path: pero.Path, callable, None or UNDEF
            Specifies the 'symbol-path' to be used as marker.
    """
    
    path = Property(UNDEF, types=(Path,), nullable=True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw marker."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        path = self.get_property('path', source, overrides)
        
        # check data
        if not path:
            return
        
        # scale path
        matrix = Matrix().scale(size, size).translate(x, y)
        path = path.transformed(matrix)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)


class MarkerProperty(Property):
    """
    Defines a marker property, which simplifies a marker definition by
    converting specific symbols into an instance of corresponding marker glyph.
    Available symbols are defined by the pero.MARKER enum.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of MarkerProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (Marker, str,)
        
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check type
        if isinstance(value, Marker):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow UNDEF and None
        if value is UNDEF or value is None:
            return value
        
        # check func
        if callable(value):
            return value
        
        # convert to marker
        return Marker.create(value)
