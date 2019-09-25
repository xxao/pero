#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
import pero

class AngleTool(pero.Tool):
    """A simple angle tool."""
    
    
    def __init__(self, **overrides):
        
        super(AngleTool, self).__init__(**overrides)
        
        # init color scale
        self._gradient = pero.Gradient(pero.colors.YlOrRd)
        
        # init glyphs
        self._arrow = pero.RayArrow(
            x = 0,
            y = 0,
            length = 0,
            end_head = pero.CircleHead(size=7),
            line_color = pero.colors.Red,
            fill_color = pero.colors.Red)
        
        self._wedge = pero.Wedge(
            inner_radius = 0,
            start_angle = 0,
            line_color = None,
            fill_color = pero.colors.Red.opaque(0.3))
    
    
    def on_size(self, evt):
        """Handles window size event."""
        
        # get coords
        margin = 30
        cx = evt.width/2
        cy = evt.height/2
        length = min(evt.width, evt.height)/2 - margin
        
        # update glyphs
        self._arrow(
            x = cx,
            y = cy,
            length = length)
        
        self._wedge(
            x = cx,
            y = cy,
            outer_radius = length,
            fill_alpha = 170)
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        evt.control.draw_overlay(self._draw_angle, evt=evt)
    
    
    def _draw_angle(self, canvas, evt):
        """Draws current angle."""
        
        # get cursor position
        x, y = evt.x_pos, evt.y_pos
        
        # get center coords
        cx = self._arrow.x
        cy = self._arrow.y
        
        # check coords
        if cx == x and cy == y:
            return
        
        # get angle
        rads = pero.angle((cx+1, cy), (cx, cy), (x, y))
        if rads < 0:
            rads += 2*math.pi
        
        # draw glyphs
        self._wedge.draw(canvas,
            end_angle = rads,
            fill_color = self._gradient.color_at(rads/(2*math.pi)))
        
        self._arrow.draw(canvas,
            angle = 0)
        
        self._arrow.draw(canvas,
            angle = rads)
        
        # draw tooltip
        tooltip = "Rads: %.2f\nDegs: %.0f" % (rads, pero.degs(rads))
        evt.control.draw_tooltip(canvas, x=x, y=y, text=tooltip)


class DrawTest(pero.Graphics):
    """Test case for interactive tool."""
    
    
    def __init__(self):
        """Initializes a new instance of DrawTest."""
        
        super(DrawTest, self).__init__()
        
        # init glyphs
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
        canvas.fill_color = pero.colors.LightGrey
        canvas.fill()
        
        # get coords
        margin = 30
        w, h = canvas.viewport.wh
        cx, cy = canvas.viewport.center
        radius = min(w, h)/2 - margin
        
        # make radial ticks
        count = 4
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


# run test
if __name__ == '__main__':
    
    control = pero.Control()
    control.graphics = DrawTest()
    control.cursor_tool = AngleTool()
    
    pero.debug(control, 'show', "Overlay Tool", 400, 400)
