#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import numpy
from ..enums import *
from ..events import *
from ..properties import *
from .fonts import FONTS
from .frame import Frame
from .matrix import Matrix
from .path import Path


class Canvas(PropertySet):
    """
    Abstract base class for drawing canvas. Each derived class must provide
    specific implementations for several basic drawing methods to unify the
    drawing API across multiple backends.
    
    The canvas 'width' and 'height' is always set in original device units (e.g.
    pixels), however, all the drawing methods are using logical units, which
    includes current line scale and drawing region aka 'viewport'. This makes
    all the drawing resolution-independent and in case of drawing the same
    graphics multiple times with different resolution, it is sufficient to
    change the 'line_scale' and 'font_scale' properties accordingly. None of the
    properties of the graphics needs to be changed.
    
    Properties:
        
        width: int or float
            Specifies the available width of the canvas in device units.
        
        height: int or float
            Specifies the available height of the canvas in device units.
        
        line_scale: int or float
            Specifies the scaling factor for drawing.
        
        line_color: pero.Color, (int,), str, None or UNDEF
            Specifies the line color as an RGB or RGBA tuple, hex code, name or
            pero.Color.
        
        line_alpha: int, None or UNDEF
            Specifies the line alpha channel as a value between 0 and 255, where
            0 is fully transparent and 255 fully opaque. If this value is set,
            it will overwrite the alpha channel of the final line color.
        
        line_width: int, float or UNDEF
            Specifies the line width.
        
        line_style: pero.LINE_STYLE or UNDEF
            Specifies the line drawing style as any item from the
            pero.LINE_STYLE enum.
        
        line_dash: (float,), None or UNDEF
            Specifies the line dash style as a collection of numbers defining the
            lengths of lines and spaces in-between. Specified value is used only
            if the 'line_style' property is set to pero.LINE_STYLE.CUSTOM.
        
        line_cap: pero.LINE_CAP or UNDEF
            Specifies the line ends shape as any item from the pero.LINE_CAP
            enum.
        
        line_join: pero.LINE_JOIN or UNDEF
            Specifies the line corners shape as any item from the
            pero.LINE_JOIN enum.
        
        fill_color: pero.Color, (int,), str, None or UNDEF
            Specifies the fill color as an RGB or RGBA tuple, hex code, name or
            pero.Color.
        
        fill_alpha: int, None or UNDEF
            Specifies the fill alpha channel as a value between 0 and 255,
            where 0 is fully transparent and 255 fully opaque. If this value is
            set, it will overwrite the alpha channel of the final fill color.
        
        fill_style: pero.FILL_STYLE or UNDEF
            Specifies the fill style as any item from the pero.FILL_STYLE
            enum.
        
        font_scale: int, float
            Specifies the scaling factor for texts.
        
        font_factor: int, float
            Specifies the font normalization factor of the canvas.
        
        font_size: int, None or UNDEF
            Specifies the font size or None to reset to default size.
        
        font_name: str, None or UNDEF
            Specifies an existing font name or None to reset to default family.
        
        font_family: pero.FONT_FAMILY, None or UNDEF
            Specifies the font family as any item from the pero.FONT_FAMILY
            enum or None to reset to default family.
        
        font_style: pero.FONT_STYLE, None or UNDEF
            Specifies the font style as any item from the pero.FONT_STYLE
            enum or None to reset to default style.
        
        font_weight: pero.FONT_WEIGHT, None or UNDEF
            Specifies the font weight as any item from the pero.FONT_WEIGHT
            enum or None to reset to default weight.
        
        text_align: pero.TEXT_ALIGN, None or UNDEF
            Specifies the text alignment as any item from the pero.TEXT_ALIGN
            enum or None to reset to default alignment.
        
        text_base: pero.TEXT_BASELINE, None or UNDEF
            Specifies the text baseline as any item from the
            pero.TEXT_BASELINE enum or None to reset to default baseline.
        
        text_color: pero.Color, (int,), str, None or UNDEF
            Specifies the text foreground color as an RGB or RGBA tuple, hex
            code, name or pero.Color.
        
        text_alpha: int, None or UNDEF
            Specifies the text foreground alpha channel as a value between 0 and
            255, where 0 is fully transparent and 255 fully opaque. If this
            value is set, it will overwrite the alpha channel of the final text
            color.
        
        text_bgr_color: pero.Color, (int,), str, None or UNDEF
            Specifies the text background color as an RGB or RGBA tuple, hex
            code, name or pero.Color.
        
        text_bgr_alpha: int, None or UNDEF
            Specifies the text background alpha channel as a value between 0 and
            255, where 0 is fully transparent and 255 fully opaque. If this
            value is set, it will overwrite the alpha channel of the final text
            background color.
        
        text_split: bool
            Specifies whether the text should be first split into individual
            lines. This requires corresponding 'text_splitter' property to be
            set.
        
        text_splitter: str
            Specifies the character(s) to be used for splitting a text into
            individual lines.
        
        text_spacing: float
            Specifies additional space to be inserted between text lines as
            multiplier of line height.
        
        viewport: pero.Frame (read-only)
            Specifies current drawing region coordinates in logical units. It
            defines actual drawing origin and logical width and height of the
            canvas.
    """
    
    width = NumProperty(100, dynamic=False)
    height = NumProperty(100, dynamic=False)
    
    line_scale = FloatProperty(1, dynamic=False)
    font_scale = FloatProperty(1, dynamic=False)
    font_factor = FloatProperty(1, dynamic=False)
    
    pen = Include(LineProperties, dynamic=False, line_color="#000")
    brush = Include(FillProperties, dynamic=False, fill_color=None)
    text = Include(TextProperties, dynamic=False, font_size=10)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Canvas."""
        
        super(Canvas, self).__init__(**overrides)
        
        # hold properties
        self.hold_property('line_color')
        self.hold_property('fill_color')
        self.hold_property('text_color')
        self.hold_property('text_bgr_color')
        
        # init property names
        self._pen_properties = set(x.name for x in LineProperties.properties())
        self._brush_properties = set(x.name for x in FillProperties.properties())
        self._text_properties = set(x.name for x in TextProperties.properties())
        
        # init scale and offset
        self._scale = numpy.array((self.line_scale, self.line_scale))
        self._offset = numpy.array((0, 0))
        
        # set font
        self._cfont = None
        
        # init views
        self._viewport = None
        self._viewport_full = Frame(0,0, self.width/self.line_scale, self.height/self.line_scale)
        
        # bind events
        self.bind(EVENT.PROPERTY_CHANGED, self._on_canvas_property_changed)
    
    
    @property
    def viewport(self):
        """
        Gets current drawing area coordinates.
        
        Returns:
            pero.Frame
                Current drawing area.
        """
        
        # get full view
        if self._viewport is None:
            return self._viewport_full
        
        # get current view
        return self._viewport
    
    
    def set_viewport(self, x=None, y=None, width=None, height=None, relative=False):
        """
        Sets rectangular region currently used for drawing. This provides an
        easy way to draw complex graphics at specific position of the
        canvas without adjusting the coordinates of the graphics. It is achieved
        by changing the origin coordinates and the logical width and height of
        the canvas.
        
        Args:
            x: int or float
                X-coordinate of the top-left corner.
            
            y: int or float
                Y-coordinate of the top-left corner.
            
            width: int, float or None
                Full width of the viewport.
            
            height: int, float or None
                Full height of the viewport.
            
            relative: bool
                If set to True the new viewport is applied relative to current
                one.
        """
        
        # reset to full
        if x is None and y is None:
            self._viewport = None
            self._offset = numpy.array((0, 0))
            return
        
        # get current viewport
        viewport = self.viewport
        
        # make relative
        if relative:
            x = (x or 0) + viewport.x
            y = (y or 0) + viewport.y
        
        # get origin
        if x is None:
            x = 0
        if y is None:
            y = 0
        
        # get width
        if width is None:
            width = viewport.width
        
        # get height
        if height is None:
            height = viewport.height
        
        # set viewport
        self._viewport = Frame(x, y, width, height)
        self._offset = numpy.array((x, y))
    
    
    def set_pen_by(self, prop_set, prefix="", source=UNDEF, overrides=None):
        """
        Extracts and applies all line properties from given property set.
        
        Args:
            prop_set: pero.PropertySet
                Object from which to extract line properties.
            
            prefix: str
                Prefix used for line properties to be extracted.
            
            source: ? or None
                Data source to be used for calculating callable properties.
            
            overrides:
                Specific properties to be overwritten.
        """
        
        # extract and set line properties
        for prop in self._pen_properties:
            value = prop_set.get_property(prefix+prop, source, overrides)
            self.set_property(prop, value, True)
    
    
    def set_brush_by(self, prop_set, prefix="", source=UNDEF, overrides=None):
        """
        Extracts and applies all fill properties from given property set.
        
        Args:
            prop_set: pero.PropertySet
                Object from which to extract fill properties.
            
            prefix: str
                Prefix used for fill properties to be extracted.
            
            source: ? or None
                Data source to be used for calculating callable properties.
            
            overrides:
                Specific properties to be overwritten.
        """
        
        # extract and set fill properties
        for prop in self._brush_properties:
            value = prop_set.get_property(prefix+prop, source, overrides)
            self.set_property(prop, value, True)
    
    
    def set_text_by(self, prop_set, prefix="", source=UNDEF, overrides=None):
        """
        Extracts and applies all text properties from given property set.
        
        Args:
            prop_set: pero.PropertySet
                Object from which to extract text properties.
            
            prefix: str
                Prefix used for text properties to be extracted.
            
            source: ? or None
                Data source to be used for calculating callable properties.
            
            overrides:
                Specific properties to be overwritten.
        """
        
        # extract and set text properties
        for prop in self._text_properties:
            value = prop_set.get_property(prefix+prop, source, overrides)
            self.set_property(prop, value, True)
    
    
    def get_font(self):
        """
        Gets current font.
        
        Returns:
            pero.Font
                Current font.
        """
        
        # get current font
        if self._cfont is not None:
            return self._cfont
        
        # get font names
        names = []
        if self.font_name:
            names.append(self.font_name)
        
        elif self.font_family in FONT_FAMILY_NAMES:
            names = FONT_FAMILY_NAMES[self.font_family]
        
        # get specific font
        for name in names:
            
            self._cfont = FONTS.get_font(
                family = name,
                style = self.font_style,
                weight = self.font_weight)
            
            if self._cfont is not None:
                return self._cfont
        
        # get regular font
        for name in names:
            
            self._cfont = FONTS.get_font(
                family = name,
                style = FONT_STYLE.NORMAL,
                weight = FONT_WEIGHT.NORMAL)
            
            if self._cfont is not None:
                return self._cfont
        
        # get font just by name
        for name in names:
            
            self._cfont = FONTS.get_font(
                family = name,
                style = None,
                weight = None)
            
            if self._cfont is not None:
                return self._cfont
        
        # font not found
        message = "Cannot initialize the font! -> %s" % ",".join(names)
        raise ValueError(message)
    
    
    def get_line_size(self, text):
        """
        Gets width and height of a single text line using current text settings.
        
        The result is given in logical units, i.e. current font scaling is
        applied but no line scaling. Note that if used directly to draw any line
        drawing (e.g. bounding rectangle), current line scaling will be applied.
        Be sure to apply inverse scaling before or use the 'get_text_size'
        method instead.
        
        This method should be overridden by specific backend to get more
        precise size.
        
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
        
        # get font
        font = self.get_font()
        
        # get font size
        size = 10
        if self.font_size:
            size = int(0.5 + self.font_size * self.font_scale * self.font_factor)
        
        # get text size
        width, height = font.get_size(text, size)
        
        # get full height
        full = font.get_size("j", size)
        height = max(height, full[1])
        
        return width, height
    
    
    def get_text_size(self, text, invert_scaling=True):
        """
        Gets width and height of the text bounding box using current text
        settings.
        
        By default, resulting width and height are inverse-scaled by current
        line scaling factor. It allows direct use for drawing text-related
        graphics like bounding rectangles etc. This behavior can be disabled
        by setting 'invert_scaling' to False.
        
        Args:
            text: str
                Text for which the size should be calculated.
            
            invert_scaling: bool
                If set to True, resulting width and height are inverse-scaled by
                current line scale factor.
        
        Returns:
            (float, float)
                Text width and height.
        """
        
        width = 0
        height = 0
        
        # check text
        if not text:
            return width, height
        
        # split lines
        lines = [text]
        if self.text_split and self.text_splitter:
            lines = text.split(self.text_splitter)
        
        # calc size
        for line in lines:
            
            # get line size
            line_width, line_height = self.get_line_size(line or " ")
            
            # update size
            height += line_height
            if line_width > width:
                width = line_width
        
        # add line spacing
        height += line_height*self.text_spacing * (len(lines) - 1)
        
        # invert scaling
        if invert_scaling:
            width /= self._scale[0]
            height /= self._scale[1]
        
        return width, height
    
    
    def get_text_bbox(self, text, x=0, y=0, angle=0, invert_scaling=True):
        """
        Gets bounding box of the text.
        
        By default, text width and height are inverse-scaled by current line
        scaling factor. It allows direct use for drawing text-related graphics
        like bounding rectangles etc. This behavior can be disabled by setting
        'invert_scaling' to False.
        
        Args:
            text: str
                Text to be drawn.
            
            x: int or float
                X-coordinate of the text anchor.
            
            y: int or float
                Y-coordinate of the text anchor.
            
            angle: float
                Text angle in radians.
            
            invert_scaling: bool
                If set to True, text width and height are inverse-scaled by
                current line scale factor.
        
        Returns:
            pero.Frame
                Text bounding box.
        """
        
        # check data
        if not text:
            return Frame(x, y, 0, 0)
        
        # init buffers
        boxes = []
        x0 = x
        y0 = y
        
        # split lines
        lines = [text]
        if self.text_split and self.text_splitter:
            lines = text.split(self.text_splitter)
        
        # calc boxes
        for line in lines:
            
            # get line size
            width, height = self.get_line_size(line or " ")
            
            # invert scaling
            if invert_scaling:
                width /= self._scale[0]
                height /= self._scale[1]
            
            # apply alignment
            if self.text_align == TEXT_ALIGN.CENTER:
                x0 = x - 0.5 * width
            
            elif self.text_align == TEXT_ALIGN.RIGHT:
                x0 = x - width
            
            # store box
            boxes.append(Frame(x0, y0, width, height))
            
            # add line spacing
            y0 += height * (1 + self.text_spacing)
        
        # apply baseline
        y_offset = 0
        total_height = y0 - y - height * self.text_spacing
        
        if self.text_base == TEXT_BASELINE.MIDDLE:
            y_offset = - 0.5*total_height
        
        elif self.text_base == TEXT_BASELINE.BOTTOM:
            y_offset = - total_height
        
        if y_offset:
            for box in boxes:
                box.offset(y=y_offset)
        
        # calc sin
        sin = numpy.sin(angle)
        cos = numpy.cos(angle)
        
        # make final frame
        frame = Frame(x, y)
        for box in boxes:
            for p in box.points:
                px = x + (p[0]-x) * cos - (p[1]-y) * sin
                py = y + (p[0]-x) * sin + (p[1]-y) * cos
                frame.extend(px, py)
        
        return frame
    
    
    def draw_arc(self, x, y, radius, start_angle, end_angle, clockwise=True):
        """
        Draws an arc of specified radius centered around given coordinates.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
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
        
        # make path
        path = Path()
        path.arc(x, y, radius, start_angle, end_angle, clockwise)
        
        # draw path
        self.draw_path(path)
    
    
    def draw_circle(self, x, y, radius):
        """
        Draws a circle of specified radius centered around given coordinates.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the circle.
        """
        
        # make path
        path = Path()
        path.circle(x, y, radius)
        
        # draw path
        self.draw_path(path)
    
    
    def draw_ellipse(self, x, y, width, height):
        """
        Draws an ellipse centered around given coordinates and fitting into the
        width and height.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
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
        
        # make path
        path = Path()
        path.ellipse(x, y, width, height)
        
        # draw path
        self.draw_path(path)
    
    
    def draw_graphics(self, graphics, source=UNDEF, **overrides):
        """
        Draws given graphics into current canvas.
        
        Args:
            graphics: pero.Graphics
                Graphics to be drawn.
            
            source: any
                Data source to be used for calculating callable properties of
                the graphics.
            
            overrides: str:any pairs
                Specific properties of the graphics to be overwritten.
        """
        
        graphics.draw(self, source=source, **overrides)
    
    
    def draw_line(self, x1, y1, x2, y2):
        """
        Draws a line between two points.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
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
        
        # make path
        path = Path()
        path.move_to(x1, y1)
        path.line_to(x2, y2)
        
        # draw path
        self.draw_path(path)
    
    
    def draw_lines(self, points):
        """
        Draws continuous open line using sequence of points.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            points: ((float, float),)
                Sequence of x,y coordinates of the points.
        """
        
        # init path
        path = Path()
        path.move_to(points[0][0], points[0][1])
        
        # add points
        for p in points[1:]:
            path.line_to(p[0], p[1])
        
        # draw path
        self.draw_path(path)
    
    
    def draw_path(self, path):
        """
        Draws given path using current pen and brush.
        
        This method must be overwritten by specific backend to provide native
        implementation for path drawing.
        
        Args:
            path: pero.Path
                Path to be drawn.
        """
        
        raise NotImplementedError("The 'draw_path' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def draw_polygon(self, points):
        """
        Draws a closed polygon using sequence of points.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            points: ((float, float),)
                Sequence of x,y coordinates of the points.
        """
        
        # check points
        if len(points) < 2:
            return
        
        # init path
        path = Path()
        path.move_to(points[0][0], points[0][1])
        
        # add points
        for p in points[1:]:
            path.line_to(p[0], p[1])
        
        # close path
        path.close()
        
        # draw path
        self.draw_path(path)
    
    
    def draw_rect(self, x, y, width, height, radius=None):
        """
        Draws a rectangle specified by given top left corner and size and
        optional round corners specified as a single value or individual value
        for each corners starting from top-left.
        
        This method should be overridden by specific backend to provide native
        implementation other than the default using pero.Path.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            width: int or float
                Full width of the rectangle.
            
            height: int or float
                Full height of the rectangle.
            
            radius: int, float, (int,int,int,int) or (float,float,float,float)
                Radius of curved corners.
        """
        
        # make path
        path = Path()
        path.rect(x, y, width, height, radius)
        
        # draw path
        self.draw_path(path)
    
    
    def draw_text(self, text, x, y, angle=0):
        """
        Draws a text string anchored at specified point using current text
        settings.
        
        This method must be overwritten by specific backend to provide native
        implementation for text drawing.
        
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
        
        raise NotImplementedError("The 'draw_text' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def draw_text_polar(self, text, x, y, radius, angle, position=POSITION.CENTER, rotation=TEXT_ROTATION.FOLLOW):
        """
        Draws a text string anchored at specified point with automatic alignment
        and baseline according to given angle, using current text settings.
        
        Args:
            text: str
                Text to be drawn.
            
            x: int or float
                X-coordinate of the text anchor.
            
            y: int or float
                Y-coordinate of the text anchor.
            
            radius: int or float
                Radius of the virtual anchor circle.
            
            angle: int or float
                Text anchor angle in radians.
            
            position: pero.POSITION_IOC
                Text position along the anchor circle as any item from the
                pero.POSITION_IOC enum.
            
            rotation: pero.TEXT_ROTATION
                Relative rotation of the text along the anchor circle as any
                item from the pero.TEXT_ROTATION enum.
        """
        
        # remember current settings
        ori_text_align = self.text_align
        ori_text_base = self.text_base
        
        # set angle tolerance
        tol = radius * numpy.sin(numpy.deg2rad(4))
        
        # rotate coordinates
        x1 = x + radius * numpy.cos(angle)
        y1 = y + radius * numpy.sin(angle)
        
        # get position
        is_perpendicular = (rotation in (TEXT_ROTATION.NATURAL, TEXT_ROTATION.FACEOUT, TEXT_ROTATION.FACEIN))
        is_out = (position == POSITION.OUTSIDE)
        
        # adjust angle
        if rotation == TEXT_ROTATION.FACEOUT:
            angle += 0.5*numpy.pi
        
        elif rotation == TEXT_ROTATION.FACEIN:
            angle -= 0.5*numpy.pi
        
        elif rotation == TEXT_ROTATION.NATURAL and y1 > y + tol:
            angle -= 0.5*numpy.pi
        
        elif rotation == TEXT_ROTATION.NATURAL:
            angle += 0.5*numpy.pi
        
        elif x1 < x - tol:
            angle -= numpy.pi
        
        # perpendicular
        if is_perpendicular:
            self.text_align = TEXT_ALIGN.CENTER
        
        # on edge
        elif position == POSITION.CENTER:
            self.text_align = TEXT_ALIGN.CENTER
        
        # left side
        elif x1 < x - tol:
            self.text_align = TEXT_ALIGN.RIGHT if is_out else TEXT_ALIGN.LEFT
        
        # right side
        elif x1 > x + tol:
            self.text_align = TEXT_ALIGN.LEFT if is_out else TEXT_ALIGN.RIGHT
        
        # rotated at center
        elif rotation == TEXT_ROTATION.FOLLOW:
            self.text_align = TEXT_ALIGN.LEFT if is_out else TEXT_ALIGN.RIGHT
        
        # at center
        else:
            self.text_align = TEXT_ALIGN.CENTER
        
        # center on edge
        if position == POSITION.CENTER:
            self.text_base = TEXT_BASELINE.MIDDLE
        
        # rotated
        elif rotation == TEXT_ROTATION.FOLLOW:
            self.text_base = TEXT_BASELINE.MIDDLE
            
        # perpendicular
        elif rotation == TEXT_ROTATION.FACEOUT:
            self.text_base = TEXT_BASELINE.BOTTOM if is_out else TEXT_BASELINE.TOP
            
        # perpendicular
        elif rotation == TEXT_ROTATION.FACEIN:
            self.text_base = TEXT_BASELINE.TOP if is_out else TEXT_BASELINE.BOTTOM
            
        # top part
        elif y1 < y - tol:
            self.text_base = TEXT_BASELINE.BOTTOM if is_out else TEXT_BASELINE.TOP
        
        # bottom part
        elif y1 > y + tol:
            self.text_base = TEXT_BASELINE.TOP if is_out else TEXT_BASELINE.BOTTOM
        
        # rotated at middle
        elif rotation == TEXT_ROTATION.NATURAL:
            self.text_base = TEXT_BASELINE.BOTTOM if is_out else TEXT_BASELINE.TOP
        
        # at middle
        else:
            self.text_base = TEXT_BASELINE.MIDDLE
        
        # draw text
        if rotation != TEXT_ROTATION.NONE:
            self.draw_text(text, x1, y1, angle=angle)
        else:
            self.draw_text(text, x1, y1)
        
        # reset original settings
        self.text_align = ori_text_align
        self.text_base = ori_text_base
    
    
    def fill(self):
        """Fills current drawing region by actual fill color."""
        
        # remove current pen
        line_width = self.line_width
        self.line_width = 0
        
        # draw rectangle
        self.draw_rect(*self.viewport.rect)
        
        # reset pen
        self.line_width = line_width
    
    
    def clip(self, path):
        """
        Sets clipping path as intersection with current one.
        
        This method needs be overwritten by specific backend to provide native
        implementation for clipping.
        
        Args:
            path: pero.Path
                Path to be used for clipping.
        """
        
        pass
    
    
    def unclip(self):
        """
        Removes last clipping path while keeping previous if any.
        
        This method needs be overwritten by specific backend to provide native
        implementation for clipping.
        """
        
        pass
    
    
    def group(self, id_tag=None, class_tag=None):
        """
        Opens new drawing group.
        
        This method needs be overwritten by specific backend to provide native
        implementation for objects grouping.
        
        Args:
            id_tag: str
                Unique id of the group.
            
            class_tag:
                Class of the group.
        """
        
        pass
    
    
    def ungroup(self):
        """
        Closes the last drawing group.
        
        This method needs be overwritten by specific backend to provide native
        implementation for objects grouping.
        """
        
        pass
    
    
    def to_device(self, x, y):
        """
        Recalculates given logical content position into absolute device
        position within the canvas by removing current line scale and origin
        offset.
        
        Args:
            x: float
                Logical x-coordinate.
            
            y: float
                Logical y-coordinate.
        
        Returns:
            (float, float)
                Absolute device x and y coordinates.
        """
        
        x = (x + self._offset[0]) * self._scale[0]
        y = (y + self._offset[1]) * self._scale[0] 
        
        return x, y
    
    
    def to_logical(self, x, y):
        """
        Recalculates given absolute device position into logical position within
        current view by applying current line scale and origin offset.
        
        Args:
            x: float
                Device x-coordinate.
            
            y: float
                Device y-coordinate.
        
        Returns:
            (float, float)
                Logical x and y coordinates within current view.
        """
        
        x = x / self._scale[0] - self._offset[0]
        y = y / self._scale[0] - self._offset[1]
        
        return x, y
    
    
    def _on_canvas_property_changed(self, evt):
        """Called after any property has changed."""
        
        # update line scaling
        if evt.name == 'line_scale':
            self._scale = numpy.array((self.line_scale, self.line_scale))
        
        # update full viewport
        if evt.name in ('line_scale', 'width', 'height'):
            self._viewport_full = Frame(0,0, self.width/self.line_scale, self.height/self.line_scale)
        
        # update current font
        if evt.name in ('font_name', 'font_family', 'font_style', 'font_weight'):
            self._cfont = None
        
        # update current pen
        if evt.name in self._pen_properties or evt.name == 'line_scale':
            self.fire(PenChangedEvt.from_evt(evt))
        
        # update current brush
        if evt.name in self._brush_properties:
            self.fire(BrushChangedEvt.from_evt(evt))
        
        # update current text
        if evt.name in self._text_properties or evt.name in ('font_scale', 'font_factor'):
            self.fire(TextChangedEvt.from_evt(evt))
