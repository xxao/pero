#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for profile drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # calc coordinates
        width, height = canvas.viewport.wh
        padding = 30
        size = (height - padding) / 4
        x = padding
        y = padding
        
        # init data
        x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y_data = [5, 2, 7, 3, 9, 2, 8, 6, 1, 10]
        
        # init scales
        x_scale = pero.LinScale()
        x_scale.in_range = (x_data[0], x_data[-1])
        x_scale.out_range = (padding, width-padding)
        
        y_scale = pero.LinScale()
        y_scale.in_range = (-1, 11)
        y_scale.out_range = (y+size-padding, y)
        
        # init label
        label = pero.Text()
        
        # init glyph
        glyph = pero.Profile(
            show_line = True,
            show_points = True,
            show_area = True,
            line_color = pero.colors.Blue,
            fill_color = pero.colors.Blue.lighter(0.7),
            marker_size = 8,
            marker_line_color = pero.colors.White,
            marker_fill_color = pero.colors.Blue)
        
        # draw line
        label.draw(canvas, x=x, y=y, text="None")
        
        glyph.draw(canvas,
            steps = pero.NONE,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            base = y_scale.scale(0))
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw steps before
        label.draw(canvas, x=x, y=y, text="Before")
        
        glyph.draw(canvas,
            steps = pero.BEFORE,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            base = y_scale.scale(0))
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw steps after
        label.draw(canvas, x=x, y=y, text="After")
        
        glyph.draw(canvas,
            steps = pero.AFTER,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            base = y_scale.scale(0))
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw steps middle
        label.draw(canvas, x=x, y=y, text="Middle")
        
        glyph.draw(canvas,
            steps = pero.MIDDLE,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            base = y_scale.scale(0))


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Profile Steps", 400, 400)
