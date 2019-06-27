#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for manually assembled pie chart drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # prepare series
        data = [10, 25, 15, 30, 5, 10, 5]
        total = float(sum(data))
        
        # init glyphs
        wedge = pero.Wedge(
            line_color = "white",
            line_width = 5,
            start_angle_units = pero.DEG,
            end_angle_units = pero.DEG,)
        
        label = pero.Text(
            text_align = pero.CENTER,
            text_base = pero.MIDDLE,
            text_color = "white",
            font_size = 16,
            font_weight = pero.BOLD)
        
        # calc coordinates
        padding = 15
        width, height = canvas.viewport.wh
        
        wedge.x = 0.5*width
        wedge.y = 0.5*height
        wedge.outer_radius = 0.5*(min(width, height) - 2*padding)
        wedge.inner_radius = 0.5*wedge.outer_radius
        
        label_c = (wedge.x, wedge.y)
        label_x = wedge.x + 0.5*(wedge.outer_radius + wedge.inner_radius)
        label_y = wedge.y
        
        # draw slices
        start_angle = -90
        for i, value in enumerate(data):
            
            # calc angle
            wedge.start_angle = start_angle
            wedge.end_angle = start_angle + 360*value/total
            start_angle = wedge.end_angle
            
            # set color
            wedge.fill_color = pero.colors.Pero[i]
            
            # draw glyph
            wedge.draw(canvas)
            
            # draw label
            label_angle = wedge.start_angle + 0.5*(wedge.end_angle - wedge.start_angle)
            x, y = pero.rotate((label_x, label_y), pero.rads(label_angle), label_c)
            label.draw(canvas, text=str(value), x=x, y=y)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Pie Chart", 500, 400)
