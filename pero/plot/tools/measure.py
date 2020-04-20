#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ...enums import *
from ...properties import *
from ...backends import Tool
from ..enums import *


class MeasureTool(Tool):
    """
    
    This tool provides a simple distance measurements across specified 'axes'
    and shows vertical or horizontal lines together with tooltip showing
    particular distance in real data units. If the 'axes' property is defined,
    only the selected axes will be used and shown, otherwise all visible axes
    will be used.
    
    By setting the 'mode' property the measurement can be limited to particular
    orientation (x or y) or automatically selected according to current main
    direction of mouse movement.
    
    The tooltip value formatting is done by using the 'format' method of each
    axis. See the Axis documentation for more information.
    
    Properties:
        
        axes: tuple or UNDEF
            Specifies the collection of axes for which the distance should be
            displayed. If set to UNDEF all visible axes are used.
        
        mode: pero.plot.MEASURE_MODE
            Specifies the measurement direction as any value from the
            pero.plot.MEASURE_MODE enum.
        
        line properties:
            Includes pero.LineProperties to specify the cursor lines.
    """
    
    axes = TupleProperty(UNDEF, intypes=(str,), dynamic=False)
    mode = EnumProperty(MEASURE_AUTO, enum=MEASURE_MODE, dynamic=False)
    line = Include(LineProperties, dynamic=False, line_color="#5559")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of MeasureTool."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._is_active = False
        self._dragging = None
    
    
    def on_key_down(self, evt):
        """Handles key-down event."""
        
        # remember key
        self.add_key(evt.key)
        
        # check if active
        if not self._is_active:
            return
        
        # escape current event
        if evt.key == KEY_ESC:
            self._escape_event(evt)
            evt.cancel()
    
    
    def on_mouse_leave(self, evt):
        """Handles mouse-leave event."""
        
        # clear keys
        self.clear_keys()
        
        # check if active
        if not self._is_active:
            return
        
        # cancel current tool event
        self._escape_event(evt)
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        # check if active
        if not self._is_active:
            return
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        
        # draw distance
        if obj == PLOT_TAG:
            evt.control.draw_overlay(self._draw_distance, evt=evt)
        
        # clear overlay
        else:
            evt.control.draw_overlay()
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_down(self, evt):
        """Handles mouse-button-down event."""
        
        # check keys
        if self.keys:
            return
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # check location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        if obj != PLOT_TAG:
            return
        
        # set as active
        self._is_active = True
        
        # remember dragging origin
        self._dragging = (evt.x_pos, evt.y_pos)
        
        # draw distance
        evt.control.draw_overlay(self._draw_distance, evt=evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_up(self, evt):
        """Handles mouse-button-up event."""
        
        # check if active
        if not self._is_active:
            return
        
        # cancel event
        self._escape_event(evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def _get_axes(self, evt, x1, y1, x2, y2):
        """Gets relevant axes."""
        
        axes = []
        
        # get plot
        plot = evt.control.graphics
        
        # get all axes
        if self.axes is UNDEF:
            
            axes = [a for a in plot.axes]
            axes.sort(key = lambda a: a.z_index)
            
            buff = [a for a in axes if a.position == POS_BOTTOM]
            buff += [a for a in axes if a.position == POS_TOP]
            buff += [a for a in axes if a.position == POS_LEFT]
            buff += [a for a in axes if a.position == POS_RIGHT]
            
            axes = buff
        
        # get selected axes
        elif self.axes:
            axes = [plot.get_obj(a) for a in self.axes]
        
        # remove invisible
        axes = [a for a in axes if a.visible]
        
        # horizontal by mode
        if self.mode == MEASURE_X:
            axes = [a for a in axes if a.position in (POS_TOP, POS_BOTTOM)]
        
        # vertical by mode
        elif self.mode == MEASURE_Y:
            axes = [a for a in axes if a.position in (POS_LEFT, POS_RIGHT)]
        
        # horizontal by direction
        elif abs(x2-x1) >= abs(y2-y1):
            axes = [a for a in axes if a.position in (POS_TOP, POS_BOTTOM)]
        
        # vertical by direction
        else:
            axes = [a for a in axes if a.position in (POS_LEFT, POS_RIGHT)]
        
        return axes
    
    
    def _get_tooltip(self, v1, v2, axes):
        """Gets tooltip text."""
        
        labels = []
        
        # get labels for each axis
        for axis in axes:
            
            # calc values
            v1i = axis.scale.invert(v1)  # origin
            v2i = axis.scale.invert(v2)  # cursor
            absolute = v2i - v1i
            relative = absolute / v1i if v1i != 0 else None
            
            # format absolute distance
            label = axis.format(absolute)
            if not label:
                continue
            
            # format relative distance
            if not relative:
                pass
            
            elif abs(relative) < 1e-7:
                label += " (%.3f ppb)" % (relative * 1e9)
            
            elif abs(relative) < 1e-4:
                label += " (%.3f ppm)" % (relative * 1e6)
            
            else:
                label += " (%.3f %%)" % (relative * 1e2)
            
            # add label
            if label:
                labels.append(label)
        
        # finalize tooltip text
        return "\n".join(labels)
    
    
    def _escape_event(self, evt):
        """Cancels current tool event."""
        
        # set as inactive
        self._is_active = False
        
        # reset dragging origin
        self._dragging = None
        
        # clear overlay
        if evt.control:
            evt.control.draw_overlay()
    
    
    def _draw_distance(self, canvas, evt):
        """Draws distance ruler and tooltip."""
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get coords
        x1, y1 = self._dragging
        x2, y2 = evt.x_pos, evt.y_pos
        frame = plot.get_frame(PLOT_TAG)
        
        # check distance
        if x1 == x2 and y1 == y2:
            return
        
        # get axes
        axes = self._get_axes(evt, x1, y1, x2, y2)
        if not axes:
            return
        
        # get direction
        is_horizontal = any(a.position in (POS_TOP, POS_BOTTOM) for a in axes)
        
        # get relevant values
        v1, v2 = (x1, x2) if is_horizontal else (y1, y2)
        
        # set cursor
        evt.control.set_cursor(CURSOR_BLANK)
        
        # set pen
        canvas.set_pen_by(self)
        
        # draw lines
        if is_horizontal:
            canvas.draw_line(x1, frame.y1, x1, frame.y2)
            canvas.draw_line(x2, frame.y1, x2, frame.y2)
            canvas.draw_line(x1, y2, x2, y2)
        else:
            canvas.draw_line(frame.x1, y1, frame.x2, y1)
            canvas.draw_line(frame.x1, y2, frame.x2, y2)
            canvas.draw_line(x2, y1, x2, y2)
        
        # get tooltip text
        text = self._get_tooltip(v1, v2, axes)
        if not text:
            return
        
        # draw tooltip
        evt.control.draw_tooltip(canvas, x=x2, y=y2, text=text, clip=frame)
