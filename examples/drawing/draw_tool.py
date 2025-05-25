#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
import pero


class AngleTool(pero.Tool):
    """A simple angle tool."""
    
    
    def __init__(self, **overrides):
        
        super().__init__(**overrides)
        
        # init values
        self._center = (0, 0)
        self._radius = 0
        self._offset = 0
        self._dragging = None
        self._is_measure = False
        self._is_rotate = False
        
        # init color scale
        self._gradient = pero.Gradient(pero.colors.YlOrRd)
        
        # init glyphs
        self._arrow = pero.RayArrow(
            start_head = pero.CircleHead(size=7),
            end_head = pero.CircleHead(size=7),
            line_color = pero.colors.Red,
            fill_color = pero.colors.Red)
        
        self._wedge = pero.Wedge(
            inner_radius = 0,
            start_angle = 0,
            line_color = None,
            fill_alpha = 170)
    
    
    def on_size(self, evt):
        """Handles window size event."""
        
        # get position
        margin = 30
        cx = evt.width/2
        cy = evt.height/2
        length = min(evt.width, evt.height)/2 - margin
        
        # update buffers
        self._center = (cx, cy)
        self._radius = length
        
        # update glyphs
        self._arrow.x = cx
        self._arrow.y = cy
        self._arrow.length = length
        
        self._wedge.x = cx
        self._wedge.y = cy
        self._wedge.outer_radius = length
    
    
    def on_mouse_down(self, evt):
        """Handles mouse-button-down event."""
        
        # skip if active
        if self._is_measure or self._is_rotate:
            return
        
        # get position
        x, y = evt.x_pos, evt.y_pos
        length = pero.distance(self._center, (x, y))
        
        # start measure
        if length <= self._radius:
            self._is_measure = True
        
        # start rotate
        else:
            self._is_rotate = True
            self._offset = evt.control.graphics.get_offset()
        
        # remember dragging
        self._dragging = (x, y)
    
    
    def on_mouse_up(self, evt):
        """Handles mouse-button-up event."""
        
        # cancel actions
        self._cancel_evt(evt)
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        # get position
        x, y = evt.x_pos, evt.y_pos
        length = pero.distance(self._center, (x, y))
        
        # set cursor
        self._set_cursor(evt, x, y)
        
        # measure angle
        if self._is_measure:
            evt.control.draw_overlay(self._draw_wedge, evt=evt, x=x, y=y)
        
        # rotate axis
        elif self._is_rotate:
            self._rotate_axis(evt, x, y)
        
        # draw current cursor
        elif length <= self._radius:
            evt.control.draw_overlay(self._draw_position, evt=evt, x=x, y=y)
        
        # clear overlay
        else:
            evt.control.clear_overlay()
    
    
    def on_mouse_leave(self, evt):
        """Handles mouse-leave event."""
        
        # cancel actions
        self._cancel_evt(evt)
    
    
    def on_mouse_dclick(self, evt):
        """Handles mouse-double-click event."""
        
        # reset axis
        self._reset_axis(evt)
    
    
    def on_touch_start(self, evt):
        """Handles touch-start event."""
        
        # skip if active
        if self._is_measure or self._is_rotate:
            return
        
        # get position
        x, y = evt.x_pos, evt.y_pos
        length = pero.distance(self._center, (x, y))
        
        # start measure
        if length <= self._radius:
            self._is_measure = True
        
        # start rotate
        else:
            self._is_rotate = True
            self._offset = evt.control.graphics.get_offset()
        
        # remember dragging
        self._dragging = (x, y)
        
        # draw current cursor
        if self._is_measure:
            evt.control.draw_overlay(self._draw_position, evt=evt, x=x, y=y)
    
    
    def on_touch_end(self, evt):
        """Handles touch-end event."""
        
        # cancel actions
        self._cancel_evt(evt)
    
    
    def on_touch_move(self, evt):
        """Handles touch-move event."""
        
        # skip if inactive
        if not self._is_measure and not self._is_rotate:
            return
        
        # get position
        x, y = evt.x_pos, evt.y_pos
        
        # measure angle
        if self._is_measure:
            evt.control.draw_overlay(self._draw_wedge, evt=evt, x=x, y=y)
        
        # rotate axis
        elif self._is_rotate:
            self._rotate_axis(evt, x, y)
        
        # clear overlay
        else:
            evt.control.clear_overlay()
    
    
    def on_touch_cancel(self, evt):
        """Handles touch-cancel event."""
        
        # cancel actions
        self._cancel_evt(evt)
    
    
    def on_touch_dtap(self, evt):
        """Handles touch-double-tap event."""
        
        # reset axis
        self._reset_axis(evt)
    
    
    def _set_cursor(self, evt, x, y):
        """Sets cursor according to state and position."""
        
        # init cursor
        cursor = pero.CURSOR_ARROW
        
        # get position
        length = pero.distance(self._center, (x, y))
        
        # use direction arrows for axis rotation
        if self._is_rotate or length > self._radius:
            
            # get angle
            cx, cy = self._center
            rads = pero.angle((cx + 1, cy), (cx, cy), (x, y))
            if rads < 0:
                rads += 2*math.pi
            
            # set cursor
            if rads <= pero.rads(45):
                cursor = pero.CURSOR_SIZENS
            elif rads <= pero.rads(135):
                cursor = pero.CURSOR_SIZEWE
            elif rads <= pero.rads(225):
                cursor = pero.CURSOR_SIZENS
            elif rads <= pero.rads(315):
                cursor = pero.CURSOR_SIZEWE
            else:
                cursor = pero.CURSOR_SIZENS
        
        # set cursor
        evt.control.set_cursor(cursor)
    
    
    def _cancel_evt(self, evt):
        """Cancels all current event."""
        
        # cancel actions
        self._is_measure = False
        self._is_rotate = False
        
        # clear overlay
        evt.control.clear_overlay()
    
    
    def _rotate_axis(self, evt, x, y):
        """Rotates main axis."""
        
        # get angle
        cx, cy = self._center
        rads = pero.angle(self._dragging, (cx, cy), (x, y)) + self._offset
        
        # shift axis
        evt.control.graphics.set_offset(rads)
        
        # redraw graphics
        evt.control.refresh()
        
        # draw tooltip
        if not evt.shift_down:
            
            # get total offset
            rads = evt.control.graphics.get_offset()
            if rads < 0:
                rads += 2*math.pi
            
            # draw tooltip
            tooltip = "Degs: %.0f\nRads: %.2f" % (pero.degs(rads), rads)
            evt.control.draw_tooltip(x=x, y=y, text=tooltip)
    
    
    def _reset_axis(self, evt):
        """Resets main axis."""
        
        # reset offset
        self._offset = 0
        
        # shift axis
        evt.control.graphics.set_offset(0)
        
        # redraw graphics
        evt.control.refresh()
    
    
    def _draw_position(self, canvas, evt, x, y):
        """Draws current cursor position."""
        
        # get angle
        cx, cy = self._center
        rads = pero.angle((cx+1, cy), (cx, cy), (x, y))
        incl = pero.inclination((cx, cy), (x, y))
        
        # draw glyphs
        self._arrow.draw(canvas, angle=rads)
        
        # draw tooltip
        if not evt.shift_down:
            
            # adjust angle
            rads = rads - evt.control.graphics.get_offset()
            if rads < 0:
                rads += 2*math.pi
            
            # draw tooltip
            tooltip = "Degs: %.0f\nRads: %.2f\nIncl: %.2f" % (pero.degs(rads), rads, incl)
            evt.control.draw_tooltip(canvas, x=x, y=y, text=tooltip)
    
    
    def _draw_wedge(self, canvas, evt, x, y):
        """Draws current wedge."""
        
        # get angle
        cx, cy = self._center
        rads = pero.angle(self._dragging, (cx, cy), (x, y))
        start_angle = pero.angle((cx+1, cy), (cx, cy), self._dragging)
        end_angle = pero.angle((cx+1, cy), (cx, cy), (x, y))
        
        # get direction
        if evt.alt_down:
            clockwise = False
            if rads > 0:
                rads -= 2*math.pi
        else:
            clockwise = True
            if rads < 0:
                rads += 2*math.pi
        
        # draw glyphs
        self._wedge.draw(canvas,
            start_angle = start_angle,
            end_angle = end_angle,
            clockwise = clockwise,
            fill_color = self._gradient.color_at(abs(rads)/(2*math.pi)))
        
        self._arrow.draw(canvas, angle=start_angle)
        self._arrow.draw(canvas, angle=end_angle)
        
        # draw tooltip
        if not evt.shift_down:
            tooltip = "Degs: %.0f\nRads: %.2f" % (pero.degs(rads), rads)
            evt.control.draw_tooltip(canvas, x=x, y=y, text=tooltip)


