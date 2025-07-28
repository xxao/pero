#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import py5
import numpy
from ... properties import *
from ... colors import Transparent, Black
from ... drawing import Canvas, Path, Matrix, ClipState
from . enums import *


class Py5Canvas(Canvas):
    """Wrapper for Py5 drawing graphics."""
    
    
    def __init__(self, pg, context=py5, **overrides):
        """
        Initializes a new instance of Py5Canvas.
        
        Args:
            pg: py5.Py5Graphics
                Sketch object to draw into.
            
            context: py5 module or py5.Sketch
                Context in which the drawing is done.
            
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        # init buffers
        self._pg = pg
        self._context = context
        self._clipping = []
        
        self._line_color = None
        self._fill_color = None
        self._for_color = Black
        self._bgr_color = None
        
        # init size
        if 'width' not in overrides:
            overrides['width'] = pg.width
        
        if 'height' not in overrides:
            overrides['height'] = pg.height
        
        # init base
        super().__init__(**overrides)
        
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
        width = self._pg.text_width(text)
        height = self._pg.text_ascent() + self._pg.text_descent()
        
        return width, height
    
    
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
        
        # draw circle
        self._pg.ellipse_mode(py5.CENTER)
        self._pg.circle(x, y, 2*radius)
    
    
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
        
        # draw ellipse
        self._pg.ellipse_mode(py5.CENTER)
        self._pg.ellipse(x, y, width, height)
    
    
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
        
        # draw line
        self._pg.line(x1, y1, x2, y2)
    
    
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
        
        # create coords
        points = numpy.concatenate((points[:-1], points[1:]), axis=1)
        
        # draw lines
        self._pg.lines(points)
    
    
    def draw_path(self, path):
        """
        Draws the path using current pen and brush.
        
        Args:
            path: pero.Path
                Path to be drawn.
        """
        
        # apply scaling and offset
        matrix = Matrix()
        matrix.translate(self._offset[0], self._offset[1])
        matrix.scale(self._scale, self._scale)
        path = path.transformed(matrix)
        
        # draw individual sub-paths
        for sub in path.split():
            
            # begin shape
            self._pg.begin_shape()
            end = py5.OPEN
            
            # draw path
            for command in sub.commands():
                
                # get data
                key = command[0]
                values = command[1:]
                
                # close
                if key == PATH_CLOSE:
                    end = py5.CLOSE
                
                # move to
                elif key == PATH_MOVE:
                    self._pg.vertex(*values[0:2])
                
                # line to
                elif key == PATH_LINE:
                    self._pg.vertex(*values[0:2])
                
                # curve to
                elif key == PATH_CURVE:
                    self._pg.bezier_vertex(*values)
            
            # end shape
            self._pg.end_shape(end)
    
    
    def draw_rect(self, x, y, width, height, radius=None):
        """
        Draws a rectangle specified by given top left corner and size and
        optional round corners specified as a single value or individual value
        for each corner starting from top-left.
        
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
        
        # draw rect
        self._pg.rect_mode(py5.CORNER)
        self._pg.rect(x, y, width, height)
    
    
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
        
        # set colors
        self._pg.no_stroke()
        if self._for_color:
            self._pg.fill(self._for_color.hex)
        
        # get full size
        full_width, full_height = self.get_text_size(text)
        
        # apply angle transformation
        if angle:
            
            shift_x = self._scale * (x + self._offset[0])
            shift_y = self._scale * (y + self._offset[1])
            
            self._pg.translate(shift_x, shift_y)
            self._pg.rotate(angle)
            
            x = 0
            y = 0
        
        # split lines
        lines = [text]
        if self.text_split and self.text_splitter:
            lines = text.split(self.text_splitter)
        
        # draw lines
        for i, line in enumerate(lines):
            
            # get line size
            line_width, line_height = self.get_line_size(line)
            line_width /= self._scale
            line_height /= self._scale
            
            # init offset
            x_offset = 0
            y_offset = 0
            
            # adjust alignment
            if self.text_align == TEXT_ALIGN_CENTER:
                x_offset -= 0.5 * line_width
            
            elif self.text_align == TEXT_ALIGN_RIGHT:
                x_offset -= line_width
            
            # adjust baseline
            if self.text_base == TEXT_BASE_MIDDLE:
                y_offset -= 0.5 * full_height
            
            elif self.text_base == TEXT_BASE_BOTTOM:
                y_offset -= full_height
            
            # add line offset
            y_offset += i * line_height * (1 + self.text_spacing)
            
            # apply scaling and offset
            if angle:
                line_x = self._scale * x_offset
                line_y = self._scale * y_offset
            else:
                line_x = self._scale * (x + x_offset + self._offset[0])
                line_y = self._scale * (y + y_offset + self._offset[1])
            
            # draw background
            if self._bgr_color:
                
                bgr_x = line_x
                bgr_y = line_y
                bgr_width = line_width * self._scale
                bgr_height = line_height * self._scale
                
                self._pg.fill(self._bgr_color.hex)
                self._pg.rect(bgr_x, bgr_y, bgr_width, bgr_height)
                
                if self._for_color:
                    self._pg.fill(self._for_color.hex)
            
            # draw text
            self._pg.text_align(py5.LEFT, py5.TOP)
            self._pg.text(line, line_x, line_y)
        
        # revert colors
        if self._line_color:
            self._pg.stroke(self._line_color.hex)
        
        if self._fill_color:
            self._pg.fill(self._fill_color.hex)
        
        # revert angle transformation
        if angle:
            self._pg.rotate(-angle)
            self._pg.translate(-shift_x, -shift_y)
    
    
    def clip(self, path):
        """
        Sets clipping path as intersection with current one.
        
        Current implementation does not truly support paths so it uses just the
        rectangular bounding box of the given path.
        
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
        
        # set clipping
        rect = path.bbox().rect
        self._pg.image_mode(py5.CORNER)
        self._pg.clip(*rect)
        
        # remember clipping
        self._clipping.append(rect)
        
        # return state
        return ClipState(self)
    
    
    def unclip(self):
        """Removes last clipping path while keeping previous if any."""
        
        # remove clip
        self._pg.no_clip()
        
        # remove from stack
        if self._clipping:
            del self._clipping[-1]
        
        # re-apply previous
        if self._clipping:
            self._pg.image_mode(py5.CORNER)
            self._pg.clip(*self._clipping[-1])
    
    
    def _update_pen(self, evt=None):
        """Updates pen with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('line_color', 'line_alpha'):
            color = ColorProperties.get_color(self, "line_")
            if color is not UNDEF:
                self._line_color = color
                self._pg.stroke(color.hex)
        
        # update width
        if prop_name is None or prop_name in ('line_width', 'line_scale'):
            line_width = self.line_width
            if line_width is not UNDEF:
                self._pg.stroke_weight(line_width)
        
        # update cap
        if prop_name is None or prop_name == 'line_cap':
            line_cap = self.line_cap
            if line_cap is not UNDEF:
                self._pg.stroke_cap(PY5_LINE_CAP[line_cap])
        
        # update join
        if prop_name is None or prop_name == 'line_join':
            line_join = self.line_join
            if line_join is not UNDEF:
                self._pg.stroke_join(PY5_LINE_JOIN[line_join])
    
    
    def _update_brush(self, evt=None):
        """Updates brush with current properties."""
        
        # get color
        color = ColorProperties.get_color(self, "fill_")
        
        # set transparent fill
        if self.fill_style == FILL_STYLE_TRANS:
            self._fill_color = Transparent
            self._pg.fill(self._fill_color.hex)
        
        # set color fill
        elif color is not UNDEF:
            self._fill_color = color
            self._pg.fill(self._fill_color.hex)
    
    
    def _update_text(self, evt=None):
        """Updates text with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update font
        if prop_name is None or prop_name in ('font_name', 'font_family', 'font_style', 'font_weight'):
            font_size = self.font_size or 10
            font = self.get_font()
            font = self._context.create_font(font.path, font_size * self.font_scale)
            self._pg.text_font(font)
        
        # update font size
        if prop_name is None or prop_name in ('font_size', 'font_scale'):
            font_size = self.font_size
            if font_size is not UNDEF:
                self._pg.text_size(font_size * self.font_scale)
        
        # update foreground color
        if prop_name is None or prop_name in ('text_color', 'text_alpha'):
            color = ColorProperties.get_color(self, "text_")
            if color is not UNDEF:
                self._for_color = color
        
        # update background color
        if prop_name is None or prop_name in ('text_bgr_color', 'text_bgr_alpha'):
            color = ColorProperties.get_color(self, "text_bgr_")
            if color is not UNDEF:
                self._bgr_color = color
