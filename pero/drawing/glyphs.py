#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import math
from ..enums import *
from ..properties import *
from .graphics import Graphics
from .matrix import Matrix
from .path import Path


class Glyph(Graphics):
    """Abstract base class for simple graphical entities."""
    
    pass


class Annulus(Glyph):
    """
    Defines a ring-like glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the center.
        
        y: int, float or callable
            Specifies the y-coordinate of the center.
        
        inner_radius: int, float or callable
            Specifies the inner radius.
        
        outer_radius: int, float or callable
            Specifies the outer radius.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    inner_radius = NumProperty(UNDEF)
    outer_radius = NumProperty(UNDEF)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        inner_radius = self.get_property('inner_radius', source, overrides)
        outer_radius = self.get_property('outer_radius', source, overrides)
        
        # make path
        path = Path().circle(x, y, inner_radius)
        if outer_radius:
            path.circle(x, y, outer_radius)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw path
        canvas.draw_path(path)


class Arc(Glyph):
    """
    Defines an arc glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the center.
        
        y: int, float or callable
            Specifies the y-coordinate of the center.
        
        radius: int, float or callable
            Specifies the arc radius.
        
        clockwise: bool or callable
            Specifies the drawing direction. If set to True the arc is drawn
            clockwise, otherwise anti-clockwise.
        
        start_angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        end_angle properties:
            Includes pero.AngleProperties to specify the end angle.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    radius = NumProperty(UNDEF)
    start_angle = Include(AngleProperties, prefix="start_")
    end_angle = Include(AngleProperties, prefix="end_")
    clockwise = BoolProperty(True)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        start_angle = AngleProperties.get_angle(self, 'start_', ANGLE.RAD, source, overrides)
        end_angle = AngleProperties.get_angle(self, 'end_', ANGLE.RAD, source, overrides)
        radius = self.get_property('radius', source, overrides)
        clockwise = self.get_property('radius', source, overrides)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_arc(x, y, radius, start_angle, end_angle, clockwise)


class Bar(Glyph):
    """
    Defines a bar glyph.
    
    Properties:
        
        left: int, float or callable
            Specifies the x-coordinate of the left edge.
        
        right: int, float or callable
            Specifies the x-coordinate of the right edge.
        
        top: int, float or callable
            Specifies the y-coordinate of the top edge.
        
        bottom: int, float or callable
            Specifies the y-coordinate of the bottom edge.
        
        radius: int, float, (int,), (float,) callable or UNDEF
            Specifies the corner radius as a single value or values for
            individual corners starting from top-left.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    left = NumProperty(0)
    right = NumProperty(0)
    top = NumProperty(0)
    bottom = NumProperty(0)
    
    radius = QuadProperty(0)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        left = self.get_property('left', source, overrides)
        right = self.get_property('right', source, overrides)
        top = self.get_property('top', source, overrides)
        bottom = self.get_property('bottom', source, overrides)
        radius = self.get_property('radius', source, overrides)
        
        # check coords
        if right < left:
            left, right = right, left
        if bottom < top:
            top, bottom = bottom, top
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_rect(left, top, right-left, bottom-top, radius)


class Ellipse(Glyph):
    """
    Defines an ellipse glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the center.
        
        y: int, float or callable
            Specifies the y-coordinate of the center.
        
        width: int, float or callable
            Specifies the full width.
        
        height: int, float or callable
            Specifies the full height.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    width = NumProperty(UNDEF)
    height = NumProperty(UNDEF)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_ellipse(x, y, width, height)


