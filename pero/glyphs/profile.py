#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from .. drawing import FrameProperty
from . glyph import Glyph
from . markers import MarkerProperty, Circle


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
            UNDEF, the points are displayed automatically as long as they are
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
            
        marker: pero.Marker, pero.MARKER, callable, None or UNDEF
            Specifies the marker glyph to be used to draw individual points. The
            value can be specified by any item from the pero.MARKER enum or
            as a pero.MARKER instance.
        
        spacing: int, float, callable
            Specifies the minimum x-distance between points to enable automatic
            points display.
        
        clip: pero.Frame, callable, None or UNDEF
            Specifies the clipping frame to skip drawing of points outside the
            frame.
        
        color: pero.Color, (int,), str, callable, None or UNDEF
            Specifies the global color as an RGB or RGBA tuple, hex code, name
            or pero.Color. If the color is set to None, transparent color is
            set instead. This value will not overwrite specific line or fill
            color if defined.
        
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
    marker = MarkerProperty(UNDEF, nullable=True)
    spacing = IntProperty(10)
    
    clip = FrameProperty(UNDEF)
    
    color = ColorProperty(UNDEF, nullable=True)
    line = Include(LineProperties, line_color=UNDEF)
    fill = Include(FillProperties, fill_color=UNDEF)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Profile."""
        
        # init marker
        if 'marker' not in overrides:
            overrides['marker'] = Circle(size=4)
        
        # init base
        super().__init__(**overrides)
    
    
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
        marker = self.get_property('marker', source, overrides)
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
        if marker and (show_points or not (show_line or show_area)):
            self._draw_points(canvas, source, overrides, x_coords, y_coords)
        
        # end drawing group
        canvas.ungroup()
    
    
    def _draw_area(self, canvas, source, overrides, x_coords, y_coords):
        """Draws area under the line."""
        
        # get properties
        base = self.get_property('base', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # set pen and brush
        canvas.fill_color = color
        canvas.line_color = None
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # init points
        points = numpy.stack((x_coords, y_coords), axis=1)
        
        # add base
        if base is not None and base is not UNDEF:
            points = numpy.append(points,
                values = [(points[-1][0], base), (points[0][0], base)],
                axis = 0)
        
        # draw polygon
        canvas.draw_polygon(points)
    
    
    def _draw_line(self, canvas, source, overrides, x_coords, y_coords):
        """Draws main line."""
        
        # get properties
        color = self.get_property('color', source, overrides)
        
        # set pen and brush
        canvas.line_color = color
        canvas.fill_color = None
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # init points
        points = numpy.stack((x_coords, y_coords), axis=1)
        
        # draw line
        canvas.draw_lines(points)
    
    
    def _draw_points(self, canvas, source, overrides, x_coords, y_coords):
        """Draws individual points."""
        
        # get properties
        marker = self.get_property('marker', source, overrides)
        clip = self.get_property('clip', source, overrides)
        data = self.get_property('data', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # get marker overrides
        marker_overrides = self.get_child_overrides('marker', overrides)
        
        # set pen and brush
        canvas.line_color = color
        canvas.fill_color = color
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # check raw data
        has_data = data is not UNDEF and data is not None and len(data) == len(x_coords)
        
        # draw points
        for i in range(len(x_coords)):
            
            # get source
            source = data[i] if has_data else None
            
            # get coords
            x = x_coords[i]
            y = y_coords[i]
            size = marker.get_property('size', source)
            radius = 0.5*size
            
            # apply clipping
            if clip and (clip.x1 > x+radius or clip.x2 < x-radius or clip.y1 > y+radius or clip.y2 < y-radius):
                continue
            
            # draw point
            marker.draw(canvas, source, x=x, y=y, size=size, **marker_overrides)
    
    
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
        
        marker: pero.Marker, pero.MARKER, callable, None or UNDEF
            Specifies the marker glyph to be used to draw individual points. The
            value can be specified by any item from the pero.MARKER enum or
            as a pero.MARKER instance.
        
        spacing: int, float, callable
            Specifies the minimum x-distance between points to enable automatic
            points display.
        
        clip: pero.Frame, callable, None or UNDEF
            Specifies the clipping frame to skip drawing of points outside the
            frame.
        
        color: pero.Color, (int,), str, callable, None or UNDEF
            Specifies the global color as an RGB or RGBA tuple, hex code, name
            or pero.Color. If the color is set to None, transparent color is
            set instead. This value will not overwrite specific line or fill
            color if defined.
        
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
    
    marker = MarkerProperty(UNDEF, nullable=True)
    spacing = IntProperty(10)
    
    clip = FrameProperty(UNDEF)
    
    color = ColorProperty(UNDEF, nullable=True)
    line = Include(LineProperties, line_color=UNDEF)
    fill = Include(FillProperties, fill_color=UNDEF)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Band."""
        
        # init marker
        if 'marker' not in overrides:
            overrides['marker'] = Circle(size=4)
        
        # init base
        super().__init__(**overrides)
    
    
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
        marker = self.get_property('marker', source, overrides)
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
        if show_points and marker:
            self._draw_points(canvas, source, overrides, x_coords, y1_coords, y2_coords)
        
        # end drawing group
        canvas.ungroup()
    
    
    def _draw_area(self, canvas, source, overrides, x_coords, y1_coords, y2_coords):
        """Draws band area."""
        
        # get properties
        color = self.get_property('color', source, overrides)
        
        # set pen and brush
        canvas.fill_color = color
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
        
        # get properties
        color = self.get_property('color', source, overrides)
        
        # set pen and brush
        canvas.line_color = color
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
        marker = self.get_property('marker', source, overrides)
        clip = self.get_property('clip', source, overrides)
        data = self.get_property('data', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # get marker overrides
        marker_overrides = self.get_child_overrides('marker', overrides)
        
        # set pen and brush
        canvas.line_color = color
        canvas.fill_color = color
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # check raw data
        has_data = data is not UNDEF and data is not None and len(data) == len(x_coords)
        
        # draw points
        for i in range(len(x_coords)):
            
            # get point data
            point_data = data[i] if has_data else None
            
            # get coords
            x = x_coords[i]
            y1 = y1_coords[i]
            y2 = y2_coords[i]
            size = marker.get_property('size', point_data)
            radius = 0.5*size
            
            # apply x-clipping
            if clip and (clip.x1 > x+radius or clip.x2 < x-radius):
                continue
            
            # draw y1
            if not clip or (clip.y1 < y1+radius and clip.y2 > y1-radius):
                marker.draw(canvas, point_data, x=x, y=y1, size=size, **marker_overrides)
            
            # draw y2
            if not clip or (clip.y1 < y2+radius and clip.y2 > y2-radius):
                marker.draw(canvas, point_data, x=x, y=y2, size=size, **marker_overrides)
