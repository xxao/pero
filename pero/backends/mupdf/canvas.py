#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import fitz
import numpy
from ... properties import *
from ... drawing import Canvas, Path, Matrix
from . enums import *


class MuPDFCanvas(Canvas):
    """Wrapper for PyMuPDF document page."""
    
    
    def __init__(self, page, **overrides):
        """
        Initializes a new instance of MuPDFCanvas.
        
        Args:
            page: fritz.Page
                PyMuPDF document page.
            
            overrides: str:any pairs
                Value overwrites for specific properties.
        """
        
        # init buffers
        self._page = page
        
        self._pen = {
            'width': None,
            'color': (0, 0, 0),
            'cap': MUPDF_LINE_CAP[SQUARE],
            'join': MUPDF_LINE_JOIN[BEVEL],
            'dashes': "[]0"}
        
        self._brush = {
            'color': None}
        
        self._font = {
            'name': 'helvetica',
            'file': None,
            'size': 10,
            'descent': 0,
            'for_color': (0, 0, 0),
            'bgr_color': None}
        
        # init size
        rect = self._page.bound()
        
        if 'width' not in overrides:
            overrides['width'] = rect.width
        
        if 'height' not in overrides:
            overrides['height'] = rect.height
        
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
        
        # init shape
        shape = self._page.newShape()
        
        # draw
        shape.drawCircle((x, y), radius)
        
        # fill and stroke
        self._fill_and_stroke(shape, close=True)
    
    
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
        
        # init shape
        shape = self._page.newShape()
        
        # draw
        shape.drawOval((x-0.5*width, y-0.5*height, x+0.5*width, y+0.5*height))
        
        # fill and stroke
        self._fill_and_stroke(shape, close=True)
    
    
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
        
        # init shape
        shape = self._page.newShape()
        
        # draw
        shape.drawLine((x1, y1), (x2, y2))
        
        # fill and stroke
        self._fill_and_stroke(shape, close=False, fill=False)
    
    
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
        
        # init shape
        shape = self._page.newShape()
        
        # draw
        shape.drawPolyline(points)
        
        # fill and stroke
        self._fill_and_stroke(shape, close=False)
    
    
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
        
        # init shape
        shape = self._page.newShape()
        cursor = (0, 0)
        origin = (0, 0)
        
        # draw
        for command in path.commands():
            
            # get data
            key = command[0]
            values = command[1:]
            
            # close
            if key == PATH_CLOSE:
                shape.drawLine(cursor, origin)
                cursor = origin
            
            # move to
            elif key == PATH_MOVE:
                cursor = values[0:2]
                origin = cursor
            
            # line to
            elif key == PATH_LINE:
                shape.drawLine(cursor, values[0:2])
                cursor = values[0:2]
            
            # curve to
            elif key == PATH_CURVE:
                shape.drawBezier(cursor, values[0:2], values[2:4], values[4:6])
                cursor = values[4:6]
        
        # fill and stroke
        self._fill_and_stroke(shape, close=False, even_odd=MUPDF_FILL_RULE[path.fill_rule])
    
    
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
        
        # init shape
        shape = self._page.newShape()
        
        # draw
        shape.drawPolyline(points)
        
        # fill and stroke
        self._fill_and_stroke(shape, close=True)
    
    
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
        
        # init shape
        shape = self._page.newShape()
        
        # draw
        shape.drawRect((x, y, x+width, y+height))
        
        # fill and stroke
        self._fill_and_stroke(shape, close=True)
    
    
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
        
        # init shape
        shape = self._page.newShape()
        
        # get full size
        full_width, full_height = self.get_text_size(text)
        descent = self._font['descent'] / self._scale
        
        # get angle transformation
        text_morph = None
        bgr_morph = None
        
        if angle:
            angle *= -1
            
            matrix = fitz.Matrix(numpy.rad2deg(angle))
            text_morph = [None, matrix]
            bgr_morph = [None, matrix]
            
            sin = numpy.sin(angle)
            cos = numpy.cos(angle)
        
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
            y_offset = line_height - descent
            
            # adjust alignment
            if self.text_align == TEXT_ALIGN_CENTER:
                x_offset -= 0.5 * line_width
            
            elif self.text_align == TEXT_ALIGN_RIGHT:
                x_offset -= line_width
            
            # adjust baseline
            if self.text_base == TEXT_BASE_MIDDLE:
                y_offset -= 0.5*full_height
            
            elif self.text_base == TEXT_BASE_BOTTOM:
                y_offset -= full_height
            
            # add line offset
            y_offset += i * line_height * (1 + self.text_spacing)
            
            # init coords
            text_x = x_offset
            text_y = y_offset
            bgr_x = x_offset
            bgr_y = y_offset + descent
            
            # apply angle
            if angle:
                
                x_shift = text_x * cos + text_y * sin
                y_shift = -text_x * sin + text_y * cos
                text_x = x_shift
                text_y = y_shift
                
                x_shift = bgr_x * cos + bgr_y * sin
                y_shift = -bgr_x * sin + bgr_y * cos
                bgr_x = x_shift
                bgr_y = y_shift
            
            # apply scaling and offset
            text_x = self._scale * (x + text_x + self._offset[0])
            text_y = self._scale * (y + text_y + self._offset[1])
            
            bgr_x1 = self._scale * (x + bgr_x + self._offset[0])
            bgr_y2 = self._scale * (y + bgr_y + self._offset[1])
            bgr_x2 = bgr_x1 + line_width * self._scale
            bgr_y1 = bgr_y2 - line_height * self._scale
            
            # set angle pivot
            if angle:
                text_morph[0] = fitz.Point(text_x, text_y)
                bgr_morph[0] = fitz.Point(bgr_x1, bgr_y2)
            
            # draw background
            if self._font['bgr_color']:
                
                shape = self._page.newShape()
                shape.drawRect((bgr_x1, bgr_y1, bgr_x2, bgr_y2))
                
                shape.finish(
                    width = 0,
                    color = None,
                    fill = self._font['bgr_color'],
                    morph = bgr_morph,
                    closePath = True)
            
            # draw text
            shape.insertText(
                (text_x, text_y),
                line,
                fontsize = self._font['size'],
                fontname = self._font['name'],
                fontfile = self._font['file'],
                set_simple = False,
                encoding = 0,
                color = None,
                fill = self._font['for_color'],
                render_mode = 0,
                morph = text_morph)
            
            # update page
            shape.commit()
    
    
    def _fill_and_stroke(self, shape, close, even_odd=True, fill=True, commit=True):
        """Fills and strokes given shape."""
        
        # draw shape
        shape.finish(
            width = self._pen['width'] if self._pen['color'] else 0,
            color = self._pen['color'] if self._pen['width'] else None,
            lineCap = self._pen['cap'],
            lineJoin = self._pen['join'],
            dashes = self._pen['dashes'],
            fill = self._brush['color'] if fill else None,
            even_odd = even_odd,
            closePath = close)
        
        # update page
        if commit:
            shape.commit()
    
    
    def _update_pen(self, evt=None):
        """Updates pen with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('line_color', 'line_alpha'):
            color = ColorProperties.get_color(self, "line_")
            if color is not UNDEF:
                self._pen['color'] = color.rgb_r if color.alpha else None
        
        # update width
        if prop_name is None or prop_name in ('line_width', 'line_scale'):
            line_width = self.line_width
            if line_width is not UNDEF:
                self._pen['width'] = line_width * self.line_scale
        
        # update cap
        if prop_name is None or prop_name == 'line_cap':
            line_cap = self.line_cap
            if line_cap is not UNDEF:
                self._pen['cap'] = MUPDF_LINE_CAP[line_cap]
        
        # update join
        if prop_name is None or prop_name == 'line_join':
            line_join = self.line_join
            if line_join is not UNDEF:
                self._pen['join'] = MUPDF_LINE_JOIN[line_join]
        
        # update style/dash
        if prop_name is None or prop_name in ('line_dash', 'line_style', 'line_width', 'line_scale'):
            line_style = self.line_style
            line_dash = self.line_dash if self.line_dash else []
            line_width = self._pen['width']
            
            if line_style == LINE_STYLE_SOLID:
                line_dash = []
            elif line_style not in (LINE_STYLE_CUSTOM, UNDEF):
                line_dash = MUPDF_LINE_STYLE[line_style]
            
            self._pen['dashes'] = "[%s]0" % " ".join(str(int(x*line_width)) for x in line_dash)
    
    
    def _update_brush(self, evt=None):
        """Updates brush with current properties."""
        
        color = ColorProperties.get_color(self, "fill_")
        
        if self.fill_style == FILL_STYLE_TRANS:
            self._brush['color'] = None
        
        elif color is not UNDEF:
            self._brush['color'] = color.rgb_r if color.alpha else None
    
    
    def _update_text(self, evt=None):
        """Updates text with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update font
        if prop_name is None or prop_name in ('font_name', 'font_family', 'font_style', 'font_weight'):
            font = self.get_font()
            name = "%s %s %s" % (font.name, font.style, font.weight)
            self._font['name'] = name.title().replace(" ", "")
            self._font['file'] = font.path
        
        # update font size
        if prop_name is None or prop_name in ('font_size', 'font_scale'):
            font_size = self.font_size
            if font_size is None:
                self._font['size'] = 11 * self.font_scale
            elif font_size is not UNDEF:
                self._font['size'] = font_size * self.font_scale
        
        # update font descent
        if prop_name is None or prop_name in ('font_name', 'font_family', 'font_style', 'font_weight', 'font_size', 'font_scale'):
            font = self.get_font()
            self._font['descent'] = font.get_descent(int(0.5+self._font['size']))
        
        # update foreground color
        if prop_name is None or prop_name in ('text_color', 'text_alpha'):
            color = ColorProperties.get_color(self, "text_")
            if color is not UNDEF:
                self._font['for_color'] = color.rgb_r if color.alpha else None
        
        # update background color
        if prop_name is None or prop_name in ('text_bgr_color', 'text_bgr_alpha'):
            color = ColorProperties.get_color(self, "text_bgr_")
            if color is not UNDEF:
                self._font['bgr_color'] = color.rgb_r if color.alpha else None
