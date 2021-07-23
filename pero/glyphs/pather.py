#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *
from .. drawing import Path
from . glyph import Glyph
from . shapes import Line
from . markers import MarkerProperty, Circle


class Pather(Glyph):
    """
    Defines a utility glyph visualizing all the details of given path. This
    draws the path in a similar way as any vector graphic editor, showing all
    the anchors, control points and handles.
    
    Properties:
        
        path: pero.Path, callable, None or UNDEF
            Specifies the path to draw.
        
        show_anchors: bool, callable
            Specifies whether anchor points should be drawn.
        
        show_handles: bool, callable
            Specifies whether control points with handles should be drawn.
        
        show_cursor: bool, callable
            Specifies whether current cursor position should be drawn.
        
        anchor: pero.Marker, pero.MARKER, callable, None or UNDEF
            Specifies the marker glyph to draw the anchor points with. The value
            can be specified by any item from the pero.MARKER enum or as a
            pero.Marker instance.
        
        control: pero.Marker, pero.MARKER, callable, None or UNDEF
            Specifies the marker glyph to draw the control points with. The
            value can be specified by any item from the pero.MARKER enum or
            as a pero.Marker instance.
        
        cursor: pero.Marker, pero.MARKER, callable, None or UNDEF
            Specifies the marker glyph to draw the cursor position with. The
            value can be specified by any item from the pero.MARKER enum or
            as a pero.Marker instance.
        
        handle: pero.Line, callable, None or UNDEF
            Specifies the line glyph to draw the control handles with.
        
        line properties:
            Includes pero.LineProperties to specify the path outline.
        
        fill properties:
            Includes pero.FillProperties to specify the path fill.
    """
    
    show_anchors = BoolProperty(True)
    show_handles = BoolProperty(True)
    show_cursor = BoolProperty(True)
    
    path = Property(UNDEF, types=(Path,), nullable=True)
    
    anchor = MarkerProperty(UNDEF, nullable=True)
    control = MarkerProperty(UNDEF, nullable=True)
    cursor = MarkerProperty(UNDEF, nullable=True)
    handle = Property(UNDEF, types=(Line,), nullable=True)
    
    pen = Include(LineProperties, line_color="#000", line_width=1)
    brush = Include(FillProperties, fill_color="#ccc")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Pather."""
        
        # init markers
        if 'anchor' not in overrides:
            overrides['anchor'] = Circle(
                size = 8,
                line_color = "#fff",
                fill_color = "#000")
        
        if 'control' not in overrides:
            overrides['control'] = Circle(
                size = 6,
                line_color = None,
                fill_color = "#77f")
        
        if 'cursor' not in overrides:
            overrides['cursor'] = Circle(
                size = 6,
                line_color = None,
                fill_color = "#f00")
        
        if 'handle' not in overrides:
            overrides['handle'] = Line(
                line_color = "#77f")
        
        # init base
        super().__init__(**overrides)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        show_anchors = self.get_property('show_anchors', source, overrides)
        show_handles = self.get_property('show_handles', source, overrides)
        show_cursor = self.get_property('show_cursor', source, overrides)
        path = self.get_property('path', source, overrides)
        anchor = self.get_property('anchor', source, overrides)
        control = self.get_property('control', source, overrides)
        cursor = self.get_property('cursor', source, overrides)
        handle = self.get_property('handle', source, overrides)
        
        # check data
        if not path:
            return
        
        # get data
        handles = path.handles()
        anchors = path.anchors()
        
        # get overrides
        anchor_overrides = self.get_child_overrides('anchor', overrides)
        control_overrides = self.get_child_overrides('control', overrides)
        cursor_overrides = self.get_child_overrides('cursor', overrides)
        handle_overrides = self.get_child_overrides('handle', overrides)
        
        # start drawing group
        canvas.group(tag, "pather")
        
        # draw path
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        canvas.draw_path(path)
        
        # draw handles
        if show_handles and handle:
            canvas.group(None, "handles")
            for item in handles:
                handle.draw(canvas, x1=item[0], y1=item[1], x2=item[2], y2=item[3], **handle_overrides)
            canvas.ungroup()
        
        # draw anchors
        if show_anchors and anchor:
            canvas.group(None, "anchors")
            for item in anchors:
                anchor.draw(canvas, x=item[0], y=item[1], **anchor_overrides)
            canvas.ungroup()
        
        # draw controls
        if show_handles and control:
            canvas.group(None, "controls")
            for item in handles:
                control.draw(canvas, x=item[2], y=item[3], **control_overrides)
            canvas.ungroup()
        
        # draw cursor
        if show_cursor and cursor:
            cursor.draw(canvas, x=path.cursor[0], y=path.cursor[1], **cursor_overrides)
        
        # end drawing group
        canvas.ungroup()
