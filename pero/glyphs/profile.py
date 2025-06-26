#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from .. drawing import Path, FrameProperty
from . glyph import Glyph
from . markers import Marker


class Profile(Glyph):
    """
    Profile glyph provides basic functionality to draw x-sorted data points as a
    line and/or individual points using specified marker glyph.
    
    To plot data as a line the 'show_line' property must be set to True.
    Similarly, to display individual points, the 'show_points' property must be
    set to True. If set to UNDEF and line is enabled, the points are
    automatically visible if they are separated enough, as defined by the
    'spacing' property.
    
    When individual points are drawn, original 'data' item is provided as the
    'source' together with relevant overrides to the marker glyph so any
    property of the marker can be dynamic.
    
    Optionally the area under the curve can also be displayed if the 'show_area'
    property is set to True. In such case the line is additionally drawn as a
    filled polygon either by connecting first and last points directly or using
    strait line defined by the 'base' property.
    
    If the 'clip' property is defined, drawn data will be clipped to show the
    specified region only. Note that this is applied to points only and not to
    the line and area fill.
    
    Properties:
        
        show_line: bool or callable
            Specifies whether the profile line should be displayed.
        
        show_points: bool, callable or UNDEF
            Specifies whether individual points should be displayed. If set to
            UNDEF, the points are displayed automatically as long as their
            distance is big enough.
        
        show_area: bool or callable
            Specifies whether the area under profile line should be displayed.
        
        data: tuple, callable, None or UNDEF
            Specifies the sequence of raw data to be provided as the source for
            drawing individual points.
        
        x: tuple or callable
            Specifies the x-coordinates of the profile line.
        
        y: tuple or callable
            Specifies the y-coordinates of the profile line.
        
        base: int, float, callable, None or UNDEF
            Specifies the y-coordinate of the area base. If not set, the area
            polygon is closed by connecting first and last point.
        
        steps: pero.LINE_STEP
            Specifies the way stepped profile should be drawn as any item from
            the pero.LINE_STEP enum.
        
        spacing: int, float, callable
            Specifies the minimum x-distance between points to enable automatic
            points display.
        
        clip: pero.Frame, callable, None or UNDEF
            Specifies the clipping frame to skip drawing of points outside the
            frame.
        
        marker: pero.MARKER, pero.Path, pero.Marker, callable, None or UNDEF
            Specifies the marker to draw actual data points with. The value
            can be specified by any item from the pero.MARKER enum, as symbol
            pero.Path or as pero.Marker directly.
        
        marker_size: int, float or callable
            Specifies the marker size.
        
        marker_line properties:
            Includes pero.LineProperties to specify the marker line.
        
        marker_fill properties:
            Includes pero.FillProperties to specify the marker fill.
        
        line properties:
            Includes pero.LineProperties to specify the profile line.
        
        fill properties:
            Includes pero.FillProperties to specify the area fill.
    """
    
    show_line = BoolProperty(True)
    show_points = BoolProperty(UNDEF)
    show_area = BoolProperty(False)
    
    data = SequenceProperty(UNDEF, nullable=True)
    x = SequenceProperty(UNDEF, intypes=(int, float))
    y = SequenceProperty(UNDEF, intypes=(int, float))
    base = NumProperty(UNDEF, nullable=True)
    
    steps = EnumProperty(None, enum=LINE_STEP, nullable=True)
    spacing = IntProperty(10)
    clip = FrameProperty(UNDEF)
    
    marker = Property(MARKER_CIRCLE, types=(str, Path, Marker), nullable=True)
    marker_size = NumProperty(4)
    marker_line = Include(LineProperties, prefix='marker_', line_color=UNDEF)
    marker_fill = Include(FillProperties, prefix='marker_', fill_color=UNDEF)
    
    line = Include(LineProperties, line_color=UNDEF)
    fill = Include(FillProperties, fill_color=UNDEF)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        show_line = self.get_property('show_line', source, overrides)
        show_points = self.get_property('show_points', source, overrides)
        show_area = self.get_property('show_area', source, overrides)
        steps = self.get_property('steps', source, overrides)
        spacing = self.get_property('spacing', source, overrides)
        x_coords = self.get_property('x', source, overrides)
        y_coords = self.get_property('y', source, overrides)
        
        # enable/disable points display
        if show_points is UNDEF:
            diff = numpy.min(numpy.diff(x_coords)) if len(x_coords) > 1 else 0
            show_points = diff > spacing
        
        # make steps
        x_steps, y_steps = self._make_steps(x_coords, y_coords, steps)
        
        # start drawing group
        canvas.group(tag, "profile")
        
        # draw area
        if show_area:
            self._draw_area(canvas, source, overrides, x_steps, y_steps)
        
        # draw line
        if show_line:
            self._draw_line(canvas, source, overrides, x_steps, y_steps)
        
        # draw points
        if show_points:
            self._draw_points(canvas, source, overrides, x_coords, y_coords)
        
        # end drawing group
        canvas.ungroup()
    
    
    def _draw_area(self, canvas, source, overrides, x_coords, y_coords):
        """Draws area under the line."""
        
        # get properties
        base = self.get_property('base', source, overrides)
        
        # set pen and brush
        canvas.line_color = None
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # add base
        if base is not None and base is not UNDEF:
            x_coords = numpy.concatenate((x_coords, (x_coords[-1], x_coords[0])), 0)
            y_coords = numpy.concatenate((y_coords, (base, base)), 0)
        
        # init points
        points = numpy.stack((x_coords, y_coords), axis=1)
        
        # draw polygon
        canvas.draw_polygon(points)
    
    
    def _draw_line(self, canvas, source, overrides, x_coords, y_coords):
        """Draws main line."""
        
        # set pen and brush
        canvas.fill_color = None
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # init points
        points = numpy.stack((x_coords, y_coords), axis=1)
        
        # draw line
        canvas.draw_lines(points)
    
    
    def _draw_points(self, canvas, source, overrides, x_coords, y_coords):
        """Draws individual points."""
        
        # get properties
        clip = self.get_property('clip', source, overrides)
        data = self.get_property('data', source, overrides)
        
        # get marker overrides
        marker_overrides = self.get_child_overrides('marker', overrides)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # check raw data
        has_data = data is not UNDEF and data is not None and len(data) == len(x_coords)
        
        # draw points
        for i in range(len(x_coords)):
            
            # get point data
            point_data = data[i] if has_data else None
            
            # get marker
            marker = self.get_property('marker', point_data, overrides)
            if not marker:
                continue
            
            # init glyph
            if not isinstance(marker, Marker):
                marker = Marker.create(marker)
                marker.set_properties_from(self, src_prefix='marker_', overrides=overrides, native=True)
            
            # get coords
            x = x_coords[i]
            y = y_coords[i]
            radius = 0.5 * marker.get_property('size', point_data, marker_overrides)
            
            # apply clipping
            if clip and (clip.x1 > x+radius or clip.x2 < x-radius or clip.y1 > y+radius or clip.y2 < y-radius):
                continue
            
            # draw point
            marker.draw(canvas, point_data, x=x, y=y, **marker_overrides)
    
    
    def _make_steps(self, x_coords, y_coords, steps):
        """Adds point to make steps."""
        
        # no steps
        if steps in (UNDEF, None, LINE_STEP_NONE):
            return x_coords, y_coords
        
        # make indices
        idxs = numpy.arange(len(x_coords)-1)+1
        
        # step before
        if steps == LINE_STEP_BEFORE:
            x_coords = numpy.insert(x_coords, idxs, x_coords[:-1])
            y_coords = numpy.insert(y_coords, idxs, y_coords[1:])
        
        # step after
        elif steps == LINE_STEP_AFTER:
            x_coords = numpy.insert(x_coords, idxs, x_coords[1:])
            y_coords = numpy.insert(y_coords, idxs, y_coords[:-1])
        
        # step middle
        elif steps == LINE_STEP_MIDDLE:
            
            idxs_2 = (numpy.arange(len(x_coords)-1)+1)*2
            values = 0.5*(x_coords[:-1] + x_coords[1:])
            
            x_coords_1 = numpy.insert(x_coords, idxs, values)
            y_coords_1 = numpy.insert(y_coords, idxs, y_coords[:-1])
            
            x_coords = numpy.insert(x_coords_1, idxs_2, values)
            y_coords = numpy.insert(y_coords_1, idxs_2, y_coords[1:])
        
        return x_coords, y_coords
