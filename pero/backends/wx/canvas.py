#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import wx
from ... properties import *
from ... colors import Transparent
from ... drawing import Canvas, Path, Matrix, ClipState
from . enums import *


class WXCanvas(Canvas):
    """Wrapper for wxPython drawing context."""
    
    
    def __init__(self, dc, **overrides):
        """
        Initializes a new instance of WXCanvas.
        
        Args:
            dc: wx.GraphicsContext
                wxPython drawing context.
            
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        # init buffers
        self._dc = dc
        self._clipping = []
        
        self._pen = self._dc.GetPen()
        self._brush = self._dc.GetBrush()
        self._default_font = self._dc.GetFont()
        
        # set font factor
        self._font_factor = 1.
        if sys.platform == 'win32':
            self._font_factor = 0.75
        
        # init size
        width, height = self._dc.GetSize()
        
        if 'width' not in overrides:
            overrides['width'] = width
        
        if 'height' not in overrides:
            overrides['height'] = height
        
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
        return self._dc.GetTextExtent(text)
    
    
    def draw_arc(self, x, y, radius, start_angle, end_angle, clockwise=True):
        """
        Draws an arc of specified radius centered on given coordinates.
        
        Args:
            x: int or float
                X-coordinate of the arc center.
            
            y: int or float
                Y-coordinate of the arc center.
            
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
        
        # make path
        gc = self._get_gc(self._dc)
        path = gc.CreatePath()
        
        # draw
        path.AddArc(x, y, radius, start_angle, end_angle, clockwise)
        gc.DrawPath(path)
    
    
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
        
        # draw
        self._dc.DrawCircle(x, y, radius)
    
    
    def draw_ellipse(self, x, y, width, height):
        """
        Draws an ellipse centered around given coordinates and fitting into the
        width and height.
        
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
        
        # make path
        gc = self._get_gc(self._dc)
        path = gc.CreatePath()
        
        # draw
        path.AddEllipse(x-0.5*width, y-0.5*height, width, height)
        gc.DrawPath(path)
    
    
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
        
        # draw
        self._dc.DrawLine(x1, y1, x2, y2)
    
    
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
        
        # draw
        self._dc.DrawLines(points)
    
    
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
        
        # make wx path
        gc = self._get_gc(self._dc)
        wx_path = self._make_native_path(path, gc)
        
        # draw path
        gc.DrawPath(wx_path, fillStyle=WX_FILL_RULE[path.fill_rule])
    
    
    def draw_polygon(self, points):
        """
        Draws a closed polygon using sequence of points.
        
        Args:
            points: ((float, float),)
                Sequence of x,y coordinates of the points.
        """
        
        # check points
        if len(points) < 3:
            return
        
        # apply scaling and offset
        points = (numpy.array(points) + self._offset) * numpy.array((self._scale, self._scale))
        
        # draw
        self._dc.DrawPolygon(points)
    
    
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
        
        # draw as path if different corners
        if radius and not all(r == radius[0] for r in radius):
            path = Path()
            path.rect(x, y, width, height, radius)
            self.draw_path(path)
            return
        
        # apply scaling and offset
        x = self._scale * (x + self._offset[0])
        y = self._scale * (y + self._offset[1])
        width = self._scale * width + 1
        height = self._scale * height + 1
        
        # no round corners
        if not radius:
            self._dc.DrawRectangle(x, y, width, height)
        
        # same radius for all corners
        else:
            radius = self._scale * radius[0]
            self._dc.DrawRoundedRectangle(x, y, width, height, radius)
    
    
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
        
        # get full size
        full_width, full_height = self.get_text_size(text)
        
        # split lines
        lines = [text]
        if self.text_split and self.text_splitter:
            lines = text.split(self.text_splitter)
        
        # get angle
        angle *= -1
        
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
                x_offset -= 0.5*line_width
            
            elif self.text_align == TEXT_ALIGN_RIGHT:
                x_offset -= line_width
            
            # adjust baseline
            if self.text_base == TEXT_BASE_MIDDLE:
                y_offset -= 0.5*full_height
            
            elif self.text_base == TEXT_BASE_BOTTOM:
                y_offset -= full_height
            
            # add line offset
            y_offset += i * line_height * (1 + self.text_spacing)
            
            # apply angle
            if angle:
                x_shift = x_offset * numpy.cos(angle) + y_offset * numpy.sin(angle)
                y_shift = -x_offset * numpy.sin(angle) + y_offset * numpy.cos(angle)
                x_offset = x_shift
                y_offset = y_shift
            
            # apply scaling and offset
            text_x = self._scale * (x + x_offset + self._offset[0])
            text_y = self._scale * (y + y_offset + self._offset[1])
            
            # draw
            if angle:
                self._dc.DrawRotatedText(line, text_x, text_y, numpy.rad2deg(angle))
            else:
                self._dc.DrawText(line, text_x, text_y)
    
    
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
        self._dc.SetClippingRegion(*rect)
        
        # remember clipping
        self._clipping.append(rect)
        
        # return state
        return ClipState(self)
    
    
    def unclip(self):
        """Removes last clipping path while keeping previous if any."""
        
        # remove clip
        self._dc.DestroyClippingRegion()
        
        # remove from stack
        if self._clipping:
            del self._clipping[-1]
        
        # re-apply previous
        if self._clipping:
            self._dc.SetClippingRegion(*self._clipping[-1])
    
    
    def _get_gc(self, dc):
        """Gets or creates GC from given DC."""
        
        # for mac
        if 'wxMac' in wx.PlatformInfo:
            gc = wx.GraphicsContext.Create(dc)
            gc.SetPen(dc.GetPen())
            gc.SetBrush(dc.GetBrush())
            return gc
        
        # for win
        else:
            return dc.GetGraphicsContext()
    
    
    def _make_native_path(self, path, gc):
        """Converts given path to native path."""

        # init path
        wx_path = gc.CreatePath()
        
        # apply commands
        for command in path.commands():
            
            # get data
            key = command[0]
            values = command[1:]
            
            # close
            if key == PATH_CLOSE:
                wx_path.CloseSubpath()
            
            # move to
            elif key == PATH_MOVE:
                wx_path.MoveToPoint(*values)
            
            # line to
            elif key == PATH_LINE:
                wx_path.AddLineToPoint(*values)
            
            # curve to
            elif key == PATH_CURVE:
                wx_path.AddCurveToPoint(*values)
        
        return wx_path
    
    
    def _update_pen(self, evt=None):
        """Updates pen with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('line_color', 'line_alpha'):
            color = ColorProperties.get_color(self, "line_")
            if color is not UNDEF:
                self._pen.Colour = color.rgba
        
        # update width
        if prop_name is None or prop_name in ('line_width', 'line_scale'):
            line_width = self.line_width
            if line_width is not UNDEF:
                self._pen.Width = line_width * self.line_scale
        
        # update cap
        if prop_name is None or prop_name == 'line_cap':
            line_cap = self.line_cap
            if line_cap is not UNDEF:
                self._pen.Cap = WX_LINE_CAP[line_cap]
        
        # update join
        if prop_name is None or prop_name == 'line_join':
            line_join = self.line_join
            if line_join is not UNDEF:
                self._pen.Join = WX_LINE_JOIN[line_join]
        
        # update style/dash
        if prop_name is None or prop_name in ('line_dash', 'line_style'):
            line_style = self.line_style
            line_dash = self.line_dash if self.line_dash else []
            
            if line_style == LINE_STYLE_SOLID:
                self._pen.Style = WX_LINE_STYLE[line_style]
                line_dash = []
            elif line_style == LINE_STYLE_CUSTOM:
                self._pen.Style = WX_LINE_STYLE[line_style]
            elif line_style is not UNDEF:
                self._pen.Style = WX_LINE_STYLE[LINE_STYLE_CUSTOM]
                line_dash = WX_LINE_STYLE[line_style]
            
            self._pen.Dashes = line_dash
        
        # set pen
        if self._pen.Width == 0:
            self._dc.SetPen(wx.TRANSPARENT_PEN)
        else:
            self._dc.SetPen(self._pen)
    
    
    def _update_brush(self, evt=None):
        """Updates brush with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('fill_color', 'fill_alpha'):
            color = ColorProperties.get_color(self, "fill_")
            if color is not UNDEF:
                self._brush.Colour = color.rgba
        
        # update style
        if prop_name is None or prop_name == 'fill_style':
            fill_style = self.fill_style
            if fill_style is not UNDEF:
                self._brush.Style = WX_FILL_STYLE[fill_style]
        
        # set back
        self._dc.SetBrush(self._brush)
    
    
    def _update_text(self, evt=None):
        """Updates text with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # get current font
        font = self._dc.GetFont()
        
        # update font name
        if prop_name is None or prop_name == 'font_name':
            font_name = self.font_name
            if font_name is None:
                font.FaceName = ""  # self._default_font.FaceName
            elif font_name is not UNDEF:
                font.FaceName = font_name
        
        # update font family
        if prop_name is None or prop_name == 'font_family':
            font_family = self.font_family
            if font_family is None:
                font.Family = self._default_font.Family
            elif font_family is not UNDEF:
                font.Family = WX_FONT_FAMILY[font_family]
        
        # update font size
        if prop_name is None or prop_name in ('font_size', 'font_scale'):
            font_size = self.font_size
            if font_size is None:
                font.PointSize = self._default_font.PointSize * self.font_scale * self._font_factor
            elif font_size is not UNDEF:
                font.PointSize = font_size * self.font_scale * self._font_factor
        
        # update font style
        if prop_name is None or prop_name == 'font_style':
            font_style = self.font_style
            if font_style is None:
                font.Style = self._default_font.Style
            elif font_style is not UNDEF:
                font.Style = WX_FONT_STYLE[font_style]
        
        # update font weight
        if prop_name is None or prop_name == 'font_weight':
            font_weight = self.font_weight
            if font_weight is None:
                font.Weight = self._default_font.Weight
            elif font_weight is not UNDEF:
                font.Weight = WX_FONT_WEIGHT[font_weight]
        
        # update foreground color
        if prop_name is None or prop_name in ('text_color', 'text_alpha'):
            color = ColorProperties.get_color(self, "text_")
            self._dc.SetTextForeground(color.rgba if color else None)
        
        # update background color
        if prop_name is None or prop_name in ('text_bgr_color', 'text_bgr_alpha'):
            color = ColorProperties.get_color(self, "text_bgr_")
            if color is Transparent:
                self._dc.SetBackgroundMode(wx.TRANSPARENT)
            elif color is not UNDEF:
                self._dc.SetTextBackground(color.rgba)
                self._dc.SetBackgroundMode(wx.SOLID)
        
        # set font
        self._dc.SetFont(font)
