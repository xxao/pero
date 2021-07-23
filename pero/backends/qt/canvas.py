#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from PyQt5.QtCore import QPoint, QLineF
from PyQt5.QtGui import QColor, QPen, QBrush, QPainterPath, QFontMetrics
from ... properties import *
from ... drawing import Canvas, Path, Matrix, ClipState
from . enums import *


class QtCanvas(Canvas):
    """Wrapper for PyQt drawing context."""
    
    
    def __init__(self, dc, **overrides):
        """
        Initializes a new instance of WXCanvas.
        
        Args:
            dc: QPainter
                PyQt drawing context.
            
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        # init buffers
        self._dc = dc
        
        self._pen = self._dc.pen()
        self._brush = self._dc.brush()
        self._default_font = self._dc.font()
        self._font_metrics = QFontMetrics(self._default_font)
        self._for_color = None
        self._bgr_color = None
        
        # init size
        rect = self._dc.viewport()
        
        if 'width' not in overrides:
            overrides['width'] = rect.width()
        
        if 'height' not in overrides:
            overrides['height'] = rect.height()
        
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
        size = self._font_metrics.boundingRect(text)
        
        return size.width(), size.height()
    
    
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
        
        self.draw_ellipse(x, y, 2*radius, 2*radius)
    
    
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
        
        # draw
        self._dc.drawEllipse(x-0.5*width, y-0.5*height, width, height)
    
    
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
        self._dc.drawLine(x1, y1, x2, y2)
    
    
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
        
        # get lines
        lines = []
        for i in range(0, len(points)-1):
            lines.append(QLineF(points[i][0], points[i][1], points[i+1][0], points[i+1][1]))
        
        # draw
        self._dc.drawLines(*lines)
    
    
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
        
        # make qt path
        qt_path = self._make_native_path(path)
        
        # draw path
        self._dc.drawPath(qt_path)
    
    
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
        self._dc.drawPolygon(*(QPoint(*p) for p in points))
    
    
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
        width = self._scale * width + .5
        height = self._scale * height + .5
        
        # no round corners
        if not radius:
            self._dc.drawRect(x, y, width, height)
        
        # same radius for all corners
        else:
            radius = self._scale * radius[0]
            self._dc.drawRoundedRect(x, y, width, height, radius, radius)
    
    
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
        ori_pen = self._dc.pen()
        ori_brush = self._dc.brush()
        
        if self._for_color is not None:
            self._dc.setPen(self._for_color)
        
        if self._bgr_color is not None:
            self._dc.setBrush(self._bgr_color)
        
        # get full size
        full_width, full_height = self.get_text_size(text)
        
        # apply angle transformation
        if angle:
            
            x = self._scale * (x + self._offset[0])
            y = self._scale * (y + self._offset[1])
            
            self._dc.save()
            self._dc.translate(x, y)
            self._dc.rotate(numpy.rad2deg(angle))
            
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
            ascent = self._font_metrics.ascent()
            
            # init offset
            x_offset = 0
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
            y_offset += i * line_height * (1 + self.text_spacing)
            
            # apply scaling and offset
            if angle:
                line_x = self._scale * x_offset
                line_y = self._scale * y_offset
            else:
                line_x = self._scale * (x + x_offset + self._offset[0])
                line_y = self._scale * (y + y_offset + self._offset[1])
            
            # draw background
            if self._bgr_color is not None:
                
                bgr_x = line_x
                bgr_y = line_y - ascent
                bgr_width = line_width * self._scale
                bgr_height = line_height * self._scale
                
                self._dc.setPen(Qt.NoPen)
                self._dc.drawRect(bgr_x, bgr_y, bgr_width, bgr_height)
                
                if self._for_color is not None:
                    self._dc.setPen(self._for_color)
            
            # draw text
            self._dc.drawText(line_x, line_y, line)
        
        # revert angle transformation
        if angle:
            self._dc.restore()
        
        # revert colors
        self._dc.setPen(ori_pen)
        self._dc.setBrush(ori_brush)
    
    
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
        qt_path = self._make_native_path(path)
        
        # set as clipping
        self._dc.setClipPath(qt_path, Qt.IntersectClip)
        
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
        """Converts given path to native path."""
        
        # init path
        qt_path = QPainterPath()
        qt_path.setFillRule(QT_FILL_RULE[path.fill_rule])
        
        # apply commands
        for command in path.commands():
            
            # get data
            key = command[0]
            values = command[1:]
            
            # close
            if key == PATH_CLOSE:
                qt_path.closeSubpath()
            
            # move to
            elif key == PATH_MOVE:
                qt_path.moveTo(*values)
            
            # line to
            elif key == PATH_LINE:
                qt_path.lineTo(*values)
            
            # curve to
            elif key == PATH_CURVE:
                qt_path.cubicTo(*values)
        
        return qt_path
    
    
    def _update_pen(self, evt=None):
        """Updates pen with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('line_color', 'line_alpha'):
            color = ColorProperties.get_color(self, "line_")
            if color is not UNDEF:
                self._pen.setColor(QColor(*color.rgba))
        
        # update width
        if prop_name is None or prop_name in ('line_width', 'line_scale'):
            line_width = self.line_width
            if line_width is not UNDEF:
                self._pen.setWidth(line_width * self.line_scale)
        
        # update cap
        if prop_name is None or prop_name == 'line_cap':
            line_cap = self.line_cap
            if line_cap is not UNDEF:
                self._pen.setCapStyle(QT_LINE_CAP[line_cap])
        
        # update join
        if prop_name is None or prop_name == 'line_join':
            line_join = self.line_join
            if line_join is not UNDEF:
                self._pen.setJoinStyle(QT_LINE_JOIN[line_join])
        
        # update style/dash
        if prop_name is None or prop_name in ('line_dash', 'line_style'):
            line_style = self.line_style
            line_dash = self.line_dash if self.line_dash else []
            
            if line_style == LINE_STYLE_SOLID:
                self._pen.setStyle(QT_LINE_STYLE[line_style])
                line_dash = []
            elif line_style == LINE_STYLE_CUSTOM:
                self._pen.setStyle(QT_LINE_STYLE[line_style])
            elif line_style is not UNDEF:
                self._pen.setStyle(QT_LINE_STYLE[LINE_STYLE_CUSTOM])
                line_dash = QT_LINE_STYLE[line_style]
            
            self._pen.setDashPattern(line_dash)
        
        # set pen
        if self._pen.width() == 0:
            self._dc.setPen(Qt.NoPen)
        else:
            self._dc.setPen(self._pen)
    
    
    def _update_brush(self, evt=None):
        """Updates brush with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('fill_color', 'fill_alpha'):
            color = ColorProperties.get_color(self, "fill_")
            if color is not UNDEF:
                self._brush.setColor(QColor(*color.rgba))
        
        # update style
        if prop_name is None or prop_name == 'fill_style':
            fill_style = self.fill_style
            if fill_style is not UNDEF:
                self._brush.setStyle(QT_FILL_STYLE[fill_style])
        
        # set back
        self._dc.setBrush(self._brush)
    
    
    def _update_text(self, evt=None):
        """Updates text with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # get current font
        font = self._dc.font()
        
        # update font name
        if prop_name is None or prop_name == 'font_name':
            font_name = self.font_name
            if font_name is None:
                font.setFamily(self._default_font.family())
            elif font_name is not UNDEF:
                font.setFamily(font_name)
        
        # update font family
        if prop_name is None or prop_name == 'font_family':
            font_family = self.font_family
            if font_family is None:
                font.setFamily(self._default_font.family())
            elif font_family is not UNDEF:
                font.setFamily(QT_FONT_FAMILY[font_family])
        
        # update font size
        if prop_name is None or prop_name in ('font_size', 'font_scale'):
            font_size = self.font_size
            if font_size is None:
                font.setPointSize(self._default_font.pointSize() * self.font_scale)
            elif font_size is not UNDEF:
                font.setPointSize(font_size * self.font_scale)
        
        # update font style
        if prop_name is None or prop_name == 'font_style':
            font_style = self.font_style
            if font_style is None:
                font.setItalic(False)
            elif font_style is not UNDEF:
                font.setItalic(QT_FONT_STYLE[font_style])
        
        # update font weight
        if prop_name is None or prop_name == 'font_weight':
            font_weight = self.font_weight
            if font_weight is None:
                font.setWeight(self._default_font.weight())
            elif font_weight is not UNDEF:
                font.setWeight(QT_FONT_WEIGHT[font_weight])
        
        # update foreground color
        if prop_name is None or prop_name in ('text_color', 'text_alpha'):
            color = ColorProperties.get_color(self, "text_")
            self._for_color = QPen(QColor(*color.rgba)) if color.alpha else None
        
        # update background color
        if prop_name is None or prop_name in ('text_bgr_color', 'text_bgr_alpha'):
            color = ColorProperties.get_color(self, "text_bgr_")
            self._bgr_color = QBrush(QColor(*color.rgba)) if color.alpha else None
        
        # set font
        self._dc.setFont(font)
        self._font_metrics = QFontMetrics(font)
