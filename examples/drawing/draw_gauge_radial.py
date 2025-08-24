#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for radial gauge drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init coords
        padding = 30
        spacing = 15
        bars = 5
        width, height = canvas.viewport.wh
        size = (height - 3 * padding)
        thickness = 0.5 * size/bars - spacing
        
        # init gauge
        gauge = pero.RadialGauge(
            bgr_line_color = "#00a7",
            bgr_fill_color = "#00a3",
            for_line_color = "#00fb",
            for_fill_color = "#00f6",
            start_angle = 90,
            start_angle_units = pero.ANGLE_DEG,
            end_angle = 0,
            end_angle_units = pero.ANGLE_DEG,
            caped = True)
        
        gauge.x = padding+0.5*size
        gauge.y = padding+0.5*size
        
        r1 = spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=0)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=.07)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=1)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0.25, end=0.5)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0.25, end=0.5, reverse=True)
        
        gauge.x = gauge.x + padding
        gauge.y = gauge.y + padding
        gauge.clockwise = False
        
        r1 = spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=0)
        
        r1 = r2 + spacing
        r2 = r1 + thickness
        gauge.draw(canvas, inner_radius=r1, outer_radius=r2, start=0, end=.2)
        
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
    pero.debug(DrawTest(), 'show', "Radial Gauge", 500, 500)
