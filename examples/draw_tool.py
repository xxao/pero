#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
import pero

class AngleTool(pero.Tool):
    """A simple angle tool."""
    
    
    def __init__(self, **overrides):
        
        super(AngleTool, self).__init__(**overrides)
        
        # init buffers
        self._center = (0, 0)
        self._radius = 0
        self._is_active = False
        self._dragging = None
        
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
        
        # get coords
        margin = 30
        cx = evt.width/2
        cy = evt.height/2
        length = min(evt.width, evt.height)/2 - margin
        
        # update buffers
        self._center = (cx, cy)
        self._radius = length
        
        # update glyphs
        self._arrow(
            x = cx,
            y = cy,
            length = length)
        
        self._wedge(
            x = cx,
            y = cy,
            outer_radius = length)
    
    
    def on_mouse_leave(self, evt):
        """Handles mouse-leave event."""
        
        # cancel action and clear overlay
        self._is_active = False
        evt.control.draw_overlay()
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        # get coords
        x, y = evt.x_pos, evt.y_pos
        length = pero.distance(self._center, (x, y))
        
        # draw current wedge
        if self._is_active:
            evt.control.draw_overlay(self._draw_angle, evt=evt)
        
        # draw current cursor
        elif length <= self._radius:
            evt.control.draw_overlay(self._draw_position, evt=evt)
        
        # clear overlay
        else:
            evt.control.draw_overlay()
    
    
    def on_mouse_down(self, evt):
        """Handles mouse-button-down event."""
        
        # skip if active
        if self._is_active:
            return
        
        # get coords
        x, y = evt.x_pos, evt.y_pos
        length = pero.distance(self._center, (x, y))
        
        # skip if outside
        if length > self._radius:
            return
        
        # set active
        self._is_active = True
        
        # remember dragging
        self._dragging = (x, y)
    
    
    def on_mouse_up(self, evt):
        """Handles mouse-button-up event."""
        
        # cancel action and clear overlay
        self._is_active = False
        evt.control.draw_overlay()
    
    
    def _draw_position(self, canvas, evt):
        """Draws current cursor position."""
        
        # get coords
        x, y = evt.x_pos, evt.y_pos
        cx, cy = self._center
        
        # get angle
        rads = pero.angle((cx+1, cy), (cx, cy), (x, y))
        if rads < 0:
            rads += 2*math.pi
        
        # draw glyphs
        self._arrow.draw(canvas, angle=rads)
        
        # draw tooltip
        tooltip = "Degs: %.0f\nRads: %.2f" % (pero.degs(rads), rads)
        evt.control.draw_tooltip(canvas, x=x, y=y, text=tooltip)
    
    
    def _draw_angle(self, canvas, evt):
        """Draws current angle."""
        
        # get coords
        x, y = evt.x_pos, evt.y_pos
        cx, cy = self._center
        
        # get angle
        rads = pero.angle(self._dragging, (cx, cy), (x, y))
        start_angle = pero.angle((cx+1, cy), (cx, cy), self._dragging)
        end_angle = pero.angle((cx+1, cy), (cx, cy), (x, y))
        
        # get direction
        if evt.right_down:
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
        tooltip = "Degs: %.0f\nRads: %.2f" % (pero.degs(rads), rads)
        evt.control.draw_tooltip(canvas, x=x, y=y, text=tooltip)


class DrawTest(pero.Graphics):
    """Test case for interactive tool."""
    
    
    def __init__(self):
        """Initializes a new instance of DrawTest."""
        
        super(DrawTest, self).__init__()
        
        # init glyphs
        self._axis = pero.RadialAxis(
            units = pero.DEG,
            labels = [str(i) for i in range(0, 360, 30)],
            label_rotation = pero.NATURAL,
            major_ticks = [i for i in range(0, 360, 30)],
            minor_ticks = [i for i in range(0, 360, 10)],
            start_angle = pero.rads(0),
            end_angle = pero.rads(360))
        
        self._ray_grid = pero.RayGrid(
            line_color = pero.colors.LightGrey,
            ticks = tuple(range(0, 360, 30)),
            units = pero.DEG)
        
        self._rad_grid = pero.RadialGrid(
            line_color = pero.colors.LightGrey)
        
        self._bgr = pero.Circle(
            line_width = 0,
            fill_color = pero.colors.White)
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill_color = pero.colors.Black.lighter(.9)
        canvas.fill()
        
        # get coords
        margin = 30
        w, h = canvas.viewport.wh
        cx, cy = canvas.viewport.center
        radius = min(w, h)/2 - margin
        
        # make radial ticks
        count = 5
        step = radius/count
        ticks = [i*step for i in range(1, count+1)]
        
        # draw glyphs
        self._bgr.draw(canvas,
            x = cx,
            y = cy,
            size = radius*2)
        
        self._ray_grid.draw(canvas,
            x = cx,
            y = cy,
            length = radius)
        
        self._rad_grid.draw(canvas,
            x = cx,
            y = cy,
            ticks = ticks)
        
        self._axis.draw(canvas,
            x = cx,
            y = cy,
            radius = radius)


# run test
if __name__ == '__main__':
    
    control = pero.Control(
        graphics = DrawTest(),
        main_tool = AngleTool())
    
    pero.debug(control, 'show', "Overlay Tool", 300, 300)
