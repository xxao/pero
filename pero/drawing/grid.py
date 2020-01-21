#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from ..enums import *
from ..properties import *
from .glyphs import Glyph


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
    
    The 'ticks' are expected to be provided as distance values from the origin.
    
    Properties:
        
        orientation: pero.ORIENTATION or callable
            Specifies the lines orientation as any item from the
            pero.ORIENTATION enum.
        
        length: int, float or callable
            Specifies the lines length.
        
        angle properties:
            Includes pero.AngleProperties to specify the lines angle.
    """
    
    orientation = EnumProperty(ORI_HORIZONTAL, enum=ORIENTATION)
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
        
        # calc sin/cos
        sin = math.sin(angle)
        cos = math.cos(angle)
        
        # start drawing group
        canvas.group(tag, "grid")
        
        # draw lines
        for tick in ticks:
            
            x1 = x - tick * sin
            y1 = y + tick * cos
            x2 = x + length * cos - tick * sin
            y2 = y + length * sin + tick * cos
            
            canvas.draw_line(x1=x1, y1=y1, x2=x2, y2=y2)
        
        # end drawing group
        canvas.ungroup()


class RayGrid(Grid):
    """
    Ray grid are drawn as a star-like series of lines of specified length.
    This type of grid is typically used by polar plots.
    
    The 'ticks' are expected to be provided in angle 'units'.
    
    Properties:
        
        length: int, float or callable
            Specifies the lines length.
        
        offset: int, float or callable
            Specifies the angle offset to be added to each tick.
        
        units: pero.ANGLE or callable
            Specifies the angle units for the ticks and offset as any item from
            the pero.ANGLE enum.
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
    Radial grid are drawn as series of concentric circles or arcs defined
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
    
    start_angle = Include(AngleProperties, prefix="start_")
    end_angle = Include(AngleProperties, prefix="end_")
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