class DrawTest(pero.Graphics):
    """Test case for interactive tool."""
    
    
    def __init__(self):
        """Initializes a new instance of DrawTest."""
        
        super().__init__()
        
        # set values
        self._offset = 0
        self._major_ticks = []
        self._minor_ticks = []
        
        # calc ticks
        self.set_offset(self._offset)
        
        # init glyphs
        self._axis = pero.RadialAxis(
            units = pero.DEG,
            labels = [str(i) for i in range(0, 360, 30)],
            label_rotation = pero.TEXT_ROT_NATURAL,
            start_angle = pero.rads(0),
            end_angle = pero.rads(360))
        
        self._ray_grid = pero.RayGrid(
            line_color = pero.colors.LightGrey,
            units = pero.ANGLE_DEG)
        
        self._rad_grid = pero.RadialGrid(
            line_color = pero.colors.LightGrey)
        
        self._bgr = pero.Circle(
            line_width = 0,
            fill_color = pero.colors.White)
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.Black.lighter(.9))
        
        # get coords
        margin = 30
        w, h = canvas.viewport.wh
        cx, cy = canvas.viewport.center
        radius = min(w, h)/2 - margin
        
        # make radial ticks
        count = 5
        step = radius/count
        rad_ticks = [i*step for i in range(1, count+1)]
        
        # draw glyphs
        self._bgr.draw(canvas,
            x = cx,
            y = cy,
            size = radius*2)
        
        self._ray_grid.draw(canvas,
            x = cx,
            y = cy,
            length = radius,
            ticks = self._major_ticks)
        
        self._rad_grid.draw(canvas,
            x = cx,
            y = cy,
            ticks = rad_ticks)
        
        self._axis.draw(canvas,
            x = cx,
            y = cy,
            radius = radius,
            major_ticks = self._major_ticks,
            minor_ticks = self._minor_ticks)
    
    
    def get_offset(self, angle=0):
        """Gets current angle offset in radians."""
        
        return self._offset
    
    
    def set_offset(self, angle=0):
        """Sets current angle offset in radians."""
        
        # set offset
        self._offset = angle
        
        # calc ticks
        offset = pero.degs(angle)
        self._major_ticks = [i+offset for i in range(0, 360, 30)]
        self._minor_ticks = [i+offset for i in range(0, 360, 10)]


# run test
if __name__ == '__main__':
    
    control = pero.Control(
        graphics = DrawTest(),
        main_tool = AngleTool())
    
    pero.debug(control, 'show', "Overlay Tool", 300, 300)
