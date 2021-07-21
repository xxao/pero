#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import html
from ... properties import *
from ... drawing import Canvas, Path, Matrix, ClipState, GroupState
from . enums import *

# define constants
_INDENT = "  "


class SVGCanvas(Canvas):
    """Wrapper for SVG drawing context."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of SVGCanvas."""
        
        # init buffers
        self._commands = []
        self._filters = {}
        self._clips = {}
        self._indent = _INDENT
        
        self._pen_attrs = {
            'stroke': None,
            'stroke-opacity': None,
            'stroke-width': None,
            'stroke-dasharray': None,
            'stroke-linecap': None,
            'stroke-linejoin': None}
        
        self._brush_attrs = {
            'fill': None,
            'fill-opacity': None}
        
        self._font_attrs = {
            'font-family': None,
            'font-size': None,
            'font-style': None,
            'font-weight': None,
            'fill': None,
            'fill-opacity': None,
            'filter': None}
        
        self._font_descent = 0
        
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
    
    
    def get_xml(self):
        """
        Gets full XML for current drawings. The output already contains the main
        XML tags so it can be directly saved into a file.
        
        Returns:
            str
                Drawings XML.
        """
        
        # make xml
        xml = '<?xml version="1.0"?>'
        xml += '\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n\n'
        xml += self.get_svg()
        
        return xml
    
    
    def get_svg(self):
        """
        Gets SVG markup for current drawings. The output does not contain the
        main XML tags so it can be directly used within HTML documents.
        
        Returns:
            str
                Drawings SVG markup.
        """
        
        # init xml
        xml = '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s">\n' % (self.width, self.height)
        
        # add defs
        if self._filters or self._clips:
            xml += "  <defs>\n"
            
            # add filters
            if self._filters:
                xml += "    %s\n" % "\n    ".join(self._filters.values())
            
            # add clip paths
            if self._clips:
                xml += "    %s\n" % "\n    ".join(self._clips.values())
            
            xml += "  </defs>\n"
        
        # add drawings
        xml += "\n".join(self._commands)
        
        # finish xml
        xml += '\n</svg>'
        
        return xml
    
    
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
        
        # get pen and brush
        pen = self._get_pen_attrs()
        brush = self._get_brush_attrs()
        
        # make command
        command = self._indent + '<circle cx="%s" cy="%s" r="%s" %s %s />' % (x, y, radius, pen, brush)
        
        # add command
        self._commands.append(command)
    
    
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
        
        # get pen and brush
        pen = self._get_pen_attrs()
        brush = self._get_brush_attrs()
        
        # make command
        command = self._indent + '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" %s %s />' % (x, y, 0.5*width, 0.5*height, pen, brush)
        
        # add command
        self._commands.append(command)
    
    
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
        
        # get pen
        pen = self._get_pen_attrs()
        
        # make command
        command = self._indent + '<line x1="%s" y1="%s" x2="%s" y2="%s" %s />' % (x1, y1, x2, y2, pen)
        
        # add command
        self._commands.append(command)
    
    
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
        
        # format
        points = ("%s,%s" % (x,y) for x,y in points)
        
        # get pen and brush
        pen = self._get_pen_attrs()
        brush = self._get_brush_attrs()
        
        # make command
        command = self._indent + '<polyline points="%s" %s %s fill-rule="evenodd" />' % (" ".join(points), pen, brush)
        
        # add command
        self._commands.append(command)
    
    
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
        
        # get svg
        svg = path.svg(self._indent+_INDENT)
        
        # get pen and brush
        pen = self._get_pen_attrs()
        brush = self._get_brush_attrs()
        fill = SVG_FILL_RULE[path.fill_rule]
        
        # make command
        command = self._indent + '<path %s %s fill-rule="%s" d="%s" />' % (pen, brush, fill, svg)
        
        # add command
        self._commands.append(command)
    
    
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
        
        # format
        points = ("%s,%s" % (x,y) for x,y in points)
        
        # get pen and brush
        pen = self._get_pen_attrs()
        brush = self._get_brush_attrs()
        
        # make command
        command = self._indent + '<polygon points="%s" %s %s fill-rule="evenodd" />' % (" ".join(points), pen, brush)
        
        # add command
        self._commands.append(command)
    
    
    def draw_rect(self, x, y, width, height, radius=0):
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
        width = self._scale * width
        height = self._scale * height
        
        # get pen and brush
        pen = self._get_pen_attrs()
        brush = self._get_brush_attrs()
        
        # no round corners
        if not radius:
            command = self._indent + '<rect x="%s" y="%s" width="%s" height="%s" %s %s />' % (x, y, width, height, pen, brush)
        
        # same radius for all corners
        else:
            radius = self._scale * radius[0]
            command = self._indent + '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" ry="%s" %s %s />' % (x, y, width, height, radius, radius, pen, brush)
        
        # add command
        self._commands.append(command)
    
    
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
        
        # get font attributes
        font = self._get_text_attrs()
        
        # get full size
        full_width, full_height = self.get_text_size(text)
        descent = self._font_descent / self._scale
        
        # get rotation origin
        trans_x = self._scale * (x + self._offset[0])
        trans_y = self._scale * (y + self._offset[1])
        angle = numpy.rad2deg(angle)
        
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
            text_x = self._scale * (x + x_offset + self._offset[0])
            text_y = self._scale * (y + y_offset + self._offset[1])
            
            # escape line
            line = html.escape(line)
            
            # make command
            transform = 'transform="rotate(%s, %s, %s)"' % (angle, trans_x, trans_y) if angle else ""
            command = self._indent + '<text x="%s" y="%s" %s %s>%s</text>' % (text_x, text_y, font, transform, line)
            
            # add command
            self._commands.append(command)
    
    
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
        
        # make clip path
        name = "clip_%03d" % len(self._clips)
        self._clips[name] = '<clipPath id="%s"><path d="%s" /></clipPath>' % (name, path.svg())
        
        # make command
        command = self._indent + '<g clip-path="url(#%s)">' % name
        
        # add command
        self._commands.append(command)
        
        # increase indentation
        self._indent += _INDENT
        
        # return state
        return ClipState(self)
    
    
    def unclip(self):
        """Removes last clipping path while keeping previous if any."""
        
        # decrease indentation
        self._indent = self._indent[:-len(_INDENT)]
        
        # add command
        self._commands.append(self._indent + '</g>')
    
    
    def group(self, id_tag=None, class_tag=None):
        """
        Opens new drawing group.
        
        Args:
            id_tag: str
                Unique id of the group.
            
            class_tag:
                Class of the group.
        
        Returns:
            pero.GroupState
                Grouping state context manager.
        """
        
        # make command
        id_tag = ' id="%s"' % id_tag if id_tag else ""
        class_tag = ' class="%s"' % class_tag if class_tag else ""
        command = self._indent + '<g%s%s>' % (id_tag, class_tag)
        
        # add command
        self._commands.append(command)
        
        # increase indentation
        self._indent += _INDENT
        
        # return state
        return GroupState(self)
    
    
    def ungroup(self):
        """Closes the last drawing group."""
        
        # decrease indentation
        self._indent = self._indent[:-len(_INDENT)]
        
        # add command
        self._commands.append(self._indent + '</g>')
    
    
    def _get_pen_attrs(self):
        """Gets current pen attributes."""
        
        attrs = ('%s="%s"' % attr for attr in self._pen_attrs.items() if attr[1] is not None)
        return " ".join(attrs)
    
    
    def _get_brush_attrs(self):
        """Gets current brush attributes."""
        
        attrs = ('%s="%s"' % attr for attr in self._brush_attrs.items() if attr[1] is not None)
        return " ".join(attrs)
    
    
    def _get_text_attrs(self):
        """Gets current text attributes."""
        
        attrs = ('%s="%s"' % attr for attr in self._font_attrs.items() if attr[1] is not None)
        return " ".join(attrs)
    
    
    def _get_text_bgr_filter(self):
        """Gets the text background filter."""
        
        # get color
        color = ColorProperties.get_color(self, "text_bgr_")
        if not color or color.alpha == 0:
            return None
        
        # make name
        name = "text_bgr_%s" % color.hex[1:]
        
        # make filter if not present
        if name not in self._filters:
            
            flood = 'flood-color="%s"' % color.hex[:-2]
            if color.alpha != 255:
                flood += ' flood-opacity="%s"' % (color.alpha/255.)
            
            self._filters[name] = '<filter id="%s" x="0" y="0" width="1" height="1"><feFlood %s /><feComposite in="SourceGraphic" /></filter>' % (name, flood)
        
        return name
    
    
    def _update_pen(self, evt=None):
        """Updates pen with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('line_color', 'line_alpha'):
            color = ColorProperties.get_color(self, "line_")
            if color is not UNDEF:
                self._pen_attrs['stroke'] = color.hex[:-2]
                self._pen_attrs['stroke-opacity'] = color.alpha/255. if color.alpha != 255 else None
        
        # update width
        if prop_name is None or prop_name in ('line_width', 'line_scale'):
            line_width = self.line_width
            if line_width is not UNDEF:
                self._pen_attrs['stroke-width'] = line_width * self.line_scale
        
        # update cap
        if prop_name is None or prop_name == 'line_cap':
            line_cap = self.line_cap
            if line_cap is not UNDEF:
                self._pen_attrs['stroke-linecap'] = SVG_LINE_CAP[line_cap]
        
        # update join
        if prop_name is None or prop_name == 'line_join':
            line_join = self.line_join
            if line_join is not UNDEF:
                self._pen_attrs['stroke-linejoin'] = SVG_LINE_JOIN[line_join]
        
        # update style/dash
        if prop_name is None or prop_name in ('line_dash', 'line_style', 'line_width', 'line_scale'):
            line_style = self.line_style
            line_dash = self.line_dash if self.line_dash else []
            line_width = self._pen_attrs['stroke-width']
            
            if line_style == LINE_STYLE_SOLID:
                line_dash = []
            elif line_style not in (LINE_STYLE_CUSTOM, UNDEF):
                line_dash = SVG_LINE_STYLE[line_style]
            
            line_dash = ",".join(str(x*line_width) for x in line_dash) if line_dash else None
            
            self._pen_attrs['stroke-dasharray'] = line_dash
    
    
    def _update_brush(self, evt=None):
        """Updates brush with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # update color
        if prop_name is None or prop_name in ('fill_color', 'fill_alpha', 'fill_style'):
            color = ColorProperties.get_color(self, "fill_")
            
            if self.fill_style == FILL_STYLE_TRANS:
                self._brush_attrs['fill'] = None
                self._brush_attrs['fill-opacity'] = 0
            
            elif color is not UNDEF:
                self._brush_attrs['fill'] = color.hex[:-2]
                self._brush_attrs['fill-opacity'] = color.alpha/255. if color.alpha != 255 else None
    
    
    def _update_text(self, evt=None):
        """Updates text with current properties."""
        
        # get property name
        prop_name = evt.name if evt is not None else None
        
        # init flag
        font_changed = False
        
        # update font name/family
        if prop_name is None or prop_name in ('font_name', 'font_family'):
            font_name = self.font_name
            font_family = self.font_family
            
            if font_name:
                self._font_attrs['font-family'] = font_name
            elif font_family is None:
                self._font_attrs['font-family'] = None
            elif font_family is not UNDEF:
                self._font_attrs['font-family'] = SVG_FONT_FAMILY[font_family]
            
            font_changed = True
        
        # update font size
        if prop_name is None or prop_name in ('font_size', 'font_scale'):
            font_size = self.font_size
            
            if font_size is None:
                self._font_attrs['font-size'] = 11 * self.font_scale
            elif font_size is not UNDEF:
                self._font_attrs['font-size'] = font_size * self.font_scale
            
            font_changed = True
        
        # update font style
        if prop_name is None or prop_name == 'font_style':
            font_style = self.font_style
            
            if font_style is None:
                self._font_attrs['font-style'] = None
            elif font_style == FONT_STYLE_NORMAL:
                self._font_attrs['font-style'] = None
            elif font_style is not UNDEF:
                self._font_attrs['font-style'] = SVG_FONT_STYLE[font_style]
            
            font_changed = True
        
        # update font weight
        if prop_name is None or prop_name == 'font_weight':
            font_weight = self.font_weight
            
            if font_weight is None:
                self._font_attrs['font-weight'] = None
            elif font_weight == FONT_WEIGHT_NORMAL:
                self._font_attrs['font-weight'] = None
            elif font_weight is not UNDEF:
                self._font_attrs['font-weight'] = SVG_FONT_WEIGHT[font_weight]
            
            font_changed = True
        
        # update foreground color
        if prop_name is None or prop_name in ('text_color', 'text_alpha'):
            color = ColorProperties.get_color(self, "text_")
            if color is not UNDEF:
                self._font_attrs['fill'] = color.hex[:-2]
                self._font_attrs['fill-opacity'] = color.alpha/255. if color.alpha != 255 else None
        
        # update background color
        if prop_name is None or prop_name in ('text_bgr_color', 'text_bgr_alpha'):
            bgr_filter = self._get_text_bgr_filter()
            
            if bgr_filter:
                self._font_attrs['filter'] = 'url(#%s)' % bgr_filter
            else:
                self._font_attrs['filter'] = None
        
        # get final font family
        if font_changed:
            font = self.get_font()
            self._font_attrs['font-family'] = font.name
            self._font_descent = font.get_descent(int(0.5+self._font_attrs['font-size']))
