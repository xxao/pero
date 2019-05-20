#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for radial gauge drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init coords
        padding = 30
        spacing = 10
        bars = 4
        width, height = canvas.viewport.wh
        size = min(0.5*(width - 3*padding), height - 2*padding)
        thickness = 0.5*size/bars - spacing
        
        # init gauge
        gauge = pero.RadialGauge(
            bgr_line_color = "#00a7",
            bgr_fill_color = "#00a3",
            for_line_color = "#00fb",
            for_fill_color = "#00f6",
            start_angle = 90,
            start_angle_units=pero.DEG,
            end_angle = 0,
            end_angle_units=pero.DEG)
        
        gauge.x = padding+0.5*size
        gauge.y = padding+0.5*size
        
        r1 = spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=0)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=1)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0.25, end=0.5)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0.25, end=0.5, reverse=True)
        
        gauge.x = gauge.x + size+padding
        gauge.clockwise = False
        
        r1 = spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=0)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=1)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0.25, end=0.5)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0.25, end=0.5, reverse=True)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Radial Gauge", 450, 250)