class Line(Glyph):
    """
    Defines a line glyph.
    
    Properties:
        
        x1: int, float or callable
            Specifies the x-coordinate of the start.
        
        y1: int, float or callable
            Specifies the y-coordinate of the start.
        
        x2: int, float or callable
            Specifies the x-coordinate of the end.
        
        y2: int, float or callable
            Specifies the y-coordinate of the end.
        
        line properties:
            Includes pero.LineProperties to specify the line.
    """
    
    x1 = NumProperty(0)
    y1 = NumProperty(0)
    x2 = NumProperty(0)
    y2 = NumProperty(0)
    
    line = Include(LineProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x1 = self.get_property('x1', source, overrides)
        y1 = self.get_property('y1', source, overrides)
        x2 = self.get_property('x2', source, overrides)
        y2 = self.get_property('y2', source, overrides)
        
        # set pen
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_line(x1, y1, x2, y2)


class Polygon(Glyph):
    """
    Defines a poly-line glyph.
    
    Properties:
        
        points: ((int, int),),  ((float, float),), callable, None or UNDEF
            Specifies the points as a sequence of (x,y) coordinates.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    points = TupleProperty(UNDEF, nullable=True)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        points = self.get_property('points', source, overrides)
        
        # check data
        if not points:
            return
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_polygon(points)


class Ray(Glyph):
    """
    Defines a ray glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the origin.
        
        y: int, float or callable
            Specifies the y-coordinate of the origin.
        
        length: int, float or callable
            Specifies the line length.
        
        offset: int, float, callable or UNDEF
            Specifies the shift from the origin while keeping the length and
            angle.
        
        angle properties:
            Includes pero.AngleProperties to specify the line angle.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    length = NumProperty(UNDEF)
    offset = NumProperty(0)
    angle = Include(AngleProperties)
    
    line = Include(LineProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        length = self.get_property('length', source, overrides)
        offset = self.get_property('offset', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE.RAD, source, overrides)
        
        # get offset
        if not offset:
            offset = 0
        
        # calc end point
        if angle:
            x = x + offset * math.cos(angle)
            y = y + offset * math.sin(angle)
            x2 = x + length * math.cos(angle)
            y2 = y + length * math.sin(angle)
        else:
            x = x + offset
            x2 = x + length
            y2 = y
        
        # set pen
        canvas.set_pen_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_line(x, y, x2, y2)


class Rect(Glyph):
    """
    Defines a rectangle glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        width: int, float or callable
            Specifies the full width.
        
        height: int, float or callable
            Specifies the full height.
        
        radius: int, float, (int,), (float,) callable or UNDEF
            Specifies the corner radius as a single value or values for
            individual corners starting from top-left.
        
        centered: bool or callable
            Specifies the anchor position. If set to True the anchor is meant
            to be the rectangle center while False means the top-left corner.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    width = NumProperty(UNDEF)
    height = NumProperty(UNDEF)
    
    radius = QuadProperty(0)
    centered = BoolProperty(False)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        centered = self.get_property('centered', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        radius = self.get_property('radius', source, overrides)
        
        # calc origin
        if centered:
            x = x - 0.5*width
            y = y - 0.5*height
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_rect(x, y, width, height, radius)


class Shape(Glyph):
    """
    Defines a path-based glyph.
    
    Properties:
        
        path: pero.Path, callable, None or UNDEF
            Specifies the path to be drawn.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    path = Property(UNDEF, types=(Path,), nullable=True)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        path = self.get_property('path', source, overrides)
        
        # check data
        if not path:
            return
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)


class Text(Glyph):
    """
    Defines a text glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        angle properties:
            Includes pero.AngleProperties to specify the text angle.
        
        text: str, callable, None or UNDEF
            Specifies the text to be drawn.
        
        text properties:
            Includes pero.TextProperties to specify the font.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    angle = Include(AngleProperties)
    
    text = StringProperty(UNDEF)
    font = Include(TextProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        text = self.get_property('text', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE.RAD, source, overrides)
        
        # check data
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_text(text, x, y, angle)


class Textbox(Text):
    """
    Defines a text box glyph.
    
    Properties:
        
        radius: int, float, (int,), (float,) callable or UNDEF
            Specifies the corner radius as a single value or values for
            individual corners starting from top-left.
        
        padding: int, float, (int,), (float,) callable or UNDEF
            Specifies the inner space as a single value or values for individual
            sides starting from top.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    radius = QuadProperty(0)
    padding = QuadProperty(5)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        radius = self.get_property('radius', source, overrides)
        padding = self.get_property('padding', source, overrides)
        text = self.get_property('text', source, overrides)
        align = self.get_property('text_align', source, overrides)
        base = self.get_property('text_base', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE.RAD, source, overrides)
        
        # check data
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # get text size
        text_width, text_height = canvas.get_text_size(text)
        
        # get padding
        if not padding:
            padding = (0,0,0,0)
        
        # get background coords
        bgr_x = x
        bgr_y = y
        bgr_width = text_width + padding[1] + padding[3]
        bgr_height = text_height + padding[0] + padding[2]
        
        if align == TEXT_ALIGN.RIGHT:
            bgr_x -= bgr_width
        elif align == TEXT_ALIGN.CENTER:
            bgr_x -= 0.5*bgr_width
        
        if base == TEXT_BASELINE.BOTTOM:
            bgr_y -= bgr_height
        elif base == TEXT_BASELINE.MIDDLE:
            bgr_y -= 0.5*bgr_height
        
        # get text coords
        text_x = 0
        text_y = 0
        
        if align == TEXT_ALIGN.LEFT:
            text_x += padding[3]
        elif align == TEXT_ALIGN.CENTER:
            text_x += 0.5*(padding[3] - padding[1])
        elif align == TEXT_ALIGN.RIGHT:
            text_x += - padding[1]
        
        if base == TEXT_BASELINE.TOP:
            text_y += padding[0]
        elif base == TEXT_BASELINE.MIDDLE:
            text_y += 0.5*(padding[0] - padding[2])
        elif base == TEXT_BASELINE.BOTTOM:
            text_y += - padding[2]
        
        if angle:
            x_shift = text_x * math.cos(angle) - text_y * math.sin(angle)
            y_shift = text_x * math.sin(angle) + text_y * math.cos(angle)
            text_x = x_shift
            text_y = y_shift
        
        text_x += x
        text_y += y
        
        # get radius
        if not radius:
            radius = (0,0,0,0)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # start drawing group
        canvas.group(tag, "textbox")
        
        # draw angled rect
        if angle:
            path = Path()
            path.rect(bgr_x, bgr_y, bgr_width, bgr_height, radius)
            path.transform(Matrix().rotate(angle, x, y))
            canvas.draw_path(path)
        
        # strait rectangle
        else:
            canvas.draw_rect(bgr_x, bgr_y, bgr_width, bgr_height, radius)
        
        # draw text
        canvas.draw_text(text, x=text_x, y=text_y, angle=angle)
        
        # end drawing group
        canvas.ungroup()


class Wedge(Glyph):
    """
    Defines a wedge glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the center.
        
        y: int, float or callable
            Specifies the y-coordinate of the center.
        
        offset: int, float, callable or UNDEF
            Specifies the shift from the center in the direction of an angle
            between start angle and end angle.
        
        inner_radius: int, float or callable
            Specifies the inner radius.
        
        outer_radius: int, float or callable
            Specifies the outer radius.
        
        start_angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        end_angle properties:
            Includes pero.AngleProperties to specify the end angle.
        
        clockwise: bool or callable
            Specifies the drawing direction. If set to True the arc is drawn
            clockwise, otherwise anti-clockwise.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    offset = NumProperty(0)
    
    inner_radius = NumProperty(UNDEF)
    outer_radius = NumProperty(UNDEF)
    
    start_angle = Include(AngleProperties, prefix="start_")
    end_angle = Include(AngleProperties, prefix="end_")
    clockwise = BoolProperty(True)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        start_angle = AngleProperties.get_angle(self, 'start_', ANGLE.RAD, source, overrides)
        end_angle = AngleProperties.get_angle(self, 'end_', ANGLE.RAD, source, overrides)
        inner_radius = self.get_property('inner_radius', source, overrides)
        outer_radius = self.get_property('outer_radius', source, overrides)
        clockwise = self.get_property('clockwise', source, overrides)
        offset = self.get_property('offset', source, overrides)
        
        # apply offset
        if offset:
            offset_angle = (end_angle + start_angle) * 0.5
            x += math.cos(offset_angle) * offset
            y += math.sin(offset_angle) * offset
        
        # init path
        path = Path()
        
        # skip drawing
        if start_angle == end_angle:
            pass
        
        # draw as annulus
        elif start_angle % (2 * math.pi) == end_angle % (2 * math.pi):
            path.circle(x, y, outer_radius)
            if inner_radius:
                path.circle(x, y, inner_radius)
        
        # draw as wedge
        else:
            path.arc(x, y, outer_radius, start_angle, end_angle, clockwise)
            path.line_to(x + inner_radius*math.cos(end_angle), y + inner_radius*math.sin(end_angle))
            if inner_radius:
                path.arc_around(x, y, start_angle, not clockwise)
            path.close()
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw path
        canvas.draw_path(path)
