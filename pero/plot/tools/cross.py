#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ...enums import *
from ...properties import *
from ...backends import Tool
from ..enums import PLOT_TAG


class CrossTool(Tool):
    """
    This tool shows current cursor position within a plot as horizontal,
    vertical or cross line together with a tooltip showing values in real data
    units for specified 'axes'. If the 'axes' property is defined, only the
    selected axes will be used and shown, otherwise all visible axes will be
    used.
    
    The tooltip value formatting is done by using the 'format' method of each
    axis. See the Axis documentation for more information.
    
    Properties:
        
        axes: tuple or UNDEF
            Specifies the collection of axes for which the position should be
            displayed. If set to UNDEF all visible axes are used.
        
        line properties:
            Includes pero.LineProperties to specify the cursor lines.
    """
    
    axes = TupleProperty(UNDEF, intypes=(str,), dynamic=False)
    line = Include(LineProperties, dynamic=False, line_color="#5559")
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        # check keys
        if self.keys:
            return
        
        # check buttons
        if evt.left_down or evt.right_down or evt.middle_down:
            return
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get location
        obj = plot.get_obj_below(evt.x_pos, evt.y_pos)
        
        # cancel event
        if obj != PLOT_TAG:
            evt.control.draw_overlay()
            return
        
        # draw position
        evt.control.draw_overlay(self._draw_position, evt=evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def _get_axes(self, evt):
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
        
        return axes
    
    
    def _get_tooltip(self, x, y, axes):
        """Gets tooltip text."""
        
        labels = []
        
        # get label for each axis
        for axis in axes:
            
            # get value
            value = x if axis.position in (POS_BOTTOM, POS_TOP) else y
            value = axis.scale.invert(value)
            
            # format value
            label = axis.format(value)
            
            # add label
            if label:
                labels.append(label)
        
        # finalize tooltip text
        return "\n".join(labels)
    
    
    def _draw_position(self, canvas, evt):
        """Draws cursor position and tooltip."""
        
        # get plot
        plot = evt.control.graphics
        
        # get coords
        x, y = evt.x_pos, evt.y_pos
        frame = plot.get_frame(PLOT_TAG)
        
        # get axes
        axes = self._get_axes(evt)
        if not axes:
            return
        
        # set cursor
        evt.control.set_cursor(CURSOR_BLANK)
        
        # set pen
        canvas.set_pen_by(self)
        
        # draw horizontal line
        if any(a.position in (POS_LEFT, POS_RIGHT) for a in axes):
            canvas.draw_line(frame.x1, y, frame.x2, y)
        
        # draw vertical line
        if any(a.position in (POS_TOP, POS_BOTTOM) for a in axes):
            canvas.draw_line(x, frame.y1, x, frame.y2)
        
        # get tooltip text
        text = self._get_tooltip(x, y, axes)
        if not text:
            return
        
        # draw tooltip
        evt.control.draw_tooltip(canvas, x=x, y=y, text=text, clip=frame)
