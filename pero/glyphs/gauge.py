#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from . glyph import Glyph
from . shapes import Wedge


class Gauge(Glyph):
    """
    Abstract base class for various types of gauges. It provides a simple glyph
    to visualize specific portion within a context of full data range.
    
    The 'start' and 'end' positions of the selected range are given as relative
    values within the range as %/100.
    
    By default the range increases the same way as device units, i.e. from left
    to right, from top to bottom or clockwise. This behavior can be changed by
    setting the 'reverse' property to True.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the origin.
        
        y: int, float or callable
            Specifies the y-coordinate of the origin.
        
        start: float or callable
            Specifies the start position of the foreground as a relative value
            of the full length in %/100."
        
        end: float or callable
            Specifies the end position of the foreground as a relative value
            of the full length in %/100."
        
        limit: int, float or callable
            Specifies the minimum display length of the foreground.
        
        reverse: bool or callable
            Specifies whether the foreground is drawn considering the top/left
            side (False) or the bottom/right side (True) as its start.
        
        bgr_line properties:
            Includes pero.LineProperties to specify the background outline.
        
        bgr_fill properties:
            Includes pero.FillProperties to specify the background fill.
        
        for_line properties:
            Includes pero.LineProperties to specify the foreground outline.
        
        for_fill properties:
            Includes pero.FillProperties to specify the foreground fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    
    start = NumProperty(0)
    end = NumProperty(0)
    limit = NumProperty(0)
    reverse = BoolProperty(False)
    
    bgr_pen = Include(LineProperties, prefix="bgr", line_color="#000")
    bgr_fill = Include(FillProperties, prefix="bgr", fill_color="#ddd")
    
    for_pen = Include(LineProperties, prefix="for", line_color="#000")
    for_fill = Include(FillProperties, prefix="for", fill_color="#000")


class StraitGauge(Gauge):
    """
    Strait gauge is drawn as a horizontal or vertical bar of specified length
    and thickness.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the top-left corner.
        
        y: int, float or callable
            Specifies the y-coordinate of the top-left corner.
        
        length: int, float or callable
            Specifies the bar length.
        
        thickness: int, float or callable
            Specifies the bar thickness.
        
        radius: int, float, tuple, callable or UNDEF
            Specifies the corner radius as a single value or values for
            individual corners starting from top-left.
        
        orientation: pero.ORIENTATION or callable
            Specifies the bar orientation as any item from the
            pero.ORIENTATION enum.
    """
    
    length = NumProperty(0)
    thickness = NumProperty(7)
    radius = QuadProperty(0)
    orientation = EnumProperty(ORI_HORIZONTAL, enum=ORIENTATION)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the gauge."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        length = self.get_property('length', source, overrides)
        thickness = self.get_property('thickness', source, overrides)
        radius = self.get_property('radius', source, overrides)
        limit = self.get_property('limit', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        reverse = self.get_property('reverse', source, overrides)
        start = self.get_property('start', source, overrides)
        end = self.get_property('end', source, overrides)
        
        # check edges
        start = max(0, min(1, start))
        end = max(0, min(1, end))
        
        # reverse direction
        if reverse:
            start = 1 - start
            end = 1 - end
        
        # check direction
        if start > end:
            start, end = end, start
        
        # make highlight absolute
        start = length*start
        end = length*end
        
        # check highlight limit
        if radius:
            limit = max(limit, 2*max(radius))
        
        if abs(end - start) < limit:
            diff = limit - abs(end - start)
            
            if start > .5*diff and end < length-.5*diff:
                start -= .5*diff
                end += .5*diff
            
            elif start > diff:
                start -= diff
            
            elif end < length-diff:
                end += diff
        
        # finalize by orientation
        if orientation == ORI_HORIZONTAL:
            bgr_width = length
            bgr_height = thickness
            for_x = x + start
            for_y = y
            for_width = end - start
            for_height = thickness
        
        else:
            bgr_width = thickness
            bgr_height = length
            for_x = x
            for_y = y + start
            for_width = thickness
            for_height = end - start
        
        # start drawing group
        canvas.group(tag, "gauge")
        
        # set pen and brush for background
        canvas.set_pen_by(self, prefix="bgr", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="bgr", source=source, overrides=overrides)
        
        # draw background
        canvas.draw_rect(x, y, bgr_width, bgr_height, radius)
        
        # set pen and brush for range
        canvas.set_pen_by(self, prefix="for", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="for", source=source, overrides=overrides)
        
        # draw range
        canvas.draw_rect(for_x, for_y, for_width, for_height, radius)
        
        # end drawing group
        canvas.ungroup()


class RadialGauge(Gauge):
    """
    Radial gauge is drawn as a circle or an arc.
    
    Properties:
        
        inner_radius: int, float or callable
            Specifies the inner radius.
        
        outer_radius: int, float or callable
            Specifies the outer radius.
        
        start_angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        end_angle properties:
            Includes pero.AngleProperties to specify the end angle.
        
        clockwise: bool or callable
            Specifies the drawing direction. If set to True the arc is drawn
            clockwise, otherwise anti-clockwise.
    """
    
    inner_radius = NumProperty(UNDEF)
    outer_radius = NumProperty(UNDEF)
    start_angle = Include(AngleProperties, prefix="start")
    end_angle = Include(AngleProperties, prefix="end")
    clockwise = BoolProperty(True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the gauge."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        bgr_start = AngleProperties.get_angle(self, 'start_', ANGLE_RAD, source, overrides)
        bgr_end = AngleProperties.get_angle(self, 'end_', ANGLE_RAD, source, overrides)
        inner_radius = self.get_property('inner_radius', source, overrides)
        outer_radius = self.get_property('outer_radius', source, overrides)
        clockwise = self.get_property('clockwise', source, overrides)
        limit = self.get_property('limit', source, overrides)
        reverse = self.get_property('reverse', source, overrides)
        start = self.get_property('start', source, overrides)
        end = self.get_property('end', source, overrides)
        
        # check edges
        start = max(0, min(1, start))
        end = max(0, min(1, end))
        
        # reverse direction
        if reverse:
            start = 1 - start
            end = 1 - end
        
        # check direction
        if start > end:
            start, end = end, start
        
        # get full range
        length = (bgr_end - bgr_start) % (2*math.pi)
        if not clockwise:
            length -= 2*math.pi
        
        if length == 0 and bgr_start != bgr_end:
            length = 2*math.pi
        
        # get highlight angles
        for_start = length*start
        for_end = length*end
        
        # finalize angles
        for_start = bgr_start + for_start
        for_end = bgr_start + for_end
        
        # init glyph
        glyph = Wedge(
            x = x,
            y = y,
            inner_radius = inner_radius,
            outer_radius = outer_radius,
            start_angle_units = ANGLE_RAD,
            end_angle_units = ANGLE_RAD,
            clockwise = clockwise)
        
        # start drawing group
        canvas.group(tag, "gauge")
        
        # draw background
        glyph.set_properties_from(self, src_prefix="bgr", source=source, overrides=overrides)
        glyph.draw(canvas, start_angle=bgr_start, end_angle=bgr_end)
        
        # draw range
        glyph.set_properties_from(self, src_prefix="for", source=source, overrides=overrides)
        glyph.draw(canvas, start_angle=for_start, end_angle=for_end)
        
        # end drawing group
        canvas.ungroup()
