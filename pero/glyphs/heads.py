#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import Matrix, Path
from . glyph import Glyph


class Head(Glyph):
    """
    Abstract base class for various types of heads, typically used as part of an
    arrow at the beginning and/or the end of the arrow line. They are simple
    glyphs defined by size and rotation angle, drawn at specified position.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        size: int, float or callable
            Specifies the full size.
        
        angle properties:
            Includes pero.AngleProperties to specify the angle.
        
        line properties:
            Includes pero.LineProperties to specify the head outline.
        
        fill properties:
            Includes pero.FillProperties to specify the head fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    size = NumProperty(10)
    angle = Include(AngleProperties)
    
    line = Include(LineProperties, line_color=UNDEF)
    fill = Include(FillProperties, fill_color=UNDEF)
    
    
    @staticmethod
    def create(symbol, **overrides):
        """
        Initializes a new instance of specified head.
        
        Args:
            symbol: str
                Head symbol.
        
        Returns:
            pero.Head
                Initialized head.
        """
        
        # convert from symbol
        if symbol == HEAD_CIRCLE:
            return CircleHead(**overrides)
        
        elif symbol == HEAD_LINE:
            return LineHead(**overrides)
        
        elif symbol in (HEAD_NORMAL, HEAD_NORMAL_B):
            return NormalHead(**overrides)
        
        elif symbol in (HEAD_OPEN, HEAD_OPEN_B):
            return OpenHead(**overrides)
        
        elif symbol in (HEAD_VEE, HEAD_VEE_B):
            return VeeHead(**overrides)
        
        raise ValueError("Unknown head symbol! -> '%s'" % symbol)


class CircleHead(Head):
    """Defines a circular head."""
    
    line_color = ColorProperty(None, nullable=True)
    fill_color = ColorProperty(UNDEF, nullable=True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw head."""
        
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
        canvas.draw_circle(x, y, 0.5 * size)


class LineHead(Head):
    """Defines a strait line head."""
    
    line_color = ColorProperty(UNDEF, nullable=True)
    fill_color = ColorProperty(None, nullable=True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw head."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # get coords
        angle -= 0.5*math.pi
        x_shift = 0.5*size * math.cos(angle)
        y_shift = 0.5*size * math.sin(angle)
        
        # set pen
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_line(x-x_shift, y-y_shift, x+x_shift, y+y_shift)


class NormalHead(Head):
    """Defines a closed triangle head."""
    
    line_color = ColorProperty(None, nullable=True)
    fill_color = ColorProperty(UNDEF, nullable=True)
    
    _f = 0.5/(math.sqrt(3)/2)
    _points = ((-_f*1.5, -0.5), (0,0), (-_f*1.5, +0.5))
    _path = Path().polygon(_points)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw head."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # transform path
        matrix = Matrix().scale(size, size).rotate(angle).translate(x, y)
        path = self._path.transformed(matrix)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)


class OpenHead(Head):
    """Defines an opened triangle head."""
    
    line_color = ColorProperty(UNDEF, nullable=True)
    fill_color = ColorProperty(None, nullable=True)
    
    _f = 0.5/(math.sqrt(3)/2)
    _points = ((-_f*1.5, -0.5), (0,0), (-_f*1.5, +0.5))
    _path = Path().move_to(*_points[0]).line_to(*_points[1]).line_to(*_points[2])
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw head."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # transform path
        matrix = Matrix().scale(size, size).rotate(angle).translate(x, y)
        path = self._path.transformed(matrix)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)


class SymbolHead(Head):
    """
    Defines a custom path head. The path must be a 'symbol-path' i.e. anchored
    at 0,0 coordinates, scaled to fit into 1x1 square and pointing right. This
    can be created from any path by calling the 'symbol' method.
    
    Properties:
        
        path: pero.Path, callable, None or UNDEF
            Specifies the symbol-path to be used as head.
    """
    
    path = Property(UNDEF, types=(Path,), nullable=True)
    
    line_color = ColorProperty(None, nullable=True)
    fill_color = ColorProperty(UNDEF, nullable=True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw head."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        path = self.get_property('path', source, overrides)
        
        # check data
        if not path:
            return
        
        # transform symbol (assuming unit coords, zero center, pointing right)
        matrix = Matrix().scale(size, size).rotate(angle).translate(x, y)
        path = path.transformed(matrix)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)


class VeeHead(Head):
    """Defines a closed V-shape head."""
    
    line_color = ColorProperty(None, nullable=True)
    fill_color = ColorProperty(UNDEF, nullable=True)
    
    _f = 0.5/(math.sqrt(3)/2)
    _points = ((-_f*1.5, -0.5), (0,0), (-_f*1.5, +0.5), (-1+_f, 0))
    _path = Path().polygon(_points)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw head."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        size = self.get_property('size', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # transform path
        matrix = Matrix().scale(size, size).rotate(angle).translate(x, y)
        path = self._path.transformed(matrix)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)


class HeadProperty(Property):
    """
    Defines a head property, which simplifies a head definition by converting
    specific symbols into an instance of corresponding head glyph. Available
    symbols are defined by the pero.HEAD enum.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of HeadProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (Head, str,)
        
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check type
        if isinstance(value, Head):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow UNDEF and None
        if value is UNDEF or value is None:
            return value
        
        # check func
        if callable(value):
            return value
        
        # convert from symbol
        return Head.create(value)
