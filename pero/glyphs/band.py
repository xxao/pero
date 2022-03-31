#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from .. drawing import Path, FrameProperty
from . glyph import Glyph
from . markers import Marker


class Band(Glyph):
    """
    Band glyph provides basic functionality to draw x-sorted data points as a
    filled band of varying thickness.
    
    To plot data as a line the 'show_line' property must be set to True.
    Similarly, to display individual points, the 'show_points' property must be
    set to True. If set to UNDEF, and line is enabled, the points are
    automatically visible if they are separated enough, as defined by the
    'spacing' property. The band area can be displayed if 'show_area' property
    is set to True.
    
    When individual points are drawn, original 'data' item is provided as the
    'source' together with relevant overrides to the marker glyph so any
    property of the marker can be dynamic.
    
    If the 'clip' property is defined, drawn data will be clipped to show the
    specified region only. Note that this is applied to points only and not to
    the line and area fill.
    
    Properties:
        
        show_line: bool or callable
            Specifies whether the profile lines should be displayed.
        
        show_points: bool, callable or UNDEF
            Specifies whether individual points should be displayed. If set to
            UNDEF, the points are displayed automatically as long as they are
            distance is big enough.
        
        show_area: bool or callable
            Specifies whether the area between the profile lines should be
            displayed.
        
        data: tuple, callable, None or UNDEF
            Specifies the sequence of raw data to be provided as the source for
            drawing individual points.
        
        x: tuple or callable
            Specifies the x-coordinates of the profile lines.
        
        y1: tuple or callable
            Specifies the top y-coordinates of the profile line.
        
        y2: tuple or callable
            Specifies the bottom y-coordinates of the profile line.
        
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
    y1 = SequenceProperty(UNDEF, intypes=(int, float))
    y2 = SequenceProperty(UNDEF, intypes=(int, float))
    
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
        spacing = self.get_property('spacing', source, overrides)
        x_coords = self.get_property('x', source, overrides)
        y1_coords = self.get_property('y1', source, overrides)
        y2_coords = self.get_property('y2', source, overrides)
        
        # enable/disable points display
        if show_points is UNDEF:
            diff = numpy.min(numpy.diff(x_coords)) if len(x_coords) > 1 else 0
            show_points = diff > spacing
        
        # start drawing group
        canvas.group(tag, "band")
        
        # draw area
        if show_area:
            self._draw_area(canvas, source, overrides, x_coords, y1_coords, y2_coords)
        
        # draw lines
        if show_line:
            self._draw_lines(canvas, source, overrides, x_coords, y1_coords, y2_coords)
        
        # draw points
        if show_points:
            self._draw_points(canvas, source, overrides, x_coords, y1_coords, y2_coords)
        
        # end drawing group
        canvas.ungroup()
    
    
    def _draw_area(self, canvas, source, overrides, x_coords, y1_coords, y2_coords):
        """Draws band area."""
        
        # set pen and brush
        canvas.line_color = None
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # concatenate points
        x_coords = numpy.concatenate((x_coords, numpy.flip(x_coords, 0)), 0)
        y_coords = numpy.concatenate((y1_coords, numpy.flip(y2_coords, 0)), 0)
        
        # init points
        points = numpy.stack((x_coords, y_coords), axis=1)
        
        # draw polygon
        canvas.draw_polygon(points)
    
    
    def _draw_lines(self, canvas, source, overrides, x_coords, y1_coords, y2_coords):
        """Draws band lines."""
        
        # set pen and brush
        canvas.fill_color = None
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # draw lines
        points = numpy.stack((x_coords, y1_coords), axis=1)
        canvas.draw_lines(points)
        
        points = numpy.stack((x_coords, y2_coords), axis=1)
        canvas.draw_lines(points)
    
    
    def _draw_points(self, canvas, source, overrides, x_coords, y1_coords, y2_coords):
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
            y1 = y1_coords[i]
            y2 = y2_coords[i]
            radius = 0.5 * marker.get_property('size', point_data, marker_overrides)
            
            # apply x-clipping
            if clip and (clip.x1 > x+radius or clip.x2 < x-radius):
                continue
            
            # draw y1
            if not clip or (clip.y1 < y1+radius and clip.y2 > y1-radius):
                marker.draw(canvas, point_data, x=x, y=y1, **marker_overrides)
            
            # draw y2
            if not clip or (clip.y1 < y2+radius and clip.y2 > y2-radius):
                marker.draw(canvas, point_data, x=x, y=y2, **marker_overrides)
