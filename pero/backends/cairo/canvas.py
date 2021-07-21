#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import cairo
import numpy
from ... properties import *
from ... drawing import Canvas, Path, Matrix, ClipState
from . enums import *


class CairoCanvas(Canvas):
    """Wrapper for Cairo drawing context."""
    
    
    def __init__(self, dc, **overrides):
        """
        Initializes a new instance of CairoCanvas.
        
        Args:
            dc: cairo.Context
                Cairo drawing context.
            
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        # init buffers
        self._dc = dc
        self._pen = (0, 0, 0, 1)
        self._brush = None
        
        self._default_font = self._dc.get_font_face()
        self._font = {
            'family': self._default_font.get_family(),
            'style': self._default_font.get_slant(),
            'weight': self._default_font.get_weight(),
            'for_color': (0, 0, 0, 1),
            'bgr_color': None}
        
        # init base
        super().__init__(**overrides)
        
        # init canvas
        self._update_pen()
        self._update_brush()
        self._update_text()
        
        # bind events
        self.bind(EVT_PEN_CHANGED, self._update_pen)
        self.bind(EVT_BRUSH_CHANGED, self._update_brush)
        self.bind(EVT_TEXT_CHANGED, self._update_text)
    
    
    def get_line_size(self, text):
        """
        Gets width and height of a single text line using current text settings.
        
        Args:
            text: str
                Text for which the size should be calculated.
        
        Returns:
            (float, float)
                Line width and height.
        """
        
        # check text
        if not text:
            return 0, 0
        
        # get size
        width = self._dc.text_extents(text).width
        height = self._dc.font_extents()[2]
        
        return width, height
    
    
    def draw_arc(self, x, y, radius, start_angle, end_angle, clockwise=True):
        """
        Draws an arc of specified radius centered around given coordinates.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the arc.
            
            start_angle: int or float
                Angle of the starting point in radians.
            
            end_angle: int or float
                Angle of the starting point in radians.
            
            clockwise: bool
                Direction of drawing between start and end point.
        """
        
        # apply scaling and offset
        x = self._scale * (x + self._offset[0])
        y = self._scale * (y + self._offset[1])
        radius = self._scale * radius
        
        # init drawing
        self._dc.new_path()
        
        # draw
        if clockwise:
            self._dc.arc(x, y, radius, start_angle, end_angle)
        else:
            self._dc.arc_negative(x, y, radius, start_angle, end_angle)
        
        # fill and stroke
        self._fill_and_stroke()
    
    
    def draw_circle(self, x, y, radius):
        """
        Draws a circle of specified radius centered around given coordinates.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the circle.
        """
        
        # apply scaling and offset
        x = self._scale * (x + self._offset[0])
        y = self._scale * (y + self._offset[1])
        radius = self._scale * radius
        
        # init drawing
        self._dc.new_path()
        
        # draw
        self._dc.arc(x, y, radius, 0, 2*numpy.pi)
        
        # fill and stroke
        self._fill_and_stroke()
    
    
    def draw_ellipse(self, x, y, width, height):
        """
        Adds an ellipse centered at given position and fitting into the size.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            width: int or float
                Full width of the ellipse.
            
            height: int or float
                Full height of the ellipse.
        """
        
        # apply scaling and offset
        x = self._scale * (x + self._offset[0])
        y = self._scale * (y + self._offset[1])
        width = self._scale * width
        height = self._scale * height
        
        # check size
        if not width or not height:
            return
        
        # get scale and radius
        scale = float(width) / height
        radius = 0.5*height
        
        # init drawing
        self._dc.new_path()
        
        # draw
        self._dc.save()
        self._dc.scale(scale, 1)
        self._dc.arc(x/scale, y, radius, 0, 2*numpy.pi)
        self._dc.restore()
        
        # fill and stroke
        self._fill_and_stroke()
    
    
    def draw_line(self, x1, y1, x2, y2):
        """
        Draws a line between two points.
        
        Args:
            x1: int or float
                X-coordinate of the line start.
            
            y1: int or float
                Y-coordinate of the line start.
            
            x2: int or float
                X-coordinate of the line end.
            
            y2: int or float
                Y-coordinate of the line end.
        """
        
        # apply scaling and offset
        x1 = self._scale * (x1 + self._offset[0])
        y1 = self._scale * (y1 + self._offset[1])
        x2 = self._scale * (x2 + self._offset[0])
        y2 = self._scale * (y2 + self._offset[1])
        
        # init drawing
        self._dc.new_path()
        self._dc.move_to(x1, y1)
        
        # draw
        self._dc.line_to(x2, y2)
        
        # fill and stroke
        self._fill_and_stroke()
    
    
    def draw_lines(self, points):
        """
        Draws continuous open line using sequence of points.
        
        Args:
            points: ((float, float),)
                Sequence of x,y coordinates of the points.
        """
        
        # check points
        if len(points) < 2:
            return
        
        # apply scaling and offset
        points = (numpy.array(points) + self._offset) * numpy.array((self._scale, self._scale))
        
        # init drawing
        self._dc.new_path()
        self._dc.move_to(points[0][0], points[0][1])
        
        # draw
        for p in points[1:]:
            self._dc.line_to(p[0], p[1])
        
        # fill and stroke
        self._fill_and_stroke()
    
    
    def draw_path(self, path):
        """
        Draws given path using current pen and brush.
        
        Args:
            path: pero.Path
                Path to be drawn.
        """
        
        # apply scaling and offset
        matrix = Matrix()
        matrix.translate(self._offset[0], self._offset[1])
        matrix.scale(self._scale, self._scale)
        path = path.transformed(matrix)
        
        # set new fill rule
        fill_rule = self._dc.get_fill_rule()
        self._dc.set_fill_rule(CAIRO_FILL_RULE[path.fill_rule])
        
        # add path
        self._make_native_path(path)
        
        # fill and stroke
        self._fill_and_stroke()
        
        # set back fill rule
        self._dc.set_fill_rule(fill_rule)
    
    
    def draw_polygon(self, points):
        """
        Draws a closed polygon using sequence of points.
        
        Args:
            points: ((float, float),)
                Sequence of x,y coordinates of the points.
        """
        
        # check points
        if len(points) < 2:
            return
        
        # apply scaling and offset
        points = (numpy.array(points) + self._offset) * numpy.array((self._scale, self._scale))
        
        # init drawing
        self._dc.new_path()
        self._dc.move_to(points[0][0], points[0][1])
        
        # draw
        for p in points[1:]:
            self._dc.line_to(p[0], p[1])
        
        self._dc.close_path()
        
        # fill and stroke
        self._fill_and_stroke()
    
    
    def draw_rect(self, x, y, width, height, radius=None):
        """
        Draws a rectangle specified by given top left corner and size and
        optional round corners specified as a single value or individual value
        for each corners starting from top-left.
        
        Args:
            x: int or float
                X-coordinate of the top left corner.
            
            y: int or float
                Y-coordinate of the top left corner.
            
            width: int or float
                Full width of the rectangle.
            
            height: int or float
                Full height of the rectangle.
            
            radius: int, float, (int,int,int,int) or (float,float,float,float)
                Radius of curved corners.
        """
        
        # get radius
        if isinstance(radius, (int, float)) and radius != 0:
            radius = (radius, radius, radius, radius)
        
        # draw as path if having round corners
        if radius:
            path = Path()
            path.rect(x, y, width, height, radius)
            self.draw_path(path)
            return
        
        # apply scaling and offset
        x = self._scale * (x + self._offset[0])
        y = self._scale * (y + self._offset[1])
        width = self._scale * width
        height = self._scale * height
        
        # init drawing
        self._dc.new_path()
        
        # draw
        self._dc.rectangle(x, y, width, height)
        
        # fill and stroke
        self._fill_and_stroke()
    
    
    def draw_text(self, text, x, y, angle=0):
        """
        Draws a text string anchored at specified point using current text
        settings.
        
        Args:
            text: str
                Text to be drawn.
            
            x: int or float
                X-coordinate of the text anchor.
            
            y: int or float
                Y-coordinate of the text anchor.
            
            angle: int or float
                Text angle in radians.
        """
        
        # set color
        self._dc.set_source_rgba(*self._font['for_color'])
        
        # get full size
        full_width, full_height = self.get_text_size(text)
        
        # get font size
        ascent, descent, font_height, max_x_advance, max_y_advance = self._dc.font_extents()
        font_height /= self._scale
        
        # apply angle transformation
        if angle:
            
            x = self._scale * (x + self._offset[0])
            y = self._scale * (y + self._offset[1])
            
            self._dc.save()
            self._dc.translate(x, y)
            self._dc.rotate(angle)
            
            x = 0
            y = 0
        
        # split lines
        lines = [text]
        if self.text_split and self.text_splitter:
            lines = text.split(self.text_splitter)
        
        # draw lines
        for i, line in enumerate(lines):
            
            # get line size
            x_bearing, y_bearing, line_width, line_height, x_advance, y_advance = self._dc.text_extents(line)
            line_width /= self._scale
            line_height /= self._scale
            
            # init offset
            x_offset = -x_bearing / self._scale
            y_offset = ascent / self._scale
            
            # adjust alignment
            if self.text_align == TEXT_ALIGN_CENTER:
                x_offset -= 0.5*line_width
            
            elif self.text_align == TEXT_ALIGN_RIGHT:
                x_offset -= line_width
            
            # adjust baseline
            if self.text_base == TEXT_BASE_MIDDLE:
                y_offset -= 0.5*full_height
            
            elif self.text_base == TEXT_BASE_BOTTOM:
                y_offset -= full_height
            
            # add line offset
            y_offset += i * font_height * (1 + self.text_spacing)
            
            # apply scaling and offset
            if angle:
                line_x = self._scale * x_offset
                line_y = self._scale * y_offset
            else:
                line_x = self._scale * (x + x_offset + self._offset[0])
                line_y = self._scale * (y + y_offset + self._offset[1])
            
            # draw background
            if self._font['bgr_color']:
                
                bgr_x = line_x + x_bearing
                bgr_y = line_y - ascent
                bgr_width = line_width * self._scale
                bgr_height = font_height * self._scale
                
                self._dc.set_source_rgba(*self._font['bgr_color'])
                self._dc.rectangle(bgr_x, bgr_y, bgr_width, bgr_height)
                self._dc.fill()
                self._dc.set_source_rgba(*self._font['for_color'])
            
            # draw text
            self._dc.move_to(line_x, line_y)
            self._dc.show_text(line)
        
        # revert angle transformation
        if angle:
            self._dc.restore()
    
    
    def clip(self, path):
        """
        Sets clipping path as intersection with current one.
        
        Args:
            path: pero.Path
                Path to be used for clipping.
        
        Returns:
            pero.ClipState
                Clipping state context manager.
        """
        
        # apply scaling and offset
        matrix = Matrix()
        matrix.translate(self._offset[0], self._offset[1])
        matrix.scale(self._scale, self._scale)
        path = path.transformed(matrix)
        
        # save current canvas state
        self._dc.save()
        
        # add path
        self._make_native_path(path)
        
        # set as clipping
        self._dc.clip()
        
        # return state
        return ClipState(self)
    
    
    def unclip(self):
        """Removes last clipping path while keeping previous if any."""
        
        # restore canvas state
        self._dc.restore()
        
        # set pen, brush and text
        self._update_pen()
        self._update_brush()
        self._update_text()
    
    
    def _make_native_path(self, path):
        """Adds given path to canvas without drawing it."""
        
        # init path
        self._dc.new_path()
        
        # draw
        for command in path.commands():
            
            # get data
            key = command[0]
            values = command[1:]
            
            # close
            if key == PATH_CLOSE:
                self._dc.close_path()
            
            # move to
            elif key == PATH_MOVE:
                self._dc.move_to(*values)
            
            # line to
            elif key == PATH_LINE:
                self._dc.line_to(*values)
            
            # curve to
            elif key == PATH_CURVE:
                self._dc.curve_to(*values)
    
    
    def _fill_and_stroke(self):
        """Fills and strokes current path."""
        
        # fill and stroke
        if self._pen and self._brush:
            
            self._dc.set_source_rgba(*self._brush)
            self._dc.fill_preserve()
            
            self._dc.set_source_rgba(*self._pen)
            self._dc.stroke()
        
        # stroke only
        elif self._pen:
            
            self._dc.set_source_rgba(*self._pen)
            self._dc.stroke()
        
        # fill only
        elif self._brush:
            
            self._dc.set_source_rgba(*self._brush)
            self._dc.fill()
    
    
    def _update_pen(self, evt=None):
        """Updates pen with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('line_color', 'line_alpha'):
            color = ColorProperties.get_color(self, "line_")
            if color is not UNDEF:
                self._pen = color.rgba_r if color.alpha else None
        
        # update width
        if prop_name is None or prop_name in ('line_width', 'line_scale'):
            line_width = self.line_width
            if line_width is not UNDEF:
                self._dc.set_line_width(line_width * self.line_scale)
        
        # update cap
        if prop_name is None or prop_name == 'line_cap':
            line_cap = self.line_cap
            if line_cap is not UNDEF:
                self._dc.set_line_cap(CAIRO_LINE_CAP[line_cap])
        
        # update join
        if prop_name is None or prop_name == 'line_join':
            line_join = self.line_join
            if line_join is not UNDEF:
                self._dc.set_line_join(CAIRO_LINE_JOIN[line_join])
        
        # update style/dash
        if prop_name is None or prop_name in ('line_dash', 'line_style', 'line_width', 'line_scale'):
            line_style = self.line_style
            line_dash = self.line_dash if self.line_dash else []
            line_width = self._dc.get_line_width()
            
            if line_style == LINE_STYLE_SOLID:
                line_dash = []
            elif line_style not in (LINE_STYLE_CUSTOM, UNDEF):
                line_dash = CAIRO_LINE_STYLE[line_style]
            
            self._dc.set_dash([x*line_width for x in line_dash])
    
    
    def _update_brush(self, evt=None):
        """Updates brush with current properties."""
        
        color = ColorProperties.get_color(self, "fill_")
        
        if self.fill_style == FILL_STYLE_TRANS:
            self._brush = None
        
        elif color is not UNDEF:
            self._brush = color.rgba_r if color.alpha else None
    
    
    def _update_text(self, evt=None):
        """Updates text with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # init flag
        init_font = False
        
        # update font name/family
        if prop_name is None or prop_name in ('font_name', 'font_family'):
            font_name = self.font_name
            font_family = self.font_family
            
            if font_name:
                self._font['family'] = font_name
            elif font_family is None:
                self._font['family'] = self._default_font.get_family()
            elif font_family is not UNDEF:
                self._font['family'] = CAIRO_FONT_FAMILY[font_family]
            
            init_font = True
        
        # update font size
        if prop_name is None or prop_name in ('font_size', 'font_scale'):
            font_size = self.font_size
            
            if font_size is None:
                self._dc.set_font_size(11 * self.font_scale)
            elif font_size is not UNDEF:
                self._dc.set_font_size(font_size * self.font_scale)
        
        # update font style
        if prop_name is None or prop_name == 'font_style':
            font_style = self.font_style
            
            if font_style is None:
                self._font['style'] = self._default_font.get_slant()
            elif font_style is not UNDEF:
                self._font['style'] = CAIRO_FONT_STYLE[font_style]
            
            init_font = True
        
        # update font weight
        if prop_name is None or prop_name == 'font_weight':
            font_weight = self.font_weight
            
            if font_weight is None:
                self._font['weight'] = self._default_font.get_weight()
            elif font_weight is not UNDEF:
                self._font['weight'] = CAIRO_FONT_WEIGHT[font_weight]
            
            init_font = True
        
        # update foreground color
        if prop_name is None or prop_name in ('text_color', 'text_alpha'):
            color = ColorProperties.get_color(self, "text_")
            if color is not UNDEF:
                self._font['for_color'] = color.rgba_r
        
        # update background color
        if prop_name is None or prop_name in ('text_bgr_color', 'text_bgr_alpha'):
            color = ColorProperties.get_color(self, "text_bgr_")
            if color is not UNDEF:
                self._font['bgr_color'] = color.rgba_r if color.alpha else None
        
        # set_font
        if init_font:
            self._dc.select_font_face(
                self._font['family'],
                self._font['style'],
                self._font['weight'])
