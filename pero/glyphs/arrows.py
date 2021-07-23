#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import Matrix, Path
from . glyph import Glyph
from . heads import HeadProperty


class Arrow(Glyph):
    """
    Abstract base class for various types of arrow glyphs. An arrow is drawn as
    a simple strait or curved line having optional heads at each side.
    
    When the 'source' argument is provided for drawing it is also submitted to
    the drawing of the heads, together with relevant overrides so it will be
    used for any dynamic property of the head. Note that the 'x', 'y' and
    'angle' properties of the heads are determined by the arrow itself and
    cannot be overwritten.
    
    Properties:
        
        start_head: pero.Head, pero.HEAD, callable, None or UNDEF
            Specifies the head glyph to be drawn at the beginning or the arrow.
            The value can be specified by any item from the pero.HEAD enum or
            pero.Head instance.
        
        end_head: pero.Head, pero.HEAD, callable, None or UNDEF
            Specifies the head glyph to be drawn at the end or the arrow. The
            value can be specified by any item from the pero.HEAD enum or
            pero.Head instance.
        
        line properties:
            Includes pero.LineProperties to specify the arrow line.
        
        fill properties:
            Includes pero.FillProperties to specify the arrow fill.
    """
    
    start_head = HeadProperty(UNDEF, nullable=True)
    end_head = HeadProperty(UNDEF, nullable=True)
    
    line = Include(LineProperties, line_color=UNDEF)
    fill = Include(FillProperties, fill_color=UNDEF)
    
    
    def draw_heads(self, canvas, source=UNDEF, **overrides):
        """Draws arrow heads into given canvas."""
        
        # get properties
        start_head = self.get_property('start_head', source, overrides)
        end_head = self.get_property('end_head', source, overrides)
        
        # draw start head
        if start_head:
            
            canvas.set_pen_by(self, source=source, overrides=overrides)
            canvas.set_brush_by(self, source=source, overrides=overrides)
            
            head_overrides = self.get_child_overrides('start_head', overrides)
            start_head.draw(canvas, source=source, **head_overrides)
        
        # draw end head
        if end_head:
            
            canvas.set_pen_by(self, source=source, overrides=overrides)
            canvas.set_brush_by(self, source=source, overrides=overrides)
            
            head_overrides = self.get_child_overrides('end_head', overrides)
            end_head.draw(canvas, source=source, **head_overrides)
    
    
    @staticmethod
    def create(symbol, **overrides):
        """
        Initializes a new instance of arrow according to given definition. The
        definition consists of the arrow type symbol surrounded by optional
        heads at both ends (e.g.'<->'). The arrow symbol must be an item from
        the pero.ARROW enum and it is required. The optional symbols for
        individual heads can be specified as an item from the pero.HEAD enum.
        
        Args:
            symbol: str
                Arrow definition.
        
        Returns:
            pero.Arrow
                Initialized arrow.
        """
        
        # get arrow type
        arrow_type = None
        for arrow in ARROW:
            if arrow in symbol:
                arrow_type = arrow
                break
        
        if arrow_type is None:
            raise ValueError("Unknown arrow style! -> '%s'" % symbol)
        
        # split symbol into heads
        start_head, end_head = symbol.split(arrow_type)
        
        # set heads
        if 'start_head' not in overrides:
            if start_head and start_head not in HEAD:
                raise ValueError("Unknown start head! -> '%s'" % symbol)
            overrides['start_head'] = start_head or None
        
        if 'end_head' not in overrides:
            if end_head and end_head not in HEAD:
                raise ValueError("Unknown end head! -> '%s'" % symbol)
            overrides['end_head'] = end_head or None
        
        # init arrow
        if arrow_type == ARROW_ARC:
            return ArcArrow(**overrides)
        
        elif arrow_type == ARROW_CONNECT_LINE:
            return ConnectorArrow(**overrides)
        
        elif arrow_type == ARROW_CONNECT_CURVE:
            if 'curve' not in overrides:
                overrides['curve'] = .85
            return ConnectorArrow(**overrides)
        
        elif arrow_type == ARROW_CURVE:
            return CurveArrow(**overrides)
        
        elif arrow_type == ARROW_LINE:
            return LineArrow(**overrides)
        
        elif arrow_type == ARROW_BOW:
            return BowArrow(**overrides)
        
        elif arrow_type == ARROW_RAY:
            return RayArrow(**overrides)


