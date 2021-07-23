#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from . glyph import Glyph


class Grid(Glyph):
    """
    Abstract base class for various types of grids, typically used to draw plot
    grids. They are drawn as series of lines for given coordinates defined by
    the 'ticks' property and specified origin. Every tick value represents a
    single coordinate according to a grid type etc. The origin coordinates
    represent a top-left corner of the bounding box or a center in centered
    grids.
    
    Grid serve as a drawing glyph only and do not implement any logic to
    generate the ticks itself. Everything is expected to be supplied in the
    final form already.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the origin.
        
        y: int, float or callable
            Specifies the y-coordinate of the origin.
        
        ticks: (float,), callable, None or UNDEF
            Specifies the sequence of ticks values according to particular
            type of grid.
        
        line properties:
            Includes pero.LineProperties to specify the line.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    ticks = TupleProperty(None, intypes=(int, float), nullable=True)
    
    pen = Include(LineProperties)


class ParallelGrid(Grid):
    """
    Parallel grid is drawn as a series of horizontal or vertical parallel
    lines of specified length. This type of grid is typically used by
    Cartesian plots.
    
    According to the 'relative' property, the ticks are expected to be provided
    as relative values (True) (as distances from the origin) or as absolute
    values (False) (as distances from device zero). The coordination of the
    distances is defined by the 'orientation' property.
    
    Properties:
        
        orientation: pero.ORIENTATION or callable
            Specifies the lines orientation as any item from the
            pero.ORIENTATION enum.
        
        relative: bool or callable
            Specifier whether the ticks values are given as a shift from the
            origin (True) or as absolute values (False).
        
        length: int, float or callable
            Specifies the lines length.
        
        angle properties:
            Includes pero.AngleProperties to specify the lines angle.
    """
    
    orientation = EnumProperty(ORI_HORIZONTAL, enum=ORIENTATION)
    relative = BoolProperty(False)
    length = NumProperty(UNDEF)
    angle = Include(AngleProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw grid."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        ticks = self.get_property('ticks', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        relative = self.get_property('relative', source, overrides)
        length = self.get_property('length', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # check ticks
        if not ticks:
            return
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # apply orientation
        if orientation == ORI_VERTICAL:
            angle -= 0.5*math.pi
            length *= -1
        
        # make ticks relative
        offset = 0
        if not relative:
            offset -= x if orientation == ORI_VERTICAL else y
        
        # calc sin/cos
        sin = round(math.sin(angle), 5)
        cos = round(math.cos(angle), 5)
        
        # start drawing group
        canvas.group(tag, "grid")
        
        # draw lines
        for tick in ticks:
            
            x1 = x - (tick+offset) * sin
            y1 = y + (tick+offset) * cos
            x2 = x + length * cos - (tick+offset) * sin
            y2 = y + length * sin + (tick+offset) * cos
            
            canvas.draw_line(x1=x1, y1=y1, x2=x2, y2=y2)
        
        # end drawing group
        canvas.ungroup()


class RayGrid(Grid):
    """
    Ray grid is drawn as a star-like series of lines of specified length.
    This type of grid is typically used by polar plots.
    
    The 'ticks' are expected to be provided in angle 'units'.
    
    Properties:
        
        length: int, float or callable
            Specifies the lines length.
        
        offset: int, float or callable
            Specifies the shift from center to be applied to each tick.
        
        units: pero.ANGLE or callable
            Specifies the angle units for the ticks as any item from the
            pero.ANGLE enum.
    """
    
    length = NumProperty(UNDEF)
    offset = NumProperty(0)
    units = EnumProperty(ANGLE_RAD, enum=ANGLE)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw grid."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        ticks = self.get_property('ticks', source, overrides)
        units = self.get_property('units', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        offset = self.get_property('offset', source, overrides)
        length = self.get_property('length', source, overrides)
        
        # check ticks
        if not ticks:
            return
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # convert angles
        if units == ANGLE_DEG:
            ticks = tuple(map(math.radians, ticks))
        
        # get radii
        inner_radius = offset
        outer_radius = offset + length
        
        # start drawing group
        canvas.group(tag, "grid")
        
        # draw lines
        for angle in ticks:
            
            cos = math.cos(angle)
            sin = math.sin(angle)
            
            x1 = x + inner_radius * cos
            y1 = y + inner_radius * sin
            x2 = x + outer_radius * cos
            y2 = y + outer_radius * sin
            
            canvas.draw_line(x1, y1, x2, y2)
        
        # end drawing group
        canvas.ungroup()


class RadialGrid(Grid):
    """
    Radial grid is drawn as series of concentric circles or arcs defined
    by 'start_angle' and 'end_angle'. This type of grid is typically used
    by polar plots.
    
    The 'ticks' are expected to be provided as distance values from the origin.
    
    Properties:
        
        start_angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        end_angle properties:
            Includes pero.AngleProperties to specify the end angle.
        
        clockwise: bool or callable
            Specifies the drawing direction. If set to True the grid is drawn
            clockwise, otherwise anti-clockwise.
    """
    
    start_angle = Include(AngleProperties, prefix="start")
    end_angle = Include(AngleProperties, prefix="end")
    clockwise = BoolProperty(True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw grid."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        ticks = self.get_property('ticks', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        clockwise = self.get_property('clockwise', source, overrides)
        start_angle = AngleProperties.get_angle(self, 'start_', ANGLE_RAD, source, overrides)
        end_angle = AngleProperties.get_angle(self, 'end_', ANGLE_RAD, source, overrides)
        
        # check ticks
        if not ticks:
            return
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "grid")
        
        # draw full circles
        if start_angle % (2 * math.pi) == end_angle % (2 * math.pi):
            for radius in ticks:
                canvas.draw_circle(x, y, radius)
        
        # draw arcs
        else:
            for radius in ticks:
                canvas.draw_arc(x, y, radius, start_angle, end_angle, clockwise)
        
        # end drawing group
        canvas.ungroup()
