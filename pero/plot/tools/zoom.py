#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ...enums import *
from ...properties import *
from ...events import ZoomEvt
from ...backends import Tool
from ..enums import *


class ZoomTool(Tool):
    """
    This tools provides a simple way to zoom axes ranges by selecting an area
    within a plot. By setting the 'mode' property the zooming can be limited to
    particular orientation (x or y) or automatically selected according to
    current main direction of mouse movement. If automatic mode is enabled the
    'switch' property defines the maximum ignorable movement to prefer just one
    zoom direction. If the 'undo' property is enable, any backwards mouse
    movement triggers zoom undo function to go to previously stored ranges.
    
    Properties:
        
        mode: pero.plot.ZOOM_MODE
            Specifies the allowed zooming direction as any value from the
            pero.plot.ZOOM_MODE enum.
        
        switch: int or float
            Specifies the maximum distance to keep zooming in the main direction
            of the cursor movement.
        
        undo: bool
            Specifies whether the zoom can be undone by dragging the mouse
            backwards.
        
        line properties:
            Includes pero.LineProperties to specify the selection outline.
        
        fill properties:
            Includes pero.FillProperties to specify the selection fill.
    """
    
    mode = EnumProperty(ZOOM_AUTO, enum=ZOOM_MODE, dynamic=False)
    switch = NumProperty(20, dynamic=False)
    undo = BoolProperty(True, dynamic=False)
    line = Include(LineProperties, dynamic=False, line_color="#bcee")
    fill = Include(FillProperties, dynamic=False, fill_color="#bce7")
    margin = QuadProperty(3, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of ZoomTool."""
        
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
        
        # draw zoom box
        evt.control.draw_overlay(self._draw_zoom_box, evt=evt)
        
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
        
        # draw zoom box
        evt.control.draw_overlay(self._draw_zoom_box, evt=evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_up(self, evt):
        """Handles mouse-button-up event."""
        
        # check if active
        if not self._is_active:
            return
        
        # zoom axes
        self._zoom_axes(evt)
        
        # cancel event
        self._escape_event(evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def _get_zoom_mode(self, evt, min_x, min_y, max_x, max_y):
        """Gets zoom mode according to settings and current selection."""
        
        # check preset mode
        if self.mode and self.mode != ZOOM_AUTO:
            return self.mode
        
        # get ranges
        x_range = abs(max_x - min_x)
        y_range = abs(max_y - min_y)
        
        # get switch
        switch = self.switch or 0
        
        # block switch if shift down
        if evt.shift_down:
            switch = 0
        
        # force switch if alt down
        if evt.alt_down:
            switch = float('inf')
        
        # get zoom mode by drag direction
        if x_range > switch and y_range > switch:
            return ZOOM_XY
        
        if x_range > y_range:
            return ZOOM_X
        
        if y_range > x_range:
            return ZOOM_Y
        
        return ZOOM_XY
    
    
    def _escape_event(self, evt):
        """Cancels current tool event."""
        
        # set as inactive
        self._is_active = False
        
        # reset dragging origin
        self._dragging = None
        
        # clear overlay
        if evt.control:
            evt.control.draw_overlay()
    
    
    def _zoom_axes(self, evt):
        """Zooms axes according to current selection."""
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get coords
        min_x, min_y = self._dragging
        max_x, max_y = evt.x_pos, evt.y_pos
        
        # check movement
        if min_x == max_x and min_y == max_y:
            return
        
        # undo last zoom
        if self.undo and min_x > max_x:
            self._zoom_back(evt)
            return
        
        # check coords
        if min_x > max_x:
            min_x, max_x = max_x, min_x
        if min_y > max_y:
            min_y, max_y = max_y, min_y
        
        # get zoom mode
        zoom_mode = self._get_zoom_mode(evt, min_x, min_y, max_x, max_y)
        
        # use zoom within plot frame
        frame = plot.get_frame(PLOT_TAG)
        
        if min_x < frame.x1:
            min_x = frame.x1
        if max_x > frame.x2:
            max_x = frame.x2
        
        if min_y < frame.y1:
            min_y = frame.y1
        if max_y > frame.y2:
            max_y = frame.y2
        
        # get axes
        axes = []
        
        # get all axes
        if zoom_mode == ZOOM_XY:
            axes = plot.axes
        
        # get horizontal axes
        elif zoom_mode == ZOOM_X:
            axes = [a for a in plot.axes if a.position in (POS_BOTTOM, POS_TOP)]
        
        # get vertical axes
        elif zoom_mode == ZOOM_Y:
            axes = [a for a in plot.axes if a.position in (POS_LEFT, POS_RIGHT)]
        
        # remove non-zoomable axes
        axes = [a for a in axes if not a.static and a.level <= 2]
        if not axes:
            return
        
        # zoom axes
        for axis in axes:
            
            # get range
            if axis.position in (POS_BOTTOM, POS_TOP):
                start, end = min_x, max_x
            else:
                start, end = max_y, min_y
            
            # recalculate range
            start = axis.scale.invert(start)
            end = axis.scale.invert(end)
            
            # finalize axis
            plot.finalize_axis(axis, start, end)
        
        # finalize zoom
        plot.finalize_zoom(axes)
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _zoom_back(self, evt):
        """Zooms back to previously stored ranges."""
        
        # check control
        if not evt.control:
            return
        
        # get coords
        x, y = self._dragging
        cursor = evt.x_pos
        
        # check coords
        switch = self.switch or 0
        if x <= cursor or (x - cursor) < switch:
            return
        
        # apply zoom back
        evt.control.zoom_back()
        
        # redraw plot
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _draw_zoom_box(self, canvas, evt):
        """Draws zoom box."""
        
        # check control
        if not evt.control:
            return
        
        # set cursor
        evt.control.set_cursor(CURSOR_ARROW)
        
        # get plot
        plot = evt.control.graphics
        
        # get coords
        min_x, min_y = self._dragging
        max_x, max_y = evt.x_pos, evt.y_pos
        
        # check movement
        if min_x == max_x and min_y == max_y:
            return
        
        # draw undo glyph
        if self.undo and min_x > max_x:
            self._draw_zoom_back(canvas, evt)
            return
        
        # check coords
        if min_x > max_x:
            min_x, max_x = max_x, min_x
        if min_y > max_y:
            min_y, max_y = max_y, min_y
        
        # get plot frame
        frame = plot.get_frame(PLOT_TAG)
        
        # apply margin
        if self.margin:
            frame = frame.clone()
            frame.shrink(*self.margin)
        
        # check box to be within plot frame
        if min_x < frame.x1:
            min_x = frame.x1
        if max_x > frame.x2:
            max_x = frame.x2
        
        if min_y < frame.y1:
            min_y = frame.y1
        if max_y > frame.y2:
            max_y = frame.y2
        
        # get zoom mode
        zoom_mode = self._get_zoom_mode(evt, min_x, min_y, max_x, max_y)
        
        # set zoom mode
        if zoom_mode == ZOOM_X:
            min_y = frame.y1
            max_y = frame.y2
        
        elif zoom_mode == ZOOM_Y:
            min_x = frame.x1
            max_x = frame.x2
        
        # set pen and brush
        canvas.set_pen_by(self)
        canvas.set_brush_by(self)
        
        # draw rectangle
        canvas.draw_rect(min_x, min_y, max_x-min_x, max_y-min_y)
    
    
    def _draw_zoom_back(self, canvas, evt):
        """Draws zoom back indicator."""
        
        # check control
        if not evt.control:
            return
        
        # get plot
        plot = evt.control.graphics
        
        # get coords
        x, y = self._dragging
        cursor = evt.x_pos
        
        # check coords
        switch = self.switch or 0
        if x <= cursor or (x - cursor) < switch:
            return
        
        # check line to be within plot frame
        frame = plot.get_frame(PLOT_TAG)
        if cursor < frame.x1:
            cursor = frame.x1
        
        # set pen and brush
        canvas.set_pen_by(self)
        canvas.set_brush_by(self)
        
        # draw back arrow
        canvas.draw_line(cursor, y, x, y)
        canvas.draw_polygon(((cursor-5, y), (cursor, y-4), (cursor, y+4)))
        canvas.draw_line(x, y-5, x, y+5)