class ArcArrow(Arrow):
    """
    This type of arrow is drawn as a simple circular arc defined by its center
    coordinates, start and end angles and the drawing direction.
    
    Properties:
        
        x: int, float, callable
            Specifies the x-coordinate of the arc center.
        
        y: int, float, callable
            Specifies the y-coordinate of the arc center.
        
        radius: int, float, callable
            Specifies the arc radius.
        
        clockwise: bool, callable
            Specifies the drawing direction. If set to True the arc is drawn
            clockwise, otherwise anti-clockwise.
        
        start_angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        end_angle properties:
            Includes pero.AngleProperties to specify the end angle.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    radius = NumProperty(0)
    clockwise = BoolProperty(True)
    start_angle = Include(AngleProperties, prefix="start")
    end_angle = Include(AngleProperties, prefix="end")
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw arrow."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        start_angle = AngleProperties.get_angle(self, 'start_', ANGLE_RAD, source, overrides)
        end_angle = AngleProperties.get_angle(self, 'end_', ANGLE_RAD, source, overrides)
        radius = self.get_property('radius', source, overrides)
        clockwise = self.get_property('clockwise', source, overrides)
        
        # make path
        path = Path()
        path.arc(x, y, radius, start_angle, end_angle, clockwise)
        
        # get coordinates
        x1 = x + radius * math.cos(start_angle)
        y1 = y + radius * math.sin(start_angle)
        x2 = x + radius * math.cos(end_angle)
        y2 = y + radius * math.sin(end_angle)
        
        direction = 1 if clockwise else -1
        start_angle = start_angle - 0.5*math.pi * direction
        end_angle = end_angle + 0.5*math.pi * direction
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "arrow")
        
        # draw path
        canvas.draw_path(path)
        
        # draw heads
        self.draw_heads(canvas,
            source = source,
            start_head_x = x1,
            start_head_y = y1,
            start_head_angle = start_angle,
            start_head_angle_units = ANGLE_RAD,
            end_head_x = x2,
            end_head_y = y2,
            end_head_angle = end_angle,
            end_head_angle_units = ANGLE_RAD,
            **overrides)
        
        # end drawing group
        canvas.ungroup()


class BowArrow(Arrow):
    """
    This type of arrow is drawn as a simple circular arc defined by its start
    and end coordinates, expected radius and the drawing direction.
    
    Properties:
        
        x1: int, float, callable
            Specifies the x-coordinate of the arrow start.
        
        y1: int, float, callable
            Specifies the y-coordinate of the arrow start.
        
        x2: int, float, callable
            Specifies the x-coordinate of the arrow end.
        
        y2: int, float, callable
            Specifies the y-coordinate of the arrow end.
        
        radius: int, float, callable
            Specifies the arc radius.
        
        large: bool
            Specifies which of the possible arcs will be drawn.
        
        clockwise: bool, callable
            Specifies the drawing direction. If set to True the arc is drawn
            clockwise, otherwise anti-clockwise.
    """
    
    x1 = NumProperty(0)
    y1 = NumProperty(0)
    x2 = NumProperty(0)
    y2 = NumProperty(0)
    radius = NumProperty(0)
    large = BoolProperty(False)
    clockwise = BoolProperty(True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw arrow."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x1 = self.get_property('x1', source, overrides)
        y1 = self.get_property('y1', source, overrides)
        x2 = self.get_property('x2', source, overrides)
        y2 = self.get_property('y2', source, overrides)
        radius = self.get_property('radius', source, overrides)
        large = self.get_property('large', source, overrides)
        clockwise = self.get_property('clockwise', source, overrides)
        
        # make path
        path = Path()
        path.move_to(x1, y1)
        path.bow_to(x2, y2, radius, large, clockwise)
        
        # get edge angles
        start_angle = path.start_angle() - math.pi
        end_angle = path.end_angle()
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "arrow")
        
        # draw path
        canvas.draw_path(path)
        
        # draw heads
        self.draw_heads(canvas,
            source = source,
            start_head_x = x1,
            start_head_y = y1,
            start_head_angle = start_angle,
            start_head_angle_units = ANGLE_RAD,
            end_head_x = x2,
            end_head_y = y2,
            end_head_angle = end_angle,
            end_head_angle_units = ANGLE_RAD,
            **overrides)
        
        # end drawing group
        canvas.ungroup()


class ConnectorArrow(Arrow):
    """
    This type of arrow is typically used to draw connections in node diagrams.
    It is drawn as a stepped-line or curve between two end points, with the
    heads facing left/right or up/down according to the 'orientation' property.
    
    Properties:
        
        x1: int, float, callable
            Specifies the x-coordinate of the arrow start.
        
        y1: int, float, callable
            Specifies the y-coordinate of the arrow start.
        
        x2: int, float, callable
            Specifies the x-coordinate of the arrow end.
        
        y2: int, float, callable
            Specifies the y-coordinate of the arrow end.
        
        orientation: pero.ORIENTATION, callable
            Specifies the main orientation of the line and heads as any item
            from the pero.ORIENTATION enum.
        
        pivot: float, callable
            Specifies the relative position of the connection line pivot point
            as a value between 0 and 1, where 0 means the arrow start, while 1
            means the arrow end. If set to 0 or 1 exactly, the arrow changes to
            simple L-shape line instead of Z-shape line.
        
        curve: float, callable
            Specifies the force used to curve the connection line as a value
            between 0 and 1, where 0 means strait line, while 1 means
            fully curved line.
    """
    
    x1 = NumProperty(0)
    y1 = NumProperty(0)
    x2 = NumProperty(0)
    y2 = NumProperty(0)
    
    orientation = EnumProperty(ORI_HORIZONTAL, enum=ORIENTATION)
    pivot = RangeProperty(0.5, minimum=0, maximum=1)
    curve = RangeProperty(0, minimum=0, maximum=1)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw arrow."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x1 = self.get_property('x1', source, overrides)
        y1 = self.get_property('y1', source, overrides)
        x2 = self.get_property('x2', source, overrides)
        y2 = self.get_property('y2', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        pivot = self.get_property('pivot', source, overrides)
        curve = self.get_property('curve', source, overrides)
        
        # get curvature
        curvature = 2*curve if curve else 1
        
        # get coords
        if orientation == ORI_HORIZONTAL:
            cx1 = x1 + min(1, curvature*pivot)*(x2-x1)
            cy1 = y1
            cx2 = x2 - min(1, curvature*(1-pivot))*(x2-x1)
            cy2 = y2
        
        else:
            cx1 = x1
            cy1 = y1 + min(1, curvature*pivot)*(y2-y1)
            cx2 = x2
            cy2 = y2 - min(1, curvature*(1-pivot))*(y2-y1)
        
        # get angles
        if x1 == cx1 and y1 == cy1:
            start_angle = math.atan2(y1-cy2, x1-cx2)
            end_angle = math.atan2(y2-cy2, x2-cx2)
        
        elif x2 == cx2 and y2 == cy2:
            start_angle = math.atan2(y1-cy1, x1-cx1)
            end_angle = math.atan2(y2-cy1, x2-cx1)
        
        else:
            start_angle = math.atan2(y1-cy1, x1-cx1)
            end_angle = math.atan2(y2-cy2, x2-cx2)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "arrow")
        
        # draw line
        if curve == 0:
            canvas.draw_lines(((x1, y1), (cx1, cy1), (cx2, cy2), (x2, y2)))
        
        # draw curve
        else:
            path = Path()
            path.move_to(x1, y1)
            path.curve_to(cx1, cy1, cx2, cy2, x2, y2)
            canvas.draw_path(path)
        
        # draw heads
        self.draw_heads(canvas,
            source = source,
            start_head_x = x1,
            start_head_y = y1,
            start_head_angle = start_angle,
            start_head_angle_units = ANGLE_RAD,
            end_head_x = x2,
            end_head_y = y2,
            end_head_angle = end_angle,
            end_head_angle_units = ANGLE_RAD,
            **overrides)
        
        # end drawing group
        canvas.ungroup()


class CurveArrow(Arrow):
    """
    This type of arrow is drawn as a Bezier curve between two anchor points.
    Unlike for normal curve, the control points are defined by relative position
    between anchor points.
    
    Properties:
        
        x1: int, float, callable
            Specifies the x-coordinate of the arrow start.
        
        y1: int, float, callable
            Specifies the y-coordinate of the arrow start.
        
        x2: int, float, callable
            Specifies the x-coordinate of the arrow end.
        
        y2: int, float, callable
            Specifies the y-coordinate of the arrow end.
        
        cx1: int, float, callable
            Specifies the relative x-coordinate of the arrow start control point
            as a value between 0 and 1, where 0 means the arrow start, while 1
            means the arrow end.
        
        cy1: int, float, callable
            Specifies the relative y-coordinate of the arrow start control point
            as a value between 0 and 1, where 0 means the arrow start, while 1
            means the arrow end.
        
        cx2: int, float, callable
            Specifies the relative x-coordinate of the arrow end control point
            as a value between 0 and 1, where 0 means the arrow end, while 1
            means the arrow start.
        
        cy2: int, float, callable
            Specifies the relative y-coordinate of the arrow end control point
            as a value between 0 and 1, where 0 means the arrow end, while 1
            means the arrow start.
    """
    
    x1 = NumProperty(0)
    y1 = NumProperty(0)
    x2 = NumProperty(0)
    y2 = NumProperty(0)
    
    cx1 = NumProperty(0.85)
    cy1 = NumProperty(0.25)
    cx2 = NumProperty(0.85)
    cy2 = NumProperty(0.25)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw arrow."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x1 = self.get_property('x1', source, overrides)
        y1 = self.get_property('y1', source, overrides)
        x2 = self.get_property('x2', source, overrides)
        y2 = self.get_property('y2', source, overrides)
        cx1 = self.get_property('cx1', source, overrides)
        cy1 = self.get_property('cy1', source, overrides)
        cx2 = self.get_property('cx2', source, overrides)
        cy2 = self.get_property('cy2', source, overrides)
        
        # calc absolute coords
        cx1 = x1 + cx1*(x2 - x1)
        cx2 = x2 - cx2*(x2 - x1)
        cy1 = y1 + cy1*(y2 - y1)
        cy2 = y2 - cy2*(y2 - y1)
        
        # make path
        path = Path()
        path.move_to(x1, y1)
        path.curve_to(cx1, cy1, cx2, cy2, x2, y2)
        
        # get angles
        start_angle = path.start_angle() + math.pi
        end_angle = path.end_angle()
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "arrow")
        
        # draw path
        canvas.draw_path(path)
        
        # draw heads
        self.draw_heads(canvas,
            source = source,
            start_head_x = x1,
            start_head_y = y1,
            start_head_angle = start_angle,
            start_head_angle_units = ANGLE_RAD,
            end_head_x = x2,
            end_head_y = y2,
            end_head_angle = end_angle,
            end_head_angle_units = ANGLE_RAD,
            **overrides)
        
        # end drawing group
        canvas.ungroup()


class LineArrow(Arrow):
    """
    This type of arrow is drawn as a strait line between two end points.
    
    Properties:
        
        x1: int, float, callable
            Specifies the x-coordinate of the arrow start.
        
        y1: int, float, callable
            Specifies the y-coordinate of the arrow start.
        
        x2: int, float, callable
            Specifies the x-coordinate of the arrow end.
        
        y2: int, float, callable
            Specifies the y-coordinate of the arrow end.
    """
    
    x1 = NumProperty(0)
    y1 = NumProperty(0)
    x2 = NumProperty(0)
    y2 = NumProperty(0)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x1 = self.get_property('x1', source, overrides)
        y1 = self.get_property('y1', source, overrides)
        x2 = self.get_property('x2', source, overrides)
        y2 = self.get_property('y2', source, overrides)
        
        # get angle
        angle = math.atan2(y2-y1, x2-x1)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "arrow")
        
        # draw line
        canvas.draw_line(x1, y1, x2, y2)
        
        # set brush
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw heads
        self.draw_heads(canvas,
            source = source,
            start_head_x = x1,
            start_head_y = y1,
            start_head_angle = angle+math.pi,
            start_head_angle_units = ANGLE_RAD,
            end_head_x = x2,
            end_head_y = y2,
            end_head_angle = angle,
            end_head_angle_units = ANGLE_RAD,
            **overrides)
        
        # end drawing group
        canvas.ungroup()


class PathArrow(Arrow):
    """
    This type of arrow is drawn as a given path rotated and scaled the way that
    its end points fit into arrow start and end.
    
    Properties:
        
        x1: int, float, callable
            Specifies the x-coordinate of the arrow start.
        
        y1: int, float, callable
            Specifies the y-coordinate of the arrow start.
        
        x2: int, float, callable
            Specifies the x-coordinate of the arrow end.
        
        y2: int, float, callable, None or UNDEF
            Specifies the y-coordinate of the arrow end.
        
        path: pero.Path, callable
            Specifies the path.
    """
    
    x1 = NumProperty(0)
    y1 = NumProperty(0)
    x2 = NumProperty(0)
    y2 = NumProperty(0)
    
    path = Property(UNDEF, types=(Path,), nullable=True)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw arrow."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x1 = self.get_property('x1', source, overrides)
        y1 = self.get_property('y1', source, overrides)
        x2 = self.get_property('x2', source, overrides)
        y2 = self.get_property('y2', source, overrides)
        path = self.get_property('path', source, overrides)
        
        # check data
        if not path:
            return
        
        # get path endpoints
        p1x, p1y = path.start()
        p2x, p2y = path.end()
        path_length = math.sqrt((p2x-p1x)**2 + (p2y-p1y)**2)
        
        # init matrix
        matrix = Matrix()
        
        # strait path
        angle = math.atan2(p2y-p1y, p2x-p1x)
        matrix.translate(-p1x, -p1y)
        matrix.rotate(-angle)
        
        # scale to final arrow
        length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        scale = length/path_length
        matrix.scale(scale, scale)
        
        # rotate to final arrow
        angle = math.atan2(y2-y1, x2-x1)
        matrix.rotate(angle)
        
        # move to final position
        matrix.translate(x1, y1)
        
        # apply to path
        path = path.transformed(matrix)
        
        # get angles
        start_angle = path.start_angle() + math.pi
        end_angle = path.end_angle()
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "arrow")
        
        # draw path
        canvas.draw_path(path)
        
        # draw heads
        self.draw_heads(canvas,
            source = source,
            start_head_x = x1,
            start_head_y = y1,
            start_head_angle = start_angle,
            start_head_angle_units = ANGLE_RAD,
            end_head_x = x2,
            end_head_y = y2,
            end_head_angle = end_angle,
            end_head_angle_units = ANGLE_RAD,
            **overrides)
        
        # end drawing group
        canvas.ungroup()


class RayArrow(Arrow):
    """
    This type of arrow is drawn as a strait line with specified origin, length
    and angle.
    
    Properties:
        
        x: int, float, callable
            Specifies the x-coordinate of the arrow origin.
        
        y: int, float, callable
            Specifies the y-coordinate of the arrow origin.
        
        length: int, float, callable
            Specifies the full arrow length.
        
        angle properties:
            Includes pero.AngleProperties to specify the line angle.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    length = NumProperty(0)
    angle = Include(AngleProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x1 = self.get_property('x', source, overrides)
        y1 = self.get_property('y', source, overrides)
        length = self.get_property('length', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # calc end point
        x2 = x1 + length * math.cos(angle)
        y2 = y1 + length * math.sin(angle)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # start drawing group
        canvas.group(tag, "arrow")
        
        # draw line
        canvas.draw_line(x1, y1, x2, y2)
        
        # draw heads
        self.draw_heads(canvas,
            source = source,
            start_head_x = x1,
            start_head_y = y1,
            start_head_angle = angle+math.pi,
            start_head_angle_units = ANGLE_RAD,
            end_head_x = x2,
            end_head_y = y2,
            end_head_angle = angle,
            end_head_angle_units = ANGLE_RAD,
            **overrides)
        
        # end drawing group
        canvas.ungroup()
