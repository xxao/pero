#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import py5
import numpy
from ... properties import *
from ... drawing import Canvas, Path, Matrix
from . enums import *


class Py5Canvas(Canvas):
    """Wrapper for Py5 drawing graphics."""
    
    
    def __init__(self, pg, **overrides):
        """
        Initializes a new instance of Py5Canvas.
        
        Args:
            pg: py5.Py5Graphics
                Sketch object to draw into.
            
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        # init buffers
        self._pg = pg
        
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
            origin = (0, 0)
            
            # draw path
            for command in sub.commands():
                
                # get data
                key = command[0]
                values = command[1:]
                
                # close
                if key == PATH_CLOSE:
                    self._pg.vertex(*origin)
                
                # move to
                elif key == PATH_MOVE:
                    self._pg.vertex(*values[0:2])
                    origin = values[0:2]
                
                # line to
                elif key == PATH_LINE:
                    self._pg.vertex(*values[0:2])
                
                # curve to
                elif key == PATH_CURVE:
                    self._pg.bezier_vertex(*values)
            
            # end shape
            self._pg.end_shape()
    
    
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
        
        pass
    
    
    def _update_pen(self, evt=None):
        """Updates pen with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('line_color', 'line_alpha'):
            color = ColorProperties.get_color(self, "line_")
            if color is not UNDEF:
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
        
        color = ColorProperties.get_color(self, "fill_")
        
        if self.fill_style == FILL_STYLE_TRANS:
            self._pg.no_fill()
        
        elif color is not UNDEF:
            self._pg.fill(color.hex)
    
    
    def _update_text(self, evt=None):
        """Updates text with current properties."""
        
        pass
